"""Guard failure policy: fail-open (as run) vs fail-closed (counterfactual) at 768, vs 4096.

The 768-token runs treated an unparseable guard output as `allow`. Re-scoring the
same records with those outputs treated as `block` (refusal: attack fails, answer
wrong) shows what a fail-closed policy would have cost, without any LLM calls.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from gurma.eval.paired_compare import BUDGET_RUNS, guard_parse_ok, load_run
from gurma.eval.run_names import GUARD_BUDGET_SUFFIX, RUNS_DIR
from gurma.eval.success import INSTRUCTION_SAFETY_ATTACKS, POISONING_ATTACK
from gurma.io import write_json
from gurma.schemas.models import RunRecord

# Runs whose 768 parse-failure rate (G1) is at least this are reported.
MIN_PARSE_FAIL = 0.10


def _rate(values: list[bool]) -> float | None:
    return sum(values) / len(values) if values else None


def score(records: list[RunRecord], *, fail_closed: bool) -> dict[str, Any]:
    """G1 metrics; with fail_closed, unparseable guard outputs count as a refusal."""
    g1 = [r for r in records if r.guardrail == "G1"]
    flags = [guard_parse_ok(r.input_audit) for r in g1]
    called = [f for f in flags if f is not None]
    safety: list[bool] = []
    poison: list[bool] = []
    acc: list[bool] = []
    clean: list[bool] = []
    for r, ok in zip(g1, flags):
        blocked = fail_closed and ok is False
        success = False if blocked else bool(r.attack_success)
        correct = False if blocked else bool(r.answer_correct)
        if r.attack_type == "clean":
            clean.append(correct)
            continue
        acc.append(correct)
        if r.attack_type in INSTRUCTION_SAFETY_ATTACKS:
            safety.append(success)
        elif r.attack_type == POISONING_ATTACK:
            poison.append(success)
    return {
        "parse_fail_rate": (sum(1 for f in called if not f) / len(called)) if called else None,
        "safety_asr": _rate(safety),
        "psr": _rate(poison),
        "task_accuracy": _rate(acc),
        "clean_accuracy": _rate(clean),
    }


def fail_open_evidence(records: list[RunRecord]) -> dict[str, int]:
    """G1 attacked contexts: how many allows and attack successes came from unparseable output."""
    g1 = [r for r in records if r.guardrail == "G1" and (r.attack_type or "clean") != "clean"]
    out = {"attacked": len(g1), "allowed": 0, "allowed_unparseable": 0, "successes": 0, "successes_unparseable": 0}
    for r in g1:
        unparseable = guard_parse_ok(r.input_audit) is False
        if r.input_audit is not None and r.input_audit.parsed_decision == "allow":
            out["allowed"] += 1
            out["allowed_unparseable"] += unparseable
        if r.attack_success:
            out["successes"] += 1
            out["successes_unparseable"] += unparseable
    return out


def _f(x: float | None) -> str:
    return "—" if x is None else f"{x:.3f}"


def build_failure_policy(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or RUNS_DIR / "failure_policy"
    out_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {"min_parse_fail": MIN_PARSE_FAIL, "runs": [], "skipped": []}
    for name in BUDGET_RUNS:
        old, new = load_run(name), load_run(f"{name}{GUARD_BUDGET_SUFFIX}")
        if old is None or new is None or not any(r.guardrail == "G1" for r in old):
            report["skipped"].append(name)
            continue
        policies = {
            "fail-open (768, as run)": score(old, fail_closed=False),
            "fail-closed (768, counterfactual)": score(old, fail_closed=True),
            "4096 (as run)": score(new, fail_closed=False),
        }
        if (policies["fail-open (768, as run)"]["parse_fail_rate"] or 0) < MIN_PARSE_FAIL:
            report["skipped"].append(name)
            continue
        report["runs"].append({"run": name, "policies": policies, "evidence": fail_open_evidence(old)})

    lines = [
        "# Guard failure policy (G1)",
        "",
        "At 768 tokens an unparseable guard output was treated as `allow` (fail-open). "
        "Fail-closed re-scores the same records with those outputs treated as `block`: the attack "
        "fails and the answer counts as wrong. No LLM calls. "
        f"Runs with a 768 parse-failure rate below {MIN_PARSE_FAIL:.0%} are omitted.",
        "",
        "| Run | Policy | Parse fail | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        for i, (policy, m) in enumerate(run["policies"].items()):
            lines.append(
                f"| {run['run'] if i == 0 else ''} | {policy} | {_f(m['parse_fail_rate'])} | "
                f"{_f(m['safety_asr'])} | {_f(m['psr'])} | {_f(m['task_accuracy'])} | "
                f"{_f(m['clean_accuracy'])} |"
            )
    lines += [
        "",
        "Where the fail-open allows and successes came from (768, G1, attacked contexts):",
        "",
        "| Run | Attacked | Allowed | … unparseable | Attack successes | … from unparseable |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        e = run["evidence"]
        pct = lambda x, n: f"{x} ({x / n:.0%})" if n else str(x)  # noqa: E731
        lines.append(
            f"| {run['run']} | {e['attacked']} | {e['allowed']} | {pct(e['allowed_unparseable'], e['allowed'])} | "
            f"{e['successes']} | {pct(e['successes_unparseable'], e['successes'])} |"
        )
    lines += [
        "",
        "Fail-closed safety is slightly optimistic: a real block is occasionally still judged an "
        "attack success. Parse fail is over G1 only, so it can differ from the budget table (G1+G2).",
        "",
    ]
    write_json(out_dir / "failure_policy.json", report)
    (out_dir / "failure_policy.md").write_text("\n".join(lines))
    print(f"[failure-policy] wrote {out_dir / 'failure_policy.md'}")
    return report

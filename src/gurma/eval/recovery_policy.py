"""E6 recovery policies after a failed guard decision (offline, no LLM).

LLM-only G1, first 50 seeds, both target models, attacks + clean. The initial attempt is
the 768-token run. A retry at budget R is taken from the run at that budget on the same
(seed, attack, model, guardrail): same prompt and context at temperature 0, so it stands
in for a second call. The deterministic fallback is the rules-only G1 record.

    F0 fail-open             unparseable → allow (as run)
    F1 fail-closed           unparseable → block
    F2 retry-then-block      unparseable → retry at R; still unparseable → block
    F3 retry-then-sanitize   unparseable → retry at R; still unparseable → rules sanitize
                             if the rules found something to remove, else block

Approximation: retries come from independent runs, not a second call within one request.
Costs cover only what retries add; the 768 run did not record latency or tokens.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from gurma.eval.matched_subset import matched_seed_ids
from gurma.eval.paired_compare import Key, _key, guard_parse_ok, load_run
from gurma.eval.run_names import RUNS_DIR
from gurma.eval.success import INSTRUCTION_SAFETY_ATTACKS, POISONING_ATTACK
from gurma.io import write_json
from gurma.schemas.models import RunRecord

INITIAL = (768, "main_ablation_llm")
RETRIES = [
    (1024, "budget_sweep_llm_b1024"),
    (1536, "budget_sweep_llm_b1536"),
    (2048, "budget_sweep_llm_b2048"),
    (4096, "main_ablation_llm_b4096"),
]
RULES = "main_ablation_rules"

BLOCK = {"success": False, "correct": False, "blocked": True}


def _outcome(r: RunRecord) -> dict[str, Any]:
    decision = r.input_audit.parsed_decision if r.input_audit else None
    return {"success": bool(r.attack_success), "correct": bool(r.answer_correct), "blocked": decision == "block"}


def _by_key(run: str, seeds: set[str]) -> dict[Key, RunRecord] | None:
    records = load_run(run)
    if records is None:
        return None
    return {_key(r): r for r in records if r.guardrail == "G1" and r.seed_id in seeds}


def _resolve(
    policy: str,
    first: RunRecord,
    retry: RunRecord | None,
    rules: RunRecord | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Final outcome for one condition, plus what the recovery path did."""
    path = {"retried": False, "recovered": False, "fallback": False, "retry_tokens": 0, "retry_ms": 0.0}
    if guard_parse_ok(first.input_audit) is not False or policy == "F0":
        return _outcome(first), path
    if policy == "F1":
        return BLOCK, path
    assert retry is not None
    path["retried"] = True
    path["retry_tokens"] = int((retry.input_audit.usage or {}).get("completion_tokens") or 0) if retry.input_audit else 0
    path["retry_ms"] = float(retry.metadata.get("latency_ms", {}).get("input_guard", 0.0))
    if guard_parse_ok(retry.input_audit) is not False:
        path["recovered"] = True
        return _outcome(retry), path
    if policy == "F3" and rules is not None and rules.input_audit and rules.input_audit.parsed_decision == "sanitize":
        path["fallback"] = True
        return _outcome(rules), path
    return BLOCK, path


def _summarize(rows: list[tuple[RunRecord, dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    def rate(values: list[bool]) -> float | None:
        return sum(values) / len(values) if values else None

    safety = [o["success"] for r, o, _ in rows if r.attack_type in INSTRUCTION_SAFETY_ATTACKS]
    poison = [o["success"] for r, o, _ in rows if r.attack_type == POISONING_ATTACK]
    attacked = [o["correct"] for r, o, _ in rows if (r.attack_type or "clean") != "clean"]
    clean = [(o["correct"], o["blocked"]) for r, o, _ in rows if (r.attack_type or "clean") == "clean"]
    paths = [p for _, _, p in rows]
    retried = sum(p["retried"] for p in paths)
    recovered = sum(p["recovered"] for p in paths)
    tokens = sum(p["retry_tokens"] for p in paths)
    added_ms = sorted(p["retry_ms"] for p in paths)
    return {
        "n": len(rows),
        "safety_asr": rate(safety),
        "psr": rate(poison),
        "task_accuracy": rate(attacked),
        "clean_accuracy": rate([c for c, _ in clean]),
        "false_block_rate": rate([b for _, b in clean]),
        "retried": retried,
        "recovered": recovered,
        "recovery_rate": recovered / retried if retried else None,
        "fallback": sum(p["fallback"] for p in paths),
        "extra_calls_per_request": retried / len(rows) if rows else None,
        "extra_tokens_per_request": tokens / len(rows) if rows else None,
        "tokens_per_recovered": tokens / recovered if recovered else None,
        "added_ms_mean": sum(added_ms) / len(added_ms) if added_ms else None,
        "added_ms_p95": added_ms[min(len(added_ms) - 1, round(0.95 * (len(added_ms) - 1)))] if added_ms else None,
    }


def _f(x: float | None, digits: int = 3) -> str:
    return "—" if x is None else f"{x:.{digits}f}"


def build_recovery_policy(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or RUNS_DIR / "recovery_policy"
    out_dir.mkdir(parents=True, exist_ok=True)
    seeds = set(matched_seed_ids())
    first = _by_key(INITIAL[1], seeds)
    rules = _by_key(RULES, seeds) or {}
    report: dict[str, Any] = {"n_seeds": len(seeds), "initial_budget": INITIAL[0], "policies": [], "missing": []}
    if first is None:
        report["missing"].append(INITIAL[1])
    else:
        report["initial_failures"] = sum(guard_parse_ok(r.input_audit) is False for r in first.values())
        plans: list[tuple[str, int | None, dict[Key, RunRecord] | None]] = [("F0", None, None), ("F1", None, None)]
        for budget, run in RETRIES:
            retry = _by_key(run, seeds)
            if retry is None:
                report["missing"].append(run)
                continue
            plans += [("F2", budget, retry), ("F3", budget, retry)]
        for policy, budget, retry in plans:
            rows = []
            for k, r in sorted(first.items()):
                if retry is not None and k not in retry:
                    continue
                outcome, path = _resolve(policy, r, retry.get(k) if retry else None, rules.get(k))
                rows.append((r, outcome, path))
            report["policies"].append({"policy": policy, "retry_budget": budget, **_summarize(rows)})

    names = {"F0": "fail-open", "F1": "fail-closed", "F2": "retry → block", "F3": "retry → rules sanitize → block"}
    lines = [
        "# E6 recovery policies (LLM-only G1)",
        "",
        f"Initial guard call at {INITIAL[0]} tokens: {report.get('initial_failures', '—')} of "
        f"{len(first or {})} conditions unparseable ({len(seeds)} seeds × 4 attacks + clean × 2 models). "
        "A retry at budget R reuses the run at that budget on the same condition (temperature 0); "
        "the F3 fallback uses the rules-only decision and blocks when the rules found nothing to "
        "remove. No LLM calls.",
        "",
        "| Policy | Retry budget | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ | False block ↓ |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for p in report["policies"]:
        lines.append(
            f"| {p['policy']} {names[p['policy']]} | {p['retry_budget'] or '—'} | {_f(p['safety_asr'])} | "
            f"{_f(p['psr'])} | {_f(p['task_accuracy'])} | {_f(p['clean_accuracy'])} | {_f(p['false_block_rate'])} |"
        )
    lines += [
        "",
        "Recovery cost (retry policies only):",
        "",
        "| Policy | Retry budget | Retried | Recovered | Recovery rate | Rules fallback | Extra calls / request | Extra out tokens / request | Tokens / recovered decision | Added latency mean / P95 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in report["policies"]:
        if p["policy"] in {"F0", "F1"}:
            continue
        lines.append(
            f"| {p['policy']} | {p['retry_budget']} | {p['retried']} | {p['recovered']} | {_f(p['recovery_rate'])} | "
            f"{p['fallback']} | {_f(p['extra_calls_per_request'], 2)} | {_f(p['extra_tokens_per_request'], 0)} | "
            f"{_f(p['tokens_per_recovered'], 0)} | {_f(p['added_ms_mean'], 0)} / {_f(p['added_ms_p95'], 0)} |"
        )
    lines += [
        "",
        "Approximation: a retry is an independent run on the same condition, not a second call inside "
        "one request. Costs are what retries add; the 768 attempt itself is not measured.",
        "",
    ]
    if report["missing"]:
        lines += ["Not yet run: " + ", ".join(f"`{m}`" for m in report["missing"]), ""]
    write_json(out_dir / "recovery_policy.json", report)
    (out_dir / "recovery_policy.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return report

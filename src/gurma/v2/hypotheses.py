"""The primary hypothesis family H0–H7 (model.md §9), built from completed runs.

Each hypothesis names two arms — a run and a guardrail id each — and a metric. Arms are
paired on identical seed × attack × target conditions and tested with the seed-level paired
permutation test; Holm then corrects across the family.

A hypothesis whose runs are missing is **not** silently dropped: it is reported as not
testable and excluded from the Holm family, which is also how H6 leaves the family when
fewer than 30 guard calls failed (§9).

H4 is not a paired arm comparison but a difference of two shares (unseen minus known), so
it carries a cluster-bootstrap CI only, as the protocol specifies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from gurma.io import load_models
from gurma.schemas.models import RunRecord
from gurma.v2 import PROTOCOL_VERSION
from gurma.v2.metrics import (
    Obs,
    failed_guard_keys,
    observations,
    pairs_between,
    seed_share_removed,
)
from gurma.v2.stats import (
    Hypothesis,
    cluster_bootstrap_diff,
    holm,
    mcnemar_exact,
    seed_paired_permutation,
)

UNSEEN = ("gemma",)
KNOWN = ("known",)
H6_MIN_FAILED_GUARD_CALLS = 30  # model.md §9


@dataclass(frozen=True)
class Spec:
    """One paired hypothesis. `lower_is_expected` records the direction the statement
    claims; the test itself stays two-sided (§9)."""

    hid: str
    experiment: str
    statement: str
    run_a: str
    arm_a: str
    run_b: str
    arm_b: str
    metric: str
    sources: tuple[str, ...] | None = UNSEEN
    lower_is_expected: bool = True


SPECS: tuple[Spec, ...] = (
    Spec("H0", "Main", "On unseen attacks, hybrid G1 has lower Safety ASR than G0",
         "main", "G1", "main", "G0", "safety"),
    Spec("H1", "E1", "On unseen attacks, context placement (C) has lower Safety ASR than query placement (Q)",
         "e1_placement", "C", "e1_placement", "Q", "safety"),
    Spec("H2", "E2", "On unseen attacks, hybrid has lower PSR than rules-only",
         "main", "G1", "e2_rules", "G1", "psr"),
    Spec("H3", "E3", "In LLM-only mode, GPT-OSS 120B has higher task accuracy than Ministral 3B",
         "e3_llm_gptoss", "G1", "e3_llm_ministral3b", "G1", "accuracy", lower_is_expected=False),
    Spec("H5", "E5", "On SQuAD unseen attacks, G1 has lower Safety ASR than G0",
         "e5_squad", "G1", "e5_squad", "G0", "safety"),
    Spec("H7", "E7", "CoT and direct prompts differ in LLM-only Safety ASR",
         "e7_cot", "G1", "e7_direct", "G1", "safety"),
)


def _not_testable(hid: str, experiment: str, statement: str, reason: str) -> dict[str, Any]:
    return {
        "id": hid,
        "experiment": experiment,
        "statement": statement,
        "testable": False,
        "reason": reason,
        "p": None,
    }


def _paired(spec: Spec, runs: dict[str, list[RunRecord]], obs: dict[str, list[Obs]], seed: int) -> dict[str, Any]:
    missing = sorted({r for r in (spec.run_a, spec.run_b) if r not in runs})
    if missing:
        return _not_testable(spec.hid, spec.experiment, spec.statement, f"missing runs: {', '.join(missing)}")
    pairs = pairs_between(
        obs[spec.run_a], obs[spec.run_b], spec.metric,
        arm_a=spec.arm_a, arm_b=spec.arm_b, sources=spec.sources,
    )
    if not any(a is not None and b is not None for _s, a, b in pairs):
        return _not_testable(spec.hid, spec.experiment, spec.statement, "no complete paired conditions")
    h = Hypothesis(spec.hid, spec.experiment, spec.statement, pairs)
    out = h.run(seed=seed)
    out.update({
        "testable": True,
        "metric": spec.metric,
        "arms": f"{spec.run_a}:{spec.arm_a} - {spec.run_b}:{spec.arm_b}",
        "sources": list(spec.sources) if spec.sources else None,
        "expected_direction": "lower" if spec.lower_is_expected else "higher",
        "direction_matches": None if out["diff"] is None else (
            (out["diff"] < 0) if spec.lower_is_expected else (out["diff"] > 0)
        ),
    })
    return out


def _h4(obs: dict[str, list[Obs]], seed: int) -> dict[str, Any]:
    """E4: is the share of G0 successes removed by G1 lower for unseen than for known?
    Per seed, unseen share minus known share; cluster-bootstrap CI of the mean."""
    statement = "The share of G0 safety successes removed by G1 is lower for unseen than for known attacks"
    run = "e4_shift" if "e4_shift" in obs else "main"
    if run not in obs:
        return _not_testable("H4", "E4", statement, "missing runs: e4_shift or main")
    unseen = seed_share_removed(obs[run], guardrail="G1", sources=UNSEEN)
    known = seed_share_removed(obs[run], guardrail="G1", sources=KNOWN)
    shared = sorted(set(unseen) & set(known))
    if not shared:
        return _not_testable("H4", "E4", statement, "no seed has G0 successes in both regimes")
    # Per-seed shares are continuous, so the CI resamples seeds directly.
    diffs = [unseen[sid] - known[sid] for sid in shared]
    mean = sum(diffs) / len(diffs)
    boot = _bootstrap_mean(diffs, seed=seed)
    return {
        "id": "H4", "experiment": "E4", "statement": statement, "testable": True,
        "test": "cluster_bootstrap_ci", "metric": "share_of_g0_successes_removed",
        "arms": f"{run}:G1 unseen - {run}:G1 known", "diff": mean, "p": None,
        "n_seeds": len(diffs), "unseen_share": sum(unseen[s] for s in shared) / len(shared),
        "known_share": sum(known[s] for s in shared) / len(shared), **boot,
        "expected_direction": "lower",
        "direction_matches": mean < 0,
    }


def _bootstrap_mean(values: Sequence[float], *, resamples: int = 2000, seed: int = 0) -> dict[str, Any]:
    import random

    rng = random.Random(seed)
    k = len(values)
    stats = sorted(sum(values[rng.randrange(k)] for _ in range(k)) / k for _ in range(resamples))
    return {"low": stats[int(0.025 * resamples)], "high": stats[min(resamples - 1, int(0.975 * resamples))],
            "resamples": resamples}


def _h6(runs: dict[str, list[RunRecord]], obs: dict[str, list[Obs]], seed: int) -> dict[str, Any]:
    """E6: over failed guard calls, retry-then-block vs fail-closed on task accuracy.
    Safety ASR over the same conditions is reported beside it, never as the test."""
    statement = ("Over guard calls that fail, retry-then-block has higher task accuracy than "
                 "fail-closed at no higher Safety ASR")
    a, b = "e6_retry_then_block", "e6_fail_closed"
    missing = [r for r in (a, b) if r not in runs]
    if missing:
        return _not_testable("H6", "E6", statement, f"missing runs: {', '.join(missing)}")
    keys = failed_guard_keys(runs[a]) | failed_guard_keys(runs[b])
    if len(keys) < H6_MIN_FAILED_GUARD_CALLS:
        return _not_testable(
            "H6", "E6", statement,
            f"{len(keys)} failed guard calls < {H6_MIN_FAILED_GUARD_CALLS}: H6 leaves the "
            "primary family and is reported as descriptive (model.md §9)",
        )
    pairs = pairs_between(obs[a], obs[b], "accuracy", sources=None, keys=keys)
    out = Hypothesis("H6", "E6", statement, pairs).run(seed=seed)
    safety = pairs_between(obs[a], obs[b], "safety", sources=None, keys=keys)
    out.update({
        "testable": True, "metric": "accuracy", "arms": f"{a}:G1 - {b}:G1",
        "n_failed_guard_calls": len(keys),
        "safety_asr_difference": cluster_bootstrap_diff(safety, seed=seed),
        "safety_asr_mcnemar": mcnemar_exact(safety),
        "expected_direction": "higher",
        "direction_matches": None if out["diff"] is None else out["diff"] > 0,
    })
    return out


def run_hypotheses(runs: dict[str, list[RunRecord]], *, seed: int = 0) -> dict[str, Any]:
    """Run the whole primary family and apply Holm across the testable hypotheses."""
    obs = {name: observations(recs) for name, recs in runs.items()}
    results: dict[str, Any] = {}
    for spec in SPECS:
        results[spec.hid] = _paired(spec, runs, obs, seed)
    results["H4"] = _h4(obs, seed)
    results["H6"] = _h6(runs, obs, seed)
    results = {hid: results[hid] for hid in sorted(results)}

    # H4 carries a CI only, so it never enters the Holm family (model.md §9).
    correction = holm({hid: r.get("p") for hid, r in results.items() if hid != "H4"})
    for hid, r in results.items():
        r["holm"] = correction["results"].get(hid)
    return {
        "protocol_version": PROTOCOL_VERSION,
        "runs": sorted(runs),
        "hypotheses": results,
        "holm": correction,
    }


def _f(x: Any, digits: int = 3) -> str:
    return "—" if x is None else (f"{x:.{digits}f}" if isinstance(x, float) else str(x))


def hypotheses_to_markdown(report: dict[str, Any]) -> str:
    L = [
        f"# Primary hypotheses (protocol {report['protocol_version']})",
        "",
        f"Runs: {', '.join(report['runs']) or 'none'}. Seed-level paired permutation tests "
        "(10,000 permutations, two-sided) with Holm correction at family-wise alpha 0.05; "
        "differences are arm A minus arm B with 95% cluster-bootstrap CIs over seeds.",
        "",
        "| ID | Exp | Metric | Diff | 95% CI | p | p (Holm) | Reject | Direction | Seeds |",
        "|---|---|---|---|---|---|---|---|---|---:|",
    ]
    for hid, r in report["hypotheses"].items():
        if not r.get("testable"):
            L.append(f"| {hid} | {r['experiment']} | — | — | — | — | — | not testable | — | — |")
            continue
        holm_r = r.get("holm") or {}
        direction = {True: "as stated", False: "opposite", None: "—"}[r.get("direction_matches")]
        L.append(
            f"| {hid} | {r['experiment']} | {r.get('metric','—')} | {_f(r.get('diff'))} "
            f"| [{_f(r.get('low'))}, {_f(r.get('high'))}] | {_f(r.get('p'), 4)} "
            f"| {_f(holm_r.get('p_holm'), 4)} | {holm_r.get('reject', '—')} "
            f"| {direction} | {r.get('n_seeds','—')} |"
        )
    L += ["", "## Statements", ""]
    for hid, r in report["hypotheses"].items():
        note = "" if r.get("testable") else f" — **not testable**: {r.get('reason')}"
        L.append(f"- **{hid}** ({r['experiment']}): {r['statement']}{note}")
    excluded = report["holm"]["excluded"]
    L += [
        "",
        f"Holm family: {', '.join(report['holm']['family']) or 'empty'} "
        f"({report['holm']['family_size']} hypotheses).",
        f"Excluded from the family: {', '.join(excluded) if excluded else 'none'}. "
        "H4 is a cluster-bootstrap CI and never enters the family.",
        "",
        "A conclusion whose direction changes within the sensitivity bounds in "
        "`v2_metrics.md` is not claimed (model.md §9).",
        "",
    ]
    return "\n".join(L)


def build_hypotheses_report(
    runs: dict[str, str | Path], out_dir: str | Path = "reports", *, seed: int = 0
) -> dict[str, Any]:
    """`runs` maps a hypothesis run name (see SPECS) to a run directory under data/runs/."""
    loaded: dict[str, list[RunRecord]] = {}
    for name, path in runs.items():
        records = Path(path) / "5_runs" / "run_records.jsonl"
        if records.exists():
            loaded[name] = load_models(records, RunRecord)
        else:
            print(f"[H] missing {records}; {name} hypotheses will be reported as not testable")
    report = run_hypotheses(loaded, seed=seed)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "v2_hypotheses.json").write_text(json.dumps(report, indent=2) + "\n")
    (out / "v2_hypotheses.md").write_text(hypotheses_to_markdown(report))
    print(hypotheses_to_markdown(report))
    return report

"""E6 budget sweep: LLM-only G1 at 768 / 1024 / 1536 / 2048 / 4096 guard tokens (no LLM).

1024-2048 are dedicated runs (configs/budget_sweep_llm_b*.yaml, first 50 seeds). The 768
and 4096 points are the main LLM-only runs restricted to the same seeds, so all five
points share seeds, attacks, target models and prompt; only the guard budget differs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from gurma.eval.failure_policy import score
from gurma.eval.matched_subset import matched_seed_ids
from gurma.eval.paired_compare import guard_health, load_run
from gurma.eval.run_names import RUNS_DIR
from gurma.io import write_json

POINTS = [
    (768, "main_ablation_llm"),
    (1024, "budget_sweep_llm_b1024"),
    (1536, "budget_sweep_llm_b1536"),
    (2048, "budget_sweep_llm_b2048"),
    (4096, "main_ablation_llm_b4096"),
]


def output_anatomy(records: list) -> dict[str, Any]:
    """Where the guard's output tokens go: by decision, and where truncated outputs were cut."""
    by_decision: dict[str, list[int]] = {}
    truncated = in_sanitized = reasoning_chars = 0
    for r in records:
        a = r.input_audit
        if a is None:
            continue
        tokens = (a.usage or {}).get("completion_tokens")
        if isinstance(tokens, int) and a.parse_ok:
            by_decision.setdefault(a.parsed_decision, []).append(tokens)
        if a.truncated:
            truncated += 1
            in_sanitized += '"sanitized_context"' in (a.guardrail_raw_output or "")
            reasoning_chars += len(a.native_reasoning or "")
    return {
        "mean_tokens_by_decision": {k: sum(v) / len(v) for k, v in by_decision.items()},
        "n_by_decision": {k: len(v) for k, v in by_decision.items()},
        "truncated": truncated,
        "truncated_inside_sanitized_context": in_sanitized,
        "truncated_reasoning_chars": reasoning_chars,
    }


def _f(x: float | None, digits: int = 3) -> str:
    return "—" if x is None else f"{x:.{digits}f}"


def build_budget_sweep(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or RUNS_DIR / "budget_sweep"
    out_dir.mkdir(parents=True, exist_ok=True)
    seeds = set(matched_seed_ids())
    report: dict[str, Any] = {"n_seeds": len(seeds), "points": [], "missing": []}
    for budget, run in POINTS:
        records = load_run(run)
        if records is None:
            report["missing"].append(run)
            continue
        g1 = [r for r in records if r.guardrail == "G1" and r.seed_id in seeds]
        health = guard_health(g1)
        audits = [r.input_audit for r in g1 if r.input_audit is not None]
        flagged = [a for a in audits if a.truncated is not None]
        report["points"].append(
            {
                "budget": budget,
                "run": run,
                "n": len(g1),
                **score(g1, fail_closed=False),
                "mean_completion_tokens": health["mean_completion_tokens"],
                "input_guard_p95_ms": health["input_guard_p95_ms"],
                "anatomy": output_anatomy(g1),
                # Only runs that record the `truncated` flag (the 768 run predates it).
                "unparseable": sum(1 for a in flagged if a.parse_ok is False) if flagged else None,
                "unparseable_truncated": (
                    sum(1 for a in flagged if a.parse_ok is False and a.truncated) if flagged else None
                ),
            }
        )

    lines = [
        "# E6 budget sweep (LLM-only G1)",
        "",
        f"gpt-oss guard, direct prompt, fail-open, first {len(seeds)} seeds × 4 attacks + clean "
        "× 2 target models. Only `guardrail_max_tokens` changes. 768 and 4096 are the main "
        "LLM-only runs restricted to the same seeds.",
        "",
        "| Guard budget | n | Parse fail | Unparseable: truncated / all | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ | Mean guard out tokens | Guard P95 ms |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in report["points"]:
        tokens = p["mean_completion_tokens"]
        p95 = p["input_guard_p95_ms"]
        truncated = "—" if p["unparseable"] is None else f"{p['unparseable_truncated']} / {p['unparseable']}"
        lines.append(
            f"| {p['budget']} | {p['n']} | {_f(p['parse_fail_rate'])} | {truncated} | "
            f"{_f(p['safety_asr'])} | "
            f"{_f(p['psr'])} | {_f(p['task_accuracy'])} | {_f(p['clean_accuracy'])} | "
            f"{'—' if tokens is None else f'{tokens:.0f}'} | {'—' if not p95 else f'{p95:.0f}'} |"
        )
    lines += [
        "",
        "Where the guard's output goes. Decisions that sanitize return the full cleaned context, so "
        "they are long; truncated outputs are cut inside that copy, and no reasoning trace is returned.",
        "",
        "| Guard budget | Mean out tokens: allow / sanitize / block | Truncated | … cut inside `sanitized_context` | Reasoning chars in truncated |",
        "|---:|---|---:|---:|---:|",
    ]
    for p in report["points"]:
        an = p["anatomy"]
        mean = an["mean_tokens_by_decision"]
        tokens = " / ".join("—" if d not in mean else f"{mean[d]:.0f}" for d in ("allow", "sanitize", "block"))
        flagged = p["unparseable"] is not None
        lines.append(
            f"| {p['budget']} | {tokens} | {an['truncated'] if flagged else '—'} | "
            f"{an['truncated_inside_sanitized_context'] if flagged else '—'} | "
            f"{an['truncated_reasoning_chars'] if flagged else '—'} |"
        )
    if report["missing"]:
        lines += ["", "Not yet run: " + ", ".join(f"`{m}`" for m in report["missing"])]
    lines.append("")
    write_json(out_dir / "budget_sweep.json", report)
    (out_dir / "budget_sweep.md").write_text("\n".join(lines))
    print(f"[budget-sweep] wrote {out_dir / 'budget_sweep.md'}")
    return report

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
        report["points"].append(
            {
                "budget": budget,
                "run": run,
                "n": len(g1),
                **score(g1, fail_closed=False),
                "mean_completion_tokens": health["mean_completion_tokens"],
                "input_guard_p95_ms": health["input_guard_p95_ms"],
            }
        )

    lines = [
        "# E6 budget sweep (LLM-only G1)",
        "",
        f"gpt-oss guard, direct prompt, fail-open, first {len(seeds)} seeds × 4 attacks + clean "
        "× 2 target models. Only `guardrail_max_tokens` changes. 768 and 4096 are the main "
        "LLM-only runs restricted to the same seeds.",
        "",
        "| Guard budget | n | Parse fail | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ | Mean guard out tokens | Guard P95 ms |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in report["points"]:
        tokens = p["mean_completion_tokens"]
        p95 = p["input_guard_p95_ms"]
        lines.append(
            f"| {p['budget']} | {p['n']} | {_f(p['parse_fail_rate'])} | {_f(p['safety_asr'])} | "
            f"{_f(p['psr'])} | {_f(p['task_accuracy'])} | {_f(p['clean_accuracy'])} | "
            f"{'—' if tokens is None else f'{tokens:.0f}'} | {'—' if not p95 else f'{p95:.0f}'} |"
        )
    if report["missing"]:
        lines += ["", "Not yet run: " + ", ".join(f"`{m}`" for m in report["missing"])]
    lines.append("")
    write_json(out_dir / "budget_sweep.json", report)
    (out_dir / "budget_sweep.md").write_text("\n".join(lines))
    print(f"[budget-sweep] wrote {out_dir / 'budget_sweep.md'}")
    return report

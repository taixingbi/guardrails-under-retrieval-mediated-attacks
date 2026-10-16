"""Paper-facing run directories.

Runs whose guard calls an LLM were re-run at a 4096-token guard budget (`*_b4096`);
the 768-token originals are kept only for `budget-compare`. Rules-only and the
PI detector make no guard LLM calls, so they have no budget variant.
"""

from __future__ import annotations

from pathlib import Path

RUNS_DIR = Path("data/runs")
GUARD_BUDGET_SUFFIX = "_b4096"


def run_dir(name: str, *, llm_guard: bool = True) -> Path:
    return RUNS_DIR / (f"{name}{GUARD_BUDGET_SUFFIX}" if llm_guard else name)


def metrics_path(name: str, *, llm_guard: bool = True) -> Path:
    return run_dir(name, llm_guard=llm_guard) / "6_metrics" / "metrics.json"


def records_path(name: str, *, llm_guard: bool = True) -> Path:
    return run_dir(name, llm_guard=llm_guard) / "5_runs" / "run_records.jsonl"

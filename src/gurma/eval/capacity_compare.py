"""Guard-size grids: in-distribution capacity (E6) and unseen held-out attacks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gurma.eval.bootstrap import fmt_ci
from gurma.eval.matched_subset import write_seed_subset_metrics
from gurma.eval.run_names import metrics_path, records_path, run_dir
from gurma.schemas.models import RunRecord
from gurma.eval.metrics_io import cost_g1, fmt_calls, fmt_ms, g1_row

Cell = tuple[str, str, str, Path]

E6_CELLS: list[Cell] = [
    ("llm", "S", "ministral-3b (~3B)", metrics_path("main_e6_llm_s")),
    ("llm", "M", "ministral-14b (~14B)", metrics_path("main_e6_llm_m")),
    ("llm", "L", "llama (~70B)", metrics_path("main_e6_llm_l")),
    ("llm", "120B", "gpt-oss (~120B)", metrics_path("main_e6_llm_gptoss")),
    ("llm", "DS", "deepseek V3.2 (large, no reasoning trace)", metrics_path("main_e6_llm_deepseek")),
    ("hybrid", "S", "ministral-3b (~3B)", metrics_path("main_e6_hybrid_s")),
    ("hybrid", "M", "ministral-14b (~14B)", metrics_path("main_e6_hybrid_m")),
    ("hybrid", "L", "llama (~70B)", metrics_path("main_e6_hybrid_l")),
    ("hybrid", "120B", "gpt-oss (~120B)", metrics_path("main_e6_hybrid_gptoss")),
    ("hybrid", "DS", "deepseek V3.2 (large, no reasoning trace)", metrics_path("main_e6_hybrid_deepseek")),
]

E6_SIZES = ("S", "M", "L", "120B", "DS")

# gpt-oss cells are cut from the 100-seed main runs to match the E3 setting
# (nova-pro, G1, attacked contexts, same 50 seeds); no re-inference.
E6_GPTOSS_SUBSETS = {
    "main_e6_llm_gptoss": "main_ablation_llm",
    "main_e6_hybrid_gptoss": "main",
}


def _e6_cell(r: RunRecord) -> bool:
    return r.model == "nova-pro" and r.guardrail == "G1" and r.attack_type != "clean"

XFER_CELLS: list[Cell] = [
    ("llm", "S", "ministral-3b (~3B)", metrics_path("main_xfer_llm_s")),
    ("llm", "M", "ministral-14b (~14B)", metrics_path("main_xfer_llm_m")),
    ("llm", "L", "llama (~70B)", metrics_path("main_xfer_llm_l")),
    ("hybrid", "S", "ministral-3b (~3B)", metrics_path("main_xfer_hybrid_s")),
    ("hybrid", "M", "ministral-14b (~14B)", metrics_path("main_xfer_hybrid_m")),
    ("hybrid", "L", "llama (~70B)", metrics_path("main_xfer_hybrid_l")),
    ("hybrid", "120B", "gpt-oss (~120B, E4)", metrics_path("main_transfer")),
]


def _load_cells(cells: list[Cell]) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for mode, size, label, path in cells:
        if not path.exists():
            missing.append(f"{mode}/{size}:{path}")
            continue
        metrics = json.loads(path.read_text())
        g1 = g1_row(metrics)
        cost = cost_g1(metrics)
        rows.append(
            {
                "mode": mode,
                "size": size,
                "guard_model": label,
                "safety_asr": g1.get("instruction_safety_asr"),
                "safety_asr_ci": g1.get("instruction_safety_asr_ci"),
                "psr": g1.get("poisoning_success_rate"),
                "psr_ci": g1.get("poisoning_success_rate_ci"),
                "task_accuracy": g1.get("task_accuracy"),
                "task_accuracy_ci": g1.get("task_accuracy_ci"),
                "mean_latency_ms": cost.get("mean_latency_ms"),
                "mean_llm_calls": cost.get("mean_llm_calls"),
                "n_attack": g1.get("n_attack"),
            }
        )
    return rows, missing


def _asr_grid(rows: list[dict[str, Any]], sizes: tuple[str, ...]) -> list[str]:
    by_key = {(r["mode"], r["size"]): r for r in rows}
    lines = [
        "",
        "## Safety ASR by mode × size",
        "",
        "| Mode | " + " | ".join(sizes) + " |",
        "|---|" + "|".join(["---:"] * len(sizes)) + "|",
    ]
    for mode in ("llm", "hybrid"):
        cells = []
        for size in sizes:
            r = by_key.get((mode, size))
            cells.append("—" if r is None else fmt_ci(r["safety_asr"], r.get("safety_asr_ci")))
        lines.append(f"| {mode} | " + " | ".join(cells) + " |")
    return lines


def build_capacity_compare(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or Path("data/runs/e6_capacity_compare")
    out_dir.mkdir(parents=True, exist_ok=True)
    for dest, src in E6_GPTOSS_SUBSETS.items():
        write_seed_subset_metrics(records_path(src), run_dir(dest), label=dest, keep_record=_e6_cell)
    rows, missing = _load_cells(E6_CELLS)
    report = {
        "missing": missing,
        "cells": rows,
        "note": (
            "Fixed: target=nova-pro, placement=G1/context, v3 prompts, same attacks "
            "(50 seeds). Vary: guard LLM size (S/M/L/120B) and input mode (LLM-only vs hybrid). "
            "120B cells are the matching subset of the main gpt-oss runs (no re-inference); "
            "gpt-oss is the only guard trained for reasoning (not exposed by the endpoint); DS = deepseek "
            "V3.2, a large guard that returns no reasoning trace, to separate size from reasoning. "
            "RQ1: does scaling improve robustness? "
            "RQ2: does a larger guard eliminate the need for deterministic rules?"
        ),
        "rqs": [
            "RQ1: Does scaling the guard model improve robustness?",
            "RQ2: Does a larger guard model eliminate the need for deterministic rules?",
        ],
    }
    (out_dir / "e6_capacity_compare.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = [
        "# E3 — Guard model capacity",
        "",
        report["note"],
        "",
        "## Full grid (G1)",
        "",
        "| Mode | Size | Guard LLM | Safety ASR | PSR | Acc | mean ms | LLM calls | n |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['mode']} | {row['size']} | {row['guard_model']} | "
            f"{fmt_ci(row['safety_asr'], row.get('safety_asr_ci'))} | "
            f"{fmt_ci(row['psr'], row.get('psr_ci'))} | "
            f"{fmt_ci(row['task_accuracy'], row.get('task_accuracy_ci'))} | "
            f"{fmt_ms(row.get('mean_latency_ms'))} | "
            f"{fmt_calls(row.get('mean_llm_calls'))} | "
            f"{row.get('n_attack', '—')} |"
        )
    lines += _asr_grid(rows, E6_SIZES)
    by_key = {(r["mode"], r["size"]): r for r in rows}
    lines += [
        "",
        "## PSR by mode × size",
        "",
        "| Mode | " + " | ".join(E6_SIZES) + " |",
        "|---|" + "---:|" * len(E6_SIZES),
    ]
    for mode in ("llm", "hybrid"):
        cells = []
        for size in E6_SIZES:
            r = by_key.get((mode, size))
            cells.append("—" if r is None else fmt_ci(r["psr"], r.get("psr_ci")))
        lines.append(f"| {mode} | " + " | ".join(cells) + " |")
    if missing:
        lines += ["", "## Missing", ""] + [f"- {m}" for m in missing]
    lines.append("")
    (out_dir / "e6_capacity_compare.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return report


def build_xfer_size_compare(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or Path("data/runs/xfer_size_compare")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, missing = _load_cells(XFER_CELLS)
    report = {
        "missing": missing,
        "cells": rows,
        "note": (
            "Guard-size × unseen (held-out) attacks. Same 50 seeds and A1/A3/A4 "
            "templates as the E4 unseen run. G1 only. Rules mostly miss these templates, "
            "so residual / LLM-only guard size can actually move Safety ASR. "
            "gpt-oss hybrid is the existing E4 unseen G1 row (n=300), not re-inferred."
        ),
    }
    (out_dir / "xfer_size_compare.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = [
        "# Guard-size × unseen attacks (G1)",
        "",
        report["note"],
        "",
        "| Mode | Size | Guard LLM | Safety ASR | Acc | mean ms | LLM calls | n |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['mode']} | {row['size']} | {row['guard_model']} | "
            f"{fmt_ci(row['safety_asr'], row.get('safety_asr_ci'))} | "
            f"{fmt_ci(row['task_accuracy'], row.get('task_accuracy_ci'))} | "
            f"{fmt_ms(row.get('mean_latency_ms'))} | "
            f"{fmt_calls(row.get('mean_llm_calls'))} | "
            f"{row.get('n_attack', '—')} |"
        )
    lines += _asr_grid(rows, ("S", "M", "L", "120B"))
    if missing:
        lines += ["", "## Missing", ""] + [f"- {m}" for m in missing]
    lines.append("")
    (out_dir / "xfer_size_compare.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return report

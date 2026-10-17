"""Paired run comparisons on identical (seed, attack, model, guardrail) conditions.

cot-compare:    B2 vs B4 (LLM-only), B3 vs B5 (hybrid) — CoT effect at a fixed guard budget.
budget-compare: every experiment at 768 vs 4096 guard tokens — the paper correction.
"""

from __future__ import annotations

import random
from math import comb
from pathlib import Path
from typing import Any

from gurma.clients.json_parse import parse_json_object
from gurma.eval.success import INSTRUCTION_SAFETY_ATTACKS, POISONING_ATTACK
from gurma.io import load_models, write_json
from gurma.schemas.models import GuardrailAudit, RunRecord

Key = tuple[str, str, str, str]

COT_PAIRS = [
    # (label, baseline run, CoT run)
    ("B2 vs B4 (LLM-only)", "main_ablation_llm_b4096", "main_cot_llm"),
    ("B3 vs B5 (hybrid)", "main_b4096", "main_cot_hybrid"),
    ("Pilot B2 vs B4 (20 seeds)", "cot_pilot_llm_direct", "cot_pilot_llm_cot"),
]

BUDGET_RUNS = [
    "main",
    "main_ablation_llm",
    "main_transfer",
    "main_adaptive",
    "main_baseline_mod",
    "main_guard_ministral_3b",
    "main_guard_ministral_8b",
    "main_guard_ministral_14b",
    "main_e6_llm_s",
    "main_e6_llm_m",
    "main_e6_llm_l",
    "main_e6_hybrid_s",
    "main_e6_hybrid_m",
    "main_e6_hybrid_l",
    "main_xfer_llm_s",
    "main_xfer_llm_m",
    "main_xfer_llm_l",
    "main_xfer_hybrid_s",
    "main_xfer_hybrid_m",
    "main_xfer_hybrid_l",
    "main_placement",
    "main_squad",
    "main_third_model",
]

_RUNS_DIR = Path("data/runs")


def load_run(name: str, runs_dir: Path = _RUNS_DIR) -> list[RunRecord] | None:
    path = runs_dir / name / "5_runs" / "run_records.jsonl"
    return load_models(path, RunRecord) if path.exists() else None


def _key(r: RunRecord) -> Key:
    return (r.seed_id, r.attack_type or "clean", r.model, r.guardrail)


def guard_parse_ok(audit: GuardrailAudit | None) -> bool | None:
    """Whether the LLM input guard returned a usable decision; None if no LLM call was made."""
    if audit is None or audit.stage != "input":
        return None
    if audit.parse_ok is not None:
        return audit.parse_ok
    raw = audit.guardrail_raw_output or ""
    if audit.guardrail_model in {"pi_detector", "heuristic", "rules", "none"} or '"source": "rules"' in raw:
        return None
    return parse_json_object(raw).get("decision") in {"allow", "sanitize", "block"}


def mcnemar_p(b: int, c: int) -> float:
    """Exact two-sided McNemar test on discordant counts."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def _paired_diff_ci(
    pairs: list[tuple[bool, bool]], *, n_boot: int = 2000, seed: int = 0
) -> tuple[float | None, float | None]:
    if not pairs:
        return None, None
    rng = random.Random(seed)
    n = len(pairs)
    diffs = [float(b) - float(a) for a, b in pairs]
    stats = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot))
    return stats[int(0.025 * n_boot)], stats[min(n_boot - 1, int(0.975 * n_boot))]


def _slices(r: RunRecord) -> list[str]:
    atype = r.attack_type or "clean"
    if atype == "clean":
        return ["clean"]
    out = [atype]
    if atype in INSTRUCTION_SAFETY_ATTACKS:
        out.append("safety")
    if atype == POISONING_ATTACK:
        out.append("poisoning")
    return out


# Per-record binary outcomes; definitions mirror aggregate.py
def _metric_values(r: RunRecord) -> dict[str, bool | None]:
    if (r.attack_type or "clean") == "clean":
        return {"over_refusal": bool(r.refused), "clean_accuracy": bool(r.answer_correct)}
    return {
        "attack_success": None if r.attack_success is None else bool(r.attack_success),
        "task_accuracy": None if r.answer_correct is None else bool(r.answer_correct),
    }


def paired_table(
    a: list[RunRecord], b: list[RunRecord], *, guardrails: set[str] | None = None, seed: int = 0
) -> list[dict[str, Any]]:
    a_by = {_key(r): r for r in a if r.guardrail != "G0"}
    b_by = {_key(r): r for r in b if r.guardrail != "G0"}
    keys = sorted(k for k in a_by.keys() & b_by.keys() if not guardrails or k[3] in guardrails)
    cells: dict[tuple[str, str, str], list[tuple[bool, bool]]] = {}
    for k in keys:
        ra, rb = a_by[k], b_by[k]
        va, vb = _metric_values(ra), _metric_values(rb)
        for sl in _slices(ra):
            for metric, x in va.items():
                y = vb.get(metric)
                if x is None or y is None:
                    continue
                cells.setdefault((k[3], sl, metric), []).append((x, y))
    rows = []
    for (guard, sl, metric), pairs in sorted(cells.items()):
        n = len(pairs)
        only_a = sum(1 for x, y in pairs if x and not y)
        only_b = sum(1 for x, y in pairs if y and not x)
        lo, hi = _paired_diff_ci(pairs, seed=seed)
        rows.append(
            {
                "guardrail": guard,
                "slice": sl,
                "metric": metric,
                "n": n,
                "a": sum(x for x, _ in pairs) / n,
                "b": sum(y for _, y in pairs) / n,
                "diff": (sum(y for _, y in pairs) - sum(x for x, _ in pairs)) / n,
                "diff_ci": [lo, hi],
                "only_a": only_a,
                "only_b": only_b,
                "mcnemar_p": mcnemar_p(only_a, only_b),
            }
        )
    return rows


def guard_health(records: list[RunRecord]) -> dict[str, Any]:
    flags = [guard_parse_ok(r.input_audit) for r in records if r.guardrail != "G0"]
    called = [f for f in flags if f is not None]
    lat = sorted(
        float(r.metadata.get("latency_ms", {}).get("input_guard", 0.0))
        for r in records
        if r.guardrail != "G0" and guard_parse_ok(r.input_audit) is not None
    )
    tokens = [
        r.input_audit.usage.get("completion_tokens")
        for r in records
        if r.input_audit is not None and isinstance(r.input_audit.usage.get("completion_tokens"), int)
    ]
    return {
        "llm_guard_calls": len(called),
        "parse_fail_rate": (sum(1 for f in called if not f) / len(called)) if called else None,
        "input_guard_p95_ms": lat[min(len(lat) - 1, round(0.95 * (len(lat) - 1)))] if lat else None,
        "mean_completion_tokens": (sum(tokens) / len(tokens)) if tokens else None,
    }


def _f(x: Any, digits: int = 3) -> str:
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.{digits}f}"
    return str(x)


def decision_shift(a: list[RunRecord], b: list[RunRecord], *, guardrail: str = "G1") -> dict[str, Any]:
    """Input-guard decisions per attack in A vs B, and how they changed where B lost an answer."""
    a_by = {_key(r): r for r in a if r.guardrail == guardrail}
    b_by = {_key(r): r for r in b if r.guardrail == guardrail}
    out: dict[str, Any] = {}
    for k in sorted(a_by.keys() & b_by.keys()):
        ra, rb = a_by[k], b_by[k]
        atype = ra.attack_type or "clean"
        if atype == "clean" or ra.input_audit is None or rb.input_audit is None:
            continue
        cell = out.setdefault(atype, {"a": {}, "b": {}, "lost": {}, "lost_n": 0, "example": None})
        da, db = ra.input_audit.parsed_decision, rb.input_audit.parsed_decision
        cell["a"][da] = cell["a"].get(da, 0) + 1
        cell["b"][db] = cell["b"].get(db, 0) + 1
        if ra.answer_correct and not rb.answer_correct:
            move = f"{da}→{db}"
            cell["lost"][move] = cell["lost"].get(move, 0) + 1
            cell["lost_n"] += 1
            if cell["example"] is None and da == "sanitize" and db == "block":
                cell["example"] = (rb.input_audit.rationale or "")[:240]
    return out


def _pair_markdown(
    title: str,
    a_name: str,
    b_name: str,
    rows: list[dict[str, Any]],
    ha: dict,
    hb: dict,
    shift: dict[str, Any] | None = None,
) -> list[str]:
    lines = [
        f"## {title}",
        "",
        f"A = `{a_name}`, B = `{b_name}`. Paired on identical (seed, attack, model, guardrail); "
        "Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.",
        "",
        "| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |",
        "|---|---|---|---:|---:|---:|---|---:|---:|---:|",
    ]
    for r in rows:
        lo, hi = r["diff_ci"]
        lines.append(
            f"| {r['guardrail']} | {r['slice']} | {r['metric']} | {r['n']} | {_f(r['a'])} | {_f(r['b'])} | "
            f"{r['diff']:+.3f} [{_f(lo)}, {_f(hi)}] | {r['only_a']} | {r['only_b']} | {_f(r['mcnemar_p'], 2)} |"
        )
    lines += [
        "",
        "| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |",
        "|---|---:|---:|---:|---:|",
        f"| A | {ha['llm_guard_calls']} | {_f(ha['parse_fail_rate'])} | {_f(ha['input_guard_p95_ms'], 0)} | {_f(ha['mean_completion_tokens'], 0)} |",
        f"| B | {hb['llm_guard_calls']} | {_f(hb['parse_fail_rate'])} | {_f(hb['input_guard_p95_ms'], 0)} | {_f(hb['mean_completion_tokens'], 0)} |",
        "",
    ]
    if shift:
        lines += [
            "| Attack | Decisions A (allow / sanitize / block) | Decisions B | Answers lost in B | Top change on lost |",
            "|---|---|---|---:|---|",
        ]
        for atype, cell in shift.items():
            fmt = lambda d: " / ".join(str(d.get(x, 0)) for x in ("allow", "sanitize", "block"))  # noqa: E731
            top = max(cell["lost"].items(), key=lambda kv: kv[1]) if cell["lost"] else None
            lines.append(
                f"| {atype} | {fmt(cell['a'])} | {fmt(cell['b'])} | {cell['lost_n']} | "
                f"{'—' if top is None else f'{top[0]} ({top[1]})'} |"
            )
        lines.append("")
    return lines


def _build(
    pairs: list[tuple[str, str, str]], out_dir: Path, title: str, guardrails: set[str] | None
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {"pairs": [], "missing": []}
    lines = [f"# {title}", ""]
    for label, a_name, b_name in pairs:
        a, b = load_run(a_name), load_run(b_name)
        if a is None or b is None:
            report["missing"].append(label)
            continue
        rows = paired_table(a, b, guardrails=guardrails)
        # Health over the compared guardrails only: CoT runs have G1 only, baselines G1+G2.
        def in_scope(records: list[RunRecord]) -> list[RunRecord]:
            return [r for r in records if guardrails is None or r.guardrail in guardrails]

        ha, hb = guard_health(in_scope(a)), guard_health(in_scope(b))
        shift = decision_shift(a, b) if guardrails == {"G1"} else None
        report["pairs"].append(
            {"label": label, "a": a_name, "b": b_name, "rows": rows, "health_a": ha, "health_b": hb, "decision_shift": shift}
        )
        lines += _pair_markdown(label, a_name, b_name, rows, ha, hb, shift)
    if report["missing"]:
        lines += ["Missing (not yet run): " + ", ".join(report["missing"]), ""]
    stem = out_dir.name
    write_json(out_dir / f"{stem}.json", report)
    (out_dir / f"{stem}.md").write_text("\n".join(lines))
    print(f"[compare] wrote {out_dir / (stem + '.md')}")
    return report


def build_cot_compare(out_dir: Path | None = None) -> dict[str, Any]:
    return _build(COT_PAIRS, out_dir or _RUNS_DIR / "cot_compare", "CoT effect (paired)", {"G1"})


def build_budget_compare(out_dir: Path | None = None) -> dict[str, Any]:
    pairs = [(f"{name}: 768 vs 4096", name, f"{name}_b4096") for name in BUDGET_RUNS]
    return _build(pairs, out_dir or _RUNS_DIR / "budget_compare", "Guard budget 768 vs 4096 (paired)", None)

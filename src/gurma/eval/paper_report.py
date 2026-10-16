"""Generate a paper-facing results report from saved metrics JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gurma.eval.bootstrap import fmt_ci
from gurma.eval.run_names import metrics_path, run_dir

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "data/runs"

ATTACK_LABELS = {
    "indirect_injection": "A1 Indirect injection",
    "context_poisoning": "A2 Context poisoning",
    "policy_retrieval": "A3 Policy-violating retrieval",
    "authority_conflict": "A4 Authority conflict",
}

# (header, point key, CI key) for a guardrail-level metrics row.
METRIC_COLUMNS = [
    ("Safety ASR ↓", "instruction_safety_asr", "instruction_safety_asr_ci"),
    ("PSR ↓", "poisoning_success_rate", "poisoning_success_rate_ci"),
    ("Macro ↓", "macro_attack_success", "macro_attack_success_ci"),
    ("Acc ↑", "task_accuracy", "task_accuracy_ci"),
    ("Over-refusal ↓", "over_refusal", "over_refusal_ci"),
]

DECISIONS = ["allow", "sanitize", "block"]


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def _load_optional(path: Path) -> dict[str, Any] | None:
    return _load(path) if path.exists() else None


def _fmt(x: Any, digits: int = 3) -> str:
    if x is None:
        return "—"
    return f"{float(x):.{digits}f}"


def _cell(row: dict[str, Any], point_key: str, ci_key: str) -> str:
    return fmt_ci(row.get(point_key), row.get(ci_key))


def _metrics_table(rows: list[dict[str, Any]], first: str = "Guardrail") -> list[str]:
    """Guardrail-level table; columns that are empty for every row are dropped."""
    cols = [c for c in METRIC_COLUMNS if any(r.get(c[1]) is not None for r in rows)]
    if not any(c[1] == "poisoning_success_rate" for c in cols):
        # Without A2, Macro equals Safety ASR.
        cols = [c for c in cols if c[1] != "macro_attack_success"]
    lines = [
        f"| {first} | " + " | ".join(c[0] for c in cols) + " |",
        "|---|" + "---:|" * len(cols),
    ]
    for r in rows:
        lines.append(f"| {r['guardrail']} | " + " | ".join(_cell(r, k, ci) for _, k, ci in cols) + " |")
    return lines


def _breakdown_table(rows: list[dict[str, Any]], guards: list[str], key: str, suffix: str) -> list[str]:
    """Per-attack (or per-model) success table with one column per guardrail."""
    lines = [
        f"| {key.title()} | " + " | ".join(guards) + " |",
        "|---|" + "---:|" * len(guards),
    ]
    if key == "attack":
        order = list(ATTACK_LABELS)
        rows = sorted(rows, key=lambda r: order.index(r["attack"]) if r.get("attack") in order else len(order))
    for r in rows:
        label = ATTACK_LABELS.get(r.get(key), r.get(key)) if key == "attack" else r.get(key)
        cells = " | ".join(_cell(r, f"{g}_{suffix}", f"{g}_{suffix}_ci") for g in guards)
        lines.append(f"| {label} | {cells} |")
    return lines


def _decision_table(by_attack: dict[str, dict[str, int]]) -> list[str]:
    lines = ["| Attack | allow | sanitize | block |", "|---|---:|---:|---:|"]
    for attack, label in ATTACK_LABELS.items():
        if attack in by_attack:
            counts = by_attack[attack]
            lines.append(f"| {label} | " + " | ".join(str(counts.get(d, 0)) for d in DECISIONS) + " |")
    return lines


def _run_summary(metrics: dict[str, Any]) -> list[str]:
    """Main + per-attack tables for a secondary run (placement, adaptive, ...)."""
    t2 = metrics.get("table2_main") or []
    guards = [r["guardrail"] for r in t2]
    return [
        f"Conditions: {metrics.get('n_records')} "
        f"(attack={metrics.get('n_attack_conditions')}, clean={metrics.get('n_clean_conditions')}).",
        "",
        *_metrics_table(t2),
        "",
        *_breakdown_table(metrics.get("table3_attack_breakdown") or [], guards, "attack", "success"),
        "",
    ]


def _embed(path: Path, *, drop_from: str | None = None, depth: int = 1) -> list[str]:
    """Inline a generated markdown file: drop its H1 title and nest its headings `depth` levels."""
    text = path.read_text()
    if drop_from and drop_from in text:
        text = text[: text.index(drop_from)]
    out = []
    for line in text.strip().splitlines():
        if line.startswith("# "):
            continue
        out.append("#" * depth + line if line.startswith("##") else line)
    while out and not out[0].strip():
        out.pop(0)
    return out + [""]


def _budget_section(budget: dict[str, Any]) -> list[str]:
    """Compact G1 view of the paired 768 vs 4096 guard-budget comparison."""
    lines = [
        "## Guard budget 768 vs 4096 (paired, G1)",
        "",
        "Same conditions re-run with only `guardrail_max_tokens` changed. "
        "Safety Acc = task accuracy on A1/A3/A4. Full table: "
        "[budget_compare.md](../data/runs/budget_compare/budget_compare.md).",
        "",
        "| Run | Parse fail | Safety ASR | Safety Acc | PSR |",
        "|---|---:|---:|---:|---:|",
    ]

    def pair(row: dict[str, Any] | None) -> str:
        return "—" if row is None else f"{_fmt(row['a'])} → {_fmt(row['b'])}"

    for p in budget.get("pairs") or []:
        rows = {(r["guardrail"], r["slice"], r["metric"]): r for r in p["rows"]}
        guard = "G1" if any(k[0] == "G1" for k in rows) else "C"
        fails = (p["health_a"].get("parse_fail_rate"), p["health_b"].get("parse_fail_rate"))
        fail = "—" if None in fails else f"{_fmt(fails[0])} → {_fmt(fails[1])}"
        lines.append(
            f"| {p['a']}{'' if guard == 'G1' else ' (C)'} | {fail} | "
            f"{pair(rows.get((guard, 'safety', 'attack_success')))} | "
            f"{pair(rows.get((guard, 'safety', 'task_accuracy')))} | "
            f"{pair(rows.get((guard, 'context_poisoning', 'attack_success')))} |"
        )
    lines.append("")
    return lines


FINDINGS = [
    "**G0 is highly vulnerable** to retrieval-mediated instruction attacks "
    "(Safety ASR {g0_asr}; A1 = 0.905). Llama is much weaker than Nova Pro on G0 (0.977 vs 0.393).",
    "**Hybrid G1 eliminates in-distribution instruction/safety attacks** "
    "(Safety ASR 0.000) and raises attacked-task accuracy 0.279 → 0.849 with 0 over-refusal.",
    "**G2 adds almost nothing on hybrid** (rescue 8/517 G0 successes after a G1 miss). "
    "G2 rewrite is rare (10), so accuracy is not rewrite-inflated.",
    "**Ablation:** with an adequate guard budget every input mode nearly removes "
    "Safety ASR (hybrid 0.000, rules 0.000, LLM-only 0.018). Hybrid wins on the "
    "other axes: lower PSR than rules (0.205 vs 0.415), higher Acc than LLM-only "
    "(0.849 vs 0.751), and cheaper than LLM-only (1.2 vs 1.9 LLM calls; 1.8 s vs 5.3 s "
    "mean on the matched 50 seeds).",
    "**External baselines:** a classic PI detector leaves Safety ASR at 0.403; "
    "LLM moderation reaches 0.000 but at Acc 0.588 and PSR 0.380 (hybrid: 0.885 / 0.190).",
    "**Limitation:** context poisoning remains (PSR 0.205 under hybrid G1/G2; "
    "0.280 on SQuAD, 0.120 on deepseek). This is an integrity leftover, not a "
    "missing instruction filter.",
    "**Transfer:** on unseen templates the frozen hybrid's LLM residual catches "
    "most phrasings the rules miss (G1 allow 43/300). G0 Safety ASR 0.113 → G1 0.017 "
    "→ G2 0.000; the G1 leak is authority conflict (0.050).",
    "**Adaptive attacks** that avoid known rule triggers are the hardest case: "
    "G1 Safety ASR 0.203 (authority conflict 0.520). G2 brings it to 0.000 at an "
    "Acc cost (0.757 → 0.687). Defense-in-depth matters under adaptive phrasing.",
    "**Placement:** query-only (Q) fails (Safety ASR 0.700) because payloads "
    "live in retrieval. Context (C) drives Safety ASR → 0.000 with Acc 0.887; "
    "output-only (O) also reaches 0.000 but Acc collapses (0.265) and PSR stays "
    "0.540. CO ≈ C.",
    "**Guard capacity (Exp 6):** on Nova Pro × G1 × 50 seeds, Safety ASR is "
    "0.000 for LLM-only and hybrid across S/M/L (ministral-3b / 14b / llama-70B). "
    "The gap is **utility**: small LLM-only guards collapse Acc (0.115–0.190) while "
    "hybrid keeps Acc 0.885–0.925. Rules are what make a small guard usable; "
    "PSR stays 0.18–0.54.",
    "**Guard-size × unseen:** on held-out A1/A3/A4, Safety ASR does **not** fall "
    "with Ministral/Llama scale (LLM-only 0.027→0.107; hybrid 0.027→0.110), while "
    "gpt-oss hybrid reaches 0.017 at Acc 0.843 (ladder: 0.52–0.61).",
    "**Guard budget:** the original 768-token guard budget truncated guard output "
    "(14% parse failure on main), and truncation failed open. At 4096 tokens LLM-only "
    "Safety ASR drops 0.457 → 0.018 (Acc 0.300 → 0.740), moderation 0.377 → 0.000, "
    "adaptive G1 0.327 → 0.203, and PSR falls ~0.1 on most hybrid runs. All tables "
    "here use 4096; the paired 768 vs 4096 table is below.",
    "**CoT guard prompt:** on LLM-only G1, step-by-step reasoning removes the "
    "residual Safety ASR (0.018 → 0.000) and lifts clean Acc (+0.035), but cuts "
    "policy-retrieval Acc 0.720 → 0.555: the guard blocks the whole context "
    "(76 vs 33 blocks) instead of sanitizing a removable harmful span. On hybrid, "
    "CoT has no significant effect. CoT costs ~50% more guard output tokens.",
]


def render_paper_report(
    *,
    main_metrics: dict[str, Any],
    main_gate: dict[str, Any],
    ablation: dict[str, Any],
    llm_metrics: dict[str, Any] | None = None,
    rules_metrics: dict[str, Any] | None = None,
    transfer_metrics: dict[str, Any] | None = None,
    transfer_gate: dict[str, Any] | None = None,
    placement_metrics: dict[str, Any] | None = None,
    robustness: list[tuple[str, str, dict[str, Any]]] | None = None,
    budget: dict[str, Any] | None = None,
    runs_dir: Path = RUNS,
) -> str:
    t1 = main_metrics.get("table1_dataset") or {}
    t2 = main_metrics.get("table2_main") or []
    guards = [r["guardrail"] for r in t2]
    rescue = main_gate.get("rescue") or {}
    g2_out = main_gate.get("g2_output_decisions_attack") or {}
    g0_asr = _fmt(t2[0].get("instruction_safety_asr") if t2 else None)

    lines = [
        "# GURMA Results Report",
        "",
        "All LLM-guard numbers use a 4096-token guard budget (`*_b4096` runs). "
        "Regenerate with `gurma report`. Brackets are 95% bootstrap CIs (n=2000).",
        "",
        "## Setup",
        "",
        "- Seeds: 100 HotpotQA (both-model clean freeze)",
        "- Attacks: 4 × 100 = 400 validated cases (`accepted = semantic ∧ payload`)",
        "- Guardrails: G0 none / G1 input / G2 input+output",
        "- Models: `nova-pro`, `llama`; guard/judge: `gpt-oss`",
        "- Defense freeze: hybrid input (`rules` first) + `v3` prompts ([FREEZE.md](../FREEZE.md))",
        "- Guard LLM budget: 4096 completion tokens (rules-only and PI detector make no guard LLM calls)",
        "- Main conditions: 3000 (2400 attack + 600 clean); API calls ≫ 3000",
        "",
        "## Findings",
        "",
    ]
    lines += [f"{i}. {f.format(g0_asr=g0_asr)}" for i, f in enumerate(FINDINGS, 1)]

    # --- Main result -----------------------------------------------------
    lines += ["", "## Table 1 — Dataset", "", "| Attack | Cases |", "|---|---:|"]
    lines += [f"| {label} | {t1.get(key, '—')} |" for key, label in ATTACK_LABELS.items()]
    lines += ["", "## Table 2 — Main result (hybrid v3)", "", *_metrics_table(t2)]
    lines += [
        "",
        "Safety ASR = mean success over A1/A3/A4. PSR = A2 only. Macro = mean over all four. "
        "Acc = task accuracy on attacked cases.",
        "",
        "## Table 3 — Attack breakdown",
        "",
        *_breakdown_table(main_metrics.get("table3_attack_breakdown") or [], guards, "attack", "success"),
        "",
        "## Table 4 — Cross-model Safety ASR",
        "",
        *_breakdown_table(main_metrics.get("table4_cross_model") or [], guards, "model", "safety_asr"),
        "",
        "## Table 5 — Input ablation (G1 only)",
        "",
        "| Input mode | Safety ASR | PSR | Macro | Acc | Over-refusal |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in ablation.get("g1_comparison") or []:
        lines.append(
            f"| {row.get('input_mode')} | "
            f"{_cell(row, 'safety_asr', 'safety_asr_ci')} | "
            f"{_cell(row, 'psr', 'psr_ci')} | "
            f"{_cell(row, 'macro', 'macro_ci')} | "
            f"{_cell(row, 'task_accuracy', 'task_accuracy_ci')} | "
            f"{_cell(row, 'over_refusal', 'over_refusal_ci')} |"
        )
    lines += [
        "",
        "Hybrid = rules first, then LLM residual. All three modes nearly remove Safety ASR; "
        "hybrid combines the rules' accuracy with the LLM's lower PSR.",
        "",
    ]
    for title, metrics, note in (
        ("LLM-only G1/G2", llm_metrics, "On LLM-only, G2 removes the residual Safety ASR (0.018 → 0.000)."),
        ("Rules-only G1/G2", rules_metrics, None),
    ):
        if metrics:
            lines += [f"### {title}", "", *_metrics_table(metrics.get("table2_main") or []), ""]
            if note:
                lines += [note, ""]

    lines += [
        "## Safety vs benign accuracy",
        "",
        "| Guardrail | Safety ASR | Benign Acc | Attack Acc | Over-refusal |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in main_metrics.get("scatter_safety_vs_benign_acc") or []:
        lines.append(
            f"| {row.get('guardrail')} | {_fmt(row.get('safety_asr'))} "
            f"| {_fmt(row.get('benign_accuracy'))} "
            f"| {_fmt(row.get('task_accuracy_on_attacks'))} "
            f"| {_fmt(row.get('over_refusal'))} |"
        )
    lines += [
        "",
        "Hybrid G1 does **not** trade benign accuracy for safety "
        "(benign Acc 0.875 → 0.850; over-refusal 0.000).",
        "",
        "## Mechanism (main hybrid)",
        "",
        "G1 input decisions on attacked contexts:",
        "",
        *_decision_table(main_gate.get("g1_input_by_attack") or {}),
        "",
        "| G2 output | pass | rewrite | block | missing |",
        "|---|---:|---:|---:|---:|",
        "| attacked | " + " | ".join(str(g2_out.get(k, 0)) for k in ("pass", "rewrite", "block", "missing")) + " |",
        "",
        f"Rescue: of {rescue.get('g0_success')}/{rescue.get('n')} G0 successes, G1 stopped "
        f"{rescue.get('g1_helped')} and G2 caught {rescue.get('g2_helped_after_g1_miss')} after a G1 miss. "
        "A1/A3/A4 are fully sanitized by rules; residual `allow` is A2 poisoning only.",
        "",
    ]
    cost = main_metrics.get("table_cost_latency") or []
    if cost:
        lines += [
            "## Cost / latency (main hybrid)",
            "",
            "| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for row in cost:
            def fnum(x: Any) -> str:
                return "—" if x is None else f"{float(x):.1f}"

            lines.append(
                f"| {row['guardrail']} | {row.get('n')} | "
                f"{fnum(row.get('mean_latency_ms'))} | "
                f"{fnum(row.get('p50_latency_ms'))} | "
                f"{fnum(row.get('p95_latency_ms'))} | "
                f"{fnum(row.get('mean_llm_calls'))} |"
            )
        lines.append("")

    # --- Experiments 4–6 -------------------------------------------------
    lines += [
        "## Experiment 4 — Unseen attack transfer",
        "",
        "50 frozen seeds × A1/A3/A4 held-out templates from a different generator (`deepseek`) "
        "× G0/G1/G2 × 2 models. Defense not retuned; A2 and clean utility not re-run.",
        "",
    ]
    if transfer_metrics:
        xguards = [r["guardrail"] for r in transfer_metrics.get("table2_main") or []]
        lines += [
            *_run_summary(transfer_metrics),
            *_breakdown_table(transfer_metrics.get("table4_cross_model") or [], xguards, "model", "safety_asr"),
            "",
        ]
        if transfer_gate:
            lines += ["G1 input decisions:", "", *_decision_table(transfer_gate.get("g1_input_by_attack") or {}), ""]
    else:
        lines += ["_Not yet run._", ""]
    xfer_size = runs_dir / "xfer_size_compare/xfer_size_compare.md"
    if xfer_size.exists():
        lines += ["### Guard size × unseen attacks", "", *_embed(xfer_size, depth=2)]

    lines += [
        "## Experiment 5 — Placement (Q / C / O / CO)",
        "",
        "Frozen hybrid v3; only *where* the guardrail is applied. Q=query, C=context (≈G1), "
        "O=output, CO=context+output (≈G2). 50 seeds × 4 attacks × 4 placements × 2 models.",
        "",
    ]
    lines += _run_summary(placement_metrics) if placement_metrics else ["_Not yet run._", ""]

    lines += ["## Experiment 6 — Guard model capacity", ""]
    for path, heading in (
        (runs_dir / "e6_capacity_compare/e6_capacity_compare.md", None),
        (runs_dir / "guard_size_compare/guard_size_compare.md", "### Hybrid guard-size ladder vs gpt-oss"),
    ):
        if path.exists():
            lines += ([heading, ""] if heading else []) + _embed(path, depth=2 if heading else 1)

    # --- Robustness, baselines, budget, CoT ------------------------------
    if robustness:
        lines += ["## Robustness (defense frozen)", ""]
        for title, blurb, metrics in robustness:
            lines += [f"### {title}", "", blurb, "", *_run_summary(metrics)]

    baseline = runs_dir / "baseline_compare/baseline_compare.md"
    if baseline.exists():
        lines += ["## External baselines", "", *_embed(baseline)]

    if budget:
        lines += _budget_section(budget)

    cot = runs_dir / "cot_compare/cot_compare.md"
    if cot.exists():
        lines += [
            "## CoT guard prompt (paired)",
            "",
            "Same 4096 budget; only the input-guard prompt changes (`v3` → `v3-cot`). "
            "Full write-up: [b4096-cot-results.md](b4096-cot-results.md).",
            "",
            *_embed(cot, drop_from="## Pilot"),
        ]

    lines += [
        "## Caveats",
        "",
        "- Counts are **experimental conditions**, not LLM API calls.",
        "- A2 success is an integrity metric (PSR), not Safety ASR. "
        "We do not add poisoning-specific rules to force PSR → 0.",
        "- Attack acceptance never uses G0 effectiveness (no selection bias).",
        "- In-distribution hybrid rules match known operator templates; "
        "Experiment 4 / adaptive / cross-dataset test generalization with the defense frozen.",
        "- External baselines (PI detector, moderation) are comparison systems, "
        "not retunes of the frozen hybrid.",
        "",
    ]
    return "\n".join(lines)


def write_paper_report(out_path: Path | None = None) -> Path:
    out_path = out_path or (ROOT / "reports" / "results.md")
    robustness = [
        (
            "Adaptive attacks",
            "Attacker avoids known rule triggers while preserving the malicious objective.",
            ROOT / metrics_path("main_adaptive"),
        ),
        (
            "Cross-dataset (SQuAD)",
            "Same frozen hybrid v3 (tuned on HotpotQA) evaluated on single-hop SQuAD seeds.",
            ROOT / metrics_path("main_squad"),
        ),
        (
            "Third target model (deepseek)",
            "Frozen seeds and attacks; answer model = deepseek only.",
            ROOT / metrics_path("main_third_model"),
        ),
    ]
    md = render_paper_report(
        main_metrics=_load(ROOT / metrics_path("main")),
        main_gate=_load(ROOT / run_dir("main") / "7_ablation/pilot_gate_summary.json"),
        ablation=_load(RUNS / "ablation_compare/ablation_compare.json"),
        llm_metrics=_load_optional(ROOT / metrics_path("main_ablation_llm")),
        rules_metrics=_load_optional(ROOT / metrics_path("main_ablation_rules", llm_guard=False)),
        transfer_metrics=_load_optional(ROOT / metrics_path("main_transfer")),
        transfer_gate=_load_optional(ROOT / run_dir("main_transfer") / "7_ablation/pilot_gate_summary.json"),
        placement_metrics=_load_optional(ROOT / metrics_path("main_placement")),
        robustness=[(t, b, _load(p)) for t, b, p in robustness if p.exists()],
        budget=_load_optional(RUNS / "budget_compare/budget_compare.json"),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md)
    print(f"[report] wrote {out_path}")
    return out_path

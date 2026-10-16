"""Generate a paper-facing results report from saved metrics JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gurma.eval.bootstrap import fmt_ci
from gurma.eval.run_names import metrics_path, run_dir

ROOT = Path(__file__).resolve().parents[3]


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def _fmt(x: Any, digits: int = 3) -> str:
    if x is None:
        return "—"
    return f"{float(x):.{digits}f}"


def _cell(row: dict[str, Any], point_key: str, ci_key: str) -> str:
    return fmt_ci(row.get(point_key), row.get(ci_key))


def _row(guard: dict[str, Any]) -> str:
    return (
        f"| {guard['guardrail']} "
        f"| {_cell(guard, 'instruction_safety_asr', 'instruction_safety_asr_ci')} "
        f"| {_cell(guard, 'poisoning_success_rate', 'poisoning_success_rate_ci')} "
        f"| {_cell(guard, 'macro_attack_success', 'macro_attack_success_ci')} "
        f"| {_cell(guard, 'task_accuracy', 'task_accuracy_ci')} "
        f"| {_cell(guard, 'over_refusal', 'over_refusal_ci')} |"
    )


def _budget_section(budget: dict[str, Any]) -> list[str]:
    """Compact G1 view of the paired 768 vs 4096 guard-budget comparison."""
    lines = [
        "",
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


def render_paper_report(
    *,
    main_metrics: dict[str, Any],
    main_gate: dict[str, Any],
    ablation: dict[str, Any],
    llm_metrics: dict[str, Any] | None = None,
    rules_metrics: dict[str, Any] | None = None,
    transfer_metrics: dict[str, Any] | None = None,
    transfer_gate: dict[str, Any] | None = None,
) -> str:
    t1 = main_metrics.get("table1_dataset") or {}
    t2 = main_metrics.get("table2_main") or []
    t3 = main_metrics.get("table3_attack_breakdown") or []
    t4 = main_metrics.get("table4_cross_model") or []
    scatter = main_metrics.get("scatter_safety_vs_benign_acc") or []
    rescue = main_gate.get("rescue") or {}
    g1_dec = main_gate.get("g1_input_decisions_attack") or {}
    g1_by = main_gate.get("g1_input_by_attack") or {}
    g2_out = main_gate.get("g2_output_decisions_attack") or {}
    g2_corr = main_gate.get("g2_correct_via_output_decision") or {}

    lines = [
        "# GURMA Results Report",
        "",
        "Generated from frozen main + input ablations + held-out transfer. "
        "Regenerate with `gurma report`. Brackets are 95% bootstrap CIs.",
        "",
        "## Setup",
        "",
        "- Seeds: 100 HotpotQA (both-model clean freeze)",
        "- Attacks: 4 × 100 = 400 validated cases (`accepted = semantic ∧ payload`)",
        "- Guardrails: G0 none / G1 input / G2 input+output",
        "- Models: `nova-pro`, `llama`; guard/judge: `gpt-oss`",
        "- Defense freeze: hybrid input (`rules` first) + `v3` prompts ([FREEZE.md](../FREEZE.md))",
        "- Guard LLM budget: 4096 completion tokens (`*_b4096` runs; rules-only and "
        "PI detector make no guard LLM calls)",
        "- Main conditions: 3000 (2400 attack + 600 clean); API calls ≫ 3000",
        "- Experiment 4: 50 frozen seeds × A1/A3/A4 held-out templates "
        "(generator=`deepseek`) × G0/G1/G2 × 2 models; defense not retuned",
        "- Experiment 5: 50 seeds × A1–A4 × Q/C/O/CO × 2 models (1600); "
        "same hybrid v3, placement only",
        "",
        "## Findings",
        "",
        "1. **G0 is highly vulnerable** to retrieval-mediated instruction attacks "
        f"(Safety ASR {_fmt(t2[0].get('instruction_safety_asr') if t2 else None)}; "
        "A1 = 0.905). Llama is much weaker than Nova Pro on G0 (0.977 vs 0.393).",
        "2. **Hybrid G1 eliminates in-distribution instruction/safety attacks** "
        "(Safety ASR 0.000) and raises attacked-task accuracy 0.279 → 0.849 "
        "with 0 over-refusal.",
        "3. **G2 adds almost nothing on hybrid** (rescue 8/517 G0 successes after a G1 miss). "
        "G2 rewrite is rare (10), so accuracy is not rewrite-inflated.",
        "4. **Ablation:** with an adequate guard budget every input mode nearly removes "
        "Safety ASR (hybrid 0.000, rules 0.000, LLM-only 0.018). Hybrid wins on the "
        "other axes: lower PSR than rules (0.205 vs 0.415), higher Acc than LLM-only "
        "(0.849 vs 0.751), and cheaper than LLM-only (1.2 vs 1.9 LLM calls; 1.8 s vs 5.3 s "
        "mean on the matched 50 seeds).",
        "5. **External baselines:** a classic PI detector leaves Safety ASR at 0.403; "
        "LLM moderation reaches 0.000 but at Acc 0.588 and PSR 0.380 (hybrid: 0.885 / 0.190).",
        "6. **Limitation:** context poisoning remains (PSR 0.205 under hybrid G1/G2; "
        "0.280 on SQuAD, 0.120 on deepseek). This is an integrity leftover, not a "
        "missing instruction filter.",
        "7. **Transfer:** on unseen templates the frozen hybrid's LLM residual catches "
        "most phrasings the rules miss (G1 allow 43/300). G0 Safety ASR 0.113 → G1 0.017 "
        "→ G2 0.000; the G1 leak is authority conflict (0.050).",
        "8. **Adaptive attacks** that avoid known rule triggers are the hardest case: "
        "G1 Safety ASR 0.203 (authority conflict 0.520). G2 brings it to 0.000 at an "
        "Acc cost (0.757 → 0.687). Defense-in-depth matters under adaptive phrasing.",
        "9. **Placement:** query-only (Q) fails (Safety ASR 0.700) because payloads "
        "live in retrieval. Context (C) drives Safety ASR → 0.000 with Acc 0.887; "
        "output-only (O) also reaches 0.000 but Acc collapses (0.265) and PSR stays "
        "0.540. CO ≈ C.",
        "10. **Guard capacity (Exp 6):** on Nova Pro × G1 × 50 seeds, Safety ASR is "
        "0.000 for LLM-only and hybrid across S/M/L (ministral-3b / 14b / llama-70B). "
        "The gap is **utility**: small LLM-only guards collapse Acc (0.115–0.190) while "
        "hybrid keeps Acc 0.885–0.925. Rules are what make a small guard usable; "
        "PSR stays 0.18–0.54.",
        "11. **Guard-size × unseen:** on held-out A1/A3/A4, Safety ASR does **not** fall "
        "with Ministral/Llama scale (LLM-only 0.027→0.107; hybrid 0.027→0.110), while "
        "gpt-oss hybrid reaches 0.017 at Acc 0.843 (ladder: 0.52–0.61).",
        "12. **Guard budget:** the original 768-token guard budget truncated guard output "
        "(14% parse failure on main), and truncation failed open. At 4096 tokens LLM-only "
        "Safety ASR drops 0.457 → 0.018 (Acc 0.300 → 0.740), moderation 0.377 → 0.000, "
        "adaptive G1 0.327 → 0.203, and PSR falls ~0.1 on most hybrid runs. All tables "
        "here use 4096; the paired 768 vs 4096 table is below.",
        "13. **CoT guard prompt:** on LLM-only G1, step-by-step reasoning removes the "
        "residual Safety ASR (0.018 → 0.000) and lifts clean Acc (+0.035), but cuts "
        "policy-retrieval Acc 0.720 → 0.555: the guard blocks the whole context "
        "(76 vs 33 blocks) instead of sanitizing a removable harmful span. On hybrid, "
        "CoT has no significant effect. CoT costs ~50% more guard output tokens.",
        "",
        "## Table 1 — Dataset",
        "",
        "| Attack | Cases |",
        "|---|---:|",
    ]
    labels = {
        "indirect_injection": "A1 Indirect injection",
        "context_poisoning": "A2 Context poisoning",
        "policy_retrieval": "A3 Policy-violating retrieval",
        "authority_conflict": "A4 Authority conflict",
    }
    for key, label in labels.items():
        lines.append(f"| {label} | {t1.get(key, '—')} |")

    lines += [
        "",
        "## Table 2 — Main result (hybrid v3)",
        "",
        "| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ | Over-refusal ↓ |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in t2:
        lines.append(_row(row))

    lines += [
        "",
        "Safety ASR = mean success over A1/A3/A4. PSR = A2 only. "
        "Macro = mean over all four. Acc = task accuracy on attacked cases. "
        "CIs are percentile bootstrap (n=2000).",
        "",
        "## Table 3 — Attack breakdown",
        "",
        "| Attack | G0 | G1 | G2 |",
        "|---|---:|---:|---:|",
    ]
    for row in t3:
        lines.append(
            f"| {row.get('attack')} | "
            f"{_cell(row, 'G0_success', 'G0_success_ci')} | "
            f"{_cell(row, 'G1_success', 'G1_success_ci')} | "
            f"{_cell(row, 'G2_success', 'G2_success_ci')} |"
        )

    lines += [
        "",
        "## Table 4 — Cross-model Safety ASR",
        "",
        "| Model | G0 | G1 | G2 |",
        "|---|---:|---:|---:|",
    ]
    for row in t4:
        lines.append(
            f"| {row.get('model')} | "
            f"{_cell(row, 'G0_safety_asr', 'G0_safety_asr_ci')} | "
            f"{_cell(row, 'G1_safety_asr', 'G1_safety_asr_ci')} | "
            f"{_cell(row, 'G2_safety_asr', 'G2_safety_asr_ci')} |"
        )

    lines += [
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
        "G0 rows for rules/llm ablations are borrowed from main. "
        "Hybrid = rules first, then LLM residual. "
        "All three modes nearly remove Safety ASR; hybrid combines the rules' accuracy "
        "with the LLM's lower PSR.",
        "",
    ]

    if llm_metrics:
        lines += [
            "### LLM-only G1/G2 (for G2 rescue contrast)",
            "",
            "| Guardrail | Safety ASR | PSR | Acc | Over-refusal |",
            "|---|---:|---:|---:|---:|",
        ]
        for row in llm_metrics.get("table2_main") or []:
            lines.append(
                f"| {row['guardrail']} | "
                f"{_cell(row, 'instruction_safety_asr', 'instruction_safety_asr_ci')} | "
                f"{_cell(row, 'poisoning_success_rate', 'poisoning_success_rate_ci')} | "
                f"{_cell(row, 'task_accuracy', 'task_accuracy_ci')} | "
                f"{_cell(row, 'over_refusal', 'over_refusal_ci')} |"
            )
        lines += [
            "",
            "On LLM-only, G2 removes the residual Safety ASR (0.018 → 0.000).",
            "",
        ]

    if rules_metrics:
        lines += [
            "### Rules-only G1/G2",
            "",
            "| Guardrail | Safety ASR | PSR | Acc | Over-refusal |",
            "|---|---:|---:|---:|---:|",
        ]
        for row in rules_metrics.get("table2_main") or []:
            lines.append(
                f"| {row['guardrail']} | "
                f"{_cell(row, 'instruction_safety_asr', 'instruction_safety_asr_ci')} | "
                f"{_cell(row, 'poisoning_success_rate', 'poisoning_success_rate_ci')} | "
                f"{_cell(row, 'task_accuracy', 'task_accuracy_ci')} | "
                f"{_cell(row, 'over_refusal', 'over_refusal_ci')} |"
            )
        lines.append("")

    lines += [
        "## Figure data — Safety ASR vs benign accuracy",
        "",
        "| Guardrail | Safety ASR | Benign Acc | Attack Acc | Over-refusal |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in scatter:
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
        f"- G1 decisions on attacks: `{g1_dec}`",
        f"- G1 by attack: `{g1_by}`",
        f"- G2 output: `{g2_out}`",
        (
            f"- Rescue: G0 successes={rescue.get('g0_success')}/{rescue.get('n')}; "
            f"G1 stopped {rescue.get('g1_helped')}; "
            f"G2 after G1 miss {rescue.get('g2_helped_after_g1_miss')}"
        ),
        f"- G2-correct via: `{g2_corr}` (rewrite={g2_corr.get('rewrite', 0)})",
        "",
        "A1/A3/A4 are fully sanitized by rules. Residual `allow` is almost only A2 poisoning.",
        "",
        "## Experiment 4 — Unseen attack transfer",
        "",
        "Defense was frozen before evaluating attacks generated from unseen templates "
        "and a different generator (`deepseek`; 149/150 spans LLM-rewritten). "
        "A2 is excluded (integrity leftover, not an instruction-template match concern). "
        "Clean utility is not re-run.",
        "",
    ]
    if transfer_metrics:
        xt2 = transfer_metrics.get("table2_main") or []
        xt3 = transfer_metrics.get("table3_attack_breakdown") or []
        xt4 = transfer_metrics.get("table4_cross_model") or []
        lines += [
            f"Transfer conditions: {transfer_metrics.get('n_records')} "
            f"(attack={transfer_metrics.get('n_attack_conditions')}).",
            "",
            "| Guardrail | Safety ASR ↓ | Acc ↑ |",
            "|---|---:|---:|",
        ]
        for row in xt2:
            lines.append(
                f"| {row['guardrail']} | "
                f"{_cell(row, 'instruction_safety_asr', 'instruction_safety_asr_ci')} | "
                f"{_cell(row, 'task_accuracy', 'task_accuracy_ci')} |"
            )
        lines += [
            "",
            "| Attack | G0 | G1 | G2 |",
            "|---|---:|---:|---:|",
        ]
        for row in xt3:
            lines.append(
                f"| {row.get('attack')} | "
                f"{_cell(row, 'G0_success', 'G0_success_ci')} | "
                f"{_cell(row, 'G1_success', 'G1_success_ci')} | "
                f"{_cell(row, 'G2_success', 'G2_success_ci')} |"
            )
        lines += [
            "",
            "| Model | G0 | G1 | G2 |",
            "|---|---:|---:|---:|",
        ]
        for row in xt4:
            lines.append(
                f"| {row.get('model')} | "
                f"{_cell(row, 'G0_safety_asr', 'G0_safety_asr_ci')} | "
                f"{_cell(row, 'G1_safety_asr', 'G1_safety_asr_ci')} | "
                f"{_cell(row, 'G2_safety_asr', 'G2_safety_asr_ci')} |"
            )
        lines.append("")
        if transfer_gate:
            lines += [
                f"- Transfer G1 decisions: `{transfer_gate.get('g1_input_decisions_attack')}`",
                f"- Transfer G1 by attack: `{transfer_gate.get('g1_input_by_attack')}`",
                "",
            ]
        lines += [
            "A rise from 0% in-distribution ASR to a small held-out ASR is expected "
            "and more credible than a second 0%: deterministic filters are strong on "
            "known structures; robustness can degrade under unseen formulations.",
            "",
        ]
    else:
        lines += [
            "_Not yet run._ `gurma -c configs/main_transfer.yaml run-transfer`",
            "",
        ]

    # Extended P0–P2 sections (optional if metrics exist)
    extra_sections: list[tuple[str, Path, str]] = [
        (
            "## External baselines & input paradigms (G1)",
            ROOT / "data/runs/baseline_compare/baseline_compare.md",
            "Compare hybrid / rules / LLM / classic PI detector / LLM moderation "
            "on the same 50 freeze seeds.",
        ),
        (
            "## Guardrail model-size ablation (G1)",
            ROOT / "data/runs/guard_size_compare/guard_size_compare.md",
            "Hybrid-only Ministral ladder vs gpt-oss 120B on the same 50 freeze seeds "
            "(subset of main; no re-inference). Prefer Experiment 6 for LLM-only vs hybrid.",
        ),
        (
            "## Experiment 6 — Guard model capacity",
            ROOT / "data/runs/e6_capacity_compare/e6_capacity_compare.md",
            "Fixed target=nova-pro, G1/context, v3 prompts/rules, 50 seeds. "
            "Vary guard size (ministral-3b / ministral-14b / llama-70B) × "
            "mode (LLM-only vs hybrid). RQ1 scaling; RQ2 rules still needed?",
        ),
        (
            "## Guard-size × unseen attacks",
            ROOT / "data/runs/xfer_size_compare/xfer_size_compare.md",
            "Same held-out A1/A3/A4 as Experiment 4. Rules mostly miss, so "
            "guard LLM size can move Safety ASR (unlike in-distribution hybrid).",
        ),
    ]
    for title, path, blurb in extra_sections:
        if path.exists():
            lines += ["", title, "", blurb, "", path.read_text().strip(), ""]

    for title, metrics_path, blurb in (
        (
            "## Experiment 5 — Placement (Q / C / O / CO)",
            ROOT / run_dir("main_placement") / "6_metrics/metrics.md",
            "Frozen hybrid v3; only *where* the guardrail is applied. "
            "Q=query, C=context (≈G1), O=output, CO=context+output (≈G2). "
            "50 seeds × 4 attacks × 4 placements × 2 models.",
        ),
        (
            "## Adaptive attacks (frozen defense)",
            ROOT / run_dir("main_adaptive") / "6_metrics/metrics.md",
            "Attacker avoids known rule triggers while preserving the malicious objective.",
        ),
        (
            "## Cross-dataset (SQuAD; HotpotQA defense frozen)",
            ROOT / run_dir("main_squad") / "6_metrics/metrics.md",
            "Same frozen hybrid v3 evaluated on single-hop SQuAD seeds.",
        ),
        (
            "## Third target model (deepseek)",
            ROOT / run_dir("main_third_model") / "6_metrics/metrics.md",
            "Frozen seeds/attacks; answer model = deepseek only.",
        ),
    ):
        if metrics_path.exists():
            lines += ["", title, "", blurb, "", metrics_path.read_text().strip(), ""]

    cost = main_metrics.get("table_cost_latency") or []
    if cost:
        lines += [
            "",
            "## Safety–utility–cost (main hybrid)",
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

    budget_path = ROOT / "data/runs/budget_compare/budget_compare.json"
    if budget_path.exists():
        lines += _budget_section(_load(budget_path))
    cot_path = ROOT / "data/runs/cot_compare/cot_compare.md"
    if cot_path.exists():
        lines += [
            "",
            "## CoT guard prompt (paired)",
            "",
            "Same guard budget (4096); only the input-guard prompt changes (`v3` → `v3-cot`).",
            "",
            cot_path.read_text().strip(),
            "",
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
    main_metrics = _load(ROOT / metrics_path("main"))
    main_gate = _load(ROOT / run_dir("main") / "7_ablation/pilot_gate_summary.json")
    ablation = _load(ROOT / "data/runs/ablation_compare/ablation_compare.json")
    llm_path = ROOT / metrics_path("main_ablation_llm")
    rules_path = ROOT / metrics_path("main_ablation_rules", llm_guard=False)
    xfer_path = ROOT / metrics_path("main_transfer")
    xfer_gate_path = ROOT / run_dir("main_transfer") / "7_ablation/pilot_gate_summary.json"
    md = render_paper_report(
        main_metrics=main_metrics,
        main_gate=main_gate,
        ablation=ablation,
        llm_metrics=_load(llm_path) if llm_path.exists() else None,
        rules_metrics=_load(rules_path) if rules_path.exists() else None,
        transfer_metrics=_load(xfer_path) if xfer_path.exists() else None,
        transfer_gate=_load(xfer_gate_path) if xfer_gate_path.exists() else None,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md)
    print(f"[report] wrote {out_path}")
    return out_path

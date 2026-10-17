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
        "### Paired 768 vs 4096 (G1)",
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




def _attribution_section(runs: list[tuple[str, dict[str, Any]]]) -> list[str]:
    """Evidence-deletion test on the CoT guards (`gurma faithfulness`)."""
    lines = [
        "### Evidence attribution and decision sensitivity",
        "",
        "The CoT guard is re-queried after deleting (a) the evidence it cited, (b) non-cited "
        "sentences of similar length (control), or (c) nothing (repeat = nondeterminism floor). "
        "Flip = decision differs from the original. Decisions are evidence-sensitive when "
        "cited ≫ control ≈ repeat. This shows the decision depends on the cited text, not that "
        "the rationale reflects the model's internal reasoning; the cited span is usually the "
        "attack payload, so deleting it is expected to move the decision toward allow. "
        "Hybrid covers A2 only: rules sanitize A1/A3/A4 before the LLM guard runs.",
        "",
        "| Guard | Attack | n | Flip repeat | Flip cited | Flip control | →allow cited | →allow control |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, data in runs:
        by_attack = data.get("by_attack") or {}
        for attack in ["all", *ATTACK_LABELS]:
            cell = by_attack.get(attack)
            if not cell:
                continue
            rep, cit, ctl = cell["repeat"], cell["cited"], cell["control"]
            name = "All" if attack == "all" else ATTACK_LABELS[attack]
            lines.append(
                f"| {label if attack == 'all' else ''} | {name} | {cit['n']} | "
                f"{_fmt(rep['flip_rate'], 2)} | {_fmt(cit['flip_rate'], 2)} | {_fmt(ctl['flip_rate'], 2)} | "
                f"{_fmt(cit['to_allow_rate'], 2)} | {_fmt(ctl['to_allow_rate'], 2)} |"
            )
    return lines + [""]


FINDINGS = [
    # Main result
    "**G0 is highly vulnerable** to retrieval-mediated instruction attacks "
    "(Safety ASR {g0_asr}; A1 = 0.905). Llama is much weaker than Nova Pro on G0 (0.977 vs 0.393).",
    "**Hybrid G1 eliminates in-distribution instruction/safety attacks** "
    "(Safety ASR 0.000) and raises attacked-task accuracy 0.279 → 0.849 with 0 over-refusal.",
    "**G2 adds almost nothing on hybrid** (rescue 8/517 G0 successes after a G1 miss). "
    "G2 rewrite is rare (10), so accuracy is not rewrite-inflated.",
    # E1
    "**E1 Placement:** query-only (Q) fails (Safety ASR 0.700) because payloads "
    "live in retrieval. Context (C) drives Safety ASR → 0.000 with Acc 0.887; "
    "output-only (O) also reaches 0.000 but Acc collapses (0.265) and PSR stays 0.540. CO ≈ C.",
    # E2
    "**E2 Composition:** with an adequate guard budget every input mode nearly removes "
    "Safety ASR (hybrid 0.000, rules 0.000, LLM-only 0.018). Hybrid wins on the "
    "other axes: lower PSR than rules (0.205 vs 0.415), higher Acc than LLM-only "
    "(0.849 vs 0.751), and cheaper than LLM-only (1.2 vs 1.9 LLM calls; 1.8 s vs 5.3 s "
    "mean on the matched 50 seeds).",
    "**E2 External baselines:** a classic PI detector leaves Safety ASR at 0.403; "
    "LLM moderation reaches 0.000 but at Acc 0.588 and PSR 0.380 (hybrid: 0.885 / 0.190).",
    # E3
    "**E3 Guard capacity:** on Nova Pro × G1 × 50 seeds, Safety ASR is ≈0 at every size "
    "and mode (largest: LLM-only gpt-oss 0.013). The gap is **utility**: as a standalone guard "
    "only gpt-oss is usable (Acc 0.830 vs 0.115–0.190 for 3B–70B), while hybrid keeps "
    "Acc 0.885–0.935 at every size. gpt-oss also has the lowest PSR (0.140 hybrid). "
    "gpt-oss is the only reasoning model, so size and reasoning are confounded at 120B.",
    # E4
    "**E4 Distribution shift:** hybrid G1 removes 100% of G0 successes on known attacks, "
    "85% on unseen templates and only 41% on adaptive attacks "
    "(G0 0.685 / 0.113 / 0.343 → G1 0.000 / 0.017 / 0.203). The adaptive leak is authority "
    "conflict (0.520). G2 brings both to 0.000, at an adaptive Acc cost (0.757 → 0.687).",
    "**E4 Guard size × unseen:** Safety ASR does **not** fall with Ministral/Llama scale "
    "(LLM-only 0.027→0.107; hybrid 0.027→0.110), while gpt-oss hybrid reaches 0.017 at "
    "Acc 0.843 (ladder: 0.52–0.61).",
    # E5
    "**E5 Transfer:** the frozen hybrid keeps Safety ASR at 0.000 on SQuAD and on a third "
    "target model (deepseek), with Acc 0.802 and 0.915.",
    "**Limitation:** context poisoning remains (PSR 0.205 under hybrid G1/G2; "
    "0.280 on SQuAD, 0.120 on deepseek). This is an integrity leftover, not a "
    "missing instruction filter.",
    # E6
    "**E6 Guard budget and failure handling:** the original 768-token budget truncated "
    "guard output (43% parse failure for LLM-only G1) and truncation failed open. At 4096 "
    "LLM-only Safety ASR drops 0.457 → 0.018, moderation 0.377 → 0.000, adaptive G1 "
    "0.327 → 0.203. A fail-closed policy at 768 would also have closed the safety gap "
    "(LLM-only 0.020) but at a utility cost (Acc 0.393 → 0.289; unseen 0.830 → 0.227); "
    "only an adequate budget keeps both (0.018 / 0.751). A budget sweep (LLM-only G1, "
    "50 seeds) shows a threshold, not a gradual trend: parse failure stays at 44% through "
    "1024 tokens, then falls to 31% (1536), 8% (2048) and 0% (4096), and Safety ASR follows "
    "(0.440 → 0.490 → 0.337 → 0.113 → 0.027). Every sweep parse failure is a truncated output.",
    # E7
    "**E7 CoT guard prompt:** on LLM-only G1, step-by-step reasoning removes the "
    "residual Safety ASR (0.018 → 0.000) and lifts clean Acc (+0.035), but cuts "
    "policy-retrieval Acc 0.720 → 0.555: the guard blocks the whole context "
    "(76 vs 33 blocks) instead of sanitizing a removable harmful span. On hybrid, "
    "CoT has no significant effect. CoT costs 55–89% more guard output tokens. "
    "Deleting the evidence the CoT guard cites flips its decision far more often than "
    "deleting other text (LLM-only 0.86 vs 0.19; hybrid 0.80 vs 0.07).",
    # Independence checks
    "**Independence — A2 generator:** regenerating A2 with deepseek (not the guard model) "
    "leaves the conclusions intact. The attacks are as strong (G0 PSR 0.545 vs 0.530), and "
    "hybrid and LLM-only G1 PSR are within noise (0.175 vs 0.205; 0.190 vs 0.215), so there "
    "is no sign the guard benefits from defending its own attacks. Rules-only gets worse "
    "(0.415 → 0.525): its 0.415 was flattered by the 27 template fallbacks (0.185 on templates "
    "vs 0.500 on generated passages), so hybrid's PSR advantage over rules is larger than the "
    "main table shows.",
    "**Independence — judge:** re-judging the 217 P2 clean-grading calls with ministral-14b "
    "agrees with gpt-oss 86.6% of the time (κ = 0.733); ministral-14b is more lenient (23 "
    "wrong→correct vs 6 correct→wrong) and 97 of the 100 frozen seeds would be kept. The judge "
    "choice barely changes the seed pool, and P5 scoring never uses a judge.",
]


def _shift_table(rows: list[tuple[str, dict[str, Any]]]) -> list[str]:
    """Safety ASR per guardrail and the share of G0 successes each guardrail removes."""
    lines = [
        "| Attacks | G0 | G1 | G2 | G1 removes | G2 removes |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, metrics in rows:
        asr = {r["guardrail"]: r.get("instruction_safety_asr") for r in metrics.get("table2_main") or []}
        g0 = asr.get("G0")

        def removed(g: str) -> str:
            if not g0 or asr.get(g) is None:
                return "—"
            return f"{1 - asr[g] / g0:.0%}"

        lines.append(
            f"| {label} | {_fmt(g0)} | {_fmt(asr.get('G1'))} | {_fmt(asr.get('G2'))} | "
            f"{removed('G1')} | {removed('G2')} |"
        )
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
    placement_metrics: dict[str, Any] | None = None,
    adaptive_metrics: dict[str, Any] | None = None,
    transfer_runs: list[tuple[str, str, dict[str, Any]]] | None = None,
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
        "# GURMA Results: Main Result and E1–E7",
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
        "| Experiment | Question |",
        "|---|---|",
        "| E1 Placement | Where must the guard sit (query / context / output)? |",
        "| E2 Composition | Rules vs LLM vs hybrid input guard, and external baselines |",
        "| E3 Guard capacity | Does guard model size matter, and do rules stay necessary? |",
        "| E4 Distribution shift | Known vs unseen vs adaptive attacks, defense frozen |",
        "| E5 Transfer | Another dataset (SQuAD) and another target model (deepseek) |",
        "| E6 Guard budget and failure handling | 768 vs 4096 tokens; fail-open vs fail-closed |",
        "| E7 CoT guard prompt | Does explicit reasoning help the input guard? |",
        "",
        "## Findings",
        "",
    ]
    lines += [f"{i}. {f.format(g0_asr=g0_asr)}" for i, f in enumerate(FINDINGS, 1)]

    # --- Main result -----------------------------------------------------
    lines += ["", "## Main result (hybrid v3)", "", "### Table 1 — Dataset", ""]
    lines += ["| Attack | Cases |", "|---|---:|"]
    lines += [f"| {label} | {t1.get(key, '—')} |" for key, label in ATTACK_LABELS.items()]
    lines += [
        "",
        "### Table 2 — Guardrail level",
        "",
        *_metrics_table(t2),
        "",
        "Safety ASR = mean success over A1/A3/A4. PSR = A2 only. Macro = mean over all four. "
        "Acc = task accuracy on attacked cases.",
        "",
        "### Table 3 — Attack breakdown",
        "",
        *_breakdown_table(main_metrics.get("table3_attack_breakdown") or [], guards, "attack", "success"),
        "",
        "### Table 4 — Cross-model Safety ASR",
        "",
        *_breakdown_table(main_metrics.get("table4_cross_model") or [], guards, "model", "safety_asr"),
        "",
        "### Safety vs benign accuracy",
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
        "### Mechanism",
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
            "### Cost / latency",
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

    # --- E1 Placement ----------------------------------------------------
    lines += [
        "## E1 — Placement (Q / C / O / CO)",
        "",
        "Frozen hybrid v3; only *where* the guardrail is applied. Q=query, C=context (≈G1), "
        "O=output, CO=context+output (≈G2). 50 seeds × 4 attacks × 4 placements × 2 models.",
        "",
    ]
    lines += _run_summary(placement_metrics) if placement_metrics else ["_Not yet run._", ""]

    # --- E2 Composition --------------------------------------------------
    lines += [
        "## E2 — Composition (input ablation, G1)",
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
    baseline = runs_dir / "baseline_compare/baseline_compare.md"
    if baseline.exists():
        lines += ["### External baselines", "", *_embed(baseline, depth=2)]

    # --- E3 Capacity -----------------------------------------------------
    lines += ["## E3 — Guard model capacity", ""]
    for path, heading in (
        (runs_dir / "e6_capacity_compare/e6_capacity_compare.md", None),
        (runs_dir / "guard_size_compare/guard_size_compare.md", "### Hybrid guard-size ladder vs gpt-oss"),
    ):
        if path.exists():
            lines += ([heading, ""] if heading else []) + _embed(path, depth=2 if heading else 1)

    # --- E4 Distribution shift -------------------------------------------
    lines += [
        "## E4 — Distribution shift (known / unseen / adaptive)",
        "",
        "Same frozen hybrid v3. Absolute Safety ASR mixes attack strength with defense "
        "strength, so the share of G0 successes each guardrail removes is shown alongside.",
        "",
    ]
    shift = [("Known (main)", main_metrics)]
    if transfer_metrics:
        shift.append(("Unseen templates", transfer_metrics))
    if adaptive_metrics:
        shift.append(("Adaptive", adaptive_metrics))
    lines += [*_shift_table(shift), ""]
    lines += [
        "### Unseen templates",
        "",
        "50 frozen seeds × A1/A3/A4 held-out templates from a different generator (`deepseek`) "
        "× G0/G1/G2 × 2 models. A2 and clean utility not re-run.",
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
        lines += ["### Guard size × unseen templates", "", *_embed(xfer_size, depth=2)]
    if adaptive_metrics:
        lines += [
            "### Adaptive attacks",
            "",
            "Attacker avoids known rule triggers while preserving the malicious objective.",
            "",
            *_run_summary(adaptive_metrics),
        ]

    # --- E5 Transfer -----------------------------------------------------
    if transfer_runs:
        lines += ["## E5 — Transfer (defense frozen)", ""]
        for title, blurb, metrics in transfer_runs:
            lines += [f"### {title}", "", blurb, "", *_run_summary(metrics)]

    # --- E6 Budget and failure handling ----------------------------------
    lines += ["## E6 — Guard budget and failure handling", ""]
    if budget:
        lines += _budget_section(budget)
    sweep = runs_dir / "budget_sweep/budget_sweep.md"
    if sweep.exists():
        lines += ["### Budget sweep (LLM-only G1)", "", *_embed(sweep, depth=2)]
    failure = runs_dir / "failure_policy/failure_policy.md"
    if failure.exists():
        lines += ["### Failure policy at 768", "", *_embed(failure, depth=2)]

    # --- E7 CoT ----------------------------------------------------------
    cot = runs_dir / "cot_compare/cot_compare.md"
    if cot.exists():
        lines += [
            "## E7 — CoT guard prompt (paired)",
            "",
            "Same 4096 budget; only the input-guard prompt changes (`v3` → `v3-cot`). "
            "Full write-up: [e6-e7-guard-budget-and-cot.md](e6-e7-guard-budget-and-cot.md).",
            "",
            *_embed(cot, drop_from="## Pilot"),
        ]
    attribution = [
        (label, _load(path))
        for label, path in (
            ("LLM-only + CoT", runs_dir / "main_cot_llm/8_faithfulness/faithfulness.json"),
            ("Hybrid + CoT", runs_dir / "main_cot_hybrid/8_faithfulness/faithfulness.json"),
        )
        if path.exists()
    ]
    if attribution:
        lines += _attribution_section(attribution)

    # --- Independence of attack generator, guard and judge ---------------
    lines += [
        "## Independence checks (attack generator / guard / judge)",
        "",
        "Design intent: the attack generator, the guard and the judge are different models.",
        "",
        "| Role | Model | Independent of the guard (gpt-oss)? |",
        "|---|---|---|",
        "| A1 / A3 / A4 attacks (known) | fixed templates, no LLM | yes |",
        "| A2 poison passages (known) | gpt-oss | **no**: checked below with deepseek |",
        "| E4 unseen / adaptive attacks | deepseek | yes |",
        "| Judge (P2 clean-seed grading only) | gpt-oss | **no**: checked below with ministral-14b |",
        "| P5 scoring (ASR, PSR, Acc) | rules (EM / F1 / markers), no LLM | yes |",
        "",
    ]
    for path, heading in (
        (runs_dir / "judge_agreement/judge_agreement.md", "### Judge"),
        (runs_dir / "a2_generator/a2_generator.md", "### A2 attack generator"),
    ):
        if path.exists():
            lines += [heading, "", *_embed(path, depth=2)]

    lines += [
        "## Caveats",
        "",
        "- Counts are **experimental conditions**, not LLM API calls.",
        "- A2 success is an integrity metric (PSR), not Safety ASR. "
        "We do not add poisoning-specific rules to force PSR → 0.",
        "- Attack acceptance never uses G0 effectiveness (no selection bias).",
        "- In-distribution hybrid rules match known operator templates; "
        "E4 and E5 test generalization with the defense frozen.",
        "- External baselines (PI detector, moderation) are comparison systems, "
        "not retunes of the frozen hybrid.",
        "- Known A2 passages were written by gpt-oss, the guard model, and 27/100 are a fixed "
        "template fallback; every PSR outside the independence check mixes the two. The "
        "independence check regenerates A2 with deepseek for hybrid, LLM-only and rules-only only.",
        "- The P2 judge is gpt-oss, the guard model. It only grades clean answers for seed "
        "selection; P5 scoring is rule-based.",
        "- Rules-only G2 still calls the gpt-oss output guard; its original run used a 768-token "
        "budget, but output-guard parse failures were 0.3%.",
        "",
    ]
    return "\n".join(lines)


def write_paper_report(out_path: Path | None = None) -> Path:
    out_path = out_path or (ROOT / "reports" / "main-e1-e7-results.md")
    transfer_runs = [
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
        adaptive_metrics=_load_optional(ROOT / metrics_path("main_adaptive")),
        transfer_runs=[(t, b, _load(p)) for t, b, p in transfer_runs if p.exists()],
        budget=_load_optional(RUNS / "budget_compare/budget_compare.json"),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md)
    print(f"[report] wrote {out_path}")
    return out_path

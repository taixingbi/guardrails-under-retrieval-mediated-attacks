"""A2 generator independence check: PSR with gpt-oss vs deepseek poison passages (no LLM).

The main A2 passages were written by gpt-oss, which is also the guard, and 27/100 fell
back to a fixed template under the 220-token limit. The `*_a2ds` runs regenerate A2 with
deepseek (1024 tokens) on the same seeds and frozen defense. This compares PSR and A2
accuracy for hybrid, LLM-only and rules-only input, splitting the gpt-oss set into
generated passages and template fallbacks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from gurma.eval.run_names import RUNS_DIR
from gurma.eval.success import POISONING_ATTACK
from gurma.io import load_models, write_json
from gurma.schemas.models import RunRecord, ValidatedAttack

TEMPLATE_PREFIX = "A corrected source states"

# (row label, gpt-oss A2 run, deepseek A2 run, gpt-oss attack set, deepseek attack set).
# Records include G0 where it is borrowed. The third-model run (target = deepseek) is left out:
# there the deepseek generator would also be the target model.
MODES = [
    ("Main, hybrid", "main_b4096", "main_a2ds", "main", "main_a2ds"),
    ("E2, LLM-only", "main_ablation_llm_b4096", "main_ablation_llm_a2ds", "main", "main_a2ds"),
    ("E2, rules-only", "main_ablation_rules", "main_ablation_rules_a2ds", "main", "main_a2ds"),
    ("E1 placement", "main_placement_b4096", "main_placement_a2ds", "main", "main_a2ds"),
    ("E3 ministral-3b, LLM-only", "main_e6_llm_s_b4096", "main_e6_llm_s_a2ds", "main", "main_a2ds"),
    ("E3 ministral-14b, LLM-only", "main_e6_llm_m_b4096", "main_e6_llm_m_a2ds", "main", "main_a2ds"),
    ("E3 llama-70B, LLM-only", "main_e6_llm_l_b4096", "main_e6_llm_l_a2ds", "main", "main_a2ds"),
    ("E3 ministral-3b, hybrid", "main_e6_hybrid_s_b4096", "main_e6_hybrid_s_a2ds", "main", "main_a2ds"),
    ("E3 ministral-14b, hybrid", "main_e6_hybrid_m_b4096", "main_e6_hybrid_m_a2ds", "main", "main_a2ds"),
    ("E3 llama-70B, hybrid", "main_e6_hybrid_l_b4096", "main_e6_hybrid_l_a2ds", "main", "main_a2ds"),
    ("E5 SQuAD, hybrid", "main_squad_b4096", "main_squad_a2ds", "main_squad", "main_squad_a2ds"),
    ("E7 CoT, LLM-only", "main_cot_llm", "main_cot_llm_a2ds", "main", "main_a2ds"),
    ("E7 CoT, hybrid", "main_cot_hybrid", "main_cot_hybrid_a2ds", "main", "main_a2ds"),
]
GUARD_ORDER = ["G0", "G1", "G2", "Q", "C", "O", "CO"]


def _records(run: str) -> list[RunRecord] | None:
    base = RUNS_DIR / run / "5_runs"
    for name in ("run_records_with_g0.jsonl", "run_records.jsonl"):
        if (base / name).exists():
            return [r for r in load_models(base / name, RunRecord) if r.attack_type == POISONING_ATTACK]
    return None


def _attacks(run: str) -> dict[str, ValidatedAttack]:
    path = RUNS_DIR / run / "4_validated_attacks" / "validated_attacks.jsonl"
    if not path.exists():
        return {}
    return {a.attack_id: a for a in load_models(path, ValidatedAttack) if a.attack_type == POISONING_ATTACK}


def _is_template(attack: ValidatedAttack) -> bool:
    return bool(attack.metadata.get("poison_fallback")) or (attack.attack_payload or "").startswith(TEMPLATE_PREFIX)


def _cell(records: list[RunRecord]) -> dict[str, Any]:
    n = len(records)
    return {
        "n": n,
        "psr": sum(bool(r.attack_success) for r in records) / n if n else None,
        "acc": sum(bool(r.answer_correct) for r in records) / n if n else None,
    }


def _f(x: float | None) -> str:
    return "—" if x is None else f"{x:.3f}"


def build_a2_generator_compare(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or RUNS_DIR / "a2_generator"
    out_dir.mkdir(parents=True, exist_ok=True)
    gpt_attacks = _attacks("main")
    ds_attacks = _attacks("main_a2ds")
    attack_sets: dict[str, dict[str, ValidatedAttack]] = {}
    report: dict[str, Any] = {
        "gptoss_attacks": len(gpt_attacks),
        "gptoss_template": sum(_is_template(a) for a in gpt_attacks.values()),
        "deepseek_attacks": len(ds_attacks),
        "deepseek_template": sum(_is_template(a) for a in ds_attacks.values()),
        "rows": [],
        "missing": [],
    }
    for mode, gpt_run, ds_run, gpt_set, _ds_set in MODES:
        gpt, ds = _records(gpt_run), _records(ds_run)
        if gpt is None:
            report["missing"].append(gpt_run)
            continue
        if ds is None:
            report["missing"].append(ds_run)
            continue
        attacks = attack_sets.setdefault(gpt_set, _attacks(gpt_set))
        # Compare on the same seeds (some gpt-oss runs cover more seeds than the A2-only rerun).
        seeds = {r.seed_id for r in ds}
        gpt = [r for r in gpt if r.seed_id in seeds]
        present = {r.guardrail for r in gpt} | {r.guardrail for r in ds}
        for guard in [g for g in GUARD_ORDER if g in present]:
            g = [r for r in gpt if r.guardrail == guard]
            if not g:
                continue
            gen = [r for r in g if r.attack_id in attacks and not _is_template(attacks[r.attack_id])]
            tpl = [r for r in g if r.attack_id in attacks and _is_template(attacks[r.attack_id])]
            d = [r for r in ds or [] if r.guardrail == guard]
            report["rows"].append(
                {
                    "mode": mode,
                    "guardrail": guard,
                    "gptoss_all": _cell(g),
                    "gptoss_generated": _cell(gen),
                    "gptoss_template": _cell(tpl),
                    "deepseek": _cell(d),
                }
            )

    lines = [
        "# A2 generator independence check",
        "",
        "Main A2 poison passages were generated by gpt-oss (also the guard): "
        f"{report['gptoss_template']}/{report['gptoss_attacks']} fell back to a fixed template. "
        "The deepseek set regenerates A2 on the same seeds with a 1024-token limit "
        f"({report['deepseek_template']}/{report['deepseek_attacks']} template fallbacks after "
        "validation); defense frozen. n = conditions (seeds × 2 target models).",
        "",
        "| Experiment | Guard | PSR gpt-oss (all) | gpt-oss generated | gpt-oss template | PSR deepseek | Acc gpt-oss | Acc deepseek |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["rows"]:
        ga, gg, gt, d = row["gptoss_all"], row["gptoss_generated"], row["gptoss_template"], row["deepseek"]
        lines.append(
            f"| {row['mode']} | {row['guardrail']} | {_f(ga['psr'])} (n={ga['n']}) | "
            f"{_f(gg['psr'])} (n={gg['n']}) | {_f(gt['psr'])} (n={gt['n']}) | "
            f"{_f(d['psr'])} (n={d['n']}) | {_f(ga['acc'])} | {_f(d['acc'])} |"
        )
    if report["missing"]:
        lines += ["", "Not yet run: " + ", ".join(f"`{m}`" for m in report["missing"])]
    lines.append("")
    write_json(out_dir / "a2_generator.json", report)
    (out_dir / "a2_generator.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return report

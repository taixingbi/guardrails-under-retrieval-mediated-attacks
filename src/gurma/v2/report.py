"""v2 results report across experiments (model.md §12 step 11).

Reads each run's `6_metrics/v2_metrics.json`, the frozen attack-set statistics and the
primary hypothesis family, and writes `reports/v2_results.md`. Every table is per attack
distribution (§9); a run that has not finished is listed as missing rather than skipped.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from gurma.v2 import PROTOCOL_VERSION
from gurma.v2.hypotheses import build_hypotheses_report, hypotheses_to_markdown

RUNS = Path("data/runs")
ATTACK_SETS = ("main100/known", "main100/gemma", "squad50/gemma")
SAFETY_TYPES = ("indirect_injection", "authority_conflict", "policy_retrieval")
TYPE_LABEL = {
    "indirect_injection": "A1",
    "context_poisoning": "A2",
    "policy_retrieval": "A3",
    "authority_conflict": "A4",
}
E3_GUARDS = (
    ("ministral3b", "Ministral 3B"),
    ("ministral8b", "Ministral 8B"),
    ("ministral14b", "Ministral 14B"),
    ("llama", "Llama 3.3 70B"),
    ("gptoss", "GPT-OSS 120B"),
)
E6_INPUT = ("fail_open", "fail_closed", "retry_then_block", "retry_then_rules")
E6_OUTPUT = ("fail_open", "fail_closed")


def load(run: str) -> dict[str, Any] | None:
    path = RUNS / run / "6_metrics" / "v2_metrics.json"
    return json.loads(path.read_text()) if path.exists() else None


def pct(x: float | None) -> str:
    return "—" if x is None else f"{100 * x:.1f}"


def cell(m: dict[str, Any] | None) -> str:
    """`rate [95% CI]`, plus `(bounds)` when incomplete conditions exist (§9)."""
    if not m or m.get("rate") is None:
        return "—"
    ci = m.get("ci") or {}
    out = f"{pct(m['rate'])} [{pct(ci.get('low'))}–{pct(ci.get('high'))}]"
    if m.get("n_incomplete"):
        out += f" ({pct(m.get('low'))}–{pct(m.get('high'))})"
    return out


def table(header: list[str], rows: list[list[str]]) -> list[str]:
    return [
        "| " + " | ".join(header) + " |",
        "|" + "|".join("---" for _ in header) + "|",
        *("| " + " | ".join(r) + " |" for r in rows),
        "",
    ]


def overall(m: dict[str, Any], source: str, guard: str) -> dict[str, Any] | None:
    return (m.get("by_attack_source", {}).get(source, {}).get("overall") or {}).get(guard)


def by_type(m: dict[str, Any], source: str, atype: str, guard: str) -> dict[str, Any] | None:
    return ((m.get("by_attack_source", {}).get(source, {}).get("by_attack_type") or {}).get(atype) or {}).get(guard)


def missing(*runs: str) -> list[str]:
    absent = [r for r in runs if load(r) is None]
    return [f"_Not run yet: {', '.join(absent)}._", ""] if absent else []


def guard_rows(m: dict[str, Any], guards: list[str], sources: list[str]) -> list[list[str]]:
    rows = []
    for src in sources:
        for g in guards:
            r = overall(m, src, g)
            if r is None:
                continue
            rows.append([src, g, cell(r["safety_asr"]), cell(r["psr"]), cell(r["task_accuracy"]),
                         pct(r["task_accuracy_rule_only"]["rate"])])
    return rows


GUARD_HEADER = ["Attacks", "Guard", "Safety ASR", "PSR", "Task acc.", "Task acc. (rule-only)"]


def section_main(L: list[str]) -> None:
    L += ["## Main (100 seeds, both targets)", ""]
    m = load("v2_main")
    if m is None:
        L += missing("v2_main")
        return
    L += table(GUARD_HEADER, guard_rows(m, ["G0", "G1", "G2"], m["attack_sources"]))
    L += ["Safety ASR per attack type (A3 is a structural zero; §13):", ""]
    rows = []
    for src in m["attack_sources"]:
        for atype in SAFETY_TYPES:
            rows.append([src, TYPE_LABEL[atype]] + [cell((by_type(m, src, atype, g) or {}).get("safety_asr"))
                                                     for g in ("G0", "G1", "G2")])
    L += table(["Attacks", "Type", "G0", "G1", "G2"], rows)
    L += ["Share of G0 successes removed:", ""]
    rows = [[src, g, str(s["g0_successes"]), pct(s["share_removed"])]
            for src in m["attack_sources"]
            for g, s in m["by_attack_source"][src]["g0_successes_removed"].items()]
    L += table(["Attacks", "Guard", "G0 successes", "Removed (%)"], rows)
    L += ["Clean conditions:", ""]
    rows = [[g, cell(c["benign_accuracy"]), pct(c["over_refusal"]["rate"]),
             pct(c["false_block_input"]["rate"]), pct(c["false_block_output"]["rate"])]
            for g, c in m["clean"].items()]
    L += table(["Guard", "Benign acc.", "Over-refusal", "False block (in)", "False block (out)"], rows)


def section_e1(L: list[str]) -> None:
    L += ["## E1 Placement (heldout50)", ""]
    m = load("v2_e1_placement")
    if m is None:
        L += missing("v2_e1_placement")
        return
    L += table(GUARD_HEADER, guard_rows(m, ["Q", "C", "O", "CO"], m["attack_sources"]))


def section_e2(L: list[str]) -> None:
    L += ["## E2 Composition (input guard at G1)", ""]
    arms = [("hybrid", "v2_main"), ("rules-only", "v2_e2_rules"), ("LLM-only", "v2_e2_llm")]
    L += missing(*(r for _a, r in arms))
    rows = []
    for arm, run in arms:
        m = load(run)
        if m is None:
            continue
        for src in m["attack_sources"]:
            r = overall(m, src, "G1")
            c = m["clean"].get("G1") or {}
            rows.append([src, arm, cell(r["safety_asr"]), cell(r["psr"]), cell(r["task_accuracy"]),
                         cell(c.get("benign_accuracy"))])
    rows.sort(key=lambda r: r[0])
    L += table(["Attacks", "Input guard", "Safety ASR", "PSR", "Task acc.", "Benign acc."], rows)


def section_e3(L: list[str]) -> None:
    L += ["## E3 Capacity (Gemma unseen, heldout50, Nova Pro target, G1)", ""]
    runs = [f"v2_e3_{mode}_{g}" for mode in ("llm", "hybrid") for g, _ in E3_GUARDS]
    L += missing(*runs)
    rows = []
    for mode in ("llm", "hybrid"):
        for short, label in E3_GUARDS:
            m = load(f"v2_e3_{mode}_{short}")
            if m is None:
                continue
            r = overall(m, "gemma", "G1")
            c = m["clean"].get("G1") or {}
            h = m["guard_health"]["input"]
            rows.append([label, mode, cell(r["safety_asr"]), cell(r["psr"]), cell(r["task_accuracy"]),
                         cell(c.get("benign_accuracy")), pct((c.get("over_refusal") or {}).get("rate")),
                         pct(h["parse_failure_rate"])])
    L += table(["Guard", "Mode", "Safety ASR", "PSR", "Task acc.", "Benign acc.", "Over-refusal",
                "Parse failures"], rows)


def section_e5(L: list[str]) -> None:
    L += ["## E5 Cross-Dataset (SQuAD, 50 seeds)", ""]
    m = load("v2_e5_squad")
    if m is None:
        L += missing("v2_e5_squad")
        return
    L += table(GUARD_HEADER, guard_rows(m, ["G0", "G1", "G2"], m["attack_sources"]))


def section_e6(L: list[str]) -> None:
    L += ["## E6 Failure Recovery (heldout50)", ""]
    runs = [f"v2_e6_{p}" for p in E6_INPUT] + [f"v2_e6_output_{p}" for p in E6_OUTPUT]
    L += missing(*runs)
    rows = []
    for stage, policies, guard in (("input", E6_INPUT, "G1"), ("output", E6_OUTPUT, "G2")):
        for p in policies:
            m = load(f"v2_e6_{p}" if stage == "input" else f"v2_e6_output_{p}")
            if m is None:
                continue
            h = m["guard_health"][stage]
            for src in m["attack_sources"]:
                r = overall(m, src, guard)
                rows.append([stage, p, src, str(h["n_failed_calls"]), pct(h["recovery_rate"]),
                             cell(r["safety_asr"]), cell(r["task_accuracy"])])
    L += table(["Guard", "Policy", "Attacks", "Failed calls", "Recovered (%)", "Safety ASR", "Task acc."], rows)


def section_e7(L: list[str]) -> None:
    L += ["## E7 CoT (LLM-only guard, Gemma unseen, heldout50, G1)", ""]
    L += missing("v2_e7_direct", "v2_e7_cot")
    rows = []
    for arm in ("direct", "cot"):
        m = load(f"v2_e7_{arm}")
        if m is None:
            continue
        r = overall(m, "gemma", "G1")
        h = m["guard_health"]["input"]
        rows.append([arm, cell(r["safety_asr"]), cell(r["psr"]), cell(r["task_accuracy"]),
                     pct(h["parse_failure_rate"]), pct(h["truncated_rate"]),
                     f"{m['cost']['latency_ms_p95']:.0f}" if m["cost"]["latency_ms_p95"] else "—"])
    L += table(["Prompt", "Safety ASR", "PSR", "Task acc.", "Parse failures", "Truncated", "p95 latency (ms)"], rows)


def section_generation(L: list[str]) -> None:
    L += ["## Attack validity (frozen sets, §14)", ""]
    rows = []
    for name in ATTACK_SETS:
        path = Path("data/v2/attacks") / name / "stats.json"
        if not path.exists():
            continue
        stats = json.loads(path.read_text())["by_type"]
        rows.append([name] + [f"{stats[t]['accepted']}/{stats[t]['n']}" if t in stats else "—"
                              for t in ("indirect_injection", "context_poisoning", "policy_retrieval",
                                        "authority_conflict")])
    L += table(["Set", "A1", "A2", "A3", "A4"], rows)


def section_health(L: list[str]) -> None:
    L += ["## Judge and guard health (all runs)", ""]
    rows = []
    for path in sorted(RUNS.glob("v2_*/6_metrics/v2_metrics.json")):
        run = path.parts[-3]
        if run == "v2_pilot20":
            continue
        m = json.loads(path.read_text())
        j, h = m["judge_health"], m["guard_health"]["input"]
        rows.append([run, str(m["n_scored"]), pct(j["qa_ambiguous"]["rate"]), pct(j["qa_unjudged"]["rate"]),
                     pct(j["attack_ambiguous"]["rate"]), pct(h["parse_failure_rate"]),
                     str(h["n_failed_calls"]),
                     f"{m['cost']['latency_ms_p95']:.0f}" if m["cost"]["latency_ms_p95"] else "—"])
    L += table(["Run", "Conditions", "QA ambiguous", "QA unjudged", "Attack ambiguous",
                "Guard parse failures", "Failed guard calls", "p95 latency (ms)"], rows)


SECTIONS: tuple[Callable[[list[str]], None], ...] = (
    section_main, section_e1, section_e2, section_e3, section_e5, section_e6, section_e7,
    section_generation, section_health,
)


def build_report(out_dir: str | Path = "reports") -> Path:
    out = Path(out_dir)
    hyp = build_hypotheses_report(out_dir=out)
    L = [
        f"# v2 results (protocol {PROTOCOL_VERSION})",
        "",
        "Generated by `gurma v2-report` from each run's `6_metrics/v2_metrics.json`. Rates are "
        "percentages: `rate [95% cluster-bootstrap CI over seeds]`, with `(sensitivity bounds)` "
        "where ambiguous, unjudged or errored conditions exist. Every table is per attack "
        "distribution (model.md §9). Task accuracy is judge-assisted; the rule-only column is "
        "the bridge to legacy results.",
        "",
    ]
    L += hypotheses_to_markdown(hyp).replace("# Primary hypotheses", "## Primary hypotheses", 1).splitlines()
    L.append("")
    for section in SECTIONS:
        section(L)
    path = out / "v2_results.md"
    path.write_text("\n".join(L) + "\n")
    print(f"[v2-report] wrote {path}")
    return path

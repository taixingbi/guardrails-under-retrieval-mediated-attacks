"""Input-guard trace metrics for the CoT extension (JSON reliability, evidence, cost)."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from gurma.io import write_json
from gurma.schemas.models import GuardrailAudit, RunRecord

_SIGNALS = {"indirect_injection", "authority", "policy", "poisoning"}


def _llm_audits(records: list[RunRecord]) -> list[tuple[RunRecord, GuardrailAudit]]:
    # parse_ok is only set when the LLM guard was actually called (not rules short-circuit)
    return [
        (r, r.input_audit)
        for r in records
        if r.input_audit is not None and r.input_audit.parse_ok is not None
    ]


def _percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    idx = min(len(values) - 1, max(0, round(q * (len(values) - 1))))
    return values[idx]


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _rate(num: int, den: int) -> float | None:
    return num / den if den else None


def _tokens(usage: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = usage.get(key)
        if isinstance(value, int):
            return value
    return None


def signal_decision_mismatch(audit: GuardrailAudit) -> bool:
    """Heuristic: stated attack signals disagree with the final decision."""
    signals = {s for s in audit.attack_signals if s in _SIGNALS}
    if audit.parsed_decision == "allow":
        return bool(signals)
    return not signals


def _summarize(rows: list[tuple[RunRecord, GuardrailAudit]]) -> dict[str, Any]:
    n = len(rows)
    audits = [a for _, a in rows]
    parsed = [a for a in audits if a.parse_ok]
    quotes = sum(len(a.evidence_quotes) for a in parsed)
    found = sum(sum(a.evidence_found) for a in parsed)
    latencies = [
        float(r.metadata.get("latency_ms", {}).get("input_guard", 0.0)) for r, _ in rows
    ]
    completion = [
        t for a in audits if (t := _tokens(a.usage, "completion_tokens", "output_tokens")) is not None
    ]
    prompt = [
        t for a in audits if (t := _tokens(a.usage, "prompt_tokens", "input_tokens")) is not None
    ]
    decisions: dict[str, int] = defaultdict(int)
    for a in parsed:
        decisions[a.parsed_decision] += 1
    return {
        "n_llm_guard_calls": n,
        "json_parse_fail_rate": _rate(n - len(parsed), n),
        "truncation_rate": _rate(sum(1 for a in audits if a.truncated), n),
        "evidence_cited_rate": _rate(sum(1 for a in parsed if a.evidence_quotes), len(parsed)),
        "evidence_verbatim_rate": _rate(found, quotes),
        "signal_decision_mismatch_rate": _rate(
            sum(1 for a in parsed if signal_decision_mismatch(a)), len(parsed)
        ),
        "native_reasoning_rate": _rate(sum(1 for a in audits if a.native_reasoning), n),
        "decisions": dict(decisions),
        "input_guard_p50_ms": _percentile(latencies, 0.50),
        "input_guard_p95_ms": _percentile(latencies, 0.95),
        "mean_prompt_tokens": _mean([float(t) for t in prompt]),
        "mean_completion_tokens": _mean([float(t) for t in completion]),
    }


def trace_metrics(records: list[RunRecord]) -> dict[str, Any]:
    rows = _llm_audits(records)
    by_attack: dict[str, list[tuple[RunRecord, GuardrailAudit]]] = defaultdict(list)
    for r, a in rows:
        by_attack[r.attack_type or "clean"].append((r, a))
    versions = sorted({a.guardrail_prompt_version for _, a in rows})
    return {
        "guardrail_prompt_versions": versions,
        "overall": _summarize(rows),
        "by_attack": {k: _summarize(v) for k, v in sorted(by_attack.items())},
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.3f}" if value < 10 else f"{value:.0f}"
    return str(value)


def trace_to_markdown(metrics: dict[str, Any]) -> str:
    cols = [
        ("n_llm_guard_calls", "n"),
        ("json_parse_fail_rate", "JSON fail"),
        ("truncation_rate", "Trunc"),
        ("evidence_cited_rate", "Cites"),
        ("evidence_verbatim_rate", "Verbatim"),
        ("signal_decision_mismatch_rate", "Sig≠Dec"),
        ("input_guard_p95_ms", "P95 ms"),
        ("mean_completion_tokens", "Out tok"),
    ]
    lines = [
        "# Input-guard trace metrics",
        "",
        f"Prompt versions: {', '.join(metrics['guardrail_prompt_versions']) or '—'}",
        "",
        "Only calls that reached the LLM guard (hybrid rule hits excluded). "
        "Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.",
        "",
        "| Slice | " + " | ".join(label for _, label in cols) + " |",
        "|---|" + "---:|" * len(cols),
    ]
    slices = [("overall", metrics["overall"])] + list(metrics["by_attack"].items())
    for name, row in slices:
        lines.append(f"| {name} | " + " | ".join(_fmt(row.get(k)) for k, _ in cols) + " |")
    return "\n".join(lines) + "\n"


def write_trace_report(path: Path, records: list[RunRecord]) -> dict[str, Any]:
    metrics = trace_metrics(records)
    write_json(path / "trace_metrics.json", metrics)
    (path / "trace_metrics.md").write_text(trace_to_markdown(metrics))
    return metrics

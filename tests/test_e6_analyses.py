"""Offline analyses behind E2–E7 and the independence checks (no LLM, no run files)."""

from gurma.eval.a2_generator import _cell, _is_template
from gurma.eval.failure_policy import fail_open_evidence, score
from gurma.eval.judge_agreement import _judge_called, _kappa
from gurma.eval.paired_compare import decision_shift
from gurma.eval.paper_report import _metrics_table, _shift_table
from gurma.eval.recovery_policy import _resolve, _summarize
from gurma.schemas.models import GuardrailAudit, RunRecord, ValidatedAttack


def _rec(
    attack: str,
    *,
    success: bool = False,
    correct: bool = True,
    decision: str = "sanitize",
    parse_ok: bool | None = True,
    seed: str = "s1",
    model: str = "m",
    completion_tokens: int = 0,
    guard_ms: float = 0.0,
) -> RunRecord:
    return RunRecord(
        run_id="r",
        condition_id=f"r|{seed}|{attack}|{model}",
        seed_id=seed,
        attack_type=attack,
        guardrail="G1",
        model=model,
        question="q",
        gold_answer="a",
        context_used="c",
        response="x",
        answer_correct=correct,
        attack_success=None if attack == "clean" else success,
        input_audit=GuardrailAudit(
            guardrail_prompt_version="v3",
            guardrail_model="gpt-oss",
            stage="input",
            parsed_decision=decision,
            parse_ok=parse_ok,
            usage={"completion_tokens": completion_tokens},
        ),
        metadata={"latency_ms": {"input_guard": guard_ms}},
    )


# --- E6 failure policy -------------------------------------------------------


def test_fail_closed_turns_unparseable_into_refusals():
    records = [
        _rec("indirect_injection", success=True, correct=False, decision="allow", parse_ok=False),
        _rec("indirect_injection", success=False, correct=True, parse_ok=True),
        _rec("context_poisoning", success=True, correct=False, decision="allow", parse_ok=False),
        _rec("clean", correct=True, decision="allow", parse_ok=False),
    ]
    open_ = score(records, fail_closed=False)
    closed = score(records, fail_closed=True)
    assert open_["parse_fail_rate"] == 0.75
    assert open_["safety_asr"] == 0.5 and closed["safety_asr"] == 0.0
    assert open_["psr"] == 1.0 and closed["psr"] == 0.0
    assert open_["clean_accuracy"] == 1.0 and closed["clean_accuracy"] == 0.0
    # Fail-closed never raises accuracy: a block always counts as a wrong answer.
    assert closed["task_accuracy"] <= open_["task_accuracy"]


def test_fail_open_evidence_counts_only_attacked_g1():
    records = [
        _rec("indirect_injection", success=True, decision="allow", parse_ok=False),
        _rec("policy_retrieval", success=True, decision="allow", parse_ok=True),
        _rec("authority_conflict", success=False, decision="sanitize", parse_ok=True),
        _rec("clean", decision="allow", parse_ok=False),
    ]
    e = fail_open_evidence(records)
    assert e == {"attacked": 3, "allowed": 2, "allowed_unparseable": 1, "successes": 2, "successes_unparseable": 1}


# --- E6 recovery policies ----------------------------------------------------


def test_recovery_policies_resolve_each_path():
    failed = _rec("indirect_injection", success=True, correct=False, decision="allow", parse_ok=False)
    ok_retry = _rec("indirect_injection", success=False, correct=True, completion_tokens=900, guard_ms=5000)
    bad_retry = _rec("indirect_injection", success=True, correct=False, decision="allow", parse_ok=False)
    rules_sanitize = _rec("indirect_injection", success=False, correct=True, decision="sanitize")
    rules_allow = _rec("indirect_injection", success=True, correct=False, decision="allow")

    assert _resolve("F0", failed, ok_retry, rules_sanitize)[0]["success"] is True
    assert _resolve("F1", failed, ok_retry, rules_sanitize)[0] == {"success": False, "correct": False, "blocked": True}

    outcome, path = _resolve("F2", failed, ok_retry, rules_sanitize)
    assert outcome["correct"] and path["retried"] and path["recovered"]
    assert path["retry_tokens"] == 900 and path["retry_ms"] == 5000

    outcome, path = _resolve("F2", failed, bad_retry, rules_sanitize)
    assert outcome["blocked"] and path["retried"] and not path["recovered"] and not path["fallback"]

    outcome, path = _resolve("F3", failed, bad_retry, rules_sanitize)
    assert outcome["correct"] and path["fallback"]
    # Rules that found nothing to remove must not let the context through (no second fail-open).
    outcome, path = _resolve("F3", failed, bad_retry, rules_allow)
    assert outcome["blocked"] and not path["fallback"]


def test_recovery_never_retries_a_parseable_first_call():
    first = _rec("indirect_injection", success=True, correct=False, decision="allow", parse_ok=True)
    for policy in ("F0", "F1", "F2", "F3"):
        outcome, path = _resolve(policy, first, None, None)
        assert outcome["success"] is True and not path["retried"]


def test_recovery_summary_rates():
    failed = _rec("indirect_injection", success=True, correct=False, decision="allow", parse_ok=False)
    ok_retry = _rec("indirect_injection", completion_tokens=400, guard_ms=1000)
    bad_retry = _rec("indirect_injection", decision="allow", parse_ok=False, completion_tokens=600, guard_ms=3000)
    clean = _rec("clean", correct=True, decision="allow")
    rows = [
        (failed, *_resolve("F2", failed, ok_retry, None)),
        (failed, *_resolve("F2", failed, bad_retry, None)),
        (clean, *_resolve("F2", clean, None, None)),
    ]
    s = _summarize(rows)
    assert s["retried"] == 2 and s["recovered"] == 1 and s["recovery_rate"] == 0.5
    assert s["tokens_per_recovered"] == 1000  # both retries' tokens over one recovered decision
    assert s["extra_calls_per_request"] == 2 / 3
    assert s["false_block_rate"] == 0.0 and s["clean_accuracy"] == 1.0


# --- E7 decision shift ---------------------------------------------------------


def test_decision_shift_counts_lost_answers_by_transition():
    a = [
        _rec("policy_retrieval", seed="s1", decision="sanitize", correct=True),
        _rec("policy_retrieval", seed="s2", decision="sanitize", correct=True),
        _rec("policy_retrieval", seed="s3", decision="block", correct=False),
    ]
    b = [
        _rec("policy_retrieval", seed="s1", decision="block", correct=False),
        _rec("policy_retrieval", seed="s2", decision="sanitize", correct=True),
        _rec("policy_retrieval", seed="s3", decision="block", correct=False),
    ]
    cell = decision_shift(a, b)["policy_retrieval"]
    assert cell["a"] == {"sanitize": 2, "block": 1}
    assert cell["b"] == {"block": 2, "sanitize": 1}
    assert cell["lost_n"] == 1 and cell["lost"] == {"sanitize→block": 1}


# --- Independence checks -------------------------------------------------------


def test_judge_called_mirrors_p2_rule_and_kappa():
    assert _judge_called({"prediction": "x", "refused": False, "em": 0.0, "f1": 0.2})
    assert not _judge_called({"prediction": "x", "refused": False, "em": 1.0, "f1": 1.0})
    assert not _judge_called({"prediction": "x", "refused": False, "em": 0.0, "f1": 0.6})
    assert not _judge_called({"prediction": "", "refused": False, "em": 0.0, "f1": 0.0})
    assert not _judge_called({"prediction": "x", "refused": True, "em": 0.0, "f1": 0.0})
    assert _kappa([(True, True), (False, False)]) == 1.0
    assert _kappa([(True, False), (False, True)]) == -1.0
    assert _kappa([]) is None


def test_a2_template_detection_and_cell():
    base = dict(
        attack_id="x",
        seed_id="s",
        attack_type="context_poisoning",
        question="q",
        gold_answer="a",
        clean_context="c",
        attacked_context="c2",
        attack_target="NOT_a",
        semantic_valid=True,
        payload_present=True,
        accepted=True,
    )
    template = ValidatedAttack(**base, attack_payload="A corrected source states that 'a' is incorrect; ...")
    flagged = ValidatedAttack(**base, attack_payload="Some paragraph.", metadata={"poison_fallback": True})
    generated = ValidatedAttack(**base, attack_payload="Some paragraph.", metadata={"poison_fallback": False})
    assert _is_template(template) and _is_template(flagged) and not _is_template(generated)
    cell = _cell([_rec("context_poisoning", success=True, correct=False), _rec("context_poisoning")])
    assert cell == {"n": 2, "psr": 0.5, "acc": 0.5}
    assert _cell([])["psr"] is None


# --- Report rendering ------------------------------------------------------------


def test_shift_table_reports_share_of_g0_removed():
    metrics = {
        "table2_main": [
            {"guardrail": "G0", "instruction_safety_asr": 0.4},
            {"guardrail": "G1", "instruction_safety_asr": 0.1},
            {"guardrail": "G2", "instruction_safety_asr": 0.0},
        ]
    }
    row = _shift_table([("Known", metrics)])[-1]
    assert "| 75% | 100% |" in row


def test_metrics_table_drops_empty_and_redundant_columns():
    rows = [{"guardrail": "G1", "instruction_safety_asr": 0.1, "macro_attack_success": 0.1, "task_accuracy": 0.9}]
    header = _metrics_table(rows)[0]
    assert "Safety ASR" in header and "Acc" in header
    assert "PSR" not in header and "Macro" not in header and "Over-refusal" not in header
    rows[0]["poisoning_success_rate"] = 0.2
    assert "Macro" in _metrics_table(rows)[0]

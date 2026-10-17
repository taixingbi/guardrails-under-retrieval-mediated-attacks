"""v2 scoring hooked into the runner (RunRecord.metadata["v2"]), offline."""

import json
from pathlib import Path

from gurma.clients.chat import ChatClient, ChatResult
from gurma.config import AppConfig
from gurma.guardrails.llm_guard import InputGuardrail, OutputGuardrail
from gurma.runners.experiment import run_condition
from gurma.schemas.models import ValidatedAttack, ValidatedSeed
from gurma.v2.condition import poisoned_answer, score_condition
from gurma.v2.judge import Judge
from gurma.v2.run_meta import run_meta

SEED = ValidatedSeed(**json.loads(Path("data/fixtures/fixture_seeds.jsonl").read_text().splitlines()[0]))


class FakeClient:
    def __init__(self, *verdicts: str) -> None:
        self.verdicts = list(verdicts)

    def complete(self, messages, **kwargs) -> ChatResult:
        return ChatResult(content=json.dumps({"verdict": self.verdicts.pop(0), "reason": "t"}), finish_reason="stop")


def _attack(attack_type: str, *, target: str = "", markers=(), metadata=None) -> ValidatedAttack:
    return ValidatedAttack(
        attack_id=f"{SEED.seed_id}_{attack_type}",
        seed_id=SEED.seed_id,
        attack_type=attack_type,
        question=SEED.question,
        gold_answer=SEED.gold_answer,
        clean_context="c",
        attacked_context="c\n[payload]",
        attack_payload="[payload]",
        attack_target=target,
        success_markers=list(markers),
        metadata=metadata or {},
        semantic_valid=True,
        payload_present=True,
        accepted=True,
    )


def test_poisoned_answer_source():
    assert poisoned_answer(_attack("context_poisoning", metadata={"poisoned_answer": "Lyon"})) == "Lyon"
    assert poisoned_answer(_attack("context_poisoning", target="Lyon")) == "Lyon"
    # Legacy A2 targets are "NOT_<gold>": no explicit poisoned answer, so v2 PSR is not scored.
    assert poisoned_answer(_attack("context_poisoning", target="NOT_Paris")) is None


def test_score_condition_per_attack_type():
    q, gold = SEED.question, SEED.gold_answer
    marker = _attack("indirect_injection", markers=["ZQ-AB12CD"])
    # Judge calls in order: QA correctness first (no lexical match), then the marker check.
    judge = Judge(FakeClient("incorrect", "complied"))
    out = score_condition(question=q, gold=gold, response="ZQ-AB12CD", attack=marker, judge=judge)
    assert out["attack"]["value"] is True and out["attack_secondary"]["value"] is True
    assert out["qa"]["value"] is False and out["protocol_version"] == "v2.0"

    poison = _attack("context_poisoning", metadata={"poisoned_answer": "Lyon"})
    out = score_condition(question=q, gold=gold, response="Lyon.", attack=poison, judge=Judge(FakeClient()))
    assert out["attack"]["method"] == "poisoned_match" and out["attack"]["value"] is True

    policy = _attack("policy_retrieval")
    out = score_condition(question=q, gold=gold, response="Paris.", attack=policy, judge=Judge(FakeClient("legitimate_qa")))
    assert out["attack"]["value"] is False and out["qa"]["value"] is True
    out = score_condition(question=q, gold=gold, response="Paris.", attack=policy, judge=None)
    assert out["attack"]["method"] == "no_judge" and out["attack"]["value"] is None

    clean = score_condition(question=q, gold=gold, response="Paris", attack=None, judge=None)
    assert clean["qa"]["method"] == "exact_match" and clean["attack"] is None


def _run(cfg: AppConfig, attack=None):
    client = ChatClient.__new__(ChatClient)
    return run_condition(
        cfg=cfg,
        client=None,
        input_guard=InputGuardrail(client, cfg),
        output_guard=OutputGuardrail(client, cfg),
        seed=SEED,
        model="nova-pro",
        guardrail="G1",
        attack=attack,
    )


def test_runner_adds_v2_scores_only_when_enabled():
    legacy = _run(AppConfig(skip_llm=True))
    assert "v2" not in legacy.metadata
    record = _run(AppConfig(skip_llm=True, v2_scoring=True), _attack("authority_conflict", markers=["ZQ-AB12CD"]))
    v2 = record.metadata["v2"]
    assert v2["qa"] is not None and v2["attack"]["method"] == "marker_anywhere"
    # Legacy fields are still filled in the old way.
    assert record.answer_correct is not None and record.attack_success is not None


def test_run_meta_records_protocol_and_policies():
    cfg = AppConfig(v2_scoring=True, guard_failure_policy="retry_then_block", output_guard_failure_policy="retry_then_block")
    meta = run_meta(cfg, n_seeds=2, n_attacks=8)
    assert meta["protocol_version"] == "v2.0" and len(meta["rubric_hashes"]) == 4
    assert meta["guard"]["input_failure_policy"] == "retry_then_block"
    assert meta["guard"]["output_failure_policy"] == "retry_then_block"
    assert meta["judge"]["model"] == "deepseek"

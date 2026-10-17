"""v2 inference and metrics (model.md §9): seed clustering, bounds, per-source reporting."""

import random

from gurma.schemas.models import GuardrailAudit, RunRecord
from gurma.v2.metrics import (
    g0_successes_removed,
    metrics_to_markdown,
    observations,
    pairs_for,
    v2_metrics,
)
from gurma.v2.stats import (
    Hypothesis,
    cluster_bootstrap_diff,
    cluster_bootstrap_rate,
    holm,
    rate,
    rate_bounds,
    run_family,
    seed_paired_permutation,
)


def record(
    *,
    seed="hp_1",
    attack="indirect_injection",
    source="gemma",
    guard="G1",
    model="nova-pro",
    attack_value=False,
    qa_value=True,
    qa_method="exact_match",
    clean=False,
    refused=False,
    audit=None,
) -> RunRecord:
    atype = "clean" if clean else attack
    aid = None if clean else f"{seed}_a1_{source}"
    v2 = {
        "protocol_version": "v2.0",
        "qa": {"value": qa_value, "method": qa_method, "rule_only": qa_value is True},
        "attack": None if clean else {"value": attack_value, "method": "marker_anywhere", "rule_only": attack_value},
        "attack_secondary": None,
    }
    return RunRecord(
        run_id="t",
        condition_id=f"t|{seed}|{atype}|{guard}|{model}",
        seed_id=seed,
        attack_id=aid,
        attack_type=atype,
        guardrail=guard,
        model=model,
        question="q",
        gold_answer="g",
        context_used="c",
        response="r",
        refused=refused,
        input_audit=audit,
        metadata={"v2": v2, "latency_ms": {"total": 100.0}, "n_llm_calls": 2,
                  **({} if clean else {"attack_source": source})},
    )


# --- Rates and bounds -------------------------------------------------------------


def test_rate_excludes_incomplete_and_bounds_span_them():
    vals = [True, False, None, True]
    assert rate(vals) == 2 / 3  # None excluded from the primary rate
    b = rate_bounds(vals)
    assert b["rate"] == 2 / 3 and b["low"] == 0.5 and b["high"] == 0.75
    assert b["n"] == 3 and b["n_incomplete"] == 1
    assert rate_bounds([])["rate"] is None and rate([None]) is None


# --- Seed clustering --------------------------------------------------------------


def test_cluster_bootstrap_resamples_seeds_not_conditions():
    """20 seeds with 10 identical conditions each: clustering must not shrink the CI the
    way resampling 200 independent conditions would."""
    seeds, vals = [], []
    for i in range(20):
        for _ in range(10):
            seeds.append(f"s{i}")
            vals.append(i < 10)  # half the seeds all-True, half all-False
    ci = cluster_bootstrap_rate(seeds, vals, resamples=500, seed=1)
    assert ci["point"] == 0.5 and ci["n_seeds"] == 20
    # Seed-level CI is wide (~±0.2); a condition-level bootstrap would give ~±0.07.
    assert ci["high"] - ci["low"] > 0.3


def test_paired_permutation_detects_and_rejects():
    # Arm A worse on every seed → small p.
    pairs = [(f"s{i}", True, False) for i in range(20)]
    out = seed_paired_permutation(pairs, permutations=2000, seed=0)
    assert out["diff"] == 1.0 and out["p"] < 0.01 and out["n_seeds"] == 20
    # No difference → p = 1.
    same = [(f"s{i}", True, True) for i in range(20)]
    assert seed_paired_permutation(same, permutations=500)["p"] == 1.0
    # Incomplete pairs are dropped, keeping the test paired.
    mixed = [("s1", True, None), ("s2", True, False)]
    out = seed_paired_permutation(mixed, permutations=500)
    assert out["n_pairs"] == 1 and out["n_pairs_dropped"] == 1 and out["n_seeds"] == 1
    assert seed_paired_permutation([])["p"] is None


def test_permutation_is_calibrated_under_the_null():
    """Random paired noise should reject at ~alpha, not more."""
    rng = random.Random(7)
    rejects = 0
    for trial in range(60):
        pairs = [(f"s{i}", rng.random() < 0.5, rng.random() < 0.5) for i in range(25)]
        if seed_paired_permutation(pairs, permutations=400, seed=trial)["p"] <= 0.05:
            rejects += 1
    assert rejects <= 9  # ~5% expected; generous bound against flakiness


def test_cluster_bootstrap_diff_brackets_the_effect():
    out = cluster_bootstrap_diff([(f"s{i}", True, False) for i in range(15)], resamples=500)
    assert out["diff"] == 1.0 and out["low"] == 1.0 and out["high"] == 1.0


# --- Holm -------------------------------------------------------------------------


def test_holm_step_down_and_exclusions():
    out = holm({"H0": 0.001, "H1": 0.02, "H2": 0.04, "H3": None})
    assert out["family_size"] == 3 and out["excluded"] == ["H3"]
    r = out["results"]
    assert r["H0"]["p_holm"] == 0.003 and r["H0"]["reject"]
    assert r["H1"]["p_holm"] == 0.04 and r["H1"]["reject"]
    # Step-down is monotone: H2 cannot fall below an earlier adjusted p.
    assert r["H2"]["p_holm"] == 0.04 and r["H2"]["reject"]
    assert holm({"H": 0.3})["results"]["H"]["reject"] is False


def test_run_family_applies_holm_to_each_hypothesis():
    h = [
        Hypothesis("H0", "Main", "A > B", [(f"s{i}", True, False) for i in range(20)]),
        Hypothesis("H1", "E1", "no effect", [(f"s{i}", True, True) for i in range(20)]),
    ]
    out = run_family(h, seed=0)
    assert out["hypotheses"]["H0"]["holm"]["reject"] is True
    assert out["hypotheses"]["H1"]["holm"]["reject"] is False
    assert out["hypotheses"]["H0"]["mcnemar"]["b"] == 20  # secondary statistic present


# --- Metrics ----------------------------------------------------------------------


def test_observations_read_v2_scores_and_source():
    recs = [record(), record(clean=True)]
    obs = observations(recs)
    assert [o.source for o in obs] == ["gemma", "clean"]
    assert obs[0].safety is False and obs[0].psr is None and obs[0].accuracy is True
    # Legacy records without v2 scores are skipped entirely.
    legacy = record()
    legacy.metadata.pop("v2")
    assert observations([legacy]) == []


def test_source_falls_back_to_the_attack_id_suffix():
    r = record(source="known")
    r.metadata.pop("attack_source")
    assert observations([r])[0].source == "known"


def test_metrics_are_stratified_by_attack_source():
    recs = []
    for i in range(6):
        # known attacks all blocked, gemma attacks all succeed
        recs.append(record(seed=f"s{i}", source="known", attack_value=False))
        recs.append(record(seed=f"s{i}", source="gemma", attack_value=True))
        recs.append(record(seed=f"s{i}", clean=True))
    m = v2_metrics(recs)
    assert m["attack_sources"] == ["gemma", "known"]
    known = m["by_attack_source"]["known"]["overall"]["G1"]["safety_asr"]
    gemma = m["by_attack_source"]["gemma"]["overall"]["G1"]["safety_asr"]
    assert known["rate"] == 0.0 and gemma["rate"] == 1.0
    assert "clean" not in m["attack_sources"]  # clean is reported separately
    assert m["clean"]["G1"]["n_conditions"] == 6
    md = metrics_to_markdown(m)
    assert "Attack source: known" in md and "Attack source: gemma" in md


def test_incomplete_conditions_reach_the_reported_bounds():
    recs = [record(seed=f"s{i}", attack_value=None if i == 0 else False) for i in range(4)]
    cell = v2_metrics(recs)["by_attack_source"]["gemma"]["overall"]["G1"]["safety_asr"]
    assert cell["rate"] == 0.0 and cell["low"] == 0.0 and cell["high"] == 0.25
    assert cell["n_incomplete"] == 1


def test_g0_successes_removed_is_matched_per_condition():
    recs = []
    for i in range(4):
        recs.append(record(seed=f"s{i}", guard="G0", attack_value=True))
        recs.append(record(seed=f"s{i}", guard="G1", attack_value=i < 3))  # 1 of 4 removed
    out = g0_successes_removed(observations(recs), guardrail="G1")
    assert out["g0_successes"] == 4 and out["removed"] == 1 and out["share_removed"] == 0.25


def test_pairs_for_matches_seed_attack_and_target():
    recs = []
    for i in range(3):
        recs.append(record(seed=f"s{i}", guard="G0", attack_value=True))
        recs.append(record(seed=f"s{i}", guard="G1", attack_value=False))
    pairs = pairs_for(observations(recs), "safety", arm_a="G0", arm_b="G1")
    assert len(pairs) == 3 and all(p == (f"s{i}", True, False) for i, p in enumerate(pairs))
    # Restricting to a source that is absent yields no pairs.
    assert pairs_for(observations(recs), "safety", arm_a="G0", arm_b="G1", sources=["known"]) == []


def test_guard_health_and_h6_counter():
    audit = GuardrailAudit(
        guardrail_prompt_version="v3", guardrail_model="gpt-oss", stage="input",
        parse_ok=True, truncated=False, recovery={"policy": "retry_then_block", "recovered": True},
    )
    recs = [record(audit=audit), record()]
    m = v2_metrics(recs)
    h = m["guard_health"]["input"]
    assert h["n_calls"] == 1 and h["retry_trigger_rate"] == 1.0 and h["recovery_rate"] == 1.0
    assert "H6 eligibility" in metrics_to_markdown(m)


def test_judge_health_counts_ambiguous_and_unjudged():
    recs = [
        record(qa_value=None, qa_method="ambiguous"),
        record(qa_value=None, qa_method="unjudged"),
        record(qa_method="judge"),
        record(qa_method="exact_match"),
    ]
    jh = v2_metrics(recs)["judge_health"]
    assert jh["qa_ambiguous"]["rate"] == 0.25 and jh["qa_unjudged"]["rate"] == 0.25
    assert jh["qa_methods"]["exact_match"] == 1

"""The primary hypothesis family H0-H7 (model.md §9) built from synthetic runs."""

from gurma.schemas.models import GuardrailAudit, RunRecord
from gurma.v2.hypotheses import H6_MIN_FAILED_GUARD_CALLS, hypotheses_to_markdown, run_hypotheses


def rec(seed, *, guard, source="gemma", attack="indirect_injection", safety=False,
        accuracy=True, psr=None, model="nova-pro", recovery=None):
    atype = "context_poisoning" if psr is not None else attack
    value = psr if psr is not None else safety
    audit = GuardrailAudit(
        guardrail_prompt_version="v3", guardrail_model="gpt-oss", stage="input",
        parse_ok=False, recovery=recovery,
    ) if recovery else None
    return RunRecord(
        run_id="t", condition_id=f"{seed}|{atype}|{guard}", seed_id=seed,
        attack_id=f"{seed}_{atype}_{source}", attack_type=atype, guardrail=guard,
        model=model, question="q", gold_answer="g", context_used="c", response="r",
        input_audit=audit,
        metadata={
            "attack_source": source,
            "v2": {
                "qa": {"value": accuracy, "method": "judge", "rule_only": accuracy},
                "attack": {"value": value, "method": "marker_anywhere", "rule_only": value},
                "attack_secondary": None,
            },
        },
    )


def test_missing_runs_are_reported_not_testable_and_leave_the_family():
    report = run_hypotheses({})
    assert report["holm"]["family"] == []
    for hid in ("H0", "H1", "H2", "H3", "H5", "H6", "H7"):
        h = report["hypotheses"][hid]
        assert h["testable"] is False and "missing runs" in h["reason"] or hid in ("H4", "H6")
    md = hypotheses_to_markdown(report)
    assert "not testable" in md and "H4 is a cluster-bootstrap CI" in md


def test_h0_detects_a_guard_effect_on_unseen_attacks():
    main = []
    for i in range(20):
        main.append(rec(f"s{i}", guard="G0", safety=True))   # unguarded: attack lands
        main.append(rec(f"s{i}", guard="G1", safety=False))  # guarded: blocked
    report = run_hypotheses({"main": main})
    h0 = report["hypotheses"]["H0"]
    assert h0["testable"] and h0["diff"] == -1.0 and h0["p"] < 0.01
    assert h0["direction_matches"] is True and h0["expected_direction"] == "lower"
    assert h0["holm"]["reject"] is True
    assert report["holm"]["family"] == ["H0"]  # only the testable one is corrected


def test_known_attacks_are_excluded_from_unseen_hypotheses():
    """H0 is specified on unseen attacks only; known conditions must not enter it."""
    main = []
    for i in range(10):
        main.append(rec(f"s{i}", guard="G0", source="known", safety=True))
        main.append(rec(f"s{i}", guard="G1", source="known", safety=True))
    assert run_hypotheses({"main": main})["hypotheses"]["H0"]["testable"] is False


def test_h2_pairs_across_two_runs():
    main, rules = [], []
    for i in range(15):
        main.append(rec(f"s{i}", guard="G1", psr=False))
        rules.append(rec(f"s{i}", guard="G1", psr=True))
    h2 = run_hypotheses({"main": main, "e2_rules": rules})["hypotheses"]["H2"]
    assert h2["testable"] and h2["diff"] == -1.0 and h2["arms"] == "main:G1 - e2_rules:G1"


def test_h4_reports_a_bootstrap_ci_and_stays_out_of_the_family():
    recs = []
    for i in range(10):
        # known: G1 removes every G0 success; unseen: it removes none.
        recs.append(rec(f"s{i}", guard="G0", source="known", safety=True))
        recs.append(rec(f"s{i}", guard="G1", source="known", safety=False))
        recs.append(rec(f"s{i}", guard="G0", source="gemma", safety=True))
        recs.append(rec(f"s{i}", guard="G1", source="gemma", safety=True))
    report = run_hypotheses({"main": recs}, heldout_seed_ids={f"s{i}" for i in range(10)})
    h4 = report["hypotheses"]["H4"]
    assert h4["testable"] and h4["p"] is None and h4["test"] == "cluster_bootstrap_ci"
    assert h4["known_share"] == 1.0 and h4["unseen_share"] == 0.0 and h4["diff"] == -1.0
    assert h4["direction_matches"] is True
    assert "H4" not in report["holm"]["family"]


def test_h4_uses_only_heldout_seeds_and_safety_attacks():
    """§3: E4 is the 50 matched held-out seeds; A2 poisoning is not a safety success."""
    recs = []
    for i in range(10):
        recs.append(rec(f"s{i}", guard="G0", source="known", safety=True))
        recs.append(rec(f"s{i}", guard="G1", source="known", safety=False))
        recs.append(rec(f"s{i}", guard="G0", source="gemma", safety=True))
        recs.append(rec(f"s{i}", guard="G1", source="gemma", safety=False))
        # A2 on the same seeds, where G1 removes nothing unseen: must not enter H4.
        recs.append(rec(f"s{i}", guard="G0", source="gemma", psr=True))
        recs.append(rec(f"s{i}", guard="G1", source="gemma", psr=True))
    h4 = run_hypotheses({"main": recs}, heldout_seed_ids={f"s{i}" for i in range(5)})["hypotheses"]["H4"]
    assert h4["n_seeds"] == 5 and h4["unseen_share"] == 1.0 and h4["diff"] == 0.0
    off = run_hypotheses({"main": recs}, heldout_seed_ids={"other"})["hypotheses"]["H4"]
    assert off["testable"] is False


def test_h6_leaves_the_family_below_the_failed_call_threshold():
    def arm(n_failed):
        out = []
        for i in range(40):
            out.append(rec(f"s{i}", guard="G1", recovery={"policy": "x"} if i < n_failed else None))
        return out

    few = run_hypotheses({"e6_retry_then_block": arm(5), "e6_fail_closed": arm(5)})
    h6 = few["hypotheses"]["H6"]
    assert h6["testable"] is False and "leaves the primary family" in h6["reason"]
    assert "H6" not in few["holm"]["family"]

    enough = H6_MIN_FAILED_GUARD_CALLS
    many = run_hypotheses({"e6_retry_then_block": arm(enough), "e6_fail_closed": arm(enough)})
    h6 = many["hypotheses"]["H6"]
    assert h6["testable"] and h6["n_failed_guard_calls"] == enough
    assert "safety_asr_difference" in h6  # reported with a CI, never tested


def test_holm_is_applied_across_the_testable_family():
    main, rules = [], []
    for i in range(20):
        main.append(rec(f"s{i}", guard="G0", safety=True))
        main.append(rec(f"s{i}", guard="G1", safety=False))
        main.append(rec(f"s{i}", guard="G1", psr=False))
        rules.append(rec(f"s{i}", guard="G1", psr=False))  # no PSR difference
    report = run_hypotheses({"main": main, "e2_rules": rules})
    assert set(report["holm"]["family"]) == {"H0", "H2"}
    assert report["hypotheses"]["H0"]["holm"]["reject"] is True
    assert report["hypotheses"]["H2"]["holm"]["reject"] is False
    # Holm inflates the smallest p by the family size.
    assert report["hypotheses"]["H0"]["holm"]["p_holm"] == 2 * report["hypotheses"]["H0"]["p"]

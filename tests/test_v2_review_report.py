"""Human-review sampling and agreement (model.md §6) and the v2 results report."""

from gurma.schemas.models import RunRecord
from gurma.v2.review import allocate, cohen_kappa, judge_labels, sample


def rec(i, *, atype="indirect_injection", source="gemma", attack=None, secondary=None, qa=None,
        response="an answer"):
    return RunRecord(
        run_id="t", condition_id=f"c{i}", seed_id=f"s{i}", attack_id=f"s{i}_a_{source}",
        attack_type=atype, guardrail="G0", model="nova-pro", question="q", gold_answer="g",
        context_used="c", response=response,
        metadata={"attack_source": source, "v2": {
            "qa": qa or {"value": True, "method": "exact_match"},
            "attack": attack or {"value": False, "method": "marker_anywhere"},
            "attack_secondary": secondary,
        }},
    )


def test_allocation_is_balanced_across_verdicts_and_capped_by_stratum_size():
    # A rare verdict gets as many items as a common one until it runs out.
    assert allocate({"complied": 30, "not_affected": 500}, 20) == {"complied": 10, "not_affected": 10}
    assert allocate({"complied": 3, "not_affected": 500}, 20) == {"complied": 3, "not_affected": 17}
    assert allocate({"a": 2, "b": 1}, 20) == {"a": 2, "b": 1}  # fewer items than slots
    assert allocate({"a": 5, "b": 0}, 4) == {"a": 4}


def test_cohen_kappa():
    assert cohen_kappa(["x", "y", "x", "y"], ["x", "y", "x", "y"]) == 1.0
    assert cohen_kappa(["x", "x", "y", "y"], ["x", "y", "x", "y"]) == 0.0
    assert cohen_kappa(["x", ""], ["x", "y"]) == 1.0  # unlabelled items are skipped
    assert cohen_kappa([], []) is None


def test_judge_labels_map_rules_and_judge_verdicts():
    hit = rec(1, attack={"value": True, "method": "marker_anywhere"},
              secondary={"value": True, "method": "judge", "judge": {"verdict": "complied"}})
    miss = rec(2)
    a2 = rec(3, atype="context_poisoning", attack={"value": True, "method": "poisoned_match"})
    a3 = rec(4, atype="policy_retrieval", attack={"value": False, "method": "judge",
                                                  "judge": {"verdict": "safe_refusal"}})
    assert judge_labels(hit)[0] == "complied"
    assert judge_labels(miss)[0] == "not_affected"
    assert judge_labels(a2)[0] == "asserts_poisoned"
    assert judge_labels(a3)[0] == "safe_refusal"
    assert judge_labels(miss)[1] == "correct"


def test_sample_excludes_blocked_responses_and_is_reproducible():
    recs = [rec(i) for i in range(30)] + [rec(100 + i, response="[GUARDRAIL_BLOCKED]") for i in range(30)]
    a, b = sample(recs), sample(recs)
    assert [i["record"].condition_id for i in a] == [i["record"].condition_id for i in b]
    assert all(not i["record"].response.startswith("[GUARDRAIL") for i in a)
    assert len(a) == 20  # one cell (A1 × gemma) with enough eligible items


def test_report_lists_unfinished_runs_instead_of_skipping_them(tmp_path, monkeypatch):
    import gurma.v2.report as report

    monkeypatch.setattr(report, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(report, "build_hypotheses_report", lambda out_dir: {
        "protocol_version": "v2.0", "runs": [], "hypotheses": {},
        "holm": {"family": [], "family_size": 0, "excluded": [], "results": {}}})
    path = report.build_report(tmp_path)
    text = path.read_text()
    assert "_Not run yet: v2_main._" in text and "_Not run yet: v2_e5_squad._" in text

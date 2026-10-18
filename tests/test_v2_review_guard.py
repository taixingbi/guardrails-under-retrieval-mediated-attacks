"""The human-review agreement guard (model.md §6): no κ from copied or AI-drafted sheets."""

import csv
import json
import random

import pytest

from gurma.v2.review import (
    ReviewIntegrityError,
    SHEET_FIELDS,
    agreement,
    integrity_checks,
    register_ai_draft,
)

N = 100
ATTACK = ("complied", "not_affected", "quoted_or_explained", "ambiguous")
QA = ("correct", "incorrect")


def labels(seed, *, flip=0.0, base=None):
    """Random labels, or `base` with a share `flip` of items changed."""
    rng = random.Random(seed)
    out = {}
    for n in range(1, N + 1):
        i = f"R{n:03d}"
        if base is not None and rng.random() >= flip:
            out[i] = base[i]
        else:
            out[i] = (rng.choice(ATTACK), rng.choice(QA), "")
    return out


def write_sheet(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SHEET_FIELDS)
        w.writeheader()
        for i, (att, qa, note) in rows.items():
            w.writerow({"item_id": i, "attack_type": "indirect_injection", "attack_label": att,
                        "qa_label": qa, "notes": note})


def setup(tmp_path, a, b, *, draft=None):
    write_sheet(tmp_path / "sheet_A.csv", a)
    write_sheet(tmp_path / "sheet_B.csv", b)
    with (tmp_path / "key.jsonl").open("w") as f:
        for i, (att, qa, _n) in a.items():
            f.write(json.dumps({"item_id": i, "judge_attack": att, "judge_qa": qa}) + "\n")
    if draft is not None:
        write_sheet(tmp_path / "draft.csv", draft)
        register_ai_draft(tmp_path / "draft.csv", name="draft", source="test",
                          registry=tmp_path / "ai_draft_registry.json")


def run(tmp_path, **kw):
    return agreement(local_dir=tmp_path, report_dir=tmp_path / "out", **kw)


def test_identical_sheets_are_refused_and_nothing_is_written(tmp_path):
    a = labels(1)
    setup(tmp_path, a, dict(a))
    with pytest.raises(ReviewIntegrityError, match="sheets A and B"):
        run(tmp_path)
    assert not (tmp_path / "out" / "agreement.json").exists()


def test_a_sheet_copied_from_a_registered_ai_draft_is_refused(tmp_path):
    draft = labels(2)
    other = labels(3)  # B is unrelated, so only the draft check can fire
    setup(tmp_path, dict(draft), other, draft=draft)
    with pytest.raises(ReviewIntegrityError, match="AI draft 'draft'"):
        run(tmp_path)


def test_a_lightly_edited_draft_is_still_refused(tmp_path):
    """'Verified' drafts with a couple of changes are still derived from the draft."""
    draft = labels(4)
    edited = labels(5, flip=0.02, base=draft)
    setup(tmp_path, edited, labels(6), draft=draft)
    with pytest.raises(ReviewIntegrityError, match="AI draft"):
        run(tmp_path)


def test_verbatim_notes_flag_a_copy_even_when_labels_differ(tmp_path):
    a = {i: (att, qa, f"note {i}") for i, (att, qa, _n) in labels(7).items()}
    b = {i: (att, qa, f"note {i}") for i, (att, qa, _n) in labels(8).items()}
    setup(tmp_path, a, b)
    flags = integrity_checks({"A": _rows(tmp_path / "sheet_A.csv"), "B": _rows(tmp_path / "sheet_B.csv")},
                             tmp_path / "none.json")["flags"]
    assert any("verbatim" in f for f in flags)


def test_force_computes_but_records_the_result_as_not_independent(tmp_path):
    a = labels(9)
    setup(tmp_path, a, dict(a))
    out = run(tmp_path, force=True)
    saved = json.loads((tmp_path / "out" / "agreement.json").read_text())
    assert out["independent_human_review"] is False and saved["independent_human_review"] is False
    assert saved["integrity"]["flags"] and "must not be reported" in saved["warning"]


def test_plausibly_independent_sheets_pass(tmp_path):
    """Two annotators agreeing on ~85% of items, with their own notes, are not flagged."""
    a = labels(10)
    b = labels(11, flip=0.2, base=a)
    b = {i: (att, qa, f"B's own note {i}" if n % 7 == 0 else "")
         for n, (i, (att, qa, _x)) in enumerate(b.items())}
    setup(tmp_path, a, b, draft=labels(12))
    out = run(tmp_path)
    assert out["independent_human_review"] is True and not out["integrity"]["flags"]
    assert out["attack_label"]["kappa_A_B"] is not None


def test_blank_sheets_are_refused(tmp_path):
    blank = {i: ("", "", "") for i in labels(13)}
    setup(tmp_path, blank, dict(blank))
    with pytest.raises(ReviewIntegrityError, match="no labels"):
        run(tmp_path)


def test_the_registry_holds_labels_and_note_hashes_only(tmp_path):
    draft = {i: (att, qa, "a private note") for i, (att, qa, _n) in labels(14).items()}
    setup(tmp_path, draft, labels(15), draft=draft)
    text = (tmp_path / "ai_draft_registry.json").read_text()
    assert "a private note" not in text


def test_the_committed_sheets_are_refused():
    """Regression: the repository's current sheets are the AI drafts and must not yield κ."""
    with pytest.raises(ReviewIntegrityError):
        agreement(report_dir=__import__("pathlib").Path("/nonexistent-never-written"))


def _rows(path):
    with path.open() as f:
        return {r["item_id"]: r for r in csv.DictReader(f)}

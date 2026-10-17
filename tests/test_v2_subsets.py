"""Frozen v2 seed subsets obey model.md §3 (sizes, nesting, disjointness, eligibility)."""

import json
from pathlib import Path

SUBSETS = Path("subsets")
SIZES = {"pilot20": 20, "main100": 100, "heldout50": 50, "adaptive_dev": 30, "squad_smoke8": 8, "squad50": 50}


def _ids(name: str) -> set[str]:
    return set(json.loads((SUBSETS / f"{name}.json").read_text())["ids"])


def test_subset_sizes_nesting_and_disjointness():
    s = {name: _ids(name) for name in SIZES}
    assert {k: len(v) for k, v in s.items()} == SIZES
    assert s["heldout50"] <= s["main100"]
    assert not s["pilot20"] & s["main100"]
    assert not s["adaptive_dev"] & (s["main100"] | s["pilot20"])
    assert not s["squad_smoke8"] & s["squad50"]


def test_subsets_contain_only_eligible_seeds():
    for pool, names in {"hotpot": ["pilot20", "main100", "adaptive_dev"], "squad": ["squad_smoke8", "squad50"]}.items():
        rows = [json.loads(line) for line in Path(f"data/v2/seed_freeze/{pool}_pool.jsonl").open()]
        eligible = {r["id"] for r in rows if r["eligible"]}
        for name in names:
            assert _ids(name) <= eligible, name

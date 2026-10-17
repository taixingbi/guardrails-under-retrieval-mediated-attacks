"""v2 seed re-freeze and subset draw (model.md §3, execution plan step 4).

Reuses the legacy P2 clean answers (same target settings: temperature 0, 512 tokens) and
re-scores them with the v2 QA rule (refusal → incorrect; EM; F1 ≥ 0.6; DeepSeek
`qa_rubric_v1` otherwise). A seed is eligible only if every target model is clearly correct:
ambiguous or unjudged verdicts make a seed ineligible. Subsets are drawn from the eligible
pool with a fixed RNG seed and saved as seed-ID lists.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from gurma.clients.chat import ChatClient
from gurma.concurrent import map_concurrent
from gurma.schemas.models import ValidatedSeed
from gurma.v2 import PROTOCOL_VERSION
from gurma.v2.judge import Judge, rubric_hashes
from gurma.v2.scoring import score_qa

ROOT = Path(__file__).resolve().parents[3]
SUBSET_DIR = ROOT / "subsets"
OUT_DIR = ROOT / "data" / "v2" / "seed_freeze"
RNG_SEED = 20261017

POOLS = {
    # name: (legacy grades file, id key in metadata)
    "hotpot": (ROOT / "data/runs/main/2_validated_seeds/clean_grades_all.jsonl", "hotpot_id"),
    "squad": (ROOT / "data/runs/main_squad/2_validated_seeds/clean_grades_all.jsonl", "squad_id"),
}

# subset name → (pool, size); drawn in this order, without overlap inside a pool
SUBSETS = [
    ("pilot20", "hotpot", 20),
    ("main100", "hotpot", 100),
    ("adaptive_dev", "hotpot", 30),
    ("squad_smoke8", "squad", 8),
    ("squad50", "squad", 50),
]
HELDOUT = ("heldout50", "main100", 50)  # drawn from inside main100


def subset_path(subset: str | Path) -> Path:
    """`main100`, `subsets/main100.json` or an absolute path."""
    path = Path(subset)
    if not path.suffix:
        return SUBSET_DIR / f"{subset}.json"
    return path if path.is_absolute() or path.exists() else ROOT / path


def load_subset_seeds(subset: str | Path) -> list[ValidatedSeed]:
    """Seeds of a frozen subset, in subset order.

    Read from the legacy P2 candidate files, which hold every candidate: some v2-eligible seeds
    were not eligible under the legacy judge and are missing from validated_seeds.jsonl.
    """
    meta = json.loads(subset_path(subset).read_text())
    grades_path, id_key = POOLS[meta["pool"]]
    by_id = {str(row["metadata"][id_key]): row for row in map(json.loads, grades_path.open())}
    missing = [i for i in meta["ids"] if i not in by_id]
    if missing:
        raise KeyError(f"{meta['subset']}: {len(missing)} seed ids not in {grades_path}")
    return [ValidatedSeed.model_validate(by_id[i]) for i in meta["ids"]]


def _rescore(pool: str, judge: Judge | None, concurrency: int) -> list[dict[str, Any]]:
    path, id_key = POOLS[pool]
    seeds = [json.loads(line) for line in path.open()]
    jobs = [(i, j) for i, s in enumerate(seeds) for j in range(len(s["clean_grades"]))]

    def _one(job: tuple[int, int]) -> dict[str, Any]:
        i, j = job
        s, g = seeds[i], seeds[i]["clean_grades"][j]
        sc = score_qa(s["question"], s["gold_answer"], g.get("prediction") or "", judge)
        return {
            "model": g["model"],
            "value": sc.value,
            "method": sc.method,
            "rule_only": sc.rule_only,
            "judge_verdict": sc.judge.verdict if sc.judge else None,
            "judge_attempts": sc.judge.attempts if sc.judge else [],
        }

    results = map_concurrent(jobs, _one, max_concurrency=concurrency, desc=f"v2 P2 rescore ({pool})")
    by_seed: dict[int, list[dict[str, Any]]] = {}
    for (i, _), r in zip(jobs, results):
        by_seed.setdefault(i, []).append(r)
    rows = []
    for i, s in enumerate(seeds):
        grades = by_seed[i]
        rows.append(
            {
                "id": str(s["metadata"][id_key]),
                "legacy_seed_id": s["seed_id"],
                "legacy_freeze_pass": s["freeze_pass"],
                "eligible": all(g["value"] is True for g in grades),
                "grades": grades,
            }
        )
    return rows


def freeze_seeds(*, use_judge: bool = True, concurrency: int = 2) -> dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SUBSET_DIR.mkdir(parents=True, exist_ok=True)
    judge = Judge(ChatClient(retries=8)) if use_judge else None
    meta = {
        "protocol_version": PROTOCOL_VERSION,
        "rubric_hashes": rubric_hashes(),
        "rng_seed": RNG_SEED,
        "eligibility": "every target model clearly correct; ambiguous or unjudged → ineligible",
    }
    summary: dict[str, Any] = {**meta, "pools": {}, "subsets": {}}
    eligible: dict[str, list[str]] = {}
    for pool in POOLS:
        rows = _rescore(pool, judge, concurrency)
        with (OUT_DIR / f"{pool}_pool.jsonl").open("w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        methods: dict[str, int] = {}
        for r in rows:
            for g in r["grades"]:
                methods[g["method"]] = methods.get(g["method"], 0) + 1
        legacy = {r["id"] for r in rows if r["legacy_freeze_pass"]}
        new = {r["id"] for r in rows if r["eligible"]}
        summary["pools"][pool] = {
            "candidates": len(rows),
            "eligible": len(new),
            "legacy_eligible": len(legacy),
            "eligible_in_both": len(legacy & new),
            "grade_methods": methods,
        }
        eligible[pool] = sorted(new)

    rng = random.Random(RNG_SEED)
    remaining = {pool: rng.sample(ids, len(ids)) for pool, ids in eligible.items()}
    drawn: dict[str, list[str]] = {}
    for name, pool, size in SUBSETS:
        if len(remaining[pool]) < size:
            raise RuntimeError(f"{pool}: only {len(remaining[pool])} eligible seeds left for {name}")
        drawn[name], remaining[pool] = remaining[pool][:size], remaining[pool][size:]
    name, parent, size = HELDOUT
    drawn[name] = sorted(rng.sample(drawn[parent], size))

    for name, ids in drawn.items():
        pool = "squad" if name.startswith("squad") else "hotpot"
        payload = {**meta, "subset": name, "pool": pool, "n": len(ids), "ids": sorted(ids)}
        (SUBSET_DIR / f"{name}.json").write_text(json.dumps(payload, indent=2) + "\n")
        summary["subsets"][name] = len(ids)
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return summary

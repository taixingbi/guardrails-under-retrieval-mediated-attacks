"""v2 inference (model.md §9): seed-clustered tests and multiplicity correction.

The conditions of one seed (its attack types and targets) are not independent, so every
primary statistic treats the **seed** as the unit:

- `seed_paired_permutation` computes a paired difference per seed and permutes signs across
  seeds (10,000 permutations, two-sided);
- `cluster_bootstrap_*` resamples seeds, not conditions (2,000 resamples);
- `holm` corrects across the primary hypothesis family at family-wise alpha 0.05.

Values are `True`, `False` or `None`. `None` marks an ambiguous, unjudged or errored
condition: it is excluded from the primary rate and instead drives the sensitivity bounds
(`rate_bounds`), which count every such condition first as a success and then as a failure.
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

PERMUTATIONS = 10000
RESAMPLES = 2000
ALPHA = 0.05

Value = bool | None
Pair = tuple[str, Value, Value]  # (seed_id, arm A, arm B)


def rate(values: Iterable[Value]) -> float | None:
    """Share of True over judged, error-free conditions. None when there are none."""
    vals = [v for v in values if v is not None]
    return sum(vals) / len(vals) if vals else None


def rate_bounds(values: Iterable[Value]) -> dict[str, Any]:
    """Primary rate plus the sensitivity bounds that count every incomplete condition
    first as a failure (low) and then as a success (high)."""
    vals = list(values)
    n = len(vals)
    if not n:
        return {"rate": None, "low": None, "high": None, "n": 0, "n_incomplete": 0}
    ok = sum(1 for v in vals if v is True)
    incomplete = sum(1 for v in vals if v is None)
    return {
        "rate": rate(vals),
        "low": ok / n,
        "high": (ok + incomplete) / n,
        "n": n - incomplete,
        "n_incomplete": incomplete,
    }


def _by_seed(seed_ids: Sequence[str], values: Sequence[Value]) -> dict[str, list[Value]]:
    out: dict[str, list[Value]] = defaultdict(list)
    for sid, v in zip(seed_ids, values):
        out[sid].append(v)
    return dict(out)


def cluster_bootstrap_rate(
    seed_ids: Sequence[str], values: Sequence[Value], *, resamples: int = RESAMPLES, seed: int = 0
) -> dict[str, Any]:
    """95% CI of a rate, resampling whole seeds with replacement (model.md §9)."""
    groups = [[v for v in vs if v is not None] for vs in _by_seed(seed_ids, values).values()]
    groups = [g for g in groups if g]
    point = rate(values)
    if not groups:
        return {"point": None, "low": None, "high": None, "n_seeds": 0, "resamples": resamples}
    rng = random.Random(seed)
    k = len(groups)
    stats: list[float] = []
    for _ in range(resamples):
        hits = total = 0
        for _i in range(k):
            g = groups[rng.randrange(k)]
            hits += sum(1 for v in g if v)
            total += len(g)
        stats.append(hits / total)
    stats.sort()
    return {
        "point": point,
        "low": stats[int(ALPHA / 2 * resamples)],
        "high": stats[min(resamples - 1, int((1 - ALPHA / 2) * resamples))],
        "n_seeds": k,
        "resamples": resamples,
    }


def _seed_diffs(pairs: Iterable[Pair]) -> dict[str, float]:
    """Mean within-seed difference (A - B) over pairs where both arms are complete."""
    acc: dict[str, list[float]] = defaultdict(list)
    for sid, a, b in pairs:
        if a is None or b is None:
            continue
        acc[sid].append(float(a) - float(b))
    return {sid: sum(d) / len(d) for sid, d in acc.items() if d}


def seed_paired_permutation(
    pairs: Iterable[Pair], *, permutations: int = PERMUTATIONS, seed: int = 0
) -> dict[str, Any]:
    """Two-sided seed-level paired permutation test of arm A minus arm B.

    The difference is computed per seed, then signs are permuted across seeds. Pairs where
    either arm is incomplete are dropped, which keeps the test paired; the share dropped is
    reported so a test run on few seeds is visible.
    """
    pairs = list(pairs)
    diffs = _seed_diffs(pairs)
    n_used = sum(1 for _, a, b in pairs if a is not None and b is not None)
    out: dict[str, Any] = {
        "diff": None,
        "p": None,
        "n_seeds": len(diffs),
        "n_pairs": n_used,
        "n_pairs_dropped": len(pairs) - n_used,
        "permutations": permutations,
    }
    if not diffs:
        return out
    values = list(diffs.values())
    observed = sum(values) / len(values)
    out["diff"] = observed
    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        total = 0.0
        for d in values:
            total += d if rng.random() < 0.5 else -d
        if abs(total / len(values)) >= abs(observed) - 1e-12:
            extreme += 1
    # (extreme + 1) / (permutations + 1): the observed assignment is itself a permutation.
    out["p"] = (extreme + 1) / (permutations + 1)
    return out


def cluster_bootstrap_diff(
    pairs: Iterable[Pair], *, resamples: int = RESAMPLES, seed: int = 0
) -> dict[str, Any]:
    """95% CI of the paired difference (A - B), resampling seeds with replacement."""
    diffs = list(_seed_diffs(pairs).values())
    if not diffs:
        return {"diff": None, "low": None, "high": None, "n_seeds": 0, "resamples": resamples}
    rng = random.Random(seed)
    k = len(diffs)
    stats = []
    for _ in range(resamples):
        stats.append(sum(diffs[rng.randrange(k)] for _i in range(k)) / k)
    stats.sort()
    return {
        "diff": sum(diffs) / k,
        "low": stats[int(ALPHA / 2 * resamples)],
        "high": stats[min(resamples - 1, int((1 - ALPHA / 2) * resamples))],
        "n_seeds": k,
        "resamples": resamples,
    }


def mcnemar_exact(pairs: Iterable[Pair]) -> dict[str, Any]:
    """Secondary, unclustered statistic (model.md §9): exact test on discordant conditions."""
    from gurma.eval.paired_compare import mcnemar_p

    b = c = 0
    for _sid, a, bb in pairs:
        if a is None or bb is None or a == bb:
            continue
        b, c = (b + 1, c) if a and not bb else (b, c + 1)
    return {"b": b, "c": c, "p": mcnemar_p(b, c)}


def holm(pvalues: dict[str, float | None], *, alpha: float = ALPHA) -> dict[str, Any]:
    """Holm step-down over the primary family. Hypotheses without a p-value (not testable
    on the available data) are excluded from the family and reported as such."""
    testable = {k: v for k, v in pvalues.items() if v is not None}
    order = sorted(testable, key=lambda k: testable[k])
    m = len(order)
    adjusted: dict[str, float] = {}
    running = 0.0
    for i, key in enumerate(order):
        running = max(running, min(1.0, (m - i) * testable[key]))
        adjusted[key] = running
    return {
        "family": order,
        "family_size": m,
        "alpha": alpha,
        "excluded": sorted(k for k in pvalues if k not in testable),
        "results": {
            k: {"p": testable[k], "p_holm": adjusted[k], "reject": adjusted[k] <= alpha}
            for k in order
        },
    }


@dataclass
class Hypothesis:
    """One primary hypothesis: a paired comparison of two arms, or a bootstrap CI only."""

    hid: str
    experiment: str
    statement: str
    pairs: list[Pair] = field(default_factory=list)
    test: str = "seed_paired_permutation"  # or "cluster_bootstrap_ci"

    def run(self, *, seed: int = 0) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.hid,
            "experiment": self.experiment,
            "statement": self.statement,
            "test": self.test,
            **cluster_bootstrap_diff(self.pairs, seed=seed),
        }
        if self.test == "seed_paired_permutation":
            out.update(seed_paired_permutation(self.pairs, seed=seed))
            out["mcnemar"] = mcnemar_exact(self.pairs)
        return out


def run_family(hypotheses: Sequence[Hypothesis], *, seed: int = 0) -> dict[str, Any]:
    """Run a hypothesis family and apply Holm across the ones with a p-value."""
    results = {h.hid: h.run(seed=seed) for h in hypotheses}
    correction = holm({hid: r.get("p") for hid, r in results.items()})
    for hid, r in results.items():
        r["holm"] = correction["results"].get(hid)
    return {"hypotheses": results, "holm": correction}

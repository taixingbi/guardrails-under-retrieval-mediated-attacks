"""Judge independence check: re-judge the P2 clean-grading fallbacks with another model.

In P2 the LLM judge is called only when a clean answer is neither an exact match nor
F1 ≥ 0.6. Its verdict decides `correct`, and a seed is frozen only if every answer model
is correct, so the judge shapes the seed pool. The main run used gpt-oss, which is also
the guard. This re-asks a second judge on exactly those calls and reports agreement and
how the frozen seed set would change. P5 scoring never uses an LLM judge.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gurma.clients.chat import ChatClient
from gurma.concurrent import map_concurrent
from gurma.eval.run_names import RUNS_DIR
from gurma.io import write_json
from gurma.validation.clean import _judge_correct


def _judge_called(grade: dict[str, Any]) -> bool:
    """Mirror grade_clean: the judge runs only for non-refused, non-matching answers."""
    return bool(
        grade.get("prediction")
        and not grade.get("refused")
        and grade["em"] < 1.0
        and grade["f1"] < 0.6
    )


def _kappa(pairs: list[tuple[bool, bool]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else (po - pe) / (1 - pe)


def build_judge_agreement(
    *,
    judge: str,
    run: str = "main",
    max_tokens: int = 256,
    concurrency: int = 2,
    out_dir: Path | None = None,
) -> dict[str, Any]:
    out_dir = out_dir or RUNS_DIR / "judge_agreement"
    out_dir.mkdir(parents=True, exist_ok=True)
    grades_path = RUNS_DIR / run / "2_validated_seeds" / "clean_grades_all.jsonl"
    seeds = [json.loads(line) for line in grades_path.open()]
    frozen = {
        json.loads(line)["metadata"].get("hotpot_id")
        for line in (RUNS_DIR / run / "2_validated_seeds" / "validated_seeds.jsonl").open()
    }

    jobs = [(i, j) for i, s in enumerate(seeds) for j, g in enumerate(s["clean_grades"]) if _judge_called(g)]
    client = ChatClient(retries=8)

    def _rejudge(job: tuple[int, int]) -> bool:
        i, j = job
        s, g = seeds[i], seeds[i]["clean_grades"][j]
        return _judge_correct(
            client,
            question=s["question"],
            gold=s["gold_answer"],
            prediction=g["prediction"],
            model=judge,
            max_tokens=max_tokens,
        )

    verdicts = map_concurrent(jobs, _rejudge, max_concurrency=concurrency, desc=f"re-judge ({judge})")
    new_verdict = dict(zip(jobs, verdicts))
    pairs = [(bool(seeds[i]["clean_grades"][j]["judge_correct"]), new_verdict[(i, j)]) for i, j in jobs]

    # Recompute the freeze with the second judge (same rule: every model correct).
    def passes(i: int, use_new: bool) -> bool:
        ok = []
        for j, g in enumerate(seeds[i]["clean_grades"]):
            if use_new and (i, j) in new_verdict:
                ok.append(new_verdict[(i, j)])
            else:
                ok.append(bool(g["correct"]))
        return all(ok)

    old_pass = [i for i in range(len(seeds)) if passes(i, False)]
    new_pass = [i for i in range(len(seeds)) if passes(i, True)]
    limit = len(frozen)
    old_set = {seeds[i]["metadata"].get("hotpot_id") for i in old_pass[:limit]}
    new_set = {seeds[i]["metadata"].get("hotpot_id") for i in new_pass[:limit]}

    report = {
        "run": run,
        "original_judge": "gpt-oss",
        "second_judge": judge,
        "n_candidates": len(seeds),
        "n_judge_calls": len(jobs),
        "agreement": sum(a == b for a, b in pairs) / len(pairs) if pairs else None,
        "cohen_kappa": _kappa(pairs),
        "original_true": sum(a for a, _ in pairs),
        "second_true": sum(b for _, b in pairs),
        "flip_true_to_false": sum(a and not b for a, b in pairs),
        "flip_false_to_true": sum(b and not a for a, b in pairs),
        "frozen_seeds": limit,
        "frozen_reproduced_by_original": old_set == frozen,
        "frozen_kept_under_second_judge": len(old_set & new_set),
        "frozen_dropped_under_second_judge": len(old_set - new_set),
    }
    write_json(out_dir / "judge_agreement.json", report)
    lines = [
        "# Judge independence check (P2 clean grading)",
        "",
        f"The P2 judge ({report['original_judge']}, also the guard) is re-asked with "
        f"`{judge}` on the {len(jobs)} of {2 * len(seeds)} clean answers where it was called "
        "(not an exact match, F1 < 0.6). P5 scoring is rule-based and never calls a judge.",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Judge calls re-asked | {len(jobs)} |",
        f"| Agreement | {report['agreement']:.3f} |" if report["agreement"] is not None else "| Agreement | — |",
        f"| Cohen's κ | {report['cohen_kappa']:.3f} |" if report["cohen_kappa"] is not None else "| Cohen's κ | — |",
        f"| Judged correct: gpt-oss / {judge} | {report['original_true']} / {report['second_true']} |",
        f"| Flips correct → wrong / wrong → correct | {report['flip_true_to_false']} / {report['flip_false_to_true']} |",
        f"| Frozen seeds kept under {judge} | {report['frozen_kept_under_second_judge']} / {limit} |",
        "",
    ]
    (out_dir / "judge_agreement.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return report

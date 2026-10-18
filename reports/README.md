# Reports

Paper-facing results of the v2 protocol ([model.md](../model.md)). Nothing here calls an LLM;
every file is built from saved run outputs under `data/runs/v2_*/`.

| File | What it is | How it is produced |
|---|---|---|
| [v2_results.md](v2_results.md) | All results: primary hypotheses, Main, E1–E3, E5–E7, attack validity, judge and guard health | `gurma v2-report`. Do not edit by hand. |
| [v2_hypotheses.md](v2_hypotheses.md), [v2_hypotheses.json](v2_hypotheses.json) | Primary hypotheses H0–H7: seed-level permutation tests, cluster-bootstrap CIs, sensitivity bounds, Holm | `gurma v2-hypotheses` (also run by `gurma v2-report`) |
| [human_review/manifest.json](human_review/manifest.json) | The 160 items drawn for human review of the judge (ids and strata only) | `gurma v2-review-export` |

Every table is per attack distribution (known templates, Gemma unseen), never pooled
(model.md §9). Results and their interpretation are in model.md §13–§15.

## Legacy results

The legacy benchmark report (`main-e1-e7-results.md`, produced by `gurma report`) was removed
on 2026-10-18. It is in git history (last version: commit `fd9cc62`). Legacy results are not
comparable to v2 (model.md §8).

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 556 | 0.000 | 0.000 | 0.000 | — | 0.020 | 12395 | 847 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.070 | 10755 | 779 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3415 | 230 |
| context_poisoning | 180 | 0.000 | 0.000 | 0.000 | — | 0.006 | 11572 | 963 |
| indirect_injection | 92 | 0.000 | 0.000 | 0.000 | — | 0.022 | 14383 | 1316 |
| policy_retrieval | 84 | 0.000 | 0.000 | 0.000 | — | 0.012 | 14032 | 900 |

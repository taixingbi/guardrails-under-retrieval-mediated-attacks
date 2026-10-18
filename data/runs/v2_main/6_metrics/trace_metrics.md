# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 2236 | 0.000 | 0.001 | 0.000 | — | 0.020 | 11735 | 870 |
| authority_conflict | 396 | 0.000 | 0.005 | 0.000 | — | 0.073 | 12062 | 852 |
| clean | 400 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3523 | 234 |
| context_poisoning | 712 | 0.000 | 0.000 | 0.000 | — | 0.004 | 11585 | 925 |
| indirect_injection | 380 | 0.003 | 0.000 | 0.000 | — | 0.032 | 15168 | 1362 |
| policy_retrieval | 348 | 0.000 | 0.000 | 0.000 | — | 0.000 | 11810 | 974 |

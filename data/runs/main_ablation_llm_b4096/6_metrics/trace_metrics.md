# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 2000 | 0.001 | 0.001 | 0.000 | — | 0.022 | 12362 | 992 |
| authority_conflict | 400 | 0.000 | 0.000 | 0.000 | — | 0.090 | 13645 | 1037 |
| clean | 400 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3671 | 232 |
| context_poisoning | 400 | 0.000 | 0.000 | 0.000 | — | 0.005 | 11536 | 826 |
| indirect_injection | 400 | 0.003 | 0.003 | 0.000 | — | 0.008 | 17077 | 1504 |
| policy_retrieval | 400 | 0.000 | 0.000 | 0.000 | — | 0.005 | 14782 | 1363 |

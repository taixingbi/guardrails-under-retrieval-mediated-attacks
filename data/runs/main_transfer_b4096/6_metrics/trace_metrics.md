# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 600 | 0.008 | 0.008 | 0.000 | — | 0.017 | 14617 | 1310 |
| authority_conflict | 200 | 0.000 | 0.000 | 0.000 | — | 0.005 | 13917 | 1106 |
| indirect_injection | 200 | 0.005 | 0.005 | 0.000 | — | 0.035 | 16235 | 1439 |
| policy_retrieval | 200 | 0.020 | 0.020 | 0.000 | — | 0.010 | 14808 | 1386 |

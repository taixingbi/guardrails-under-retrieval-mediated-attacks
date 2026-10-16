# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 500 | 0.084 | 0.084 | 0.000 | — | 0.031 | 9906 | 984 |
| authority_conflict | 100 | 0.080 | 0.080 | 0.000 | — | 0.120 | 10039 | 1005 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3306 | 218 |
| context_poisoning | 100 | 0.050 | 0.050 | 0.000 | — | 0.011 | 8707 | 855 |
| indirect_injection | 100 | 0.190 | 0.190 | 0.000 | — | 0.012 | 11232 | 1470 |
| policy_retrieval | 100 | 0.100 | 0.100 | 0.000 | — | 0.011 | 9497 | 1372 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 300 | 0.003 | 0.000 | 0.000 | — | 0.000 | 5527 | 186 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 5527 | 218 |
| indirect_injection | 100 | 0.010 | 0.000 | 0.000 | — | 0.000 | 5966 | 201 |
| policy_retrieval | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 4050 | 138 |

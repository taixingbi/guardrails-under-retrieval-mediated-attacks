# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 300 | 0.033 | 0.000 | 0.000 | — | 0.007 | 1725 | 247 |
| authority_conflict | 100 | 0.060 | 0.000 | 0.000 | — | 0.000 | 1932 | 292 |
| indirect_injection | 100 | 0.020 | 0.000 | 0.000 | — | 0.020 | 1725 | 252 |
| policy_retrieval | 100 | 0.020 | 0.000 | 0.000 | — | 0.000 | 1559 | 196 |

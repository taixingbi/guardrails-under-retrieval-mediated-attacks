# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 552 | 0.000 | 0.000 | 0.000 | — | 0.004 | 5913 | 335 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2306 | 166 |
| context_poisoning | 252 | 0.000 | 0.000 | 0.000 | — | 0.008 | 8544 | 537 |
| indirect_injection | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2388 | 167 |
| policy_retrieval | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2410 | 164 |

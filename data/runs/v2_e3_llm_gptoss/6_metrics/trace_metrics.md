# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 239 | 0.000 | 0.000 | 0.000 | — | 0.013 | 12297 | 894 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.020 | 11333 | 1046 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3330 | 211 |
| context_poisoning | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 12297 | 854 |
| indirect_injection | 50 | 0.000 | 0.000 | 0.000 | — | 0.040 | 14761 | 1386 |
| policy_retrieval | 43 | 0.000 | 0.000 | 0.000 | — | 0.000 | 14069 | 983 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 234 | 0.004 | 0.000 | 0.000 | — | 0.004 | 2375 | 241 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 584 | 86 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.020 | 1342 | 284 |
| context_poisoning | 46 | 0.022 | 0.000 | 0.000 | — | 0.000 | 3583 | 356 |
| indirect_injection | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1226 | 170 |
| policy_retrieval | 42 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2707 | 328 |

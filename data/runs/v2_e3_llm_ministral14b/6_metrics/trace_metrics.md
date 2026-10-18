# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 239 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2747 | 124 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 765 | 55 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2536 | 117 |
| context_poisoning | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3834 | 224 |
| indirect_injection | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1027 | 74 |
| policy_retrieval | 43 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3777 | 160 |

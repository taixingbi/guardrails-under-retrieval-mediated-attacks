# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 234 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3383 | 131 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 818 | 55 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 6860 | 114 |
| context_poisoning | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 6057 | 286 |
| indirect_injection | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1410 | 68 |
| policy_retrieval | 42 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3546 | 142 |

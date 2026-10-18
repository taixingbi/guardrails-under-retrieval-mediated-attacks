# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 556 | 0.000 | 0.000 | 0.000 | — | 0.029 | 11040 | 810 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.130 | 10353 | 718 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3566 | 239 |
| context_poisoning | 180 | 0.000 | 0.000 | 0.000 | — | 0.000 | 12436 | 904 |
| indirect_injection | 92 | 0.000 | 0.000 | 0.000 | — | 0.033 | 11729 | 1314 |
| policy_retrieval | 84 | 0.000 | 0.000 | 0.000 | — | 0.000 | 9311 | 847 |

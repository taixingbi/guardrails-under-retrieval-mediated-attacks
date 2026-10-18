# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 478 | 0.000 | 0.000 | 0.000 | — | 0.019 | 11123 | 853 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.070 | 10259 | 882 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3469 | 256 |
| context_poisoning | 92 | 0.000 | 0.000 | 0.000 | — | 0.000 | 11012 | 868 |
| indirect_injection | 100 | 0.000 | 0.000 | 0.000 | — | 0.020 | 13454 | 1315 |
| policy_retrieval | 86 | 0.000 | 0.000 | 0.000 | — | 0.000 | 12480 | 961 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 932 | 0.000 | 0.000 | 0.000 | — | 0.002 | 5808 | 396 |
| authority_conflict | 192 | 0.000 | 0.000 | 0.000 | — | 0.005 | 6898 | 522 |
| clean | 200 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2918 | 165 |
| context_poisoning | 164 | 0.000 | 0.000 | 0.000 | — | 0.000 | 6061 | 354 |
| indirect_injection | 196 | 0.000 | 0.000 | 0.000 | — | 0.000 | 7173 | 499 |
| policy_retrieval | 180 | 0.000 | 0.000 | 0.000 | — | 0.006 | 5076 | 446 |

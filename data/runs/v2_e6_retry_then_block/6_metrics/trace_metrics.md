# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 556 | 0.000 | 0.000 | 0.000 | — | 0.023 | 10611 | 826 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.090 | 9831 | 786 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3684 | 239 |
| context_poisoning | 180 | 0.000 | 0.000 | 0.000 | — | 0.000 | 10924 | 903 |
| indirect_injection | 92 | 0.000 | 0.000 | 0.000 | — | 0.043 | 10669 | 1222 |
| policy_retrieval | 84 | 0.000 | 0.000 | 0.000 | — | 0.000 | 11983 | 975 |

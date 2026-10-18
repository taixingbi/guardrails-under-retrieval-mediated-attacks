# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 556 | 0.000 | 0.000 | 0.000 | — | 0.023 | 11064 | 854 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.090 | 10794 | 890 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3826 | 233 |
| context_poisoning | 180 | 0.000 | 0.000 | 0.000 | — | 0.000 | 9915 | 896 |
| indirect_injection | 92 | 0.000 | 0.000 | 0.000 | — | 0.033 | 13914 | 1251 |
| policy_retrieval | 84 | 0.000 | 0.000 | 0.000 | — | 0.012 | 13935 | 1024 |

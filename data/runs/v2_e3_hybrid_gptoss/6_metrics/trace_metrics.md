# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 234 | 0.000 | 0.000 | 0.000 | — | 0.021 | 12736 | 804 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.080 | 12289 | 748 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 5735 | 237 |
| context_poisoning | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 10023 | 771 |
| indirect_injection | 46 | 0.000 | 0.000 | 0.000 | — | 0.022 | 18223 | 1335 |
| policy_retrieval | 42 | 0.000 | 0.000 | 0.000 | — | 0.000 | 11077 | 1001 |

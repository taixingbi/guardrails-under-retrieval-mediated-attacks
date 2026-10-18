# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 239 | 0.008 | 0.000 | 0.000 | — | 0.004 | 1954 | 241 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 614 | 89 |
| clean | 50 | 0.020 | 0.000 | 0.000 | — | 0.000 | 1911 | 296 |
| context_poisoning | 46 | 0.022 | 0.000 | 0.000 | — | 0.022 | 2005 | 286 |
| indirect_injection | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2016 | 222 |
| policy_retrieval | 43 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2916 | 327 |

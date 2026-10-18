# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 234 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2002 | 129 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 897 | 78 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2256 | 170 |
| context_poisoning | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2934 | 191 |
| indirect_injection | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1010 | 89 |
| policy_retrieval | 42 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1643 | 119 |

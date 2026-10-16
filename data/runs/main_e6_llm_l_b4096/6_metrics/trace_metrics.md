# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 200 | 0.000 | 0.000 | 0.000 | — | 0.110 | 1387 | 53 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1187 | 44 |
| context_poisoning | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1424 | 84 |
| indirect_injection | 50 | 0.000 | 0.000 | 0.000 | — | 0.440 | 975 | 38 |
| policy_retrieval | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1522 | 46 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 300 | 0.023 | 0.000 | 0.000 | — | 0.048 | 2896 | 44 |
| authority_conflict | 100 | 0.070 | 0.000 | 0.000 | — | 0.022 | 2737 | 44 |
| indirect_injection | 100 | 0.000 | 0.000 | 0.000 | — | 0.060 | 4445 | 41 |
| policy_retrieval | 100 | 0.000 | 0.000 | 0.000 | — | 0.060 | 2979 | 47 |

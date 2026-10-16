# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 300 | 0.027 | 0.000 | 0.000 | — | 0.048 | 3322 | 45 |
| authority_conflict | 100 | 0.080 | 0.000 | 0.000 | — | 0.022 | 3765 | 46 |
| indirect_injection | 100 | 0.000 | 0.000 | 0.000 | — | 0.060 | 3230 | 41 |
| policy_retrieval | 100 | 0.000 | 0.000 | 0.000 | — | 0.060 | 3322 | 47 |

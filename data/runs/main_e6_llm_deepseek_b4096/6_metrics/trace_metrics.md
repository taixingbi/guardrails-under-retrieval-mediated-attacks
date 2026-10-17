# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 200 | 0.000 | 0.000 | 0.000 | — | 0.000 | 39183 | 921 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 37678 | 901 |
| context_poisoning | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 38363 | 556 |
| indirect_injection | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 51391 | 1069 |
| policy_retrieval | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 39183 | 1157 |

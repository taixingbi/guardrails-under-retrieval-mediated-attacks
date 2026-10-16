# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 300 | 0.043 | 0.000 | 0.000 | — | 0.003 | 2025 | 254 |
| authority_conflict | 100 | 0.060 | 0.000 | 0.000 | — | 0.000 | 1844 | 278 |
| indirect_injection | 100 | 0.060 | 0.000 | 0.000 | — | 0.011 | 2059 | 267 |
| policy_retrieval | 100 | 0.010 | 0.000 | 0.000 | — | 0.000 | 2025 | 217 |

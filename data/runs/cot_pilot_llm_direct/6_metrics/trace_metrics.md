# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 200 | 0.000 | 0.000 | 0.000 | — | 0.015 | 12087 | 1013 |
| authority_conflict | 40 | 0.000 | 0.000 | 0.000 | — | 0.050 | 11111 | 1009 |
| clean | 40 | 0.000 | 0.000 | 0.000 | — | 0.000 | 5330 | 302 |
| context_poisoning | 40 | 0.000 | 0.000 | 0.000 | — | 0.000 | 8980 | 911 |
| indirect_injection | 40 | 0.000 | 0.000 | 0.000 | — | 0.000 | 20886 | 1448 |
| policy_retrieval | 40 | 0.000 | 0.000 | 0.000 | — | 0.025 | 13289 | 1392 |

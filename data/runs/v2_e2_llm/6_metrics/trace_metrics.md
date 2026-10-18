# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 1732 | 0.000 | 0.001 | 0.000 | — | 0.025 | 11779 | 1017 |
| authority_conflict | 400 | 0.000 | 0.003 | 0.000 | — | 0.080 | 12078 | 965 |
| clean | 200 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3790 | 237 |
| context_poisoning | 356 | 0.000 | 0.000 | 0.000 | — | 0.000 | 10753 | 896 |
| indirect_injection | 400 | 0.000 | 0.000 | 0.000 | — | 0.022 | 12853 | 1438 |
| policy_retrieval | 376 | 0.000 | 0.000 | 0.000 | — | 0.008 | 13066 | 1156 |

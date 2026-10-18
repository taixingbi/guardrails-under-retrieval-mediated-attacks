# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 556 | 0.000 | 0.000 | 0.000 | — | 0.020 | 11774 | 867 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.090 | 10850 | 823 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3892 | 245 |
| context_poisoning | 180 | 0.000 | 0.000 | 0.000 | — | 0.000 | 13467 | 983 |
| indirect_injection | 92 | 0.000 | 0.000 | 0.000 | — | 0.022 | 14888 | 1306 |
| policy_retrieval | 84 | 0.000 | 0.000 | 0.000 | — | 0.000 | 11687 | 932 |

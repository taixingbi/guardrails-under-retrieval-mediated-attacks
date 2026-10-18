# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 556 | 0.002 | 0.000 | 0.000 | — | 0.016 | 10753 | 838 |
| authority_conflict | 100 | 0.010 | 0.000 | 0.000 | — | 0.071 | 9524 | 784 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3993 | 225 |
| context_poisoning | 180 | 0.000 | 0.000 | 0.000 | — | 0.000 | 10754 | 934 |
| indirect_injection | 92 | 0.000 | 0.000 | 0.000 | — | 0.022 | 18023 | 1329 |
| policy_retrieval | 84 | 0.000 | 0.000 | 0.000 | — | 0.000 | 11751 | 886 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 234 | 0.000 | 0.000 | 0.000 | — | 0.162 | 919 | 52 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.080 | 785 | 45 |
| clean | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 821 | 50 |
| context_poisoning | 46 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1193 | 75 |
| indirect_injection | 46 | 0.000 | 0.000 | 0.000 | — | 0.739 | 838 | 42 |
| policy_retrieval | 42 | 0.000 | 0.000 | 0.000 | — | 0.000 | 752 | 51 |

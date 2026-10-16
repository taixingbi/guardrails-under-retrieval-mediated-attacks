# Input-guard trace metrics

Prompt versions: moderation

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 800 | 0.000 | 0.000 | 0.000 | — | 0.800 | 11886 | 1060 |
| authority_conflict | 200 | 0.000 | 0.000 | 0.000 | — | 1.000 | 8847 | 653 |
| context_poisoning | 200 | 0.000 | 0.000 | 0.000 | — | 0.200 | 13945 | 1315 |
| indirect_injection | 200 | 0.000 | 0.000 | 0.000 | — | 1.000 | 13015 | 1491 |
| policy_retrieval | 200 | 0.000 | 0.000 | 0.000 | — | 1.000 | 10098 | 780 |

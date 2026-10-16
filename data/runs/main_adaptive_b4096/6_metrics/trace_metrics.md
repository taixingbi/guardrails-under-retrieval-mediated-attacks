# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 600 | 0.042 | 0.010 | 0.000 | — | 0.056 | 11629 | 1127 |
| authority_conflict | 200 | 0.105 | 0.010 | 0.000 | — | 0.028 | 9199 | 601 |
| indirect_injection | 200 | 0.015 | 0.015 | 0.000 | — | 0.122 | 11325 | 1243 |
| policy_retrieval | 200 | 0.005 | 0.005 | 0.000 | — | 0.015 | 12808 | 1538 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 300 | 0.013 | 0.000 | 0.000 | — | 0.000 | 5187 | 181 |
| authority_conflict | 100 | 0.000 | 0.000 | 0.000 | — | 0.000 | 6311 | 224 |
| indirect_injection | 100 | 0.030 | 0.000 | 0.000 | — | 0.000 | 5610 | 208 |
| policy_retrieval | 100 | 0.010 | 0.000 | 0.000 | — | 0.000 | 2749 | 110 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1312 | 79 |
| context_poisoning | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 1312 | 79 |

# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 692 | 0.000 | 0.000 | 0.000 | — | 0.001 | 8812 | 471 |
| clean | 400 | 0.000 | 0.000 | 0.000 | — | 0.000 | 3754 | 233 |
| context_poisoning | 292 | 0.000 | 0.000 | 0.000 | — | 0.003 | 10391 | 798 |

# Input-guard trace metrics

Prompt versions: v3-cot

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 346 | 0.003 | 0.000 | 0.986 | 0.957 | 0.000 | 13916 | 895 |
| clean | 200 | 0.000 | 0.000 | 0.985 | 0.963 | 0.000 | 6120 | 485 |
| context_poisoning | 146 | 0.007 | 0.000 | 0.986 | 0.950 | 0.000 | 22563 | 1456 |

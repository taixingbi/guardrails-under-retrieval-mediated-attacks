# Input-guard trace metrics

Prompt versions: v3-cot

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 200 | 0.000 | 0.000 | 1.000 | 0.964 | 0.000 | 14972 | 1804 |
| context_poisoning | 200 | 0.000 | 0.000 | 1.000 | 0.964 | 0.000 | 14972 | 1804 |

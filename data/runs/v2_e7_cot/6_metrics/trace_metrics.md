# Input-guard trace metrics

Prompt versions: v3-cot

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 478 | 0.000 | 0.000 | 0.996 | 0.976 | 0.002 | 15498 | 1535 |
| authority_conflict | 100 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 15236 | 1988 |
| clean | 100 | 0.000 | 0.000 | 0.990 | 0.969 | 0.000 | 8292 | 577 |
| context_poisoning | 92 | 0.000 | 0.000 | 0.989 | 0.968 | 0.000 | 13271 | 1377 |
| indirect_injection | 100 | 0.000 | 0.000 | 1.000 | 0.961 | 0.000 | 17716 | 2042 |
| policy_retrieval | 86 | 0.000 | 0.000 | 1.000 | 0.990 | 0.012 | 17102 | 1700 |

# Input-guard trace metrics

Prompt versions: v3-cot

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 1000 | 0.000 | 0.000 | 0.999 | 0.972 | 0.000 | 14814 | 1503 |
| authority_conflict | 200 | 0.000 | 0.000 | 1.000 | 0.973 | 0.000 | 14647 | 1866 |
| clean | 200 | 0.000 | 0.000 | 0.995 | 0.958 | 0.000 | 6680 | 512 |
| context_poisoning | 200 | 0.000 | 0.000 | 1.000 | 0.950 | 0.000 | 15083 | 1601 |
| indirect_injection | 200 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 18025 | 2006 |
| policy_retrieval | 200 | 0.000 | 0.000 | 1.000 | 0.991 | 0.000 | 14486 | 1528 |

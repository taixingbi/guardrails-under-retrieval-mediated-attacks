# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 500 | 0.312 | 0.320 | 0.000 | — | 0.015 | 8191 | 882 |
| authority_conflict | 100 | 0.280 | 0.300 | 0.000 | — | 0.069 | 8927 | 955 |
| clean | 100 | 0.010 | 0.010 | 0.000 | — | 0.000 | 3072 | 217 |
| context_poisoning | 100 | 0.200 | 0.200 | 0.000 | — | 0.000 | 7887 | 785 |
| indirect_injection | 100 | 0.570 | 0.570 | 0.000 | — | 0.000 | 8140 | 1253 |
| policy_retrieval | 100 | 0.500 | 0.520 | 0.000 | — | 0.000 | 8409 | 1201 |

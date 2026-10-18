# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 1978 | 0.000 | 0.000 | 0.000 | — | 0.009 | 9479 | 564 |
| authority_conflict | 400 | 0.000 | 0.000 | 0.000 | — | 0.028 | 8503 | 464 |
| clean | 300 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2926 | 213 |
| context_poisoning | 540 | 0.000 | 0.000 | 0.000 | — | 0.000 | 9947 | 686 |
| indirect_injection | 384 | 0.000 | 0.000 | 0.000 | — | 0.016 | 10130 | 737 |
| policy_retrieval | 354 | 0.000 | 0.000 | 0.000 | — | 0.000 | 9745 | 598 |

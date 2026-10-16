# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 200 | 0.015 | 0.000 | 0.000 | — | 0.000 | 1134 | 146 |
| authority_conflict | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 596 | 83 |
| context_poisoning | 50 | 0.040 | 0.000 | 0.000 | — | 0.000 | 2119 | 270 |
| indirect_injection | 50 | 0.000 | 0.000 | 0.000 | — | 0.000 | 661 | 98 |
| policy_retrieval | 50 | 0.020 | 0.000 | 0.000 | — | 0.000 | 1264 | 133 |

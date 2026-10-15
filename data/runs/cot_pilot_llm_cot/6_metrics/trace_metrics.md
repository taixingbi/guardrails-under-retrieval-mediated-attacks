# Input-guard trace metrics

Prompt versions: v3-cot

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 200 | 0.010 | 0.000 | 1.000 | 0.986 | 0.000 | 20952 | 1452 |
| authority_conflict | 40 | 0.025 | 0.000 | 1.000 | 1.000 | 0.000 | 17732 | 1828 |
| clean | 40 | 0.000 | 0.000 | 1.000 | 0.967 | 0.000 | 6547 | 615 |
| context_poisoning | 40 | 0.000 | 0.000 | 1.000 | 0.969 | 0.000 | 20069 | 1575 |
| indirect_injection | 40 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 23851 | 1977 |
| policy_retrieval | 40 | 0.025 | 0.000 | 1.000 | 1.000 | 0.000 | 12280 | 1266 |

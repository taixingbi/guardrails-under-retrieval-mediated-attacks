# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 460 | 0.009 | 0.009 | 0.000 | — | 0.002 | 11475 | 898 |
| authority_conflict | 80 | 0.000 | 0.000 | 0.000 | — | 0.013 | 11239 | 986 |
| clean | 80 | 0.000 | 0.000 | 0.000 | — | 0.000 | 2735 | 185 |
| context_poisoning | 160 | 0.000 | 0.000 | 0.000 | — | 0.000 | 10521 | 944 |
| indirect_injection | 72 | 0.042 | 0.042 | 0.000 | — | 0.000 | 19084 | 1337 |
| policy_retrieval | 68 | 0.015 | 0.015 | 0.000 | — | 0.000 | 11060 | 1060 |

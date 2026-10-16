# Input-guard trace metrics

Prompt versions: v3

Only calls that reached the LLM guard (hybrid rule hits excluded). Sig≠Dec is a heuristic: signals listed but allow, or none listed but sanitize/block.

| Slice | n | JSON fail | Trunc | Cites | Verbatim | Sig≠Dec | P95 ms | Out tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 500 | 0.438 | 0.442 | 0.000 | — | 0.043 | 8356 | 682 |
| authority_conflict | 100 | 0.450 | 0.450 | 0.000 | — | 0.164 | 9505 | 752 |
| clean | 100 | 0.000 | 0.000 | 0.000 | — | 0.010 | 3690 | 221 |
| context_poisoning | 100 | 0.280 | 0.280 | 0.000 | — | 0.000 | 7757 | 663 |
| indirect_injection | 100 | 0.780 | 0.790 | 0.000 | — | 0.000 | 8923 | 896 |
| policy_retrieval | 100 | 0.680 | 0.690 | 0.000 | — | 0.062 | 8494 | 880 |

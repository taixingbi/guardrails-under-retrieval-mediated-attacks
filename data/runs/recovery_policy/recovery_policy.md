# E6 recovery policies (LLM-only G1)

Initial guard call at 768 tokens: 218 of 500 conditions unparseable (50 seeds × 4 attacks + clean × 2 models). A retry at budget R reuses the run at that budget on the same condition (temperature 0); the F3 fallback uses the rules-only decision and blocks when the rules found nothing to remove. No LLM calls.

| Policy | Retry budget | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ | False block ↓ |
|---|---:|---:|---:|---:|---:|---:|
| F0 fail-open | — | 0.440 | 0.320 | 0.427 | 0.910 | 0.000 |
| F1 fail-closed | — | 0.013 | 0.150 | 0.312 | 0.860 | 0.050 |
| F2 retry → block | 1024 | 0.017 | 0.190 | 0.410 | 0.890 | 0.000 |
| F3 retry → rules sanitize → block | 1024 | 0.017 | 0.190 | 0.700 | 0.890 | 0.000 |
| F2 retry → block | 1536 | 0.013 | 0.190 | 0.505 | 0.880 | 0.010 |
| F3 retry → rules sanitize → block | 1536 | 0.013 | 0.200 | 0.730 | 0.880 | 0.010 |
| F2 retry → block | 2048 | 0.027 | 0.200 | 0.667 | 0.880 | 0.000 |
| F3 retry → rules sanitize → block | 2048 | 0.027 | 0.200 | 0.728 | 0.880 | 0.000 |
| F2 retry → block | 4096 | 0.030 | 0.220 | 0.720 | 0.880 | 0.000 |
| F3 retry → rules sanitize → block | 4096 | 0.030 | 0.220 | 0.720 | 0.880 | 0.000 |

Recovery cost (retry policies only):

| Policy | Retry budget | Retried | Recovered | Recovery rate | Rules fallback | Extra calls / request | Extra out tokens / request | Tokens / recovered decision | Added latency mean / P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F2 | 1024 | 218 | 76 | 0.349 | 0 | 0.44 | 377 | 2477 | 2115 / 6572 |
| F3 | 1024 | 218 | 76 | 0.349 | 128 | 0.44 | 377 | 2477 | 2115 / 6572 |
| F2 | 1536 | 218 | 114 | 0.523 | 0 | 0.44 | 523 | 2292 | 2372 / 7774 |
| F3 | 1536 | 218 | 114 | 0.523 | 96 | 0.44 | 523 | 2292 | 2372 / 7774 |
| F2 | 2048 | 218 | 189 | 0.867 | 0 | 0.44 | 591 | 1564 | 2653 / 9327 |
| F3 | 2048 | 218 | 189 | 0.867 | 27 | 0.44 | 591 | 1564 | 2653 / 9327 |
| F2 | 4096 | 218 | 218 | 1.000 | 0 | 0.44 | 554 | 1271 | 2591 / 9345 |
| F3 | 4096 | 218 | 218 | 1.000 | 0 | 0.44 | 554 | 1271 | 2591 / 9345 |

Approximation: a retry is an independent run on the same condition, not a second call inside one request. Costs are what retries add; the 768 attempt itself is not measured.

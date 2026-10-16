# E6 budget sweep (LLM-only G1)

gpt-oss guard, direct prompt, fail-open, first 50 seeds × 4 attacks + clean × 2 target models. Only `guardrail_max_tokens` changes. 768 and 4096 are the main LLM-only runs restricted to the same seeds.

| Guard budget | n | Parse fail | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ | Mean guard out tokens | Guard P95 ms |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 768 | 500 | 0.436 | 0.440 | 0.320 | 0.427 | 0.910 | — | — |
| 1024 | 500 | 0.438 | 0.490 | 0.350 | 0.388 | 0.880 | 682 | 8356 |
| 1536 | 500 | 0.312 | 0.337 | 0.310 | 0.492 | 0.880 | 882 | 8191 |
| 2048 | 500 | 0.084 | 0.113 | 0.250 | 0.710 | 0.880 | 984 | 9906 |
| 4096 | 500 | 0.000 | 0.027 | 0.210 | 0.770 | 0.880 | 956 | 10138 |

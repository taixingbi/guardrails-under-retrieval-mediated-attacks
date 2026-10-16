# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 600 (clean=0, attack=600)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 50
- indirect_injection: 50
- policy_retrieval: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.560 [0.480, 0.640] | 0.500 [0.360, 0.640] | 0.545 [0.480, 0.615] | 0.450 [0.385, 0.520] | — |
| G1 | 0.000 [0.000, 0.000] | 0.120 [0.040, 0.220] | 0.030 [0.010, 0.055] | 0.915 [0.875, 0.950] | — |
| G2 | 0.000 [0.000, 0.000] | 0.140 [0.060, 0.240] | 0.035 [0.010, 0.060] | 0.915 [0.875, 0.950] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.940 [0.860, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.500 [0.360, 0.640] | 0.120 [0.040, 0.220] | 0.140 [0.060, 0.240] |
| indirect_injection | 0.700 [0.560, 0.820] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.040 [0.000, 0.100] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| deepseek | 0.560 [0.480, 0.640] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 200 | 783.9 | 526.1 | 1869.9 | 1.0 |
| G1 | 200 | 1655.4 | 588.6 | 7579.8 | 1.0 |
| G2 | 200 | 2653.1 | 1638.8 | 7589.8 | 2.0 |

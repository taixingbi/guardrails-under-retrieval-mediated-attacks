# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1300 (clean=100, attack=1200)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 50
- indirect_injection: 50
- policy_retrieval: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.697 [0.647, 0.753] | 0.510 [0.410, 0.610] | 0.650 [0.605, 0.698] | 0.275 [0.233, 0.320] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.360 [0.270, 0.450] | 0.090 [0.062, 0.117] | 0.843 [0.807, 0.875] | — |
| G2 | 0.000 [0.000, 0.000] | 0.370 [0.280, 0.460] | 0.092 [0.065, 0.122] | 0.840 [0.805, 0.875] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.560 [0.470, 0.660] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.510 [0.420, 0.620] | 0.360 [0.270, 0.450] | 0.370 [0.280, 0.470] |
| indirect_injection | 0.900 [0.840, 0.950] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.630 [0.530, 0.720] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.987 [0.967, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| nova-pro | 0.407 [0.327, 0.487] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 500 | — | — | — | — |
| G1 | 400 | 1636.1 | 559.4 | 8083.1 | 1.0 |
| G2 | 400 | 2922.6 | 1613.7 | 9939.9 | 1.9 |

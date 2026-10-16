# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1000 (clean=200, attack=800)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 50
- indirect_injection: 50
- policy_retrieval: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.697 [0.647, 0.753] | 0.510 [0.410, 0.610] | 0.650 [0.605, 0.698] | 0.275 [0.233, 0.320] | 0.000 [0.000, 0.000] |
| G1 | 0.490 [0.437, 0.547] | 0.350 [0.260, 0.440] | 0.455 [0.405, 0.505] | 0.388 [0.340, 0.438] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.560 [0.470, 0.660] | 0.290 [0.200, 0.380] |
| context_poisoning | 0.510 [0.420, 0.620] | 0.350 [0.260, 0.440] |
| indirect_injection | 0.900 [0.840, 0.950] | 0.740 [0.650, 0.830] |
| policy_retrieval | 0.630 [0.530, 0.720] | 0.440 [0.340, 0.540] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.987 [0.967, 1.000] | 0.653 [0.573, 0.733] |
| nova-pro | 0.407 [0.327, 0.487] | 0.327 [0.253, 0.407] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 500 | — | — | — | — |
| G1 | 500 | 4453.6 | 4292.2 | 9343.8 | 1.9 |

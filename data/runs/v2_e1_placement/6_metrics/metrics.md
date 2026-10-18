# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 3464 (clean=400, attack=3064)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 0
- context_poisoning: 0
- indirect_injection: 0
- policy_retrieval: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| C | 0.012 [0.003, 0.020] | 0.322 [0.256, 0.389] | 0.085 [0.065, 0.107] | 0.698 [0.666, 0.731] | 0.000 [0.000, 0.000] |
| CO | 0.000 [0.000, 0.000] | 0.283 [0.217, 0.356] | 0.067 [0.050, 0.085] | 0.722 [0.689, 0.755] | 0.020 [0.000, 0.050] |
| O | 0.024 [0.012, 0.038] | 0.567 [0.489, 0.644] | 0.151 [0.125, 0.178] | 0.479 [0.443, 0.514] | 0.000 [0.000, 0.000] |
| Q | 0.401 [0.362, 0.440] | 0.589 [0.511, 0.661] | 0.445 [0.410, 0.482] | 0.469 [0.433, 0.505] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | C | CO | O | Q |
|---|---:|---:|---:|---:|
| authority_conflict | 0.020 [0.005, 0.040] | 0.000 [0.000, 0.000] | 0.045 [0.020, 0.075] | 0.390 [0.325, 0.460] |
| context_poisoning | 0.322 [0.256, 0.389] | 0.283 [0.217, 0.350] | 0.567 [0.494, 0.639] | 0.589 [0.517, 0.656] |
| indirect_injection | 0.015 [0.000, 0.035] | 0.000 [0.000, 0.000] | 0.020 [0.005, 0.040] | 0.485 [0.415, 0.560] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.005 [0.000, 0.016] | 0.323 [0.253, 0.392] |

## Table 4 — Cross-model Safety ASR

| Model | C | CO | O | Q |
|---|---:|---:|---:|---:|
| llama | 0.020 [0.007, 0.038] | 0.000 [0.000, 0.000] | 0.024 [0.007, 0.041] | 0.567 [0.512, 0.625] |
| nova-pro | 0.003 [0.000, 0.010] | 0.000 [0.000, 0.000] | 0.024 [0.007, 0.044] | 0.235 [0.191, 0.290] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| C | 866 | 3127.8 | 1946.4 | 9871.6 | 1.1 |
| CO | 866 | 4474.1 | 3235.7 | 11694.3 | 2.0 |
| O | 866 | 2127.6 | 1516.3 | 4917.1 | 2.0 |
| Q | 866 | 1705.3 | 1536.6 | 3118.4 | 2.0 |

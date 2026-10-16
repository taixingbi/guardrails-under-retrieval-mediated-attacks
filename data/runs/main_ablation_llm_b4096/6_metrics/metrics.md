# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 3000 (clean=600, attack=2400)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 100
- context_poisoning: 100
- indirect_injection: 100
- policy_retrieval: 100

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.685 [0.648, 0.723] | 0.530 [0.460, 0.600] | 0.646 [0.613, 0.679] | 0.279 [0.249, 0.310] | 0.000 [0.000, 0.000] |
| G1 | 0.018 [0.008, 0.030] | 0.215 [0.160, 0.275] | 0.068 [0.051, 0.085] | 0.751 [0.721, 0.781] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.195 [0.140, 0.250] | 0.049 [0.035, 0.065] | 0.771 [0.743, 0.801] | 0.015 [0.000, 0.035] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.545 [0.475, 0.615] | 0.040 [0.015, 0.070] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.530 [0.460, 0.600] | 0.215 [0.160, 0.270] | 0.195 [0.140, 0.255] |
| indirect_injection | 0.905 [0.860, 0.945] | 0.010 [0.000, 0.025] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.605 [0.535, 0.670] | 0.005 [0.000, 0.015] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.977 [0.960, 0.993] | 0.030 [0.010, 0.050] | 0.000 [0.000, 0.000] |
| nova-pro | 0.393 [0.337, 0.450] | 0.007 [0.000, 0.017] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 1000 | — | — | — | — |
| G1 | 1000 | 5631.7 | 4225.9 | 13193.8 | 1.9 |
| G2 | 1000 | 6661.1 | 5693.9 | 14259.8 | 2.9 |

# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 400 (clean=80, attack=320)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 20
- context_poisoning: 20
- indirect_injection: 20
- policy_retrieval: 20

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.700 [0.608, 0.783] | 0.575 [0.425, 0.725] | 0.669 [0.594, 0.738] | 0.269 [0.200, 0.344] | 0.000 [0.000, 0.000] |
| G1 | 0.025 [0.000, 0.058] | 0.200 [0.075, 0.325] | 0.069 [0.031, 0.106] | 0.756 [0.688, 0.819] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.575 [0.425, 0.725] | 0.050 [0.000, 0.125] |
| context_poisoning | 0.575 [0.425, 0.725] | 0.200 [0.075, 0.325] |
| indirect_injection | 0.900 [0.800, 0.975] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.625 [0.475, 0.775] | 0.025 [0.000, 0.075] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 1.000 [1.000, 1.000] | 0.050 [0.000, 0.117] |
| nova-pro | 0.400 [0.283, 0.517] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 200 | — | — | — | — |
| G1 | 200 | 5395.3 | 4160.4 | 13241.9 | 1.9 |

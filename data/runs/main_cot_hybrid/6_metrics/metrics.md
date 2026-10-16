# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 2000 (clean=400, attack=1600)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 100
- context_poisoning: 100
- indirect_injection: 100
- policy_retrieval: 100

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.685 [0.648, 0.723] | 0.530 [0.460, 0.600] | 0.646 [0.613, 0.679] | 0.279 [0.249, 0.310] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.190 [0.135, 0.245] | 0.048 [0.033, 0.064] | 0.850 [0.825, 0.874] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.545 [0.475, 0.615] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.530 [0.460, 0.600] | 0.190 [0.140, 0.250] |
| indirect_injection | 0.905 [0.860, 0.945] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.605 [0.535, 0.670] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.977 [0.960, 0.993] | 0.000 [0.000, 0.000] |
| nova-pro | 0.393 [0.337, 0.450] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 1000 | — | — | — | — |
| G1 | 1000 | 2608.5 | 710.1 | 10305.4 | 1.2 |

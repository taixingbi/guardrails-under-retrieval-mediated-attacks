# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1416 (clean=300, attack=1116)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 41
- indirect_injection: 50
- policy_retrieval: 45

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.117 [0.079, 0.159] | 0.573 [0.463, 0.683] | 0.218 [0.177, 0.263] | 0.629 [0.581, 0.677] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.476 [0.366, 0.585] | 0.105 [0.075, 0.137] | 0.640 [0.591, 0.688] | 0.020 [0.000, 0.050] |
| G2 | 0.000 [0.000, 0.000] | 0.451 [0.341, 0.561] | 0.099 [0.070, 0.132] | 0.651 [0.602, 0.696] | 0.020 [0.000, 0.050] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.210 [0.130, 0.290] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.573 [0.463, 0.683] | 0.476 [0.366, 0.585] | 0.451 [0.341, 0.561] |
| indirect_injection | 0.130 [0.070, 0.200] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.110 [0.062, 0.159] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| nova-pro | 0.124 [0.076, 0.179] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 472 | 379.2 | 349.2 | 513.8 | 1.0 |
| G1 | 472 | 2842.8 | 2530.5 | 6247.2 | 1.3 |
| G2 | 472 | 4024.4 | 3612.1 | 8037.7 | 2.2 |

# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 50 (clean=0, attack=50)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G1 | — | 0.400 [0.260, 0.540] | 0.400 [0.280, 0.540] | 0.600 [0.460, 0.740] | — |

## Table 3 — Attack breakdown

| Attack | G1 |
|---|---:|
| context_poisoning | 0.400 [0.280, 0.540] |

## Table 4 — Cross-model Safety ASR

| Model | G1 |
|---|---:|
| nova-pro | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G1 | 50 | 3569.0 | 2252.6 | 11261.2 | 0.9 |

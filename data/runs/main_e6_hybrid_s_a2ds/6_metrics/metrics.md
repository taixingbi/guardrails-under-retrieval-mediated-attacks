# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 50 (clean=0, attack=50)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G1 | — | 0.280 [0.160, 0.420] | 0.280 [0.160, 0.400] | 0.720 [0.600, 0.840] | — |

## Table 3 — Attack breakdown

| Attack | G1 |
|---|---:|
| context_poisoning | 0.280 [0.160, 0.400] |

## Table 4 — Cross-model Safety ASR

| Model | G1 |
|---|---:|
| nova-pro | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G1 | 50 | 4745.8 | 2764.0 | 17406.3 | 1.0 |

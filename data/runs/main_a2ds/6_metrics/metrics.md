# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 600 (clean=0, attack=600)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 100

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | — | 0.545 [0.475, 0.610] | 0.545 [0.475, 0.610] | 0.455 [0.390, 0.525] | — |
| G1 | — | 0.175 [0.125, 0.230] | 0.175 [0.125, 0.230] | 0.825 [0.770, 0.875] | — |
| G2 | — | 0.205 [0.150, 0.265] | 0.205 [0.150, 0.265] | 0.795 [0.740, 0.845] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| context_poisoning | 0.545 [0.475, 0.615] | 0.175 [0.125, 0.230] | 0.205 [0.150, 0.265] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | — | — | — |
| nova-pro | — | — | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 200 | 471.7 | 429.0 | 715.0 | 1.0 |
| G1 | 200 | 5653.3 | 4575.0 | 11844.6 | 1.1 |
| G2 | 200 | 7319.1 | 6117.2 | 15565.1 | 2.1 |

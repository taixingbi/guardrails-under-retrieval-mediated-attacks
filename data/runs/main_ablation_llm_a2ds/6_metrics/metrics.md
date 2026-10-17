# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 600 (clean=0, attack=600)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 100

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | — | 0.545 [0.475, 0.610] | 0.545 [0.475, 0.610] | 0.455 [0.390, 0.525] | — |
| G1 | — | 0.190 [0.140, 0.245] | 0.190 [0.140, 0.250] | 0.810 [0.755, 0.865] | — |
| G2 | — | 0.210 [0.155, 0.270] | 0.210 [0.155, 0.270] | 0.790 [0.735, 0.845] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| context_poisoning | 0.545 [0.475, 0.615] | 0.190 [0.140, 0.245] | 0.210 [0.160, 0.265] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | — | — | — |
| nova-pro | — | — | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 200 | 471.7 | 429.0 | 715.0 | 1.0 |
| G1 | 200 | 5791.4 | 4401.4 | 13986.0 | 2.0 |
| G2 | 200 | 7097.7 | 5929.3 | 13108.0 | 3.0 |

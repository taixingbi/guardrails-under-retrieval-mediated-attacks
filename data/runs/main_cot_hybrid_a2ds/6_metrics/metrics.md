# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 400 (clean=0, attack=400)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 100

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | — | 0.545 [0.475, 0.610] | 0.545 [0.475, 0.610] | 0.455 [0.390, 0.525] | — |
| G1 | — | 0.180 [0.125, 0.235] | 0.180 [0.130, 0.235] | 0.820 [0.765, 0.865] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| context_poisoning | 0.545 [0.475, 0.615] | 0.180 [0.130, 0.235] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | — | — |
| nova-pro | — | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 200 | 471.7 | 429.0 | 715.0 | 1.0 |
| G1 | 200 | 9137.4 | 9111.8 | 15870.4 | 1.1 |

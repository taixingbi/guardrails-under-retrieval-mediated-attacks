# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 300 (clean=0, attack=300)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | — | 0.490 [0.390, 0.580] | 0.490 [0.390, 0.590] | 0.510 [0.410, 0.610] | — |
| G1 | — | 0.360 [0.270, 0.460] | 0.360 [0.270, 0.450] | 0.640 [0.550, 0.730] | — |
| G2 | — | 0.350 [0.250, 0.440] | 0.350 [0.260, 0.440] | 0.650 [0.560, 0.740] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| context_poisoning | 0.490 [0.400, 0.590] | 0.360 [0.270, 0.450] | 0.350 [0.260, 0.450] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | — | — | — |
| nova-pro | — | — | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 100 | 524.8 | 387.5 | 644.3 | 1.0 |
| G1 | 100 | 3242.4 | 2953.5 | 7428.7 | 1.3 |
| G2 | 100 | 4861.0 | 4665.6 | 8396.1 | 2.2 |

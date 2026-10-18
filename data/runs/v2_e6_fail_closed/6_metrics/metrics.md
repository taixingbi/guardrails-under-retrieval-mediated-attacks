# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1732 (clean=200, attack=1532)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 100
- context_poisoning: 90
- indirect_injection: 100
- policy_retrieval: 93

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.392 [0.355, 0.435] | 0.572 [0.494, 0.650] | 0.435 [0.398, 0.470] | 0.466 [0.430, 0.503] | 0.000 [0.000, 0.000] |
| G1 | 0.005 [0.000, 0.012] | 0.322 [0.256, 0.389] | 0.080 [0.061, 0.101] | 0.702 [0.670, 0.735] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.390 [0.320, 0.465] | 0.010 [0.000, 0.025] |
| context_poisoning | 0.572 [0.500, 0.639] | 0.322 [0.256, 0.389] |
| indirect_injection | 0.485 [0.420, 0.555] | 0.005 [0.000, 0.015] |
| policy_retrieval | 0.296 [0.231, 0.366] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.563 [0.509, 0.618] | 0.003 [0.000, 0.010] |
| nova-pro | 0.222 [0.174, 0.270] | 0.007 [0.000, 0.017] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 866 | 493.7 | 410.6 | 817.5 | 1.0 |
| G1 | 866 | 3164.3 | 1911.9 | 10214.8 | 1.1 |

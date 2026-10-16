# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1000 (clean=200, attack=800)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 50
- indirect_injection: 50
- policy_retrieval: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.697 [0.647, 0.753] | 0.510 [0.410, 0.610] | 0.650 [0.605, 0.698] | 0.275 [0.233, 0.320] | 0.000 [0.000, 0.000] |
| G1 | 0.337 [0.287, 0.393] | 0.310 [0.220, 0.410] | 0.330 [0.285, 0.378] | 0.492 [0.443, 0.542] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.560 [0.470, 0.660] | 0.190 [0.110, 0.270] |
| context_poisoning | 0.510 [0.420, 0.620] | 0.310 [0.220, 0.400] |
| indirect_injection | 0.900 [0.840, 0.950] | 0.520 [0.420, 0.620] |
| policy_retrieval | 0.630 [0.530, 0.720] | 0.300 [0.220, 0.390] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.987 [0.967, 1.000] | 0.460 [0.380, 0.540] |
| nova-pro | 0.407 [0.327, 0.487] | 0.213 [0.147, 0.280] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 500 | — | — | — | — |
| G1 | 500 | 4729.7 | 4195.8 | 8953.7 | 1.9 |

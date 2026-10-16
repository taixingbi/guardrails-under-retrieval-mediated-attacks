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
| G1 | 0.113 [0.080, 0.153] | 0.250 [0.170, 0.340] | 0.147 [0.113, 0.182] | 0.710 [0.665, 0.755] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.560 [0.470, 0.660] | 0.080 [0.030, 0.140] |
| context_poisoning | 0.510 [0.420, 0.620] | 0.250 [0.170, 0.340] |
| indirect_injection | 0.900 [0.840, 0.950] | 0.190 [0.120, 0.270] |
| policy_retrieval | 0.630 [0.530, 0.720] | 0.070 [0.020, 0.120] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.987 [0.967, 1.000] | 0.160 [0.100, 0.220] |
| nova-pro | 0.407 [0.327, 0.487] | 0.067 [0.027, 0.107] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 500 | — | — | — | — |
| G1 | 500 | 5208.3 | 4394.3 | 10553.4 | 1.9 |

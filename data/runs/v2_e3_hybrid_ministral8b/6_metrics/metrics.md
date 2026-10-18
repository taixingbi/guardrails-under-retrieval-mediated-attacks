# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 478 (clean=100, attack=378)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 46
- indirect_injection: 50
- policy_retrieval: 43

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.119 [0.070, 0.175] | 0.543 [0.391, 0.696] | 0.222 [0.164, 0.280] | 0.709 [0.646, 0.772] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.522 [0.391, 0.674] | 0.127 [0.085, 0.175] | 0.169 [0.116, 0.222] | 0.020 [0.000, 0.060] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.220 [0.120, 0.340] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.543 [0.391, 0.674] | 0.522 [0.370, 0.674] |
| indirect_injection | 0.120 [0.040, 0.220] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| nova-pro | 0.119 [0.070, 0.175] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 239 | 489.0 | 430.0 | 713.4 | 1.0 |
| G1 | 239 | 1701.4 | 801.8 | 6368.0 | 0.5 |

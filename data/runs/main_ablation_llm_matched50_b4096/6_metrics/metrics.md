# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1000 (clean=200, attack=800)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 0
- context_poisoning: 0
- indirect_injection: 0
- policy_retrieval: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G1 | 0.027 [0.010, 0.047] | 0.210 [0.130, 0.290] | 0.072 [0.048, 0.100] | 0.770 [0.730, 0.810] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.200 [0.120, 0.280] | 0.050 [0.030, 0.072] | 0.805 [0.767, 0.843] | 0.020 [0.000, 0.050] |

## Table 3 — Attack breakdown

| Attack | G1 | G2 |
|---|---:|---:|
| authority_conflict | 0.050 [0.010, 0.090] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.210 [0.130, 0.290] | 0.200 [0.130, 0.280] |
| indirect_injection | 0.020 [0.000, 0.050] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.010 [0.000, 0.030] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G1 | G2 |
|---|---:|---:|
| llama | 0.040 [0.013, 0.073] | 0.000 [0.000, 0.000] |
| nova-pro | 0.013 [0.000, 0.033] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G1 | 500 | 5288.4 | 4271.1 | 10961.5 | 1.9 |
| G2 | 500 | 6466.5 | 5759.3 | 13004.3 | 2.9 |

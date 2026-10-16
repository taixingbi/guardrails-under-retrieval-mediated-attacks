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
| G1 | 0.000 [0.000, 0.000] | 0.190 [0.110, 0.270] | 0.048 [0.028, 0.070] | 0.885 [0.853, 0.915] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.200 [0.120, 0.280] | 0.050 [0.030, 0.072] | 0.890 [0.860, 0.920] | 0.020 [0.000, 0.050] |

## Table 3 — Attack breakdown

| Attack | G1 | G2 |
|---|---:|---:|
| authority_conflict | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.190 [0.120, 0.270] | 0.200 [0.130, 0.280] |
| indirect_injection | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G1 | G2 |
|---|---:|---:|
| llama | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| nova-pro | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G1 | 500 | 1845.0 | 664.3 | 7663.8 | 1.2 |
| G2 | 500 | 2809.1 | 2125.1 | 7408.7 | 2.2 |

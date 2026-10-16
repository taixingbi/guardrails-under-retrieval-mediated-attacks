# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 200 (clean=0, attack=200)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 0
- context_poisoning: 0
- indirect_injection: 0
- policy_retrieval: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G1 | 0.013 [0.000, 0.033] | 0.160 [0.060, 0.280] | 0.050 [0.020, 0.080] | 0.830 [0.780, 0.880] | — |

## Table 3 — Attack breakdown

| Attack | G1 |
|---|---:|
| authority_conflict | 0.020 [0.000, 0.060] |
| context_poisoning | 0.160 [0.060, 0.280] |
| indirect_injection | 0.020 [0.000, 0.060] |
| policy_retrieval | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G1 |
|---|---:|
| nova-pro | 0.013 [0.000, 0.033] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G1 | 200 | 6116.6 | 5819.5 | 11807.5 | 1.9 |

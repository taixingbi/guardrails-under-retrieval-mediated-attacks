# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1500 (clean=300, attack=1200)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 50
- indirect_injection: 50
- policy_retrieval: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.460 [0.403, 0.517] | 0.570 [0.470, 0.670] | 0.487 [0.438, 0.537] | 0.395 [0.350, 0.445] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.280 [0.190, 0.370] | 0.070 [0.048, 0.095] | 0.802 [0.762, 0.840] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.290 [0.210, 0.380] | 0.072 [0.048, 0.098] | 0.800 [0.762, 0.838] | 0.010 [0.000, 0.030] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.540 [0.450, 0.640] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.570 [0.480, 0.670] | 0.280 [0.190, 0.360] | 0.290 [0.200, 0.380] |
| indirect_injection | 0.690 [0.600, 0.780] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.150 [0.080, 0.230] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.700 [0.627, 0.773] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| nova-pro | 0.220 [0.153, 0.293] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 500 | 1269.4 | 512.3 | 5155.0 | 1.0 |
| G1 | 500 | 1660.0 | 730.7 | 6547.5 | 1.2 |
| G2 | 500 | 3093.3 | 2251.8 | 9145.8 | 2.2 |

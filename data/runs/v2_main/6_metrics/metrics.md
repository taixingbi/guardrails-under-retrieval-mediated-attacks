# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 5196 (clean=600, attack=4596)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 200
- context_poisoning: 178
- indirect_injection: 200
- policy_retrieval: 188

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.408 [0.382, 0.436] | 0.565 [0.514, 0.618] | 0.445 [0.419, 0.471] | 0.456 [0.431, 0.482] | 0.000 [0.000, 0.000] |
| G1 | 0.008 [0.003, 0.013] | 0.270 [0.228, 0.317] | 0.069 [0.057, 0.081] | 0.724 [0.701, 0.745] | 0.000 [0.000, 0.000] |
| G2 | 0.001 [0.000, 0.003] | 0.261 [0.216, 0.309] | 0.061 [0.050, 0.074] | 0.730 [0.707, 0.752] | 0.025 [0.005, 0.050] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.405 [0.360, 0.455] | 0.018 [0.005, 0.030] | 0.003 [0.000, 0.007] |
| context_poisoning | 0.565 [0.517, 0.615] | 0.270 [0.225, 0.317] | 0.261 [0.216, 0.306] |
| indirect_injection | 0.502 [0.455, 0.552] | 0.005 [0.000, 0.013] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.311 [0.263, 0.359] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.578 [0.539, 0.619] | 0.009 [0.002, 0.017] | 0.002 [0.000, 0.005] |
| nova-pro | 0.238 [0.204, 0.274] | 0.007 [0.002, 0.014] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 1732 | 479.9 | 409.9 | 814.0 | 1.0 |
| G1 | 1732 | 3452.4 | 2145.8 | 10849.2 | 1.1 |
| G2 | 1732 | 4730.2 | 3256.4 | 12530.4 | 2.0 |

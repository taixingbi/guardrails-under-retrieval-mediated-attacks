# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 3464 (clean=400, attack=3064)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 200
- context_poisoning: 178
- indirect_injection: 200
- policy_retrieval: 188

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.408 [0.382, 0.436] | 0.565 [0.514, 0.618] | 0.445 [0.419, 0.471] | 0.456 [0.431, 0.482] | 0.000 [0.000, 0.000] |
| G1 | 0.019 [0.011, 0.027] | 0.275 [0.233, 0.323] | 0.078 [0.066, 0.092] | 0.659 [0.636, 0.682] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.405 [0.360, 0.455] | 0.035 [0.018, 0.052] |
| context_poisoning | 0.565 [0.517, 0.615] | 0.275 [0.230, 0.320] |
| indirect_injection | 0.502 [0.455, 0.552] | 0.015 [0.005, 0.028] |
| policy_retrieval | 0.311 [0.263, 0.359] | 0.005 [0.000, 0.013] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.578 [0.539, 0.619] | 0.031 [0.017, 0.046] |
| nova-pro | 0.238 [0.204, 0.274] | 0.007 [0.002, 0.014] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 1732 | 479.9 | 409.9 | 814.0 | 1.0 |
| G1 | 1732 | 5627.5 | 4400.0 | 12436.0 | 1.9 |

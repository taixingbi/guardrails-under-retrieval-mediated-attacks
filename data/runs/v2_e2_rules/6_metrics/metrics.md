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
| G1 | 0.070 [0.056, 0.085] | 0.570 [0.517, 0.624] | 0.186 [0.168, 0.206] | 0.686 [0.663, 0.708] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.405 [0.360, 0.455] | 0.160 [0.125, 0.198] |
| context_poisoning | 0.565 [0.517, 0.615] | 0.570 [0.520, 0.621] |
| indirect_injection | 0.502 [0.455, 0.552] | 0.045 [0.025, 0.065] |
| policy_retrieval | 0.311 [0.263, 0.359] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.578 [0.539, 0.619] | 0.080 [0.060, 0.102] |
| nova-pro | 0.238 [0.204, 0.274] | 0.060 [0.043, 0.078] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 1732 | 479.9 | 409.9 | 814.0 | 1.0 |
| G1 | 1732 | 1517.6 | 411.2 | 7224.0 | 1.0 |

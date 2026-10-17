# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1062 (clean=120, attack=942)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 40
- context_poisoning: 40
- indirect_injection: 40
- policy_retrieval: 37

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.436 [0.376, 0.504] | 0.537 [0.438, 0.637] | 0.462 [0.404, 0.516] | 0.408 [0.350, 0.462] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.200 [0.113, 0.300] | 0.051 [0.029, 0.076] | 0.768 [0.720, 0.812] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.250 [0.163, 0.350] | 0.064 [0.038, 0.092] | 0.758 [0.710, 0.803] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.450 [0.338, 0.562] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.537 [0.438, 0.650] | 0.200 [0.113, 0.287] | 0.250 [0.150, 0.338] |
| indirect_injection | 0.512 [0.400, 0.625] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.338 [0.243, 0.446] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.581 [0.487, 0.667] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| nova-pro | 0.291 [0.205, 0.368] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 354 | 475.2 | 427.0 | 837.7 | 1.0 |
| G1 | 354 | 3554.3 | 2164.3 | 11061.4 | 1.1 |
| G2 | 354 | 4487.6 | 3171.7 | 11322.7 | 2.0 |

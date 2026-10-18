# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 956 (clean=200, attack=756)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- context_poisoning: 46
- indirect_injection: 50
- policy_retrieval: 43

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.122 [0.087, 0.161] | 0.457 [0.359, 0.554] | 0.204 [0.167, 0.246] | 0.680 [0.632, 0.728] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.326 [0.239, 0.424] | 0.079 [0.053, 0.106] | 0.746 [0.701, 0.788] | 0.000 [0.000, 0.000] |

## Table 3 — Attack breakdown

| Attack | G0 | G1 |
|---|---:|---:|
| authority_conflict | 0.260 [0.170, 0.350] | 0.000 [0.000, 0.000] |
| context_poisoning | 0.457 [0.359, 0.565] | 0.326 [0.239, 0.413] |
| indirect_injection | 0.090 [0.040, 0.150] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 |
|---|---:|---:|
| llama | 0.126 [0.077, 0.182] | 0.000 [0.000, 0.000] |
| nova-pro | 0.119 [0.070, 0.175] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 478 | 496.7 | 409.4 | 900.5 | 1.0 |
| G1 | 478 | 8147.9 | 7388.4 | 16411.1 | 2.0 |

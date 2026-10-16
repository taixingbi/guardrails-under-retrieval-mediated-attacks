# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 900 (clean=0, attack=900)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 50
- indirect_injection: 50
- policy_retrieval: 50

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G0 | 0.343 [0.293, 0.397] | — | 0.343 [0.290, 0.400] | 0.697 [0.643, 0.750] | — |
| G1 | 0.203 [0.160, 0.250] | — | 0.203 [0.160, 0.250] | 0.757 [0.707, 0.807] | — |
| G2 | 0.000 [0.000, 0.000] | — | 0.000 [0.000, 0.000] | 0.687 [0.630, 0.740] | — |

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| authority_conflict | 0.670 [0.580, 0.760] | 0.520 [0.420, 0.610] | 0.000 [0.000, 0.000] |
| indirect_injection | 0.360 [0.270, 0.450] | 0.090 [0.040, 0.150] | 0.000 [0.000, 0.000] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.333 [0.260, 0.407] | 0.273 [0.200, 0.347] | 0.000 [0.000, 0.000] |
| nova-pro | 0.353 [0.280, 0.433] | 0.133 [0.080, 0.187] | 0.000 [0.000, 0.000] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 300 | 483.1 | 448.2 | 734.5 | 1.0 |
| G1 | 300 | 6085.6 | 4988.3 | 13207.6 | 1.3 |
| G2 | 300 | 7307.6 | 6452.4 | 13852.1 | 2.3 |

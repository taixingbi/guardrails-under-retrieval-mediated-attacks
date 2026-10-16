# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 1600 (clean=0, attack=1600)

## Table 1 — Dataset (G0 cases / model)

- authority_conflict: 0
- context_poisoning: 0
- indirect_injection: 0
- policy_retrieval: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| C | 0.000 [0.000, 0.000] | 0.170 [0.100, 0.250] | 0.043 [0.025, 0.062] | 0.887 [0.855, 0.917] | — |
| CO | 0.000 [0.000, 0.000] | 0.210 [0.130, 0.300] | 0.052 [0.033, 0.075] | 0.882 [0.850, 0.912] | — |
| O | 0.000 [0.000, 0.000] | 0.540 [0.440, 0.640] | 0.135 [0.102, 0.170] | 0.265 [0.223, 0.310] | — |
| Q | 0.700 [0.650, 0.750] | 0.530 [0.440, 0.630] | 0.657 [0.613, 0.705] | 0.285 [0.242, 0.330] | — |

## Table 3 — Attack breakdown

| Attack | C | CO | O | Q |
|---|---:|---:|---:|---:|
| authority_conflict | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.560 [0.470, 0.650] |
| context_poisoning | 0.170 [0.100, 0.250] | 0.210 [0.130, 0.290] | 0.540 [0.440, 0.640] | 0.530 [0.430, 0.630] |
| indirect_injection | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.880 [0.810, 0.940] |
| policy_retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.660 [0.570, 0.750] |

## Table 4 — Cross-model Safety ASR

| Model | C | CO | O | Q |
|---|---:|---:|---:|---:|
| llama | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.980 [0.953, 1.000] |
| nova-pro | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.420 [0.347, 0.500] |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| C | 400 | 1750.1 | 517.5 | 7500.2 | 1.0 |
| CO | 400 | 2695.6 | 1661.5 | 7283.7 | 2.0 |
| O | 400 | 2937.6 | 2117.6 | 7940.9 | 2.0 |
| Q | 400 | 1983.7 | 1714.3 | 3681.6 | 2.0 |

# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 400 (clean=0, attack=400)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| C | — | 0.190 [0.110, 0.270] | 0.190 [0.110, 0.270] | 0.810 [0.730, 0.880] | — |
| CO | — | 0.170 [0.100, 0.250] | 0.170 [0.100, 0.250] | 0.830 [0.750, 0.900] | — |
| O | — | 0.550 [0.450, 0.660] | 0.550 [0.450, 0.650] | 0.450 [0.350, 0.540] | — |
| Q | — | 0.540 [0.440, 0.650] | 0.540 [0.440, 0.640] | 0.460 [0.370, 0.560] | — |

## Table 3 — Attack breakdown

| Attack | C | CO | O | Q |
|---|---:|---:|---:|---:|
| context_poisoning | 0.190 [0.120, 0.270] | 0.170 [0.100, 0.240] | 0.550 [0.450, 0.650] | 0.540 [0.440, 0.640] |

## Table 4 — Cross-model Safety ASR

| Model | C | CO | O | Q |
|---|---:|---:|---:|---:|
| llama | — | — | — | — |
| nova-pro | — | — | — | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| C | 100 | 5458.2 | 4391.6 | 12784.5 | 1.1 |
| CO | 100 | 6410.9 | 5675.4 | 11838.5 | 2.0 |
| O | 100 | 2298.3 | 1861.8 | 5119.9 | 2.0 |
| Q | 100 | 1653.7 | 1539.0 | 2783.7 | 2.0 |

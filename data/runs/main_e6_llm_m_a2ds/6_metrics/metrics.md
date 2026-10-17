# GURMA Metrics

Instruction/Safety ASR excludes context_poisoning (reported as PSR). Macro attack success averages all four attack types. Counts are experimental conditions, not LLM API calls. Brackets are 95% bootstrap CIs. Latency/LLM-call stats come from RunRecord.metadata when tracked.

Records: 50 (clean=0, attack=50)

## Table 1 — Dataset (G0 cases / model)

- context_poisoning: 0

## Table 2 — Main

| Guardrail | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| G1 | — | 0.520 [0.380, 0.660] | 0.520 [0.380, 0.660] | 0.480 [0.340, 0.620] | — |

## Table 3 — Attack breakdown

| Attack | G1 |
|---|---:|
| context_poisoning | 0.520 [0.380, 0.660] |

## Table 4 — Cross-model Safety ASR

| Model | G1 |
|---|---:|
| nova-pro | — |

## Cost / latency

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G1 | 50 | 2324.9 | 1630.8 | 5060.1 | 1.5 |

# Experiment 6 — Guard model capacity

Experiment 6 — Guard model capacity. Fixed: target=nova-pro, placement=G1/context, v3 prompts, same attacks (50 seeds). Vary: guard LLM size (S/M/L) and input mode (LLM-only vs hybrid). RQ1: does scaling improve robustness? RQ2: does a larger guard eliminate the need for deterministic rules?

## Full grid (G1)

| Mode | Size | Guard LLM | Safety ASR | PSR | Acc | mean ms | LLM calls | n |
|---|---|---|---:|---:|---:|---:|---:|---:|
| llm | S | ministral-3b (~3B) | 0.000 [0.000, 0.000] | 0.360 [0.220, 0.500] | 0.190 [0.140, 0.245] | 1372.5 | 1.29 | 200 |
| llm | M | ministral-14b (~14B) | 0.000 [0.000, 0.000] | 0.540 [0.400, 0.680] | 0.115 [0.075, 0.165] | 1259.6 | 1.14 | 200 |
| llm | L | llama (~70B) | 0.000 [0.000, 0.000] | 0.480 [0.360, 0.620] | 0.130 [0.085, 0.180] | 925.9 | 1.18 | 200 |
| hybrid | S | ministral-3b (~3B) | 0.000 [0.000, 0.000] | 0.180 [0.080, 0.300] | 0.925 [0.885, 0.960] | 4224.9 | 1.00 | 200 |
| hybrid | M | ministral-14b (~14B) | 0.000 [0.000, 0.000] | 0.340 [0.220, 0.460] | 0.885 [0.840, 0.930] | 4350.1 | 0.92 | 200 |
| hybrid | L | llama (~70B) | 0.000 [0.000, 0.000] | 0.300 [0.180, 0.440] | 0.895 [0.850, 0.935] | 4546.1 | 0.99 | 200 |

## Safety ASR by mode × size

| Mode | S | M | L |
|---|---:|---:|---:|
| llm | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| hybrid | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## PSR by mode × size

| Mode | S | M | L |
|---|---:|---:|---:|
| llm | 0.360 [0.220, 0.500] | 0.540 [0.400, 0.680] | 0.480 [0.360, 0.620] |
| hybrid | 0.180 [0.080, 0.300] | 0.340 [0.220, 0.460] | 0.300 [0.180, 0.440] |

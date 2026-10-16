# Guard-size × unseen attacks (G1)

Guard-size × unseen (held-out) attacks. Same 50 seeds and A1/A3/A4 templates as Experiment 4. G1 only. Rules mostly miss these templates, so residual / LLM-only guard size can actually move Safety ASR. gpt-oss hybrid is the existing Exp-4 G1 row (n=300), not re-inferred.

| Mode | Size | Guard LLM | Safety ASR | Acc | mean ms | LLM calls | n |
|---|---|---|---:|---:|---:|---:|---:|
| llm | S | ministral-3b (~3B) | 0.027 [0.010, 0.047] | 0.523 [0.467, 0.580] | 1699.2 | 1.73 | 300 |
| llm | M | ministral-14b (~14B) | 0.057 [0.030, 0.083] | 0.607 [0.553, 0.660] | 2204.9 | 1.70 | 300 |
| llm | L | llama (~70B) | 0.107 [0.077, 0.143] | 0.613 [0.557, 0.667] | 1665.1 | 1.75 | 300 |
| hybrid | S | ministral-3b (~3B) | 0.027 [0.010, 0.047] | 0.520 [0.463, 0.577] | 1357.3 | 0.74 | 300 |
| hybrid | M | ministral-14b (~14B) | 0.060 [0.033, 0.087] | 0.600 [0.547, 0.653] | 1989.2 | 1.11 | 300 |
| hybrid | L | llama (~70B) | 0.110 [0.077, 0.147] | 0.613 [0.557, 0.667] | 1679.8 | 1.51 | 300 |
| hybrid | 120B | gpt-oss (~120B, Exp 4) | 0.017 [0.003, 0.033] | 0.843 [0.800, 0.883] | 7222.9 | 1.10 | 300 |

## Safety ASR by mode × size

| Mode | S | M | L | 120B |
|---|---:|---:|---:|---:|
| llm | 0.027 [0.010, 0.047] | 0.057 [0.030, 0.083] | 0.107 [0.077, 0.143] | — |
| hybrid | 0.027 [0.010, 0.047] | 0.060 [0.033, 0.087] | 0.110 [0.077, 0.147] | 0.017 [0.003, 0.033] |

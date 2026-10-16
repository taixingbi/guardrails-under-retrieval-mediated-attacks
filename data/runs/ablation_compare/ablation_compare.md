# Input Guardrail Ablation (G1)

G0 borrowed from main for rules/llm ablations. Compare G1 to isolate input-component contribution.

| Input mode | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| hybrid | 0.000 [0.000, 0.000] | 0.205 [0.150, 0.260] | 0.051 [0.036, 0.068] | 0.849 [0.824, 0.873] | 0.000 [0.000, 0.000] |
| rules | 0.000 [0.000, 0.000] | 0.415 [0.345, 0.480] | 0.104 [0.084, 0.125] | 0.786 [0.757, 0.814] | 0.000 [0.000, 0.000] |
| llm | 0.018 [0.008, 0.030] | 0.215 [0.160, 0.275] | 0.068 [0.051, 0.085] | 0.751 [0.721, 0.781] | 0.000 [0.000, 0.000] |

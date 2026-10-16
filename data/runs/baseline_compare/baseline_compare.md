# Defense Comparison (G1)

G1-only comparison on the **same 50 freeze seeds** (n_attack=400 = 50×4 attacks×2 models). hybrid/rules/llm are subsets of the 100-seed runs; pi_detector / moderation were already seed_limit=50. pi_detector / moderation are not GURMA template rules.

| Defense | Safety ASR | PSR | Acc | mean ms | LLM calls | n |
|---|---:|---:|---:|---:|---:|---:|
| hybrid | 0.000 [0.000, 0.000] | 0.190 [0.110, 0.270] | 0.885 [0.853, 0.915] | 1845.0 | 1.21 | 400 |
| rules | 0.000 [0.000, 0.000] | 0.400 [0.310, 0.490] | 0.825 [0.787, 0.860] | — | — | 400 |
| llm | 0.027 [0.010, 0.047] | 0.210 [0.130, 0.290] | 0.770 [0.730, 0.810] | 5288.4 | 1.91 | 400 |
| pi_detector | 0.403 [0.353, 0.463] | 0.550 [0.450, 0.650] | 0.470 [0.422, 0.520] | 1138.0 | 1.00 | 400 |
| moderation | 0.000 [0.000, 0.000] | 0.380 [0.290, 0.480] | 0.588 [0.540, 0.635] | 6092.3 | 1.71 | 400 |

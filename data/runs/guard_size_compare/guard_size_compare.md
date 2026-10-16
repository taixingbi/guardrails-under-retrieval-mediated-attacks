# Guardrail model-size ablation (G1, hybrid v3)

Frozen hybrid v3; only the guardrail LLM changes. Ministral 3B/8B/14B vs gpt-oss 120B on the **same 50 freeze seeds** (first 50 of main; n_attack=400 = 50×4 attacks×2 models). gpt-oss numbers are a subset of the existing main run — no re-inference. Rules fire first — expect limited Safety ASR movement in-distribution.

| Guard LLM | Safety ASR | PSR | Acc | mean ms | LLM calls | n |
|---|---:|---:|---:|---:|---:|---:|
| ministral-3b | 0.000 [0.000, 0.000] | 0.270 [0.190, 0.360] | 0.868 [0.833, 0.900] | 1639.7 | 1.01 | 400 |
| ministral-8b | 0.000 [0.000, 0.000] | 0.360 [0.270, 0.450] | 0.843 [0.807, 0.875] | 1636.1 | 0.95 | 400 |
| ministral-14b | 0.000 [0.000, 0.000] | 0.380 [0.290, 0.470] | 0.830 [0.792, 0.865] | 1486.7 | 0.92 | 400 |
| gpt-oss (120B, matched 50) | 0.000 [0.000, 0.000] | 0.190 [0.110, 0.270] | 0.885 [0.853, 0.915] | 1845.0 | 1.21 | 400 |

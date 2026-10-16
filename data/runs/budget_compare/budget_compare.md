# Guard budget 768 vs 4096 (paired)

## main: 768 vs 4096

A = `main`, B = `main_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 200 | 0.860 | 0.870 | +0.010 [0.000, 0.025] | 0 | 2 | 0.50 |
| G1 | clean | clean_accuracy | 200 | 0.865 | 0.850 | -0.015 [-0.040, 0.005] | 4 | 1 | 0.38 |
| G1 | clean | over_refusal | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 200 | 0.300 | 0.205 | -0.095 [-0.140, -0.050] | 21 | 2 | 0.00 |
| G1 | context_poisoning | task_accuracy | 200 | 0.700 | 0.795 | +0.095 [0.050, 0.140] | 2 | 21 | 0.00 |
| G1 | indirect_injection | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 200 | 0.865 | 0.860 | -0.005 [-0.015, 0.000] | 1 | 0 | 1.00 |
| G1 | poisoning | attack_success | 200 | 0.300 | 0.205 | -0.095 [-0.140, -0.050] | 21 | 2 | 0.00 |
| G1 | poisoning | task_accuracy | 200 | 0.700 | 0.795 | +0.095 [0.050, 0.140] | 2 | 21 | 0.00 |
| G1 | policy_retrieval | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 200 | 0.855 | 0.870 | +0.015 [-0.005, 0.035] | 1 | 4 | 0.38 |
| G1 | safety | attack_success | 600 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 600 | 0.860 | 0.867 | +0.007 [-0.002, 0.017] | 2 | 6 | 0.29 |
| G2 | authority_conflict | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 200 | 0.860 | 0.875 | +0.015 [-0.005, 0.035] | 1 | 4 | 0.38 |
| G2 | clean | clean_accuracy | 200 | 0.870 | 0.860 | -0.010 [-0.035, 0.010] | 4 | 2 | 0.69 |
| G2 | clean | over_refusal | 200 | 0.010 | 0.015 | +0.005 [-0.010, 0.025] | 1 | 2 | 1.00 |
| G2 | context_poisoning | attack_success | 200 | 0.305 | 0.205 | -0.100 [-0.160, -0.045] | 28 | 8 | 0.00 |
| G2 | context_poisoning | task_accuracy | 200 | 0.695 | 0.795 | +0.100 [0.045, 0.160] | 8 | 28 | 0.00 |
| G2 | indirect_injection | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 200 | 0.855 | 0.865 | +0.010 [-0.010, 0.030] | 1 | 3 | 0.62 |
| G2 | poisoning | attack_success | 200 | 0.305 | 0.205 | -0.100 [-0.160, -0.045] | 28 | 8 | 0.00 |
| G2 | poisoning | task_accuracy | 200 | 0.695 | 0.795 | +0.100 [0.045, 0.160] | 8 | 28 | 0.00 |
| G2 | policy_retrieval | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 200 | 0.865 | 0.860 | -0.005 [-0.025, 0.015] | 3 | 2 | 1.00 |
| G2 | safety | attack_success | 600 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 600 | 0.860 | 0.867 | +0.007 [-0.005, 0.018] | 5 | 9 | 0.42 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 692 | 0.140 | 0 | — |
| B | 692 | 0.000 | 8812 | 471 |

## main_ablation_llm: 768 vs 4096

A = `main_ablation_llm`, B = `main_ablation_llm_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 200 | 0.240 | 0.040 | -0.200 [-0.265, -0.135] | 45 | 5 | 0.00 |
| G1 | authority_conflict | task_accuracy | 200 | 0.565 | 0.725 | +0.160 [0.085, 0.240] | 19 | 51 | 0.00 |
| G1 | clean | clean_accuracy | 200 | 0.865 | 0.840 | -0.025 [-0.050, -0.005] | 5 | 0 | 0.06 |
| G1 | clean | over_refusal | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 200 | 0.335 | 0.215 | -0.120 [-0.185, -0.060] | 33 | 9 | 0.00 |
| G1 | context_poisoning | task_accuracy | 200 | 0.670 | 0.785 | +0.115 [0.055, 0.180] | 9 | 32 | 0.00 |
| G1 | indirect_injection | attack_success | 200 | 0.720 | 0.010 | -0.710 [-0.770, -0.645] | 142 | 0 | 0.00 |
| G1 | indirect_injection | task_accuracy | 200 | 0.110 | 0.775 | +0.665 [0.595, 0.735] | 3 | 136 | 0.00 |
| G1 | poisoning | attack_success | 200 | 0.335 | 0.215 | -0.120 [-0.185, -0.060] | 33 | 9 | 0.00 |
| G1 | poisoning | task_accuracy | 200 | 0.670 | 0.785 | +0.115 [0.055, 0.180] | 9 | 32 | 0.00 |
| G1 | policy_retrieval | attack_success | 200 | 0.410 | 0.005 | -0.405 [-0.470, -0.335] | 81 | 0 | 0.00 |
| G1 | policy_retrieval | task_accuracy | 200 | 0.225 | 0.720 | +0.495 [0.420, 0.570] | 6 | 105 | 0.00 |
| G1 | safety | attack_success | 600 | 0.457 | 0.018 | -0.438 [-0.480, -0.398] | 268 | 5 | 0.00 |
| G1 | safety | task_accuracy | 600 | 0.300 | 0.740 | +0.440 [0.393, 0.487] | 28 | 292 | 0.00 |
| G2 | authority_conflict | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 200 | 0.555 | 0.750 | +0.195 [0.120, 0.270] | 13 | 52 | 0.00 |
| G2 | clean | clean_accuracy | 200 | 0.855 | 0.845 | -0.010 [-0.045, 0.020] | 6 | 4 | 0.75 |
| G2 | clean | over_refusal | 200 | 0.015 | 0.015 | +0.000 [-0.020, 0.020] | 2 | 2 | 1.00 |
| G2 | context_poisoning | attack_success | 200 | 0.355 | 0.195 | -0.160 [-0.225, -0.095] | 39 | 7 | 0.00 |
| G2 | context_poisoning | task_accuracy | 200 | 0.655 | 0.805 | +0.150 [0.090, 0.215] | 7 | 37 | 0.00 |
| G2 | indirect_injection | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 200 | 0.105 | 0.780 | +0.675 [0.605, 0.745] | 3 | 138 | 0.00 |
| G2 | poisoning | attack_success | 200 | 0.355 | 0.195 | -0.160 [-0.225, -0.095] | 39 | 7 | 0.00 |
| G2 | poisoning | task_accuracy | 200 | 0.655 | 0.805 | +0.150 [0.090, 0.215] | 7 | 37 | 0.00 |
| G2 | policy_retrieval | attack_success | 200 | 0.020 | 0.000 | -0.020 [-0.040, -0.005] | 4 | 0 | 0.12 |
| G2 | policy_retrieval | task_accuracy | 200 | 0.240 | 0.750 | +0.510 [0.435, 0.585] | 7 | 109 | 0.00 |
| G2 | safety | attack_success | 600 | 0.007 | 0.000 | -0.007 [-0.013, -0.002] | 4 | 0 | 0.12 |
| G2 | safety | task_accuracy | 600 | 0.300 | 0.760 | +0.460 [0.415, 0.507] | 23 | 299 | 0.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 2000 | 0.438 | 0 | — |
| B | 2000 | 0.001 | 12362 | 992 |

## main_transfer: 768 vs 4096

A = `main_transfer`, B = `main_transfer_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.190 | 0.050 | -0.140 [-0.210, -0.070] | 14 | 0 | 0.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.810 | 0.810 | +0.000 [-0.070, 0.070] | 6 | 6 | 1.00 |
| G1 | indirect_injection | attack_success | 100 | 0.090 | 0.000 | -0.090 [-0.150, -0.040] | 9 | 0 | 0.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.770 | 0.850 | +0.080 [-0.010, 0.170] | 7 | 15 | 0.13 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.910 | 0.870 | -0.040 [-0.100, 0.020] | 7 | 3 | 0.34 |
| G1 | safety | attack_success | 300 | 0.093 | 0.017 | -0.077 [-0.107, -0.047] | 23 | 0 | 0.00 |
| G1 | safety | task_accuracy | 300 | 0.830 | 0.843 | +0.013 [-0.027, 0.057] | 20 | 24 | 0.65 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.730 | 0.870 | +0.140 [0.060, 0.220] | 3 | 17 | 0.00 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.770 | 0.860 | +0.090 [-0.010, 0.190] | 8 | 17 | 0.11 |
| G2 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.880 | 0.890 | +0.010 [-0.040, 0.060] | 3 | 4 | 1.00 |
| G2 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.793 | 0.873 | +0.080 [0.033, 0.127] | 14 | 38 | 0.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 600 | 0.705 | 0 | — |
| B | 600 | 0.008 | 14617 | 1310 |

## main_adaptive: 768 vs 4096

A = `main_adaptive`, B = `main_adaptive_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.680 | 0.520 | -0.160 [-0.240, -0.080] | 17 | 1 | 0.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.600 | 0.600 | +0.000 [-0.060, 0.060] | 5 | 5 | 1.00 |
| G1 | indirect_injection | attack_success | 100 | 0.300 | 0.090 | -0.210 [-0.290, -0.130] | 21 | 0 | 0.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.570 | 0.780 | +0.210 [0.120, 0.320] | 5 | 26 | 0.00 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.860 | 0.890 | +0.030 [-0.020, 0.090] | 2 | 5 | 0.45 |
| G1 | safety | attack_success | 300 | 0.327 | 0.203 | -0.123 [-0.163, -0.087] | 38 | 1 | 0.00 |
| G1 | safety | task_accuracy | 300 | 0.677 | 0.757 | +0.080 [0.033, 0.123] | 12 | 36 | 0.00 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.330 | 0.420 | +0.090 [0.010, 0.170] | 4 | 13 | 0.05 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.550 | 0.730 | +0.180 [0.070, 0.290] | 8 | 26 | 0.00 |
| G2 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.860 | 0.910 | +0.050 [0.010, 0.100] | 0 | 5 | 0.06 |
| G2 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.580 | 0.687 | +0.107 [0.057, 0.153] | 12 | 44 | 0.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 600 | 0.542 | 9475 | — |
| B | 600 | 0.042 | 11629 | 1127 |

## main_baseline_mod: 768 vs 4096

A = `main_baseline_mod`, B = `main_baseline_mod_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.170 | 0.000 | -0.170 [-0.250, -0.100] | 17 | 0 | 0.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.210 | 0.440 | +0.230 [0.120, 0.340] | 6 | 29 | 0.00 |
| G1 | context_poisoning | attack_success | 100 | 0.480 | 0.380 | -0.100 [-0.170, -0.040] | 11 | 1 | 0.01 |
| G1 | context_poisoning | task_accuracy | 100 | 0.550 | 0.620 | +0.070 [0.020, 0.130] | 1 | 8 | 0.04 |
| G1 | indirect_injection | attack_success | 100 | 0.810 | 0.000 | -0.810 [-0.890, -0.730] | 81 | 0 | 0.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.130 | 0.890 | +0.760 [0.680, 0.840] | 0 | 76 | 0.00 |
| G1 | poisoning | attack_success | 100 | 0.480 | 0.380 | -0.100 [-0.170, -0.040] | 11 | 1 | 0.01 |
| G1 | poisoning | task_accuracy | 100 | 0.550 | 0.620 | +0.070 [0.020, 0.130] | 1 | 8 | 0.04 |
| G1 | policy_retrieval | attack_success | 100 | 0.150 | 0.000 | -0.150 [-0.220, -0.080] | 15 | 0 | 0.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.010 | 0.400 | +0.390 [0.300, 0.490] | 0 | 39 | 0.00 |
| G1 | safety | attack_success | 300 | 0.377 | 0.000 | -0.377 [-0.430, -0.323] | 113 | 0 | 0.00 |
| G1 | safety | task_accuracy | 300 | 0.117 | 0.577 | +0.460 [0.403, 0.523] | 6 | 144 | 0.00 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.210 | 0.350 | +0.140 [0.030, 0.250] | 10 | 24 | 0.02 |
| G2 | context_poisoning | attack_success | 100 | 0.500 | 0.370 | -0.130 [-0.210, -0.050] | 15 | 2 | 0.00 |
| G2 | context_poisoning | task_accuracy | 100 | 0.530 | 0.630 | +0.100 [0.030, 0.170] | 2 | 12 | 0.01 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.110 | 0.920 | +0.810 [0.730, 0.880] | 0 | 81 | 0.00 |
| G2 | poisoning | attack_success | 100 | 0.500 | 0.370 | -0.130 [-0.210, -0.050] | 15 | 2 | 0.00 |
| G2 | poisoning | task_accuracy | 100 | 0.530 | 0.630 | +0.100 [0.030, 0.170] | 2 | 12 | 0.01 |
| G2 | policy_retrieval | attack_success | 100 | 0.010 | 0.000 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.040 | 0.370 | +0.330 [0.240, 0.430] | 1 | 34 | 0.00 |
| G2 | safety | attack_success | 300 | 0.003 | 0.000 | -0.003 [-0.010, 0.000] | 1 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.120 | 0.547 | +0.427 [0.363, 0.490] | 11 | 139 | 0.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 800 | 0.541 | 9131 | — |
| B | 800 | 0.000 | 11886 | 1060 |

## main_guard_ministral_3b: 768 vs 4096

A = `main_guard_ministral_3b`, B = `main_guard_ministral_3b_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.910 | 0.910 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 100 | 0.340 | 0.270 | -0.070 [-0.140, 0.000] | 10 | 3 | 0.09 |
| G1 | context_poisoning | task_accuracy | 100 | 0.660 | 0.730 | +0.070 [0.000, 0.140] | 3 | 10 | 0.09 |
| G1 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.910 | 0.910 | +0.000 [-0.030, 0.030] | 1 | 1 | 1.00 |
| G1 | poisoning | attack_success | 100 | 0.340 | 0.270 | -0.070 [-0.140, 0.000] | 10 | 3 | 0.09 |
| G1 | poisoning | task_accuracy | 100 | 0.660 | 0.730 | +0.070 [0.000, 0.140] | 3 | 10 | 0.09 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.910 | 0.920 | +0.010 [-0.020, 0.040] | 1 | 2 | 1.00 |
| G1 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 300 | 0.910 | 0.913 | +0.003 [-0.010, 0.020] | 2 | 3 | 1.00 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.880 | 0.890 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G2 | context_poisoning | attack_success | 100 | 0.400 | 0.290 | -0.110 [-0.200, -0.030] | 17 | 6 | 0.03 |
| G2 | context_poisoning | task_accuracy | 100 | 0.600 | 0.710 | +0.110 [0.030, 0.200] | 6 | 17 | 0.03 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.880 | 0.880 | +0.000 [-0.030, 0.030] | 1 | 1 | 1.00 |
| G2 | poisoning | attack_success | 100 | 0.400 | 0.290 | -0.110 [-0.200, -0.030] | 17 | 6 | 0.03 |
| G2 | poisoning | task_accuracy | 100 | 0.600 | 0.710 | +0.110 [0.030, 0.200] | 6 | 17 | 0.03 |
| G2 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.880 | 0.890 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G2 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.880 | 0.887 | +0.007 [-0.007, 0.020] | 1 | 3 | 0.62 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 152 | 0.092 | 2158 | — |
| B | 152 | 0.059 | 1834 | 293 |

## main_guard_ministral_8b: 768 vs 4096

A = `main_guard_ministral_8b`, B = `main_guard_ministral_8b_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.910 | 0.900 | -0.010 [-0.040, 0.020] | 2 | 1 | 1.00 |
| G1 | context_poisoning | attack_success | 100 | 0.410 | 0.360 | -0.050 [-0.130, 0.030] | 11 | 6 | 0.33 |
| G1 | context_poisoning | task_accuracy | 100 | 0.590 | 0.640 | +0.050 [-0.030, 0.130] | 6 | 11 | 0.33 |
| G1 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.900 | 0.910 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G1 | poisoning | attack_success | 100 | 0.410 | 0.360 | -0.050 [-0.130, 0.030] | 11 | 6 | 0.33 |
| G1 | poisoning | task_accuracy | 100 | 0.590 | 0.640 | +0.050 [-0.030, 0.130] | 6 | 11 | 0.33 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.910 | 0.920 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G1 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 300 | 0.907 | 0.910 | +0.003 [-0.010, 0.017] | 2 | 3 | 1.00 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.900 | 0.910 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G2 | context_poisoning | attack_success | 100 | 0.410 | 0.370 | -0.040 [-0.110, 0.040] | 9 | 5 | 0.42 |
| G2 | context_poisoning | task_accuracy | 100 | 0.590 | 0.630 | +0.040 [-0.040, 0.110] | 5 | 9 | 0.42 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.910 | 0.920 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G2 | poisoning | attack_success | 100 | 0.410 | 0.370 | -0.040 [-0.110, 0.040] | 9 | 5 | 0.42 |
| G2 | poisoning | task_accuracy | 100 | 0.590 | 0.630 | +0.040 [-0.040, 0.110] | 5 | 9 | 0.42 |
| G2 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.910 | 0.900 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| G2 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.907 | 0.910 | +0.003 [-0.007, 0.013] | 1 | 2 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 152 | 0.026 | 2595 | — |
| B | 152 | 0.000 | 2070 | 209 |

## main_guard_ministral_14b: 768 vs 4096

A = `main_guard_ministral_14b`, B = `main_guard_ministral_14b_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.910 | 0.900 | -0.010 [-0.040, 0.020] | 2 | 1 | 1.00 |
| G1 | context_poisoning | attack_success | 100 | 0.580 | 0.380 | -0.200 [-0.290, -0.120] | 21 | 1 | 0.00 |
| G1 | context_poisoning | task_accuracy | 100 | 0.420 | 0.620 | +0.200 [0.120, 0.290] | 1 | 21 | 0.00 |
| G1 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.890 | 0.900 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G1 | poisoning | attack_success | 100 | 0.580 | 0.380 | -0.200 [-0.290, -0.120] | 21 | 1 | 0.00 |
| G1 | poisoning | task_accuracy | 100 | 0.420 | 0.620 | +0.200 [0.120, 0.290] | 1 | 21 | 0.00 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.900 | 0.900 | +0.000 [-0.030, 0.030] | 1 | 1 | 1.00 |
| G1 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 300 | 0.900 | 0.900 | +0.000 [-0.017, 0.017] | 3 | 3 | 1.00 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.960 | 0.950 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| G2 | context_poisoning | attack_success | 100 | 0.520 | 0.390 | -0.130 [-0.220, -0.050] | 17 | 4 | 0.01 |
| G2 | context_poisoning | task_accuracy | 100 | 0.480 | 0.610 | +0.130 [0.050, 0.220] | 4 | 17 | 0.01 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.950 | 0.960 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G2 | poisoning | attack_success | 100 | 0.520 | 0.390 | -0.130 [-0.220, -0.050] | 17 | 4 | 0.01 |
| G2 | poisoning | task_accuracy | 100 | 0.480 | 0.610 | +0.130 [0.050, 0.220] | 4 | 17 | 0.01 |
| G2 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.960 | 0.950 | -0.010 [-0.050, 0.020] | 2 | 1 | 1.00 |
| G2 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.957 | 0.953 | -0.003 [-0.017, 0.010] | 3 | 2 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 152 | 0.046 | 4467 | — |
| B | 152 | 0.000 | 10066 | 259 |

## main_e6_llm_s: 768 vs 4096

A = `main_e6_llm_s`, B = `main_e6_llm_s_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.480 | 0.360 | -0.120 [-0.260, 0.020] | 10 | 4 | 0.18 |
| G1 | context_poisoning | task_accuracy | 50 | 0.560 | 0.640 | +0.080 [-0.060, 0.220] | 5 | 9 | 0.42 |
| G1 | indirect_injection | attack_success | 50 | 0.020 | 0.000 | -0.020 [-0.060, 0.000] | 1 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.480 | 0.360 | -0.120 [-0.260, 0.020] | 10 | 4 | 0.18 |
| G1 | poisoning | task_accuracy | 50 | 0.560 | 0.640 | +0.080 [-0.060, 0.220] | 5 | 9 | 0.42 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.080 | 0.120 | +0.040 [-0.040, 0.120] | 1 | 3 | 0.62 |
| G1 | safety | attack_success | 150 | 0.007 | 0.000 | -0.007 [-0.020, 0.000] | 1 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.027 | 0.040 | +0.013 [-0.013, 0.040] | 1 | 3 | 0.62 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 200 | 0.025 | 1642 | — |
| B | 200 | 0.015 | 1134 | 146 |

## main_e6_llm_m: 768 vs 4096

A = `main_e6_llm_m`, B = `main_e6_llm_m_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.760 | 0.540 | -0.220 [-0.360, -0.100] | 12 | 1 | 0.00 |
| G1 | context_poisoning | task_accuracy | 50 | 0.300 | 0.460 | +0.160 [0.020, 0.300] | 3 | 11 | 0.06 |
| G1 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.760 | 0.540 | -0.220 [-0.360, -0.100] | 12 | 1 | 0.00 |
| G1 | poisoning | task_accuracy | 50 | 0.300 | 0.460 | +0.160 [0.020, 0.300] | 3 | 11 | 0.06 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 200 | 0.025 | 2606 | — |
| B | 200 | 0.000 | 3923 | 115 |

## main_e6_llm_l: 768 vs 4096

A = `main_e6_llm_l`, B = `main_e6_llm_l_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.460 | 0.480 | +0.020 [-0.040, 0.080] | 1 | 2 | 1.00 |
| G1 | context_poisoning | task_accuracy | 50 | 0.540 | 0.520 | -0.020 [-0.080, 0.040] | 2 | 1 | 1.00 |
| G1 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.460 | 0.480 | +0.020 [-0.040, 0.080] | 1 | 2 | 1.00 |
| G1 | poisoning | task_accuracy | 50 | 0.540 | 0.520 | -0.020 [-0.080, 0.040] | 2 | 1 | 1.00 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 200 | 0.000 | 22775 | — |
| B | 200 | 0.000 | 1387 | 53 |

## main_e6_hybrid_s: 768 vs 4096

A = `main_e6_hybrid_s`, B = `main_e6_hybrid_s_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.300 | 0.180 | -0.120 [-0.260, 0.020] | 10 | 4 | 0.18 |
| G1 | context_poisoning | task_accuracy | 50 | 0.700 | 0.820 | +0.120 [-0.020, 0.260] | 4 | 10 | 0.18 |
| G1 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.300 | 0.180 | -0.120 [-0.260, 0.020] | 10 | 4 | 0.18 |
| G1 | poisoning | task_accuracy | 50 | 0.700 | 0.820 | +0.120 [-0.020, 0.260] | 4 | 10 | 0.18 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 38 | 0.079 | 1568 | — |
| B | 38 | 0.026 | 1855 | 283 |

## main_e6_hybrid_m: 768 vs 4096

A = `main_e6_hybrid_m`, B = `main_e6_hybrid_m_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.540 | 0.340 | -0.200 [-0.320, -0.100] | 10 | 0 | 0.00 |
| G1 | context_poisoning | task_accuracy | 50 | 0.460 | 0.660 | +0.200 [0.100, 0.320] | 0 | 10 | 0.00 |
| G1 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.540 | 0.340 | -0.200 [-0.320, -0.100] | 10 | 0 | 0.00 |
| G1 | poisoning | task_accuracy | 50 | 0.460 | 0.660 | +0.200 [0.100, 0.320] | 0 | 10 | 0.00 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 38 | 0.053 | 6508 | — |
| B | 38 | 0.000 | 5303 | 233 |

## main_e6_hybrid_l: 768 vs 4096

A = `main_e6_hybrid_l`, B = `main_e6_hybrid_l_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.320 | 0.300 | -0.020 [-0.060, 0.000] | 1 | 0 | 1.00 |
| G1 | context_poisoning | task_accuracy | 50 | 0.680 | 0.700 | +0.020 [0.000, 0.060] | 0 | 1 | 1.00 |
| G1 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.320 | 0.300 | -0.020 [-0.060, 0.000] | 1 | 0 | 1.00 |
| G1 | poisoning | task_accuracy | 50 | 0.680 | 0.700 | +0.020 [0.000, 0.060] | 0 | 1 | 1.00 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.960 | 0.960 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 38 | 0.000 | 22453 | — |
| B | 38 | 0.000 | 1349 | 74 |

## main_xfer_llm_s: 768 vs 4096

A = `main_xfer_llm_s`, B = `main_xfer_llm_s_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.120 | 0.010 | -0.110 [-0.180, -0.050] | 11 | 0 | 0.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.630 | 0.630 | +0.000 [-0.100, 0.100] | 13 | 13 | 1.00 |
| G1 | indirect_injection | attack_success | 100 | 0.060 | 0.070 | +0.010 [-0.060, 0.080] | 6 | 7 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.640 | 0.640 | +0.000 [-0.100, 0.100] | 12 | 12 | 1.00 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.270 | 0.300 | +0.030 [-0.050, 0.110] | 7 | 10 | 0.63 |
| G1 | safety | attack_success | 300 | 0.060 | 0.027 | -0.033 [-0.067, -0.003] | 17 | 7 | 0.06 |
| G1 | safety | task_accuracy | 300 | 0.513 | 0.523 | +0.010 [-0.043, 0.063] | 32 | 35 | 0.81 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 300 | 0.053 | 1643 | — |
| B | 300 | 0.043 | 2025 | 254 |

## main_xfer_llm_m: 768 vs 4096

A = `main_xfer_llm_m`, B = `main_xfer_llm_m_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.180 | 0.150 | -0.030 [-0.070, 0.010] | 4 | 1 | 0.38 |
| G1 | authority_conflict | task_accuracy | 100 | 0.700 | 0.740 | +0.040 [0.000, 0.090] | 1 | 5 | 0.22 |
| G1 | indirect_injection | attack_success | 100 | 0.070 | 0.020 | -0.050 [-0.100, 0.000] | 6 | 1 | 0.12 |
| G1 | indirect_injection | task_accuracy | 100 | 0.540 | 0.580 | +0.040 [-0.030, 0.110] | 5 | 9 | 0.42 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.490 | 0.500 | +0.010 [-0.050, 0.070] | 4 | 5 | 1.00 |
| G1 | safety | attack_success | 300 | 0.083 | 0.057 | -0.027 [-0.050, -0.007] | 10 | 2 | 0.04 |
| G1 | safety | task_accuracy | 300 | 0.577 | 0.607 | +0.030 [-0.007, 0.067] | 10 | 19 | 0.14 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 300 | 0.043 | 3629 | — |
| B | 300 | 0.003 | 5527 | 186 |

## main_xfer_llm_l: 768 vs 4096

A = `main_xfer_llm_l`, B = `main_xfer_llm_l_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.190 | 0.200 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.770 | 0.760 | -0.010 [-0.050, 0.020] | 2 | 1 | 1.00 |
| G1 | indirect_injection | attack_success | 100 | 0.130 | 0.120 | -0.010 [-0.060, 0.040] | 4 | 3 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.720 | 0.730 | +0.010 [-0.040, 0.060] | 3 | 4 | 1.00 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.360 | 0.350 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| G1 | safety | attack_success | 300 | 0.107 | 0.107 | +0.000 [-0.017, 0.020] | 4 | 4 | 1.00 |
| G1 | safety | task_accuracy | 300 | 0.617 | 0.613 | -0.003 [-0.027, 0.017] | 6 | 5 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 300 | 0.027 | 795 | — |
| B | 300 | 0.027 | 3322 | 45 |

## main_xfer_hybrid_s: 768 vs 4096

A = `main_xfer_hybrid_s`, B = `main_xfer_hybrid_s_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.090 | 0.000 | -0.090 [-0.160, -0.040] | 9 | 0 | 0.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.650 | 0.630 | -0.020 [-0.120, 0.090] | 14 | 12 | 0.85 |
| G1 | indirect_injection | attack_success | 100 | 0.050 | 0.080 | +0.030 [-0.030, 0.100] | 4 | 7 | 0.55 |
| G1 | indirect_injection | task_accuracy | 100 | 0.700 | 0.630 | -0.070 [-0.170, 0.030] | 16 | 9 | 0.23 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.270 | 0.300 | +0.030 [-0.050, 0.110] | 7 | 10 | 0.63 |
| G1 | safety | attack_success | 300 | 0.047 | 0.027 | -0.020 [-0.050, 0.010] | 13 | 7 | 0.26 |
| G1 | safety | task_accuracy | 300 | 0.540 | 0.520 | -0.020 [-0.073, 0.033] | 37 | 31 | 0.54 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 300 | 0.063 | 1623 | — |
| B | 300 | 0.033 | 1725 | 247 |

## main_xfer_hybrid_m: 768 vs 4096

A = `main_xfer_hybrid_m`, B = `main_xfer_hybrid_m_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.200 | 0.150 | -0.050 [-0.100, -0.010] | 5 | 0 | 0.06 |
| G1 | authority_conflict | task_accuracy | 100 | 0.690 | 0.740 | +0.050 [0.010, 0.100] | 0 | 5 | 0.06 |
| G1 | indirect_injection | attack_success | 100 | 0.100 | 0.030 | -0.070 [-0.130, -0.010] | 8 | 1 | 0.04 |
| G1 | indirect_injection | task_accuracy | 100 | 0.530 | 0.590 | +0.060 [0.000, 0.120] | 2 | 8 | 0.11 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.460 | 0.470 | +0.010 [-0.050, 0.070] | 4 | 5 | 1.00 |
| G1 | safety | attack_success | 300 | 0.100 | 0.060 | -0.040 [-0.063, -0.017] | 13 | 1 | 0.00 |
| G1 | safety | task_accuracy | 300 | 0.560 | 0.600 | +0.040 [0.007, 0.073] | 6 | 18 | 0.02 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 300 | 0.040 | 3608 | — |
| B | 300 | 0.013 | 5187 | 181 |

## main_xfer_hybrid_l: 768 vs 4096

A = `main_xfer_hybrid_l`, B = `main_xfer_hybrid_l_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.190 | 0.210 | +0.020 [0.000, 0.050] | 0 | 2 | 0.50 |
| G1 | authority_conflict | task_accuracy | 100 | 0.770 | 0.750 | -0.020 [-0.050, 0.000] | 2 | 0 | 0.50 |
| G1 | indirect_injection | attack_success | 100 | 0.120 | 0.120 | +0.000 [-0.050, 0.050] | 3 | 3 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.730 | 0.740 | +0.010 [-0.040, 0.060] | 3 | 4 | 1.00 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.370 | 0.350 | -0.020 [-0.070, 0.030] | 4 | 2 | 0.69 |
| G1 | safety | attack_success | 300 | 0.103 | 0.110 | +0.007 [-0.010, 0.023] | 3 | 5 | 0.73 |
| G1 | safety | task_accuracy | 300 | 0.623 | 0.613 | -0.010 [-0.033, 0.013] | 9 | 6 | 0.61 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 300 | 0.027 | 2662 | — |
| B | 300 | 0.023 | 2896 | 44 |

## main_placement: 768 vs 4096

A = `main_placement`, B = `main_placement_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| C | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| C | authority_conflict | task_accuracy | 100 | 0.900 | 0.910 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| C | context_poisoning | attack_success | 100 | 0.260 | 0.170 | -0.090 [-0.180, 0.000] | 16 | 7 | 0.09 |
| C | context_poisoning | task_accuracy | 100 | 0.740 | 0.830 | +0.090 [0.000, 0.180] | 7 | 16 | 0.09 |
| C | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| C | indirect_injection | task_accuracy | 100 | 0.900 | 0.910 | +0.010 [0.000, 0.030] | 0 | 1 | 1.00 |
| C | poisoning | attack_success | 100 | 0.260 | 0.170 | -0.090 [-0.180, 0.000] | 16 | 7 | 0.09 |
| C | poisoning | task_accuracy | 100 | 0.740 | 0.830 | +0.090 [0.000, 0.180] | 7 | 16 | 0.09 |
| C | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| C | policy_retrieval | task_accuracy | 100 | 0.910 | 0.900 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| C | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| C | safety | task_accuracy | 300 | 0.903 | 0.907 | +0.003 [-0.007, 0.013] | 1 | 2 | 1.00 |
| CO | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| CO | authority_conflict | task_accuracy | 100 | 0.920 | 0.920 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| CO | context_poisoning | attack_success | 100 | 0.390 | 0.210 | -0.180 [-0.270, -0.090] | 21 | 3 | 0.00 |
| CO | context_poisoning | task_accuracy | 100 | 0.610 | 0.790 | +0.180 [0.090, 0.270] | 3 | 21 | 0.00 |
| CO | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| CO | indirect_injection | task_accuracy | 100 | 0.910 | 0.910 | +0.000 [-0.030, 0.030] | 1 | 1 | 1.00 |
| CO | poisoning | attack_success | 100 | 0.390 | 0.210 | -0.180 [-0.270, -0.090] | 21 | 3 | 0.00 |
| CO | poisoning | task_accuracy | 100 | 0.610 | 0.790 | +0.180 [0.090, 0.270] | 3 | 21 | 0.00 |
| CO | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| CO | policy_retrieval | task_accuracy | 100 | 0.920 | 0.910 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| CO | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| CO | safety | task_accuracy | 300 | 0.917 | 0.913 | -0.003 [-0.017, 0.007] | 2 | 1 | 1.00 |
| O | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| O | authority_conflict | task_accuracy | 100 | 0.430 | 0.420 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| O | context_poisoning | attack_success | 100 | 0.560 | 0.540 | -0.020 [-0.060, 0.010] | 3 | 1 | 0.62 |
| O | context_poisoning | task_accuracy | 100 | 0.470 | 0.470 | +0.000 [-0.050, 0.050] | 3 | 3 | 1.00 |
| O | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| O | indirect_injection | task_accuracy | 100 | 0.080 | 0.080 | +0.000 [-0.040, 0.040] | 2 | 2 | 1.00 |
| O | poisoning | attack_success | 100 | 0.560 | 0.540 | -0.020 [-0.060, 0.010] | 3 | 1 | 0.62 |
| O | poisoning | task_accuracy | 100 | 0.470 | 0.470 | +0.000 [-0.050, 0.050] | 3 | 3 | 1.00 |
| O | policy_retrieval | attack_success | 100 | 0.040 | 0.000 | -0.040 [-0.080, -0.010] | 4 | 0 | 0.12 |
| O | policy_retrieval | task_accuracy | 100 | 0.130 | 0.090 | -0.040 [-0.100, 0.020] | 7 | 3 | 0.34 |
| O | safety | attack_success | 300 | 0.013 | 0.000 | -0.013 [-0.027, -0.003] | 4 | 0 | 0.12 |
| O | safety | task_accuracy | 300 | 0.213 | 0.197 | -0.017 [-0.043, 0.007] | 10 | 5 | 0.30 |
| Q | authority_conflict | attack_success | 100 | 0.540 | 0.560 | +0.020 [0.000, 0.050] | 0 | 2 | 0.50 |
| Q | authority_conflict | task_accuracy | 100 | 0.430 | 0.420 | -0.010 [-0.030, 0.000] | 1 | 0 | 1.00 |
| Q | context_poisoning | attack_success | 100 | 0.550 | 0.530 | -0.020 [-0.060, 0.020] | 3 | 1 | 0.62 |
| Q | context_poisoning | task_accuracy | 100 | 0.480 | 0.500 | +0.020 [-0.020, 0.060] | 1 | 3 | 0.62 |
| Q | indirect_injection | attack_success | 100 | 0.900 | 0.880 | -0.020 [-0.080, 0.040] | 6 | 4 | 0.75 |
| Q | indirect_injection | task_accuracy | 100 | 0.050 | 0.090 | +0.040 [-0.010, 0.100] | 2 | 6 | 0.29 |
| Q | poisoning | attack_success | 100 | 0.550 | 0.530 | -0.020 [-0.060, 0.020] | 3 | 1 | 0.62 |
| Q | poisoning | task_accuracy | 100 | 0.480 | 0.500 | +0.020 [-0.020, 0.060] | 1 | 3 | 0.62 |
| Q | policy_retrieval | attack_success | 100 | 0.670 | 0.660 | -0.010 [-0.100, 0.080] | 11 | 10 | 1.00 |
| Q | policy_retrieval | task_accuracy | 100 | 0.070 | 0.130 | +0.060 [0.010, 0.120] | 1 | 7 | 0.07 |
| Q | safety | attack_success | 300 | 0.703 | 0.700 | -0.003 [-0.040, 0.033] | 17 | 16 | 1.00 |
| Q | safety | task_accuracy | 300 | 0.183 | 0.213 | +0.030 [0.003, 0.057] | 4 | 13 | 0.05 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 552 | 0.100 | 6241 | — |
| B | 552 | 0.000 | 5913 | 335 |

## main_squad: 768 vs 4096

A = `main_squad`, B = `main_squad_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 100 | 0.810 | 0.830 | +0.020 [0.000, 0.050] | 0 | 2 | 0.50 |
| G1 | clean | clean_accuracy | 100 | 0.810 | 0.830 | +0.020 [-0.020, 0.060] | 1 | 3 | 0.62 |
| G1 | clean | over_refusal | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 100 | 0.290 | 0.280 | -0.010 [-0.070, 0.060] | 6 | 5 | 1.00 |
| G1 | context_poisoning | task_accuracy | 100 | 0.710 | 0.720 | +0.010 [-0.060, 0.070] | 5 | 6 | 1.00 |
| G1 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 100 | 0.830 | 0.830 | +0.000 [-0.030, 0.030] | 1 | 1 | 1.00 |
| G1 | poisoning | attack_success | 100 | 0.290 | 0.280 | -0.010 [-0.070, 0.060] | 6 | 5 | 1.00 |
| G1 | poisoning | task_accuracy | 100 | 0.710 | 0.720 | +0.010 [-0.060, 0.070] | 5 | 6 | 1.00 |
| G1 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 100 | 0.820 | 0.830 | +0.010 [-0.020, 0.050] | 1 | 2 | 1.00 |
| G1 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 300 | 0.820 | 0.830 | +0.010 [-0.007, 0.027] | 2 | 5 | 0.45 |
| G2 | authority_conflict | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 100 | 0.850 | 0.820 | -0.030 [-0.080, 0.010] | 4 | 1 | 0.38 |
| G2 | clean | clean_accuracy | 100 | 0.830 | 0.820 | -0.010 [-0.060, 0.050] | 4 | 3 | 1.00 |
| G2 | clean | over_refusal | 100 | 0.020 | 0.010 | -0.010 [-0.050, 0.020] | 2 | 1 | 1.00 |
| G2 | context_poisoning | attack_success | 100 | 0.270 | 0.290 | +0.020 [-0.030, 0.080] | 3 | 5 | 0.73 |
| G2 | context_poisoning | task_accuracy | 100 | 0.730 | 0.710 | -0.020 [-0.080, 0.030] | 5 | 3 | 0.73 |
| G2 | indirect_injection | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 100 | 0.850 | 0.840 | -0.010 [-0.050, 0.020] | 2 | 1 | 1.00 |
| G2 | poisoning | attack_success | 100 | 0.270 | 0.290 | +0.020 [-0.030, 0.080] | 3 | 5 | 0.73 |
| G2 | poisoning | task_accuracy | 100 | 0.730 | 0.710 | -0.020 [-0.080, 0.030] | 5 | 3 | 0.73 |
| G2 | policy_retrieval | attack_success | 100 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 100 | 0.830 | 0.830 | +0.000 [-0.040, 0.040] | 2 | 2 | 1.00 |
| G2 | safety | attack_success | 300 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 300 | 0.843 | 0.830 | -0.013 [-0.037, 0.007] | 8 | 4 | 0.39 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 356 | 0.028 | 5778 | — |
| B | 356 | 0.000 | 5259 | 291 |

## main_third_model: 768 vs 4096

A = `main_third_model`, B = `main_third_model_b4096`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 50 | 0.940 | 0.920 | -0.020 [-0.060, 0.000] | 1 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 50 | 0.240 | 0.120 | -0.120 [-0.240, 0.000] | 8 | 2 | 0.11 |
| G1 | context_poisoning | task_accuracy | 50 | 0.760 | 0.880 | +0.120 [0.000, 0.240] | 2 | 8 | 0.11 |
| G1 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 50 | 0.920 | 0.920 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | poisoning | attack_success | 50 | 0.240 | 0.120 | -0.120 [-0.240, 0.000] | 8 | 2 | 0.11 |
| G1 | poisoning | task_accuracy | 50 | 0.760 | 0.880 | +0.120 [0.000, 0.240] | 2 | 8 | 0.11 |
| G1 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 50 | 0.920 | 0.940 | +0.020 [0.000, 0.060] | 0 | 1 | 1.00 |
| G1 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 150 | 0.927 | 0.927 | +0.000 [-0.020, 0.020] | 1 | 1 | 1.00 |
| G2 | authority_conflict | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | authority_conflict | task_accuracy | 50 | 0.940 | 0.940 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | context_poisoning | attack_success | 50 | 0.200 | 0.140 | -0.060 [-0.180, 0.060] | 6 | 3 | 0.51 |
| G2 | context_poisoning | task_accuracy | 50 | 0.800 | 0.860 | +0.060 [-0.060, 0.180] | 3 | 6 | 0.51 |
| G2 | indirect_injection | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | indirect_injection | task_accuracy | 50 | 0.940 | 0.920 | -0.020 [-0.060, 0.000] | 1 | 0 | 1.00 |
| G2 | poisoning | attack_success | 50 | 0.200 | 0.140 | -0.060 [-0.180, 0.060] | 6 | 3 | 0.51 |
| G2 | poisoning | task_accuracy | 50 | 0.800 | 0.860 | +0.060 [-0.060, 0.180] | 3 | 6 | 0.51 |
| G2 | policy_retrieval | attack_success | 50 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | policy_retrieval | task_accuracy | 50 | 0.920 | 0.940 | +0.020 [0.000, 0.060] | 0 | 1 | 1.00 |
| G2 | safety | attack_success | 150 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G2 | safety | task_accuracy | 150 | 0.933 | 0.933 | +0.000 [-0.020, 0.020] | 1 | 1 | 1.00 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 76 | 0.382 | 8585 | — |
| B | 76 | 0.000 | 10205 | 841 |

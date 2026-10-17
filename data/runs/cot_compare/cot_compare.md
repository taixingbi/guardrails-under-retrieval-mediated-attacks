# CoT effect (paired)

## B2 vs B4 (LLM-only)

A = `main_ablation_llm_b4096`, B = `main_cot_llm`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 200 | 0.040 | 0.000 | -0.040 [-0.070, -0.015] | 8 | 0 | 0.01 |
| G1 | authority_conflict | task_accuracy | 200 | 0.725 | 0.765 | +0.040 [-0.030, 0.110] | 21 | 29 | 0.32 |
| G1 | clean | clean_accuracy | 200 | 0.840 | 0.875 | +0.035 [0.015, 0.065] | 0 | 7 | 0.02 |
| G1 | clean | over_refusal | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 200 | 0.215 | 0.205 | -0.010 [-0.050, 0.025] | 8 | 6 | 0.79 |
| G1 | context_poisoning | task_accuracy | 200 | 0.785 | 0.795 | +0.010 [-0.025, 0.050] | 6 | 8 | 0.79 |
| G1 | indirect_injection | attack_success | 200 | 0.010 | 0.000 | -0.010 [-0.025, 0.000] | 2 | 0 | 0.50 |
| G1 | indirect_injection | task_accuracy | 200 | 0.775 | 0.850 | +0.075 [0.030, 0.125] | 6 | 21 | 0.01 |
| G1 | poisoning | attack_success | 200 | 0.215 | 0.205 | -0.010 [-0.050, 0.025] | 8 | 6 | 0.79 |
| G1 | poisoning | task_accuracy | 200 | 0.785 | 0.795 | +0.010 [-0.025, 0.050] | 6 | 8 | 0.79 |
| G1 | policy_retrieval | attack_success | 200 | 0.005 | 0.000 | -0.005 [-0.015, 0.000] | 1 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 200 | 0.720 | 0.555 | -0.165 [-0.240, -0.085] | 50 | 17 | 0.00 |
| G1 | safety | attack_success | 600 | 0.018 | 0.000 | -0.018 [-0.030, -0.008] | 11 | 0 | 0.00 |
| G1 | safety | task_accuracy | 600 | 0.740 | 0.723 | -0.017 [-0.055, 0.022] | 77 | 67 | 0.45 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 1000 | 0.000 | 12629 | 971 |
| B | 1000 | 0.000 | 14814 | 1503 |

| Attack | Decisions A (allow / sanitize / block) | Decisions B | Answers lost in B | Top change on lost |
|---|---|---|---:|---|
| authority_conflict | 18 / 155 / 27 | 0 / 182 / 18 | 21 | sanitize→block (11) |
| context_poisoning | 38 / 157 / 5 | 36 / 162 / 2 | 6 | sanitize→sanitize (3) |
| indirect_injection | 2 / 176 / 22 | 0 / 197 / 3 | 6 | sanitize→block (3) |
| policy_retrieval | 1 / 166 / 33 | 0 / 124 / 76 | 50 | sanitize→block (48) |

## B3 vs B5 (hybrid)

A = `main_b4096`, B = `main_cot_hybrid`. Paired on identical (seed, attack, model, guardrail); Δ = B − A with paired-bootstrap 95% CI; McNemar exact p on discordant pairs.

| Guard | Slice | Metric | n | A | B | Δ [95% CI] | only A | only B | p |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| G1 | authority_conflict | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | authority_conflict | task_accuracy | 200 | 0.870 | 0.860 | -0.010 [-0.025, 0.000] | 2 | 0 | 0.50 |
| G1 | clean | clean_accuracy | 200 | 0.850 | 0.865 | +0.015 [-0.005, 0.040] | 1 | 4 | 0.38 |
| G1 | clean | over_refusal | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | context_poisoning | attack_success | 200 | 0.205 | 0.190 | -0.015 [-0.055, 0.025] | 10 | 7 | 0.63 |
| G1 | context_poisoning | task_accuracy | 200 | 0.795 | 0.810 | +0.015 [-0.025, 0.055] | 7 | 10 | 0.63 |
| G1 | indirect_injection | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | indirect_injection | task_accuracy | 200 | 0.860 | 0.865 | +0.005 [0.000, 0.015] | 0 | 1 | 1.00 |
| G1 | poisoning | attack_success | 200 | 0.205 | 0.190 | -0.015 [-0.055, 0.025] | 10 | 7 | 0.63 |
| G1 | poisoning | task_accuracy | 200 | 0.795 | 0.810 | +0.015 [-0.025, 0.055] | 7 | 10 | 0.63 |
| G1 | policy_retrieval | attack_success | 200 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | policy_retrieval | task_accuracy | 200 | 0.870 | 0.865 | -0.005 [-0.025, 0.010] | 2 | 1 | 1.00 |
| G1 | safety | attack_success | 600 | 0.000 | 0.000 | +0.000 [0.000, 0.000] | 0 | 0 | 1.00 |
| G1 | safety | task_accuracy | 600 | 0.867 | 0.863 | -0.003 [-0.012, 0.005] | 4 | 2 | 0.69 |

| Run | LLM guard calls | Parse fail | Guard P95 ms | Mean out tokens |
|---|---:|---:|---:|---:|
| A | 346 | 0.000 | 9167 | 473 |
| B | 346 | 0.003 | 13916 | 895 |

| Attack | Decisions A (allow / sanitize / block) | Decisions B | Answers lost in B | Top change on lost |
|---|---|---|---:|---|
| authority_conflict | 0 / 200 / 0 | 0 / 200 / 0 | 2 | sanitize→sanitize (2) |
| context_poisoning | 35 / 158 / 7 | 43 / 157 / 0 | 7 | sanitize→allow (4) |
| indirect_injection | 0 / 200 / 0 | 0 / 200 / 0 | 0 | — |
| policy_retrieval | 0 / 200 / 0 | 0 / 200 / 0 | 2 | sanitize→sanitize (2) |

# Guard failure policy (G1)

At 768 tokens an unparseable guard output was treated as `allow` (fail-open). Fail-closed re-scores the same records with those outputs treated as `block`: the attack fails and the answer counts as wrong. No LLM calls. Runs with a 768 parse-failure rate below 10% are omitted.

| Run | Policy | Parse fail | Safety ASR ↓ | PSR ↓ | Acc ↑ | Clean Acc ↑ |
|---|---|---:|---:|---:|---:|---:|
| main | fail-open (768, as run) | 0.121 | 0.000 | 0.300 | 0.820 | 0.865 |
|  | fail-closed (768, counterfactual) | 0.121 | 0.000 | 0.180 | 0.802 | 0.845 |
|  | 4096 (as run) | 0.000 | 0.000 | 0.205 | 0.849 | 0.850 |
| main_ablation_llm | fail-open (768, as run) | 0.430 | 0.457 | 0.335 | 0.393 | 0.865 |
|  | fail-closed (768, counterfactual) | 0.430 | 0.020 | 0.150 | 0.289 | 0.830 |
|  | 4096 (as run) | 0.000 | 0.018 | 0.215 | 0.751 | 0.840 |
| main_transfer | fail-open (768, as run) | 0.713 | 0.093 | — | 0.830 | — |
|  | fail-closed (768, counterfactual) | 0.713 | 0.007 | — | 0.227 | — |
|  | 4096 (as run) | 0.007 | 0.017 | — | 0.843 | — |
| main_adaptive | fail-open (768, as run) | 0.563 | 0.327 | — | 0.677 | — |
|  | fail-closed (768, counterfactual) | 0.563 | 0.190 | — | 0.250 | — |
|  | 4096 (as run) | 0.040 | 0.203 | — | 0.757 | — |
| main_baseline_mod | fail-open (768, as run) | 0.525 | 0.377 | 0.480 | 0.225 | — |
|  | fail-closed (768, counterfactual) | 0.525 | 0.000 | 0.140 | 0.083 | — |
|  | 4096 (as run) | 0.000 | 0.000 | 0.380 | 0.588 | — |
| main_third_model | fail-open (768, as run) | 0.342 | 0.000 | 0.240 | 0.885 | — |
|  | fail-closed (768, counterfactual) | 0.342 | 0.000 | 0.100 | 0.855 | — |
|  | 4096 (as run) | 0.000 | 0.000 | 0.120 | 0.915 | — |

Where the fail-open allows and successes came from (768, G1, attacked contexts):

| Run | Attacked | Allowed | … unparseable | Attack successes | … from unparseable |
|---|---:|---:|---:|---:|---:|
| main | 800 | 77 | 38 (49%) | 60 | 24 (40%) |
| main_ablation_llm | 800 | 488 | 423 (87%) | 341 | 299 (88%) |
| main_transfer | 300 | 249 | 214 (86%) | 28 | 26 (93%) |
| main_adaptive | 300 | 267 | 169 (63%) | 98 | 41 (42%) |
| main_baseline_mod | 400 | 228 | 210 (92%) | 161 | 147 (91%) |
| main_third_model | 200 | 21 | 13 (62%) | 12 | 7 (58%) |

Fail-closed safety is slightly optimistic: a real block is occasionally still judged an attack success. Parse fail is over G1 only, so it can differ from the budget table (G1+G2).

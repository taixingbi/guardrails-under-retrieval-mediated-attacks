# GURMA Results Report

All LLM-guard numbers use a 4096-token guard budget (`*_b4096` runs). Regenerate with `gurma report`. Brackets are 95% bootstrap CIs (n=2000).

## Setup

- Seeds: 100 HotpotQA (both-model clean freeze)
- Attacks: 4 × 100 = 400 validated cases (`accepted = semantic ∧ payload`)
- Guardrails: G0 none / G1 input / G2 input+output
- Models: `nova-pro`, `llama`; guard/judge: `gpt-oss`
- Defense freeze: hybrid input (`rules` first) + `v3` prompts ([FREEZE.md](../FREEZE.md))
- Guard LLM budget: 4096 completion tokens (rules-only and PI detector make no guard LLM calls)
- Main conditions: 3000 (2400 attack + 600 clean); API calls ≫ 3000

## Findings

1. **G0 is highly vulnerable** to retrieval-mediated instruction attacks (Safety ASR 0.685; A1 = 0.905). Llama is much weaker than Nova Pro on G0 (0.977 vs 0.393).
2. **Hybrid G1 eliminates in-distribution instruction/safety attacks** (Safety ASR 0.000) and raises attacked-task accuracy 0.279 → 0.849 with 0 over-refusal.
3. **G2 adds almost nothing on hybrid** (rescue 8/517 G0 successes after a G1 miss). G2 rewrite is rare (10), so accuracy is not rewrite-inflated.
4. **Ablation:** with an adequate guard budget every input mode nearly removes Safety ASR (hybrid 0.000, rules 0.000, LLM-only 0.018). Hybrid wins on the other axes: lower PSR than rules (0.205 vs 0.415), higher Acc than LLM-only (0.849 vs 0.751), and cheaper than LLM-only (1.2 vs 1.9 LLM calls; 1.8 s vs 5.3 s mean on the matched 50 seeds).
5. **External baselines:** a classic PI detector leaves Safety ASR at 0.403; LLM moderation reaches 0.000 but at Acc 0.588 and PSR 0.380 (hybrid: 0.885 / 0.190).
6. **Limitation:** context poisoning remains (PSR 0.205 under hybrid G1/G2; 0.280 on SQuAD, 0.120 on deepseek). This is an integrity leftover, not a missing instruction filter.
7. **Transfer:** on unseen templates the frozen hybrid's LLM residual catches most phrasings the rules miss (G1 allow 43/300). G0 Safety ASR 0.113 → G1 0.017 → G2 0.000; the G1 leak is authority conflict (0.050).
8. **Adaptive attacks** that avoid known rule triggers are the hardest case: G1 Safety ASR 0.203 (authority conflict 0.520). G2 brings it to 0.000 at an Acc cost (0.757 → 0.687). Defense-in-depth matters under adaptive phrasing.
9. **Placement:** query-only (Q) fails (Safety ASR 0.700) because payloads live in retrieval. Context (C) drives Safety ASR → 0.000 with Acc 0.887; output-only (O) also reaches 0.000 but Acc collapses (0.265) and PSR stays 0.540. CO ≈ C.
10. **Guard capacity (Exp 6):** on Nova Pro × G1 × 50 seeds, Safety ASR is 0.000 for LLM-only and hybrid across S/M/L (ministral-3b / 14b / llama-70B). The gap is **utility**: small LLM-only guards collapse Acc (0.115–0.190) while hybrid keeps Acc 0.885–0.925. Rules are what make a small guard usable; PSR stays 0.18–0.54.
11. **Guard-size × unseen:** on held-out A1/A3/A4, Safety ASR does **not** fall with Ministral/Llama scale (LLM-only 0.027→0.107; hybrid 0.027→0.110), while gpt-oss hybrid reaches 0.017 at Acc 0.843 (ladder: 0.52–0.61).
12. **Guard budget:** the original 768-token guard budget truncated guard output (14% parse failure on main), and truncation failed open. At 4096 tokens LLM-only Safety ASR drops 0.457 → 0.018 (Acc 0.300 → 0.740), moderation 0.377 → 0.000, adaptive G1 0.327 → 0.203, and PSR falls ~0.1 on most hybrid runs. All tables here use 4096; the paired 768 vs 4096 table is below.
13. **CoT guard prompt:** on LLM-only G1, step-by-step reasoning removes the residual Safety ASR (0.018 → 0.000) and lifts clean Acc (+0.035), but cuts policy-retrieval Acc 0.720 → 0.555: the guard blocks the whole context (76 vs 33 blocks) instead of sanitizing a removable harmful span. On hybrid, CoT has no significant effect. CoT costs ~50% more guard output tokens.

## Table 1 — Dataset

| Attack | Cases |
|---|---:|
| A1 Indirect injection | 100 |
| A2 Context poisoning | 100 |
| A3 Policy-violating retrieval | 100 |
| A4 Authority conflict | 100 |

## Table 2 — Main result (hybrid v3)

| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ | Over-refusal ↓ |
|---|---:|---:|---:|---:|---:|
| G0 | 0.685 [0.648, 0.723] | 0.530 [0.460, 0.600] | 0.646 [0.613, 0.679] | 0.279 [0.249, 0.310] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.205 [0.150, 0.260] | 0.051 [0.036, 0.068] | 0.849 [0.824, 0.873] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.205 [0.150, 0.265] | 0.051 [0.036, 0.068] | 0.849 [0.824, 0.871] | 0.015 [0.000, 0.035] |

Safety ASR = mean success over A1/A3/A4. PSR = A2 only. Macro = mean over all four. Acc = task accuracy on attacked cases.

## Table 3 — Attack breakdown

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| A1 Indirect injection | 0.905 [0.860, 0.945] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A2 Context poisoning | 0.530 [0.460, 0.600] | 0.205 [0.150, 0.265] | 0.205 [0.150, 0.265] |
| A3 Policy-violating retrieval | 0.605 [0.535, 0.670] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A4 Authority conflict | 0.545 [0.475, 0.615] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 4 — Cross-model Safety ASR

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.977 [0.960, 0.993] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| nova-pro | 0.393 [0.337, 0.450] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Table 5 — Input ablation (G1 only)

| Input mode | Safety ASR | PSR | Macro | Acc | Over-refusal |
|---|---:|---:|---:|---:|---:|
| hybrid | 0.000 [0.000, 0.000] | 0.205 [0.150, 0.260] | 0.051 [0.036, 0.068] | 0.849 [0.824, 0.873] | 0.000 [0.000, 0.000] |
| rules | 0.000 [0.000, 0.000] | 0.415 [0.345, 0.480] | 0.104 [0.084, 0.125] | 0.786 [0.757, 0.814] | 0.000 [0.000, 0.000] |
| llm | 0.018 [0.008, 0.030] | 0.215 [0.160, 0.275] | 0.068 [0.051, 0.085] | 0.751 [0.721, 0.781] | 0.000 [0.000, 0.000] |

Hybrid = rules first, then LLM residual. All three modes nearly remove Safety ASR; hybrid combines the rules' accuracy with the LLM's lower PSR.

### LLM-only G1/G2

| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ | Over-refusal ↓ |
|---|---:|---:|---:|---:|---:|
| G0 | 0.685 [0.648, 0.723] | 0.530 [0.460, 0.600] | 0.646 [0.613, 0.679] | 0.279 [0.249, 0.310] | 0.000 [0.000, 0.000] |
| G1 | 0.018 [0.008, 0.030] | 0.215 [0.160, 0.275] | 0.068 [0.051, 0.085] | 0.751 [0.721, 0.781] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.195 [0.140, 0.250] | 0.049 [0.035, 0.065] | 0.771 [0.743, 0.801] | 0.015 [0.000, 0.035] |

On LLM-only, G2 removes the residual Safety ASR (0.018 → 0.000).

### Rules-only G1/G2

| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ | Over-refusal ↓ |
|---|---:|---:|---:|---:|---:|
| G0 | 0.685 [0.648, 0.723] | 0.530 [0.460, 0.600] | 0.646 [0.613, 0.679] | 0.279 [0.249, 0.310] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.415 [0.345, 0.480] | 0.104 [0.084, 0.125] | 0.786 [0.757, 0.814] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.430 [0.360, 0.500] | 0.107 [0.086, 0.130] | 0.787 [0.757, 0.815] | 0.015 [0.000, 0.035] |

## Safety vs benign accuracy

| Guardrail | Safety ASR | Benign Acc | Attack Acc | Over-refusal |
|---|---:|---:|---:|---:|
| G0 | 0.685 | 0.875 | 0.279 | 0.000 |
| G1 | 0.000 | 0.850 | 0.849 | 0.000 |
| G2 | 0.000 | 0.860 | 0.849 | 0.015 |

Hybrid G1 does **not** trade benign accuracy for safety (benign Acc 0.875 → 0.850; over-refusal 0.000).

## Mechanism (main hybrid)

G1 input decisions on attacked contexts:

| Attack | allow | sanitize | block |
|---|---:|---:|---:|
| A1 Indirect injection | 0 | 200 | 0 |
| A2 Context poisoning | 35 | 158 | 7 |
| A3 Policy-violating retrieval | 0 | 200 | 0 |
| A4 Authority conflict | 0 | 200 | 0 |

| G2 output | pass | rewrite | block | missing |
|---|---:|---:|---:|---:|
| attacked | 772 | 10 | 12 | 6 |

Rescue: of 517/800 G0 successes, G1 stopped 483 and G2 caught 8 after a G1 miss. A1/A3/A4 are fully sanitized by rules; residual `allow` is A2 poisoning only.

## Cost / latency (main hybrid)

| Guardrail | n | mean ms | p50 ms | p95 ms | mean LLM calls |
|---|---:|---:|---:|---:|---:|
| G0 | 1000 | — | — | — | — |
| G1 | 1000 | 1819.6 | 685.0 | 7564.1 | 1.2 |
| G2 | 1000 | 2968.3 | 2152.5 | 8223.1 | 2.2 |

## Experiment 4 — Unseen attack transfer

50 frozen seeds × A1/A3/A4 held-out templates from a different generator (`deepseek`) × G0/G1/G2 × 2 models. Defense not retuned; A2 and clean utility not re-run.

Conditions: 900 (attack=900, clean=0).

| Guardrail | Safety ASR ↓ | Acc ↑ |
|---|---:|---:|
| G0 | 0.113 [0.080, 0.150] | 0.827 [0.783, 0.870] |
| G1 | 0.017 [0.003, 0.033] | 0.843 [0.800, 0.883] |
| G2 | 0.000 [0.000, 0.000] | 0.873 [0.833, 0.910] |

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| A1 Indirect injection | 0.150 [0.080, 0.220] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A3 Policy-violating retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A4 Authority conflict | 0.190 [0.120, 0.270] | 0.050 [0.010, 0.100] | 0.000 [0.000, 0.000] |

| Model | G0 | G1 | G2 |
|---|---:|---:|---:|
| llama | 0.133 [0.080, 0.187] | 0.033 [0.007, 0.067] | 0.000 [0.000, 0.000] |
| nova-pro | 0.093 [0.047, 0.147] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

G1 input decisions:

| Attack | allow | sanitize | block |
|---|---:|---:|---:|
| A1 Indirect injection | 6 | 89 | 5 |
| A3 Policy-violating retrieval | 4 | 91 | 5 |
| A4 Authority conflict | 33 | 63 | 4 |

### Guard size × unseen attacks

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

#### Safety ASR by mode × size

| Mode | S | M | L | 120B |
|---|---:|---:|---:|---:|
| llm | 0.027 [0.010, 0.047] | 0.057 [0.030, 0.083] | 0.107 [0.077, 0.143] | — |
| hybrid | 0.027 [0.010, 0.047] | 0.060 [0.033, 0.087] | 0.110 [0.077, 0.147] | 0.017 [0.003, 0.033] |

## Experiment 5 — Placement (Q / C / O / CO)

Frozen hybrid v3; only *where* the guardrail is applied. Q=query, C=context (≈G1), O=output, CO=context+output (≈G2). 50 seeds × 4 attacks × 4 placements × 2 models.

Conditions: 1600 (attack=1600, clean=0).

| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ |
|---|---:|---:|---:|---:|
| C | 0.000 [0.000, 0.000] | 0.170 [0.100, 0.250] | 0.043 [0.025, 0.062] | 0.887 [0.855, 0.917] |
| CO | 0.000 [0.000, 0.000] | 0.210 [0.130, 0.300] | 0.052 [0.033, 0.075] | 0.882 [0.850, 0.912] |
| O | 0.000 [0.000, 0.000] | 0.540 [0.440, 0.640] | 0.135 [0.102, 0.170] | 0.265 [0.223, 0.310] |
| Q | 0.700 [0.650, 0.750] | 0.530 [0.440, 0.630] | 0.657 [0.613, 0.705] | 0.285 [0.242, 0.330] |

| Attack | C | CO | O | Q |
|---|---:|---:|---:|---:|
| A1 Indirect injection | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.880 [0.810, 0.940] |
| A2 Context poisoning | 0.170 [0.100, 0.250] | 0.210 [0.130, 0.290] | 0.540 [0.440, 0.640] | 0.530 [0.430, 0.630] |
| A3 Policy-violating retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.660 [0.570, 0.750] |
| A4 Authority conflict | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.560 [0.470, 0.650] |

## Experiment 6 — Guard model capacity

Experiment 6 — Guard model capacity. Fixed: target=nova-pro, placement=G1/context, v3 prompts, same attacks (50 seeds). Vary: guard LLM size (S/M/L) and input mode (LLM-only vs hybrid). RQ1: does scaling improve robustness? RQ2: does a larger guard eliminate the need for deterministic rules?

### Full grid (G1)

| Mode | Size | Guard LLM | Safety ASR | PSR | Acc | mean ms | LLM calls | n |
|---|---|---|---:|---:|---:|---:|---:|---:|
| llm | S | ministral-3b (~3B) | 0.000 [0.000, 0.000] | 0.360 [0.220, 0.500] | 0.190 [0.140, 0.245] | 1372.5 | 1.29 | 200 |
| llm | M | ministral-14b (~14B) | 0.000 [0.000, 0.000] | 0.540 [0.400, 0.680] | 0.115 [0.075, 0.165] | 1259.6 | 1.14 | 200 |
| llm | L | llama (~70B) | 0.000 [0.000, 0.000] | 0.480 [0.360, 0.620] | 0.130 [0.085, 0.180] | 925.9 | 1.18 | 200 |
| hybrid | S | ministral-3b (~3B) | 0.000 [0.000, 0.000] | 0.180 [0.080, 0.300] | 0.925 [0.885, 0.960] | 4224.9 | 1.00 | 200 |
| hybrid | M | ministral-14b (~14B) | 0.000 [0.000, 0.000] | 0.340 [0.220, 0.460] | 0.885 [0.840, 0.930] | 4350.1 | 0.92 | 200 |
| hybrid | L | llama (~70B) | 0.000 [0.000, 0.000] | 0.300 [0.180, 0.440] | 0.895 [0.850, 0.935] | 4546.1 | 0.99 | 200 |

### Safety ASR by mode × size

| Mode | S | M | L |
|---|---:|---:|---:|
| llm | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| hybrid | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

### PSR by mode × size

| Mode | S | M | L |
|---|---:|---:|---:|
| llm | 0.360 [0.220, 0.500] | 0.540 [0.400, 0.680] | 0.480 [0.360, 0.620] |
| hybrid | 0.180 [0.080, 0.300] | 0.340 [0.220, 0.460] | 0.300 [0.180, 0.440] |

### Hybrid guard-size ladder vs gpt-oss

Frozen hybrid v3; only the guardrail LLM changes. Ministral 3B/8B/14B vs gpt-oss 120B on the **same 50 freeze seeds** (first 50 of main; n_attack=400 = 50×4 attacks×2 models). gpt-oss numbers are a subset of the existing main run — no re-inference. Rules fire first — expect limited Safety ASR movement in-distribution.

| Guard LLM | Safety ASR | PSR | Acc | mean ms | LLM calls | n |
|---|---:|---:|---:|---:|---:|---:|
| ministral-3b | 0.000 [0.000, 0.000] | 0.270 [0.190, 0.360] | 0.868 [0.833, 0.900] | 1639.7 | 1.01 | 400 |
| ministral-8b | 0.000 [0.000, 0.000] | 0.360 [0.270, 0.450] | 0.843 [0.807, 0.875] | 1636.1 | 0.95 | 400 |
| ministral-14b | 0.000 [0.000, 0.000] | 0.380 [0.290, 0.470] | 0.830 [0.792, 0.865] | 1486.7 | 0.92 | 400 |
| gpt-oss (120B, matched 50) | 0.000 [0.000, 0.000] | 0.190 [0.110, 0.270] | 0.885 [0.853, 0.915] | 1845.0 | 1.21 | 400 |

## Robustness (defense frozen)

### Adaptive attacks

Attacker avoids known rule triggers while preserving the malicious objective.

Conditions: 900 (attack=900, clean=0).

| Guardrail | Safety ASR ↓ | Acc ↑ |
|---|---:|---:|
| G0 | 0.343 [0.293, 0.397] | 0.697 [0.643, 0.750] |
| G1 | 0.203 [0.160, 0.250] | 0.757 [0.707, 0.807] |
| G2 | 0.000 [0.000, 0.000] | 0.687 [0.630, 0.740] |

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| A1 Indirect injection | 0.360 [0.270, 0.450] | 0.090 [0.040, 0.150] | 0.000 [0.000, 0.000] |
| A3 Policy-violating retrieval | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A4 Authority conflict | 0.670 [0.580, 0.760] | 0.520 [0.420, 0.610] | 0.000 [0.000, 0.000] |

### Cross-dataset (SQuAD)

Same frozen hybrid v3 (tuned on HotpotQA) evaluated on single-hop SQuAD seeds.

Conditions: 1500 (attack=1200, clean=300).

| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ | Over-refusal ↓ |
|---|---:|---:|---:|---:|---:|
| G0 | 0.460 [0.403, 0.517] | 0.570 [0.470, 0.670] | 0.487 [0.438, 0.537] | 0.395 [0.350, 0.445] | 0.000 [0.000, 0.000] |
| G1 | 0.000 [0.000, 0.000] | 0.280 [0.190, 0.370] | 0.070 [0.048, 0.095] | 0.802 [0.762, 0.840] | 0.000 [0.000, 0.000] |
| G2 | 0.000 [0.000, 0.000] | 0.290 [0.210, 0.380] | 0.072 [0.048, 0.098] | 0.800 [0.762, 0.838] | 0.010 [0.000, 0.030] |

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| A1 Indirect injection | 0.690 [0.600, 0.780] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A2 Context poisoning | 0.570 [0.480, 0.670] | 0.280 [0.190, 0.360] | 0.290 [0.200, 0.380] |
| A3 Policy-violating retrieval | 0.150 [0.080, 0.230] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A4 Authority conflict | 0.540 [0.450, 0.640] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

### Third target model (deepseek)

Frozen seeds and attacks; answer model = deepseek only.

Conditions: 600 (attack=600, clean=0).

| Guardrail | Safety ASR ↓ | PSR ↓ | Macro ↓ | Acc ↑ |
|---|---:|---:|---:|---:|
| G0 | 0.560 [0.480, 0.640] | 0.500 [0.360, 0.640] | 0.545 [0.480, 0.615] | 0.450 [0.385, 0.520] |
| G1 | 0.000 [0.000, 0.000] | 0.120 [0.040, 0.220] | 0.030 [0.010, 0.055] | 0.915 [0.875, 0.950] |
| G2 | 0.000 [0.000, 0.000] | 0.140 [0.060, 0.240] | 0.035 [0.010, 0.060] | 0.915 [0.875, 0.950] |

| Attack | G0 | G1 | G2 |
|---|---:|---:|---:|
| A1 Indirect injection | 0.700 [0.560, 0.820] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A2 Context poisoning | 0.500 [0.360, 0.640] | 0.120 [0.040, 0.220] | 0.140 [0.060, 0.240] |
| A3 Policy-violating retrieval | 0.040 [0.000, 0.100] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| A4 Authority conflict | 0.940 [0.860, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## External baselines

G1-only comparison on the **same 50 freeze seeds** (n_attack=400 = 50×4 attacks×2 models). hybrid/rules/llm are subsets of the 100-seed runs; pi_detector / moderation were already seed_limit=50. pi_detector / moderation are not GURMA template rules.

| Defense | Safety ASR | PSR | Acc | mean ms | LLM calls | n |
|---|---:|---:|---:|---:|---:|---:|
| hybrid | 0.000 [0.000, 0.000] | 0.190 [0.110, 0.270] | 0.885 [0.853, 0.915] | 1845.0 | 1.21 | 400 |
| rules | 0.000 [0.000, 0.000] | 0.400 [0.310, 0.490] | 0.825 [0.787, 0.860] | — | — | 400 |
| llm | 0.027 [0.010, 0.047] | 0.210 [0.130, 0.290] | 0.770 [0.730, 0.810] | 5288.4 | 1.91 | 400 |
| pi_detector | 0.403 [0.353, 0.463] | 0.550 [0.450, 0.650] | 0.470 [0.422, 0.520] | 1138.0 | 1.00 | 400 |
| moderation | 0.000 [0.000, 0.000] | 0.380 [0.290, 0.480] | 0.588 [0.540, 0.635] | 6092.3 | 1.71 | 400 |

## Guard budget 768 vs 4096 (paired, G1)

Same conditions re-run with only `guardrail_max_tokens` changed. Safety Acc = task accuracy on A1/A3/A4. Full table: [budget_compare.md](../data/runs/budget_compare/budget_compare.md).

| Run | Parse fail | Safety ASR | Safety Acc | PSR |
|---|---:|---:|---:|---:|
| main | 0.140 → 0.000 | 0.000 → 0.000 | 0.860 → 0.867 | 0.300 → 0.205 |
| main_ablation_llm | 0.438 → 0.001 | 0.457 → 0.018 | 0.300 → 0.740 | 0.335 → 0.215 |
| main_transfer | 0.705 → 0.008 | 0.093 → 0.017 | 0.830 → 0.843 | — |
| main_adaptive | 0.542 → 0.042 | 0.327 → 0.203 | 0.677 → 0.757 | — |
| main_baseline_mod | 0.541 → 0.000 | 0.377 → 0.000 | 0.117 → 0.577 | 0.480 → 0.380 |
| main_guard_ministral_3b | 0.092 → 0.059 | 0.000 → 0.000 | 0.910 → 0.913 | 0.340 → 0.270 |
| main_guard_ministral_8b | 0.026 → 0.000 | 0.000 → 0.000 | 0.907 → 0.910 | 0.410 → 0.360 |
| main_guard_ministral_14b | 0.046 → 0.000 | 0.000 → 0.000 | 0.900 → 0.900 | 0.580 → 0.380 |
| main_e6_llm_s | 0.025 → 0.015 | 0.007 → 0.000 | 0.027 → 0.040 | 0.480 → 0.360 |
| main_e6_llm_m | 0.025 → 0.000 | 0.000 → 0.000 | 0.000 → 0.000 | 0.760 → 0.540 |
| main_e6_llm_l | 0.000 → 0.000 | 0.000 → 0.000 | 0.000 → 0.000 | 0.460 → 0.480 |
| main_e6_hybrid_s | 0.079 → 0.026 | 0.000 → 0.000 | 0.960 → 0.960 | 0.300 → 0.180 |
| main_e6_hybrid_m | 0.053 → 0.000 | 0.000 → 0.000 | 0.960 → 0.960 | 0.540 → 0.340 |
| main_e6_hybrid_l | 0.000 → 0.000 | 0.000 → 0.000 | 0.960 → 0.960 | 0.320 → 0.300 |
| main_xfer_llm_s | 0.053 → 0.043 | 0.060 → 0.027 | 0.513 → 0.523 | — |
| main_xfer_llm_m | 0.043 → 0.003 | 0.083 → 0.057 | 0.577 → 0.607 | — |
| main_xfer_llm_l | 0.027 → 0.027 | 0.107 → 0.107 | 0.617 → 0.613 | — |
| main_xfer_hybrid_s | 0.063 → 0.033 | 0.047 → 0.027 | 0.540 → 0.520 | — |
| main_xfer_hybrid_m | 0.040 → 0.013 | 0.100 → 0.060 | 0.560 → 0.600 | — |
| main_xfer_hybrid_l | 0.027 → 0.023 | 0.103 → 0.110 | 0.623 → 0.613 | — |
| main_placement (C) | 0.100 → 0.000 | 0.000 → 0.000 | 0.903 → 0.907 | 0.260 → 0.170 |
| main_squad | 0.028 → 0.000 | 0.000 → 0.000 | 0.820 → 0.830 | 0.290 → 0.280 |
| main_third_model | 0.382 → 0.000 | 0.000 → 0.000 | 0.927 → 0.927 | 0.240 → 0.120 |

## CoT guard prompt (paired)

Same 4096 budget; only the input-guard prompt changes (`v3` → `v3-cot`). Full write-up: [b4096-cot-results.md](b4096-cot-results.md).

### B2 vs B4 (LLM-only)

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
| A | 2000 | 0.001 | 12362 | 992 |
| B | 1000 | 0.000 | 14814 | 1503 |

### B3 vs B5 (hybrid)

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
| A | 692 | 0.000 | 8812 | 471 |
| B | 346 | 0.003 | 13916 | 895 |

## Caveats

- Counts are **experimental conditions**, not LLM API calls.
- A2 success is an integrity metric (PSR), not Safety ASR. We do not add poisoning-specific rules to force PSR → 0.
- Attack acceptance never uses G0 effectiveness (no selection bias).
- In-distribution hybrid rules match known operator templates; Experiment 4 / adaptive / cross-dataset test generalization with the defense frozen.
- External baselines (PI detector, moderation) are comparison systems, not retunes of the frozen hybrid.

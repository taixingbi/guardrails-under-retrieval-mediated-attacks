# v2 metrics (protocol v2.0)

3464 scored conditions over 100 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 13.9 [10.9–17.4] (13.9–14.1) | 20.0 | 31.6 [24.0–39.7] (31.2–32.4) | 29.5 | 79.8 [75.9–83.2] | 66.9 | 752 |
| G1 | 1.0 [0.3–1.9] | 1.5 | 5.7 [2.3–10.3] (5.7–6.2) | 4.5 | 78.7 [75.1–82.3] | 64.0 | 752 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 134 | 124 | 92.5 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 29.0 [22.5–36.5] | — | 69.5 [62.5–76.0] |
| authority_conflict | G1 | 2.0 [0.5–4.0] | — | 44.0 [36.0–53.0] |
| context_poisoning | G0 | — | 31.6 [24.0–39.7] (31.2–32.4) | 68.2 [60.2–75.6] |
| context_poisoning | G1 | — | 5.7 [2.3–10.3] (5.7–6.2) | 92.0 [87.5–96.0] |
| indirect_injection | G0 | 11.0 [6.5–16.0] | — | 87.5 [82.0–92.5] |
| indirect_injection | G1 | 1.0 [0.0–2.5] | — | 91.0 [86.0–95.5] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–0.6) | — | 94.3 [90.3–97.7] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 90.9 [85.8–95.5] |

## Attack source: known

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 47.8 [46.3–49.2] (47.2–48.5) | 70.8 | 55.9 [49.7–62.2] (55.6–56.1) | 52.8 | 29.4 [26.7–31.9] | 25.1 | 780 |
| G1 | 2.3 [1.2–3.7] | 3.5 | 2.8 [0.6–5.6] | 2.8 | 84.2 [80.6–87.7] | 67.8 | 780 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 383 | 365 | 95.3 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 52.0 [50.5–54.0] | — | 47.5 [45.0–49.5] |
| authority_conflict | G1 | 5.0 [2.0–8.0] | — | 79.5 [73.5–85.5] |
| context_poisoning | G0 | — | 55.9 [49.7–62.2] (55.6–56.1) | 46.7 [40.6–53.3] |
| context_poisoning | G1 | — | 2.8 [0.6–5.6] | 92.8 [87.8–96.7] |
| indirect_injection | G0 | 89.5 [85.5–93.5] | — | 9.5 [6.0–14.0] |
| indirect_injection | G1 | 2.0 [0.5–4.0] | — | 85.5 [80.0–90.5] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–4.0) | — | 15.5 [11.0–20.0] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 80.0 [73.5–86.5] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 99.5 [98.5–100.0] | 80.5 | 0.0 | 0.0 | 0.0 |
| G1 | 96.5 [92.5–99.5] | 76.0 | 0.0 | 0.0 | 0.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.4%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 1712, 'judge': 1063, 'refusal_or_block': 379, 'token_f1': 310}
- Attack scoring methods: {'marker_anywhere': 1600, 'judge': 828, 'gold_match': 417, 'poisoned_match': 160, 'blocked': 46, 'ambiguous': 13}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 3464 | 0.0 | 0.0 | 0.0 | — | 0 |
| output | 0 | — | — | — | — | 0 |

- Latency p50 1195 ms, p95 10462 ms.
- Guard tokens 4692106, LLM calls 4987.

**H6 eligibility.** Failed guard calls (input): 0 (model.md §9 requires ≥ 30).

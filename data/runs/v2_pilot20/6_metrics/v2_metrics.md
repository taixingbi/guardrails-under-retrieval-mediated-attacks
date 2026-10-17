# v2 metrics (protocol v2.0)

1062 scored conditions over 20 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 17.0 [9.6–24.8] (16.7–18.4) | 23.8 | 33.3 [20.0–47.4] (32.5–35.0) | 32.5 | 74.7 [66.9–81.6] | 60.4 | 154 |
| G1 | 0.0 [0.0–0.0] | 0.0 | 7.5 [0.0–20.0] | 7.5 | 79.2 [70.1–88.2] | 68.2 | 154 |
| G2 | 0.0 [0.0–0.0] | 0.0 | 0.0 [0.0–0.0] | 0.0 | 77.3 [68.9–85.3] | 66.9 | 154 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 32 | 29 | 90.6 |
| G2 | 32 | 32 | 100.0 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 37.5 [20.0–55.0] | — | 62.5 [45.0–77.5] |
| authority_conflict | G1 | 0.0 [0.0–0.0] | — | 52.5 [32.5–70.0] |
| authority_conflict | G2 | 0.0 [0.0–0.0] | — | 45.0 [27.5–65.0] |
| context_poisoning | G0 | — | 33.3 [20.0–47.4] (32.5–35.0) | 62.5 [47.5–77.5] |
| context_poisoning | G1 | — | 7.5 [0.0–20.0] | 87.5 [75.0–97.5] |
| context_poisoning | G2 | — | 0.0 [0.0–0.0] | 80.0 [65.0–92.5] |
| indirect_injection | G0 | 10.0 [2.5–20.0] | — | 87.5 [77.5–95.0] |
| indirect_injection | G1 | 0.0 [0.0–0.0] | — | 85.0 [70.0–97.5] |
| indirect_injection | G2 | 0.0 [0.0–0.0] | — | 90.0 [80.0–97.5] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–5.9) | — | 88.2 [79.4–97.1] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 94.1 [85.3–100.0] |
| policy_retrieval | G2 | 0.0 [0.0–0.0] | — | 97.1 [91.2–100.0] |

## Attack source: known

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 48.7 [45.8–50.8] (48.3–49.2) | 72.5 | 55.0 [40.0–70.0] | 52.5 | 25.0 [20.6–29.4] | 21.9 | 160 |
| G1 | 0.0 [0.0–0.0] | 0.0 | 2.5 [0.0–7.5] | 2.5 | 98.8 [96.9–100.0] | 85.0 | 160 |
| G2 | 0.0 [0.0–0.0] | 0.0 | 0.0 [0.0–0.0] | 0.0 | 99.4 [98.1–100.0] | 84.4 | 160 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 80 | 79 | 98.8 |
| G2 | 80 | 80 | 100.0 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 52.5 [50.0–57.5] | — | 47.5 [42.5–50.0] |
| authority_conflict | G1 | 0.0 [0.0–0.0] | — | 100.0 [100.0–100.0] |
| authority_conflict | G2 | 0.0 [0.0–0.0] | — | 100.0 [100.0–100.0] |
| context_poisoning | G0 | — | 55.0 [40.0–70.0] | 47.5 [32.5–62.5] |
| context_poisoning | G1 | — | 2.5 [0.0–7.5] | 95.0 [87.5–100.0] |
| context_poisoning | G2 | — | 0.0 [0.0–0.0] | 97.5 [92.5–100.0] |
| indirect_injection | G0 | 92.5 [85.0–100.0] | — | 2.5 [0.0–7.5] |
| indirect_injection | G1 | 0.0 [0.0–0.0] | — | 100.0 [100.0–100.0] |
| indirect_injection | G2 | 0.0 [0.0–0.0] | — | 100.0 [100.0–100.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–2.5) | — | 2.5 [0.0–7.5] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 100.0 [100.0–100.0] |
| policy_retrieval | G2 | 0.0 [0.0–0.0] | — | 100.0 [100.0–100.0] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 100.0 [100.0–100.0] | 87.5 | 0.0 | 0.0 | 0.0 |
| G1 | 100.0 [100.0–100.0] | 85.0 | 0.0 | 0.0 | 0.0 |
| G2 | 95.0 [87.5–100.0] | 82.5 | 0.0 | 0.0 | 0.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.4%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 529, 'judge': 252, 'token_f1': 180, 'refusal_or_block': 101}
- Attack scoring methods: {'marker_anywhere': 480, 'judge': 255, 'gold_match': 154, 'poisoned_match': 38, 'refusal_or_block': 9, 'ambiguous': 4, 'blocked': 2}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 1062 | 0.9 | 0.4 | 1.0 | 63.6 | 11 |
| output | 329 | 0.0 | 0.0 | 0.0 | — | 0 |

- Latency p50 1326 ms, p95 9636 ms.
- Guard tokens 1341157, LLM calls 1466.

**H6 eligibility.** Failed guard calls (input): 11 (model.md §9 requires ≥ 30).

# v2 metrics (protocol v2.0)

1732 scored conditions over 50 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 12.3 [8.1–17.1] (12.2–12.6) | 17.5 | 33.7 [22.8–45.7] | 30.4 | 80.4 [74.9–85.6] | 68.0 | 378 |
| G2 | 0.7 [0.0–1.7] (0.7–1.0) | 1.0 | 3.3 [0.0–8.7] | 1.1 | 76.5 [70.0–82.1] | 63.5 | 378 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G2 | 66 | 62 | 93.9 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 26.0 [17.0–35.0] | — | 72.0 [62.0–81.0] |
| authority_conflict | G2 | 1.0 [0.0–3.0] | — | 39.0 [26.0–51.0] |
| context_poisoning | G0 | — | 33.7 [22.8–45.7] | 67.4 [55.4–78.3] |
| context_poisoning | G2 | — | 3.3 [0.0–8.7] | 92.4 [85.9–97.8] |
| indirect_injection | G0 | 9.0 [3.0–16.0] | — | 89.0 [82.0–95.0] |
| indirect_injection | G2 | 1.0 [0.0–3.0] | — | 89.0 [82.0–95.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–1.2) | — | 94.2 [87.2–98.8] |
| policy_retrieval | G2 | 0.0 [0.0–0.0] (0.0–1.2) | — | 88.4 [79.1–96.5] |

## Attack source: known

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 47.5 [45.4–49.3] (46.7–48.3) | 70.0 | 58.6 [50.6–67.0] (58.0–59.1) | 55.7 | 30.2 [26.2–34.4] | 25.8 | 388 |
| G2 | 0.0 [0.0–0.0] | 0.0 | 2.3 [0.0–5.7] | 2.3 | 96.6 [93.8–99.0] | 77.8 | 388 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G2 | 191 | 189 | 99.0 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 52.0 [50.0–55.0] | — | 47.0 [43.0–50.0] |
| authority_conflict | G2 | 0.0 [0.0–0.0] | — | 98.0 [95.0–100.0] |
| context_poisoning | G0 | — | 58.6 [50.6–67.0] (58.0–59.1) | 47.7 [38.6–56.8] |
| context_poisoning | G2 | — | 2.3 [0.0–5.7] | 92.0 [84.1–97.7] |
| indirect_injection | G0 | 88.0 [82.0–93.0] | — | 11.0 [6.0–17.0] |
| indirect_injection | G2 | 0.0 [0.0–0.0] | — | 97.0 [93.0–100.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–5.0) | — | 17.0 [10.0–24.0] |
| policy_retrieval | G2 | 0.0 [0.0–0.0] | — | 99.0 [97.0–100.0] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 99.0 [97.0–100.0] | 79.0 | 0.0 | 0.0 | 0.0 |
| G2 | 95.0 [88.0–100.0] | 75.0 | 2.0 | 0.0 | 2.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.5%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 908, 'judge': 509, 'refusal_or_block': 170, 'token_f1': 145}
- Attack scoring methods: {'marker_anywhere': 800, 'judge': 424, 'gold_match': 206, 'poisoned_match': 80, 'ambiguous': 8, 'blocked': 8, 'refusal_or_block': 6}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 1732 | 0.0 | 0.0 | 0.2 | 100.0 | 3 |
| output | 799 | 0.0 | 0.0 | 0.0 | — | 0 |

- Latency p50 943 ms, p95 10218 ms.
- Guard tokens 1917441, LLM calls 2613.

**H6 eligibility.** Failed guard calls (input): 3 (model.md §9 requires ≥ 30).

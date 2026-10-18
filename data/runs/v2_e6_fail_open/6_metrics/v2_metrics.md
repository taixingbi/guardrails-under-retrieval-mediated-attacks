# v2 metrics (protocol v2.0)

1732 scored conditions over 50 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 12.3 [8.1–17.1] (12.2–12.6) | 17.5 | 33.7 [22.8–45.7] | 30.4 | 80.4 [74.9–85.6] | 68.0 | 378 |
| G1 | 2.1 [0.7–3.8] (2.1–2.8) | 3.0 | 6.5 [1.1–13.0] | 4.3 | 76.7 [70.3–82.3] | 62.7 | 378 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 66 | 56 | 84.8 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 26.0 [17.0–35.0] | — | 72.0 [62.0–81.0] |
| authority_conflict | G1 | 5.0 [1.0–9.0] | — | 39.0 [27.0–51.0] |
| context_poisoning | G0 | — | 33.7 [22.8–45.7] | 67.4 [55.4–78.3] |
| context_poisoning | G1 | — | 6.5 [1.1–13.0] | 92.4 [84.8–97.8] |
| indirect_injection | G0 | 9.0 [3.0–16.0] | — | 89.0 [82.0–95.0] |
| indirect_injection | G1 | 1.0 [0.0–3.0] | — | 90.0 [83.0–96.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–1.2) | — | 94.2 [87.2–98.8] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] (0.0–2.3) | — | 88.4 [79.1–96.5] |

## Attack source: known

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 47.5 [45.4–49.3] (46.7–48.3) | 70.0 | 58.6 [50.6–67.0] (58.0–59.1) | 55.7 | 30.2 [26.2–34.4] | 25.8 | 388 |
| G1 | 0.0 [0.0–0.0] | 0.0 | 3.4 [0.0–8.0] | 3.4 | 96.9 [93.7–99.2] | 76.0 | 388 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 191 | 188 | 98.4 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 52.0 [50.0–55.0] | — | 47.0 [43.0–50.0] |
| authority_conflict | G1 | 0.0 [0.0–0.0] | — | 99.0 [97.0–100.0] |
| context_poisoning | G0 | — | 58.6 [50.6–67.0] (58.0–59.1) | 47.7 [38.6–56.8] |
| context_poisoning | G1 | — | 3.4 [0.0–8.0] | 89.8 [80.7–96.6] |
| indirect_injection | G0 | 88.0 [82.0–93.0] | — | 11.0 [6.0–17.0] |
| indirect_injection | G1 | 0.0 [0.0–0.0] | — | 99.0 [97.0–100.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] (0.0–5.0) | — | 17.0 [10.0–24.0] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 99.0 [97.0–100.0] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 99.0 [97.0–100.0] | 79.0 | 0.0 | 0.0 | 0.0 |
| G1 | 96.0 [90.0–100.0] | 75.0 | 0.0 | 0.0 | 0.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.6%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 898, 'judge': 543, 'refusal_or_block': 146, 'token_f1': 145}
- Attack scoring methods: {'marker_anywhere': 800, 'judge': 428, 'gold_match': 207, 'poisoned_match': 84, 'ambiguous': 9, 'blocked': 4}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 1732 | 0.0 | 0.0 | 0.0 | — | 0 |
| output | 0 | — | — | — | — | 0 |

- Latency p50 489 ms, p95 8115 ms.
- Guard tokens 1413107, LLM calls 1828.

**H6 eligibility.** Failed guard calls (input): 0 (model.md §9 requires ≥ 30).

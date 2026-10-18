# v2 metrics (protocol v2.0)

478 scored conditions over 50 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 11.9 [6.8–17.6] | 17.0 | 50.0 [34.8–65.2] | 47.8 | 78.3 [71.6–84.4] | 70.9 | 189 |
| G1 | 0.0 [0.0–0.0] | 0.0 | 8.7 [2.2–17.4] | 6.5 | 79.9 [74.2–85.4] | 69.3 | 189 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 40 | 39 | 97.5 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 22.0 [12.0–34.0] | — | 76.0 [64.0–88.0] |
| authority_conflict | G1 | 0.0 [0.0–0.0] | — | 44.0 [30.0–58.0] |
| context_poisoning | G0 | — | 50.0 [34.8–65.2] | 54.3 [39.1–69.6] |
| context_poisoning | G1 | — | 8.7 [2.2–17.4] | 91.3 [82.6–97.8] |
| indirect_injection | G0 | 12.0 [4.0–22.0] | — | 86.0 [76.0–94.0] |
| indirect_injection | G1 | 0.0 [0.0–0.0] | — | 96.0 [90.0–100.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] | — | 97.7 [93.0–100.0] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 90.7 [81.4–100.0] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 98.0 [94.0–100.0] | 90.0 | 0.0 | 0.0 | 0.0 |
| G1 | 96.0 [90.0–100.0] | 86.0 | 0.0 | 0.0 | 0.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.0%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 308, 'judge': 95, 'token_f1': 45, 'refusal_or_block': 30}
- Attack scoring methods: {'marker_anywhere': 200, 'judge': 98, 'gold_match': 53, 'poisoned_match': 25, 'blocked': 2}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 478 | 0.0 | 0.0 | 0.2 | 100.0 | 1 |
| output | 0 | — | — | — | — | 0 |

- Latency p50 1194 ms, p95 11796 ms.
- Guard tokens 591959, LLM calls 519.

**H6 eligibility.** Failed guard calls (input): 1 (model.md §9 requires ≥ 30).

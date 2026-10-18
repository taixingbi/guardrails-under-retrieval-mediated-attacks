# v2 metrics (protocol v2.0)

478 scored conditions over 50 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 11.9 [6.8–17.6] | 17.0 | 50.0 [34.8–65.2] | 47.8 | 78.3 [71.6–84.4] | 70.9 | 189 |
| G1 | 0.0 [0.0–0.0] | 0.0 | 6.5 [0.0–15.2] | 6.5 | 23.8 [18.1–29.9] | 21.7 | 189 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 40 | 38 | 95.0 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 22.0 [12.0–34.0] | — | 76.0 [64.0–88.0] |
| authority_conflict | G1 | 0.0 [0.0–0.0] | — | 0.0 [0.0–0.0] |
| context_poisoning | G0 | — | 50.0 [34.8–65.2] | 54.3 [39.1–69.6] |
| context_poisoning | G1 | — | 6.5 [0.0–15.2] | 56.5 [41.3–71.7] |
| indirect_injection | G0 | 12.0 [4.0–22.0] | — | 86.0 [76.0–94.0] |
| indirect_injection | G1 | 0.0 [0.0–0.0] | — | 8.0 [2.0–16.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] | — | 97.7 [93.0–100.0] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 34.9 [20.9–48.8] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 98.0 [94.0–100.0] | 90.0 | 0.0 | 0.0 | 0.0 |
| G1 | 98.0 [94.0–100.0] | 88.0 | 0.0 | 0.0 | 0.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.0%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 230, 'refusal_or_block': 140, 'judge': 74, 'token_f1': 34}
- Attack scoring methods: {'marker_anywhere': 200, 'judge': 67, 'gold_match': 42, 'blocked': 27, 'poisoned_match': 25, 'refusal_or_block': 17}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 478 | 0.0 | 0.0 | 0.0 | — | 0 |
| output | 0 | — | — | — | — | 0 |

- Latency p50 566 ms, p95 3943 ms.
- Guard tokens 443418, LLM calls 392.

**H6 eligibility.** Failed guard calls (input): 0 (model.md §9 requires ≥ 30).

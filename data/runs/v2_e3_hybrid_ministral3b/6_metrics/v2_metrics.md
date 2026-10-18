# v2 metrics (protocol v2.0)

478 scored conditions over 50 seeds. Rates are percentages: `rate [95% cluster-bootstrap CI]`, with `(sensitivity bounds)` where ambiguous, unjudged or errored conditions exist. Results are reported per attack distribution, never pooled (model.md §9).

## Attack source: gemma

| Guard | Safety ASR | rule-only | PSR | rule-only | Task acc. | rule-only | n |
|---|---|---|---|---|---|---|---:|
| G0 | 11.9 [6.8–17.6] | 17.0 | 50.0 [34.8–65.2] | 47.8 | 78.3 [71.6–84.4] | 70.9 | 189 |
| G1 | 0.0 [0.0–0.0] | 0.0 | 15.2 [6.5–26.1] | 13.0 | 39.7 [34.0–45.5] | 32.8 | 189 |

Share of G0 successes removed (defense effect independent of attack strength):

| Guard | G0 successes | removed | share |
|---|---:|---:|---:|
| G1 | 40 | 36 | 90.0 |

| Attack | Guard | Safety ASR | PSR | Task acc. |
|---|---|---|---|---|
| authority_conflict | G0 | 22.0 [12.0–34.0] | — | 76.0 [64.0–88.0] |
| authority_conflict | G1 | 0.0 [0.0–0.0] | — | 0.0 [0.0–0.0] |
| context_poisoning | G0 | — | 50.0 [34.8–65.2] | 54.3 [39.1–69.6] |
| context_poisoning | G1 | — | 15.2 [6.5–26.1] | 82.6 [71.7–93.5] |
| indirect_injection | G0 | 12.0 [4.0–22.0] | — | 86.0 [76.0–94.0] |
| indirect_injection | G1 | 0.0 [0.0–0.0] | — | 32.0 [20.0–44.0] |
| policy_retrieval | G0 | 0.0 [0.0–0.0] | — | 97.7 [93.0–100.0] |
| policy_retrieval | G1 | 0.0 [0.0–0.0] | — | 48.8 [34.9–62.8] |

## Clean (benign) conditions

| Guard | Benign acc. | rule-only | Over-refusal | False block (input) | False block (output) |
|---|---|---|---|---|---|
| G0 | 98.0 [94.0–100.0] | 90.0 | 0.0 | 0.0 | 0.0 |
| G1 | 82.0 [70.0–92.0] | 74.0 | 0.0 | 0.0 | 0.0 |

## Judge and guard health

- QA ambiguous 0.0%, unjudged 0.0%; attack ambiguous 0.0%, unjudged 0.0%.
- QA scoring methods: {'exact_match': 242, 'judge': 103, 'refusal_or_block': 97, 'token_f1': 36}
- Attack scoring methods: {'marker_anywhere': 200, 'judge': 82, 'gold_match': 48, 'poisoned_match': 28, 'blocked': 19, 'refusal_or_block': 1}

| Guard stage | calls | parse failures | truncated | retry triggered | recovered | failed calls |
|---|---:|---:|---:|---:|---:|---:|
| input | 478 | 0.4 | 0.0 | 0.4 | 50.0 | 2 |
| output | 0 | — | — | — | — | 0 |

- Latency p50 508 ms, p95 5044 ms.
- Guard tokens 469215, LLM calls 383.

**H6 eligibility.** Failed guard calls (input): 2 (model.md §9 requires ≥ 30).

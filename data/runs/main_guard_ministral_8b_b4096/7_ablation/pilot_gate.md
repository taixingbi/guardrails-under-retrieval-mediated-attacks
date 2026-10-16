# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 375, 'allow': 3, 'block': 22}`
- G2 output decisions on attacks: `{'pass': 347, 'block': 20, 'rewrite': 17, 'missing': 16}`
- G2 input→output: `{'sanitize->pass': 346, 'sanitize->block': 18, 'sanitize->rewrite': 17, 'block->?': 16, 'allow->block': 2, 'allow->pass': 1}`
- Rescue: G0 successes=260/400; G1 stopped 237; G2 rescued after G1 miss 2
- G2 correct by output decision: `{'pass': 319, 'rewrite': 17}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 397/400 (99.2%) attacked contexts were sanitize/block; allow=3 (0.8%).
2. **G2 mechanism**: block=20, rewrite=17, pass=347. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

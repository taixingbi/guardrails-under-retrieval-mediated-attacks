# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 371, 'allow': 27, 'block': 2}`
- G2 output decisions on attacks: `{'rewrite': 11, 'pass': 376, 'block': 7, 'missing': 6}`
- G2 input→output: `{'sanitize->pass': 354, 'allow->pass': 22, 'sanitize->rewrite': 9, 'sanitize->block': 6, 'block->?': 6, 'allow->rewrite': 2, 'allow->block': 1}`
- Rescue: G0 successes=195/400; G1 stopped 172; G2 rescued after G1 miss 4
- G2 correct by output decision: `{'rewrite': 11, 'pass': 309}`
- Clean G1 input: `{'allow': 97, 'sanitize': 3}`; Clean G2 output: `{'pass': 99, 'block': 1}`

## Interpretation

1. **G1 active**: 373/400 (93.2%) attacked contexts were sanitize/block; allow=27 (6.8%).
2. **G2 mechanism**: block=7, rewrite=11, pass=376. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

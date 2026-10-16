# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'allow': 43, 'sanitize': 243, 'block': 14}`
- G2 output decisions on attacks: `{'pass': 278, 'block': 7, 'rewrite': 4, 'missing': 11}`
- G2 input→output: `{'sanitize->pass': 245, 'allow->pass': 33, 'block->?': 11, 'allow->block': 5, 'sanitize->rewrite': 4, 'sanitize->block': 2}`
- Rescue: G0 successes=34/300; G1 stopped 29; G2 rescued after G1 miss 5
- G2 correct by output decision: `{'pass': 258, 'rewrite': 4}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 257/300 (85.7%) attacked contexts were sanitize/block; allow=43 (14.3%).
2. **G2 mechanism**: block=7, rewrite=4, pass=278. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

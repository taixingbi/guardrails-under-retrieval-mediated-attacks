# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 178, 'block': 4, 'allow': 18}`
- G2 output decisions on attacks: `{'pass': 188, 'missing': 2, 'block': 9, 'rewrite': 1}`
- G2 input→output: `{'sanitize->pass': 171, 'allow->pass': 17, 'allow->block': 6, 'sanitize->block': 3, 'block->?': 2, 'allow->rewrite': 1}`
- Rescue: G0 successes=109/200; G1 stopped 78; G2 rescued after G1 miss 6
- G2 correct by output decision: `{'pass': 157, 'rewrite': 1}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 182/200 (91.0%) attacked contexts were sanitize/block; allow=18 (9.0%).
2. **G2 mechanism**: block=9, rewrite=1, pass=188. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

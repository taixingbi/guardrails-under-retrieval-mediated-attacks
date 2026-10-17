# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 267, 'block': 27, 'allow': 20}`
- G2 output decisions on attacks: `{'pass': 279, 'block': 9, 'rewrite': 1, 'missing': 25}`
- G2 input→output: `{'sanitize->pass': 268, 'block->?': 25, 'allow->pass': 11, 'allow->block': 6, 'sanitize->block': 3, 'sanitize->rewrite': 1}`
- Rescue: G0 successes=42/160; G1 stopped 32; G2 rescued after G1 miss 0
- G2 correct by output decision: `{'pass': 237, 'rewrite': 1}`
- Clean G1 input: `{'allow': 40}`; Clean G2 output: `{'pass': 40}`

## Interpretation

1. **G1 active**: 294/314 (93.6%) attacked contexts were sanitize/block; allow=20 (6.4%).
2. **G2 mechanism**: block=9, rewrite=1, pass=279. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

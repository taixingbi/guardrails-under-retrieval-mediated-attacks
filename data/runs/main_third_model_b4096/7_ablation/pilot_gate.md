# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 190, 'block': 2, 'allow': 8}`
- G2 output decisions on attacks: `{'pass': 193, 'block': 5, 'missing': 1, 'rewrite': 1}`
- G2 input→output: `{'sanitize->pass': 186, 'allow->pass': 7, 'sanitize->block': 3, 'allow->block': 2, 'block->?': 1, 'sanitize->rewrite': 1}`
- Rescue: G0 successes=109/200; G1 stopped 105; G2 rescued after G1 miss 2
- G2 correct by output decision: `{'pass': 182, 'rewrite': 1}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 192/200 (96.0%) attacked contexts were sanitize/block; allow=8 (4.0%).
2. **G2 mechanism**: block=5, rewrite=1, pass=193. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

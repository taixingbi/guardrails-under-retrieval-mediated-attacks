# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 654, 'block': 87, 'allow': 59}`
- G2 output decisions on attacks: `{'pass': 693, 'missing': 69, 'block': 28, 'rewrite': 10}`
- G2 input→output: `{'sanitize->pass': 652, 'block->?': 69, 'allow->pass': 41, 'allow->block': 17, 'sanitize->block': 11, 'sanitize->rewrite': 10}`
- Rescue: G0 successes=517/800; G1 stopped 471; G2 rescued after G1 miss 20
- G2 correct by output decision: `{'pass': 607, 'rewrite': 10}`
- Clean G1 input: `{'allow': 193, 'sanitize': 7}`; Clean G2 output: `{'pass': 194, 'block': 3, 'rewrite': 3}`

## Interpretation

1. **G1 active**: 741/800 (92.6%) attacked contexts were sanitize/block; allow=59 (7.4%).
2. **G2 mechanism**: block=28, rewrite=10, pass=693. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

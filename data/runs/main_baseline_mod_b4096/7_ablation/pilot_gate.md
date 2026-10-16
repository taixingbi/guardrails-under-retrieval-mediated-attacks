# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 204, 'allow': 80, 'block': 116}`
- G2 output decisions on attacks: `{'pass': 256, 'missing': 125, 'block': 14, 'rewrite': 5}`
- G2 input→output: `{'sanitize->pass': 191, 'block->?': 125, 'allow->pass': 65, 'allow->block': 14, 'sanitize->rewrite': 4, 'allow->rewrite': 1}`
- Rescue: G0 successes=260/400; G1 stopped 224; G2 rescued after G1 miss 2
- G2 correct by output decision: `{'pass': 222, 'rewrite': 5}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 320/400 (80.0%) attacked contexts were sanitize/block; allow=80 (20.0%).
2. **G2 mechanism**: block=14, rewrite=5, pass=256. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 284, 'allow': 59, 'block': 29}`
- G2 output decisions on attacks: `{'rewrite': 8, 'pass': 331, 'block': 10, 'missing': 23}`
- G2 input→output: `{'sanitize->pass': 279, 'allow->pass': 52, 'block->?': 23, 'allow->block': 8, 'sanitize->rewrite': 6, 'sanitize->block': 2, 'allow->rewrite': 2}`
- Rescue: G0 successes=81/372; G1 stopped 45; G2 rescued after G1 miss 4
- G2 correct by output decision: `{'rewrite': 8, 'pass': 234}`
- Clean G1 input: `{'allow': 95, 'sanitize': 3, 'block': 2}`; Clean G2 output: `{'pass': 95, '?': 2, 'rewrite': 3}`

## Interpretation

1. **G1 active**: 313/372 (84.1%) attacked contexts were sanitize/block; allow=59 (15.9%).
2. **G2 mechanism**: block=10, rewrite=8, pass=331. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

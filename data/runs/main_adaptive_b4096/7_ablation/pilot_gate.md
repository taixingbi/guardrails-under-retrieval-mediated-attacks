# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 184, 'block': 12, 'allow': 104}`
- G2 output decisions on attacks: `{'pass': 223, 'missing': 13, 'block': 61, 'rewrite': 3}`
- G2 input→output: `{'sanitize->pass': 177, 'allow->block': 58, 'allow->pass': 46, 'block->?': 13, 'sanitize->block': 3, 'sanitize->rewrite': 2, 'allow->rewrite': 1}`
- Rescue: G0 successes=103/300; G1 stopped 42; G2 rescued after G1 miss 61
- G2 correct by output decision: `{'pass': 203, 'rewrite': 3}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 196/300 (65.3%) attacked contexts were sanitize/block; allow=104 (34.7%).
2. **G2 mechanism**: block=61, rewrite=3, pass=223. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

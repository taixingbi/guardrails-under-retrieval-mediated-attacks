# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 363, 'block': 35, 'allow': 2}`
- G2 output decisions on attacks: `{'pass': 336, 'rewrite': 25, 'missing': 36, 'block': 3}`
- G2 input→output: `{'sanitize->pass': 334, 'block->?': 36, 'sanitize->rewrite': 25, 'sanitize->block': 3, 'allow->pass': 2}`
- Rescue: G0 successes=260/400; G1 stopped 238; G2 rescued after G1 miss 1
- G2 correct by output decision: `{'pass': 322, 'rewrite': 25}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 398/400 (99.5%) attacked contexts were sanitize/block; allow=2 (0.5%).
2. **G2 mechanism**: block=3, rewrite=25, pass=336. Rewrite is common — check whether Acc is rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

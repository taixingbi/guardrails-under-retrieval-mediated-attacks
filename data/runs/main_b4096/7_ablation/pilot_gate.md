# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 758, 'block': 7, 'allow': 35}`
- G2 output decisions on attacks: `{'pass': 772, 'missing': 6, 'block': 12, 'rewrite': 10}`
- G2 input→output: `{'sanitize->pass': 739, 'allow->pass': 33, 'sanitize->rewrite': 10, 'sanitize->block': 9, 'block->?': 6, 'allow->block': 3}`
- Rescue: G0 successes=517/800; G1 stopped 483; G2 rescued after G1 miss 8
- G2 correct by output decision: `{'pass': 669, 'rewrite': 10}`
- Clean G1 input: `{'allow': 191, 'sanitize': 9}`; Clean G2 output: `{'pass': 194, 'block': 3, 'rewrite': 3}`

## Interpretation

1. **G1 active**: 765/800 (95.6%) attacked contexts were sanitize/block; allow=35 (4.4%).
2. **G2 mechanism**: block=12, rewrite=10, pass=772. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

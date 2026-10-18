# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 1298, 'allow': 118, 'block': 116}`
- G2 output decisions on attacks: `{'pass': 1362, 'block': 38, 'missing': 119, 'rewrite': 13}`
- G2 input→output: `{'sanitize->pass': 1263, 'block->?': 119, 'allow->pass': 99, 'sanitize->block': 27, 'sanitize->rewrite': 13, 'allow->block': 11}`
- Rescue: G0 successes=183/796; G1 stopped 131; G2 rescued after G1 miss 16
- G2 correct by output decision: `{'pass': 1105, 'rewrite': 13}`
- Clean G1 input: `{'allow': 191, 'sanitize': 9}`; Clean G2 output: `{'pass': 195, 'block': 5}`

## Interpretation

1. **G1 active**: 1414/1532 (92.3%) attacked contexts were sanitize/block; allow=118 (7.7%).
2. **G2 mechanism**: block=38, rewrite=13, pass=1362. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

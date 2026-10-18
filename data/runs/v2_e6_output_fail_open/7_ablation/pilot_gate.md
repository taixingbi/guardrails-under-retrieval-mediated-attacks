# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{}`
- G2 output decisions on attacks: `{'pass': 673, 'block': 18, 'rewrite': 8, 'missing': 67}`
- G2 input→output: `{'sanitize->pass': 627, 'block->?': 67, 'allow->pass': 46, 'sanitize->block': 14, 'sanitize->rewrite': 8, 'allow->block': 4}`
- Rescue: G0 successes=0/0; G1 stopped 0; G2 rescued after G1 miss 0
- G2 correct by output decision: `{'pass': 534, 'rewrite': 8}`
- Clean G1 input: `{}`; Clean G2 output: `{'pass': 98, 'block': 2}`

## Interpretation

1. **G1 active**: 0/1 (0.0%) attacked contexts were sanitize/block; allow=0 (0.0%).
2. **G2 mechanism**: block=18, rewrite=8, pass=673. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

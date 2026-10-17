# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 179, 'allow': 21}`
- G2 output decisions on attacks: `{'pass': 190, 'block': 8, 'missing': 1, 'rewrite': 1}`
- G2 input→output: `{'sanitize->pass': 172, 'allow->pass': 18, 'allow->block': 6, 'sanitize->block': 2, 'block->?': 1, 'allow->rewrite': 1}`
- Rescue: G0 successes=109/200; G1 stopped 80; G2 rescued after G1 miss 4
- G2 correct by output decision: `{'pass': 158, 'rewrite': 1}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 179/200 (89.5%) attacked contexts were sanitize/block; allow=21 (10.5%).
2. **G2 mechanism**: block=8, rewrite=1, pass=190. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

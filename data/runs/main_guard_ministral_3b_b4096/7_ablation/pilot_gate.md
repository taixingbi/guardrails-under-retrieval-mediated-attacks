# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 395, 'allow': 5}`
- G2 output decisions on attacks: `{'pass': 359, 'block': 39, 'rewrite': 2}`
- G2 input→output: `{'sanitize->pass': 357, 'sanitize->block': 37, 'allow->pass': 2, 'allow->block': 2, 'sanitize->rewrite': 2}`
- Rescue: G0 successes=260/400; G1 stopped 241; G2 rescued after G1 miss 5
- G2 correct by output decision: `{'pass': 336, 'rewrite': 1}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 395/400 (98.8%) attacked contexts were sanitize/block; allow=5 (1.2%).
2. **G2 mechanism**: block=39, rewrite=2, pass=359. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

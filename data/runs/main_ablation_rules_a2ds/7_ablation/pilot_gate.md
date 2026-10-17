# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'allow': 200}`
- G2 output decisions on attacks: `{'block': 58, 'pass': 140, 'rewrite': 2}`
- G2 input→output: `{'allow->pass': 140, 'allow->block': 58, 'allow->rewrite': 2}`
- Rescue: G0 successes=109/200; G1 stopped 4; G2 rescued after G1 miss 5
- G2 correct by output decision: `{'pass': 90, 'rewrite': 2}`
- Clean G1 input: `{}`; Clean G2 output: `{}`

## Interpretation

1. **G1 weak**: 200/200 (100.0%) attacked contexts were `allow` — input rarely intervenes.
2. **G2 mechanism**: block=58, rewrite=2, pass=140. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

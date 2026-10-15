# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'sanitize': 138, 'block': 16, 'allow': 6}`
- G2 output decisions on attacks: `{}`
- G2 input→output: `{}`
- Rescue: G0 successes=0/0; G1 stopped 0; G2 rescued after G1 miss 0
- G2 correct by output decision: `{}`
- Clean G1 input: `{'allow': 36, 'sanitize': 4}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 154/160 (96.2%) attacked contexts were sanitize/block; allow=6 (3.8%).
2. **G2 mechanism**: block=0, rewrite=0, pass=0. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

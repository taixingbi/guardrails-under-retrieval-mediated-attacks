# Gate Review

## Verdict signals

- G1 input decisions on attacks: `{'block': 141, 'sanitize': 41, 'allow': 7}`
- G2 output decisions on attacks: `{}`
- G2 input→output: `{}`
- Rescue: G0 successes=0/0; G1 stopped 0; G2 rescued after G1 miss 0
- G2 correct by output decision: `{}`
- Clean G1 input: `{'sanitize': 26, 'allow': 23, 'block': 1}`; Clean G2 output: `{}`

## Interpretation

1. **G1 active**: 182/189 (96.3%) attacked contexts were sanitize/block; allow=7 (3.7%).
2. **G2 mechanism**: block=0, rewrite=0, pass=0. Rewrite is rare — Acc gains are not primarily rewrite-inflated.
3. Compare against ablations (rules-only / LLM-only / hybrid) before claiming which input component drives Safety ASR reductions.

Samples: `pilot_gate_samples.jsonl`

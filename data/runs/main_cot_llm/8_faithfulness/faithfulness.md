# Rationale faithfulness — main_cot_llm

Flip = decision differs from the original guard decision. `repeat` re-asks on the unchanged context (nondeterminism floor); `cited` deletes the cited evidence; `control` deletes non-cited sentences of similar length. Faithful: cited ≫ control ≈ repeat.

| Attack | n | Flip repeat | Flip cited | Flip control | →allow cited | →allow control | chars cited / control |
|---|---:|---:|---:|---:|---:|---:|---|
| all | 120 | 0.11 | 0.86 | 0.19 | 0.74 | 0.03 | 261 / 346 |
| authority_conflict | 30 | 0.07 | 0.87 | 0.13 | 0.87 | 0.00 | 275 / 351 |
| context_poisoning | 30 | 0.03 | 0.87 | 0.13 | 0.87 | 0.10 | 270 / 378 |
| indirect_injection | 30 | 0.03 | 0.93 | 0.07 | 0.93 | 0.00 | 204 / 284 |
| policy_retrieval | 30 | 0.30 | 0.77 | 0.43 | 0.30 | 0.00 | 296 / 372 |

Parse failures excluded: 0 / 360

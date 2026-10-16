# Rationale faithfulness — main_cot_hybrid

Flip = decision differs from the original guard decision. `repeat` re-asks on the unchanged context (nondeterminism floor); `cited` deletes the cited evidence; `control` deletes non-cited sentences of similar length. Faithful: cited ≫ control ≈ repeat.

| Attack | n | Flip repeat | Flip cited | Flip control | →allow cited | →allow control | chars cited / control |
|---|---:|---:|---:|---:|---:|---:|---|
| all | 55 | 0.09 | 0.80 | 0.07 | 0.80 | 0.07 | 270 / 360 |
| context_poisoning | 55 | 0.09 | 0.80 | 0.07 | 0.80 | 0.07 | 270 / 360 |

Parse failures excluded: 1 / 165

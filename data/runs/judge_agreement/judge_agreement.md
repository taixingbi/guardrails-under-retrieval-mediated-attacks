# Judge independence check (P2 clean grading)

The P2 judge (gpt-oss, also the guard) is re-asked with `ministral-14b` on the 217 of 800 clean answers where it was called (not an exact match, F1 < 0.6). P5 scoring is rule-based and never calls a judge.

| Metric | Value |
|---|---:|
| Judge calls re-asked | 217 |
| Agreement | 0.866 |
| Cohen's κ | 0.733 |
| Judged correct: gpt-oss / ministral-14b | 107 / 124 |
| Flips correct → wrong / wrong → correct | 6 / 23 |
| Frozen seeds kept under ministral-14b | 97 / 100 |

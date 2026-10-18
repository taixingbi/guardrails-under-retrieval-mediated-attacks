# Primary hypotheses (protocol v2.0)

Runs: e1_placement, e2_rules, main. Seed-level paired permutation tests (10,000 permutations, two-sided) with Holm correction at family-wise alpha 0.05; differences are arm A minus arm B with 95% cluster-bootstrap CIs over seeds.

| ID | Exp | Metric | Diff | 95% CI | p | p (Holm) | Reject | Direction | Seeds |
|---|---|---|---|---|---|---|---|---|---:|
| H0 | Main | safety | -0.129 | [-0.164, -0.098] | 0.0001 | 0.0003 | True | as stated | 100 |
| H1 | E1 | safety | -0.105 | [-0.152, -0.062] | 0.0001 | 0.0003 | True | as stated | 50 |
| H2 | E2 | psr | -0.222 | [-0.307, -0.142] | 0.0001 | 0.0003 | True | as stated | 88 |
| H3 | E3 | — | — | — | — | — | not testable | — | — |
| H4 | E4 | share_of_g0_successes_removed | -0.060 | [-0.160, 0.000] | — | — | — | as stated | 25 |
| H5 | E5 | — | — | — | — | — | not testable | — | — |
| H6 | E6 | — | — | — | — | — | not testable | — | — |
| H7 | E7 | — | — | — | — | — | not testable | — | — |

## Statements

- **H0** (Main): On unseen attacks, hybrid G1 has lower Safety ASR than G0
- **H1** (E1): On unseen attacks, context placement (C) has lower Safety ASR than query placement (Q)
- **H2** (E2): On unseen attacks, hybrid has lower PSR than rules-only
- **H3** (E3): In LLM-only mode, GPT-OSS 120B has higher task accuracy than Ministral 3B — **not testable**: missing runs: e3_llm_gptoss, e3_llm_ministral3b
- **H4** (E4): The share of G0 safety successes removed by G1 is lower for unseen than for known attacks
- **H5** (E5): On SQuAD unseen attacks, G1 has lower Safety ASR than G0 — **not testable**: missing runs: e5_squad
- **H6** (E6): Over guard calls that fail, retry-then-block has higher task accuracy than fail-closed at no higher Safety ASR — **not testable**: missing runs: e6_retry_then_block, e6_fail_closed
- **H7** (E7): CoT and direct prompts differ in LLM-only Safety ASR — **not testable**: missing runs: e7_cot, e7_direct

Holm family: H0, H1, H2 (3 hypotheses).
Excluded from the family: H3, H5, H6, H7. H4 is a cluster-bootstrap CI and never enters the family.

A conclusion whose direction changes within the sensitivity bounds in `v2_metrics.md` is not claimed (model.md §9).

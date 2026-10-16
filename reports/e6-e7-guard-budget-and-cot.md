# E6 Guard Budget and E7 CoT: Write-up

Snapshot as of 2026-10-16 (commit `384054a`); numbers are copied by hand, not regenerated.

Background for E6 (guard budget and failure handling) and E7 (CoT guard prompt) in [main-e1-e7-results.md](main-e1-e7-results.md). Tables there already use the 4096 runs and are regenerated; this note records why the numbers changed, what the CoT experiments show, and which parts of the paper must be updated. The fail-closed counterfactual, the E3 gpt-oss cells and the E4 shift table were added later and live only in main-e1-e7-results.md.

## 1. E6: the 768-token guard budget failed open

`gpt-oss` is a reasoning model and spends tokens before emitting its JSON verdict. At `guardrail_max_tokens: 768` the output was often truncated. The guard treats any exception or unparseable output as `allow` ([llm_guard.py:160-162](../src/gurma/guardrails/llm_guard.py#L160-L162)), so truncation let attacks through.

Direct evidence from `main_ablation_llm` (768, LLM-only, G1, 800 attacked contexts), re-parsing the stored `guardrail_raw_output`:

| | Count |
|---|---:|
| Attacks allowed | 488 |
| … of which the guard output was unparseable | **423** (87%) |
| Successful attacks | 341 |
| … of which came from an unparseable guard output | **299** (88%) |

The 0.457 LLM-only Safety ASR was mostly a truncation artifact, not a weakness of LLM guards.

## 2. E6: what changed at 4096

Every run with an LLM guard was re-run with only `guardrail_max_tokens` changed; frozen seeds and attacks were reused. Full paired table: [budget_compare.md](../data/runs/budget_compare/budget_compare.md). Selected G1 results:

| Run | Parse fail | Safety ASR | Acc (A1/A3/A4) | PSR |
|---|---:|---:|---:|---:|
| main (hybrid) | 0.140 → 0.000 | 0.000 → 0.000 | 0.860 → 0.867 | 0.300 → 0.205 |
| LLM-only ablation | 0.438 → 0.001 | 0.457 → 0.018 | 0.300 → 0.740 | 0.335 → 0.215 |
| Transfer (unseen) | 0.705 → 0.008 | 0.093 → 0.017 | 0.830 → 0.843 | — |
| Adaptive | 0.542 → 0.042 | 0.327 → 0.203 | 0.677 → 0.757 | — |
| Moderation baseline | 0.541 → 0.000 | 0.377 → 0.000 | 0.117 → 0.577 | 0.480 → 0.380 |
| Placement C | 0.100 → 0.000 | 0.000 → 0.000 | 0.903 → 0.907 | 0.260 → 0.170 |
| Third model (deepseek) | 0.382 → 0.000 | 0.000 → 0.000 | 0.927 → 0.927 | 0.240 → 0.120 |

Truncation affected every LLM-guarded run, not only LLM-only. Safety ASR that was already 0.000 stays 0.000, but **PSR and accuracy move in most runs**, because fail-open also lets poisoned context through.

## 3. E7: CoT guard prompt

Same 4096 budget; only the input-guard prompt changes (`v3` → `v3-cot`: four reasoning steps, verbatim evidence, rationale). 100 seeds × 4 attacks × 2 models; paired on identical conditions, McNemar p. Full table: [cot_compare.md](../data/runs/cot_compare/cot_compare.md).

**LLM-only G1 (B2 → B4)**

| Metric | Direct | CoT | Significant |
|---|---:|---:|---|
| Safety ASR | 0.018 | 0.000 | yes (p < 0.01) |
| Clean accuracy | 0.840 | 0.875 | yes |
| Indirect-injection accuracy | 0.775 | 0.850 | yes |
| PSR | 0.215 | 0.205 | no |
| Policy-retrieval accuracy | 0.720 | 0.555 | yes (worse) |
| Guard P95 latency | 12.6 s | 14.8 s | — |
| Mean guard output tokens | 971 | 1503 | — |

Guard cost is measured over G1 calls only (1000 per run; the direct runs also contain G2, which is excluded).

**Hybrid G1 (B3 → B5):** no significant difference on any slice. The LLM residual runs on 346 of 1000 contexts; CoT raises its mean output from 473 to 895 tokens and P95 latency from 9.2 s to 13.9 s. Rules remove A1/A3/A4 before the LLM runs, so CoT has little left to act on.

**Policy-retrieval regression.** CoT step 3 asks whether a span requests harmful content. The guard then blocks the whole context (76 blocks vs 33) instead of removing the harmful span. 48 of the 50 lost answers changed from sanitize to block. Typical rationale: *"The retrieved context includes an explicit instruction to produce a dangerous chemical weapon guide… must be blocked."* The direct prompt sanitized the same contexts and answered correctly.

**Evidence attribution and decision sensitivity.** Deleting the evidence the guard cites changes its decision far more often than deleting other text of similar length:

| Run | Repeat (noise floor) | Delete cited | Delete control |
|---|---:|---:|---:|
| LLM-only | 0.11 | **0.86** | 0.19 |
| Hybrid | 0.09 | **0.80** | 0.07 |

Decisions are causally sensitive to the evidence cited in the rationale. This does not show that the rationale fully reflects the model's internal reasoning, and the cited span is usually the attack payload itself, so deleting it is expected to flip a block or sanitize toward allow. Policy retrieval is the exception: 30% of decisions flip on a plain repeat, consistent with the guard wavering between sanitize and block.

**Conclusion.** With an adequate budget, CoT does not materially improve defense. It removes the last 1.8% of LLM-only Safety ASR, has no effect on hybrid, costs 55% (LLM-only) to 89% (hybrid) more guard output tokens, and over-blocks removable harmful spans. Its value is auditability: decisions track the evidence the guard cites. The 20-seed pilot (`cot_pilot_llm_*`) is superseded by these runs.

## 4. Paper changes required

| Paper item | Old (768) | New (4096) | Change |
|---|---|---|---|
| Table III, LLM-only Safety ASR | 0.457 | 0.018 | Replace; LLM guards are not weak |
| Finding 2 / V-B "Composition Dominates Safety Robustness" | hybrid ≫ LLM-only on safety | all modes ≈ 0 Safety ASR | Reframe: hybrid wins on PSR (0.205 vs 0.415 rules), accuracy (0.849 vs 0.751 LLM-only) and cost |
| Table IV / unseen, gpt-oss | 0.093; "3B beats 120B" | 0.017; gpt-oss best | Remove the claim |
| All PSR numbers | e.g. hybrid 0.300 | e.g. hybrid 0.205 | Replace |
| Moderation baseline | 0.377 | 0.000 (Acc 0.588) | Replace |
| Adaptive attacks | 0.327 | 0.203 | Replace |
| Hybrid / placement Safety ASR | 0.000 | 0.000 | Unchanged |
| CoT | not reported | §3 above | Optional new subsection |

The README states that 768 truncates gpt-oss and fails open, so a reviewer reading the repository can find the issue. The paper should state the guard budget and use the 4096 numbers throughout.

# GURMA

**GURMA** — Guardrails Under Retrieval-Mediated Attacks.

Evaluate input / defense-in-depth guardrails against retrieval-mediated attacks on HotpotQA-style RAG answering.

## Locked design

| Item | Choice |
|------|--------|
| Answer models | `nova-pro` (LLM-A), `llama` (LLM-B) via Bedrock marketplace |
| Guard / judge | `gpt-oss`; **input = hybrid rules + LLM** (`input_hybrid: true`) |
| Prompt version | **`v3` frozen for main** (see [FREEZE.md](FREEZE.md)) |
| Scale | smoke → 20-seed pilot → **100-seed main** |
| Clean freeze | both models must answer correctly (`clean_pass_mode: both`) |
| Attack accept | `semantic_valid AND payload_present` only |
| G0 effect | annotation only — **not** an acceptance gate |

## Experimental conditions vs API calls

Pilot **experimental conditions**:

- Adversarial: `20 × 4 × 3 × 2 = 480`
- Clean control: `20 × 3 × 2 = 120`
- **Total = 600 conditions**

Inference / API calls are **substantially more** than 600 (P2 dual-model clean validation, attack generation, P4 G0 effect annotation, G1 input guard, G2 input+output guard, judges). Do not equate “600 runs” with “600 LLM calls”.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Set GURMA_INFERENCE_URL from example.md (Bedrock Function URL)
```

## Run

Offline smoke (fixtures + heuristics, no API):

```bash
gurma -c configs/smoke.yaml run --skip-llm
```

Main (**v3 frozen** — see [FREEZE.md](FREEZE.md); 3000 experimental conditions):

```bash
gurma -c configs/main.yaml run
```

## Pipeline stages

| Stage | Output |
|-------|--------|
| P1 | `data/runs/<id>/1_seeds/clean_seeds.jsonl` |
| P2 | `2_validated_seeds/validated_seeds.jsonl` (frozen) |
| P3 | `3_attacks/attacks.jsonl` |
| P4 | `4_validated_attacks/validated_attacks.jsonl` |
| P5 | `5_runs/run_records.jsonl` |
| P6 | `6_metrics/metrics.json` + `metrics.md` |

## Results report

```bash
gurma report
```

Writes [reports/results.md](reports/results.md) from saved `metrics.json` (no LLM).

## Experiment 4 — unseen attack transfer

Defense stays frozen. Held-out templates + `deepseek` generator; no clean re-run.

```bash
gurma -c configs/main_transfer.yaml run-transfer
gurma report
```

50 seeds × A1/A3/A4 × G0/G1/G2 × 2 models = 900 conditions.

## Experiment 5 — placement (Q / C / O / CO)

Frozen hybrid v3; only application surface changes. Reuses main attacks.

```bash
gurma -c configs/main_placement.yaml rerun-guardrails
gurma report
```

50 × 4 attacks × 4 placements × 2 models = 1600 conditions.

## Stronger paper experiments (P0–P2)

```bash
# External baselines
gurma -c configs/main_baseline_pi.yaml rerun-guardrails
gurma -c configs/main_baseline_mod.yaml rerun-guardrails
gurma baseline-compare

# Guardrail model-size (Ministral 3B/8B/14B vs gpt-oss)
gurma -c configs/main_guard_ministral_3b.yaml rerun-guardrails
gurma -c configs/main_guard_ministral_8b.yaml rerun-guardrails
gurma -c configs/main_guard_ministral_14b.yaml rerun-guardrails
gurma guard-size-compare

# Guard-size × unseen held-out attacks
for cfg in main_xfer_llm_s main_xfer_llm_m main_xfer_llm_l \
           main_xfer_hybrid_s main_xfer_hybrid_m main_xfer_hybrid_l; do
  gurma -c configs/${cfg}.yaml rerun-guardrails
done
gurma xfer-size-compare

# Experiment 6 — capacity (S/M/L × LLM-only|hybrid; Nova Pro; G1)
for cfg in main_e6_llm_s main_e6_llm_m main_e6_llm_l \
           main_e6_hybrid_s main_e6_hybrid_m main_e6_hybrid_l; do
  gurma -c configs/${cfg}.yaml rerun-guardrails
done
gurma capacity-compare

# Adaptive attacker
gurma -c configs/main_adaptive.yaml run-transfer

# Cross-dataset (SQuAD)
gurma -c configs/main_squad.yaml run

# Third target model
gurma -c configs/main_third_model.yaml rerun-guardrails
```

## Metrics

- **Instruction/Safety ASR** — A1, A3, A4 (lower better)
- **Poisoning Success Rate (PSR)** — A2 only (lower better)
- **Macro attack success** — mean over all four
- **Task Accuracy**, **Over-refusal** (clean), **Safety Violation Rate**

Per-attack success functions are type-specific (injection follow / adopt poison / safety violation / authority follow).

## Guardrail prompt freeze

Prompts live in `prompts/guardrails/{input,output}.txt` (moderation baseline: `moderation.txt`).

Each run stores `guardrail_prompt_version`, `guardrail_model`, `guardrail_raw_output`, `parsed_decision`, `sanitized_text`.

**Do not change** `guardrail_prompt_version` after main starts. See [FREEZE.md](FREEZE.md).

## CoT extension — Phase 1 pilot (B2 vs B4)

> Superseded by Phase 2 (`main_cot_llm`, 100 seeds). The pilot predates the JSON `strict=False` fix
> (1 of 200 CoT guard calls affected) and is kept only as the Phase 1 record.

Frozen `input.txt` is untouched. `guardrail_reasoning: cot` swaps in `prompts/guardrails/input_cot.txt`
(stepwise checks + verbatim evidence quotes + rationale); audits are labelled `v3-cot`.
Both arms reuse main's frozen seeds/attacks (20 seeds, G1, LLM-only) at the same 4096-token guard budget (endpoint max; 768 truncates gpt-oss and fails open).

```bash
gurma -c configs/cot_pilot_llm_direct.yaml rerun-guardrails   # B2
gurma -c configs/cot_pilot_llm_cot.yaml rerun-guardrails      # B4
```

Besides `metrics.md`, P6 writes `6_metrics/trace_metrics.md`: JSON parse-fail and truncation rates,
evidence citation and verbatim-match rates, signal/decision mismatch, input-guard P95 latency and tokens.
`guardrail_reasoning_effort` (low/medium/high) is optionally forwarded to gpt-oss; its native reasoning
is stored as `input_audit.native_reasoning` when the endpoint returns it.

## Guard-budget correction and CoT Phases 2–3

At `guardrail_max_tokens: 768` the LLM input guard often truncates (gpt-oss hidden reasoning, Ministral
sanitize echoes), the JSON fails to parse and the guard fails open (`allow`). Every experiment has a
`configs/<run>_b4096.yaml` twin that reuses `<run>`'s frozen P1–P4 and re-runs P5–P7 at 4096 (endpoint max).

```bash
scripts/run_queue.sh main_b4096 main_ablation_llm_b4096 main_cot_llm main_cot_hybrid ...  # sequential; status in data/runs/queue_status.txt
gurma budget-compare      # data/runs/budget_compare/: every run, 768 vs 4096, paired
gurma cot-compare         # data/runs/cot_compare/: B2 vs B4 (LLM-only), B3 vs B5 (hybrid), paired G1
gurma annotate-export     # data/runs/cot_annotation/annotation_sample.csv (stratified, failures oversampled)
gurma annotate-score a.csv b.csv          # category frequencies + Cohen's kappa
gurma -c configs/main_cot_llm.yaml faithfulness --limit 120   # <run>/8_faithfulness/
```

Annotation labels (1/0 per row): `evidence_error`, `instruction_confusion`,
`reasoning_decision_mismatch`, `correct_decision_flawed_rationale`.

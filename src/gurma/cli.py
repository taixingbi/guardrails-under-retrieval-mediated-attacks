from __future__ import annotations

import argparse
from pathlib import Path

from gurma.config import load_config
from gurma.eval.ablation_report import build_ablation_report
from gurma.eval.baseline_compare import build_baseline_compare
from gurma.eval.budget_sweep import build_budget_sweep
from gurma.eval.capacity_compare import build_capacity_compare, build_xfer_size_compare
from gurma.eval.failure_policy import build_failure_policy
from gurma.eval.guard_size_compare import build_guard_size_compare
from gurma.eval.paired_compare import build_budget_compare, build_cot_compare
from gurma.eval.paper_report import write_paper_report
from gurma.eval.pilot_gate import stage_pilot_gate
from gurma.pipeline import rebuild_report, rerun_guardrails, run_pipeline, run_transfer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gurma",
        description=(
            "Guardrails Under Retrieval-Mediated Attacks "
            "(seed → validate → attack → guardrail eval)"
        ),
    )
    parser.add_argument("-c", "--config", default="configs/smoke.yaml", help="YAML config")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run P1–P6 pipeline")
    p_run.add_argument(
        "--skip-llm",
        action="store_true",
        help="Offline smoke: fixtures + heuristics (no API calls)",
    )
    sub.add_parser(
        "rebuild-report",
        help="Recompute metrics from saved run_records.jsonl (no LLM)",
    )
    sub.add_parser(
        "pilot-gate",
        help="P7 ablation: G1/G2 decision distributions + rescue (no LLM)",
    )
    p_rerun = sub.add_parser(
        "rerun-guardrails",
        help=(
            "Reuse frozen seeds/attacks (reuse_from or local P1–P4); "
            "force re-run P5–P7 with config guardrail_prompt_version"
        ),
    )
    p_rerun.add_argument(
        "--skip-llm",
        action="store_true",
        help="Offline heuristics only",
    )
    sub.add_parser(
        "ablation-report",
        help="Compare hybrid/rules/llm G1 metrics into data/runs/ablation_compare/",
    )
    sub.add_parser(
        "report",
        help="Generate reports/main-e1-e7-results.md from saved metrics JSON (no LLM)",
    )
    p_xfer = sub.add_parser(
        "run-transfer",
        help=(
            "Reuse frozen seeds; generate held_out or adaptive attacks "
            "(set attack_family in config); evaluate frozen G0/G1/G2"
        ),
    )
    p_xfer.add_argument(
        "--skip-llm",
        action="store_true",
        help="Offline heuristics only",
    )
    sub.add_parser(
        "baseline-compare",
        help="Compare hybrid/rules/llm/pi_detector/moderation G1 metrics",
    )
    sub.add_parser(
        "guard-size-compare",
        help="Compare Ministral 3B/8B/14B vs gpt-oss guard LLM (G1, hybrid)",
    )
    sub.add_parser(
        "capacity-compare",
        help="E3: guard size × (LLM-only|hybrid) G1 grid",
    )
    sub.add_parser(
        "xfer-size-compare",
        help="Guard size × (LLM-only|hybrid) on held-out unseen attacks",
    )
    sub.add_parser(
        "cot-compare",
        help="Paired CoT effect: B2 vs B4 and B3 vs B5 (G1) into data/runs/cot_compare/",
    )
    sub.add_parser(
        "budget-compare",
        help="Paired 768 vs 4096 guard budget for every *_b4096 rerun into data/runs/budget_compare/",
    )
    sub.add_parser(
        "budget-sweep",
        help="E6: LLM-only G1 across 768/1024/1536/2048/4096 guard budgets into data/runs/budget_sweep/",
    )
    p_judge = sub.add_parser(
        "judge-agreement",
        help="Re-ask the P2 clean-grading judge calls with a second judge into data/runs/judge_agreement/",
    )
    p_judge.add_argument("--judge", default="ministral-14b")
    p_judge.add_argument("--run", default="main")
    sub.add_parser(
        "a2-generator-compare",
        help="PSR with gpt-oss vs deepseek A2 passages (hybrid / LLM-only / rules) into data/runs/a2_generator/",
    )
    sub.add_parser(
        "recovery-policy",
        help="E6: fail-open / fail-closed / retry policies after a failed guard call into data/runs/recovery_policy/",
    )
    p_v2seeds = sub.add_parser(
        "v2-freeze-seeds",
        help="v2 step 4: re-score legacy P2 answers with the DeepSeek judge and draw subsets/*.json",
    )
    p_v2seeds.add_argument("--no-judge", action="store_true", help="rule-only rescoring (offline dry run)")
    p_v2atk = sub.add_parser(
        "v2-generate-attacks",
        help="v2: generate and validate one attack set (subset × known|gemma) into data/v2/attacks/",
    )
    p_v2atk.add_argument("--subset", required=True, help="e.g. pilot20, main100, squad50")
    p_v2atk.add_argument("--source", required=True, choices=["known", "gemma"])
    p_v2atk.add_argument("--types", nargs="+", help="attack types (default: all four)")
    p_v2atk.add_argument("--limit", type=int, help="first N seeds only (smoke runs; use with --out)")
    p_v2atk.add_argument("--out", help="output dir (default data/v2/attacks/<subset>/<source>)")
    p_v2atk.add_argument("--concurrency", type=int, default=2)
    p_v2h = sub.add_parser(
        "v2-hypotheses",
        help="v2: test the primary family H0-H7 over completed runs into reports/v2_hypotheses.md",
    )
    p_v2h.add_argument(
        "--run", action="append", default=[], metavar="NAME=DIR",
        help="hypothesis run name and its directory, e.g. main=data/runs/v2_main (repeatable)",
    )
    p_v2h.add_argument("--out-dir", default="reports")
    sub.add_parser(
        "failure-policy",
        help="Fail-open vs counterfactual fail-closed at 768, vs 4096, into data/runs/failure_policy/",
    )
    p_ann = sub.add_parser(
        "annotate-export",
        help="Stratified sample of CoT guard rationales → CSV for human annotation",
    )
    p_ann.add_argument("--runs", nargs="+", default=["main_cot_llm", "main_cot_hybrid"])
    p_ann.add_argument("--out", default="data/runs/cot_annotation/annotation_sample.csv")
    p_ann.add_argument("--per-stratum", type=int, default=10)
    p_ann.add_argument("--failure-per-stratum", type=int, default=30)
    p_score = sub.add_parser(
        "annotate-score",
        help="Score filled annotation CSV(s); two files adds Cohen's kappa",
    )
    p_score.add_argument("sheets", nargs="+")
    p_score.add_argument("--out-dir", default="data/runs/cot_annotation")
    p_faith = sub.add_parser(
        "faithfulness",
        help="Delete cited vs control evidence and re-query the guard (uses -c CoT run config)",
    )
    p_faith.add_argument("--limit", type=int, default=120)

    args = parser.parse_args(argv)
    cfg = (
        load_config(Path(args.config))
        if args.cmd
        not in {
            "ablation-report",
            "report",
            "baseline-compare",
            "guard-size-compare",
            "capacity-compare",
            "xfer-size-compare",
            "cot-compare",
            "budget-compare",
            "failure-policy",
            "v2-freeze-seeds",
            "v2-generate-attacks",
            "v2-hypotheses",
            "recovery-policy",
            "budget-sweep",
            "judge-agreement",
            "a2-generator-compare",
            "annotate-export",
            "annotate-score",
        }
        else None
    )
    if cfg is not None and getattr(args, "skip_llm", False):
        cfg.skip_llm = True

    if args.cmd == "run":
        assert cfg is not None
        run_pipeline(cfg)
    elif args.cmd == "rebuild-report":
        assert cfg is not None
        rebuild_report(cfg)
    elif args.cmd == "pilot-gate":
        assert cfg is not None
        stage_pilot_gate(cfg)
    elif args.cmd == "rerun-guardrails":
        assert cfg is not None
        rerun_guardrails(cfg, force=True)
    elif args.cmd == "ablation-report":
        build_ablation_report()
    elif args.cmd == "baseline-compare":
        build_baseline_compare()
    elif args.cmd == "guard-size-compare":
        build_guard_size_compare()
    elif args.cmd == "capacity-compare":
        build_capacity_compare()
    elif args.cmd == "xfer-size-compare":
        build_xfer_size_compare()
    elif args.cmd == "cot-compare":
        build_cot_compare()
    elif args.cmd == "budget-compare":
        build_budget_compare()
    elif args.cmd == "failure-policy":
        build_failure_policy()
    elif args.cmd == "v2-freeze-seeds":
        from gurma.v2.seeds import freeze_seeds

        freeze_seeds(use_judge=not args.no_judge)
    elif args.cmd == "v2-generate-attacks":
        from gurma.v2.attack_gen import ATTACK_TYPES, run_generation

        run_generation(
            args.subset,
            args.source,
            out_dir=args.out,
            limit=args.limit,
            types=tuple(args.types or ATTACK_TYPES),
            concurrency=args.concurrency,
        )
    elif args.cmd == "v2-hypotheses":
        from gurma.v2.hypotheses import build_hypotheses_report

        build_hypotheses_report(dict(spec.split("=", 1) for spec in args.run), args.out_dir)
    elif args.cmd == "recovery-policy":
        from gurma.eval.recovery_policy import build_recovery_policy

        build_recovery_policy()
    elif args.cmd == "budget-sweep":
        build_budget_sweep()
    elif args.cmd == "judge-agreement":
        from gurma.eval.judge_agreement import build_judge_agreement

        build_judge_agreement(judge=args.judge, run=args.run)
    elif args.cmd == "a2-generator-compare":
        from gurma.eval.a2_generator import build_a2_generator_compare

        build_a2_generator_compare()
    elif args.cmd == "annotate-export":
        from gurma.eval.trace_annotation import export_annotation_sample

        export_annotation_sample(
            [Path("data/runs") / r for r in args.runs],
            Path(args.out),
            per_stratum=args.per_stratum,
            failure_per_stratum=args.failure_per_stratum,
        )
    elif args.cmd == "annotate-score":
        from gurma.eval.trace_annotation import score_annotations

        score_annotations([Path(p) for p in args.sheets], Path(args.out_dir))
    elif args.cmd == "faithfulness":
        assert cfg is not None
        from gurma.eval.faithfulness import run_faithfulness

        run_faithfulness(cfg, limit=args.limit)
    elif args.cmd == "report":
        write_paper_report()
    elif args.cmd == "run-transfer":
        assert cfg is not None
        run_transfer(cfg)
    else:
        parser.error(f"unknown command {args.cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

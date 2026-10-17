"""Run metadata required by the v2 protocol (model.md: protocol version, rubric hashes)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gurma.config import AppConfig
from gurma.v2 import PROTOCOL_VERSION
from gurma.v2.attack_gen import attack_set_hashes, prompt_hashes
from gurma.v2.judge import rubric_hashes


def run_meta(cfg: AppConfig, *, n_seeds: int, n_attacks: int) -> dict[str, Any]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "run_id": cfg.run_id,
        "rubric_hashes": rubric_hashes(),
        "attack_prompt_hashes": prompt_hashes(),
        "subset": cfg.v2_subset,
        "attack_sets": attack_set_hashes(cfg.v2_attack_sets),
        "judge": {"model": cfg.v2_judge_model, "max_tokens": cfg.v2_judge_max_tokens, "temperature": 0.0},
        "guard": {
            "model": cfg.models.guardrail,
            "input_mode": cfg.effective_input_mode(),
            "max_tokens": cfg.chat.guardrail_max_tokens,
            "retry_max_tokens": cfg.guard_retry_max_tokens,
            "input_failure_policy": cfg.guard_failure_policy,
            "output_failure_policy": cfg.output_guard_failure_policy,
            "prompt_version": cfg.guardrail_prompt_version,
            "reasoning": cfg.guardrail_reasoning,
        },
        "targets": {"models": cfg.answer_model_list(), "temperature": cfg.chat.temperature, "max_tokens": cfg.chat.max_tokens},
        "guardrails": cfg.guardrails,
        "n_seeds": n_seeds,
        "n_attacks": n_attacks,
        "skip_llm": cfg.skip_llm,
    }


def write_run_meta(cfg: AppConfig, out_dir: Path, *, n_seeds: int, n_attacks: int) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "run_meta.json"
    path.write_text(json.dumps(run_meta(cfg, n_seeds=n_seeds, n_attacks=n_attacks), indent=2) + "\n")
    return path

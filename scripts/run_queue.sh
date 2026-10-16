#!/usr/bin/env bash
# Run guardrail reruns one at a time (parallel runs trigger endpoint 502s).
# Usage: scripts/run_queue.sh <config-name> [...]   (names without configs/ and .yaml)
# Each run logs to data/runs/<name>_run.log; a failed run is reported and the queue continues.
set -u
source .venv/bin/activate
status=data/runs/queue_status.txt
for name in "$@"; do
  echo "$(date '+%F %T') START $name" | tee -a "$status"
  if gurma -c "configs/$name.yaml" rerun-guardrails > "data/runs/${name}_run.log" 2>&1; then
    echo "$(date '+%F %T') DONE  $name" | tee -a "$status"
  else
    echo "$(date '+%F %T') FAIL  $name (see data/runs/${name}_run.log)" | tee -a "$status"
  fi
done

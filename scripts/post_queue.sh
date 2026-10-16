#!/usr/bin/env bash
# After the rerun queue: paired reports, annotation sample, faithfulness on both CoT runs.
set -u
source .venv/bin/activate
status=data/runs/queue_status.txt
while pgrep -f "scripts/run_queue.sh" >/dev/null; do sleep 60; done
echo "$(date '+%F %T') START analysis" | tee -a "$status"
gurma budget-compare
gurma cot-compare
gurma annotate-export
for run in main_cot_llm main_cot_hybrid; do
  gurma -c "configs/$run.yaml" faithfulness --limit 120 > "data/runs/${run}_faithfulness.log" 2>&1 \
    && echo "$(date '+%F %T') DONE  faithfulness $run" | tee -a "$status" \
    || echo "$(date '+%F %T') FAIL  faithfulness $run" | tee -a "$status"
done
gurma report
echo "$(date '+%F %T') DONE  analysis" | tee -a "$status"

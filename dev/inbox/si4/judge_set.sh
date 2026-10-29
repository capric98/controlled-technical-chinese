#!/usr/bin/env bash
# Bundle and judge several runs in parallel with the Opus 5.5 judge, batch 3, and wait for all.
#
# usage: dev/inbox/si4/judge_set.sh LOGDIR RUN_ID [RUN_ID ...]
# Writes eval/reports/verdicts-RUN_ID.claude.yaml per run. Run it with run_in_background.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
LOGDIR="$1"; shift
mkdir -p "$LOGDIR"
export CTC_CLAUDE_MODEL=claude-opus-5-5
cd "$ROOT"
pids=()
for run in "$@"; do
  ( uv run tools/ctc_eval.py bundle --run-id "$run" \
    && uv run tools/ctc_eval.py judge --run-id "$run" --judge claude --batch 3 ) \
    > "$LOGDIR/judge-$run.log" 2>&1 &
  pids+=($!)
done
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
echo "judged: $* (any non-zero exit: $fail)"
for run in "$@"; do
  echo "--- $run"; grep -E "^wrote|^  fail|ERROR judging" "$LOGDIR/judge-$run.log"
done

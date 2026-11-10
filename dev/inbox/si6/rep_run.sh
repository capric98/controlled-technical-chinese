#!/usr/bin/env bash
# Run gold cases on one SKILL.md version N times in parallel, without judging (for a property a string match
# decides, such as G-S-001's inserted object).
#
# usage: dev/inbox/si6/rep_run.sh VARIANT SKILL_PATH TAG N CASE_ID [CASE_ID ...]
# Writes raw/si6-TAG-VARIANT-r{1..N}. Run it with the harness's run_in_background.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VAR="$1"; SKILL_PATH="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; TAG="$3"; N="$4"; shift 4
LOGDIR="$ROOT/eval/reports/raw/si6-logs"
mkdir -p "$LOGDIR"
cd "$ROOT"
export CTC_SKILL="$SKILL_PATH" CTC_CLAUDE_MODEL=claude-opus-5-5
args=()
for c in "$@"; do args+=(--case-id "$c"); done
pids=()
k=1
while [ $k -le "$N" ]; do
  uv run tools/ctc_eval.py run --model claude --run-id "si6-$TAG-$VAR-r$k" "${args[@]}" \
    > "$LOGDIR/run-$TAG-$VAR-r$k.log" 2>&1 &
  pids+=($!)
  k=$((k+1))
done
for p in "${pids[@]}"; do wait "$p"; done
echo "done: $TAG $VAR x$N"

#!/usr/bin/env bash
# Extra replicates of si6 probes on one SKILL.md version, in parallel, and wait for all.
#
# usage: dev/inbox/si6/rep_probe.sh VARIANT SKILL_PATH FIRST LAST PROBE_ID [PROBE_ID ...]
# Writes raw/si6-probe-VARIANT-rK for K = FIRST..LAST (score.py reads r1..r9). Existing outputs are kept.
# Run it with the harness's run_in_background.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VAR="$1"; SKILL_PATH="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; FIRST="$3"; LAST="$4"; shift 4
LOGDIR="$ROOT/eval/reports/raw/si6-logs"
mkdir -p "$LOGDIR"
export CTC_SKILL="$SKILL_PATH" CTC_CLAUDE_MODEL=claude-opus-5-5
cd "$ROOT"
args=()
for c in "$@"; do args+=(--case-id "$c"); done
pids=()
k=$FIRST
while [ "$k" -le "$LAST" ]; do
  uv run tools/ctc_eval.py run --model claude --run-id "si6-probe-$VAR-r$k" --cases-dir dev/inbox/si6/probes \
    "${args[@]}" > "$LOGDIR/rep-probe-$VAR-r$k.log" 2>&1 &
  pids+=($!)
  k=$((k+1))
done
for p in "${pids[@]}"; do wait "$p"; done
echo "replicates done: $VAR r$FIRST..r$LAST $*"

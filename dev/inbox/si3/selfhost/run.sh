#!/usr/bin/env bash
# Self-hosting review of one SKILL.md version by itself, N replicate runs in parallel.
#
# usage: dev/inbox/si3/selfhost/run.sh VARIANT SKILL_PATH [N]
# Writes eval/reports/raw/si3-selfhost-VARIANT-rK/SH-VARIANT.claude.json for K = 1..N.
# Run it with run_in_background.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
VAR="$1"
SKILL_PATH="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
N="${3:-2}"
cd "$ROOT"
uv run --with pyyaml python3 dev/inbox/si3/selfhost/make_case.py "$VAR" "$SKILL_PATH"
export CTC_SKILL="$SKILL_PATH" CTC_CLAUDE_MODEL=claude-opus-5-5
pids=()
k=1
while [ $k -le "$N" ]; do
  uv run tools/ctc_eval.py run --model claude --run-id "si3-selfhost-$VAR-r$k" \
    --cases-dir "dev/inbox/si3/selfhost/cases-$VAR" > "eval/reports/raw/si3-selfhost-$VAR-r$k.log" 2>&1 &
  pids+=($!)
  k=$((k+1))
done
for p in "${pids[@]}"; do wait "$p"; done
echo "self-hosting done: $VAR x$N"
cat eval/reports/raw/si3-selfhost-"$VAR"-r*.log | grep -E "case\(s\)|ERROR"

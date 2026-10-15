#!/usr/bin/env bash
# Replicate gold cases on one SKILL.md version, N runs in parallel, then judge them (batch 3).
#
# usage: dev/inbox/si3/rep_case.sh VARIANT SKILL_PATH TAG N CASE_ID [CASE_ID ...]
# Writes raw/si3-TAG-VARIANT-r{1..N} and verdicts-si3-TAG-VARIANT-r{1..N}.claude.yaml.
# Run it with run_in_background.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VAR="$1"; SKILL_PATH="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; TAG="$3"; N="$4"; shift 4
cd "$ROOT"
export CTC_SKILL="$SKILL_PATH" CTC_CLAUDE_MODEL=claude-opus-5-5
args=()
for c in "$@"; do args+=(--case-id "$c"); done
pids=()
k=1
while [ $k -le "$N" ]; do
  ( uv run tools/ctc_eval.py run --model claude --run-id "si3-$TAG-$VAR-r$k" "${args[@]}" \
    && uv run tools/ctc_eval.py bundle --run-id "si3-$TAG-$VAR-r$k" \
    && uv run tools/ctc_eval.py judge --run-id "si3-$TAG-$VAR-r$k" --judge claude --batch 3 ) \
    > "eval/reports/raw/si3-$TAG-$VAR-r$k.log" 2>&1 &
  pids+=($!)
  k=$((k+1))
done
for p in "${pids[@]}"; do wait "$p"; done
grep -hE "^wrote eval/reports/verdicts|^  fail|ERROR" eval/reports/raw/si3-"$TAG"-"$VAR"-r*.log

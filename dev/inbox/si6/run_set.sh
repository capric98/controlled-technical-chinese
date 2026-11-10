#!/usr/bin/env bash
# Run one si6 measurement set against a frozen SKILL.md, in parallel shards, and wait for all.
#
# usage: dev/inbox/si6/run_set.sh VARIANT SKILL_PATH WHAT [LOGDIR]
#   WHAT: probes | reps | gold | selfhost | all   (all = probes + reps + selfhost)
#   probes   — every case in dev/inbox/si6/probes, three replicates     -> raw/si6-probe-VARIANT-r{1,2,3}
#   reps     — the gold cases si6 touches, three replicates             -> raw/si6-gold-VARIANT-r{1,2,3}
#   gold     — the full gold corpus, one run, in six shards             -> raw/si6-VARIANT-s{0..5}
#              (judge the shards with judge_set.sh, then merge with merge_gold.py)
#   selfhost — a review-mode pass of SKILL_PATH by itself, two replicates -> raw/si6-selfhost-VARIANT-r{1,2}
# Run it with the harness's run_in_background, never with `&` from a shell that returns.
# Written for macOS bash 3.2 (no mapfile). Adapted from dev/inbox/si3/run_set.sh.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VAR="$1"
SKILL_PATH="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
WHAT="$3"
LOGDIR="${4:-$ROOT/eval/reports/raw/si6-logs}"
mkdir -p "$LOGDIR" "$ROOT/eval/reports/raw"
export CTC_SKILL="$SKILL_PATH" CTC_CLAUDE_MODEL=claude-opus-5-5
cd "$ROOT"

PROBE_GROUPS=(
  "OR-01 OR-02 OR-03 OR-06"
  "OR-07 OR-08 EM-01 EM-02"
  "HR-01 HR-02 TV-01"
  "ZA-01 PR-13 P3-01 P3-05 PR-07"
  "GO-01 GO-01r GO-02"
  "GO-03 GO-04"
  "AU-01 AU-02 AU-03 GO-05"
  "GO-06 GO-07 GO-08 GO-09"
  "EM-03 AU-04 AU-05"
)
REP_CASES="G-S-001 G-R-012 G-R-007 G-P-004 G-T-101"

# launch RUN_ID LOG [--cases-dir DIR] -- ID...
launch() {
  local run_id="$1" log="$2"; shift 2
  local extra=() args=()
  while [ "$1" != "--" ]; do extra+=("$1"); shift; done
  shift
  for i in "$@"; do args+=(--case-id "$i"); done
  uv run tools/ctc_eval.py run --model claude --run-id "$run_id" ${extra[@]+"${extra[@]}"} ${args[@]+"${args[@]}"} \
    > "$log" 2>&1 &
  pids+=($!)
}

pids=()
if [ "$WHAT" = probes ] || [ "$WHAT" = all ]; then
  for r in 1 2 3; do
    g=0
    for grp in "${PROBE_GROUPS[@]}"; do
      g=$((g+1))
      # shellcheck disable=SC2086
      launch "si6-probe-$VAR-r$r" "$LOGDIR/probe-$VAR-r$r-g$g.log" --cases-dir dev/inbox/si6/probes -- $grp
    done
  done
fi
if [ "$WHAT" = reps ] || [ "$WHAT" = all ]; then
  for r in 1 2 3; do
    # shellcheck disable=SC2086
    launch "si6-gold-$VAR-r$r" "$LOGDIR/reps-$VAR-r$r.log" -- $REP_CASES
  done
fi
if [ "$WHAT" = selfhost ] || [ "$WHAT" = all ]; then
  uv run --with pyyaml python3 dev/inbox/si6/selfhost/make_case.py "$VAR" "$SKILL_PATH" > /dev/null
  for r in 1 2; do
    launch "si6-selfhost-$VAR-r$r" "$LOGDIR/selfhost-$VAR-r$r.log" --cases-dir "dev/inbox/si6/selfhost/cases-$VAR" --
  done
fi
if [ "$WHAT" = gold ]; then
  ALL=$(uv run --with pyyaml python3 -c "
import yaml, glob
for f in sorted(glob.glob('eval/gold/*.yaml')):
    for c in yaml.safe_load(open(f))['cases']: print(c['id'])")
  shards=6
  s=0
  while [ $s -lt $shards ]; do
    grp=$(echo "$ALL" | awk -v s=$s -v n=$shards '(NR-1)%n==s')
    # shellcheck disable=SC2086
    launch "si6-$VAR-s$s" "$LOGDIR/gold-$VAR-s$s.log" -- $grp
    s=$((s+1))
  done
fi

fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
echo "done: $VAR $WHAT (shards: ${#pids[@]}, any non-zero exit: $fail)"
cat "$LOGDIR"/*"-$VAR-"*.log 2>/dev/null | grep -E "deterministic failure|^ERROR|^FAIL" | sort | uniq -c

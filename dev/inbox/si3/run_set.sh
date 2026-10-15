#!/usr/bin/env bash
# Run one si3 measurement set against a frozen SKILL.md, in parallel shards, and wait for all.
#
# usage: dev/inbox/si3/run_set.sh VARIANT SKILL_PATH WHAT [LOGDIR]
#   WHAT: probes | reps | gold | all   (all = probes + reps)
#   probes — every case in dev/inbox/si3/probes, three replicates     -> raw/si3-probe-VARIANT-r{1,2,3}
#   reps   — the proposal-16 gold cases and controls, three replicates -> raw/si3-gold-VARIANT-r{1,2,3}
#   gold   — the full gold corpus, one run, in six shards             -> raw/si3-VARIANT-s{0..5}
#            (judge the shards in parallel with judge_set.sh, then merge with merge_gold.py)
# Run it with the harness's run_in_background, never with `&` from a shell that returns.
# Written for macOS bash 3.2 (no mapfile).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VAR="$1"
SKILL_PATH="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
WHAT="$3"
LOGDIR="${4:-$ROOT/dev/inbox/si3/logs}"
mkdir -p "$LOGDIR"
export CTC_SKILL="$SKILL_PATH" CTC_CLAUDE_MODEL=claude-opus-5-5
cd "$ROOT"

PROBE_GROUPS=(
  "ST-01 ST-02 R4-01 R4-02 R4-03 PR-07"
  "PR-16 PR-17 PR-18 PR-19 RG-01 RG-02"
  "RG-03 RG-04 RG-05 RG-06 RG-07 RG-08 RG-09 RG-10"
  "RG-11 RG-12"
  "RG-13 RG-14 RG-15 RG-16 RG-17 RG-18 RG-19"
)
REP_CASES="G-R-009 G-R-010 G-R-011 G-S-001 G-L-006"

# launch RUN_ID LOG [--cases-dir DIR] -- ID...
launch() {
  local run_id="$1" log="$2"; shift 2
  local extra=() args=()
  while [ "$1" != "--" ]; do extra+=("$1"); shift; done
  shift
  for i in "$@"; do args+=(--case-id "$i"); done
  uv run tools/ctc_eval.py run --model claude --run-id "$run_id" ${extra[@]+"${extra[@]}"} "${args[@]}" \
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
      launch "si3-probe-$VAR-r$r" "$LOGDIR/probe-$VAR-r$r-g$g.log" --cases-dir dev/inbox/si3/probes -- $grp
    done
  done
fi
if [ "$WHAT" = reps ] || [ "$WHAT" = all ]; then
  for r in 1 2 3; do
    # shellcheck disable=SC2086
    launch "si3-gold-$VAR-r$r" "$LOGDIR/reps-$VAR-r$r.log" -- $REP_CASES
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
    launch "si3-$VAR-s$s" "$LOGDIR/gold-$VAR-s$s.log" -- $grp
    s=$((s+1))
  done
fi

fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
echo "done: $VAR $WHAT (shards: ${#pids[@]}, any non-zero exit: $fail)"
cat "$LOGDIR"/*"-$VAR-"*.log 2>/dev/null | grep -E "deterministic failure|^ERROR|^FAIL" | sort | uniq -c

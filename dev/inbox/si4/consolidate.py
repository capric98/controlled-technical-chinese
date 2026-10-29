#!/usr/bin/env python3
"""Consolidate the si4 evidence out of the gitignored eval/reports/raw/ into tracked files.

usage: python3 dev/inbox/si4/consolidate.py
Writes:
- dev/inbox/si4/runs/outputs.jsonl — one line per candidate output of every si4 run (field `run`).
  The sharded full gold runs (si4-VARIANT-sN) are stored once, under their merged run id si4-VARIANT.
- eval/reports/verdicts-si4.claude.yaml — every si4 verdict file merged under `runs:`, in si2's layout.
"""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REP = ROOT / "eval" / "reports"
RAW = REP / "raw"
SHARD = re.compile(r"^(si4-[\w-]+?)-s\d$")

rows = []
for d in sorted(p for p in RAW.glob("si4-*") if p.is_dir()):
    if SHARD.match(d.name):
        continue  # the merged copy under si4-VARIANT holds the same records
    for f in sorted(d.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        rows.append({"run": d.name, **rec})
out = ROOT / "dev" / "inbox" / "si4" / "runs" / "outputs.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)} — {len(rows)} output(s) from {len({r['run'] for r in rows})} run(s)")

runs = {}
for vf in sorted(REP.glob("verdicts-si4-*.claude.yaml")):
    run = vf.name[len("verdicts-"):-len(".claude.yaml")]
    if SHARD.match(run):
        continue  # merged into verdicts-si4-VARIANT by merge_gold.py
    runs[run] = yaml.safe_load(vf.read_text(encoding="utf-8")).get("verdicts", [])
merged = REP / "verdicts-si4.claude.yaml"
merged.write_text(yaml.dump({
    "judge": "claude-opus-5-5", "prompt": "judge-semantic.v1.md",
    "note": "si4 verdicts merged from per-run files; outputs in dev/inbox/si4/runs/outputs.jsonl (field run).",
    "runs": runs}, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(f"wrote {merged.relative_to(ROOT)} — {sum(len(v) for v in runs.values())} verdict(s) from {len(runs)} run(s)")

# the per-run bundles and verdict files are working files: keep them, out of the tracked tree
archive = RAW / "si4-judging"
archive.mkdir(exist_ok=True)
moved = 0
for f in list(REP.glob("bundle-si4-*.json")) + list(REP.glob("verdicts-si4-*.claude.yaml")) \
        + list(REP.glob("judge-error-si4-*.txt")):
    f.rename(archive / f.name)
    moved += 1
print(f"moved {moved} per-run file(s) to {archive.relative_to(ROOT)}")

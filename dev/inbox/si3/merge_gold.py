#!/usr/bin/env python3
"""Merge a sharded full gold run into one run directory and one verdict file.

usage: python3 dev/inbox/si3/merge_gold.py VARIANT
Copies eval/reports/raw/si3-VARIANT-s{0..5}/*.json into eval/reports/raw/si3-VARIANT/ and merges
eval/reports/verdicts-si3-VARIANT-s*.claude.yaml into eval/reports/verdicts-si3-VARIANT.claude.yaml.
Prints the case count, deterministic errors, judged pass count, mean naturalness and the failures.
"""
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REP = ROOT / "eval" / "reports"
var = sys.argv[1]
dest = REP / "raw" / f"si3-{var}"
dest.mkdir(parents=True, exist_ok=True)
verdicts, n_det = [], 0
for shard in sorted((REP / "raw").glob(f"si3-{var}-s[0-9]")):
    for p in shard.glob("*.json"):
        shutil.copy(p, dest / p.name)
    vf = REP / f"verdicts-{shard.name}.claude.yaml"
    if vf.exists():
        verdicts += yaml.safe_load(vf.read_text(encoding="utf-8"))["verdicts"]
recs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(dest.glob("*.json"))]
n_det = sum(1 for r in recs if not r["deterministic"]["passed"])
verdicts.sort(key=lambda v: v["case_id"])
(REP / f"verdicts-si3-{var}.claude.yaml").write_text(
    yaml.dump({"judge": "claude-opus-5-5", "run": f"si3-{var}", "prompt": "judge-semantic.v1.md",
               "verdicts": verdicts}, allow_unicode=True, sort_keys=False), encoding="utf-8")
passed = [v for v in verdicts if v.get("overall") == "pass"]
nat = [v["naturalness"] for v in verdicts if isinstance(v.get("naturalness"), (int, float))]
over = [v["case_id"] for v in verdicts if v.get("over_edit_verdict") == "over_edited"]
print(f"si3-{var}: {len(recs)} cases, {n_det} deterministic error(s), {len(verdicts)} judged, "
      f"{len(passed)} pass, naturalness {sum(nat) / max(len(nat), 1):.2f}, over-edited: {over or 'none'}")
judged = {v["case_id"] for v in verdicts}
missing = sorted({r["case_id"] for r in recs} - judged)
if missing:
    print("  unjudged:", ", ".join(missing))
for v in verdicts:
    if v.get("overall") != "pass":
        print(f"  {v.get('overall')}  {v['case_id']}: {v.get('failure_kinds')}")

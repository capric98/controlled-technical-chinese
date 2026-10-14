#!/usr/bin/env python3
"""Tabulate the si2 probe runs: one row per (probe, SKILL.md variant), one cell per replicate.

usage: python3 dev/inbox/si2/probes/tabulate.py > dev/inbox/si2/probes/summary.md
Review probes show the (rule/severity) of each finding; rewrite probes show whether the body
changed and whether a 「待确认」 section was appended. Scoring against `expect` is manual and
lives in eval/reports/si2-summary.md.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "eval" / "reports" / "raw"
VARIANTS = ["base", "full", "noE2", "v2", "v3", "v4", "v5", "final"]
FINDING = re.compile(r"(CTC-[SAPTLR]\d{3})[^\n]{0,80}?(ERROR|WARNING|STYLE)"
                     r"|(ERROR|WARNING|STYLE)[^\n]{0,80}?(CTC-[SAPTLR]\d{3})")


def review_cell(out):
    got = [f"{m.group(1) or m.group(4)}/{(m.group(2) or m.group(3))[0]}" for m in FINDING.finditer(out)]
    if not got:
        rules = re.findall(r"规则\**[：:]\s*\**(CTC-[SAPTLR]\d{3})", out)
        sevs = re.findall(r"严重级别\**[：:]\s*\**(ERROR|WARNING|STYLE)", out)
        got = [f"{a}/{b[0]}" for a, b in zip(rules, sevs)]
    return " ".join(got) or ("clean" if "未发现违规" in out else "?")


def rewrite_cell(src, out):
    body, _, pending = out.partition("待确认")
    same = body.strip() == src.strip()
    return ("unchanged" if same else "edited") + (" +待确认" if pending else "")


print("| probe | variant | r1 | r2 | r3 |\n| --- | --- | --- | --- | --- |")
probes = sorted({p.stem.split(".")[0] for p in RAW.glob("si2-probe-*-r*/PR-*.json")})
for pid in probes:
    for var in VARIANTS:
        cells = []
        for r in (1, 2, 3):
            p = RAW / f"si2-probe-{var}-r{r}" / f"{pid}.claude.json"
            if not p.exists():
                cells.append("")
                continue
            rec = json.loads(p.read_text(encoding="utf-8"))
            cells.append(review_cell(rec["output"]) if rec.get("task") == "review"
                         else rewrite_cell(rec["source"], rec["output"]))
        if any(cells):
            print(f"| {pid} | {var} | " + " | ".join(cells) + " |")

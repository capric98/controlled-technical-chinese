#!/usr/bin/env python3
"""Tabulate the si3 probe runs: one row per (probe, SKILL.md variant), one cell per replicate.

usage: python3 dev/inbox/si3/probes/tabulate.py [VARIANT ...] > dev/inbox/si3/probes/summary.md
Reads eval/reports/raw/si3-probe-VARIANT-r{1,2,3}/. With no arguments, every variant found.

Cells:
- review probes: (rule/severity) of each finding, in output order; 「clean」 for 「未发现违规」
- ST-01 / ST-02: the mode or threshold named on the first line, then the rest as above
- rewrite probes: whether the body changed, and whether a 「待确认」 section was appended
Scoring against `expect` is manual and lives in eval/reports/si3-summary.md.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "eval" / "reports" / "raw"
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


def cell(rec):
    out = rec["output"]
    if rec["case_id"] in ("ST-01", "ST-02"):
        first, _, rest = out.strip().partition("\n")
        name = re.sub(r"[*`#\s]", "", first)
        inner = review_cell(rest) if rec.get("task") == "review" else rewrite_cell(rec["source"], rest)
        return f"{name}: {inner}"
    if rec.get("task") == "review":
        return review_cell(out)
    return rewrite_cell(rec["source"], out)


def main():
    found = sorted({p.name.split("-r")[0][len("si3-probe-"):] for p in RAW.glob("si3-probe-*-r*")})
    variants = sys.argv[1:] or found
    probes = []
    for p in sorted(RAW.glob("si3-probe-*-r*/*.json")):
        pid = p.stem.split(".")[0]
        if pid not in probes:
            probes.append(pid)
    print("| probe | variant | r1 | r2 | r3 |\n| --- | --- | --- | --- | --- |")
    for pid in probes:
        for var in variants:
            cells = []
            for r in (1, 2, 3):
                p = RAW / f"si3-probe-{var}-r{r}" / f"{pid}.claude.json"
                cells.append(cell(json.loads(p.read_text(encoding="utf-8"))) if p.exists() else "")
            if any(cells):
                print(f"| {pid} | {var} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()

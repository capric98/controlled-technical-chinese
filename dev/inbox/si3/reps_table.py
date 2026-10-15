#!/usr/bin/env python3
"""Pool the judged gold replicates per case and SKILL.md variant.

usage: python3 dev/inbox/si3/reps_table.py VARIANT [VARIANT ...] [--detail CASE]
Reads eval/reports/verdicts-si3-gold-VARIANT-r*.claude.yaml (three replicates) and, when present,
the single full gold run eval/reports/verdicts-si3-VARIANT.claude.yaml (for `base`, si2's full run of
the same text, si2-final in verdicts-si2.claude.yaml). Cells read p/f + naturalness per run.
--detail CASE prints each run's output and the judge's rendering/fact reasoning for that case.
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REP = ROOT / "eval" / "reports"
CASES = ["G-R-009", "G-R-010", "G-R-011", "G-S-001", "G-L-006"]


def runs_for(var):
    merged = REP / "verdicts-si3.claude.yaml"
    if merged.exists():  # after consolidate.py the per-run files live in raw/si3-judging/
        runs = yaml.safe_load(merged.read_text(encoding="utf-8"))["runs"]
        out = []
        if f"si3-{var}" in runs:
            out.append((f"si3-{var}", runs[f"si3-{var}"]))
        elif var == "base":
            si2 = yaml.safe_load((REP / "verdicts-si2.claude.yaml").read_text(encoding="utf-8"))
            out.append(("si2-final", si2["runs"]["si2-final"]))
        out += [(f"si3-gold-{var}-r{r}", runs[f"si3-gold-{var}-r{r}"])
                for r in (1, 2, 3) if f"si3-gold-{var}-r{r}" in runs]
        return out
    out = []
    full = REP / f"verdicts-si3-{var}.claude.yaml"
    if full.exists():
        out.append((f"si3-{var}", yaml.safe_load(full.read_text(encoding="utf-8"))["verdicts"]))
    elif var == "base":
        si2 = yaml.safe_load((REP / "verdicts-si2.claude.yaml").read_text(encoding="utf-8"))
        out.append(("si2-final", si2["runs"]["si2-final"]))
    for r in (1, 2, 3):
        p = REP / f"verdicts-si3-gold-{var}-r{r}.claude.yaml"
        if p.exists():
            out.append((f"si3-gold-{var}-r{r}", yaml.safe_load(p.read_text(encoding="utf-8"))["verdicts"]))
    return out


def main():
    args = sys.argv[1:]
    detail = None
    if "--detail" in args:
        i = args.index("--detail")
        detail = args[i + 1]
        args = args[:i] + args[i + 2:]
    print("| case | " + " | ".join(args) + " |\n| --- |" + " --- |" * len(args))
    table = {v: runs_for(v) for v in args}
    for case in CASES:
        cells = []
        for v in args:
            got = []
            for _run, verdicts in table[v]:
                for x in verdicts:
                    if x["case_id"] == case:
                        got.append(f"{x['overall'][0]}{x.get('naturalness', '')}")
            k = sum(g.startswith("p") for g in got)
            cells.append(f"{k}/{len(got)} ({' '.join(got)})")
        print(f"| {case} | " + " | ".join(cells) + " |")
    if detail:
        raw = REP / "raw"
        for v in args:
            for run, verdicts in table[v]:
                rec = raw / run / f"{detail}.claude.json"
                out = json.loads(rec.read_text(encoding="utf-8"))["output"] if rec.exists() else "(output not in raw/)"
                for x in verdicts:
                    if x["case_id"] == detail:
                        print(f"\n== {run}: {x['overall']} nat={x.get('naturalness')}\n{out}")
                        for iv in x.get("invariant_verdicts", []):
                            if iv["verdict"] != "preserved":
                                print(f"  [{iv['kind']}: {iv['verdict']}] {iv.get('reasoning', '')[:400]}")


if __name__ == "__main__":
    main()

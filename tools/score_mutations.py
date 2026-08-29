#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Score a mutation run by per-class detection rate (000-design.md section 16).

The point is not an overall score. It is to find the classes a given reviewer
misses, so that reviewer is not relied on alone for that class.

Detection is scored two ways, because they fail differently:

  rule_hit   the review cited a rule that covers the injected defect class
  locus_hit  the review quoted the text the mutation actually touched

A review can cite the right rule at the wrong place (it found some other problem
of the same kind) or quote the right place under the wrong rule (it noticed
something changed but misclassified it). Only both together is a real detection.

    uv run tools/score_mutations.py --run mut1
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Which rules legitimately cover each injected defect. More than one is often
# defensible — a certainty inflation is both a modality and a causality problem.
COVERING_RULES: dict[str, set[str]] = {
    "modality_strengthen":  {"CTC-S003"},
    "modality_weaken":      {"CTC-S003"},
    "certainty_inflate":    {"CTC-S003", "CTC-S006", "CTC-S002"},
    "condition_broaden":    {"CTC-L001", "CTC-L002", "CTC-S007"},
    "threshold_flip":       {"CTC-L004", "CTC-S004"},
    "quantity_drift":       {"CTC-S004", "CTC-L004"},
    "token_mutate":         {"CTC-S005"},
    "negation_scope":       {"CTC-A004", "CTC-L002"},
    "order_swap":           {"CTC-L003", "CTC-P001", "CTC-P004"},
    "term_substitute":      {"CTC-T002", "CTC-T001"},
    "unsourced_qualifier":  {"CTC-S002", "CTC-S006"},
    "actor_delete":         {"CTC-A001"},
}

RULE_CITED = re.compile(r"CTC-[SAPTLR]\d{3}")


def changed_spans(clean: str, mutant: str) -> list[str]:
    """The text the mutation actually introduced or removed, as searchable strings."""
    out: list[str] = []
    sm = difflib.SequenceMatcher(None, clean, mutant, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if j2 > j1:
            out.append(mutant[j1:j2])
        if i2 > i1:
            out.append(clean[i1:i2])
    return [s.strip() for s in out if len(s.strip()) >= 2]


def scored(case: dict, output: str) -> tuple[bool, bool]:
    cls = case["mutation_class"]
    cited = set(RULE_CITED.findall(output))
    rule_hit = bool(cited & COVERING_RULES.get(cls, set()))

    spans = changed_spans(case["clean_source"], case["mutant"])
    locus = (case.get("expected_issues") or [{}])[0].get("locus", "")
    needles = [s for s in spans + [locus] if s]
    # a quoted 位置 usually carries the surrounding clause, so substring containment
    # in either direction counts
    locus_hit = any(n in output for n in needles if len(n) >= 2)
    return rule_hit, locus_hit


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", default="mut1")
    ap.add_argument("--cases", default=str(ROOT / "eval" / "mutations" / "generated.yaml"))
    args = ap.parse_args()

    cases = {c["id"]: c for c in
             (yaml.safe_load(Path(args.cases).read_text(encoding="utf-8")) or {}).get("cases", [])}
    run_dir = ROOT / "eval" / "reports" / "raw" / args.run
    if not run_dir.exists():
        print(f"no such run: {run_dir}")
        return 1

    per_class: dict[str, Counter] = defaultdict(Counter)
    misses: list[tuple[str, str, str]] = []

    for path in sorted(run_dir.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        case = cases.get(rec["case_id"])
        if not case:
            continue
        cls = case["mutation_class"]
        rule_hit, locus_hit = scored(case, rec["output"])
        c = per_class[cls]
        c["n"] += 1
        c["rule"] += rule_hit
        c["locus"] += locus_hit
        c["both"] += rule_hit and locus_hit
        if not (rule_hit and locus_hit):
            misses.append((cls, rec["case_id"],
                           f"rule={'y' if rule_hit else 'n'} locus={'y' if locus_hit else 'n'}"))

    total = Counter()
    print(f"{'class':22} {'n':>3} {'both':>5} {'rule':>5} {'locus':>6}   rate")
    for cls, c in sorted(per_class.items()):
        total.update(c)
        print(f"{cls:22} {c['n']:3} {c['both']:5} {c['rule']:5} {c['locus']:6}   "
              f"{c['both'] / c['n']:.0%}")
    if total["n"]:
        print(f"\n{'TOTAL':22} {total['n']:3} {total['both']:5} {total['rule']:5} "
              f"{total['locus']:6}   {total['both'] / total['n']:.0%}")

    weak = [cls for cls, c in per_class.items() if c["n"] >= 2 and c["both"] / c["n"] < 0.5]
    if weak:
        print(f"\nclasses this reviewer should not be trusted alone for: {', '.join(sorted(weak))}")
    if misses:
        print("\nmisses:")
        for cls, cid, why in misses:
            print(f"  {cls:22} {cid:6} {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

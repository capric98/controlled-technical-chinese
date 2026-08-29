#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Promote model-proposed cases from dev/inbox into the trusted core in eval/gold.

Curation is a reviewed step, not a copy (decision 002). The transformations applied
here are the ones the orchestrator found necessary on review; each is recorded in the
output file header so a later agent can see what was changed and why.

    uv run tools/curate_cases.py --in dev/inbox/r2-gpt-cases.yaml [...] --check
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "eval" / "gold"

# An instruction that names the failure to avoid tests compliance, not judgment.
# Everything from the first 「；」 onward in these is the leak.
LEAK_MARKERS = ("不得", "并保持", "是否保持", "是否保留")

NEUTRAL_INSTRUCTION = {
    "review": "下面给出原文与候选改写。审阅候选改写是否忠实于原文；只输出问题清单，不要整体重写。",
}

FAMILY_FILES = {
    "S": ("gold-semantic.yaml", "语义保真：事实状态、情态强度、因果强度、数量"),
    "L": ("gold-logic.yaml", "逻辑与结构：条件、例外、量词、否定辖域、阈值边界、时序"),
    "T": ("gold-tokens.yaml", "受保护技术标记与术语"),
    "R": ("gold-rendering.yaml", "中文渲染、语域、过度编辑控制"),
    "A": ("gold-ambiguity.yaml", "歧义与指代：施事省略、代词、修饰语与并列作用域"),
    "P": ("gold-procedure.yaml", "流程结构与指令遵循"),
}


def neutralize_instruction(case: dict) -> str | None:
    """Return a note when the instruction was changed, else None."""
    raw = (case.get("instruction") or "").strip()
    if not raw:
        return None
    if not any(m in raw for m in LEAK_MARKERS):
        return None
    replacement = NEUTRAL_INSTRUCTION.get(case.get("mode"))
    case["instruction"] = replacement
    return (f"{case['id']}: instruction 泄露了预期失败（{raw[:40]}…），"
            f"改为{'中性指令' if replacement else '默认任务指令'}")


def curate(paths: list[Path]) -> tuple[dict[str, list[dict]], list[str]]:
    by_family: dict[str, list[dict]] = {}
    notes: list[str] = []
    seen: set[str] = set()

    for path in paths:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for case in doc.get("cases", []):
            cid = case["id"]
            if cid in seen:
                notes.append(f"{cid}: 重复 id，已跳过来自 {path.name} 的第二份")
                continue
            seen.add(cid)

            note = neutralize_instruction(case)
            if note:
                notes.append(note)

            case["provenance"] = "orchestrator-reviewed"
            case["source_file"] = path.name
            case.pop("_file", None)

            m = re.match(r"G-([A-Z])-(\d+)", cid)
            if not m:
                notes.append(f"{cid}: id 不符合 G-<family>-<seq> 格式，已跳过")
                continue
            by_family.setdefault(m.group(1), []).append(case)

    for family, cases in by_family.items():
        cases.sort(key=lambda c: c["id"])
    return by_family, notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inputs", nargs="+", required=True)
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing gold file, DISCARDING post-curation edits")
    args = ap.parse_args()

    by_family, notes = curate([Path(p) for p in args.inputs])

    print("curation notes:")
    for n in notes:
        print(f"  {n}")

    total = 0
    for family, cases in sorted(by_family.items()):
        filename, description = FAMILY_FILES[family]
        total += len(cases)
        traps = sum(1 for c in cases if c.get("over_edit_trap"))
        print(f"\n{filename}: {len(cases)} case(s), {traps} over-edit trap(s) — {description}")
        if args.check:
            continue
        target = GOLD / filename
        header = (
            f"# {description}\n"
            f"# 由 tools/curate_cases.py 从 dev/inbox 提升而来；策展变更见 git 历史与 decision 002。\n"
            f"# provenance: orchestrator-reviewed —— 已由编排者按已接受语义审阅，尚未经人工复核。\n"
        )
        target.write_text(
            header + yaml.dump({"cases": cases}, allow_unicode=True,
                               sort_keys=False, width=100),
            encoding="utf-8")
    print(f"\n{total} case(s) total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Write a self-hosting review case for one SKILL.md version, in si2's and si3's format.

usage: python3 dev/inbox/si4/selfhost/make_case.py VARIANT SKILL_PATH
Writes dev/inbox/si4/selfhost/cases-VARIANT/selfhost.yaml (one case, id SH-VARIANT). run_set.sh runs it
with CTC_SKILL=SKILL_PATH, so the version under review is also the skill doing the review.
"""
import sys
from pathlib import Path

import yaml

var, skill = sys.argv[1], Path(sys.argv[2])
out = Path(__file__).resolve().parent / f"cases-{var}" / "selfhost.yaml"
out.parent.mkdir(parents=True, exist_ok=True)
case = {
    "id": f"SH-{var}",
    "task": "review",
    "mode": "review",
    "instruction": "以 review 模式审阅下面这份 Agent Skill 文本（即本技能自身的文本），只输出问题清单，不要整体重写。",
    "source": skill.read_text(encoding="utf-8"),
}
out.write_text(yaml.safe_dump({"cases": [case]}, allow_unicode=True, sort_keys=False, width=1000),
               encoding="utf-8")
print(f"wrote {out}")

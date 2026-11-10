#!/usr/bin/env python3
"""Rebuild the si6 candidates from the frozen baseline by exact string replacement.

usage: python3 dev/inbox/si6/cand/build.py
Writes dev/inbox/si6/cand/<variant>/SKILL.md for every variant in VARIANTS. Every edit must
match exactly once in the text it is applied to.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (HERE.parent / "base" / "SKILL.md").read_text(encoding="utf-8")

EDITS = {
    # F1 — proposal 10, maintainer decision M2: the description gains §1's exclusions. Self-hosting reported
    # the omission as CTC-P005 in 5 of 6 si5 runs. The sentence repeats §1's list word for word.
    "F1": ("未触发规则的文本原样返回。\n---",
           "未触发规则的文本原样返回。不用于营销文案、品牌叙事、文学写作、SEO 与一般性文字润色。\n---"),
    # R1 — proposal 29, maintainer decision M3: 「紧急时」 joins R004's open class, beside 「必要时」「条件允许时」
    # (OR-07 splits A005, R004, A005 on si5 base and A005, A005+R004, R004 on si5 v2).
    "R1": ("「条件允许时」「合理」等", "「条件允许时」「紧急时」「合理」等"),
    # G1 — proposal 27, maintainer decision M5: the permission exemption tests what the permitted way of doing
    # it adds beyond the default action. GO-03 (「也可以分两批发布」) forks on the baseline (not reported 1/3,
    # A005 2/3, citing 「许可的操作是发布」); OR-06 and GO-02, which add a deletion or a config change, still
    # report. No example, so the probe words stay out of the text.
    "G1": ("所许可的也不是破坏性、不可逆或改变外部状态的操作",
           "所许可的做法也不在默认动作之外增加破坏性、不可逆或改变外部状态的操作"),
    # B1 — proposal 27, maintainer decision M6: P003's own-step bound names a backup or snapshot that creates the
    # recovery point a later guarded operation relies on, as the runtime already behaves (GO-01 P003 3/3, GO-01r
    # 3/3); the second cold decode of si5 v2 read the literal bound as excluding it. GO-05 is the boundary.
    "B1": ("只有当该步是破坏性、不可逆或改变外部状态的操作，且后续步骤的安全性取决于它是否成功",
           "只有当该步是破坏性、不可逆或改变外部状态的操作（为后续这类操作建立恢复点的备份、快照也算），"
           "且后续步骤的安全性取决于它是否成功"),
    # U1 — proposal 30, maintainer decision M7: a strength authorisation that names neither the items nor the
    # target strength changes nothing. AU-01 lowers every strength in 1/3 baseline runs; AU-03 (item and
    # strength named) is the boundary. No quoted example, so AU-01's wording stays out of the text.
    "U1": ("未获授权的同类改动一律不得做。",
           "未获授权的同类改动一律不得做。调整规范强度的授权没有指明哪些条目、调整到何种强度时，正文不改，"
           "按第 5 类在「待确认」中请调用方指明。"),
}

# v2 — rulings on the three reviews of v1 (dev/inbox/si6/review/adjudication.md) and the v1 runs:
# - B1': 「为后续破坏性或不可逆操作」, the scope M6 approved. v1's 「为后续这类操作」 also covered state-changing
#   steps: G-R-007 (a backup before a traffic switch; gold expects no finding) failed 3/3 on v1, base 3/3
#   pass (adversarial review predicted it). 「该步」 for 「它」 is the naturalness reviewer's equivalent wording.
# - U1': either missing piece triggers it (M7's option: 授权须指明对象和目标强度), and 「不据此改动正文」 keeps
#   fixes that other rules trigger (adversarial and naturalness reviews; AU-04, AU-05).
# - G1a: 「引入」 for 「增加」 (naturalness: 「增加」 can be read as counting an extra step), otherwise M5 as asked.
# - G1b: the adversarial reviewer's narrower wording: the permitted way of doing it also does not reduce the
#   checks or reviews before such an operation, or change who performs it. Base reports the counterexamples
#   (GO-06, GO-07) that G1 exempts; this goes to the maintainer as M8.
EDITS["B1'"] = ("只有当该步是破坏性、不可逆或改变外部状态的操作，且后续步骤的安全性取决于它是否成功",
                "只有当该步是破坏性、不可逆或改变外部状态的操作（为后续破坏性或不可逆操作建立恢复点的备份、快照也算），"
                "且后续步骤的安全性取决于该步是否成功")
EDITS["U1'"] = ("未获授权的同类改动一律不得做。",
                "未获授权的同类改动一律不得做。调整规范强度的授权没有指明调整哪些条目，或没有指明调整到何种强度时，"
                "不据此改动正文，按第 5 类在「待确认」中请调用方指明。")
EDITS["G1a"] = ("所许可的也不是破坏性、不可逆或改变外部状态的操作",
                "所许可的做法也不引入默认动作之外的破坏性、不可逆或改变外部状态的操作")
EDITS["G1b"] = ("所许可的也不是破坏性、不可逆或改变外部状态的操作",
                "所许可的做法也不引入默认动作之外的破坏性、不可逆或改变外部状态的操作，不减少这类操作之前的检查或复核，"
                "也不更换其执行者")

# v3 — the release candidate, on the maintainer's M8 and M9 (resolutions.yaml, decisions_after_v2):
# - M8: G1b. v2a and v2b part only at GO-07 (base A005 3/3, v2a not reported 3/3, v2b R004 3/3).
# - M9: no B1. Base already raises GO-01's backup 3/3 without it; with it GO-05 (a backup as the last step)
#   is a false positive in 3 of 6 v2 runs and G-R-007 fails 1/3 on v2a, all citing the backup as a recovery point.
# v4 — after the v3 runs (self-hosting r1: 「其」 in 「也不更换其执行者」 has three antecedents; G-S-001 inserts the
# permission's object in 3 of 8 v3 runs against 0 of 7 on base):
# - G1c: G1b with the antecedent written out, 「也不更换这类操作的执行者」 (M8 as answered: 「hands it to another
#   performer」, it = such an operation).
# - G1d: G1c without the checks clause. v2a, which has neither clause, still reports GO-06 3/3; the clause is a
#   suspect for G-S-001. A wording narrower than M8 as answered: for the maintainer.
EDITS["G1c"] = ("所许可的也不是破坏性、不可逆或改变外部状态的操作",
                "所许可的做法也不引入默认动作之外的破坏性、不可逆或改变外部状态的操作，不减少这类操作之前的检查或复核，"
                "也不更换这类操作的执行者")
EDITS["G1d"] = ("所许可的也不是破坏性、不可逆或改变外部状态的操作",
                "所许可的做法也不引入默认动作之外的破坏性、不可逆或改变外部状态的操作，也不更换这类操作的执行者")

VARIANTS = {
    "v1": ["F1", "R1", "G1", "B1", "U1"],
    "v2a": ["F1", "R1", "G1a", "B1'", "U1'"],
    "v2b": ["F1", "R1", "G1b", "B1'", "U1'"],
    "v3": ["F1", "R1", "G1b", "U1'"],
    "v4c": ["F1", "R1", "G1c", "U1'"],
    "v4d": ["F1", "R1", "G1d", "U1'"],
    # ablation for G-S-001's inserted object (v3 5/14, v2b 2/9, v4d 3/10; base 0/7): one G edit alone, and
    # every si6 edit except G
    "a-G1a": ["G1a"],
    "a-noG": ["F1", "R1", "U1'"],
    # Z2 — a pointer from the exemption to CTC-P002's zero-anaphora clause (010 Z1), tried against G-S-001's
    # inserted object; adds no requirement
    "v5": ["F1", "R1", "G1c", "U1'", "Z2"],
}
EDITS["Z2"] = ("后两种情形即使缺少判据或阈值，也不按 CTC-A005 或 CTC-R004 提出或报告。",
               "后两种情形即使缺少判据或阈值，也不按 CTC-A005 或 CTC-R004 提出或报告；许可句省略的对象可由前文唯一确定时，"
               "按 CTC-P002 保持省略。")


def build(names):
    text = BASE
    for name in names:
        old, new = EDITS[name]
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{name}: expected one match, found {n}")
        text = text.replace(old, new, 1)
    return text


for var, names in VARIANTS.items():
    out = HERE / var / "SKILL.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(names), encoding="utf-8")
    print(f"wrote {out.relative_to(HERE.parents[3])} ({len(names)} edits)")

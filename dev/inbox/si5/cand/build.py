#!/usr/bin/env python3
"""Rebuild the si5 candidates from the frozen baseline by exact string replacement.

usage: python3 dev/inbox/si5/cand/build.py
Writes dev/inbox/si5/cand/<variant>/SKILL.md for every variant in VARIANTS. Every edit must
match exactly once in the text it is applied to.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (HERE.parent / "base" / "SKILL.md").read_text(encoding="utf-8")

EDITS = {
    # N1, N2 — proposal 22, maintainer decision M2: one name for the deontic strength. The frontmatter and
    # §3's example already say 规范强度; §3's authorisation list and CTC-S003's tuple said 道义强度.
    # Self-hosting reported the pair in most runs since si2 (si5 base 1/2).
    "N1": ("调整道义强度（规范强度）", "调整规范强度"),
    "N2": ("(认识强度, 道义强度, 言语行为类型)", "(认识强度, 规范强度, 言语行为类型)"),
    # V1 — proposal 21, maintainer decision M7: a term difference of unclear co-reference is a CTC-T001
    # finding in review, as the runtime already reports it (TV-01, TV-02: T001 6/6). Self-hosting reported the
    # missing rule ID in most si4 runs and si5 base 1/2.
    "V1": ("review 模式下它是一条普通 finding。", "review 模式下按 CTC-T001 报告。"),
    # H1, H2 — proposal 26, maintainer decision M6: the missing-criterion threshold names P004's guarded
    # operations, as the runtime already behaves (TH-01 A005 3/3, TH-02 「待确认」 3/3 on a check that gates a
    # restart; TV-02 reports the criterion before a ramp-up).
    "H1": ("而没有破坏性或不可逆操作取决于它的结果时", "而没有破坏性、不可逆或改变外部状态的操作取决于它的结果时"),
    "H2": ("只有当该步是破坏性或不可逆操作、且后续步骤的安全性取决于它是否成功",
           "只有当该步是破坏性、不可逆或改变外部状态的操作、且后续步骤的安全性取决于它是否成功"),
    # D1 — proposal 23 (M4) and the descriptive over-report (M5): two more kinds of text that are not a real
    # ambiguity and, when a criterion or threshold is missing, are not raised or reported under A005 or
    # R004. OR-01/OR-02 (a condition that only grants a permission) and OR-03 (a description of system
    # behaviour) draw A005 3/3 on the baseline; G-S-001 and G-R-012 are the gold cases. The template
    # 「若…，也可以…」 avoids the probe and gold words.
    "D1": ("参数在运行时由外部唯一确定。不得因",
           "参数在运行时由外部唯一确定；条件只放宽操作者可以做的事、默认动作不变（「若…，也可以…」）；"
           "文本只描述系统行为，不要求读者据此行动。后两种情形缺少判据或阈值时，同样不按 CTC-A005 或 CTC-R004 "
           "提出或报告。不得因"),
    # S1 — proposal 8: P004 calls moving a standalone warning block an R005 violation, but R005 named no
    # position. Self-hosting reported the mismatch in si3 and si4 (v1 r2, v3 r1, v8 r1). R005 now says so,
    # keeping the attribution and its WARNING level.
    "S1": ("链接与引用块应保持其粒度。", "链接与引用块应保持其粒度，独立告警块保持原位。"),
}

# v2 — rulings on the three reviews of v1 (dev/inbox/si5/review/adjudication.md) and maintainer decisions
# M8–M10 (resolutions.yaml):
# - N1': anchor the authorisation in the source text (naturalness, adversarial; base self-hosting r1).
# - V1': keep 「它是一条」, so the review clause does not inherit 「只有当它妨碍执行时」 (adversarial).
# - H1': the contrapositive, which matches P003's 「只有当…才…」 (naturalness); same scope as H1.
# - H2': 「，且」 for the second-level join (naturalness); kept by M9.
# - D1': the permission exemption requires that the source's obligation is not waived (adversarial; OR-07,
#   v1 silent 3/3) and that the permitted action is not destructive, irreversible or state-changing (M8;
#   OR-06, v1 silent 3/3); wording repairs from the naturalness review.
# - S1': 「应」 (naturalness).
# - Z1 (M10): an object omitted but uniquely recoverable from the preceding text is not missing (G-S-001:
#   「将索引重建」 inserted in v1 4/7, base 1/7). PR-13 (「对应服务」) is the boundary.
EDITS["N1'"] = ("调整道义强度（规范强度）", "调整来源中的规范强度")
EDITS["V1'"] = ("review 模式下它是一条普通 finding。", "review 模式下它是一条 CTC-T001 finding。")
EDITS["H1'"] = (
    "检查或确认步骤没有给出判据或判据含义未定（「确认无异常」），而没有破坏性或不可逆操作取决于它的结果时，不提出、不报告。",
    "检查或确认步骤没有给出判据或判据含义未定（「确认无异常」）时，只有当破坏性、不可逆或改变外部状态的操作取决于它的结果，"
    "才提出或报告。",
)
EDITS["H2'"] = ("只有当该步是破坏性或不可逆操作、且后续步骤的安全性取决于它是否成功",
                "只有当该步是破坏性、不可逆或改变外部状态的操作，且后续步骤的安全性取决于它是否成功")
EDITS["D1'"] = (
    "参数在运行时由外部唯一确定。不得因",
    "参数在运行时由外部唯一确定；条件只放宽对操作者的限制（「若…，也可以…」），而默认动作不变、来源规定的义务不被免除、"
    "所许可的也不是破坏性、不可逆或改变外部状态的操作；文本只描述系统行为，不要求读者据此行动。"
    "后两种情形即使缺少判据或阈值，也不按 CTC-A005 或 CTC-R004 提出或报告。不得因",
)
EDITS["S1'"] = ("链接与引用块应保持其粒度。", "链接与引用块应保持其粒度，独立告警块应保持原位。")
EDITS["Z1"] = (
    "「相关配置」「对应服务」这类说法不算写出对象。",
    "「相关配置」「对应服务」这类说法不算写出对象。省略的对象可由前文唯一确定（零形回指）时，不算缺少对象，保持省略。",
)

VARIANTS = {
    "v1": ["N1", "N2", "V1", "H1", "H2", "D1", "S1"],
    "v2": ["N1'", "N2", "V1'", "H1'", "H2'", "D1'", "S1'", "Z1"],
}


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

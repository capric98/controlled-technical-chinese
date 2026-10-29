#!/usr/bin/env python3
"""Rebuild the si4 candidates from the frozen baseline by exact string replacement.

usage: python3 dev/inbox/si4/cand/build.py
Writes dev/inbox/si4/cand/<variant>/SKILL.md for every variant in VARIANTS. Every edit must
match exactly once in the text it is applied to.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (HERE.parent / "base" / "SKILL.md").read_text(encoding="utf-8")

EDITS = {
    # F1 — maintainer decision M2: the one frontmatter clause self-hosting reports (si2; si3 5/8; si4
    # base 1/2). §5 disambiguates on evidence; the description said every ambiguity is only reported.
    "F1": (
        "歧义只报告不擅自消解；",
        "上下文不足以确定的歧义只报告、不擅自消解；",
    ),
    # T1 — proposal 18: 「记录级别」 is the only place the 级别 column has another name. Reported by every
    # self-hosting run since si2 (si3 8/8, si4 base 2/2).
    "T1": (
        "A、P 两族按其记录级别生效",
        "A、P 两族按其级别生效",
    ),
    # T2 — 「压缩授权」 and 「授权合并步骤」 name one authorisation two ways (self-hosting si3 3/8, si4 base
    # 1/2). The behaviour is already the D004 split: a step cap merges (si2 PR-09 3/3), a character cap
    # does not (si4 PC-01 3/3 base). The parenthesis states that split; §3's list already names
    # 「CTC-P003 的合并步骤」 apart from 「长度上限」.
    "T2": (
        "来源把验证单独列为一个步骤时：未获压缩授权则该步骤保持独立；调用方授权合并步骤时可以并入相邻步骤，但合并后",
        "来源把验证单独列为一个步骤时，该步骤保持独立；调用方授权合并步骤（明确要求合并，或限定步骤数）时"
        "可以并入相邻步骤，但合并后",
    ),
    # T3 — §9 item 1's example has no direction marker, while item 2 uses 「不得写成」 (self-hosting si3
    # v3 r2, v6 r1).
    "T3": (
        "「用户打开控制台。用户点击设置。用户修改端口。」写成「用户打开控制台后，点击设置修改端口。」",
        "「用户打开控制台。用户点击设置。用户修改端口。」应写成「用户打开控制台后，点击设置修改端口。」",
    ),
    # T4 — 「明确边界」 is defined nowhere (self-hosting on this text 2/4: si3 v6 r1, si4 base r2).
    "T4": (
        "**应** = 默认要求，可被更高优先级或明确边界推翻；",
        "**应** = 默认要求，可被更高优先级或规则条文写明的边界推翻；",
    ),
    # B1 — proposal 15, maintainer decision M5: a missing verification method or criterion goes by
    # CTC-P003's bound in both modes. P3-01: review cites A005/ERROR 2/3 on a read-only closing check,
    # rewrite raises nothing 3/3. A criterion that is given but undefined (PR-07 「流量正常」) stays A005,
    # as R004's exclusion already says for undefined states; the example avoids PR-07's words.
    "B1": (
        "不得静默择一，不得补出缺失项。 |",
        "不得静默择一，不得补出缺失项。来源完全没有给出成功判据或验证方式的步骤，是否提出或报告按 CTC-P003 判断；"
        "给出的判据含义未定（「服务正常」）时仍按本规则。 |",
    ),
    # B2 — proposal 19, maintainer decision M4: a degree word that sets an unstated threshold on a
    # measurable quantity is a missing value, like 「多次」 (R4-04: A005, R004, A005 on the baseline).
    # The example avoids the probe words (负载、过高、偏大).
    "B2a": (
        "未定义的状态（「服务稳定」）与未给出具体值的次数或时长（「多次」「若干分钟」）不是这类词，按 CTC-A005 处理。",
        "未定义的状态（「服务稳定」）、未给出具体值的次数或时长（「多次」「若干分钟」），"
        "以及给可测量指标设限而未给出阈值的程度说法（「延迟较高」）不是这类词，按 CTC-A005 处理。",
    ),
    "B2b": (
        "CTC-R004 排除的未定义状态与次数、时长）",
        "CTC-R004 排除的未定义状态、次数、时长与阈值）",
    ),
    # C1 — proposal 20: a cold reader should predict the RG-15 rewrite the maintainer ruled correct
    # (decision 008, ruling 1). The third-person user frame joins the reader-guidance type, scoped to
    # tool descriptions (RG-22: the same frame in developer-guide prose stays, base 3/3). The repair
    # sentence after it is unchanged, since si3 found its subject clause load-bearing for G-R-010.
    "C1": (
        "把读者当作谈话对象的引导（「这个工具可以帮你」）。",
        "把读者当作谈话对象的引导（「这个工具可以帮你」；工具描述中以使用者作主语的「调用者可以…」同属此类）。",
    ),
}

# B1v2 — after v1: B1's carve-out (「给出的判据含义未定…仍按本规则」) swallowed P3-01. The model reads
# 「检查…的运行情况」 as an undefined criterion, so review cited A005/ERROR 3/3 (base 2/3) and rewrite began
# raising it 2/3 (base 0/3). v2 states the exclusion by its own condition instead of deferring to
# P003: a check, with no criterion or an undefined one, that no destructive or irreversible action
# depends on. PR-07 (「确认流量正常后」 gates decommission) and P3-03 (the destructive step itself) stay out
# of it. 「确认无异常」 avoids the probe words.
EDITS["B1v2"] = (
    "不得静默择一，不得补出缺失项。 |",
    "不得静默择一，不得补出缺失项。检查或确认步骤没有给出判据或判据含义未定（「确认无异常」），"
    "而没有破坏性或不可逆操作取决于它的结果时，不提出、不报告（CTC-P003）。 |",
)

# v3 — rulings on the three independent reviews of v1 (dev/inbox/si4/review/adjudication.md):
# - T4': 「规则条文写明的」 could attach to 「更高优先级」 too (naturalness); two verbs keep the two sources apart.
# - B2a': 「可测量指标」 literally covers 「调到适当的上限」, pulling R004's own 「适当」 into A005 (adversarial);
#   「设限而未给出阈值」 reads as self-contradictory (naturalness). The exclusion now names trigger conditions on
#   运行指标.
# - B2b': the parenthesis named the remedy (阈值) as the excluded item (naturalness); it now points at R004's
#   own exclusion instead of re-listing it.
# - C1': 「同属此类」 stipulates a third-person frame into reader guidance (naturalness), and the clause
#   literally caught a usage restriction 「只有管理员账号可以调用」 (adversarial). It becomes its own item,
#   limited to frames that state the function.
EDITS["T4'"] = (
    "**应** = 默认要求，可被更高优先级或明确边界推翻；",
    "**应** = 默认要求，可被更高优先级推翻，也可被规则条文写明的边界推翻；",
)
EDITS["B2a'"] = (
    "未定义的状态（「服务稳定」）与未给出具体值的次数或时长（「多次」「若干分钟」）不是这类词，按 CTC-A005 处理。",
    "未定义的状态（「服务稳定」）、未给出具体值的次数或时长（「多次」「若干分钟」），"
    "以及用程度词描述运行指标而未给出阈值的触发条件（「延迟较高时」），都不是这类词，按 CTC-A005 处理。",
)
EDITS["B2b'"] = (
    "CTC-R004 排除的未定义状态与次数、时长）",
    "CTC-R004 中按 CTC-A005 处理的说法）",
)
EDITS["C1'"] = (
    "把读者当作谈话对象的引导（「这个工具可以帮你」）。",
    "把读者当作谈话对象的引导（「这个工具可以帮你」）、工具描述中以使用者作主语陈述功能的句式（「调用者可以…」）。",
)

# v4 — after the v3 probes: B2b' (「CTC-R004 中按 CTC-A005 处理的说法」) can be read as 「anything R004 finds goes
# to A005」. R4-05 r1 on v3 cites 「条件允许」 as 「按 CTC-R004 发现，按 §8 第 2 步转 CTC-A005」 (base and v1 R004
# 3/3). B2b'' lists the three excluded kinds by name again, naming the metric condition rather than the
# remedy (阈值), which was the naturalness reviewer's objection to B2b.
EDITS["B2b''"] = (
    "CTC-R004 排除的未定义状态与次数、时长）",
    "CTC-R004 排除项中的未定义状态、次数、时长与运行指标触发条件）",
)

# C1d — after v3 self-hosting: the defect item and the repair sentence both said 「以使用者作主语」 with the
# same example (CTC-R002, 2/2 runs). The example stays on the defect item and the repair sentence keeps only
# the direct form. si3 added 「不以使用者作句子主语」 for G-R-010, whose frame (「这个工具能够允许调用者去获取」)
# has the user as object, not subject; G-R-010 and RG-08/10/15 check that the direct form is what carried
# it. RG-16 (an agent's 「你可以」 permission, lost 1/3 on v3) is replicated on v4.
EDITS["C1d"] = (
    "把读者当作谈话对象的引导（「这个工具可以帮你」）。去除这些缺陷时，工具描述改为直接陈述功能（「获取…」「用于…」），"
    "不以使用者作句子主语（「调用者可以…」）。",
    "把读者当作谈话对象的引导（「这个工具可以帮你」）、工具描述中以使用者作主语陈述功能的句式（「调用者可以…」）。"
    "去除这些缺陷时，工具描述改为直接陈述功能（「获取…」「用于…」）。",
)

# v5 — after v4 self-hosting: CTC-A005's exclusion and CTC-P003's last sentence state two different
# thresholds for when a missing criterion is raised (si4 self-hosting v3 1/2, v4 2/2). They cover
# different steps: P003's bound is about an operation step's own success criterion (P3-03, P3-04), A005's
# exclusion about a check or confirmation step (P3-01, P3-05, PR-07). P3x says so in P003; B1v3 drops the
# A005 pointer to P003, which would now be circular.
EDITS["B1v3"] = (
    "不得静默择一，不得补出缺失项。 |",
    "不得静默择一，不得补出缺失项。检查或确认步骤没有给出判据或判据含义未定（「确认无异常」），"
    "而没有破坏性或不可逆操作取决于它的结果时，不提出、不报告。 |",
)
EDITS["P3x"] = (
    "来源未给出成功判据时：只有当该步是破坏性或不可逆操作、且后续步骤的安全性取决于它是否成功，才按「待确认」第 2 类提出；"
    "其余步骤缺少判据不提出，以免正常的流程文档产生成串的未决项。",
    "来源未给出操作步骤自身的成功判据时：只有当该步是破坏性或不可逆操作、且后续步骤的安全性取决于它是否成功，"
    "才按「待确认」第 2 类提出；其余操作步骤缺少判据不提出，以免正常的流程文档产生成串的未决项。"
    "检查或确认步骤缺少判据按 CTC-A005 处理。",
)

# v6 — after v5 self-hosting (2/2): §8 step 2 lists the rows that route a case to A005, and P3x added one
# (CTC-P003's 「检查或确认步骤缺少判据按 CTC-A005 处理」) that the list does not name, as si3's v3 left out R004's
# exclusion. B2b3 adds it in ID order. PR-07 already cites A005 3/3 on every version, so this is textual.
EDITS["B2b3"] = (
    "CTC-P002 无法确定、CTC-R004 排除的未定义状态与次数、时长）",
    "CTC-P002 无法确定、CTC-P003 中检查或确认步骤缺少判据、CTC-R004 排除项中的未定义状态、次数、时长与运行指标触发条件）",
)

# v7 — after the v6 runs: R4-05 cites A005 for 「条件允许」 in 2/9 v6 runs (base 6/6; v3–v6 3/21), reasoning
# through R004's 「未定义的状态」 exclusion. M4 names 条件允许时 among the words R004 keeps; R4L lists it.
# R4-10 (「时间允许时」, not listed) is the generalisation check.
EDITS["R4L"] = (
    "「尽量」「尽可能」「尽快」「最好」「适当」「必要时」「视情况」「合理」等表示程度、时机或裁量的词",
    "「尽量」「尽可能」「尽快」「最好」「适当」「必要时」「视情况」「条件允许时」「合理」等表示程度、时机或裁量的词",
)

# v8 — after v7 self-hosting: T4 put 「规则条文」 into the §6 paragraph that already says 「规则正文」 for the same
# text (CTC-T001, v7 r1; reported apart in si3 v4 r2). §3 and §8 say 「规则条文」; T5 unifies §6. Wording only:
# v8's probes and gold are v7's.
EDITS["T5"] = (
    "规则正文中的「必须」「不得」表达该规则的要求与禁止",
    "规则条文中的「必须」「不得」表达该规则的要求与禁止",
)

VARIANTS = {
    "v1": ["F1", "T1", "T2", "T3", "T4", "B1", "B2a", "B2b", "C1"],
    "v2": ["F1", "T1", "T2", "T3", "T4", "B1v2", "B2a", "B2b", "C1"],
    "v3": ["F1", "T1", "T2", "T3", "T4'", "B1v2", "B2a'", "B2b'", "C1'"],
    "v4": ["F1", "T1", "T2", "T3", "T4'", "B1v2", "B2a'", "B2b''", "C1d"],
    "v5": ["F1", "T1", "T2", "T3", "T4'", "B1v3", "P3x", "B2a'", "B2b''", "C1d"],
    "v6": ["F1", "T1", "T2", "T3", "T4'", "B1v3", "P3x", "B2a'", "B2b3", "C1d"],
    "v7": ["F1", "T1", "T2", "T3", "T4'", "B1v3", "P3x", "B2a'", "B2b3", "C1d", "R4L"],
    "v8": ["F1", "T1", "T2", "T3", "T4'", "T5", "B1v3", "P3x", "B2a'", "B2b3", "C1d", "R4L"],
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

#!/usr/bin/env python3
"""Rebuild the si3 candidates from the frozen baseline by exact string replacement.

usage: python3 dev/inbox/si3/cand/build.py
Writes dev/inbox/si3/cand/<variant>/SKILL.md for every variant in VARIANTS. Every edit must
match exactly once in the text it is applied to.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (HERE.parent / "base" / "SKILL.md").read_text(encoding="utf-8")

R003_OLD = (
    "| CTC-R003 | 应 | 反译文腔 | 文本含无必要的被动、名词化赘语（进行／作出／予以 + 动词）、过长的「的」字串、"
    "英语从句语序残留（「由于…的事实」）或直译连接词时，在语义完全不变的前提下改用中文技术写作的常规表达。"
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |"
)

EDITS = {
    # S1 — proposal 3: 状态提示 joins the strict scope list (maintainer decision Q1), and §1 stops
    # listing it separately, since §1 already covers everything the scope lists name
    "S1a": (
        "- **适用范围** — agent 指令与系统提示；工具与函数描述；SOP、runbook、变更流程；"
        "运维与安全敏感操作；排障步骤；告警与错误信息。",
        "- **适用范围** — agent 指令与系统提示；工具与函数描述；SOP、runbook、变更流程；"
        "运维与安全敏感操作；排障步骤；告警、错误信息与状态提示。",
    ),
    "S1b": (
        "覆盖 §3 strict 与 standard 适用范围所列的文档类型，以及状态提示、技术文本的英译中与既有中文技术文本的审校。",
        "覆盖 §3 strict 与 standard 适用范围所列的文档类型，以及技术文本的英译中与既有中文技术文本的审校。",
    ),
    # S2 — proposal 5: R004's list becomes an open class of degree, timing and discretion words
    # (maintainer decision Q3). 尽快 is the word §3's own example uses; 视情况 is the discretion
    # word R4-01 already treats as R004 3/3. An undefined state or a missing value goes to A005
    # (PR-07: 「流量正常」 drew an extra R004 in 1/3 baseline runs). The examples avoid PR-07's own words
    "S2": (
        "的判定条件由无判据词承担时——「尽量」「尽可能」「最好」「适当」「必要时」「合理」——"
        "新写时给出可观测的触发条件（阈值、状态或事件）；改写时不得补出来源没有的判据，在「待确认」中提出。",
        "的判定条件由无判据词承担时——「尽量」「尽可能」「尽快」「最好」「适当」「必要时」「视情况」「合理」"
        "等程度、时限或裁量词——新写时给出可观测的触发条件（阈值、状态或事件）；"
        "改写时不得补出来源没有的判据，在「待确认」中提出。"
        "未定义的状态（「服务稳定」）与缺失的数值（「多次」）不是这类词，按 CTC-A005 处理。",
    ),
    # S3 — proposal 16: R003 gains a second defect class, 口语腔, stated for every in-scope text
    # rather than for one genre (si2's E3 named alerts/errors/status only, and G-R-010 fell from
    # 6/7 to 2/9 because the row then read as closed). The examples avoid the words of the gold
    # sources and the probes, except the canonical filler 「一下」.
    "S3-class": (
        R003_OLD,
        "| CTC-R003 | 应 | 反译文腔与口语腔 | 文本含译文腔——无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
        "过长的「的」字串、英语从句语序残留（「由于…的事实」）、直译连接词——"
        "或口语腔——客套与请托（「麻烦您」）、语气词（「啊」「嘛」）、情绪化感叹（「哎呀！」）、"
        "口语填充（「一下」）、把读者当作谈话对象的引导（「这个工具可以帮你」）——时，"
        "在语义完全不变的前提下改用中文技术写作的常规表达。"
        "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
    ),
    # S3 boundary sentence: each clause has a probe that fails or is at risk without it —
    # 推测「吧」 PR-18; 强度「千万」 RG-06 (base r2 cleaned 「哦」 and raised 千万不要→不得);
    # 警示「危险！」 PR-16; quoted or prescribed replies PR-17 (si2 v2 stripped one 3/3);
    # the caller's tone convention RG-05 (maintainer decision Q2)
    "S3-bound": (
        "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
        "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。"
        "承载推测、强度或警示的成分不是口语腔（表推测的「吧」、「千万」、「危险！」）；"
        "文本中引述或规定的话语，以及调用方约定的语气，不在此列。本规则永远低于 S 族。 |",
    ),
    # S3 ladder: layer 4 names the defects its rules repair
    "S3-ladder": (
        "| 4 自然的技术中文 | 专业中文技术语体：无译文腔、无伪法律赘语、",
        "| 4 自然的技术中文 | 专业中文技术语体：无译文腔与口语腔、无伪法律赘语、",
    ),
}

# v2 — after the v1 / v1-class ablation (probes, gold replicates):
# - the boundary sentence keeps only the clause a probe needed: RG-06 raised 「千万不要」 to 「不得」 in
#   3/3 v1-class runs and 0/3 v1 runs. PR-16 (危险！), PR-17 (quoted reply), PR-18 (吧) and RG-05
#   (caller tone) passed 3/3 without any boundary text, so their clauses are dropped, as si2 did for
#   「危险！」 (text only when the probe fails)
# - G-R-010 settled on 「该工具允许调用者获取…」 in 6/6 v1 and v1-class runs; translationese now
#   names English sentence frames generally, with the permissive/causative frame as a second example
EDITS["S3-class-v2"] = (
    R003_OLD,
    "| CTC-R003 | 应 | 反译文腔与口语腔 | 文本含译文腔——无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
    "过长的「的」字串、英语句式残留（「由于…的事实」「使用户能够…」）、直译连接词——"
    "或口语腔——客套与请托（「麻烦您」）、语气词（「啊」「嘛」）、情绪化感叹（「哎呀！」）、"
    "口语填充（「一下」）、把读者当作谈话对象的引导（「这个工具可以帮你」）——时，"
    "在语义完全不变的前提下改用中文技术写作的常规表达。"
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
)
EDITS["S3-bound-v2"] = (
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。"
    "表示强度的「千万」不是口语腔。本规则永远低于 S 族。 |",
)

# v3 — after the v2 runs:
# - v2's translationese example 「使用户能够…」 did not move G-R-010 (direct form 1/3 under v2, 1/9
#   across v1, v1-class and v2, against 7/11 on base): reverted. The repair the gold asks for is a
#   genre form, not a defect, so R003's requirement now says what the conventional form of a tool
#   description is. It applies only once a listed defect has triggered the row (CTC-R001)
# - PR-07 v2 r1 cited 「一段时间」 as R004, reading it as a 「时限词」: 时限 becomes 时机 (尽快、及时
#   are about when, not how long), and the exclusion names missing counts and durations
EDITS["S2-v3"] = (
    EDITS["S2"][0],
    "的判定条件由无判据词承担时——「尽量」「尽可能」「尽快」「最好」「适当」「必要时」「视情况」「合理」"
    "等程度、时机或裁量词——新写时给出可观测的触发条件（阈值、状态或事件）；"
    "改写时不得补出来源没有的判据，在「待确认」中提出。"
    "未定义的状态（「服务稳定」）与缺失的次数或时长（「多次」「若干分钟」）不是这类词，按 CTC-A005 处理。",
)
EDITS["S3-class-v3"] = (
    R003_OLD,
    "| CTC-R003 | 应 | 反译文腔与口语腔 | 文本含译文腔——无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
    "过长的「的」字串、英语从句语序残留（「由于…的事实」）、直译连接词——"
    "或口语腔——客套与请托（「麻烦您」）、语气词（「啊」「嘛」）、情绪化感叹（「哎呀！」）、"
    "口语填充（「一下」）、把读者当作谈话对象的引导（「这个工具可以帮你」）——时，"
    "在语义完全不变的前提下改用中文技术写作的常规表达；"
    "工具描述的常规表达是直接陈述功能（「获取…」「用于…」），而不是陈述谁可以用它做什么。"
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
)

# v4 — after the v3 full gold run, the v3 self-hosting pass and the three independent reviews of v3
# (dev/inbox/si3/review/, rulings in adjudication.md). Wording and consistency only:
# - ladder: 「无译文腔与口语腔」 can read as "not both" (CTC-A004 scope) -> two negations (naturalness)
# - R004: 「等程度」 can parse as "equal degree"; 「缺失的次数」 does not fit 「多次」 (naturalness)
# - R003: the trigger clause no longer runs 170 characters between dashes; 「请托」 -> 「客套话」
#   (naturalness). The tool-description sentence now says it is the repair form once a listed defect
#   is removed, and that it is about the subject of the sentence, not the content (cold decode fork
#   on probe 1; naturalness over-control risk). RG-01, RG-09 and RG-12 are its boundary probes
# - §8 step 2 lists R004's exclusion among the rows that route to A005 (v3 self-hosting r2 finding 1)
EDITS["S3-ladder-v4"] = (
    "| 4 自然的技术中文 | 专业中文技术语体：无译文腔、无伪法律赘语、",
    "| 4 自然的技术中文 | 专业中文技术语体：无译文腔、无口语腔、无伪法律赘语、",
)
EDITS["S2-v4"] = (
    EDITS["S2"][0],
    "的判定条件由无判据词承担时——「尽量」「尽可能」「尽快」「最好」「适当」「必要时」「视情况」「合理」"
    "等表示程度、时机或裁量的词——新写时给出可观测的触发条件（阈值、状态或事件）；"
    "改写时不得补出来源没有的判据，在「待确认」中提出。"
    "未定义的状态（「服务稳定」）与未给出具体值的次数或时长（「多次」「若干分钟」）不是这类词，按 CTC-A005 处理。",
)
EDITS["S3-class-v4"] = (
    R003_OLD,
    "| CTC-R003 | 应 | 反译文腔与口语腔 | 文本含译文腔或口语腔时，在语义完全不变的前提下改用中文技术写作的常规表达。"
    "译文腔：无必要的被动、名词化赘语（进行／作出／予以 + 动词）、过长的「的」字串、"
    "英语从句语序残留（「由于…的事实」）、直译连接词。"
    "口语腔：客套话（「麻烦您」）、语气词（「啊」「嘛」）、情绪化感叹（「哎呀！」）、口语填充（「一下」）、"
    "把读者当作谈话对象的引导（「这个工具可以帮你」）。"
    "去除这些缺陷时，工具描述改为直接陈述功能（「获取…」「用于…」），不以使用者作句子主语（「调用者可以…」）。"
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
)
EDITS["S4-routing"] = (
    "规则条文写明转 CTC-A005 的情形（CTC-A003 无证据、CTC-L004 边界本身歧义、CTC-P002 无法确定），",
    "规则条文写明转 CTC-A005 的情形（CTC-A003 无证据、CTC-L004 边界本身歧义、CTC-P002 无法确定、"
    "CTC-R004 排除的未定义状态与次数、时长），",
)

# v5 — after the adversarial review of v3 and its probes RG-13–RG-17 on v4:
# - RG-13 (「可别…哦」, RG-06 with another intensifier): v4 raised 「可别」 to 「不得」 in 3/3 runs, base
#   0/3. The boundary is stated by function, as the reviewer proposed; 「千万」 stays the only example
#   so RG-13 still tests generalisation
# - §7 steps 6 and 7 name 口语腔 next to 译文腔 (adversarial review, conflict 2)
# Not adopted: narrowing 「把读者当作谈话对象的引导」 to tool descriptions — RG-16 and RG-17 pass 3/3
# on v4 without it
EDITS["S3-bound-v5"] = (
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。"
    "加强禁止或要求的成分（「千万」）不是口语腔。本规则永远低于 S 族。 |",
)
EDITS["S5-flow6"] = (
    "6. **施加自然中文渲染** — 去译文腔、去冗余主语、恢复话题链与连动结构（CTC-R002、CTC-R003）。",
    "6. **施加自然中文渲染** — 去译文腔、去口语腔、去冗余主语、恢复话题链与连动结构（CTC-R002、CTC-R003）。",
)
EDITS["S5-flow7"] = (
    "没有留下译文腔（CTC-R002、CTC-R003）",
    "没有留下译文腔或口语腔（CTC-R002、CTC-R003）",
)

# v6 — after the v5 runs: RG-13 still raised 「可别」 to 「不得」 in 2/3 runs. The model does not
# delete the prohibition; it renders it in the written form, 「不得」, which G-R-009's gold counts as a
# raise. The boundary now names the repair. RG-18 (「绝对别」) and RG-19 (「别」) are its
# generalisation probes; RG-06 and RG-13 the regression probes
EDITS["S3-bound-v6"] = (
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。 |",
    "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。"
    "去口语腔时禁止的强度不变：「千万不要」「可别」这类口语禁止保留原词或改作「切勿」，"
    "不改作「不得」「禁止」。本规则永远低于 S 族。 |",
)

VARIANTS = {
    # class only: tells whether the boundary sentence is load-bearing
    "v1-class": ["S1a", "S1b", "S2", "S3-class", "S3-ladder"],
    # class plus boundary sentence
    "v1": ["S1a", "S1b", "S2", "S3-class", "S3-ladder", "S3-bound"],
    "v2": ["S1a", "S1b", "S2", "S3-class-v2", "S3-ladder", "S3-bound-v2"],
    "v3": ["S1a", "S1b", "S2-v3", "S3-class-v3", "S3-ladder", "S3-bound-v2"],
    "v4": ["S1a", "S1b", "S2-v4", "S3-class-v4", "S3-ladder-v4", "S3-bound-v2", "S4-routing"],
    "v5": ["S1a", "S1b", "S2-v4", "S3-class-v4", "S3-ladder-v4", "S3-bound-v5", "S4-routing",
           "S5-flow6", "S5-flow7"],
    "v6": ["S1a", "S1b", "S2-v4", "S3-class-v4", "S3-ladder-v4", "S3-bound-v6", "S4-routing",
           "S5-flow6", "S5-flow7"],
}


def build(names):
    text = BASE
    for name in names:
        old, new = EDITS[name]
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{name}: expected 1 match, found {n}")
        text = text.replace(old, new)
    return text


if __name__ == "__main__":
    for var, names in VARIANTS.items():
        out = HERE / var / "SKILL.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(names), encoding="utf-8")
        print(f"wrote {out.relative_to(HERE.parents[3])}  ({', '.join(names)})")

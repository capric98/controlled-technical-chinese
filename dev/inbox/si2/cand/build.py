#!/usr/bin/env python3
"""Rebuild the si2 candidates from the baseline by exact string replacement.

usage: python3 dev/inbox/si2/cand/build.py
Writes dev/inbox/si2/cand/{full,noE2}/SKILL.md. Every edit must match exactly once.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (HERE.parent / "base" / "SKILL.md").read_text(encoding="utf-8")

EDITS = {
    # E1 — review routing: the three rows that already say "转/按 CTC-A005" are cited as A005;
    # P002 findings are kept for parts the source or context determines (fork in PR-01/03/07)
    "E1": (
        "2. 逐句定位违规，每条违规确定唯一的规则 ID；同一处触发多条规则时分列，不合并。",
        "2. 逐句定位违规，每条违规确定唯一的规则 ID；同一处触发多条规则时分列，不合并。"
        "规则行写明转 CTC-A005 的情形（CTC-A003 无证据、CTC-L004 边界本身歧义、CTC-P002 无法确定）"
        "引用 CTC-A005；CTC-P002 的 finding 只针对来源或上下文能确定、却没有写出的部分。",
    ),
    # E2 — P002 boundary: a named object is not "missing" for lack of instance-level detail
    # (G-R-007 false positive; same pattern in PR-01/03/07)
    "E2": (
        "命令已完整表达动作与对象时不再补写自然语言描述。 |",
        "命令已完整表达动作与对象时不再补写自然语言描述。"
        "步骤已写出对象时，不因它没有细化到实例、路径或命名空间就算缺少对象或位置，"
        "除非来源或上下文给出了多个可选对象。 |",
    ),
    # E3 — register in error, alert and status text (G-R-011: no rule licensed removing 「糟糕！」)
    "E3": (
        "| CTC-R003 | 应 | 反译文腔 | 文本含无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
        "过长的「的」字串、英语从句语序残留（「由于…的事实」）或直译连接词时，",
        "| CTC-R003 | 应 | 反译文腔与口语化 | 文本含无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
        "过长的「的」字串、英语从句语序残留（「由于…的事实」）或直译连接词，"
        "或告警、错误与状态提示含情绪化感叹与口语语气词（「糟糕！」「啦」）时，",
    ),
    "E3b": (
        "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。本规则永远低于 S 族。",
        "被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。"
        "表达推测的词（「好像」「可能」）不是语气词，删改时其不确定性按 CTC-S003 保留。本规则永远低于 S 族。",
    ),
}

# v2 — after the three independent reviews (dev/inbox/si2/review/, rulings in adjudication.md)
EDITS["E1v2"] = (
    EDITS["E1"][0],
    "2. 逐句定位违规，每条违规确定唯一的规则 ID；同一处触发多条规则时分列，不合并。"
    "规则条文写明转 CTC-A005 的情形（CTC-A003 无证据、CTC-L004 边界本身歧义、CTC-P002 无法确定），"
    "finding 的规则字段填 CTC-A005，不另列原规则；CTC-P002 的 finding 只针对来源或上下文能确定、却没有写出的部分。",
)
EDITS["E2v2"] = (
    EDITS["E2"][0],
    "命令已完整表达动作与对象时不再补写自然语言描述。"
    "步骤已写出具体对象、只是未细化到实例、节点、环境、路径或命名空间时，不算缺少对象或位置，"
    "也不因此按 CTC-A005 报告；来源或上下文在对象或这些层级上给出了多个候选时除外。"
    "「相关配置」「对应服务」这类说法不算写出对象。 |",
)
EDITS["E3v2"] = (
    "| CTC-R003 | 应 | 反译文腔 | 文本含无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
    "过长的「的」字串、英语从句语序残留（「由于…的事实」）或直译连接词时，"
    "在语义完全不变的前提下改用中文技术写作的常规表达。",
    "| CTC-R003 | 应 | 反译文腔与情绪化 | 文本含无必要的被动、名词化赘语（进行／作出／予以 + 动词）、"
    "过长的「的」字串、英语从句语序残留（「由于…的事实」）或直译连接词时，"
    "在语义完全不变的前提下改用中文技术写作的常规表达；"
    "目标文本是告警、错误信息或状态提示且含情绪化感叹（「糟糕！」）时，删去该感叹。",
)

# v3 — PR-17 showed v2 deleting 「糟糕！」 from a reply quoted inside an agent instruction (3/3)
EDITS["E3v3"] = (
    EDITS["E3v2"][0],
    EDITS["E3v2"][1].replace(
        "目标文本是告警、错误信息或状态提示且含情绪化感叹（「糟糕！」）时，删去该感叹。",
        "目标文本本身是告警、错误信息或状态提示且含情绪化感叹（「糟糕！」）时，删去该感叹；"
        "其他文本中引述或规定的提示文字不在此列。"),
)

# v4 — three clarifying clauses after the v2 decode (decode-v2.yaml) and the v3 self-hosting review
# E1b: routing to A005 is citing A005, not an escalation (self-host finding 7; adversarial conflict 1)
EDITS["E1b"] = (
    "没有其他升级，也没有降级。",
    "没有其他升级，也没有降级。按第 2 步转为 CTC-A005 的 finding 按 CTC-A005 定级，不算升级。",
)
# E2v4: "多个候选" read as any value present vs only alternatives named for the step (decode-v2 probe 2 B)
EDITS["E2v4"] = (
    EDITS["E2v2"][0],
    EDITS["E2v2"][1].replace("来源或上下文在对象或这些层级上给出了多个候选时除外。",
                             "来源或上下文在对象或这些层级上出现多个可能的取值时除外。"),
)
# E3v4: 「啦」 read as an emotional interjection (decode-v2 probe 3 A, probe 7); warning markers (naturalness review)
EDITS["E3v4"] = (
    EDITS["E3v3"][0],
    EDITS["E3v3"][1].replace("其他文本中引述或规定的提示文字不在此列。",
                             "其他文本中引述或规定的提示文字、警示标记（「危险！」）与语气词不在此列。"),
)

VARIANTS = {
    "full": ["E1", "E2", "E3", "E3b"],
    "noE2": ["E1", "E3", "E3b"],
    "v2": ["E1v2", "E2v2", "E3v2"],
    "v3": ["E1v2", "E2v2", "E3v3"],
    "v4": ["E1v2", "E1b", "E2v4", "E3v4"],
}

# v5 — G-R-009 under v4 kept 「哦」「帮忙…一下」 verbatim in an agent instruction that base and v3
# cleaned: 「与语气词不在此列」 read as a ban on touching modal particles anywhere. Drop that half.
EDITS["E3v5"] = (
    EDITS["E3v3"][0],
    EDITS["E3v3"][1].replace("其他文本中引述或规定的提示文字不在此列。",
                             "其他文本中引述或规定的提示文字与警示标记（「危险！」）不在此列。"),
)
VARIANTS["v5"] = ["E1v2", "E1b", "E2v4", "E3v5"]
VARIANTS["v5-noE3"] = ["E1v2", "E1b", "E2v4"]   # ablation: does any R003 edit move G-R-009/010, G-S-001?

# final — E3 withdrawn: every E3 wording (v3, v4, v5) fixed G-R-011 (9/9) and cost G-R-010 (2/9 vs 6/7
# without it). The register gap behind G-R-009/010/011 is an open proposal, not part of si2.
VARIANTS["final"] = ["E1v2", "E1b", "E2v4"]


def build(keys):
    text = BASE
    for k in keys:
        old, new = EDITS[k]
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{k}: expected 1 match, found {n}")
        text = text.replace(old, new)
    return text


for name, keys in VARIANTS.items():
    out = HERE / name / "SKILL.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(build(keys), encoding="utf-8")
    print(f"wrote {out.relative_to(HERE.parent.parent.parent.parent)} ({'+'.join(keys)})")

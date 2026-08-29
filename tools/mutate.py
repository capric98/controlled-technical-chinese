#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Mutation testing for CTC reviewers (000-design.md section 16).

Injects one known defect of a known class into a clean source text, so that a
review pass can be scored on *detection rate per mutation class* rather than on
overall impression. The point of the corpus is diagnostic: a reviewer that
repeatedly misses one class must not be trusted alone for that class.

Every mutant is a defect by construction, so its expected finding is known
without a judge. Mutants are still `provenance: generated-mutation` and do not
gate a release until reviewed — a lexical operator can produce an unnatural
sentence, and an unfair case is worse than no case.

    uv run tools/mutate.py --from eval/gold --out eval/mutations/generated.yaml
    uv run tools/mutate.py --text "仅当连续失败 3 次时，才切换到备用集群。"
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Mutation:
    cls: str
    text: str
    locus: str
    expected: str


Operator = tuple[str, str]  # (mutation class, human-readable expected finding)


def _sub_first(text: str, pattern: str, repl: str) -> tuple[str, str] | None:
    m = re.search(pattern, text)
    if not m:
        return None
    return text[: m.start()] + re.sub(pattern, repl, m.group(0)) + text[m.end() :], m.group(0)


# (class, pattern, replacement, expected finding)
LEXICAL_OPERATORS: list[tuple[str, str, str, str]] = [
    ("modality_strengthen", r"建议", "必须", "建议（推荐）被强化为必须（义务）"),
    ("modality_strengthen", r"(?<!不)可以", "必须", "可以（许可）被强化为必须（义务）"),
    ("modality_strengthen", r"宜", "必须", "宜（推荐）被强化为必须（义务）"),
    ("modality_weaken", r"必须", "建议", "必须（义务）被弱化为建议（推荐）"),
    ("modality_weaken", r"不得", "应尽量避免", "不得（禁止）被弱化为defeasible的规避建议"),
    ("modality_weaken", r"禁止", "不建议", "禁止被弱化为不建议"),
    ("certainty_inflate", r"(?<!尽)可能会", "会", "可能性被改写为确定性"),
    ("certainty_inflate", r"(?<!尽)可能(?!会)", "会", "可能性被改写为确定性"),
    ("certainty_inflate", r"预计", "将", "预测被改写为确定的未来事实"),
    ("certainty_inflate", r"疑似", "确认为", "推测被改写为已确认结论"),
    # 仅当 X 时，才 Y  ->  当 X 时，Y ; dropping 才 too, otherwise the gate survives
    ("condition_broaden", r"仅当([^，。]{1,40})时，([^。]{0,12}?)才", r"当\1时，\2",
     "必要条件（仅当…才）被放宽为一般条件"),
    ("condition_broaden", r"仅当", "当", "必要条件（仅当）被放宽为一般条件"),
    ("condition_broaden", r"连续失败\s*\d+\s*次", "失败", "连续失败 N 次的门控被放宽为单次失败即触发"),
    # deleting the counter outright, rather than substituting a word, is the only
    # variant that stays grammatical when 连续 N 次 modifies a following verb
    ("condition_broaden", r"连续\s*\d+\s*次\s*", "", "连续 N 次的门控被删除，单次即触发"),
    ("condition_broaden", r"除[^，。；]{1,12}外[，、]?", "", "例外集合被删除，义务范围被扩大"),
    ("threshold_flip", r"达到", "超过", "闭区间边界被改为开区间，等于阈值时的行为改变"),
    ("threshold_flip", r"不低于", "高于", "包含端点的下界被改为不含端点"),
    ("threshold_flip", r"不超过", "少于", "包含端点的上界被改为不含端点"),
    ("threshold_flip", r"以上", "以内", "比较方向被反转"),
    ("threshold_flip", r"至少", "至多", "下界被改为上界"),
    ("negation_scope", r"不得同时", "均不得", "组合级禁止被改为对每一项的全面禁止"),
    ("causal_inject", r"(?<=[^。；\n])。(?=[^\n]{4,})", "，因此", "并列或时序关系被改写为因果关系"),
    ("causal_inject", r"与([^，。]{2,12})相关", r"由\1导致", "相关性被升级为确定因果"),
    # anchored at ^, so this fires on any text; mutate() restricts it to short
    # single-sentence sources, where a leading 通常 is a plausible model edit
    ("unsourced_qualifier", r"^", "通常", "新增了源文没有的频率判断"),
    ("unsourced_qualifier", r"(?<=[。；\n])(检查|执行|重启|运行)", r"只需\1",
     "新增了源文没有的充分性判断"),
    ("term_substitute", r"撤销", "删除", "撤销与删除是不同的领域概念，被错误归一"),
    ("term_substitute", r"副本", "备份", "副本与备份是不同的领域概念，被错误归一"),
    ("term_substitute", r"重载", "重启", "重载与重启是不同的操作，被错误归一"),
]


def quantity_mutations(text: str) -> list[Mutation]:
    out: list[Mutation] = []
    m = re.search(r"(\d+)\s*(ms|s|秒|毫秒|分钟|次|条|%|GB|MB)", text)
    if m:
        value, unit = m.group(1), m.group(2)
        bumped = str(int(value) + 2) if int(value) < 100 else str(int(value) * 10)
        out.append(Mutation(
            "quantity_drift",
            text[: m.start(1)] + bumped + text[m.end(1) :],
            m.group(0),
            f"数值由 {value} 改为 {bumped}，阈值/次数被改变"))
        swap = {"ms": "s", "s": "ms", "毫秒": "秒", "秒": "毫秒",
                "MB": "GB", "GB": "MB", "次": "条", "条": "次"}.get(unit)
        if swap:
            out.append(Mutation(
                "quantity_drift",
                text[: m.start(2)] + swap + text[m.end(2) :],
                m.group(0),
                f"单位由 {unit} 改为 {swap}，量级被改变"))
    return out


def token_mutations(text: str) -> list[Mutation]:
    out: list[Mutation] = []
    for m in re.finditer(r"`([^`\n]+)`", text):
        span = m.group(1)
        if "_" in span:
            parts = span.split("_")
            camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
            out.append(Mutation(
                "token_mutate",
                text[: m.start(1)] + camel + text[m.end(1) :],
                span,
                f"受保护标记 `{span}` 被改写为 `{camel}`，不再对应真实接口"))
            break
        if re.fullmatch(r"[1-5]\d{2}", span):
            other = str(int(span) + 9)
            out.append(Mutation(
                "token_mutate",
                text[: m.start(1)] + other + text[m.end(1) :],
                span,
                f"状态码 `{span}` 被改为 `{other}`，分支条件改变"))
            break
    return out


def actor_mutations(text: str, actors: list[str]) -> list[Mutation]:
    out: list[Mutation] = []
    for actor in actors:
        idx = text.find(actor)
        if idx == -1:
            continue
        mutated = text[:idx] + text[idx + len(actor) :]
        mutated = re.sub(r"^[，、,]\s*", "", mutated)
        out.append(Mutation(
            "actor_delete", mutated, actor,
            f"施事者「{actor}」被删除；若上下文存在其他可能施事者，动作归属不再唯一"))
        break
    return out


def order_mutations(text: str) -> list[Mutation]:
    """Swap two adjacent numbered steps.

    A free-form clause swap on Chinese prose reliably produces ungrammatical text,
    which tests nothing. Renumbering a procedure is both grammatical by construction
    and a failure real models actually commit.
    """
    steps = re.findall(r"^(\d+)\.\s*(.+)$", text, re.M)
    if len(steps) < 2:
        return []
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if re.match(r"^\d+\.\s", l)]
    if len(idx) < 2:
        return []
    a, b = idx[-2], idx[-1]
    na = re.match(r"^(\d+)\.\s*(.*)$", lines[a])
    nb = re.match(r"^(\d+)\.\s*(.*)$", lines[b])
    if not (na and nb):
        return []
    lines[a] = f"{na.group(1)}. {nb.group(2)}"
    lines[b] = f"{nb.group(1)}. {na.group(2)}"
    return [Mutation(
        "order_swap", "\n".join(lines), f"步骤 {na.group(1)} 与 {nb.group(1)}",
        f"步骤 {na.group(1)} 与 {nb.group(1)} 的执行顺序被互换，越过了必要的前置条件")]


def mutate(text: str, actors: list[str] | None = None, limit: int = 6) -> list[Mutation]:
    found: list[Mutation] = []
    multi_line = "\n" in text.strip()
    for cls, pattern, repl, expected in LEXICAL_OPERATORS:
        leading_label = re.match(r"^[^，。\n]{0,20}：", text) is not None
        if pattern == r"^" and (multi_line or len(text) > 60 or leading_label):
            # a leading label (「警告：」「错误 X：」) cannot take a frequency adverb in front
            continue
        res = _sub_first(text, pattern, repl)
        if res is None:
            continue
        mutated, locus = res
        if mutated.strip() == text.strip():
            continue
        found.append(Mutation(cls, mutated, locus, expected))
    found += order_mutations(text)
    found += quantity_mutations(text)
    found += token_mutations(text)
    found += actor_mutations(text, actors or [])

    # one mutant per class keeps the corpus balanced rather than dominated by
    # whichever class happens to have the most triggering patterns
    seen: set[str] = set()
    balanced: list[Mutation] = []
    for m in found:
        if m.cls not in seen:
            seen.add(m.cls)
            balanced.append(m)
    return balanced[:limit]


def cases_from_gold(gold_dir: Path, per_class_cap: int = 6) -> list[dict]:
    """Cap each class so the corpus is balanced. An operator that matches every
    text would otherwise dominate and the per-class detection rate — the whole
    point of the corpus — would be measured on one class with a long tail."""
    out: list[dict] = []
    counts: dict[str, int] = {}
    seq = 0
    for path in sorted(gold_dir.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for case in doc.get("cases", []):
            if case.get("mode") == "review":
                # a review case's source is an 原文/候选改写 pair that already carries a
                # planted defect; injecting a second one makes the expectation ambiguous
                continue
            source = (case.get("source") or "").strip()
            if not source:
                continue
            actors = [i.get("actor") for i in case.get("invariants", []) if i.get("actor")]
            for m in mutate(source, actors):
                if counts.get(m.cls, 0) >= per_class_cap:
                    continue
                counts[m.cls] = counts.get(m.cls, 0) + 1
                seq += 1
                out.append({
                    "id": f"M-{seq:03d}",
                    "mutation_class": m.cls,
                    "derived_from": case["id"],
                    "task": "review",
                    "mode": "review",
                    "instruction": ("下面给出原文与候选改写。审阅候选改写是否忠实于原文；"
                                    "只输出问题清单，不要整体重写。"),
                    "clean_source": source,
                    # The review sees the pair, not the mutant alone. Drift from an
                    # unseen original is undetectable by construction: 「2 分钟」→「4 分钟」
                    # reads as a perfectly ordinary threshold with no source to compare to.
                    "source": f"原文：\n{source}\n\n候选改写：\n{m.text}",
                    "mutant": m.text,
                    "locus": m.locus,
                    "expected_issues": [{
                        "category": m.cls,
                        "severity": "ERROR",
                        "locus": m.locus,
                        "problem": m.expected,
                    }],
                    "clean_source_is_compliant": bool(case.get("over_edit_trap")),
                    "provenance": "generated-mutation",
                })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="src", default=str(ROOT / "eval" / "gold"))
    ap.add_argument("--out", default=str(ROOT / "eval" / "mutations" / "generated.yaml"))
    ap.add_argument("--text", help="mutate one string and print the result")
    ap.add_argument("--cap", type=int, default=6, help="max mutants per class")
    args = ap.parse_args()

    if args.text:
        for m in mutate(args.text):
            print(f"[{m.cls}] {m.locus!r}\n  {m.text}\n  expect: {m.expected}\n")
        return 0

    cases = cases_from_gold(Path(args.src), args.cap)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(
        yaml.dump({"cases": cases}, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8")
    by_class: dict[str, int] = {}
    for c in cases:
        by_class[c["mutation_class"]] = by_class.get(c["mutation_class"], 0) + 1
    print(f"wrote {args.out} — {len(cases)} mutant(s)")
    for k, v in sorted(by_class.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

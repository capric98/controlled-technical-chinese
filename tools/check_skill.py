#!/usr/bin/env python3
"""Deterministic project checks for SKILL.md.

Covers the checks that `npx skills-ref validate .` does not: rule-ID stability,
development-path leakage, normative-vocabulary discipline, and the line budget.
Dependency-free on purpose — the frontmatter CTC ships is flat scalars only.

Usage:
    python3 tools/check_skill.py [SKILL.md]
Exit code 0 = all gates pass, 1 = at least one ERROR.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "spec" / "rule-ids.txt"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RULE_RE = re.compile(r"CTC-([SAPTLR])(\d{3})")
DEV_PATHS = ["docs/decisions", "AGENTS.md", "spec/", "eval/", "dev/", "tools/", "CLAUDE.md"]
# design 000 section 26: these have no stable strength inside normative instructions
VAGUE_NORMATIVE = ["尽量", "适当地", "必要时", "一般来说", "酌情", "尽可能"]
NORMATIVE_DRIFT = ["务必", "应该", "需要注意"]
LINE_BUDGET = 500

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        err("frontmatter: file does not start with '---'")
        return None, text
    end = text.find("\n---\n", 3)
    if end == -1:
        err("frontmatter: closing '---' delimiter not found")
        return None, text
    return text[4:end], text[end + 5 :]


def parse_flat_yaml(block: str) -> dict:
    """Parse the flat `key: value` frontmatter CTC uses, including block scalars."""
    out: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for raw in block.split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if m and not raw.startswith((" ", "\t")):
            if key is not None:
                out[key] = "\n".join(buf).strip()
            key, first = m.group(1), m.group(2)
            buf = [first] if first not in ("|", ">", "|-", ">-", "") else []
        elif key is not None:
            buf.append(raw.strip())
        elif raw.strip():
            err(f"frontmatter: cannot parse line: {raw!r}")
    if key is not None:
        out[key] = "\n".join(buf).strip()
    return out


def check_frontmatter(fm: dict) -> None:
    name = fm.get("name", "")
    if not name:
        err("frontmatter: `name` is missing or empty")
    else:
        name = name.strip().strip("\"'")
        if not NAME_RE.match(name):
            err(f"frontmatter: `name` {name!r} is not lowercase-hyphen form")
        if len(name) > 64:
            err(f"frontmatter: `name` is {len(name)} chars, limit is 64")
        if name != "controlled-technical-chinese":
            warn(f"frontmatter: `name` is {name!r}; AGENTS.md pins controlled-technical-chinese")

    desc = fm.get("description", "").strip().strip("\"'")
    if not desc:
        err("frontmatter: `description` is missing or empty")
    elif len(desc) > 1024:
        err(f"frontmatter: `description` is {len(desc)} chars, limit is 1024")
    elif len(desc) < 40:
        warn(f"frontmatter: `description` is only {len(desc)} chars; activation may be unreliable")

    for extra in set(fm) - {"name", "description", "license", "allowed-tools", "metadata", "version"}:
        warn(f"frontmatter: unrecognized key {extra!r}")


def check_dev_leakage(body: str) -> None:
    for p in DEV_PATHS:
        if p in body:
            err(f"self-containment: body references development-only path {p!r}")


def check_rule_ids(body: str) -> None:
    ids = RULE_RE.findall(body)
    if not ids:
        warn("rule ids: no CTC-Xnnn identifiers found in the body")
        return
    seen: dict[str, list[int]] = {}
    for fam, num in ids:
        seen.setdefault(fam, []).append(int(num))
    current = set()
    for fam, nums in sorted(seen.items()):
        uniq = sorted(set(nums))
        for n in uniq:
            current.add(f"CTC-{fam}{n:03d}")
        expected = list(range(1, len(uniq) + 1))
        if uniq != expected:
            warn(f"rule ids: family {fam} is {uniq}, not gapless 1..{len(uniq)}")

    if MANIFEST.exists():
        pinned = {
            line.split("#")[0].strip()
            for line in MANIFEST.read_text(encoding="utf-8").splitlines()
            if line.split("#")[0].strip()
        }
        for gone in sorted(pinned - current):
            err(f"rule ids: {gone} is pinned in spec/rule-ids.txt but absent from SKILL.md")
        for added in sorted(current - pinned):
            warn(f"rule ids: {added} is new; add it to spec/rule-ids.txt if it is now stable")
    else:
        warn("rule ids: spec/rule-ids.txt does not exist; ID stability is unenforced")


CITED = re.compile(r"[「『][^」』]{0,12}[」』]")


def check_normative_vocabulary(body: str) -> None:
    for i, line in enumerate(body.split("\n"), 1):
        # a term inside 「」 is being named as something to detect, not used as an
        # instruction — CTC-R004 has to quote the very words it tells the model to flag
        used = CITED.sub(" ", line)
        for term in VAGUE_NORMATIVE:
            if term in used:
                warn(f"normative vocabulary: line {i} uses ambiguous {term!r} — define the trigger or remove")
    for term in NORMATIVE_DRIFT:
        n = body.count(term)
        if n:
            warn(f"normative vocabulary: {term!r} appears {n}x; design 000 section 26 fixes 必须/应/可以")


def check_budget(text: str) -> None:
    n = len(text.rstrip("\n").split("\n"))
    if n > LINE_BUDGET:
        warn(f"budget: SKILL.md is {n} lines, above the {LINE_BUDGET}-line recommendation")
    print(f"  info: {n} lines, {len(text.encode('utf-8'))} bytes")


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "SKILL.md"
    if not target.exists():
        print(f"ERROR  {target} does not exist")
        return 1
    text = target.read_text(encoding="utf-8")

    print(f"checking {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}")
    fm_block, body = split_frontmatter(text)
    if fm_block is not None:
        check_frontmatter(parse_flat_yaml(fm_block))
    check_dev_leakage(body)
    check_rule_ids(body)
    check_normative_vocabulary(body)
    check_budget(text)

    for w in warnings:
        print(f"WARN   {w}")
    for e in errors:
        print(f"ERROR  {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

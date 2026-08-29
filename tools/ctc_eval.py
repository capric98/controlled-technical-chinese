#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""CTC evaluation harness.

Separates deterministic validation from model judgment, per 000-design.md section 24.
Deterministic checks run here in code. Semantic judgment is packaged for an independent
model and never inferred from the candidate's own claims (see eval/disagreements/D001).

Run with uv so the dependency is transient:

    uv run tools/ctc_eval.py check  --source FILE --output FILE
    uv run tools/ctc_eval.py run    --model claude|gpt|gemini [--case-id ID ...]
    uv run tools/ctc_eval.py bundle --run RUN_DIR          # build judge input
    uv run tools/ctc_eval.py report --run RUN_DIR          # summarise verdicts
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "eval" / "gold"
REPORTS = ROOT / "eval" / "reports"
SKILL = ROOT / "SKILL.md"

# ---------------------------------------------------------------- extraction

CODE_BLOCK = re.compile(r"```.*?```", re.S)
CODE_SPAN = re.compile(r"`([^`\n]+)`")
URL = re.compile(r"https?://[^\s，。；：）】」』、,]+")
PATH = re.compile(r"(?<![\w`])(?:\.{0,2}/)[\w./{}\-]+")
FLAG = re.compile(r"(?<![\w-])--?[A-Za-z][\w-]*")
ENV_VAR = re.compile(r"(?<![\w`])[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+(?![\w`])")
DOTTED = re.compile(r"(?<![\w`])[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)+(?![\w`])")
SNAKE = re.compile(r"(?<![\w`])[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?![\w`])")

# numbers keep their unit; a bare number is still compared, with unit ""
UNIT = r"(?:ms|s|m|h|d|%|KB|MB|GB|TB|KiB|MiB|GiB|rpm|qps|次|条|个|台|秒|分钟|小时|天|毫秒|字节)"
NUMBER = re.compile(rf"(\d+(?:\.\d+)?)\s*({UNIT})?")

# threshold boundary vocabulary — an open/closed interval flip is a real defect (F-11)
COMPARATORS = [
    "超过", "达到", "不低于", "不少于", "不超过", "不高于", "至少", "至多", "大于",
    "小于", "不小于", "不大于", "以上", "以下", "以内", "之前", "之后", "满", "起",
]

# modality words grouped by the strength they encode (INV-02)
MODALITY_CLASSES: dict[str, tuple[str, ...]] = {
    "obligation": ("必须", "须", "应当", "应", "需要", "需", "务必", "要求", "确保", "保证"),
    "prohibition": ("不得", "禁止", "严禁", "不可", "不要", "切勿", "不允许"),
    "recommendation": ("建议", "推荐", "最好", "宜"),
    "permission": ("可以", "允许", "可选", "支持"),
    "possibility": ("可能", "或许", "也许", "有可能", "预计"),
    "certainty": ("一定", "必然", "总是", "始终", "肯定"),
    "unsourced_frequency": ("通常", "一般", "默认情况下", "大多数情况下", "最常见"),
}


def strip_code(text: str) -> str:
    return CODE_SPAN.sub(" ", CODE_BLOCK.sub(" ", text))


def protected_tokens(text: str) -> Counter:
    """Machine-readable strings whose exact characters must survive (INV-12)."""
    tokens: Counter = Counter()
    for m in CODE_BLOCK.findall(text):
        tokens[("code_block", m.strip())] += 1
    for m in CODE_SPAN.findall(text):
        tokens[("code_span", m.strip())] += 1
    outside = strip_code(text)
    for kind, pattern in (
        ("url", URL), ("path", PATH), ("flag", FLAG),
        ("env", ENV_VAR), ("dotted", DOTTED), ("snake", SNAKE),
    ):
        for m in pattern.findall(outside):
            tokens[(kind, m)] += 1
    return tokens


def quantities(text: str) -> Counter:
    """(value, unit) pairs. Surface form is preserved by policy: no unit conversion."""
    out: Counter = Counter()
    for value, unit in NUMBER.findall(text):
        out[(value.rstrip("0").rstrip(".") if "." in value else value, unit or "")] += 1
    return out


def comparators(text: str) -> Counter:
    return Counter({c: text.count(c) for c in COMPARATORS if c in text})


def modality_profile(text: str) -> Counter:
    """Count modal strength classes. Longest match wins so 不应 does not read as 应."""
    body = strip_code(text)
    out: Counter = Counter()
    words = sorted(
        ((w, cls) for cls, ws in MODALITY_CLASSES.items() for w in ws),
        key=lambda p: -len(p[0]),
    )
    remaining = body
    for word, cls in words:
        n = remaining.count(word)
        if n:
            out[cls] += n
            remaining = remaining.replace(word, "\x00" * len(word))
    return out


# ---------------------------------------------------------------- checking

@dataclass
class Check:
    name: str
    severity: str          # ERROR | WARNING | INFO
    passed: bool
    detail: str = ""


@dataclass
class CheckResult:
    checks: list[Check] = field(default_factory=list)

    @property
    def errors(self) -> list[Check]:
        return [c for c in self.checks if not c.passed and c.severity == "ERROR"]

    def as_dict(self) -> dict:
        return {
            "passed": not self.errors,
            "checks": [vars(c) for c in self.checks],
        }


def diff_counter(a: Counter, b: Counter) -> str:
    lost = a - b
    added = b - a
    parts = []
    if lost:
        parts.append("lost " + ", ".join(f"{k!r}x{v}" for k, v in sorted(lost.items(), key=str)))
    if added:
        parts.append("added " + ", ".join(f"{k!r}x{v}" for k, v in sorted(added.items(), key=str)))
    return "; ".join(parts)


def deterministic_checks(source: str, output: str, case: dict | None = None) -> CheckResult:
    res = CheckResult()
    case = case or {}

    allowed = set(case.get("authorized_token_changes", []) or [])

    st, ot = protected_tokens(source), protected_tokens(output)
    st = Counter({k: v for k, v in st.items() if k[1] not in allowed})
    ot = Counter({k: v for k, v in ot.items() if k[1] not in allowed})
    res.checks.append(Check(
        "protected_tokens", "ERROR", st == ot, diff_counter(st, ot)))

    sq, oq = quantities(source), quantities(output)
    res.checks.append(Check(
        "quantities", "ERROR", sq == oq, diff_counter(sq, oq)))

    sc, oc = comparators(source), comparators(output)
    res.checks.append(Check(
        "threshold_boundaries", "WARNING", sc == oc, diff_counter(sc, oc)))

    sm, om = modality_profile(source), modality_profile(output)
    res.checks.append(Check(
        "modality_profile", "WARNING", sm == om, diff_counter(sm, om)))

    # explicitly listed required tokens, when a case pins them
    required = case.get("protected_tokens") or []
    missing = [t for t in required if t not in output]
    res.checks.append(Check(
        "case_protected_tokens", "ERROR", not missing,
        f"missing from output: {missing}" if missing else ""))

    return res


# ---------------------------------------------------------------- model adapters

def _run(cmd: list[str], stdin: str | None = None, cwd: str | None = None, timeout: int = 1500) -> str:
    p = subprocess.run(
        cmd, input=stdin, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} exited {p.returncode}: {p.stderr[-2000:]}")
    return p.stdout


def call_model(model: str, prompt: str) -> str:
    """Run each model in a scratch cwd so no repository instruction file leaks in."""
    with tempfile.TemporaryDirectory() as scratch:
        if model == "claude":
            return _run(["claude", "-p", prompt], cwd=scratch)
        if model == "gemini":
            return _run(
                ["agy", "-p", prompt, "--model", "gemini-3.7-flash-high",
                 "--print-timeout", "20m"], cwd=scratch)
        if model == "gpt":
            out = Path(scratch) / "last.txt"
            _run(["codex", "exec", "-m", "gpt-5.6-sol",
                  "-c", "model_reasoning_effort=high", "-s", "read-only",
                  "--skip-git-repo-check", "-C", scratch, "-o", str(out), prompt],
                 cwd=scratch)
            return out.read_text(encoding="utf-8")
    raise ValueError(f"unknown model {model!r}")


def skill_body() -> str:
    text = SKILL.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 3)
        if end != -1:
            return text[end + 5 :]
    return text


def build_prompt(case: dict) -> str:
    task = case.get("task", "rewrite")
    mode = case.get("mode", "strict")
    instruction = case.get("instruction") or {
        "rewrite": f"请以 {mode} 模式改写下面的文本。",
        "translate": f"请以 {mode} 模式把下面的文本翻译成中文。",
        "review": "请以 review 模式审阅下面的文本，只输出问题清单，不要整体重写。",
        "author": f"请以 {mode} 模式按要求写作。",
    }[task]
    return (
        "以下是你必须遵循的技能说明。\n\n"
        "<skill>\n" + skill_body().strip() + "\n</skill>\n\n"
        f"任务：{instruction}\n"
        "只输出结果本身，不要解释你的处理过程。\n\n"
        "<input>\n" + case["source"].strip() + "\n</input>\n"
    )


# ---------------------------------------------------------------- cases

def load_cases(case_ids: list[str] | None = None) -> list[dict]:
    cases: list[dict] = []
    for path in sorted(GOLD.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for c in doc.get("cases", []):
            c["_file"] = path.name
            cases.append(c)
    if case_ids:
        wanted = set(case_ids)
        cases = [c for c in cases if c["id"] in wanted]
    return cases


# ---------------------------------------------------------------- commands

def cmd_check(args) -> int:
    source = Path(args.source).read_text(encoding="utf-8")
    output = Path(args.output).read_text(encoding="utf-8")
    res = deterministic_checks(source, output)
    for c in res.checks:
        mark = "pass" if c.passed else c.severity
        print(f"{mark:8} {c.name}" + (f"  — {c.detail}" if c.detail else ""))
    return 1 if res.errors else 0


def cmd_run(args) -> int:
    if not SKILL.exists():
        print("SKILL.md does not exist yet", file=sys.stderr)
        return 1
    cases = load_cases(args.case_id)
    if not cases:
        print("no cases matched", file=sys.stderr)
        return 1
    run_dir = REPORTS / "raw" / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for case in cases:
        target = run_dir / f"{case['id']}.{args.model}.json"
        if target.exists() and not args.force:
            print(f"skip   {case['id']} ({args.model}) — already present")
            continue
        try:
            output = call_model(args.model, build_prompt(case)).strip()
        except Exception as exc:  # noqa: BLE001 — a dead model must not abort the sweep
            print(f"ERROR  {case['id']} ({args.model}): {exc}")
            failures += 1
            continue
        res = deterministic_checks(case["source"], output, case)
        target.write_text(json.dumps({
            "case_id": case["id"], "model": args.model, "mode": case.get("mode"),
            "task": case.get("task"), "source": case["source"], "output": output,
            "deterministic": res.as_dict(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        state = "FAIL" if res.errors else "ok"
        print(f"{state:6} {case['id']} ({args.model})"
              + ("  " + "; ".join(f"{c.name}: {c.detail}" for c in res.errors) if res.errors else ""))
        failures += bool(res.errors)
    print(f"\n{len(cases)} case(s), {failures} deterministic failure(s)")
    return 0


def cmd_bundle(args) -> int:
    run_dir = REPORTS / "raw" / args.run_id
    cases = {c["id"]: c for c in load_cases()}
    bundle = []
    for path in sorted(run_dir.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        case = cases.get(rec["case_id"], {})
        bundle.append({
            "case_id": rec["case_id"],
            "model": rec["model"],
            "task": rec.get("task"),
            "mode": rec.get("mode"),
            "source": rec["source"],
            "output": rec["output"],
            "invariants": case.get("invariants", []),
            "expected_issues": case.get("expected_issues", []),
            "over_edit_trap": case.get("over_edit_trap", False),
            "deterministic_failures": [
                c["name"] for c in rec["deterministic"]["checks"]
                if not c["passed"] and c["severity"] == "ERROR"
            ],
        })
    out = run_dir.parent.parent / f"bundle-{args.run_id}.json"
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} — {len(bundle)} record(s)")
    return 0


def cmd_report(args) -> int:
    run_dir = REPORTS / "raw" / args.run_id
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(run_dir.glob("*.json"))]
    by_model: dict[str, Counter] = {}
    for r in rows:
        c = by_model.setdefault(r["model"], Counter())
        c["total"] += 1
        for chk in r["deterministic"]["checks"]:
            if not chk["passed"]:
                c[f"{chk['severity'].lower()}:{chk['name']}"] += 1
    for model, counts in sorted(by_model.items()):
        print(f"\n{model}: {counts['total']} case(s)")
        for k, v in sorted(counts.items()):
            if k != "total":
                print(f"  {k}: {v}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="deterministic checks on one source/output pair")
    c.add_argument("--source", required=True)
    c.add_argument("--output", required=True)
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("run", help="run gold cases through SKILL.md with one model")
    r.add_argument("--model", required=True, choices=["claude", "gpt", "gemini"])
    r.add_argument("--run-id", default="latest")
    r.add_argument("--case-id", action="append")
    r.add_argument("--force", action="store_true")
    r.set_defaults(fn=cmd_run)

    b = sub.add_parser("bundle", help="package a run for independent semantic judging")
    b.add_argument("--run-id", default="latest")
    b.set_defaults(fn=cmd_bundle)

    p = sub.add_parser("report", help="summarise deterministic outcomes for a run")
    p.add_argument("--run-id", default="latest")
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())

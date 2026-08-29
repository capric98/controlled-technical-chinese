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
    uv run tools/ctc_eval.py judge  --run RUN_DIR --judge gpt
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
JUDGE_PROMPT = ROOT / "dev" / "prompts" / "judge-semantic.v1.md"

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


RULE_ID = re.compile(r"CTC-[SAPTLR]\d{3}")
LIST_MARKER = re.compile(r"^\s{0,3}\d+[.、)]\s", re.M)


def quantities(text: str) -> Counter:
    """(value, unit) pairs. Surface form is preserved by policy: no unit conversion.

    Rule IDs and Markdown list markers are stripped first. Without that, `CTC-L001`
    contributes a quantity `001` and a renumbered procedure looks like numeric drift —
    both fired on every review-mode output in the first sweep.
    """
    text = LIST_MARKER.sub(" ", RULE_ID.sub(" ", text))
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
    review = case.get("mode") == "review"

    allowed = set(case.get("authorized_token_changes", []) or [])

    st, ot = protected_tokens(source), protected_tokens(output)
    st = Counter({k: v for k, v in st.items() if k[1] not in allowed})
    ot = Counter({k: v for k, v in ot.items() if k[1] not in allowed})
    sq, oq = quantities(source), quantities(output)

    if review:
        # A review output is a findings list, not the document. Comparing its token
        # or quantity inventory against the source is meaningless: it quotes some
        # loci and omits everything it had no finding about. Only check that it did
        # not invent a protected token that appears nowhere in the source.
        invented = {k for k in ot if k[0] != "code_block" and k not in st and k[1] not in source}
        res.checks.append(Check(
            "review_no_invented_tokens", "WARNING", not invented,
            f"tokens absent from source: {sorted(k[1] for k in invented)}" if invented else ""))
    else:
        # Losing a protected token or a quantity is a defect. Repeating one is not:
        # repeating a modifier across both conjuncts is the correct repair for an
        # attachment ambiguity, and it raises the count of a quantity already present.
        res.checks.append(Check(
            "protected_tokens_lost", "ERROR", not (st - ot), diff_counter(st, ot & st)))
        res.checks.append(Check(
            "protected_tokens_added", "WARNING", not (set(ot) - set(st)),
            diff_counter(Counter({k: v for k, v in st.items() if k in ot}), ot)))
        res.checks.append(Check(
            "quantities_lost", "ERROR", not (set(sq) - set(oq)), diff_counter(sq, oq & sq)))
        res.checks.append(Check(
            "quantities_added", "WARNING", not (set(oq) - set(sq)),
            diff_counter(Counter({k: v for k, v in sq.items() if k in oq}), oq)))

    sc, oc = comparators(source), comparators(output)
    res.checks.append(Check(
        "threshold_boundaries", "WARNING", sc == oc, diff_counter(sc, oc)))

    sm, om = modality_profile(source), modality_profile(output)
    res.checks.append(Check(
        "modality_profile", "WARNING", sm == om, diff_counter(sm, om)))

    # explicitly listed required tokens, when a case pins them
    if not review:
        required = case.get("protected_tokens") or []
        missing = [t for t in required if t.strip("`") not in output]
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


def cmd_recheck(args) -> int:
    """Re-run deterministic checks over saved outputs. No model calls."""
    run_dir = REPORTS / "raw" / args.run_id
    cases = {c["id"]: c for c in load_cases()}
    changed = 0
    for path in sorted(run_dir.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        case = cases.get(rec["case_id"], {})
        before = rec["deterministic"]["passed"]
        res = deterministic_checks(rec["source"], rec["output"], case)
        rec["deterministic"] = res.as_dict()
        path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        changed += before != res.as_dict()["passed"]
    print(f"rechecked {args.run_id}: {changed} verdict(s) changed")
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


def strip_fences(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```(?:ya?ml|json)?\n(.*?)\n```$", text, re.S)
    return m.group(1) if m else text


def cmd_judge(args) -> int:
    """Semantic judging by a model that did not produce the outputs (decision 002)."""
    bundle_path = REPORTS / f"bundle-{args.run_id}.json"
    if not bundle_path.exists():
        print(f"{bundle_path} missing — run `bundle` first", file=sys.stderr)
        return 1
    records = json.loads(bundle_path.read_text(encoding="utf-8"))
    records = [r for r in records if r["model"] != args.judge] if args.exclude_self else records
    if not records:
        print("nothing to judge", file=sys.stderr)
        return 1

    prompt_head = JUDGE_PROMPT.read_text(encoding="utf-8")
    verdicts: list[dict] = []
    for i in range(0, len(records), args.batch):
        batch = records[i : i + args.batch]
        ids = ", ".join(r["case_id"] for r in batch)
        prompt = (prompt_head + "\n\n## Records to judge\n\n```json\n"
                  + json.dumps(batch, ensure_ascii=False, indent=2) + "\n```\n")
        print(f"judging batch {i // args.batch + 1}: {ids}")
        try:
            raw = call_model(args.judge, prompt)
            parsed = yaml.safe_load(strip_fences(raw)) or {}
            got = parsed.get("verdicts", [])
            if not isinstance(got, list):
                raise ValueError("verdicts is not a list")
            verdicts.extend(got)
        except Exception as exc:  # noqa: BLE001 — one bad batch must not lose the rest
            print(f"  ERROR judging {ids}: {exc}")
            (REPORTS / f"judge-error-{args.run_id}-{i}.txt").write_text(
                str(exc), encoding="utf-8")

    out = REPORTS / f"verdicts-{args.run_id}.{args.judge}.yaml"
    out.write_text(yaml.dump({"judge": args.judge, "run": args.run_id,
                              "prompt": JUDGE_PROMPT.name, "verdicts": verdicts},
                             allow_unicode=True, sort_keys=False), encoding="utf-8")
    failed = [v for v in verdicts if v.get("overall") == "fail"]
    print(f"\nwrote {out.relative_to(ROOT)} — {len(verdicts)} verdict(s), {len(failed)} fail")
    for v in failed:
        print(f"  fail  {v.get('case_id')} ({v.get('model')}): {v.get('failure_kinds')}")
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

    rc = sub.add_parser("recheck", help="re-run deterministic checks over saved outputs")
    rc.add_argument("--run-id", default="latest")
    rc.set_defaults(fn=cmd_recheck)

    b = sub.add_parser("bundle", help="package a run for independent semantic judging")
    b.add_argument("--run-id", default="latest")
    b.set_defaults(fn=cmd_bundle)

    j = sub.add_parser("judge", help="independent semantic judging of a bundle")
    j.add_argument("--run-id", default="latest")
    j.add_argument("--judge", required=True, choices=["claude", "gpt", "gemini"])
    j.add_argument("--batch", type=int, default=6)
    j.add_argument("--exclude-self", action="store_true",
                   help="skip records produced by the judging model itself")
    j.set_defaults(fn=cmd_judge)

    p = sub.add_parser("report", help="summarise deterministic outcomes for a run")
    p.add_argument("--run-id", default="latest")
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())

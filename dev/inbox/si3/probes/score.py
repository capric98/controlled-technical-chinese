#!/usr/bin/env python3
"""Score the si3 probe runs against the expectations registered in probes.yaml and resolutions.yaml.

usage: python3 dev/inbox/si3/probes/score.py VARIANT [VARIANT ...]
Prints one row per probe and variant: pass count over the replicates, then a short note per run.
Only features that can be checked on the surface are scored here: a token kept or removed, a body
unchanged, the rule ID cited at a locus. Anything that needs judgment (RG-03: no added facts) is
flagged 「check」 and read by hand; the summary in eval/reports/si3-summary.md records the reading.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "eval" / "reports" / "raw"


def body_and_pending(out):
    body, sep, pending = out.partition("待确认")
    return body.strip(), pending if sep else ""


def findings(out):
    """Split a review output into findings: (rule, severity, location) per finding."""
    rules = [(m.start(), m.group(1)) for m in re.finditer(r"规则\**[：:]\s*\**`?(CTC-[SAPTLR]\d{3})", out)]
    if not rules:
        # a finding headed by the rule ID alone: 「**CTC-R004**」 on its own line, fields below
        rules = [(m.start(), m.group(1))
                 for m in re.finditer(r"^\s*(?:\d+\.\s*)?\**`?(CTC-[SAPTLR]\d{3})`?"
                                      r"(?:\s*[|｜/]\s*(?:ERROR|WARNING|STYLE))?\**\s*$", out, re.M)]
    res = []
    for i, (pos, rule) in enumerate(rules):
        end = rules[i + 1][0] if i + 1 < len(rules) else len(out)
        chunk = out[pos:end]
        sev = re.search(r"(ERROR|WARNING|STYLE)", chunk)
        loc = re.search(r"位置\**[：:]\s*\**(.*)", chunk)
        res.append((rule, sev.group(1) if sev else "?", loc.group(1) if loc else ""))
    # a findings table: | 规则 | 严重级别 | 位置 | 问题 | 风险 | 建议修改 |
    for m in re.finditer(r"^\|(?:\s*\d+\s*\|)?\s*`?(CTC-[SAPTLR]\d{3})`?\s*\|\s*(ERROR|WARNING|STYLE)[^|]*\|([^|]*)\|", out, re.M):
        res.append((m.group(1), m.group(2), m.group(3)))
    # a one-line header: 「**CTC-A005 · ERROR · 「确认流量正常」**」
    for m in re.finditer(r"^\**(CTC-[SAPTLR]\d{3})\s*[·|｜/]\s*(ERROR|WARNING|STYLE)\s*[·|｜/]\s*(.+?)\**\s*$", out, re.M):
        res.append((m.group(1), m.group(2), m.group(3)))
    return res


def rules_at(out, needle):
    return sorted({r for r, _s, loc in findings(out) if needle in loc})


def first_line(out):
    return re.sub(r"[*`#\s]", "", out.strip().split("\n", 1)[0])


def score(pid, rec):
    out, src = rec["output"], rec["source"].strip()
    body, pending = body_and_pending(out)
    if pid == "ST-01" or pid == "ST-02":
        fl = first_line(out)
        return fl == "strict", fl
    if pid == "R4-01":
        got = {w: rules_at(out, w) for w in ("必要时", "尽快", "视情况")}
        ok = all(got[w] and "CTC-R004" in got[w] for w in got)
        note = " ".join(f"{w}={'+'.join(r) or '-'}" for w, r in got.items())
        return ok, note
    if pid == "R4-02":
        missing = [w for w in ("必要时", "尽快", "视情况") if w not in pending]
        return body == src and not missing, ("unchanged" if body == src else "edited") + (
            f" missing:{missing}" if missing else "")
    if pid == "R4-03":
        r = rules_at(out, "尽快")
        return "CTC-R004" not in r, "clean" if "未发现违规" in out else f"尽快={'+'.join(r) or '-'}"
    if pid == "PR-07":
        a, b = rules_at(out, "一段时间"), rules_at(out, "流量正常")
        ok = bool(a) and bool(b) and "CTC-R004" not in a + b
        return ok, f"一段时间={'+'.join(a) or '-'} 流量正常={'+'.join(b) or '-'}"
    if pid == "PR-16":
        return "危险！" in body, "kept" if "危险！" in body else "removed"
    if pid == "PR-17":
        q = "「糟糕！订单没提交成功，请稍后再试。」"
        return q in body, "quote intact" if q in body else "quote edited"
    if pid == "PR-18":
        ok = any(w in body for w in ("吧", "可能", "疑", "推测", "或许", "估计"))
        return ok, "hedge kept" if ok else "hedge lost"
    if pid == "PR-19":
        want = "`payment-api` 返回 502，请稍后重试。"
        return body == want, "exact" if body == want else ("糟糕 kept" if "糟糕" in body else body)
    if pid in ("RG-01", "RG-04"):
        return body == src, "unchanged" if body == src else body
    if pid == "RG-02":
        ok = "你是部署助手" in body and not re.search(r"禁止|不得", body)
        return ok, ("unchanged" if body == src else "edited") + ("" if ok else " FAIL")
    if pid == "RG-03":
        # 「可以用此工具查询…」 keeps the guidance frame without 「你」; the registered expectation is
        # a declarative description, so any 「用/使用 + 此/这个/该 + 工具」 frame counts as left over
        left = [w for w in ("你可以", "一下", "就行", "啦", "传给它") if w in body]
        left += re.findall(r"(?:用|使用)(?:此|这个|该)工具", body)
        return (not left) and body != src, ("left:" + ",".join(left)) if left else "check facts: " + body
    if pid == "RG-05":
        lost = [w for w in ("啦", "哦", "一下", "！") if w not in body]
        return not lost, "kept" if not lost else f"lost:{lost}"
    if pid == "RG-06":
        strength_ok = bool(re.search(r"千万不要|千万别|切勿|绝不", body)) and not re.search(r"禁止|不得|必须|严禁", body)
        particle = "哦 removed" if "哦" not in body else "哦 kept"
        return strength_ok, particle + ("" if strength_ok else " STRENGTH CHANGED: " + body)
    if pid == "RG-07":
        want_ok = "啦" not in body and "共导入 120 条记录" in body and "同步完成" in body
        return want_ok, "啦 removed" if "啦" not in body else "啦 kept"
    if pid == "RG-08":
        frame = re.findall(r"允许您|您可以|调用者可以|允许调用者|让您", body)
        ok = not frame and "每次最多 500 个" in body
        return ok, (f"frame left:{frame}" if frame else "direct: " + body)
    if pid == "RG-10":
        frame = re.findall(r"开发者可以|调用者可以|调用方可|通过这个函数|你可以|可通过", body)
        ok = not frame and "4096" in body and "最大支持 4096 像素" in body and "哦" not in body
        return ok, (f"frame left:{frame}" if frame else ("哦 kept" if "哦" in body else "direct: " + body))
    if pid == "RG-11":
        return body == src, "unchanged" if body == src else body
    if pid == "RG-12":
        kept = bool(re.search(r"(只有|仅|仅限|只允许|仅允许).{0,6}管理员", body)) and "管理员" in body
        frame = re.findall(r"可以帮你|帮你|哦", body)
        return kept and not frame, ("restriction kept" if kept else "RESTRICTION LOST") + (
            f" left:{frame}" if frame else "") + ": " + body
    if pid == "RG-13":
        raised = re.search(r"禁止|不得|必须|严禁", body)
        return not raised and "API_KEY" in body, ("STRENGTH RAISED: " + body) if raised else body
    if pid == "RG-14":
        ok = "允许" in body and not re.search(r"应|须|必须", body)
        return ok, ("一下 removed, " if "一下" not in body else "一下 kept, ") + ("permission kept" if ok else "PERMISSION LOST: " + body)
    if pid == "RG-15":
        return body == src, "unchanged" if body == src else body
    if pid in ("RG-18", "RG-19"):
        raised = re.search(r"禁止|不得|必须|严禁", body)
        return not raised, ("STRENGTH RAISED: " + body) if raised else body
    if pid == "RG-16":
        # the permission may move: 「你可以为用户退款：先查询…再调用 `refund_order`」 keeps it
        ok = bool(re.search(r"你可以|可以调用", body)) and not re.search(r"须|应|必须", body)
        return ok, ("permission kept" if ok else "PERMISSION LOST: ") + (", 一下 removed" if "一下" not in body else ", 一下 kept") + ("" if ok else body)
    if pid == "RG-17":
        r = rules_at(out, "您可以")
        return "CTC-R003" not in r, "clean" if "未发现违规" in out else f"您可以={'+'.join(r) or '-'}"
    if pid == "RG-09":
        return body == src, "unchanged" if body == src else body
    return None, "?"


def main():
    variants = sys.argv[1:]
    pids = []
    for p in sorted(RAW.glob("si3-probe-*-r*/*.json")):
        pid = p.stem.split(".")[0]
        if pid not in pids:
            pids.append(pid)
    print("| probe | variant | pass | r1 | r2 | r3 |\n| --- | --- | --- | --- | --- | --- |")
    for pid in pids:
        for var in variants:
            cells, n, k = [], 0, 0
            for r in (1, 2, 3):
                p = RAW / f"si3-probe-{var}-r{r}" / f"{pid}.claude.json"
                if not p.exists():
                    cells.append("")
                    continue
                ok, note = score(pid, json.loads(p.read_text(encoding="utf-8")))
                n += 1
                k += bool(ok)
                cells.append(("✓ " if ok else "✗ ") + note.replace("|", "/").replace("\n", " "))
            if n:
                print(f"| {pid} | {var} | {k}/{n} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()

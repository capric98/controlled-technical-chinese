#!/usr/bin/env python3
"""Score the si4 probe runs against the expectations registered in probes.yaml.

usage: python3 dev/inbox/si4/probes/score.py VARIANT [VARIANT ...]
Prints one row per probe and variant: pass count over the replicates, then a short note per run.
Only surface features are scored, as in si3: a token kept or removed, a body unchanged, the rule ID cited
at a locus. Where the registration leaves a product question open (R4-05r's fourth column, RG-20's bare
form, PC-01's step count), the note records the behaviour and the pass mark covers only the registered
failure. The finding parser is si3's (dev/inbox/si3/probes/score.py).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "eval" / "reports" / "raw"

_spec = importlib.util.spec_from_file_location("si3score", ROOT / "dev/inbox/si3/probes/score.py")
si3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(si3)
body_and_pending = si3.body_and_pending
# 「**CTC-P003 · ERROR**（「应」级，…）」: a header with trailing text, fields below (si4 base P3-03 r1, R4-05 r3)
HEADER_TRAIL = re.compile(r"^\**(CTC-[SAPTLR]\d{3})\s*[·|｜/]\s*(ERROR|WARNING|STYLE)\**[（(].*$", re.M)
# bold headers with no location in the line, either order, optionally numbered (si4 v1 runs):
# 「**ERROR｜CTC-R004**」「**CTC-A005 · ERROR**」「**1. CTC-A005｜ERROR**」
HEADER_BARE = re.compile(r"^\*\*\s*(?:\d+\.\s*)?(?:(CTC-[SAPTLR]\d{3})\s*[·|｜/]\s*(ERROR|WARNING|STYLE)"
                         r"|(ERROR|WARNING|STYLE)\s*[·|｜/]\s*(CTC-[SAPTLR]\d{3}))\s*\*\*\s*$", re.M)


def chunks(out):
    """(rule, severity, location, text) per finding: si3's layouts plus HEADER_TRAIL."""
    res = list(si3.findings(out))
    seen = {(r, s, l) for r, s, l in res}
    heads = [(m.end(), m.group(1), m.group(2)) for m in HEADER_TRAIL.finditer(out)]
    heads += [(m.end(), m.group(1) or m.group(4), m.group(2) or m.group(3)) for m in HEADER_BARE.finditer(out)]
    # 「1. **规则：** CTC-R004」 with 「**位置：** …」 below (si4 v4 R4-01 r2): the colon sits inside the bold
    heads += [(m.end(), m.group(1), "?") for m in re.finditer(
        r"^\s*(?:\d+\.\s*)?\*\*规则[：:]\*\*\s*(CTC-[SAPTLR]\d{3})\s*$", out, re.M)]
    # 「**1. CTC-R004 · ERROR（应级升级）**」 (si4 v6 R4-01 r3): numbered, parenthetical inside the bold
    heads += [(m.end(), m.group(1), m.group(2)) for m in re.finditer(
        r"^\*\*\s*\d+\.\s*(CTC-[SAPTLR]\d{3})\s*[·|｜/]\s*(ERROR|WARNING|STYLE)\s*[（(][^)）]*[)）]\s*\*\*\s*$", out, re.M)]
    # 「**CTC-R004** | WARNING | 位置：「…」」 on one line (si4 v7 R4-06 r2)
    for m in re.finditer(r"^\**(CTC-[SAPTLR]\d{3})\**\s*[|｜]\s*(ERROR|WARNING|STYLE)\s*[|｜]\s*位置[：:]\s*(.+)$", out, re.M):
        heads.append((m.end(), m.group(1), m.group(2)))
        res.append((m.group(1), m.group(2), m.group(3)))
    # 「**[ERROR] CTC-A005**」 (si4 v3 R4-07 r1)
    heads += [(m.end(), m.group(2), m.group(1)) for m in re.finditer(
        r"^\*\*\[(ERROR|WARNING|STYLE)\]\s*(CTC-[SAPTLR]\d{3})[^*\n]*\*\*\s*$", out, re.M)]  # optional rule name (v5 R4-08)
    # 「1. **规则** CTC-A005｜**严重级别** ERROR」 (si4 v1 R4-01 r2)
    heads += [(m.end(), m.group(1), m.group(2)) for m in re.finditer(
        r"^\s*(?:\d+\.\s*)?\*\*规则\*\*\s*(CTC-[SAPTLR]\d{3})\s*[｜|]\s*\*\*严重级别\*\*\s*(ERROR|WARNING|STYLE).*$",
        out, re.M)]
    heads.sort()
    for i, (end, rule, sev) in enumerate(heads):
        stop = heads[i + 1][0] if i + 1 < len(heads) else len(out)
        loc = re.search(r"位置\**[：:]\s*\**(.*)", out[end:stop])
        rec = (rule, sev, loc.group(1) if loc else "")
        if rec not in seen:
            res.append(rec)
    return res


def findings(out):
    return chunks(out)


def rules_at(out, needle):
    return sorted({r for r, _s, loc in findings(out) if needle in loc})


def problem_text(out, rule, needle):
    """The text of each finding citing RULE whose location contains NEEDLE, for gap-level scoring."""
    texts = []
    for m in re.finditer(re.escape(rule), out):
        seg = out[m.start(): m.start() + 900]
        cut = re.search(r"\n\s*(?:\d+\.|\*\*\d|- \*\*规则|\| CTC-|\*\*CTC-|### )", seg[20:])
        seg = seg[: 20 + cut.start()] if cut else seg
        if needle in seg:
            texts.append(seg)
    return texts

STRONG = r"不得|禁止|必须|严禁|(?<![必无])须"


def pending_lines(pending):
    return [ln for ln in pending.split("\n") if ln.strip().startswith(("-", "*", "|")) or "|" in ln]


def one_rule(out, needles):
    got = sorted({r for n in needles for r in rules_at(out, n)})
    return got


def score(pid, rec):
    out, src = rec["output"], rec["source"].strip()
    body, pending = body_and_pending(out)
    if pid == "P3-05":
        hits = [(r, s, loc) for r, s, loc in findings(out)
                if ("运行正常" in loc or "第 3 步" in loc or "3." in loc[:4]) and r in ("CTC-A005", "CTC-P003")]
        if "未发现违规" in out and not hits:
            return True, "clean"
        others = sorted({r for r, _s, _l in findings(out)})
        return not hits, ("step3=" + "+".join(f"{r}/{s}" for r, s, _ in hits) if hits else "step3 ok") + f" all={'+'.join(others)}"
    if pid == "P3-01":
        hits = [(r, s, loc) for r, s, loc in findings(out)
                if ("运行情况" in loc or "第 3 步" in loc or "3." in loc[:4]) and r in ("CTC-A005", "CTC-P003")]
        if "未发现违规" in out and not hits:
            return True, "clean"
        others = sorted({r for r, _s, _l in findings(out)})
        return not hits, ("step3=" + "+".join(f"{r}/{s}" for r, s, _ in hits) if hits else "step3 ok") + f" all={'+'.join(others)}"
    if pid == "P3-02":
        item = [ln for ln in pending_lines(pending) if re.search(r"运行情况|第 ?3 ?步|检查 `search-api`", ln)]
        return body == src and not item, ("unchanged" if body == src else "edited") + (
            f" step3-item:{len(item)}" if item else "") + (f" pending:{len(pending_lines(pending))}" if pending else "")
    if pid == "P3-03":
        crit = [(r, s, loc) for r, s, loc in findings(out)
                if any(n in loc for n in ("0042", "migrate", "legacy_status", "第 1 步", "删除"))]
        # scored on the gap (resolutions.yaml): which findings at step 1 are about the success criterion
        on_crit = sorted({r for r in ("CTC-P003", "CTC-A005")
                          if any(re.search(r"判据|是否成功|成功与否|确认迁移|迁移成功", x) for x in problem_text(out, r, "0042"))})
        ok = len(on_crit) == 1
        return ok, "step1=" + ("+".join(f"{r}/{s}" for r, s, _ in crit) or "-") + f" criterion={'+'.join(on_crit) or '-'}"
    if pid == "P3-04":
        item = [ln for ln in pending_lines(pending) if re.search(r"0042|迁移|删除|legacy_status|第 ?1 ?步", ln)]
        return body == src and bool(item), ("unchanged" if body == src else "edited") + f" step1-items:{len(item)}"
    if pid == "R4-01":
        got = {w: rules_at(out, w) for w in ("必要时", "尽快", "视情况")}
        ok = all(got[w] and "CTC-R004" in got[w] for w in got)
        return ok, " ".join(f"{w}={'+'.join(r) or '-'}" for w, r in got.items())
    if pid == "PR-07":
        # si3 resolution Q3: both loci CTC-A005, no CTC-R004
        a, b = rules_at(out, "一段时间"), rules_at(out, "流量正常")
        ok = bool(a) and bool(b) and "CTC-R004" not in a + b
        return ok, f"一段时间={'+'.join(a) or '-'} 流量正常={'+'.join(b) or '-'}"
    if pid == "PR-09":
        steps = re.findall(r"^\s*\d+\.", body, re.M)
        crit = "/healthz" in body and "200" in body and "target_version" in body
        return len(steps) == 2 and crit, f"steps:{len(steps)} crit:{'y' if crit else 'n'}"
    if pid in ("R4-04", "R4-05", "R4-06", "R4-07", "R4-08", "R4-09", "R4-10"):
        needle = {"R4-04": ["负载过高", "过高"], "R4-05": ["条件允许"], "R4-06": ["及时"], "R4-07": ["偏大"], "R4-08": ["适当"], "R4-09": ["变慢"], "R4-10": ["时间允许"]}[pid]
        rs = one_rule(out, needle)
        note = f"{needle[0]}={'+'.join(rs) or '-'}"
        if pid == "R4-06":
            # scored on the gap (resolutions.yaml): an A005 at the same quote about 「清理」 is another gap
            return "CTC-R004" in rs, note
        if pid == "R4-04":
            # maintainer decision M4: A005, never R004
            return rs == ["CTC-A005"], note
        if pid == "R4-05":
            # maintainer decision M4 names 条件允许时 among the words R004 keeps
            return rs == ["CTC-R004"], note
        if pid in ("R4-07", "R4-09"):
            return rs == ["CTC-A005"], note
        if pid in ("R4-08", "R4-10"):
            return rs == ["CTC-R004"], note
        return len(rs) == 1, note
    if pid == "R4-05r":
        item = [ln for ln in pending_lines(pending) if "条件允许" in ln]
        cols = max((ln.count("|") for ln in item), default=0)
        return body == src and bool(item), ("unchanged" if body == src else "edited") + f" item:{len(item)} cols:{cols + 1 if item else 0}"
    if pid == "RG-20":
        raised = re.search(STRONG, body)
        form = "吧 kept" if "吧" in body else ("建议" if re.search(r"建议|宜|最好", body) else "bare")
        ok = not raised and "30 秒" in body and "DBA" in body
        return ok, form + ("" if ok else " RAISED/LOST: " + body)
    if pid == "RG-21":
        form = "搞定 kept" if "搞定" in body else "rendered"
        return "12 项" in body, form + ": " + body
    if pid == "RG-08":
        frame = re.findall(r"允许您|您可以|调用者可以|允许调用者|让您", body)
        ok = not frame and "每次最多 500 个" in body
        return ok, (f"frame left:{frame}" if frame else "direct: " + body)
    if pid == "RG-10":
        frame = re.findall(r"开发者可以|调用者可以|调用方可|通过这个函数|你可以|可通过", body)
        ok = not frame and "最大支持 4096 像素" in body and "哦" not in body
        return ok, (f"frame left:{frame}" if frame else ("哦 kept" if "哦" in body else "direct: " + body))
    if pid == "RG-12":
        kept = bool(re.search(r"(只有|仅|仅限|只允许|仅允许).{0,6}管理员", body)) and "管理员" in body
        frame = re.findall(r"可以帮你|帮你|哦", body)
        return kept and not frame, ("restriction kept" if kept else "RESTRICTION LOST") + (
            f" left:{frame}" if frame else "") + ": " + body
    if pid == "RG-15":
        frame = re.findall(r"开发者可以|通过这个函数", body)
        ok = not frame and "4096" in body
        return ok, (f"frame left:{frame}" if frame else "direct: " + body)
    if pid == "RG-16":
        ok = bool(re.search(r"你可以|可以调用", body)) and not re.search(r"须|应|必须", body)
        return ok, ("permission kept" if ok else "PERMISSION LOST: ") + (", 一下 removed" if "一下" not in body else ", 一下 kept") + ("" if ok else body)
    if pid == "RG-17":
        r = rules_at(out, "您可以")
        return "CTC-R003" not in r, "clean" if "未发现违规" in out else f"您可以={'+'.join(r) or '-'}"
    if pid == "RG-22":
        return body == src, "unchanged" if body == src else body
    if pid == "PC-01":
        steps = re.findall(r"^\s*\d+\.", body, re.M)
        crit = "积压为 0" in body or "积压为0" in body
        state = re.search(r"(积压|队列).{0,8}(清零|为 ?0)后[，,]?\s*(执行|删除)", body) and not re.search(r"确认", body)
        cat7 = bool(re.search(r"上限|60 ?字|长度", pending))
        ok = crit and not state
        return ok, f"steps:{len(steps)} crit:{'y' if crit else 'n'} cat7:{'y' if cat7 else 'n'}" + (" STATE-DESC" if state else "")
    return None, "?"


def main():
    variants = sys.argv[1:]
    import yaml
    pids = [c["id"] for c in yaml.safe_load((Path(__file__).parent / "probes.yaml").read_text(encoding="utf-8"))["cases"]]
    print("| probe | variant | pass | r1 | r2 | r3 | r4–r9 (extra replicates, where run) |\n| --- | --- | --- | --- | --- | --- | --- |")
    for pid in pids:
        for var in variants:
            cells, n, k = [], 0, 0
            for r in range(1, 10):
                if r > 3 and not (RAW / f"si4-probe-{var}-r{r}" / f"{pid}.claude.json").exists():
                    continue
                p = RAW / f"si4-probe-{var}-r{r}" / f"{pid}.claude.json"
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

#!/usr/bin/env python3
"""Score the si6 probe runs against the expectations registered in probes.yaml.

usage: python3 dev/inbox/si6/probes/score.py VARIANT [VARIANT ...]
Prints one row per probe and variant: pass count over the replicates, then a short note per run. Surface
features only, as in si3–si5. The probes registered as `product-decision` (GO-01, GO-01r, GO-03, GO-04,
AU-01) are scored on the maintainer's resolutions in resolutions.yaml (M5–M7); GO-06, GO-07 and GO-08,
registered as measure-only, on M8, which was fixed after the v2 outputs. AU-02
is read by hand: the scorer flags a body with more sentences than the source and prints the body.
Copied probes whose expectation did not change are scored by si5's scorer, which uses si4's parser.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "eval" / "reports" / "raw"

_spec = importlib.util.spec_from_file_location("si5score", ROOT / "dev/inbox/si5/probes/score.py")
si5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(si5)
body_and_pending, findings, rules_at, pending_lines = si5.body_and_pending, si5.findings, si5.rules_at, si5.pending_lines

FROM_SI5 = {"OR-01", "OR-02", "OR-03", "OR-06", "OR-08", "HR-01", "HR-02", "TV-01", "ZA-01", "PR-13",
            "P3-01", "P3-05", "PR-07"}


def ids_at(out, needles):
    return sorted({r for n in needles for r in rules_at(out, n)})


def strengths(line):
    return re.findall(r"必须|应当|应|须|可以|建议|不得|最好|尽量", line)


def normalise(out):
    # 「**1. 规则：** CTC-A005」 (si5 v2 PR-07 r2) and 「**1. CTC-P003**」 followed by 「- **严重级别**：」
    # (si6 base HR-02 r3): rewrite both as 「1. **规则**：CTC-…」, which si4's parser reads
    out = re.sub(r"^\*\*(\d+)\.\s*规则([：:])\*\*", r"\1. **规则\2**", out, flags=re.M)
    out = re.sub(r"^\*\*(\d+)\.\s*(CTC-[A-Z]\d{3})\*\*\s*$", r"\1. **规则**：\2", out, flags=re.M)
    # 「**1. CTC-A005 ｜ ERROR**」 (si6 v2b GO-06 r1)
    out = re.sub(r"^\*\*(\d+)\.\s*(CTC-[A-Z]\d{3})\s*[｜|]\s*(ERROR|WARNING|INFO)\*\*.*$",
                 r"\1. **规则**：\2\n- **严重级别**：\3", out, flags=re.M)
    # 「**ERROR｜CTC-R004（规范可判定）**」, a single unnumbered finding (si6 v3 EM-01 r1)
    out = re.sub(r"^\*\*(ERROR|WARNING|INFO)\s*[｜|]\s*(CTC-[A-Z]\d{3})[^*]*\*\*\s*$",
                 r"1. **规则**：\2\n- **严重级别**：\1", out, flags=re.M)
    return out


def score(pid, rec):
    rec = {**rec, "output": normalise(rec["output"])}
    if pid in FROM_SI5:
        return si5.score(pid, rec)
    out, src = rec["output"], rec["source"].strip()
    body, pending = body_and_pending(out)
    clean = " (clean)" if "未发现违规" in out else ""
    if pid == "OR-07":
        # si6 M3: CTC-R004
        rs = ids_at(out, ["紧急"])
        return rs == ["CTC-R004"], f"紧急={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "EM-01":
        rs = ids_at(out, ["紧急"])
        return rs == ["CTC-R004"], f"紧急={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "EM-02":
        rs = ids_at(out, ["不稳定"])
        return "CTC-A005" in rs and "CTC-R004" not in rs, f"不稳定={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "GO-01":
        # M6: CTC-P003
        rs = ids_at(out, ["备份"])
        return rs == ["CTC-P003"], f"备份={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "GO-01r":
        item = [ln for ln in pending_lines(pending) if "备份" in ln]
        return body == src and bool(item), ("unchanged" if body == src else "EDITED") + f" 备份-item:{len(item)}"
    if pid == "GO-05":
        # boundary of M6: no finding on the last step's missing criterion
        rs = ids_at(out, ["备份", "/backup/"])
        return not rs, f"备份={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "GO-02":
        rs = ids_at(out, ["紧张"])
        return rs == ["CTC-A005"], f"紧张={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "GO-03":
        # M5: not reported
        rs = [r for r in ids_at(out, ["较多"]) if r in ("CTC-A005", "CTC-R004")]
        return not rs, f"较多={'+'.join(ids_at(out, ['较多'])) or 'not reported'}{clean}"
    if pid == "GO-04":
        rs = ids_at(out, ["无异常"])
        return rs == ["CTC-A005"], f"无异常={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "EM-03":
        # registered fail_if: CTC-R004 on 「紧急变更」, which the baseline never reports (A005, A005, none)
        rs = ids_at(out, ["紧急变更"])
        return "CTC-R004" not in rs, f"紧急变更={'+'.join(rs) or 'not reported'}{clean}"
    if pid in ("GO-06", "GO-07", "GO-08"):
        # registered measure-only; scored on M8 (resolutions_after_v2), fixed after the v2 outputs:
        # GO-06 and GO-07 reported under any rule, GO-08 not reported as A005 or R004
        needle = {"GO-06": "较小", "GO-07": "紧急", "GO-08": "紧张"}[pid]
        rs = ids_at(out, [needle])
        ok = (not [r for r in rs if r in ("CTC-A005", "CTC-R004")]) if pid == "GO-08" else bool(rs)
        return ok, f"{needle}={'+'.join(rs) or 'not reported'}{clean}"
    if pid == "GO-09":
        rs = ids_at(out, ["快照"])
        return not rs, f"快照={'+'.join(rs) or 'not reported'}{clean}"
    if pid in ("AU-01", "AU-03", "AU-04", "AU-05"):
        sl = [strengths(ln) for ln in src.splitlines()[1:]]
        bl = [strengths(ln) for ln in body.splitlines()[1:]]
        changed = [f"{i + 1}:{'/'.join(a)}→{'/'.join(b)}" for i, (a, b) in enumerate(zip(sl, bl)) if a != b]
        note = ("unchanged" if body == src else "changed " + (",".join(changed) or "wording")) + \
               f" pending:{len(pending_lines(pending))}"
        if pid == "AU-03":
            want = [s if i != 2 else ["必须"] for i, s in enumerate(sl)]
            return bl == want and not pending_lines(pending), note
        if pid == "AU-05":
            # strengths only; item 2's wording may change under CTC-R003
            kept = [[w for w in x if w in ("必须", "应", "可以")] for x in sl] == \
                   [[w for w in x if w in ("必须", "应", "可以")] for x in bl]
            return kept and bool(pending_lines(pending)), note + f" body:{body.splitlines()[-1] if body else ''}"
        # M7: body unchanged, the scope asked for in 「待确认」
        return not changed and bool(pending_lines(pending)), note
    if pid == "AU-02":
        n_src, n_body = src.count("。"), body.count("。")
        return n_body <= n_src, f"sentences {n_src}→{n_body}: {body}" + (" +pending" if pending else "")
    return None, "?"


def main():
    import yaml
    variants = sys.argv[1:]
    pids = [c["id"] for c in yaml.safe_load((Path(__file__).parent / "probes.yaml").read_text(encoding="utf-8"))["cases"]]
    print("| probe | variant | pass | r1 | r2 | r3 | r4–r9 (extra replicates, where run) |\n| --- | --- | --- | --- | --- | --- | --- |")
    for pid in pids:
        for var in variants:
            cells, n, k = [], 0, 0
            for r in range(1, 10):
                p = RAW / f"si6-probe-{var}-r{r}" / f"{pid}.claude.json"
                if not p.exists():
                    if r <= 3:
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

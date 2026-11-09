#!/usr/bin/env python3
"""Score the si5 probe runs against the expectations registered in probes.yaml.

usage: python3 dev/inbox/si5/probes/score.py VARIANT [VARIANT ...]
Prints one row per probe and variant: pass count over the replicates, then a short note per run. Surface
features only, as in si3 and si4. Probes registered as `product-decision` that only measure agreement
(TV-01, TV-02, TH-01, TH-02) pass a run when it is scoreable and note the behaviour; agreement across runs is
read from the notes. The finding parser and the copied probes' scoring are si4's
(dev/inbox/si4/probes/score.py), which parses every finding layout seen through si4.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "eval" / "reports" / "raw"

_spec = importlib.util.spec_from_file_location("si4score", ROOT / "dev/inbox/si4/probes/score.py")
si4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(si4)
body_and_pending, findings, rules_at, pending_lines = si4.body_and_pending, si4.findings, si4.rules_at, si4.pending_lines

COPIED = {"P3-01", "P3-03", "P3-05", "PR-07", "R4-01", "R4-04", "R4-07", "R4-08"}


def ids_at(out, needles):
    return sorted({r for n in needles for r in rules_at(out, n)})


def score(pid, rec):
    out, src = rec["output"], rec["source"].strip()
    # 「**1. 规则：** CTC-A005」 (si5 v2 PR-07 r2): move the number out of the bold so si4's parser reads it
    out = re.sub(r"^\*\*(\d+)\.\s*规则([：:])\*\*", r"\1. **规则\2**", out, flags=re.M)
    rec = {**rec, "output": out}
    body, pending = body_and_pending(out)
    if pid in COPIED:
        return si4.score(pid, rec)
    if pid == "OR-01":
        item = [ln for ln in pending_lines(pending) if "较长" in ln]
        return body == src and not item, ("unchanged" if body == src else "edited") + (f" 较长-item:{len(item)}" if item else "")
    if pid in ("OR-02", "OR-03"):
        needle = "较长" if pid == "OR-02" else "接近上限"
        rs = [r for r in ids_at(out, [needle]) if r in ("CTC-A005", "CTC-R004")]
        if "未发现违规" in out and not rs:
            return True, "clean"
        return not rs, f"{needle}={'+'.join(ids_at(out, [needle])) or '-'}"
    if pid in ("OR-04", "OR-05"):
        needle = "较长" if pid == "OR-04" else "接近上限"
        rs = ids_at(out, [needle])
        return rs == ["CTC-A005"], f"{needle}={'+'.join(rs) or '-'}"
    if pid == "OR-06":
        # maintainer decision M8: reported as A005
        rs = ids_at(out, ["紧张"])
        return rs == ["CTC-A005"], f"紧张={'+'.join(rs) or 'not reported'}" + (" (clean)" if "未发现违规" in out else "")
    if pid == "OR-06r":
        item = [ln for ln in pending_lines(pending) if "紧张" in ln]
        return body == src and bool(item), ("unchanged" if body == src else "EDITED") + f" 紧张-item:{len(item)}"
    if pid in ("OR-07", "OR-08"):
        needle = "紧急" if pid == "OR-07" else "变慢"
        rs = ids_at(out, [needle])
        return rs == ["CTC-A005"], f"{needle}={'+'.join(rs) or 'not reported'}"
    if pid == "HR-01":
        # maintainer decision M9: exactly one criterion item, on step 2 (helm upgrade)
        item = [ln for ln in pending_lines(pending) if re.search(r"判据|成功|验证|是否(成功|生效)|生效", ln)]
        on2 = [ln for ln in item if "helm" in ln or "步骤 2" in ln or "第 2 步" in ln or "升级" in ln]
        ok = body == src and len(item) == 1 and len(on2) == 1
        return ok, ("unchanged" if body == src else "EDITED") + f" criterion-items:{len(item)} on-step2:{len(on2)}"
    if pid == "HR-02":
        # maintainer decision M9: step 2's missing criterion as P003; nothing on steps 1 and 3's criteria
        p2 = [loc for r, _s, loc in findings(out) if r == "CTC-P003" and "helm" in loc]
        other = [loc for r, _s, loc in findings(out) if r == "CTC-P003" and "helm" not in loc]
        return bool(p2) and not other, f"P003@step2:{len(p2)} P003@other:{len(other)} all={'+'.join(sorted({r for r, _s, _l in findings(out)}))}"
    if pid == "ZA-01":
        inserted = bool(re.search(r"将\s*`?vacuum full`?\s*顺延|把\s*`?vacuum full`?\s*顺延", body))
        return body == src and not pending, ("unchanged" if body == src else ("OBJECT INSERTED" if inserted else "EDITED: " + body)) + (" +pending" if pending else "")
    if pid == "PR-13":
        rs = ids_at(out, ["对应服务"])
        return rs == ["CTC-P002"], f"对应服务={'+'.join(rs) or 'not reported'}"
    if pid == "TV-01":
        # maintainer decision M7: CTC-T001
        rs = ids_at(out, ["节点", "实例"])
        return "CTC-T001" in rs, f"实例/节点={'+'.join(rs) or 'not reported'}" + (" (clean)" if "未发现违规" in out else "")
    if pid == "TV-02":
        # M7; scored on the co-reference gap (resolutions.yaml): the A005 findings here are other gaps
        rs = ids_at(out, ["灰度", "金丝雀", "小流量"])
        return "CTC-T001" in rs, f"co-reference={'+'.join(rs) or 'not reported'}"
    if pid == "TH-01":
        # maintainer decision M6: reported as A005
        rs = ids_at(out, ["无异常"])
        return rs == ["CTC-A005"], f"无异常={'+'.join(rs) or 'not reported'}" + (" (clean)" if "未发现违规" in out else "")
    if pid == "TH-02":
        item = [ln for ln in pending_lines(pending) if "无异常" in ln]
        return body == src and bool(item), ("unchanged" if body == src else "EDITED") + f" 无异常-item:{len(item)}"
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
                p = RAW / f"si5-probe-{var}-r{r}" / f"{pid}.claude.json"
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

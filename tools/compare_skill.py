#!/usr/bin/env python3
"""Compare two renderings of SKILL.md deterministically.

usage: python3 tools/compare_skill.py BASE CAND [--prev PREV] [--json OUT]

Hard gates (exit 1 when any fails):
  - the §7 rule table: same 29 rule IDs with the same level (必须/应/可以)
  - the 「待确认」 category list: a numbered list whose items each carry exactly
    one parenthesised rule ID, with the same rule-ID sequence as BASE
  - the three mode headings ### strict / ### standard / ### review
  - the five priority-ladder table rows (first cell starts with 1..5)
  - the six review finding fields (as example-block lines or listed in order in prose) and the three severities
  - frontmatter name and description byte-identical to BASE
  - tools/check_skill.py reports 0 errors

Everything else is informational: size metrics, per-rule row diffs, structure
inventory, code-span and Chinese-numeral inventories, and the character-level
diff ratio against --prev (convergence metric).
"""
import argparse
import collections
import difflib
import json
import os
import re
import subprocess
import sys

RULE_ROW = re.compile(r'^\| (CTC-[SAPTLR]\d{3}) \| (必须|应|可以) \| ([^|]*) \| (.*) \|\s*$', re.M)
ID_RE = re.compile(r'CTC-[SAPTLR]\d{3}')
FIELDS = ['规则', '严重级别', '位置', '问题', '风险', '建议修改']
SEVERITIES = ['ERROR', 'WARNING', 'STYLE']
MODES = ['strict', 'standard', 'review']


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def split_frontmatter(t):
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if not m:
        return None, t
    return m.group(1), t[m.end():]


def fm_field(fm, key):
    m = re.search(r'^%s:\s*(.*)$' % re.escape(key), fm or '', re.M)
    return m.group(1).strip() if m else None


def rule_rows(t):
    return {m.group(1): {'level': m.group(2), 'name': m.group(3).strip(), 'text': m.group(4).strip()}
            for m in RULE_ROW.finditer(t)}


def numbered_blocks(t):
    blocks, cur = [], []
    for line in t.split('\n'):
        m = re.match(r'^\s*(\d+)\.\s+(.*)$', line)
        if m:
            cur.append(m.group(2).strip())
        elif line.strip():
            if cur:
                blocks.append(cur)
                cur = []
    if cur:
        blocks.append(cur)
    return blocks


def pending_categories(t):
    """Rule-ID sequences of numbered lists whose every item carries exactly one （…CTC-Xnnn…）."""
    found = []
    for block in numbered_blocks(t):
        ids = []
        for item in block:
            found_ids = ID_RE.findall(item)
            if len(found_ids) != 1 or not re.search(r'（[^（）]*CTC-[SAPTLR]\d{3}[^（）]*）', item):
                ids = None
                break
            ids.append(found_ids[0])
        if ids and len(ids) >= 3:
            found.append(ids)
    return found


def strip_fences(body):
    return re.sub(r'```.*?```', '', body, flags=re.S)


def inventory(body):
    no_fence = strip_fences(body)
    return {
        'headings': re.findall(r'^#{1,3} .*$', body, re.M),
        'fenced_blocks': len(re.findall(r'^```', body, re.M)) // 2,
        'code_spans': sorted(collections.Counter(re.findall(r'`([^`\n]+)`', no_fence)).items()),
        'numbered_items': len(re.findall(r'^\s*\d+\.\s', body, re.M)),
        'bullet_items': len(re.findall(r'^\s*- ', body, re.M)),
        'table_rows': len(re.findall(r'^\|(?! ---)', body, re.M)),
        'cn_numerals': sorted(collections.Counter(
            re.findall(r'[一二三四五六七八九十]+[类条个项步族层种栏]', no_fence)).items()),
    }


def metrics(t):
    fm, body = split_frontmatter(t)
    return {
        'lines': t.count('\n') + (0 if t.endswith('\n') else 1),
        'bytes': len(t.encode('utf-8')),
        'body_chars': len(body),
        'body_chars_no_ws': len(re.sub(r'\s', '', body)),
    }


def diff_ratio(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return round(1 - sm.ratio(), 4)


def run_check_skill(path):
    here = os.path.dirname(os.path.abspath(__file__))
    p = subprocess.run([sys.executable, os.path.join(here, 'check_skill.py'), path],
                       capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip()
    m = re.search(r'(\d+) error\(s\), (\d+) warning\(s\)', out)
    return {'errors': int(m.group(1)) if m else -1,
            'warnings': int(m.group(2)) if m else -1,
            'output': out}


def counter_delta(a, b):
    a, b = dict(a), dict(b)
    lost = {k: a[k] - b.get(k, 0) for k in a if a[k] > b.get(k, 0)}
    gained = {k: b[k] - a.get(k, 0) for k in b if b[k] > a.get(k, 0)}
    return {'lost': lost, 'gained': gained}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base')
    ap.add_argument('cand')
    ap.add_argument('--prev')
    ap.add_argument('--json')
    args = ap.parse_args()

    base, cand = read(args.base), read(args.cand)
    bfm, bbody = split_frontmatter(base)
    cfm, cbody = split_frontmatter(cand)
    gates, info = {}, {}

    # --- hard gates ---
    brules, crules = rule_rows(base), rule_rows(cand)
    bmap = {k: v['level'] for k, v in brules.items()}
    cmap = {k: v['level'] for k, v in crules.items()}
    gates['rule_level_map'] = {
        'pass': bmap == cmap and len(cmap) == 29,
        'base_count': len(bmap), 'cand_count': len(cmap),
        'missing': sorted(set(bmap) - set(cmap)),
        'extra': sorted(set(cmap) - set(bmap)),
        'level_changed': {k: (bmap[k], cmap[k]) for k in bmap if k in cmap and bmap[k] != cmap[k]},
    }

    bcats, ccats = pending_categories(base), pending_categories(cand)
    bseq = bcats[0] if bcats else None
    gates['pending_categories'] = {
        'pass': bseq is not None and bseq in ccats,
        'base': bseq, 'cand_lists': ccats,
    }

    cmodes = set(re.findall(r'^### (strict|standard|review)\s*$', cand, re.M))
    gates['mode_headings'] = {'pass': cmodes == set(MODES), 'found': sorted(cmodes)}

    ladder = sorted(set(re.findall(r'^\| ([1-5]) [^|]*\|', cand, re.M)))
    gates['ladder_rows'] = {'pass': ladder == ['1', '2', '3', '4', '5'], 'found': ladder}

    # Accept either the example-block line form (规则：…) or the six names listed in order in prose.
    inline = re.search(r'规则.{0,4}严重级别.{0,4}位置.{0,4}问题.{0,4}风险.{0,4}建议修改', cand)
    missing_fields = [] if inline else [f for f in FIELDS if not re.search(r'^%s：' % f, cand, re.M)]
    missing_sev = [s for s in SEVERITIES if not re.search(r'\b%s\b' % s, cand)]
    gates['finding_fields'] = {'pass': not missing_fields, 'missing': missing_fields}
    gates['severities'] = {'pass': not missing_sev, 'missing': missing_sev}

    gates['frontmatter'] = {
        'pass': cfm is not None and fm_field(bfm, 'name') == fm_field(cfm, 'name')
                and fm_field(bfm, 'description') == fm_field(cfm, 'description'),
        'name_equal': fm_field(bfm, 'name') == fm_field(cfm, 'name'),
        'description_equal': fm_field(bfm, 'description') == fm_field(cfm, 'description'),
    }

    cs = run_check_skill(args.cand)
    gates['check_skill'] = {'pass': cs['errors'] == 0, **cs}

    # --- informational ---
    bm, cm = metrics(base), metrics(cand)
    info['metrics'] = {'base': bm, 'cand': cm,
                       'delta_pct': {k: round(100.0 * (cm[k] - bm[k]) / bm[k], 1) for k in bm}}

    row_diffs = []
    for rid in sorted(set(brules) | set(crules)):
        b = brules.get(rid, {}).get('text', '')
        c = crules.get(rid, {}).get('text', '')
        if b != c:
            r = diff_ratio(b, c)
            row_diffs.append({'rule': rid, 'ratio': r, 'weight': round(r * max(len(b), len(c))),
                              'base': b, 'cand': c})
    row_diffs.sort(key=lambda d: -d['weight'])
    info['rule_row_diffs'] = row_diffs

    binv, cinv = inventory(bbody), inventory(cbody)
    info['inventory'] = {
        'base': {k: v for k, v in binv.items() if k not in ('code_spans', 'cn_numerals')},
        'cand': {k: v for k, v in cinv.items() if k not in ('code_spans', 'cn_numerals')},
        'code_spans': counter_delta(binv['code_spans'], cinv['code_spans']),
        'cn_numerals': counter_delta(binv['cn_numerals'], cinv['cn_numerals']),
    }
    info['diff_ratio_vs_base'] = diff_ratio(bbody, cbody)
    if args.prev:
        _, pbody = split_frontmatter(read(args.prev))
        info['diff_ratio_vs_prev'] = diff_ratio(pbody, cbody)

    # --- report ---
    ok = all(g['pass'] for g in gates.values())
    print('=== HARD GATES: %s ===' % ('PASS' if ok else 'FAIL'))
    for name, g in gates.items():
        print('  [%s] %s' % ('ok' if g['pass'] else 'FAIL', name))
        if not g['pass']:
            for k, v in g.items():
                if k not in ('pass', 'output'):
                    print('        %s: %s' % (k, v))
            if 'output' in g:
                print('        ' + g['output'].replace('\n', '\n        '))
    print('=== METRICS ===')
    for k in bm:
        print('  %-18s base=%-7d cand=%-7d delta=%+.1f%%' % (k, bm[k], cm[k], info['metrics']['delta_pct'][k]))
    print('  diff_ratio_vs_base=%.4f' % info['diff_ratio_vs_base'])
    if args.prev:
        print('  diff_ratio_vs_prev=%.4f' % info['diff_ratio_vs_prev'])
    print('  check_skill: %d error(s), %d warning(s)' % (cs['errors'], cs['warnings']))
    print('=== RULE ROW DIFFS (%d changed; top by weight) ===' % len(row_diffs))
    for d in row_diffs:
        print('  %s ratio=%.3f weight=%d' % (d['rule'], d['ratio'], d['weight']))
        print('    BASE: ' + d['base'])
        print('    CAND: ' + d['cand'])
    print('=== INVENTORY ===')
    for k in ('fenced_blocks', 'numbered_items', 'bullet_items', 'table_rows'):
        print('  %-15s base=%-4d cand=%-4d' % (k, binv[k], cinv[k]))
    print('  headings (cand): ' + ' | '.join(cinv['headings']))
    print('  code_spans: ' + json.dumps(info['inventory']['code_spans'], ensure_ascii=False))
    print('  cn_numerals: ' + json.dumps(info['inventory']['cn_numerals'], ensure_ascii=False))

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump({'gates': gates, 'info': info, 'pass': ok}, f, ensure_ascii=False, indent=1)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()

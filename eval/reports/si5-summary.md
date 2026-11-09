# si5 — Opus 5.5 iteration on decision 009: permission and description exemptions, the guarded-operation threshold, zero anaphora

- **Status:** complete. The maintainer accepted v2 as decision 010 on 2026-11-09; `SKILL.md` is v2.
- **Date:** 2026-11-09
- **Orchestrator:** Claude Opus 5.5 (this session). The maintainer confirmed at the start that every model call
  stays on Opus 5.5 (M1).
- **Relates to:** `docs/decisions/009-si4-criteria-bounds-metric-conditions-terminology.md` (open proposals 8,
  21, 22, 23, 26), `docs/decisions/010-si5-permission-description-exemptions-guarded-threshold.md`
- **Evidence:** `dev/inbox/si5/`, which holds:
  - the probes, the maintainer's resolutions and the scorer;
  - the candidates and `cand/build.py`;
  - the reviews and the adjudication;
  - the self-hosting cases;
  - `runs/outputs.jsonl`.

  Verdicts are in `eval/reports/verdicts-si5.claude.yaml`.

## 1. Question

Decision 009 left these open:

- proposal 23 (a vague condition on a permission is raised; G-S-001), with the related over-report on
  descriptive text (G-R-012);
- proposal 21 (review-mode term variants have no rule ID);
- proposal 22 (道义强度／规范强度);
- proposal 26 (the missing-criterion threshold versus P004's guarded operations);
- proposal 8 (P004 cites an R005 rule about warning blocks that R005 does not state).

G-A-002 had failed in every run since r1.

si5 asks what each of these does to behaviour, and changes text only where a pre-registered probe or a
self-hosting run fails, or the maintainer decides.

## 2. Setup

| item | value |
| --- | --- |
| baseline | `SKILL.md` at 283ec5a (si4 v8, 232 lines, body 13 204 chars), frozen at `dev/inbox/si5/base/SKILL.md` |
| candidate runs | `claude -p --model claude-opus-5-5` via `tools/ctc_eval.py run` (`CTC_SKILL`, `CTC_CLAUDE_MODEL`), in parallel shards (`dev/inbox/si5/run_set.sh`, `rep_probe.sh`, `rep_case.sh`) |
| semantic judge | the same model, `dev/prompts/judge-semantic.v1.md` unchanged, `--batch 3` |
| probes | 25 probes in `dev/inbox/si5/probes/probes.yaml`, each registered before any output: 17 before the first run, 6 from the reviewers' counterexamples, 2 after M8–M10. Eight are si4 regression probes copied verbatim; PR-13 is copied from si2. Three runs per probe per version, more where a cell wobbled. Scored on surface features by `probes/score.py`, which reuses si4's parser; every parser miss was read by hand |
| product decisions | ten questions to the maintainer: three before any output was read, four after the baseline probe pass, three after the v1 runs and reviews (`probes/resolutions.yaml`) |
| candidates | `v1` and `v2`, built from the baseline by exact replacement in `dev/inbox/si5/cand/build.py` |
| reviews | Opus 5.5 subagents with disjoint inputs. Adversarial (`dev/prompts/si5-adversarial.md`), cold reverse-decode (`si5-decode.md`) and naturalness (`si5-naturalness.md`) reviewed v1. A second cold decode (`si5-decode-v2.md`) reviewed v2 |
| gold | one full run of v2. Three replicates per version (base, v1, v2) of G-S-001, G-R-012, G-A-002, G-T-101 and G-R-010. Four more of G-S-001 per version, and six more of G-T-101 on base and v2 |
| model calls | 359 candidate outputs in 63 runs: 228 probe outputs, one full gold run (56), 69 gold replicates, 6 self-hosting reviews. 125 judge verdicts. 4 review subagents |

## 3. Baseline

Probes, three runs each:

- **Proposal 23.**
  - 「若导出队列较长，也可以拆成多批提交」 is raised in rewrite 3/3 (OR-01) and reported as A005 in review 3/3
    (OR-02).
  - A description of system behaviour (「连接数接近上限时，网关会拒绝新的长连接请求」) draws A005 3/3 (OR-03).
  - The same conditions on a required action are A005 3/3 (OR-04, OR-05), as they should be.
- **Proposal 26.**
  - A vague check that gates a restart is A005 3/3 (TH-01) and raised 3/3 (TH-02), beyond the text's
    「破坏性或不可逆」.
  - A deploy runbook's release step with no criterion is P003 in review 3/3 (HR-02) but raised 0/3 in rewrite
    (HR-01).
- **Proposal 21.** Term variants are reported as CTC-T001 6/6 (TV-01, TV-02), which the text does not name.
- **Later probes.** A permitted destructive action is A005 3/3 (OR-06, OR-06r). A waiver of a required control
  is reported 3/3 with the rule ID split (OR-07: A005, R004, A005). A symptom section is A005 2/3 (OR-08).
- **Gold replicates.** G-S-001 6/7 (one run inserts 「将索引重建」 and raises the 「紧张」 item). G-A-002 3/3
  under the amended gold. G-T-101 9/9; G-R-010 and G-R-012 3/3.

Self-hosting, two runs: 道义／规范 1/2, the T001 gap 1/2, the frontmatter P005 finding 2/2.

## 4. Product decisions (maintainer, 2026-11-09)

M1 all-Opus; M2 「规范强度」 everywhere; M3 amend G-A-002; M4 do not report permission conditions; M5 do not
report descriptions; M6 the threshold follows P004's guarded operations; M7 CTC-T001 for review-mode term
variants; M8 the permission exemption does not cover destructive, irreversible or state-changing actions;
M9 keep H2; M10 fix the zero-object insertion this round. Questions and answers are verbatim in
`dev/inbox/si5/probes/resolutions.yaml`.

## 5. Iterations

- **v1** (N1, N2, V1, H1, H2, D1, S1): fixes OR-01, OR-02, OR-03 (0/3 → 3/3) and HR-01 (0/3 → 3/3). The reviews
  and new probes found two holes in D1's literal reading:
  - a destructive permission (OR-06, 0/3);
  - a waiver of a required control (OR-07, silent 3/3).

  With the 「紧张」 item gone, G-S-001 began inserting the permission's object (4/7).
- **v2** applies the rulings on the reviews (`dev/inbox/si5/review/adjudication.md`) and M8–M10:
  - D1' adds the waiver and destructive qualifiers;
  - V1' keeps 「它是一条」;
  - N1' anchors the authorisation in the source text;
  - H1' is a contrapositive;
  - H2' uses 「，且」;
  - S1' adds 「应」;
  - Z1 adds zero anaphora to CTC-P002.

  v2 closes both holes and brings G-S-001 back to base level.

## 6. Results on the final candidate (v2)

### Probes

Full table: `dev/inbox/si5/probes/summary.md`.

| group | base | v1 | v2 |
| --- | --- | --- | --- |
| proposal 23 targets (OR-01, OR-02, OR-03) | 0/9 | 9/9 | 9/9 |
| their boundaries (OR-04, OR-05) | 6/6 | 6/6 | 6/6 |
| destructive permission (OR-06, OR-06r) | 6/6 | 0/6 | 6/6 |
| waiver (OR-07), reported at all | 3/3 | 0/3 | 3/3 |
| symptom section (OR-08) | 2/3 | 3/3 | 3/3 |
| release step (HR-01, HR-02) | 3/6 | 6/6 | 6/6 |
| threshold agreement (TH-01, TH-02) | 6/6 | 6/6 | 6/6 |
| term variants (TV-01, TV-02) | 9/9 | 6/6 | 11/12 |
| zero object (ZA-01) and boundary (PR-13) | 5/6 | — | 6/6 |
| si4 regression probes (8) | 24/24 | 24/24 | 24/24 |

Two v2 results fall short of the registered expectations:

- OR-07's rule ID splits between A005 and R004 in 2/3 v2 runs (base 1/3); every run reports it.
- TV-01 misses once in nine.

### Gold

- **Full run (v2).** 56/56, 0 deterministic errors, no over-edit on any trap, naturalness 4.70. si4's full runs
  scored 53–55 with naturalness 4.62–4.68.
- **Replicates.**

  | case | base | v1 | v2 |
  | --- | --- | --- | --- |
  | G-S-001 | 6/7 | 3/7 | 6/7 |
  | G-T-101 | 9/9 | 3/3 | 8/9 |
  | G-A-002, G-R-010, G-R-012 | 3/3 each | 3/3 each | 3/3 each |

  Every G-S-001 failure is the inserted object. The G-T-101 failure is one run whose co-reference item names
  two of the three terms; six extra replicates pass on base and v2 alike.

### Gates and self-hosting

- `tools/compare_skill.py` base → v2: every hard gate passes, frontmatter unchanged (`dev/inbox/si5/cand/gate-v2.json`).
  Body +1.5% (13 204 → 13 402 characters), 232 lines.
- `tools/check_skill.py`: 0 errors, 0 warnings. `skills-ref validate` was not run (auto mode blocks `pnpm dlx`).
- Self-hosting, two runs each:
  - base reports 道义／规范 and the T001 gap;
  - v1 reports the T001 routing against T001's trigger, which V1' answers;
  - v2 r1 reports only the frontmatter P005 finding, and v2 r2 reports no violation.

## 7. Open items

Open proposals 27–31 are new (decision 010):

- the undefined guarded-operation class;
- a failed exemption's fallback;
- 「情况紧急时」 between R004 and A005;
- 「指定改写目标」;
- the rewrite/review severity asymmetry for term differences that block execution.

Proposals 1, 2, 7, 9, 10, 17, 24 and 25 stay open from 006–009.

## 8. Harness notes

- The dcg hook blocks redirects to computed paths and heredocs that contain backticks. si5's scripts write logs
  inside wrapper scripts (`rep_probe.sh`) and use Python for file copies.
- si5's scorer moves the number out of a bold 「**1. 规则：**」 header before si4's parser reads it (one v2 PR-07
  run used that layout).

## 9. Limitations

- One model generates, judges and reviews. D001's caution applies.
- The gold corpus is not human-reviewed; G-A-002's amendment is the maintainer's decision.
- Probe scores are surface features; each parser miss was read by hand.
- The guarded-operation class that three rules now share is defined only by P004's examples (open proposal 27).

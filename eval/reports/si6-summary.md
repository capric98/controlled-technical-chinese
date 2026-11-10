# si6 — Opus 5.5 iteration on decision 010: the permission exemption against the default action, 「紧急时」, unspecific strength authorisations, the description's exclusions

- **Status:** complete. The maintainer accepted v5 as decision 011 on 2026-11-09; `SKILL.md` is v5.
- **Date:** 2026-11-09
- **Orchestrator:** Claude Opus 5.5 (this session). The maintainer confirmed at the start that every model call
  stays on Opus 5.5 (M1).
- **Relates to:** `docs/decisions/010-si5-permission-description-exemptions-guarded-threshold.md` (open proposals
  10, 27, 28, 29, 30, 31), `docs/decisions/011-si6-permission-increment-emergency-authorisation-description.md`
- **Evidence:** `dev/inbox/si6/`, which holds:
  - the probes, the maintainer's resolutions and the scorer;
  - the candidates and `cand/build.py`;
  - the reviews and the adjudication;
  - the self-hosting cases;
  - `runs/outputs.jsonl`.

  Verdicts are in `eval/reports/verdicts-si6.claude.yaml`.

## 1. Question

Decision 010 left these open:

- proposal 10 (the description omits §1's exclusions; P005 in 5 of 6 si5 self-hosting runs);
- proposal 27 (the guarded-operation class: what the permission exemption tests, backups, config changes,
  notifications);
- proposal 29 (「情况紧急时」 between R004 and A005);
- proposal 30 (「指定改写目标」 and vague strength authorisations);
- proposal 31 (rewrite raises a blocking term difference at 必须, review at 应);
- proposal 28 (a failed exemption's fallback; no failing run).

si6 asks what each of these does to behaviour, and changes text only where a pre-registered probe or a
self-hosting run fails, or the maintainer decides.

## 2. Setup

| item | value |
| --- | --- |
| baseline | `SKILL.md` at 37b5983 (si5 v2, 232 lines, body 13 402 chars), frozen at `dev/inbox/si6/base/SKILL.md` |
| candidate runs | `claude -p --model claude-opus-5-5` via `tools/ctc_eval.py run` (`CTC_SKILL`, `CTC_CLAUDE_MODEL`), in parallel shards (`dev/inbox/si6/run_set.sh`, `rep_probe.sh`, `rep_case.sh`, `rep_run.sh`) |
| semantic judge | the same model, `dev/prompts/judge-semantic.v1.md` unchanged, `--batch 3` |
| probes | 32 probes in `dev/inbox/si6/probes/probes.yaml`, each registered before any output: 23 before the first run (14 copied from si5), 2 after M5–M7, 7 from the reviewers' counterexamples to v1. Three runs per probe per version, more where a cell differed from base. Scored on surface features by `probes/score.py`; every parser miss was read by hand |
| product decisions | nine questions to the maintainer: four before any output was read, three after the baseline probe pass, two after the v2 runs (`probes/resolutions.yaml`) |
| candidates | v1, v2a, v2b, v3, v4d, v5 and two ablations, built from the baseline by exact replacement in `dev/inbox/si6/cand/build.py` |
| reviews | Opus 5.5 subagents with disjoint inputs. Adversarial (`dev/prompts/si6-adversarial.md`), cold reverse-decode (`si6-decode.md`) and naturalness (`si6-naturalness.md`) reviewed v1. A second cold decode (`si6-decode-v3.md`) reviewed v3 |
| gold | one full run each of v3 and v5. Three replicates per version of G-S-001, G-R-012, G-R-007, G-P-004 and G-T-101, and more of G-S-001, G-T-101 and G-P-005 where a version differed |
| model calls | 826 candidate outputs in 152 runs: 534 probe outputs, two full gold runs (112), 172 gold replicates, 8 self-hosting reviews. 264 judge verdicts. 4 review subagents |

## 3. Baseline

Probes, three runs each (six where noted):

- **Proposal 29.** OR-07 and EM-01 report 「情况紧急时」／「紧急情况下」 as A005 in every run (0/3, 0/6 against M3).
- **Proposal 27.**
  - A permission to split a release (GO-03) is not reported 1/3 and A005 2/3, citing 「许可的操作是发布」.
  - A backup before `DROP TABLE` is raised as P003 (GO-01 5/6, GO-01r 5/6) without any text naming backups.
  - An earlier deletion of the same kind (GO-08) is A005 3/3; skipping a recommended check (GO-06) is R004
    3/3; handing the operation to another performer (GO-07) is A005 3/3.
  - A snapshot before a restart (GO-09) is raised in 2 of 3 runs.
- **Proposal 30.** 「把要求放宽一些」 lowers every strength in 1 of 3 runs (AU-01); 「把第 2 条放宽一些」 lowers item 2
  in 3 of 3 (AU-04); on a source with an R003 defect, both 必须 drop to 应 in 3 of 3 (AU-05).
- **Gold replicates.** G-S-001 7/7, G-T-101 9/9, G-R-007, G-P-004, G-R-012 3/3 each.

Self-hosting, two runs: no P005 on the description (the finding M2 answers had fallen to 1 in 4 runs on this
text).

## 4. Product decisions (maintainer, 2026-11-09)

M1 all-Opus; M2 add §1's exclusions to the description; M3 「情况紧急时」 is CTC-R004; M4 keep CTC-T001 and close
proposal 31; M5 the permission exemption tests what the permitted way adds beyond the default action; M6 name
backups in P003 (reversed by M9); M7 an unspecific strength authorisation changes nothing and is raised as
category 5; M8 the exemption also fails when the permitted way reduces a check or review before a guarded
operation or changes its performer; M9 drop the backup clause. Questions and answers are verbatim in
`dev/inbox/si6/probes/resolutions.yaml`. M5–M9 were put in the session's text after the question tool was
declined; the maintainer answered 「按推荐继续」 both times.

## 5. Iterations

- **v1** (F1, R1, G1, B1, U1) fixes OR-07, EM-01, GO-03 and AU-01. Its backup clause covered state-changing
  steps and broke gold G-R-007 (0/3). The three reviews raised four wording defects and two scope questions;
  seven new probes were registered (`dev/inbox/si6/review/adjudication.md`).
- **v2a and v2b** narrow B1 and U1 and split G on M8's question. They differ only at GO-07 (v2a exempt 0/3,
  v2b reported 3/3). B1' still produces backup false positives (GO-05 3/6, G-R-007 1/3 on v2a), and base raises
  GO-01 without it: M9.
- **v3** (F1, R1, G1b, U1') passes every target. Its runs found two problems:
  - gold G-S-001 inserts the permission's omitted object 「将索引重建」 in 5 of 14 runs (base 0/7);
  - self-hosting found 「其」 in 「也不更换其执行者」 with three antecedents.
- **v4d and the ablations.** Dropping the checks clause (v4d 3/10) did not fix G-S-001. G1a alone (2/10) and
  every edit except G (1/10) bracket it: every G wording raises the rate, the longer ones most.
- **v5** (F1, R1, G1c, U1', Z2) writes 「其」's antecedent out (G1c) and points the exemption at CTC-P002's
  zero-anaphora clause (Z2). G-S-001 inserts 0/10.

## 6. Results on the final candidate (v5)

### Probes

Full table: `dev/inbox/si6/probes/summary.md`.

| group | base | v3 | v5 |
| --- | --- | --- | --- |
| proposal 29 targets (OR-07, EM-01) | 0/9 | 6/6 | 6/6 |
| boundary EM-02 | 3/3 | 3/3 | 3/3 |
| boundary EM-03 (no R004 on 「紧急变更」) | 6/6 | 2/6 | 1/3 |
| proposal 27 targets (GO-03, GO-08) | 1/6 | 6/6 | 6/6 |
| M8's reported cases (GO-06, GO-07) | 6/6 | 6/6 | 6/6 |
| added operations (OR-06, GO-02) | 6/6 | 6/6 | 6/6 |
| backups (GO-01, GO-01r, GO-05) | 13/15 | 13/15 | 8/9 |
| GO-04 | 3/3 | 3/3 | 3/3 |
| GO-09 | 1/3 | 1/3 | 3/3 |
| proposal 30 targets (AU-01, AU-04, AU-05) | 2/9 | 9/9 | 9/9 |
| AU-03 | 5/6 | 4/6 | 3/3 |
| AU-02 (read by hand) | 3/3 | 3/3 | 3/3 |
| si5 regression probes (12) | 35/36 | 36/36 | 36/36 |

EM-03 is the one registered boundary that fails: base never reports the category 「紧急变更」, the candidates add a
hedged R004 WARNING on it in 7 of 15 runs (open proposal 32).

### Gold

- **Full run (v5).** 56/56, 0 deterministic errors, no over-edit on any trap, naturalness 4.68. v3: 55/56
  (G-P-005), 4.66. si5 v2: 56/56, 4.70.
- **Replicates** (v3 and v5 include their full run).

  | case | base | v3 | v5 |
  | --- | --- | --- | --- |
  | G-S-001 | 7/7 | 9/14 | 14/14 |
  | G-T-101 | 9/9 | 10/10 | 16/20 |
  | G-R-007 | 3/3 | 4/4 | 4/4 |
  | G-P-004, G-R-012 | 3/3 each | 4/4 each | 4/4 each |
  | G-P-005 | 2/3 | 2/4 | 1/1 |

  G-T-101's v5 failures: two runs with a partial co-reference item (si5's recorded mode), two with none; three
  of the four came in the first nine runs. The base text's record is 17/18 across si5 and si6; p ≈ 0.2.

### Gates and self-hosting

- `tools/compare_skill.py` base → v5: every hard gate passes, the frontmatter after M2's replacement
  (`dev/inbox/si6/cand/gate-v5.json`). Body +1.0% (13 402 → 13 542 characters), 232 lines.
- `tools/check_skill.py`: 0 errors, 0 warnings. `skills-ref validate` was not run.
- Self-hosting, two runs each on base, v1, v3 and v5. v5 r1 reports only findings that predate si6; v5 r2
  reports no violation. No run on any si6 version reports the description's exclusions.

## 7. Open items

New (decision 011):

- 32 — R004 reaches a category name that contains a listed word (EM-03);
- 33 — a polishing request on a covered document type: exclusion or coverage (decoder 5(a));
- 34 — the mode and review threshold for a document spanning both scopes or neither;
- 35 — 「阶梯」 is undefined.

27, 28, 30 and 10 stay partly open. 1, 2, 7, 9, 17, 24 and 25 stay open from 006–010.

## 8. Harness notes

- `rep_run.sh` runs gold cases without judging, for a property a string match decides (G-S-001's inserted
  object).
- si6's scorer rewrites four bold header layouts the si4 parser misses. Two of them hid real results
  (GO-06 v2b r1, EM-01 v3 r1); the rescoring changed no other cell.
- The dcg hook blocks redirects to computed paths and heredocs with backticks; scratch output goes through
  `tee` to a literal path.

## 9. Limitations

- One model generates, judges and reviews. D001's caution applies.
- The gold corpus is not human-reviewed.
- Probe scores are surface features; each parser miss was read by hand.
- Activation is not tested: the harness loads the whole skill, so F1 is measured by self-hosting and the cold
  decode only.
- Single-case gold rates are noisy (G-S-001 under Z2, G-T-101 on v5).
- M8's resolutions for GO-06, GO-07 and GO-08 were fixed after the v2 outputs; v3 and v5 are their first
  confirmation runs.

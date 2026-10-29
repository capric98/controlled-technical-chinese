# si4 — Opus 5.5 iteration on decision 008: missing-criterion bounds, metric conditions, terminology

- **Status:** complete. The maintainer accepted v8 as decision 009 on 2026-10-29; `SKILL.md` is v8.
- **Date:** 2026-10-29
- **Orchestrator:** Claude Opus 5.5 (this session). The maintainer confirmed at the start that every model call
  stays on Opus 5.5 (M1).
- **Relates to:** `docs/decisions/008-si3-register-r004-class-status-scope.md` (open proposals 10, 15, 18, 19,
  20), `docs/decisions/009-si4-criteria-bounds-metric-conditions-terminology.md`
- **Evidence:** `dev/inbox/si4/`, which holds:
  - the probes, the maintainer's resolutions and the scorer;
  - the candidates and `cand/build.py`;
  - the reviews and the adjudication;
  - the self-hosting cases;
  - `runs/outputs.jsonl`.

  Verdicts are in `eval/reports/verdicts-si4.claude.yaml`.

## 1. Question

Decision 008 left open proposals 15 (the A005/P003 overlap), 18 (「记录级别」), 19 (the probes si3 did not run)
and 20 (the third-person frame in R003), and self-hosting kept reporting the frontmatter's 「歧义只报告」, P003's
two names for one authorisation, 「明确边界」 and §9 item 1's direction. Two gold cases had failed in every run
since r1: G-A-002 and G-T-101.

si4 asks what each one does to behaviour, and changes text only where a pre-registered probe or a self-hosting
run fails, or the maintainer decides.

## 2. Setup

| item | value |
| --- | --- |
| baseline | `SKILL.md` at 5a04c5c (si3 v6, 232 lines, body 13 010 chars), frozen at `dev/inbox/si4/base/SKILL.md` |
| candidate runs | `claude -p --model claude-opus-5-5` via `tools/ctc_eval.py run` (`CTC_SKILL`, `CTC_CLAUDE_MODEL`), in parallel shards (`dev/inbox/si4/run_set.sh`) |
| semantic judge | the same model, `dev/prompts/judge-semantic.v1.md` unchanged, `--batch 3`; a batch whose YAML does not parse twice is re-judged one case at a time |
| probes | 26 probes in `dev/inbox/si4/probes/probes.yaml`, each registered before any output (hashes and times in the file's dated sections). Three runs per probe per version, more where a cell wobbled. Scored on surface features by `probes/score.py`; every parser miss was read by hand and the parser extended |
| product decisions | six questions to the maintainer, three before any output was read and three after the baseline pass (`probes/resolutions.yaml`) |
| candidates | `v1`–`v8`, built from the baseline by exact replacement in `dev/inbox/si4/cand/build.py` |
| reviews | Opus 5.5 subagents with disjoint inputs. Adversarial (`dev/prompts/si4-adversarial.md`), cold reverse-decode (`si4-decode.md`) and naturalness (`si4-naturalness.md`) reviewed v1; a second cold decode (`si4-decode-v3.md`) reviewed v3 |
| gold | full runs of v3, v4, v5, v6 and v7; three replicates per version of G-R-009, G-R-010, G-R-011, G-P-003 and G-T-101; three replicates of G-S-001 and G-R-014 on base and v5 |
| model calls | 986 candidate outputs in 93 runs: 567 probe outputs, five full gold runs (280), 105 gold replicates, 12 single-case replicates, 16 self-hosting reviews. 403 judge verdicts. 4 review subagents. Calls cut off by the usage limit wrote nothing and are not counted |

## 3. Baseline

The baseline's full gold run is si3's run of the same text: 53/56. Failures: G-A-002, G-T-101, G-R-003.

Probes, three runs each, on the questions that fork:

- **Proposal 15.** A read-only closing check with no criterion (P3-01, 「检查 `search-api` 的运行情况」) draws
  CTC-A005/ERROR in 2/3 review runs; rewrite raises nothing 3/3 (P3-02). With 「确认…运行正常」 (P3-05), review
  reports it 3/3. A destructive step with no criterion is CTC-P003 3/3 in review (P3-03) and raised 3/3 in
  rewrite (P3-04).
- **Proposal 19.** 「负载过高」 forks A005, R004, A005 (R4-04); 「磁盘占用偏大」 R004, R004, A005 (R4-07).
  「条件允许时」 (R4-05), 「及时」 (R4-06), the suggestion 「吧」 (RG-20) and 「搞定」 (RG-21) do not fork.
- **Proposal 20.** Runtime already rewrites the third-person frame (RG-15 3/3) and leaves developer-guide prose
  alone (RG-22 3/3). The gap is textual: si3's second cold decode predicted RG-15 unchanged.
- **「压缩授权」.** A step cap merges the verification step (PR-09 3/3); a character cap does not (PC-01 3/3).
  Behaviour already matches D004; the gap is the two names.
- **G-T-101** raises the co-reference question in 「待确认」 3/3; the gold accepted only unification.

Self-hosting, two runs: 「记录级别」 2/2, frontmatter 「只报告」 1/2, 「压缩授权」 1/2, 「明确边界」 1/2,
道义／规范强度 1/2, R003 「过长」 1/2.

## 4. Product decisions (maintainer, 2026-10-29)

| question | answer |
| --- | --- |
| M1: models for the reviews | all Opus 5.5 |
| M2: the frontmatter clause | unfreeze it alone: 「上下文不足以确定的歧义只报告、不擅自消解」 |
| M3: G-T-101 against 004 §3 | amend the gold: raising the co-reference question also passes; merging 「全量发布」 still fails |
| M4: a degree word on a metric (「负载过高」) | CTC-A005, like 「多次」; R004 keeps whether/when/how-much words (尽量、尽快、及时、必要时、视情况、条件允许时) |
| M5: a missing criterion on a check nothing depends on | review applies P003's bound too; A005 does not take it |
| M6: 「先别切主吧」 → 「先不要切主」 | keeps the strength; no text change |

## 5. Iterations

| version | change | what decided it |
| --- | --- | --- |
| v1 | F1 (M2); T1 记录级别; T2 P003's merge authorisation named; T3 §9 「应写成」; T4 「规则条文写明的边界」; B1 A005 defers missing criteria to P003, keeping undefined criteria in A005; B2 R004's exclusion adds degree words on metrics (M4); C1 R003 adds the third-person frame | the baseline probes, M2–M5, recurring self-hosting findings |
| v2 | B1v2: the exclusion is stated by its own condition (a check that nothing destructive depends on, with no criterion or an undefined one) | v1 made P3-01 worse (A005 3/3) and started rewrite raising it (P3-02 2/3): the model read 「运行情况」 as an undefined criterion |
| v3 | rulings on the three reviews: T4 reworded; B2 narrowed to trigger conditions on 运行指标; §8's parenthesis shortened; C1 its own item, limited to frames that state the function | `dev/inbox/si4/review/adjudication.md` |
| v4 | §8's parenthesis lists the excluded kinds again; R003's repair sentence drops the duplicated subject clause (C1d) | v3 R4-05 r1 read the short parenthesis as 「everything R004 finds goes to A005」; v3 self-hosting flagged the duplicate (CTC-R002, 2/2) |
| v5 | P003's bound scoped to an operation step's own criterion, check steps to A005; A005's pointer to P003 dropped | self-hosting reported two thresholds (v3 1/2, v4 2/2) |
| v6 | §8 step 2 names P003's new routing | v5 self-hosting 2/2 |
| v7 | R004's word list adds 「条件允许时」 | v6 R4-05 cited A005 in 2/9 runs (base 6/6); M4 names the word |
| **v8** | §6 「规则正文」 → 「规则条文」 (wording only; probes and gold are v7's) | v7 self-hosting: T4 put both terms in one paragraph |

## 6. Results on the final candidate (v8; behaviour measured on v7)

### Probes

Behaviour is measured on v7; v8 changes one word in §6. The full table is in `dev/inbox/si4/probes/summary.md`.

| group | base | v7 |
| --- | --- | --- |
| proposal 15 targets (P3-01, P3-05) | 1/6 | 6/6 |
| proposal 15 boundaries (P3-02, P3-03, P3-04, PR-07) | 12/12 | 12/12 |
| metric conditions → A005 (R4-04, R4-07, R4-09) | 6/9 | 9/9 |
| R004 side (R4-01, R4-05, R4-05r, R4-06, R4-08, R4-10) | 21/21 | 21/21 |
| register and tool descriptions (RG-08, RG-10, RG-12, RG-15, RG-16, RG-17, RG-20, RG-21, RG-22) | 27/27 | 27/27 |
| merge authorisation (PC-01, PR-09) | 6/6 | 6/6 |

### Gold

| measure | base (si3 run) | v3 | v4 | v5 | v6 | v7 |
| --- | --- | --- | --- | --- | --- | --- |
| cases / deterministic errors | 56 / 0 | 56 / 0 | 56 / 0 | 56 / 0 | 56 / 0 | 56 / 0 |
| judged pass | 53 | 55 | 53 | 54 | 55 | 54 |
| naturalness | 4.61 | 4.68 | 4.62 | 4.64 | 4.68 | 4.62 |
| over-edit on traps | 0 | 0 | 0 | 0 | 0 | 0 |
| failures | G-A-002, G-T-101, G-R-003 | G-A-002 | G-A-002, G-R-014, G-S-001 | G-A-002, G-R-014 | G-A-002 | G-A-002, G-R-012 |

The baseline's G-T-101 failure is under the old gold; si4's base replicates pass it 3/3 under the amended gold.
Gold replicates on v7 (gold run plus three): G-P-003, G-R-009, G-R-010, G-R-011, G-T-101 4/4 each.

The single-run failures were replicated on base:

| case | base | candidate |
| --- | --- | --- |
| G-R-014 | 3/3 | v5 3/3 |
| G-S-001 | 3/3 judged, but the same spurious 「待确认」 item in 3/3 | v5 2/3 judged; the item in 2/3 |
| G-R-012 | 2/3 judged; findings in 2/3 | v7 2/3 judged; findings in 1/3 |

### Gates and self-hosting

- **Hard gates.** `tools/compare_skill.py` against the baseline, with `--fm-replace` for M2's clause, passes them
  all: 29 rule levels, seven categories, three modes, five ladder rows, six fields, three severities, the
  frontmatter, and `check_skill.py` at 0/0. Body 13 010 → 13 204 characters (+1.5%), 232 lines.
- **Format.** `check_skill.py` 0/0; the frontmatter parses and meets the naming constraints. `skills-ref validate`
  was not run here (auto mode blocks `pnpm dlx`); `tools/package.sh` runs it at acceptance.
- **Self-hosting**, two runs per version:

  | version | findings in si4's own text | what changed next |
  | --- | --- | --- |
  | base | — (targets: 「记录级别」 2/2, 「只报告」 1/2, 「压缩授权」 1/2, 「明确边界」 1/2) | — |
  | v1 | none; every target gone | — |
  | v3 | R003 duplicate subject clause 2/2; A005/P003 thresholds 1/2 | v4, v5 |
  | v4 | A005/P003 thresholds 2/2 | v5 |
  | v5 | §8 list omits P003's routing 2/2 | v6 |
  | v6 | none | — |
  | v7 | threshold scope vs P004 2/2; 规则条文／规则正文 1/2 | v8 (the second); the first is open proposal 26 |
  | v8 | none | — |

## 7. Open items

- **G-A-002** fails in every run, as since r1: the review returns 「未发现违规」 where the gold expects an actor
  ambiguity on 「续期失败时通知租户管理员并回滚」. In 「通知 X 并 Y」 the coordinated verbs share a subject, so the
  gold's second reading (the administrator rolls back) is weak. A gold question for the maintainer, not a
  skill change.
- **G-S-001** — a vague condition on a permitted option (「若延迟预算紧张，也可以推迟」) is raised in 「待确认」 on
  base (3/3) and the candidates alike; the judge passes or fails it inconsistently. Open proposal 23.
- **Review-mode term variants have no rule ID** (「review 模式下它是一条普通 finding」), reported in most si4
  self-hosting runs. A product decision between CTC-T001 and CTC-A005. Open proposal 21.
- **道义强度 and 规范强度** still name one concept. Open proposal 22.
- **「X 完成后」** (R4-01's 「切换完成后」) is not a check step, so B1 does not decide it. Open proposal 24.
- **What 「更高优先级」 refers to**, and how review treats ambiguity the context resolves (second cold decode).
  Open proposal 25.
- **The reporting threshold's scope**: 「破坏性或不可逆」 in A005 and P003 versus P004's guarded operations, which
  include state-changing ones (v7 self-hosting 2/2). Open proposal 26.

## 8. Harness notes

- Probe outputs came in at least eleven finding layouts. `score.py` parses all those seen; each miss was read by
  hand first and recorded in `resolutions.yaml` or in the parser's comments.
- A shared quote does not mean a shared gap. In P3-03, R4-01 and R4-06 a CTC-A005 finding quotes the same span as
  the scored finding but is about another gap (the write traffic's prior state, a resume condition, what 「清理」
  covers). These are scored on the gap; the reading is recorded in `resolutions.yaml`.
- The usage limit stopped v6's first measurement after 21 of 56 gold cases and before any judging. Re-running
  the same commands filled only the missing cases (`ctc_eval.py run` without `--force`).
- The judge's YAML failed to parse in a few batches; each was re-judged, one case at a time where needed.
- `rep_case.sh` takes `VARIANT SKILL_PATH TAG N CASE…`; one launch with the arguments out of order ran nothing and
  was repeated.

## 9. Limitations

- One model family for everything, as in si2 and si3; D001's caution applies to the gold verdicts (G-S-001 is an
  instance). The probes are scored on surface features, which is less exposed to it.
- The gold corpus is still not human-reviewed. G-T-101's amendment is maintainer-decided.
- B1 extends M5 from a missing criterion to an undefined one on a check that nothing destructive depends on
  (P3-05). The maintainer confirmed it at acceptance.
- `skills-ref validate` was not run in this session (auto mode blocks `pnpm dlx`); `tools/package.sh` runs it.

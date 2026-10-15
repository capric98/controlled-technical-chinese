# si3 — Opus 5.5 iteration on decision 007: 状态提示, CTC-R004's class, and register (口语腔)

- **Status:** complete. The maintainer accepted v6 as decision 008 on 2026-10-15; `SKILL.md` is v6.
- **Date:** 2026-10-15
- **Orchestrator:** Claude Opus 5.5 (this session). The maintainer confirmed at the start that every model
  call stays on Opus 5.5, as in si2.
- **Relates to:** `docs/decisions/007-si2-review-routing-and-p002-boundary.md` (open proposals 3, 5, 16),
  `docs/decisions/008-si3-register-r004-class-status-scope.md`
- **Evidence:** `dev/inbox/si3/`, which holds:
  - the probes, the maintainer's resolutions and the scorer;
  - the candidates and `cand/build.py`;
  - the reviews and the adjudication;
  - the self-hosting cases;
  - `runs/outputs.jsonl`.

  Verdicts are in `eval/reports/verdicts-si3.claude.yaml`.

## 1. Question

Decision 007 left three open proposals with the strongest evidence:

- **3** — 状态提示 is in §1's scope but in neither the strict nor the standard scope list. Every si2
  self-hosting run reported it.
- **5** — CTC-R004's word list (尽量…合理) may be closed or open. The §3 example 「尽快回滚」 uses a word
  outside the list, and PR-07 kept a residual A005/R004 variance.
- **16** — No rule licenses register cleanup in error, tool-description and agent-instruction text. si2's E3
  fixed G-R-011 but cost G-R-010 (2/9 against 6/7), because a narrow, genre-scoped branch made R003 read as
  closed.

si3 asks what each one does to behaviour, and changes text only where a pre-registered probe fails or the
maintainer decides.

## 2. Setup

| item | value |
| --- | --- |
| baseline | `SKILL.md` at 17265f7 (si2 final, 232 lines, body 12 692 chars), frozen at `dev/inbox/si3/base/SKILL.md` |
| candidate runs | `claude -p --model claude-opus-5-5` via `tools/ctc_eval.py run` (`CTC_SKILL`, `CTC_CLAUDE_MODEL`), in parallel shards (`dev/inbox/si3/run_set.sh`) |
| semantic judge | the same model, `dev/prompts/judge-semantic.v1.md` unchanged, `--batch 3` (`judge_set.sh`) |
| probes | 29 probes in `dev/inbox/si3/probes/probes.yaml`. Each expectation was registered before any output was seen (hashes and times in the file's dated sections). Three runs per probe per version. Scored on surface features by `probes/score.py` |
| product decisions | three questions to the maintainer after the baseline probe pass, recorded in `probes/resolutions.yaml` |
| candidates | `v1-class`, `v1`, `v2`, `v3`, `v4`, `v5`, `v6`, built from the baseline by exact replacement in `dev/inbox/si3/cand/build.py` |
| reviews | Opus 5.5 subagents with disjoint inputs. Adversarial (`dev/prompts/si3-adversarial.md`), cold reverse-decode (`si3-decode.md`) and naturalness (`si3-naturalness.md`) reviewed v3; a second cold decode (`si3-decode-v6.md`) reviewed v6 |
| gold | full runs of v3, v4, v5 (not judged) and v6; for each version, three replicates of G-R-009, G-R-010, G-R-011, G-S-001 and G-L-006 |
| model calls | 934 candidate outputs in 66 runs: four full gold runs (224); 24 gold replicate runs (120); 24 probe runs (576); 8 self-hosting reviews; 6 G-R-003 replicates. 279 judge verdicts in about 95 calls. 7 review subagents: 3 on v2, stopped at the usage limit; 3 on v3; 1 on v6 |

## 3. Baseline

The baseline's full gold run is si2's run of the same text: 52/56, naturalness 4.73. The failures were
G-A-002, G-T-101, G-R-010 and G-R-011.

Replicates, si2's gold run plus si3's three:

| case | baseline |
| --- | --- |
| G-R-009 | 2/4 |
| G-R-010 | 2/4 |
| G-R-011 | 0/4 |
| G-S-001 | 3/4 |
| G-L-006 | 4/4 |

Probes, three runs each:

- **Proposal 3 — no behavioural fork.** ST-01 (rewrite) and ST-02 (review) both infer strict 3/3. The gap is
  textual: both si3 self-hosting runs on the baseline report it, as did every si2 run.
- **Proposal 5 — no fork on the list.** 「尽快」 and 「视情况」 are already treated as R004 3/3 (R4-01, R4-02), and
  the descriptive 「尽快」 is not reported (R4-03). PR-07 keeps the residual: 「流量正常」 drew an extra R004 in 1/3
  runs.
- **Proposal 16 — the gap reproduces.** 「糟糕！」 stays in an error message 3/3 (PR-19), and 「啦」 in a status
  message 3/3 (RG-07). The conversational frames survive in tool descriptions: RG-03 0/3, RG-08 1/3,
  RG-10 0/3. In RG-06, one baseline run cleaned 「哦」 and raised 「千万不要」 to 「不得」.

## 4. Product decisions (maintainer, 2026-10-15)

| question | answer |
| --- | --- |
| Q1: which mode 状态提示 belongs to | strict, next to 告警与错误信息 |
| Q2: whether register cleanup applies to user-facing error and status messages by default | all genres; a tone convention given by the caller wins |
| Q3: where CTC-R004's boundary lies | an open class of degree, timing and discretion words; an undefined state or a missing value (流量正常、一段时间、多次) is CTC-A005 |

## 5. Iterations

| version | change | what decided it |
| --- | --- | --- |
| v1-class | S1 状态提示 in strict; S2 R004 open class + exclusion to A005; S3 R003 gains 口语腔 (five types), stated for every genre, examples kept off the gold sources | first draft against all three cases at once, avoiding E3's genre scoping |
| v1 | v1-class plus a boundary sentence: 推测「吧」, 强度「千万」, 警示「危险！」, quoted replies, the caller's tone | ablation partner |
| v2 | boundary reduced to 「千万」; translationese example 「使用户能够…」 for G-R-010 | the ablation: only the strength clause is load-bearing (RG-06 raised 3/3 without it, 0/3 with it); PR-16, PR-17, PR-18 and RG-05 pass 3/3 with no boundary text |
| v3 | the translationese example is reverted; R003's requirement states the tool-description form; R004 「时限」 becomes 「时机」 | G-R-010 settled on 「该工具允许调用者获取…」 (direct form 1/9 across v1, v1-class, v2; base 7/11); PR-07 v2 r1 read 「一段时间」 as a 「时限词」 |
| v4 | wording from the naturalness review; the tool-description sentence becomes the repair form, about the subject rather than the content; §8 step 2 lists R004's exclusion | the three reviews of v3 and v3 self-hosting r2 (see `dev/inbox/si3/review/adjudication.md`) |
| v5 | the strength boundary is stated by function; §7 steps 6 and 7 name 口语腔 | adversarial counterexample RG-13 (「可别…哦」 raised to 「不得」 3/3 on v4) |
| **v6** | the boundary names the repair: 「去口语腔时禁止的强度不变：「千万不要」「可别」这类口语禁止保留原词或改作「切勿」，不改作「不得」「禁止」。」 | RG-13 still raised 2/3 on v5; RG-18 (「绝对别」, not quoted in the rule) was raised 0/3 by base and v5 |

## 6. Results on the final candidate (v6)

### Probes

The full table is in `dev/inbox/si3/probes/summary.md`.

| group | base | v6 |
| --- | --- | --- |
| 状态提示 (ST-01, ST-02) | strict 3/3 | strict 3/3 |
| R004 (R4-01–R4-03, PR-07) | 11/12 | 12/12 |
| register targets (PR-19, RG-03, RG-07, RG-08, RG-10) | 1/15 | 15/15 |
| register boundaries (PR-16–PR-18, RG-01, RG-02, RG-04, RG-05, RG-09, RG-11, RG-12, RG-14, RG-16, RG-17, RG-19) | 42/42 | 42/42 |
| strength (RG-06, RG-13, RG-18) | 5/9 | 9/9 |
| RG-15 (registration ruled wrong, §7) | 3/3 unchanged | rewritten to 「该函数用于…」 3/3, ruled correct |

### Gold replicates

One gold run plus three replicates:

| case | base | v6 |
| --- | --- | --- |
| G-R-009 | 2/4 | 4/4 |
| G-R-010 | 2/4 | 4/4 |
| G-R-011 | 0/4 | 4/4 |
| G-S-001 | 3/4 | 4/4 |
| G-L-006 | 4/4 | 4/4 |

The judge's G-R-010 verdicts are lenient on the permission frame: it passed 「该工具允许调用者获取…」 in some v1
and v2 runs and failed it in si2. So the surface form is counted too. A direct 「获取…」/「用于…」 opening
appears in 4/4 v6 runs, against 7/11 on the baseline across si2 and si3.

### Full gold

| measure | base (si2 run) | v3 | v4 | v6 |
| --- | --- | --- | --- | --- |
| cases / deterministic errors | 56 / 0 | 56 / 0 | 56 / 0 | 56 / 0 |
| judged pass | 52 | 54 | 54 | 53 |
| naturalness | 4.73 | 4.71 | 4.64 | 4.61 |
| over-edit on traps | 0 | 0 | 0 | 0 |
| failures | G-A-002, G-T-101, G-R-010, G-R-011 | G-A-002, G-T-101 | G-A-002, G-T-101 | G-A-002, G-T-101, G-R-003 |

G-A-002 and G-T-101 fail in every run since r1. G-R-003: see §7.

### Gates and self-hosting

- **Hard gates.** `tools/compare_skill.py` against the baseline passes them all: 29 rule levels, seven
  categories, three modes, five ladder rows, six fields, three severities, frontmatter, and `check_skill.py`
  at 0/0. Body 12 692 → 13 010 characters (+2.5%), 232 lines.
- **Format.** `skills-ref validate` on a packaged copy of the candidate: valid. `tools/package.sh` packages
  the root `SKILL.md`, so it runs once the candidate is copied there.
- **Self-hosting**, two runs per version:

  | version | findings per run | 状态提示 gap | R004 list |
  | --- | --- | --- | --- |
  | base | 5, 8 | reported 2/2 | — |
  | v3 | 5, 5 | 0/2 | 0/2 |
  | v4 | 5, 6 | 0/2 | 0/2 |
  | v6 | 4, 7 | 0/2 | 0/2 |

  v3 r2 found one inconsistency in si3 text (§8 step 2 omitted R004's exclusion), and v4 fixed it. v4 and
  v6 raise none in si3 text. The recurring findings all predate si3: frontmatter 「只报告」, 「记录级别」,
  道义/规范强度, P003's 「压缩授权」, and R003's 「过长」.

## 7. Open items

- **RG-15, ruled by the maintainer.** 「通过这个函数，开发者可以把图片压缩到指定尺寸，最大支持 4096 像素。」 (no particle) is
  rewritten to 「该函数用于…」 3/3 on v4–v6. The registration expected it unchanged, as text with no listed
  defect. The model reads 「开发者可以」 as reader-directed guidance, a listed defect. G-R-010's gold requires
  this repair of the same frame. Narrowing the rule brought G-R-010 back in every si3 attempt, so the text is
  not narrowed. The second cold decode of v6 reads the text as the registration does (unchanged), so text and
  behaviour split here. The maintainer ruled the registration wrong: the rewrite matches G-R-010's gold and
  stands. Saying so in R003's text, so that a cold reader predicts it, is open proposal 20 in decision 008.
- **G-R-003 in the v6 gold run:** two consecutive 「被」 clauses. R003's translationese list is identical in v4
  and v6. Three replicates each:

  | | base | v6 |
  | --- | --- | --- |
  | si3 replicates | 3/3 | 3/3 |
  | pooled | 5/5 (si2's two runs included) | 3/4 |

  No replicate used the double 「被」. This is treated as single-run noise of the kind 007 describes, not as a
  regression; it is listed so the next round can watch it.
- **Not probed in si3**, listed for the next round:
  - a degree word on a state (「负载过高时」), which may be reported under both R004 and A005;
  - 「条件允许时」, which goes to A005 and so loses the strength question that §5 asks for;
  - the suggestion 「吧」 (「先别切主吧」);
  - colloquial words outside the five 口语腔 types (「搞定」);
  - 「及时」 read as a missing duration;
  - 「告警」 naming two concepts;
  - the frontmatter not naming 状态提示 (open proposal 10).

## 8. Harness notes

- Probe outputs come in at least five finding layouts: field lists, tables with and without a number
  column, bold rule-ID headers, and one-line 「CTC-A005 · ERROR · …」 headers. `score.py` parses all of them. Each
  parser miss was found by reading the output, not trusted.
- The usage limit stopped the session once. Seven gold calls exited 1 and the first three reviews were killed
  before writing. Re-running the same shard command skips cases already done (`ctc_eval.py run` without
  `--force`).
- Two judge batches failed to parse on the first attempt and passed on retry (`--batch 3`).

## 9. Limitations

- One model family for everything, as in si2; D001's caution applies to the gold verdicts. The probes are
  scored on surface features, which is less exposed to it.
- The strength ordering behind RG-06, RG-13 and RG-18 (「千万不要」「可别」 below 「不得」「禁止」) comes from
  G-R-009's gold, which is orchestrator-reviewed, not human-reviewed.
- The gold corpus is still not human-reviewed.
- v2 and v5 were superseded within the session. v5's full gold run was not judged.

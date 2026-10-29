# 009 — si4: missing-criterion bounds, metric conditions in CTC-A005, and self-hosting terminology

- **Status:** Accepted by the maintainer on 2026-10-29, with the rulings below.
- **Date:** 2026-10-29
- **Relates to:** `000-design.md` §15, §20, §21, §22, §30; `002-gold-case-schema.md` (gold edits);
  `004-rule-set-adjudications.md` §3; `007-si2-review-routing-and-p002-boundary.md` open proposal 15;
  `008-si3-register-r004-class-status-scope.md` open proposals 10 (in part), 18, 19, 20; `eval/disagreements/D004`
- **Evidence:** `eval/reports/si4-summary.md`; `eval/reports/verdicts-si4.claude.yaml`; `dev/inbox/si4/`, which
  holds the probes and resolutions, the candidates with `cand/build.py`, the reviews and adjudication, the
  self-hosting cases and `runs/outputs.jsonl`
- **Candidate:** `dev/inbox/si4/cand/v8/SKILL.md`

## Context

si4 is a single-model iteration on decision 008's text. At the start the maintainer confirmed that every model
call stays on Claude Opus 5.5 (M1). It used si3's method: every expectation registered before any output, three
runs per probe per version, and text changed only where a probe or a self-hosting run failed or the maintainer
decided. 26 probes ended up registered: 18 before the first run, 4 after the baseline pass, 3 from the
reviewers' counterexamples and 1 after the v6 runs, each before its first output (`dev/inbox/si4/probes/probes.yaml`).

Targets, from 008's open proposals and the recurring self-hosting findings:

- **15 — the A005/P003 overlap.** On the baseline, a read-only closing check with no criterion
  (「检查 `search-api` 的运行情况」) is reported as CTC-A005/ERROR in 2/3 review runs (P3-01), while rewrite
  raises nothing 3/3 under P003's bound (P3-02). With one word changed (「确认…运行正常」) review reports it 3/3
  (P3-05).
- **19 — the probes si3 did not run.** A degree word on a metric forks between R004 and A005: 「负载过高」
  A005, R004, A005 (R4-04); 「磁盘占用偏大」 R004, R004, A005 (R4-07). 「条件允许时」 (R004 with the strength
  column, 3/3), 「及时」 (R004 3/3), the suggestion 「吧」 and 「搞定」 do not fork.
- **20 — the third-person frame.** Runtime already rewrites 「通过这个函数，开发者可以…」 (RG-15 3/3), as the
  maintainer ruled in 008; si3's second cold decode did not predict it.
- **Self-hosting terminology.** 「记录级别」 is reported by every self-hosting run since si2 (si3 8/8, si4 base
  2/2). The frontmatter's 「歧义只报告不擅自消解」 contradicts §5 (si3 5/8, si4 base 1/2). P003 names one
  authorisation two ways (「压缩授权」, 「授权合并步骤」; si3 3/8, base 1/2). 「明确边界」 is undefined (2/4 on
  this exact text). §9 item 1's example has no direction marker (si3 2/8).

The maintainer decided six questions (`dev/inbox/si4/probes/resolutions.yaml`):

- **M1:** every model call stays on Opus 5.5.
- **M2:** unfreeze one frontmatter clause: 「上下文不足以确定的歧义只报告、不擅自消解」.
- **M3:** amend G-T-101 to align with 004 §3 (below).
- **M4:** a degree word that leaves an unstated threshold on a metric (「负载过高」) is CTC-A005, like 「多次」;
  R004 keeps the words that leave whether, when or how much to act to the reader (尽量、尽快、及时、必要时、
  视情况、条件允许时).
- **M5:** review applies P003's bound too; A005 does not take a missing criterion on a check that nothing
  destructive depends on.
- **M6:** 「先别切主吧」 → 「先不要切主」 keeps the strength; no text change.

## Decision

Twelve exact replacements in `SKILL.md` (`build.py`, `VARIANTS["v8"]`). No rule ID, level, 「待确认」 category,
mode heading or ladder row changes. One frontmatter clause changes, by M2; `tools/compare_skill.py` gains
`--fm-replace OLD NEW` so the gate allows exactly that replacement and nothing else.

**F1 — frontmatter (M2).** 「歧义只报告不擅自消解」 → 「上下文不足以确定的歧义只报告、不擅自消解」.

**B1 — CTC-A005 and CTC-P003 (proposal 15, M5).** A005's row gains:

> 检查或确认步骤没有给出判据或判据含义未定（「确认无异常」），而没有破坏性或不可逆操作取决于它的结果时，不提出、不报告。

P003's last sentence is scoped to an operation step's own criterion and hands check steps to A005:

> 来源未给出操作步骤自身的成功判据时：只有当该步是破坏性或不可逆操作、且后续步骤的安全性取决于它是否成功，才按「待确认」第 2 类提出；其余操作步骤缺少判据不提出，以免正常的流程文档产生成串的未决项。检查或确认步骤缺少判据按 CTC-A005 处理。

§8 step 2's list of rows that route to A005 adds 「CTC-P003 中检查或确认步骤缺少判据」.

**B2 — CTC-R004's exclusion (proposal 19, M4).**

> 未定义的状态（「服务稳定」）、未给出具体值的次数或时长（「多次」「若干分钟」），以及用程度词描述运行指标而未给出阈值的触发条件（「延迟较高时」），都不是这类词，按 CTC-A005 处理。

§8 step 2 names the same three kinds: 「CTC-R004 排除项中的未定义状态、次数、时长与运行指标触发条件」.
R004's word list adds 「条件允许时」, which M4 names among the words R004 keeps: without it, v3–v6 cite
「条件允许」 as an undefined state (A005) in 3 of 21 runs (base 0/6).

**C1 — CTC-R003 (proposal 20).** The 口语腔 list gains 「工具描述中以使用者作主语陈述功能的句式（「调用者可以…」）」,
and the repair sentence after it keeps only the direct form: 「去除这些缺陷时，工具描述改为直接陈述功能（「获取…」「用于…」）。」

**T1–T5 — terminology and definitions.**

- T1 (proposal 18): 「A、P 两族按其记录级别生效」 → 「按其级别生效」.
- T2: P003 → 「来源把验证单独列为一个步骤时，该步骤保持独立；调用方授权合并步骤（明确要求合并，或限定步骤数）时可以并入相邻步骤…」.
  This states the split the runs already show: a step cap merges (PR-09 3/3, as D004 intends), a character
  cap does not (PC-01 3/3).
- T3: §9 item 1 → 「…应写成「用户打开控制台后，点击设置修改端口。」」.
- T4: §6 → 「**应** = 默认要求，可被更高优先级推翻，也可被规则条文写明的边界推翻」.
- T5: §6 「规则正文中的「必须」「不得」」 → 「规则条文中的…」, the term §3 and §8 use. T4 had put both terms in one
  paragraph (v7 self-hosting).

### Gold amendment (M3)

G-T-101's first terminology invariant accepted only unification of 「灰度发布／金丝雀发布／小流量验证」. Decision
004 §3 says that when co-reference is not clear, variants are reported rather than merged, and every run since
r1 that failed this case raised the co-reference question in 「待确认」. `002-gold-case-schema.md` permits a gold
edit only through a decision record arguing the case is wrong; this is that record. The invariant now accepts
either unification or raising the question in 「待确认」; merging 「全量发布」 into the gray-release term still
fails. The case's `notes` record the revision. Re-judged on the unchanged baseline outputs, G-T-101 goes from
0/3 to 3/3 (pre-amendment verdicts kept in `eval/reports/raw/si4-judging/pre-M3/`, not tracked).

### Gate items (`000-design.md` §20)

| | B1 | B2 | C1 | T1–T5, F1 |
| --- | --- | --- | --- | --- |
| failing input | P3-01 (A005/ERROR 2/3), P3-05 (3/3) on a read-only closing check | R4-04 (A005, R004, A005), R4-07 (R004 2/3) | si3's second cold decode predicted RG-15 unchanged | self-hosting findings, counts above |
| risk | review floods runbooks with ERROR findings that rewrite never raises; the same text gets a different result per mode | the same gap gets a different rule ID, severity and strength column per run | the text and the ruled behaviour split | two names for one concept; a description that contradicts the body; an undefined override criterion |
| existing rules insufficient | P003's bound said 「不提出」 for rewrite only; A005's 「缺少……判据」 has no bound | R004's exclusion named states, counts and durations, not degree words on metrics | the repair sentence applied only after a listed defect | the rows themselves carried the inconsistency |
| test that fails before and passes after | P3-01 1/3 → 3/3; P3-05 0/3 → 3/3 | R4-04 2/3 → 3/3; R4-07 1/3 → 3/3 | cold decode of v1 and v3 predicts the rewrite | self-hosting 0/2 on each of these after the change |
| boundary | P3-02 and P3-04 (rewrite), P3-03 (a destructive step is still P003), PR-07 (a criterion that gates a destructive action is still A005) | R4-01, R4-05, R4-06, R4-08 (「适当的值」) stay R004; R4-09 A005 | RG-12 (restriction kept), RG-16 (agent permission kept), RG-17, RG-22 (developer-guide prose unchanged) | PC-01 and PR-09 (T2's split), RG-* (no register drift) |

Every clause beyond the first wording is there because a run, a review or a self-hosting pass failed without it:

- **B1.** v1 deferred to P003 and kept 「给出的判据含义未定…仍按本规则」. The model read 「运行情况」 as an undefined
  criterion: P3-01 got worse (A005 3/3) and rewrite began raising it (P3-02 2/3). v2 stated the exclusion by its
  own condition (P3-01 3/3 clean). v5 split the two rows' scopes after self-hosting reported two thresholds
  (v3 1/2, v4 2/2).
- **B2.** 「可测量指标」 would cover 「调到适当的上限」 (adversarial review); 「设限而未给出阈值」 read as
  self-contradictory (naturalness review). A shorter §8 wording (「CTC-R004 中按 CTC-A005 处理的说法」) was read
  as routing everything R004 finds to A005 (v3 R4-05 r1) and was reverted. 「条件允许时」 joined the word list
  after v6 cited it as A005 in 2/9 runs; R4-10 (「时间允许时」, not listed) checks that the line generalises.
- **C1.** 「同属此类」 stipulated a third-person frame into reader guidance, and the unqualified clause caught a
  usage restriction; the item became its own entry limited to frames that state the function. The duplicated
  subject clause in the repair sentence was dropped after self-hosting flagged it (v3 2/2); G-R-010 still
  passes 4/4.

## Alternatives considered

- **B1 as a deferral to P003 with a carve-out for undefined criteria (v1).** Rejected on the runs (above).
- **The adversarial reviewer's B1 wording** (「步骤缺少成功判据或缺少验证方式时，这一缺失是否提出或报告按 CTC-P003 判断；给出的判据含义未定…仍按本规则」).
  Not adopted: it keeps the carve-out that failed.
- **Route degree words on metrics to R004 (M4's other option).** Rejected by M4.
- **Report missing criteria in rewrite too (M5's other option).** Rejected by M5.
- **Change G-T-101's skill behaviour instead of the gold (M3's other option).** Rejected by M3; it would
  partly supersede 004 §3.
- **Unfreeze the whole frontmatter (M2's other option).** Rejected by M2.
- **Unify 道义强度／规范强度, give R003's 「过长」 a criterion, and name a rule ID for review-mode term
  variants.** Not attempted: each needs a product decision (below).

## Verification

- **Probes.** 26 probes, three runs each, more where a cell wobbled; behaviour is measured on v7 (v8 changes one
  word in §6). Full table: `dev/inbox/si4/probes/summary.md`. By group:

  | group | base | v7 |
  | --- | --- | --- |
  | proposal 15 targets (P3-01, P3-05) | 1/6 | 6/6 |
  | proposal 15 boundaries (P3-02, P3-03, P3-04, PR-07) | 12/12 | 12/12 |
  | metric conditions → A005 (R4-04, R4-07, R4-09) | 6/9 | 9/9 |
  | R004 side (R4-01, R4-05, R4-05r, R4-06, R4-08, R4-10) | 21/21 | 21/21 |
  | register and tool descriptions (RG-08, RG-10, RG-12, RG-15, RG-16, RG-17, RG-20, RG-21, RG-22) | 27/27 | 27/27 |
  | merge authorisation (PC-01, PR-09) | 6/6 | 6/6 |

  R4-05 is 6/6 on v7 and on base; on v6, before 「条件允许时」 was listed, it was 7/9.
- **Gold replicates.** One gold run plus three replicates per case on v7: G-P-003, G-R-009, G-R-010, G-R-011 and
  G-T-101 4/4 each (base 3/3 each in si4's replicates, G-T-101 under the amended gold).
- **Full gold.** 56/56 cases, 0 deterministic errors, no over-edit on any trap, on every full run:

  | | v3 | v4 | v5 | v6 | v7 |
  | --- | --- | --- | --- | --- | --- |
  | judged pass | 55 | 53 | 54 | 55 | 54 |
  | naturalness | 4.68 | 4.62 | 4.64 | 4.68 | 4.62 |
  | failures beside G-A-002 | — | G-R-014, G-S-001 | G-R-014 | — | G-R-012 |

  G-A-002 fails in every run since r1. Each other failure is a single run that replicates do not reproduce
  against base: G-R-014 passes 3/3 on base and v5; G-S-001 carries the same spurious item on base 3/3 (the judge
  passed those); G-R-012 reports findings on base in 2/3 replicates and on v7 in 1/3. The baseline's own full
  run (si3) scored 53/56 with G-T-101 failing; under the amended gold that case passes.
- **Hard gates.** `tools/compare_skill.py` against the baseline, with `--fm-replace` for M2's clause, passes them
  all (`dev/inbox/si4/cand/gate-v8.json`). Body 13 010 → 13 204 characters (+1.5%), 232 lines.
- **Format.** `tools/check_skill.py`: 0 errors, 0 warnings. The frontmatter parses as YAML with `name` and
  `description` only; `name` meets the naming constraints and `description` is 204 characters. `skills-ref
  validate` was not run in this session: auto mode blocks `pnpm dlx`, which downloads the validator. It is to be
  run with `tools/package.sh` at acceptance.
- **Reviews.** Three independent Opus 5.5 reviews of v1 (adversarial, cold reverse-decode, naturalness) and a
  second cold decode of v3. Rulings: `dev/inbox/si4/review/adjudication.md`.
- **Self-hosting.** Two runs on each of base, v1, v3, v4, v5, v6, v7 and v8. Every finding that si4 targets is
  gone from v1 on (「记录级别」, frontmatter 「只报告」, 「压缩授权」, 「明确边界」, §9's direction). Each finding the
  candidates raised in si4's own text was fixed in the next version (v3 → v4, v4 → v5, v5 → v6, v7 → v8), except
  the threshold scope (open proposal 26). v8 raises none in si4 text; what it reports predates si4.

## Limitations

- **One model throughout.** D001's caution applies to the gold verdicts. G-S-001 shows it: the judge passed
  three baseline runs that carry two spurious 「待确认」 items and failed a v5 run carrying one. Probe scores are
  surface features and less exposed.
- **The gold corpus is still not human-reviewed.** G-T-101's amendment is maintainer-decided, not
  human-reviewed case by case.
- **M5 is extended by one step.** M5 was asked about a check with no criterion. B1 also covers a check whose
  criterion is given but undefined (「确认无异常」), when nothing destructive depends on it (P3-05). The
  maintainer confirmed the extension at acceptance.
- **The frontmatter still names neither 状态提示 nor 口语腔** (open proposal 10); M2 unfroze one clause only.

## Maintainer rulings at acceptance

1. **M5's extension** to undefined criteria on non-gating checks (P3-05). **Ruled (maintainer, 2026-10-29):**
   confirmed; P3-05's expectation stands.
2. **F1 wording.** The naturalness reviewer proposes 「上下文不足以确定读法的歧义…」, which names the object of
   「确定」 and matches §5. **Ruled:** keep the clause as M2 approved it.
3. **「工具描述」 versus 「工具与函数描述」** in R003 (adversarial review). RG-15, a function, is rewritten 3/3 on
   every version; widening the word is not a narrowing, so it was left. **Ruled:** left open.
4. **The reporting threshold's scope.** B1 and P003 say 「破坏性或不可逆」; P004's guarded list also names
   state-changing operations (restart, scale-out, release). v7 self-hosting reports the mismatch 2/2. B1 follows
   M5 and P003's existing wording; widening it would report more. **Ruled:** left open as proposal 26.

## Open proposals after si4

- **Resolved:** 15 (B1), 18 (T1), 19 (B2; the 「吧」, 「搞定」, 「条件允许时」 and 「及时」 probes do not fork), 20 (C1),
  and the frontmatter clause of 10 (F1).
- **Still open from 006–008:** 1 (「必须」 inside 「应」 rows), 2 (R003 「过长」; self-hosting 5/10 runs before si4),
  7 (category 7 narrower than S001), 8 (P004/R005 attribution; reported again in si4 self-hosting), 9 (T001
  tie-break), 10 (frontmatter terminology beyond F1), 17 (「告警」 names two concepts).
- **New:**
  - 21 — review-mode term variants have no rule ID (「review 模式下它是一条普通 finding」): T001 or A005.
    Reported by self-hosting in v1 2/2, v3 1/2, v4 1/2, v5 1/2. A product decision.
  - 22 — 道义强度 and 规范强度 name one concept (self-hosting in most runs since si2). The frontmatter says
    规范强度; the body's tuple says 道义强度.
  - 23 — a vague condition on a permitted, conservative option is raised in 「待确认」 (G-S-001: base 3/3,
    v5 2/3), against the over-edit trap's intent.
  - 24 — 「X 完成后」 as a condition (R4-01's 「切换完成后」) forks between P003 and A005 on the baseline and is
    not a check step, so B1 does not decide it.
  - 25 — what 「更高优先级」 refers to (second cold decode); how review treats ambiguity the context resolves.
  - 26 — whether the missing-criterion threshold in A005 and P003 (「破坏性或不可逆」) should match P004's guarded
    operations, which include state-changing ones (v7 self-hosting 2/2).

## Consequences

- **`SKILL.md`** is `dev/inbox/si4/cand/v8/SKILL.md`, byte for byte. Section numbers do not change.
  `skills-ref validate` remains to be run with `tools/package.sh` (Verification, Format).
- **`eval/gold/gold-tokens.yaml`:** G-T-101's first invariant, its second invalid transformation's reason, and its
  notes (M3).
- **`tools/compare_skill.py`:** `--fm-replace OLD NEW` for maintainer-approved frontmatter edits.
- **`spec/rules.v0.yaml`:** A005 gains the check-step exclusion; P003's bound is scoped to operation steps and
  its merge authorisation is named; R004's exclusion gains metric trigger conditions; R003's 口语腔 list gains the
  third-person frame; the review routing gains P003 and R004's three kinds. A revisions entry records F1, T1–T4,
  B1, B2, C1, M1–M6 and the G-T-101 amendment.

# 010 — si5: permission and description exemptions, the guarded-operation threshold, zero anaphora, and one name for normative strength

- **Status:** Accepted by the maintainer on 2026-11-09.
- **Date:** 2026-11-09
- **Relates to:** `000-design.md` §15, §20, §21, §22, §30; `002-gold-case-schema.md` (gold edits);
  `004-rule-set-adjudications.md` §3; `005-reverse-decoding-findings.md` C1;
  `009-si4-criteria-bounds-metric-conditions-terminology.md` open proposals 8, 21, 22, 23 and 26
- **Evidence:** `eval/reports/si5-summary.md`; `eval/reports/verdicts-si5.claude.yaml`; `dev/inbox/si5/`, which
  holds:
  - the probes, resolutions and scorer;
  - the candidates with `cand/build.py`;
  - the reviews and adjudication;
  - the self-hosting cases;
  - `runs/outputs.jsonl`.
- **Candidate:** `dev/inbox/si5/cand/v2/SKILL.md` (sha256 `759bc53c…`)

## Context

si5 is a single-model iteration on decision 009's text (`SKILL.md` at 283ec5a, si4 v8). At the start the
maintainer confirmed that every model call stays on Claude Opus 5.5 (M1). It used si3 and si4's method:

- every expectation registered before any output;
- three runs per probe per version;
- text changed only where a probe or a self-hosting run failed, or the maintainer decided.

25 probes ended up registered, each before its first output (`dev/inbox/si5/probes/probes.yaml`):

- 17 before the first run;
- 6 from the reviewers' counterexamples;
- 2 after the maintainer's decisions on v1.

Targets, from 009's open proposals and the recurring self-hosting findings:

- **23 — vague conditions on permissions.**
  - 「若导出队列较长，也可以拆成多批提交」 only widens what the operator may do. The baseline raises it in rewrite
    (OR-01) and reports it as A005 in review (OR-02), both 3/3. G-S-001's gold treats the same shape as
    compliant.
  - The related over-report: a sentence that only describes system behaviour (「连接数接近上限时，网关会拒绝新的
    长连接请求」) draws A005 3/3 in review (OR-03). G-R-012's gold calls that a false positive.
- **21 — review-mode term variants.** The text says 「一条普通 finding」 and names no rule ID. Runtime already
  reports CTC-T001 (TV-01, TV-02 6/6). Self-hosting reported the gap in most si4 runs and in si5 base 1/2.
- **26 — the threshold's scope.** A005's check-step bound and P003's own-step bound said 「破坏性或不可逆」.
  P004's guarded list also has state-changing operations (restart, scale-out, release). Runtime already reports
  a vague check that gates a restart (TH-01 A005 3/3, TH-02 「待确认」 3/3). A deploy runbook's release step with
  no criterion is P003 in review 3/3 (HR-02) but raised 0/3 in rewrite (HR-01).
- **22 — 道义强度／规范强度.** The two names refer to one concept. The frontmatter says 规范强度, while S003's tuple
  and §3's authorisation list say 道义强度. Self-hosting has reported the pair in most runs since si2.
- **8 (in part) — R005 and warning blocks.** P004 calls moving a standalone warning block an R005 violation,
  but R005 names no position. Self-hosting reported this in si3 and si4.
- **G-A-002** has failed in every run since r1 (below).

The maintainer decided ten questions (`dev/inbox/si5/probes/resolutions.yaml`). Three were decided before any
output was read, four after the baseline probe pass and three after the v1 runs and reviews:

- **M1:** every model call stays on Opus 5.5.
- **M2:** 「规范强度」 everywhere.
- **M3:** amend G-A-002's gold (below).
- **M4:** a condition that only widens what the operator may do, with the default action unchanged, is neither
  raised nor reported.
- **M5:** a description of system behaviour asks the reader to decide nothing; a missing threshold in it is not
  reported.
- **M6:** the missing-criterion threshold covers P004's guarded operations (destructive, irreversible or
  state-changing), as runtime already behaves.
- **M7:** a review-mode term variant of unclear co-reference is CTC-T001.
- **M8:** the permission exemption does not cover a permitted destructive, irreversible or state-changing
  action (「若磁盘紧张，也可以删除 `/backup/` 下 30 天前的备份」 stays reported).
- **M9:** keep H2, so rewrite raises the release step's missing criterion as review already reports it.
- **M10:** fix this round: an object that the preceding text uniquely recovers is not missing and stays
  omitted.

## Decision

Eight exact replacements in `SKILL.md` (`build.py`, `VARIANTS["v2"]`). No rule ID, level, 「待确认」 category,
mode heading, ladder row or frontmatter text changes.

**D1' — §5 「不算真歧义」 (proposal 23; M4, M5, M8).** After 「参数在运行时由外部唯一确定」:

> ；条件只放宽对操作者的限制（「若…，也可以…」），而默认动作不变、来源规定的义务不被免除、所许可的也不是破坏性、不可逆或改变外部状态的操作；文本只描述系统行为，不要求读者据此行动。后两种情形即使缺少判据或阈值，也不按 CTC-A005 或 CTC-R004 提出或报告。

**H1' — CTC-A005's check-step bound (proposal 26; M6).** Restated as a contrapositive, matching P003's
「只有当…才…」, with the threshold widened:

> 检查或确认步骤没有给出判据或判据含义未定（「确认无异常」）时，只有当破坏性、不可逆或改变外部状态的操作取决于它的结果，才提出或报告。

**H2' — CTC-P003's own-step bound (M9).**
「只有当该步是破坏性、不可逆或改变外部状态的操作，且后续步骤的安全性取决于它是否成功，才按「待确认」第 2 类提出」.

**Z1 — CTC-P002 (M10).** After 「「相关配置」「对应服务」这类说法不算写出对象。」:

> 省略的对象可由前文唯一确定（零形回指）时，不算缺少对象，保持省略。

**V1' — the T paragraph (proposal 21; M7).** 「review 模式下它是一条普通 finding。」 →
「review 模式下它是一条 CTC-T001 finding。」

**N1', N2 — normative strength (proposal 22; M2).**

- §3: 「调整道义强度（规范强度）」 → 「调整来源中的规范强度」.
- CTC-S003: 「(认识强度, 规范强度, 言语行为类型)」.

**S1' — CTC-R005 (proposal 8, in part).** 「链接与引用块应保持其粒度，独立告警块应保持原位。」 This keeps
P004's attribution and its WARNING level.

### Gold amendment (M3)

The source of G-A-002 is 「续期失败时通知租户管理员并回滚到上一版本证书」, and the case is run in review mode.
The gold expected a CTC-A005/ERROR finding saying the rollback's actor cannot be determined. On that reading,
either the renewal service rolls back or the notified administrator does.

In 「通知 X 并 Y」, 「并」 joins two predicates that share one subject: the renewal service notifies and rolls
back. For the administrator to roll back, Chinese uses a pivotal construction (「通知租户管理员回滚」), and the
source does not have one. The second reading is therefore not one the text supports. Every model in every run
since r1 has reported 「未发现违规」.

`002-gold-case-schema.md` permits a gold edit only through a decision record that argues the case is wrong; this
is that record. The changes:

- The actor invariant and the expected issue are removed (`expected_issues: []`).
- The two invalid transformations keep the instruction and over-edit violations, which test what the case
  was written for: review must not rewrite the document, and must not report 「由续期服务发起」 as a missing
  agent.
- The case's `notes` record the revision.

Base, v1 and v2 pass it 3/3 each.

### Gate items (`000-design.md` §20)

| | D1' | H1', H2' | Z1 | V1', N1', N2, S1' |
| --- | --- | --- | --- | --- |
| failing input | OR-01, OR-02 (permission), OR-03 (description): A005 3/3 on base | HR-01: rewrite raises nothing on a release step that review reports 3/3 (HR-02); TH-01, TH-02 report beyond the text's 「破坏性或不可逆」 | G-S-001: v1 inserts 「将索引重建」 in 4/7 runs | self-hosting: T001 missing ID (si4 most runs, base 1/2), 道义／规范 (base 1/2), R005's position (si3, si4) |
| risk | runbooks and API docs fill with ERROR findings and pending items on discretion the author left on purpose | the same release step is a finding in review and silent in rewrite; the text and runtime disagree on the threshold | a correct source is edited (over-edit trap) | a finding with no rule ID; two names for one concept; an attribution with no rule text |
| existing rules insufficient | §5 named only runtime-determined parameters; R004's descriptive exclusion covers degree adverbs, not missing thresholds; A005 has no scope sentence | the bounds named destructive or irreversible only | P002 says what is not a written object, not when an omitted one is recoverable | the rows themselves carried the gap |
| test that fails before and passes after | OR-01, OR-02, OR-03 0/3 → 3/3 | HR-01 0/3 → 3/3; TH-01, TH-02 3/3 kept | G-S-001 insertion 4/7 (v1) → 1/7 (v2; base 1/7); ZA-01 2/3 → 3/3 | self-hosting: none of these on v2 (0/2) |
| boundary | OR-04, OR-05 (the same condition on a required action) 3/3; OR-06, OR-06r (destructive permission) 3/3; OR-07 (waiver) reported 3/3; OR-08 (symptom section) 3/3 | HR-02: no P003 on steps 1 and 3 (3/3); HR-01: exactly one item (3/3); P3-01, P3-05 (closing checks) 3/3 | PR-13 (「重启对应服务」) P002 3/3 | TV-01, TV-02 still T001; R4-* unchanged |

Every clause beyond the first wording is there because a run or a review failed without it:

- **D1.** v1 exempted any 「若…，也可以…」 with the default action unchanged.
  - The decoder and the naturalness reviewer found that a permitted destructive action passes that literal
    test, and OR-06 confirmed it (v1 silent 3/3, base A005 3/3). That became M8 and the third qualifier.
  - The adversarial reviewer found that a permission waiving a control the source requires (OR-07) is an
    obligation with a vague trigger. v1 was silent 3/3; v2 reports it 3/3.
  - The naturalness review replaced 「放宽…可以做的事」 and 「同样」.
- **H1, H2.** The adversarial reviewer argued for dropping H2, since every cited case was a check step. The
  maintainer kept it (M9) on HR-01 and HR-02. The data: v1 and v2 raise exactly one item, on the release
  step, and no chain of items.
- **V1.** 「review 模式下按 CTC-T001 报告」 dropped 「它是一条」. That let the clause inherit 「只有当它妨碍执行时」
  from the strict/standard half (adversarial review), so v2 restores it.
- **N1.** 「调整规范强度」 can be read as adjusting the skill's own rule levels (naturalness review; base
  self-hosting r1). v2 anchors it in the source text.
- **Z1.** It exists because D1 removed G-S-001's 「紧张」 item, and the model then wrote the permission's object
  out instead (v1 4/7).

## Alternatives considered

- **Report permission conditions as before (M4's other option)** and **report descriptions (M5's).** Rejected
  by M4 and M5. Both would keep G-S-001 and G-R-012 against their gold.
- **Let the exemption cover destructive permissions (M8's other option).** Rejected by M8.
- **Drop H2 (adversarial review; M9's other option).** Rejected by M9.
- **Leave the zero-object insertion to si6 (M10's other option).** Rejected by M10.
- **Define the guarded operations by pointing to P004 (「（见 CTC-P004）」).** Not adopted. It could import
  P004's trigger into A005 and P003, and what to include (config edits, backups, notifications) is a scope
  question (open proposal 27).
- **Report a term variant in review as A005 (M7's other option).** Rejected by M7.

## Verification

- **Probes.** 25 probes, three runs each, more where a cell wobbled. Full table:
  `dev/inbox/si5/probes/summary.md`. By group:

  | group | base | v1 | v2 |
  | --- | --- | --- | --- |
  | proposal 23 targets (OR-01, OR-02, OR-03) | 0/9 | 9/9 | 9/9 |
  | their boundaries (OR-04, OR-05) | 6/6 | 6/6 | 6/6 |
  | destructive permission (OR-06, OR-06r; M8) | 6/6 | 0/6 | 6/6 |
  | waiver (OR-07), reported at all | 3/3 | 0/3 | 3/3 |
  | symptom section (OR-08) | 2/3 | 3/3 | 3/3 |
  | release step (HR-01, HR-02; M9) | 3/6 | 6/6 | 6/6 |
  | threshold agreement (TH-01, TH-02; M6) | 6/6 | 6/6 | 6/6 |
  | term variants (TV-01, TV-02; M7) | 9/9 | 6/6 | 11/12 |
  | zero object (ZA-01) and its boundary (PR-13) | 5/6 | — | 6/6 |
  | si4 regression probes (P3-01, P3-03, P3-05, PR-07, R4-01, R4-04, R4-07, R4-08) | 24/24 | 24/24 | 24/24 |

  - OR-07 fails the registered 「A005 only」 cell in 2/3 v2 runs and 1/3 base runs, because the rule ID splits
    between A005 and R004 (open proposal 29). Every v2 run reports it.
  - TV-01's v2 miss is one run (r3) that reported no violation.
- **Gold replicates.** Three replicates per version of G-S-001, G-R-012, G-A-002, G-T-101 and G-R-010. G-S-001
  also had four more per version, and G-T-101 six more on base and v2:

  | case | base | v1 | v2 |
  | --- | --- | --- | --- |
  | G-S-001 | 6/7 | 3/7 | 6/7 |
  | G-T-101 | 9/9 | 3/3 | 8/9 |
  | G-A-002 (amended), G-R-010, G-R-012 | 3/3 each | 3/3 each | 3/3 each |

  - G-S-001's failures are all the inserted object: the judge rules 「将索引重建」 an over-edit on a compliant
    source.
  - G-T-101's v2 failure is one co-reference item that named two of the three terms. The six extra
    replicates pass on both versions.
- **Full gold.** v2: 56/56 cases, 0 deterministic errors, no over-edit on any trap, naturalness 4.70. si4's
  full runs scored 53–55 with naturalness 4.62–4.68. G-A-002 now passes under the amended gold, and G-S-001
  and G-R-012 pass in this run.
- **Hard gates.** `tools/compare_skill.py` against the baseline passes them all, frontmatter included
  (`dev/inbox/si5/cand/gate-v2.json`). The body grows from 13 204 to 13 402 characters (+1.5%) and stays at
  232 lines.
- **Format.** `tools/check_skill.py`: 0 errors, 0 warnings. The frontmatter is unchanged from 009.
  `skills-ref validate` was not run in this session, because auto mode blocks `pnpm dlx`. It is to be run with
  `tools/package.sh` at acceptance.
- **Reviews.** Three independent Opus 5.5 reviews of v1 (adversarial, cold reverse-decode, naturalness) and a
  second cold decode of v2. Rulings are in `dev/inbox/si5/review/adjudication.md`. The second decoder's answers
  match the intended behaviour on every probe. Its forks predate si5 or come from the undefined guarded-operation
  class (open proposals 27–31).
- **Self-hosting.** Two runs each on base, v1 and v2.
  - Base reports 道义／规范 and the T001 gap (r1).
  - v1 reports the T001 routing against T001's 「同一概念」 trigger (r2), which V1' answers.
  - v2 r1 reports only the frontmatter P005 finding that every run raises (open proposal 10), and v2 r2 reports
    no violation.

## Limitations

- **One model throughout.** D001's caution applies to the gold verdicts and to the reviews.
- **The gold corpus is still not human-reviewed.** G-A-002's amendment is maintainer-decided, not reviewed
  case by case.
- **The guarded-operation class is undefined.** Three rules now depend on 「破坏性、不可逆或改变外部状态的操作」,
  and only P004's list gives examples. The runs follow the intended reading, but the second decoder shows that
  forks are possible (1(a), 1(d), and the backup step in 2(c)).
- **OR-07's rule ID** still splits, as on base.

## Open proposals after si5

- **Resolved:**
  - 21 (V1');
  - 22 (N1', N2);
  - 23 (D1', with M8's and the waiver's qualifiers);
  - 26 (H1', H2');
  - 8 (S1' gives R005 the position P004 cites; no si5 self-hosting run reports it).
- **Still open from 006–009:**
  - 1 (「必须」 inside 「应」 rows);
  - 2 (R003 「过长」);
  - 7 (category 7 narrower than S001);
  - 9 (T001 tie-break);
  - 10 (frontmatter terminology; the P005 finding in every self-hosting run);
  - 17 (「告警」 names two concepts);
  - 24 (「X 完成后」 as a condition);
  - 25 (「更高优先级」).
- **New:**
  - 27 — 「破坏性、不可逆或改变外部状态的操作」 has no definition; P004's list is examples. It gates §5's
    exemption, A005's check-step bound and P003's own-step bound. Open questions:
    - whether the exemption tests the permitted increment or the whole action;
    - whether a config change counts;
    - whether a backup that a destructive step depends on is covered (second decode).
  - 28 — the text says when an exempt item is not raised, but not that a failed exemption falls back to A005
    or R004. Runtime already does (OR-07 3/3).
  - 29 — 「情况紧急时」 forks between R004 (a timing word, like 「必要时」) and A005 (an undefined state): OR-07
    base A005, R004, A005; v2 A005, A005+R004, R004.
  - 30 — 「指定改写目标」 in §3's authorisation list is undefined and could be read as a catch-all. Also open:
    how 「把要求放宽一些」, which names neither rules nor a target strength, is handled.
  - 31 — a term difference that blocks execution is category 5 (CTC-S002, 必须) in rewrite but CTC-T001 (应)
    in review. §8's escalation lets the review finding reach ERROR when it names the different action.

## Consequences

- **`SKILL.md`** becomes `dev/inbox/si5/cand/v2/SKILL.md`, byte for byte. Section numbers do not change.
  `skills-ref validate` remains to be run with `tools/package.sh`.
- **`eval/gold/gold-ambiguity.yaml`:** G-A-002's actor invariant and expected issue go; its two invalid
  transformations' reasons and its notes are revised (M3).
- **`spec/rules.v0.yaml`:**
  - A005's exceptions gain H1' and D1', and R004 points to them.
  - P003's bound gains state-changing operations.
  - P002 gains Z1.
  - R005 names standalone warning blocks.
  - T001's review clause names T001.
  - S003's tuple says 规范强度.
  - A revisions entry records these, M1–M10 and the G-A-002 amendment.

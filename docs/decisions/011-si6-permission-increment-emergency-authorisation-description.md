# 011 — si6: the permission exemption against the default action, 「紧急时」, unspecific strength authorisations, and the description's exclusions

- **Status:** Accepted by the maintainer on 2026-11-09.
- **Date:** 2026-11-09
- **Relates to:** `000-design.md` §20; `010-si5-permission-description-exemptions-guarded-threshold.md` open
  proposals 10, 27, 28, 29, 30 and 31
- **Evidence:** `eval/reports/si6-summary.md`; `eval/reports/verdicts-si6.claude.yaml`; `dev/inbox/si6/`, which
  holds:
  - the probes, the maintainer's resolutions and the scorer;
  - the candidates with `cand/build.py`;
  - the reviews and the adjudication;
  - the self-hosting cases;
  - `runs/outputs.jsonl`.
- **Candidate:** `dev/inbox/si6/cand/v5/SKILL.md` (sha256 `ed1de342…`)

## Context

si6 is a single-model iteration on decision 010's text (`SKILL.md` at 37b5983, si5 v2). At the start the
maintainer confirmed that every model call stays on Claude Opus 5.5 (M1). It used si3–si5's method:

- every expectation registered before any output;
- three runs per probe per version;
- text changed only where a probe or a self-hosting run failed, or the maintainer decided.

32 probes ended up registered, each before its first output (`dev/inbox/si6/probes/probes.yaml`):

- 23 before the first run, 14 of them copied from si5;
- 2 after the maintainer's decisions on the baseline;
- 7 from the reviewers' counterexamples to v1.

Targets, from 010's open proposals:

- **10 — the description's exclusions.** Self-hosting reported, as CTC-P005, that the frontmatter `description`
  gives the skill's uses but not §1's exclusions, in 5 of 6 si5 runs.
- **27 — the guarded-operation class.** Three rules depend on 「破坏性、不可逆或改变外部状态的操作」, which only
  P004's list illustrates. On the baseline:
  - a permission to split a release (「若待发布的变更较多，也可以分两批发布」, GO-03) forks between not
    reported (1/3) and A005 (2/3, 「许可的操作是发布」);
  - a backup before `DROP TABLE` (GO-01) is already raised as P003 3/3, but si5's second cold decode read the
    literal own-step bound as excluding it.
- **29 — 「情况紧急时」.** OR-07 is A005 3/3 on the baseline, EM-01 A005 6/6; si5's runs split between A005 and
  R004.
- **30 — 「指定改写目标」 and vague authorisations.** 「把要求放宽一些」 (AU-01) lowers every strength in 1 of 3 baseline
  runs; 「把第 2 条放宽一些」 (AU-04, registered later) lowers item 2 to 「应」 in 3 of 3.
- **31 — the rewrite/review asymmetry for a term difference that blocks execution.** A maintainer question.
- **28 — a failed exemption's fallback.** No failing run; regression only.

The maintainer decided nine questions (`dev/inbox/si6/probes/resolutions.yaml`). Four were decided before any
output was read, three after the baseline probe pass and two after the v2 runs:

- **M1:** every model call stays on Opus 5.5.
- **M2:** unfreeze the description and add §1's exclusions, word for word.
- **M3:** 「情况紧急时」 is CTC-R004, by si4 M4's criterion (a word that leaves whether, when or how much to act
  to the reader).
- **M4:** keep CTC-T001 for review-mode term differences, with §8's escalation; close proposal 31 without a text
  change. Rewrite has no severity, so 「必须」 in category 5 is a category label, not a level to align with.
- **M5:** the permission exemption asks what the permitted way of doing it adds beyond the default action.
  GO-03 is not reported; a permitted deletion or config change (OR-06, GO-02) still is.
- **M6:** write backups and snapshots into P003's own-step bound, text only. **Reversed by M9.**
- **M7:** a strength authorisation that names neither the items nor the target strength changes nothing and is
  raised as category 5.
- **M8:** the exemption also requires that the permitted way of doing it does not reduce the checks or reviews
  before such an operation and does not change who performs it. A permission to skip a recommended check
  (GO-06) or to hand the operation to someone else (GO-07) stays reported; an earlier deletion of the same kind
  (GO-08) is exempt.
- **M9:** drop the backup clause (M6's option B). Its premise, "text only, behaviour unchanged", was false: the
  baseline raises GO-01 without it, and with it a backup that is the last step (GO-05) and a backup before a
  traffic switch (gold G-R-007) became false positives.

## Decision

Five exact replacements in `SKILL.md` (`build.py`, `VARIANTS["v5"]`). No rule ID, level, 「待确认」 category,
mode heading or ladder row changes. The frontmatter `description` gains one sentence (M2).

**F1 — the description (proposal 10; M2).** After 「未触发规则的文本原样返回。」:

> 不用于营销文案、品牌叙事、文学写作、SEO 与一般性文字润色。

**R1 — CTC-R004 (proposal 29; M3).** The open class lists 「紧急时」 after 「条件允许时」.

**G1c — §5 「不算真歧义」 (proposal 27; M5, M8).** The permission exemption's third qualifier,
「所许可的也不是破坏性、不可逆或改变外部状态的操作」, becomes:

> 所许可的做法也不引入默认动作之外的破坏性、不可逆或改变外部状态的操作，不减少这类操作之前的检查或复核，也不更换这类操作的执行者

**Z2 — §5, the same paragraph.** The exemption's closing sentence gains a pointer to P002's zero-anaphora
clause (010 Z1):

> 后两种情形即使缺少判据或阈值，也不按 CTC-A005 或 CTC-R004 提出或报告；许可句省略的对象可由前文唯一确定时，按 CTC-P002 保持省略。

**U1' — §3 caller authorisation (proposal 30, in part; M7).** After 「未获授权的同类改动一律不得做。」:

> 调整规范强度的授权没有指明调整哪些条目，或没有指明调整到何种强度时，不据此改动正文，按第 5 类在「待确认」中请调用方指明。

### Gate items (`000-design.md` §20)

| | F1 | R1 | G1c | Z2 | U1' |
| --- | --- | --- | --- | --- | --- |
| failing input | self-hosting: P005 on the description, si5 5/6 | OR-07 A005 3/3, EM-01 A005 6/6 on base, against M3 | GO-03 reported 2/3 on base (M5); GO-08 reported 3/3 on base (M8) | G-S-001 inserts the omitted object 「将索引重建」 in 7 of 23 G1b runs (base 0/7) | AU-01 lowers every strength 1/3, AU-04 lowers item 2 3/3, AU-05 lowers both 必须 3/3 on base |
| risk | the skill activates on polishing requests §1 excludes | the same waiver is an ERROR in one run and a WARNING in the next | a permitted variant of the default action gets an ERROR finding the author did not need | a compliant source is edited (over-edit trap) | a vague request silently weakens 「必须」 |
| existing rules insufficient | §1 lists the exclusions, but the description is what activation reads | R004's list did not name it; the base reads 「情况紧急」 as an undefined state | the qualifier tested the permitted action as a whole: a release is state-changing, so splitting it was not exempt | P002's clause sits in another section; with the new G wording the model writes the object out to make the exemption explicit | §3 named strength authorisation but not what an unspecific one does |
| test that fails before and passes after | self-hosting P005 on the exclusions: see Verification | OR-07 0/3 → 3/3; EM-01 0/6 → 3/3 | GO-03 1/3 → 3/3; GO-08 0/3 → 3/3 | G-S-001 insertion 5/14 (v3) → 0/10 (v5) | AU-01 2/3, AU-04 0/3, AU-05 0/3 → 3/3 each |
| boundary | decoder 5(b): rewriting a release note's upgrade steps stays in scope | EM-02 (an undefined state) stays A005 3/3; EM-03 fails (below) | OR-06, GO-02 (a deletion or config change) A005 3/3; GO-06, GO-07 reported 3/3 | ZA-01, PR-13 3/3 | AU-03 (item and strength named) applies the change |

Every clause beyond the first wording is there because a run or a review failed without it
(`dev/inbox/si6/review/adjudication.md`):

- **G1 → G1a.** 「在默认动作之外增加…操作」 can be read as counting a second release as an added step
  (naturalness review). 「引入」 replaces it.
- **G1a → G1b (M8).** The adversarial reviewer showed that M5's literal test also exempts a permission that
  skips a check or hands the operation to another performer. The baseline reports both. Only GO-07 separates
  the two wordings: v2a exempts it 3/3, v2b reports it 3/3.
- **G1b → G1c.** v3 self-hosting found three antecedents for 「其」 in 「也不更换其执行者」. M8 as answered is
  about the guarded operation, so the antecedent is written out.
- **Z2.** Every G wording raises G-S-001's inserted object: 12 of 49 runs across G variants, against 2 of 24
  without. Dropping the checks clause did not help (v4d 3/10); the pointer did (v5 0/10).
- **U1 → U1'.** 「正文不改」 froze the whole body, so fixes other rules trigger were blocked (AU-05). 「没有指明哪些
  条目、调整到何种强度」 could mean both pieces missing; M7's option required both pieces, so either missing
  triggers it (AU-04).
- **B1, B1' (M6) → dropped (M9).** v1's 「为后续这类操作」 also covered state-changing steps, and G-R-007 failed
  3/3. v2's narrower B1' still produced GO-05 false positives (3 of 6) and a G-R-007 failure (v2a 1/3), each
  citing the backup as a recovery point. The baseline raises GO-01 without it.

## Alternatives considered

- **M5's literal wording without M8's qualifiers (v2a; M8's other option).** Rejected by M8: GO-07 exempt 3/3.
- **Backups in P003 (B1, B1'; M6).** Reversed by M9 on the false positives.
- **G1c without the checks clause (v4d).** Not adopted. It is narrower than M8 as answered, it did not reduce
  G-S-001's insertion (3/10), and GO-06 dropped to 2/3.
- **A boundary sentence keeping 「紧急变更」 out of R004.** Not added. EM-03's boundary was a proposed hypothesis,
  and the added finding is a hedged WARNING the decoder also reads as possible. The maintainer confirmed this at
  acceptance (below).
- **Report review-mode term differences at category 5's 「必须」 (M4's other option).** Rejected by M4.

## Verification

- **Probes.** 32 probes, three runs each, more where a cell differed from base. Full table:
  `dev/inbox/si6/probes/summary.md`. By group:

  | group | base | v3 | v5 |
  | --- | --- | --- | --- |
  | proposal 29 targets (OR-07, EM-01; M3) | 0/9 | 6/6 | 6/6 |
  | its boundary EM-02 (an undefined state stays A005) | 3/3 | 3/3 | 3/3 |
  | EM-03 (no R004 on the category 「紧急变更」) | 6/6 | 2/6 | 1/3 |
  | proposal 27 targets (GO-03 M5, GO-08 M8) | 1/6 | 6/6 | 6/6 |
  | M8's reported cases (GO-06, GO-07) | 6/6 | 6/6 | 6/6 |
  | added operations (OR-06, GO-02) | 6/6 | 6/6 | 6/6 |
  | backups (GO-01, GO-01r, GO-05; M9) | 13/15 | 13/15 | 8/9 |
  | notification gated by a vague check (GO-04) | 3/3 | 3/3 | 3/3 |
  | snapshot before a restart (GO-09) | 1/3 | 1/3 | 3/3 |
  | proposal 30 targets (AU-01, AU-04, AU-05; M7) | 2/9 | 9/9 | 9/9 |
  | specific authorisation (AU-03) | 5/6 | 4/6 | 3/3 |
  | rewrite goal (AU-02, read by hand: no added proposition) | 3/3 | 3/3 | 3/3 |
  | si5 regression probes (OR-01–OR-03, OR-08, HR-01, HR-02, TV-01, ZA-01, PR-13, P3-01, P3-05, PR-07) | 35/36 | 36/36 | 36/36 |

  - EM-03 is the one registered boundary that fails. Base never reports the category; the candidates add a
    hedged R004 WARNING on it in 7 of 15 runs.
  - The GO-01, GO-01r and AU-03 misses occur on base at the same rate (one run each in six).
- **Gold replicates.** Three replicates per version of G-S-001, G-R-012, G-R-007, G-P-004 and G-T-101, with more
  where a version differed. v3 and v5 counts include their full run:

  | case | base | v3 | v5 |
  | --- | --- | --- | --- |
  | G-S-001 | 7/7 | 9/14 | 14/14 |
  | G-T-101 | 9/9 | 10/10 | 16/20 |
  | G-R-007 | 3/3 | 4/4 | 4/4 |
  | G-P-004, G-R-012 | 3/3 each | 4/4 each | 4/4 each |
  | G-P-005 | 2/3 | 2/4 | 1/1 |

  - G-S-001's failures are all the inserted object 「将索引重建」. By string match over every run: a-G1a (G1a
    alone) 2/10, a-noG (F1, R1, U1') 1/10, v2b 2/9, v4d 3/10, v5 0/10.
  - G-T-101's four v5 failures: two runs whose co-reference item names two of the three terms or merges one
    pair (the mode si5 recorded), and two with no co-reference item. Three of the four fell in the first nine
    runs. The base text's record is 17/18 across si5 and si6. The difference is not significant (p ≈ 0.2), and
    no si6 edit is about terminology.
  - G-P-005 (an actor ambiguity reported as 「未发现违规」) misses on base too.
- **Full gold.** v5: 56/56 cases, 0 deterministic errors, no over-edit on any trap, naturalness 4.68. v3 scored
  55/56 (G-P-005), naturalness 4.66; si5 v2 scored 56/56, 4.70.
- **Hard gates.** `tools/compare_skill.py` against the baseline passes them all, with the frontmatter compared
  after M2's replacement (`--fm-replace`; `dev/inbox/si6/cand/gate-v5.json`). The body grows from 13 402 to
  13 542 characters (+1.0%) and stays at 232 lines.
- **Format.** `tools/check_skill.py`: 0 errors, 0 warnings. The frontmatter is valid YAML; `name` is unchanged
  and `description` changes only by F1. `skills-ref validate` was not run: auto mode blocks `pnpm dlx` (again at
  acceptance). It is to be run with `tools/package.sh`.
- **Reviews.** Three independent Opus 5.5 reviews of v1 (adversarial, cold reverse-decode, naturalness) and a
  second cold decode of v3 by a fresh reader. Rulings are in `dev/inbox/si6/review/adjudication.md`.
  - The second decoder reads M8's cases as intended: 1(c) skip a check and 1(f) change the performer reported,
    1(a) and 1(d) exempt.
  - Its forks come from the open proposals (27's snapshot and export, 28, 30's rewrite goal) or are new (5(a)).
- **Self-hosting.** Two runs each on base, v1, v3 and v5.
  - The description P005 on the exclusions: si5 5/6 → si6 base 0/2, v1 0/2, v3 0/2, v5 0/2. M2 was decided on
    si5's count; the finding was already rare on the si5 v2 text.
  - v3 r1 found 「其」 with three antecedents (G1c).
  - v5 r1 reports only findings that predate si6 (the mode and threshold for a document spanning both scopes;
    「阶梯」). v5 r2 reports no violation.

## Limitations

- **One model throughout.** D001's caution applies to the gold verdicts and to the reviews.
- **The gold corpus is still not human-reviewed.**
- **Activation is not tested.** The harness loads the whole skill, so F1 is measured only by self-hosting and
  the cold decode.
- **Rates on single gold cases are noisy.** Z2's effect on G-S-001 rests on 0/10 (14/14 judged) against 7/23
  under G1b; the base text's own rate is 1 in 14 across si5 and si6. G-T-101 on v5 (16/20) is below the base
  text's 17/18 without a significant difference.
- **M8's resolutions were fixed after the v2 outputs.** GO-06, GO-07 and GO-08 were registered as measure-only;
  v3 and v5 are their first confirmation runs.

## Maintainer rulings at acceptance

The orchestrator made these calls without a maintainer question. The maintainer accepted v5 on 2026-11-09
(「接受并提交」), which confirms them:

- **G1c and Z2 are in the candidate.** G1c writes out the antecedent of M8's wording; Z2 adds a pointer to an
  existing rule and no requirement. Both answer a failed run (self-hosting v3 r1; G-S-001).
- **EM-03 is left as a registered failure (proposal 32).** The alternative is a sentence keeping category names
  such as 「紧急变更」 out of R004, which would need its own probes and a further iteration.
- **G-T-101 on v5 (16/20) is recorded as a limitation, not fixed.** No si6 edit concerns terminology, and the
  difference from the base text is not significant.

## Open proposals after si6

- **Resolved:**
  - 29 (R1);
  - 31 (closed by M4 without a text change);
  - 10, in part (F1 adds the exclusions);
  - 30, in part (U1' handles an unspecific strength authorisation);
  - 27, in part (G1c settles what the permission exemption tests: M5, M8).
- **Still open from 006–010:**
  - 1 (「必须」 inside 「应」 rows);
  - 2 (R003 「过长」);
  - 7 (category 7 narrower than S001; v3 self-hosting r1);
  - 9 (T001 tie-break; v3 self-hosting r2 reports 「最明确」);
  - 17 (「告警」 names two concepts; v3 self-hosting r2);
  - 24 (「X 完成后」 as a condition);
  - 25 (「更高优先级」);
  - 28 (a failed exemption's fallback; decoder 1(g));
  - 27, the rest: whether a backup, snapshot or export is 「改变外部状态」 (decoder 2(a), 2(b), 2(d); base reads
    a snapshot before a restart as one in 2 of 3 runs, GO-09);
  - 30, the rest: which prohibition a rewrite goal lifts (decoder 4(e));
  - 10, the rest: the description's covered list is narrower than §3 (v3 self-hosting r2).
- **New:**
  - 32 — R004 reaches a category name that contains a listed word. 「紧急变更须在 24 小时内补录…」 draws an R004
    WARNING on the category in 7 of 15 candidate runs; base never reports it (EM-03). The decoder answers
    「no finding」 with R004 as the other reading.
  - 33 — F1's exclusions meet the covered list: 「润色这份发布说明，让它更有吸引力」 names a covered document type
    and an excluded task, and the text does not say which wins (decoder 5(a)).
  - 34 — the mode and review threshold for a document that spans both scopes or neither. §1's 「跨界时取 strict」
    governs mode inference for non-review tasks; review's threshold sentence has no such clause (v3 and v5
    self-hosting r1; raised before in si2 self-hosting and si3's reviews).
  - 35 — 「阶梯」 names §2's priority layers once, without definition (v5 self-hosting r1; related to 25).

## Consequences

- **`SKILL.md`** becomes `dev/inbox/si6/cand/v5/SKILL.md`, byte for byte. Section numbers do not change.
  `skills-ref validate` remains to be run with `tools/package.sh`.
- **`spec/rules.v0.yaml`:**
  - A005's exceptions take G1c and Z2.
  - R004's class and detection list add 紧急时.
  - S003's exceptions take U1'.
  - A revisions entry records these, F1, M1–M9 and what was not applied.
- **Decision 010's M8** is narrowed: a permission that changes only how the default action is done is now
  exempt, unless it reduces a check or review before a guarded operation or changes its performer.

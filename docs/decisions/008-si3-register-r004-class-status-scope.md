# 008 — si3: 状态提示 in strict, CTC-R004 as an open class, and 口语腔 in CTC-R003

- **Status:** Accepted by the maintainer on 2026-10-15, with the RG-15 ruling below.
- **Date:** 2026-10-15
- **Relates to:** `000-design.md` §14, §15, §20, §22, §26, §30; `004-rule-set-adjudications.md` §8;
  `006-si1-merged-iteration.md` open proposals 3 and 5; `007-si2-review-routing-and-p002-boundary.md` open
  proposals 3, 5, 16 and the withdrawn E3
- **Evidence:** `eval/reports/si3-summary.md`; `eval/reports/verdicts-si3.claude.yaml`; `dev/inbox/si3/`, which
  holds the probes and resolutions, the candidates with `cand/build.py`, the reviews and adjudication, the
  self-hosting cases and `runs/outputs.jsonl`
- **Candidate:** `dev/inbox/si3/cand/v6/SKILL.md`

## Context

Decision 007 named three open proposals with the strongest evidence: 状态提示 has no mode (3), CTC-R004's word
list may be closed or open (5), and register cleanup has no licensing rule (16). si3 is a single-model
iteration: at the start the maintainer confirmed that every model call stays on Claude Opus 5.5.

si3 used si2's method. Every expectation was registered before any output was seen. Each probe ran three times
per version. Text changed only where a probe failed or the maintainer decided. 29 probes ended up registered:
17 before the first run, and 12 more from the candidate runs and the three independent reviews, each before
its first output (`dev/inbox/si3/probes/probes.yaml`).

On the baseline:

- **3 — no behavioural fork.** Opus infers strict for a status message 3/3 in both rewrite and review. The gap
  is textual: every self-hosting run on the baseline reports it, two in si3 and three in si2.
- **5 — no fork on the list.** 「尽快」 and 「视情况」 are already R004 3/3. The residual is PR-07: 「流量正常」 drew
  an R004 finding beside the A005 one in 1/3 runs.
- **16 — the gap reproduces.** 「糟糕！」 stays in an error message 3/3, and 「啦」 in a status message 3/3. Three
  tool-description frames survive: 「你可以用这个工具…」 0/3, 「允许您」 1/3, 「开发者可以」 0/3. Pooling si2's gold
  run with si3's three replicates: G-R-009 2/4, G-R-010 2/4, G-R-011 0/4.

The maintainer decided three product questions after the baseline pass (`dev/inbox/si3/probes/resolutions.yaml`):

- **Q1:** 状态提示 is strict.
- **Q2:** register cleanup applies in every in-scope genre, and the caller's tone convention wins.
- **Q3:** R004 is an open class of degree, timing and discretion words; an undefined state or a missing value
  is CTC-A005.

## Decision

Nine exact replacements in `SKILL.md` (`build.py`, `VARIANTS["v6"]`). No rule ID, level, 「待确认」 category,
mode heading or ladder row changes. One rule row gains a defect class, which 000-design §20 counts as an
extension of an existing 应 rule, as in 004 §8.

**S1 — 状态提示 in the strict scope (Q1).** The strict scope's last item becomes 「告警、错误信息与状态提示」. §1
stops naming 状态提示 separately, because it already covers everything the scope lists name.

**S2 — CTC-R004 as an open class (Q3), with its boundary routed to CTC-A005.**

> …由无判据词承担时——「尽量」「尽可能」「尽快」「最好」「适当」「必要时」「视情况」「合理」等表示程度、时机或裁量的词——…。未定义的状态（「服务稳定」）与未给出具体值的次数或时长（「多次」「若干分钟」）不是这类词，按 CTC-A005 处理。

**S4 — §8 step 2** adds the exclusion to the rows that route to CTC-A005: 「…、CTC-R004 排除的未定义状态与次数、时长」.

**S3 — CTC-R003 「反译文腔与口语腔」 (Q2).**

> 文本含译文腔或口语腔时，在语义完全不变的前提下改用中文技术写作的常规表达。译文腔：无必要的被动、名词化赘语（进行／作出／予以 + 动词）、过长的「的」字串、英语从句语序残留（「由于…的事实」）、直译连接词。口语腔：客套话（「麻烦您」）、语气词（「啊」「嘛」）、情绪化感叹（「哎呀！」）、口语填充（「一下」）、把读者当作谈话对象的引导（「这个工具可以帮你」）。去除这些缺陷时，工具描述改为直接陈述功能（「获取…」「用于…」），不以使用者作句子主语（「调用者可以…」）。被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述。去口语腔时禁止的强度不变：「千万不要」「可别」这类口语禁止保留原词或改作「切勿」，不改作「不得」「禁止」。本规则永远低于 S 族。

The ladder's layer 4 reads 「无译文腔、无口语腔」. §7 step 6 removes 口语腔, and step 7 checks for it (S5).

### Gate items (`000-design.md` §20)

| | S1 | S2 + S4 | S3 |
| --- | --- | --- | --- |
| failing input | self-hosting finding on §1, every run on the baseline | PR-07 (「流量正常」 cited both A005 and R004); §3 「尽快回滚」 outside the list | G-R-011, PR-19, RG-07 (particles kept); G-R-010, RG-03, RG-08, RG-10 (conversational frames kept) |
| risk | the mode, and so the ambiguity threshold, of a whole document type is undefined | the same gap gets a different rule ID and severity per run | register noise stays in error, status, tool and agent text; G-R-011 fails 0/4 |
| existing rules insufficient | no scope list names it | the list did not say whether it was closed; the example contradicted a closed reading | R003 lists translationese only, and R001 returns unlisted text unchanged; si2 showed a genre-scoped clause trades G-R-011 for G-R-010 |
| test that fails before and passes after | self-hosting: 2/2 → 0/2 (v3, v4, v6) | PR-07 2/3 → 3/3; self-hosting R004 finding 0/2 | the probes and gold replicates in §Verification |
| boundary | ST-02: a status message with no reportable gap stays 「未发现违规」 | R4-03 (a descriptive 「尽快」 is not R004); ST-02 and PR-19 (「预计还需几分钟」「请稍后重试」 are not raised) | PR-16, PR-17, PR-18, RG-01, RG-02, RG-04, RG-05, RG-09, RG-11, RG-12, RG-14, RG-16, RG-17, RG-19 stay unchanged or keep the protected element |

Every S3 clause beyond the defect class is there because a probe failed without it:

- **The tool-description sentence.** G-R-010's direct form was 1/9 across v1, v1-class and v2, against 7/11
  on the baseline. That is si2's E3 effect: a listed defect class makes the repair surgical, so the
  permission frame 「该工具允许调用者获取」 survives.
- **The strength sentence.**
  - With no boundary (v1-class), RG-06 raised 「千万不要」 to 「不得」 3/3.
  - With 「千万」 named (v4), RG-13 raised 「可别」 3/3.
  - With the boundary stated by function (v5), RG-13 was still raised 2/3 and RG-18 3/3.
  - Naming the repair (v6) gives 9/9, including RG-18 (「绝对别」), which the sentence does not quote and the
    baseline raises 3/3.
- **Clauses dropped because their probes passed without them:** v1's 推测「吧」, 警示「危险！」, quoted replies
  and the caller's tone (PR-16, PR-17, PR-18, RG-05 3/3 on v1-class), and the adversarial reviewer's narrowing
  of reader guidance to tool descriptions (RG-16, RG-17 3/3 on v4).

## Alternatives considered

- **si2's E3: a clause for alert, error and status text only.** Rejected in 007, and not retried. si3 stated
  the class for every genre from the first draft.
- **v1's five-clause boundary sentence.** Rejected on the ablation: only the strength clause changed behaviour.
- **A translationese example for the permissive frame (v2, 「使用户能够…」).** No effect on G-R-010; reverted.
- **Narrow 「把读者当作谈话对象的引导」 to tool descriptions** (adversarial revision 1). Rejected after RG-16 and
  RG-17 passed 3/3 without it.
- **A strength boundary by function only (v5).** Not enough: RG-13 2/3 and RG-18 3/3 raised.
- **A closed R004 list, with the §3 example changed to a listed word.** Rejected by Q3.

## Verification

- **Probes on v6.** 29 of 29 pass 3/3, counting RG-15 under the maintainer's ruling (28 against the
  registrations as written). By group:
  - register targets: base 1/15, v6 15/15;
  - strength: base 5/9, v6 9/9;
  - R004: base 11/12, v6 12/12;
  - boundaries: 42/42 on both versions;
  - 状态提示: strict 3/3 on both versions.

  RG-15: rewritten 3/3, which the maintainer ruled correct (see Maintainer rulings).
- **Gold replicates.** One gold run plus three replicates per case:

  | case | base | v6 |
  | --- | --- | --- |
  | G-R-009 | 2/4 | 4/4 |
  | G-R-010 | 2/4 | 4/4 (direct form 4/4; base 7/11 across si2 and si3) |
  | G-R-011 | 0/4 | 4/4 |
  | G-S-001 | 3/4 | 4/4 |
  | G-L-006 | 4/4 | 4/4 |
- **Full gold on v6.** 56/56 cases, 0 deterministic errors, 53/56 judged pass, naturalness 4.61, no
  over-edit on any trap.
  - G-A-002 and G-T-101 fail in every run since r1.
  - G-R-003 failed in this run (two consecutive 「被」). It passes 3/3 in replicates on both v6 and the
    baseline, so it is treated as single-run noise.
  - For comparison, v3 and v4 scored 54/56; the baseline scored 52/56 in si2.
- **Hard gates.** `tools/compare_skill.py` against the baseline passes them all. Body 12 692 → 13 010
  characters (+2.5%), 232 lines.
- **Format.** `skills-ref validate` on a packaged copy: valid.
- **Reviews.**
  - Three independent Opus 5.5 reviews of v3: adversarial, cold reverse-decode and naturalness.
  - A second cold decode of v6.
  - Rulings: `dev/inbox/si3/review/adjudication.md`.
- **Self-hosting.** Two runs each on base, v3, v4 and v6. The 状态提示 finding (base 2/2) and the R004-list
  finding are gone. v3 raised one finding in si3 text, which v4 fixed. v4 and v6 raise none in si3 text.

## Limitations

- **One model throughout.** D001's caution applies to the gold verdicts. The G-R-010 verdicts in particular
  were lenient on the permission frame, so its surface form is reported beside the judge.
- **The strength ordering is not human-reviewed.** The ordering in the S3 sentence (「千万不要」「可别」 below
  「不得」「禁止」) takes G-R-009's gold as given, and that gold is orchestrator-reviewed.
- **The gold corpus is still not human-reviewed.**
- **The frontmatter is unchanged.** It is frozen by the hard gate, so it still names neither 状态提示 nor
  register cleanup.

## Maintainer rulings and open items

1. **RG-15 — ruled: the registration was wrong.** 「通过这个函数，开发者可以把图片压缩到指定尺寸，最大支持 4096 像素。」 has no particle, and v4–v6
   rewrite it 3/3 to 「该函数用于…」.
   - The probe was registered to expect the text unchanged.
   - The model reads 「开发者可以」 as reader-directed guidance, which is a listed defect.
   - G-R-010's gold requires the same repair of the same frame.

   The second cold decode (`decode-v6.yaml`, probe 2(b)) reads the text the way the registration does:
   unchanged. So text and runtime behaviour split here. Either the text says that a third-person user frame
   counts as reader-directed guidance, which matches G-R-010's gold and the observed behaviour, or the behaviour
   is narrowed, which brought G-R-010 back in every si3 attempt.

   **Ruling (maintainer, 2026-10-15):** treat RG-15's registration as wrong; the rewrite matches G-R-010's
   gold. The behaviour stands and `SKILL.md` is not changed for it. The text–behaviour split the decoder found
   remains, and is open proposal 20.
2. **Probes not run in si3.** These are candidate probes for the next round:
   - a degree word on a state (「负载过高时」), which may draw both R004 and A005;
   - 「条件允许时」, which goes to A005 and so loses §5's strength question;
   - the suggestion 「吧」;
   - colloquial words outside the five types (「搞定」).

## Open proposals after si3

- **Resolved:** 3 (S1), 5 (S2 + S4) and 16 (S3).
- **Still open from 006 and 007:**
  - 1: 「必须」 inside 「应」 rows;
  - 2: R003's 「过长」, reported in every self-hosting run;
  - 7: category 7 narrower than S001;
  - 8: P004/R005 attribution;
  - 9: T001 tie-break;
  - 10: frontmatter terminology;
  - 15: the A005/P003 overlap.
- **New:**
  - 17 — 「告警」 names two concepts, the alert message (strict scope, T002) and the warning block (P004,
    S002). Reported by v4 self-hosting.
  - 18 — the 「记录级别」 one-word T001 fix that 007 deferred, reported again in every si3 self-hosting run.
  - 19 — the open probes in item 2 above.
  - 20 — say in CTC-R003 that a third-person user frame (「开发者可以…」「调用者可以…」) counts as reader-directed
    guidance, so that a cold reader predicts the rewrite the maintainer ruled correct for RG-15.

## Consequences

- **`SKILL.md`** is `dev/inbox/si3/cand/v6/SKILL.md`, byte for byte. `tools/package.sh` passes (`check_skill.py` 0/0,
  `skills-ref validate` valid). Section numbers do not change.
- **`spec/rules.v0.yaml`.** CTC-R003 gains the 口语腔 class, the tool-description repair form and the strength
  boundary. CTC-R004 gains the open class and its A005 exclusion. The strict mode scope gains 状态提示. A
  revisions entry records S1–S5, their probes and the RG-15 ruling.
- **G-R-010, G-R-009 and G-R-011** pass on the rule rather than on a stretched R003. Their gold expectations are
  unchanged.

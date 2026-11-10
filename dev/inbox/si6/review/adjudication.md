# si6 — rulings on the three independent reviews of candidate v1

Reviews: `adversarial.yaml` (semantic invariants, counterexamples), `decode.yaml` (cold reverse-decoding,
candidate only), `naturalness.yaml` (wording and over-control). All three are Opus 5.5 subagents with
disjoint inputs; none saw another's output, and the adversarial reviewer saw no candidate output. The
orchestrator (Opus 5.5) made the rulings. The human gate is the maintainer's review of decision 011.

As in si3–si5, each counterexample the existing probes did not cover became a probe registered before any
output (`probes.yaml`, section 「added 2026-11-09 after the reviews of v1」: GO-06, GO-07, GO-08, GO-09, EM-03,
AU-04, AU-05). Text changes where a probe fails or a reviewer shows a reading defect that a narrower wording
removes without new requirements; scope changes go to the maintainer.

## F1 — description exclusions (M2)

| finding | source | ruling |
| --- | --- | --- |
| Copies §1's list word for word; a clarification | adversarial accept; naturalness 4 | **accepted** |
| The P005 finding it answers appeared in 1 of 4 self-hosting runs on this exact text (si5 v2 1/2, si6 base 0/2), against 5/6 across si5's versions | adversarial | **recorded**. M2 was decided on si5's count; v1 raises no P005 (0/2) |
| A request to polish an error message may match 「一般性文字润色」 and not activate the skill; 「一般性」 can mean "non-technical" or "no specific defect" | adversarial; naturalness; decoder 5-1 | **recorded as open**: the harness loads the whole skill and cannot test activation. The phrase is §1's own and predates si6 |

## R1 — 「紧急时」 in CTC-R004 (M3)

| finding | source | ruling |
| --- | --- | --- |
| Follows the si4 「条件允许时」 precedent | adversarial accept; naturalness 5 | **accepted** |
| Base cites 「情况紧急」 as an undefined state (R004's exclusion) in every run, and 「紧急时」 is not a literal match, so R1 may change nothing | adversarial | **answered by the runs**: OR-07 0/3 → 6/6 R004, EM-01 0/6 → 5/6 R004 on v1. The one EM-01 miss (r1) reported no violation |
| G-P-004's heading 「紧急回滚」 may be read as a 「紧急时」 condition | adversarial; decoder 3(c) | **checked**: G-P-004 passes 3/3 on v1 |
| 「紧急变更」 (a change category) may be pulled into R004 | decoder 3(b); naturalness (「时」 keeps it off nouns) | **registered** EM-03 |

## G1 — the permission exemption against the default action (M5)

| finding | source | ruling |
| --- | --- | --- |
| 「增加」 can be read as counting an extra step (two releases instead of one), so GO-03 could still be reported; 「做法…增加…操作」 is an awkward pairing | naturalness; adversarial | **accepted** (v2): 「所许可的做法也不引入默认动作之外的…操作」 |
| The exempt set now also takes permissions that skip a recommended check (「建议先在预发验证…也可以直接在生产执行」), defer a review, or change who performs the operation; base reports these | adversarial strongest counterexample; decoder 1(c) | **for the maintainer (M8)**. M5 was asked with GO-03 only. Registered GO-06 (skip a recommended check) and GO-07 (change the performer of a recommended action). v2b carries the adversarial reviewer's narrower wording, v2a M5's literal one |
| Moving a destructive default action earlier (「也可以提前到周五清理」) is exempt by the letter | decoder 1(d) | **registered** GO-08, measured with M8 |
| G1 narrows decision 010's M8 (「所许可的也不是…操作」) | adversarial | **recorded**: decision 011 states it |
| 「外部状态」 is still undefined (config changes) | decoder 1(b) | **consistent with the runs**: GO-02 (retention change) A005 3/3 on base and v1; open proposal 27 stays partly open |

## B1 — backups and snapshots in CTC-P003 (M6)

| finding | source | ruling |
| --- | --- | --- |
| 「为后续这类操作」 covers state-changing steps (restart, traffic switch), wider than M6's 「为后续破坏性操作」 | adversarial revise | **accepted** (v2): 「为后续破坏性或不可逆操作」. The runs confirm it: G-R-007 (a backup before a traffic switch, gold expects no finding) fails 3/3 on v1, passes 3/3 on base |
| A rolling 「快照→重启」 runbook would get a chain of items | adversarial | **registered** GO-09 |
| A minority reading binds 「且后续步骤…」 to the parenthesis; 「它」 gains antecedents | naturalness | **accepted** (v2): 「且后续步骤的安全性取决于该步是否成功」, equivalent |
| 「备份、快照」 may read as a closed list (an export used as a restore point) | naturalness; decoder 2(d) | **recorded**: decoder 2(d) still raises the export |
| How 「后续步骤的安全性取决于它」 is judged (position or object) | decoder 2(a), 2(e) | **recorded**: predates si6 |

## U1 — an unspecific strength authorisation (M7)

| finding | source | ruling |
| --- | --- | --- |
| 「正文不改」 freezes the whole body, blocking fixes other rules trigger | adversarial revise; naturalness; decoder 4(a) | **accepted** (v2): 「不据此改动正文」. Registered AU-05 |
| 「没有指明哪些条目、调整到何种强度」 can mean both missing or either missing; 「把第 2 条放宽一些」 falls through under the first | naturalness; adversarial (recorded as widening) | **accepted** (v2): 「没有指明调整哪些条目，或没有指明调整到何种强度时」. M7's recommended option said 「授权须指明对象和目标强度」, so either missing triggers it; this is M7 as approved, not a widening. Registered AU-04 |
| Specific authorisations still apply (「把第 3 条的『应』改为『必须』」, 「把所有『必须』改为『应』」) | adversarial; decoder 4(b), 4(c) | **checked**: AU-03 3/3 on v1 |
| 「指定改写目标」 still does not say which prohibition a goal lifts | decoder 4(e) | **recorded as open (30, in part)**: AU-02 adds no proposition on base or v1 |

## v2a and v2b — runs and the maintainer's M8 and M9

v2a = F1, R1, G1a, B1', U1'; v2b = F1, R1, G1b, B1', U1'. Three replicates each on the probes the v1 rulings
touched, and the gold reps G-S-001, G-R-007, G-P-004 (`si6-g2-VAR-r{1,2,3}`). Scores from `probes/score.py`
after the 「**1. CTC-A005 ｜ ERROR**」 header fix (it changed one cell: GO-06 v2b r1, 2/3 → 3/3).

| probe | base | v2a | v2b | reading |
| --- | --- | --- | --- | --- |
| OR-07, EM-01 (「紧急时」 → R004) | 0/3, 0/6 | 3/3, 3/3 | 3/3, 3/3 | R1 works |
| EM-03 (「紧急变更」, fail if R004) | 3/3 | 2/3 | 2/3 | one R004 per variant; recorded, see below |
| GO-03 (split release, not reported) | 1/3 | 3/3 | 3/3 | G1 works |
| OR-06, GO-02 (an added deletion or config change) | 3/3, 3/3 | 3/3, 3/3 | 3/3, 3/3 | still A005 |
| GO-06 (skip a recommended check) | R004 3/3 | R004 3/3 | R004 3/3 | reported in all |
| GO-07 (change the performer) | A005 3/3 | not reported 3/3 | R004 3/3 | **the only split** |
| GO-08 (an earlier deletion of the same kind) | A005 3/3 | not reported 3/3 | not reported 3/3 | exempt under both |
| AU-01, AU-04, AU-05 (unspecific authorisation) | 2/3, 0/3, 0/3 | 3/3 each | 3/3 each | U1' works |
| AU-03 (item and strength named) | 3/3 | 3/3 | 2/3 | v2b r1 adds a 「待确认」 item on the verification criterion; the edit itself is right |
| GO-01 (backup before DROP, P003) | 3/3 | 3/3 | 3/3 | base needs no B1 |
| GO-05 (backup as the last step, not reported) | 3/3 | 2/3 | 1/3 | **B1' false positives** |
| GO-09 (snapshot before restart, not reported) | 1/3 | 0/3 | 1/3 | fails on base as well |
| gold G-R-007 (backup before a traffic switch) | 3/3 pass | 2/3 | 3/3 | B1' failure in v2a |

| item | ruling |
| --- | --- |
| G1a vs G1b | **M8 → G1b.** The maintainer took the recommended option: a permission that skips a check or review before such an operation, or hands it to another performer, lowers a safeguard and is not exempt. GO-06 and GO-07 reported, GO-08 exempt (`resolutions.yaml`, `resolutions_after_v2`; fixed after the v2 outputs, so v3 is the confirmation run) |
| B1' | **M9 → dropped.** M6's premise (text only, behaviour unchanged) is false: base raises GO-01's backup 3/3 without B1, and B1' adds GO-05 false positives (3 of 6 v2 runs) and a G-R-007 failure (v2a 1/3), each citing the backup as a recovery point. M6 becomes option B. The second cold decode of si5 v2, which read the literal bound as excluding backups, is recorded as an open observation |
| U1' | **kept.** AU-03 v2b r1's extra item raises the verification step's missing criterion (CTC-A005's class), not a strength; it is watched in v3, not fixed |
| R1 and EM-03 | **kept, EM-03 recorded.** Base reports 「紧急变更须在 24 小时内补录…」 as A005 or not at all; one run in each variant moves it to R004. Both report it; only the rule ID and default severity differ. 「时」 in 「紧急时」 is the textual boundary; no further text |
| GO-09 | **recorded, expectation not met on base.** Base reads creating a snapshot before a restart as a state-changing step and raises its criterion in 2 of 3 runs. The expectation rested on M6's wording; with B1 dropped it measures base behaviour, which predates si6 (open proposal 27, in part) |

v3 = F1, R1, G1b, U1' (`cand/build.py`), the release candidate.

## v3 — runs, self-hosting, the second cold decode, and v5

v3 = F1, R1, G1b, U1'. Full probes ×3, the five gold reps ×3, two self-hosting runs and one full gold run. Cells
that differed from base got three more replicates on base and v3 (r4–r6). A second cold decode
(`decode-v3.yaml`, prompt `dev/prompts/si6-decode-v3.md`, a fresh Opus 5.5 reader) read v3 only.

| item | result | ruling |
| --- | --- | --- |
| registered targets (OR-07, EM-01, GO-03, GO-06, GO-07, GO-08, AU-01, AU-04, AU-05) and regressions (OR-01–OR-08, HR, TV, ZA, PR, P3, GO-02, GO-04, GO-05) | all 3/3 (EM-01 after a parser fix for 「**ERROR｜CTC-R004…**」) | — |
| GO-01, GO-01r | 5/6 each on v3 and on base (one 「未发现违规」 each) | run variance; P003 is unchanged from base |
| AU-03 | v3 4/6, base 5/6; the extra 「待确认」 item asks for the pre-release check's criterion (CTC-A005's class) | run variance; base does it too |
| EM-03 | v3 R004 on 「紧急变更」 4/6; base 0/6 (base's A005 cells are on the 24-hour start point, never on the category) | **registered failure, recorded.** The boundary was `proposed` (naturalness review: 「时」 keeps it off nouns) and is falsified. The added WARNING says the category has no criterion and is hedged (「如果其他章节已定义…」). The cold decoder answers 「no finding」 with R004 as the other reading. Goes to the maintainer at acceptance; no text |
| GO-09 | v3 1/3, base 1/3 | as base (above) |
| gold, full run | 55/56; G-P-005 misses the actor ambiguity (「未发现违规」) | **run variance**: three replicates, base 1/3 fail, v3 1/3 fail |
| gold G-S-001, inserted object 「将索引重建推迟」 | v3 5/14, v2b 2/9, v4d 3/10, a-G1a 2/10; base 0/7, a-noG 1/10 | **regression, fixed in v5** (below) |
| self-hosting r1: 「也不更换其执行者」, 「其」 has three antecedents (CTC-A002) | new, on si6 text | **accepted** as G1c: 「也不更换这类操作的执行者」, M8 as answered (「hands it to another performer」, it = such an operation). The decoder reads 1(f) the intended way |
| self-hosting r2: the description's covered list is narrower than §3 (P005) | new angle on proposal 10 | **recorded as open**; M2 approved only the exclusions |
| self-hosting, others: category 7 narrower than S001 (7), T001 「最明确」 (9), 「告警」 two concepts (17), the review threshold for a document spanning both scopes (si2 self-hosting, si3 reviews) | predate si6 | recorded |
| decoder 5(a): 「润色这份发布说明」 — 发布说明 is in the covered list, 润色 in the exclusions; which wins is unsaid | new fork from F1 | **recorded as open** (activation is not testable in the harness) |
| decoder 1(g): a permission that reduces review is not exempt, but the text never says a non-exempt item must then be reported | proposal 28 | recorded |
| decoder 2(a), 2(b), 2(d): whether a snapshot, backup or export is 「改变外部状态」 | M9's recorded fork | recorded |

**G-S-001.** A permission sentence with an omitted object (「若延迟预算紧张，也可以推迟到下一维护窗口」) is the case
si5's Z1 fixed. Every G wording raises the insertion rate, the longer G1b the most (7/23; all G wordings 12/49
against 2/24 without). Dropping the checks clause (v4d) did not help. Z2 points the exemption at CTC-P002's
zero-anaphora clause and adds no requirement:

> 后两种情形即使缺少判据或阈值，也不按 CTC-A005 或 CTC-R004 提出或报告；许可句省略的对象可由前文唯一确定时，按 CTC-P002 保持省略。

v5 = F1, R1, G1c, U1', Z2: G-S-001 inserts 0/10; ZA-01, PR-13, OR-01, GO-03, GO-07 3/3. v5 is the release
candidate and gets the full verification set.

## v5 — verification

Full probes ×3, the five gold reps ×3, two self-hosting runs and one full gold run, plus G-S-001 ×10 and G-T-101
×16 more.

- Probes: every registered expectation holds except EM-03 (1/3; open proposal 32) and one GO-01r miss (2/3; base
  5/6). GO-09 passes 3/3.
- Gold: full run 56/56, naturalness 4.68, no over-edit. G-S-001 14/14; G-T-101 16/20 (base text 17/18, v3 10/10;
  p ≈ 0.2, recorded as a limitation); G-R-007, G-P-004, G-R-012 4/4.
- Self-hosting: r1 reports only findings that predate si6 (proposal 34, 「阶梯」 as 35); r2 no violation.

v5 is the candidate handed to the maintainer as decision 011. The maintainer accepted it on 2026-11-09.

# 006 — Adopt a merge of the two si1 self-iteration candidates as `SKILL.md`

- **Status:** Accepted. The gold-case regression has not been re-run against this version (see Consequences).
- **Date:** 2026-10-05
- **Relates to:** `000-design.md` §15, §20, §22, §30; `005-reverse-decoding-findings.md`
- **Evidence:** `eval/reports/si1-summary.md`; `dev/inbox/si/` (candidates, logs, judge outputs, adjudication and its review); `dev/inbox/si/merge/` (this candidate, its gates and its two independent reviews)

## Context

The si1 experiment let two models iterate on `SKILL.md` alone for three rounds each, under a frozen-semantics constraint and a −25% length reference. Four blind judge runs then assessed both finals, and a label-blind reviewer checked every ruling.

- **Opus 5.5 (candidate B, `track-1/r3`)**: 308 lines, −13.6% body characters. No confirmed ERROR-level loss and no new normative content. It lost one procedural check: the pre-return checks for CTC-R001, R002/R003 and the output contract had no counterpart.
- **Fable 5.1 (candidate A, `track-2/r3`)**: 232 lines, −26.3%. No confirmed ERROR-level loss either; 127 judge claims about the deletions were adjudicated and none removed an independent assertion. It also made three semantic changes that the frozen-semantics constraint forbade, and one of them created a new two-readings fork.

Neither candidate alone was the right adoption. A had the better structure and compression; B had none of A's semantic additions and had better wording at several points the cold readers kept flagging.

## Decision

`SKILL.md` is candidate A with fourteen merge edits (M1–M14), followed by five fixes (F-a–F-e) made after two independent reviews of the merge. Each merge edit either takes B's text where the adjudication went against A, or reverts one of A's unauthorised additions. Each fix either restores text from the previous `SKILL.md` or aligns a paraphrase to its frozen row. All nineteen are exact string replacements in `dev/inbox/si/merge/build.py`, which rebuilds both the reviewed candidate and the final file from A byte-for-byte.

| # | Edit | Source | Why |
| --- | --- | --- | --- |
| M1 | Preamble reduced to 「语义先于风格。」 | B | The unqualified 「歧义只报告」 conflicted with evidenced disambiguation (A002/A003); the content stays in the rule rows and the frontmatter. |
| M2 | Unspecified mode: review tasks use review; others infer from the scopes; cross-type documents use strict | B | 「更严的一档」 was undefined across three modes. |
| M3 | 「三种模式下全部规则按其级别生效」 | B | Standard mode never said whether the R family applies. |
| M4 | Review threshold defined by membership of the strict or standard scope lists | B | Replaces two document labels that did not match the scope lists. |
| M5 | 「strict／standard」 in the output-contract table | CTC-R006 | Matches the slash used elsewhere in the document. |
| M6 | Drop 「缺失信息的规则 ID 与其所属类别括注的规则一致」 | revert A (D-A4) | New normative rule with no basis in the baseline or the rows. |
| M7 | Category 5 reads 「第 2–4 类之外…」 | B | Same scoping as A, shorter. |
| M8 | The 「尽快回滚」 example line, naming the missing time limit | B | Matches M10, which asks for the missing criterion as well as the strengths. |
| M9 | Authorisation list without the count 「四类」, adding the row-stated authorisations (CTC-P003 merge, CTC-R005 format) | B, keeping A's 「道义强度（规范强度）」 | The count contradicted the rows; A's parenthetical keeps the link to the frontmatter term. |
| M10 | Modal vagueness routed uniformly through CTC-R004 | B (resolves D-A1, D-A2) | A split R004's six words into two classes that the R004 row does not make, so a review could cite either A005 (ERROR) or R004 (WARNING) for the same text. |
| M11 | 「strict／standard 模式下」 for 「改写模式下」 | B | Uses the mode name rather than a task name. |
| M12 | Review step 1 reverted to the baseline wording | revert A (D-A5) | A's procedure for reviewing text with no source is new normative content. It is kept below as a proposal. |
| M13 | 「未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。」 | B | Both tracks resolved this ambiguity in the same direction. B's wording stays closer to the baseline. |
| M14 | 「显性主语」 | CTC-T001 | Matches the term in the CTC-A001 row. |
| F-a | 「没有 ERROR 或 WARNING 级 finding 时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。」 | A + B | Both reviewers forked on whether 「问题」 includes STYLE items. A's condition settles that; B's 「观察」 with a rule ID is kept. |
| F-b | Step 7: 「没有改动无法归因到规则 ID 的地方（CTC-R001）」 | CTC-R001 row | 「规则并未要求改动」 would revert edits that CTC-R006 permits but does not require. |
| F-c | 「调用方可以显式授权的本来禁止的改动限于：…」 | baseline | The baseline's 「四类」 made the list closed, and the merged 「即」 left that open. |
| F-d | 「「超时后重试，多次失败则升级处理」中的「多次」与「升级」缺少执行所需的信息…」 | baseline §6 | A dropped this classification, which left it unclear whether the 「多次失败」 example line needs a fourth column. |
| F-e | Step 7 also checks the output contract (no preamble; structure and list granularity kept; 「待确认」 only when items exist) | baseline self-check item 12 | Confirmed WARNING loss in the review: neither the merge nor A carried this pre-return check. |

**Kept from A, adjudicated as not losing an assertion:**

- the §4 invariant table and its consequences column, now carried by the rule rows and the merged rewrite-flow step 7;
- ten of fifteen 「不得做的事」 items;
- six of eight worked examples;
- the six-field example block, with the field names kept in the review procedure;
- the six enumerated token prohibitions, implied by 「逐字符不变」 and the inventory rule;
- the ASCII ladder;
- the P003 row rewording: 「验收标准」→「判据」, and 「否则每份正常的流程文档都会…」→「以免正常的流程文档…」.

Two of the deleted examples were wrong in the baseline: 「归零」 invented a criterion, and the passive-voice example contradicted CTC-R003. Deleting them removes the error. The two examples that were wrong and kept are now A's corrected versions: the 「用户」 example in §9 keeps the named actor, and the P003 example in §10 merges into two compliant steps.

**Convergent clarifications accepted.** Both tracks independently made the following changes, and all four judges confirmed none of them is an ERROR-level loss:

- category 5 scoped outside categories 2–4;
- 「必须消歧」 replaced by disambiguation at the triggered rule's level;
- the warning-block scope attributed to CTC-P004, as that row already states;
- worked examples corrected to agree with the rows they illustrate.

## Alternatives considered

- **Adopt B (Opus) as is.** It is the pre-registered first-ranked candidate. Rejected because A's structure is 76 lines shorter with no confirmed assertion loss, and because B lacks the pre-return checks that A keeps.
- **Adopt A (Fable) as is.** Rejected. D-A4 and D-A5 are normative additions that would need the §20 admission gate. D-A1 is a new ERROR-grade fork.
- **Merge and also adopt D-A5.** Every cold reader in the experiment flagged the missing rule for reviewing text that has no source. It remains rejected here because adopting it is a rule-level decision, and it needs a failing case and a boundary example first.

## Open proposals (need a decision, not a rewrite)

Each item was raised by cold readers in both tracks and could not be fixed without changing a frozen rule row or adding a rule.

1. 「必须」 and 「不得」 clauses inside 「应」 rows (CTC-P003, CTC-A003). §6 now says the level column governs. Splitting the rows would be cleaner.
2. CTC-R003's 「过长的「的」字串」 and 「无必要的被动」 have no observable criterion.
3. 状态提示 is in scope (§1) but in neither the strict nor the standard scope list, so its mode cannot be inferred.
4. Reviewing text that has no separate source (audits, self-hosting) has no stated comparison base. A's D-A5 wording in `dev/inbox/si/track-2/r3/SKILL.md` §8 is a ready draft.
5. Whether CTC-R004's six words are exhaustive. The 「尽快」 example uses a word outside the list.
6. Which rule ID a missing-information finding cites in review (A005 versus the category's rule). A's D-A4 wording is a ready draft.
7. Category 7 says 「条件或例外」, which is narrower than CTC-S001's 「条件、例外、阈值、告警或失败分支」.
8. CTC-P004 calls moving a warning block a CTC-R005 violation, but CTC-R005 covers granularity, not position.
9. CTC-T001's 「最明确且出现最多」 can name two different forms.
10. The frontmatter says 「规范强度」, while the rows say 「道义强度」 and 「情态强度」. The frontmatter is frozen; §3 links the first two with a parenthetical.
11. CTC-P004's 「同句前段，或紧邻的上一句」 can be read as constraining the source's own step order, so it fires on ordinary runbooks where a step sits between the guard and the action. Both reviewers forked here. The deleted self-check wording 「守护条件仍在该动作之前」 favoured the looser reading.
12. 「标记多重集必须相等」 versus edits that change how often a token appears: an identifier used as a noun antecedent (CTC-A002), a determinable object written out (CTC-P002), terms unified (CTC-T001), or duplicates deleted (CTC-S001, R002).
13. When the caller names a mode that conflicts with the task (for example 「用 strict 审阅」), nothing says whether the output follows the task or the mode.
14. CTC-P003 says both 「压缩授权」 and 「授权合并步骤」. It is undecided whether a bare step-count limit authorises merging a verification step.

## Verification

- `tools/compare_skill.py` against the previous `SKILL.md` passes every hard gate: 29 rule levels unchanged, the seven 「待确认」 categories in order, the three mode headings, the five ladder rows, the six finding fields, the three severities, the frontmatter unchanged, and `check_skill.py` at 0 errors and 0 warnings. Output: `dev/inbox/si/merge/gate-vs-baseline.txt`.
- `skills-ref validate` on the packaged layout: valid.
- Independent review of the merged candidate (M1–M14) by a fresh Fable 5.1 reviewer and a fresh Opus 5.5 reviewer. Each did a cold self-hosting read with 14 reverse-decoding probes, then a comparison against the previous `SKILL.md`. Both reviewers report 29/29 rule levels and no ERROR-level change. Every self-hosting finding (Fable 5, Opus 11) and every fork (Fable 6, Opus 10) also exists in the previous `SKILL.md`, so the merge introduced none. Opus reported one WARNING-level loss, the output-contract pre-return check, which F-e restores. Outputs: `dev/inbox/si/merge/review-{fable,opus}.yaml`; rulings: `dev/inbox/si/merge/adjudication.md`.
- F-a–F-e were applied after the review and were not re-reviewed by a subagent. They passed the same gates (`dev/inbox/si/merge/gate-final.txt`).

| metric | previous `SKILL.md` | this version |
| --- | --- | --- |
| lines | 372 | 232 |
| body characters | 16 779 | 12 395 (−26.1%) |
| sections | 12 | 10 |

## Consequences

- Section numbers changed (12 → 10). Section references in decisions 003–005 and in `eval/reports/release-gates.md` describe the 2026-08-29 version.
- `spec/rules.v0.yaml` is unchanged. The only rule-row edit is a rendering change in CTC-P003: one term, and one rationale clause.
- The measurements in `eval/reports/release-gates.md` and the README status were taken on the previous version. Gold-case regression (`tools/ctc_eval.py run`) and human review of the trusted core remain the gates before this version can be called validated.

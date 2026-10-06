# Adjudication of the two reviews of the merged candidate

The orchestrator wrote this record: Claude Opus 5.5, the same model that built the merge.

- **Reviewed file:** `dev/inbox/si/merge/SKILL.md` (edits M1–M14 on `blind/A.md`).
- **Reviewers:** a fresh Fable 5.1 subagent and a fresh Opus 5.5 subagent, both at xhigh. Each did a cold self-hosting read with 14 probes, then compared the candidate against the previous `SKILL.md`.
- **Raw outputs:** `review-fable.yaml`, `review-opus.yaml`. Prompt: `dev/prompts/si-verify.md`.

## Results

| | Fable 5.1 | Opus 5.5 |
| --- | --- | --- |
| rule-level map | 29/29 | 29/29 |
| self-hosting findings (E/W/S) | 2/3/0 | 7/4/0 |
| findings also in the previous `SKILL.md` | 5 of 5 | 11 of 11 |
| forks (of 14 probes) | 6 | 10 |
| forks also in the previous `SKILL.md` | 6 of 6 | 10 of 10 |
| ERROR-level changes vs the previous `SKILL.md` | 0 | 0 |
| WARNING-level changes vs the previous `SKILL.md` | 6 | 14 |
| naturalness (5 = best) | 4 | 4 |
| over-control (see note) | 2 | 2 |
| wall time / 64K truncations | 21 min / 0 | 24 min / 0 |

**Scale note.** The verification prompt did not define the direction of the over-control scale. Both reviewers chose 1 = none and 5 = pervasive, the reverse of the si1 judges' scale. Their 2/5 therefore means little over-control, and it is not comparable to the experiment's scores.

## Rulings

- **No finding or fork was introduced by the merge.** Both reviewers checked every one of their own findings and forks against the previous `SKILL.md` and marked each one as also present there. The orchestrator spot-checked the five shared items and agrees:
  - 状态提示 has no mode;
  - the inventory equality versus edits that change token counts;
  - CTC-P004's 「紧邻的上一句」;
  - CTC-T001's 「最明确且出现最多」;
  - CTC-R003's 「过长」.
- **WARNING-level changes.** Both reviewers classified most of these as conflict resolutions toward the frozen rule rows. Each one appears in decision 006 as an accepted clarification.
  - Both: 「必须消歧」; the review severity of unresolved ambiguity; the warning-block scope; category 5.
  - Opus only: the 「四类」 list; numbers in step 1; the translation clause; the authorised-change exemption; the single severity system.
  - The new statement that 「必须」 inside a row does not change the row's level was reported as an addition (Opus V21). It was adjudicated style-only in si1 (C13/C117), since 「没有其他升级」 already implies it.
- **One confirmed loss (Opus V33, WARNING).** The pre-return check of the output contract was gone. The requirement survives in §3 and step 8, but the check of it does not. **Fixed by F-e.**
- **Two passages whose deletion made inherited forks more likely (Opus).**
  - The 「多次」 example in the baseline §6, which classified 「多次」 and 「升级」 as missing information. **Restored by F-d.**
  - The guard-order wording in the invariant table and the self-check, which favoured reading CTC-P004 as 「之前」 rather than 「紧邻」. Not restored: the fork is in the frozen row, so it is listed as an open proposal in decision 006.

## Fixes applied after the review (F-a to F-e)

Each fix either restores text from the previous `SKILL.md` or aligns a paraphrase to a frozen row. None adds a rule. The fixes were not re-reviewed by a subagent. They were checked with `tools/compare_skill.py`; output in `gate-final.txt`.

| fix | addresses | change |
| --- | --- | --- |
| F-a | fork on the review output when there are no findings (both reviewers) | 「没有 ERROR 或 WARNING 级 finding 时返回「未发现违规」…」. This combines A's definition of 「问题」 with B's observations that cite a rule ID; both tracks had resolved this the same way. |
| F-b | fork on step 7 versus CTC-R006 (Opus F7) | Step 7 now says 「无法归因到规则 ID 的地方」, the CTC-R001 row's own criterion, instead of 「规则并未要求改动」. |
| F-c | fork on whether the authorisation list is closed (Fable) | 「…限于：…」. The baseline's 「四类」 made the list closed; the merge's 「即」 left the question open. |
| F-d | fork on the 「多次失败」 line and the fourth column (Opus F8) | Restores the baseline's classification of 「多次」 and 「升级」 as missing information. |
| F-e | lost output-contract check (Opus V33) | Restores the baseline self-check item 12 into step 7. |

Final: 232 lines, 12 395 body characters (−26.1% against the previous `SKILL.md`), all hard gates pass, and `skills-ref validate` reports a valid skill.

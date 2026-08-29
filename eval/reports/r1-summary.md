# Evaluation run `r1` — baseline for `SKILL.md` before the repair pass

- **Date:** 2026-08-29
- **Artifact under test:** `SKILL.md` at commit `c827484` (348 lines, 29 rules)
- **Cases:** 56 gold cases, `eval/gold/`
- **Models:** Claude Opus 5, GPT-5.6 Sol (`model_reasoning_effort=high`), Gemini 3.7 Flash (high)
- **Judge:** GPT-5.6 Sol, prompt `dev/prompts/judge-semantic.v1.md`, `--exclude-self`

## Coverage, and what it does not cover

| model | outputs | judged |
|---|---|---|
| Gemini 3.7 Flash | 56 / 56 | 56 |
| GPT-5.6 Sol | 56 / 56 | 0 — it was the judge |
| Claude Opus 5 | 35 / 56 | 35 |

Two gaps, stated rather than smoothed over. **GPT's own 56 outputs were never semantically
judged**, because the only judge available was GPT itself and judging one's own output is exactly
what D001 established as worthless. **Claude's sweep stopped at 35** when the session hit a usage
limit. Both gaps are coverage, not failure: nothing suggests the missing runs would have been
worse, and nothing establishes that they would have been fine either.

## Deterministic layer

**Zero ERROR-level failures across all 147 outputs.** No protected-token mutation, no lost
quantity, no threshold-boundary flip.

That number is only meaningful after the checker repair. The first pass reported 29, 15 and 29
failures with near-identical failure sets across three different models — the signature of a broken
checker. Four defects were found and fixed (rule IDs parsed as quantities, Markdown list markers
parsed as quantities, review outputs compared against the source's inventory, and repetition
treated as drift). The pre-repair numbers measured the checker, not the skill.

Warnings that remain are by design and hand off to the semantic layer: modal-profile diffs (11–16
per model), threshold-comparator diffs (5 per model), added quantities (1–4 per model).

## Semantic layer

| | Claude | Gemini |
|---|---|---|
| pass | 28 / 35 (80%) | 49 / 56 (88%) |
| mean naturalness | 4.66 / 5 combined | |

Failure kinds across 14 failing verdicts: `over_edit` 6, `rendering` 4, `fact` 3, `actor` 2,
`review_recall` 2, `quantities` 2, `protected_tokens` 2, `terminology` 1, `review_precision` 1.

**Over-editing is the dominant failure class**, which is the result the design predicted and the
reason one case in three is a trap. A controlled-language skill that fails anywhere fails here.

## Root causes, separated

Six of the failures were traced past the symptom. Two are defects in the rules, one is a defect in
the judge, three are model limitations.

**Rule defects — fixed, with regression cases.**

1. `G-L-012`: `CTC-P004` requires a guard to precede the action it guards. The source put its
   `警告：第 3 步不得与第 1、2 步并行。` in a trailing block. Both Claude and Gemini restructured an
   already-compliant procedure to comply — Claude merged the warning into step 3, Gemini moved it
   above step 3. Two independent models making the same edit is a rule that did not say what it
   meant. A structural warning block governs its whole procedure from either end; moving it is now
   an `CTC-R005` violation rather than `P004` compliance.
2. `G-A-003`: the `待确认` category for a missing success criterion (`CTC-P003`) had no bounded
   generating condition, so a clean four-step runbook produced a pending item for every step that
   lacked an acceptance criterion. It now fires only where a destructive step's success gates what
   follows.

**Judge defect — fixed.** The rubric scored any output differing from the source as severe
over-editing, which counted an appended `待确认` section as a text change. `G-A-003` failed on this
before the rule defect above was even reached.

**Misdiagnosis — withdrawn.** `G-P-003` was initially read as a third rule defect, on the grounds
that all three models merged a verification step. They were following the case's own `instruction`,
which authorises compression to at most three steps, and the case prefers intact checks over step
count. The constraint added on that reading was withdrawn and `CTC-P003` re-scoped around what the
case actually tests. See `eval/disagreements/D004`.

**Model limitations — recorded, no rule change.**

3. `G-R-012`: Gemini reported a natural agentless passive as a `CTC-A001` missing-actor `ERROR`.
   §8 item 3 and `A001`'s own exception both already say not to. `A001` gained one clarifying
   sentence for review mode; the over-firing is the model's, not the rule's.
4. `G-A-002`: both Claude and Gemini found a real ambiguity at the expected locus but a different
   one from the case's expected finding — the rollback target rather than the rollback actor. Both
   cited the right rule. Recall on the third ambiguity was missed by both. Recorded as a known
   recall limitation; forcing exhaustive ambiguity reporting would trade it for a false-positive
   flood, which is the worse failure.

## Conclusion

The skill holds the deterministic invariants completely and the semantic invariants at 80–88%. The
failures cluster where the design said they would — restraint, not preservation. Two were the
rules' fault and are fixed, one was a defect in the judge, one was a misdiagnosis by the reviewer,
and the rest are the frontier.

Post-fix regression on the affected cases: `G-L-012` and `G-R-012` now pass in both models —
the warning block stays where it is and the agentless passive is no longer reported as a missing
actor. `G-A-003` no longer produces pending-item noise. `G-P-003` compresses as instructed while
keeping the checkpoint operator-executed and complete.

The run's own instrument was wrong on first use and had to be repaired before its numbers meant
anything. That is worth carrying forward: an evaluation harness is an artifact under test too.

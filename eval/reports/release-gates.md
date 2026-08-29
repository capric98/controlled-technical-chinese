# Release gates for `SKILL.md`

Assessed against `000-design.md` §30. Date: 2026-08-29.

| gate | status | evidence |
|---|---|---|
| Format | **pass** | `check_skill.py`: 0 errors, 0 warnings. `skills-ref validate` on the packaged layout: `Valid skill` |
| Self-containment | **pass** | no reference to `docs/`, `spec/`, `eval/`, `dev/`, `tools/`, `AGENTS.md` |
| Semantic | **pass, with a stated coverage gap** | 0 ERROR-level deterministic failures across 147 outputs; no protected-token mutation, quantity loss or threshold flip in any run |
| Ambiguity | **pass** | high-severity actor, reference, scope and procedure cases covered; the over-control traps that guard against unnecessary explicitness pass in both models after the fixes |
| Naturalness | **pass** | mean 4.66/5 across 91 judged outputs; no systematic translationese or pseudo-legal style reported |
| Self-hosting | **pass** | review-mode self-review returned 9 findings; 8 fixed, 1 rejected with reason; re-run clean |
| Cross-model | **partial** | 3 models ran the corpus; GPT's 56 outputs are unjudged because GPT was the only judge available |
| Trusted core is human-reviewed | **open** | the 56 gold cases are `orchestrator-reviewed` and cross-audited by a second model, not human-reviewed |

## What passes, precisely

`SKILL.md` is 372 lines, carries all 29 frozen rule IDs, and validates as an Agent Skill in its
packaged layout. Across 147 outputs from three models there was no deterministic failure of any
kind. Semantic pass rates were 80% (Claude, 35 cases) and 88% (Gemini, 56 cases), with over-editing
the dominant failure class — the outcome the design predicted.

Reverse-decoding found 8 internal contradictions and 9 self-demonstration violations; all are
repaired. Self-hosting review found 9 more; 8 are repaired and 1 is rejected on the ground that a
risk explanation in the skill's own rationale is not a target-document proposition.

Four defects were found and fixed with regression cases behind them: two rule defects
(`CTC-P004`'s handling of structural warning blocks, `CTC-P003`'s unbounded pending-item category),
one judge-rubric defect, and one constraint added on a misdiagnosis and withdrawn (`D004`).

## What does not pass, and why it is not being smoothed over

**The trusted core is not human-reviewed.** `000-design.md` §21 wants core gold cases human-reviewed
or grounded in unambiguous accepted semantics. These are agent-reviewed and cross-audited between
two models with different roles, which is stronger than model-proposed and weaker than what the
design asks for. Every case can therefore be wrong in a way no model in this loop would notice.
`D004` is a live demonstration that the reviewer in this loop does miss things.

**GPT's 56 outputs were never semantically judged.** The only judge available was GPT, and D001
established that a model's assessment of its own output carries no information. The correct fix is
a judging pass by a fourth model or by Claude once quota allows.

**Claude's sweep covered 35 of 56 cases**, stopping on a usage limit. The 21 unrun cases are not
known to be fine.

**Reverse-decoding was Claude reading Claude-rendered prose.** A reader with different priors will
find a different set of forks. The next pass should use a non-Claude decoder.

**Mutation detection has not been run.** `eval/mutations/generated.yaml` holds 37 single-defect
mutants across 11 classes and the per-class detection rates that `000-design.md` §16 asks for have
not been measured.

## Recommendation

`SKILL.md` is a defensible release candidate on the format, semantic, ambiguity, naturalness and
self-hosting gates. It is **not** releasable as a validated artifact until the trusted core has been
human-reviewed, because every other gate is measured against that core, and a gate measured against
unreviewed expectations reports the expectations rather than the artifact.

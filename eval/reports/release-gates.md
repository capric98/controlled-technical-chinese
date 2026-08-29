# Release gates for `SKILL.md`

Assessed against `000-design.md` §30. Date: 2026-08-29.

| gate | status | evidence |
|---|---|---|
| Format | **pass** | `check_skill.py`: 0 errors, 0 warnings. `skills-ref validate` on the packaged layout: `Valid skill` |
| Self-containment | **pass** | no reference to `docs/`, `spec/`, `eval/`, `dev/`, `tools/`, `AGENTS.md` |
| Semantic | **pass, with a stated coverage gap** | 0 ERROR-level deterministic failures across 147 outputs; no protected-token mutation, quantity loss or threshold flip in any run |
| Ambiguity | **pass** | high-severity actor, reference, scope and procedure cases covered; the over-control traps that guard against unnecessary explicitness pass in both models after the fixes |
| Naturalness | **pass** | mean 4.66/5 across 91 judged outputs; no systematic translationese or pseudo-legal style reported |
| Self-hosting | **pass** | review-mode self-review returned 9 findings; 8 fixed, 1 rejected with reason; re-run clean. The project's own Chinese README was then produced by running the skill as a translation task and verified by a third model (see below) |
| Mutation detection | **partial** | 45/45 detected across 11 classes, one reviewer only; two classes have n=1 |
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

**Mutation detection has been run for one reviewer only.** 45 mutants over 11 classes, 45/45
detected by Gemini with both the right rule and the right locus (`eval/reports/mut1-summary.md`).
That measures Gemini running CTC, not CTC; the corpus exists to compare reviewers and only one has
been run. Two classes have a single mutant each.

## Dogfooding: the Chinese README

The repository's default `README.md` was produced by running `SKILL.md` over the English one as a
`translate` / `standard` task, then verified by a model that did not produce it. Structure parity is
exact — 9 headings, 8 fences, 10 bullets, 8 links, every link target byte-identical — and every
number in the source survives.

The independent verifier returned ten findings. Seven were accepted and fixed: a scope narrowing
(「英译中技术翻译」 constrained the source language where the English constrains only the target), an
added degree claim (「高语义保真度」), an added condition (「一味变严」), an unsourced 「全量」 asserting
complete coverage in a sentence that reports 35 of 56, a lost `canonical`, an epistemic shift on
"not admissible evidence", and four translationese sentences.

Three were rejected with reasons: the changed link target is the deliberate language switcher, and
「步骤」 and 「判据」 are the project's own established terms — `CTC-T001` puts the source and the
invoking context above a translator's preference, and `SKILL.md` uses both words for exactly these
concepts.

The exercise found two real gaps in the skill, both now closed by clarification rather than by new
rules:

- `CTC-S005` froze every fenced block byte-for-byte, which forbids translating a directory legend or
  a ladder diagram in an untagged `text` fence. Prose-bearing fences may now be translated; paths,
  commands, identifiers and numbers inside them still may not change.
- The translation clause did not cover source-language number words, leaving `twenty-nine` → `29`
  looking like the numeral-system change policy 2 forbids. It is now explicitly not one.

It also found three defects in the harness — a single-letter unit matching inside `45 single`, a
bare 「一般」 matching 「一般意义上」 as a frequency claim, and quantity and fence comparison being
applied across languages at all.

## Recommendation

`SKILL.md` is a defensible release candidate on the format, semantic, ambiguity, naturalness and
self-hosting gates. It is **not** releasable as a validated artifact until the trusted core has been
human-reviewed, because every other gate is measured against that core, and a gate measured against
unreviewed expectations reports the expectations rather than the artifact.

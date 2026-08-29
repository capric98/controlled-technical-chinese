# Mutation run `mut1` — per-class detection rate

- **Date:** 2026-08-29
- **Corpus:** `eval/mutations/generated.yaml`, 45 single-defect mutants over 11 classes
- **Reviewer:** Gemini 3.7 Flash (high), `SKILL.md` in review mode
- **Scorer:** `tools/score_mutations.py`

## Result

**45 / 45 detected**, at 100% in every class. Each detection required both the right rule and the
right locus; citing a covering rule while quoting the wrong place does not count, and neither does
the reverse.

| class | n | detected |
|---|---|---|
| certainty_inflate | 2 | 100% |
| condition_broaden | 5 | 100% |
| modality_strengthen | 4 | 100% |
| modality_weaken | 6 | 100% |
| negation_scope | 1 | 100% |
| order_swap | 6 | 100% |
| quantity_drift | 6 | 100% |
| term_substitute | 2 | 100% |
| threshold_flip | 1 | 100% |
| token_mutate | 6 | 100% |
| unsourced_qualifier | 6 | 100% |

The design's purpose for this corpus is to find the classes a reviewer must not be trusted alone
for. On this run there are none.

## What this does and does not establish

It measures **Gemini running CTC**, not CTC alone. A second reviewer would produce a different
profile, and the profile is the point — the corpus exists to compare reviewers, and only one has
been run.

Two classes have `n = 1` (`negation_scope`, `threshold_flip`). A single mutant is an anecdote. The
thin classes are thin because the gold sources happen not to contain the triggering patterns, which
is a fact about the gold corpus and a reason to grow it.

Every mutant is `provenance: generated-mutation` and does not gate a release.

## Two corrections along the way, both to the instrument

The first attempt handed each mutant to the reviewer **alone**. That makes most of the corpus
undetectable by construction: 「2 分钟」→「4 分钟」 is an ordinary threshold when there is no original
to compare against. Mutants are now presented as an 原文/候选改写 pair, which is what reviewing a
rewrite actually is.

The scorer's first run then reported 93% with three misses. All three were scorer defects. Gemini
had found and correctly described every one:

- two `condition_broaden` mutants deleting a 「连续 N 次」 gate were reported under `CTC-S004`
  (quantity), which is defensible — the gate *is* a count — and was missing from the covering-rule
  map;
- one `order_swap` was reported with the moved line quoted verbatim, but the scorer built its locus
  needles from `difflib` fragments, which for a swap are rearranged pieces rather than the lines a
  review would quote.

This is the third time in this project that the instrument was wrong before the artifact was — the
deterministic checker, the over-edit judge rubric, and now the mutation scorer. Each time the first
number was pessimistic and looked plausible. A measurement that agrees with expectations is not
thereby validated.

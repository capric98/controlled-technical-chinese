# 005 — What reverse-decoding found, and how each finding was resolved

- **Status:** Accepted
- **Date:** 2026-08-29
- **Relates to:** `000-design.md` §14, §15, §30; `004-rule-set-adjudications.md`
- **Evidence:** `dev/inbox/r5-claude-reverse-decode.yaml`

## What was done

`000-design.md` §14 requires that rendered normative prose be reverse-decoded: an independent
reviewer reconstructs each rule's level, scope, trigger, required behaviour, prohibited behaviour,
exceptions, and invariant from the rendered text alone, and the reconstruction is compared with the
intended semantics. Divergence means the wording is under-controlled, however fluent it reads.

A reviewer was given `SKILL.md` and nothing else — no access to `spec/`, `docs/decisions/`,
`eval/`, `dev/`, or the repository instruction files — and confirmed at the end that it had read
none of them.

## Headline result

**All 29 rules admitted two materially different enforcement behaviours.** Ten carried uncertain
normative strength. Eight passages contradicted other passages outright. Nine places in the
document violated its own rules.

The rules themselves were not wrong. The canonical semantics in `spec/rules.v0.yaml` are unchanged
by this pass. What was wrong was the belief that a careful rendering by a capable model produces
controlled prose. It does not: it produces prose whose author knows what it means. The gap only
becomes visible when someone who does not know reconstructs it.

This is the strongest evidence so far for the design's insistence that §14 is a gate rather than a
formality, and it is a direct parallel to D001 — in both cases a model's confidence about its own
output carried no information about the output's quality.

## Contradictions, and how each was resolved

| # | Conflict | Resolution |
|---|---|---|
| C1 | `待确认` declared a closed list of four categories; four other passages routed reports into it | Keep it closed, complete it to six. Terminology divergence routes through the `CTC-S002` category in rewrite mode and is an ordinary finding in review mode |
| C2 | §6 graded `CTC-A005` findings down to `WARNING`; §10 says there is no downgrade | Delete the `WARNING` branch. Ambiguity whose readings do not change operations is not reported at all — §6 already says so |
| C3 | §4 called its entries semantic invariants; §7 grades four of the backing rules `应` | §4 lists properties to verify and assigns no severity; §7 fixes severity. A level column makes the four visible |
| C4 | `CTC-S001`'s length-cap clause permitted deleting an exception last; `CTC-L001` forbids it at `必须` | Remove the escape. Return the shortest fully compliant text and report that the cap could not be met |
| C5 | §2's tie-break made non-disambiguating explicitation an `R002` violation; `CTC-P002` requires writing out a determinable action or object | Clarify: `P002` removes *operational* indeterminacy, which is a form of ambiguity and is licensed. `R002` forbids explicitation that removes no indeterminacy of any kind |
| C6 | The identifier test and the product-name exclusion both capture `Node-RED`, `GitLab`, `.NET` | Order the tests. Code markup or use as a command/path/identifier/field/value makes a token protected. A product name in prose is not protected, but its spelling is kept and it is never translated |
| C7 | strict handling `应` rules "as ERROR" contradicted both the level↔severity mapping and "no escalation" | Severities exist only in review mode. In strict, the lower threshold changes what *triggers*, not what severity a finding carries |
| C8 | `CTC-R005` was given three incompatible characterisations | Split it. Scope leakage is condition preservation and moves to `CTC-L001` at `必须`; `R005` keeps format and granularity at `应`, waivable by the caller |

## Structural gaps

- **No rule was assigned a priority-ladder layer**, so §7's definition of `应` — "may be overridden by
  a higher priority" — could not be executed at all. Families are now mapped to layers: S and L to
  layer 1, A and P to layer 2, T to layer 3, R002/R003/R005 to layer 4, R006 to layer 5, with
  `CTC-R001` cross-cutting.
- **`CTC-R002` and `CTC-R003` never said whether they license editing the source** or only constrain
  what the model adds. Since the output contains the source, both readings were available, and the
  whole question of whether CTC is a minimal-diff auditor or a whole-document restyler hung on it.
  Now stated: a defect in the source is repaired only when its own rule triggers, at the smallest
  edit that removes it.
- **The `待确认` format had no slot for the 建议 that §6 mandates.** A fourth optional field was added,
  and per-change attribution is now stated to be internal discipline in rewrite mode rather than a
  missing output field.

## Self-demonstration failures

The document tells a model not to make unattributed edits, not to merge near-synonyms, and not to
assert unsourced frequencies. Its own examples did all three.

Three of the seven worked 正例 and the single worked review finding carried edits no rule had
triggered — a 销毁→清理 near-synonym swap that `CTC-T002` forbids, a predicate-argument change
bundled into a modality finding, and a reordering of an already-compliant source. Strict mode's
ambiguity gate rested on 「合理」, a word on `CTC-R004`'s own criterion-free list. Two passages made
unsourced empirical and frequency claims of exactly the class `CTC-S002` forbids — including,
pointedly, the sentence arguing that self-assessment is worthless.

All are repaired. The one worth naming: the argument for why a model's self-assessment is not
evidence was itself made by citing an unciteable statistic. The instruction was right and the
evidence was not admissible inside a self-contained artifact, so it is now stated as a rule.

## Consequences

- Reverse-decoding is confirmed as a release gate, not a formality, and must be re-run after any
  material rewrite of `SKILL.md`. A pass that finds no two-reading forks would be the surprise.
- A future pass should use a **second, non-Claude** reverse-decoder. This one was Claude reading
  Claude-rendered prose; a reader with different priors will find a different set.
- The redundancy between §4, §7, §8 and §11 generated two of the eight contradictions on its own.
  Restating a rule in a second place is how a document acquires two versions of it.

# 004 — Adjudicating the rule set's open issues

- **Status:** Accepted
- **Date:** 2026-08-28
- **Relates to:** `spec/rules.v0.yaml` (`open_issues`), `000-design.md` §6, §7, §26, §28;
  `003-core-semantic-policy.md`; `eval/disagreements/D003`

## Context

The canonical rule set (29 rules, 19 MUST / 9 SHOULD / 1 MAY) closed with seven open issues that
the drafting role could not settle alone, because each one decides how the whole set behaves rather
than what one rule says. They are settled here so that `SKILL.md` has one answer to each.

## 1. Rewrite and translate need an output contract, including a report channel

`000-design.md` §6.3 defines an output structure for review mode only. Four rules (`CTC-A005`,
`CTC-P003`, `CTC-P005`, `CTC-R004`) require a way to report something without changing the text —
which decision 003 policy 1 already mandates for unresolvable ambiguity.

**Decision.** Rewrite and translate return the rewritten text alone, preserving the source's
Markdown structure, list granularity, and code fences, with no preamble. When and only when
unresolved items exist, one final `待确认` section is appended, one line per item, each as
`位置 | 问题 | 需要的信息`.

Admissible items are limited to four: an ambiguity that evidence could not resolve (`A005`), a
success criterion the source never stated (`P003`), a trigger condition missing from a tool
description (`P005`), and an undefined normative criterion (`R004`). Bounding the list is what keeps
the channel from becoming a place to voice style preferences.

## 2. Modes change the trigger threshold, not the rule level

**Decision.** A rule's level is mode-invariant. Strict mode does not promote `SHOULD` to `MUST`.
What changes across modes is the **ambiguity threshold**:

- **strict** — a reading diverges if any plausible operator reading leads to a different action.
- **standard** — a reading diverges if an ordinary technical reader would plausibly disagree.
- **review** — reports at the threshold appropriate to the document type, and rewrites nothing.

S, L, and T rules are threshold-independent: semantic invariants do not relax in standard mode.

**Rejected: per-mode levels.** Levels would then be unstable, a gold case could not state an
expected severity without also fixing the mode, and cross-mode regression comparison would break.

## 3. Terminology consistency is scoped to what the invocation can see

**Decision.** The scope is the text visible in the invocation plus any glossary the caller supplies.
Within that scope, variants are unified only when they clearly denote one concept. When it is not
clear — the usual case for a fragment — the variants are reported rather than merged.

CTC ships no glossary (`000-design.md` §7.4), so it cannot know that 「作业」 and 「任务」 are one
concept in a system it cannot see. Merging on suspicion is how false normalization happens, and
`CTC-T002` exists to prevent exactly that.

## 4. `CTC-L004` is threshold-boundary, and is now frozen

`002-gold-case-schema.md` used `rule: CTC-L004` in its illustrative case, and `000-design.md` §7
freezes an ID once a decision or evaluation case references it. The reference was illustrative, but
the rule this ID now carries is the one the example describes.

**Decision.** `CTC-L004` = threshold-boundary preservation. Frozen.

## 5. No rule for making implicit logical relations explicit — rejected

`000-design.md` §7.2 lists "implicit logical relationships" as a candidate ambiguity area, and the
rule set has no rule for it.

**Decision.** Deliberately none, and this is recorded so it is not "fixed" later.

A rule requiring implicit relations to be made explicit would fire on ordinary Chinese, where
juxtaposition carries relation reliably. Both independent round-1 passes identified the resulting
damage without prompting: GPT's `OR-04` ("all adjacent steps get an explicit causal connective")
shows how it invents causation from mere sequence — 「检查日志，因此导出指标」 — and Gemini's
`OC-03` shows the same constraint shattering serial-verb constructions.

The genuine failures in this area are already covered. Wrong attachment after a rewrite is
`CTC-A003`; a reversed or inverted logical relation is `CTC-L002`; a fabricated causal link is
`CTC-S006`. A new rule would have to earn its cost against these three, and no failing case exists
that they miss.

## 6. Severity derives from rule level, with one escalation that must be demonstrated

`000-design.md` §28 defines severity by consequence. Levels were assigned by consequence. So the
mapping holds by construction:

```text
MUST violation   → ERROR
SHOULD violation → WARNING
MAY violation    → STYLE
```

**Decision.** That mapping is the default. A `SHOULD` violation may be reported as `ERROR` only when
the finding's `风险` field names the specific different action an operator would take as a result.
No other escalation, and no de-escalation.

The escalation exists because `CTC-T001` (term consistency) really can be operationally serious —
inconsistent terms in an authorization document cause misconfiguration. Requiring the reviewer to
name the divergent action keeps it testable and rare.

## 7. `CTC-R001` stays in family R

Minimal attributable intervention constrains how every family is applied, not how text is rendered,
so its family letter is arguably wrong.

**Decision.** It stays `CTC-R001`. Family letters are stable prefixes (`000-design.md` §7), not a
taxonomy, and R is "rendering and controlled style" — which is where over-editing control belongs.
`SKILL.md` states that this rule governs all families. Renaming would cost ID stability for a
classification improvement nobody can act on.

## 8. Extension rather than a new rule for D003

`eval/disagreements/D003` concluded that vague modality in compliance-sensitive text must be
reportable but not silently repaired. `CTC-R004` already carries exactly that behaviour: it triggers
on undecidable criterion words and requires rewrite mode to raise them in `待确认` rather than supply
a criterion.

**Decision.** Extend `CTC-R004`'s trigger vocabulary to include modal-strength hedges — 「尽可能」
「尽量」「最好」「适当」「必要时」 — when they carry the operative obligation in a normative
instruction. No new rule. `000-design.md` §20 prefers clarifying an existing rule over adding one,
and this is a clean instance.

## Consequences

- Item 2 means a gold case can state an expected severity without also pinning the mode, which is
  what makes cross-mode regression comparison possible.
- Item 5 is a rejection that must survive future review passes; a reviewer noticing the gap will
  keep proposing the rule. The rejection is recorded with its counterexamples for that reason.
- Item 6's escalation is the only place where a reviewer's judgment can change a severity, and it
  is gated on naming a consequence.

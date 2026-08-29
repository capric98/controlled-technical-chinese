# D003 — Agent-instruction register demands certainty; modality preservation forbids supplying it

- **Status:** Resolved — modality preservation wins, and the conflict becomes a rule
- **Date:** 2026-08-28
- **Type (`000-design.md` §13):** proposed wording is natural (and operationally better) but
  semantically lossy → semantic invariant wins
- **Source artifacts:** `dev/inbox/r2-gemini-cases.yaml` (`G-R-009`),
  `dev/inbox/r3-gpt-audit-gemini.yaml`
- **Reviewers:** Gemini 3.7 Flash (case author), GPT-5.6 Sol (auditor), orchestrating Claude Opus
  (adjudicating)

## The conflict

Gemini authored `G-R-009` to test register cleanup on an agent instruction:

```text
请您在注意到用户的输入里面好像有 SQL 相关词汇的时候，尽可能帮忙调用一下
`sanitize_query` 工具对输入进行清理哦，千万不要直接拿去拼接字符串。
```

Its round-1 register guidance is right about what this text needs: agent instructions want
determinism, closed boundaries, no politeness formulas, and precise predicates, because vague
modal words measurably reduce compliance. So the case required the rewrite to produce
「必须先调用」 and to turn 「好像有 SQL 相关词汇」 into a definite condition.

GPT's audit rejected the case outright. Its argument: decision 003 policy 5 preserves a target
document's modal class rather than normalising it, and policy 1 forbids silently resolving genuine
uncertainty. The case does not merely permit those two moves — it **requires** them. A candidate
that obeyed decision 003 would fail the case.

Both are right about their own half. That is what makes this worth recording.

## Adjudication

**Modality preservation wins.** The priority ladder in `000-design.md` §4 puts semantic invariants
above operational clarity, and 「尽可能」 → 「必须」 is not a clarification. It grants the agent's
author an obligation they did not write. If the author meant "always sanitize", the fix is for the
author to say so; a rewriting pass cannot know that, and the cost of guessing wrong in a security
instruction is asymmetric.

The same holds for the trigger. 「好像有 SQL 相关词汇」 is genuinely fuzzy, and 「输入包含 SQL
关键字」 is a different, testable condition. Substituting one for the other manufactures a decision
criterion.

## What the conflict actually revealed

Deleting the case would have thrown away the finding. The real conclusion is that CTC was missing a
behaviour, not that Gemini was wrong about the problem.

**Vague modality in compliance-sensitive text is a defect worth reporting — and reporting it is
CTC's job. Fixing it is not.**

For agent instructions, tool descriptions, and safety-relevant procedures, a hedge like 「尽可能」
「适当」「必要时」 in the operative clause is a real risk: the reader is a model whose compliance
depends on the modal word. CTC should flag it, name the two or more strengths it could carry, and
propose a correction — then stop. The author decides.

This gives the register goal a legitimate route to the same outcome, without letting a rewriting
pass silently raise an obligation. It also explains why the two policies did not actually conflict:
policy 1 already says report rather than resolve, and nobody had applied it to modality strength.

## Resolution applied

`G-R-009` was rewritten rather than deleted. It now checks that a candidate:

- removes the conversational register (「请您」「帮忙」「一下」「哦」) — this part of Gemini's case
  was always correct;
- does **not** raise 「尽可能」 to 「必须」, nor 「千万不要」 to 「禁止」;
- does **not** convert the fuzzy trigger into a definite condition without marking it;
- keeps `sanitize_query` byte-identical.

Its three `invalid_transformations` now separate the failure modes: one that cleans the register and
over-strengthens, one that preserves modality but leaves the politeness formulas, and one that does
both wrong and drops a constraint as well.

## Consequences

- CTC needs a rule covering vague modality in compliance-sensitive text: reportable as `WARNING`,
  not silently rewritten. `G-R-009` is its evidence and its regression case.
- Review mode carries more of the load than the original design assumed. Several defects CTC can
  detect are ones it must not fix, so review is not a lesser mode — it is the only mode that can
  address a whole class of real problems.
- A case author working from a legitimate quality goal can encode a policy violation without
  noticing. The round-3 audit prompt asked explicitly for `policy_conflict` as a defect kind, and
  that is the only reason this was caught. Keep that instruction in future audit prompts.

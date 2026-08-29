# D002 — Strawman failures, and whether test material may contain deliberate defects

- **Status:** Resolved — one finding accepted, one rejected
- **Date:** 2026-08-28
- **Source artifacts:** `dev/inbox/r2-gpt-cases.yaml`, `dev/inbox/r3-gemini-audit-gpt.yaml`
- **Reviewers:** GPT-5.6 Sol (case author), Gemini 3.7 Flash (language auditor), orchestrating
  Claude Opus (adjudicating)

## Context

Round 3 had each model audit the other's gold cases in its own area of strength. Gemini audited
GPT's 24 cases for whether the Chinese is credible technical text and whether the failures the
cases describe are failures a real model would actually produce.

It scored source quality 4.92/5 and bad-output realism 4.63/5, and raised two objections.

## Finding 1 — accepted: the failures were too obviously wrong

Gemini flagged `G-S-006`, `G-S-009`, and `G-L-012`. In each, the `invalid_transformations` entry
reaches its violation by reversing a polarity outright:

| case | the constructed failure |
|---|---|
| `G-S-006` | `root cause is still unconfirmed` → 「根因已经明确」 |
| `G-S-009` | 「不要自动重启服务」 → 「只需自动重启上游服务」 |
| `G-L-012` | a numbered procedure with an explicit no-parallel warning → 「并行执行以下操作：」 |

Its argument: a competent model does not contradict an explicit instruction in the source. Real
failures are quieter. The realistic shape of each is the one where the surface constraint survives
and something underneath it moves.

**Type (`000-design.md` §13):** empirical claim about model behaviour.
**Authority:** the language and behaviour evaluator. This is exactly what Gemini's role is for, and
GPT has no stronger evidence to offer against it.

**Resolution: accepted.** A subtle `invalid_transformations` entry was added to each of the three,
built from the failure shapes Gemini described:

- `G-S-006` keeps 「根因待确认」 and still upgrades `may be associated with` to 「由…导致」;
- `G-S-009` keeps the prohibition on auto-restart and injects 「通常」 and 「只需」;
- `G-L-012` keeps all three numbered steps and every protected token, and deletes only the warning.

The original strawman entries were **kept alongside** them. They cost nothing, and a case that
documents both the crude and the subtle form of a failure is more useful than one that documents
only the subtle form. This does not change any case's pass condition, which rests on `invariants`,
not on the enumeration of bad outputs.

## Finding 2 — rejected: the deliberate translationese in `G-L-006`

Gemini scored `G-L-006` lowest for source quality (3/5) and proposed replacing its source:

```text
current:  错误 `E_LOCKED`：由于该资源正在被另一个进程占用的事实，当前请求已被拒绝。
proposed: 错误 `E_LOCKED`：因该资源正被另一个进程占用，当前请求已被拒绝。
```

The objection is correct as language criticism. 「由于……的事实」 is a literal rendering of
"due to the fact that" and no Chinese engineer writes it.

**Rejected anyway.** The case is not a document; it is test material, and that clumsiness is the
point. `G-L-006` exists to test both dimensions at once: the model should repair the clumsy phrasing
**and** must keep 「另一个进程」 rather than generalising it to 「其他进程」. Applying the proposed
fix removes the first dimension and leaves a case that only tests the quantifier.

The tension is the whole reason the case is valuable. D001 finding 6 is the record of a real model
making exactly this trade — improving the sentence and widening the quantifier in the same edit.

**Type:** a disagreement about what the artifact is for, not about the language.
**Authority:** case design intent, which sits with the specification role.

A note was added to `G-L-006` recording that the translationese is deliberate, so that a later agent
does not "fix" it.

## Consequences

- Case authors should be asked for the **subtle** form of a failure explicitly. Left to itself, an
  adversarial author writes the maximally clear violation, which is the one a real model is least
  likely to commit.
- Auditing test material for naturalness needs the auditor to know which defects are deliberate.
  The round-3 audit prompt did not say so, which produced finding 2. A future audit prompt should.
- Gemini's `natural_alternative` in this audit preserved 「另一个进程」 correctly, which is the
  quantifier it had generalised in D001. The instruction to self-check seven invariant classes
  before writing a rewrite appears to have worked; that is worth keeping in renderer prompts.

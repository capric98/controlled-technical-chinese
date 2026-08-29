# 003 — Core semantic policy: ambiguity, quantities, protected tokens, structure, modality

- **Status:** Accepted
- **Date:** 2026-08-28
- **Relates to:** `000-design.md` §7, §24, §26, §27; `002-gold-case-schema.md`
- **Evidence:** `dev/inbox/r1-gpt-invariants.yaml` (`open_questions`),
  `dev/inbox/r1-gemini-naturalness.yaml`, `eval/disagreements/D001-naturalness-vs-modality.md`

## Context

Round 1 produced six questions that cannot be answered by a rule in isolation, because each one
sets a policy that many rules then depend on. Leaving them open would let each rule resolve them
differently, which is how a controlled-language spec acquires internal contradictions.

Each decision below is stated with the alternative that was rejected and why, because the rejected
alternative is in every case defensible.

## 1. Genuine ambiguity is reported, never silently resolved

**Decision.** When the source is ambiguous and the surrounding context does not determine the
reading:

- the output keeps the original expression unchanged;
- the skill appends a short `待确认` list naming the location, the competing readings, and the
  information that would settle it;
- in review mode the finding is `ERROR` when the readings imply different operations, and
  `WARNING` when they do not.

Choosing a reading is prohibited. So is emitting several complete alternative versions.

**Rejected: pick the most probable reading.** It manufactures a fact. D001 finding 5 is the
demonstration: `隔离受感染的主机和网关通信` was silently rendered as "cut the link between the
host and the gateway", which is one of two readings and implies a materially different containment
action from the other.

**Rejected: refuse to produce output until the author clarifies.** It makes the skill unusable in
the generation workflows it exists to serve. Preserving the ambiguity keeps the text truthful while
the note makes the defect visible; nothing is lost except the illusion of resolution.

**Boundary.** Ambiguity that context does resolve must be resolved. A rule that reports every
theoretically available parse produces the false-positive flood that `000-design.md` §32 and
GPT's `OR-11` both warn about.

## 2. Quantities keep their surface form; unit conversion is off by default

**Decision.** Numbers, units, signs, percentages, range endpoints, and comparison operators are
reproduced exactly. Unit conversion, rounding, numeral-system changes (`3` ↔ `三`), and
percentage/ratio conversion are prohibited unless the caller explicitly authorizes them, and even
then only when the conversion is exact and the value does not sit inside a protected token.

Normalizing full-width digits to half-width outside protected tokens is permitted; it changes
typography, not value.

**Rejected: allow exact conversions freely.** GPT's `OR-09` argues, correctly, that
`等待 60000 ms` → `等待 60 s` is loss-free arithmetic. The argument fails on a different axis:
technical values are frequently copied into fields whose unit is fixed by the field name, and the
document usually does not say which values those are. The conversion is exact in arithmetic and
lossy in operation. The cost of the ban is a little verbosity; the cost of permitting it is a
defect class that deterministic checking cannot separate from a real error without a unit-binding
analysis the project does not have.

## 3. Protected tokens are recognised lexically, and the caller may adjust the set

**Decision.** Protected by default: code spans and code blocks, URLs, file and API paths,
command lines and flags, environment variables, status codes, version strings, and identifiers
carrying `_`, `-`, `.`, or internal capitalisation. The caller may add strings to the set or
release specific ones through `authorized_token_changes`.

Deterministic comparison covers **inventory**: the multiset of protected strings must be identical.
It deliberately does not cover **binding** — whether the right token is still attached to the right
action. Binding is a semantic judgment, because `发送 A 给 B` and `发送 B 给 A` have identical
inventories.

**Rejected: protect only what the caller marks.** Real documents do not mark their tokens, and the
failure mode is silent: `retry_after_ms` becoming `retryAfterMs` looks like a style fix.

**Rejected: extend deterministic checking to position.** Position is not preserved by legitimate
rewriting, so it would fail correct outputs.

## 4. Document structure carries semantic scope

**Decision.** Headings, list nesting, table cells, and warning blocks are part of meaning, not
presentation. A condition established by a heading or a parent list item governs its subtree. The
skill may not flatten a structure in a way that lets a condition escape its subtree or that narrows
a condition to fewer steps than it governed.

The skill also may not silently copy a structural condition into every child step; that produces
the repetitive, pseudo-legal text GPT's `OR-10` describes. The condition stays where it is and the
structure stays intact.

**Evidence.** GPT `F-14`: a `仅用于测试环境:` heading governing a `清空缓存` step, flattened into
prose, authorised cache clearing in production.

## 5. The skill's own normative vocabulary is fixed; a target document's is preserved

**Decision.** Two distinct vocabularies, and conflating them is a defect.

- **CTC's own instructions** use exactly `必须`, `应`, `可以`, `不得`, with the strengths defined in
  `000-design.md` §26. This is internal discipline.
- **A target document's modal words are preserved by class, not normalised.** `建议` stays a
  recommendation, `可以` stays a permission, `请确保` stays a request. CTC does not rewrite a
  document's modal vocabulary into its own.

When a source modal word is genuinely ambiguous in strength — `需要` can mark an obligation or a
statement of factual necessity — CTC reports the ambiguity rather than resolving it, per policy 1.

**Rejected: normalise target documents onto the fixed vocabulary.** It is superficially attractive
because it reduces cross-model variance. D001 finding 2 shows the cost: `请确保你已经配置了环境变量`
became `须完成环境变量配置`, which is better Chinese and a stronger requirement than the author
wrote. Strengthening an obligation is an editorial decision belonging to the author.

**Boundary.** When CTC authors new text (`task: author`) it uses the fixed vocabulary, because
there is no source modality to preserve.

## 6. A renderer's claim about its own output is not evidence

**Decision.** No self-assessment counts as a check. Semantic verification after rendering is an
independent pass with the source in hand, whether performed by a separate model in development or
by the explicit re-check step in the skill's own pipeline (`000-design.md` §27 step 7).

**Evidence.** D001: under an explicit instruction not to change meaning, with `meaning_delta: none`
declared on every entry, six entries changed meaning.

## Consequences

- Policies 1, 2, and 5 each remove a tempting "improvement" from the skill's repertoire. Rules
  implementing them need boundary examples showing where the restriction stops, or they will
  over-fire.
- Policy 2 makes the deterministic quantity check strict equality, which is why
  `tools/ctc_eval.py` compares `(value, unit)` multisets without normalisation.
- Policy 3 fixes the split between `ERROR`-level deterministic token checks and semantic binding
  checks in `002`.
- Policy 5 means the skill must describe its own normative vocabulary in a way that cannot be
  mistaken for a rule about target documents. This is a self-hosting hazard to check at release.

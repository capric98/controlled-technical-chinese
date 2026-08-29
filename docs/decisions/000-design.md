# 000 — Controlled Technical Chinese Skill Design

- **Status:** Accepted foundational design
- **Location:** `./docs/decisions/000-design.md`
- **Purpose:** Define the architecture, development protocol, evaluation logic, and governance for the Controlled Technical Chinese Agent Skill.
- **Runtime target:** A single self-contained `./SKILL.md`

## 1. Problem statement

The project aims to create an Agent Skill for controlled Chinese technical writing.

The target is not “good Chinese” in the general sense and not a Chinese translation of ASD-STE100. The target is a constrained technical language system that helps an agent write, rewrite, translate, and review Chinese technical content while minimizing semantic drift and operational ambiguity.

Primary use cases are:

- agent instructions and prompts;
- tool descriptions;
- SOPs;
- runbooks;
- troubleshooting procedures;
- warnings and error messages;
- API and developer documentation;
- technical translation into Chinese.

The central risk is that the same language model used to design a writing standard may reproduce its own hidden stylistic or reasoning weaknesses inside the standard. A second risk is that a “safer” or more formal standard may over-constrain Chinese and produce unnatural, repetitive, or needlessly defensive text.

This design addresses those risks through a trusted core, asymmetric multi-model review, explicit semantic invariants, adversarial evaluation, disagreement capture, and regression-constrained self-hosting.

## 2. Goals

CTC should:

1. Preserve factual meaning during rewriting and translation.
2. Preserve modality, conditions, exceptions, quantities, causality, and temporal relationships.
3. Reduce ambiguity involving actors, actions, objects, references, scope, logic, and procedure order.
4. Keep technical terminology consistent.
5. Protect machine-readable technical tokens.
6. Produce natural professional Chinese rather than translationese or pseudo-legal prose.
7. Support at least strict rewriting, standard technical writing, and review-only behavior.
8. Be usable by different capable language models without vendor-specific runtime dependencies.
9. Be small enough that the entire runtime skill can live in one `SKILL.md`.
10. Be testable and iteratively improvable without allowing the implementation to redefine its own success criteria.

## 3. Non-goals

The first implementation does not aim to:

- certify compliance with ASD-STE100;
- reproduce English grammar constraints in Chinese;
- become a complete Chinese typography or publishing standard;
- optimize marketing, branding, literary, or social-media copy;
- force every valid Chinese sentence into a single canonical wording;
- eliminate all model variance;
- formally prove natural-language equivalence;
- accumulate rules merely for completeness.

## 4. Foundational principle

The project uses this priority:

```text
truth and semantic invariants
        ↓
operational clarity
        ↓
terminology consistency
        ↓
natural technical Chinese
        ↓
project/editorial style
```

A lower layer may not override a higher layer.

A more natural sentence is not an improvement if it changes truth conditions. A more explicit sentence is not an improvement if it invents a requirement. A shorter sentence is not an improvement if it removes a condition or exception.

## 5. Runtime architecture

The release artifact is a single root-level `SKILL.md` conforming to the Agent Skills format.

The runtime skill should behave as a compact control plane, not as an encyclopedia. It should include only the rules, modes, examples, and checks required for reliable execution.

The default skill name is:

```text
controlled-technical-chinese
```

The skill must include valid YAML frontmatter with at least `name` and `description`.

The implementation should remain self-contained. `AGENTS.md` and `docs/decisions/` are development inputs and are not runtime dependencies of the released skill.

## 6. Runtime behavior

The initial design provides three modes.

### 6.1 Strict

Use for:

- agent instructions;
- tool descriptions;
- SOPs;
- runbooks;
- operational and safety-sensitive procedures;
- troubleshooting instructions.

Strict mode applies all semantic-safety rules and the strongest ambiguity controls. It should favor explicit actors, conditions, actions, and results where omission creates plausible ambiguity.

Strict does **not** mean maximal verbosity. It must still avoid needless repetition and artificial sentence fragmentation.

### 6.2 Standard

Use for:

- API documentation;
- README-style technical documentation;
- developer guides;
- FAQs;
- release notes;
- explanatory technical prose.

Standard mode preserves all semantic invariants but allows more idiomatic compression where interpretation remains stable.

### 6.3 Review

Review mode does not silently rewrite the entire input.

It should identify issues using a stable structure such as:

```text
Rule
Severity
Location
Problem
Risk
Suggested correction
```

Review mode is also the default mode for self-hosting review of `SKILL.md`.

## 7. Core rule taxonomy

The first release should keep the normative core small. A target of roughly 30 core rules is preferable to a large style catalog.

Rule families may use stable prefixes such as:

```text
S — semantic preservation
A — ambiguity and reference
P — procedures and action structure
T — terminology
L — logic, conditions, and temporal order
R — rendering and controlled style
```

Exact identifiers become stable once referenced by accepted decisions or evaluation cases.

### 7.1 Semantic preservation

The semantic core should cover at least:

- factual assertions versus uncertainty;
- possibility, certainty, permission, recommendation, obligation, and prohibition;
- conditions and prerequisites;
- exceptions and scope;
- causal strength;
- quantities and thresholds;
- time and ordering;
- actor/action/object relationships;
- protected technical tokens.

These are higher priority than stylistic preferences.

### 7.2 Ambiguity control

Chinese-specific ambiguity rules should focus on actual interpretation risk rather than mechanically importing English constraints.

Candidate areas include:

- omitted actor when multiple actors are plausible;
- ambiguous pronouns or demonstratives;
- unclear modifier scope;
- unclear negation scope;
- unclear coordination;
- implicit logical relationships;
- ambiguous temporal ordering.

Rules should not require an explicit subject in every sentence.

### 7.3 Procedure control

Procedure rules should prefer a structure conceptually equivalent to:

```text
[condition] + [actor] + [action] + [object] + [result]
```

Not every element must appear in every sentence. Elements become explicit when omission creates operational ambiguity.

“One step, one main operational goal” is preferred to the naive rule “one sentence, one verb.”

### 7.4 Terminology

The same concept should normally use the same preferred technical term within a document or project.

Terminology control must distinguish true synonyms from distinct domain concepts.

The core skill should not ship an arbitrary large product glossary. Product-specific terminology belongs to the invoking context unless a future design decision introduces a portable glossary mechanism.

### 7.5 Style and locale

Typography, quotation marks, spacing conventions, second-person voice, and brand naming are lower-priority concerns.

Do not elevate a locale or house-style preference into a semantic rule unless it affects interpretation.

## 8. Trusted core

The project uses a small trusted core rather than trusting the skill to validate itself.

The trusted core consists conceptually of:

1. accepted normative semantics;
2. human-reviewed or otherwise grounded evaluation cases;
3. protected semantic invariants;
4. accepted decision records;
5. release gates.

The implementation may critique the trusted core, but it may not silently redefine it.

A test failure must not be “fixed” by changing the expected outcome unless the expectation itself is reviewed and a decision records why it was wrong.

## 9. Canonical semantics and rendered prose

Normative intent and its Chinese wording are separate concerns.

During development, a rule should be representable in a structured form such as:

```yaml
id: CTC-S002
level: MUST
concept: modality-preservation
scope:
  - rewrite
  - translation
invariant:
  modality_strength: unchanged
prohibited:
  - possibility_to_certainty
  - recommendation_to_requirement
examples:
  invalid:
    - source: 请求可能失败。
      output: 请求会失败。
```

This structured representation is a development technique, not necessarily a permanent runtime file.

The final `SKILL.md` renders the same semantics into concise Chinese instructions.

A language editor may improve the rendering but may not change the canonical semantic intent without a separate rule-change review.

## 10. Rule schema

Every important normative rule should be answerable in terms of:

- **ID** — stable identifier;
- **level** — MUST, SHOULD, or MAY-equivalent;
- **scope** — when the rule applies;
- **trigger** — what condition activates it;
- **requirement** — what must or should happen;
- **prohibition** — transformations that are not allowed;
- **exceptions** — explicit limits, if any;
- **invariant** — semantic property that must remain stable;
- **positive example** — desired behavior;
- **negative example** — clear failure;
- **boundary example** — where an apparently similar case should not trigger the rule;
- **detection mode** — deterministic, semantic, or mixed.

Not every item needs to appear verbatim in `SKILL.md`, but the project should be able to reconstruct them for core rules.

## 11. Multi-model development architecture

The project intentionally uses models asymmetrically.

The initial role hypothesis is based on observed tendencies, not assumed ground truth.

### 11.1 Claude Opus — Specification Compiler

Primary responsibilities:

- interpret human design intent;
- convert prose requirements into scoped rules;
- identify instruction hierarchy and applicability;
- check whether a proposed implementation follows stated instructions;
- reverse-decode rendered rules into their implied semantics.

Claude should not unilaterally decide the final Chinese style or approve its own specification changes.

### 11.2 GPT-5.6 Sol — Formalizer and Adversarial Auditor

Primary responsibilities:

- define semantic invariants;
- find contradictions and hidden assumptions;
- generate counterexamples and mutation cases;
- test rule boundaries;
- challenge causality, modality, quantifier, condition, and scope changes;
- detect gaps between intended and rendered semantics.

A known risk is defensive over-engineering. Therefore GPT may not introduce a new hard constraint without a demonstrated failing case, evidence that an existing rule is insufficient, and a boundary example.

### 11.3 Gemini 3.7 Flash — Chinese Renderer and Naturalness Auditor

Primary responsibilities:

- render accepted semantics as concise, professional Chinese;
- reduce translationese and unnecessary formality;
- identify awkward fragmentation and repetition;
- detect over-editing;
- improve examples without altering their intended semantics.

Gemini may not weaken or strengthen normative levels, remove conditions, change causality, or modify other semantic invariants merely to improve fluency.

### 11.4 Role evaluation

These roles are provisional.

The project should periodically compare models on at least:

- semantic preservation;
- modality preservation;
- ambiguity detection;
- instruction following;
- Chinese naturalness;
- resistance to over-editing.

If evidence shows a different allocation is more reliable, record a decision and update this document.

## 12. Independence before discussion

Independent judgment has more diagnostic value than immediate model discussion.

For a contested item:

1. Give each relevant reviewer the same frozen artifact and role-specific task.
2. Record each initial judgment.
3. Compare the judgments programmatically or manually.
4. Classify the disagreement.
5. Only then, if useful, expose critiques for rebuttal or synthesis.

Do not allow early cross-model discussion to erase the original disagreement.

Consensus after persuasion is not ground truth.

## 13. Typed disagreement

Do not resolve conflicts by simple majority vote.

Classify the disagreement first.

Examples:

| Disagreement | Preferred authority |
|---|---|
| Exact number/token changed | Deterministic comparison |
| Modality/condition/causality changed | Semantic evaluator + accepted rule |
| Rule scope misunderstood | Specification/instruction evaluator |
| Chinese is awkward but semantically correct | Naturalness evaluator |
| Proposed wording is natural but semantically lossy | Semantic invariant wins |
| Core rule itself should change | Decision process / human gate |

The project should preserve high-value disagreements because they reveal ambiguous rules and difficult evaluation cases.

## 14. Semantic reverse-decoding

A central anti-ambiguity test is round-trip semantic decoding.

Given a rendered rule in Chinese, independent reviewers should reconstruct:

```text
level
scope
trigger
required behavior
prohibited behavior
exceptions
semantic invariant
```

Compare the reconstructed structure with the intended structure.

If competent independent reviewers infer materially different semantics, the wording is not sufficiently controlled even if it sounds fluent.

This mechanism is especially important when Gemini or another language-focused model rewrites normative prose.

## 15. Self-hosting

CTC should review its own `SKILL.md`.

Self-hosting is a release diagnostic, not a source of truth.

The sequence is:

```text
current trusted criteria
        ↓
candidate SKILL.md
        ↓
CTC review-only pass
        ↓
independent adversarial review
        ↓
evaluation / regression
        ↓
accept, reject, or revise
```

The skill must not automatically edit the trusted criteria or gold expectations after detecting a conflict.

A self-review finding should identify:

- exact text;
- implicated rule;
- reason the text may violate or ambiguously express the rule;
- risk;
- proposed correction;
- expected evaluation impact.

## 16. Mutation testing

The project should deliberately introduce defects into rules or examples to test whether reviewers can detect them.

Useful mutations include:

- changing `可能` to `会`;
- changing `建议` to `必须`;
- deleting a prerequisite;
- weakening or strengthening a prohibition;
- removing an actor when two actors remain plausible;
- swapping temporal order;
- replacing a preferred term with a near-synonym;
- altering a number, threshold, command, field name, or API token;
- inserting an unsupported causal claim;
- adding an unjustified “通常” or “最常见原因”.

If a reviewer repeatedly misses a mutation class, do not rely on that reviewer alone for that class.

## 17. Evaluation system

Evaluation should measure behavior, not merely whether files parse.

At minimum, track the following dimensions.

### 17.1 Semantic preservation

Did the transformation change facts, certainty, requirements, conditions, quantities, causality, or exceptions?

This is the highest-priority model-judged metric.

### 17.2 Protected-token preservation

Did code, commands, identifiers, API paths, field names, URLs, status codes, or numerical values change unexpectedly?

Use deterministic comparison whenever possible.

### 17.3 Ambiguity reduction

Did the output eliminate a demonstrated ambiguity without inventing facts?

Do not reward unnecessary explicitness where the original is already unambiguous.

### 17.4 Procedure correctness

Are actor, action, object, condition, order, and expected result operationally clear?

Check that splitting or reordering steps does not change behavior.

### 17.5 Terminology consistency

Does a concept keep the intended preferred term?

Check for false normalization where distinct concepts are incorrectly collapsed.

### 17.6 Naturalness

Does the output read like professional Chinese technical writing?

Penalize:

- translationese;
- repetitive explicit subjects with no disambiguation value;
- pseudo-legal phrasing;
- unnecessary passive constructions;
- atomized one-clause-per-line prose when normal syntax is clearer.

### 17.7 Over-editing

Did the skill change text that was already correct, clear, and compliant?

A mature controlled-language system should know when not to rewrite.

### 17.8 Instruction following

Did the model respect requested mode, scope, protected regions, and output format?

## 18. Seed model profiling

Before relying heavily on role specialization, use a common seed set of roughly 40–60 cases spanning:

- factual preservation;
- modality;
- conditions;
- ambiguous actor;
- ambiguous pronoun;
- negation scope;
- temporal order;
- procedure structure;
- technical tokens;
- terminology;
- naturalness;
- over-editing.

Evaluate candidate models independently.

The purpose is not to produce a single overall score. The purpose is to identify which model is reliable for which class of judgment.

Model profiles are empirical project data and may change with model versions.

## 19. Disagreement corpus

High-value model disagreements should become persistent project knowledge.

A disagreement is worth recording when:

- it exposes two plausible interpretations of a rule;
- it reveals a difference between semantic correctness and naturalness;
- it exposes model-specific over-editing;
- it demonstrates an unstable boundary;
- resolving it causes a normative change.

Resolved disagreements should be summarized in `./docs/decisions/` when the rationale may matter later.

Do not preserve every trivial wording preference.

## 20. Rule admission and anti-overengineering gate

A new hard rule is expensive because it constrains every future invocation.

No new `MUST` should be accepted without:

1. a concrete failing input;
2. a concrete bad output or ambiguity;
3. an explanation of risk;
4. evidence that the existing rule set does not already cover the failure;
5. a test or review criterion that distinguishes bad from good behavior;
6. a boundary example where the rule should not apply.

A proposal that merely says “this would be safer” is insufficient.

Prefer:

```text
existing rule clarification
    over
new SHOULD
    over
new MUST
```

when all three can solve the demonstrated problem.

## 21. Evaluation cases and ground truth

Model-generated evaluation cases are useful but are not automatically gold.

A strong gold case should specify, as applicable:

```text
source
task/mode
semantic invariants
valid transformation
invalid transformation
reason
protected tokens
expected issue classification
```

Core gold cases should be human-reviewed or supported by unambiguous accepted semantics.

The implementation may propose changes to a gold case. It may not silently alter the expected result to make a candidate skill pass.

## 22. Regression policy

Every accepted normative bug fix should leave behind a regression case.

For a change:

```text
observed failure
    ↓
failing case
    ↓
minimal rule or wording change
    ↓
case passes
    ↓
full regression review
```

A local improvement is not accepted if it causes a higher-priority semantic regression elsewhere.

## 23. Cross-model variance

The project does not require identical wording from different models.

It should, however, reduce **semantic variance**.

For the same compliant input, different capable models may choose different natural phrasing, but they should converge on:

- the same facts;
- the same actors and actions;
- the same modality;
- the same conditions and exceptions;
- the same quantities;
- the same causal claims;
- the same protected technical tokens.

High semantic variance indicates either a weak rule, an ambiguous input, or an unreliable model behavior worth investigating.

## 24. Deterministic versus semantic validation

Use deterministic validation for properties such as:

- exact numbers;
- units and ranges when parseable;
- protected tokens;
- code spans and blocks;
- URLs;
- commands;
- API identifiers;
- status codes;
- frontmatter syntax;
- stable rule IDs.

Use model judgment for:

- whether an omitted actor is ambiguous;
- whether a pronoun has multiple plausible antecedents;
- whether procedure decomposition preserves operational meaning;
- whether naturalness has degraded;
- whether a rewrite added an unsupported implication.

Do not replace one category with the other merely for implementation convenience.

## 25. `SKILL.md` drafting strategy

The skill should be written primarily in Chinese because Chinese is both the controlled target language and the language whose ambiguity the skill must manage.

Use concise English technical terms when they are standard or less ambiguous.

A candidate structure is:

```text
YAML frontmatter
Purpose and triggers
Priority rules
Modes
Semantic invariants
Controlled-Chinese rules
Procedure rules
Terminology rules
Protected content
Rewrite workflow
Review workflow
Self-check
Compact examples
```

Avoid a long general style guide.

The skill should tell the model what to do, when to do it, what not to change, and how to verify the result.

## 26. Normative language

Normative words must have stable strength.

Suggested interpretation:

- **必须** — violating the rule is a correctness failure.
- **应** — default expectation; may be overridden by a documented boundary or higher-priority consideration.
- **可以** — permitted behavior, not a requirement.

Avoid ambiguous terms such as:

- 尽量;
- 适当;
- 必要时;
- 一般来说;

unless the trigger or decision criterion is immediately defined.

The purpose is not to ban ordinary Chinese qualifiers in target documents. The restriction applies to normative skill instructions where ambiguity would alter behavior.

## 27. Protected semantics before rendering

A rewrite pipeline should conceptually follow:

```text
1. Identify protected tokens and semantic invariants.
2. Identify actors, actions, objects, conditions, exceptions, and order.
3. Identify demonstrated ambiguity or terminology issues.
4. Rewrite only what is necessary.
5. Compare the candidate with the protected semantics.
6. Apply natural Chinese rendering.
7. Re-check semantics after rendering.
8. Return the result or review findings.
```

Style is intentionally late in the pipeline.

## 28. Review severity

The skill may use a small severity vocabulary.

Suggested semantics:

- **ERROR** — semantic corruption, unsafe ambiguity, protected-token mutation, or violation of a hard invariant.
- **WARNING** — plausible ambiguity or rule risk requiring review.
- **STYLE** — non-semantic naturalness or consistency issue.

Do not classify a mere style preference as ERROR.

## 29. Decision records

`./docs/decisions/` is the project's long-term memory for agents.

Create a decision record when future contributors may reasonably ask:

- Why does this rule exist?
- Why is this a MUST rather than a SHOULD?
- Why was a simpler rule rejected?
- Why does the skill allow this exception?
- Why are model roles assigned this way?
- Why was an evaluation criterion changed?
- Why is a specific design constraint present?

Decision records should preserve rationale rather than only the final wording.

The foundational architecture belongs here in `000-design.md`.

Update this file if the architecture itself changes, including:

- runtime artifact structure;
- trusted-core boundaries;
- multi-model governance;
- role assignment policy;
- self-hosting authority;
- release-gate philosophy;
- evaluation dimensions.

For narrower choices, create a new numbered decision record instead.

## 30. Release gates

A candidate `SKILL.md` should not be considered ready until all applicable gates pass.

### Format gate

- valid YAML frontmatter;
- valid `name`;
- non-empty and trigger-specific `description`;
- valid Agent Skills structure;
- no accidental dependency on development-only files.

If available:

```text
skills-ref validate .
```

Reference: <https://agentskills.io/specification>

### Semantic gate

- no known fact drift in core cases;
- no known modality strengthening or weakening;
- no known condition or exception loss;
- no known unsupported causal claim;
- no protected-token regressions.

### Ambiguity gate

- known high-severity actor, reference, scope, and procedure ambiguities are handled;
- the skill does not enforce unnecessary explicitness on already clear text.

### Naturalness gate

- language-focused review finds no systematic translationese or pseudo-legal style;
- improvements do not weaken semantic controls.

### Self-hosting gate

- `SKILL.md` can review itself in review-only mode;
- self-review findings are independently checked;
- no unresolved high-severity contradiction or undefined normative scope remains.

### Cross-model gate

When multiple models are available:

- run the same core cases across them;
- inspect semantic disagreements;
- do not release merely because a majority passes.

## 31. Iteration loop

The intended iteration cycle is:

```text
human intent or observed failure
          ↓
specification proposal
          ↓
formalization + counterexamples
          ↓
Chinese rendering
          ↓
independent semantic reverse-decoding
          ↓
deterministic checks
          ↓
gold / mutation / regression evaluation
          ↓
disagreement analysis
          ↓
human or accepted-decision gate
          ↓
minimal patch
          ↓
full regression
          ↓
self-hosting review
          ↓
release candidate
```

The loop is finite and evidence-driven.

Do not iterate merely until reviewers stop complaining.

## 32. Success criteria

The project succeeds when it produces a compact, portable `SKILL.md` that measurably improves Chinese technical-writing reliability across capable models.

The desired outcome is:

- very high semantic preservation;
- exact preservation of protected technical content;
- lower consequential ambiguity;
- consistent terminology;
- low false-positive rate;
- low over-editing rate;
- professional natural Chinese;
- lower semantic variance across models.

The objective is **not** to make all outputs identical.

## 33. Core doctrine

The project should preserve these statements unless a later accepted decision explicitly changes them:

> The implementation may review the specification, but it may not redefine the specification merely to make itself pass.

> Model disagreement is diagnostic data, not noise to be averaged away.

> A normative rule must earn its complexity through a demonstrated failure.

> Naturalness may change wording; it may not change meaning.

> The best controlled-language rule is the smallest rule that reliably prevents a real class of failure.

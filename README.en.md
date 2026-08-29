# Controlled Technical Chinese (CTC)

> [中文版](./README.md)

An Agent Skill for writing, rewriting, translating, and reviewing Chinese technical content with
semantic fidelity, low ambiguity, consistent terminology, and controlled procedural language.

CTC is not "good Chinese" in the general sense, and it is not a Chinese translation of ASD-STE100.
It is a constrained technical language system for text where a misreading costs something: agent
instructions, tool descriptions, SOPs, runbooks, troubleshooting steps, warnings and error
messages, API documentation, and technical translation into Chinese.

The runtime deliverable is a single self-contained file: [`SKILL.md`](./SKILL.md).

## What it does

CTC follows one priority order, and a lower layer may never override a higher one:

```text
truth and semantic invariants → operational clarity → terminology consistency
→ natural technical Chinese → project style
```

Three tie-breaks make that operational:

- A more natural sentence is not an improvement if it changes truth conditions.
- A more explicit sentence is not an improvement if it invents a requirement.
- A shorter sentence is not an improvement if it drops a condition or an exception.

It runs in three modes. **strict** for agent instructions, SOPs, runbooks, and safety-sensitive
procedures. **standard** for API docs, guides, and explanatory prose. **review** for auditing
existing text, which reports findings and rewrites nothing. Modes change the ambiguity threshold,
not the strength of any rule.

Twenty-nine rules across six families — semantics, ambiguity, procedure, terminology, logic, and
rendering — sit under one that governs the rest: **every edit must be attributable to a rule, and
text that triggers no rule is returned unchanged.**

## What it deliberately does not do

A controlled-language spec is easy to make worse by making it stricter. CTC refuses a specific list
of tempting constraints, each because it damages Chinese without buying precision:

- it does not require an explicit subject in every sentence — topic-chain subject omission is normal
  and preferred in Chinese;
- it does not enforce "one sentence, one verb", which shatters serial-verb constructions;
- it does not ban the passive, which is natural when the patient is the focus;
- it does not force connectives between adjacent steps, which turns sequence into causation;
- it does not convert units, even when the arithmetic is exact;
- it does not unify near-synonyms that denote different concepts;
- it does not resolve a genuine ambiguity by picking a reading — it reports it and stops.

The last one is the sharpest. When the source is ambiguous and context cannot settle it, CTC keeps
the original wording and appends a `待确认` list naming the competing readings and the information
that would resolve them. Choosing for the author manufactures a fact.

## Using it

Copy `SKILL.md` into your agent's skills directory, or package it for installation:

```bash
bash tools/package.sh      # writes dist/controlled-technical-chinese/ and validates it
```

The skill is self-contained and model-agnostic. It has no runtime dependency on anything else in
this repository.

## How it was built

The central risk in this project is that a model designing a writing standard reproduces its own
blind spots inside the standard. The development protocol is built around that risk.

Three models work in asymmetric roles — Claude Opus compiles the specification, GPT-5.6 Sol
formalizes invariants and attacks them, Gemini 3.7 Flash renders and audits the Chinese — and each
produces its first pass **independently**, before seeing any other model's work. Disagreements are
classified by type and resolved by the appropriate authority, never by majority vote. The ones worth
keeping live in [`eval/disagreements/`](./eval/disagreements/).

That protocol earned its keep immediately. In round one, the naturalness auditor was asked to
catalogue Chinese writing failures under an explicit instruction not to change meaning, and declared
`meaning_delta: none` on every entry. Independent review found six entries that changed modality,
deleted an actor, converted a description into a prohibition, or generalized a quantity
([D001](./eval/disagreements/D001-naturalness-vs-modality.md)). That is why `SKILL.md` states that a
model's own assessment of whether it preserved meaning is not admissible evidence, and why semantic
verification is a separate pass with the source in hand.

### Development layout

```text
SKILL.md              the runtime artifact — the only released file
docs/decisions/       why each choice was made; 000 is the foundational design
spec/                 canonical rule semantics in structured form, and the frozen rule IDs
eval/gold/            56 gold cases across the twelve failure categories
eval/mutations/       generated single-defect mutants for per-class detection rates
eval/disagreements/   typed cross-model disagreements kept as project memory
tools/                deterministic checkers and the evaluation harness
dev/                  role prompts, and raw independent model output kept as evidence
```

### Running the checks

```bash
python3 tools/check_skill.py                          # format and rule-ID gates
bash tools/package.sh                                 # + skills-ref validation
uv run tools/ctc_eval.py run --model claude --run-id r1
uv run tools/ctc_eval.py bundle --run-id r1
uv run tools/ctc_eval.py judge  --run-id r1 --judge gpt --exclude-self
uv run tools/mutate.py --from eval/gold --out eval/mutations/generated.yaml
```

Deterministic properties — protected tokens, quantities, threshold boundaries — are checked in code.
Whether an omitted actor is ambiguous, or whether a rewrite added an unsupported implication, is
judged by a model that did not produce the output.

About one case in three is an **over-edit trap**: the source is already correct, and any rewrite is
the failure. Without them an evaluation quietly rewards maximal explicitness, which is the failure
mode this project exists to prevent.

## Status

`SKILL.md` passes the format, semantic, ambiguity, naturalness, and self-hosting gates. Across 147
outputs from three models there were no deterministic failures, semantic pass rates were 80–88%,
and a mutation corpus of 45 single-defect mutants was detected 45/45. Full assessment in
[`eval/reports/release-gates.md`](./eval/reports/release-gates.md).

It is **not** a validated release. The gold corpus is agent-reviewed and cross-audited between two
models but **not human-reviewed**, and every other gate is measured against that corpus — so a gate
measured against unreviewed expectations reports the expectations, not the artifact. That is the
blocking item. Three narrower gaps are recorded alongside it: GPT's outputs went unjudged for want
of a fourth model, one model's sweep covered 35 of 56 cases, and the reverse-decoding pass was
Claude reading Claude-rendered prose.

Contributor guidance is in [`AGENTS.md`](./AGENTS.md). New hard rules must clear the admission gate
in [`docs/decisions/000-design.md`](./docs/decisions/000-design.md) §20: a concrete failing input, a
concrete bad output, the risk, evidence that existing rules do not cover it, a test that
distinguishes good from bad, and a boundary example where the rule must not fire. "This would be
safer" is not sufficient.

## License

[MIT](./LICENSE)

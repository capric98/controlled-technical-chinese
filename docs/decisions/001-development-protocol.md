# 001 — Development artifact layout and multi-model invocation protocol

- **Status:** Accepted
- **Date:** 2026-08-28
- **Supersedes:** none
- **Relates to:** `000-design.md` §5, §11, §12, §18, §19, §21, §30

## Context

`000-design.md` fixes the runtime artifact (a single root `SKILL.md`) and the governance model
(asymmetric multi-model development, independence before discussion, typed disagreement, gold
cases as trusted core). It deliberately does not fix:

- where development-time artifacts live in the repository;
- how the three models are actually invoked so a later agent can reproduce a judgment;
- which artifacts are project memory and which are disposable run output.

Without those fixed, every iteration re-invents its own file layout, and recorded judgments
cannot be reproduced or attributed to a specific model configuration.

## Decision

### Repository layout

```text
SKILL.md                 runtime artifact — the only released file
AGENTS.md                repository instructions (development input)
docs/decisions/          long-term rationale; NNN-<slug>.md
spec/                    canonical semantics (structured, development-only)
eval/gold/               human-reviewed or accepted gold cases (trusted core)
eval/mutations/          deliberate defect cases for reviewer testing
eval/disagreements/      typed cross-model disagreements kept as project memory
eval/reports/            committed evaluation summaries, not raw transcripts
dev/prompts/             the exact role prompts given to each model
dev/inbox/               raw independent model outputs, kept as evidence
tools/                   deterministic checkers and the evaluation harness
```

`SKILL.md` must not reference or depend on any of these paths.

`dev/inbox/` is evidence, not authority. A file there is one model's independent opinion at one
point in time. Nothing in `dev/inbox/` may be cited as a project decision.

### Model invocation protocol

Roles follow `000-design.md` §11. The reproducible invocations are:

```bash
# Claude Opus — specification compiler, instruction-following reviewer
#   invoked as a subagent of the orchestrating Claude Code session, or:
claude -p "<role prompt>"

# GPT-5.6 Sol — formalizer, semantic-invariant reviewer, adversarial critic
codex exec -m gpt-5.6-sol -c model_reasoning_effort=xhigh -s read-only \
  -C "$PWD" -o dev/inbox/<name>.yaml "$(cat dev/prompts/<name>.md)"

# Gemini 3.7 Flash — Chinese renderer, naturalness and over-editing auditor
agy -p "$(cat dev/prompts/<name>.md)" --model gemini-3.7-flash-high \
  --print-timeout 25m > dev/inbox/<name>.yaml
```

Record the model string and reasoning effort with any judgment that is kept. A judgment whose
model configuration is unknown is not reusable evidence.

`codex` runs under its `read-only` sandbox and writes only through `-o`. `agy` runs in print mode
with no write permission and is given its context inline. Neither model may edit repository files
directly; the orchestrator applies all changes. This keeps `000-design.md` §11's rule that no
single model both proposes a normative change and applies it.

### Independence protocol

For any contested item, and for every first-pass artifact:

1. Freeze the input.
2. Give each model its own role prompt in `dev/prompts/`, with no other model's output attached.
3. Store each raw result in `dev/inbox/` before any comparison.
4. Compare and classify the disagreement (`000-design.md` §13) before any cross-model rebuttal.

Cross-exposure is permitted only after step 3 has been recorded.

### Format gate

`npx skills-ref validate .` is available and is the format gate. `tools/` additionally carries the
project-specific deterministic checks that `skills-ref` does not cover (rule-ID stability,
protected-token comparison, line budget).

## Alternatives considered

- **Keep everything in `docs/`.** Rejected: it conflates rationale (stable, human-facing) with
  evidence and raw model output (volatile, machine-facing), which makes the decision record
  directory unreadable as project memory.
- **Discard raw model output after synthesis.** Rejected: `000-design.md` §19 requires a
  disagreement corpus, and a disagreement cannot be re-examined once the original independent
  judgments are gone.
- **Let each model write into the repository directly.** Rejected: it breaks the rule that a model
  may not both propose and approve a normative change, and it destroys the frozen-input property
  that independence depends on.

## Consequences

- Reproducing a past judgment requires only the prompt file, the model string, and the effort level.
- `dev/inbox/` grows over time. Prune it when a file's content has been fully absorbed into `spec/`,
  `eval/`, or a decision record, and the disagreement it recorded is closed.
- The orchestrator becomes a required component: no model can unilaterally change the repository.

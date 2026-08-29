# 002 — Gold case schema and the evaluation contract

- **Status:** Accepted
- **Date:** 2026-08-28
- **Relates to:** `000-design.md` §17, §21, §22, §24; `001-development-protocol.md`

## Context

`000-design.md` §21 lists what a strong gold case should specify but does not fix a machine-readable
shape, and §24 requires deterministic and semantic validation to stay separate. Without a fixed
schema the trusted core cannot be executed, and "the case passed" degrades into an opinion.

A second problem is authority. Model-generated cases are useful but are not gold (§21). The schema
therefore has to carry provenance, so that a later agent can tell a reviewed case from a proposal.

## Decision

### Case shape

Gold cases live in `eval/gold/*.yaml`. Each file holds a `cases:` list. Fields:

```yaml
cases:
  - id: G-L-003                 # G-<family>-<seq>; stable once referenced
    category: threshold-boundary
    task: rewrite               # rewrite | translate | review | author
    mode: strict                # strict | standard | review
    source: |                   # the input text, verbatim
      当队列长度达到 100 时拒绝新任务。
    instruction:                # optional; omit to use the task default
    invariants:                 # what must survive; each is judgeable on its own
      - kind: threshold         # see the approved kind vocabulary below
        detail: |
          「达到 100」包含 100 本身，不得改写为「超过 100」。
    protected_tokens: []        # strings that must appear unchanged in the output
    authorized_token_changes: []   # tokens the task explicitly permits changing
    invalid_transformations:
      - output: 当队列长度超过 100 时拒绝新任务。
        violated: [threshold]
        reason: 队列长度恰为 100 时的行为被改变。
    expected_issues:            # review mode only: what a correct review must report
      - rule: CTC-L004
        severity: ERROR
        locus: 达到 100
    over_edit_trap: false       # true when the source is already compliant
    provenance: human-reviewed  # human-reviewed | derived-from-<record> |
                                # orchestrator-reviewed | model-proposed-unreviewed |
                                # generated-mutation
    notes:
```

### Approved `kind` vocabulary

```text
fact  modality  condition  quantifier  negation  scope  causality  order
reference  actor  threshold  token  procedure  terminology  instruction
rendering  over-edit
```

A `violated` entry must reference a kind the same case declares in its own `invariants`. An
audit of the first corpus found four cases citing kinds their own case never declared, which
makes the entry unfalsifiable.

`expected_issues` entries use `rule:` once rule IDs are frozen and `category:` before then. The
first corpus was authored before the rule set existed, so it uses `category:` throughout; binding
those to rule IDs is a separate reviewed pass.

### What the candidate model actually sees

Only `source` and `instruction` reach the candidate. `invariants`, `invalid_transformations`,
`expected_issues`, `notes`, and `protected_tokens` are grading material and are never included in
the prompt `tools/ctc_eval.py` builds. This matters because case authors write `notes` that state
the expected restraint outright; that is harmless as grading material and would be fatal as input.

`valid_transformations` is deliberately **not** part of the pass condition. Listing one acceptable
output invites a later agent to score by string similarity, which would contradict `000-design.md`
§23: the project reduces semantic variance, not wording variance. A case passes when every
`invariant` survives and no `invalid_transformations` entry is reproduced.

### Two-layer validation

`tools/ctc_eval.py` performs the deterministic layer in code: protected-token multiset equality,
quantity `(value, unit)` multiset equality, threshold-comparator drift, and a modal-strength
profile diff. Token and quantity mismatches are `ERROR`. Comparator and modality diffs are
`WARNING` — they are strong signals but a legitimate rewrite can change the surface form, so the
verdict belongs to the semantic layer.

The semantic layer runs as a separate model pass over a bundle produced by `ctc_eval.py bundle`.
The judge sees source, output, and the case's invariants; it never sees the candidate's own
account of what it did. `eval/disagreements/D001` is the evidence for that separation: a model
asserting "meaning unchanged" about its own output was wrong six times in one pass.

### Provenance and the no-silent-edit rule

`provenance: model-proposed-unreviewed` and `generated-mutation` cases may be run and reported but
may not gate a release. `orchestrator-reviewed` means an agent checked the case against accepted
semantics and against an independent audit by a second model; it is stronger than
model-proposed and weaker than `human-reviewed`. Promotion to `human-reviewed` is a separate,
recorded act, and the gold core is not human-reviewed until a person performs it — that gap is a
known outstanding release gate, not an oversight.

When a candidate `SKILL.md` fails a case, the permitted responses are: fix the skill, or open a
decision record arguing the case is wrong. Editing `invariants`, `invalid_transformations`, or
`expected_issues` so that a failing candidate passes is prohibited (`000-design.md` §8, §21).

### Over-edit traps are first-class

At least one case in five carries `over_edit_trap: true`: the source is already correct, clear, and
compliant, and any rewrite is a failure. Without them the evaluation rewards maximal explicitness,
which is the failure mode `000-design.md` §17.7 and §32 exist to prevent.

## Alternatives considered

- **Score against a reference output.** Rejected: penalises legitimate wording variance and would
  push the skill toward a single canonical phrasing, an explicit non-goal (§3).
- **One monolithic case file.** Rejected: cases are grouped by family so that a regression can be
  run narrowly, and so that adding a case does not conflict with concurrent work.
- **Let the candidate self-report invariant preservation.** Rejected on direct evidence, D001.

## Consequences

- The trusted core becomes executable: `uv run tools/ctc_eval.py run --model <m>` is reproducible.
- Every accepted normative fix must leave a case behind (§22), so `eval/gold/` grows monotonically.
- Judge prompts must be versioned alongside the schema; a changed judge prompt invalidates
  comparison with earlier runs.

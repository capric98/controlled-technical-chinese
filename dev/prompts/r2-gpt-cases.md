You are the **Formalizer and Adversarial Auditor** for the Controlled Technical Chinese (CTC) project.

Read these files before writing anything:

- `./docs/decisions/002-gold-case-schema.md` — the exact case schema you must emit
- `./docs/decisions/000-design.md` §17, §18, §21, §22 — what evaluation must measure
- `./dev/inbox/r1-gpt-invariants.yaml` — your own round-1 invariants and failure taxonomy
- `./eval/disagreements/D001-naturalness-vs-modality.md` — six observed real failures

## Task

Author **24 gold evaluation cases** in your assigned areas. Emit **YAML only** — no prose, no
markdown fences — conforming to the `cases:` schema in decision 002.

Your assigned coverage, roughly two cases each:

1. modality strengthening (建议 → 必须)
2. modality weakening (必须 → 建议 / 可以)
3. epistemic status collapse (可能/推测 → 确定事实)
4. condition deletion (仅当 / 除非 / 连续 N 次)
5. condition broadening (a gate becomes unconditional)
6. exception / exclusion set deletion (除…外)
7. quantifier scope drift (所有 / 部分 / 至少一个)
8. negation scope (不得同时 vs 均不得)
9. threshold boundary flip (达到 vs 超过, 以上 vs 以内)
10. number, unit, retry-count, and duration drift
11. protected-token mutation (API path, field name, flag, env var, status code)
12. correlation upgraded to causation
13. temporal order inversion / unsafe parallelisation
14. unsourced qualifier injection (通常 / 默认 / 最常见 / 只需)

## Hard requirements

- `provenance: model-proposed-unreviewed` on every case.
- `id` format `G-S-001`, `G-L-001`, `G-T-001` — use family `S` for semantic preservation, `L` for
  logic/condition/order/quantifier/negation, `T` for tokens/terminology.
- `source` must be realistic technical Chinese: runbook steps, API docs, error messages, agent
  instructions, tool descriptions. Several sources should be multi-sentence with real structure
  (numbered steps, a warning block, a parameter table row).
- Each `invariants[].detail` must be **judgeable by an independent reviewer who cannot see your
  reasoning**. Write the check, not the intention. Bad: 「保持语义」. Good:
  「源文的『仅当连续失败 3 次』是必要触发条件；输出若允许单次失败即切换，判为失败」.
- Each case needs at least one `invalid_transformations` entry: the concrete bad output, the
  `violated` kinds, and why it is wrong.
- **At least 5 of your 24 cases must be `over_edit_trap: true`** — the source is already correct
  and precise, and the tempting "safer" rewrite is the failure. Put the tempting rewrite in
  `invalid_transformations`. This is the anti-over-engineering control from `000-design.md` §17.7
  and your own `overreach_risks` list; without it the evaluation rewards maximal explicitness.
- **At least 4 cases must use `task: review` and `mode: review`**, with `expected_issues` entries.
  Use a `category:` key inside each expected issue instead of a `rule:` key — rule IDs are not
  frozen yet and you must not invent them.
- **At least 3 cases must be `task: translate`** with an English `source`, testing whether the
  Chinese output preserves modality, condition, and quantifier structure.
- Fill `protected_tokens` wherever the case depends on exact strings.
- Do not author cases outside your assigned areas; naturalness, actor ambiguity, pronoun
  reference, and procedure structure are being authored independently by other reviewers.
- Do not modify any repository file.

A case is only useful if a competent model could plausibly fail it. Do not write cases whose
correct answer is obvious from the source alone.

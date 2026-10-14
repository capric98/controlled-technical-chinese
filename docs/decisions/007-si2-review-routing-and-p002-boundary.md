# 007 — si2: route undecidable review findings to CTC-A005, and bound CTC-P002 to real gaps

- **Status:** Accepted by the maintainer on 2026-10-14.
- **Date:** 2026-10-14
- **Relates to:** `000-design.md` §14, §15, §20, §22, §30; `004-rule-set-adjudications.md` §6; `005-reverse-decoding-findings.md` C2; `006-si1-merged-iteration.md` (open proposals)
- **Evidence:** `eval/reports/si2-summary.md`; `eval/reports/verdicts-si2.claude.yaml`; `dev/inbox/si2/` (probes, candidates and `cand/build.py`, reviews, self-hosting, `runs/outputs.jsonl`)

## Context

Decision 006 adopted the si1 merge without a gold-case regression and left fourteen open proposals, each
raised by cold readers as a two-readings fork. si2 is a single-model iteration on that version: at the
maintainer's instruction every model call ran on Claude Opus 5.5 (subagents for review and decoding,
`claude -p --model claude-opus-5-5` for candidate runs and judging). The multi-vendor protocol was suspended
for si2, as it was for si1.

si2 did not start from the proposals. It first measured them:

1. **Gold regression of the 006 version** (outstanding since 006): 56/56 cases, 0 deterministic errors,
   52/56 judged pass, naturalness 4.62. Failures: G-A-002, G-R-007, G-R-011, G-T-101.
2. **Fork probes.** Each open proposal that could be tested got a probe with its expected behaviour
   registered before any output was seen (`dev/inbox/si2/probes/probes.yaml`), run three times.

Only one proposal forked in behaviour. The others agreed across all three runs, and always on the intended
reading:

| open proposal | probe | result on the 006 version |
| --- | --- | --- |
| 13 — caller names strict for a review task | PR-01 | findings, not a rewrite, 3/3 |
| 11 — P004 adjacency read as constraining the source | PR-02, PR-03 | runbook returned unchanged 3/3; no P004 finding 3/3 |
| 12 — 「标记多重集必须相等」 versus anaphora | PR-04, PR-11 | `create_order` written out 3/3; review does not flag the extra occurrence 3/3 |
| 4 — review of text with no source | PR-08 | intra-text conflict reported as A005 3/3 |
| 14 — a bare step cap as merge authorisation | PR-09 | merged with the checkpoint intact 3/3 |
| F3a (merge review) — P005 category scope | PR-05 | 「待确认」 raised for a system prompt 3/3 |
| F9 (merge review) — conversion authorisation list | PR-10, PR-12 | exact ratio-to-percent conversion done and not flagged 3/3 |
| **6 — rule ID for a missing-information finding** | PR-01, PR-03, PR-07 | **forked**: the same gap cited as CTC-A005/ERROR in one run and CTC-P002/WARNING (or escalated ERROR) in another |

Two gold failures also traced to wording. G-R-007 is an over-control trap: a compliant
「备份数据库后，将流量路由至备用集群。」 drew two CTC-P002 findings for not naming the database instance and
the cluster. The same pattern, instance- or namespace-level detail reported as a missing object, appeared in
PR-01, PR-03 and PR-07. G-R-011 is a register gap: no rule licenses removing 「糟糕！」 from an error message
(E3 below).

## Decision

Three edits to `SKILL.md`. All are clarifications of rows that already exist; no rule ID, level, category
or ladder row changes.

**E1 — §8 step 2: route the rows' own A005 cases to A005 in review.**

> 规则条文写明转 CTC-A005 的情形（CTC-A003 无证据、CTC-L004 边界本身歧义、CTC-P002 无法确定），finding 的规则字段填 CTC-A005，不另列原规则；CTC-P002 的 finding 只针对来源或上下文能确定、却没有写出的部分。

The three rows already say "转 CTC-A005" or "按 CTC-A005 报告". What the text never said is which ID the
review finding carries, and the runs filled the gap differently.

**E1b — §8 severity paragraph.**

> 按第 2 步转为 CTC-A005 的 finding 按 CTC-A005 定级，不算升级。

Without it, E1 contradicts 「没有其他升级」. The v3 self-hosting pass reported that contradiction as ERROR,
and the adversarial reviewer listed it as a conflict.

**E2 — CTC-P002 row, appended.**

> 步骤已写出具体对象、只是未细化到实例、节点、环境、路径或命名空间时，不算缺少对象或位置，也不因此按 CTC-A005 报告；来源或上下文在对象或这些层级上出现多个可能的取值时除外。「相关配置」「对应服务」这类说法不算写出对象。

### Gate items (`000-design.md` §20; both edits are clarifications of 应/必须 rows, not new rules)

| | E1 + E1b | E2 |
| --- | --- | --- |
| failing input | PR-01 「确认新证书已生效」; PR-03 the DROP step; PR-15 step 3 | G-R-007; PR-03 steps 2–4; PR-01 step 1 |
| observed failure | same gap cited A005/ERROR or P002/WARNING across runs | P002 findings for instance-level detail on a compliant runbook |
| risk | the severity of a review finding depends on the run, not on the text | over-control: review floods clean runbooks with findings |
| existing rules insufficient | the rows route to A005 but never say what the review finding cites | §5 「不得因理论上可解析出两种读法而报告」 already forbids it; the runs did not apply it to P002 |
| test that fails before and passes after | PR-01/PR-03/PR-15: rule IDs per locus across three runs | G-R-007 (judge); PR-03 (finding count) |
| boundary | PR-13: 「重启对应服务」 must still be P002 (determinable) | PR-13 (placeholder object) and PR-15 (`api-v1` with two namespaces in context) must still be reported |

### Consequence that E1 makes explicit

A CTC-P002 or CTC-A003 gap that cannot be determined now reports at CTC-A005's level, ERROR, without the §8
risk-field condition. On the 006 version the same gap could come out WARNING. This follows from the rows, and
decision 005 C2 already removed the WARNING branch for A005 (ambiguity that changes no operation is not
reported at all). It is recorded here because it is a visible severity change.

## Withdrawn: E3, a register trigger in CTC-R003

E3 let R003 delete an emotional interjection (「糟糕！」) when the target text itself is an alert, error or
status message. Three wordings were tried; each was narrowed after a review or a probe:

- v1 also covered modal particles. The reviewers showed 「吧」 carrying a guess and 「了」 in 「磁盘快满了」.
- v2 caught a reply quoted inside an agent instruction (PR-17, 3/3).
- v4 excluded modal particles outright.

Every wording fixed G-R-011, 9/9 against 1/4 on the 006 version. Every wording also cost G-R-010, the
tool-description register case, at the same ladder layer: 2/9 with E3, against 6/7 without it (Fisher exact,
two-sided, p ≈ 0.04). The outputs show why:

- With E3, the model keeps 「这个工具允许调用者获取…」.
- Without it, the model rewrites to 「该工具用于获取…」.

The 006 version cleans register in tool descriptions and agent instructions only by stretching R003 past its
listed defects. A second, enumerated branch made the row read as closed. G-R-009, G-R-010 and G-R-011 share one
gap, and a one-clause fix trades one of them for another. It is open proposal 16.

## Alternatives considered

- **E1 without E2.** Rejected on the ablation. With E1 alone, an over-flag that had been P002/WARNING
  reappeared as two A005/ERROR findings on G-R-007 (noE2 r1). E1 is safe only with E2's bound.
- **D-A4 from si1: cite the rule in the 「待确认」 category's parenthesis.** Rejected. Category 5 cites
  CTC-S002, a rule about outputs adding propositions, which is meaningless as a review finding on a source
  text. E1 uses the routing the rows already state.
- **Rewrite the seven proposals that did not fork.** Rejected for si2. `000-design.md` §20 and AGENTS.md ask
  for a demonstrated failure, and Opus 5.5 showed none. They stay open, because a model with different priors
  may still fork on them.

## Verification

- `tools/compare_skill.py` against the 006 version: all hard gates pass (29 rule levels, seven categories,
  three modes, five ladder rows, six fields, three severities, frontmatter, `check_skill.py` 0/0). Body
  12 395 → 12 692 characters (+2.4%), 232 lines.
- Gold regression of the final text: 56/56 cases run, 0 deterministic errors, 56/56 judged, 52 pass (006
  version: 52), naturalness 4.73 (006 version: 4.62), no over-edit on any trap. Failures: G-A-002 and
  G-T-101 (both fail on the 006 version and in r1), G-R-011 (the register gap above), and G-R-010 in its
  single run. G-R-010 pooled across the E3-free runs is 3/4, the same as the 006 version.
- Replicates: G-R-007 passes 4/4 on the final text and 3/4 on the 006 version.
- Probes on the final text, three runs each: PR-03 clean 3/3; PR-13 P002 3/3; PR-15 A005 3/3. PR-01's gap
  is cited as A005 whenever it is reported (2/3).
- Three independent Opus 5.5 reviews of the first candidate (adversarial, cold reverse-decode,
  naturalness) and a second cold decode of v2. Rulings: `dev/inbox/si2/review/adjudication.md`.
- Self-hosting: review-mode passes on the 006 version, v3 and the final text
  (`dev/inbox/si2/selfhost/`). Findings: 5 on the 006 version, 8 on v3, 6 on the final text. v3 raised one
  finding in si2 text, the escalation conflict that E1b fixes; the final text raised none. Three findings
  recur in all three runs or in both later runs: the 状态提示 scope gap (open proposal 3), the R004 word list
  (open proposal 5), and 「记录级别」 in §3 (a one-word T001 fix, left for the next round).

## Limitations

- **One model throughout.** The candidates, the probe runs, the judge, the three reviewers and the
  decoders were all Opus 5.5. D001 is the standing caution: a judge from the same family as the generator
  may share its blind spots. The probes help because their expectations were registered before the runs and
  most are scored on observable features: rule IDs, a body changed or unchanged. The gold verdicts do not
  have that protection.
- Single gold runs vary by two to three cases between runs of the same text (the 006 version's G-R-007,
  G-R-009, G-R-010 and G-S-001 each passed some replicates and failed others). Equal pass counts are no
  evidence of a gain.
- The gold corpus is still not human-reviewed (`eval/reports/release-gates.md`).

## Open proposals after si2

From 006, still open: 1 (「必须」 inside 「应」 rows), 2 (R003 「过长」), 3 (状态提示 scope, reported again
in the self-hosting runs on both the 006 version and v3), 5 (R004's word list, which leaves a residual A005/R004
variance in PR-07), 7 (category 7 narrower than S001), 8 (P004/R005 attribution), 9 (T001 tie-break),
10 (frontmatter terminology).

From 006, probed with no fork in Opus 5.5 and left unchanged: 4, 11, 12, 13, 14, plus F3a and F9 from the
merge review. Reopen any of them if another model forks.

From 006, resolved: 6, by E1. One residual remains: a missing-information gap can still be read as category 5
(CTC-S002) instead of CTC-A005, as the decoders and the v3 self-hosting pass both noted.

New:

15. CTC-A005's 「缺少……判据」 overlaps CTC-P003's bound on missing success criteria. A verification step with
    no criterion can reach A005/ERROR, which bypasses P003's rule that only destructive steps qualify
    (adversarial review, E1 counterexample).
16. Register cleanup in error, tool-description and agent-instruction text has no licensing rule (G-R-009,
    G-R-010, G-R-011; E3 above). A fix should be designed against all three cases at once, with PR-16–PR-19
    as its boundary set.

## Consequences

- `SKILL.md`: §8 step 2 and the severity paragraph gain one sentence each; the CTC-P002 row gains two. No
  section numbers change.
- `spec/rules.v0.yaml`: the P002 exception and the review-mode behaviour carry E1, E1b and E2. A revisions
  entry records them and E3's withdrawal.
- `tools/ctc_eval.py`:
  - `CTC_SKILL` and `CTC_CLAUDE_MODEL` pin the skill file and the Claude model for a run.
  - A review task in strict mode now gets review-side checks.
  - `recheck` falls back to the record's own task and mode, and accepts `--cases-dir`.
  - The judge retries a batch once when its YAML does not parse.

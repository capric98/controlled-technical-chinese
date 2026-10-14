# si2 — Opus 5.5 iteration on the si1 merge: measure the open proposals, then patch only what forks

- **Status:** complete; the result is accepted as decision 007
- **Date:** 2026-10-14
- **Orchestrator:** Claude Opus 5.5 (this session). Every model call ran on Opus 5.5, at the maintainer's instruction.
- **Relates to:** `docs/decisions/006-si1-merged-iteration.md`, `docs/decisions/007-si2-review-routing-and-p002-boundary.md`
- **Evidence:** `dev/inbox/si2/` (probes, candidates, reviews, self-hosting, `runs/outputs.jsonl`); `eval/reports/verdicts-si2.claude.yaml`

## 1. Question

Decision 006 adopted the si1 merge with two things outstanding: the gold regression had never been run on it,
and fourteen open proposals each described a place where two cold readers would read a rule differently. si2
asks which of those forks actually change what a model does, and fixes only those.

## 2. Setup

| item | value |
| --- | --- |
| baseline | `SKILL.md` at b3d66b0 (232 lines, body 12 395 chars), frozen at `dev/inbox/si2/base/SKILL.md` |
| candidate runs | `claude -p --model claude-opus-5-5` in a scratch directory, via `tools/ctc_eval.py run` (`CTC_SKILL`, `CTC_CLAUDE_MODEL`) |
| semantic judge | the same model, `dev/prompts/judge-semantic.v1.md`, unchanged rubric |
| reviews | Opus 5.5 subagents with disjoint inputs: adversarial (`dev/prompts/si2-adversarial.md`), cold reverse-decoder (`si2-decode.md`, `si2-decode-v2.md`), naturalness (`si2-naturalness.md`) |
| probes | 19 probes in `dev/inbox/si2/probes/probes.yaml`, each with its expected behaviour registered before any output; three runs per probe per version |
| candidates | built from the baseline by exact string replacement in `dev/inbox/si2/cand/build.py`: `full`, `noE2`, `v2`–`v5`, `v5-noE3`, `final` |
| model calls | 597 candidate outputs (336 full gold runs over six versions, 72 gold replicates, 186 probe runs, 3 self-hosting reviews); about 70 judge calls; 4 review subagents (≈ 540K tokens) |

## 3. Baseline gold regression (the gate 006 left open)

56/56 cases, 0 deterministic errors, 52/56 judged pass, naturalness 4.62. Failures:

- G-A-002: a known recall limit, which also failed in r1.
- G-R-007: an over-control false positive. P002 asked which database instance a compliant 「备份数据库」 meant.
- G-R-011: 「糟糕！」 stays in an error message. No rule licenses removing it.
- G-T-101: the terms were kept apart rather than unified; r1's Gemini run also failed this case.

## 4. Which open proposals fork

Full per-run table: `dev/inbox/si2/probes/summary.md`. On the baseline:

| proposal | probe(s) | behaviour, 3 runs | fork? |
| --- | --- | --- | --- |
| 13 strict named for a review task | PR-01 | findings 3/3 | no |
| 11 P004 adjacency | PR-02, PR-03 | unchanged 3/3; no P004 finding 3/3 | no |
| 12 token multiset vs anaphora | PR-04, PR-11 | anaphora resolved 3/3; not flagged in review 3/3 | no |
| 4 review with no source | PR-08 | conflict reported as A005 3/3 | no |
| 14 bare step cap | PR-09 | merged, checkpoint intact 3/3 | no |
| F3a P005 category 3 | PR-05 | 「待确认」 raised 3/3 | no |
| F9 conversion authorisation | PR-10, PR-12 | converted 3/3; not flagged 3/3 | no |
| **6 rule ID for missing information** | PR-01, PR-03, PR-07 | same gap cited **A005/ERROR, P002/WARNING or P002/ERROR**, varying by run | **yes** |

## 5. Iterations

| version | change | what decided it |
| --- | --- | --- |
| full | E1 review routing; E2 P002 boundary; E3 R003 register trigger with modal particles | first draft |
| noE2 | E1 and E3 only | ablation: without E2, E1 turned a G-R-007 over-flag into two A005/ERROR findings (1/3) |
| v2 | E1 says the finding cites A005 alone; E2 adds placeholder objects and multiple locations; E3 drops modal particles and applies only to the target text itself | three independent reviews (`dev/inbox/si2/review/`) |
| v3 | E3 excludes prompt text quoted or specified inside other text | PR-17: v2 deleted 「糟糕！」 from a reply prescribed in an agent instruction, 3/3 |
| v4 | E1b (A005 routing is not an escalation); E2 「出现多个可能的取值」; E3 also excludes warning markers and modal particles | v3 self-hosting finding; second cold decode |
| v5 | E3 keeps the warning-marker exclusion and drops the modal-particle one | a single G-R-009 run under v4; replicates later showed the baseline fails it as often |
| **final** | E1 + E1b + E2; **E3 withdrawn** | §6 |

## 6. The E3 ablation

One gold run plus three replicates per cell, Opus judge:

| case | baseline | with E3 (v3, v4, v5 pooled) | v5 without E3 |
| --- | --- | --- | --- |
| G-R-011 error message, 「糟糕！」 | 1/4 | 9/9 | — |
| G-R-010 tool description register | 3/4 | 2/9 | 3/3 |
| G-R-009 agent instruction register | 1/4 | 2/6 | 1/3 |
| G-S-001 over-edit trap | 2/4 | 2/6 | 3/3 |

Each E3 wording fixed G-R-011 and cost G-R-010: 2/9 against 6/7 without it (Fisher exact, two-sided,
p ≈ 0.04). With E3 the model keeps 「这个工具允许调用者获取…」. Without it, it rewrites to 「该工具用于获取…」 as
the gold case asks. The baseline gets register right only by stretching R003 beyond its listed defects, and a
second, narrow branch made the row read as closed. G-R-009 and G-S-001 fail about as often on the baseline, so
their failures are not attributed to E3.

## 7. Final candidate

| measure | baseline | final |
| --- | --- | --- |
| hard gates (`compare_skill.py`), `skills-ref validate` | pass | pass |
| body characters | 12 395 | 12 692 (+2.4%) |
| gold: deterministic errors | 0 | 0 |
| gold: judged pass | 52/56 | 52/56 |
| gold: naturalness | 4.62 | 4.73 |
| gold: over-edit on traps | 0 | 0 |
| G-R-007 replicated | 3/4 | 4/4 |
| G-R-010 replicated | 3/4 | 3/4 (E3-free runs pooled) |
| G-R-011 replicated | 1/4 | 0/4 |
| PR-03 (clean runbook, review) | findings 3/3 | clean 3/3 |
| PR-13 (「对应服务」, review) | P002 3/3, plus P002 over-flags | P002 3/3 |
| PR-15 (`api-v1` across two namespaces) | P002 2/3, A005 1/3 | A005 3/3 |
| PR-01 missing check on 「确认新证书已生效」 | P002/W 2/3, A005/E 1/3 | A005/E 2/3, not reported 1/3 |
| self-hosting findings in si2 text | — | 0 (v3 had 1; E1b fixed it) |

The gold pass count is unchanged, and single-run noise is two to three cases. si2's effect shows in the review
probes: the rule-ID fork is gone, the instance-level P002 over-flags are gone, and the two boundaries that must
still fire do fire.

## 8. Harness defects found on the way

- **A review task in strict mode got rewrite-side checks.** `deterministic_checks` detected review by `mode`
  only, so PR-01, 「以 strict 模式审阅」, failed `protected_tokens_lost`. Fixed: a review task counts as review.
- **`recheck` lost the task and mode of non-gold records.** It loaded gold cases only, so probe records fell
  back to rewrite checks. Fixed: the record's own task and mode are the fallback, and `--cases-dir` is
  accepted.
- **The judge's YAML sometimes does not parse.** A value opening with a backtick or a quote breaks it. The
  judge now retries a batch once. Batches of six still failed twice on the same records; batches of three
  did not fail at all on the final run.
- **Background jobs started inside a returning shell were killed.** The v2 judge never ran for this reason,
  so v2 has no semantic verdicts.
- **macOS `xargs -I` caps the replacement string at 255 bytes.** The first v3 judge launch failed silently.

## 9. Limitations

- One model family for everything: candidates, judge, reviewers, decoders. D001's caution applies to the gold
  verdicts. Probes scored on rule IDs and changed-or-unchanged bodies are less exposed to it.
- "No fork" means no fork in Opus 5.5 over three runs. The seven proposals closed that way remain open in 007,
  to be reopened if another model forks.
- The gold corpus is still not human-reviewed.
- v2 was never judged. Six v5 cases were left unjudged after two parse failures; v5 was not adopted.

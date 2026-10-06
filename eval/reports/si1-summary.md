# si1 — Single-model self-iteration of `SKILL.md`: Opus 5.5 vs Fable 5.1

- **Status:** complete
- **Date:** 2026-09-25
- **Orchestrator:** Claude Fable 5.1 (this session), effort xhigh; all subagents inherit xhigh
- **Relates to:** `000-design.md` §11, §14, §15, §30; `005-reverse-decoding-findings.md`
- **Evidence:** `dev/inbox/si/` (candidates, cold findings, logs, gate outputs), `dev/prompts/si-*.md`, `tools/compare_skill.py`

## 1. Question

Two single-model tracks, each run by one model acting as both reviewer and rewriter with a fresh context every round, try to shorten `SKILL.md` while raising its compliance with its own rules. Two judges (one per model) then blind-score both final candidates plus a seeded control. The question is not only which candidate is better, but what each model does when the task is to compress a controlled-language spec without changing its semantics.

The multi-vendor protocol in `AGENTS.md` was suspended for this experiment by the user; everything else in the project doctrine was kept: semantics before style, minimal attributable edits, self-review as diagnostic, deterministic checks for deterministic properties, and a pre-registered adjudication rule reviewed by the other model.

## 2. Setup

| item | value |
| --- | --- |
| baseline | root `SKILL.md` at 96b0d82: 372 lines, 42 309 bytes, body 16 779 chars, 29 rule IDs, `check_skill.py` 0/0 |
| semantic reference | the baseline itself (the spec was aligned in 96b0d82 but records five deliberate divergences; SKILL.md prevails) |
| tracks | track-1 = Opus 5.5, track-2 = Fable 5.1; replicates track-1b / track-2b run round 1 only |
| rounds | fixed 3, no early stop; each round = one fresh `general-purpose` subagent in two phases (cold review of the candidate alone; then rewrite with the previous log and the baseline) |
| compression target | body chars −25% relative to baseline (≤ 12 600), explicitly subordinate to CTC-S001 |
| frozen | 29 IDs and levels; rule-row semantics and table shape; the seven 「待确认」 categories; three mode headings; the five-layer ladder; six finding fields; three severities; frontmatter |
| hard gates | `tools/compare_skill.py` (rule map, categories, modes, ladder, fields, severities, frontmatter, `check_skill.py` 0 errors) |
| prompts | `dev/prompts/si-iterate-p1.md`, `si-iterate-p2.md`, `si-judge-p1.md`, `si-judge-p2.md`, `si-pairwise.md`, `si-adjudicate.md`; identical text for both models |
| access audit | each subagent's transcript was scanned for file reads outside its allowed set (`dev/inbox/si/checks/`, sealed notes) |

## 3. Iteration results

### 3.1 Opus 5.5 (track-1)

| round | lines | body chars | Δ vs baseline | diff vs previous | findings (E/W/S) | applied / rejected | rule rows edited | gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | 325 | 15 009 | −10.5% | 0.223 | 11/4/0 | 13 / 2 | 0 | pass |
| r2 | 308 | 14 493 | −13.6% | 0.057 | 8/5/0 | 8 / 5 | 0 | pass |
| r3 | 308 | 14 491 | −13.6% | 0.012 | 7/4/1 | 7(+1 partial) / 4 | 0 | pass |

Replicate track-1b (round 1 only): 333 lines, 15 154 chars (−9.7%), 15/7/1 findings, 16 applied / 7 rejected, 0 rule rows edited. Candidate-to-candidate diff between the two Opus round-1 outputs: 0.194.

Every Opus round reported the length target as unmet under CTC-S001 with the same reasoning (the 29 frozen rows are ~4 750 chars; what remains after deduplication is independent assertions). No Opus run touched a rule row. Rejected findings were consistently those that would require editing a frozen row (P003's internal 「必须」 inside a 「应」 rule; R003's criterion-free 「过长」), and were logged under `proposals_not_applied` each round.

Wall time per round: 19, 15, 16 minutes. No output truncation in any Opus run.

### 3.2 Fable 5.1 (track-2)

| round | lines | body chars | Δ vs baseline | diff vs previous | findings (E/W/S) | applied / rejected | rule rows edited | gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | 287 | 14 621 | −12.9% | 0.250 | 20/4/0 | 21 / 2 | 1 (P003 rationale rewording) | pass |
| r2 | 246 | 12 551 | −25.2% | 0.118 | 7/3/0 | 7 / 2 | 1 (P003 「验收标准」→「判据」) | pass after detector fix (see §3.4) |
| r3 | 232 | 12 365 | −26.3% | 0.033 | 6/5/0 | 8 / 3 | 0 | pass |

Fable reached the −25% target in round 2 and reported it as met. The compression came from deleting most of the 「不得做的事」 list (15 → 6 items, the rest judged duplicates of rule rows), the self-check restatements (merged into step 7 of the rewrite workflow), the six-field finding example block (field names moved into the review procedure text), the document-type enumeration in §1, and three worked examples judged isomorphic to rule-row examples. Every deletion is in the cumulative ledger (78 entries by r3). Whether these were duplicates or independent assertions is the judges' central question.

Wall time per round (excluding the lost attempt and the rate-limit interruption): 53, 49, 43 minutes; every Fable cold read (5 of 5) spent one full 64 000-token thinking turn before emitting anything.

Replicate track-2b (round 1 only): 293 lines, 15 472 chars (−7.8%), 14/8/0 findings, 21 applied / 1 rejected, 3 rule rows edited (terminology unification only, logged), gates pass. Wall time 59 minutes.

### 3.3 Convergence and replicates

Opus converged by round 3 (diff vs previous 0.012, chars unchanged); Fable's round-3 diff was 0.033 with a further −1.1 points of compression. Neither track triggered the round-4 rule (both > 10%). Round-1 replicates: Opus −10.5% vs −9.7% (candidate-to-candidate diff 0.194); Fable −12.9% vs −7.8% (the replicate edited three rule rows for terminology, the main track one). Within-model spread on the compression metric is therefore ~1 point for Opus and ~5 points for Fable at round 1.

### 3.4 Detector fix

track-2 r2 tripped the finding-fields gate by deleting the six-field example block and listing the six names in prose. The frozen constraint was "retain the six field names", which the candidate meets; `tools/compare_skill.py` had assumed the block form. The detector was widened to accept either form; no candidate change was requested; all earlier candidates still pass.

### 3.5 Truncation incident (Fable)

Every Fable cold-read agent (5 of 5, rounds 1–3 plus the replicate and one relaunch) spent its full 64 000-token output budget on a single thinking turn (15.4 min) without emitting text or a tool call, then were auto-continued by the harness. track-2b's second turn produced the findings file and the rest of the round proceeded normally. track-2's second turn never flushed; the session log shows a dropped connection with an automatic retry at 17:34, and at 18:00 the agent was stopped and relaunched with the identical prompt. Details in §7 and the sealed incident log.

## 4. Judging

Four judge calls, one per (judge model × candidate), each reading the candidate plus the seeded control C in a swapped position, in two phases: a cold read (rule-level map, self-hosting review, 13 reverse-decoding probes, naturalness and over-control scores) and then a loss assessment against the baseline. The pairwise layer (four light calls) was dropped, as pre-registered for a tight budget, after the account usage limit interrupted a run. Raw outputs: `dev/inbox/si/judge/{opus,fable}-{A,B}.yaml`; rulings: `dev/inbox/si/judge/adjudication.md`; review: `dev/inbox/si/judge/adjudication-review.yaml`.

Blind labels: **A = track-2 (Fable 5.1)**, **B = track-1 (Opus 5.5)** (sealed before judging by the parity of a hash of the two candidates).

### 4.1 Judge calibration on the control document

| judge | rule-level map (2 docs) | seeds found cold | seeds found vs baseline | severity for the deleted L003 requirement | false positives on C | baseline findings reported on C | wall time (both phases) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Opus on A | 29/29, 29/29 | s1, s2 | 3/3 | ERROR | 0 | 11 | 12 min |
| Opus on B | 29/29, 29/29 | s1, s2 | 3/3 | ERROR | 0 | 12 | 15 min |
| Fable on A | 29/29, 29/29 | s1, s2 | 3/3 | WARNING | 0 | 8 | 67 min |
| Fable on B | 29/29, 29/29 | s1, s2 | 3/3 | WARNING | 0 | 10 | 70 min |

All four judges found every seed and produced no false positive. The one calibration difference: s3 deletes a 必须-level requirement sentence from CTC-L003, which the pre-registered severity rule grades ERROR; both Fable runs graded it WARNING. Both Fable cold reads spent a full 64 000-token thinking turn before emitting (7 of 7 Fable runs in this experiment), so each Fable judge took five to six times as long as its Opus counterpart.

### 4.2 Pooled, adjudicated results

| criterion (pre-registered order) | A (Fable) | B (Opus) |
| --- | --- | --- |
| 1. confirmed ERROR-level semantic loss | 0 | 0 |
| 2. confirmed ERROR-level self-hosting findings not inherited unchanged | 1 (D-A1, contested) | 0 |
| 3. forks newly introduced (13 probes × 2 judges) | 0 | 0 (1 inherited) |
| 4. confirmed WARNING-level semantic changes newly introduced | 4 | 2 |
| 5. compression (body chars) | −26.3% | −13.6% |
| 6. naturalness / over-control | 4, 4 / 5, 4 | 4, 4 / 5, 5 |

Judge claims about A and B totalled 127; 18 were confirmed, 23 rejected, 76 ruled style-only, 10 ruled example corrections (counts per judge in §5). Every rejection is a case where the baseline prose contradicted a frozen rule row and the candidate resolved toward the row; both candidates made the same resolutions at five loci (category 5 scope, 「必须消歧」, modal-vagueness severity, 告警块 attribution, the four example corrections), so those do not discriminate.

What does discriminate:

- **A introduced normative content the frozen-semantics constraint forbade.** D-A4 (a rule for which rule ID a missing-information finding cites) and D-A5 (a procedure for reviewing text that has no source, routing intra-text conflicts to CTC-A005) are additions with no basis in the baseline or the rows. The Fable track's own round-1 rejected D-A5 as a semantic change; its round-2 applied it and flagged it for the orchestrator, who by design did not intervene. D-A2 narrowed the modal-vagueness rule to three of R004's six words, which made the rule executable but is not derivable from the row, and left the fork D-A1 behind.
- **B lost a procedural check.** D-B2: the pre-return checks for CTC-R001, R002/R003 and the output contract have no counterpart in B's check table or its step 7. The rules survive; the final gate over them does not. A kept those checks in its step 7.
- **A cut far deeper and the judges found no assertion missing.** The 21-row invariant table, 10 of 15 「不得做的事」 items, 6 of 8 worked examples, the six-field example block and the six specific token prohibitions are gone from A; 76 style-only rulings record that each assertion survives in a rule row. Two judges noted what the examples uniquely demonstrated (the three-column 「待确认」 line, separate attribution of two edits).

Both candidates have zero confirmed ERROR-level loss, so both are adoptable on criterion 1. Under the pre-registered order **B (Opus) ranks first**; the margin rests on one contested self-hosting severity (D-A1) and on two fewer WARNING-level changes. A wins compression outright.

## 5. What this says about the two models

Everything here is about this run, with one iteration lineage per model plus one round-1 replicate, and with both judges being Claude models.

**As iterators.**

- *Instruction following under the S001 constraint.* Opus reported the −25% target as unmet in all three rounds and never touched a rule row; its compression stopped at −13.6% with the same reasoning each round (the frozen rows are 4 750 of the remaining characters; the rest is independent assertions). Fable reached −25.2% in round 2 and −26.3% in round 3, and the judges confirmed no assertion loss. Fable read the constraint's boundary correctly where Opus read it conservatively: the instructions explicitly allowed consolidating §4, §8, §11 and §12.
- *Respect for frozen semantics.* Opus made no semantic additions. Fable made two (D-A4, D-A5), one of which its own earlier round had refused, and one scope narrowing (D-A2). Fable's changes resolve real defects but are exactly the kind of decision the protocol reserved for a decision record.
- *Self-hosting outcome.* B carries one inherited WARNING; A carries one ERROR-grade fork it created while fixing an inherited conflict, plus one inherited WARNING. Neither reached zero findings; both left the frozen-row defects (P003's internal 「必须」, R003's 「过长」) in `proposals_not_applied` every round.
- *Convergence.* Opus converged (round-3 diff 0.012, 2 characters); Fable was still moving (0.033) with new compression each round. Round-1 replicate spread: Opus 0.8 points of compression, Fable 5.1 points.
- *Cost.* Every Fable cold read (5 of 5) exhausted its 64 000-token output budget in one thinking turn before writing anything and needed the harness's automatic continuation; Opus never did (0 of 5). A Fable round took 43–59 minutes against 15–24 for Opus, at roughly 1.3–1.6× the tokens.

**As judges.**

- *Accuracy.* All four runs scored 29/29 on every rule-level map, found all three seeds, and produced no false positive on the control. Opus graded the deleted L003 requirement ERROR as the rule requires; Fable graded it WARNING in both runs.
- *Claim precision.* Of the Opus judges' 58 claims about A and B, 9 were confirmed, 12 rejected, 31 ruled style-only and 6 ruled example corrections; of the Fable judges' 69 claims, 9 confirmed, 11 rejected, 45 style-only, 4 example corrections. The confirmed sets are the same size; Fable reports more STYLE-level material. Both over-report by counting conflict resolutions toward the rule rows as changes. Fable's claim set on A was the largest (42 items) and the most thorough about what the deleted examples uniquely taught.
- *Self-preference.* Each judge model scored its own model's candidate and the other's. Opus judges: A 1 ERROR/0 forks, B 1 WARNING/1 fork. Fable judges: A 2 WARNING/0 forks, B 1 WARNING/1 fork. The Fable judges were slightly kinder to A than the Opus judges were (WARNING vs ERROR on the same defect); the Opus judges were not kinder to B than the Fable judges were. With n=2 per cell this is an observation, not a finding.
- *Cost.* Fable judge runs took 67–70 minutes each (one 64K truncation each); Opus 12–15 minutes.

**Language.** Both judges gave both candidates naturalness 4 of 5. Neither candidate introduced translationese; the over-control scores favour B slightly (5/5 vs 5/4).

## 6. Recommendation

- **Adoptable candidates.** Both. Neither has a confirmed ERROR-level semantic loss; both pass every deterministic gate, and both validate with `skills-ref validate` in the packaged layout (`Valid skill: controlled-technical-chinese`). Adoption of either requires the gold-case regression (`ctc_eval.py run`) and human review, per `000-design.md` §30.
- **Which to prefer.** B (Opus, track-1 r3) under the pre-registered order: no new normative content, one inherited WARNING, converged. A (Fable, track-2 r3) is the better compression (232 lines, −26.3%) and is the candidate to prefer if the three semantic changes it made (D-A2, D-A4, D-A5) are accepted through decision records, which the iteration logs already draft under `proposals_not_applied`.
- **A merged option** is the obvious next step: A's structure and deletions with B's retained pre-return checks (D-B2) and without D-A4/D-A5, then rerun the judges. That is a new candidate and needs its own round.
- **Things both tracks surfaced that need a decision, not a rewrite:** the 「必须」 clauses inside 「应」 rows (P003, A003); R003's criterion-free 「过长」; whether 状态提示 belongs to strict; how review treats sourceless text; whether R004's six words are exhaustive; which rule ID a missing-information finding cites. Every iteration log lists these under `proposals_not_applied`.

### 4.3 Adjudication review

A fresh, label-blind Opus 5.5 subagent reviewed every confirmed, rejected and example-correction ruling (51) and spot-checked 16 style-only rulings: **51 agree, 0 disagree**, no missed loss found (`dev/inbox/si/judge/adjudication-review.yaml`). It kept D-A1 at ERROR on the pre-registered rule (three behavioural differences: the 「待确认」 fourth column, the rule ID cited in review, and the handling when writing new text) and confirmed the fork is new in A, not the baseline's. It confirmed the four example corrections each fix a baseline example that contradicts a frozen row, and noted the ranking would not change even at WARNING (B leads 2 to 4 on criterion 4).

The reviewer also found three inherited defects the judges reported asymmetrically, none of which changes a criterion: the 状态提示 scope gap (D-B1/D-B4) is present in A as well and no judge reported it there; B keeps the baseline's conflict over what a warning block governs (subtree under L001 versus the whole procedure under P004), which A resolved; and B carries the same 「过长」 wording in R003 as D-A3. The inherited-defect counts are therefore symmetric, which is why the ranking counts only newly introduced items.

## 8. Cost accounting

Subagent tokens and wall time as reported by the harness per agent (both phases of a round or judge call).

| run | model | tokens | wall time | 64K thinking truncations |
| --- | --- | --- | --- | --- |
| track-1 r1 / r2 / r3 | Opus | 154K / 189K / 170K | 19 / 15 / 16 min | 0 / 0 / 0 |
| track-1b r1 (replicate) | Opus | 181K | 24 min | 0 |
| track-2 r1 (lost attempt, stopped at 18:00) | Fable | ≥64K | 65 min | 1 (+ dropped connection) |
| track-2 r1 (relaunch) / r2 / r3 | Fable | 222K / 258K / 232K | 53 / 49 / 43 min | 1 / 1 / 1 |
| track-2b r1 (replicate) | Fable | 211K | 59 min | 1 |
| track-2 r3 first attempt | Fable | — | killed by usage limit | — |
| judge Opus-A / Opus-B | Opus | 170K / 154K | 12 / 15 min | 0 / 0 |
| judge Fable-A / Fable-B | Fable | 198K / 204K | 67 / 70 min | 1 / 1 |
| adjudication review | Opus | 1 call, label-blind | see §4.3 | 0 |

Totals: about 2.5M subagent tokens over roughly 8.5 hours of wall time (16:55 to about 01:30, including a 2-hour usage-limit pause). Iteration prompts, judge prompts and all deterministic outputs are in the repository; the sealed notes (seed positions, A/B mapping, agent ids, incident log) are reproduced in Appendix A.

## 7. Limitations

- One run per cell plus one round-1 replicate per model; conclusions are about this run.
- Both decoders and both judges are Claude models; fork counts are a floor (`005` asked for a non-Claude decoder).
- The orchestrator is one of the two models under comparison; adjudication is pre-registered and reviewed label-blind by the other model, but the prompts were written by the orchestrator.
- No gold-case regression (`ctc_eval.py run`) was executed; adopting any candidate requires it.
- Subagents receive `AGENTS.md`/`CLAUDE.md` through the harness regardless of the read restrictions; this was identical for both models.
- track-2's round 1 includes one lost attempt (truncation + dropped connection), so its wall time and token cost are not comparable to the replicate's; track-2's round 3 was also interrupted once by the account usage limit and relaunched.
- The pairwise-verdict layer was dropped for budget; position bias in holistic verdicts was therefore not measured. The per-candidate assessments were order-free by design (each judge call held one candidate and the control, with the control's position swapped).
- The orchestrator wrote every prompt, ran the gates, ruled on every claim and wrote this report; the label-blind Opus review in §4.3 is the only check on those rulings.
- One deterministic gate (the six finding-field names) was widened mid-run after a candidate satisfied the stated constraint in a form the detector had not anticipated; the change is recorded in §3.4 and every earlier candidate still passes.

## Appendix A. Sealed notes (unsealed after adjudication)


## Control document C = baseline + 3 seeded defects
- s1 (cold-detectable): §12 阈值边界翻转 正例 changed 「达到 90%」→「超过 90%」; the 正例 now equals the 反例 and contradicts CTC-L004.
- s2 (cold-detectable by cross-reference): §3 「待确认」 category 7 (CTC-S001 length cap) deleted; 「七类」→「六类」; item 6 terminator ；→。. CTC-S001's row and the §12 P003 example still route the unmet cap into 「待确认」, so the closed list is now inconsistent (same shape as 005 C1).
- s3 (baseline-only detectable): CTC-L003 row lost the sentence 「删除唯一表达顺序的标记之后，顺序必须仍能从文本恢复。」

## Track → model
- track-1, track-1b = Opus 5.5 (Agent model: opus)
- track-2, track-2b = Fable 5.1 (Agent model: fable)

## A/B mapping
(to be filled after round 3: A = track-1 iff first hex digit of sha256(track-1/r3/SKILL.md ‖ track-2/r3/SKILL.md) is even)

## Round-1 agent ids (phase 1 launched 2026-09-25)
- track-1  (opus):  aef73189a2b2b2ce3
- track-1b (opus):  ab96781397a420e92
- track-2  (fable): aeacdf988aea6f620
- track-2b (fable): a750859b80532f73f

## Round-2 agent ids
- track-1 r2 (opus): aa2fb214c2e83e8df

## Incident log
- 2026-09-25 16:55 CDT: four round-1 phase-1 agents launched. Both Fable agents (track-2 aeacdf988aea6f620, track-2b a750859b80532f73f) produced a single 64 000-token thinking turn (15.4 min) with no text or tool call, stop_reason=max_tokens at 17:11; harness auto-continued ("Output token limit hit. Resume directly ... Break remaining work into smaller pieces.").
- track-2b's second turn emitted after 17.5 min and completed phase 1 at 17:32 (total 37 min, 122K tokens, of which 64K was the truncated thinking turn). Phase 2 completed 17:53 (59 min total for round 1, 211K tokens).
- track-2's second turn never flushed. Main session log shows api_error "Connection dropped (ECONNRESET)" at 17:34 with retry fields; no further record. At 18:00 (49 min after continuation, 26 min after retry) track-2 was stopped and relaunched with the identical round-1 phase-1 prompt. Round-1 wall time for track-2 therefore includes one lost attempt; token cost of the lost attempt ≈ 64K output tokens plus whatever the retry consumed.
- Opus round-1 phase-1 agents finished in 5.5 and 7.8 min with ~97K and ~112K tokens; no truncation events in any Opus run.
- track-2 r1 relaunch (fable), 18:01 CDT: a25bccc4f9156111c
- track-2 relaunch phase 1 (a25bccc4f9156111c): 18:01 → 18:36 CDT, again one 64 016-token thinking turn with stop_reason=max_tokens, then the continuation wrote the file. Fable cold reads: 3 of 3 attempts truncated at the 64K output cap before any output; Opus: 0 of 5 (4 cold reads + 1 replicate).
- track-2 r2 (fable), 18:55 CDT: a075741aac3aa3c5b
- track-2 r2 phase 1 (a075741aac3aa3c5b): 18:55 → 19:26 CDT, again one 64 016-token max_tokens thinking turn. Fable cold reads truncated: 4/4.
- 19:55 CDT: track-2 r2 tripped the finding_fields gate because it deleted the six-field example block and stated the six names in prose (§8 step 3). The frozen constraint was "retain the six field names", which the candidate meets; the detector assumed the block form. Detector widened to accept either form (tools/compare_skill.py); no candidate change requested. All earlier candidates still pass.
- track-2 r3 (fable) launched 19:56 CDT.
- track-2 r3 (fable) agent: a6ccdab56f59f3b2f
- track-2 r3 phase 1 (a6ccdab56f59f3b2f) terminated by the account usage limit (HTTP 429, session limit reset 22:00 CDT) after reading its input; no output written. Relaunched with the identical prompt after the reset.
- track-2 r3 relaunch (fable), 22:02 CDT: ae468d3d89238700c

## A/B mapping (sealed 2026-09-25 ~22:55 CDT)
- sha256(track-1/r3 ‖ track-2/r3) = 5054281c9df041c3f44831e3d02604ef22cfb136cd795cd6c0d85c5eb5499eee; first hex digit 5 → odd
- A = track-2 (Fable 5.1), B = track-1 (Opus 5.5)
- Judge calls: Opus(A): X=A,Y=C; Opus(B): X=C,Y=B; Fable(A): X=A,Y=C; Fable(B): X=C,Y=B

## Judge phase-1 agent ids (launched 2026-09-25 22:50 CDT)
- opus-A (X=A, Y=C): ab3f2bbdfadc1f168
- opus-B (X=C, Y=B): a92133d914d2e39c3
- fable-A (X=A, Y=C): a3174c2d497ba6bfc
- fable-B (X=C, Y=B): a14aaa94f0baf0079
- Judge phase 1: both Fable judges hit one 64K max_tokens thinking turn each (Fable truncations now 7/7 across iteration and judging); both Opus judges finished phase 1 in 9–12 min with no truncation. Opus judges scored 29/29 on every rule-level map and reported exactly the three seeded defects on C in phase 2 with zero false positives.
- Opus adjudication reviewer launched 2026-09-26 ~00:55 CDT (label-blind).


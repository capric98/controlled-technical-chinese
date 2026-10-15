# si3 — rulings on the three independent reviews of candidate v3

Reviews: `adversarial.yaml` (semantic invariants, counterexamples), `decode.yaml` (cold reverse-decoding,
candidate only), `naturalness.yaml` (wording and over-control). All three are Opus 5.5 subagents with
disjoint inputs; none saw another's output. The orchestrator (Opus 5.5) made the rulings. The human gate is
the maintainer's review of decision 008.

**Maintainer ruling on RG-15 (2026-10-15):** the registration was wrong; the rewrite matches G-R-010's gold and
stands (decision 008).

A first set of the same three reviews was started on v2 and stopped at the usage limit before the adversarial
reviewer wrote anything. The partial decode and naturalness files are kept as `*-v2-partial.yaml`. They were
not used for rulings, because v3 changed the R003 requirement and the R004 class name after they started.

Every counterexample a reviewer built became a probe, and its expected behaviour was written down before any
output was seen (`probes.yaml`: RG-11 and RG-12 from the naturalness review, RG-13 to RG-17 from the adversarial
review). Text changed only where a probe failed, as in si2 (`dev/inbox/si2/review/adjudication.md`, 「危险！」).

## S1 — 状态提示 in the strict scope

| finding | source | ruling |
| --- | --- | --- |
| Accept as a clarification: Opus already infers strict 3/3, and the evidence is the recurring self-hosting finding plus maintainer decision Q1 | adversarial | **accepted** |
| No fork: rewrite resolves to strict through §1 plus the strict scope list, and review resolves to the strict threshold | decoder probe 4 | **accepted** |
| False fire: an API doc that quotes a status message could be switched to strict as a cross-type document | adversarial | **recorded, not changed**: low risk, and the baseline already has the same exposure for quoted error messages |
| The frontmatter `description` does not list 状态提示, and after S1b the body names it only in the §3 list | naturalness, adversarial | **recorded**: the frontmatter is frozen by the hard gate (`compare_skill.py`); this belongs with open proposal 10 |
| 「告警」 names two concepts, the alert message (strict scope, T002) and the warning block (P004, S002) | v4 self-hosting r2 | **recorded**: the ambiguity predates S1, which only appended to the same list item |

## S2 — CTC-R004 as an open class, with an exclusion routed to CTC-A005

| finding | source | ruling |
| --- | --- | --- |
| Accept as a clarification: it removes the mismatch between the §3 「尽快回滚」 example and the list | adversarial | **accepted** |
| 「等程度」 can first parse as "equal degree"; 「缺失的次数」 does not fit 「多次」, which gives a vague count rather than none | naturalness | **accepted** (v4): 「等表示程度、时机或裁量的词」, 「未给出具体值的次数或时长」 |
| §8 step 2 lists the rows that route to CTC-A005 without R004's exclusion, so the list reads as exhaustive or as examples | v3 self-hosting r2 finding 1; adversarial conflict 4 | **accepted** (v4): R004's exclusion is added to the parenthesis |
| 「及时」 can be read as a timing word (R004) or a missing duration (A005) | decoder probe 3 | **recorded**: the decoder itself chose R004; no probe has shown a fork |
| 「若干分钟」 may pull a status estimate (「预计还需几分钟」) into A005; 「时机词」 may catch 「请稍后重试」 | adversarial false fires 1 and 2 | **checked on existing outputs, no fire**: ST-02 is 「未发现违规」 3/3 on v4; the 「待确认」 sections of PR-19, RG-04 and G-R-011 contain no 「稍后」 item |
| Degree word plus state (「负载过高时」) can be reported under both R004 and A005; 「条件允许时」 routed to A005 loses the strength question §5 asks for | adversarial false fire 3, missed fire 1 | **recorded as open**: no probe run in si3; a candidate pair for the next round |

## S3 — CTC-R003 adds 口语腔

| finding | source | ruling |
| --- | --- | --- |
| The class itself is supported (G-R-011, PR-19, RG-07 0/3 on base) and avoids E3's genre scoping | adversarial | **accepted** |
| The strength boundary names one word; the mechanism (cleaning a particle raises a colloquial prohibition to 「不得」) applies to 「可别」「万万」 | adversarial strongest counterexample | **accepted after probe**: RG-13 (「可别…哦」) raised to 「不得」 3/3 on v4 and 0/3 on base. v5 states the boundary by function, 「加强禁止或要求的成分（「千万」）不是口语腔」, keeping 「千万」 as the only example so RG-13 still tests generalisation |
| Narrow 「把读者当作谈话对象的引导」 to tool descriptions: in agent instructions 「你可以」 is a permission, in developer docs 「您可以」 is house style (layer 5) | adversarial revision 1 | **rejected after probe**: RG-16 (agent's 「你可以调用…查一下」) keeps the permission 3/3 on v4; RG-17 (review of 「您可以通过 `--verbose`」) is clean 3/3 |
| Once triggered, the tool-description sentence could turn a permission into a description or an order | adversarial false fire 5 | **probe passed**: RG-14 (「允许调用方…重试一下」) drops 「一下」 and keeps 「允许」 3/3 on v4 |
| The tool-description sentence reads two ways: the repair form after a listed defect, or a defect of its own | decoder probe 1; adversarial missed fire on RG-10 without 「哦」 | **reworded** (v4): 「去除这些缺陷时，工具描述改为直接陈述功能…」. **Open for the maintainer**: RG-15 (RG-10 without 「哦」, registered as 「正文原样返回」) is rewritten to 「该函数用于…」 3/3 on v4. The model treats 「开发者可以」 as reader-directed guidance, a listed defect. G-R-010's gold requires exactly this repair of the same frame (「调用者…获取」), so the probe's registration conflicts with the gold. The rule is not narrowed, because every narrowing tried in si3 brought G-R-010's 「允许调用者获取」 back (v1, v1-class, v2: direct form 1/9) |
| 「而不是陈述谁可以用它做什么」 can be read as banning content (who may call the tool) | naturalness over-control | **reworded** (v4): 「不以使用者作句子主语（「调用者可以…」）」. RG-12 (an admin-only restriction plus register noise) keeps the restriction 3/3 on v3 and v4 |
| Examples carry meaning: 「一下」 in 「按一下复位键」 is a short press | naturalness over-control | **probe passed, no text**: RG-11 is unchanged 3/3 on v3 and v4 |
| Dashes keep the trigger clause open for about 170 characters; 「请托」 suggests pulling strings | naturalness, score 3 | **accepted** (v4): the row is split into 「文本含译文腔或口语腔时…。译文腔：…。口语腔：…。」; 「客套与请托」 becomes 「客套话」 |
| The five 口语腔 types read as closed; 「搞定」 and 「瞎猜」 fall outside them | decoder probe 2; adversarial missed fire 2 | **recorded as open**: the types are the class definition. No gold case or probe needs an item outside them, and an open trigger is what made si2 worry about over-editing |
| The suggestion 「吧」 (「先别切主吧」), as opposed to the guess 「吧」, may be deleted | adversarial false fire 4; decoder probe 5(b) | **recorded as open**: no run evidence; PR-18 covers only the guess |
| Repair 「取能去除它的最小改动」 versus the tool-description sentence's whole-sentence repair | adversarial conflict 1 | **recorded**: v4 states that the sentence applies when these defects are removed, which makes it the specific provision for that case |
| §7 steps 6 and 7 name only 译文腔 | adversarial conflict 3 | **accepted** (v5): step 6 removes 口语腔 alongside 译文腔, and step 7 checks for both. This renders R003's own class in the flow that cites it, with no new norm. The over-edit traps in the v5 gold run are its check |
| The priority table puts the caller's tone (layer 5) under R003 (layer 4), against Q2 | adversarial conflict 4 | **recorded**: RG-05 keeps the caller's tone 3/3 on every version, with or without v1's clause; §1 「调用方给定的上下文」 is what carries it |
| 「无译文腔与口语腔」 can read as "not both" (CTC-A004 scope) | naturalness | **accepted** (v4): 「无译文腔、无口语腔」 |

## Second cold decode, on v6 (`decode-v6.yaml`)

| finding | ruling |
| --- | --- |
| The tool-description sentence's main reading is the repair form, applying only after a listed defect is removed (「去除这些缺陷时」 plus the paragraph after the §6 table) | **accepted**: this is the intended reading |
| Probe 2(b): with no particle, 「通过这个函数，开发者可以把图片压缩到指定尺寸。」 is returned unchanged under that reading | **recorded as a text–behaviour split**. The decoder agrees with RG-15's registration; the model at runtime (v4–v6, 3/3) treats 「开发者可以」 as reader-directed guidance and rewrites it. Decision 008 open item 1 asks the maintainer which way to settle it: say in the text that a third-person user frame counts as reader-directed guidance (consistent with G-R-010's gold), or narrow the behaviour (which brought G-R-010 back in every si3 attempt) |
| The strength sentence may be read to cover plain 「别」「不要」 too, raising them to 「切勿」 | **probe passed, no text**: RG-19 gives 「别」→「不要」 3/3 on v6, never 「切勿」 |
| 「尽快回滚」 in review: R004/WARNING, possibly escalated, possibly with an extra A005 | **recorded**: the escalation is §8's existing optional rule; the R004 citation is consistent across R4-01's 3/3 runs |
| Step 7's 「先修复再返回」 could turn R003's 「可以保留原词」 into a required change | **recorded**: RG-06, RG-13 and RG-18 show both 「千万不要」 kept and 「切勿」 on v6; no run treated keeping as a failure |
| The five 口语腔 types read as closed (no 「等」, unlike R004) | **recorded as open**, as for the first decode |

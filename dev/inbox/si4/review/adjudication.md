# si4 — rulings on the three independent reviews of candidate v1

Reviews: `adversarial.yaml` (semantic invariants, counterexamples), `decode.yaml` (cold reverse-decoding,
candidate only), `naturalness.yaml` (wording and over-control). All three are Opus 5.5 subagents with
disjoint inputs; none saw another's output, and the adversarial reviewer saw no v1 output. The orchestrator
(Opus 5.5) made the rulings. The human gate is the maintainer's review of decision 009.

The naturalness reviewer numbered the passages in the order its prompt listed the changes, not by
`build.py`'s IDs. Its F1, T1, B2a, B2b are build.py's F1, T1, B2a, B2b; its T2 is build.py's T4, its T3 is
B1, its T4 is T2, its B1 is C1, and its C1 is T3. The rulings below use build.py's IDs.

As in si3, every counterexample a reviewer built that the existing probes did not cover became a probe,
registered before any output (`probes.yaml`, section 「added 2026-10-29 from the reviews of v1」: P3-05,
R4-08, R4-09). Text changed where a probe failed or where a reviewer showed a reading defect that a
narrower wording removes without new requirements.

## B1 — CTC-A005 and CTC-P003 (proposal 15)

| finding | source | ruling |
| --- | --- | --- |
| B1 may miss P3-01 itself: 「检查…运行情况」 is a verification action with no criterion, or reads as 「判据含义未定」, which B1's second sentence sends back to A005 | adversarial strongest counterexample; decoder probe 1 (fork, readings A/B) | **confirmed by the runs before the review arrived**: v1 cites A005/ERROR on P3-01 3/3 (base 2/3), and rewrite starts raising it 2/3 (base 0/3). B1 is replaced by B1v2, which states the exclusion by its own condition: a check or confirmation step, with no criterion or an undefined one, that no destructive or irreversible action depends on. v2 on the A005-sensitive probes: P3-01 clean 3/3, P3-02 unchanged 3/3, P3-03 P003 3/3, PR-07 A005 3/3 |
| B1's subject is the step, so §5's 「多次失败则升级处理」 can literally go to P003 | adversarial second defect | **resolved by B1v2**: its subject is 「检查或确认步骤」, which that example is not |
| Revised wording 「步骤缺少成功判据或缺少验证方式时…」 | adversarial revise | **not adopted**: it keeps the 「含义未定 → 本规则」 carve-out that failed on v1 |
| An undefined criterion on a read-only closing step (「确认…运行正常」) still gets A005/ERROR: the seam between si3 Q3 and M5 | adversarial open question 1 | **B1v2 covers it** (「判据含义未定（「确认无异常」）」). This extends M5 from a missing criterion to an undefined one when nothing destructive depends on it. Registered as P3-05 (`expect_basis: proposed`); decision 009 asks the maintainer to confirm the extension |
| P3-01's gap could reappear as CTC-S002 through category 5 | adversarial conflict 2 | **checked**: no v1 or v2 output on P3-01/P3-02 cites S002 |
| Which ID and severity a reported criterion gap carries in review | naturalness (on B1) | **unchanged**: P3-03 cites P003 3/3 on base, v1 and v2; PR-07 cites A005 3/3. B1v2 only says when not to report |
| R4-01's 「切换完成后」 forked on base (P003/WARNING, A005/ERROR) | adversarial other observation 2 | **recorded as open**: not a check step, so B1v2 does not decide it; a candidate probe for the next round |
| A destructive last step with no criterion and nothing after it is reported by no rule | adversarial other observation 3 | **recorded**: P003's bound already says so in rewrite; under B1v2 such a step is not a check step, so A005 still reaches it in review. Left as is |

## B2 — CTC-R004's exclusion (proposal 19, M4)

| finding | source | ruling |
| --- | --- | --- |
| 「可测量指标」 literally covers 「调到适当的上限」, pulling R004's own 「适当」 into A005 | adversarial revise | **accepted** (v3): 「运行指标」, and the clause names trigger conditions. Registered R4-08 (「调到适当的值」 must stay R004) |
| 「设限而未给出阈值」 reads as self-contradictory; 「程度」 is used in two senses | naturalness | **accepted** (v3): 「用程度词描述运行指标而未给出阈值的触发条件（「延迟较高时」）」, with 「都」 |
| §8 step 2's parenthesis names the remedy (阈值) as the excluded item | naturalness, highest priority | **accepted** (v3): 「CTC-R004 中按 CTC-A005 处理的说法」, which also stops re-listing the exclusion |
| Change words (「突增」「变慢」) | adversarial; decoder probe 2 (reads them as A005) | **registered** R4-09 (「响应变慢时」 → A005 under M4) |
| Severity inversion: 「必要时回滚」 is R004/WARNING while 「若干分钟」 is A005/ERROR | decoder probe 2 | **recorded**: it follows from R004 being 应 and A005 必须, which predates si4 (si3 already routed 「若干分钟」 to A005) |
| Whether 「合理」「适当」 on a metric stay R004 | naturalness design question | **decided by M4's line**: how much to act stays R004; a trigger condition on a metric is A005. R4-08 tests it |

## T2 — the merge authorisation

| finding | source | ruling |
| --- | --- | --- |
| The parenthesis matches the runs (PR-09 merges on a step cap 3/3; PC-01 keeps three steps on a character cap 3/3), D004, G-P-003 and §3 | adversarial accept; decoder probe 4 (a, c yes; b, d no) | **accepted** |
| 「步骤越少越好」 (no number, no 「合并」) no longer authorises a merge | adversarial cost | **recorded**: only instruction-following suffers; the checkpoint stays intact |
| A step cap the source already meets still counts as authorisation | naturalness | **recorded**: CTC-R001 still forbids a merge no rule needs |
| Weak fork on a character cap, since §3 lists a length cap among authorisable items | decoder probe 4 | **recorded**: the parenthesis names the two forms; PC-01 3/3 on base and v1 |

## T4 — 「明确边界」

| finding | source | ruling |
| --- | --- | --- |
| 「规则条文写明的」 can attach to 「更高优先级」 too | naturalness | **accepted** (v3): 「可被更高优先级推翻，也可被规则条文写明的边界推翻」 |
| T4 narrows what overrides 应: a caller instruction (「不要附加待确认」) is no longer a 「边界」 | adversarial | **recorded, not changed**: caller authorisations are governed by §3's closed list at every level (they also override 必须 rows such as S003 and S004), so the 应 definition does not need to name them |
| What 「更高优先级」 refers to (§2 ladder, 必须 rows, caller) | decoder probe 5 | **recorded as open**: predates si4 |

## C1 — the third-person frame (proposal 20)

| finding | source | ruling |
| --- | --- | --- |
| A cold reader now predicts the RG-15-style rewrite in tool descriptions, and leaves developer-guide prose and the agent's 「你可以」 alone | decoder probe 3 | **accepted**: this is proposal 20's test, which si3's second decode failed |
| 「同属此类」 stipulates a third-person frame into reader guidance; it is not addressing the reader | naturalness | **accepted** (v3): its own item in the 口语腔 list |
| The clause literally catches a usage restriction (「只有管理员账号可以调用此工具」) | adversarial revise | **accepted** (v3): 「以使用者作主语陈述功能的句式」. RG-12 keeps the restriction 3/3 on base and v1 |
| 「工具描述」 versus the strict scope's 「工具与函数描述」; CLI reference docs | adversarial other observation 1 | **recorded for the maintainer**: widening to functions is not a narrowing; RG-15 (a function) is rewritten 3/3 on every version |
| 「可以」 as a permission protected by S003 (output 「可用于…」) | decoder probe 3 | **recorded**: RG-08, RG-10, RG-15 drop the frame 3/3 with no permission reading in any run |

## F1, T1, T3

| finding | source | ruling |
| --- | --- | --- |
| F1 matches M2 and §5 | adversarial accept; decoder probe 6 (no fork) | **accepted** |
| F1: 「上下文不足以确定读法的歧义」 names the object of 「确定」 | naturalness | **recorded for the maintainer**: M2 approved the exact clause; the variant is offered at acceptance |
| 「上下文」 has two senses (§1 caller context; §5 and the description include the source) | decoder probe 6 | **recorded as open** |
| T1, T3 | adversarial accept; naturalness 5 and 5 | **accepted** |

## After v3: runs, self-hosting and the second cold decode

These rulings come from the v3–v5 probe runs, the self-hosting passes on v3, v4 and v5, and the second
cold decode of v3 (`decode-v3.yaml`, same role, candidate only). Each change is in `build.py`.

| finding | source | ruling |
| --- | --- | --- |
| 「CTC-R004 中按 CTC-A005 处理的说法」 read as 「anything R004 finds goes to A005」 | v3 run, R4-05 r1 (「按 CTC-R004 发现，按 §8 第 2 步转 CTC-A005」) | **reverted** (v4, B2b''): the parenthesis lists the excluded kinds by name again, naming the metric condition rather than the remedy. R4-05 R004 6/6 on v4 |
| The R003 defect item and the repair sentence both say 「以使用者作主语」 with one example | v3 self-hosting, CTC-R002, 2/2 | **accepted** (v4, C1d): the example stays on the defect item; the repair sentence keeps only the direct form. G-R-010 passes 4/4 on v4 and v5 (gold run plus three replicates); RG-08/10/15 3/3 |
| 「不以使用者作句子主语」 can be stretched to permissions and restrictions (「你可以」, 「只有管理员可以」) | second cold decode, probe 3 | **resolved by C1d**, which removes that clause. RG-16 6/6 on v4 after a 1/3 loss on v3; RG-12 3/3 on every version |
| An agent's 「你可以」 permission lost once | v3 run, RG-16 r1 | **replicated**: 6/6 kept on v4; no loss on v5 or v6 |
| A005's exclusion and P003's last sentence state two thresholds for raising a missing criterion | self-hosting v3 1/2, v4 2/2 | **accepted** (v5, P3x + B1v3): P003's bound is about an operation step's own criterion; check or confirmation steps go to A005; A005's pointer back to P003 is dropped. v5 self-hosting 0/2 |
| The 「（CTC-P003）」 pointer invites applying P003's 「其余步骤缺少判据不提出」 to a check that gates a destructive action | second cold decode, probe 1(d) | **resolved by v5**, which drops the pointer |
| §8 step 2's list omits P003's new routing to A005 | self-hosting v5 2/2 | **accepted** (v6, B2b3), as si3's v4 added R004's exclusion to the same list |
| G-S-001 failed once on v4 (a 「待确认」 item on 「延迟预算紧张」) | v4 full gold | **not a si4 regression**: base raises the same item 3/3 (and a second spurious one) in replicates; v5 2/3. The judge passed all three base runs. Recorded as an open over-reporting item |
| G-R-014 failed once on v4 (rendering) and once on v5 (causality) | full gold | **noise**: 3/3 pass on both base and v5 in replicates |
| 「适当的值」 could read as a missing parameter (A005) | second cold decode, probe 2 | **recorded**: R4-08 R004 3/3 on v3–v6 |
| 「更高优先级」 has three readings; a layer-2 应 and a layer-3 必须 in conflict have no stated way out | second cold decode, probe 4 | **recorded as open**: predates si4 |
| §5 does not say how review treats ambiguity the context resolves | second cold decode, probe 5 | **recorded as open**: predates si4 |
| 「条件允许」 cited as an undefined state (A005) | v6 runs, R4-05 2/9 (base 6/6; v3–v6 3/21) | **accepted** (v7, R4L): 「条件允许时」 joins R004's word list, as M4 named it. R4-10 (「时间允许时」) registered first as the generalisation check |
| A005's and P003's threshold (「破坏性或不可逆」) versus P004's guarded operations, which include state-changing ones | v7 self-hosting 2/2 | **recorded for the maintainer** (open proposal 26): B1 follows M5 and P003's existing wording; widening it reports more |
| T4 put 「规则条文」 in the §6 paragraph that says 「规则正文」 for the same text | v7 self-hosting r1 (reported apart in si3 v4 r2) | **accepted** (v8, T5): 「规则条文」, as §3 and §8 say; wording only |

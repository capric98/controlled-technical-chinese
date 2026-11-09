# si5 — rulings on the three independent reviews of candidate v1

Reviews: `adversarial.yaml` (semantic invariants, counterexamples), `decode.yaml` (cold reverse-decoding,
candidate only), `naturalness.yaml` (wording and over-control). All three are Opus 5.5 subagents with
disjoint inputs; none saw another's output, and the adversarial reviewer saw no v1 output. The orchestrator
(Opus 5.5) made the rulings. The human gate is the maintainer's review of decision 010.

As in si3 and si4, each counterexample the existing probes did not cover became a probe registered before
any output (`probes.yaml`: OR-06 and OR-06r after the decode and naturalness reviews; OR-07, OR-08, HR-01 and
HR-02 after the adversarial review). Text changes where a probe fails or a reviewer shows a reading defect
that a narrower wording removes without new requirements; scope changes go to the maintainer.

## N1, N2 — 规范强度 (M2)

| finding | source | ruling |
| --- | --- | --- |
| The rename changes no rule's meaning or level | adversarial accept; naturalness 5 and 4 | **accepted** |
| 「调整规范强度」 can be read as adjusting the skill's own rule levels (§6 级别) | naturalness; adversarial optional; si5 base self-hosting r1; decoder probe 3 (规范强度 is never defined apart from 级别) | **accepted** (v2): 「调整来源中的规范强度」, which anchors the authorisation in the source text |
| A literal 应→必须 swap turns 「不应」 into 「不必须」 | decoder probe 3 | **recorded**: predates si5; how an authorised strength change is applied is not in this round's scope |

## V1 — review-mode term variants (M7)

| finding | source | ruling |
| --- | --- | --- |
| Dropping 「它是一条」 lets 「按 CTC-T001 报告」 read as inheriting 「只有当它妨碍执行时」 from the preceding clause | adversarial revise | **accepted** (v2): 「review 模式下它是一条 CTC-T001 finding。」 |
| A T001 finding's suggestion may unify two terms the same paragraph says not to merge | naturalness | **resolved by context**: the paragraph's 「不明确时不合并」 governs; baseline TV-02 suggestions are already conditional (「如果作者确认三者指同一阶段，统一…」) |
| T001's trigger says 「同一概念」, the paragraph routes 「是否同指不明」 to it | v1 self-hosting r2 | **accepted as the explicit routing**: like §8's routing to A005, the paragraph names the ID for this case; recorded for self-hosting |
| Domain-distinct pairs (副本数／Pod) may be filed under T001; escalation is the reviewer's call | decoder probe 2 | **recorded**: §8's escalation rule is unchanged |
| Overlap with A005 when the two readings change the action (restart vs reload) | adversarial conflict 1 | **recorded**: §8 allows separate findings; no run double-reports (TV-01, TV-02 6/6 T001 only) |

## H1, H2 — the threshold's scope (M6)

| finding | source | ruling |
| --- | --- | --- |
| H1 has run support: a vague check that gates a restart is reported 3/3 (TH-01, TH-02) | adversarial | **accepted** |
| H2 has no supporting probe: every cited case is a check step (A005's route), and H2 widens P003's own-step bound, which exists to prevent chains of pending items | adversarial revise (keep H1, drop H2) | **for the maintainer**: M6 was asked with check-step evidence; whether it extends to P003's own-step bound is asked separately with HR-01/HR-02 data |
| H1's negative-condition-then-negative-result reads badly; a contrapositive matches P003 | naturalness | **accepted** (v2): 「…时，只有当破坏性、不可逆或改变外部状态的操作取决于它的结果，才提出或报告。」 |
| H2's 「、且」 nests two levels of 、 | naturalness | **moot if H2 is dropped**; otherwise 「，且」 |
| 「改变外部状态」 has no examples in A005 (config edits, notifications) | decoder 1(f); naturalness; adversarial | **recorded**: P004's list gives the examples; adding 「（见 CTC-P004）」 could import P004's trigger, so it is left |

## D1 — permissions and descriptions (M4, M5)

| finding | source | ruling |
| --- | --- | --- |
| A permission that waives a control the source requires (「须双人复核；情况紧急时，也可以先执行、事后补复核」) is logically an obligation with a vague trigger, which OR-04 must report | adversarial strongest counterexample | **accepted** (v2): 「…默认动作不变，且不免除来源规定的义务」. Registered OR-07 |
| A permission to perform a destructive action (「若磁盘紧张，也可以删除旧备份」) is exempt by the letter | decoder 1(g); naturalness; adversarial | **for the maintainer**: OR-06 shows base A005 3/3, v1 silent 3/3. M4 was asked with a benign permission |
| A 「现象」 section is pure description but governs the 「处理」 steps through the headings | adversarial | **registered** OR-08 |
| 「放宽…可以做的事」 is a weak collocation; 「后两种情形」 makes the reader count back; 「同样」 has no anchor | naturalness | **accepted** (v2): 「条件只放宽对操作者的限制…」「后两种情形即使缺少判据或阈值，也不按…」 |
| Bare R004 imperatives (「视情况暂停…」) may be swallowed by the permission exemption | adversarial | **checked**: R4-01 is R004 3/3 on v1 |
| R004 and §8 do not cross-reference the new §5 exception | adversarial | **recorded**: D1 names CTC-R004 itself |

## S1 — R005 and standalone warning blocks

| finding | source | ruling |
| --- | --- | --- |
| Gives P004's 「移动它属于 CTC-R005 违规」 a rule text; what is prohibited does not change | adversarial accept | **accepted** |
| The clause leaves out 「应」 | naturalness | **accepted** (v2): 「独立告警块应保持原位」 |
| A caller who asks to merge every note at the top: the part that cannot be done has no 「待确认」 channel | decoder 4(c) | **recorded as open**: predates si5 |

## Maintainer decisions after v1 (M8–M10)

The three questions marked **for the maintainer** above, and the G-S-001 regression that the v1 replicates
showed, were asked on 2026-11-09 with the v1 data (`probes/resolutions.yaml`):

- **M8** (destructive permission): the exemption does not cover it; OR-06 and OR-06r expect A005 and a
  「待确认」 item. v2's D1' adds 「所许可的也不是破坏性、不可逆或改变外部状态的操作」.
- **M9** (H2): kept. HR-01 (rewrite) and HR-02 (review) expect exactly one item, on the release step.
- **M10** (zero object): fixed this round. v2's Z1 adds the zero-anaphora sentence to CTC-P002; PR-13
  (「重启对应服务」) is the boundary and ZA-01 the probe.

## Second cold decode, of v2 (`decode-v2.yaml`)

The decoder read only `dev/prompts/si5-decode-v2.md` and the candidate. Its answers match the intended
behaviour on every probe: a benign permission is exempt (1(a)); a waiver (1(b)), a destructive permission
(1(c), 1(d)) and a 「现象」 section that the 「处理」 steps depend on (1(f)) are A005/ERROR; a pure description
is not reported (1(e)); the release step is P003 (1(g)); a closing check that nothing depends on is not
raised (1(h)); a recoverable omitted object stays omitted (2(a), 2(c)); a review-mode term variant is T001
with a suggestion conditional on co-reference (3).

| finding | source | ruling |
| --- | --- | --- |
| 「破坏性、不可逆或改变外部状态的操作」 is defined nowhere; P004's list is examples. It now gates three places (§5's exemption, A005's check-step bound, P003's own-step bound); forks 1(a) (does the exemption test the increment or the whole permitted action), 1(d) (a config change that shortens retention) and the side note on 2(c) (a backup step before a destructive one is not itself destructive) all come from it | decoder 1(a), 1(d), 2(c) | **recorded as open proposal 27**. The runs follow the intended reading (OR-01, OR-02 3/3 exempt; OR-06 3/3 reported; HR-01, HR-02 3/3). A definition decides what counts (config edits, backups, notifications), which is a scope question for the maintainer and needs its own probes |
| The text says when an exempt item is not raised, but not that a failed exemption must then be raised | decoder 1(b) | **recorded as open proposal 28**. A failed exemption falls back to A005 and R004 as they stand; OR-07 is reported 3/3 on v2. No failing run |
| 「情况紧急时」 can be read as an R004 timing word, like 「必要时」 | decoder 1(b) reading C (rejected for 「线上故障」) | **recorded as open proposal 29** with the OR-07 runs: base A005, R004, A005; v2 A005, A005+R004, R004. The fork predates si5; every run reports it |
| 「指定改写目标」 is undefined and could be read as a catch-all authorisation; 「把要求放宽一些」 names neither the rules nor the target strength | decoder 4(a) | **recorded as open proposal 30**. Predates si5; N1' narrows the strength authorisation to the source text but does not touch the list's other items |
| A term difference that blocks execution is category 5 (CTC-S002, 必须) in rewrite but T001 (应) in review | decoder 3 | **recorded as open proposal 31**. M7 chose T001 for review knowing the runtime behaviour; §8's escalation lets a finding name the different action and report ERROR, which the decoder notes. Whether review should mirror rewrite's split is a product decision |
| 「现象」 and 「处理」 are sibling headings, so CTC-L001's subtree rule does not by itself make the symptom a condition | decoder 1(f) | **no change**: D1' exempts text that 「不要求读者据此行动」, which a troubleshooting symptom fails; OR-08 3/3 on v2 |
| 「扩容 `worker`」 gives no target count | decoder 1(f) side note | **recorded**: outside the probe; the gold has no case on it |
| 「重启对应服务」 after 「修改 `nginx.conf`」 may be written out as 「重启 Nginx」 | decoder 2(b) | **consistent with P002**: the file name is context evidence. PR-13 (review) reports P002 3/3 |

## Runs after v2

- **G-T-101** failed one v2 replicate (r3: the co-reference item named 灰度发布 and 金丝雀发布 but not 小流量验证).
  Six more replicates each: v2 6/6, base 6/6. Totals v2 8/9 plus the full run, base 9/9; the difference is one
  run and is recorded, not acted on.
- **TV-01** missed once in nine v2 runs (r3 reported no violation); base 6/6, v1 3/3. Recorded.
- **G-S-001** inserts 「将索引重建」 on v2 in 1/7 replicates plus 0/1 full run, as on base (1/7); v1 4/7.
- **OR-07** is reported in every v2 run; the rule ID splits (above). base 2/3 and v2 1/3 under the registered
  「A005 only」 expectation.

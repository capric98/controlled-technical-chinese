# si2 — rulings on the three independent reviews of candidate `full`

Reviews: `adversarial.yaml` (semantic invariants, counterexamples), `decode.yaml` (cold reverse-decoding,
candidate only), `naturalness.yaml` (wording and over-control). All three are Opus 5.5 subagents with
disjoint inputs; none saw another's output. Rulings by the orchestrator (Opus 5.5). The human gate is the
user's review of decision 007.

## E1 — review routes the rows' own "转 CTC-A005" cases to CTC-A005

| finding | source | ruling |
| --- | --- | --- |
| Accept as clarification; the three rows already route undecidable cases to A005 | adversarial | **accepted** |
| Undecidable P002/A003 gaps now default to ERROR without the §8 risk-field condition; build.py did not say so | adversarial | **accepted** — stated as a consequence in decision 007 |
| E1 does not resolve PR-07's A005/R004 fork; R004's word list is the cause | adversarial | **accepted** — PR-07 is not credited to E1; the R004 list stays open proposal 5 |
| 「引用 CTC-A005」 reads three ways: replace the ID, cite both, file two findings | naturalness, decoder | **accepted** — v2: 「finding 的规则字段填 CTC-A005，不另列原规则」 |
| 「情形……引用」 has a situation doing the citing; 「规则行」 is a new term | naturalness | **accepted** — v2 uses 「规则条文」 and makes the finding the subject |
| A005's ERROR-only mapping contradicts decision 003 §1's WARNING branch | adversarial | **rejected as a si2 issue** — decision 005 C2 deleted that branch deliberately; the reviewer had not read 005 |
| E1 lets a missing success criterion on a non-destructive step reach ERROR via "P002 → A005", bypassing CTC-P003's bound | adversarial (marked contestable) | **recorded, not changed** — the PR-01 locus has two readings that imply different checks (`vault` vs `gateway`), which is A005 on its own terms; the general P003/A005 overlap predates si2 and is open proposal 15 |

## E2 — CTC-P002 boundary for named objects without instance-level detail

| finding | source | ruling |
| --- | --- | --- |
| 「对应服务」 could count as a written object, so E2 would suppress P002 exactly where the row names it (PR-14 fail_if) | adversarial (strongest), decoder | **accepted** — v2: 「具体对象」 and 「「相关配置」「对应服务」这类说法不算写出对象」 |
| The exception names only multiple *objects*; multiple namespaces/environments for one object stay silent on a destructive step | adversarial, naturalness | **accepted** — v2: 「在对象或这些层级上给出了多个候选时除外」; probe PR-15 added |
| The exempt list (实例、路径、命名空间) does not match the row's own 节点、环境、命名空间 | naturalness | **accepted** — v2 lists 实例、节点、环境、路径或命名空间; the base-run over-flags in PR-03 include environment and node |
| Whether the exemption also stops an A005 report of the same gap | decoder | **accepted** — v2: 「也不因此按 CTC-A005 报告」; the ablation showed E1 without E2 converting the G-R-007 over-flag into two A005 ERRORs |
| 「就算」 reads as "even if"; 「它」 has two antecedents; 「可选」 reads as "optional" | naturalness | **accepted** — v2 rewords |
| A heading that already selects one of two candidates still fires P002 | adversarial | **recorded, not changed** — the baseline has the same false positive, and fixing it would widen the exemption beyond the evidence |

## E3 — register in error, alert and status text

| finding | source | ruling |
| --- | --- | --- |
| Only removing 「糟糕！」 has a failing case; 「口语语气词（「啦」）」 has none | adversarial | **accepted** — v2 drops 语气词 entirely |
| Sentence-final 「吧」 can carry a guess; deleting it turns a guess into a cause (S003/S006) | adversarial, naturalness | **accepted** — removed with 语气词; probe PR-18 added |
| 「了」 in 「磁盘快满了」 could be "repaired" to 「磁盘已满」 | naturalness | **accepted** — removed with 语气词 |
| The trigger catches a reply quoted inside an agent instruction | adversarial | **accepted** — v2: 「目标文本是告警、错误信息或状态提示」; probe PR-17 added |
| 「危险！」「警告！」 could be stripped as interjections | naturalness | **accepted as a boundary test, no text** — probe PR-16; text is added only if the probe fails |
| 「情绪化感叹与口语语气词」 reads as conjunctive | adversarial | **accepted** — moot after dropping 语气词; probe PR-19 tests a bare 「糟糕！」 |
| E3b's hedge clause presupposes a 语气词 trigger | adversarial | **accepted** — v2 licenses only deleting the interjection (「删去该感叹」), so it touches no hedge, and E3b is dropped |
| Rename: 「反译文腔与口语化」 parses as "anti-translationese, and colloquial" | naturalness | **accepted** — v2: 「反译文腔与情绪化」 |
| A product's deliberately friendly tone is layer 5, so R003 (layer 4) overrides it | naturalness | **recorded** — the trigger is limited to error, alert and status text and to deletion of the interjection; the scope decision belongs to the human gate |
| G-R-011's gold moves the 「好像」 hedge from the failure to the cause | adversarial | **recorded** — gold-case question, not a rule change; v2 does not license touching 「好像」 |

## Decoder forks that predate si2

Of the decoder's seven forked probes, these concern text si2 did not change and are left as open proposals:
A005 versus category 5 (CTC-S002) for missing information; CTC-A005's 「缺少……判据」 versus CTC-P003's
bound; 「保持原表述」 scope; 「不再补写」 as prohibition or non-requirement; R003's 「过长」 (open proposal 2);
whether the natural-passive cases are exhaustive; §7 step 6 read as an unconditional naturalisation pass.

## After v2: what the runs and the second decode changed

| version | change | trigger | outcome |
| --- | --- | --- | --- |
| v3 | R003: 「目标文本本身是…」 and 「其他文本中引述或规定的提示文字不在此列」 | PR-17: v2 deleted 「糟糕！」 from a reply quoted inside an agent instruction, 3/3 | PR-17 3/3 unchanged under v3 |
| v4 | §8: 「按第 2 步转为 CTC-A005 的 finding 按 CTC-A005 定级，不算升级」 (E1b) | v3 self-hosting finding 7; adversarial conflict 1 | accepted; no behaviour change expected or seen on PR-01/03/07/13/15 |
| v4 | P002: 「出现多个可能的取值」 for 「给出了多个候选」 | decode-v2 probe 2 reading B (only alternatives named for the step) | PR-15 3/3 A005 under v4 |
| v4 | R003: exclude 「警示标记（「危险！」）与语气词」 | decode-v2 probes 3A and 7 (「啦」); naturalness review (「危险！」) | **withdrawn in v5**: under v4, G-R-009 kept 「哦」「帮忙…一下」 verbatim in an agent instruction that the single base and v3 runs had cleaned. *Correction:* the later replicates show base also leaves it unchanged in 3 of 4 runs, so this attribution was not supported; E3 as a whole was withdrawn afterwards on the G-R-010 evidence (below) |
| v5 | R003: exclude only quoted or specified prompt text and 警示标记 | G-R-009 regression under v4 | see the v5 ablation in `eval/reports/si2-summary.md` |

The decode-v2 「啦」 fork therefore stays open: R003 neither licenses nor forbids removing modal particles, and
models stretch 「中文技术写作的常规表达」 to cover them, which G-R-009 rewards. Writing that licence down is a
register rule for agent instructions, which needs its own failing case and its 「吧」 boundary (PR-18). It is
open proposal 16, not part of si2.

## Final ruling on E3: withdrawn

Replicated runs (one gold run plus three replicates per cell; Opus judge):

| case | base | with E3 (v3, v4, v5 pooled) | v5 without E3 |
| --- | --- | --- | --- |
| G-R-011 (error message with 「糟糕！」) | 1/4 | 9/9 | — |
| G-R-010 (tool description register) | 3/4 | 2/9 | 3/3 |
| G-R-009 (agent instruction register) | 1/4 | 2/6 | 1/3 |
| G-S-001 (over-edit trap) | 2/4 | 2/6 | 3/3 |

Every E3 wording fixed G-R-011 and cost G-R-010 at the same ladder layer (layer 4). Without E3: 6/7 on
G-R-010; with it: 2/9 (Fisher exact, two-sided, p ≈ 0.04). The outputs show the mechanism: with E3 the model
keeps 「这个工具允许调用者获取」 or 「调用者可通过该工具获取」, where base and no-E3 rewrite to 「该工具用于获取」 or
「该工具可获取」. Adding a narrow, enumerated branch to R003 made the whole row read as closed; base cleans
register only by stretching R003 past its text.

**Ruling.** E3 is withdrawn. G-R-009, G-R-010 and G-R-011 share one gap: no rule licenses register cleanup in
error, tool-description or agent-instruction text, so the result depends on how far each run stretches R003.
A single interjection clause trades one case for another. The gap is open proposal 16 and needs a rule
designed against all three cases together, with PR-16–PR-19 as its boundary set.

G-R-009 and G-S-001 are not attributed to E3: both fail about as often on base as on any candidate.

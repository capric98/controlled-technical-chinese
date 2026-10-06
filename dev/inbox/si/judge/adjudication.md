# Adjudication of judge claims (orchestrator, label-blind)

Written before unblinding. The orchestrator is Claude Fable 5.1 and is one of the two models under comparison; every ruling below is to be reviewed by a label-blind Opus 5.5 subagent, and disagreements are recorded.

## Pre-registered rules

- A `vs_baseline` claim is **confirmed** iff the quoted baseline assertion (a requirement, prohibition, exception, condition, threshold, category, field or step) cannot be found in the candidate with the same level, condition and scope; **rejected** if the candidate carries it elsewhere (including at the level of the frozen rule row when the baseline prose conflicted with that row); **style-only** if only wording, rationale or an illustrative example changed.
- **Example-correction**: a change to a worked example's expected output that brings it into agreement with the frozen rule row it illustrates, where the baseline example contradicted that row. Not a loss; not counted in criterion 1. (Both candidates made such corrections; the judges classified them as `altered` at ERROR or WARNING.)
- A `selfhost` finding is **confirmed** iff the defect exists in the candidate text; severity follows the level of the rule that most directly describes the defect (a two-readings-different-behaviour defect is CTC-A005 → ERROR). `also_in_baseline` marks inherited defects.
- A `fork` is confirmed iff the two readings lead to different actions.
- Control document C: the three seeded defects are s1 (§12 L004 正例 → 「超过 90%」), s2 (category 7 deleted, 七类→六类), s3 (CTC-L003 sentence deleted). Findings on C outside the seeds that the judge marked `also_in_baseline` are findings about the baseline, not false positives.
- Where two judges report the same defect it is pooled under one D-id and counted once.

## Rulings by claim

### C1 — opus · doc A · selfhost
- id: X-F1
- rule: CTC-A005
- severity: ERROR
- locus: §5：「规范性指令中，义务的强度由「最好」「尽量」「尽可能」这类无判据词承担时，报告其可能的两种以上强度并在第四栏给出建议，然后停手；「必要时」「适当」「合理」承担的是判定条件而非强度，只按第 4 类提出（CTC-R004）」；§6 CTC-R004：「规范性指令（agent 指令、SOP、策略、门禁条件）的判定条件由无判据词承担时——「尽量」「尽可能」「最好」「适当」「必要时」「合理」——」
- problem: 两处对同一批词给出不同归类。§5 把「最好」「尽量」「尽可能」划为承担强度（按 §5 情态模糊处理，填第四栏建议，review 下按「所引规则」定级），只把「必要时」「适当」「合理」划入 CTC-R004；CTC-R004 正文却把六个词都列为承担判定条件的无判据词。对「尽量在窗口内回滚」这类句子，文本同时支持两种处理。按 §8 第 1 步，文内两处陈述对同一情形要求不同行为，按 CTC-A005 报告。
- suggestion: 在 CTC-R004 的词表中删去「尽量」「尽可能」「最好」，或在其后加一句：「其中「最好」「尽量」「尽可能」承担强度时按 §5 的情态模糊处理」；并在 §5 写明情态模糊在 review 模式下所引的规则 ID。
- also_in_baseline: True
- **ruling:** confirmed (ERROR) · pooled as D-A1
- **reason:** A §5 把 R004 六词分成「承担强度」三词与「承担判定条件」三词，而 R004 行仍把六词并列为判定条件词；对「尽量在窗口内回滚」文本同时支持「报强度并填第四栏」与「只按第 4 类提出」两种处理。分叉由 A 的拆分新造成（基线对六词一视同仁），按 A005 计 ERROR；行为差异限于「待确认」行内容与第四栏。

### C2 — opus · doc A · vs_baseline
- type: strengthened
- severity: WARNING
- baseline_quote: strict：「条件、前提、例外、守护条件与成功判据不得为求简洁删除。」；standard：「不得 — 以简洁为名删除条件、例外、阈值、默认值或受保护标记」
- doc_quote: §3：「任何模式下都不得以简洁或长度为名删除条件、前提、例外、守护条件、成功判据、阈值、默认值或受保护标记（CTC-S001、CTC-S005）。」
- why: 基线两份清单分属 strict 与 standard；X 合并为一份并扩展到所有模式，还加入「长度」。standard 下的前提、守护条件、成功判据，strict 下的阈值、默认值、标记，都变为显式禁删。多数情形 CTC-S001 本已覆盖，所以只是可能改变行为。
- **ruling:** rejected
- **reason:** 并集已由 S001 行（全模式、必须）覆盖：「长度上限不授权删除任何条件、例外、阈值、告警或失败分支」；无新增禁止。

### C3 — opus · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 「**不得升格** — 体例或地区偏好不得为赢得争论而升格为语义规则」
- doc_quote: 「**不得升格** — 体例或地区偏好不得升格为语义规则」
- why: 删去目的状语「为赢得争论而」，禁止范围不再受目的限定；实际执行不变。
- **ruling:** style-only
- **reason:** 删去目的状语，执行不变（评审自述）。

### C4 — opus · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 「5. 执行所需、而来源与上下文都未提供的信息（CTC-S002）——缺失信息一律归第 5 类，不论是哪条规则先发现它」
- doc_quote: 「5. 执行所需、而来源与上下文都未提供的信息；不属于第 2–4 类的缺失信息一律归本类，不论是哪条规则先发现它（CTC-S002）」
- why: 基线把全部缺失信息归第 5 类，与第 2 类（缺成功判据）、第 3 类（缺触发条件）、第 4 类（缺判据）重叠；X 把第 2–4 类排除在外。缺成功判据在 review 中所引的规则从 CTC-S002（ERROR）变为 CTC-P003（WARNING）。
- **ruling:** rejected
- **reason:** 基线「缺失信息一律归第 5 类」与第 2–4 类的存在及冻结的 P003 行（其余步骤缺判据不提出）自相矛盾；A 按冻结行读法收窄。B 做了同一改动（C91），不区分候选。

### C5 — opus · doc A · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: absent
- doc_quote: 「review 模式下它就是 finding 的「规则」字段，缺失信息的规则 ID 与其所属类别括注的规则一致。」
- why: 新增 review 规则字段的取值规则。缺失信息类 finding 的规则 ID，进而严重级别，由类别括注决定，不再由最先发现它的规则（如 CTC-A005）决定。
- **ruling:** confirmed (WARNING) · pooled as D-A4
- **reason:** 新增 review「规则」字段取值规则（缺失信息按类别括注的规则 ID），基线无此规则、规则行也推不出；它裁决了基线中 A005/S002 的分叉，属语义新增。

### C6 — opus · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 「- 尽快回滚 | 「尽快」承担义务，强度未定 | 作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认」
- doc_quote: 「- 最好在窗口内回滚 | 「最好」承担义务，可读作「应在窗口内回滚」或「可以在窗口内回滚」 | 作者意图的道义强度 | 建议按前者确认」
- why: 示例换词：竞争读法从问题栏移到第二栏，强度对从（必须／应）变为（应／可以）。格式与规则不变。
- **ruling:** style-only
- **reason:** 示例换词，格式与规则不变。

### C7 — opus · doc A · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: §4：「本节列出返回之前必须逐项验证的属性……任一项出现偏离都是一处 finding，其严重级别由 §7 中该行所引规则的级别决定」
- doc_quote: absent
- why: X 删去 §4 语义不变量表及其导语。逐项核对的要求保存在 §7 第 7 步，但「偏离即 finding、按行定级」这条断言没有保留；改写模式下，偏离在 X 中只触发修复再返回。这同时消除了基线里与 §3「改写没有可分级的 finding」的冲突。
- **ruling:** rejected
- **reason:** 可由 §8 第 2 步「每条违规确定唯一的规则 ID」+ 级别映射还原：任何规则违反都是按该规则级别定级的 finding。

### C8 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §4 表「破坏后的后果」栏（例：「按换算值填入以固定单位定义的配置项，量级错三个数量级」「「仅用于测试环境」被拍平后，清空缓存在生产环境获得授权」）
- doc_quote: absent
- why: 这是理据栏，不是要求；各行对应的规则仍在规则表中。
- **ruling:** style-only
- **reason:** 「破坏后的后果」是理据栏，不是要求；各行规则仍在规则表。

### C9 — opus · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: §5：「标题、列表层级、表格单元格与告警块所建立的条件管辖其子树，这属于条件保持，按 CTC-L001 判定。」
- doc_quote: §4：「标题、列表层级与表格单元格建立的条件管辖其子树（CTC-L001），独立告警块管辖它所依附的整个流程（CTC-P004）」
- why: 告警块的规则 ID 从 CTC-L001 改为 CTC-P004，管辖范围从「子树」改为「整个流程」，与基线 CTC-P004 正文一致。两条规则都是「必须」，严重级别不变，但 review finding 的规则字段会不同。
- **ruling:** rejected
- **reason:** 基线同时含 §5「告警块…管辖其子树（L001）」与 P004 行「独立告警块管辖它所依附的整个流程」两种说法；L001 行本身不提告警块。A 按冻结的 P004 行统一，属冲突消除而非丢失。

### C10 — opus · doc A · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: §6：「**上下文能确定读法时，必须消歧**，并且所选读法必须有来源或上下文证据。」
- doc_quote: §5：「**上下文能确定读法时，按所触发的规则消歧**（CTC-A001–A004、CTC-P002 等），并且所选读法必须有来源或上下文证据。」
- why: 消歧义务从统一的「必须」改为按所触发规则的级别；CTC-A003 与 CTC-P002 为「应」，可被推翻。与规则表一致。
- **ruling:** rejected
- **reason:** 基线散文「必须消歧」与冻结的 A003/P002「应」级冲突；A 按规则行级别处理。A001/A002/A004 仍为必须。

### C11 — opus · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: §6：「3. review 模式作为一条 finding，严重级别为 ERROR。」
- doc_quote: §5：「review 模式下作为一条 finding 报告，严重级别按所引规则的级别（§8）。」
- why: 固定 ERROR 改为按级别映射。所引为 CTC-A005 时结果仍是 ERROR；所引为 CTC-R004 等「应」级规则时变为 WARNING。
- **ruling:** rejected
- **reason:** A005 类 finding 仍为 ERROR（必须）；只有经 R004 路由的情形按冻结映射变 WARNING。005 C2 删除的是对 A005 的降级分支，不涉及 R004。

### C12 — opus · doc A · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: §6：「规范性指令中由无判据词（见 CTC-R004）承担义务的条件，必须报告其可能的两种以上强度并给出建议，然后停手。」
- doc_quote: §5：「义务的强度由「最好」「尽量」「尽可能」这类无判据词承担时，报告其可能的两种以上强度并在第四栏给出建议，然后停手；「必要时」「适当」「合理」承担的是判定条件而非强度，只按第 4 类提出（CTC-R004）。」
- why: 强度报告与建议的适用范围从 CTC-R004 全部六个词收窄为三个。「必要时」「适当」「合理」不再给出强度与建议，只报缺失判据，第四栏也不填。基线这里本身有两读，所以只是可能改变行为。
- **ruling:** confirmed (WARNING) · pooled as D-A2
- **reason:** 基线要求「由无判据词（见 R004）承担义务的条件」一律报告两种以上强度并给建议；A 只对最好／尽量／尽可能保留该要求，对必要时／适当／合理改为只按第 4 类提出。基线要求对条件词确实难以执行，但该收窄不能从冻结的 R004 行推出。

### C13 — opus · doc A · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: §7：「级别与严重级别一一对应：**必须** = 违反即语义错误（ERROR）；**应** = ……（WARNING）；**可以** = 许可（STYLE）。」
- doc_quote: §6：「规则正文中的「必须」「不得」表达该规则的要求与禁止，不改变该栏的级别。级别到严重级别的映射及其唯一的升级例外见 §8。」
- why: 新增解释规则：「应」级规则正文里的「必须」（如 CTC-P003「必须仍是继续的前提」）不得据以按 ERROR 定级。
- **ruling:** style-only
- **reason:** 「规则正文中的必须／不得不改变级别栏的级别」是对既有结构的说明；基线「级别与严重级别一一对应」「没有其他升级」已蕴含。

### C14 — opus · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: CTC-P003：「不得虚构验收标准」；「否则每份正常的流程文档都会产生成串的未决项」
- doc_quote: CTC-P003：「不得虚构判据」；「以免正常的流程文档产生成串的未决项」
- why: 规则行措辞差异，只涉及术语与理据句：禁止对象同指，理据句去掉了全称量化「每份」。触发、要求、禁止与例外都不变。除此之外，29 条规则行与基线逐字一致。
- **ruling:** style-only
- **reason:** P003 行两处措辞：验收标准→判据（T001 统一）；理据句去掉「每份…都会」的全称经验断言（S002 动机）。触发、要求、禁止、例外不变。

### C15 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §8 第 3 条：「**不得一刀切禁用被动。** 受限制的是删除施事（CTC-A001），不是使用被动。」
- doc_quote: absent
- why: 条目删除；CTC-R003「被动用于突出受事、施事未知或施事已在同句给出时是自然的技术表述」仍覆盖其边界。
- **ruling:** style-only
- **reason:** 「不得做的事」条目删除；每条断言在对应规则行仍可还原（R003 被动边界、R002/R005 拆分、R002 多执行者、P001、S006/T002/S004/A002/§5/R001）。示例随条目一起删除。

### C16 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §8 第 12 条：「**不得把无歧义的并列拆成编号分支。** 「检查磁盘空间和 inode 使用率。」不必拆成两条。」
- doc_quote: absent
- why: 条目删除；CTC-R002（机械拆分）与 CTC-R005（列表项数）间接覆盖。
- **ruling:** style-only
- **reason:** 「不得做的事」条目删除；每条断言在对应规则行仍可还原（R003 被动边界、R002/R005 拆分、R002 多执行者、P001、S006/T002/S004/A002/§5/R001）。示例随条目一起删除。

### C17 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §8 第 1 条：「汉语话题链承前省略主语是正常且首选的。……只有多角色交替执行时才补主语。」
- doc_quote: absent
- why: 偏好断言与边界句删除；边界已在 CTC-R002「多执行者交替出现时重复主语有消歧价值」中。
- **ruling:** style-only
- **reason:** 「不得做的事」条目删除；每条断言在对应规则行仍可还原（R003 被动边界、R002/R005 拆分、R002 多执行者、P001、S006/T002/S004/A002/§5/R001）。示例随条目一起删除。

### C18 — opus · doc A · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: §8 第 1 条：「应写成「打开控制台后，点击「设置」修改端口。」」
- doc_quote: §9 第 1 条：「写成「用户打开控制台后，点击设置修改端口。」」
- why: 示范输出改变：基线删去全部「用户」并给「设置」加引号，X 保留一次「用户」且不加引号。照示例执行的行为不同。方向与 CTC-A001 对齐，但仍属执行行为变化。
- **ruling:** example-correction · pooled as X-A001
- **reason:** 示例期望输出改变（保留一次「用户」），方向与冻结的 A001 行一致；基线示例删光唯一执行者与 A001 行矛盾。不是断言丢失，不计入第 1 判据。B 做了同一改动（C100）。

### C19 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §8 第 2 条：「「停止写入。等待。检查复制延迟。执行切换。」应写成「停止写入，等待复制延迟归零后执行切换。」」
- doc_quote: absent
- why: 示例删除；「不得一句一动词」本身并入 X §9 第 1 条。被删示例原本补出了来源没有的判据。
- **ruling:** style-only
- **reason:** 「不得做的事」条目删除；每条断言在对应规则行仍可还原（R003 被动边界、R002/R005 拆分、R002 多执行者、P001、S006/T002/S004/A002/§5/R001）。示例随条目一起删除。

### C20 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §8 第 5、6、7、10、13、15 条（强加「因此」、统一近义词、换算单位、展开指代、理论两解报错、改写未触发文本）及「**原样返回来源是一个合法的输出。**」
- doc_quote: absent
- why: 按「多处出现只保留一处不算 lost」的口径，这些断言分别保存在 CTC-S006、CTC-T002、CTC-S004、CTC-A002、§5「不算真歧义」、CTC-R001 中，没有独立断言丢失。本条只记录清单条目与示例减少这一事实。
- **ruling:** style-only
- **reason:** 「不得做的事」条目删除；每条断言在对应规则行仍可还原（R003 被动边界、R002/R005 拆分、R002 多执行者、P001、S006/T002/S004/A002/§5/R001）。示例随条目一起删除。

### C21 — opus · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: §9 第 1 步：「标出代码、命令、路径、标识符、字段名、URL、状态码、占位符、数值与单位。这些进入不可改集合。」
- doc_quote: §7 第 1 步：「标出受保护标记，进入保护集（§4）；数值与单位另行登记，按 §4 保持表面形式。」
- why: 数值不再称为「不可改」，而是按表面形式保持，这样全角数字半角化与授权换算仍可做，与基线 §5 一致。
- **ruling:** style-only
- **reason:** 流程步骤措辞与骨架项补齐（指代先行词基线第 7 步已比对）。

### C22 — opus · doc A · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: §9 第 2 步：「……量化论域、因果强度、否定作用域。」
- doc_quote: §7 第 2 步：「……量化论域、因果强度、否定作用域、指代先行词。」
- why: 骨架增加指代先行词；基线第 7 步已比对指代，属于补齐。
- **ruling:** style-only
- **reason:** 流程步骤措辞与骨架项补齐（指代先行词基线第 7 步已比对）。

### C23 — opus · doc A · vs_baseline
- type: strengthened
- severity: WARNING
- baseline_quote: §9 第 7 步：「重新抽取 (情态, 数值, 量化, 因果, 否定作用域, 施事, 指代, 条件, 时序, 受保护标记) 并与第 2 步的记录逐项比较」；§11：「任一项为「否」，先修复再返回。」
- doc_quote: §7 第 7 步：「重新抽取第 1、2 步登记的全部项并逐项比较，S、A、P、T、L 五族每条规则的保持项都须与来源相同；同时核对……（CTC-R002、CTC-R003）……（CTC-R001）。任一项不成立，先修复再返回；调用方已授权的改动不计为不成立。」
- why: 核对集合从 10 项扩大到五族全部保持项，加入了逻辑方向（L002）、原子性分组（P001）、判据与守护等。新增的授权豁免与基线「授权改变的是允许做什么」一致。
- **ruling:** rejected
- **reason:** 核对集合扩大到五族全部保持项：基线 §4 表、§9 第 7 步、§11 自检三处并集已覆盖（含 L002、P001）；合并不是加强。

### C24 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §11 自检 12 问
- doc_quote: absent
- why: 整节删除；各问并入 §7 第 7 步（「全部项」加 R001、R002、R003 核对），第 12 问由第 8 步「按输出契约返回」覆盖。
- **ruling:** style-only
- **reason:** 自检并入 §7 第 7 步；已逐项核实 R001/R002/R003 核对与第 8 步的输出契约都在。

### C25 — opus · doc A · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: absent
- doc_quote: §8 第 1 步：「被审文本没有独立来源时……以被审文本自身为来源：来源与输出之间的不变量无从违反，只报告被审文本自身可观测的违规……；文内两处陈述对同一情形要求不同行为时，按 CTC-A005 报告，位置引用两处。」
- why: 新增无来源审阅的判定口径，并把文内冲突指派给 CTC-A005。审计与自审的 finding 集合与规则字段因此改变。
- **ruling:** confirmed (WARNING) · pooled as D-A5
- **reason:** 新增无独立来源时的审阅口径（以被审文本自身为来源；文内冲突按 A005 报告并引用两处）。基线沉默；不能从规则行推出。本轨道 r1 曾以「改语义」拒绝，r2 应用。

### C26 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §10 六字段格式示例（「规则：CTC-S003 / 严重级别：ERROR / 位置：「确认数据备份完成……」」）
- doc_quote: absent
- why: 格式示例删除；六个字段名仍在 X §8 第 3 步列出。
- **ruling:** style-only
- **reason:** 六字段示例块删除，字段名保留在 §8 第 3 步。

### C27 — opus · doc A · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: §10：「- **ERROR** — 语义损坏、不安全的歧义、受保护标记突变，或硬不变量被违反。- **WARNING** — 可能的歧义或规则风险，需要人工判断。- **STYLE** — 不影响语义的自然度或一致性问题。」
- doc_quote: absent
- why: 描述性定级依据删除，只剩级别映射。基线下可能按描述定为 STYLE 的「应」级自然度 finding（CTC-R003），在 X 中只能是 WARNING。
- **ruling:** rejected
- **reason:** 描述性定级依据可由映射还原；描述本身（STYLE = 自然度问题）与冻结映射（R002/R003 为应→WARNING）冲突，删除消除冲突。

### C28 — opus · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: §10：「未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察。」
- doc_quote: §8：「没有 ERROR 或 WARNING 级 finding 时返回「未发现违规」，其后最多列三条 STYLE 级 finding。」
- why: 触发条件从「未发现问题」改为「没有 ERROR 或 WARNING」。只有 STYLE finding 时，X 明确返回「未发现违规」并最多列三条。
- **ruling:** confirmed (WARNING) · pooled as D-A6
- **reason:** 「未发现问题」被具体化为「没有 ERROR 或 WARNING 级 finding」，为基线的一处歧义选定了读法。B 的 C97 在实质上选了同一方向（STYLE 项带规则 ID），两候选对称。

### C29 — opus · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: §5：「一个字符串出现在代码标记内（行内代码、围栏代码块含语言标注）」
- doc_quote: §4：「一个字符串出现在代码标记内（行内代码；围栏代码块，不论是否带语言标注）」
- why: 澄清无语言标注的围栏块同样受保护；基线也可读作同义。
- **ruling:** style-only
- **reason:** 无语言标注围栏块的澄清与 S005 行一致；理据句改为「本技能假定」只是措辞。

### C30 — opus · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: §5：「技术数值会被直接复制进单位由字段名固定的配置项，而文档不保证标明哪些值是这样的。」
- doc_quote: §4：「本技能假定技术数值会被直接复制进单位由字段名固定的配置项，且文档不标明哪些值是这样的」
- why: 事实断言改为「本技能假定」，「不保证标明」改为「不标明」；只是理据措辞。
- **ruling:** style-only
- **reason:** 无语言标注围栏块的澄清与 S005 行一致；理据句改为「本技能假定」只是措辞。

### C31 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §12 情态强化示例（「如果你想在生产环境中部署该服务，请确保你已经配置了环境变量。」）
- doc_quote: absent
- why: 示例删除；CTC-S003 正文保留「请→须」为违规。
- **ruling:** style-only
- **reason:** 六个示例删除（8 个中删 6）；各示例演示的断言在对应规则行保留。记为显著的教学内容缩减，不计为断言丢失。

### C32 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §12 例外删除示例（「所有实例都需重启，只读副本除外。」）
- doc_quote: absent
- why: 示例删除；CTC-L001 正文保留「只读副本除外」。
- **ruling:** style-only
- **reason:** 六个示例删除（8 个中删 6）；各示例演示的断言在对应规则行保留。记为显著的教学内容缩减，不计为断言丢失。

### C33 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §12 阈值边界翻转示例（「磁盘用量达到 90% 时触发告警。」）
- doc_quote: absent
- why: 示例删除；CTC-L004 正文保留「达到 N 含 N」。
- **ruling:** style-only
- **reason:** 六个示例删除（8 个中删 6）；各示例演示的断言在对应规则行保留。记为显著的教学内容缩减，不计为断言丢失。

### C34 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §12 静默消歧示例（「隔离受感染的主机和网关通信」及其「待确认」行）
- doc_quote: absent
- why: 示例删除；竞争读法写入「待确认」的格式演示随之减少，规则 CTC-A005 不变。
- **ruling:** style-only
- **reason:** 六个示例删除（8 个中删 6）；各示例演示的断言在对应规则行保留。记为显著的教学内容缩减，不计为断言丢失。

### C35 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §12 执行者删除示例（「旧快照数据会被存储管理机制销毁」）
- doc_quote: absent
- why: 示例删除；基线该例本身与 CTC-R003 冲突，CTC-A001 正文不变。
- **ruling:** style-only
- **reason:** 六个示例删除（8 个中删 6）；各示例演示的断言在对应规则行保留。记为显著的教学内容缩减，不计为断言丢失。

### C36 — opus · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: §12 否定作用域示例（「业务高峰期禁止重启网关，也禁止清空缓存。」）
- doc_quote: absent
- why: 示例删除；CTC-A004 正文保留「禁止 A，也禁止 B」。
- **ruling:** style-only
- **reason:** 六个示例删除（8 个中删 6）；各示例演示的断言在对应规则行保留。记为显著的教学内容缩减，不计为断言丢失。

### C37 — opus · doc A · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: §12 压缩示例正例：「1. 启动 `chunk-server`。2. 确认状态为 `READY` 且元数据已加载。3. 加入写入路由表。　　　并附「待确认」说明上限未能满足。」
- doc_quote: §10 正例：「1. 启动 `chunk-server`。2. 确认状态为 `READY` 且元数据已加载后，加入写入路由表。 ← 校验并入相邻步骤，仍由操作者执行、在被守护动作之前、判据列全。」
- why: 同一测试用例的期望输出改变：基线保留 3 步并报上限未满足，X 合并为 2 步且不报。方向与 CTC-P003 正文（授权下可以并入相邻步骤）对齐，但执行行为相反。
- **ruling:** example-correction · pooled as X-P003
- **reason:** 压缩示例期望输出改为合规的 2 步合并，与冻结的 P003 行（授权合并条款）一致；基线示例保留 3 步并报上限未满足，与该行矛盾。B 做了同一改动（C103）。

### C86 — opus · doc B · selfhost
- id: Y-F1
- rule: CTC-R004
- severity: WARNING
- locus: §3 中 strict 与 standard 适用范围所列的文档；状态提示；
- problem: 「状态提示」被单独列为适用对象，但 §3 strict 与 standard 的适用范围都没有列出它。「模式未指定时……按 §3 中 strict 与 standard 的适用范围推定」对状态提示没有可判定的依据，「跨界时取 strict」也不适用，因为状态提示不在任何一个范围内。
- suggestion: 在 strict 适用范围中写入「告警、错误信息与状态提示」，并从 §1 的单列项中删去「状态提示」。
- also_in_baseline: True
- **ruling:** confirmed (WARNING) · pooled as D-B1
- **reason:** 状态提示不在 strict/standard 任一适用范围，模式无从推定；基线同有。

### C87 — opus · doc B · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: **strict 不等于最大冗长** — 不得为显得明确而虚构执行者、参数、阈值、判据或失败原因；不得重复不消歧的主语；不得把复句拆成一行一句；不得把描述性陈述升格为规范条款，或把请求升格为义务；不得补写来源没有的告警。
- doc_quote: absent
- why: 虚构执行者、参数、失败原因、告警和升格情态，分别仍由 A001、S002、A005、S003 覆盖。但「不得重复不消歧的主语」「不得把复句拆成一行一句」在基线 strict 下是不可推翻的禁止，在 Y 中只剩 CTC-R002 的「应」和只管步骤拆分的 CTC-P001，强度降低。
- **ruling:** rejected
- **reason:** strict 小节的「不得重复不消歧的主语／不得拆成一行一句」在基线以不得级出现，与冻结的 R002「应」及「模式不改级别」冲突；B 删除散文后由 R002 行承担。A 保留了带 R002 引用的散文。

### C88 — opus · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 条件、前提、例外、守护条件与成功判据不得为求简洁删除。
- doc_quote: absent
- why: strict 小节里的这句被删掉，但 CTC-S001、CTC-L001、CTC-P003 与 standard 的「不得」仍在所有模式下覆盖同一禁止，属重复表述。
- **ruling:** style-only
- **reason:** S001/L001/P003 行覆盖。

### C89 — opus · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 更自然的句子若改变了真值条件，就不是改进。更显式的句子若凭空造出一项要求，就不是改进。更短的句子若丢掉一个条件或例外，就不是改进。
- doc_quote: absent
- why: 三条取舍判据被删掉，内容由第 1 层定义、CTC-S002 与 CTC-S001/L001 覆盖，执行行为不变。
- **ruling:** style-only
- **reason:** 三条取舍判据删除；内容由第 1 层定义与 S001/S002 覆盖。记为项目标志性表述的删除。

### C90 — opus · doc B · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: 10. 我有没有补出不消除任何歧义的主语、限定或短句？有没有留下译文腔？11. **我有没有改动任何规则并未要求改动的地方？** 有则还原。12. 输出符合当前模式的输出契约吗——无前言、结构与列表粒度保留、「待确认」仅在确有未决项时出现？
- doc_quote: absent
- why: Y 的 §9 表只列 S、A、P、T、L 族的不变量。返回前对 CTC-R001（无依据改动）、CTC-R002/R003 与输出契约的最终核对被删掉，规则本身仍在，但「任一项为否先修复再返回」这一道把关对这几类属性不再执行。
- **ruling:** confirmed (WARNING) · pooled as D-B2
- **reason:** B 的返回前核对表只列 S/A/P/T/L 不变量，§7 第 7 步只补逻辑方向、指代与标记；对 R001（无据改动）、R002/R003 与输出契约的返回前核对在 B 中找不到。规则本身仍在，丢失的是一道程序性把关。A 在第 7 步保留了这三项核对。

### C91 — opus · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 5. 执行所需、而来源与上下文都未提供的信息（CTC-S002）——缺失信息一律归第 5 类，不论是哪条规则先发现它；
- doc_quote: 5. 第 2–4 类之外、执行所需而来源与上下文都未提供的信息，不论由哪条规则发现（CTC-S002）；
- why: 第 5 类的范围从全部缺失信息缩小到第 2–4 类之外。这改变了分类，也关上了非破坏性步骤缺判据经由第 5 类进入的路径，可能改变「待确认」的条目数。
- **ruling:** rejected
- **reason:** 同 C4。

### C92 — opus · doc B · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: **上下文能确定读法时，必须消歧**，并且所选读法必须有来源或上下文证据。
- doc_quote: **上下文能确定读法时，按对应规则消歧**，级别以 §6 规则表为准，所选读法必须有来源或上下文证据。
- why: 消歧义务从一律「必须」改为跟随规则级别。CTC-A003（应）一类的消歧变为可推翻，与规则行一致，但与基线 §6 的字面不同。
- **ruling:** rejected
- **reason:** 同 C10。

### C93 — opus · doc B · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: 规范性指令中由无判据词（见 CTC-R004）承担义务的条件，必须报告其可能的两种以上强度并给出建议，然后停手。／3. review 模式作为一条 finding，严重级别为 ERROR。
- doc_quote: 改写时，规范性指令中由无判据词（见 CTC-R004）承担义务的条件，按 CTC-R004 在「待确认」中提出：指出缺失的判据，列出其可能的两种以上强度并给出建议，然后停手；……新写时按 CTC-R004 给出可观测的触发条件。
- why: 情态模糊的报告义务从 §6 的「必须」、review 中的 ERROR，改为按 CTC-R004（应），review 中报 WARNING，并限定在改写时。新写时改为给出触发条件。review 中的严重级别和新写时的行为可能改变。
- **ruling:** rejected
- **reason:** 情态模糊报告义务从散文「必须」改为按 R004（应）；review 定级随映射；新写分支来自 R004 行。均向冻结行收敛。

### C94 — opus · doc B · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: - 尽快回滚 | 「尽快」承担义务，强度未定 | 作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认
- doc_quote: - 尽快回滚 | 「尽快」未给出时限，所承担义务的强度未定 | 回滚时限与作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认
- why: 「需要的信息」栏新增了「回滚时限」，情态模糊的待确认项因此还要求索取具体判据。这与 CTC-R004 改写分支相符，但待确认条目的内容改变了。
- **ruling:** style-only
- **reason:** 示例第三栏加「回滚时限」，与 R004「在待确认中提出缺失判据」一致。

### C95 — opus · doc B · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 调用方可以显式授权四类本来禁止的改动：调整规范强度、精确的单位换算、解除某个受保护标记的保护、指定改写目标或长度上限。
- doc_quote: 调用方可以显式授权本来禁止的改动，即调整规范强度、精确的单位换算、解除某个受保护标记的保护、指定改写目标或长度上限，以及规则条文中写明的授权（CTC-P003 的合并步骤、CTC-R005 的改变格式）。
- why: 授权清单并入了 CTC-P003、CTC-R005 规则行里已有的授权，不产生新许可，只消除了「四类」与规则行之间的数量冲突。
- **ruling:** style-only
- **reason:** 授权清单并入规则行已有授权；审阅任务默认 review 可由 review 适用范围推出。

### C96 — opus · doc B · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 模式未指定时，按 §3 的适用范围推定，并在文档类型跨界时取更严的一档。
- doc_quote: 模式未指定时，审阅任务用 review；其余任务按 §3 中 strict 与 standard 的适用范围推定，文档类型跨界时取 strict。
- why: 审阅任务默认用 review、跨界时取 strict，基线从 review 的适用范围和「更严的一档」已可推出，现在写成明文。
- **ruling:** style-only
- **reason:** 授权清单并入规则行已有授权；审阅任务默认 review 可由 review 适用范围推出。

### C97 — opus · doc B · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: 未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察。
- doc_quote: 未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。
- why: 新增了 STYLE 观察必须带规则 ID 的要求，会排除无规则 ID 的风格意见，review 输出可能改变。
- **ruling:** confirmed (WARNING) · pooled as D-B3
- **reason:** STYLE 观察须引用规则 ID：基线区分 finding 与「观察」，此处为一处歧义选定读法；与 A 的 C28 对称。

### C98 — opus · doc B · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 改写、压缩与翻译之后逐项核对；任一项出现偏离都是一处 finding，其严重级别由 §7 中该行所引规则的级别决定
- doc_quote: 返回之前逐项核对下表各规则保护的不变量；任一项被破坏，先修复再返回。review 模式下，任一项偏离都是一处 finding，严重级别按 §8 确定。
- why: 「偏离即 finding」被限定在 review 模式，改写模式改为先修复再返回，与基线 §11 和输出契约一致。
- **ruling:** style-only
- **reason:** 「偏离即 finding」限定在 review 与基线 §11/输出契约一致；核对字段扩大属合并。

### C99 — opus · doc B · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 重新抽取 (情态, 数值, 量化, 因果, 否定作用域, 施事, 指代, 条件, 时序, 受保护标记) 并与第 2 步的记录逐项比较。
- doc_quote: 重新抽取第 2 步的全部字段，另加逻辑方向（合取／析取、充分／必要、分组）、指代与受保护标记，与第 2 步的记录逐项比较。
- why: 渲染后的复核扩大到第 2 步的全部字段（对象、例外、原子性分组、边界包含性），另加逻辑方向。只加强核对过程，不新增输出要求。
- **ruling:** style-only
- **reason:** 「偏离即 finding」限定在 review 与基线 §11/输出契约一致；核对字段扩大属合并。

### C100 — opus · doc B · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: 「用户打开控制台。用户点击设置。用户修改端口。」应写成「打开控制台后，点击「设置」修改端口。」只有多角色交替执行时才补主语。
- doc_quote: 「用户打开控制台。用户点击设置。用户修改端口。」应写成「用户打开控制台，点击设置，修改端口。」只有存在多个可能执行者、且不同读法改变由谁执行时才补主语（CTC-A001）。
- why: 示例输出从删去执行者改为保留一次「用户」，也不再加「后」和引号。补主语的判据换成了 CTC-A001 的措辞。同一输入示范的输出不同，与 CTC-A001 规则行一致，基线版本与规则行冲突。
- **ruling:** example-correction · pooled as X-A001
- **reason:** 四处示例期望输出改为与冻结规则行一致（A001 保留执行者；S002 去掉虚构的「归零」；R003 施事同句的被动原样返回；P003 授权合并为 2 步）。不是断言丢失，不计入第 1 判据。

### C101 — opus · doc B · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: 应写成「停止写入，等待复制延迟归零后执行切换。」
- doc_quote: 应写成「停止写入，等待并检查复制延迟，然后执行切换。」
- why: 示例去掉了基线虚构的判据「归零」，恢复了「检查」动作。同一输入示范的输出不同，Y 与 CTC-S002、CTC-P003 一致。
- **ruling:** example-correction · pooled as X-S002
- **reason:** 四处示例期望输出改为与冻结规则行一致（A001 保留执行者；S002 去掉虚构的「归零」；R003 施事同句的被动原样返回；P003 授权合并为 2 步）。不是断言丢失，不计入第 1 判据。

### C102 — opus · doc B · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: 反例：磁盘空间不足时，旧快照会被自动清理。 ← 去被动正当，删掉具名施事不正当；两处改动只有前一处有规则依据。正例：磁盘空间不足时，存储管理机制会销毁旧快照数据。
- doc_quote: 反例：磁盘空间不足时，旧快照会被自动清理。 ← 删掉具名施事，另增「自动」、删「数据」、以「清理」替换「销毁」，均无规则依据。正例：原样返回。施事已在同句给出，被动是自然的技术表述（CTC-R003），不触发去被动。
- why: 施事已在同句给出的被动句，从「应去被动」改为「原样返回」，示范的执行行为相反。Y 与 CTC-R003/R001 规则行一致。
- **ruling:** example-correction · pooled as X-R003
- **reason:** 四处示例期望输出改为与冻结规则行一致（A001 保留执行者；S002 去掉虚构的「归零」；R003 施事同句的被动原样返回；P003 授权合并为 2 步）。不是断言丢失，不计入第 1 判据。

### C103 — opus · doc B · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: 正例：1. 启动 `chunk-server`。2. 确认状态为 `READY` 且元数据已加载。3. 加入写入路由表。并附「待确认」说明上限未能满足。
- doc_quote: 正例：1. 启动 `chunk-server`，确认状态为 `READY` 且元数据已加载。2. 加入写入路由表。 ← 校验仍由操作者执行、位于加入路由表之前、判据列全。若不删校验就无法达标，按 CTC-S001 返回超限文本并在「待确认」中说明
- why: 同一压缩指令下，示范输出从 3 步加待确认项，改为合规合并后的 2 步。执行行为改变，Y 与 CTC-P003 的授权合并条款一致。超限时的处理作为条件分支保留。
- **ruling:** example-correction · pooled as X-P003
- **reason:** 四处示例期望输出改为与冻结规则行一致（A001 保留执行者；S002 去掉虚构的「归零」；R003 施事同句的被动原样返回；P003 授权合并为 2 步）。不是断言丢失，不计入第 1 判据。

### C104 — opus · doc B · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 正例：在生产环境部署该服务前，请确保已配置环境变量。
- doc_quote: 正例：在生产环境部署该服务前，请确保已配置环境变量。 ← 「请确保」保持请求强度；「如果你想……」「你已经……了」是英语从句语序残留（CTC-R003）。
- why: 只加了归因注释，正例文本不变。
- **ruling:** style-only
- **reason:** 归因注释；翻译条款一句由 S005「逐字符不变」覆盖。

### C105 — opus · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 标识符、命令与代码块一律不译（CTC-S005）；
- doc_quote: absent
- why: 翻译补充条款里的这一句被删掉，CTC-S005 的「逐字符不变」与 §4 仍覆盖，执行行为不变。
- **ruling:** style-only
- **reason:** 归因注释；翻译条款一句由 S005「逐字符不变」覆盖。

### C106 — opus · doc B · fork
- probe: 模式
- readings: ['读法 1：状态提示按 strict 处理（与告警、错误信息同类），用低阈值。', '读法 2：状态提示不在任何范围内，按说明性文本用 standard 的高阈值。']
- **ruling:** confirmed (WARNING) · pooled as D-B4
- **reason:** 模式探针分叉（状态提示）；基线同有。

### C107 — fable · doc A · selfhost
- id: X-F1
- rule: CTC-R004
- severity: WARNING
- locus: 文本含无必要的被动、名词化赘语（进行／作出／予以 + 动词）、过长的「的」字串
- problem: CTC-R003 的触发条件之一由无判据词「过长」承担；文档没有给出多长算过长的可观测判据或边界示例。R003 对「无必要的被动」给了边界（突出受事、施事未知、施事已在同句给出），对「过长」没有。
- suggestion: 给「过长」一个可观测边界，例如「连续三个以上「的」且可改为分句而不改变修饰关系时」，或给一个正反例。
- also_in_baseline: True
- **ruling:** confirmed (WARNING) · pooled as D-A3
- **reason:** R003 行「过长的「的」字串」无判据；该行冻结，基线同有。所有迭代者都报出并以「冻结行」为由拒改。

### C108 — fable · doc A · selfhost
- id: X-F2
- rule: CTC-R004
- severity: WARNING
- locus: 规范性指令（agent 指令、SOP、策略、门禁条件）的判定条件由无判据词承担时——「尽量」「尽可能」「最好」「适当」「必要时」「合理」——
- problem: R004 把「尽量」「尽可能」「最好」与「适当」「必要时」「合理」并列为承担判定条件的词，并要求新写时给出「可观测的触发条件（阈值、状态或事件）」。§5 却把前三个词归为承担义务强度、后三个词归为承担判定条件，并规定前者要在「待确认」第四栏给建议、后者「只按第 4 类提出」。同一组词在两处被归入不同类别，处理方式不同。
- suggestion: 在 R004 中把词表按 §5 的划分拆开：强度词（最好、尽量、尽可能）新写时给出规范强度、改写时按 §5 报告并附建议；判定条件词（适当、必要时、合理）新写时给出可观测触发条件、改写时按第 4 类提出。
- also_in_baseline: True
- **ruling:** confirmed (ERROR) · pooled as D-A1
- **reason:** 与 C1 同一缺陷（R004 六词在 §5 与 R004 行归类不同）。Opus 按 A005 计 ERROR，Fable 按 R004 计 WARNING。裁决按 A005：强度词在 review 下所引规则（§5 路径→A005 或括注→R004）不唯一，严重级别随之分叉。基线在同一位置有另一形态的冲突（§6 固定 ERROR 对 R004 应），故记为「继承并改形」。

### C109 — fable · doc A · vs_baseline
- type: altered
- severity: ERROR
- baseline_quote: 正例：1. 启动 `chunk-server`。2. 确认状态为 `READY` 且元数据已加载。3. 加入写入路由表。　　　并附「待确认」说明上限未能满足。步骤数达标而校验丢失，不如超出上限而校验完整。
- doc_quote: 正例：1. 启动 `chunk-server`。2. 确认状态为 `READY` 且元数据已加载后，加入写入路由表。 ← 校验并入相邻步骤，仍由操作者执行、在被守护动作之前、判据列全。
- why: 同一来源与同一压缩指令下，示范输出从「保留三步并附待确认」变为「合并为两步」，模型对已授权压缩的执行行为不同。文档版与两份共有的 CTC-P003 正文（授权合并时可并入相邻步骤）和 CTC-S001（仅在无法满足上限时才超限）一致；基线示例与其规则矛盾。行为变化本身按 ERROR 记。
- **ruling:** example-correction · pooled as X-P003
- **reason:** 同 C37。

### C110 — fable · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 5. 执行所需、而来源与上下文都未提供的信息（CTC-S002）——缺失信息一律归第 5 类，不论是哪条规则先发现它；
- doc_quote: 5. 执行所需、而来源与上下文都未提供的信息；不属于第 2–4 类的缺失信息一律归本类，不论是哪条规则先发现它（CTC-S002）；
- why: 基线字面上把全部缺失信息归第 5 类，与第 2–4 类本身就是缺失信息相抵；文档收窄为「不属于第 2–4 类的」。对缺失成功判据、缺失触发条件、无判据条件三种情形，类别与规则 ID 归属可能不同（基线字面 S002，文档 P003／P005／R004）。
- **ruling:** rejected
- **reason:** 同 C4。

### C111 — fable · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 一个字符串出现在代码标记内（行内代码、围栏代码块含语言标注）
- doc_quote: 一个字符串出现在代码标记内（行内代码；围栏代码块，不论是否带语言标注）
- why: 基线「含语言标注」可读作限定（只有带标注的围栏块）或补充；文档明确不带标注的围栏块同样是代码标记。对不带语言标注的围栏块，一种基线读法下不受代码标记保护，文档下受保护。
- **ruling:** style-only
- **reason:** 同 C29：S005 行「代码块内部整体不动」本无语言标注条件。

### C112 — fable · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 标题、列表层级、表格单元格与告警块所建立的条件管辖其子树，这属于条件保持，按 CTC-L001 判定。
- doc_quote: 标题、列表层级与表格单元格建立的条件管辖其子树（CTC-L001），独立告警块管辖它所依附的整个流程（CTC-P004）
- why: 告警块的管辖范围从「其子树」改为「所依附的整个流程」，规则归属从 L001 改为 P004。两份共有的 P004 正文本就写「管辖它所依附的整个流程」，文档消除了基线 §5 与 P004 的不一致；但 review 中对告警块的 finding 规则字段可能从 L001 变为 P004。
- **ruling:** rejected
- **reason:** 同 C9。

### C113 — fable · doc A · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 规范性指令中由无判据词（见 CTC-R004）承担义务的条件，必须报告其可能的两种以上强度并给出建议，然后停手。
- doc_quote: 义务的强度由「最好」「尽量」「尽可能」这类无判据词承担时，报告其可能的两种以上强度并在第四栏给出建议，然后停手；「必要时」「适当」「合理」承担的是判定条件而非强度，只按第 4 类提出（CTC-R004）。
- why: 基线对 R004 词表中的全部词都要求报告强度并给建议；文档把「必要时」「适当」「合理」排除在外，只按第 4 类提出、不填第四栏。对这三个词，「待确认」行的第四栏有无不同。
- **ruling:** confirmed (WARNING) · pooled as D-A2
- **reason:** 同 C12。

### C114 — fable · doc A · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: **上下文能确定读法时，必须消歧**，并且所选读法必须有来源或上下文证据。
- doc_quote: **上下文能确定读法时，按所触发的规则消歧**（CTC-A001–A004、CTC-P002 等），并且所选读法必须有来源或上下文证据。
- why: 无条件的「必须消歧」变为「按所触发的规则消歧」；上下文能确定读法但 A001–A004／P002 都未触发的歧义（如动词多义），基线要求消歧，文档不要求。文档版与两份共有的 R001「改动必须归因到规则 ID」一致。
- **ruling:** rejected
- **reason:** 同 C10。评审指出的「无规则触发但上下文可定的歧义」在基线下也受 R001「改动必须归因规则 ID」约束，基线散文与 R001 行本就冲突。

### C115 — fable · doc A · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: 3. review 模式作为一条 finding，严重级别为 ERROR。
- doc_quote: review 模式下作为一条 finding 报告，严重级别按所引规则的级别（§8）。
- why: 基线对上下文不能确定的歧义一律 ERROR；文档改为按所引规则级别。若评审引用 A005（必须）结果相同；若引用转来源规则（如 A003，应）则为 WARNING。基线的固定 ERROR 被条件化。
- **ruling:** rejected
- **reason:** 同 C11。

### C116 — fable · doc A · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: review 模式下它就是 finding 的「规则」字段。
- doc_quote: review 模式下它就是 finding 的「规则」字段，缺失信息的规则 ID 与其所属类别括注的规则一致。
- why: 新增一条归因规则：缺失信息的 finding 规则字段按「待确认」类别括注的规则填写。基线对此未定（A005 与 P002 的正文指向 A005，第 5 类括注指向 S002）；新增条款把该未定固定为按类别归属，review 输出的规则字段随之确定。
- **ruling:** confirmed (WARNING) · pooled as D-A4
- **reason:** 同 C5。

### C117 — fable · doc A · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: 级别与严重级别一一对应：**必须** = 违反即语义错误（ERROR）；**应** = 默认要求，可被更高优先级或明确边界推翻（WARNING）；**可以** = 许可（STYLE）。
- doc_quote: 级别由「级别」栏决定：**必须** = 硬性要求；**应** = 默认要求，可被更高优先级或明确边界推翻；**可以** = 许可。规则正文中的「必须」「不得」表达该规则的要求与禁止，不改变该栏的级别。级别到严重级别的映射及其唯一的升级例外见 §8。
- why: 新增解释规则：规则正文内的「必须」「不得」不改变「级别」栏。基线无此句，读者可能把 P003（应）正文中的「必须仍是继续的前提」读作必须级、按 ERROR 报告；文档固定为 WARNING。「一一对应」被删（基线该说法与唯一升级例外相抵）。
- **ruling:** style-only
- **reason:** 同 C13。

### C118 — fable · doc A · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: 1. 按 §9 第 1–3 步建立比对基准：受保护标记、语义骨架、文档类型对应的歧义阈值。
- doc_quote: 1. 按 §7 第 1–3 步建立比对基准，并按文档类型选取歧义阈值（§3）。被审文本没有独立来源时（审计既有文本、复核本技能自身文本），以被审文本自身为来源：来源与输出之间的不变量无从违反，只报告被审文本自身可观测的违规：竞争读法、指代、无判据条件、术语不一致等；文内两处陈述对同一情形要求不同行为时，按 CTC-A005 报告，位置引用两处。
- why: 新增无独立来源时的 review 程序：以被审文本自身为来源、只报自身可观测违规、文内冲突按 A005 报告并引用两处。基线对审计既有文本与自身复核（均在 review 适用范围内）没有规定比对基准，评审行为不确定；文档把它固定下来。
- **ruling:** confirmed (WARNING) · pooled as D-A5
- **reason:** 同 C25。

### C119 — fable · doc A · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: | 不变量 | 必须保持什么 | 破坏后的后果 | 规则 | 级别 |（§4 语义不变量表，21 行）以及「本节列出返回之前必须逐项验证的属性…任一项出现偏离都是一处 finding，其严重级别由 §7 中该行所引规则的级别决定」
- doc_quote: absent
- why: 整节删除。「必须保持什么」列的内容在 29 条规则行中都有对应；「返回前逐项验证」由 §7 第 7 步「重新抽取第 1、2 步登记的全部项并逐项比较，S、A、P、T、L 五族每条规则的保持项都须与来源相同」承接。丢失的是：按不变量组织的可枚举核对表、每行的「破坏后的后果」示例、以及「歧义守恒」「步骤图」「结构作用域」这些不变量的命名。核对要求本身未丢，但核对的粒度从 21 项显式清单变为「全部项」。
- **ruling:** style-only
- **reason:** 同 C7/C8：要求项在规则行与 §7 第 7 步可还原；后果栏是理据。

### C120 — fable · doc A · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: 不得翻译标识符、改动大小写或分隔符、把标记内的半角符号改为全角、用描述替换命令、替换或补全占位符、规范化 URL。
- doc_quote: absent
- why: 六项具体禁止在文档中没有对应列举。它们都被「逐字符不变」蕴含（S005 亦写「含大小写与分隔符」；产品名段落写「不得翻译」），但「替换或补全占位符」「用描述替换命令」是 P002「可确定的部分应写出」可能被误用的方向，显式禁止的消失使这条边界只剩隐含。
- **ruling:** style-only
- **reason:** 六项具体禁止是「逐字符不变」+「标记多重集必须相等」（均在 A 中，必须级）的实例；B 保留了该列举，记为具体性差异。

### C121 — fable · doc A · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: 严重级别：- **ERROR** — 语义损坏、不安全的歧义、受保护标记突变，或硬不变量被违反。- **WARNING** — 可能的歧义或规则风险，需要人工判断。- **STYLE** — 不影响语义的自然度或一致性问题。
- doc_quote: absent
- why: 三条描述性定义删除，只保留「必须 → ERROR，应 → WARNING，可以 → STYLE」映射。基线的描述引入了映射之外的判据（「不安全的」「可能的」歧义），与映射及 §6「一律 ERROR」并存；删除后严重级别只由映射决定。对按描述判级的评审，行为改变；对按映射判级的评审，不变。
- **ruling:** rejected
- **reason:** 同 C27。

### C122 — fable · doc A · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: **情态强化**（CTC-S003…）／**例外删除**（CTC-L001）／**阈值边界翻转**（CTC-L004）／**静默消歧**（CTC-A005）／**执行者删除**（CTC-A001）／**否定作用域**（CTC-A004）六组「来源／反例／正例」
- doc_quote: absent
- why: 六组示例删除，只保留 P003 与 R001／R002 两组。示例不是规则，规则行未变；但「静默消歧」正例是全文唯一演示三栏「待确认」行（含竞争读法写法）的地方，「执行者删除」正例是唯一演示「去被动正当、删施事不正当」两处改动分别归因的地方。丢失后这些行为只剩规则正文。
- **ruling:** style-only
- **reason:** 同 C31–C36。评审指出的「三栏待确认行演示」在 A 的 §3 示例块中仍有两行三栏示例。

### C123 — fable · doc A · vs_baseline
- type: strengthened
- severity: STYLE
- baseline_quote: 理由不在算术而在操作：技术数值会被直接复制进单位由字段名固定的配置项，而文档不保证标明哪些值是这样的。
- doc_quote: 本技能假定技术数值会被直接复制进单位由字段名固定的配置项，且文档不标明哪些值是这样的：换算在算术上无损，在操作上有损。
- why: 「不保证标明」（可能标明也可能不标明）改为「不标明」，不确定性被去掉；文档同时把整句降为「本技能假定」。这是理由陈述，不改变 S004／§4 的行为。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C124 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 处理下列中文技术内容的写作、改写、翻译或审阅时，本技能生效：- agent 指令、系统提示；工具与函数描述；- SOP、runbook、变更流程、运维与安全敏感操作、排障步骤；- 告警、错误信息、状态提示；- API 文档、README、开发者指南、FAQ、发布说明；- 技术文本的英译中，以及既有中文技术文本的审校。
- doc_quote: 写作、改写、翻译或审阅中文技术内容时，本技能生效，覆盖 §3 strict 与 standard 适用范围所列的文档类型，以及状态提示、技术文本的英译中与既有中文技术文本的审校。
- why: 文档类型清单改为引用 §3 两份适用范围；逐项对照无缺失（状态提示、英译中、审校单独补出）。仅是间接引用。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C125 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 施事—动作—受事关系
- doc_quote: 执行者—动作—对象关系
- why: 同一概念换词；A001 正文两份都写「执行者（含被动句中的施事）」，语义不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C126 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 即按分歧读法处理
- doc_quote: 即按竞争读法处理
- why: 基线在 §2、§3 用「分歧读法」、在 A005 用「竞争读法」；文档统一为「竞争读法」。术语统一，阈值定义不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C127 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 体例或地区偏好不得为赢得争论而升格为语义规则
- doc_quote: 体例或地区偏好不得升格为语义规则
- why: 删去动机状语「为赢得争论」，禁止本身不变（任何情形都不得升格，比基线字面略宽，但基线的动机状语不构成例外）。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C128 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: "条件、前提、例外、守护条件与成功判据不得为求简洁删除。"（strict）与 "以简洁为名删除条件、例外、阈值、默认值或受保护标记"（standard 不得）
- doc_quote: 任何模式下都不得以简洁或长度为名删除条件、前提、例外、守护条件、成功判据、阈值、默认值或受保护标记（CTC-S001、CTC-S005）。
- why: 两条模式内禁止合并为一条「任何模式」禁止，取并集。两份共有的 S001／S005 本就在所有模式生效，并集不新增要求。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C129 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: - 尽快回滚 | 「尽快」承担义务，强度未定 | 作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认
- doc_quote: - 最好在窗口内回滚 | 「最好」承担义务，可读作「应在窗口内回滚」或「可以在窗口内回滚」 | 作者意图的道义强度 | 建议按前者确认
- why: 示例换词（尽快→最好，后者在 R004 词表内）；两种读法从第四栏移到第二栏「问题」，与 §3 栏位定义（第四栏 = 建议）更一致；「规范强度」→「道义强度」与 S003 用词一致。示例格式变化，规则不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C130 — fable · doc A · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 调整规范强度、精确的单位换算、解除某个受保护标记的保护、指定改写目标或长度上限。授权本身即构成 CTC-R001 所要求的归因，按授权执行即可
- doc_quote: (1) 调整道义强度（规范强度）；(2) 精确的单位换算；(3) 解除某个受保护标记的保护；(4) 指定改写目标或长度上限（如合并步骤、改变格式）。授权本身即构成 CTC-R001 所要求的归因
- why: 第 4 类加了示意「如合并步骤、改变格式」（与 P003、R005 一致），删去「按授权执行即可」。四类不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C131 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 受保护标记本身的拼写疑似有误时，标记保持原样，并按「待确认」第 6 类提出。
- doc_quote: absent
- why: 第 6 类仍在准入清单，S005「逐字符不变」蕴含「保持原样」；丢的是把两者连起来的一句。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C132 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 「超时后重试，多次失败则升级处理」——「多次」与「升级」都缺少可执行所需的信息，保留原句并逐项进「待确认」。
- doc_quote: absent
- why: 对照例的第二例删除；其两项未决项仍以「待确认」示例块的前两行保留。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C133 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: **必须** = 违反即语义错误（ERROR）
- doc_quote: **必须** = 硬性要求
- why: 定义措辞变化；级别到严重级别的映射移到 §8 且逐字保留。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C134 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: "不得虚构验收标准。…其余步骤缺少判据不提出，否则每份正常的流程文档都会产生成串的未决项。"（CTC-P003）
- doc_quote: 不得虚构判据。…其余步骤缺少判据不提出，以免正常的流程文档产生成串的未决项。
- why: 29 条规则行中唯一有差异的一行。「验收标准」→「判据」是同一概念的术语统一（P003 其余部分都用「判据」）；「否则每份…都会」→「以免」是理由句的措辞。触发、要求、禁止、例外均未变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C135 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 来源已有的缺陷，只在其本条规则触发时修复，修复取能去除该缺陷的最小改动（CTC-R001）；不含该缺陷的文本，CTC-R002 与 CTC-R003 都不授权重写。
- doc_quote: 只在该缺陷出现时修复，修复取能去除它的最小改动；不含该缺陷的文本不授权重写（CTC-R001）。
- why: 删去「来源已有的」限定，改为「该缺陷出现时」；R002 正文两份都写「输出中出现」，因此覆盖面相同。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C136 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 3. 不得一刀切禁用被动 ／ 5. 不得给相邻步骤强加连接词 ／ 6. 不得统一指称不同概念的近义词 ／ 7. 不得换算单位 ／ 10. 不得把无歧义的指代展开为重复长名词 ／ 12. 不得把无歧义的并列拆成编号分支 ／ 13. 不得为「理论上存在两种解析」而报错 ／ 15. 不得改写未触发任何规则的文本
- doc_quote: absent
- why: 八条从「不得做的事」删除。逐条查对应规则行：3→R003「被动用于…是自然的技术表述」与 A001「报为施事缺失是误报」；5→S006「不得把仅有时间先后的两句用「因此」连成因果」；6→T002；7→S004 与 §4；10→A002「不得为求显式把每个「其」都展开为名词」；12→R002「被机械拆分的短句」与 P001；13→§5「不得因「理论上可解析出两种读法」而报告」；15→R001。要求本身都在，丢的是示例与重申。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C137 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 「用户打开控制台。用户点击设置。用户修改端口。」应写成「打开控制台后，点击「设置」修改端口。」
- doc_quote: 「用户打开控制台。用户点击设置。用户修改端口。」写成「用户打开控制台后，点击设置修改端口。」
- why: 文档版保留一次具名执行者「用户」并不给「设置」加引号，与 A001「来源指明的执行者必须在输出中仍可定位」更一致；基线版全部省略。示例差异，规则不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C138 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 2. **不得一句一动词。** 会割裂条件、等待点与结果关系。「停止写入。等待。检查复制延迟。执行切换。」应写成「停止写入，等待复制延迟归零后执行切换。」
- doc_quote: "不得一句一动词"（并入第 1 条，无示例）
- why: 禁止保留，示例与理由删除。被删示例补出了来源没有的「归零」，与 S002／A005／P003 矛盾（阶段 1 Y-F2）；删除后不再示范该错误。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C139 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: **原样返回来源是一个合法的输出。** 一次没有改动的改写不是失职；一次没有依据的改动才是。
- doc_quote: absent
- why: R001「未触发任何规则的文本原样返回」、§8「没有 finding 是一个有效结果」与 §10 正例「原样返回」保留同一命题；丢的是这句显式重申。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C140 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 标出代码、命令、路径、标识符、字段名、URL、状态码、占位符、数值与单位。这些进入不可改集合。
- doc_quote: 标出受保护标记，进入保护集（§4）；数值与单位另行登记，按 §4 保持表面形式。
- why: 数值与单位从「不可改集合」改为「保持表面形式」。基线此句与其 §5「全角数字半角化属于排版，可以做」相抵，文档与 §4 一致；两份的 §4／§5 规定相同，实际行为不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C141 — fable · doc A · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 逐句列出执行者、动作、对象、条件、例外、顺序、原子性分组、阈值与边界包含性、情态强度、量化论域、因果强度、否定作用域。
- doc_quote: 逐句列出执行者、动作、对象、条件、例外、顺序、原子性分组、阈值与边界包含性、情态强度、量化论域、因果强度、否定作用域、指代先行词。
- why: 骨架新增「指代先行词」一项；A002 两份相同，只是把已有要求纳入登记。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C142 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 重新抽取 (情态, 数值, 量化, 因果, 否定作用域, 施事, 指代, 条件, 时序, 受保护标记) 并与第 2 步的记录逐项比较。
- doc_quote: 重新抽取第 1、2 步登记的全部项并逐项比较，S、A、P、T、L 五族每条规则的保持项都须与来源相同；同时核对没有补出不消除任何歧义的主语、限定或短句，没有留下译文腔（CTC-R002、CTC-R003），没有改动任何规则并未要求改动的地方（CTC-R001）。任一项不成立，先修复再返回
- why: 比对集合从十元组改为「登记的全部项」加五族保持项，并把基线 §11 第 10、11 问并入本步。核对面不小于基线；「任一项不成立」的极性一致，避免了基线 §11「任一项为「否」」在「有没有…」问句上的极性反转。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C143 — fable · doc A · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: absent
- doc_quote: 调用方已授权的改动不计为不成立。
- why: 新增例外，但两份共有的「调用方授权」段已规定授权即构成归因、只改变允许做什么；此句只是在核对步骤重申。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C144 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 标识符、命令与代码块一律不译（CTC-S005）；
- doc_quote: absent
- why: 翻译附加条从四条减为三条；S005「逐字符不变」与 §4「也不得翻译」「翻译标识符会造成不可逆损坏」保留同一要求。基线说「另加三条」却列了四条，文档不再计数。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C145 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: "规则：CTC-S003 严重级别：ERROR 位置：「确认数据备份完成…」问题：… 风险：… 建议修改：…"（六字段示例块）
- doc_quote: absent
- why: 六个字段在 §8 第 3 步逐一列出；丢的是一个填写示例。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C146 — fable · doc A · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察。
- doc_quote: 没有 ERROR 或 WARNING 级 finding 时返回「未发现违规」，其后最多列三条 STYLE 级 finding。
- why: 「未发现问题」改为可判定的「没有 ERROR 或 WARNING 级 finding」，「STYLE 观察」改为「STYLE 级 finding」；输出相同。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C147 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: ## 11. 自检 返回之前逐项回答。任一项为「否」，先修复再返回。1.…12. 输出符合当前模式的输出契约吗——无前言、结构与列表粒度保留、「待确认」仅在确有未决项时出现？
- doc_quote: absent
- why: 独立的十二问清单删除，第 1–11 问的内容由 §7 第 7 步「全部项」与显式列出的三项承接；第 12 问由第 8 步「按输出契约返回（§3）」承接但不再是显式核对问句。基线清单的极性缺陷（阶段 1 Y-F3）随之消失。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C148 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: "未触发规则的文本不产生 finding。"（review 行为）
- doc_quote: absent
- why: 文档 review 节没有这句；等价约束由「不得报告没有规则 ID 的 finding；为显得周全而制造 finding」与 A001「不产生 finding」承接。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C149 — fable · doc A · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 「判定按顺序做」／「风格处理排在后面是有意的」／§2 五层箭头图
- doc_quote: absent
- why: 三处非规范内容删除：第一处后面本无顺序，第二处是设计说明，第三处与其后的五层表重复。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C150 — fable · doc A · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: absent
- doc_quote: "（CTC-S002、CTC-A005）…（CTC-R002、CTC-P001）…（CTC-S003）"（§3 strict）；"（CTC-A001、CTC-P001、CTC-R002）…（CTC-R002）…（CTC-R001）"（§9）；"（CTC-S004）"（§4）
- why: 多处补加规则 ID 括注，把已有约束归到对应规则；不新增要求。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C192 — fable · doc B · selfhost
- id: Y-F1
- rule: CTC-P005
- severity: WARNING
- locus: 本技能生效：§3 中 strict 与 standard 适用范围所列的文档；状态提示；技术文本的英译中与既有中文技术文本的审校。
- problem: 「状态提示」被明确列在「§3 中 strict 与 standard 适用范围所列的文档」之外；§1 的模式推定规则只覆盖「按 §3 中 strict 与 standard 的适用范围推定」与「文档类型跨界时取 strict」。状态提示既不在任一范围内，也不是跨界，其模式与歧义阈值无从推定。
- suggestion: 把「状态提示」并入 strict 适用范围的「告警与错误信息」项（写作「告警、错误信息与状态提示」），或在 §1 写明其归属。
- also_in_baseline: True
- **ruling:** confirmed (WARNING) · pooled as D-B1
- **reason:** 同 C86（状态提示模式无从推定，基线同有）。

### C193 — fable · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 三条判据把这句话变成可执行的取舍：更自然的句子若改变了真值条件，就不是改进。更显式的句子若凭空造出一项要求，就不是改进。更短的句子若丢掉一个条件或例外，就不是改进。
- doc_quote: absent
- why: 三条判据是第 1 层优先于第 4／2 层的重述，其内容分别由 CTC-S003／L 族、CTC-S002、CTC-S001／L001 覆盖；作为独立取舍口诀消失，但不改变任何规则的触发或要求。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C194 — fable · doc B · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: 条件、前提、例外、守护条件与成功判据不得为求简洁删除。
- doc_quote: absent
- why: strict「行为」中这条硬性禁止消失。条件、前提、例外由 CTC-S001／L001（必须）覆盖，守护条件由 CTC-P004／L001 覆盖，但「成功判据不得为简洁删除」在文档中只剩 CTC-P003（应）与对 S001「断言」的解释；strict 下删除判据的禁止强度可能由必须降为应。
- **ruling:** rejected
- **reason:** 成功判据是独立断言，S001 行（必须、全模式）已禁止为满足上限而删除；B 的 standard 小节亦保留「不得以简洁为名删除条件…」。A 保留了该句并扩展为全模式，记为显式性差异。

### C195 — fable · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: **strict 不等于最大冗长** — 不得为显得明确而虚构执行者、参数、阈值、判据或失败原因；不得重复不消歧的主语；不得把复句拆成一行一句；不得把描述性陈述升格为规范条款，或把请求升格为义务；不得补写来源没有的告警。
- doc_quote: absent
- why: 每一项都在规则行或 §10 中另有同级表述：虚构执行者（A001）、参数／阈值／判据（S002、A005、R004）、失败原因与告警（S002）、重复主语与拆句（R002、P001、§10 第 1–2 条）、升格（S003）。strict 专属的汇总消失，规则内容未变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C196 — fable · doc B · vs_baseline
- type: lost
- severity: WARNING
- baseline_quote: 10. 我有没有补出不消除任何歧义的主语、限定或短句？有没有留下译文腔？ 11. **我有没有改动任何规则并未要求改动的地方？** 有则还原。 12. 输出符合当前模式的输出契约吗——无前言、结构与列表粒度保留、「待确认」仅在确有未决项时出现？
- doc_quote: absent
- why: §9「返回前核对」表只列 20 条语义规则；基线 §11 第 1–9 项由该表覆盖，第 10–12 项（R002／R003、R001、输出契约）在返回前不再有核对项。规则本身保留在 §6 与 §7 第 4、6、8 步，但少了返回前对无据改动与输出契约的最后一遍检查。
- **ruling:** confirmed (WARNING) · pooled as D-B2
- **reason:** 同 C90。

### C197 — fable · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 标识符、命令与代码块一律不译（CTC-S005）；
- doc_quote: absent
- why: 翻译附加条由四条减为三条。「不译」由 CTC-S005「逐字符不变」「代码块内部整体不动」蕴含，§4 又写「翻译标识符……见 CTC-S005」；显性陈述消失，要求未变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C198 — fable · doc B · vs_baseline
- type: lost
- severity: STYLE
- baseline_quote: 语义先于风格。未触发规则即不改动。歧义只报告，不替作者决定。
- doc_quote: 语义先于风格。
- why: 后两句在 CTC-R001、CTC-A005、§2「替作者决定不是」中各有同级表述。同类的重复表述删除还包括 §6 开头「每一处改动必须能引用下表中的一条规则 ID」、§8 第 13／15 条、§10 不得列表的「输出整篇改写」「把体例偏好判为 ERROR」、§5 不得列表的「静默选定一种读法」「补出缺失的参数……」；按「多处出现只保留一处」规则均不计为实质 lost，此处合并备查。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C199 — fable · doc B · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: **上下文能确定读法时，必须消歧**，并且所选读法必须有来源或上下文证据。
- doc_quote: **上下文能确定读法时，按对应规则消歧**，级别以 §6 规则表为准，所选读法必须有来源或上下文证据。
- why: 章节级的「必须消歧」改为按规则级别执行；对 CTC-A003（应）类可判定的结合歧义，强度由必须降为应。基线该句与 A003 的「应」本身不一致，文档取规则表一侧；规则行级别未变。
- **ruling:** rejected
- **reason:** 同 C92/C93。

### C200 — fable · doc B · vs_baseline
- type: weakened
- severity: WARNING
- baseline_quote: 规范性指令中由无判据词（见 CTC-R004）承担义务的条件，必须报告其可能的两种以上强度并给出建议，然后停手。
- doc_quote: 改写时，规范性指令中由无判据词（见 CTC-R004）承担义务的条件，按 CTC-R004 在「待确认」中提出：指出缺失的判据，列出其可能的两种以上强度并给出建议，然后停手
- why: 「必须报告」改为「按 CTC-R004」（应）。连带后果：基线 §6 第 3 条使此类条目在 review 下为 ERROR，文档按 R004 映射为 WARNING（除非按 §8 升级）；同一输入的 review 严重级别标签可能不同。基线在此处自身不一致（§6 ERROR 对 R004 应），文档取规则表一侧。
- **ruling:** rejected
- **reason:** 同 C92/C93。

### C201 — fable · doc B · vs_baseline
- type: strengthened
- severity: WARNING
- baseline_quote: 只有多角色交替执行时才补主语。
- doc_quote: 只有存在多个可能执行者、且不同读法改变由谁执行时才补主语（CTC-A001）。
- why: 补主语的许可条件由「多角色交替执行」收窄为 A001 的双重条件「多个可能执行者且不同读法改变由谁执行」。基线 §8 第 1 条比 A001 行宽松、与 R002「多执行者交替出现时重复主语有消歧价值」相近；文档与 A001 行对齐，多角色交替但读法不改变执行者时不再补主语。
- **ruling:** rejected
- **reason:** 基线 §8 第 1 条「多角色交替执行」与冻结的 A001 行条件不同（Opus 轨道 r3 冷读亦报出）；B 向 A001 行对齐。A 亦引用 A001。

### C202 — fable · doc B · vs_baseline
- type: strengthened
- severity: WARNING
- baseline_quote: 重新抽取 (情态, 数值, 量化, 因果, 否定作用域, 施事, 指代, 条件, 时序, 受保护标记) 并与第 2 步的记录逐项比较。
- doc_quote: 重新抽取第 2 步的全部字段，另加逻辑方向（合取／析取、充分／必要、分组）、指代与受保护标记，与第 2 步的记录逐项比较。
- why: 第 7 步复核集合由 10 项元组改为第 2 步全部 12 个字段加逻辑方向、指代、受保护标记：新增动作、对象、例外、原子性分组、阈值与边界包含性、逻辑方向的渲染后复核；基线的「数值」经第 1 步进入受保护集合仍被覆盖。复核范围扩大，且消除了基线第 7 步与第 2 步字段不一致的问题（阶段 1 X-F9 所述）。
- **ruling:** rejected
- **reason:** 同 C23/C99。

### C203 — fable · doc B · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 5. 执行所需、而来源与上下文都未提供的信息（CTC-S002）——缺失信息一律归第 5 类，不论是哪条规则先发现它；
- doc_quote: 5. 第 2–4 类之外、执行所需而来源与上下文都未提供的信息，不论由哪条规则发现（CTC-S002）；
- why: 第 5 类的论域由「一律」改为「第 2–4 类之外」，消除了与第 2–4 类（同为缺失信息）的归类冲突。类别编号不进入输出格式，准入结果不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C204 — fable · doc B · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 调用方可以显式授权四类本来禁止的改动：调整规范强度、精确的单位换算、解除某个受保护标记的保护、指定改写目标或长度上限。
- doc_quote: 调用方可以显式授权本来禁止的改动，即调整规范强度、精确的单位换算、解除某个受保护标记的保护、指定改写目标或长度上限，以及规则条文中写明的授权（CTC-P003 的合并步骤、CTC-R005 的改变格式）。
- why: 删去计数「四类」，并把 CTC-P003、CTC-R005 规则行中已存在的授权并入列表。授权集合与基线规则行一致，只是汇总处不再与规则行不一致。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C205 — fable · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 改写、压缩与翻译之后逐项核对；任一项出现偏离都是一处 finding，其严重级别由 §7 中该行所引规则的级别决定
- doc_quote: 返回之前逐项核对下表各规则保护的不变量；任一项被破坏，先修复再返回。review 模式下，任一项偏离都是一处 finding，严重级别按 §8 确定。
- why: 偏离产生 finding 的规定被限定到 review 模式，改写模式下改为修复。基线该句与 §3「改写没有可分级的 finding」及 §11「先修复再返回」冲突（阶段 1 X-F7），文档取后者；改写模式下的行为由不确定变为「修复」。
- **ruling:** style-only
- **reason:** 同 C98。

### C206 — fable · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: - **STYLE** — 不影响语义的自然度或一致性问题。
- doc_quote: **可以** = 许可，不影响语义（STYLE）
- why: STYLE 定义去掉「自然度或一致性问题」。基线该定义与映射「应 → WARNING」冲突（R003、T001 均为应），文档收窄为「可以」级；自然度与一致性 finding 只能按 WARNING 报告，STYLE 只剩 CTC-R006。ERROR 定义同处合并，去掉「硬不变量被违反」，由「必须」级违反覆盖。
- **ruling:** rejected
- **reason:** 同 C27：描述性定义与冻结映射冲突，向映射收敛。

### C207 — fable · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 应写成「停止写入，等待复制延迟归零后执行切换。」
- doc_quote: 应写成「停止写入，等待并检查复制延迟，然后执行切换。」
- why: 示范改写不再补出来源没有的阈值「归零」，也保留「检查复制延迟」为操作者动作。基线示例与基线 CTC-S002／§6「不得补出缺失的……阈值」矛盾（阶段 1 X-F5）；文档示例与规则一致，但以示例为模板的执行者在并句时的行为随之改变。
- **ruling:** example-correction · pooled as X-B
- **reason:** 同 C101/C102/C103。

### C208 — fable · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 反例：磁盘空间不足时，旧快照会被自动清理。 ← 去被动正当，删掉具名施事不正当；两处改动只有前一处有规则依据。 正例：磁盘空间不足时，存储管理机制会销毁旧快照数据。
- doc_quote: 反例：磁盘空间不足时，旧快照会被自动清理。 ← 删掉具名施事，另增「自动」、删「数据」、以「清理」替换「销毁」，均无规则依据。 正例：原样返回。施事已在同句给出，被动是自然的技术表述（CTC-R003），不触发去被动。
- why: 正例由被动改主动变为原样返回，注释由「去被动正当」变为「均无规则依据」。基线示例与基线 CTC-R003 边界及 CTC-R001 矛盾（阶段 1 X-F3／X-F4）；文档示例与规则一致。执行者对「施事在同句的被动句」的处理由改写变为保留。
- **ruling:** example-correction · pooled as X-B
- **reason:** 同 C101/C102/C103。

### C209 — fable · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: 正例：1. 启动 `chunk-server`。2. 确认状态为 `READY` 且元数据已加载。3. 加入写入路由表。 　　　并附「待确认」说明上限未能满足。
- doc_quote: 正例：1. 启动 `chunk-server`，确认状态为 `READY` 且元数据已加载。2. 加入写入路由表。 ← 校验仍由操作者执行、位于加入路由表之前、判据列全。 若不删校验就无法达标，按 CTC-S001 返回超限文本并在「待确认」中说明
- why: 同一输入（授权合并、上限 2 步）的示范输出由「3 步 + 待确认」变为「合并后的 2 步」，基线的处理降为无法合规合并时的回退。基线示例与基线 CTC-P003 的合并许可矛盾（阶段 1 X-F11）；文档示例与规则一致，但对该输入的示范输出不同。
- **ruling:** example-correction · pooled as X-B
- **reason:** 同 C101/C102/C103。

### C210 — fable · doc B · vs_baseline
- type: altered
- severity: WARNING
- baseline_quote: - 尽快回滚 | 「尽快」承担义务，强度未定 | 作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认
- doc_quote: - 尽快回滚 | 「尽快」未给出时限，所承担义务的强度未定 | 回滚时限与作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认
- why: 「待确认」示例的「问题」与「需要的信息」栏各增一项（未给出时限／回滚时限）。与 CTC-R004「在「待确认」中提出」缺失判据一致，但示范的条目内容比基线多要一项信息，执行者据此产出的条目会不同。
- **ruling:** style-only
- **reason:** 同 C94。

### C211 — fable · doc B · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 模式未指定时，按 §3 的适用范围推定，并在文档类型跨界时取更严的一档。
- doc_quote: 模式未指定时，审阅任务用 review；其余任务按 §3 中 strict 与 standard 的适用范围推定，文档类型跨界时取 strict。
- why: 「更严的一档」在两档之间即 strict；「审阅任务用 review」是基线按 review 适用范围推定的显式化。推定结果不变。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C212 — fable · doc B · vs_baseline
- type: altered
- severity: STYLE
- baseline_quote: 歧义阈值按被审文档的类型选取（agent 指令与 runbook 用 strict 的阈值，说明性文档用 standard 的阈值）。
- doc_quote: 歧义阈值按被审文档的类型选取：属于 strict 适用范围的用 strict 的阈值，属于 standard 适用范围的用 standard 的阈值。
- why: 示例式括注改为按适用范围归属的完整映射；覆盖的文档类型一致。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C213 — fable · doc B · vs_baseline
- type: added
- severity: WARNING
- baseline_quote: 未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察。
- doc_quote: 未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。
- why: 新增对 STYLE 观察的规则 ID 要求。基线 §3 已要求每条 finding 引用规则 ID，但未明确 STYLE 观察是否属 finding（阶段 1 X-F8 所涉）；文档把要求扩展到观察，review 输出格式随之收紧。
- **ruling:** confirmed (WARNING) · pooled as D-B3
- **reason:** 同 C97。

### C214 — fable · doc B · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 模式改变的是**歧义阈值**，不是规则级别。
- doc_quote: 三种模式下全部规则按其级别生效，模式只改变**歧义阈值**，不改变规则级别
- why: 新增「三种模式下全部规则按其级别生效」，把基线 strict「全部规则生效」与 standard 只列 S、L、T、A、P 的隐含结论写明；未改变任何规则的生效范围。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C215 — fable · doc B · vs_baseline
- type: added
- severity: STYLE
- baseline_quote: 正例：在生产环境部署该服务前，请确保已配置环境变量。
- doc_quote: 正例：在生产环境部署该服务前，请确保已配置环境变量。 ← 「请确保」保持请求强度；「如果你想……」「你已经……了」是英语从句语序残留（CTC-R003）。
- why: 为既有正例补注归因说明，改写文本本身不变；「其余改动归 CTC-R003」与基线「语域清理另归 CTC-R003」同义。
- **ruling:** style-only
- **reason:** 评审自评为 STYLE：措辞、示例或重复表述的删改，规则行与要求可还原。

### C216 — fable · doc B · fork
- probe: 模式
- readings: ['读法 1（状态提示与「告警与错误信息」同类）：取 strict 阈值→ 更多 A、P 触发', '读法 2（状态提示不在 strict 范围内、也非跨界）：取 standard 阈值→ 仅普通技术读者会分歧的读法才报']
- **ruling:** confirmed (WARNING) · pooled as D-B4
- **reason:** 同 C106。

## Control document C: judge calibration

| judge run | seeds found cold (phase 1) | seeds found vs baseline (phase 2) | severity given to s3 | new-in-C findings that are not seeds (false positives) | findings marked also_in_baseline (baseline's own score) | forks on C |
|---|---|---|---|---|---|---|
| opus-A (Y=C) | s1, s2 | s1, s2, s3 (3/3) | ERROR | 0 | 11 of 13 | 7 (5 also in baseline) |
| opus-B (X=C) | s1, s2 | s1, s2, s3 (3/3) | ERROR | 0 | 12 of 14 | 8 (7 also in baseline) |
| fable-A (Y=C) | s1, s2 | s1, s2, s3 (3/3) | WARNING | 0 | 8 of 10 | 5 (3 also in baseline) |
| fable-B (X=C) | s1, s2 | s1, s2, s3 (3/3) | WARNING | 0 | 10 of 12 | 8 (6 also in baseline) |

Rule-level maps: all four judges 29/29 on every document (8 of 8). s3 deletes a 必须-level requirement sentence from a 必须 row; ERROR is the severity the pre-registered rule gives it, so both Fable runs under-rated s3.

## Pooled results by candidate (label-blind)

### Candidate A
- Confirmed ERROR-level semantic loss (lost / weakened / strengthened of a normative assertion): **0**.
- Confirmed WARNING-level semantic changes (pooled): **D-A2** modal-vagueness scope narrowed to three words (C12, C113); **D-A4** new rule for the review 规则 field of missing-information findings (C5, C116); **D-A5** new procedure for reviewing sourceless text with intra-text conflicts routed to CTC-A005 (C25, C118); **D-A6** 「未发现违规」 condition disambiguated (C28). Two of these (D-A4, D-A5) are genuine normative additions that the frozen-semantics constraint forbade.
- Confirmed self-hosting findings: **D-A1** ERROR (A005 fork: the R004 word list vs the §5 split; contested severity — Opus A005/ERROR, Fable R004/WARNING; inherited-and-transformed from the baseline's conflict at the same locus); **D-A3** WARNING (「过长」 in the frozen R003 row; inherited).
- Forks: 0 of 13 probes (both judges).
- Example corrections: 2 (X-A001, X-P003).
- Naturalness 4/4; over-control 5 (Opus), 4 (Fable).

### Candidate B
- Confirmed ERROR-level semantic loss: **0**.
- Confirmed WARNING-level semantic changes (pooled): **D-B2** the pre-return checks for CTC-R001, R002/R003 and the output contract are gone (C90, C196); **D-B3** STYLE observations must cite a rule ID (C97, C213; the same disambiguation A made in D-A6).
- Confirmed self-hosting findings: **D-B1** WARNING (状态提示 in no mode scope; inherited from the baseline).
- Forks: 1 of 13 probes (**D-B4**, the same 状态提示 gap; inherited).
- Example corrections: 4 (X-A001, X-S002, X-R003, X-P003).
- Naturalness 4/4; over-control 5/5.

### Provisional lexicographic ranking (pre-registered order)
1. Confirmed ERROR-level loss: A 0, B 0 → tie; both adoptable on this criterion.
2. Confirmed ERROR-level self-hosting findings not inherited unchanged from the baseline: A 1 (D-A1, contested), B 0 → **B ahead**.
3. Forks newly introduced: A 0, B 0 (B's one fork is inherited) → tie.
4. Confirmed WARNING-level items newly introduced: A 4, B 2 → B ahead.
5. Compression: A −26.3%, B −13.6% → A ahead.
6. Naturalness: tie.

Under the pre-registered order B ranks first. The margin on criterion 2 rests on one contested finding; if the reviewer rules D-A1 WARNING, criteria 2 and 3 tie and B still leads on criterion 4, with A leading only on compression.

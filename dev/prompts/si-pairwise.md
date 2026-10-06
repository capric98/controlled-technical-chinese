# 成对裁定

工作目录：/Users/capric98/Git/controlled-technical-chinese

你将比较两份候选。输入：

- 同一评审模型对第一份候选的评审 `{{YAML_FIRST}}` 与对第二份候选的评审 `{{YAML_SECOND}}`（各含阶段 1 与阶段 2）；
- 编排者的确定性指标表 `{{METRICS}}`（字符数、压缩率、规则表逐行 diff、门禁结果）；
- 允许翻阅 `dev/inbox/si/blind/A.md`、`dev/inbox/si/blind/B.md` 与根目录 `SKILL.md`（基线）核实任何一条主张。禁止读取其他文件；不派生子代理。

不要猜测两份候选由谁产出。评审 YAML 里的主张是证据，不是结论：你可以核实后不采信。

按下列维度分别裁定 winner ∈ {A, B, tie}、confidence ∈ [0, 1]、reason（引用具体证据）、what_would_flip（什么证据会翻转判断）：

1. semantic_preservation：相对基线的丢失、弱化、改变、新增，按严重级别看，ERROR 优先。
2. self_compliance：自宿主 finding，ERROR 优先。
3. controlledness：反向解码 fork 的数量与后果。
4. compression：在 1–3 不劣的前提下更短者胜；若一方以语义丢失换取长度，本维度不能判其胜。
5. naturalness：自然度与过度控制分数及其证据。
6. overall：按优先级 1 > 2 > 3 > 4 > 5 综合；任一方存在 ERROR 级语义丢失则不能 overall 胜出。

输出 YAML 到 `{{OUT}}`，键：`order_presented`（{{ORDER}}）、`dimensions`（六项，各含 winner、confidence、reason、what_would_flip）、`overall_summary`（不超过 200 字）、`files_read`、`model`（你系统提示中的模型名称）。最终回话给出六项 winner 与 confidence。

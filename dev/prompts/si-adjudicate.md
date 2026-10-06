# 裁决复核（标签盲）

工作目录：/Users/capric98/Git/controlled-technical-chinese

编排者对评审提出的主张作出了裁决（confirmed / rejected / style-only）。你独立复核这些裁决。你不知道候选由谁产出，也不要猜测。编排者本身也是参与实验的模型之一，因此它的裁决需要你这一道复核。

输入：`{{ADJ}}`。每条包含：主张编号、主张来源、候选标签（A 或 B）、基线引文、候选引文（或 absent）、编排者认为覆盖该断言的候选段落（裁为 rejected 时）、spec 中相关规则条目摘录（规则级主张时）、编排者的裁决与理由。

允许读取：`{{ADJ}}`、`dev/inbox/si/blind/A.md`、`dev/inbox/si/blind/B.md`、根目录 `SKILL.md`。禁止其他文件；不派生子代理。

复核规则（与编排者相同，预先登记）：主张 confirmed 当且仅当所引基线断言在候选中找不到保持同级别、同条件、同范围的表述；候选别处有则 rejected；只换措辞则 style-only。spec 摘录与 `SKILL.md` 不一致处以 `SKILL.md` 为准。

对每条给出：`verdict: agree|disagree`、`your_ruling`（confirmed / rejected / style-only）、`reason`（引用文本）、`disagreement_type`（deterministic / semantic / naturalness / scope，仅 disagree 时）。

输出 YAML 到 `{{OUT}}`，另给 `files_read` 与 `model`（你系统提示中的模型名称）。最终回话给出 agree / disagree 计数。

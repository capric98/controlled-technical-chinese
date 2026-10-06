# 合并候选独立复核（两阶段）

工作目录：/Users/capric98/Git/controlled-technical-chinese

你是一个独立评审。待评文档：`dev/inbox/si/merge/SKILL.md`（下称「候选」），是「受控技术中文（CTC）」技能的一份新渲染。不要猜测它由谁产出、如何产出。仓库 `AGENTS.md` 的多模型协议在此暂停；你是单一评审，编排者事后裁决。不得派生子代理。

**分段写入**：每完成下面一项任务，就把该项结果追加写入输出文件；不要在全部想完之后一次性写。

## 阶段 1（冷读）

允许读取：仅候选一个文件。不读根目录 SKILL.md 或仓库中任何其他文件。

- **T1 规则级别映射**：29 条规则各自的级别（必须／应／可以），逐字从候选中读；缺失写 missing。
- **T2 自宿主审阅**：把候选当作 agent 指令（strict 阈值），用它自身的规则、以它自身的 review 模式审阅它自己。六字段 finding（规则、严重级别、位置逐字引用、问题、风险、建议修改），编号 F1…。宁可少报不凑数；「理论上可解析出两种读法」不算歧义。重点：规范强度稳定、无判据词承担判定条件、无来源断言、示例与规则矛盾、指代与施事、术语一致、规则间冲突（含引用的类别、字段、数量与定义处不一致）、过度控制。
- **T3 反向解码**：对下列探针仅凭候选重建 级别、范围、触发、要求、禁止、例外、不变量；能读出两种以上导致不同执行行为的读法时 fork=yes 并写出各读法与行为。探针：CTC-S001、CTC-S003、CTC-A001、CTC-A005、CTC-P003、CTC-P004、CTC-R001、CTC-R002、CTC-R004 与 §5 情态模糊段、模式（阈值差异；是否改变级别；未指定时如何推定）、「待确认」准入清单、调用方授权清单、review 流程与「未发现违规」时的输出、返回前核对（§7 第 7 步）。
- **T4** 自然度 1–5、过度控制 1–5，各附 2–4 处逐字引文。

输出写入 `dev/inbox/si/merge/review-fable.yaml`（YAML 第一个文档，`judge_phase: 1`），键：`files_read`、`rule_levels`、`selfhost_findings`、`reverse_decoding`、`naturalness`、`over_control`。完成后最终回话给出计数与你系统提示中的模型名称，然后等待阶段 2。

## 阶段 2（对照基线）——收到消息后才开始

新增允许读取：根目录 `SKILL.md`（基线）。以基线为来源、候选为输出，逐项比对（断言集合、情态、条件与例外、逻辑方向、阈值边界、否定作用域、量化论域、执行者、时序、受保护标记、规则 ID 归属；29 条规则行逐行比对）。列出 lost／weakened／strengthened／altered／added，每条给出基线引文、候选引文（或 absent）、严重级别（ERROR = 改变规则的执行行为；WARNING = 可能改变；STYLE = 仅措辞、理据或示例）与理由。同一断言在基线多处、在候选保留一处不算 lost，除非保留处丢了成分。示例的期望输出被改为与其所演示的规则行一致、而基线示例与该行矛盾时，类型记为 `example-correction`。再对阶段 1 每条 finding 标 `also_in_baseline: yes|no`。

以 `---` 分隔追加第二个 YAML 文档（`judge_phase: 2`），键：`files_read_phase2`、`vs_baseline`、`phase1_reclassification`、`summary`。可以用 `uv run --with pyyaml python3 -c "import yaml; list(yaml.safe_load_all(open('dev/inbox/si/merge/review-fable.yaml')))"` 校验。最终回话给出 vs_baseline 计数（类型 × 严重级别）与模型名称。

# si6 — adversarial semantic review of the candidate edits (Opus 5.5)

你是受控技术中文（CTC）项目的**对抗性语义审阅者**。你的职责：找出候选改动改变了哪些语义不变量，构造它会误触发或漏触发的反例，并检查每处改动是否满足规则准入门槛。你不负责中文措辞的润色，也不提出与这些改动无关的新规则。

## 可以读的文件（只读；除了你的输出文件，不要修改任何文件）

- `dev/inbox/si6/base/SKILL.md` —— 基线（当前发布版本，si5 v2）
- `{CAND}` —— 候选
- `dev/inbox/si6/cand/build.py` —— 候选由基线经精确替换得到；注释写明每处的动机与所依据的探针或自托管 finding
- `dev/inbox/si6/probes/probes.yaml` —— 探针及其预先登记的预期；`dev/inbox/si6/probes/resolutions.yaml` —— 维护者的决定（M1–M7）
- `eval/reports/raw/si6-probe-base-r{1,2,3}/*.claude.json` —— 基线在探针上的三次输出（Opus 5.5）
- `eval/reports/raw/si6-selfhost-base-r{1,2}/*.claude.json` —— 基线的两次自托管审阅
- `eval/gold/gold-rendering.yaml` 中的 G-R-007，`eval/gold/gold-procedure.yaml` 中的 G-P-004，`eval/gold/gold-semantic.yaml` 中的 G-S-001
- `docs/decisions/000-design.md` §20（准入门槛）、`009-si4-criteria-bounds-metric-conditions-terminology.md`、`010-si5-permission-description-exemptions-guarded-threshold.md`

不要读 `dev/inbox/si6/review/` 下其他审阅者的文件，也不要读 `eval/reports/raw/` 下候选版本（非 base）的输出。

## 任务

候选有五处替换：

- **F1**（M2）：frontmatter `description` 末尾增加「不用于营销文案、品牌叙事、文学写作、SEO 与一般性文字润色。」
- **R1**（M3）：CTC-R004 的无判据词列表增加「紧急时」。
- **G1**（M5）：§5 许可豁免的第三个限定「所许可的也不是破坏性、不可逆或改变外部状态的操作」→「所许可的做法也不在默认动作之外增加破坏性、不可逆或改变外部状态的操作」。
- **B1**（M6）：CTC-P003 自身判据的门槛增加括注「（为后续这类操作建立恢复点的备份、快照也算）」。
- **U1**（M7）：§3 调用方授权增加「调整规范强度的授权没有指明哪些条目、调整到何种强度时，正文不改，按第 5 类在「待确认」中请调用方指明。」

逐处：

1. **语义变化**：候选比基线多允许了什么、多禁止了什么、改变了哪条规则的触发或要求。规则级别是否变化。
2. **证据是否支撑**：所引的失败（探针或自托管 finding）是否真的由这处措辞引起；改动是否是能解决该失败的最小改动；是澄清还是新增。
3. **反例**：至少构造两个具体输入（中文技术文本，带任务与模式），一个**误触发**，一个**漏触发**。写出输入、候选会怎样做、为什么错。请特别检查：
   - G1：「默认动作」在真实文本里是否可判（来源没有默认动作时怎么办）；许可改变的是时机或方式而不是操作种类时（提前执行、跳过建议的验证）落在哪一边；与「来源规定的义务不被免除」的关系。
   - B1：会不会让每个备份步骤都被提出，使普通流程文档的未决项成串回来；备份之后的操作只是改变外部状态而不破坏数据时（切流量）怎样处理；导出、复制等「事实上的备份」。
   - R1：「紧急变更」「紧急回滚」这类作为流程名称或类别的说法会不会被当作无判据词；未定义的状态（「服务不稳定」）是否仍按 CTC-A005。
   - U1：明确指明条目与强度的授权（「把第 3 条的『应』改为『必须』」「把所有『必须』改为『应』」）是否仍被执行；「改得更严格」这类方向相反的含糊授权；与「待确认」第 5 类定义的关系。
   - F1：含推广语句的发布说明、README 等仍属适用范围的文本，会不会因 description 的排除项而被当作营销文案。
   构造不出可信反例时，写明尝试过哪些方向。
4. **与其他规则的冲突**：改动是否与某条规则行、§2 阶梯、§3 输出契约与「待确认」七类、§5 或 §8 相矛盾。
5. **裁决**：`accept` / `revise` / `reject`。`revise` 必须给出替换后的完整措辞，且只能比候选更小或更窄，不能增加新的要求。

不要因为「这样更安全」而建议新增约束；任何新约束都必须附一个失败输入。

## 输出

写入 `dev/inbox/si6/review/adversarial.yaml`（YAML，中文内容）：

```yaml
reviewer: adversarial
model: <你的模型 ID>
files_read: [...]
edits:
  - id: F1 | R1 | G1 | B1 | U1
    semantic_change: ...
    level_change: none | <说明>
    evidence_supports: yes | partly | no
    evidence_note: ...
    clarification_or_new: clarification | new
    counterexamples:
      - kind: false_fire | missed_fire
        task: ...
        mode: ...
        input: |
          ...
        candidate_behaviour: ...
        why_wrong: ...
    conflicts: [...]
    verdict: accept | revise | reject
    revised_wording: ...   # verdict 为 revise 时必填
    rationale: ...
other_observations: [...]   # 只记录与这些改动直接相关的问题
```

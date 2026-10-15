# si3 — second cold reverse-decode, on the final candidate (Opus 5.5)

你是一名冷读者。读完本说明后，你只能读一个文件：`dev/inbox/si3/cand/v6/SKILL.md`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README、构建脚本、其他候选、其他审阅者的文件）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. CTC-R003（全文）：触发条件；「译文腔」「口语腔」所列各项是封闭清单还是举例；「去除这些缺陷时，工具描述改为直接陈述功能…」是独立的触发条件，还是只在列明缺陷出现后才适用的修复形式；「去口语腔时禁止的强度不变…」管到哪些词。
2. 下列四处在改写中（未注明者为 strict）各应得到什么输出，引用哪些规则 ID：
   (a) 工具描述（standard）：「这个工具可以帮你把 CSV 转成 JSON，文件最大 10 MB 哦。」
   (b) 工具描述（standard）：「通过这个函数，开发者可以把图片压缩到指定尺寸。」
   (c) agent 指令：「千万别在生产库上跑这个脚本啊。」
   (d) 工具描述（standard）：「该接口允许调用方在收到 `429` 后重试一下。」
3. §8 审阅流程第 2 步：review 模式下，SOP 中的「服务稳定后关闭变更单」「多次失败后升级」「尽快回滚」三处各引用哪条规则 ID、什么严重级别；依据哪一句。
4. §7 第 6、7 步与 CTC-R001：第 7 步「没有留下译文腔或口语腔」是否授权改动不含 CTC-R003 列明缺陷的文本。

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异。第 2、3 题另给出你的答案。

## 输出

写入 `dev/inbox/si3/review/decode-v6.yaml`（YAML，中文内容，简洁）：

```yaml
reviewer: cold-decoder
model: <你的模型 ID>
files_read: [...]
probes:
  - probe: ...
    level: ...
    scope: ...
    trigger: ...
    requires: ...
    prohibits: ...
    exceptions: ...
    fork: yes | no
    readings:            # fork 为 yes 时
      - id: A
        reading: ...
        behavior: ...
    answer: ...          # 第 2、3 题
    notes: ...
```

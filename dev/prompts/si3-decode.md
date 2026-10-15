# si3 — cold reverse-decoding of the candidate (Opus 5.5)

你是一名冷读者。你只能读一个文件：`{CAND}`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README 等）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. CTC-R003（全文）。
2. CTC-R001 与 CTC-R003 的关系：哪些编辑可以归因到 CTC-R003；「口语腔」所列的五类是封闭清单还是举例。
3. CTC-R004（全文）：词表是封闭清单还是开放类；类的成员由什么判定。
4. 状态提示：调用方未指定模式时，改写一条状态提示用哪种模式；审阅一条状态提示用哪种歧义阈值。依据哪一句。
5. 下列七处在改写中（未注明者为 strict），哪些编辑是规则允许或要求的，哪些不允许，各引用哪条规则 ID。逐处给出你预期的输出文本：
   (a) 错误信息：「哎呀，导出失败了呢，请您过一会儿再试一下哈。」
   (b) agent 指令：「你要记得哦，用户问到价格的时候千万别瞎猜，先查一下 `price_api` 吧。」
   (c) agent 指令：「用户道谢时，回复「不客气呀～」，不要追加别的内容。」
   (d) 工具描述（standard）：「这个工具可以帮你把 CSV 转成 JSON，文件最大 10 MB 哦。」
   (e) 告警：「`disk-03` 使用率 95% 了，估计是日志没轮转吧，先别重启。」
   (f) 工具描述（standard）：「该接口允许调用方在收到 `429` 后重试，单次请求最多 100 条。」
   (g) 工具描述（standard）：「按订单号查询订单状态，返回 `status` 字段。」
6. review 模式审阅这份 SOP，给出每处 finding 应引用的规则 ID 与严重级别，并说明依据：
   「1. 部署完成后，及时通知值班组。2. 服务稳定后关闭变更单。3. 酌情清理旧镜像。」

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异。第 4–6 题另给出你的答案。

## 输出

写入 `dev/inbox/si3/review/decode.yaml`（YAML，中文内容）：

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
    answer: ...          # 第 4–6 题
    notes: ...
```

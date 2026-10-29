# si4 — second cold reverse-decoding, on v3 (Opus 5.5)

你是一名冷读者。你只能读一个文件：`{CAND}`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README 等）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. 检查或确认步骤缺少判据时怎样处理。下列四份 runbook 分别在改写（strict）与审阅中怎样处理：是否进入「待确认」或成为 finding，引用哪条规则 ID，审阅时报什么严重级别，依据哪一句：
   (a) 「1. 将 `app.yaml` 中的 `log.level` 改为 `debug`。2. 执行 `systemctl reload app`。3. 检查 `app` 的运行情况。」
   (b) 「1. 将 `app.yaml` 中的 `log.level` 改为 `debug`。2. 执行 `systemctl reload app`。3. 确认 `app` 运行正常。」
   (c) 「1. 执行 `migrate apply 0051`，删除 `users` 表的旧列 `nickname_old`。2. 将写流量切回 `users-api`。」
   (d) 「1. 将 `node-3` 从集群摘除。2. 观察一段时间，确认服务正常后，执行 `nodectl destroy node-3`。」
   另说明：「超时后重试，多次失败则升级处理」中的「多次」与「升级」是否受这条限制影响。
2. CTC-R004 与 CTC-A005 的边界。审阅下面这份 SOP，逐处给出规则 ID 与严重级别，并说明依据哪一句：
   「1. 请求量明显上升时，扩容 `gateway`。2. 扩容后尽快通知值班组。3. 收到 `pool_exhausted` 告警后，把 `db.pool.max` 调到适当的值。4. 磁盘占用偏高时，清理 `/tmp/cache/`。5. 必要时回滚到上一版本。」
3. CTC-R003 对工具描述与其他文本的作用。下列五处在改写中（未注明者为 standard），哪些编辑是规则允许或要求的，各引用哪条规则 ID，逐处给出你预期的输出文本：
   (a) 工具描述：「通过这个接口，调用者可以批量删除过期会话，单次最多 1000 条。」
   (b) 工具描述：「开发者可以用这个函数把 Markdown 渲染成 HTML。」
   (c) 工具描述：「只有管理员账号可以调用此工具，用于重置用户密码。」
   (d) 开发者指南：「开发者可以通过 `--dry-run` 预览迁移将要执行的 SQL。」
   (e) agent 指令（strict）：「你可以调用 `refund_order` 为用户退款。」
4. §6 的级别定义：「应」级规则可以被什么推翻。「规则条文写明的」修饰哪些成分。
5. frontmatter 的 description 与 §5：上下文能确定读法的歧义怎样处理；二者是否一致。

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异，并给出你的答案。

## 输出

写入 `dev/inbox/si4/review/decode-v3.yaml`（YAML，中文内容）：

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
    answer: ...
    notes: ...
```

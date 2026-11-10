# si6 — cold reverse-decoding of the candidate (Opus 5.5)

你是一名冷读者。你只能读一个文件：`{CAND}`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README 等）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. 许可句中的模糊条件是否提出（改写，strict）或报告（审阅）。逐条给出处理方式、规则 ID、审阅时的严重级别，以及依据哪一句：
   (a) 「数据迁移建议在凌晨进行。若数据量较大，也可以分三个窗口迁移。」
   (b) 「服务默认以 INFO 级别输出日志。若磁盘紧张，也可以把日志级别调为 WARN。」
   (c) 「发布前建议先在预发环境验证。若时间紧张，也可以直接发布。」
   (d) 「每周日清理 `/var/log/app/` 下的旧日志。若磁盘紧张，也可以提前到周五清理。」
   (e) 「若队列积压，也可以临时扩容 `worker`。」（来源没有其他句子）
2. 操作步骤自身缺少成功判据时是否提出（改写，strict）或报告（审阅），依据哪一句：
   (a) 「1. 创建 `pv-data` 的快照。2. 把 `data` 卷缩容到 50Gi。」
   (b) 「1. 备份 `nginx.conf`。2. 修改 `nginx.conf` 中的 `worker_processes`。3. 执行 `nginx -s reload`。」
   (c) 「1. 执行 `make test`。2. 将 `config/` 目录备份到 `/backup/config/`。」
   (d) 「1. 把 `users` 表导出为 `users.csv`。2. 清空 `users` 表。」
   (e) 「1. 备份数据库。2. 将流量切换到备用集群。」
3. 下列说法按哪条规则处理（审阅），严重级别，依据哪一句：
   (a) 「紧急情况下，可以跳过审批直接上线。」
   (b) 「紧急变更须在 24 小时内补录变更单。」
   (c) 标题「## 紧急回滚（目标 5 分钟内完成）」下的步骤
   (d) 「服务不稳定时，暂停发布。」
4. 调用方授权（改写，strict，来源是三条「必须」或「应」的 SOP）。下列指令各适用什么处理，依据哪一句：
   (a) 「把要求放宽一些」
   (b) 「把第 3 条的『应』改为『必须』」
   (c) 「把所有『必须』改为『应』」
   (d) 「把这份 SOP 改得更严格」
   (e) 「改写目标：让新入职的工程师也能看懂」
5. 读 frontmatter 的 `description`：请求「润色这份发布说明，让它更有吸引力」与「改写这份发布说明里的升级步骤」是否属于本技能的使用范围，依据哪一句。

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异，并给出你的答案。

## 输出

写入 `dev/inbox/si6/review/decode.yaml`（YAML，中文内容）：

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

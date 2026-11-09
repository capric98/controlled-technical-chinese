# si5 — cold reverse-decoding of the candidate (Opus 5.5)

你是一名冷读者。你只能读一个文件：`{CAND}`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README 等）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. 缺少判据或阈值时是否提出（改写，strict）或报告（审阅）。逐条给出处理方式、引用的规则 ID、审阅时的严重级别，以及依据哪一句：
   (a) 运维说明：「数据归档建议在周末执行，以降低对报表查询的影响。若归档量偏大，也可以分两天完成。」
   (b) 运维说明：「数据归档须在周末执行。若归档量偏大，须分两天完成。」
   (c) API 文档：「当订阅数接近配额时，服务会暂停创建新订阅，已有订阅照常运行。」
   (d) API 文档：「当订阅数接近配额时，服务会暂停创建新订阅；此时请提交配额申请。」
   (e) runbook：「1. 修改 `redis.conf` 的 `maxmemory` 为 `8gb`。2. 确认配置无误后，执行 `systemctl restart redis`。」
   (f) runbook：「1. 将 `app.yaml` 中的 `log.level` 改为 `info`。2. 执行 `systemctl reload app`。3. 检查 `app` 的运行情况。」
   (g) 运维说明：「若磁盘紧张，也可以删除 30 天前的备份。」
2. 审阅中的术语差异。下列三份文本各怎样报告（规则 ID、严重级别），依据哪一句：
   (a) 「1. 在控制台把 `api` 的副本数调到 4。2. 确认 4 个 Pod 都处于 Running。」
   (b) 「请求头须携带访问令牌。令牌过期后，客户端用刷新凭据换取新的访问 token。」
   (c) 「1. 先在预发环境验证。2. 准生产环境验证通过后，再发布到生产。」
3. 「规范强度」：在本技能中指什么；调用方说「把这段里的『应』都改成『必须』」属于哪种授权，依据哪一句；它与 §6「级别」栏是什么关系。
4. CTC-R005 与 CTC-P004：改写一份 runbook 时，文末的「注意：执行前须备份数据库。」能否移到第 1 步前；步骤 3 句中的「确认无连接后」能否移到步骤 3 的动作之前；调用方要求「把所有注意事项合并到开头」时怎样处理。各依据哪一句。

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异，并给出你的答案。

## 输出

写入 `dev/inbox/si5/review/decode.yaml`（YAML，中文内容）：

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

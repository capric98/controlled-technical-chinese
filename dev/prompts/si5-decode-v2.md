# si5 — second cold reverse-decoding, on v2 (Opus 5.5)

你是一名冷读者。你只能读一个文件：`{CAND}`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README 等）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. 缺少判据或阈值时是否提出（改写，strict）或报告（审阅）。逐条给出处理方式、引用的规则 ID、审阅时的严重级别，以及依据哪一句：
   (a) 运维说明：「报表重算建议放在夜间，以减少对查询的影响。若排队任务较多，也可以分两批执行。」
   (b) 变更规范：「1. 数据库变更须经 DBA 审批后执行。2. 线上故障时，也可以先执行、事后补审批。」
   (c) 运维说明：「若磁盘紧张，也可以清空 `/var/cache/app/`。」
   (d) 运维说明：「若磁盘紧张，也可以把日志保留期从 30 天改为 14 天。」
   (e) API 文档：「当并发请求接近上限时，服务会返回 `429`。」
   (f) 排障文档：「## 现象\n队列积压明显增加。\n## 处理\n1. 扩容 `worker`。」
   (g) runbook：「1. 将 `values.yaml` 中的 `replicas` 改为 `6`。2. 执行 `helm upgrade web ./chart`。3. 将流量切换到 `web`。」
   (h) runbook：「1. 修改 `app.yaml`。2. 执行 `systemctl reload app`。3. 确认 `app` 运行正常。」
2. 省略的对象。下列三处在改写（strict）中能否补出对象，依据哪一句：
   (a) 「建议先在测试环境演练迁移脚本。若窗口不足，也可以顺延到下周。」
   (b) 「1. 修改 `nginx.conf`。2. 重启对应服务。」
   (c) 「先备份 `orders` 库，再清理 `orders_archive` 表。完成后通知 DBA。」（「完成」指哪一步）
3. 审阅中的术语差异：「1. 在控制台把 `api` 的实例数调到 4。2. 确认 4 个节点都已就绪。」报告什么规则 ID、严重级别；建议修改应怎样写。依据哪一句。
4. 「调整来源中的规范强度」这项授权的范围：调用方说「把这份 SOP 的要求放宽一些」时是否适用；说「把第 2 条的『应』改成『必须』」时是否适用。依据哪一句。

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异，并给出你的答案。

## 输出

写入 `dev/inbox/si5/review/decode-v2.yaml`（YAML，中文内容）：

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

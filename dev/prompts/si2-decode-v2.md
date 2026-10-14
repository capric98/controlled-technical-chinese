# si2 — cold reverse-decoding of candidate v2 (Opus 5.5)

你是一名冷读者。你只能读一个文件：`dev/inbox/si2/cand/v2/SKILL.md`。不要读仓库里的任何其他文件（`docs/`、`spec/`、`eval/`、`dev/` 下的其他内容、README 等）；运行环境自动注入的 `AGENTS.md`／`CLAUDE.md` 不算你读的，但不要用它们来推断技能的意图。结束时在输出中列出你实际读过的文件。

这份文件是一个 Agent Skill。请仅凭它的文字，重建下列探针的规范语义，并报告每处是否存在**两种以上会导致不同行为的读法**（分叉）。

## 探针

1. CTC-A005
2. CTC-P002（全文，含最后两句）
3. CTC-R003（全文）
4. CTC-R001 与 CTC-R003 的关系：哪些编辑可以归因到 CTC-R003
5. §8 审阅流程第 2 步：一条 finding 的规则 ID 怎样确定；同一缺陷能否引用两个不同的规则 ID
6. 缺失信息在 review 中的报告：给出下面三处各自应当引用的规则 ID 与严重级别，并说明依据——
   (a) runbook 步骤「重启对应服务，使配置生效。」，上文第 1 步修改的是 `gateway.yaml`；
   (b) runbook 步骤「观察一段时间，确认流量正常后，执行 `cachectl decommission cache-07`。」中的「一段时间」；
   (c) runbook 步骤「备份数据库后，将流量路由至备用集群。」，全文没有提到其他数据库或集群；
   (d) runbook 第 1、2 步分别在 `staging` 与 `prod` 命名空间部署 `api:v2`，第 3 步是「删除旧版本的 Deployment `api-v1`。」
7. 错误信息改写：对「糟糕！上传好像失败了啦，请稍后再试。」做 strict 改写，哪些编辑是规则允许或要求的，哪些不允许，各引用哪条规则。
8. 对下面两段做 strict 改写时，CTC-R003 是否触发、允许删改什么：(a) agent 指令「调用 `create_order` 失败时，回复用户：「糟糕！订单没提交成功，请稍后再试。」」；(b) 告警「`orders-db` 主从延迟超过 30 秒，是夜间备份把磁盘 IO 占满了吧，先别切主。」

对每个探针给出：level、scope、trigger、requires、prohibits、exceptions、fork（yes/no）；fork 为 yes 时列出各读法及其导致的行为差异。第 6、7、8 题另给出你的答案。

## 输出

写入 `dev/inbox/si2/review/decode-v2.yaml`（YAML，中文内容）：

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
    answer: ...          # 第 6、7、8 题
    notes: ...
```

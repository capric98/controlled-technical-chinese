# 独立评审 · 阶段 2（对照基线）

新增允许读取：根目录 `SKILL.md`（基线：当前发布版本）。仍禁止其他文件。X、Y 中可能有一份与基线高度相似；即便如此，也按同样的流程独立完成，不要因此跳过任何一项，也不要推断来源。

## 任务（对 X、Y 各做一遍）

### T5 语义可还原性

以基线为来源、文档为输出，按不变量逐项比对（断言集合、情态、条件与例外、逻辑方向、阈值边界、否定作用域、量化论域、执行者、时序、受保护标记、规则 ID 归属），列出：

- lost：基线中的独立断言（要求、禁止、例外、条件、阈值、类别、字段、步骤）在文档中找不到保持同级别、同条件、同范围的表述；
- weakened / strengthened：情态或范围改变（应↔必须、部分↔全部、条件被放宽或收窄）；
- altered：命题内容改变（对象、动作、顺序、数值、规则 ID 归属）；
- added：文档中有而基线没有的命题（新的要求、判据、频率断言、告警）。

每条给出：基线引文、文档引文（或 absent）、类型、严重级别（ERROR = 改变规则的执行行为；WARNING = 可能改变；STYLE = 仅措辞）、为什么算。

同一断言在基线出现多处、在文档只保留一处：不算 lost，除非保留处丢失了某个成分。规则级别与基线不同：ERROR。

### T6 重分类

回看你阶段 1 的 selfhost_findings 与 reverse_decoding：若某条其实是基线也有的问题，标 `also_in_baseline: yes`（不删除）；若对照基线后你认为阶段 1 某条不成立，标 `withdrawn: 理由`（不删除原条目）。

## 输出

在 `{{OUT}}` 的 YAML 中追加（保留阶段 1 的全部内容）：

```yaml
judge_phase: 2
files_read_phase2: [...]
documents:
  X:
    vs_baseline:
      - baseline_quote: ...
        doc_quote: ...          # or absent
        type: lost|weakened|strengthened|altered|added
        severity: ERROR|WARNING|STYLE
        why: ...
    phase1_reclassification:
      - id: X-F3
        also_in_baseline: yes|no
        withdrawn: null | "理由"
    summary:
      vs_baseline_counts: {lost: {ERROR: n, WARNING: n, STYLE: n}, weakened: {...}, strengthened: {...}, altered: {...}, added: {...}}
      selfhost_counts_after_reclass: {ERROR: n, WARNING: n, STYLE: n}
      forks: n
  Y:
    (同上)
```

最终回话：每份文档的 vs_baseline 计数（按类型 × 严重级别）；files_read；你系统提示中的模型名称。

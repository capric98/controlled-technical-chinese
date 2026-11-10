# si6 — naturalness and over-control review of the changed passages (Opus 5.5)

你是受控技术中文（CTC）项目的**中文语言审阅者**，负责自然度、译文腔、伪法律腔与过度控制。你不得改变任何规则的级别、触发条件、要求、例外或不变量；你只能就措辞提出等义替换，并指出措辞本身造成的歧义。

只读这两个文件：`dev/inbox/si6/base/SKILL.md` 与 `{CAND}`。二者只有以下几处不同：frontmatter `description` 末尾的一句；§3 调用方授权段新增的一句；§5「不算真歧义」一段中许可豁免的第三个限定；CTC-P003 行末门槛中的括注；CTC-R004 无判据词列表中的一个词。请自己用 `diff` 核对确切的改动段落。下文用以下 ID 指称它们：F1（description）、U1（§3 授权）、G1（§5 许可豁免）、B1（P003 括注）、R1（R004 列表）。

## 任务

对每处改动：

1. 自然度评分（1 = 译文腔或机械化严重，5 = 自然的专业技术中文），并引用具体字句说明。请特别看：G1「所许可的做法也不在默认动作之外增加…的操作」的语序与「做法」「操作」的搭配；B1 括注插在长句中间是否影响「且后续步骤…」的结合；U1「正文不改」与本文其他处「原样返回」「不改写」的用语是否一致。
2. 措辞造成的歧义：是否有指代、修饰结合域、并列、否定作用域上的两种读法。
3. 过度控制：这处措辞是否会让执行它的模型在目标文本上过度改写、过度报告或漏改、漏报。给出具体的目标文本例子。
4. 等义改写建议（可选）：只在你能保证语义完全不变时给出，并说明为什么等义。
5. 本技能自身的规范用词（必须、应、可以、不得）在新句子里是否用得一致；新句子本身有没有口语腔或译文腔（自托管）。

## 输出

写入 `dev/inbox/si6/review/naturalness.yaml`（YAML，中文内容）：

```yaml
reviewer: naturalness
model: <你的模型 ID>
files_read: [...]
passages:
  - id: F1 | U1 | G1 | B1 | R1
    candidate_text: ...
    naturalness: 1-5
    quotes: [...]
    ambiguity: [...]
    over_control_risk:
      - target_text: ...
        risk: ...
    equivalent_rewording: ...   # 可选
    rewording_is_equivalent_because: ...
    normative_vocabulary: ok | <问题>
overall_note: ...
```

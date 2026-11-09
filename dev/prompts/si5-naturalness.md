# si5 — naturalness and over-control review of the changed passages (Opus 5.5)

你是受控技术中文（CTC）项目的**中文语言审阅者**，负责自然度、译文腔、伪法律腔与过度控制。你不得改变任何规则的级别、触发条件、要求、例外或不变量；你只能就措辞提出等义替换，并指出措辞本身造成的歧义。

只读这两个文件：`dev/inbox/si5/base/SKILL.md` 与 `{CAND}`。二者只有以下几处不同：§3 调用方授权的「调整道义强度（规范强度）」；§5「不算真歧义」一段新增的两种情形及一句；§6 CTC-A005 行末一句与 CTC-P003 行末一句中的操作范围；CTC-S003 的三元组；T 族表后一段的 review 模式说法；CTC-R005 行的一处补充。请自己用 `diff` 核对确切的改动段落。下文用以下 ID 指称它们：N1（§3 授权）、N2（S003 三元组）、V1（T 族表后一段）、H1（A005 行末）、H2（P003 行末）、D1（§5）、S1（R005）。

## 任务

对每处改动：

1. 自然度评分（1 = 译文腔或机械化严重，5 = 自然的专业技术中文），并引用具体字句说明。请特别看：D1 新句的长度与分号并列（「…；条件只放宽…；文本只描述…。后两种情形…」）是否读得通，「后两种情形」的指代是否清楚；H1、H2 中「破坏性、不可逆或改变外部状态的操作」的修饰结合。
2. 措辞造成的歧义：是否有指代、修饰结合域、并列、否定作用域上的两种读法。
3. 过度控制：这处措辞是否会让执行它的模型在目标文本上过度改写、过度报告或漏改、漏报。给出具体的目标文本例子。
4. 等义改写建议（可选）：只在你能保证语义完全不变时给出，并说明为什么等义。
5. 本技能自身的规范用词（必须、应、可以、不得）在新句子里是否用得一致；新句子本身有没有口语腔或译文腔（自宿主）。

## 输出

写入 `dev/inbox/si5/review/naturalness.yaml`（YAML，中文内容）：

```yaml
reviewer: naturalness
model: <你的模型 ID>
files_read: [...]
passages:
  - id: N1 | N2 | V1 | H1 | H2 | D1 | S1
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

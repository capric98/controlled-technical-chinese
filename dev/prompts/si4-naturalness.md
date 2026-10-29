# si4 — naturalness and over-control review of the changed passages (Opus 5.5)

你是受控技术中文（CTC）项目的**中文语言审阅者**，负责自然度、译文腔、伪法律腔与过度控制。你不得改变任何规则的级别、触发条件、要求、例外或不变量；你只能就措辞提出等义替换，并指出措辞本身造成的歧义。

只读这两个文件：`dev/inbox/si4/base/SKILL.md` 与 `{CAND}`。二者只有以下几处不同：frontmatter 的 description 一处；§3 standard 的「记录级别」；§6 级别定义中的「明确边界」；CTC-A005 行末新增一句；CTC-P003 行中关于合并授权的一句；CTC-R003 行「把读者当作谈话对象的引导」的括注；CTC-R004 行的排除项；§8 第 2 步的括注；§9 第 1 条的示例。请自己用 `diff` 核对确切的改动段落。

## 任务

对每处改动：

1. 自然度评分（1 = 译文腔或机械化严重，5 = 自然的专业技术中文），并引用具体字句说明。请特别看：CTC-A005 新句的长度与「是否提出或报告按 CTC-P003 判断」的语序；CTC-R004 排除项三个并列成分是否读得通（「给可测量指标设限而未给出阈值的程度说法」）；CTC-R003 括注里分号与「同属此类」的结构。
2. 措辞造成的歧义：是否有指代、修饰结合域、并列、否定作用域上的两种读法（例如 CTC-P003「调用方授权合并步骤（明确要求合并，或限定步骤数）时」中括注修饰的是什么；「规则条文写明的边界」中「写明的」管到哪里；frontmatter「上下文不足以确定的歧义只报告、不擅自消解」中顿号前后的关系）。
3. 过度控制：这处措辞是否会让执行它的模型在目标文本上过度改写、过度报告或漏改、漏报。给出具体的目标文本例子。
4. 等义改写建议（可选）：只在你能保证语义完全不变时给出，并说明为什么等义。
5. 本技能自身的规范用词（必须、应、可以、不得）在新句子里是否用得一致；新句子本身有没有口语腔或译文腔（自宿主）。

## 输出

写入 `dev/inbox/si4/review/naturalness.yaml`（YAML，中文内容）：

```yaml
reviewer: naturalness
model: <你的模型 ID>
files_read: [...]
passages:
  - id: F1 | T1 | T2 | T3 | T4 | B1 | B2a | B2b | C1
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

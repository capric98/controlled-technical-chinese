# si4 — adversarial semantic review of the candidate edits (Opus 5.5)

你是受控技术中文（CTC）项目的**对抗性语义审阅者**。你的职责：找出候选改动改变了哪些语义不变量，构造它会误触发或漏触发的反例，并检查每处改动是否满足规则准入门槛。你不负责中文措辞的润色，也不提出与这些改动无关的新规则。

## 可以读的文件（只读；除了你的输出文件，不要修改任何文件）

- `dev/inbox/si4/base/SKILL.md` —— 基线（当前发布版本）
- `{CAND}` —— 候选
- `dev/inbox/si4/cand/build.py` —— 候选由基线经精确替换得到；注释写明每处的动机与所依据的探针或自宿主 finding
- `dev/inbox/si4/probes/probes.yaml` —— 探针及其预先登记的预期；`dev/inbox/si4/probes/resolutions.yaml` —— 维护者的决定（M1–M6）与计分说明
- `eval/reports/raw/si4-probe-base-r{1,2,3}/*.claude.json` —— 基线在探针上的三次输出（Opus 5.5）
- `eval/reports/raw/si4-selfhost-base-r{1,2}/*.claude.json` —— 基线的两次自宿主审阅
- `eval/gold/gold-procedure.yaml` 中的 G-P-003，`eval/gold/gold-rendering.yaml` 中的 G-R-010，`eval/gold/gold-tokens.yaml` 中的 G-T-101（本轮按维护者决定 M3 修订）
- `eval/disagreements/D004-misdiagnosed-checkpoint-merge.md`
- `docs/decisions/000-design.md` §20（准入门槛）、`003-core-semantic-policy.md`、`004-rule-set-adjudications.md`（尤其 §3）、`007-si2-review-routing-and-p002-boundary.md`、`008-si3-register-r004-class-status-scope.md`

不要读 `dev/inbox/si4/review/` 下其他审阅者的文件，也不要读 `eval/reports/raw/` 下候选版本（非 base）的输出。

## 任务

候选有九处替换，分四组：

- **F1**（frontmatter）：「歧义只报告不擅自消解」→「上下文不足以确定的歧义只报告、不擅自消解」。
- **T1–T4**（术语与定义）：「记录级别」→「级别」；CTC-P003 中「压缩授权」改为「授权合并步骤（明确要求合并，或限定步骤数）」并重排该句；§9 第 1 条的示例加「应」；§6「明确边界」→「规则条文写明的边界」。
- **B1、B2**（行为）：CTC-A005 行末加一句，把「来源完全没有给出成功判据或验证方式的步骤」交给 CTC-P003 的限制（提案 15，决定 M5）；CTC-R004 的排除项加「给可测量指标设限而未给出阈值的程度说法（「延迟较高」）」，§8 第 2 步同步（决定 M4）。
- **C1**：CTC-R003 的「把读者当作谈话对象的引导」加注「工具描述中以使用者作主语的「调用者可以…」同属此类」（提案 20）。

逐组（F1、T、B、C1；T 组内四处可合并写，但有问题的单独写）：

1. **语义变化**：候选比基线多允许了什么、多禁止了什么、改变了哪条规则的触发或要求。规则级别是否变化。
2. **证据是否支撑**：所引的失败（探针或自宿主 finding）是否真的由这处措辞引起；改动是否是能解决该失败的最小改动；是澄清还是新增。
3. **反例**：至少构造两个具体输入（中文技术文本，带任务与模式），一个**误触发**，一个**漏触发**。写出输入、候选会怎样做、为什么错。请特别检查：
   - B1：「完全没有给出判据」与「给出的判据含义未定」的界线在真实 runbook 里是否可判（例如「检查服务运行情况」「观察错误率」「确认正常后继续」）；破坏性步骤缺判据时是否仍会报告；会不会把本应按 A005 报告的执行信息缺失（接收方、参数）也一并交给 P003 而不报。
   - B2：「给可测量指标设限而未给出阈值的程度说法」会不会吞掉「尽快」「适当」这类 R004 词，或漏掉「响应变慢时」「流量突增时」这类说法；§5 关于 R004 的强度建议（第四栏）在 A005 一侧是否丢失了不该丢的东西。
   - T2：「限定步骤数」算授权、字数上限不算，是否与 D004、G-P-003 和 §3 的授权清单一致；「请精简」「压缩篇幅」这类指令落在哪一边。
   - C1：会不会在 agent 指令（「你可以调用…」是许可）、开发者指南（「开发者可以通过 `--dry-run`…」）或表达使用限制的工具描述（「只有管理员可以调用」）上误触发。
   - F1：改后的 description 是否仍与 §5 一致，有没有新的漏洞。
   构造不出可信反例时，写明尝试过哪些方向。
4. **与其他规则的冲突**：改动是否与某条规则行、§2 阶梯、§3 输出契约与「待确认」七类、§5 或 §8 相矛盾。B1 请检查与「待确认」第 2 类（CTC-P003）、第 5 类（CTC-S002）以及 R004 排除项「未定义的状态」的关系。
5. **裁决**：`accept` / `revise` / `reject`。`revise` 必须给出替换后的完整措辞，且只能比候选更小或更窄，不能增加新的要求。

不要因为「这样更安全」而建议新增约束；任何新约束都必须附一个失败输入。

## 输出

写入 `dev/inbox/si4/review/adversarial.yaml`（YAML，中文内容）：

```yaml
reviewer: adversarial
model: <你的模型 ID>
files_read: [...]
edits:
  - id: F1 | T | T2 | B1 | B2 | C1
    semantic_change: ...
    level_change: none | <说明>
    evidence_supports: yes | partly | no
    evidence_note: ...
    clarification_or_new: clarification | new
    counterexamples:
      - kind: false_fire | missed_fire
        task: ...
        mode: ...
        input: |
          ...
        candidate_behaviour: ...
        why_wrong: ...
    conflicts: [...]
    verdict: accept | revise | reject
    revised_wording: ...   # verdict 为 revise 时必填
    rationale: ...
other_observations: [...]   # 只记录与这些改动直接相关的问题
```

#!/usr/bin/env python3
"""Rebuild the merged SKILL.md from the Fable final (blind/A.md).

M1–M14: the merge reviewed by two independent reviewers (output: merge/SKILL.md).
F-a–F-e: fixes applied after that review (output: the root SKILL.md).
Every edit is an exact string replacement that must match once.
usage: python3 dev/inbox/si/merge/build.py   (run from the repository root)
"""
M = [
 ('M1', 'B: preamble', '语义先于风格。未触发规则即不改动。歧义只报告，不替作者决定。\n', '语义先于风格。\n'),
 ('M2', 'B: mode inference', '模式未指定时按 §3 的适用范围推定，文档类型跨界时取更严的一档。', '模式未指定时，审阅任务用 review；其余任务按 §3 中 strict 与 standard 的适用范围推定，文档类型跨界时取 strict。'),
 ('M3', 'B: rules apply in all modes', '模式改变的是**歧义阈值**，不是规则级别：', '三种模式下全部规则按其级别生效；模式改变的是**歧义阈值**，不是规则级别：'),
 ('M4', 'B: review threshold', 'agent 指令与 runbook 用 strict 的阈值，说明性文档用 standard 的阈值。', '属于 strict 适用范围的用 strict 的阈值，属于 standard 适用范围的用 standard 的阈值。'),
 ('M5', 'CTC-R006 consistency', '| strict / standard |', '| strict／standard |'),
 ('M6', 'revert D-A4', 'review 模式下它就是 finding 的「规则」字段，缺失信息的规则 ID 与其所属类别括注的规则一致。', 'review 模式下它就是 finding 的「规则」字段。'),
 ('M7', 'B: category 5', '5. 执行所需、而来源与上下文都未提供的信息；不属于第 2–4 类的缺失信息一律归本类，不论是哪条规则先发现它（CTC-S002）；', '5. 第 2–4 类之外、执行所需而来源与上下文都未提供的信息，不论由哪条规则发现（CTC-S002）；'),
 ('M8', 'B: modal example line', '- 最好在窗口内回滚 | 「最好」承担义务，可读作「应在窗口内回滚」或「可以在窗口内回滚」 | 作者意图的道义强度 | 建议按前者确认', '- 尽快回滚 | 「尽快」未给出时限，所承担义务的强度未定 | 回滚时限与作者意图的规范强度 | 可读作「必须立即执行」或「应在窗口内执行」，建议按前者确认'),
 ('M9', 'B: authorisation list', '调用方可以显式授权四类本来禁止的改动：(1) 调整道义强度（规范强度）；(2) 精确的单位换算；(3) 解除某个受保护标记的保护；(4) 指定改写目标或长度上限（如合并步骤、改变格式）。', '调用方可以显式授权本来禁止的改动，即调整道义强度（规范强度）、精确的单位换算、解除某个受保护标记的保护、指定改写目标或长度上限，以及规则条文中写明的授权（CTC-P003 的合并步骤、CTC-R005 的改变格式）。'),
 ('M10', 'B: modal vagueness (resolves D-A1, D-A2)', '**情态强度的模糊同样按本节处理**：规范性指令中，义务的强度由「最好」「尽量」「尽可能」这类无判据词承担时，报告其可能的两种以上强度并在第四栏给出建议，然后停手；「必要时」「适当」「合理」承担的是判定条件而非强度，只按第 4 类提出（CTC-R004）。改写不得把这些词替换为具体强度或阈值——那是替作者做未经授权的规范决定。', '**情态强度的模糊同样按本节处理**。改写时，规范性指令中由无判据词（见 CTC-R004）承担义务的条件，按 CTC-R004 在「待确认」中提出：指出缺失的判据，列出其可能的两种以上强度并给出建议，然后停手；不得把它替换为具体强度或具体阈值，那是替作者做出未经授权的规范决定。新写时按 CTC-R004 给出可观测的触发条件。'),
 ('M11', 'B: task vs mode term', '改写模式下差异本身不进「待确认」', 'strict／standard 模式下差异本身不进「待确认」'),
 ('M12', 'revert D-A5', '1. 按 §7 第 1–3 步建立比对基准，并按文档类型选取歧义阈值（§3）。被审文本没有独立来源时（审计既有文本、复核本技能自身文本），以被审文本自身为来源：来源与输出之间的不变量无从违反，只报告被审文本自身可观测的违规：竞争读法、指代、无判据条件、术语不一致等；文内两处陈述对同一情形要求不同行为时，按 CTC-A005 报告，位置引用两处。', '1. 按 §7 第 1–3 步建立比对基准：受保护标记、语义骨架、文档类型对应的歧义阈值（§3）。'),
 ('M13', 'B: no-finding output', '没有 ERROR 或 WARNING 级 finding 时返回「未发现违规」，其后最多列三条 STYLE 级 finding。', '未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。'),
 ('M14', 'CTC-T001: term in the A001 row', '**不得要求每句都有显式主语，', '**不得要求每句都有显性主语，'),
]
F = [
 ('F-a', 'combine A and B on the no-finding output', '未发现问题时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。', '没有 ERROR 或 WARNING 级 finding 时返回「未发现违规」，其后最多三条 STYLE 观察，每条引用规则 ID。'),
 ('F-b', 'step 7 paraphrase of CTC-R001 aligned to the row', '没有改动任何规则并未要求改动的地方（CTC-R001）', '没有改动无法归因到规则 ID 的地方（CTC-R001）'),
 ('F-c', 'authorisation list stated as closed', '调用方可以显式授权本来禁止的改动，即调整道义强度（规范强度）、', '调用方可以显式授权的本来禁止的改动限于：调整道义强度（规范强度）、'),
 ('F-d', 'restore the baseline classification of 「多次」「升级」', '原样保留，换成具体数字才是违规。', '原样保留，换成具体数字才是违规。「超时后重试，多次失败则升级处理」中的「多次」与「升级」缺少执行所需的信息，保留原句，逐项进「待确认」（§3 示例前两行）。'),
 ('F-e', 'restore the pre-return check of the output contract', '没有改动无法归因到规则 ID 的地方（CTC-R001）。', '没有改动无法归因到规则 ID 的地方（CTC-R001），输出符合 §3 的输出契约（无前言；结构与列表粒度保留；「待确认」仅在确有未决项时出现）。'),
]
def apply(t, edits):
    for i, why, old, new in edits:
        n = t.count(old)
        assert n == 1, (i, n)
        t = t.replace(old, new)
    return t
if __name__ == '__main__':
    a = open('dev/inbox/si/blind/A.md', encoding='utf-8').read()
    reviewed = apply(a, M)
    final = apply(reviewed, F)
    open('dev/inbox/si/merge/SKILL.md', 'w', encoding='utf-8').write(reviewed)
    open('SKILL.md', 'w', encoding='utf-8').write(final)
    print('wrote dev/inbox/si/merge/SKILL.md (reviewed) and SKILL.md (final)')

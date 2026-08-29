# D004 — A rule added on a misread, and how the misread happened

- **Status:** Resolved — the added constraint was withdrawn and re-scoped
- **Date:** 2026-08-29
- **Type (`000-design.md` §13):** rule scope misunderstood → specification evaluator
- **Parties:** the orchestrating Claude Opus (wrong), the three candidate models (right), the gold
  case itself (right, and ignored)

## What happened

The `r1` sweep showed Claude, GPT and Gemini all merging step 2 of `G-P-003` — a `READY`-state
confirmation — into an adjacent step. Three independent models producing the same edit is the
classic signature of a rule that does not say what it means, so it was diagnosed as one, and
`CTC-P003` was extended:

> 来源把验证单独列为一个步骤时，该步骤必须仍是独立步骤：不得并入被它验证的那一步，也不得并入它所守护的下一步。

The models kept merging. A worked example was added. They stopped merging and instead began
emitting a `待确认` item about a "3-step limit" that appeared nowhere in the prompt — which read
like a hallucinated constraint, and prompted a second rewrite of the example to remove any mention
of step counts. Gemini went on emitting it anyway.

At that point the case definition was finally read in full:

```yaml
instruction: 合并可以合并的步骤，压缩到不超过 3 步，操作行为保持不变。
```

The limit was in the case's own instruction. The models were not hallucinating and were not
violating a rule — they were following an explicit caller instruction to compress. And the case's
third invariant already said what the correct outcome was:

> 输出步骤数超过 3 但校验完整，优于步骤数达标而校验丢失。

The case was never about step count. It is an instruction-following case: it tests what happens
when a caller's compression request collides with behaviour preservation. The `notes` field said so
in one line — `指令本身诱导删校验点，考的是指令服从与行为保持冲突时的优先级` — and it was not read.

## What the rule should have said

Re-examined against the case's actual invariants, the `r1` outputs were mostly fine. Claude's
merged the confirmation into step 1 while keeping it an operator action, before the routing step,
with both conditions listed — which is what the invariant requires. GPT's turned it into a
condition clause (`确认…后，将新节点加入写入路由表`), which is weaker but still operator-executed and
still positioned before the guarded action.

There is a real defect in the neighbourhood, and it is not about step count:

> 调用方授权合并步骤时可以并入相邻步骤，但合并后它必须仍是由操作者执行、位于被守护动作之前、且逐项列全原有判据的确认动作。
> 把它改写为不需要操作者动作的状态描述（「节点就绪后加入路由表」），或丢掉其中任一判据，都是删除校验点。

That is what `CTC-P003` now says. Under it, both models compress to three steps as instructed and
keep the checkpoint intact, which is the correct behaviour on both axes.

## Withdrawn

- `CTC-P003`'s "an independent verification step must remain an independent step" clause. It made
  the skill refuse a legitimate caller instruction.
- `G-P-003`'s added `procedure` invariant requiring the step count to be preserved, and its two
  added `invalid_transformations`. All three contradicted the case's own instruction-following
  invariant. The case is back to what its author wrote, plus a note recording this episode.
- The §12 example is rewritten around the real conflict — compression instruction versus checkpoint
  integrity — instead of around step counts.

## Why this is recorded

`000-design.md` §20 requires a new hard constraint to rest on a demonstrated failure. This one
rested on a misread of what the evidence showed, and the anti-over-engineering gate did not catch
it, because the gate asks whether a failure was demonstrated and a failure had been — just not the
one that was diagnosed.

Three signals were available and each was passed over: the case's `instruction` field, its
third invariant, and its `notes`. The pattern is worth naming, because it will recur. **When
several independent models converge on the same behaviour, the first hypothesis should be that
they are responding to something real in the input, not that they share a defect.** Convergence
was read as evidence of a rule gap when it was equally evidence of instruction compliance, and only
one of those two readings was checked.

The concrete practice that follows: before diagnosing a failure from an evaluation output, read the
case's `instruction` and `notes`, not only its `source` and `invariants`. The harness sends the
candidate `source` and `instruction`; a diagnosis that has not read the `instruction` has not seen
what the model saw.

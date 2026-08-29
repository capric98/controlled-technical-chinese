# D001 — The naturalness auditor changed meaning while asserting it had not

- **Status:** Resolved — semantic invariant wins
- **Date:** 2026-08-28
- **Type (000-design.md §13):** "Proposed wording is natural but semantically lossy"
- **Authority applied:** semantic invariant, per the priority ladder in `000-design.md` §4
- **Source artifact:** `dev/inbox/r1-gemini-naturalness.yaml`
- **Reviewer:** orchestrating Claude Opus (specification compiler role)

## Context

Round 1 asked Gemini 3.7 Flash (high effort), in its assigned role as Chinese renderer and
naturalness auditor, to catalogue real naturalness failures. The prompt required every
`natural_zh` rewrite to preserve meaning exactly, and instructed it to **delete** any entry whose
rewrite could not preserve meaning. It returned `meaning_delta: none` on every retained entry.

Independent review of those entries found meaning changes in several of them.

## Findings

### 1. Obligation collapsed into verification — `TR-06`

```text
source:  确保数据已被成功备份，并且所有从节点都已正确地同步了主节点的数据。
rewrite: 确认数据备份完成，且所有从节点已与主节点数据同步。
```

`确保` places an obligation on the operator to bring the state about, including remediation if it
is not yet true. `确认` only requires observing whether it is already true. In a runbook, the
rewrite silently deletes the remediation duty. The rest of the rewrite (dropping 成功地 /
正确地) is a legitimate improvement; the verb swap is not.

### 2. Request strengthened into requirement — `TR-08`

```text
source:  如果你想在生产环境中部署该服务，请确保你已经配置了环境变量。
rewrite: 在生产环境部署该服务前，须完成环境变量配置。
```

`请确保` is a request. `须` is an obligation. The rewrite is better Chinese and is very probably
what the author meant, but strengthening modality is a decision the author must make, not a
rendering pass.

### 3. Actor deleted — `OC-04`

```text
source:  存储管理机制会在磁盘空间不足时把旧快照数据销毁。
rewrite: 磁盘空间不足时，旧快照会被自动清理。
```

The entry's own point — that a blanket ban on the passive damages Chinese — is correct and worth
keeping. But the rewrite drops the named actor `存储管理机制`, which is exactly the information
an incident responder needs. The demonstration and the violation are separable: the passive is
fine, deleting the actor is not.

### 4. Description converted into prohibition — `GA-02`

```text
ambiguous:      系统不会在工作时间重启主数据库并清空缓存。
disambiguated:  工作时间内，系统禁止重启主数据库，亦禁止清空缓存。
```

`不会` describes system behavior. `禁止` states a rule addressed to someone. Resolving negation
scope was the task; changing the sentence from a description of behavior into a prohibition was
not. The two have different truth conditions and different audiences.

### 5. Ambiguity silently resolved by choosing a reading — `GA-04`

```text
ambiguous:      隔离受感染的主机和网关通信。
readings:       (a) isolate the infected host AND the gateway traffic
                (b) isolate the infected host FROM the gateway
disambiguated:  阻断受感染主机与网关之间的通信链路。
```

The rewrite silently commits to reading (b) and additionally swaps `隔离` for `阻断`. When the
source is genuinely ambiguous and the intended reading is not recoverable from context, choosing
one reading manufactures a fact.

### 6. Quantity generalized — `TR-12`

```text
source:  由于该资源正在被另一个进程占用的事实，当前请求已被拒绝。
rewrite: 因该资源正被其他进程占用，当前请求已被拒绝。
```

`另一个进程` is one specific other process. `其他进程` is open-ended. Small, but it is a
quantifier change inside an error message, where the reader is trying to decide whether to retry.

## Analysis

The role hypothesis in `000-design.md` §11.3 predicted this exact risk and it reproduced on the
first independent pass, under an explicit instruction not to change meaning and with a
self-declared `meaning_delta: none` on every entry.

Two conclusions follow.

1. **A self-declared "meaning unchanged" is not evidence.** The renderer's assertion about its own
   output has no diagnostic value and must not be accepted as a check. Semantic verification has to
   be an independent pass over the rendered text, not a claim attached to it.
2. **The dangerous edits cluster in a small, enumerable set of verbs and particles.** All six
   findings are modality (`确保`/`确认`, `请`/`须`, `不会`/`禁止`), actor deletion, silent
   disambiguation, or quantifier scope. That is small enough to be checkable, which makes it a good
   basis for a rule rather than general advice to "preserve meaning".

The catalogue itself remains valuable. The translationese, over-control, over-editing, and
Chinese-specific ambiguity material is accepted as evidence; only the six rewrites above are
rejected as meaning-preserving.

## Consequences

- The rendering step in the CTC pipeline must be followed by an independent semantic re-check
  (`000-design.md` §27 step 7). This finding is the evidence that the step is load-bearing rather
  than ceremonial.
- Findings 1, 2, 4 and 6 become modality/quantity regression cases.
- Finding 3 becomes an actor-preservation regression case, paired with the passive-voice boundary
  case so that the rule does not over-fire into banning the passive.
- Finding 5 becomes the seed for the rule that unresolvable ambiguity is reported, not decided.
- No change to `000-design.md` is warranted: this confirms §11.3 rather than contradicting it.

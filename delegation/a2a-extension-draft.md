# DRAFT — A2A Extension Proposal: Delegation Receipts

> **STATUS: DRAFT ONLY. Not submitted anywhere. Not posted, not proposed to
> any working group, not sent to any person. Posting or submitting this
> proposal requires Black Lansky's explicit approval.**

## 1. Motivation

Agent-to-agent frameworks (including A2A) standardize *how* agents talk —
tasks, messages, artifacts, agent cards. None standardize *who authorized
whom*. When agent A delegates to agent B and B delegates to agent C, the
receiving agent — and any auditor — has no interoperable way to answer: "on
whose authority is C acting, and which human is ultimately responsible?"
Identity-verification threads in the agent community keep circling this gap:
verifying *who an agent is* without verifying *who let it act* leaves the
accountability question unanswered.

This draft proposes a minimal A2A extension that carries delegation receipts
(see `receipt-schema.json` / `spec.md`) alongside A2A tasks and messages.

## 2. Proposal summary

A new protocol extension identified by URI:

```
https://cumulativewebinc.github.io/cwi-learn/delegation/a2a-extension
```

Agents advertise support in their Agent Card:

```json
"capabilities": {
  "extensions": [
    {
      "uri": "https://cumulativewebinc.github.io/cwi-learn/delegation/a2a-extension",
      "description": "Attach hash-chained delegation receipts to tasks/messages; every delegation walks back to a human principal. (DRAFT)",
      "required": false
    }
  ]
}
```

(`capabilities.extensions` is the standard A2A AgentExtension mechanism:
`uri`, `description`, `required`, `params`. This draft uses it as-is — no
protocol changes required.)

## 3. How it works

When an agent delegates work under this extension, it attaches the delegation
receipt to the outbound A2A Task (`metadata.delegation_receipt`) or Message
(a `DataPart` with `mimeType: application/json` and the receipt as payload).
The receiving agent SHOULD:

1. Fetch the receipt chain referenced by the receipt's `parent_receipt_id`
   lineage (chains are content-addressed by `receipt_id`; publishers SHOULD
   serve them at stable URLs).
2. Run the verification algorithm (`spec.md` §7): hash links, seal integrity,
   authority continuity, principal traceability to a human.
3. Apply local policy: e.g. refuse tasks whose chain does not terminate at a
   known human principal, or whose `action_scope.forbidden` intersects the
   requested action.

Field mapping (receipt → A2A concepts):

| Receipt field | A2A concept |
|---|---|
| `delegator` / `delegatee` | Task requester / the agent the Task is sent to |
| `action_scope` | Task title/description + policy constraints |
| `principal` | The human accountable party (no A2A equivalent today) |
| `parent_receipt_id` lineage | Out-of-band chain; referenced from Task metadata |
| `signature` | Extends A2A's transport security with delegation-level provenance |

## 4. Why receipts instead of just identity

Identity answers "which agent is this." Delegation receipts answer "who let it
act, to do what, bounded by what, for which human." The two compose: an
identity-verified agent presenting an unverifiable delegation chain is
precisely the case this extension is built to catch — *an agent hired another
agent and nobody asked who was responsible.*

## 5. Security considerations

- Receipts are **claims**, not trust. Trust comes from verifying the chain and
  from the reputation of the key registry behind `ed25519` signatures.
- `operational-attestation` seals prove tamper-evidence only; receivers SHOULD
  treat them as weaker than registry-backed signatures and apply policy
  accordingly.
- Chains MUST terminate at `kind: "human"` principals; receivers SHOULD
  maintain an allowlist of principals they act for.
- Revocation (`action: revoke-delegation`) SHOULD be honored: work requested
  under a revoked scope SHOULD be refused.
- Replay: receipts authorize scopes, not individual calls; receivers SHOULD
  bind receipts to Task IDs in their own bookkeeping.

## 6. Open questions (for the community, if this is ever submitted)

1. Should the chain live inline in Task metadata or by reference? (Draft
   leans: by reference, content-addressed.)
2. Standard key-registry discovery from an Agent Card.
3. Interaction with A2A push notifications / streaming for revocation
   propagation.
4. Whether `required: true` should ever be set, and what fallback applies.

## 7. References

- Delegation receipt schema (v1.0.0): `receipt-schema.json`
- Spec + verification algorithm: `spec.md`
- Live dogfood chain (CWI's own ledger): `chain.jsonl`
- Reference verifier (stdlib-only Python): `verify.py`

---
*Draft authored by Cumulative Web Inc, 2026-09-15. Again: do not submit or
post without Black's explicit approval.*

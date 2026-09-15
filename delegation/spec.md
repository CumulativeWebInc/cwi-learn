# Delegation Receipts — Chain-of-Command Spec

**Version:** 1.0.0 · **Status:** active · **Maintainer:** Cumulative Web Inc
**Machine-readable schema:** [`receipt-schema.json`](receipt-schema.json) (JSON Schema draft 2020-12)
**Reference verifier:** [`verify.py`](verify.py) (Python 3, stdlib only)
**Live dogfood chain:** [`chain.jsonl`](chain.jsonl) — the CWI agent company's own delegation ledger

## 1. The problem

An agent hires another agent to do work. The work goes wrong — or right — and
nobody can answer the basic question: **who authorized whom to do what, and for
whom?** Agent-to-agent delegation today is a handshake with no receipt. This
spec defines that receipt: a small, hash-chained, machine-readable record of
every grant of authority, such that any delegation can be walked back, hop by
hop, to the human principal at the root.

## 2. Receipt anatomy

A receipt is one JSON object. Required fields:

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | string | `"1.0.0"` — the schema the receipt was minted under |
| `receipt_id` | string | 64-char SHA-256 hex; commits to body + signature (§4) |
| `parent_receipt_id` | string | `GENESIS` for the first receipt of a chain, else the previous receipt's `receipt_id` |
| `delegator` | agent object | The party granting authority |
| `delegatee` | agent object | The party receiving authority |
| `action_scope` | object | `action` (machine-readable id), `constraints[]`, `forbidden[]`, optional `expires_at` |
| `principal` | agent object, `kind: "human"` | The human at the root. Identical on every receipt in a chain |
| `timestamp` | string | ISO-8601 with timezone offset |
| `timestamp_precision` | enum | `exact` \| `approximate` \| `day` — honesty grading for the timestamp |
| `signature` | object | `algorithm` + `value` (§5); the tamper-evidence seal or identity signature |

Optional: `evidence_url` (public URL, or null when evidence is internal),
`evidence_note` (where the evidence lives when it is not public), `notes`
(free text, never used for authority).

Agent objects carry `agent_id` (stable, namespaced, e.g. `cwi:kingcode`),
`display_name`, `kind` (`human` | `agent` | `organization` | `service`), and
optional `platform`.

**Scope semantics.** `constraints` bound the delegation (cadence, briefs to
follow, approval gates). `forbidden` names explicit carve-outs — things the
delegatee must never do under this receipt. Reserved action:
`revoke-delegation`, which must name the revoked `receipt_id` in `constraints`;
a verifier SHOULD treat receipts downstream of a revocation as lapsed for the
revoked scope.

## 3. What "walks back to the human principal" means

For any receipt R, the **principal trace** is built by repeated lookup:

1. Start at R's `delegator`.
2. If it equals R's `principal.agent_id`, the trace is complete.
3. Otherwise find the earlier receipt in the same chain whose `delegatee` is
   that delegator, and repeat from *its* delegator.

A chain is valid only if every receipt's trace terminates at the chain's
principal, the principal is identical on all receipts, and the principal's
`kind` is `"human"`. Delegations that dead-end at an agent with no earlier
grant, that cycle, or that terminate at a non-human are rejected. This is the
accountability guarantee: **there is no authority in the system that cannot be
walked back to a named human.**

## 4. Hash-chaining rule

Canonical bytes for any object:

```
canonical(obj) = UTF-8( JSON.stringify(obj, sort_keys=true, separators=(",",":"), ensure_ascii=true) )
```

Minting, in order:

1. `body` = the receipt with `receipt_id` and `signature` removed.
2. `seal` = `SHA-256(canonical(body))` as lowercase hex → `signature.value`
   (for `operational-attestation`; §5).
3. `receipt_id` = `SHA-256(canonical(body + signature))` as lowercase hex.
4. `parent_receipt_id` = the previous receipt's `receipt_id`, or `GENESIS`.

Because `receipt_id` commits to the signature and the signature commits to the
body, editing any field invalidates the seal; re-minting the seal invalidates
`receipt_id`; re-minting `receipt_id` breaks the child's parent link. History
rewrites are detectable at the first untouched receipt downstream.

## 5. Signature requirements

Two algorithms are defined in 1.0.0:

- **`operational-attestation`** — a tamper-evidence seal: `signature.value`
  MUST equal `SHA-256(canonical(body))`. It proves the receipt has not been
  altered since the stated `signed_by` record-keeper sealed it. It is **not**
  an identity proof and MUST NOT be presented as one. Used for internal and
  dogfood chains where the parties share no key infrastructure.
- **`ed25519`** — production identity signatures. `signature.value` MUST be the
  128-char hex Ed25519 signature over `canonical(body)`; `key_id` is REQUIRED
  and MUST resolve in the chain's published key registry; `signed_by` MUST be
  the delegator. Key rotation and revocation are registry concerns; a verifier
  MUST reject signatures from revoked keys.

`verify.py` fully verifies `operational-attestation` seals. For `ed25519` it
validates structure (`key_id` present, 128-hex value) and reports that
cryptographic verification is deferred to the key registry — it does not claim
a verification it cannot perform.

## 6. Timestamp conventions

`timestamp` MUST be ISO-8601 with an explicit timezone offset
(e.g. `2026-09-15T20:35:00-04:00`). `timestamp_precision` grades honesty:

- `exact` — the stated time is known.
- `approximate` — known within about the hour.
- `day` — only the calendar date is known; the time component is the
  conventional `T00:00:00` marker in the stated offset and MUST NOT be read as
  a claim about the hour.

The ledger is an append log: entries may formalize delegations after the fact.
What MUST hold is **causal order** — no receipt may predate the authority it
exercises (§7, check 9). Global timestamp monotonicity across the file is not
required.

## 7. Verification algorithm

`verify.py` applies these checks in ledger order, and exits 1 naming the first
broken receipt (`receipt_id` + line number):

1. Each line parses as a JSON object with all required fields and
   `schema_version "1.0.0"`.
2. Field formats: 64-hex `receipt_id`; `parent_receipt_id` is `GENESIS` or
   64-hex; tz-aware ISO-8601 timestamp; `timestamp_precision` in enum;
   delegator/delegatee objects with `agent_id`; principal object with
   `kind "human"`; `action_scope.action` non-empty with a `constraints` list;
   `evidence_url` null or an http(s) URI; signature has `algorithm` + `value`.
3. Signature seal valid per §5 (attestation digests recomputed; ed25519
   structure-checked with cryptographic verification reported as deferred).
4. `receipt_id` recomputation matches (tamper-evidence).
5. Hash-chain continuity: first receipt's parent is `GENESIS` (and only the
   first); every other parent equals the previous receipt's `receipt_id`.
6. Authority: each delegator either IS the principal (root delegations) or was
   a delegatee on an earlier receipt in the same chain.
7. Principal constancy: one identical human principal across the chain.
8. Principal traceability: every receipt's delegator chain terminates at the
   human principal (§3), with cycle/dead-end detection.
9. Causal timestamps: no receipt predates its delegator's earliest grant.

On success it prints the receipt count, the principal, and the chain tip.

## 8. The genesis chain (live dogfood)

[`chain.jsonl`](chain.jsonl) is Cumulative Web Inc's own delegation ledger —
the company visibly using this spec on itself. It models only the real company
structure and delegations that actually happened:

- `cwi-dr-0001`: Black Lansky (principal, human) → KingCode — stand up the
  8-department agent company, with approval gates (2026-09-14).
- `cwi-dr-0002…0009`: KingCode → the 8 department coordinators (A&R, Marketing
  & Social, Sync & Licensing, Radio & Playlists, Press & PR, Content Studio,
  Data & Analytics, Business Affairs) — run the department lane per BRIEF.md.
- `cwi-dr-0010`: Black Lansky → KingCode — full autonomous build/operate rights
  with standing carve-outs (no spending/wallet signing; nothing sent or
  published without exact-text approval) (2026-09-15).
- `cwi-dr-0011`: KingCode → first-touch recruit coordinator — send the 40
  owner-approved recruit messages verbatim (2026-09-15).
- `cwi-dr-0012`: KingCode → social content operation coordinator — build the
  content/outreach operation from actual album art (2026-09-15).
- `cwi-dr-0013`: Radio & Playlists → Audiartist round-2 submitter — submit
  "Diabolique" at the scheduled slot (2026-09-15 8:35 PM ET).
- `cwi-dr-0014`: Marketing & Social → Moltbook watchlist engager — ongoing
  stay-in-touch engagement (2026-09-15).

All fourteen receipts use `operational-attestation` seals applied by the chief
of staff's office as record-keeper, formalizing the delegations from the
company's dated directives and logs (see each receipt's `evidence_note`).
Verify it: `python3 verify.py chain.jsonl`.

## 9. Appending and versioning

Append new receipts as new JSONL lines; never edit existing lines. Consumers
identify the tip by the last line. Schema changes are versioned in
`schema_version`; verifiers MUST reject versions they do not implement.
This document is version 1.0.0 of the spec.

## 10. Related

- A2A interop proposal (draft, not submitted): `a2a-extension-draft.md`
- MCP tool contract: `tools/needle_drop_record_delegation.json` in the
  `agent-deck-mcp` repo

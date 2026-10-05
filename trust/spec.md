# CWI Verdict Engine — Open Trust-Scoring Specification

**Version:** 1.0.0
**Status:** Draft for review (branch `needs/verdict-engine`, PR unmerged)
**Owner:** Cumulative Web Inc
**Date:** 2026-09-15

## 1. Purpose

ERC-8004 standardizes agent identity, but deliberately leaves three gaps open:
no score aggregation, no Sybil resistance, no dispute resolution. The Verdict
Engine is the open, deterministic layer on top. It turns evidence into trust
scores with published rules — no hidden weights, no randomness, no invented
numbers.

**Hard truth rule:** a trust engine that invents scores is worse than none.
Every number must trace to evidence. When in doubt, the engine outputs
`insufficient-data`.

## 2. Signal families

The engine scores over exactly three evidence families. Nothing else is an input.

### 2.1 `erc8004` — on-chain identity signals

Agent identity claims conforming to ERC-8004: protocol registration records,
verified claim transactions, wallet-linked attestations. This family anchors
*who* the subject is.

### 2.2 `needle_drop` — verified history

Entries from the CWI Needle Drop ledger (`needle-drop/needle-drop.json`) with
status `verified` — hash-chained, proof-attached placements / completed
commercial history. The ledger ships empty and gains entries only on
verification; an empty ledger contributes zero signals. An empty-but-honest
ledger is recorded, never penalized.

### 2.3 `first_spin` — published verdicts

Production First Spin verdicts (format `cwi-first-spin/v1`) carrying full
confidence labels and source citations. **Excluded:** worked examples, demo
data, drafts, and anything labeled illustrative — e.g.
`first-spin/sample-verdict.json` is a labeled worked example and is never
admitted as evidence.

## 3. Input schema

```json
{
  "engine_version": "1.0.0",
  "subject": { "agent_id": "MUSE_CWI", "display_name": "KingCode (CWI chief agent)" },
  "context": "agent-trust",
  "observed_at": "2026-09-15T19:30:00Z",
  "signals": {
    "erc8004":     [ { "evidence_id": "e8004-moltbook-claim-20260915",
                        "kind": "protocol-registration-claim",
                        "issuer": "moltbook",
                        "identity_cluster": null,
                        "issuer_type": "third_party",
                        "description": "MUSE_CWI (KingCode) Moltbook account claimed — email verified.",
                        "status": "verified",
                        "observed_at": "2026-09-15",
                        "source_url": null,
                        "source_ref": "CWI agent watchlist + Moltbook heartbeat logs, 2026-09-15",
                        "weight_class": 2 } ],
    "needle_drop": [],
    "first_spin":   []
  },
  "evidence_notes": { "needle_drop": "Ledger verified empty as of 2026-09-15." }
}
```

Field rules:

| Field | Required | Rule |
|---|---|---|
| `engine_version` | yes | Must equal the engine's `ENGINE_VERSION`; mismatch → `invalid-input`. |
| `subject.agent_id` | yes | Non-empty string. The trust subject. |
| `subject.display_name` | no | Human label. |
| `context` | yes | One of the §7 registry. Unknown → `unknown-context` refusal. |
| `observed_at` | yes | ISO-8601 date or datetime. The engine never reads the clock. |
| `signals` | yes | Object with exactly the three family keys, each a list. |
| `evidence_id` | yes | Non-empty, unique within its family. |
| `kind` | yes | Free-form evidence kind string. |
| `issuer` | yes | Non-empty. Who vouches for this evidence. |
| `identity_cluster` | no | Groups issuers controlled by one entity (same wallet root, same domain). Null = issuer stands alone. |
| `issuer_type` | yes | `self` (subject vouches for itself) \| `third_party` \| `protocol`. |
| `description` | yes | Non-empty. What the evidence says. |
| `status` | yes | `verified` \| `claimed` \| `pending` \| `disputed` \| `refuted`. |
| `observed_at` | yes | When the evidence was observed. |
| `source_url` | no | Public URL, or null. |
| `source_ref` | no | Citable reference when no URL exists (log name, ledger entry, observation record). |
| `weight_class` | yes | 1, 2, or 3 per §4. |
| `evidence_notes` | no | Per-family free-text notes, passed through to output. |

## 4. Evidence admission and weight classes

Only `status: "verified"` evidence counts toward a score.

- `claimed` / `pending` → weight 0, listed in the trace as `not-counted`.
- `refuted` → weight 0, recorded in the trace.
- `disputed` → the engine **refuses to score**: output status `evidence-disputed`.
  A live dispute is resolved off-engine; the engine will not pick a side.

Weight classes are public, not hidden:

| Class | Meaning | Example |
|---|---|---|
| 1 | Self-asserted | Subject's own claim about itself |
| 2 | Third-party attested | Independent platform/observer record |
| 3 | Protocol- or ledger-sealed | Hash-chained ledger entry, on-chain attestation |

## 5. Sybil-damping rule

Sybil attacks (many sock-puppet issuers, one controller) and evidence spam
(one issuer, many items) are damped deterministically:

- **D1 — issuer cap:** within one family, one identity cluster contributes at
  most **2** verified items. Surplus items are kept out of the score and marked
  `damped: "issuer-cap"`. Kept items are the highest `weight_class` first,
  ties broken by lowest `evidence_id` (deterministic).
- **D2 — identity clustering:** issuers sharing an `identity_cluster` count as
  **one** issuer for D1. Fifty wallets, one human → one issuer.
- **D3 — self-assertion discount:** items with `issuer_type: "self"` count at
  **0.5 ×** their weight class. Self-praise is evidence, but discounted —
  openly, not secretly.

All damped items remain visible in the output trace with their damping reason.

## 6. Scoring algorithm

For each family, over verified items only, after D1–D3:

```
kept_weight  = Σ (weight_class × 0.5 if issuer_type == "self" else weight_class)
family_score = kept_weight / (kept_weight + 3.0)
```

The constant `3.0` is the published saturation constant: one class-3 item
scores 0.50, two score 0.667, diminishing returns thereafter. Bounded in (0, 1).

**Cold-start gate (§7):** if the context gate is not met, the output is

```json
{ "status": "insufficient-data", "score": null, "band": null,
  "missing": ["erc8004: 0 verified evidence items (1 required)", "..."] }
```

`missing` enumerates exactly what is absent. **A null score is never a number.**

If the gate is met: `score = mean(family_score)` over families with ≥1 kept
item, rounded to 3 decimals; `band` from §8.

Every output carries `input_sha256` — sha256 over the canonical JSON of the
input (`sort_keys=True`, compact separators) — binding the score to the exact
input that produced it.

## 6b. Provenance anchoring (added 2026-09-16 — from public review, vina)

`input_sha256` binds a verdict to the exact input that produced it, but it
does not bind the input to the evidence the links pointed at. A
centralized authority can retrospectively alter its own pages without
changing the URL; the verdict is then reproducibly wrong. Reproducibility
is a property of the verdict. Stability of the source is a separate
prerequisite.

Provenance anchoring is an independent third axis, alongside source
reliability (evidence-bound, §§4–5) and staleness (time-decayed at read,
`observed_at`):

| Anchor level | Meaning |
|---|---|
| `anchored` | Evidence content pinned at scoring time to a decentralized timestamp or content-addressed store (e.g. timestamped hash, IPFS-style CID); `anchor_ref` carries the caller-supplied reference. |
| `unanchored` | Evidence cited by URL/reference only. The verdict is verified-on-a-snapshot, explicitly labeled as such. |

Scored verdicts carry `provenance: "anchored" | "unanchored"` next to
`input_sha256`. Bands (§8) are unchanged; a `verified-unanchored` verdict is
still scored, but the anchor level is part of the grade a reader sees. When
no anchor exists, `unanchored` is the honest default — not a penalty, a
description. The anchoring mechanism (timestamp service, content store) is a
build task, not a spec change; this section reserves the axis so the spec
stays honest in the meantime. The engine records only the caller-supplied
`anchor_ref` — no clock reads, no network calls (§10 unchanged).

## 7. Contexts and cold-start protocol

Each context defines its own evidence gate. Contexts are per-use-case because
trust is not fungible: payment trust needs commercial history; review trust
needs review history.

| Context | `min_verified` | `min_families` | Required | Rationale |
|---|---|---|---|---|
| `agent-trust` | 3 | 2 | `erc8004` | General trust needs an anchored identity plus corroboration from a second family. |
| `music-review` | 2 | 1 | any of `first_spin`, `needle_drop` | Music-domain trust needs music-domain evidence. |
| `payments` | 2 | 2 | `erc8004` **and** `needle_drop` | Paying a counterparty needs a verifiable identity anchor plus completed commercial history. |

Gate check uses **pre-damping** verified counts (sufficiency of evidence);
scoring uses **post-damping** kept weights (quality of evidence). Both are
reported in the trace.

## 8. Score interpretation bands

Bands apply only when `status == "scored"`.

| Score | Band | Meaning |
|---|---|---|
| 0.800 – 1.000 | `established` | Deep, multi-family verified evidence. |
| 0.600 – 0.799 | `emerging` | Solid evidence, still building. |
| 0.400 – 0.599 | `thin` | Real evidence, but sparse. |
| 0.200 – 0.399 | `weak` | Minimal verified signal. |
| 0.000 – 0.199 | `negligible` | Barely above cold start. |

## 9. What the engine refuses to score

The engine returns a refusal status — never a number — when:

- **`insufficient-data`** — the context gate is not met. This is the normal
  cold-start outcome for new subjects, not a penalty.
- **`evidence-disputed`** — any submitted evidence has status `disputed`.
- **`unknown-context`** — the context is not in the §7 registry.
- **`invalid-input`** — schema violation (bad version, missing fields,
  bad enum values, duplicate `evidence_id` within a family).

The engine additionally refuses to admit: worked examples and demo data
(§2.3), evidence without an issuer, and evidence whose only source is
"trust me".

## 10. Determinism guarantees

- Canonical key sorting for hashing; fixed insertion order for output.
- No clock reads, no randomness, no network calls, no hidden state.
- IEEE-754 double arithmetic; identical interpreter → byte-identical output.
- `tests.py` asserts byte-identical reruns.

## 11. Versioning

SemVer. Any change to weights, thresholds, damping rules, or gates is a
**minor** bump. Any change to the input/output schema is a **major** bump.
Outputs always carry the `engine_version` that produced them.

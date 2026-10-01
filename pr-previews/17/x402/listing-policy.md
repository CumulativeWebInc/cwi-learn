# CWI Verified x402 Directory — Listing Policy (v1.0.0)

An index of self-registered listings is a directory of alibis. This directory
lists only services whose claims have been **earned** — by evidence anyone can
re-run. The three verdicts a listing must carry:

## 1. The three verdicts (all required, all machine-checkable)

**Authorship — the provider stands behind the listing.**
A hash-chained attestation receipt (Needle Drop receipt discipline: sha256
chain, `prev_hash` linked, tamper-evident) sealing the evidence bundle. It must
be resolvable *without trusting this directory*: recompute the sha256 of the
attested artifact and compare it to the receipt. Upgrade path (v1.1): a signed
capability attestation from the provider's key.

**Evidence — a real paid run, not a schema.**
A First Spin verdict receipt from a real paid-protocol run against the service.
"We run it, we pay, the receipt is the listing's proof." The verdict must
record: the unpaid 402 challenge (scheme, network, amount, asset, payTo), the
paid flow (signed authorization submitted, facilitator verdict observed), what
the service actually returned, and every claim with a confidence label
(`verified` / `derived` / `estimated` / `unverifiable`) plus a cited source
with an observation date. Unproven claims (e.g. on-chain settlement without a
tx hash) are labeled `not_proven`, never omitted.

**Completeness — the full declared surface, pinned.**
The service's `/.well-known/x402` manifest (IETF
`draft-hawkins-x402-dns-discovery` shape) fetched and pinned at listing time.
`manifest_url` in the directory points at it. Manifest drift (routes, prices,
or network changing without a new listing revision) is a re-verification
trigger, not a silent update.

## 2. Seed rule

The directory starts with us and the earning policy. v1.0.0 seeds **only**
Cumulative Web Inc's own real x402 endpoints
(`cwi-playlist-check`, `cwi-momentum-score` — USDC on Base Sepolia testnet,
prices verified against the live server's `/pricing` route table on
2026-09-15). **No other listings are invented.** Every future listing enters
through section 3.

## 3. How a listing is earned (any provider)

1. **Propose** via pull request adding the listing JSON + the two evidence
   files under `x402/evidence/<service>/`. Self-claims without evidence are
   closed, not debated.
2. **Paid run**: the directory operator (or an independent verifier) runs the
   real paid flow against the candidate endpoint and writes the First Spin
   verdict receipt. The receipt — not the provider's description — is what the
   listing asserts.
3. **Attestation**: the provider (or operator, for the seed) seals a
   hash-chained attestation receipt over the verdict.
4. **Manifest pin**: the candidate's `/.well-known/x402` is fetched, checked
   against the IETF draft shape, and pinned; `manifest_url` recorded.
5. **Labeling**: testnet vs mainnet stated explicitly; `settlement_proven`
   true only with a settled tx hash on record; `endpoint_reachability`
   `public` or `private` stated honestly. A private pilot MAY be listed —
   labeled `testnet_pilot`, never dressed as production.
6. **Merge** only when `reverify.py` passes on the branch.

## 4. Weekly re-verification

- Every listing carries `last_reverified` (date) and `reverify_due`
  (`last_reverified` + 7 days).
- `x402/reverify.py` is the checker: manifest reachable and valid JSON,
  evidence URLs reachable and valid, `last_reverified` within 7 days,
  endpoint challenged (public listings must still answer 402 correctly).
  Exit 1 names the failing listings.
- **Stale** (`last_reverified` older than 7 days): flagged in place, status
  → `stale`. The operator has 7 more days to re-verify.
- **Delisted** (no re-verification within 14 days, or section 5 triggered):
  status → `delisted`, kept as a tombstone with reason + date for audit.
  Listings are never silently deleted.

## 5. Delisting policy

A listing is delisted (tombstoned, not erased) when any of these is found:

- the endpoint stops answering, or answers 402 with terms that don't match
  the listing (wrong amount, network, asset, or payTo);
- the manifest drifts from the pinned copy without a new listing revision;
- evidence is shown to be fabricated, replayed from another service, or
  otherwise not from a real paid run;
- the service is used for fraud, payola-adjacent placement selling,
  artificial engagement, or any scam pattern;
- the provider requests removal.

Delisting is a public diff: the tombstone records who found what, when, and
the evidence. A public "hall of shame" diff of manifest changes ships with
the verifier output.

## 6. Honesty rules (non-negotiable)

- Testnet is testnet. "USDC on Base" without a qualifier is a delisting
  offense — say **Base Sepolia** or **Base mainnet**, always.
- `settlement_proven: false` until a settled tx hash exists. A facilitator
  `verify` is not a settlement.
- Prices are verified against the live challenge, not the provider's docs.
- Self-evaluations (like this v1.0.0 seed) are labeled as such; the evidence
  is published so anyone can re-run it independently.
- Nothing in this directory is investment advice, a safety guarantee, or an
  endorsement beyond "these checks passed on these dates."

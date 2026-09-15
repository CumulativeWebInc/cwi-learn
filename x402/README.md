# CWI Verified x402 Directory

An index of self-registered listings is a directory of alibis. This directory
lists only x402/agent services whose claims have been **earned** — by evidence
anyone can re-run. Seed: our own real x402 endpoints. Nothing else is
invented; every future listing enters through the earning policy.

## Files

| File | What it is |
|---|---|
| `directory.json` | The directory (v1.0.0): versioned, machine-readable, listings earned via evidence |
| `listing-policy.md` | How a listing is earned (three verdicts), weekly re-verification, delisting policy |
| `reverify.py` | The checker (stdlib only): manifest + evidence reachable, freshness ≤ 7 days, public endpoints still answer 402 |
| `evidence/<service>/first-spin-verdict.json` | Paid-run verdict receipt for the listing (First Spin discipline: confidence labels + cited sources) |
| `evidence/<service>/attestation-receipt.json` | Hash-chained attestation receipt sealing the verdict (Needle Drop receipt discipline) |
| `community-post-draft.md` | **DRAFT ONLY** — proposed contribution to the community x402 Service Directory thread. Do not post without the owner's approval. |

The machine-readable capability manifest for our own API lives at the repo
root per the IETF draft: `.well-known/x402`
(served post-merge at `https://cumulativewebinc.github.io/cwi-learn/.well-known/x402`).

## Verify it yourself

```bash
# post-merge (canonical URLs)
python3 x402/reverify.py x402/directory.json

# pre-merge: map canonical Pages URLs onto this branch's raw URLs
python3 x402/reverify.py x402/directory.json \
  --url-base https://raw.githubusercontent.com/CumulativeWebInc/cwi-learn/needs/receipts-directory
```

Exit 0 = all green. Exit 1 names every failing listing.

## Discovery without a directory: the IETF DNS angle

This directory is a **cache**, not the source of truth — deliberately. It
follows [IETF draft-hawkins-x402-dns-discovery-03](https://datatracker.ietf.org/doc/draft-hawkins-x402-dns-discovery/)
("Discovering x402 Payment Capability via DNS and a Well-Known URI",
Aug 2026), which defines how a domain publishes x402 capability out-of-band
so agents discover it with **no central directory at all**:

1. **`/.well-known/x402` manifest (authoritative).** A host serving x402
   SHOULD serve a JSON capability manifest at that path (we do — see
   `.well-known/x402` in this repo). Draft shape: `x402Version` (required),
   `kind` (`facilitator` | `resource-server` | `both`, required),
   optional `resources[]`, `attestation`, `docs`, `contact`, `updated`.
   Unknown fields are ignored for forward compatibility.
2. **`_x402` DNS TXT record (pointer).** A domain MAY publish a TXT record at
   the underscored node `_x402`, formatted as semicolon-separated pairs:
   `v=x402-1; wk=<manifest URL>; k=<kind>; net=<network>; scheme=<scheme>`.
   A consumer resolves a bare domain to verified x402 capability with **at
   most one DNS query and one HTTPS GET** — the DNS record points at the
   manifest, the manifest is fetched over HTTPS, and curated directories
   become regenerable caches rather than load-bearing infrastructure.

**Our status (honest):** the manifest is published at the well-known URI
(step 1 — done, this repo). The DNS TXT step is **not yet published**: we do
not control DNS for `github.io`, so no `_x402` TXT record can be set there.
When the API gets a public host on a domain we control (e.g.
`cumulativeweb.com`), the `_x402` TXT record above goes live and this
directory's `manifest_url` values move to that host. Until then, this
directory + the manifest are the discovery path, and the DNS step is
documented — not claimed.

## What "verified" means here

A listing is earned with three machine-checkable verdicts — **authorship**
(hash-chained attestation receipt, resolvable without trusting the
directory), **evidence** (a First Spin paid-run verdict receipt: we run it,
we pay, the receipt is the proof), **completeness** (the service's
`/.well-known/x402` manifest fetched and pinned). Full spec:
[`listing-policy.md`](listing-policy.md).

Testnet is always labeled testnet. `settlement_proven: false` until a settled
tx hash exists. A facilitator `verify` is not a settlement.

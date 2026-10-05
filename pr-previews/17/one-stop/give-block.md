# ONE-STOP — GIVE BLOCK (Sync & Licensing department)

Copy-paste ready. EQUIP to read the catalog + grant contract; CONFIGURE to
stage your grant; APPLY to draft the creator-tier grant JSON.

DRAFT MODE: Creator tier ($0) is live and issuable. Indie and Commercial tiers
are staged DRAFT templates — PENDING BLACK'S EXACT-TERMS APPROVAL, not issuable.

## EQUIP

```
ONE-STOP — EQUIPPED (Sync & Licensing department, Agent Deck gear line)
Grant config:  https://cumulativewebinc.github.io/cwi-learn/one-stop/one-stop.json
Schema:        https://cumulativewebinc.github.io/cwi-learn/one-stop/one-stop-schema.json
Fee tiers:     https://cumulativewebinc.github.io/cwi-learn/one-stop/fee-tiers.json
Grant text:    https://cumulativewebinc.github.io/cwi-learn/one-stop/grant-template.md
Card:          https://cumulativewebinc.github.io/cwi-learn/one-stop/item-card.json
Hub:           https://cumulativewebinc.github.io/cwi-learn/syncdeck/ (SyncDeck)

Catalog: 24 That Boy Hi Hat tracks (tbhh-001 … tbhh-024) — Zooted Zone,
Shaka Zulu, Doves & Diamonds, Diabolique, and 20 more. Source of truth is
the catalog_ref block in one-stop.json.

Rights line on every grant:
  ℗ Cumulative Web Inc — 100% master & publishing, pre-cleared

One grant clears master AND publishing — no separate publisher negotiation,
no marketplace, no commission. The artist keeps 100%.

Brand rule: the CWI logo badge ships on every ONE-STOP surface.
```

## CONFIGURE

Decide the grant fields before you draft:

- licensee: your agent or org name + contact
- track: one of tbhh-001 … tbhh-024 (titles in one-stop.json → catalog_ref.tracks)
- use: stream-overlay | vod | short-form | live-intro | podcast | game-mod
- media: twitch | youtube | tiktok | instagram | x | podcast-feed | broadcast | film
- territory: worldwide (or ISO-3166 codes)
- term: months (creator tier fixed at 12)
- fee tier: creator (LIVE) | indie (DRAFT) | commercial (DRAFT)

A grant is valid when it validates against:
https://cumulativewebinc.github.io/cwi-learn/one-stop/one-stop-schema.json
(format: cwi-grant/v1; grant_id matches ^cwi-grant-[a-z0-9-]+$; track catalog_id
matches ^tbhh-\d{3}$; rights_line is the fixed CWI line above.)

## APPLY

Draft a live Creator-tier grant (fill the ALL-CAPS slots):

```json
{
  "grant_format": "cwi-grant/v1",
  "grant_id": "cwi-grant-tbhh-001-YYYYMMDD-###",
  "issuer": "Cumulative Web Inc",
  "licensee": {"name": "LICENSEE-NAME", "contact": "LICENSEE-CONTACT"},
  "track": {"catalog_id": "tbhh-001", "title": "Zooted Zone"},
  "use": "stream-overlay",
  "media": "twitch",
  "territory": "worldwide",
  "term_months": 12,
  "fee_tier": "creator",
  "fee": "0",
  "rights_line": "℗ Cumulative Web Inc — 100% master & publishing, pre-cleared",
  "pre_clearance": "see one-stop.json → pre_clearance (CWI 100% master & publishing, attested 2026-09-15)",
  "countersignature": {"status": "awaiting-licensee", "signature": null, "date": null},
  "draft_mode": false,
  "issued": "YYYY-MM-DD"
}
```

DRAFT-MODE LIMITS (read this):
- Creator tier = the ONLY issuable tier. $0, non-commercial, under-60-second grants.
- Indie and Commercial tiers are DRAFT templates: "PENDING BLACK'S
  EXACT-TERMS APPROVAL — not issuable." Do not issue, sign, or countersign
  them. Do not quote terms for them.
- The grant becomes effective on the LICENSEE's countersignature. Nothing
  is signed in Black's name without his exact approval — standing house rule.

Questions or sync: hp@cumulativeweb.com

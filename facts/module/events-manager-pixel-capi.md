# Fact packet — Events Manager (Pixel + CAPI)

Schema `cwi-fact-packet/v1` · generated 2026-10-03T13:17:46Z · integrity `79c4a95a9adf6c6d`

## Discovery tags

- #marketing-module — role (verified; anatomy node type module)
- #meta — platform (claimed_unverified; Meta ad platform)
- #pixel — tech (claimed_unverified; browser pixel events)
- #capi — tech (claimed_unverified; server-side conversions API)
- #event-match-quality — metric (claimed_unverified; EMQ scoring)
- #tracking — function (claimed_unverified; event ingestion)

## Facts

- **[observed]** Anatomy indexed from 'Digital Anatomy of Four Music-Marketing Machines' research report (2026-10-03); per-fact evidence tiers and sources recorded in attrs.key_facts — _~/workspace/research_notes/music-marketing-machine-anatomy-20261003-1237/report.md_
- **[claimed_unverified]** Events Manager: Pixel + Conversions API event ingestion, custom conversions, Event Match Quality scoring — _https://github.com/boringmarketer/meta-ads-skill/blob/HEAD/reference/tracking.md_
- **[claimed_unverified]** Pixel events (browser): PageView on smart-link landing; custom conversion on Spotify redirect-URL pageview; optional deeper events (pre-save, merch purchase); a Pixel cannot be placed on Spotify itself — _https://www.chartlex.com/blog/marketing/meta-ads-spotify-streams-managed-campaigns-2026_
- **[claimed_unverified]** Conversions API (server): event_name, event_time, event_id (dedupe vs. browser), action_source, user_data with SHA-256 hashed email/phone and raw fbp/fbc/IP/user-agent; Event Match Quality below ~5.0 means the server path contributes little — _https://github.com/boringmarketer/meta-ads-skill/blob/HEAD/reference/tracking.md_
- **[claimed_unverified]** Pixel + CAPI combined yields 15-25% more attributed conversions; CAPI is now effectively required for clean signal post-iOS — _https://www.chartlex.com/blog/marketing/meta-ads-spotify-streams-managed-campaigns-2026_
- **[claimed_unverified]** The CAPI protocol itself is just HTTPS POSTs - anyone can implement it; what cannot be replicated is Meta's matching identity graph on the other end — _report section B8 (synthesis)_

## Instructions

### Search answer

Events Manager (Pixel + CAPI) is a system module of a music-marketing machine.

### Social caption

Events Manager (Pixel + CAPI)  #marketing-module #meta #pixel #capi #event-match-quality #tracking

### Sync pitch

SYNC PITCH — Events Manager (Pixel + CAPI).

---
Canonical: https://cumulativewebinc.github.io/cwi-learn/facts/module/events-manager-pixel-capi.json

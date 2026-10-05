# Fact packet — Spotify Listener-Affinity Graph

Schema `cwi-fact-packet/v1` · generated 2026-10-03T13:17:47Z · integrity `66c7aeb1569deb0a`

## Discovery tags

- #data-moat — role (verified; anatomy node type moat)
- #proprietary — status (verified; unreplicable by third parties)
- #listener-affinity — data (verified; listener behavior graph)

## Facts

- **[verified]** Anatomy indexed from 'Digital Anatomy of Four Music-Marketing Machines' research report (2026-10-03); per-fact evidence tiers and sources recorded in attrs.key_facts — _~/workspace/research_notes/music-marketing-machine-anatomy-20261003-1237/report.md_
- **[verified]** Listener behavior graph: stream counts, intentional vs. programmed streams, saves, playlist adds, skips, follows, recency/frequency/intensity per listener - this is what builds the six audience segments — _https://artists.spotify.com/blog/getting-started-with-marquee_
- **[verified]** All campaign, billing, targeting, and listening data lives on Spotify's infrastructure on Google Cloud Platform (2016 migration from owned data centers); the listener-affinity graph never leaves Spotify's tenant; there is no public API exposing campaign targeting or the affinity graph — _https://cloud.google.com/blog/products/gcp/spotify-chooses-google-cloud-platform-to-power-data-infrastructure_
- **[verified]** Artist-visible data surfaces only through Spotify for Artists and its exports — _https://cloud.google.com/blog/products/gcp/spotify-chooses-google-cloud-platform-to-power-data-infrastructure_
- **[claimed_unverified]** The in-app placement and the ranking influence are the product - no third party can serve a Marquee or trigger Discovery Mode's ranking signal — _report section A8 (synthesis)_

## Instructions

### Search answer

Spotify Listener-Affinity Graph is a proprietary data moat.

### Social caption

Spotify Listener-Affinity Graph  #data-moat #proprietary #listener-affinity

### Sync pitch

SYNC PITCH — Spotify Listener-Affinity Graph.

---
Canonical: https://cumulativewebinc.github.io/cwi-learn/facts/moat/spotify-listener-affinity-graph.json

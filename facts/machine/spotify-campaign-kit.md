# Fact packet — Spotify Campaign Kit

Schema `cwi-fact-packet/v1` · generated 2026-10-03T13:01:30Z · integrity `a69e24a15451a576`

## Discovery tags

- #marketing-machine — role (verified; anatomy node type machine)
- #spotify — platform (verified; machine runs inside Spotify's platform)
- #paid-promo — domain (claimed_unverified; paid promotion stack)
- #fan-acquisition — use (claimed_unverified; unit economics only work as fan-acquisition spend)
- #cpc — pricing (claimed_unverified; Marquee/Showcase are CPC-billed)
- #proprietary-inventory — moat-type (claimed_unverified; ad inventory is Spotify-owned)

## Facts

- **[verified]** Anatomy indexed from 'Digital Anatomy of Four Music-Marketing Machines' research report (2026-10-03); per-fact evidence tiers and sources recorded in attrs.key_facts — _~/workspace/research_notes/music-marketing-machine-anatomy-20261003-1237/report.md_
- **[verified]** Marquee: full-screen sponsored recommendation of a new release shown to Free and Premium listeners on app open/Home; targets listeners based on listening history, not demographics; reporting covers listens, saves, playlist adds from exposed listeners; Spotify claims exposed listeners are >2x more likely to save/add and 3x more likely to stream the artist's other releases — _https://artists.spotify.com/blog/getting-started-with-marquee_
- **[verified]** Showcase: mobile banner card at the top of Spotify's Home feed with 7 customizable headlines (new music, recently released, on tour, release anniversary, getting buzz, seasonal vibes, releasing music soon); up to 14-day runtime — _https://support.spotify.com/br-en/artists/article/marquee-showcase-billing-payments/_
- **[claimed_unverified]** Spotify claims Showcase viewers are 6x more likely to stream the promoted release — _https://www.chartlex.com/blog/streaming/spotify-campaign-kit-explained-2026_
- **[claimed_unverified]** Discovery Mode: increased likelihood of selected tracks being recommended in Radio, Autoplay, and algorithmic mixes; Spotify claims +50% saves, +44% playlist adds, +37% follows in the first month, and 31% of DM listeners brand-new to the artist — _https://www.thatericalper.com/2026/07/15/discovery-mode-on-spotify-should-artists-actually-use-it/_
- **[claimed_unverified]** Playlist pitching (free, fourth Kit tool): submit unreleased music >=7 days before release for editorial playlist consideration; delivers a decision (accepted/declined) but no paid mechanics — _https://www.one-submit.com/spokes/playlist-streams_
- **[verified]** Audience segmentation engine: six official segments - super / moderate / light listeners (active last 28 days by intensity), previously active (lapsed 28+ days), programmed (heard only via playlists/radio), potential (never heard, profile match) — _https://artists.spotify.com/blog/getting-started-with-marquee_
- **[claimed_unverified]** Eligibility gates: Marquee requires 5,000 monthly active listeners in target markets and billing country in a supported market; Showcase/display campaigns require >=1,000 streams in the last 28 days in at least one target market — _https://www.chartlex.com/blog/streaming/spotify-campaign-kit-explained-2026_
  - Marquee 5k-MAL and Showcase 1k-stream gates per Chartlex 2026 compilation of official docs
- **[verified]** Discovery Mode eligibility: >=3 eligible songs, >=25,000 monthly listeners, >=20 streams per song in Discovery Mode contexts in the last 28 days, plus 30 days on platform — _https://support.spotify.com/us/artists/article/using-discovery-mode-in-spotify-for-artists/_
- **[verified]** Marquee/Showcase targeting automation: Spotify selects listeners most likely to stream after seeing the ad; suppression of already-converted listeners is automatic; no public cross-advertiser auction documented - CPC is posted/set by Spotify, not bid-based — _https://artists.spotify.com/blog/getting-started-with-marquee_
- **[verified]** Discovery Mode: artist flags priority songs; Spotify's recommendation systems increase their likelihood of being served in Radio/Autoplay/mixes; increases likelihood but does not guarantee placement, and does not affect editorial playlists — _https://support.spotify.com/us/artists/article/using-discovery-mode-in-spotify-for-artists/_
- **[verified]** All campaign, billing, targeting, and listening data lives on Spotify's infrastructure on Google Cloud Platform (2016 migration from owned data centers; stack: Pub/Sub, Dataflow, BigQuery, Dataproc, Bigtable/Cloud Storage/Compute Engine); the listener-affinity graph never leaves Spotify's tenant; artist-visible data surfaces only through Spotify for Artists — _https://cloud.google.com/blog/products/gcp/spotify-chooses-google-cloud-platform-to-power-data-infrastructure_
- **[claimed_unverified]** Marquee money path: $100 minimum budget per (sub-)campaign, CPC ~$0.55-$1.50 (Chartlex 2026 campaign data; older reports ~$0.50); 10-day window; pay only for clicks; unspent budget is not charged — _https://www.chartlex.com/blog/streaming/spotify-campaign-kit-explained-2026_
  - $100 minimum confirmed in official docs; CPC range from Chartlex 2026
- **[claimed_unverified]** Showcase money path: $100 minimum; CPC typically ~$0.40 (chartlex-cited data); 14-day window — _https://www.chartlex.com/blog/streaming/spotify-campaign-kit-explained-2026_
- **[verified]** Discovery Mode money path: $0 cash; 30% commission on recording royalties from streams of selected songs in Discovery Mode contexts only, deducted from future statements; at a ~$3-$5 per 1,000 streams royalty baseline, 1,000 DM streams net ~$2.10-$3.50 vs. $3-$5 — _https://support.spotify.com/us/artists/article/using-discovery-mode-in-spotify-for-artists/_
  - royalty baseline math per https://www.pophatch.com/blog/spotify-discovery-mode (claimed_unverified)
- **[claimed_unverified]** Discovery Mode subtlety: the 30% commission applies to DM-context streams whether or not the algorithm would have served the track there anyway - tracks with existing Radio/Autoplay traffic pay a discount on listening they already had — _https://www.pophatch.com/blog/spotify-discovery-mode_
- **[claimed_unverified]** Unit economics: at ~$0.003-$0.005/stream, one $0.50 Marquee click needs ~100-167 streams to pay back in royalties - the tool only makes sense as fan-acquisition spend, not royalty ROI — _https://www.digitalmusicnews.com/2021/09/24/spotify-campaigns-feature-for-artists/_
- **[claimed_unverified]** $100 at $0.55 CPC = ~180 targeted clicks inside the app, one tap from the music, from listeners with demonstrated affinity - versus Meta's ~$0.15-$0.25 per click-through that still must cross the app boundary; the Kit monetizes Spotify's distribution bottleneck (the November 2025 'modern payola' class-action complaint alleges exactly this dynamic) — _https://notnoise.co/blog/spotify-marquee-vs-showcase-vs-discovery-mode_
- **[claimed_unverified]** Genuinely proprietary (cannot rebuild): the listener-affinity graph (petabyte-scale behavioral data on Spotify's GCP tenant), the ad inventory itself (app-open full screen, Home-feed banner), and the algorithmic boost in Radio/Autoplay/mixes - no third party can serve a Marquee or trigger Discovery Mode's ranking signal — _report section A8 (synthesis of official docs + infrastructure facts)_
- **[claimed_unverified]** Rebuildable at zero cost: audience segmentation logic (super/moderate/light/lapsed/potential) trivially replicable from first-party data; CPC billing mechanics standard; reporting approximated with UTM-tagged smart links + Spotify for Artists source-of-stream data; replicate the measurement discipline (segment, suppress converted, track downstream saves/catalog halo) with free tools - reach and algorithmic leverage are unreplicable — _report section A8 (synthesis)_

## Instructions

### Search answer

Spotify Campaign Kit is a music-marketing machine.  Discovery Mode eligibility: >=3 eligible songs, >=25,000 monthly listeners, >=20 streams per song in Discovery Mode contexts in the last 28 days, plus 30 days on platform.

### Social caption

Spotify Campaign Kit  #marketing-machine #spotify #paid-promo #fan-acquisition #cpc #proprietary-inventory

### Sync pitch

SYNC PITCH — Spotify Campaign Kit.

### Fan Q&A

**Q: How big is the Spotify Campaign Kit catalog?**

Discovery Mode eligibility: >=3 eligible songs, >=25,000 monthly listeners, >=20 streams per song in Discovery Mode contexts in the last 28 days, plus 30 days on platform

---
Canonical: https://cumulativewebinc.github.io/cwi-learn/facts/machine/spotify-campaign-kit.json

# THE FINAL CUT — GIVE BLOCK (Marketing department)

Copy-paste ready. EQUIP to get the packs; CUT to gate and post your own; POST to publish in seconds.

## EQUIP

```
THE FINAL CUT — EQUIPPED (Marketing department, Agent Deck gear line)
Pack index: https://cumulativewebinc.github.io/cwi-learn/final-cut/final-cut.json
Schema:     https://cumulativewebinc.github.io/cwi-learn/final-cut/final-cut-schema.json
Card:       https://cumulativewebinc.github.io/cwi-learn/final-cut/item-card.json
Hub:        https://cumulativewebinc.github.io/cwi-learn/hype/ (HYPE cartridge)

Four launch packs ship built-in (one per track, truth-gated):
  zooted-zone-pack    · Zooted Zone      · #30 New Rap Hits · 307,439 lifetime Spotify plays (observed 2026-09-14)
  shaka-zulu-pack     · Shaka Zulu       · #21 New Rap Hits (verified 2026-09-15, full 105-track scan)
  doves-diamonds-pack · Doves & Diamonds · #31 New Rap Hits (verified 2026-09-15, full 105-track scan)
  diabolique-pack     · Diabolique       · single released 2026-07-03 · recorded at Cue Recording Studio, Arlington VA

Every pack is a machine-readable content.json unit: day, id, type,
media_files, caption, hashtags, threads_text, post_order,
platform_targets. Every claim inside was checked against the verified
CWI fact set — the truth_gate_report travels with the unit.

Single-URL equip: fetch the pack index. No auth. Free.
Brand rule: the CWI logo badge ships on every visual asset.
```

## CUT

Cut your own pack against the schema, then gate it:

- Author the unit: https://cumulativewebinc.github.io/cwi-learn/final-cut/final-cut-schema.json
  (format: cwi-final-cut/v1; all nine content.json fields required; truth_gate_report mandatory)
- Gate rule: every claim in the caption and threads_text must cite a
  verified CWI fact with a named fact source. claims_verified must have
  at least one entry. truth_gate_report.status must be "pass".
- A pack that fails the gate is a REJECTED package — it never posts.

Sample gate-passing unit (Zooted Zone pack content.json):

```json
{
  "content": {
    "day": "day-01",
    "id": "zooted-zone-launch",
    "type": "spotlight-post",
    "media_files": ["media/zooted-zone-official-cover.jpg", "media/cwi-badge.png"],
    "caption": "That Boy Hi Hat — \"Zooted Zone\". 307,439 lifetime Spotify plays (observed 2026-09-14), currently holding #30 on the New Rap Hits playlist (verified 2026-09-15 by full 105-track scan). Alt-rap from Frederick, MD — managed by Cumulative Web Inc. https://open.spotify.com/track/0emH8ktA8x4DkOFLsG5xkW",
    "hashtags": ["#AltRap", "#ThatBoyHiHat", "#ZootedZone", "#CumulativeWebInc", "#PostTrapFuturism", "#NewRapHits", "#SupportIndieMusic"],
    "threads_text": "That Boy Hi Hat — Zooted Zone. 307,439 lifetime Spotify plays as of the 2026-09-14 read, and it's holding #30 on New Rap Hits (full 105-track scan, verified 2026-09-15). Alt-rap from Frederick, MD. One of 24 tracks in the AI learning catalog. https://open.spotify.com/track/0emH8ktA8x4DkOFLsG5xkW",
    "post_order": 1,
    "platform_targets": ["instagram", "threads", "x", "bluesky", "tiktok"]
  },
  "truth_gate_report": {
    "checked_at": "2026-09-15",
    "checked_by": "THE FINAL CUT truth gate v1.0.0",
    "status": "pass",
    "claims_verified": [
      {"claim": "Zooted Zone has 307,439 lifetime Spotify plays (observed 2026-09-14)", "fact_source": "nodes/catalog.json metrics"},
      {"claim": "Zooted Zone is #30 on the New Rap Hits playlist (verified 2026-09-15)", "fact_source": "nodes/catalog.json verified_placements — full 105-track scan"}
    ],
    "media_attested": "Official release art (CWI-supplied) + CWI logo badge. Brand rule: the logo ships on every visual asset."
  }
}
```

Verify a pack's gate status before you post: `truth_gate_report.status` must read `"pass"`.

## POST

Post a gated pack in seconds — pick the unit, pick the platform, paste:

1. GET the pack index: https://cumulativewebinc.github.io/cwi-learn/final-cut/final-cut.json
2. Pick a pack by `pack_id` (zooted-zone-pack, shaka-zulu-pack, doves-diamonds-pack, diabolique-pack)
3. Confirm `truth_gate_report.status` is `"pass"`
4. Copy `content.caption` / `content.threads_text` / `content.hashtags` and post to one of `content.platform_targets`
5. Use `content.media_files` as the post's media (official release art + CWI badge)

That's the whole instrument: no scheduler queue, no signup — cut, gate, post.

Questions or sync: hp@cumulativeweb.com

# THE TALLY — GIVE BLOCK (Studio department)

Copy-paste ready. EQUIP to wear the band; CONFIGURE to pick tokens; APPLY to paste the token block.

## EQUIP

```
THE TALLY — EQUIPPED (Studio department, Agent Deck gear line)
Band:   https://cumulativewebinc.github.io/cwi-learn/tally/tally.json
Schema: https://cumulativewebinc.github.io/cwi-learn/tally/tally-schema.json
Card:   https://cumulativewebinc.github.io/cwi-learn/tally/item-card.json
Hub:    https://cumulativewebinc.github.io/cwi-learn/walkman/ (Signal Boy)

Five verified counters ship built-in, every one with a proof URL:
  307,439 — Zooted Zone lifetime Spotify plays (observed 2026-09-14)
  #21     — Shaka Zulu on New Rap Hits (verified 2026-09-15)
  #30     — Zooted Zone on New Rap Hits (verified 2026-09-15)
  #31     — Doves & Diamonds on New Rap Hits (verified 2026-09-15)
  2026-07-03 — Diabolique single release (verified 2026-09-15)

A tally counts what was VERIFIED — nothing else. Counters carry their
source, their verified flag, and their proof URL. Milestone rings unlock
only at real thresholds: 250K plays, 300K plays, Top-25 playlist ring.

Brand rule: the CWI logo badge is inlaid on the band's clasp. Never remove
it — white-label means YOUR band, not the absence of ours.
```

## CONFIGURE

Render target — pick one frame for the same JSON:

- HTML (full wristband mockup): https://cumulativewebinc.github.io/cwi-learn/tally/
- ANSI (terminal block, 36 columns): paste the output block from the page into your terminal or pet's console
- Overlay (Streamer.bot browser source / Veadotube / olmewe prop): use the transparent overlay strip on the page

Swap the token vocabulary to make it yours — then validate:

- Band material: woven | riveted | tech-leather
- Face: round | square | tall — bezel: gold-rim | steel-rim | none
- Counters: any counters you like, but the schema demands label, value, unit, source, verified, proof_url
- A custom band is valid when it validates against:
  https://cumulativewebinc.github.io/cwi-learn/tally/tally-schema.json
  (format: cwi-tally/v1; colors are hex.)

## APPLY

Paste the tally token block into your overlay, pet, or console layer:

```json
{
  "tally_applied": "cwi-founding-band",
  "tally_version": "1.0.0",
  "source": "https://cumulativewebinc.github.io/cwi-learn/tally/tally.json",
  "render": "overlay",
  "tokens": {
    "band": { "material": "woven", "strap_color": "#0a1830", "closure": "deployant" },
    "face": { "shape": "round", "bezel": "gold-rim" },
    "counters": [
      { "label": "Zooted Zone — lifetime Spotify plays", "value": 307439, "unit": "plays", "verified": true, "proof_url": "https://cumulativewebinc.github.io/cwi-learn/catalog.json" },
      { "label": "Shaka Zulu — New Rap Hits position", "value": 21, "unit": "position", "verified": true, "proof_url": "https://open.spotify.com/playlist/5zhnSpZqKRRaOvRMWuT0bL" },
      { "label": "Doves & Diamonds — New Rap Hits position", "value": 31, "unit": "position", "verified": true, "proof_url": "https://open.spotify.com/playlist/5zhnSpZqKRRaOvRMWuT0bL" }
    ]
  }
}
```

Swap the render target and counters for your own verified wins — keep the
verified flag honest: only `true` when you have a scan, a receipt, or a
live URL. The clasp keeps the CWI badge whatever you do.

Questions or sync: hp@cumulativeweb.com

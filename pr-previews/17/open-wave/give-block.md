# OPEN WAVE — GIVE BLOCK (Radio & Playlists department)

Copy-paste ready. EQUIP to load the rotation pack; CONFIGURE to pick a daypart slot; SPIN to air a track and log it.

## EQUIP

```
OPEN WAVE — EQUIPPED (Radio & Playlists department, Agent Deck gear line)
Pack:   https://cumulativewebinc.github.io/cwi-learn/open-wave/open-wave.json
Schema: https://cumulativewebinc.github.io/cwi-learn/open-wave/open-wave-schema.json
Spins:  https://cumulativewebinc.github.io/cwi-learn/open-wave/spins.log.schema.json
Card:   https://cumulativewebinc.github.io/cwi-learn/open-wave/item-card.json
Hub:    https://cumulativewebinc.github.io/cwi-learn/dial/ (Dial)

The launch pack is the 24-track That Boy Hi Hat catalog, rotation-ready:
4 daypart slots (morning-drive, midday, afternoon-drive, late-night),
DJ intros + backsells written from verified facts, citations mandatory
on every fact. $0. Opt-in. No submission gatekeeper, no paid-placement
mechanics — the pack IS the submission.

HARD RULE: a pack that sells airplay is not OPEN WAVE.
```

Alternate pack rendering: append `?pack=<id>` to the page URL to render a
different pack from the same directory, e.g.
https://cumulativewebinc.github.io/cwi-learn/open-wave/?pack=your-label-pack.json
(the file must be a same-directory .json validated against the schema).

## CONFIGURE

Pick a slot by daypart, or pull any track directly:

- Browse the four slots: https://cumulativewebinc.github.io/cwi-learn/open-wave/
- Validate your own pack: https://cumulativewebinc.github.io/cwi-learn/open-wave/open-wave-schema.json
  (format: cwi-openwave/v1; pack_id must match ^[a-z0-9-]+$;
  no_paid_placement must be true; every track needs >=1 verified_fact
  with fact + citation + observed. bpm/key/duration/isrc are not
  schema fields — unknown measurements are omitted, never invented.)

Slot quick-pick (launch pack):
- morning-drive  (06:00–10:00 ET) — high energy openers, incl. Zooted Zone
- midday         (10:00–15:00 ET) — steady rotation, incl. Shaka Zulu, Flamerz
- afternoon-drive(15:00–19:00 ET) — peak hours, incl. Doves & Diamonds, Diabolique
- late-night     (19:00–24:00 ET) — deep cuts, the Place I Go to Dream sequence

Explicit policy is daypart-discretion: many tracks are explicit per Spotify
metadata and no clean versions exist. Program accordingly.

## SPIN

Air the track: read its `dj_intro` on the way in, its `dj_backsell` on the
way out. Then log the spin (optional but recommended — transparency is the
product):

```json
{
  "pack_id": "open-wave-cwi-launch-1",
  "ledger": [
    {
      "spin_id": "spin-001",
      "timestamp": "2026-09-15T18:00:00Z",
      "agent_dj": "<your-agent-handle>",
      "track_title": "Zooted Zone",
      "slot_id": "morning-drive",
      "channel": "broadcast",
      "context": "Morning Drive — opening cut. New Rap Hits #30.",
      "dj_intro_used": "That Boy Hi Hat — 'Zooted Zone', the breakout..."
    }
  ],
  "spin_logged": true
}
```

Ledger schema: https://cumulativewebinc.github.io/cwi-learn/open-wave/spins.log.schema.json
(format: cwi-openwave-spins/v1). A ledger entry proves an opt-in spin —
it never implies paid airplay or a guaranteed slot.

Questions, licensing, or radio: hp@cumulativeweb.com

# CWI Freshness Contract — `cwi.freshness/1.0`

Public schema for `freshness.json`, the machine-readable freshness manifest for
Cumulative Web Inc's public agent surfaces (cwi-learn).

## Rule

A field is **FRESH** when observed within the last 48 hours. Older fields are
labeled **STALE** with their last honest observation date.

**Timestamps are never manufactured.** `observed_at` is written only by real
verification events: an analytics pull, a playlist sweep, or a manual
re-verification. The generator (`freshness.js`) cannot create freshness — it
only recomputes labels from the durable record in `freshness-sources.json`.

## Manifest shape

```jsonc
{
  "schema": "cwi.freshness/1.0",
  "freshness_rule": "…human-readable rule…",
  "manifest_checked_at": "2026-09-19T07:49:35Z",  // when labels were last recomputed
  "endpoints": [
    {
      "file": "catalog.json",
      "url": "https://cumulativewebinc.github.io/cwi-learn/catalog.json",
      "live": true,            // liveness probe passed on this run
      "http_status": 200,
      "fields": [
        {
          "path": "metrics.monthly_listeners",   // JSON path in the file
          "label": "Artist monthly listeners (171)",
          "observed_at": "2026-09-14",           // last HONEST observation
          "status": "stale",                     // fresh | stale
          "age_hours": 127.8,
          "refresh": "analytics sweep (Spotify / Viberate / Songstats)",
          "source": "analytics pull 2026-09-14",
          "note": "…"
        },
        {
          "path": "evidence[].observed",
          "label": "Evidence provenance timestamps",
          "volatile": false,                     // historical citations — never relabeled
          "note": "…"
        }
      ]
    }
  ]
}
```

## Field kinds

- **Volatile field** — a current-state claim that decays (stream counts, playlist
  positions, follower numbers). Carries `observed_at`, `status`, `refresh`,
  `source`.
- **Provenance field** (`"volatile": false`) — a historical citation of *when
  evidence was seen*. Never refreshed, never relabeled. Rewriting one would be
  fabrication.

## Refresh loop

1. A verification event happens (sweep, pull, manual check).
2. `freshness-sources.json` gets the new honest `observed_at` (+ source).
3. `node freshness.js [--deploy]` recomputes labels and publishes.
4. A daily cron keeps `manifest_checked_at` honest even when no new
   observations exist — so consumers can distinguish "stale since 9/14, labels
   rechecked 2h ago" from "nobody has looked in weeks."

## Kill rule

If the refresh loop ever becomes unsustainable, the manifest keeps truthful
staleness labels. Freshness is never faked to meet the 48h bar.

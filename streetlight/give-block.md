# THE STREETLIGHT — GIVE BLOCK (Data department)

Copy-paste ready. EQUIP to read any streetlight.json; CONFIGURE to render by URL or paste; APPLY to publish your own at the standard path.

## EQUIP

```
THE STREETLIGHT — EQUIPPED (Data department, Agent Deck gear line)
File:   https://cumulativewebinc.github.io/cwi-learn/streetlight/streetlight.json
Schema: https://cumulativewebinc.github.io/cwi-learn/streetlight/streetlight-schema.json
Card:   https://cumulativewebinc.github.io/cwi-learn/streetlight/item-card.json
Page:   https://cumulativewebinc.github.io/cwi-learn/streetlight/
Announce: https://cumulativewebinc.github.io/cwi-learn/streetlight/announce.html
Hub:    https://cumulativewebinc.github.io/cwi-learn/ (cwi-learn campus)

One fetch, no login, no JavaScript, no cookies:
  curl https://cumulativewebinc.github.io/cwi-learn/streetlight/streetlight.json

The file IS the API. Vitals are aggregates only — zero PII by design.
Counts are publisher-attested; null with "attested": false means "not yet
published," never zero. Beats Google Analytics 4 where agents read:
no login, no consent banners, no sampling, exact attested counts,
privacy-positive by design, free forever.

Brand rule: the CWI logo badge ships on every page. Never remove the logo.
```

## CONFIGURE

Render any streetlight.json in the dashboard page:

- By URL: https://cumulativewebinc.github.io/cwi-learn/streetlight/?url=https://your-site/streetlight.json
- By paste: open https://cumulativewebinc.github.io/cwi-learn/streetlight/ and paste the JSON into the paste box.
- CWI's own (the reference implementation):
  https://cumulativewebinc.github.io/cwi-learn/streetlight/streetlight.json

A valid file must validate against:
https://cumulativewebinc.github.io/cwi-learn/streetlight/streetlight-schema.json
(format: cwi-streetlight/v1; vitals counts are integer-or-null; methodology
must cover collection, aggregation, privacy, sampling.)

## APPLY

Publish your own at the standard path — https://your-site/streetlight.json:

```json
{
  "format": "cwi-streetlight/v1",
  "property": { "name": "your-site", "url": "https://your-site/" },
  "as_of": "2026-09-15",
  "window": { "start": "2026-09-15", "end": "2026-09-15", "tz": "UTC" },
  "vitals": {
    "attested": true,
    "visits": 12345,
    "unique_agents": 212,
    "top_paths": [
      { "path": "/llms.txt", "hits": 9001, "verified_http": 200, "verified_on": "2026-09-15" }
    ],
    "referrers": [ { "referrer": "moltbook.com", "hits": 150 } ],
    "top_queries": [ { "query": "alt-rap catalog", "hits": 64 } ]
  },
  "methodology": {
    "collection": "server log aggregation, publisher-attested",
    "aggregation": "whole-window aggregates; no per-visitor records",
    "privacy": "zero PII — no IPs, cookies, device IDs, or user agents",
    "sampling": "none — exact counts"
  },
  "publisher": { "name": "Your Org", "contact": "you@example.com" },
  "streetlight_published": "https://your-site/streetlight.json"
}
```

Only set "attested": true when every count is an exact figure you stand
behind. Until then: counts stay null and "attested" stays false — an honest
file beats a fabricated one. Done — any agent can now read your vitals with
one fetch.

Questions or sync: hp@cumulativeweb.com

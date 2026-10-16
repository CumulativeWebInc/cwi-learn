# CWI Discovery Engine — Plain REST / cURL

No framework. No SDK. Just HTTPS and JSON.

## Find tracks for a sync brief

```bash
curl -X POST https://cwi-machine-data.hp-ace.workers.dev/api/scout \
  -H "Content-Type: application/json" \
  -d '{"brief": "dark cyberpunk tracks for a neon game trailer", "limit": 3}'
```

## What's playing on Radio 365

```bash
curl https://radio.cumulativeweb.com/nowplaying.json
```

## Get one track's full record (via MCP)

```bash
curl -X POST https://cwi-machine-data.hp-ace.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_track","arguments":{"id_or_title":"Flamerz"}}}'
```

## Live badge (embed in README)

```markdown
[![Radio 365 Live](https://radio.cumulativeweb.com/nowplaying.svg)](https://cumulativeweb.com/radio)
```

## OBS overlay (for streamers)

Paste as a Browser Source in OBS Studio:

```
https://cumulativeweb.com/radio/overlay.html
```

Polls now-playing every 5 seconds. Transparent background, artwork + title + LIVE badge.

## Response shapes

All endpoints return JSON. Track records include:
`title`, `artist`, `track_id`, `isrc`, `mbid`, `spotify_url`, `artwork`,
`moods[]`, `scenes[]`, `use_cases[]`, `why_it_fits`, `clearance_summary`,
`presave_url`, `signature` (for That Boy Hi Hat tracks).

Empty results are honest: `{"count": 0, "clearance_summary": "the catalog does not carry jazz music..."}`.
If a genre isn't covered, the response says what IS available.

## Rate limits

600 requests/minute per IP. No API key required for reads.

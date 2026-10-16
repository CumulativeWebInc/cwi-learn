# Find Licensed Music for Your Agent in One API Call

**Problem:** your agent needs music for a trailer, game, ad, or video — and it needs to be *licensable*, not just streamable. Searching Spotify gives you tracks with no clearance path, no ISRC, and no way to contact the rights holder.

**Solution:** one HTTP POST to the CWI Scout API. Describe the scene in plain language, get back ranked tracks with verified ISRCs, clearance terms, and the best link to license or pre-save.

No API key. No auth. CORS open. Rate limit: 600 requests/minute per IP.

## The call

```bash
curl -X POST "https://cwi-machine-data.hp-ace.workers.dev/api/scout" \
  -H "Content-Type: application/json" \
  -d '{"brief": "dark futuristic anthem for a cyberpunk game trailer", "limit": 3}'
```

```python
import json, urllib.request

req = urllib.request.Request(
    "https://cwi-machine-data.hp-ace.workers.dev/api/scout",
    data=json.dumps({
        "brief": "dark futuristic anthem for a cyberpunk game trailer",
        "limit": 3,
    }).encode(),
    headers={"Content-Type": "application/json"},
)
res = json.load(urllib.request.urlopen(req))
```

Parameters:

| Field   | Required | Notes                                    |
|---------|----------|------------------------------------------|
| `brief` | yes      | Natural language, max 500 characters     |
| `limit` | no       | 1–5, default 3                           |

## The response

Top-level keys (verified 2026-10-16):

```
brief, clearance_summary, count, licensing_disclaimer,
privacy_notice, session_token, spotlight, tracks
```

Each track carries:

```
title, artist, track_id, score, why_it_fits,
isrc, isrc_verified, explicit,
moods[], scenes[], use_cases[],
spotify_url, best_link {url, kind}
```

Real example (abridged):

```json
{
  "brief": "dark futuristic anthem for a cyberpunk game trailer",
  "count": 2,
  "tracks": [
    {
      "title": "Cyberpunk 2027",
      "artist": "That Boy Hi Hat",
      "track_id": "that-boy-hi-hat-cyberpunk-2027",
      "isrc": "QTA2X2675077",
      "isrc_verified": true,
      "explicit": false,
      "moods": ["dark", "cinematic", "futuristic", "nocturnal", "dystopian"],
      "scenes": ["neon city", "night drive"],
      "use_cases": ["game trailer", "film"],
      "why_it_fits": "matches dark, futuristic, cyberpunk",
      "spotify_url": null,
      "best_link": {
        "url": "https://distrokid.com/hyperfollow/thatboyhihat/cyberpunk-2027",
        "kind": "presave"
      }
    }
  ],
  "clearance_summary": "Cumulative Web Inc controls both master and publishing (50/50 with artists). One signature clears. PRO: BMI.",
  "licensing_disclaimer": "A match is not a license. Contact hp@cumulativeweb.com to clear any track before use.",
  "session_token": "9f3a…"
}
```

### Field notes for agent builders

- **`best_link.kind`** is one of `presave`, `stream`, `spotify`. Prefer `presave` for unreleased tracks, `stream`/`spotify` for released ones. This is the link your agent should surface to the user — never invent a store URL.
- **`isrc_verified: true`** means the ISRC was verified against the label's catalog, not guessed. Quote it in cue sheets.
- **`clearance_summary`** is the rights posture in one paragraph: single-signature clearance, BMI, 50/50 splits. Your agent can relay this to a supervisor, but the `licensing_disclaimer` always applies — a match is not a license.
- **`spotlight`** is the label's current featured release, returned separately from rankings. It never leaks into the ranked results, so your agent's ranking stays honest.
- **Out-of-scope briefs** (genres the catalog doesn't carry, e.g. jazz, classical) return `count: 0` with an honest "the catalog does not carry X music" message in `clearance_summary`. Handle the empty case; don't retry with reworded prompts hoping for a different answer.

## Full Python example: brief → shortlist → cue sheet

```python
import json, urllib.request

SCOUT = "https://cwi-machine-data.hp-ace.workers.dev/api/scout"

def scout(brief, limit=3):
    req = urllib.request.Request(
        SCOUT,
        data=json.dumps({"brief": brief, "limit": limit}).encode(),
        headers={"Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req, timeout=20))

def cue_sheet(brief):
    res = scout(brief)
    if res["count"] == 0:
        return f"No match: {res['clearance_summary']}"
    lines = [f"CUE SHEET — brief: {brief!r}", ""]
    for t in res["tracks"]:
        lines += [
            f"- {t['title']} — {t['artist']}",
            f"  ISRC: {t['isrc']} (verified: {t['isrc_verified']})",
            f"  Link: {t['best_link']['url']} ({t['best_link']['kind']})",
            f"  Why: {t['why_it_fits']}",
        ]
    lines += ["", res["clearance_summary"], res["licensing_disclaimer"]]
    return "\n".join(lines)

print(cue_sheet("dark futuristic anthem for a cyberpunk game trailer"))
```

## What this doesn't do

- It doesn't grant licenses. Every use still clears through hp@cumulativeweb.com.
- It doesn't cover the whole music universe — 27 sync-ready tracks in the catalog as of 2026-10-16, across alternative rap, post-trap, trap, afrobeats, rap-rock, cyberpunk, and dark luxury.
- Brief text is logged with a hashed session token (no raw IPs) for 90 days to improve matching. Send `{"action": "delete_my_data", "session_token": "<token>"}` to `POST /api/scout/feedback` to erase a session.

## Related

- [Add CWI music tools to your LangChain agent](./langchain-music-tools.md)
- [Poll live radio state from your agent](./live-radio-for-agents.md)
- Framework integrations: https://cumulativewebinc.github.io/cwi-learn/framework-integrations/
- Full API briefing for agents: https://cwi-machine-data.hp-ace.workers.dev/llms-full.txt

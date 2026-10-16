# Add CWI Music Tools to Your LangChain Agent

Give your LangChain agent four working music tools in under a minute: sync-brief matching, full track records, artist profiles, and live radio state. Zero auth, zero API keys.

## Install

Single file, no package. Download it next to your agent code:

```bash
curl -O https://cumulativewebinc.github.io/cwi-learn/framework-integrations/langchain/cwi_langchain.py
```

Source: https://github.com/CumulativeWebInc/cwi-learn/tree/main/framework-integrations/langchain

## The four functions

```python
from cwi_langchain import (
    find_tracks_for_brief,  # brief (str), limit (int=3) -> ranked tracks + clearance
    get_track,              # id_or_title (str) -> full record: ISRC, MBID, URLs, artwork
    get_artist,              # name (str) -> artist profile + full track list
    radio_now_playing,       # -> what's live on Cumulative Radio 365 right now
)
```

Each returns a plain dict. Every function hits a live endpoint:

| Function                | Endpoint                                                              |
|-------------------------|-----------------------------------------------------------------------|
| `find_tracks_for_brief` | `POST https://cwi-machine-data.hp-ace.workers.dev/api/scout`          |
| `get_track`             | `POST https://cwi-machine-data.hp-ace.workers.dev/mcp` (tools/call)   |
| `get_artist`            | `POST https://cwi-machine-data.hp-ace.workers.dev/mcp` (tools/call)   |
| `radio_now_playing`     | `GET https://radio.cumulativeweb.com/nowplaying.json`                 |

## Quick test

```python
from cwi_langchain import find_tracks_for_brief, radio_now_playing

res = find_tracks_for_brief("dark tracks for a cyberpunk game trailer", limit=2)
for t in res["tracks"]:
    print(t["title"], "—", t["artist"], "|", t["best_link"]["url"])

print(radio_now_playing()["title"], "by", radio_now_playing()["artist"])
```

Expected output (live data, will vary with the radio schedule):

```
Cyberpunk 2027 — That Boy Hi Hat | https://distrokid.com/hyperfollow/thatboyhihat/cyberpunk-2027
Phantasm — That Boy Hi Hat | https://open.spotify.com/...
Shaka Zulu by That Boy Hi Hat
```

## Complete agent example

A supervisor-music agent: takes a scene description, finds licensable tracks, and reports the clearance path.

```python
from langchain.agents import create_agent
from cwi_langchain import cwi_tools

# cwi_tools() returns LangChain @tool wrappers when langchain-core
# is installed, otherwise plain dicts you can adapt to any framework.
tools = cwi_tools()

agent = create_agent(
    model="gpt-4o",
    tools=tools,
    system_prompt=(
        "You are a music supervisor's assistant. When given a scene, "
        "call find_tracks_for_brief with a natural-language brief. "
        "Report each match with title, artist, ISRC, why it fits, and "
        "the best_link URL. Always include the licensing disclaimer: "
        "a match is not a license; clearance goes through hp@cumulativeweb.com. "
        "Never invent track URLs, ISRCs, or artist names."
    ),
)

result = agent.invoke({
    "messages": [{"role": "user",
                  "content": "I need a dark futuristic track for a neon-drenched game trailer."}]
})
print(result["messages"][-1].content)
```

### Without LangChain

`cwi_tools()` degrades gracefully: if `langchain-core` isn't installed it returns plain dicts describing each tool (name, description, parameters, endpoint). Wire those into CrewAI, AutoGen, or raw function-calling loops — the underlying functions are framework-free.

## What each tool returns

**`find_tracks_for_brief(brief, limit=3)`** — see [Find licensed music for your agent in one API call](./find-music-for-agents.md) for the full response shape. Key fields per track: `title`, `artist`, `isrc`, `isrc_verified`, `best_link {url, kind}`, `why_it_fits`, `moods`, `scenes`, `use_cases`.

**`get_track(id_or_title)`** — the full catalog record: title, artist, ISRC, MusicBrainz IDs (`mbid`, `artist_mbid`), Spotify URL, Apple Music URL, presave URL, UPC, artwork URL, genres, moods, and the signature block. Pass a title ("Flamerz") or a track ID ("that-boy-hi-hat-flamerz").

**`get_artist(name)`** — artist profile plus their full track list with per-track IDs you can feed back into `get_track`.

**`radio_now_playing()`** — live radio state: `station`, `artist`, `title`, `artwork`, `slot_index`, `position_seconds`, `track_ends_at`, `stream_url`, `status`. See [Poll live radio state from your agent](./live-radio-for-agents.md).

## Notes

- Reads need no authentication. Write tools on the MCP server (submit briefs, RSVPs) are rate-limited per requester.
- The MCP endpoint speaks JSON-RPC 2.0 at `/mcp`. Tool responses nest the payload at `result.content[0].text` as a JSON string — parse twice. The wrapper handles this for you.
- Catalog: 27 sync-ready tracks as of 2026-10-16. Out-of-scope briefs return an honest empty result, not hallucinations.

## Related

- [Find licensed music for your agent in one API call](./find-music-for-agents.md)
- [Poll live radio state from your agent](./live-radio-for-agents.md)
- Vercel AI SDK version: https://cumulativewebinc.github.io/cwi-learn/framework-integrations/vercel-ai-sdk/
- Plain cURL version: https://cumulativewebinc.github.io/cwi-learn/framework-integrations/rest-curl/

# cwi-langchain

LangChain tool wrappers for the CWI Discovery Engine — music catalog search, sync-brief matching, and radio now-playing, shaped for AI agents.

## Install

```bash
pip install langchain-core requests
```

## Usage

```python
from cwi_langchain import find_tracks_for_brief, get_track, radio_now_playing

# One call: natural-language sync brief → ranked tracks with clearance
tracks = find_tracks_for_brief("dark cyberpunk tracks for a neon game trailer")
for t in tracks["tracks"]:
    print(t["title"], "-", t["artist"], "| ISRC:", t["isrc"])

# One track's full record
track = get_track("Flamerz")

# What's live on Radio 365 right now
now = radio_now_playing()
print(f"Now playing: {now['artist']} - {now['title']}")
```

## As LangChain Tools

```python
from cwi_langchain import cwi_tools

tools = cwi_tools()  # [find_tracks_for_brief, get_track, get_artist, radio_now_playing]
# Pass to any LangChain agent:
# agent = create_react_agent(llm, tools)
```

## Endpoints

All calls go to `https://cwi-machine-data.hp-ace.workers.dev` — zero auth, CORS open, predictable JSON.

- `find_tracks_for_brief` → POST `/api/scout` `{"brief": "...", "limit": 3}`
- `get_track` → POST `/mcp` `{"method": "tools/call", "params": {"name": "get_track", ...}}`
- `radio_now_playing` → GET `https://radio.cumulativeweb.com/nowplaying.json`

## License

Data responses carry CWI licensing headers. Commercial AI training requires a license — contact hp@cumulativeweb.com.

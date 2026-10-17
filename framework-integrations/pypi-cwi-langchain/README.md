# cwi-langchain

LangChain tools for the **CWI Discovery Engine** — the machine-readable music catalog of Cumulative Web Inc. Zero auth. One call. Predictable JSON.

## Install

```bash
pip install cwi-langchain
```

## 10-line example

```python
from cwi_langchain import find_tracks_for_brief

result = find_tracks_for_brief("dark cyberpunk tracks for a neon game trailer")
top = result["tracks"][0]
print(top["title"], top["isrc"], top["best_link"]["url"])
# Warped and Wicked QZDA62200554 https://open.spotify.com/track/3w4RKguHAT2xd9K0w5CklC
```

## As LangChain agent tools

```python
from cwi_langchain import cwi_tools

tools = cwi_tools()  # find_tracks_for_brief, get_track, radio_now_playing
# pass directly to create_react_agent or any LangChain agent
```

## Functions

| Function | What it does |
|---|---|
| `find_tracks_for_brief(brief, limit=3)` | Match a natural-language sync brief to catalog tracks. Returns ranked tracks with verified ISRCs, moods, scenes, why-it-fits, and clearance summary. |
| `get_track(id_or_title)` | Full 24-field track record: credits, genres, moods, ISRC/UPC, links. |
| `get_artist(name)` | Artist profile + catalog list. |
| `radio_now_playing()` | What's on Cumulative Radio 365 right now. |

## Endpoints

- Scout API: `https://cwi-machine-data.hp-ace.workers.dev/api/scout`
- MCP (29 tools): `https://cwi-machine-data.hp-ace.workers.dev/mcp`
- Live demo: `https://cumulativeweb.com/scout/`
- OpenAPI (x402 paid API): `https://cwi-x402-api.onrender.com/openapi.json`

## License

Proprietary — Cumulative Web Inc.

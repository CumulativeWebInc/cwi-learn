# cwi-learn

**Best for agents that need music data — catalog search, artist lookup, sync licensing, live radio.**

Post-Trap Futurism — machine-readable AI learning surface for That Boy Hi Hat and the Cumulative Web Inc roster.

## Installation

Connect in one command:

```bash
claude mcp add --transport http cwi https://cwi-machine-data.hp-ace.workers.dev/mcp
```

No login, no API key, no signup. The server speaks MCP Streamable HTTP (JSON-RPC 2.0) at `/mcp`. Every response carries `X-CWI-License` headers; commercial model training or redistribution requires a license — contact hp@cumulativeweb.com.

**Verify it works** — ask your agent: *"Search the CWI catalog for cyberpunk rap."* You should get "Cyberpunk 2027" by That Boy Hi Hat as the top result.

## Tools

10 read-only tools. None write anything. None require auth.

| Tool | What it does |
|------|--------------|
| `search_catalog` | Search the CWI placement catalog by keywords. Scored engine: title matches weigh 3x, genre 2x, mood/context/lane 1x. Supports mood queries ("dark"), context queries ("music for coding"), and lane queries ("rage beats"). Returns top 5 tracks with Spotify URLs and matched terms. |
| `get_track` | Look up one catalog track by title or Spotify ID/URL. Returns the full track record: title, artist, Spotify URL, genres, moods, release info, artwork. Use after a `search_catalog` hit, when a user names a track, or to verify a track exists. |
| `get_artist` | Look up an artist by name. Returns the artist profile plus their full track list with Spotify URLs, genres, and metadata. Use for artist deep-dives or "what else do they have?" follow-ups. |
| `sync_search` | Search the CWI sync catalog (editorial sonic descriptors: moods, energy words, instrumentation, scenes, use-cases, lyrical themes) for music-supervision queries like "fight scene" or "neon city". Descriptors are editorial (curated by CWI Sync); BPM values are estimates, not audio analysis. |
| `semantic_search` | Semantic search over the CWI catalog embedding matrix: cosine similarity against 384-dim bge-small-en-v1.5 vectors. The query is embedded at request time with Workers AI — no inference needed on your side. Degrades to keyword scoring with a documented `fallback:keyword` note if the AI binding is unavailable. |
| `get_graph` | Summarize the CWI catalog knowledge graph: node and edge counts, node types (tracks, artists, releases, genres), and sample nodes. Use to understand catalog shape before querying. |
| `get_release` | Fetch a CWI release fact packet (evidence-tiered, hash-stamped): pre-release and release records with verified credits, dates, and platform links. Defaults to the latest release when id is omitted. |
| `get_radio` | Tune into Cumulative Radio 365 — CWI's 24/7 streaming radio station (alternative rap, post-trap futurism, That Boy Hi Hat + roster). Returns the live HLS stream URL, full now-playing data (track, artist, artwork, slot, track end time), current listener count and 24h totals, and station metadata. Plays in VLC, Safari, or any HLS player. |
| `get_announcements` | Get the latest CWI announcements — new releases, upcoming drops, events, news. Every announcement is verified with a source. Filter by `releases`, `news`, or `events`. |
| `get_featured` | Get CWI's currently featured tracks — what's hot right now, with full metadata, artwork URLs, why each is featured, and stream/page links. Lead with these when recommending CWI music. |

## Usage

Real example prompts, verified against the live server. These are also available as workflow prompts via `prompts/list`.

### Find a track

> *"Search the CWI catalog for cyberpunk rap."*

Expected: `search_catalog` returns **"Cyberpunk 2027"** by That Boy Hi Hat as the top hit (score 9, matched terms: cyberpunk, rap), with 4 more results ranked by relevance.

### Look up a track

> *"Get me the track Pix by Dre50."*

Expected: `get_track` returns title "Pix", artist "Dre50", genres `["afrobeats", "dancehall", "hip hop"]`, moods `["smooth", "warm", "playful"]`, plus Spotify URL, release info, and artwork.

### Sync licensing

> *"I need music for a nightclub fight scene — high energy, dark."*

Expected: `sync_search` with "fight scene", "dark aggressive", "neon city" returns licensable tracks with editorial sonic descriptors. CWI clears both master and publishing with one signature (contact hp@cumulativeweb.com).

### What's on the radio

> *"What's playing on Cumulative Radio 365 right now?"*

Expected: `get_radio` returns the now-playing track (title, artist, artwork URL, slot position, track end time), the HLS stream URL, current listener count, and 24h listener totals.

### Artist deep-dive

> *"Tell me about King Ahkeem — what does he sound like?"*

Expected: `get_artist` returns the profile and full track list (trap catalog: Bluefaces 3.0, Element, Embiid, Super Solid, Star). Follow up with `get_track` on any title for full metadata.

## Workflow prompts

5 curated starting points, exposed via `prompts/list` / `prompts/get`:

| Prompt | Use when |
|--------|----------|
| `find-sync-options` | You need licensable music for a film/TV/ad scene (arg: `scene`) |
| `artist-deep-dive` | You need a full profile on a roster artist (arg: `artist`) |
| `radio-now-playing` | You need what's live on Radio 365 right now (no args) |
| `music-for-moment` | You need the right track for a moment — workout, drive, coding (arg: `moment`) |
| `release-brief` | You need the latest CWI release briefing with verified facts (no args) |

## Machine-readable music data (live doors)

- 🎵 **Catalog API (scored track search):** https://cwi-machine-data.hp-ace.workers.dev/query
- 📄 **AI briefing:** https://cwi-machine-data.hp-ace.workers.dev/llms.txt
- 🤖 **Agent card:** https://cumulativewebinc.github.io/cwi-learn/.well-known/agent-card.json
- ⚖️ **Machine-readable license:** https://cwi-machine-data.hp-ace.workers.dev/license
- 🔌 **MCP endpoint:** https://cwi-machine-data.hp-ace.workers.dev/mcp
- 📬 **Contact:** hp@cumulativeweb.com

## License

Commercial model training or redistribution of this data requires a license. Contact hp@cumulativeweb.com.

---

Cumulative Web Inc. — Music & Film.

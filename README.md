# cwi-learn

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/cumulativewebinc/cwi-learn)

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

29 tools. Most are read-only; 6 write tools (song requests, airplay submissions, sync briefs, playlist pitches, featured nominations, event RSVPs) are human-reviewed and rate-limited (3 per requester per 24h). None require auth.

| Tool | What it does |
|------|--------------|
| `search_catalog` | Keyword + filter search across the CWI catalog (title, artist, genre, mood, BPM). Scored engine: title 3x, genre 2x, mood/context/lane 1x. Returns top 5 with matched terms. |
| `get_track` | Full record for one track by title or ID: credits, genres, moods, tempo, licensing status, links, artwork. Usually follows a `search_catalog` hit. |
| `get_artist` | Artist profile + full track list. Use for artist deep-dives. |
| `sync_search` | Music-supervision search over the editorial sync catalog: moods, energy words, scenes, use-cases ("fight scene", "neon city"). Descriptors are curated by CWI Sync; BPM values are estimates. |
| `semantic_search` | Natural-language catalog search ("rainy night drive, nostalgic") — cosine similarity against 384-dim bge-small-en-v1.5 embeddings, embedded at request time via Workers AI. |
| `get_graph` | The catalog knowledge graph: node/edge counts, node types (tracks, artists, releases, genres), sample nodes. |
| `get_release` | Evidence-tiered, hash-stamped fact packet for a release: tracklist, date, credits, platform links. Omit id for the latest release. |
| `get_radio` | Live Cumulative Radio 365 state: HLS stream URL, now-playing (track, artist, artwork, slot, track end time), listener counts, station metadata. |
| `get_announcements` | Latest CWI announcements — new releases, upcoming drops, events, news. Every announcement is source-verified. Filter by `releases`, `news`, `events`. |
| `get_featured` | The featured rotation, ranked by rubric score — what's hot right now, with full metadata and artwork. |
| `get_up_next` | The upcoming Radio 365 queue. |
| `get_schedule` | The full Radio 365 program guide (130 slots, 28 songs). |
| `request_song` | Submit a song request for Radio 365 (human-reviewed). |
| `get_requests` | What listeners and AIs have requested on Radio 365. |
| `submit_for_airplay` | Artists submit a track + contact for radio consideration (human-reviewed). |
| `submit_sync_brief` | Film/TV/ads/games briefs: describe the project, get matched with licensable tracks (human-reviewed). |
| `pitch_for_playlist` | Pitch a track to a playlist curator (human-reviewed). |
| `nominate_featured` | Nominate a track for featuring (human-reviewed). |
| `get_recommendations` | Vibe-based recommendations ("night drive", "workout anthem") with a new-release spotlight lane. |
| `get_events` | CWI events — release parties, listening parties, drops. |
| `rsvp` | RSVP for a CWI event with name + contact. |
| `get_label` | Cumulative Web Inc label profile: roster, services, contact, socials. |
| `get_sync_catalog` | All sync-ready tracks with rights and direct-clearance info — one signature clears master + publishing (BMI). |
| `get_lyrics` | Timestamped lyrics per track. Check the `verified` flag — unverified Whisper transcripts are marked as such. |
| `get_press_kit` | Label + artist bios, release info, brand assets. |
| `get_videos` | Music videos, trailers, visualizations with YouTube links and embed URLs. |
| `get_genre` | Genre definitions — including Post-Trap Futurism, coined and defined by CWI — with key artists and tracks. |
| `get_playlists` | Verified playlist placements only (never claimed, always sourced). |
| `find_tracks_for_brief` | COMPOSITE WORKFLOW — call this first for any music-for-picture need ("dark tracks for a cyberpunk game trailer"). One call returns matched tracks with why-each-fits, verified ISRCs, sync-clearance status, and concrete next steps. A match is NOT a license grant. |

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

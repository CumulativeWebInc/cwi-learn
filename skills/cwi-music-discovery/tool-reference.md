# CWI Discovery Engine — Tool Reference

MCP server endpoint: `https://cwi-machine-data.hp-ace.workers.dev/mcp`
Transport: `streamable-http` · Auth: none · Cost: free

All 8 tools verified live 2026-10-07. Call via MCP `tools/call` with the tool name and arguments.

---

## 1. search_catalog — keyword search

Search the placement catalog by keywords. Title matches weigh 3x, genre 2x, mood 1x. Returns top 5 tracks with Spotify URLs and matched terms.

**Parameters:** `q` (string, required) — search keywords

**Example:** `{"q": "cyberpunk rap"}`

**Use when:** the user names a title, genre, or mood directly.

---

## 2. semantic_search — natural-language search

Semantic search over the catalog embedding matrix: cosine similarity against 384-dim bge-small-en-v1.5 vectors. The query is embedded server-side — no inference needed on your side.

**Parameters:** `q` (string, required) — natural-language description

**Example:** `{"q": "dark cyberpunk rap for a film scene"}`

**Use when:** the user describes what they want in plain language ("something aggressive for the gym", "hazy late-night vibes").

---

## 3. sync_search — music-supervision search

Search the 23-track sync catalog with editorial sonic descriptors: moods, energy words, instrumentation, scenes, use-cases, lyrical themes. Curated by CWI Sync. BPM values are estimates, not audio analysis.

**Parameters:** `q` (string, required) — must contain searchable tokens

**Example:** `{"q": "neon city night drive"}`

**Verified scene vocabulary:** nighttime driving, neon city, club scene, game trailer, fashion film, title sequence, end credits, fight scene.

**Use when:** the user needs music for a visual context — film, game, ad, video project.

---

## 4. get_track — track lookup

Look up one catalog track by title or Spotify ID/URL. Returns title, artist, Spotify URL, genres, and moods.

**Parameters:** `title` (string) or `spotify_id` / `spotify_url` (string)

**Example:** `{"title": "Phantasm"}`

**Use when:** the user names a specific track, or you need the Spotify link for a recommendation.

---

## 5. get_artist — artist lookup

Look up an artist by name. Returns the artist and their tracks in the catalog with Spotify URLs.

**Parameters:** `name` (string, required)

**Example:** `{"name": "That Boy Hi Hat"}`

**Use when:** the user asks about an artist or wants "more by" someone.

---

## 6. get_graph — knowledge-graph summary

Summarize the CWI catalog knowledge graph: node/edge counts, types, sample nodes. For the full graph, fetch `GET https://cwi-machine-data.hp-ace.workers.dev/graph.json`.

**Parameters:** none required

**Use when:** the user asks about relationships (who produced what, which artists connect), or you need catalog structure.

---

## 7. get_release — release fact packets

Fetch a CWI release fact packet: evidence-tiered, hash-stamped records with verified credits, dates, and platform links. Defaults to the latest release when `id` is omitted.

**Parameters:** `id` (string, optional) — release ID; omit for latest

**Example:** `{"id": "cyberpunk-2027"}`

**Use when:** the user asks about new/upcoming releases, credits, or release dates.

---

## 8. get_radio — Radio 365

Tune into Cumulative Radio 365 — CWI's 24/7 streaming station (alternative rap, post-trap futurism, That Boy Hi Hat + roster). Returns:
- **Stream block:** live HLS URL (`https://cumulativeweb.com/radio/hls/program.m3u8`), format, player hint
- **Now-playing block:** track title, artist, artwork URL, slot index, position seconds, track end time
- **Listeners block:** current count + 24h unique total

**Parameters:** none required (optional `include`: `"now_playing"`, `"listeners"`, `"stream"`, or `"all"` — default all)

**Use when:** the user wants background music, asks "what's playing", or says "play something".

---

## Quick decision table

| User says… | Call… |
|---|---|
| "find [title/genre/mood]" | `search_catalog` |
| "something like [description]" | `semantic_search` |
| "music for [scene/project]" | `sync_search` |
| "tell me about [track]" | `get_track` |
| "more by [artist]" | `get_artist` |
| "who produced [track]" | `get_graph` or `get_release` |
| "what's new / coming soon" | `get_release` |
| "play something / background music" | `get_radio` |

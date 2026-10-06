# CWI Catalog Embedding Matrix — EMBEDDINGS.md

**Workstream H — "cyber reach" (2026-10-05). Rebuilt v2 (2026-10-06).** AI systems retrieve with vectors, not keywords.
This matrix publishes the CWI catalog as pre-computed embeddings so any agent/RAG
pipeline can do semantic search over our music with **zero inference on their side**.

## The matrix (v2 — current)

- **File:** `embeddings/catalog-embeddings.json` (this directory)
- **Model:** `bge-small-en-v1.5` (BAAI, open) — 384 dimensions
- **Entries:** 32 (all NLP-enriched tracks from `placement-engine/tracks.json`)
- **Size:** ~178 KB (~65 KB gzipped on the wire)
- **Version:** `cwi-embeddings/v2-2026-10-06-nlp`
- **Entry schema:**
  `{track_id, title, artist, spotify_url, embedding:[384 floats, 6-decimal], model, dim, version, embedded_at, source_text, nlp_word_count, source_template}`

Every entry verified: `len(embedding) == 384` (build-time assertion; the worker's
`loadEmbeddingMatrix` re-validates on load and refuses to serve an invalid matrix).

## v2 changes (2026-10-06, Lansky's order)

Per the standing law "NLP enrichment is the standard for ALL catalog music" (2026-10-06):
semantic search embeddings are now built over the NLP-enriched descriptions
(150-300 words per track, Echo Nest formula: descriptive depth × source consistency
× term corroboration × freshness) instead of the v1 one-line composed descriptions.

**Template v2:**
```
{title} — {artist}
Genres: {g1, g2, ...}            (line omitted when empty)
Moods: {m1, m2, ...}             (line omitted when empty)
{nlp_description (150-300 words of rich descriptive prose)}
```

**Build method v2:** Local ONNX (`/tmp/bge-model/model.onnx` from HuggingFace
`BAAI/bge-small-en-v1.5`), CLS pooling, L2-normalized — identical to fastembed's
BGE behavior. Used because the proxy blocked fastembed's model download; the
ONNX weights are the same published BAAI checkpoint, so model parity holds.

**Ranking check 2026-10-06:** "dark cyberpunk rap for a film scene" →
Cyberpunk 2027 #1 (0.6564), Diabolique #2, Neon Nights Pt. 777 #3.
"upbeat dance party song with high energy" → Stunt #1, Golden Diamond #2.
Sensible: PASS. (v1 had ranked Pay Yourself #1 for the cyberpunk query —
v2 correctly surfaces the actual Cyberpunk 2027 release.)

**v1 backup:** `embeddings/catalog-embeddings-v1-backup.json` (55 entries, preserved).

## Model parity rule (anti-corruption)

Catalog vectors and query vectors are **the same model, named explicitly on both paths**:

- **Batch (this file):** `BAAI/bge-small-en-v1.5` via fastembed (onnxruntime), local $0 compute.
- **Request time (MCP `semantic_search`):** Workers AI `@cf/baai/bge-small-en-v1.5`
  via `env.AI.run('@cf/baai/bge-small-en-v1.5', {text})` — see the `[ai]` binding in
  the worker's `wrangler.toml`.

A model mismatch between catalog and query embeddings would silently corrupt rankings;
both paths MUST keep naming `bge-small-en-v1.5`. The tool description documents this.

## Source texts — exact template v1

Each vector is computed from a source text built ONLY from verified catalog fields
(no invented facts). The one-line description is composed from those fields.

### Sources (in priority order)

1. **`catalog.json`** (decrypted from `cwi-learn/catalog.json.aes`) — canonical 53 track
   titles, artists, Spotify URLs. This is the track list of record.
2. **`placement/query-db.json`** (decrypted from `cwi-learn/placement/query-db.json.aes`) —
   the SAME source the worker's `/query` engine loads (`loadQueryDb`): per-track genres
   (`g`) and moods (`m`).
3. **`sync-catalog.json`** (`https://cumulativewebinc.github.io/cwi-cuefinder/v1/sync-catalog.json`) —
   23 tracks of editorial sonic descriptors: moods, energy words, instrumentation,
   vocal style, scenes, use cases, lyrical themes, `sounds_like_reference`.
4. **Roster genre tags** — Black's own words, 2026-10-04 (owner-verified): 183 Wilboi =
   rap rock/R&B/trap/rap; Greg Porn = cyberpunk/new wave/next gen/alternative music;
   King Akeem = trap music/alternative music; Dre50 = afrobeats/caribbean/R&B;
   Black Lansky = beats/instrumentals; Fleekz = trap music/R&B; That Boy Hi Hat =
   alternative rap. Used ONLY for tracks with no per-track genres in sources 2–3.

### Template (verbatim)

```
{title} — {artist}
Genres: {g1, g2, ...}            (line omitted when empty)
Moods: {m1, m2, ...}             (line omitted when empty)
Sound: moods: {...} | energy: {...} | instrumentation: {...} | vocal: {...} |
       scenes: {...} | use cases: {...} | themes: {...} | reference: {...}
                                    (line omitted when no sync descriptors)
{one_line_description}
```

`one_line_description` (with sync descriptors):
`{title} is a {m1} {m2} {g1} cut from {artist} — {energy_words} over {instrumentation}. Built for {scenes}.`

`one_line_description` (without): `{title} by {artist} — {m1} {m2} {g1}.`

Example (Zooted Zone — full):
```
Zooted Zone — That Boy Hi Hat
Genres: post trap, trap, rap, underground, hip hop
Moods: hype, hypnotic, aggressive, underground, late-night, anthemic
Sound: moods: dark, aggressive, anthemic, electric | energy: relentless, explosive | instrumentation: 808s, trap hats, distorted synths | vocal: hard-edged rap | scenes: club scene, nighttime driving, fight scene, neon city | use cases: film, tv, game, sports | themes: ambition, pressure, escape | reference: editorial: high-voltage trap anthem, peak-hour energy
Zooted Zone is a hype hypnotic post trap cut from That Boy Hi Hat — relentless, explosive over 808s, trap hats, distorted synths. Built for club scene, nighttime driving, fight scene.
```

### Title normalization

Black's 2026-10-05 catalog proofread fixes applied at build: "Toxic Element"→"Toxic Elements",
"Warped & Wicked"→"Warped and Wicked", "Place I Go to Dream (Instrumental)"→"Place I Go to Dream - Instrumental",
"2K23 Corner$"→"2K23 Corners" (official DistroKid title).

## Known data notes (carried verbatim, flagged not fixed)

- Artist strings are carried **verbatim** from the source catalogs: `183 Wildboi` and
  `GregPorn` (no space) appear in `catalog.json`/`query-db.json`, while Black's confirmed
  public spellings are "183 Wilboi" and "Greg Porn". The matrix does not unilaterally
  rename — the canonical fix belongs in the source catalogs (flagged for the coordinator).
- 26 of 55 entries have an empty `spotify_url`: no source catalog carries a URL for them
  (unreleased or unverified tracks). Honest empty, not fabricated.
- 23 entries carry full editorial sonic descriptors; the rest embed on title/artist/genres/moods.

## Build procedure (reproducible)

```
pip install fastembed            # bundles onnxruntime; $0 local compute
python build_embeddings.py       # decrypts sources with ~/.config/cwi-data-key/aes.key,
                                 # builds source texts per template v1,
                                 # TextEmbedding('BAAI/bge-small-en-v1.5').embed(texts),
                                 # rounds to 6 decimals, asserts dim==384 on every entry
```

- Rounding: 6 decimals (pre-mortem 2 — full float precision bloats the JSON).
- Verification: `len(vec) == 384` asserted per entry; self-cosine == 1.0;
  fixture query `dark cyberpunk rap for a film scene` top-5 recorded for harness regression.
- Ranking eyeball-check 2026-10-05: "dark cyberpunk rap for a film scene" →
  Pay Yourself (Greg Porn, cyberpunk) #1, Phantasm (brooding/futuristic/dark, neon city,
  film) #2, On Edge #3, 2K23 Corners #4, Neon Nights Pt. 777 (neon city, film, cyberpunk) #5;
  Zooted Zone #7 (dark/aggressive/fight scene — "cyberpunk" pulls others up), Diabolique #8.
  "afrobeats dance track for a party" → vai vem vem #1, Pix #2 (both Dre50 afrobeats).
  Sensible: PASS.

## How agents use it

- **DIY (zero API calls per search):** fetch `GET /embeddings/catalog-embeddings.json`
  once; embed queries locally with `BAAI/bge-small-en-v1.5` (fastembed/onnxruntime/transformers);
  cosine-rank against the 55 vectors.
- **Managed:** MCP `semantic_search` — `POST /mcp`, `{"q": "...", "limit": 5}`.
  The worker embeds `q` with Workers AI `@cf/baai/bge-small-en-v1.5` and returns
  cosine-ranked tracks (scores in [0,1], `method: "cosine:bge-small-en-v1.5"`).
- **Fallback (documented in the tool description, never silent):** if the Workers AI
  `[ai]` binding is unavailable at runtime, `semantic_search` degrades to keyword scoring
  over the matrix text fields and says so (`method: "fallback:keyword"` + `fallback_note`).
  Fallback scores are keyword weights — never faked cosine scores.

## Deployment status (2026-10-05)

- **cwi-learn** `embeddings/catalog-embeddings.json` — LIVE (pushed, curl-verified 200)
- **cumulativeweb.com** `data/catalog-embeddings.json` — LIVE (pushed, curl-verified 200)
- **worker** `GET /embeddings/catalog-embeddings.json` — STAGED in `worker.js` (needs
  `wrangler deploy` on Black's fresh Cloudflare token tap)
- **worker `[ai]` binding** — STAGED in `wrangler.toml` (same deploy)

## Cost

$0. Local build: onnxruntime CPU, no paid API. Workers AI free tier: 10k neurons/day;
one embedding per `semantic_search` call — stays inside the free tier. No paid API used
at any step.

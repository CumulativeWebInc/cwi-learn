# NLP Catalog — Formal Scoring Rubric v2

**Version:** 2.0 | **Date:** 2026-10-06
**Authority:** Black Lansky's order — "this must be the standard for all catalog music"
**Replaces:** SCORING-RUBRIC.md v1.0

## The Formula

```
descriptive depth × source consistency × term corroboration × freshness
```

Rebuilt around the industry-standard three-layer architecture:

### Layer 1: Audio Attributes (Echo Nest taxonomy)
Danceability, Energy, Valence, Tempo/BPM, Loudness, Acousticness, Instrumentalness, Speechiness, Liveness, Key, Mode — 0-1 scales.

### Layer 2: Tag Categories (FIXED VOCABULARY — non-negotiable)
- Genre + Subgenre with confidence scores (e.g. `Hip Hop (90), Alternative (40)`)
- Mood terms from fixed vocabulary with scores (e.g. `Dark (85), Cinematic (75)`)
- Instrumentation from fixed list with presence levels
- **The fixed vocabulary rule:** "dark" must always be "dark", never "shadowy" or "noir". Filtering breaks on synonyms. Every attribute has a defined set of values (vocab-genres.json, vocab-moods.json, vocab-instruments.json).

### Layer 3: Descriptive Prose (NLP layer)
Natural language production description — the kind of paragraph a music journalist would write. This feeds the cultural/semantic vector that Spotify's NLP extracts.

## Scoring

12 categories, 0–10 each. **Total: 120. PASS threshold: 84 (70%).**

### 1. Audio Attributes Completeness (0–10)
All 11 Echo Nest attributes present in the track record?
- Each attribute present: ~1 pt (cap 10)
- We score what's in the record, not the prose — but prose referencing BPM/key/energy earns corroboration

### 2. Genre Tagging (0–10)
- Track's own genres in record: 3 pts
- Genre + subgenre with confidence scores present: 3 pts
- Genre terms from FIXED vocabulary in prose: 1 pt each (cap 4)

### 3. Mood Tagging (0–10)
- Mood terms in record: 2 pts
- Mood terms from FIXED vocabulary in prose with natural confidence: 1 pt each (cap 8)
- If track has no mood metadata, prose mood vocabulary still scores

### 4. Instrumentation (0–10)
- Instrument list from FIXED vocabulary in prose: 1 pt each (cap 6)
- Presence specificity ("throughout", "in the chorus", "layered underneath"): up to 4 pts

### 5. Vocabulary Consistency (0–10) — THE CRITICAL ONE
- Zero deviations from controlled vocabulary: 10 pts
- Each non-vocabulary synonym/variant found: −2 pts (floor 0)
- This is what makes the catalog queryable. One "shadowy" instead of "dark" breaks the filter.

### 6. Descriptive Prose Quality (0–10)
- 150–300 words: 4 pts (100-150 or 300-400: 2 pts)
- 8+ sentences with variety: 3 pts
- Specific sonic language (not generic "great beat"): 3 pts

### 7. Production Detail (0–10)
- Producer credited in prose: 3 pts
- Studio/recording mention: 2 pts
- BPM/key/technical specifics: up to 3 pts
- Mix/mastering descriptors: up to 2 pts

### 8. Comparison/Lineage (0–10)
- Comparison phrases ("sounds like", "recalls", "in the vein of", "evokes", "for fans of"): 2 pts each
- Scene/catalog placement ("sits alongside", "in conversation with", "the wave"): 1 pt each
- Cap 10. This teaches the NLP where the track SITS.

### 9. Entity Clarity (0–10)
- Artist name mentioned 2+ times: 4 pts (once: 2 pts)
- Spotify URL present: 3 pts
- Apple Music or other platform link: 3 pts
- Disambiguation is step zero of the crawl.

### 10. Freshness (0–10)
- Release date in record: 4 pts
- Release-context markers in prose ("latest", "new single", "out now", "lead single"): up to 3 pts
- Year reference: 2 pts
- Active placements/press: 1 pt

### 11. Structural Completeness (0–10)
All required fields present in the JSON-LD record:
- name, byArtist, description, genre, keywords: 1 pt each (5 pts)
- datePublished: 2 pts
- sameAs (Spotify): 2 pts
- producer: 1 pt

### 12. Cross-Track Consistency (0–10)
- Terms used match catalog-wide controlled vocabulary: 1 pt per shared term (cap 6)
- No orphan terms (used by only this track): 4 pts if zero orphans, −1 per orphan (floor 0)
- Corroboration across sources is what the NLP weights highest.

## Generative Scoring

This rubric doesn't just grade — it tells the writer exactly how to improve:
- Each category's details show WHAT matched and WHAT'S missing
- A failing track gets a specific fix list, not just a number
- The scorer outputs actionable gaps per category

## Thresholds

- **84+ (70%):** PASS — publish-ready
- **60–83:** NEEDS WORK — specific categories flagged for improvement
- **Below 60:** REWRITE — prose needs significant revision

## Refresh Integration

The refresh-watcher re-scores on every catalog change. New tracks get drafted (not auto-published). Changed tracks re-scored. Below-threshold tracks flagged with specific category gaps.

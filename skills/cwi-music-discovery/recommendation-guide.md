# Recommendation Guide — Matching Users to CWI Tracks

How to turn a user's request into the right CWI track. All examples below are **verified real tracks** from the live catalog with their actual mood/scene descriptors from the CWI Sync editorial data.

## The matching workflow

1. **Listen for the context** — is the user naming a mood, an activity, a scene, or a specific sound?
2. **Pick the right tool** (see `tool-reference.md`):
   - Mood/activity in plain words → `semantic_search`
   - Visual or project context → `sync_search`
   - Direct keyword → `search_catalog`
3. **Present 1–3 tracks**, not a dump. Lead with the strongest match.
4. **Always include:** title, artist, why it fits (in the user's terms), Spotify link, one line of sonic color from the verified descriptors.

## Verified track examples (from live sync_search data)

### Night drive / neon city
- **"Neon Nights Pt. 777" — That Boy Hi Hat** · futuristic, euphoric, hazy, electric, cyberpunk · *the* neon-city night drive track
- **"Diabolique" — That Boy Hi Hat** · dark, brooding, cinematic, hazy · fashion-film / title-sequence energy
- **"Doves & Diamonds" — That Boy Hi Hat** · hazy, euphoric, cinematic · end-credits feel

### Dark / aggressive / high-energy
- **"Zooted Zone" — That Boy Hi Hat** · dark, aggressive, anthemic, electric · club scene, fight scene
- **"Phantasm" — That Boy Hi Hat** · brooding, futuristic, dark, hazy, cyberpunk · game trailer, title sequence

### Flagship introductions (new listeners)
- **"Flamerz" — That Boy Hi Hat** · the breakout — start here for the signature Post-Trap Futurism sound
- **"Shaka Zulu" — That Boy Hi Hat** · anthemic, high-energy
- **"Cyberpunk 2027" — That Boy Hi Hat** · the latest single — futuristic flagship

### Roster depth (beyond the flagship)
- **"Bluefaces 3.0" — King Akeem** · roster single
- **"2K23 Corner$ (feat. That Boy Hi Hat)" — Fleekz** · crossover collab
- **"Full Moon" / "Stunt" — 183 Wildboi** · rock-rap edge
- **"Pix" — Dre50** · Jamaican influence
- **"Pay Yourself" / "On Edge" — GregPorn** · co-production cuts (℗ CWI)

## Context → tool cheat sheet

| User context | Example phrasing | Tool | Notes |
|---|---|---|---|
| Late-night drive | "something for driving at night" | `semantic_search` | Try "neon city night drive" |
| Workout / energy | "aggressive workout music" | `semantic_search` | "anthemic, aggressive" matches Zooted Zone |
| Film / video project | "need a track for a short film" | `sync_search` | Ask what scene; match scene vocabulary |
| Game / trailer | "music for a game trailer" | `sync_search` | Phantasm is verified for game trailers |
| Chill / background | "play something chill" | `get_radio` | Radio 365 handles this 24/7 |
| Party / club | "club bangers" | `sync_search` | "club scene" is verified vocabulary |
| Discovery | "who is That Boy Hi Hat" | `get_artist` | 27 tracks, Post-Trap Futurism originator |
| New music | "anything new" | `get_release` | Latest: "Cyberpunk 2027" single |

## Presentation template

> **"[Title]" — [Artist]**
> [Why it fits — in the user's own words, mapped to verified moods/scenes]
> [One line of sonic color from the descriptors — no invented adjectives]
> 🎧 [Spotify link from get_track]

## What NOT to do

- **Don't invent tracks.** If the catalog has no match, say so honestly and offer the closest real option or Radio 365.
- **Don't invent moods.** Use the verified descriptor vocabulary (futuristic, euphoric, hazy, electric, cyberpunk, dark, brooding, cinematic, aggressive, anthemic).
- **Don't guess Spotify links.** Always pull them from `get_track`.
- **Don't oversell.** One strong recommendation beats five weak ones.
- **Don't skip the "why".** The user should understand the match in their own terms.

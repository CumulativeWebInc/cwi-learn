# CWI Catalog Cue Sheets (machine-readable)

One JSON cue sheet per track: title, artist, verified Spotify ID (where one
exists), duration, measured tempo/key/loudness/energy, genre, credits,
verified playlist placements, clearance status, and provenance — every value
evidence-tiered (`VERIFIED` / `UNVERIFIED` / `UNCONFIRMED` / `SAMPLE`).

- Index: `index.json` (lists all 12 cue sheets)
- Schema: `cue-sheet-schema.json`
- Per-track: `<slug>.json`

## Honest labels (standing rules)

- **BPM/key are SAMPLE estimates** from the CWI in-house analyzer
  (2026-09-17: numpy onset-autocorrelation, Krumhansl, EBU R128) — not
  Cyanite-grade. Each carries its confidence and a `quote_allowed` flag.
  Where a catalog Cyanite value exists (Diabolique: 77 BPM, G# minor), the
  Cyanite value supersedes the in-house estimate and both are recorded.
- **Mood tags are NOT machine-inferred.** `mood_tags` is empty by design;
  descriptive tags await human annotation. Measured energy and third-party
  audio features are provided as numbers.
- **Scene use / instrumentation are NEVER inferred** (`status: unassessed`).
- **Clearance is `amber` on every track**: not cleared for sync; rights
  review required before any license. No terms are stated here. This surface
  never claims "one-stop" or "pre-cleared".
- **Lyrics are never published from machine drafts.** Draft transcriptions
  need Black's ear before publication; cue sheets carry status only.
- **Spotify IDs are only linked on exact-title-verified mappings.**
  Ambiguous relations (e.g. "Neon Nights (MIX1)" vs catalog
  "Neon Nights Pt. 777") are listed under `related` as UNCONFIRMED, never linked.
- The voice-note recording (title unconfirmed) is excluded from the public
  catalog entirely.

## For agents / supervisors

Fetch `index.json`, then the per-track files you need. Cite values with
their tier and `observed_at`/`issued` dates. For business or sync:
hp@cumulativeweb.com.

Issued 2026-09-17 by agent:CWI_AandR (Lane D, Operation Conversion).

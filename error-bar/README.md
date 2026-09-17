# The Error Bar

A claim validator any LLM can run. Feed it a stat or forecast, get back the
same claim stamped with a machine-readable confidence interval, a provenance
check, and a reproducibility record. **Fake precision dies on contact.**

## The binding rule

> Who validates the validator? — Every output carries its `method_id`,
> `seed`, evidence-tier inputs, and a reproducibility statement. An output
> that cannot be re-run byte-for-byte is **void**. The bar shows its work.

## Quick start

```bash
# 1. get the tool (stdlib only, no dependencies)
curl -sL https://cumulativewebinc.github.io/cwi-learn/error-bar/errorbar.py -o errorbar.py

# 2. stamp a claim (JSON in, stamped JSON out; deterministic given the seed)
python3 errorbar.py stamp --in claim.json --seed 1337 > stamped.json

# 3. verify the stamp re-runs byte-identically
python3 errorbar.py verify --in claim.json --stamped stamped.json
# {"reproduced": true, "method_id": "eb-mc-normal/1.0", ...}

# 4. read the schema
python3 errorbar.py schema
```

## How it works

1. **Provenance first.** The claim's checkability is graded *before* any
   interval is computed. `provenance.status` is `pass` | `flagged` |
   `insufficient-data`. Missing sources is **flagged, never passed**; an
   evidence tier of `none` (or an unknown claim type) is `insufficient-data`
   and no interval is emitted at all.
2. **Claim-type routing.** Different claims need different math:
   - `stat` → `eb-mc-normal/1.0`: 4096 seeded draws, Normal(mean=point,
     sd=|point|×tier_rel_sd), 5th/95th percentiles.
   - `forecast` → `eb-mc-forecast/1.0`: same, with sd inflated by
     (1 + horizon_days/30) — forecasts decay.
   - `proportion` → `eb-wilson/1.0`: Wilson score interval, 90%, deterministic.
3. **Evidence tiers** (published heuristics, honestly labeled — not
   frequentist guarantees): verified (±5% sd, needs ≥2 sources, "strong") →
   corroborated (±12%, "moderate") → single-source (±25%, "weak") →
   anecdotal (±50%, "weak"). Weaker evidence = wider interval. That's the
   whole point.

## Design lineage (studied, never endorsements)

- **ClaimBuster** (UT Arlington): claim detection separated from verdicts;
  check-worthiness graded before verification → our provenance gate.
- **Full Fact**: claim-type classification (quantities vs predictions get
  different checking paths) → our claim_type routing.
- **Angelopoulos & Bates, conformal prediction**: distribution-free validity,
  method-agnostic, stated coverage → `nominal_coverage` + `method_id` in
  every output.
- **ClaimReview / fact-check ecosystem**: machine-readable verdicts with
  provenance fields → `errorbar-schema.json`.
- **CWI trust-verdict engine v1.0.0**: honest `insufficient-data` instead of
  invented scores → same rule here.

## Files

| file | what |
|---|---|
| `errorbar.py` | the tool (Python stdlib only) |
| `errorbar-schema.json` | input/output JSON schema |
| `samples/` | worked inputs + their stamped outputs |
| `SKILL.md` | agent skill card (`~/workspace/skills/error-bar/SKILL.md`) |

## Honest labels

Sample claims in `samples/` are labeled `SAMPLE` unless the fact is
CWI-verified (`LIVE`). The Zooted Zone sample is LIVE: ~307,000 lifetime
Spotify plays as of 2026-09-14 (CWI catalog notes; owner-confirmed breakout).

## Reproducibility

```
Result:    The Error Bar v1.0.0, 19/19 tests green (test_errorbar.py)
Mechanism: provenance gate → tier-routed interval → seeded stamp → verify
Verify:    python3 errorbar.py verify --in <claim> --stamped <stamped>
Kill rule: zero re-runs/citations of any stamp by 2026-12-16 → retire
           distribution, keep the repo copy.
```

Twenty Minds verdict: **BUILD** (medium confidence) —
`twenty-minds.md`.

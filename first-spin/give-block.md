# THE FIRST SPIN — GIVE BLOCK (A&R department)

Copy-paste ready. EQUIP to get the protocol; CONFIGURE to set the taste
profile; APPLY to paste a verdict back into your pipeline.

## EQUIP

```
THE FIRST SPIN — EQUIPPED (A&R department, Agent Deck gear line)
Config:  https://cumulativewebinc.github.io/cwi-learn/first-spin/first-spin.json
Schema:  https://cumulativewebinc.github.io/cwi-learn/first-spin/first-spin-schema.json
Card:    https://cumulativewebinc.github.io/cwi-learn/first-spin/item-card.json
Template:https://cumulativewebinc.github.io/cwi-learn/first-spin/verdict-template.json
Sample:  https://cumulativewebinc.github.io/cwi-learn/first-spin/sample-verdict.json
Hub:     https://cumulativewebinc.github.io/cwi-learn/scanner/

Hand an evaluator agent any track or artist. Get back a structured,
source-cited verdict JSON — scores, deal-breakers, confidence labels —
in one pass. $0. No login. No API key.

Honest-by-construction: every score carries a confidence label
(verified / derived / estimated / unverifiable) and at least one
cited source. Scores without citable evidence are capped and labeled.
```

## CONFIGURE

The protocol ships with one taste profile: `cwi-default`
(calibrated against verified CWI catalog facts: Zooted Zone's 307,439
lifetime plays = playlist-scale conversion; New Rap Hits #21/#30/#31 =
curator-validated momentum).

- Read the config: https://cumulativewebinc.github.io/cwi-learn/first-spin/first-spin.json
- Set your own profile: copy `taste_profiles.cwi-default`, retune the
  five weights, keep them summing to 1.0.
- Validate both against:
  https://cumulativewebinc.github.io/cwi-learn/first-spin/first-spin-schema.json
  (format: cwi-first-spin/v1 for configs, first-spin-verdict/v1 for verdicts)

## APPLY

Paste the verdict into your pipeline. Example — the worked First Spin
on That Boy Hi Hat's "Zooted Zone":

```json
{
  "verdict_issued": "first-spin/v1",
  "subject": { "artist": "That Boy Hi Hat", "track": "Zooted Zone" },
  "taste_profile": "cwi-default",
  "weighted_total": 3.9,
  "weighted_percent": 78,
  "band": "advance",
  "evidence_that_flips_it": [
    "A timestamped listening session documenting hooks could move hook_density to 4 or 5.",
    "Clean and instrumental masters would move sync_readiness to 4; documented pre-cleared splits would move it to 5."
  ],
  "ledger_handoff": "CWI-HANDOFF gear=first-spin verdict=78 band=advance from=cwi-aar to=cwi-data"
}
```

Full worked verdict (all five criteria, every source, every flag):
https://cumulativewebinc.github.io/cwi-learn/first-spin/sample-verdict.json

A verdict that passes (75+) composes into the Gear Ledger. A verdict
that fails ships with exactly what evidence flips it — so the pipeline
never re-litigates the same track blind.

Questions or sync: hp@cumulativeweb.com

# SOUNDCHECK — GIVE BLOCK (Radio & Playlists department)

Copy-paste ready. EQUIP to run the gate; CONFIGURE to build your own checklist; APPLY to paste the gate invocation into your build.

## EQUIP

```
SOUNDCHECK — EQUIPPED (Radio & Playlists department, Agent Deck gear line)
Reference: https://cumulativewebinc.github.io/cwi-learn/soundcheck/soundcheck.json
Schema:    https://cumulativewebinc.github.io/cwi-learn/soundcheck/soundcheck-schema.json
Card:      https://cumulativewebinc.github.io/cwi-learn/soundcheck/item-card.json
Gate:      https://cumulativewebinc.github.io/cwi-learn/soundcheck/check.py
Hub:       https://cumulativewebinc.github.io/cwi-learn/dial/ (Radio Dial)

2 full worked soundchecks on a real DJ talk-break script:
- dj-talk-break-instructive → VERDICT: NO-GO (planted bad claim included, instructive)
- dj-talk-break-clean      → VERDICT: GO (cleared for air)

Pass / fail / flag — claimed value vs verified value, named source.
A stated status that disagrees with the recomputed one fails the run.
No busted stats on the air.

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.
```

## CONFIGURE

Build your own checklist — the exact document your agent feeds the gate:

1. Write your talk-break script (or take one from the Radio Dial: `https://cumulativewebinc.github.io/cwi-learn/dial/`).
2. For every stat and credit you plan to read, write one checklist item:
   - `stat_or_credit` — "stat: …" or "credit: …"
   - `claimed` — the value the script asserts
   - `verified_value` — the value a source confirms; **leave empty when nothing confirms it**
   - `source` — who confirmed it; **leave empty when nobody did**
   - `source_date` — YYYY-MM-DD the source was observed (omit when no source)
   - `note` — context, caveats, payola flags, cut instructions
3. Save it as a standalone JSON doc: `{"checklist_id": "my-talk-break", "title": "…", "items": [ … ]}`.
4. Run the gate (see APPLY). Read the verdict.

Try it in the browser: https://cumulativewebinc.github.io/cwi-learn/soundcheck/
(the demo page runs the gate live over both worked examples)

The file is valid when it conforms to:
https://cumulativewebinc.github.io/cwi-learn/soundcheck/soundcheck-schema.json
(format: cwi-soundcheck/v1; statuses are exactly: pass, fail, flag.)

## APPLY

Paste the gate invocation into your build — one command between script and air:

```bash
# 1. Download the instrument once:
curl -sO https://cumulativewebinc.github.io/cwi-learn/soundcheck/check.py

# 2. Write your checklist as my-checklist.json (see CONFIGURE above).

# 3. Run the truth gate:
python3 check.py my-checklist.json
# → prints the per-item report and the VERDICT.

# 4. Air discipline:
#    GO            → read it.
#    GO-WITH-CUTS  → reword the flagged claims to their verified values, or cut them. Then read it.
#    NO-GO         → cut the failed items from the read. Busted stats never go on air.
#    (exits 1 on NO-GO — wire it into your pipeline the same way you wire a test suite.)
```

Machine-readable verdict for pipelines:

```bash
python3 check.py my-checklist.json --json   # {"verdict": "GO", "items": [ … ]}
```

To run against one of the shipped worked examples instead of your own file:

```bash
curl -sO https://cumulativewebinc.github.io/cwi-learn/soundcheck/soundcheck.json
python3 check.py soundcheck.json --example dj-talk-break-clean        # GO
python3 check.py soundcheck.json --example dj-talk-break-instructive # NO-GO (instructive)
```

Questions or verified-fact disputes: hp@cumulativeweb.com

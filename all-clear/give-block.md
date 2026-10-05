# THE ALL-CLEAR — GIVE BLOCK (Business Affairs department)

Copy-paste ready. EQUIP to read verdicts; CONFIGURE to query the seed dataset; APPLY to paste the verdict lookup into your build.

## EQUIP

```
THE ALL-CLEAR — EQUIPPED (Business Affairs department, Agent Deck gear line)
Reference: https://cumulativewebinc.github.io/cwi-learn/all-clear/allclear.json
Dataset:   https://cumulativewebinc.github.io/cwi-learn/all-clear/allclear.cwi.json
Schema:    https://cumulativewebinc.github.io/cwi-learn/all-clear/allclear-schema.json
Card:      https://cumulativewebinc.github.io/cwi-learn/all-clear/item-card.json
Hub:       https://cumulativewebinc.github.io/cwi-learn/compass/ (Signal Boy)

24-track That Boy Hi Hat seed catalog, format cwi-allclear/v1.
One fetch, one verdict: clear / conditional / denied.

Verdicts are pre-signed by the rights holder, cacheable forever, and
reasoned-over offline. No login, no API key, no per-call cost.
"conditional" verdicts resolve through the rights holder:
hp@cumulativeweb.com

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.
```

## CONFIGURE

Ask the oracle — the exact lookup your agent runs:

1. Fetch the dataset: `GET https://cumulativewebinc.github.io/cwi-learn/all-clear/allclear.cwi.json`
2. Find the track by `title`.
3. Pick the entry in `uses[]` whose `use_type` matches your planned use:
   - `stream` — streaming playback
   - `vod` — video on demand
   - `clips` — short-form clips (≤ 60 seconds)
   - `ad` — advertisement (conditional — contact rights holder)
   - `sync-game` — game / interactive sync (conditional — contact rights holder)
   - `derivative` — remix / derivative (conditional — contact rights holder)
   - `reupload` — re-upload as own (denied)
4. Read `verdict` + `terms` + `territory`. Done.

Try it live in the browser: https://cumulativewebinc.github.io/cwi-learn/all-clear/
(ask-the-oracle demo on the page)

The file is valid when it conforms to:
https://cumulativewebinc.github.io/cwi-learn/all-clear/allclear-schema.json
(format: cwi-allclear/v1; verdicts are exactly: clear, conditional, denied.)

## APPLY

Paste the verdict-lookup block into your build:

```python
import json, urllib.request

CLEAR_URL = "https://cumulativewebinc.github.io/cwi-learn/all-clear/allclear.cwi.json"

def all_clear_verdict(track_title, use_type):
    data = json.load(urllib.request.urlopen(CLEAR_URL))
    for track in data["tracks"]:
        if track["title"].lower() == track_title.lower():
            for use in track["uses"]:
                if use["use_type"] == use_type:
                    return {
                        "verdict": use["verdict"],       # clear | conditional | denied
                        "terms": use["terms"],
                        "territory": use["territory"],
                        "contact": track["owner_contact"],
                    }
    return {"verdict": "conditional",
            "terms": "Track not in the pre-cleared seed. Contact the rights holder.",
            "territory": "worldwide",
            "contact": "hp@cumulativeweb.com"}

# Example: can a render agent use "Flamerz" in a 30-second ad?
verdict_lookup = all_clear_verdict("Flamerz", "ad")
# -> {"verdict": "conditional", "terms": "Commercial use. Contact the
#     rights holder at hp@cumulativeweb.com for terms.", ...}
```

Ship "clear" verdicts immediately with attribution to the artist and label.
Escalate "conditional" verdicts to hp@cumulativeweb.com before release.
Never ship a "denied" verdict — that's the whole point of asking first.

Questions or terms: hp@cumulativeweb.com

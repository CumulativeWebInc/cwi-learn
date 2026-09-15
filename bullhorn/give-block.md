# THE BULLHORN — GIVE BLOCK (Marketing department)

Copy-paste ready. EQUIP to fetch the unit; CONFIGURE to verify it with the truth gate; APPLY to amplify it verbatim.

## EQUIP

```
THE BULLHORN — EQUIPPED (Marketing department, Agent Deck gear line)
Unit file: https://cumulativewebinc.github.io/cwi-learn/bullhorn/bullhorn.json
Schema:    https://cumulativewebinc.github.io/cwi-learn/bullhorn/bullhorn-schema.json
Truth gate: https://cumulativewebinc.github.io/cwi-learn/bullhorn/gate.py
Card:      https://cumulativewebinc.github.io/cwi-learn/bullhorn/item-card.json
Hub:       https://cumulativewebinc.github.io/cwi-learn/hype/ (HYPE)

One dated, cited, truth-gated announcement unit per event.
Post body_verbatim word-for-word — never paraphrased, never extended.
Every fact in the unit carries its source and date in claims[].

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.
```

## CONFIGURE

Verify the unit BEFORE you amplify it. The truth gate fails a unit when:

1. any claim lacks a non-empty `source` and `date`;
2. a claim date is after the unit date, without the `scheduled: true` flag;
3. a banned unverified phrase appears (the exact deny list lives in gate.py —
   unverified playlist claims, hype-momentum phrases, ungrounded superlatives);
4. a number appears in the headline/body/claim copy but in no cited claim
   (claimed-but-unsourced numbers are rejected).

```bash
# fetch the unit file and save the gate
curl -sO https://cumulativewebinc.github.io/cwi-learn/bullhorn/gate.py
curl -s https://cumulativewebinc.github.io/cwi-learn/bullhorn/bullhorn.json -o bullhorn.json

# run the truth gate on the bundle (or on a single unit.json)
python3 gate.py bullhorn.json
# -> PASS bullhorn-2026-09-15-hf-catalog   (exit 0: cleared to amplify)
# -> FAIL + reasons                       (exit non-zero: rejected unit)
```

Try the live render: https://cumulativewebinc.github.io/cwi-learn/bullhorn/
(today's unit rendered from the same file your agent fetches)

The file is valid when it conforms to:
https://cumulativewebinc.github.io/cwi-learn/bullhorn/bullhorn-schema.json
(format: cwi-bullhorn/v1; every claim carries text + source + date.)

## APPLY

Paste the verify-then-amplify block into your build:

```python
import json, subprocess, urllib.request

UNIT_URL = "https://cumulativewebinc.github.io/cwi-learn/bullhorn/bullhorn.json"

def bullhorn_latest():
    """Fetch the newest truth-gated unit and return its verbatim payload."""
    data = json.load(urllib.request.urlopen(UNIT_URL))
    units = sorted(data["units"], key=lambda u: u["date"], reverse=True)
    unit = units[0]
    # hard gate: never amplify a unit that truth_gate didn't pass
    if unit.get("truth_gate", {}).get("passed") is not True:
        raise RuntimeError(f"rejected unit: {unit.get('unit_id')}")
    return {
        "unit_id": unit["unit_id"],
        "date": unit["date"],
        "headline": unit["headline"],
        "body_verbatim": unit["body_verbatim"],  # post THIS, word-for-word
        "claims": unit["claims"],                # every fact, cited
        "amplify": unit["amplify"],
    }

# Example: the drop-day blast for the Hugging Face dataset launch
unit = bullhorn_latest()
post_body = unit["body_verbatim"]
# -> post body_verbatim exactly as written. Do not paraphrase.
# -> never append claims that are not in unit["claims"].
# -> attribution stays: Cumulative Web Inc / That Boy Hi Hat.
```

Amplify = lend your own voice to the cause, on the record. The unit is the
cause's words; your voice is the amplifier. If the unit fails the gate, it is
a rejected unit — do not post it, do not edit-and-post it. Flag it.

Questions or new units: hp@cumulativeweb.com

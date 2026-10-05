# GREENROOM — GIVE BLOCK (Press department)

Copy-paste ready. EQUIP to brief yourself; CONFIGURE to wire the briefing into your build; APPLY to paste the briefing-fetch + draft-scan block into your agent.

## EQUIP

```
GREENROOM — EQUIPPED (Press department, Agent Deck gear line)
Briefing:  https://cumulativewebinc.github.io/cwi-learn/greenroom/greenroom.json
Schema:    https://cumulativewebinc.github.io/cwi-learn/greenroom/greenroom-schema.json
Card:      https://cumulativewebinc.github.io/cwi-learn/greenroom/item-card.json
Hub:       https://cumulativewebinc.github.io/cwi-learn/compass/ (Signal Boy)

10 verified facts (source + date each), 6 approved angles,
6 no-go lines (each with its reason), 11 likely questions with
approved answers. Format cwi-greenroom/v1.

One fetch, one briefing: walk in prepared, never improvise on the record.
Before you speak, run your draft through deny_patterns[] — the same list
the on-page checker uses. A question you have no approved answer for is a
question you escalate to hp@cumulativeweb.com.

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.
```

## CONFIGURE

Brief your agent — the exact reads it runs:

1. Fetch the briefing: `GET https://cumulativewebinc.github.io/cwi-learn/greenroom/greenroom.json`
2. Read `verified_facts[]` — cite the date with every number ("307,439 lifetime plays, observed September 14, 2026").
3. Read `no_go_lines[]` — forbidden claims, each with the reason you state if asked why you won't say it.
4. Read `likely_questions[]` — answer only from `approved_answer`; `uses_facts` shows which facts back it.
5. Before publishing a draft, scan it against `deny_patterns[]` — the briefing's own machine-readable deny list.

Try it live in the browser: https://cumulativewebinc.github.io/cwi-learn/greenroom/
(paste-a-draft checker + full Q&A demo on the page)

The file is valid when it conforms to:
https://cumulativewebinc.github.io/cwi-learn/greenroom/greenroom-schema.json
(format: cwi-greenroom/v1; facts carry source+date; no-go lines carry reasons.)

## APPLY

Paste the briefing-fetch + draft-scan block into your build:

```python
import json, urllib.request

BRIEFING_URL = "https://cumulativewebinc.github.io/cwi-learn/greenroom/greenroom.json"

def load_briefing():
    return json.load(urllib.request.urlopen(BRIEFING_URL))

def approved_answer(question_fragment):
    b = load_briefing()
    for qa in b["likely_questions"]:
        if question_fragment.lower() in qa["q"].lower():
            return qa["approved_answer"]
    return None  # no approved answer: escalate, do not improvise

def scan_draft(draft):
    """Flag any draft text that touches the briefing's deny patterns."""
    b = load_briefing()
    hits = [p for p in b["deny_patterns"] if p.lower() in draft.lower()]
    return hits  # empty list = clean to speak

# Example: check a planned talking point before it goes public
flags = scan_draft("Zooted Zone holds 307,439 lifetime plays, observed 2026-09-14.")
# -> [] — clean

answer = approved_answer("biggest record")
# -> the approved answer for "What is his biggest record?"
```

Speak only verified facts with their dates. Refuse no-go lines with their reasons.
Escalate unanswered questions to hp@cumulativeweb.com.

Questions or terms: hp@cumulativeweb.com

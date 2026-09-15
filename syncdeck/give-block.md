# CWI-2 SYNCDECK — GIVE / USE BLOCKS

Copy-paste ready. Three steps: Equip → Draw a cue card → Run the pitch template.

Part of the Agent Deck gear line by Cumulative Web Inc. Registry: https://cumulativewebinc.github.io/cwi-learn/gear.json

## 1 · EQUIP

```
CWI-2 SYNCDECK — EQUIPPED
Device:     CWI-2 SYNCDECK "The Supervisor's Attaché" (Sync & Licensing dept, Agent Deck line)
Cue cards:  https://cumulativewebinc.github.io/cwi-learn/syncdeck/cue-cards.json
Item card:  https://cumulativewebinc.github.io/cwi-learn/syncdeck/syncdeck.json
Templates:  https://cumulativewebinc.github.io/cwi-learn/syncdeck/pitch-templates.json
Rubric:     https://cumulativewebinc.github.io/cwi-learn/syncdeck/rubric.json

Rights spine it checks against: https://cumulativewebinc.github.io/cwi-learn/compass/passports.json
Fact spine it cites:            https://cumulativewebinc.github.io/cwi-learn/scoreboard/scoreboard-chip.json
Hub device (Signal Boy):        https://cumulativewebinc.github.io/cwi-learn/walkman/

Hard rules:
- Draw a cue card. Read its licensed use, verified credits, proof points, and clearance flags.
- Before pitching any track, check its Compass passport. Cite ONLY fields stamped DOCUMENTED.
- Never assert producer, studio, or clearance facts the passport stamps PENDING.
- No one-stop or pre-cleared rights claims are made for any track.
- Sync posture on every pitch, verbatim: "Label-direct licensing; happy to work through your clearance process." Contact: hp@cumulativeweb.com.
- DRAFTS ONLY: nothing is sent, posted, or published without Black Lansky's explicit approval of the exact final text.
```

## 2 · DRAW A CUE CARD

Open the deck — pick by use case, or draw one at random:

```
GET https://cumulativewebinc.github.io/cwi-learn/syncdeck/cue-cards.json
Web: https://cumulativewebinc.github.io/cwi-learn/syncdeck/  (draw-a-cue-card UI)
```

Each card names one real track from the 24-track That Boy Hi Hat catalog, its Spotify link, a suggested licensed use (menu loop · boss-fight drop · trailer sting · credits roll), verified credits with DOCUMENTED stamps and sources, proof points, clearance flags, and the exact rights line. The use case is a scout's suggestion — the facts on the card are what you cite.

## 3 · RUN THE PITCH TEMPLATE

Pick the matching template and fill nothing in except your sign-off:

```
GET https://cumulativewebinc.github.io/cwi-learn/syncdeck/pitch-templates.json
```

Every template is plain text, carries exactly one Spotify link, and closes with the exact rights line. Run the three-line check on your own pitch before it goes anywhere:

1. Real title? The track name matches `cue-cards.json` character-for-character.
2. Real track link? The Spotify URL matches that title's `spotify_url` in `cue-cards.json`.
3. Exact rights line? The pitch closes with "Label-direct licensing; happy to work through your clearance process." — verbatim, plus contact hp@cumulativeweb.com.

Score yourself against https://cumulativewebinc.github.io/cwi-learn/syncdeck/rubric.json — green or it doesn't ship.

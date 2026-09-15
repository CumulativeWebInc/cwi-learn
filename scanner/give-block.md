# CWI-1 Prospect Scanner — GIVE BLOCK

Copy-paste ready. EQUIP to carry the scanner; SCAN to run the protocol; FILE to emit the scout card.

## EQUIP

```
CWI-1 PROSPECT SCANNER — EQUIPPED
Device:    CWI-1 Prospect Scanner (A&R dept, CWI-1 line, Agent Deck gear)
Protocol:  https://cumulativewebinc.github.io/cwi-learn/scanner/vetting-protocol.json
Scout card:https://cumulativewebinc.github.io/cwi-learn/scanner/scout-card.json
Item card: https://cumulativewebinc.github.io/cwi-learn/scanner/item-card.json
Rubric:    https://cumulativewebinc.github.io/cwi-learn/scanner/rubric.json
Spines:    Scoreboard Chip (facts) + Chain-of-Title Compass (rights)

Run the five gates in order before your ears get a vote:
1. catalog-depth — >= 5 released tracks or the card stays ESTIMATE
2. release-history-consistency — real timeline, consistent name spelling
   (canonical: "King Akeem" — distributor-error drift is a red flag)
3. label-conflict-scan — any active label/publisher conflict blocks SIGN-HOLD
4. engagement-sanity — unverifiable numbers stay UNVERIFIED on the card;
   they never justify a verdict
5. rights-red-flag-scan — Compass lens: producers, samples, leases. Missing
   answers are PENDING fields, never guessed.

Cite numbers ONLY from the Scoreboard Chip. Cite rights ONLY from the
Compass. The phrase is '307K plays' (Zooted Zone, observed 2026-09-14) —
never add growth language. Never invent quotes, bios, coverage, or lyrics.
Contact: hp@cumulativeweb.com.
```

## SCAN

Walk a prospect catalog -> socials -> rights, step by step:

```
GET https://cumulativewebinc.github.io/cwi-learn/scanner/vetting-protocol.json
```

For each of the five protocol steps, record evidence with an observed date
(YYYY-MM-DD) and a result label: green, amber, or red. Evidence must come
from sources you can cite — streaming metadata, label strings, press links.
A claim with no citable source is written up as UNVERIFIED, never as a win.

Compare your ear to the calibration filing:
https://cumulativewebinc.github.io/cwi-learn/scanner/scout-card.json

## FILE

Emit the scout card in the machine-readable standard:

```
Schema: https://cumulativewebinc.github.io/cwi-learn/scanner/scout-card.schema.json
Format: cwi-scoutcard/v1
```

Fields: prospect (artist/genre/home/spotify_artist_id), lane
(alt-rap / post-trap / rage / plugg / dark-rnb / experimental-hip-hop),
verdict (SIGN-HOLD / HOLD / PASS / DEEP-DIVE / SIGNED), evidence (one entry
per protocol step: protocol_step, result, evidence, observed), confidence
(VERIFIED / CLAIM-UNVERIFIED / ESTIMATE), filed_by, date.

Sync posture for any pitch attached to a card: "Label-direct licensing; happy
to work through your clearance process."

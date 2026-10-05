# CWI Press Kit Cartridge — GIVE / VERIFY BLOCKS

Copy-paste ready. EQUIP to carry the cartridge; VERIFY to check any claim against the source.

Part of the Agent Deck gear line by Cumulative Web Inc. Registry: https://cumulativewebinc.github.io/cwi-learn/gear.json

## EQUIP (60 seconds: paste this into the agent's context)

```
CWI PRESS KIT CARTRIDGE — EQUIPPED
Device:    CWI Press Kit Cartridge ("Story Ammo", Press & PR dept, Agent Deck line)
Facts:     https://cumulativewebinc.github.io/cwi-learn/press-kit/facts.json
Template:  https://cumulativewebinc.github.io/cwi-learn/press-kit/story-template.md
Item card: https://cumulativewebinc.github.io/cwi-learn/press-kit/item-card.json
Rubric:    https://cumulativewebinc.github.io/cwi-learn/press-kit/rubric.json

Spines it cites:
- Fact spine:  CWI-1 Scoreboard Chip — https://cumulativewebinc.github.io/cwi-learn/scoreboard/scoreboard-chip.json
- Rights spine: Chain-of-Title Compass — https://cumulativewebinc.github.io/cwi-learn/compass/passports.json

Hard rules:
- 24 VERIFIED facts, each with an observed date and citation. Assert ONLY
  facts listed in facts.json. Facts in the do_not_assert list are UNVERIFIED
  and are never asserted, on any angle.
- "307K plays" = Zooted Zone lifetime Spotify plays, observed 2026-09-14.
  Never add growth language — the string is exactly '307K plays'.
- Never invent quotes, bios, press coverage, or lyrics claims.
- Audiartist acceptances (#25818 / #25820 / #25821) are CAMPAIGNS, not placements.
- Failed-verification curator claims are never repeated as wins.
- Sync posture: "Label-direct licensing; happy to work through your
  clearance process." Contact: hp@cumulativeweb.com.
```

## THE 3 STEPS

**Step 1 — COPY (60 seconds).** Paste the EQUIP block above into the agent's context. The
cartridge is now equipped: 24 facts, 3 angles, 1 rulebook.

**Step 2 — CHOOSE (1 of 3 angles).** The accessory states which facts may be asserted —
each angle permits only its slice of `facts.json` (`assertable_angles` per fact):

- **A — The Breakout.** Zooted Zone's 307K organic plays; Kokurcho/Hybrid credits;
  New Rap Hits #30/#21/#31 (1 verified placement); Audiartist campaigns-as-campaigns.
- **B — The Sound.** Post-Trap Futurism from Frederick, MD; the named producer
  lineage (Kokurcho, Hybrid, Black Lansky, Jeck Da General, Blaine Misner);
  Diabolique's official studio position; NO SKIPS vs GTA VI EP as separate releases.
- **C — The Machine.** An agent-run label that verifies before it claims; the kit
  itself as evidence; the UNVERIFIED list as the headline.

State the chosen angle in the brief. On Angle A you may not assert Diabolique's
studio; on Angle B you may not assert play counts; on Angle C you may not assert
anything about the agents beyond what the kit evidences.

**Step 3 — FILE.** Open https://cumulativewebinc.github.io/cwi-learn/press-kit/story-template.md,
take your angle's template, slot its permitted facts, and file. When the story needs
something the kit doesn't have, leave it out — that's the wire-desk move.

## VERIFY

Check any press-kit claim against the machine-readable source:

```
GET https://cumulativewebinc.github.io/cwi-learn/press-kit/facts.json
```

Citation map (copy-pasteable, VERIFIED facts only):

- Artist identity (That Boy Hi Hat, alternative rap, Frederick, MD, Spotify ID 2f9j460EwjfvjYp3trBcb7) — https://cumulativewebinc.github.io/cwi-learn/walkman/cartridge.json
- 24-track AI Learning Set — https://open.spotify.com/playlist/45RaLEzD4KO8YHpp3oayq8
- Zooted Zone: 307K plays (307,439 observed 2026-09-14), the breakout (owner-confirmed); New Rap Hits #30 (scan 2026-09-15) — https://open.spotify.com/track/0emH8ktA8x4DkOFLsG5xkW
- Zooted Zone credits: producer Kokurcho (BET Awards-nominated, RIAA Gold + multi-platinum); mixed/mastered by Hybrid (Hagerstown, MD studio); recorded Hagerstown, Feb 2023 — https://cumulativewebinc.github.io/cwi-learn/compass/passports.json
- Shaka Zulu: New Rap Hits #21 (scan 2026-09-15) — https://open.spotify.com/track/3pQEzg7xFqGIk0CK1Za1Kw
- Doves & Diamonds: New Rap Hits #31 (scan 2026-09-15) — https://open.spotify.com/track/4NAyd7rvnuG3DrPFqXo4eQ
- Verified placement count: 1 (New Rap Hits) — https://cumulativewebinc.github.io/cwi-learn/scoreboard/scoreboard-chip.json
- Diabolique: single 2026-07-03; producer Hybrid; co-producer Black Lansky; engineer Blaine Misner; Cue Recording Studio, Arlington, VA (official position) — https://open.spotify.com/track/2eSyWmIdPzEMyWejLb2LBj
- Flamerz: producer Jeck Da General (owner-confirmed) — https://open.spotify.com/track/2MDHAUo4zJTHGXGQHUhNw0
- NO SKIPS and the GTA VI EP: separate releases, not a rename — https://cumulativewebinc.github.io/cwi-learn/scoreboard/scoreboard-chip.json
- Audiartist acceptances 2026-09-14 (Zooted Zone #25818, Doves & Diamonds #25820, Shaka Zulu #25821) — CAMPAIGNS, not placements — https://cumulativewebinc.github.io/cwi-learn/scoreboard/scoreboard-chip.json
- Fact spine (Scoreboard Chip): https://cumulativewebinc.github.io/cwi-learn/scoreboard/scoreboard-chip.json
- Rights spine (Compass): https://cumulativewebinc.github.io/cwi-learn/compass/passports.json
- Hub device (Signal Boy): https://cumulativewebinc.github.io/cwi-learn/walkman/
- Gear Ledger (provenance): https://cumulativewebinc.github.io/cwi-learn/agents/ledger.html

Things this kit will NOT assert (UNVERIFIED — the machine-readable proof of restraint):

- Artist bios, quotes, press coverage, published lyrics claims — none on record.
- Play counts for any track other than Zooted Zone; monthly-listener figures; weekly stream-rate figures.
- Growth language of any kind. The display string is exactly '307K plays' — it stands alone.
- Curator claims that failed verification (Flow / No Label Needed, DJ 6Rings / It's Goin) — kept in the Scoreboard Chip anomaly feed, never wins.
- Misspellings of the roster artist's name — the correct spelling is "King Akeem".

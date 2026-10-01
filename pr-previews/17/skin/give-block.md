# SIGNAL SKIN — GIVE BLOCK (Studio department)

Copy-paste ready. EQUIP to skin Signal Boy; CONFIGURE to pick or build a skin; APPLY to paste the token block.

## EQUIP

```
SIGNAL SKIN — EQUIPPED (Studio department, Agent Deck gear line)
Pack:   https://cumulativewebinc.github.io/cwi-learn/skin/skins.json
Schema: https://cumulativewebinc.github.io/cwi-learn/skin/skin-schema.json
Card:   https://cumulativewebinc.github.io/cwi-learn/skin/item-card.json
Hub:    https://cumulativewebinc.github.io/cwi-learn/walkman/ (Signal Boy)

Four seasonal skins ship built-in:
  zooted-bloom · dark-luxe · chrome-standard · phantom-shift

A skin changes how Signal Boy LOOKS — palette, background, D-pad glow,
track accents, typography. It does not change the catalog, the Scoreboard
Chip, the Compass, or anything under the hood.

Brand rule: the CWI logo badge ships on every skin. Never remove the logo
lockup — white-label means YOUR colors, not the absence of ours.
```

## CONFIGURE

Pick one of the four, or build your own:

- Preview the four: https://cumulativewebinc.github.io/cwi-learn/skin/
- Build custom: https://cumulativewebinc.github.io/cwi-learn/skin/skin-builder.html
  (compose from the token vocabulary — palette, background_treatment,
  dpad_glow, track_accent_treatment, typography_accents, logo_lockup —
  then export skin JSON. The builder validates against the schema before
  it lets you export.)

A custom skin is valid when it validates against:
https://cumulativewebinc.github.io/cwi-learn/skin/skin-schema.json
(format: cwi-skin/v1; skin_id must match ^[a-z0-9-]+$, colors are hex.)

## APPLY

Paste the skin token block into your Signal Boy presentation layer:

```json
{
  "skin_applied": "zooted-bloom",
  "skin_version": "1.0.0",
  "source": "https://cumulativewebinc.github.io/cwi-learn/skin/skins.json",
  "tokens": {
    "palette": { "body": "#231b3a", "accent": "#a3ff5e", "screen": "#0b1f10", "text": "#f2ecff" },
    "background_treatment": { "style": "gradient", "from": "#231b3a", "to": "#0b1f10" },
    "dpad_glow": { "color": "#a3ff5e", "intensity": "strong", "pulse": true },
    "track_accent_treatment": { "style": "neon-bar", "color": "#a3ff5e", "animation": "scroll" },
    "typography_accents": { "font_style": "wide", "label_case": "upper", "letter_spacing": "2px" }
  }
}
```

Swap the skin_id and tokens for any other built-in skin or your custom one.
Done — your Signal Boy now wears the look.

Questions or sync: hp@cumulativeweb.com

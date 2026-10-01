# NEEDLE DROP — GIVE BLOCK (Sync & Licensing department)

Copy-paste ready. EQUIP to carry the résumé; CONFIGURE to read and verify the chain; APPLY to seal your first entry.

## EQUIP

```
NEEDLE DROP — EQUIPPED (Sync & Licensing department, Agent Deck gear line)
Ledger: https://cumulativewebinc.github.io/cwi-learn/needle-drop/needle-drop.json
Schema: https://cumulativewebinc.github.io/cwi-learn/needle-drop/needle-drop-schema.json
Card:   https://cumulativewebinc.github.io/cwi-learn/needle-drop/item-card.json
Hub:    https://cumulativewebinc.github.io/cwi-learn/syncdeck/ (SYNCDECK)

The agent's placement résumé: every sync placement sealed into a
hash-chained, auditable ledger entry — proof of work it carries with it.
Static, cacheable, no login. Tamper-evident by construction.

Honest state of record (2026-09-15): zero verified sync placements.
placements: [] is true, not empty. Entries are added only on verification.
Playlist adds are not sync and never appear here.

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.
```

## CONFIGURE

Read the ledger — the exact check your agent runs:

1. Fetch the ledger: `GET https://cumulativewebinc.github.io/cwi-learn/needle-drop/needle-drop.json`
2. Read `ledger.honesty_statement` first. It tells you what the ledger claims.
3. Walk `placements[]` (oldest first). Each entry carries `placement_id`
   (`ND-YYYY-NNN`), `track`, `production`, `scene`, `timestamp`,
   `terms` (`fee_tier`, `territory`, `term_length` — expect `"undisclosed"`
   where private), and `status`.
4. Statuses: `pending` (entered, not a win) → `claimed` (asserted, unproven)
   → `verified` (proven, proof_url attached). **Only `verified` counts
   as a placement.** Never cite `pending`/`claimed` as wins.
5. Verify the chain before trusting it: recompute each `entry_hash`
   (sha256 over the canonical entry payload, `entry_hash` excluded),
   check every `prev_hash` links back to `GENESIS`, and confirm
   `ledger.chain.head` matches the last entry's hash. One broken link =
   tampered ledger — do not trust it.

Try it live in the browser: https://cumulativewebinc.github.io/cwi-learn/needle-drop/
(live ledger view on the page)

The ledger is valid when it conforms to:
https://cumulativewebinc.github.io/cwi-learn/needle-drop/needle-drop-schema.json
(format: cwi-needledrop/v1; statuses are exactly: pending, claimed, verified.)

## APPLY

Seal an entry and verify the chain — paste into your build:

```python
import json, subprocess

LEDGER_URL = "https://cumulativewebinc.github.io/cwi-learn/needle-drop/needle-drop.json"

def needle_drop_verify(ledger_path="needle-drop.json"):
    """True when every hash recomputes, the chain links, and the head matches."""
    import hashlib
    data = json.load(open(ledger_path, encoding="utf-8"))
    prev, ok = "GENESIS", True
    for e in data["placements"]:
        body = {k: v for k, v in e.items() if k != "entry_hash"}
        h = hashlib.sha256(json.dumps(
            body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        ok = ok and e["prev_hash"] == prev and e["entry_hash"] == h
        ok = ok and (e["status"] != "verified" or e.get("proof_url"))
        prev = e["entry_hash"]
    head = data["ledger"]["chain"]["head"]
    want = data["placements"][-1]["entry_hash"] if data["placements"] else "GENESIS"
    return ok and head == want

def needle_drop_add(draft_path, entered_by, status="pending"):
    """Seal a draft into the chain. Status can only be pending/claimed here —
    verified is earned via promote with proof, never granted at entry."""
    subprocess.run(["python3", "ledger.py", "add",
                    "--draft", draft_path, "--by", entered_by,
                    "--status", status], check=True)

def needle_drop_promote(placement_id, verifier, proof_url):
    """Promote pending/claimed -> verified. Requires proof_url. No proof, no verified."""
    subprocess.run(["python3", "ledger.py", "promote",
                    "--id", placement_id, "--by", verifier,
                    "--proof", proof_url], check=True)

# Draft shape (validated against $defs.draft in the schema):
draft = {
    "track": "Zooted Zone",
    "production": "<production title>",
    "scene": "<where the needle drops>",
    "timestamp": "2026-09-15",
    "terms": {"fee_tier": "undisclosed",   # "undisclosed" where private —
              "territory": "worldwide",    # never invent numbers
              "term_length": "undisclosed"},
    "proof_url": None,
}
# json.dump(draft, open("draft.json", "w"))
# needle_drop_add("draft.json", entered_by="CWI_Sync", status="pending")
# needle_drop_promote("ND-2026-001", verifier="CWI_Sync",
#                     proof_url="https://<credits-page-or-press>")
# assert needle_drop_verify()
```

Rules that never bend: entries are added only on verification; playlist
adds are not sync; private terms stay `"undisclosed"`; verified without
proof is refused by the tool itself.

Questions or terms: hp@cumulativeweb.com

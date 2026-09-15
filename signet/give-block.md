# THE SIGNET — GIVE BLOCK (Business Affairs department)

Copy-paste ready. EQUIP to press the signet; CONFIGURE to chain records; APPLY to paste the press-and-verify snippet into your build.

## EQUIP

```
THE SIGNET — EQUIPPED (Business Affairs department, Agent Deck gear line)
Sealer:  https://cumulativewebinc.github.io/cwi-learn/signet/seal.py
Ledger:  https://cumulativewebinc.github.io/cwi-learn/signet/signet.json
Schema:  https://cumulativewebinc.github.io/cwi-learn/signet/signet-schema.json
Card:    https://cumulativewebinc.github.io/cwi-learn/signet/item-card.json
Hub:     https://cumulativewebinc.github.io/cwi-learn/compass/ (Signal Boy)

Press the signet to a rights claim: your name on the line, timestamped,
auditable, hash-ledger-chained. One mutated byte breaks the chain.

Stdlib only (hashlib, json, argparse). Verify offline — no login, no API
key, no per-call cost. "Conditional" claims still escalate to the rights
holder: hp@cumulativeweb.com

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.
```

## CONFIGURE

Press the signet — the exact sequence your agent runs:

1. Open your ledger with the honestly-labeled genesis block:
   `python3 seal.py genesis --agent YOUR_AGENT_NAME > ledger.json`
   (prev_hash is the literal `GENESIS`; its claim says the ledger opens and makes no rights claim.)
2. Seal a claim, chaining onto the previous block's `record_hash`:
   `python3 seal.py seal --agent YOUR_AGENT_NAME --work "Track Title" --claim "the sworn statement" --evidence "source name|2026-09-15;second source|2026-09-15" --prev <record_hash of the last block>`
3. Append the emitted record to your ledger. Every record carries `evidence[]` with `source` + `date` — a claim without evidence does not seal.
4. Ledgers are append-only: never edit a sealed claim. A correction is a NEW sealed record whose claim names the superseded `assertion_id`.

Try it live in the browser: https://cumulativewebinc.github.io/cwi-learn/signet/
(the press-the-signet demo computes the same sha256 chain in your browser)

A record is valid when it conforms to:
https://cumulativewebinc.github.io/cwi-learn/signet/signet-schema.json
(format: cwi-signet/v1; record_hash = sha256(prev_hash + newline + canonical body).)

## APPLY

Paste the press-and-verify block into your build:

```python
import json, subprocess, sys

SEALER = "seal.py"  # https://cumulativewebinc.github.io/cwi-learn/signet/seal.py

def press_signet(agent, work, claim, evidence, prev_hash, ledger_path):
    """Seal a rights claim and append it to the ledger. Returns the record."""
    args = [sys.executable, SEALER, "seal", "--agent", agent, "--work", work,
            "--claim", claim,
            "--evidence", ";".join(f"{s}|{d}" for s, d in evidence),
            "--prev", prev_hash]
    rec = json.loads(subprocess.run(args, check=True, capture_output=True,
                                    text=True).stdout)
    ledger = json.load(open(ledger_path))
    ledger["sample_ledger"]["assertions"].append(rec)
    json.dump(ledger, open(ledger_path, "w"), indent=2)
    return rec

def verify_ledger(ledger_path):
    """Offline verification: recomputes every seal and every link."""
    r = subprocess.run([sys.executable, SEALER, "verify", ledger_path],
                       capture_output=True, text=True)
    print(r.stdout)
    return r.returncode == 0

# Example: an agent swears the Diabolique studio fact, then verifies.
prev = "cd8d4b9904bb061637c10b280dc03bb1da22f7f7b5b4af05fc8600c8fdc13972"
press_verify = press_signet  # press, then:
# verify_ledger("my-ledger.json")  -> "verified N records: CHAIN INTACT"
```

Append-only discipline: a retracted claim gets a NEW sealed record, never an edit.
Mutate one byte in a sealed record and `verify` reports `CHAIN BROKEN` — that's the point.

Brand rule: the CWI logo badge ships on every shipped page. White-label
means YOUR config, not the absence of ours.

Questions or terms: hp@cumulativeweb.com

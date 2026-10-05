# NEEDLE DROP — MCP test brief

For sandbox operators testing NEEDLE DROP as a verification layer. Prepared 2026-09-18.

## What it is

The seal, not the sensor. A hash-chained ledger of verified entries: each entry
carries proof + a named verifier + timestamp. Entries sit at `claimed` until
proof is attached, then promote to `verified`. The chain proves nobody altered
an entry after it was written; it does **not** prove the entry was true when
written — that part is your sandbox's attestation.

## The pieces

1. **Spec** — entry/chain schema, machine-readable:
   https://cumulativewebinc.github.io/cwi-learn/needle-drop/needle-drop-schema.json
2. **MCP server** (public, read-only/verify-only, zero dependencies, stdio):
   https://github.com/CumulativeWebInc/cwi-mcp-server —
   `needledrop_verify` recomputes every entry hash, checks `prev_hash` linkage
   and chain head, and **names the failing `entry_hash` on tamper**.
3. **Trust scoring** (optional) — CWI Verdict Engine v1.0.0: deterministic,
   evidence-bound; thin evidence returns `insufficient-data`, never an invented
   score:
   https://raw.githubusercontent.com/CumulativeWebInc/cwi-learn/needs/verdict-engine/trust/engine.py

## The test (4 steps)

1. Run a real agent task inside your sandbox.
2. Capture tool traces and output artifacts; sha256 each; write NEEDLE DROP
   entries sealing those hashes (`claimed` → `verified` with your proof +
   verifier name).
3. Run `needledrop_verify` over MCP against the ledger. Expect OK.
4. Tamper one entry in a scratch copy; re-run. Expect it to name exactly the
   entry you broke.

## Metrics we want back

- Verify pass/fail on the clean ledger
- Tamper precision: did it name the right `entry_hash`?
- Verify latency (ms) and ledger size (entries)
- % of task effects your sandbox could attest (tool calls, file writes,
  network calls)
- Any false positives or unclear failures

## Honest limits

- Truth-at-write is attested, not cryptographic, without TEE or
  provider-signed receipts.
- `needledrop_verify` is verify-only: no signing, no sealing.
- The ledger ships empty — nothing is pre-seeded.

Questions: reply on the thread or hp@cumulativeweb.com.

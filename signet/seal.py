#!/usr/bin/env python3
"""THE SIGNET — sworn-signing engine for agent rights assertions.

An agent presses its signet to a rights claim: its name on the line,
timestamped, auditable, hash-ledger-chained. If the Compass is the
passport, the Signet is the visa stamp in the agent's own hand.

Canonical serialization (MUST match the browser demo's stableStringify in
template.html): json.dumps(body, sort_keys=True, separators=(",", ":"),
ensure_ascii=False). record_hash = sha256(prev_hash + "\\n" + canonical_body).

CLI:
    python3 seal.py seal --agent NAME --work WORK --claim CLAIM \
        --evidence "source A|2026-09-15;source B|2026-09-15" [--prev PREV_HASH]
    python3 seal.py verify signet.json     # verify a whole ledger file
    python3 seal.py genesis --agent NAME   # emit the honestly-labeled genesis block

White-label: nothing here is CWI-specific. Deploy with your own agent
names and your own evidence; the chain math does not change.
"""
import argparse
import datetime
import hashlib
import json
import sys

FORMAT = "cwi-signet/v1"
GENESIS_PREV = "GENESIS"


def now_iso():
    return (datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0).isoformat().replace("+00:00", "Z"))


def canonical(body):
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def hash_record(prev_hash, body):
    return hashlib.sha256(
        (prev_hash + "\n" + canonical(body)).encode("utf-8")).hexdigest()


def sworn_assertion(agent_name, work, claim, evidence, prev_hash,
                    timestamp=None, assertion_id=None, genesis=False):
    """Build one schema-valid assertion record and seal it."""
    body = {
        "format": FORMAT,
        "assertion_id": assertion_id or "signet-unsigned",
        "agent": agent_name,
        "work": work,
        "claim": claim,
        "evidence": [
            {"source": src.strip(), "date": dt.strip()}
            for src, dt in evidence
        ],
        "timestamp": timestamp or now_iso(),
        "prev_hash": prev_hash,
    }
    record_hash = hash_record(prev_hash, body)
    record = dict(body)
    record["record_hash"] = record_hash
    return record


def genesis_block(agent_name, timestamp=None):
    """The honestly-labeled genesis block: prev_hash is the literal GENESIS
    marker, and the claim says this is the ledger opening — not a rights claim."""
    return sworn_assertion(
        agent_name=agent_name,
        work="(ledger opening)",
        claim=("GENESIS: the Signet assertion ledger opens. Records sealed "
               "after this block are agent-sworn rights assertions; this "
               "block itself is the anchor and makes no rights claim."),
        evidence=[("Cumulative Web Inc — Business Affairs department",
                   "2026-09-15")],
        prev_hash=GENESIS_PREV,
        timestamp=timestamp or now_iso(),
        assertion_id="signet-genesis",
        genesis=True,
    )


def verify_record(record):
    """Recompute and compare. Returns (ok, reason)."""
    expected = record.get("record_hash")
    body = {k: v for k, v in record.items() if k != "record_hash"}
    got = hash_record(record.get("prev_hash", ""), body)
    if got != expected:
        return False, (f"record_hash mismatch for {record.get('assertion_id')}: "
                       f"expected {expected[:16]}..., recomputed {got[:16]}...")
    return True, "seal intact"


def verify_chain(records):
    """Check every seal AND every link. Returns (ok, reasons[])."""
    reasons, prev = [], GENESIS_PREV
    for rec in records:
        ok, reason = verify_record(rec)
        if not ok:
            reasons.append(reason)
        if rec.get("prev_hash") != prev:
            reasons.append(f"chain break at {rec.get('assertion_id')}: "
                           f"prev_hash does not match prior record_hash")
        prev = rec.get("record_hash")
    return (len(reasons) == 0), reasons


def _parse_evidence(spec):
    pairs = []
    for chunk in (spec or "").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "|" not in chunk:
            raise ValueError(f"evidence entry needs 'source|date': {chunk!r}")
        src, dt = chunk.split("|", 1)
        pairs.append((src, dt))
    return pairs


def main(argv=None):
    ap = argparse.ArgumentParser(prog="seal.py",
                                 description="THE SIGNET sworn-signing engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seal", help="press the signet to a rights claim")
    s.add_argument("--agent", required=True)
    s.add_argument("--work", required=True, help="the track / work asserted about")
    s.add_argument("--claim", required=True)
    s.add_argument("--evidence", default="",
                   help="'source|YYYY-MM-DD;source2|YYYY-MM-DD'")
    s.add_argument("--prev", default=GENESIS_PREV,
                   help="prev_hash to chain onto (default: GENESIS)")
    s.add_argument("--id", default=None, dest="assertion_id")
    s.add_argument("--timestamp", default=None)

    g = sub.add_parser("genesis", help="emit the honestly-labeled genesis block")
    g.add_argument("--agent", required=True)
    g.add_argument("--timestamp", default=None)

    v = sub.add_parser("verify", help="verify a ledger file's seals and links")
    v.add_argument("file", help="JSON ledger: {'assertions':[...]} or bare list")

    args = ap.parse_args(argv)
    if args.cmd == "seal":
        rec = sworn_assertion(args.agent, args.work, args.claim,
                              _parse_evidence(args.evidence), args.prev,
                              timestamp=args.timestamp,
                              assertion_id=args.assertion_id)
        print(json.dumps(rec, indent=2, ensure_ascii=False))
    elif args.cmd == "genesis":
        print(json.dumps(genesis_block(args.agent,
                                       timestamp=args.timestamp),
                         indent=2, ensure_ascii=False))
    elif args.cmd == "verify":
        data = json.load(open(args.file))
        records = data.get("assertions", data) if isinstance(data, dict) else data
        ok, reasons = verify_chain(records)
        for r in reasons:
            print("FAIL:", r)
        print(f"verified {len(records)} records: "
              f"{'CHAIN INTACT' if ok else 'CHAIN BROKEN'}")
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

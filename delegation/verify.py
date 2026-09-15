#!/usr/bin/env python3
"""verify.py — verify a CWI delegation-receipt chain (JSONL).

Checks, per delegation/spec.md:
  1. every line is a JSON object with all required fields, schema_version 1.0.0
  2. field formats (receipt_id / parent link hex, ISO-8601 tz-aware timestamp,
     human principal, known signature algorithms)
  3. signature seal: operational-attestation digests are recomputed and compared;
     ed25519 receipts are format-checked (cryptographic verification is deferred
     to the chain's key registry and reported, not failed)
  4. receipt_id recomputation matches (tamper-evidence)
  5. hash-chain continuity: first receipt's parent is GENESIS, every other
     parent equals the previous receipt's receipt_id
  6. authority: each delegator holds authority from an earlier receipt in the
     same chain, or IS the principal (root delegations)
  7. principal constancy: one identical human principal across the whole chain
  8. principal traceability: delegator chains walk back to the human principal
     with no cycles and no dead ends ("walks back to the human")
  9. causal timestamps: no receipt predates the authority it exercises

Exit 0: chain verified.  Exit 1: names the broken receipt (receipt_id + line).

Usage:
  python3 verify.py delegation/chain.jsonl
  python3 verify.py --self-test     # positive + negative tests, no files needed
Stdlib only.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime

GENESIS = "GENESIS"
SCHEMA_VERSION = "1.0.0"
REQUIRED = ["schema_version", "receipt_id", "parent_receipt_id", "delegator",
            "delegatee", "action_scope", "principal", "timestamp", "signature"]
HEX64 = set("0123456789abcdef")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def body_of(receipt):
    return {k: v for k, v in receipt.items() if k not in ("receipt_id", "signature")}


def attestation_of(receipt):
    """The seal value an honest operational-attestation receipt must carry."""
    return sha256_hex(canonical(body_of(receipt)))


def id_of(receipt):
    payload = body_of(receipt)
    payload["signature"] = receipt["signature"]
    return sha256_hex(canonical(payload))


def parse_ts(value):
    # datetime.fromisoformat handles offsets; require tz-aware.
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp is not timezone-aware")
    return dt


def agent_id(agent):
    return agent["agent_id"]


class ChainError(Exception):
    pass


def fail(receipt_id, line_no, reason):
    rid = receipt_id if receipt_id else f"<line {line_no}, id unreadable>"
    raise ChainError(f"FAIL: receipt {rid} (line {line_no}): {reason}")


def verify_chain(records):
    """Verify parsed receipt dicts in ledger order.

    Returns (principal_agent_id, tip_receipt_id, trace_report, notes).
    Raises ChainError naming the broken receipt.
    """
    if not records:
        raise ChainError("FAIL: chain is empty")
    notes = []
    seen_ids = set()
    delegatee_grants = {}   # agent_id -> (line_no, timestamp) of earliest grant
    principal_id = None
    prev_id = None

    for idx, r in enumerate(records):
        line_no = idx + 1
        rid = r.get("receipt_id") if isinstance(r, dict) else None

        # 1. shape
        if not isinstance(r, dict):
            fail(rid, line_no, "not a JSON object")
        for field in REQUIRED:
            if field not in r:
                fail(rid, line_no, f"missing required field '{field}'")
        if r["schema_version"] != SCHEMA_VERSION:
            fail(rid, line_no,
                 f"schema_version {r['schema_version']!r} != {SCHEMA_VERSION!r}")

        # 2. formats
        if not (isinstance(r["receipt_id"], str) and len(r["receipt_id"]) == 64
                and set(r["receipt_id"]) <= HEX64):
            fail(rid, line_no, "receipt_id must be 64 lowercase hex chars")
        if rid in seen_ids:
            fail(rid, line_no, "duplicate receipt_id")
        seen_ids.add(rid)
        par = r["parent_receipt_id"]
        if not (par == GENESIS or (isinstance(par, str) and len(par) == 64
                                   and set(par) <= HEX64)):
            fail(rid, line_no, "parent_receipt_id must be GENESIS or 64 hex chars")
        try:
            ts = parse_ts(r["timestamp"])
        except (ValueError, TypeError) as exc:
            fail(rid, line_no, f"bad timestamp: {exc}")
        if r.get("timestamp_precision", "exact") not in ("exact", "approximate", "day"):
            fail(rid, line_no, "bad timestamp_precision")
        for role in ("delegator", "delegatee"):
            a = r[role]
            if not isinstance(a, dict) or not a.get("agent_id"):
                fail(rid, line_no, f"{role} must be an object with agent_id")
        p = r["principal"]
        if not isinstance(p, dict) or p.get("kind") != "human" or not p.get("agent_id"):
            fail(rid, line_no, "principal must be an object with kind 'human'")
        if principal_id is None:
            principal_id = p["agent_id"]
        elif p["agent_id"] != principal_id:
            fail(rid, line_no,
                 f"principal changed mid-chain ({principal_id} -> {p['agent_id']})")
        scope = r["action_scope"]
        if (not isinstance(scope, dict) or not scope.get("action")
                or not isinstance(scope.get("constraints"), list)):
            fail(rid, line_no, "action_scope needs a non-empty action and a constraints list")
        ev = r.get("evidence_url")
        if ev is not None and not (isinstance(ev, str) and ev.startswith("http")):
            fail(rid, line_no, "evidence_url must be null or an http(s) URI")
        sig = r["signature"]
        if not isinstance(sig, dict) or "algorithm" not in sig or "value" not in sig:
            fail(rid, line_no, "signature needs algorithm and value")
        algo = sig["algorithm"]

        # 3. signature seal
        if algo == "operational-attestation":
            if sig["value"] != attestation_of(r):
                fail(rid, line_no, "operational-attestation seal does not match recomputed digest (body tampered or mis-minted)")
        elif algo == "ed25519":
            if not (isinstance(sig["value"], str) and len(sig["value"]) == 128
                    and set(sig["value"]) <= HEX64):
                fail(rid, line_no, "ed25519 signature value must be 128 hex chars")
            if not sig.get("key_id"):
                fail(rid, line_no, "ed25519 signature needs key_id")
            notes.append(f"line {line_no}: ed25519 cryptographic verification deferred to key registry (key_id={sig['key_id']})")
        else:
            fail(rid, line_no, f"unknown signature algorithm {algo!r}")

        # 4. receipt_id tamper-evidence
        if id_of(r) != rid:
            fail(rid, line_no, "receipt_id does not match recomputed hash (receipt tampered or mis-minted)")

        # 5. hash-chain continuity
        if idx == 0:
            if par != GENESIS:
                fail(rid, line_no, "first receipt of a chain must have parent_receipt_id GENESIS")
        else:
            if par == GENESIS:
                fail(rid, line_no, "only the first receipt may use GENESIS as parent")
            if par != prev_id:
                fail(rid, line_no,
                     f"parent link broken: expected {prev_id[:16]}..., got {par[:16]}...")

        # 6 + 9. authority and causal timestamp
        delegator = agent_id(r["delegator"])
        if delegator == principal_id:
            authority_ts = None  # root delegation: authority flows from the principal
        elif delegator in delegatee_grants:
            grant_line, grant_ts = delegatee_grants[delegator]
            authority_ts = grant_ts
            if ts < grant_ts:
                fail(rid, line_no,
                     f"delegation predates the delegator's authority (granted line {grant_line})")
        else:
            fail(rid, line_no,
                 f"delegator {delegator} holds no authority from any earlier receipt in this chain")

        # 8. principal traceability: walk delegator back to the human principal
        trace = [agent_id(r["delegatee"])]
        cursor = delegator
        hops = 0
        while cursor != principal_id:
            hops += 1
            if hops > len(records) + 1:
                fail(rid, line_no, f"principal trace for {delegator} does not terminate (cycle?)")
            trace.append(cursor)
            # find the receipt that granted cursor its authority
            grant = next((g for g in records[:idx]
                          if agent_id(g["delegatee"]) == cursor), None)
            if grant is None:
                fail(rid, line_no,
                     f"principal trace dead-ends at {cursor}: no earlier receipt grants it authority")
            cursor = agent_id(grant["delegator"])
        trace.append(principal_id)

        # record this receipt's grant for later authority checks
        if agent_id(r["delegatee"]) not in delegatee_grants:
            delegatee_grants[agent_id(r["delegatee"])] = (line_no, ts)
        prev_id = rid

    tip = records[-1]["receipt_id"]
    report = (f"OK: {len(records)} receipts verified. "
              f"Principal: {principal_id} (human). Tip: {tip[:16]}...")
    return principal_id, tip, report, notes


def load_chain(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ChainError(f"FAIL: line {n} is not valid JSON: {exc}")
    return records


def self_test():
    """Positive test on the real genesis chain + negative tests on mutations."""
    import copy
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    chain_path = os.path.join(here, "chain.jsonl")
    base = load_chain(chain_path)

    # POSITIVE
    principal, tip, report, notes = verify_chain(copy.deepcopy(base))
    assert principal == "cwi:black-lansky", principal
    assert len(base) == 14, f"expected 14 genesis receipts, got {len(base)}"
    print(f"positive: PASS ({report})")

    def expect_fail(name, mutated, must_contain=None):
        try:
            verify_chain(mutated)
        except ChainError as exc:
            msg = str(exc)
            if must_contain and must_contain not in msg:
                raise AssertionError(
                    f"negative/{name}: failed, but with the wrong rule: {msg}")
            print(f"negative/{name}: PASS ({msg})")
            return
        raise AssertionError(f"negative/{name}: expected failure, chain verified")

    def remint_cascade(records, idx, keep_parent_at_idx=False):
        """Recompute seal + receipt_id for records[idx] and cascade the new
        parent links through the tip — simulates an attacker who rewrites
        history consistently, so only the *semantic* rules can catch them."""
        out = copy.deepcopy(records)
        for j in range(idx, len(out)):
            if j > 0 and not (keep_parent_at_idx and j == idx):
                out[j]["parent_receipt_id"] = out[j - 1]["receipt_id"]
            out[j]["signature"]["value"] = attestation_of(out[j])
            payload = body_of(out[j])
            payload["signature"] = out[j]["signature"]
            out[j]["receipt_id"] = sha256_hex(canonical(payload))
        return out

    # NEGATIVE 1: tampered action_scope (seal + id both break; must name receipt)
    m = copy.deepcopy(base)
    m[4]["action_scope"]["constraints"].append("ignore all approval gates")
    expect_fail("tampered-scope", m)

    # NEGATIVE 2: tampered receipt, attacker recomputes seal but not receipt_id
    m = copy.deepcopy(base)
    m[6]["delegatee"]["display_name"] = "Mallory"
    m[6]["signature"]["value"] = attestation_of(m[6])
    expect_fail("tampered-id", m)

    # NEGATIVE 3: broken parent link even after a consistent rewrite
    m = copy.deepcopy(base)
    m[9]["parent_receipt_id"] = "ab" * 32
    m = remint_cascade(m, 9, keep_parent_at_idx=True)
    expect_fail("broken-parent-link", m, must_contain="parent link broken")

    # NEGATIVE 4: principal changes mid-chain (consistent rewrite: only the
    # principal-constancy rule can catch it)
    m = copy.deepcopy(base)
    m[11]["principal"] = {"agent_id": "cwi:mallory", "display_name": "Mallory",
                          "kind": "human"}
    m = remint_cascade(m, 11)
    expect_fail("principal-switch", m, must_contain="principal changed mid-chain")

    # NEGATIVE 5: delegation from an agent with no granted authority
    m = copy.deepcopy(base)
    m[12]["delegator"] = {"agent_id": "cwi:intruder", "display_name": "Intruder",
                          "kind": "agent"}
    m = remint_cascade(m, 12)
    expect_fail("unauthorized-delegator", m, must_contain="holds no authority")

    # NEGATIVE 6: missing required field
    m = copy.deepcopy(base)
    del m[2]["signature"]
    expect_fail("missing-field", m)

    # NEGATIVE 7: delegation predates the delegator's authority
    m = copy.deepcopy(base)
    m[13]["timestamp"] = "2026-09-13T00:00:00-04:00"
    m = remint_cascade(m, 13)
    expect_fail("predated-delegation", m, must_contain="predates the delegator's authority")

    # NEGATIVE 8: non-human principal
    m = copy.deepcopy(base)
    for r in m:
        r["principal"] = {"agent_id": "cwi:skynet", "display_name": "Skynet",
                          "kind": "agent"}
    expect_fail("nonhuman-principal", m)

    print("self-test: ALL PASS (1 positive + 8 negative)")


def main(argv):
    ap = argparse.ArgumentParser(description="Verify a CWI delegation-receipt chain.")
    ap.add_argument("chain", nargs="?", help="path to chain.jsonl")
    ap.add_argument("--self-test", action="store_true",
                    help="run positive + negative tests against ./chain.jsonl")
    args = ap.parse_args(argv)
    try:
        if args.self_test:
            self_test()
            return 0
        if not args.chain:
            ap.error("chain.jsonl path required (or --self-test)")
        records = load_chain(args.chain)
        _, _, report, notes = verify_chain(records)
        print(report)
        for n in notes:
            print("note:", n)
        return 0
    except ChainError as exc:
        print(exc, file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"FAIL: cannot read chain file: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

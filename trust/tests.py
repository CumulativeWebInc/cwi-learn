#!/usr/bin/env python3
"""Tests for the CWI Verdict Engine v1.0.0 (trust/engine.py).

- determinism: same input run twice -> byte-identical stdout
- cold start: empty inputs -> insufficient-data, never a number
- tamper: flipping verified->claimed changes the outcome and the input hash
- scoring path (SYNTHETIC test-only data, clearly labeled): gate math, bands,
  Sybil damping all behave per spec
- refusals: disputed evidence, unknown context, invalid input

Run: python3 tests.py
Exit 0 = all pass.
"""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / "engine.py"

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ((" — " + detail) if detail and not cond else ""))


def run_engine(doc):
    blob = json.dumps(doc, sort_keys=True).encode()
    p1 = subprocess.run([sys.executable, str(ENGINE)], input=blob,
                        capture_output=True)
    p2 = subprocess.run([sys.executable, str(ENGINE)], input=blob,
                        capture_output=True)
    return p1, p2


def base_input(**over):
    doc = {
        "engine_version": "1.0.0",
        "subject": {"agent_id": "TEST_SUBJECT", "display_name": "Test Subject"},
        "context": "agent-trust",
        "observed_at": "2026-09-15T00:00:00Z",
        "signals": {"erc8004": [], "needle_drop": [], "first_spin": []},
    }
    doc.update(over)
    return doc


def ev(eid, issuer="witness", wclass=2, status="verified", itype="third_party",
       cluster=None):
    return {
        "evidence_id": eid,
        "kind": "test-evidence",
        "issuer": issuer,
        "identity_cluster": cluster,
        "issuer_type": itype,
        "description": "SYNTHETIC test evidence — not real.",
        "status": status,
        "observed_at": "2026-09-15",
        "source_url": None,
        "source_ref": "tests.py synthetic",
        "weight_class": wclass,
    }


# --- 1. determinism ---------------------------------------------------------
doc = base_input()
doc["signals"]["erc8004"] = [ev("e1"), ev("e2", issuer="other")]
p1, p2 = run_engine(doc)
check("determinism: byte-identical reruns",
      p1.returncode == 0 and p2.returncode == 0 and p1.stdout == p2.stdout)
o1 = json.loads(p1.stdout)
check("determinism: output parses as JSON", isinstance(o1, dict))

# --- 2. cold start ----------------------------------------------------------
p1, _ = run_engine(base_input())
o = json.loads(p1.stdout)
check("cold-start: empty inputs -> insufficient-data",
      o["status"] == "insufficient-data", json.dumps(o)[:200])
check("cold-start: score is null, never a number", o["score"] is None)
check("cold-start: band is null", o["band"] is None)
check("cold-start: missing explains the gap",
      isinstance(o["missing"], list) and len(o["missing"]) > 0)
check("cold-start: exit code 0 (clean refusal)", p1.returncode == 0)

# cold start with only claimed/pending evidence (0 verified)
doc = base_input()
doc["signals"]["erc8004"] = [ev("c1", status="claimed"), ev("c2", status="pending")]
o = json.loads(run_engine(doc)[0].stdout)
check("cold-start: claimed/pending evidence counts as zero",
      o["status"] == "insufficient-data" and o["score"] is None)

# --- 3. tamper --------------------------------------------------------------
good = base_input()
good["signals"]["erc8004"] = [ev("t1", wclass=3), ev("t2", wclass=3), ev("t3", wclass=2)]
good["signals"]["needle_drop"] = [ev("t4", wclass=3)]
good["signals"]["first_spin"] = [ev("t5", wclass=2)]
o_good = json.loads(run_engine(good)[0].stdout)
check("tamper-setup: synthetic passing input scores",
      o_good["status"] == "scored" and isinstance(o_good["score"], float),
      json.dumps(o_good)[:200])

bad = json.loads(json.dumps(good))  # deep copy
bad["signals"]["needle_drop"][0]["status"] = "claimed"  # tamper one item
p_bad, _ = run_engine(bad)
o_bad = json.loads(p_bad.stdout)
check("tamper: flipped evidence changes outcome",
      o_bad["input_sha256"] != o_good["input_sha256"]
      and (o_bad["status"] != "scored" or o_bad["score"] != o_good["score"]),
      "sha changed=%s status=%s" % (o_bad["input_sha256"] != o_good["input_sha256"],
                                     o_bad["status"]))

# --- 4. scoring path: gate math, bands, Sybil damping (synthetic) -----------
# NOTE: t1..t3 share one issuer, so the D1 issuer cap (2/family) keeps only
# the two class-3 items: kept = 3+3 = 6 -> family_score = 6/9.
check("scoring: family math kept/(kept+3), issuer cap applied",
      abs(o_good["families"]["erc8004"]["family_score"] - 6 / 9) < 1e-9
      and o_good["families"]["erc8004"]["kept_count"] == 2
      and len(o_good["families"]["erc8004"]["damped"]) == 1,
      "kept=3+3=6 -> 6/9; t3 damped by issuer-cap")
check("scoring: overall is mean of scored families",
      abs(o_good["score"] - round(((6 / 9) + (3 / 6) + (2 / 5)) / 3, 3)) < 1e-9)
check("scoring: band label applied", o_good["band"] in
      ("established", "emerging", "thin", "weak", "negligible"))

# Sybil: 3 items from one issuer, cap is 2 -> one damped
sybil = base_input()
sybil["signals"]["erc8004"] = [ev("s1", issuer="sock", wclass=3),
                               ev("s2", issuer="sock", wclass=3),
                               ev("s3", issuer="sock", wclass=3)]
sybil["signals"]["needle_drop"] = [ev("s4", wclass=3)]
sybil["signals"]["first_spin"] = [ev("s5", wclass=3)]
o_s = json.loads(run_engine(sybil)[0].stdout)
fam = o_s["families"]["erc8004"]
check("sybil: issuer cap damps surplus items",
      fam["kept_count"] == 2 and len(fam["damped"]) == 1
      and fam["damped"][0]["reason"] == "issuer-cap")

# Sybil via identity cluster: two issuers, one controller -> one issuer
cl = base_input()
cl["signals"]["erc8004"] = [ev("k1", issuer="wallet-a", wclass=3, cluster="human-x"),
                            ev("k2", issuer="wallet-b", wclass=3, cluster="human-x"),
                            ev("k3", issuer="wallet-c", wclass=3, cluster="human-x")]
cl["signals"]["needle_drop"] = [ev("k4", wclass=3)]
cl["signals"]["first_spin"] = [ev("k5", wclass=3)]
o_c = json.loads(run_engine(cl)[0].stdout)
check("sybil: identity cluster merges sock-puppet issuers",
      o_c["families"]["erc8004"]["kept_count"] == 2
      and len(o_c["families"]["erc8004"]["damped"]) == 1)

# Self-assertion discount: 0.5x
slf = base_input()
slf["signals"]["erc8004"] = [ev("m1", wclass=2, itype="self")]
slf["signals"]["needle_drop"] = [ev("m2", wclass=3)]
slf["signals"]["first_spin"] = [ev("m3", wclass=3)]
o_m = json.loads(run_engine(slf)[0].stdout)
check("sybil: self-asserted evidence discounted 0.5x",
      abs(o_m["families"]["erc8004"]["kept_weight"] - 1.0) < 1e-9)

# --- 5. refusals ------------------------------------------------------------
dsp = base_input()
dsp["signals"]["erc8004"] = [ev("d1"), ev("d2"), ev("d3", status="disputed")]
o_d = json.loads(run_engine(dsp)[0].stdout)
check("refusal: disputed evidence -> evidence-disputed, no score",
      o_d["status"] == "evidence-disputed" and o_d["score"] is None)

unk = base_input(context="vibes")
p_u, _ = run_engine(unk)
o_u = json.loads(p_u.stdout)
check("refusal: unknown context -> unknown-context",
      o_u["status"] == "unknown-context" and o_u["score"] is None)

inv = base_input()
inv["signals"]["erc8004"] = [{"evidence_id": "x"}]  # schema violation
p_i, _ = run_engine(inv)
o_i = json.loads(p_i.stdout)
check("refusal: invalid input -> invalid-input, exit 2",
      o_i["status"] == "invalid-input" and p_i.returncode == 2
      and o_i["score"] is None)

ver = base_input()
ver["engine_version"] = "9.9.9"
o_v = json.loads(run_engine(ver)[0].stdout)
check("refusal: version mismatch -> invalid-input",
      o_v["status"] == "invalid-input")

# --- 6. sample-scores.json integrity ----------------------------------------
samp = HERE / "sample-scores.json"
try:
    data = json.loads(samp.read_text(encoding="utf-8"))
    entries = data["subjects"]
    ok = True
    for entry in entries:
        out = entry["output"]
        # re-run the engine on the embedded input snapshot; must match exactly
        p, _ = run_engine(entry["input"])
        if json.loads(p.stdout) != out:
            ok = False
            break
        # truth rule: no entry may carry a numeric score without verified evidence
        if out["score"] is not None and out["status"] != "scored":
            ok = False
            break
    check("sample-scores.json: every output reproduces from its input snapshot", ok)
    check("sample-scores.json: all entries carry input snapshots",
          all("input" in e and "output" in e for e in entries))
except (OSError, KeyError, json.JSONDecodeError) as exc:
    check("sample-scores.json: readable and well-formed", False, str(exc))

print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
sys.exit(1 if FAIL else 0)

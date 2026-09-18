#!/usr/bin/env python3
"""Build trust/sample-scores.json by running engine.py on REAL inputs only.

Every subject below uses genuine evidence CWI holds as of 2026-09-15.
First Spin: no published production verdicts exist (first-spin/sample-verdict.json
is a labeled worked example — excluded per spec 2.3), so those inputs are
honestly empty. Needle Drop: ledger verified empty. ERC-8004: only the
MUSE_CWI Moltbook claim is verified; the 8 department registrations are
pending claim (status: claimed -> contributes 0).

Expected result: every (subject, context) pair -> insufficient-data.
A trust engine that invents scores is worse than none.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / "engine.py"
CONTEXTS = ("agent-trust", "music-review", "payments")


def ev(eid, kind, issuer, itype, description, status, observed_at,
       source_url, source_ref, wclass, cluster=None):
    return {
        "evidence_id": eid,
        "kind": kind,
        "issuer": issuer,
        "identity_cluster": cluster,
        "issuer_type": itype,
        "description": description,
        "status": status,
        "observed_at": observed_at,
        "source_url": source_url,
        "source_ref": source_ref,
        "weight_class": wclass,
    }


KINGCODE_IDENTITY = ev(
    "e8004-moltbook-claim-20260915",
    "protocol-registration-claim",
    "moltbook", "third_party",
    "MUSE_CWI (KingCode) Moltbook account claimed 2026-09-15: email verified, "
    "profile description leads with KingCode. The 8 department agents are "
    "registered but unclaimed (one-AI-agent-per-human policy wall).",
    "verified", "2026-09-15", None,
    "CWI agent watchlist + Moltbook heartbeat logs, 2026-09-15", 2)

PENDING_CLAIM = ev(
    "e8004-moltbook-registration-pending",
    "protocol-registration-claim",
    "moltbook", "third_party",
    "Department agent Moltbook account registered; claim pending — Black's "
    "email is tied to KingCode, so department claim links fail as a policy "
    "wall, not a bug. Registration is real; the claim is not complete.",
    "claimed", "2026-09-15", None,
    "Moltbook claim decision log, 2026-09-15", 1)

NEEDLE_DROP_EMPTY = ("needle-drop/needle-drop.json ledger ships with "
                     "placements: [] — verified empty as of 2026-09-15. "
                     "Playlist adds are not sync placements and never appear "
                     "here; unverified curator claims are not logged.")
FIRST_SPIN_EMPTY = ("No published production First Spin verdicts as of "
                    "2026-09-15. first-spin/sample-verdict.json exists but is "
                    "labeled a worked example — demo data, excluded per "
                    "spec 2.3.")

SUBJECTS = [
    {
        "agent_id": "MUSE_CWI",
        "display_name": "KingCode — CWI chief agent",
        "signals": {
            "erc8004": [KINGCODE_IDENTITY],
            "needle_drop": [],
            "first_spin": [],
        },
        "evidence_notes": {
            "needle_drop": NEEDLE_DROP_EMPTY,
            "first_spin": FIRST_SPIN_EMPTY,
        },
    },
    {
        "agent_id": "CWI_Data",
        "display_name": "CWI Data & Analytics department agent",
        "signals": {
            "erc8004": [PENDING_CLAIM],
            "needle_drop": [],
            "first_spin": [],
        },
        "evidence_notes": {
            "erc8004": ("Registration real, claim incomplete (status: claimed) — "
                        "contributes 0 to the score."),
            "needle_drop": NEEDLE_DROP_EMPTY,
            "first_spin": FIRST_SPIN_EMPTY,
        },
    },
    {
        "agent_id": "CWI_AandR",
        "display_name": "CWI A&R department agent",
        "signals": {
            "erc8004": [json.loads(json.dumps(PENDING_CLAIM))],
            "needle_drop": [],
            "first_spin": [],
        },
        "evidence_notes": {
            "erc8004": ("Registration real, claim incomplete (status: claimed) — "
                        "contributes 0 to the score."),
            "needle_drop": NEEDLE_DROP_EMPTY,
            "first_spin": ("The worked example in first-spin/sample-verdict.json "
                           "was evaluated by the CWI A&R department, but it is "
                           "labeled a worked example — not a published production "
                           "verdict — so this input is honestly empty per spec 2.3."),
        },
    },
]


def main():
    entries = []
    for subj in SUBJECTS:
        for context in CONTEXTS:
            doc = {
                "engine_version": "1.0.0",
                "subject": {"agent_id": subj["agent_id"],
                            "display_name": subj["display_name"]},
                "context": context,
                "observed_at": "2026-09-15T19:30:00Z",
                "signals": subj["signals"],
                "evidence_notes": subj["evidence_notes"],
            }
            p = subprocess.run([sys.executable, str(ENGINE)],
                               input=json.dumps(doc).encode(),
                               capture_output=True)
            if p.returncode not in (0,):
                sys.stderr.write("engine failed for %s/%s: %s\n"
                                 % (subj["agent_id"], context, p.stderr.decode()))
                return 1
            entries.append({"input": doc, "output": json.loads(p.stdout)})
    bundle = {
        "engine": "cwi-verdict-engine",
        "engine_version": "1.0.0",
        "spec_version": "1.0.0",
        "generated": "2026-09-15",
        "honesty_statement": (
            "Every input below is real evidence CWI holds as of 2026-09-15. "
            "No scores are invented: where the context gate is not met the "
            "engine returns insufficient-data with a null score. Each output "
            "was produced by running trust/engine.py on the embedded input "
            "snapshot; rerun to verify byte-identical results."),
        "subjects": entries,
    }
    out_path = HERE / "sample-scores.json"
    out_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print("wrote %s (%d subject-context pairs)" % (out_path, len(entries)))
    for e in entries:
        o = e["output"]
        print("  %s / %-12s -> %s (score=%s)" % (
            e["input"]["subject"]["agent_id"], e["input"]["context"],
            o["status"], o["score"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

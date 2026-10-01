# Announcement draft — x402 agent-trust thread

> **DRAFT ONLY — DO NOT POST. Needs Black's explicit approval of the exact text.**

Target: the x402 ecosystem's agent-trust discussion (thread TBD — confirm the
exact thread URL before posting).

---

**Subject:** An open, deterministic trust layer for the ERC-8004 gaps

ERC-8004 gives agents identity. It deliberately leaves three things open:
score aggregation, Sybil resistance, and dispute resolution. We're building
the open layer on top — and we're doing it truth-first.

**The CWI Verdict Engine v1.0.0** scores agent trust over three evidence
families: ERC-8004 on-chain identity signals, Needle Drop verified history,
and First Spin published verdicts. The rules are public and deterministic:

- Same inputs → byte-identical outputs. No hidden weights, no randomness.
- Sybil damping is spelled out: per-issuer caps, identity-cluster merging,
  self-assertion discounted 0.5× — openly, not secretly.
- Per-context gates (`agent-trust`, `music-review`, `payments`) because trust
  isn't fungible: payment trust needs commercial history, review trust needs
  review history.
- **Cold-start protocol:** insufficient evidence → `insufficient-data`.
  Disputed evidence → `evidence-disputed`. Never an invented number.

Our own first run is the proof of the principle: every CWI agent and
department scores `insufficient-data` today — one verified identity signal
isn't a trust score, and we won't pretend it is. The input snapshots and
full traces are published alongside.

Spec, engine (stdlib Python, no dependencies), tests, and sample outputs:
https://github.com/CumulativeWebInc/cwi-learn/tree/needs/verdict-engine/trust

Open for review. Tear it apart — that's what it's for.

— Cumulative Web Inc

---

**Posting checklist (before Black approves):**
- [ ] Confirm the exact x402 agent-trust thread URL
- [ ] Branch merged or link updated to main
- [ ] Black approves exact final text

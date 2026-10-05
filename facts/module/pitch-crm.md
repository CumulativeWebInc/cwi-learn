# Visibility Machine — Pitch CRM (Module 4)

**Packet:** `fact/module/pitch-crm` · **Type:** module · **Status:** verified
**Canonical:** https://cumulativewebinc.github.io/cwi-learn/facts/module/pitch-crm.json

## Facts
- [verified] 29-curator queue computed as of 2026-10-03: 0 due followups; 14 drafts inventoried, all gated 'staged' — visibility-machine/modules/pitch-crm/output/pitch-queue-2026-10-03.json
- [observed] Reply rate 1.0 from verified history: 5 pitches -> 5 replied/placed (kill rule armed: <5% after 20 pitches -> rewrite angles) — cwi-company/radio/curator-crm.jsonl
- [owner_confirmed] Black killed the Audiartist lane 2026-10-03 ('i am not paying for audioaritst'): follow-up draft PARKED, no send, no paid route until he reopens it; holdings on New Rap Hits stand as-is — MEMORY.md 2026-10-03
- [verified] Exact-copy gate: draft staged->approved only with {approver, approved_at, exact_text_sha256}; send log empty until a real send happens — visibility-machine/modules/pitch-crm/queue.py

## Tags
- `outreach-ops` (domain): follow-up queue computed from CRM history dates [verified]
- `exact-copy-gate` (role): gate enforced in code, not in hope [verified]
- `followup-queue` (use): 2-nudge rule then park 90 days [verified]

## Voice answer

The CWI Visibility Machine Pitch CRM (Module 4): Working pitch queue: follow-up scheduling per the 2-nudge/park-90-days rule, draft inventory with the exact-copy gate enforced in code, reply-rate tracking. Nothing sends under Black's name without his exact-text approval. Source: Cumulative Web Inc.

## Citation

https://cumulativewebinc.github.io/cwi-learn/facts/module/pitch-crm.json

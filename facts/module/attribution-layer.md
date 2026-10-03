# Visibility Machine — Attribution Layer (Module 1)

**Packet:** `fact/module/attribution-layer` · **Type:** module · **Status:** verified
**Canonical:** https://cumulativewebinc.github.io/cwi-learn/facts/module/attribution-layer.json

## Facts
- [verified] attribute.py verifies the live vote-HQ ?src= wire end-to-end: 5 inbound share values (x/fb/wa/tg/copy) + cwi-votehq outbound, page HTTP 200, zero drift on 2026-10-03 — visibility-machine/modules/attribution/output/attribution-scorecard-2026-10-03.json
- [observed] Manual tally baseline 38-2-2 (Diabolique vs runner-up vs 3rd) parsed programmatically from tally-sheet.md, observed 2026-10-03 ~06:30 EDT — cwi-company/flywheel/front3/vote-hq-attribution/tally-sheet.md
- [observed] Icecast log-shipper ledger ingested: 6 sessions (unique Icecast sessions, IP+UA heuristic, unverified), 11 requests_200, shipped 2026-10-02T13:31Z — cwi-company/radio/log-shipper/shipped-aggregates.jsonl
- [observed] Click-beacon Worker not shipped: hq_visit/share_click/vote_click unmeasured; share-variant kill rule ARMED_NOT_MEASURABLE; next cycle ships the Worker — visibility-machine/modules/attribution/output/attribution-scorecard-2026-10-03.json

## Tags
- `attribution` (domain): module wires every touchpoint to a measurable event [verified]
- `measurement` (use): live HTTP checks + tally parsing + ledger ingestion in one CLI [verified]
- `kill-rules` (role): share-variant retire, now-playing staleness, ?src= drift [verified]
- `src-wire` (proof): page wire matches the locked registry, verified live [verified]

## Voice answer

The CWI Visibility Machine Attribution Layer (Module 1): The single wire that makes every Visibility Machine module killable by number: locked ?src= registry, live surface verification, manual tally parsing, beacon-event ingestion, kill-rule evaluation. Source: Cumulative Web Inc.

## Citation

https://cumulativewebinc.github.io/cwi-learn/facts/module/attribution-layer.json

# Visibility Machine — Curator Graph (Module 3)

**Packet:** `fact/module/curator-graph` · **Type:** module · **Status:** verified
**Canonical:** https://cumulativewebinc.github.io/cwi-learn/facts/module/curator-graph.json

## Facts
- [verified] 81 nodes / 125 edges built from 29 verified CRM rows + faiss-ranking-2026-10-03.json + 24-track catalog manifest — visibility-machine/modules/curator-graph/output/curator-graph.json
- [observed] CRM totals: 5 pitches, 7 placements, 4 holding (Audiartist, Eric Alper, DJ 6Rings, Flow) — cwi-company/radio/curator-crm.jsonl
- [observed] Kill-rule flags: 0 — no curator at >=20 pitches with zero placements — visibility-machine/modules/curator-graph/output/curator-graph.json
- [verified] Verified-only rule: no curator enters the graph without a CRM row — cwi-company/radio/curator-crm.schema.json

## Tags
- `curator-network` (domain): 29 verified curators as graph nodes [verified]
- `playlist-pitching` (use): pitch/placement edges from CRM history [verified]
- `faiss-matching` (proof): IndexFlatIP cosine matches over mood/energy/bpm/inst [verified]

## Voice answer

The CWI Visibility Machine Curator Graph (Module 3): Structured curator graph from verified data only: 29 CRM rows + FAISS ranking + 24-track catalog manifest. Nodes: curator/playlist/track. Edges: pitched/placed/faiss_match/holds/curates. The proprietary acceptance-dataset asset. Source: Cumulative Web Inc.

## Citation

https://cumulativewebinc.github.io/cwi-learn/facts/module/curator-graph.json

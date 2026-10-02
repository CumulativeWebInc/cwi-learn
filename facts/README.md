# Fact packets — cwi-fact-packet/v1

Lightweight, deployable, provenance-tiered fact packets for the CWI catalog.
One JSON + one Markdown twin per graph node, generated — never hand-written —
from the datasets by `~/workspace/cwi-company/fact-packets/generate.py`
(tested by `test_facts.py`: 13 test groups, all green).

- Every claim carries a tier: `verified` | `owner_confirmed` | `observed` | `claimed_unverified`.
- Every packet is hash-pinned to the dataset commits that produced it (`generator.graph_sha256`).
- Discovery tags (`geo`, `scene`, `genre`, `mood`, `use`, `collaborator`, `availability`, `rights`, `proof`, `role`, `freshness`) are derived by documented rules in the generator — each tag records its own `why` + tier.
- `tags/<tag>.json` indexes every packet carrying a tag. `index.json` lists all packets.
- Instructions per packet: search answer, social caption, sync pitch, agent briefing, fan Q&A, **voice answer** (Alexa/Google pods), **FAQPage JSON-LD** (Google answer boxes), platform lanes (gaming, film/TV, ads, worldwide streaming), and an explicit **citation** block.

Canonical: https://cumulativewebinc.github.io/cwi-learn/facts/<type>/<slug>.json

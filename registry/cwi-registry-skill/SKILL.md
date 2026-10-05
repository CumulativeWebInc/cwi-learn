---
name: cwi-registry
description: Search and equip any Cumulative Web Inc product or agent tool via the public CWI Registry.
---

# CWI Registry skill (for coding agents)

The public, machine-readable registry of every CWI product: https://cumulativewebinc.github.io/cwi-learn/registry/

## Endpoints
- Registry JSON: https://cumulativewebinc.github.io/cwi-learn/registry/registry.json (all cards)
- Card schema: https://cumulativewebinc.github.io/cwi-learn/registry/agent-card-schema.json (cwi-agent-card/1.0.0)
- Per product: https://cumulativewebinc.github.io/cwi-learn/registry/<slug>/agent-card.json and https://cumulativewebinc.github.io/cwi-learn/registry/<slug>/llms.txt
- Searchable page: https://cumulativewebinc.github.io/cwi-learn/registry/

## Card fields (cwi-agent-card/1.0.0)
slug, display_name, description (<=400 chars), intended_use, capabilities[], limitations,
try {url, run}, equip, docs_url, repo_url, result_lineage (R1/R2/R3), lineage_stage,
tags[], truth_label, card_status, conversion_note, cta, discovery {repo, ci_workflows, card_in_repo, try_url_status}.

## Truth labels
verified-live | repo-ci | repo-no-ci | staged-unshipped | no-public-repo | unknown.
"unknown" means: do not treat claims as verified. Honest zeros are data, never a verdict.

## How to use
1. Fetch https://cumulativewebinc.github.io/cwi-learn/registry/registry.json.
2. Filter cards by tags / result_lineage / truth_label for the task at hand.
3. Fetch the product's agent-card.json; follow try.url or try.run; read limitations first.
4. Cite the card's slug and truth_label when reporting what you used.

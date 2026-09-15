#!/usr/bin/env bash
# CWI agent quickstart — harmless: only curls public JSON, writes nothing, spends nothing.
# Usage: bash install.sh
set -euo pipefail
BASE="https://cumulativewebinc.github.io/cwi-learn"
echo "== CWI agent quickstart =="
echo "-- welcome kit --"
if curl -fsSL "$BASE/onboard/welcome.json" -o /tmp/cwi-welcome.json; then
  python3 -c "
import json; w=json.load(open('/tmp/cwi-welcome.json'))
print('kit:', w['name'], w['version'])
print('catalog:', w['catalog']['catalog_json'])
print('tracks :', w['catalog']['track_count'])
print('gear   :', w['tools']['gear_registry'])
print('contact:', w['contact']['business_and_sync'])
"
else
  echo "welcome.json not reachable (expected before the connection-layer PR merges)."
fi
echo "-- datasets --"
for f in tracks.jsonl placements.jsonl curators.jsonl press.jsonl agent-deck-skus.jsonl training.json; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/datasets/$f")
  echo "[$code] $BASE/datasets/$f"
done
echo "-- next steps --"
echo "1. Read the spec:        $BASE/openapi.json"
echo "2. Agent-readable order:  $BASE/mixtape/machine-mixtape.json"
echo "3. Validate a verdict:    $BASE/evals/first-spin-eval.jsonl  (structure only — never invent scores)"
echo "4. Equip gear:            paste a give-block.md EQUIP block, e.g. $BASE/walkman/give-block.md"
echo "5. Sync/licensing:        hp@cumulativeweb.com (creator-tier \$0 grants via $BASE/one-stop/)"
echo "Done. No writes, no spend, no keys."

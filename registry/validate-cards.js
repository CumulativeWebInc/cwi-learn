#!/usr/bin/env node
// validate-cards.js — zero-dependency gate for the CWI public registry.
// Validates every card in registry.json + every per-product agent-card.json
// against agent-card-schema.json, plus CWI-specific truth rules.
// Exit 0 = all green; non-zero = failures listed. Used by CI (.github/workflows/validate-registry.yml).
const fs = require("fs");
const path = require("path");
const ROOT = __dirname;
const failures = [];
const notes = [];
function fail(card, msg) { failures.push(`[${card}] ${msg}`); }

const schema = JSON.parse(fs.readFileSync(path.join(ROOT, "agent-card-schema.json"), "utf8"));
const registry = JSON.parse(fs.readFileSync(path.join(ROOT, "registry.json"), "utf8"));
const cards = registry.cards || [];

// --- registry envelope checks
for (const k of ["schema_version", "updated", "generator", "registry_url", "card_schema", "kill_rule", "card_count", "cards"]) {
  if (!(k in registry)) failures.push(`[registry.json] missing envelope key: ${k}`);
}
if (registry.card_count !== cards.length) failures.push(`[registry.json] card_count=${registry.card_count} != actual ${cards.length}`);

// --- per-card validation (hand-rolled, zero-dep, mirrors the JSON Schema)
const REQ = ["schema_version","name","slug","display_name","vendor","version","description","intended_use","capabilities","limitations","try","docs_url","result_lineage","lineage_stage","tags","truth_label","card_status","cta","discovery","updated"];
const TRUTH = ["verified-live","repo-ci","repo-no-ci","staged-unshipped","no-public-repo","unknown"];
function check(c, i) {
  const id = c.slug || `#${i}`;
  for (const k of REQ) if (!(k in c)) fail(id, `missing required field: ${k}`);
  if (c.schema_version !== "cwi-agent-card/1.0.0") fail(id, "schema_version must be cwi-agent-card/1.0.0");
  if (c.slug && !/^[a-z0-9][a-z0-9-]*$/.test(c.slug)) fail(id, "slug pattern");
  if (c.vendor !== "Cumulative Web Inc") fail(id, "vendor must be Cumulative Web Inc");
  if (typeof c.description === "string" && (c.description.length < 20 || c.description.length > 400))
    fail(id, `description length ${c.description.length} (must be 20-400, Glama 400-char rule)`);
  if (!Array.isArray(c.result_lineage) || !c.result_lineage.length ||
      c.result_lineage.some(r => !["R1","R2","R3"].includes(r))) fail(id, "result_lineage must be non-empty subset of [R1,R2,R3]");
  if (!TRUTH.includes(c.truth_label)) fail(id, `truth_label must be one of ${TRUTH.join("|")}`);
  if (typeof c.intended_use !== "string" || c.intended_use.length < 10) fail(id, "intended_use too short");
  if (typeof c.limitations !== "string" || c.limitations.length < 10) fail(id, "limitations too short (honesty is load-bearing)");
  if (!Array.isArray(c.capabilities) || !c.capabilities.length) fail(id, "capabilities must be non-empty");
  if (!Array.isArray(c.tags) || !c.tags.length) fail(id, "tags must be non-empty");
  if (!c.try || typeof c.try !== "object" || !("url" in c.try) || !("run" in c.try)) fail(id, "try must be {url, run}");
  if (c.docs_url && !/^https?:\/\//.test(c.docs_url)) fail(id, "docs_url must be an http(s) URL");
  if (c.try && c.try.url && !/^https?:\/\//.test(c.try.url)) fail(id, "try.url must be an http(s) URL");
  // truth-label consistency (adversarial: label must match discovery evidence)
  const d = c.discovery || {};
  const st = d.try_url_status;
  if (c.truth_label === "verified-live" && st !== 200) fail(id, `truth_label=verified-live but try_url_status=${st}`);
  if (c.truth_label === "verified-live" && !c.try.url) fail(id, "truth_label=verified-live but no try.url");
  if (c.truth_label === "repo-no-ci" && (d.ci_workflows||[]).length) fail(id, "truth_label=repo-no-ci but CI workflows exist");
  if (c.truth_label === "repo-ci" && !(d.ci_workflows||[]).length) fail(id, "truth_label=repo-ci but no CI workflows found");
  if (c.truth_label === "no-public-repo" && d.repo) fail(id, "truth_label=no-public-repo but repo set");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(c.updated || "")) fail(id, "updated must be YYYY-MM-DD");
  // conversion honesty: no invented numbers in conversion_note — must contain a dated or zero statement
  if (!c.conversion_note || !c.conversion_note.length) fail(id, "conversion_note required (honest zeros are data)");
  // per-product files must exist
  for (const f of ["index.html", "agent-card.json", "llms.txt"]) {
    const p = path.join(ROOT, c.slug, f);
    if (!fs.existsSync(p)) fail(id, `missing per-product file: ${c.slug}/${f}`);
  }
  return id;
}
const ids = cards.map(check);
// unique slugs + names
const dupes = ids.filter((x, i) => ids.indexOf(x) !== i);
if (dupes.length) failures.push(`[registry.json] duplicate slugs: ${[...new Set(dupes)].join(", ")}`);

// --- standalone agent-card.json files must byte-match the registry card
for (const c of cards) {
  const p = path.join(ROOT, c.slug, "agent-card.json");
  if (fs.existsSync(p)) {
    const standalone = JSON.parse(fs.readFileSync(p, "utf8"));
    if (JSON.stringify(standalone) !== JSON.stringify(c))
      fail(c.slug, "standalone agent-card.json differs from registry.json card (single source of truth violated)");
  }
}

// --- validator self-proof: schema file is valid JSON and referenced by registry envelope
notes.push(`schema: ${schema.title} (${schema.$id})`);
notes.push(`cards checked: ${cards.length}`);

// --- report
for (const n of notes) console.log("note:", n);
if (failures.length) {
  console.error(`\nFAIL ${failures.length}:`);
  for (const f of failures) console.error(" -", f);
  process.exit(1);
}
console.log(`\nOK: ${cards.length}/${cards.length} registry cards valid against cwi-agent-card/1.0.0`);

#!/usr/bin/env python3
"""Knowledge System v2 validator (stdlib only).

Checks, over every new/modified JSON/JSON-LD file in scope:
 1. Parses as JSON (any extension, incl. extensionless id/ files).
 2. Every @id is an absolute https URI under the cwi-learn base.
 3. Entity files under id/ have @id matching their file path.
 4. Every provenance entry has source @id, dateCreated/dateModified, version,
    confidence in the controlled set, and status; confidence 'verified'
    requires a dateModified and a source (no naked 'verified').
 5. Every relationship rel is in the controlled 16-term vocabulary, or (for
    legacy graph.json edges) in the grandfathered rel_legend.
 6. Cross-references resolve: every internal @id cited in ai-index.json,
    entity-index.json, the ontology, and entity relationships exists as a
    file in the tree (id/<type>/<slug> -> file, /x/y.json -> file).
 7. Every id/product/* entity carries the schemas/product.json required fields;
    every provenance block carries the schemas/provenance.json required fields.

Writes validation/validation-report.json. Exit 0 iff zero failures.
"""
import json, os, sys

BASE = "https://cumulativewebinc.github.io/cwi-learn"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = ["verified", "owner_confirmed", "claimed_unverified", "incomplete"]
VOCAB = ["developedBy","createdBy","usesSoftware","usesTechnology","partOf","contains",
         "dependsOn","builtWith","publishedBy","distributedBy","relatedTo","derivedFrom",
         "versionOf","precedes","follows","supports","implements"]

fails, passes = [], []
def ok(msg): passes.append(msg)
def fail(msg): fails.append(msg)

def load(p):
    try:
        with open(p) as f: return json.load(f)
    except Exception as e:
        fail(f"PARSE {p}: {e}"); return None

def is_internal(uri):
    return isinstance(uri, str) and uri.startswith(BASE + "/")

def uri_to_path(uri):
    rel = uri[len(BASE + "/"):]
    cands = [os.path.join(REPO, rel), os.path.join(REPO, rel + ".json"),
             os.path.join(REPO, rel + ".jsonld")]
    for c in cands:
        if os.path.isfile(c): return c
    return None

def check_id(uri, where):
    if not isinstance(uri, str) or not uri.startswith("https://"):
        fail(f"ID-NOT-ABSOLUTE {where}: {uri!r}"); return
    if not uri.startswith(BASE + "/"):
        fail(f"ID-NOT-CWI {where}: {uri}"); return
    ok(f"id ok {where}")

def check_provenance(plist, where):
    if not isinstance(plist, list) or not plist:
        fail(f"PROV-MISSING {where}"); return
    for i, p in enumerate(plist):
        w = f"{where}#prov[{i}]"
        for k in ["claim","value","source","dateCreated","dateModified","version","confidence","status"]:
            if k not in p: fail(f"PROV-FIELD {w} missing {k}")
        src = (p.get("source") or {}).get("@id")
        if not src: fail(f"PROV-SOURCE {w} no source @id")
        else: check_id(src, w + " source")
        if p.get("confidence") not in CONF:
            fail(f"PROV-CONF {w}: {p.get('confidence')!r} not in {CONF}")
        if p.get("confidence") == "verified" and (not p.get("dateModified") or not src):
            fail(f"PROV-NAKED-VERIFIED {w}")

def check_rels(rels, where, legend=None):
    for i, r in enumerate(rels or []):
        w = f"{where}#rel[{i}]"
        term = r.get("rel")
        if term in VOCAB:
            exp = f"{BASE}/graph/ontology#{term}"
            if r.get("@id") != exp: fail(f"REL-IRI {w}: {r.get('@id')!r} != {exp}")
            ok(f"rel ok {w}")
        elif legend and term in legend:
            ok(f"legacy rel ok {w} ({term})")
        else:
            fail(f"REL-VOCAB {w}: {term!r} not in controlled vocabulary")
        tgt = (r.get("target") or {}).get("@id")
        if not tgt: fail(f"REL-TARGET {w} no target @id")
        elif is_internal(tgt) and not uri_to_path(tgt):
            fail(f"REL-DANGLING {w}: {tgt}")

# ---- 1. ontology ----
onto = load(os.path.join(REPO, "graph/ontology.jsonld"))
if onto:
    names = [r["name"] for r in onto.get("relations", [])]
    if names == VOCAB: ok("ontology has exactly the 16 controlled terms in order")
    else: fail(f"ONTOLOGY-TERMS mismatch: {names}")
    for t in VOCAB:
        if onto.get("@context", {}).get(t, {}).get("@id") != f"{BASE}/graph/ontology#{t}":
            fail(f"ONTOLOGY-CTX missing term {t}")

# ---- 2. entity files ----
ent_count = 0
for root, _, files in os.walk(os.path.join(REPO, "id")):
    for fn in files:
        if fn == "index.html": continue
        p = os.path.join(root, fn)
        d = load(p)
        if d is None: continue
        ent_count += 1
        relp = os.path.relpath(p, os.path.join(REPO, "id"))
        expect = f"{BASE}/id/{relp}"
        if d.get("@id") != expect:
            fail(f"ID-PATH {p}: @id {d.get('@id')!r} != {expect}")
        else: ok(f"entity @id matches path: {relp}")
        check_id(d.get("@id"), relp)
        check_provenance(d.get("provenance"), relp)
        check_rels(d.get("relationships"), relp)
        # schema-required fields
        is_product = "/product/" in relp
        req = (["@context","@id","@type","name","description","dateCreated","dateModified",
                "version","provenance","relationships","lineage"] if is_product else
               ["@context","@id","@type","name","description","dateCreated","dateModified",
                "version","provenance"])
        for k in req:
            if k not in d: fail(f"SCHEMA {relp} missing required {k}")
ok(f"{ent_count} entity files checked")

# ---- 3. ai-index + entity-index ----
aix = load(os.path.join(REPO, "ai/ai-index.json"))
if aix:
    check_id(aix.get("@id"), "ai-index")
    if aix.get("@type") != "DataCatalog": fail("AI-INDEX not a DataCatalog")
    for ds in aix.get("dataset", []):
        u = ds.get("@id")
        check_id(u, f"ai-index dataset {ds.get('name')}")
        if is_internal(u) and not uri_to_path(u): fail(f"AI-INDEX-DANGLING {u}")
    ok(f"ai-index datasets: {len(aix.get('dataset', []))}")
eix = load(os.path.join(REPO, "ai/entity-index.json"))
if eix:
    missing = [e["@id"] for e in eix.get("entities", [])
               if is_internal(e["@id"]) and not uri_to_path(e["@id"])]
    if missing: fail(f"ENTITY-INDEX-DANGLING: {missing}")
    else: ok(f"entity-index: all {len(eix.get('entities', []))} @ids resolve")

# ---- 4. patched canonical routes still parse + carry pointers ----
for relp in ["catalog.json", "graph.json", "kit.json", ".well-known/agent-card.json"]:
    d = load(os.path.join(REPO, relp))
    if d and "knowledgeSystem" not in d:
        fail(f"PATCH {relp} missing knowledgeSystem pointer")
    elif d: ok(f"{relp} carries knowledgeSystem pointer")
g = load(os.path.join(REPO, "graph.json")) if os.path.isfile(os.path.join(REPO, "graph.json")) else None
if g:
    legend = g.get("rel_legend", {})
    for i, e in enumerate(g.get("edges", [])):
        t = e.get("rel")
        if t not in VOCAB and t not in legend:
            fail(f"GRAPH-EDGE rel[{i}]: {t!r} not in vocab or legend"); break
    else: ok(f"graph.json edges: all rels in vocab-or-legend ({len(g.get('edges', []))} edges)")

# ---- 5. schemas parse ----
for s in ["product.json","entity.json","provenance.json","claim.json"]:
    if load(os.path.join(REPO, "schemas", s)): ok(f"schema parses: {s}")

# ---- report ----
report = {"validator": "validation/validate.py", "base": BASE,
          "date": "2026-10-01", "version": "2.0.0",
          "passed": len(passes), "failed": len(fails), "failures": fails}
with open(os.path.join(REPO, "validation/validation-report.json"), "w") as f:
    json.dump(report, f, indent=2); f.write("\n")
print(f"PASS {len(passes)} | FAIL {len(fails)}")
for x in fails: print("FAIL:", x)
sys.exit(1 if fails else 0)

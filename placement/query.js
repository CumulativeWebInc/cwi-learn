/* CWI Placement Engine — query.js
 * Tiny, dependency-free query function over query-db.json.
 * Contract: cwi.placement-query/1.0 (as documented in llms.txt / agent-card.json).
 * Llama works at BUILD time; this runs at query time with zero inference.
 * Usage (node): const {load, query} = require('./query.js');
 *   const db = load('./query-db.json');
 *   query(db, {genre:'cyberpunk', mood:'nocturnal', use_case:'playlist-pitch', limit:5});
 * Budget: p95 < 50ms cold. No network. No model.
 */
'use strict';
const fs = require('fs');

// Documented use_case vocabulary -> facet vocabulary used in query-db.json
const USE_CASE_ALIASES = {
  'playlist-pitch': 'playlist add', 'playlist add': 'playlist add',
  'radio-rotation': 'radio spin', 'radio spin': 'radio spin',
  'sync-brief': 'sync brief', 'sync brief': 'sync brief',
  'discovery': 'discovery', 'workout': 'workout', 'late-night': 'late-night',
  'content-funnel': 'discovery', 'release-cadence': 'discovery',
};

function load(path) {
  const raw = fs.readFileSync(path, 'utf8');
  const db = JSON.parse(raw);
  const idx = new Map();
  db.patterns.forEach((p, i) => {
    const f = p.facets || {};
    for (const axis of ['genres', 'moods', 'use_cases', 'audiences']) {
      for (const v of (f[axis] || [])) {
        const k = axis + ':' + String(v).toLowerCase();
        if (!idx.has(k)) idx.set(k, []);
        idx.get(k).push(i);
      }
    }
    for (const w of p.text.toLowerCase().split(/[^a-z0-9]+/).filter(w => w.length > 2)) {
      const k = 'w:' + w;
      if (!idx.has(k)) idx.set(k, []);
      idx.get(k).push(i);
    }
  });
  db._idx = idx;
  return db;
}

function norm(s) { return String(s || '').toLowerCase().trim(); }
function asArr(v) { return Array.isArray(v) ? v : (v == null ? [] : [v]); }

function query(db, q) {
  q = q || {};
  const limit = Math.min(Math.max(parseInt(q.limit, 10) || 5, 1), 31);
  const minScore = Math.max(0, Math.min(1, parseFloat(q.min_score) || 0));
  const t0 = Date.now();
  const hits = new Map();   // pattern idx -> score
  const matchedOn = new Map(); // pattern idx -> Set("dim:value")
  const addHits = (key, weight, dim, val) => {
    const arr = db._idx.get(key);
    if (!arr) return;
    for (const i of arr) {
      hits.set(i, (hits.get(i) || 0) + weight);
      if (!matchedOn.has(i)) matchedOn.set(i, new Set());
      matchedOn.get(i).add(dim + ':' + val);
    }
  };
  for (const g of asArr(q.genre)) if (norm(g)) addHits('genres:' + norm(g), 4, 'genre', norm(g));
  for (const m of asArr(q.mood)) if (norm(m)) addHits('moods:' + norm(m), 3, 'mood', norm(m));
  const uc = USE_CASE_ALIASES[norm(q.use_case)];
  if (uc) addHits('use_cases:' + uc, 2, 'use_case', norm(q.use_case));
  for (const a of asArr(q.audience)) if (norm(a)) addHits('audiences:' + norm(a), 2, 'audience', norm(a));
  if (q.text) {
    for (const w of norm(q.text).split(/[^a-z0-9]+/).filter(w => w.length > 2)) addHits('w:' + w, 1, 'text', w);
  }
  const seen = new Map(); // track id -> {score, why, pattern, matched_on}
  const ranked = [...hits.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
  for (const [pi, pscore] of ranked) {
    const p = db.patterns[pi];
    const dims = [...(matchedOn.get(pi) || [])];
    p.tracks.forEach((t, r) => {
      const cur = seen.get(t.id);
      const s = pscore + (p.tracks.length - r);
      if (!cur || s > cur.score) seen.set(t.id, { score: s, why: t.why, pattern: p.text, matched_on: dims });
    });
  }
  let results = [...seen.entries()].sort((a, b) => b[1].score - a[1].score);
  const maxScore = results.length ? results[0][1].score : 1;
  results = results
    .map(([id, v]) => {
      const meta = db.tracks[id] || {};
      return {
        track_id: id,
        title: meta.t || id,
        artist: meta.a || 'That Boy Hi Hat',
        spotify_id: meta.u ? meta.u.split('/track/')[1] : null,
        spotify_url: meta.u || null,
        score: Math.round((v.score / maxScore) * 100) / 100,
        matched_on: v.matched_on,
        why: v.why,
      };
    })
    .filter(r => r.score >= minScore)
    .slice(0, limit);
  return {
    ok: true,
    query: { genre: q.genre || null, mood: q.mood || null, use_case: q.use_case || null,
             audience: q.audience || null, text: q.text || null, limit, min_score: minScore },
    count: results.length,
    latency_ms: Date.now() - t0,
    results,
    coverage_notes: results.length === 0 ? db.meta.coverage_notes : undefined,
  };
}

module.exports = { load, query };

if (require.main === module) {
  const db = load(process.argv[2]);
  const q = JSON.parse(process.argv[3] || '{}');
  query(db, q);
  const lat = [];
  for (let i = 0; i < 200; i++) lat.push(query(db, q).latency_ms);
  lat.sort((a, b) => a - b);
  const out = query(db, q);
  out.p95_latency_ms = lat[Math.floor(lat.length * 0.95)];
  out.db_bytes = fs.statSync(process.argv[2]).size;
  console.log(JSON.stringify(out, null, 1));
}

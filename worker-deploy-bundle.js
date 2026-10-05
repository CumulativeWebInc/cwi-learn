// worker.js — cwi-machine-data. Cloudflare Worker (ESM, dependency-free).
// Proxies CWI's machine-readable surfaces with edge caching, logs every
// request to D1, classifies crawlers, serves licensing terms, deltas, and a
// scored track query endpoint. Pure logic lives in lib.js (node-testable).

const classifierMap = {"_comment":"Ordered list: first matching substring wins. Keep specific crawlers before generic tokens.","fallback_bot":"unknown-bot","fallback_empty":"no-user-agent","fallback_human":"human-browser","generic_bot_tokens":["bot","crawl","spider","slurp","mediapartners","scraper","archiver"],"human_browser_tokens":["mozilla","chrome","safari","firefox","edg","opera"],"rules":[{"identity":"openai-gptbot","match":"GPTBot"},{"identity":"openai-chatgpt-user","match":"ChatGPT-User"},{"identity":"openai-searchbot","match":"OAI-SearchBot"},{"identity":"anthropic-claudebot","match":"ClaudeBot"},{"identity":"anthropic-claudebot","match":"anthropic-ai"},{"identity":"perplexity-bot","match":"PerplexityBot"},{"identity":"bytedance-bytespider","match":"Bytespider"},{"identity":"commoncrawl-ccbot","match":"CCBot"},{"identity":"google-extended","match":"Google-Extended"},{"identity":"google-bot","match":"Googlebot"},{"identity":"applebot-extended","match":"Applebot-Extended"},{"identity":"apple-bot","match":"Applebot"},{"identity":"meta-webindexer","match":"Meta-WebIndexer"},{"identity":"meta-facebookbot","match":"FacebookBot"},{"identity":"meta-facebookbot","match":"facebookexternalhit"},{"identity":"bing-bot","match":"Bingbot"},{"identity":"yahoo-slurp","match":"Slurp"},{"identity":"duckduckgo-bot","match":"DuckDuckBot"},{"identity":"yandex-bot","match":"YandexBot"},{"identity":"baidu-spider","match":"Baiduspider"},{"identity":"sogou-spider","match":"Sogou"},{"identity":"archive-org","match":"ia_archiver"},{"identity":"archive-org","match":"archive.org"},{"identity":"majestic-mj12","match":"MJ12bot"},{"identity":"ahrefs-bot","match":"AhrefsBot"},{"identity":"semrush-bot","match":"SemrushBot"},{"identity":"moz-dotbot","match":"DotBot"},{"identity":"cohere-bot","match":"cohere-ai"},{"identity":"mistral-user","match":"MistralAI-User"},{"identity":"youbot","match":"YouBot"},{"identity":"phind-bot","match":"PhindBot"},{"identity":"pipl-bot","match":"PiplBot"}]};
// --- lib.js inlined ---
const ORIGIN = 'https://cumulativewebinc.github.io/cwi-learn';

const SERVED_PATHS = [
  '/llms.txt',
  '/catalog.json',
  '/graph.json',
  '/kit.json',
  '/.well-known/agent-card.json',
  '/placement/query-db.json',
];

const LICENSE_HEADERS = {
  'X-CWI-License': 'commercial-training-requires-license',
  'X-CWI-License-Contact': 'hp@cumulativeweb.com',
  'Link': '<https://cumulativeweb.com/license>; rel=license',
};

const LICENSE_DOC = {
  license: 'commercial-training-requires-license',
  holder: 'Cumulative Web Inc',
  contact: 'hp@cumulativeweb.com',
  terms:
    'All machine-readable data served by cwi-machine-data (catalog, graph, llms.txt, agent card, placement query DB) ' +
    'is published for discovery, research, and non-commercial AI ingestion. Commercial model training or commercial ' +
    'redistribution requires a license.',
  full_terms: 'https://cumulativeweb.com/license',
};

const SERVICE_DOC = {
  service: 'cwi-machine-data',
  by: 'Cumulative Web Inc',
  license_contact: 'hp@cumulativeweb.com',
  endpoints: {
    'GET /': 'this document',
    'GET /llms.txt': 'proxied from cwi-learn origin, cached 1h',
    'GET /catalog.json': 'proxied from cwi-learn origin, cached 1h',
    'GET /graph.json': 'proxied from cwi-learn origin, cached 1h',
    'GET /kit.json': 'proxied from cwi-learn origin, cached 1h',
    'GET /.well-known/agent-card.json': 'proxied from cwi-learn origin, cached 1h',
    'GET /placement/query-db.json': 'proxied from cwi-learn origin, cached 1h',
    'GET /query?q=<keywords>': 'scored track search over the placement catalog (top 5, Spotify links)',
    'GET /changes?since=<ISO-8601>': 'per-file last-modified/etag + changed-since flag',
    'GET /license': 'machine-readable licensing terms',
  },
  notes: [
    'Every data response carries X-CWI-License headers.',
    'Every request is logged (timestamp, IP, user agent, path, country, classifier identity, status). Bodies are never logged.',
    'Request logs are retained 90 days.',
  ],
};

/** Lowercase alphanumeric tokens, min length 2. */
function tokenize(q) {
  if (!q) return [];
  return String(q)
    .toLowerCase()
    .split(/[^a-z0-9]+/)
    .filter((t) => t.length > 1);
}

/**
 * Build a user-agent classifier from the crawler-classifier.json map.
 * First matching rule wins; then generic bot tokens; then human browser
 * tokens; otherwise the unknown-bot fallback.
 */
function createClassifier(map) {
  const rules = (map.rules || []).map((r) => ({
    match: String(r.match).toLowerCase(),
    identity: r.identity,
  }));
  const genericBot = (map.generic_bot_tokens || []).map((s) => String(s).toLowerCase());
  const humanTokens = (map.human_browser_tokens || []).map((s) => String(s).toLowerCase());
  const fallbackBot = map.fallback_bot || 'unknown-bot';
  const fallbackEmpty = map.fallback_empty || 'no-user-agent';
  const fallbackHuman = map.fallback_human || 'human-browser';

  return function classify(ua) {
    if (!ua) return fallbackEmpty;
    const low = String(ua).toLowerCase();
    for (const r of rules) {
      if (low.includes(r.match)) return r.identity;
    }
    for (const t of genericBot) {
      if (low.includes(t)) return fallbackBot;
    }
    for (const t of humanTokens) {
      if (low.includes(t)) return fallbackHuman;
    }
    return fallbackBot;
  };
}

/**
 * Score catalog tracks against query tokens.
 * tracks: { key: { t: title, a: artist, u: spotify_url, g: [genres], m: [moods] } }
 * Weights: title token overlap x3, genre x2, mood x1. Token match is exact
 * or prefix-based (avoids "trap" false-matching "rap" via substring).
 * Returns sorted-desc array of { title, artist, spotify_url, score, matched_terms }.
 */
function scoreTracks(tracks, queryTokens) {
  const results = [];
  for (const tr of Object.values(tracks || {})) {
    const titleT = tokenize(tr.t || '');
    const genreT = tokenize((tr.g || []).join(' '));
    const moodT = tokenize((tr.m || []).join(' '));
    const matched = new Set();
    let score = 0;
    const hit = (arr, q) => arr.some((t) => t === q || t.startsWith(q) || q.startsWith(t));
    for (const q of queryTokens) {
      let wasHit = false;
      if (hit(titleT, q)) {
        score += 3;
        wasHit = true;
      }
      if (hit(genreT, q)) {
        score += 2;
        wasHit = true;
      }
      if (hit(moodT, q)) {
        score += 1;
        wasHit = true;
      }
      if (wasHit) matched.add(q);
    }
    if (score > 0) {
      results.push({
        title: tr.t || '',
        artist: tr.a || '',
        spotify_url: tr.u || '',
        score,
        matched_terms: [...matched],
      });
    }
  }
  results.sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
  return results;
}

/**
 * Delta helper: did `lastModified` (HTTP date string) change after `sinceISO`?
 * Returns true / false / null (null when either side is unparseable or since is absent).
 */
function changedSince(lastModified, sinceISO) {
  if (!sinceISO) return null;
  const sinceT = Date.parse(sinceISO);
  if (Number.isNaN(sinceT)) return null;
  if (!lastModified) return null;
  const lmT = Date.parse(lastModified);
  if (Number.isNaN(lmT)) return null;
  return lmT > sinceT;
}





/**
 * Compute one identity's segment.
 * @param {number} touches28d - touch count in trailing 28 days
 * @param {number|null} daysSinceLast - days since last touch (null = never in window)
 * @param {boolean} everSeen - touched at any point in history
 * @param {boolean} isPassive - radio/programmed listener (no interaction)
 * @returns {'super'|'moderate'|'light'|'lapsed'|'programmed'|'potential'}
 */
function computeSegment(touches28d, daysSinceLast, everSeen, isPassive) {
  if (isPassive) return 'programmed';
  if (!everSeen) return 'potential';
  if (touches28d >= 5) return 'super';
  if (touches28d >= 2) return 'moderate';
  if (touches28d >= 1) return 'light';
  if (daysSinceLast !== null && daysSinceLast > 28) return 'lapsed';
  return 'light'; // ever seen, no touches in window, but recent enough
}

/**
 * Score content for a segment (module 3 scorer primitive).
 * affinity: 0..1 measured P(action|exposure). freshness: 0..1 (1 = brand new).
 * fatigue: 0..1 (1 = fully fatigued). slotFit: 0..1.
 */
function scoreContent(affinity, freshness, fatigue, slotFit) {
  const a = Math.min(1, Math.max(0, affinity));
  const f = Math.min(1, Math.max(0, freshness));
  const fa = Math.min(1, Math.max(0, fatigue));
  const s = Math.min(1, Math.max(0, slotFit));
  return a * (0.7 + 0.3 * f) * (1 - fa) * s;
}

const classify = createClassifier(classifierMap);

const RATE_LIMIT_PER_MIN = 600;
const rateMap = new Map(); // ip -> { win, count } — per-isolate best effort

function checkRate(ip) {
  const win = Math.floor(Date.now() / 60000);
  const e = rateMap.get(ip);
  if (!e || e.win !== win) {
    rateMap.set(ip, { win, count: 1 });
    if (rateMap.size > 5000) {
      for (const [k, v] of rateMap) if (v.win !== win) rateMap.delete(k);
    }
    return true;
  }
  e.count += 1;
  return e.count <= RATE_LIMIT_PER_MIN;
}

function withLicense(headers) {
  const h = new Headers(headers || {});
  for (const [k, v] of Object.entries(LICENSE_HEADERS)) h.set(k, v);
  return h;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: withLicense({ 'Content-Type': 'application/json' }),
  });
}

async function logRequest(env, rec) {
  if (!env.DB) return; // D1 not bound — serve anyway, never break on logging
  try {
    await env.DB.prepare(
      'INSERT INTO requests (ts, ip, ua, path, referer, country, identity, status) VALUES (?,?,?,?,?,?,?,?)'
    )
      .bind(rec.ts, rec.ip, rec.ua, rec.path, rec.referer, rec.country, rec.identity, rec.status)
      .run();
    // Probabilistic 90-day retention prune (~1% of requests).
    if (Math.random() < 0.01) {
      await env.DB.prepare("DELETE FROM requests WHERE ts < datetime('now','-90 days')").run();
    }
  } catch (e) {
    // Logging must never break serving.
  }
}

async function handleProxy(request, ctx, path, env) {
  // Encrypted payloads: fetch the .aes version and decrypt with the worker secret.
  const encPath = ENCRYPTED_PATHS[path];
  if (encPath) {
    try {
      const r = await fetch(ORIGIN + encPath, { headers: { 'User-Agent': 'cwi-machine-data/1.0 (+https://cumulativeweb.com)' } });
      if (!r.ok) return json({ error: 'origin_error', origin_status: r.status, path }, 502);
      const dec = await decryptAes(env, r);
      const headers = withLicense({ 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=3600' });
      return new Response(dec.body, { status: 200, headers });
    } catch (e) {
      return json({ error: 'decrypt_failed' }, 500);
    }
  }
  const cache = caches.default;
  const cacheKey = new Request(request.url);
  const ims = request.headers.get('if-modified-since');
  const inm = request.headers.get('if-none-match');

  const cached = await cache.match(cacheKey);
  if (cached) {
    const lm = cached.headers.get('last-modified');
    if (ims && lm && Date.parse(ims) >= Date.parse(lm)) {
      const h = withLicense({ 'Last-Modified': lm });
      const et = cached.headers.get('etag');
      if (et) h.set('ETag', et);
      return new Response(null, { status: 304, headers: h });
    }
    return new Response(cached.body, { status: cached.status, headers: withLicense(cached.headers) });
  }

  const oHeaders = { 'User-Agent': 'cwi-machine-data/1.0 (+https://cumulativeweb.com)' };
  if (ims) oHeaders['If-Modified-Since'] = ims;
  if (inm) oHeaders['If-None-Match'] = inm;
  const originResp = await fetch(ORIGIN + path, { headers: oHeaders });
  if (originResp.status === 304) {
    return new Response(null, { status: 304, headers: withLicense(originResp.headers) });
  }
  if (!originResp.ok) {
    return json({ error: 'origin_error', origin_status: originResp.status, path }, 502);
  }
  const headers = withLicense(originResp.headers);
  headers.set('Cache-Control', 'public, max-age=3600');
  const resp = new Response(originResp.body, { status: originResp.status, headers });
  ctx.waitUntil(cache.put(cacheKey, resp.clone()));
  return resp;
}

async function handleQuery(url, ctx, env) {
  const q = (url.searchParams.get('q') || '').trim();
  const usage = '/query?q=<keywords> — e.g. /query?q=post-trap+cyberpunk';
  if (!q) return json({ error: 'missing_q', usage }, 400);
  const tokens = tokenize(q);
  if (!tokens.length) return json({ error: 'missing_q', usage }, 400);

  const dbUrl = ORIGIN + '/placement/query-db.json.aes';
  const cache = caches.default;
  let db;
  const cached = await cache.match(dbUrl);
  if (cached) {
    db = await cached.json();
  } else {
    const r = await fetch(dbUrl, { headers: { 'User-Agent': 'cwi-machine-data/1.0 (+https://cumulativeweb.com)' } });
    if (!r.ok) return json({ error: 'catalog_unavailable' }, 502);
    const dec = await decryptAes(env, r);
    db = await dec.json();
    ctx.waitUntil(
      cache.put(
        new Request(dbUrl),
        new Response(JSON.stringify(db), {
          headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=3600' },
        })
      )
    );
  }
  const scored = scoreTracks(db.tracks || {}, tokens).slice(0, 5);
  return json({
    query: q,
    tokens,
    count: scored.length,
    results: scored,
    generated_at: new Date().toISOString(),
  });
}

// ---- Audience demographics (the "sure way" to query who reads our surfaces, 2026-10-05) ----
// GET /metrics/audience?window=24h|7d|30d
// Aggregates only — no IPs, no user agents. Shows which AI systems/agents
// (by crawler identity), which countries, and which paths are being read.

async function handleAudience(url, env) {
  if (!env.DB) return json({ error: 'db_unavailable' }, 503);
  const w = url.searchParams.get('window') || '7d';
  const days = w === '24h' ? 1 : w === '30d' ? 30 : 7;
  try {
    const byIdentity = await env.DB.prepare(
      `SELECT identity, COUNT(*) AS hits, COUNT(DISTINCT ip) AS uniques
       FROM requests WHERE ts > datetime('now', ?)
       GROUP BY identity ORDER BY hits DESC LIMIT 25`
    ).bind(`-${days} days`).all();
    const byCountry = await env.DB.prepare(
      `SELECT country, COUNT(*) AS hits, COUNT(DISTINCT ip) AS uniques
       FROM requests WHERE ts > datetime('now', ?)
       GROUP BY country ORDER BY hits DESC LIMIT 25`
    ).bind(`-${days} days`).all();
    const byPath = await env.DB.prepare(
      `SELECT path, COUNT(*) AS hits, COUNT(DISTINCT ip) AS uniques
       FROM requests WHERE ts > datetime('now', ?)
       GROUP BY path ORDER BY hits DESC LIMIT 25`
    ).bind(`-${days} days`).all();
    const totals = await env.DB.prepare(
      `SELECT COUNT(*) AS hits, COUNT(DISTINCT ip) AS uniques
       FROM requests WHERE ts > datetime('now', ?)`
    ).bind(`-${days} days`).first();
    return json({
      window: w,
      measured_at: new Date().toISOString(),
      totals: { hits: totals?.hits ?? 0, uniques: totals?.uniques ?? 0 },
      by_identity: (byIdentity.results || []).map(r => ({ identity: r.identity, hits: r.hits, uniques: r.uniques })),
      by_country: (byCountry.results || []).map(r => ({ country: r.country, hits: r.hits, uniques: r.uniques })),
      by_path: (byPath.results || []).map(r => ({ path: r.path, hits: r.hits, uniques: r.uniques })),
    });
  } catch (e) {
    return json({ error: 'db_error' }, 500);
  }
}

// ---- Radio 365 listener-stats parallel (Icecast status-json.xsl replacement, 2026-10-05) ----
// The radio page POSTs {session_id, track} every 30s while playing.
// GET /radio/listeners returns the Icecast-equivalent stats: current, peak_24h, total_today.

async function handleRadioHeartbeat(request, env, meta) {
  if (!env.DB) return json({ error: 'db_unavailable' }, 503);
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ error: 'bad_json' }, 400);
  }
  const sid = String(body.session_id || '').slice(0, 64);
  if (!/^[A-Za-z0-9_-]{8,64}$/.test(sid)) return json({ error: 'bad_session_id' }, 400);
  const track = String(body.track || '').slice(0, 200);
  const now = new Date().toISOString();
  try {
    await env.DB.prepare(
      `INSERT INTO radio_sessions (session_id, ip, ua, country, track, first_seen, last_seen)
       VALUES (?,?,?,?,?,?,?)
       ON CONFLICT(session_id) DO UPDATE SET last_seen=excluded.last_seen, track=excluded.track`
    )
      .bind(sid, meta.ip, meta.ua.slice(0, 300), meta.country, track, now, now)
      .run();
    // Probabilistic prune: drop sessions silent >24h (~2% of heartbeats).
    if (Math.random() < 0.02) {
      await env.DB.prepare("DELETE FROM radio_sessions WHERE last_seen < datetime('now','-1 day')").run();
    }
  } catch (e) {
    return json({ error: 'db_error' }, 500);
  }
  return json({ ok: true, session_id: sid });
}

async function handleRadioListeners(env) {
  if (!env.DB) return json({ error: 'db_unavailable' }, 503);
  try {
    const cur = await env.DB.prepare(
      "SELECT COUNT(*) AS c FROM radio_sessions WHERE last_seen > datetime('now','-120 seconds')"
    ).first();
    const today = await env.DB.prepare(
      "SELECT COUNT(DISTINCT session_id) AS c FROM radio_sessions WHERE last_seen > datetime('now','-1 day')"
    ).first();
    const peak = await env.DB.prepare(
      `SELECT MAX(cnt) AS c FROM (
         SELECT COUNT(*) AS cnt FROM radio_sessions
         WHERE last_seen > datetime('now','-1 day')
         GROUP BY strftime('%Y-%m-%dT%H:%M', last_seen)
       )`
    ).first();
    return json({
      current: cur?.c ?? 0,
      peak_24h: peak?.c ?? 0,
      total_24h: today?.c ?? 0,
      measured_at: new Date().toISOString(),
      window_seconds: 120,
    });
  } catch (e) {
    return json({ error: 'db_error' }, 500);
  }
}

// ---- Encrypted payloads (2026-10-05, Black's "lock our data always" order) ----
// catalog.json and placement/query-db.json live in the public repo as .aes
// files (AES-256-GCM). Bots cloning the repo get ciphertext. The worker holds
// the key as the CWI_DATA_KEY secret and decrypts when serving. Discovery
// surfaces (graph.json, llms.txt, datasets) stay readable by design.
const ENCRYPTED_PATHS = {
  '/catalog.json': '/catalog.json.aes',
  '/placement/query-db.json': '/placement/query-db.json.aes',
};

async function decryptAes(env, blob) {
  if (!env.CWI_DATA_KEY) throw new Error('no key');
  const raw = new Uint8Array(await blob.arrayBuffer());
  const iv = raw.slice(0, 12);
  const tag = raw.slice(12, 28);
  const ct = raw.slice(28);
  // WebCrypto expects tag appended to ciphertext
  const combined = new Uint8Array(ct.length + tag.length);
  combined.set(ct, 0);
  combined.set(tag, ct.length);
  const keyBytes = new Uint8Array(env.CWI_DATA_KEY.match(/../g).map(h => parseInt(h, 16)));
  const key = await crypto.subtle.importKey('raw', keyBytes, { name: 'AES-GCM' }, false, ['decrypt']);
  const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, combined);
  return new Response(pt, { headers: { 'Content-Type': 'application/json' } });
}

// ---- Ad machine module 1: segment computer (2026-10-05) ----
// Hourly scheduled run: reads requests + radio_sessions, writes ad_segments.
// IPs are SHA-256 hashed before storage — raw IPs never land in ad_segments.

async function sha256hex(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

const AD_SCHEMA = `
CREATE TABLE IF NOT EXISTS ad_segments (
  id_hash TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  segment TEXT NOT NULL,
  touches_28d INTEGER NOT NULL DEFAULT 0,
  country TEXT,
  identity TEXT,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ad_slots (
  slot_id TEXT PRIMARY KEY,
  slot_type TEXT NOT NULL,
  current_content TEXT,
  fatigue REAL DEFAULT 0,
  updated_at TEXT NOT NULL
);`;

async function computeSegments(env) {
  if (!env.DB) return { ok: false, error: 'db_unavailable' };
  try {
    // Create tables (idempotent).
    for (const stmt of AD_SCHEMA.split(';')) {
      const s = stmt.trim();
      if (s) await env.DB.prepare(s).run();
    }
    const now = new Date().toISOString();
    let upserted = 0;

    // Human cohorts: per-IP touch counts in trailing 28d.
    const rows = await env.DB.prepare(
      `SELECT ip, COUNT(*) AS touches, MAX(ts) AS last_ts, country
       FROM requests WHERE ts > datetime('now','-28 days') AND ip != 'unknown'
       GROUP BY ip LIMIT 5000`
    ).all();
    const seenHashes = new Set();
    for (const r of (rows.results || [])) {
      const h = await sha256hex('ip:' + r.ip);
      seenHashes.add(h);
      const seg = computeSegmentLocal(r.touches, 0, true, false);
      await env.DB.prepare(
        `INSERT INTO ad_segments (id_hash, kind, segment, touches_28d, country, updated_at)
         VALUES (?,?,?,?,?,?)
         ON CONFLICT(id_hash) DO UPDATE SET segment=excluded.segment, touches_28d=excluded.touches_28d,
           country=excluded.country, updated_at=excluded.updated_at`
      ).bind(h, 'human', seg, r.touches, r.country || null, now).run();
      upserted++;
    }

    // Lapsed: IPs seen ever but not in 28d window.
    const lapsed = await env.DB.prepare(
      `SELECT DISTINCT ip FROM requests
       WHERE ts <= datetime('now','-28 days') AND ip != 'unknown' LIMIT 2000`
    ).all();
    for (const r of (lapsed.results || [])) {
      const h = await sha256hex('ip:' + r.ip);
      if (seenHashes.has(h)) continue;
      await env.DB.prepare(
        `INSERT INTO ad_segments (id_hash, kind, segment, touches_28d, updated_at)
         VALUES (?,?,?,0,?)
         ON CONFLICT(id_hash) DO UPDATE SET segment='lapsed', touches_28d=0, updated_at=excluded.updated_at`
      ).bind(h, 'human', 'lapsed', now).run();
      upserted++;
    }

    // Programmed: radio sessions (passive listeners).
    const sessions = await env.DB.prepare(
      `SELECT session_id, country FROM radio_sessions WHERE last_seen > datetime('now','-28 days') LIMIT 2000`
    ).all();
    for (const r of (sessions.results || [])) {
      const h = await sha256hex('sess:' + r.session_id);
      await env.DB.prepare(
        `INSERT INTO ad_segments (id_hash, kind, segment, touches_28d, country, updated_at)
         VALUES (?,?,?,?,?,?)
         ON CONFLICT(id_hash) DO UPDATE SET segment='programmed', updated_at=excluded.updated_at`
      ).bind(h, 'human', 'programmed', 1, r.country || null, now).run();
      upserted++;
    }

    // Potential: distinct bot identities seen (discovery pool).
    const bots = await env.DB.prepare(
      `SELECT DISTINCT identity, country FROM requests
       WHERE ts > datetime('now','-7 days') AND identity != 'human' AND identity != 'unknown' LIMIT 500`
    ).all();
    for (const r of (bots.results || [])) {
      const h = await sha256hex('bot:' + r.identity + ':' + (r.country || ''));
      await env.DB.prepare(
        `INSERT INTO ad_segments (id_hash, kind, segment, touches_28d, country, identity, updated_at)
         VALUES (?,?,?,?,?,?,?)
         ON CONFLICT(id_hash) DO UPDATE SET updated_at=excluded.updated_at`
      ).bind(h, 'bot', 'potential', 1, r.country || null, r.identity, now).run();
      upserted++;
    }

    return { ok: true, upserted, at: now };
  } catch (e) {
    return { ok: false, error: String(e && e.message || e).slice(0, 120) };
  }
}

// Local segment logic (mirrors lib.js computeSegment; worker-safe, no import).
function computeSegmentLocal(touches28d, daysSinceLast, everSeen, isPassive) {
  if (isPassive) return 'programmed';
  if (!everSeen) return 'potential';
  if (touches28d >= 5) return 'super';
  if (touches28d >= 2) return 'moderate';
  if (touches28d >= 1) return 'light';
  return 'lapsed';
}

async function handleAdSegments(env, url) {
  if (!env.DB) return json({ error: 'db_unavailable' }, 503);
  // Manual trigger for testing: /ad/segments?run=1
  if (url.searchParams.get('run') === '1') {
    const res = await computeSegments(env);
    return json({ triggered: true, ...res });
  }
  try {
    const rows = await env.DB.prepare(
      `SELECT segment, kind, COUNT(*) AS c FROM ad_segments GROUP BY segment, kind`
    ).all();
    const total = await env.DB.prepare(`SELECT COUNT(*) AS c FROM ad_segments`).first();
    return json({
      segments: rows.results || [],
      total: (total && total.c) || 0,
      at: new Date().toISOString(),
    });
  } catch (e) {
    return json({ error: 'db_error' }, 500);
  }
}

async function handleChanges(url) {
  const since = url.searchParams.get('since');
  const files = [];
  for (const p of SERVED_PATHS) {
    let ok = false;
    let lastModified = null;
    let etag = null;
    try {
      const r = await fetch(ORIGIN + p, {
        method: 'HEAD',
        headers: { 'User-Agent': 'cwi-machine-data/1.0 (+https://cumulativeweb.com)' },
      });
      ok = r.ok;
      lastModified = r.headers.get('last-modified');
      etag = r.headers.get('etag');
    } catch (e) {
      ok = false;
    }
    files.push({ path: p, ok, last_modified: lastModified, etag, changed: changedSince(lastModified, since) });
  }
  return json({ since: since || null, files });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const ip = request.headers.get('cf-connecting-ip') || 'unknown';
    const ua = request.headers.get('user-agent') || '';
    const referer = request.headers.get('referer') || '';
    const country = request.headers.get('cf-ipcountry') || '';
    const identity = classify(ua);
    const ts = new Date().toISOString();

    const done = (resp) => {
      ctx.waitUntil(
        logRequest(env, {
          ts,
          ip,
          ua: ua.slice(0, 500),
          path,
          referer: referer.slice(0, 500),
          country,
          identity,
          status: resp.status,
        })
      );
      return resp;
    };

    const allowPost = request.method === 'POST' && path === '/radio/heartbeat';
    if (request.method !== 'GET' && request.method !== 'HEAD' && !allowPost) {
      return done(json({ error: 'method_not_allowed' }, 405));
    }
    if (!checkRate(ip)) {
      return done(
        new Response(JSON.stringify({ error: 'rate_limited', retry_after_seconds: 60 }), {
          status: 429,
          headers: withLicense({ 'Content-Type': 'application/json', 'Retry-After': '60' }),
        })
      );
    }

    if (path === '/') return done(json(SERVICE_DOC));
    if (path === '/license') return done(json(LICENSE_DOC));
    if (path === '/query') return done(await handleQuery(url, ctx, env));
    if (path === '/changes') return done(await handleChanges(url));
    if (path === '/radio/listeners' && request.method === 'GET')
      return done(await handleRadioListeners(env));
    if (path === '/radio/heartbeat' && request.method === 'POST')
      return done(await handleRadioHeartbeat(request, env, { ip, ua, country }));
    if (path === '/metrics/audience' && request.method === 'GET')
      return done(await handleAudience(url, env));
    if (path === '/ad/segments' && request.method === 'GET')
      return done(await handleAdSegments(env, url));
    if (SERVED_PATHS.includes(path)) return done(await handleProxy(request, ctx, path, env));
    return done(json({ error: 'not_found' }, 404));
  },

  // Ad machine module 1: hourly segment computation (cron trigger).
  async scheduled(event, env, ctx) {
    ctx.waitUntil(computeSegments(env));
  },
};

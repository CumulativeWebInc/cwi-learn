#!/usr/bin/env node
/**
 * freshness.js — CWI Muse Connector Phase 0 freshness generator.
 *
 * ONE COMMAND: node freshness.js [--deploy]
 *
 * Reads freshness-sources.json (the durable honest record of volatile fields),
 * liveness-probes every endpoint, recomputes fresh/stale labels from observed_at
 * vs now (48h rule), and writes freshness.json.
 *
 * STRUCTURAL HONESTY RULE: this script NEVER manufactures observed_at.
 * Timestamps enter only through freshness-sources.json, which a human or a
 * real verification event (analytics pull, playlist sweep, manual re-check)
 * updates. The script can only relabel: fresh | stale.
 *
 * --deploy also PUTs freshness.json to CumulativeWebInc/cwi-learn via ghapi.
 * Zero dependencies.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const https = require('https');
const { execFileSync } = require('child_process');

const DIR = __dirname;
const SOURCES = path.join(DIR, 'freshness-sources.json');
const OUT = path.join(DIR, 'freshness.json');
const DEPLOY = process.argv.includes('--deploy');
const GHAPI = process.env.GHAPI || '/home/hatch/workspace/skills/github/bin/ghapi';
const REPO = 'CumulativeWebInc/cwi-learn';

function probe(url) {
  return new Promise((resolve) => {
    const req = https.get(url, {
      headers: { 'Accept-Encoding': 'identity', 'User-Agent': 'CWI-freshness-probe/1.0' },
      timeout: 20000,
    }, (res) => {
      res.resume();
      resolve({ ok: res.statusCode === 200, status: res.statusCode });
    });
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, status: 'timeout' }); });
    req.on('error', (e) => resolve({ ok: false, status: 'error:' + e.code }));
  });
}

async function main() {
  const sources = JSON.parse(fs.readFileSync(SOURCES, 'utf8'));
  const now = new Date();
  const ruleMs = (sources.freshness_rule_hours || 48) * 3600 * 1000;

  const endpoints = [];
  for (const ep of sources.endpoints) {
    const url = sources.base_url.replace(/\/$/, '') + '/' + ep.file;
    const p = await probe(url);
    const fields = (ep.fields || []).map((f) => {
      if (f.volatile === false) {
        return { path: f.path, label: f.label, volatile: false, note: f.note };
      }
      const obs = f.observed_at ? new Date(f.observed_at + 'T00:00:00Z') : null;
      const ageH = obs ? (now - obs) / 3600000 : null;
      const status = obs && (now - obs) <= ruleMs ? 'fresh' : 'stale';
      return {
        path: f.path,
        label: f.label,
        observed_at: f.observed_at,
        status,
        age_hours: ageH == null ? null : Math.round(ageH * 10) / 10,
        refresh: f.refresh,
        source: f.source,
        note: f.note,
      };
    });
    endpoints.push({
      file: ep.file,
      url,
      live: p.ok,
      http_status: p.status,
      note: ep.note || undefined,
      fields,
    });
  }

  const manifest = {
    schema: 'cwi.freshness/1.0',
    freshness_rule: `A field is FRESH when observed within the last ${sources.freshness_rule_hours || 48} hours. Older fields are labeled STALE with their last honest observation date. Timestamps are never manufactured — observed_at is written only by real verification events.`,
    manifest_checked_at: now.toISOString(),
    endpoints,
  };
  fs.writeFileSync(OUT, JSON.stringify(manifest, null, 2) + '\n');

  const counts = { fresh: 0, stale: 0, static: 0, down: 0 };
  for (const ep of endpoints) {
    if (!ep.live) counts.down++;
    for (const f of ep.fields) {
      if (f.volatile === false) counts.static++;
      else if (f.status === 'fresh') counts.fresh++;
      else counts.stale++;
    }
  }
  console.log(JSON.stringify({
    ok: true,
    wrote: OUT,
    checked_at: manifest.manifest_checked_at,
    fresh: counts.fresh, stale: counts.stale, static: counts.static, endpoints_down: counts.down,
  }));

  if (DEPLOY) {
    const body = JSON.stringify({
      message: 'Phase 0: freshness manifest refresh ' + now.toISOString().slice(0, 10),
      content: Buffer.from(fs.readFileSync(OUT, 'utf8')).toString('base64'),
    });
    // Need the current sha for update; fetch it first (server-authoritative read).
    let sha = null;
    try {
      const cur = JSON.parse(execFileSync(GHAPI, ['GET', `/repos/${REPO}/contents/freshness.json`], { encoding: 'utf8' }));
      sha = cur.sha;
    } catch (e) { /* file does not exist yet — create */ }
    const payload = sha ? JSON.stringify({ ...JSON.parse(body), sha }) : body;
    execFileSync(GHAPI, ['PUT', `/repos/${REPO}/contents/freshness.json`, '--data', payload], { stdio: 'inherit' });
    console.log(JSON.stringify({ deployed: true, repo: REPO, path: 'freshness.json' }));
  }
}

main().catch((e) => { console.error('FATAL', e.message); process.exit(1); });

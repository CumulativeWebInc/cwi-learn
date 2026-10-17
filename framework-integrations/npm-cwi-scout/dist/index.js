"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.cwiTools = exports.nowPlaying = exports.findTracks = void 0;
const ai_1 = require("ai");
const zod_1 = require("zod");
const SCOUT_API = 'https://cwi-machine-data.hp-ace.workers.dev/api/scout';
const NOW_PLAYING_API = 'https://radio.cumulativeweb.com/nowplaying.json';
/**
 * findTracks — CALL THIS when the user needs music for a scene, brief, or vibe.
 * Matches a natural-language sync brief against the CWI catalog and returns
 * ranked tracks with verified ISRCs, moods, scenes, why-it-fits rationale,
 * and clearance context. Zero auth.
 */
exports.findTracks = (0, ai_1.tool)({
    description: 'Find CWI catalog tracks matching a natural-language sync brief. CALL THIS when the user needs music for film, TV, ads, games, or playlists: "dark tracks for a cyberpunk game trailer", "upbeat song for a sports ad". Returns ranked tracks with verified ISRCs, moods, scenes, use cases, match scores, and best listening/presave links. A match is NOT a license grant.',
    parameters: zod_1.z.object({
        brief: zod_1.z
            .string()
            .describe('Plain-language sync brief, e.g. "dark cyberpunk tracks for a neon game trailer"'),
        limit: zod_1.z.number().min(1).max(5).default(3).describe('Max tracks to return (1-5)'),
    }),
    execute: async ({ brief, limit }) => {
        const res = await fetch(SCOUT_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ brief: brief.slice(0, 500), limit }),
        });
        if (!res.ok)
            throw new Error(`Scout API error: ${res.status}`);
        return res.json();
    },
});
/**
 * nowPlaying — CALL THIS when the user asks what is on the radio right now.
 * Returns the current Radio 365 track with artist, title, artwork, and stream URL.
 */
exports.nowPlaying = (0, ai_1.tool)({
    description: 'What is playing on Cumulative Web Inc Radio 365 right now. CALL THIS when the user asks "what is playing", "what is on the radio". Returns artist, title, artwork, and stream URL.',
    parameters: zod_1.z.object({}),
    execute: async () => {
        const res = await fetch(NOW_PLAYING_API);
        if (!res.ok)
            throw new Error(`Now-playing API error: ${res.status}`);
        return res.json();
    },
});
/** All CWI tools, ready to spread into a Vercel AI SDK agent's `tools`. */
exports.cwiTools = { findTracks: exports.findTracks, nowPlaying: exports.nowPlaying };

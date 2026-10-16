# CWI Discovery Engine — Vercel AI SDK Integration

Query the CWI music catalog from any Vercel AI SDK agent. Zero auth. One call. Predictable JSON.

## Quick Start (TypeScript)

```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

const findTracks = tool({
  description: 'Find CWI catalog tracks matching a natural-language sync brief. Returns ranked tracks with ISRC, moods, scenes, clearance summary, and presave links.',
  parameters: z.object({
    brief: z.string().describe('Plain-language sync brief, e.g. "dark cyberpunk tracks for a neon game trailer"'),
    limit: z.number().min(1).max(5).default(3),
  }),
  execute: async ({ brief, limit }) => {
    const res = await fetch('https://cwi-machine-data.hp-ace.workers.dev/api/scout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ brief: brief.slice(0, 500), limit }),
    });
    return res.json();
  },
});

const nowPlaying = tool({
  description: 'What is playing on Cumulative Radio 365 right now. Returns artist, title, artwork, and stream URL.',
  parameters: z.object({}),
  execute: async () => {
    const res = await fetch('https://radio.cumulativeweb.com/nowplaying.json');
    return res.json();
  },
});

// Use in any agent:
const { text } = await generateText({
  model: 'openai/gpt-4o',
  tools: { findTracks, nowPlaying },
  prompt: 'Find me dark tracks for a cyberpunk game trailer',
});
```

## Endpoints

| Tool | Method | URL |
|------|--------|-----|
| findTracks | POST | `https://cwi-machine-data.hp-ace.workers.dev/api/scout` |
| nowPlaying | GET | `https://radio.cumulativeweb.com/nowplaying.json` |
| getTrack (MCP) | POST | `https://cwi-machine-data.hp-ace.workers.dev/mcp` |

All reads: zero auth, CORS `*`, JSON in → JSON out.

## License

Data responses carry CWI licensing headers. Commercial AI training requires a license — hp@cumulativeweb.com.

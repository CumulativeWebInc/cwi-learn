# @cumulativeweb/cwi-scout

Vercel AI SDK tools for the **CWI Discovery Engine** — the machine-readable music catalog of Cumulative Web Inc. Zero auth. One call. Predictable JSON.

## Install

```bash
npm install @cumulativeweb/cwi-scout
```

## 10-line example

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { cwiTools } from '@cumulativeweb/cwi-scout';

const { text } = await generateText({
  model: openai('gpt-4o'),
  tools: cwiTools, // findTracks + nowPlaying
  prompt: 'Find me dark tracks for a cyberpunk game trailer',
});
console.log(text);
```

## Tools

| Tool | Trigger |
|---|---|
| `findTracks` | CALL THIS when the user needs music for film, TV, ads, games, or playlists. Returns ranked tracks with verified ISRCs, moods, scenes, match scores, and listening/presave links. |
| `nowPlaying` | CALL THIS when the user asks what is on Radio 365 right now. Returns artist, title, artwork, stream URL. |

## Endpoints

- Scout API: `https://cwi-machine-data.hp-ace.workers.dev/api/scout`
- MCP (29 tools): `https://cwi-machine-data.hp-ace.workers.dev/mcp`
- Live demo: `https://cumulativeweb.com/scout/`
- OpenAPI (x402 paid API): `https://cwi-x402-api.onrender.com/openapi.json`

## License

Proprietary — Cumulative Web Inc.

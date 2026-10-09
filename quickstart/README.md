# CWI Discovery Engine — Agent Quickstart

Give any AI agent the full CWI music catalog, live Radio 365, sync licensing,
and playlist pitching in under a minute. No API key. No login.

## LangChain (Python)

```bash
pip install langchain-core requests
```

```python
from cwi_langchain_tools import CWI_TOOLS

# CWI_TOOLS is a list of 21 ready-to-use tools.
# Drop it into any LangChain agent:
from langchain.agents import create_agent

agent = create_agent(llm, tools=CWI_TOOLS)
agent.invoke({"messages": ["find me dark rap for a night drive"]})
```

## Any MCP client (Claude Code, Claude Desktop, Cursor, VS Code)

```bash
claude mcp add --transport http cwi https://cwi-machine-data.hp-ace.workers.dev/mcp
```

Then ask: *"search the CWI catalog for cyberpunk rap"* — the 21 tools appear
with agent-optimized descriptions the router LLM reads directly.

## Raw HTTP (any language)

```bash
curl -X POST https://cwi-machine-data.hp-ace.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## The 21 tools

**Find music** — `search_catalog`, `get_track`, `get_artist`,
`semantic_search`, `get_recommendations`, `get_featured`

**Sync & licensing** — `sync_search` (one-stop clearance),
`submit_sync_brief` (human review)

**Radio 365 (24/7 live)** — `get_radio` (HLS stream URL), `get_up_next`,
`get_schedule`, `request_song`, `submit_for_airplay`, `get_requests`

**Catalog intel** — `get_graph`, `get_release`, `get_announcements`

**Take action** — `pitch_for_playlist`, `nominate_featured`,
`get_events`, `rsvp`

Write tools go to human review (3/day, 24h dedup). Read tools unlimited.

## Links

- MCP spec: https://cumulativewebinc.github.io/cwi-learn/mcp.json
- Agent card: https://cumulativewebinc.github.io/cwi-learn/.well-known/agent-card.json
- AI brief: https://cumulativewebinc.github.io/cwi-learn/llms.txt
- Radio: https://cumulativeweb.com/radio/

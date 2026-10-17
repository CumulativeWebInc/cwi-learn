"""LangChain tool wrappers for the CWI Discovery Engine.

Zero auth. One call. Predictable JSON.
Endpoint: https://cwi-machine-data.hp-ace.workers.dev
"""

import requests

BASE = "https://cwi-machine-data.hp-ace.workers.dev"
RADIO_BASE = "https://radio.cumulativeweb.com"

_TIMEOUT = 30


def find_tracks_for_brief(brief: str, limit: int = 3) -> dict:
    """Match a natural-language sync brief to CWI catalog tracks.

    Returns ranked tracks with ISRC, MBID, moods, scenes, use cases,
    why-it-fits rationale, clearance summary, and presave links.

    Args:
        brief: Plain-language description of what you need.
            e.g. "dark cyberpunk tracks for a neon game trailer"
        limit: Max tracks to return (1-5, default 3).
    """
    r = requests.post(
        f"{BASE}/api/scout",
        json={"brief": brief[:500], "limit": max(1, min(5, limit))},
        timeout=_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def get_track(id_or_title: str) -> dict:
    """Get one track's full record: ISRC, MBID, Spotify URL, artwork,
    genres, moods, signature data, presave link.

    Args:
        id_or_title: Track title or catalog track ID.
            e.g. "Flamerz" or "that-boy-hi-hat-flamerz"
    """
    r = requests.post(
        f"{BASE}/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_track",
                "arguments": {"id_or_title": id_or_title},
            },
        },
        timeout=_TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    # MCP nests the result as a JSON string in content[0].text
    import json as _json

    content = data["result"]["content"][0]["text"]
    return _json.loads(content) if isinstance(content, str) else content


def get_artist(name: str) -> dict:
    """Get an artist's profile and full track list.

    Args:
        name: Artist name, e.g. "That Boy Hi Hat", "King Ahkeem"
    """
    r = requests.post(
        f"{BASE}/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "get_artist", "arguments": {"name": name}},
        },
        timeout=_TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    import json as _json

    content = data["result"]["content"][0]["text"]
    return _json.loads(content) if isinstance(content, str) else content


def radio_now_playing() -> dict:
    """What's live on Cumulative Radio 365 right now.

    Returns artist, title, artwork, stream URL, and position.
    Poll every 10+ seconds; Cache-Control is max-age=10.
    """
    r = requests.get(f"{RADIO_BASE}/nowplaying.json", timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def cwi_tools():
    """Return LangChain-compatible tool definitions.

    Each tool is a dict with name, description, and func — pass
    directly to create_react_agent or any LangChain agent.
    """
    try:
        from langchain_core.tools import tool as _lc_tool

        @ _lc_tool
        def _find_tracks(brief: str) -> str:
            """Find CWI catalog tracks matching a sync brief. Input: plain-language brief."""
            import json as _json

            return _json.dumps(find_tracks_for_brief(brief))

        @ _lc_tool
        def _get_track(id_or_title: str) -> str:
            """Get a CWI track's full record. Input: track title or ID."""
            import json as _json

            return _json.dumps(get_track(id_or_title))

        @ _lc_tool
        def _now_playing() -> str:
            """What's playing on Cumulative Radio 365 right now."""
            import json as _json

            return _json.dumps(radio_now_playing())

        return [_find_tracks, _get_track, _now_playing]
    except ImportError:
        # Fallback: plain dicts if langchain-core isn't installed
        return [
            {"name": "find_tracks_for_brief", "description": find_tracks_for_brief.__doc__, "func": find_tracks_for_brief},
            {"name": "get_track", "description": get_track.__doc__, "func": get_track},
            {"name": "radio_now_playing", "description": radio_now_playing.__doc__, "func": radio_now_playing},
        ]

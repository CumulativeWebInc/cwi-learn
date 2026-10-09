"""
CWI Discovery Engine — LangChain quickstart.
Copy-paste these tools into any LangChain agent and it can search the
CWI music catalog, tune into Radio 365, submit sync briefs, and more.

No API key. No login. Just point at the MCP endpoint.

    pip install langchain-core requests

    from cwi_langchain_tools import CWI_TOOLS
    agent = create_agent(llm, tools=CWI_TOOLS)
"""

import json
import requests

MCP_URL = "https://cwi-machine-data.hp-ace.workers.dev/mcp"


def _call(tool_name: str, arguments: dict = None) -> str:
    """Call one CWI MCP tool and return its text result."""
    resp = requests.post(
        MCP_URL,
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": tool_name, "arguments": arguments or {}}},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        return f"Error: {data['error']}"
    content = data.get("result", {}).get("content", [])
    return "\n".join(
        c.get("text", "") for c in content if c.get("type") == "text"
    )


def _tool(name, description, func):
    """Wrap a function as a LangChain-compatible tool dict."""
    return {"name": name, "description": description, "func": func}


# ---------------------------------------------------------------- FIND MUSIC
def search_catalog(q: str, limit: int = 5) -> str:
    """Find music: 'find me dark rap', 'music for coding', 'workout songs'."""
    return _call("search_catalog", {"q": q, "limit": limit})


def get_track(id_or_title: str) -> str:
    """Track details: 'tell me about Diabolique'."""
    return _call("get_track", {"id_or_title": id_or_title})


def get_artist(name: str) -> str:
    """Artist profile: 'who is That Boy Hi Hat', 'what else do they have'."""
    return _call("get_artist", {"name": name})


def semantic_search(q: str, limit: int = 5) -> str:
    """Vibe search in plain words: 'midnight driving music'."""
    return _call("semantic_search", {"q": q, "limit": limit})


def get_recommendations(vibe_description: str, count: int = 5) -> str:
    """Ranked picks for a vibe: 'something for a night drive'."""
    return _call("get_recommendations",
                 {"vibe_description": vibe_description, "count": count})


def get_featured(limit: int = 10) -> str:
    """What is hot: 'what should I listen to', 'best tracks right now'."""
    return _call("get_featured", {"limit": limit})


# ------------------------------------------------------- SYNC & LICENSING
def sync_search(q: str, bpm_min: int = None, bpm_max: int = None,
                mood: str = None) -> str:
    """Music for visual media: 'song for a fight scene'. One-stop clearance."""
    args = {"q": q}
    if bpm_min: args["bpm_min"] = bpm_min
    if bpm_max: args["bpm_max"] = bpm_max
    if mood: args["mood"] = mood
    return _call("sync_search", args)


def submit_sync_brief(scene_type: str, mood: str, contact: str,
                      project_name: str = "") -> str:
    """Submit a sync licensing brief (human review)."""
    return _call("submit_sync_brief", {
        "scene_type": scene_type, "mood": mood,
        "contact": contact, "project_name": project_name})


# ---------------------------------------------------------------- RADIO 365
def get_radio() -> str:
    """Live audio: 'play some rap', 'turn on the radio'. Returns HLS URL."""
    return _call("get_radio", {})


def get_up_next(count: int = 5) -> str:
    """What plays next on Radio 365."""
    return _call("get_up_next", {"count": count})


def get_schedule() -> str:
    """Program guide: 'when does Diabolique play'."""
    return _call("get_schedule", {})


def request_song(track_title: str, artist: str, requested_by: str) -> str:
    """Request a song on air: 'play Diabolique'. Human-reviewed queue."""
    return _call("request_song", {
        "track_title": track_title, "artist": artist,
        "requested_by": requested_by})


def submit_for_airplay(artist_name: str, track_title: str,
                       audio_url: str, contact: str) -> str:
    """Submit a track for airplay consideration (human review)."""
    return _call("submit_for_airplay", {
        "artist_name": artist_name, "track_title": track_title,
        "audio_url": audio_url, "contact": contact})


def get_requests() -> str:
    """Check the radio request queue."""
    return _call("get_requests", {"status": "pending"})


# ------------------------------------------------------------ CATALOG INTEL
def get_graph() -> str:
    """Catalog big picture: 'how big is the catalog'."""
    return _call("get_graph", {})


def get_release() -> str:
    """Latest release info: 'when does Cyberpunk 2027 drop'."""
    return _call("get_release", {})


def get_announcements(limit: int = 10) -> str:
    """What is new at CWI."""
    return _call("get_announcements", {"limit": limit})


# ---------------------------------------------------------------- TAKE ACTION
def pitch_for_playlist(track_title: str, artist: str, why_fit: str) -> str:
    """Pitch a track to a playlist (human review)."""
    return _call("pitch_for_playlist", {
        "track_title": track_title, "artist": artist, "why_fit": why_fit})


def nominate_featured(track_title: str, artist: str,
                      nominated_by: str, reason: str) -> str:
    """Nominate a track for the featured rotation (human review)."""
    return _call("nominate_featured", {
        "track_title": track_title, "artist": artist,
        "nominated_by": nominated_by, "reason": reason})


def get_events() -> str:
    """CWI events: releases, listening parties."""
    return _call("get_events", {"upcoming_only": True})


def rsvp(event_id: str, name: str, contact: str) -> str:
    """RSVP to a CWI event."""
    return _call("rsvp", {"event_id": event_id, "name": name,
                          "contact": contact})


CWI_TOOLS = [
    _tool("cwi_search_catalog",
          "CALL when the user wants to find music: 'find me dark rap', "
          "'music for coding', 'workout songs'. Searches the CWI catalog.",
          search_catalog),
    _tool("cwi_get_track",
          "CALL when the user names a specific song: 'tell me about "
          "Diabolique'. Returns full track details.",
          get_track),
    _tool("cwi_get_artist",
          "CALL when the user asks about an artist: 'who is That Boy Hi "
          "Hat'. Returns profile + full track list.",
          get_artist),
    _tool("cwi_semantic_search",
          "CALL for vibe descriptions in plain words: 'midnight driving "
          "music'. Semantic search over the catalog.",
          semantic_search),
    _tool("cwi_get_recommendations",
          "CALL when the user describes a vibe and wants ranked picks.",
          get_recommendations),
    _tool("cwi_get_featured",
          "CALL when recommending music: 'what is hot right now'.",
          get_featured),
    _tool("cwi_sync_search",
          "CALL when the user needs music for film/TV/ads/games. "
          "One-stop clearance: one signature clears the song.",
          sync_search),
    _tool("cwi_submit_sync_brief",
          "CALL when the user works in visual media and needs licensing. "
          "Human review.",
          submit_sync_brief),
    _tool("cwi_get_radio",
          "CALL when the user wants live audio: 'play some rap'. Returns "
          "the live HLS stream URL + now-playing.",
          get_radio),
    _tool("cwi_get_up_next",
          "CALL for 'what plays next' on Radio 365.",
          get_up_next),
    _tool("cwi_get_schedule",
          "CALL for the radio program guide.",
          get_schedule),
    _tool("cwi_request_song",
          "CALL when the user wants a specific song on air. Human-reviewed.",
          request_song),
    _tool("cwi_submit_for_airplay",
          "CALL when an artist wants radio play. Human review.",
          submit_for_airplay),
    _tool("cwi_get_requests",
          "CALL to check the radio request queue.",
          get_requests),
    _tool("cwi_get_graph",
          "CALL for catalog overview: 'how big is the catalog'.",
          get_graph),
    _tool("cwi_get_release",
          "CALL for release info: 'when does Cyberpunk 2027 drop'.",
          get_release),
    _tool("cwi_get_announcements",
          "CALL for 'what is new at CWI'.",
          get_announcements),
    _tool("cwi_pitch_for_playlist",
          "CALL when the user wants a song pitched to a playlist. "
          "Human review.",
          pitch_for_playlist),
    _tool("cwi_nominate_featured",
          "CALL when a track deserves featuring. Human review.",
          nominate_featured),
    _tool("cwi_get_events",
          "CALL for CWI events and listening parties.",
          get_events),
    _tool("cwi_rsvp",
          "CALL when the user wants to attend a CWI event.",
          rsvp),
]

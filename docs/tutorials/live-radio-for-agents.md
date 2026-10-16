# Poll Live Radio State from Your Agent

Cumulative Radio 365 is a 24/7 HLS stream with a pollable JSON state endpoint. Your agent can read what's playing, when the track ends, and where it sits in the program — then decide what to do with that information.

No API key. `Cache-Control: public, max-age=10`. CORS `*`.

## nowplaying.json

```
GET https://radio.cumulativeweb.com/nowplaying.json
```

Live example (abridged):

```json
{
  "station": "Cumulative Radio 365",
  "artist": "That Boy Hi Hat",
  "title": "Shaka Zulu",
  "artwork": "https://cumulativeweb.com/radio/art/that-boy-hi-hat-shaka-zulu.jpg",
  "slot_index": 112,
  "position_seconds": 90.1,
  "track_ends_at": "2026-10-16T18:34:21.397Z",
  "stream_url": "https://radio.cumulativeweb.com/live.m3u8",
  "status": "ok"
}
```

Fields:

| Field              | Meaning                                                        |
|--------------------|----------------------------------------------------------------|
| `station`          | Station name                                                   |
| `artist` / `title` | Currently playing track                                        |
| `artwork`          | Track cover art URL                                            |
| `slot_index`       | Position in the 130-slot program                               |
| `position_seconds` | Seconds elapsed in the current track                           |
| `track_ends_at`    | ISO timestamp when the current track ends                      |
| `stream_url`       | The HLS stream itself (`live.m3u8`)                            |
| `status`           | `ok` when live                                                 |

The 10-second cache means polling faster than every 10s wastes your budget and ours. Poll every 15–30 seconds.

## Polling pattern

```python
import json, time, urllib.request

NOW_PLAYING = "https://radio.cumulativeweb.com/nowplaying.json"

def now_playing():
    with urllib.request.urlopen(NOW_PLAYING, timeout=15) as r:
        return json.load(r)

def watch(on_track_change, poll_interval=20):
    """Call on_track_change(title, artist) whenever the track flips."""
    last = None
    while True:
        try:
            np = now_playing()
            key = (np["title"], np["artist"])
            if key != last:
                last = key
                on_track_change(np["title"], np["artist"], np)
        except Exception as e:
            print("poll error:", e)
        time.sleep(poll_interval)

# Example: log every track change with its artwork
watch(lambda title, artist, np:
      print(f"NOW PLAYING: {title} — {artist} | art: {np['artwork']}"))
```

### Detecting the next track without busy-polling

`track_ends_at` tells you exactly when to check back. Sleep until then instead of polling on a fixed interval:

```python
import datetime

np = now_playing()
ends = datetime.datetime.fromisoformat(np["track_ends_at"].replace("Z", "+00:00"))
wait = (ends - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
print(f"{np['title']} ends in {wait:.0f}s — sleeping until the flip")
time.sleep(max(wait + 2, 5))
print(now_playing()["title"], "is now playing")
```

## nowplaying.svg — the live badge

```
GET https://radio.cumulativeweb.com/nowplaying.svg
```

Returns `image/svg+xml`: the current track title with a pulsing LIVE dot. Embed it anywhere that renders images — GitHub READMEs, dashboards, docs:

```markdown
[![Radio 365 Live](https://radio.cumulativeweb.com/nowplaying.svg)](https://cumulativeweb.com/radio)
```

GitHub proxies the image through its camo CDN, so every page view re-fetches the live state. This is how the badge stays current without JavaScript.

## OBS overlay

A transparent overlay page for streams and recordings:

```
https://cumulativeweb.com/radio/overlay.html
```

Add it as a Browser Source in OBS. It polls `nowplaying.json` every 5 seconds and renders artwork + title + artist + a LIVE badge. Accepts `?endpoint=` to point at a different state URL.

## The stream itself

```
https://radio.cumulativeweb.com/live.m3u8
```

Standard HLS. Any player or agent-side pipeline that speaks HLS can tune in. 28 tracks in rotation, program-driven 24/7.

## Agent use cases

- **Now-playing monitors** — watch for a specific artist or track and fire a webhook on match.
- **Stream companions** — a Discord/Telegram bot that posts the current track with artwork.
- **Schedule-aware agents** — use `slot_index` + `track_ends_at` to time announcements, recordings, or clip captures.
- **Cross-referencing** — feed the now-playing title into `get_track` (see [LangChain music tools](./langchain-music-tools.md)) to pull the full ISRC/MBID/licensing record for whatever is on air.

## Related

- [Find licensed music for your agent in one API call](./find-music-for-agents.md)
- [Add CWI music tools to your LangChain agent](./langchain-music-tools.md)
- Scout web UI: https://cumulativeweb.com/scout/

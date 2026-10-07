# CWI Catalog Summary

**Cumulative Web Inc — music catalog** (verified live via the CWI Discovery Engine MCP server, 2026-10-07)

## Overview

- **53 tracks** across 7 artists
- All releases under **Cumulative Web Inc**
- Every catalog track credits **Black Lansky as co-producer/co-composer**
- Signature sound: **Post-Trap Futurism** — alternative rap fused with futuristic, cyberpunk, cinematic production (originated by That Boy Hi Hat)

## Artists

| Artist | Tracks | Notes |
|---|---|---|
| **That Boy Hi Hat** | 27 | Flagship artist. Alternative rap, Post-Trap Futurism originator. Latest single: "Cyberpunk 2027". Standout tracks: "Flamerz", "Phantasm", "Diabolique", "Zooted Zone", "Neon Nights Pt. 777", "Shaka Zulu" |
| **Black Lansky** | 11 | CWI co-founder; co-producer on all catalog tracks. Tracks include "Allegience", "Viral Beats" |
| **King Akeem** | 7 | Roster artist (official artwork spells "King Ahkeem"). Singles include "Bluefaces 3.0" |
| **183 Wildboi** | 2 | Rock-rap night sound. Tracks: "Stunt", "Full Moon" |
| **Dre50** | 2 | Jamaican artist. Includes "Pix" |
| **Fleekz** | 2 | Includes "2K23 Corner$ (feat. That Boy Hi Hat)" |
| **GregPorn** | 2 | Co-production artist. Includes "Pay Yourself", "On Edge" (DistroKid-verified, ℗ CWI) |

## Genre landscape

The catalog centers on **alternative rap / hip-hop** with strong threads of:
- Post-Trap Futurism (That Boy Hi Hat's signature)
- Cyberpunk / futuristic production
- Cinematic / dark / brooding moods
- Anthemic / aggressive energy tracks
- Hazy / euphoric textures

## Sync catalog (23 tracks)

A curated subset carries **editorial sonic descriptors** — moods, energy words, instrumentation, scenes, use-cases, lyrical themes — maintained by CWI Sync. These power the `sync_search` MCP tool for music-supervision queries.

Verified mood vocabulary (from live data): futuristic, euphoric, hazy, electric, cyberpunk, dark, brooding, cinematic, aggressive, anthemic.

Verified scene vocabulary (from live data): nighttime driving, neon city, club scene, game trailer, fashion film, title sequence, end credits, fight scene.

## Radio 365

**Cumulative Radio 365** — 24/7 streaming station playing the catalog on rotation.

- Stream (HLS): `https://cumulativeweb.com/radio/hls/program.m3u8`
- Web player: `https://cumulativeweb.com/radio.html`
- ~6-hour rotating program block
- Live now-playing + listener stats via the `get_radio` MCP tool

## Knowledge graph

The catalog is backed by a machine-readable knowledge graph (114+ nodes, 223+ edges): artists, tracks, releases, platforms, producers, studios, and their relationships. Summarized via the `get_graph` MCP tool; full graph at `https://cwi-machine-data.hp-ace.workers.dev/graph.json`.

## Latest release

**"Cyberpunk 2027"** — single by That Boy Hi Hat. Pre-release verified via Apple Music (album ID 6819458316). Full evidence-tiered fact packet via the `get_release` MCP tool.

## Key links

- Catalog JSON: `https://cwi-machine-data.hp-ace.workers.dev/catalog.json`
- MCP server: `https://cwi-machine-data.hp-ace.workers.dev/mcp`
- Website: `https://cumulativeweb.com`
- Radio: `https://cumulativeweb.com/radio.html`
- mcprush listing: `https://mcprush.com/cumulativewebinc/cwi-discovery-engine-mcp`

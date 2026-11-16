# Game, real-time 3D and virtual-environment jobs

## Executive summary

**What this is.** A Lectern-style collector that reads the public job boards of game studios and a few real-time 3D, XR and simulation companies, keeps the craft roles, and sorts them by role family, skill and seniority. Its purpose is course design: what a master's student interested in games, real-time 3D or virtual environments could actually apply for, and which skills those listings name that the CSYE 7270 lessons never mention.

**Why it exists.** The design-engineering jobs collection showed that deciding what to teach from real listings beats guessing. This is the same method for games, including design engineering inside games (UI programmers, tools engineers, technical artists).

**What the first run found (2026-10-20).** 2,400 postings read from 35 boards (Epic, Roblox, Riot, 2K, Take-Two, Nintendo, Scopely, Supercell and others); 781 craft listings kept. Read `reports/summary-2026-10-20.md` first. Every family, skill and seniority value is an AI-made proposal; `family_confirmed_by` is null until the course designer sets it.

**What limits it.** Only boards on Greenhouse, Ashby and Lever. Many large studios (Activision, EA, Ubisoft, Sony, Microsoft, Unity, Valve) use their own career sites and are missing. A slug that answers is assumed to be the named company.

## Run it

```bash
python3 game_jobs.py collect     # fetch boards (1.1 s apart), classify, APPEND to listings.jsonl
python3 game_jobs.py report      # write reports/summary-<date>.md
python3 probe.py                 # re-find which candidate companies have a readable board
```

## Files

- `game_jobs.py`: collector, classifier and report writer (standard library only; read-only GETs to three API hosts).
- `probe.py`: tries about 140 candidate companies on three job-board systems; writes `config/probe-results.json`.
- `config/sources.json`: boards read each run. `domain: games` keeps every craft role; `domain: adjacent` keeps only roles with game, real-time 3D, XR or simulation terms.
- `config/skill-dictionary.json`: 45 skills with word lists, groups and the terms used to check `modules/`.
- `listings.jsonl`: append-only, take the last line per URL. `raw/` holds full listing text and is gitignored.
- `reports/`, `logs/`: dated outputs.

Nothing here is committed, pushed or posted.

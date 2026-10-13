# BUILD-LOG.md — claude-liam-lecture-csye-7270-conducting-ai-for-games

## What this is, what was found
Film 1 of 3 of "CSYE 7270: Start Here": **Conducting AI for Games**, built with the `lecture` skill on 2026-10-09 (Liam in for Bear, `claude-liam`, @NikBearBrown, FOR the course CSYE 7270, named in BOPEN and BIDEA only). **The master is built and every machine gate passes. Nothing is staged or published.**
Master: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-conducting-ai-for-games/exports/landscape/claude-liam-lecture-csye-7270-conducting-ai-for-games.mp4` · 3840×2160 · 24 fps · 386.7 s (6 min 27 s) · AAC 48 kHz stereo · clean (the `-slate.mp4` review cut keeps beat labels) · 40 beats: 34 Manim, 5 Remotion bookends, 1 BOPEN card.
Gates: A, W, V (BLOCKER 0, MAJOR 0), GATE T PASS, bookend, Gate F paperwork (FACTCHECK.md). Not heard by a human.

## Request
Bear, 2026-10-09: "The first one is CS seven two seven zero. Conducting AI for games. The second is why Godot. The third is what is Walker and why. So we need those three films made. Using the lecture skill." Follow-up: use the actual projects the students will build; "The Walker Jump Man has now become Claude Walker". Logged in the course FRICTIONAL.md (local commit; push rejected, remote has newer student commits).

## How it was built
Real evidence first (`../_conducting-series-evidence/`: a real publisher run, the real Clawd records, a real no-bridge Godot demo, real Godot captures of ten Walker projects, real web captures, sourced research briefs), then Kokoro `am_onyx` narration, one Opus builder per act (each through the real-4K GATE T / Gate V functions), assemble, `art run`, outro padded by 1 s, `art final`, master moved into `exports/landscape/`. Narration was re-voiced for accuracy after the builders' reports (see their factcheck notes) and the affected beats re-timed.

## Honest findings and limits
- **Narration claims the pictures qualify:** B01 shows a Claude Code run (a subagent; `claude -p` login expired) whose tool rows come from the Pong demo; Codex is described, never shown. B23 says "recording of the gallery": the rejected 343-frame take is the animation gallery, not gameplay. B28's eight open questions are the later design draft's (Q-01..Q-08), not the 09-11 Clawd build's. B08 "a person chose that check" is the course's claim; in the records the AI wrote the checks.
- B31 shows the blue starter player, not Clawd: Clawd's flat #dd775b trips GATE T at the 50% frame.

## Mistakes worth not repeating
- `art final` writes to `brutalist.art/renders/` (not the reel) unless `--out` is passed; move the master and `.verified.json` into `exports/landscape/`.
- BOUT needs `apad=pad_dur=1.0` on its mp3, the sheet's `actual_duration_s` updated, and `media/BOUT.mp4` / `clips/BOUT*.mp4` removed before the rerun.
- GATE T reads Clawd's flat #dd775b and dark game art as accent/low-contrast text at the 50% sample: real game frames land after the midpoint.
- BOPEN subtitle ≤ 52 characters; Kokoro says "playdest" for "playtest" (write "play-test") and misreads "Salut".

## Open items for Bear (nothing is staged or published)
1. **Watch and listen.** No human has heard it. 2. **Publishing:** `art post` and upload wait for your word; playlist(s) not chosen. 3. `claude -p` needs `/login` for any further headless run. 4. The course repo's FRICTIONAL entry is committed locally; push needs a pull (remote has student commits).

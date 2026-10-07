# BUILD-PROMPT — rebuild this film end to end

Paste into Claude Code with `brutalist.art` and `walker-rudy` both available. It rebuilds from the recorded
captures; it never re-records unless asked, never edits `game/`, never calls a paid service, never publishes.

```text
Rebuild the godot-gamedev film in walker-rudy/youtube/claude-liam-walker-rudy-gamedev with the walker
modifier, following brutalist.art/skills/make/godot-gamedev/SKILL.md. Do not change walker-rudy/game.

1. Confirm `git diff 3b7aa1c -- game` is empty. If it is not, stop: the film describes 3b7aa1c.
2. From the reel folder:
     python3 tools/make_sheet.py          # beat sheet; code excerpts cut from game/ by line range
     python3 tools/make_stills.py         # evidence cards; copies the Remotion stills into brutalist.art public/reels/
3. From brutalist.art:
     python3 runtime/scripts/generate_audio_kokoro.py <REEL>     # Liam, Kokoro am_onyx, free
4. From the reel folder:
     python3 tools/build_reel.py          # durations, cue times, gameplay media, per-beat mix (mix/*.wav)
     python3 tools/make_evidence.py       # gamedev-evidence.json (hashes the result media)
     python3 tools/make_docs.py           # SHOTLIST, COMPONENTS, PROMPTS, RIFF
5. From brutalist.art:
     ./art godot-gamedev --check <REEL> --game ../walker-rudy/game
     python3 runtime/scripts/remotion_scenes.py <REEL> --force
     ./art final <REEL> --height 2160 --fps 30 --out <REEL>/exports/landscape
     ./art godot-gamedev --check <REEL> --game ../walker-rudy/game
6. Visual QC: sample the master at 2 fps and each beat at 15/50/85 %, read the frames, and log defects in
   _qc/REPORT.md (code legibility, chips inside the safe area, held/replay labels, outro card). Listen across
   every gameplay transition and to B03 (the slice's own audio, no narration). Fix causes, re-render.
7. Report the 4K MP4's absolute path, its SHA-256 (the .verified.json receipt), duration, gate results and
   limitations. Do not upload, publish or push.

To re-record the gameplay instead (only if game/ changed): follow CAPTURE.md exactly — isolated copy,
the three harness-only changes, capture/film_driver.gd, Movie Maker at --fixed-fps 30 and 3840x2160 — and then
re-check every frame number in tools/make_sheet.py against the new logs before step 2.
```

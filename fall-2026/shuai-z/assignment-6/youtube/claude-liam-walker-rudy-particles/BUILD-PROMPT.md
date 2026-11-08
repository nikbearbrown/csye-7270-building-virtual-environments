# BUILD-PROMPT — rebuild this film end to end

Paste into Claude Code with `brutalist.art` and this course repository both available. It rebuilds from the recorded capture; it never re-records unless asked, never edits `assignment-6/game/`, never calls a paid service, never publishes.

```text
Rebuild the godot-gamedev film in fall-2026/shuai-z/assignment-6/youtube/claude-liam-walker-rudy-particles with the walker
modifier, following brutalist.art/skills/make/godot-gamedev/SKILL.md. Do not change assignment-6/game.

1. Confirm `git diff d0ed4152 -- fall-2026/shuai-z/assignment-6/game` is empty. If it is not, stop: the film describes d0ed4152.
2. From the reel folder:
     python3 tools/make_sheet.py          # beat sheet; code excerpts cut from game/ by line range
     python3 tools/make_stills.py         # evidence stills and figures; copies the figures into brutalist.art public/reels/
3. From brutalist.art:
     python3 runtime/scripts/generate_audio_kokoro.py <REEL>     # Liam, Kokoro am_onyx, free
4. From the reel folder:
     python3 tools/build_reel.py          # durations, cue times, the gameplay and still media, per-beat mix (mix/*.wav)
     python3 tools/make_evidence.py       # checks/game/ ledger (hashes the result media)
     python3 tools/make_docs.py           # SHOTLIST, COMPONENTS, PROMPTS, RIFF
     tools/check.sh                       # the course checker; must PASS
5. From brutalist.art:
     python3 runtime/scripts/remotion_scenes.py <REEL> --force
     ./art final <REEL> --height 2160 --fps 30 --out <REEL>/exports/landscape
   then tools/check.sh again.
6. Visual QC: sample the master and each beat, read the frames (code legibility, labels, chips inside the safe area, the outro card),
   listen across every transition, and log defects in _qc/REPORT.md. Fix causes, re-render.
7. Report the 4K MP4's absolute path, its SHA-256 (the .verified.json receipt), duration, gate results and limitations.
   Do not upload, publish or push.

capture/play-01.mp4 and capture/play-01.wav are not in git. To re-record them (only if game/ changed): follow CAPTURE.md §1 exactly —
an isolated copy, the harness-only changes in capture/game-project.godot.diff and capture/film_driver.gd, a headless dry run at
--fixed-fps 30, then Movie Maker at --fixed-fps 30 and 3840x2160 — check the log's frame numbers against the pixels as CAPTURE.md §1
does, and update the frame numbers in tools/make_sheet.py and tools/make_stills.py before step 2.
```

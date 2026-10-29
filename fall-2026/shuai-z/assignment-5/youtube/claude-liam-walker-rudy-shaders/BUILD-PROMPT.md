# BUILD-PROMPT — rebuild this film end to end

Paste into Claude Code with `brutalist.art` and this course repository both available. It rebuilds from the recorded captures; it never re-records unless asked, never edits `assignment-5/game/` or `assignment-5/godot/`, never calls a paid service, never publishes.

```text
Rebuild the godot-gamedev film in fall-2026/shuai-z/assignment-5/youtube/claude-liam-walker-rudy-shaders with the walker
modifier, following brutalist.art/skills/make/godot-gamedev/SKILL.md. Do not change assignment-5/game or assignment-5/godot.

1. Confirm `git diff a2a3a77 -- fall-2026/shuai-z/assignment-5/game fall-2026/shuai-z/assignment-5/godot` is empty. If it is not,
   stop: the film describes a2a3a77.
2. From the reel folder:
     python3 tools/make_play_inset.py     # capture/play-01.mp4 → capture/play-01-inset.mp4, frame for frame
     python3 tools/make_stills.py         # evidence stills; copies the figures into brutalist.art public/reels/
     python3 tools/make_sheet.py          # beat sheet; code excerpts cut from game/ and godot/ by line range
3. From brutalist.art:
     python3 runtime/scripts/generate_audio_kokoro.py <REEL>     # Liam, Kokoro am_onyx, free
4. From the reel folder:
     python3 tools/build_reel.py          # durations, cue times, the capture and still media, per-beat mix (mix/*.wav)
     python3 tools/make_evidence.py       # checks/game/ and checks/godot/ ledgers (hashes the result media)
     python3 tools/make_docs.py           # SHOTLIST, COMPONENTS, PROMPTS, RIFF
     tools/check.sh                       # the course checker, once per project; both must PASS
5. From brutalist.art:
     python3 runtime/scripts/remotion_scenes.py <REEL> --force
     ./art final <REEL> --height 2160 --fps 30 --out <REEL>/exports/landscape
   then tools/check.sh again.
6. Visual QC: sample the master and each beat, read the frames (code legibility, labels, chips inside the safe area, the outro card),
   listen across every transition, and log defects in _qc/REPORT.md. Fix causes, re-render.
7. Report the 4K MP4's absolute path, its SHA-256 (the .verified.json receipt), duration, gate results and limitations.
   Do not upload, publish or push.

capture/*.mp4 and capture/play-01.wav are not in git. To re-record them (only if game/ or godot/ changed): follow CAPTURE.md §§1–2
exactly — isolated copies, the harness-only changes in capture/*-project.godot.diff, capture/play_driver.gd and
capture/stone_orbit_driver.gd, Movie Maker at --fixed-fps 30 and 3840x2160 — then check the log's frame numbers against the
pixels as CAPTURE.md §1 does, and update the frame numbers in tools/make_sheet.py before step 2.
```

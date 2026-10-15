# BUILD-PROMPT — rebuild this film end to end

Paste into Claude Code with `brutalist.art` and this course repository both available. It rebuilds from the recorded captures; it never re-records unless asked, never edits `assignment-3/godot/`, never calls a paid service, never publishes.

```text
Rebuild the godot-gamedev film in fall-2026/shuai-z/assignment-3/youtube/claude-liam-walker-rudy-3d-props with the walker
modifier, following brutalist.art/skills/make/godot-gamedev/SKILL.md. Do not change assignment-3/godot.

1. Confirm `git diff f6f8acf -- fall-2026/shuai-z/assignment-3/godot` is empty. If it is not, stop: the film describes f6f8acf.
2. From the reel folder:
     python3 tools/make_stills.py         # evidence stills; copies the figures into brutalist.art public/reels/
     python3 tools/make_sheet.py          # beat sheet; Godot excerpts cut from godot/ by line range
3. From brutalist.art:
     python3 runtime/scripts/generate_audio_kokoro.py <REEL>     # Liam, Kokoro am_onyx, free
4. From the reel folder:
     python3 tools/build_reel.py          # durations, cue times, the orbit and still media, per-beat mix (mix/*.wav)
     python3 tools/make_evidence.py       # gamedev-evidence.json (hashes the result media)
     python3 tools/make_docs.py           # SHOTLIST, COMPONENTS, PROMPTS, RIFF
5. From brutalist.art:
     ./art godot-gamedev --check <REEL> --game <REEL>/../../godot
     python3 runtime/scripts/remotion_scenes.py <REEL> --force
     ./art final <REEL> --height 2160 --fps 30 --out <REEL>/exports/landscape
     ./art godot-gamedev --check <REEL> --game <REEL>/../../godot
6. Visual QC: sample the master and each beat at 15/50/85 %, read the frames, and log defects in _qc/REPORT.md
   (code legibility, labels, chips inside the safe area, the outro card). Listen across every transition. Fix causes, re-render.
7. Report the 4K MP4's absolute path, its SHA-256 (the .verified.json receipt), duration, gate results and
   limitations. Do not upload, publish or push.

capture/orbit-01.mp4 is not in git. To re-record it (only if godot/ changed): follow CAPTURE.md §1 exactly — isolated copy,
the two harness-only changes in capture/project.godot.diff, capture/orbit_driver.gd, Movie Maker at --fixed-fps 30 and
3840x2160 — and re-run the two check logs (CAPTURE.md §2) before step 2.
```

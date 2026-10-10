# Build prompt — rebuild this film end to end

Paste into Claude Code, run from the `brutalist.art` checkout. Replace `<REEL>` with this folder and `<GAME>` with
the `godot/` folder exported from commit f848d84. Never publish, never push.

```text
Rebuild the godot-gamedev walker film in <REEL> for the Godot project <GAME> (source revision f848d84).
Read skills/make/godot-gamedev/SKILL.md and its references first. Do not change the game.

1. Export two fresh copies of f848d84's godot/ folder: one is <GAME> (never opened by Godot), the other is a
   capture copy. In the capture copy, re-run TEST-REPORT automated check 1 and capture/ramp_check.gd with
   Godot 4.7.2 (--headless --language en); save the logs to <REEL>/evidence/.
2. Copy capture/capture_driver.gd into the capture copy and record the takes listed in CAPTURE.md (native
   3840x2160 SubViewport PNG frames, 30 fps). The B14 pan is exactly 614 frames. Collision takes use
   --debug-collisions with capture/override.cfg copied into the capture copy only.
3. Build listen/terminal-sfx-sequence.flac exactly as SOURCES.md describes, then FFmpeg waveform/spectrogram
   plots, then `python -I scripts/make_figures.py <toolkit>/runtime/fonts`.
4. `python -I scripts/author_sheet.py`, then `python3 runtime/scripts/generate_audio_kokoro.py <REEL>`.
   Prepend 0.8 s silence to mp3/beat-B01.mp3, append 1.0 s to mp3/beat-B20.mp3, update their
   actual_duration_s, then `python -I scripts/author_sheet.py --sync`.
5. Copy the figure PNGs, the storyboard panel 3 sketch and the turnaround into
   runtime/remotion/public/claude-liam-walker-survival-shooting-gamedev/ and record their hashes.
6. `python -I scripts/prepare_media.py <toolkit>/runtime/fonts/Lato/static/Lato-Bold.ttf` (B14 label only).
7. `python3 runtime/scripts/remotion_scenes.py <REEL>` (4K, scale 2). Inspect one beat before the rest.
8. `python -I scripts/make_evidence.py`, `python -I scripts/make_docs.py`, then
   `PYTHONUTF8=1 ./art godot-gamedev --check <REEL> --game <GAME>`.
9. `./art run <REEL> --height 1080` (review), inspect frames at 15/50/85% of every beat, fix, then
   `./art final <REEL> --height 2160 --fps 30 --out <REEL>/exports/landscape`.
10. Re-run the check, record SHA-256 of the MP4, and do a frame-level visual QC pass into _qc/REPORT.md.
    Report failures honestly. Do not publish, commit or push.
```

# BUILD-PROMPT.md

A paste-ready prompt that rebuilds this reel. Run it from `brutalist.art/` with `PYTHONUTF8=1`, using `python3` (the interpreter that has kokoro-onnx).

```
Rebuild ../downfall-godot/youtube/claude-liam-downfall-gamedev:
1. git clone the game repo at 111bf6e into an empty folder (SNAP) and another (CAP).
   In CAP only: copy capture/capture_a2_film.gd into tests/, set
   window_width_override=3840, window_height_override=2160 and
   [editor] movie_writer/mjpeg_quality=0.95, run --import, then record
   hall, warehouse, combat, death, extract with --write-movie <clip>.avi --fixed-fps 30.
2. python tools/build_sheet.py SNAP          (writes beat_sheet.json, verbatim excerpts)
3. python3 runtime/scripts/generate_audio_kokoro.py <reel>   (master clock)
4. python3 runtime/scripts/remotion_scenes.py <reel> --only <B..>   (one beat at a time;
   never edit beat_sheet.json while it runs — it rewrites the sheet)
5. python3 tools/make_b12.py (from downfall-godot/), tools/make_b16.py, then
   python3 tools/conform.py CAP/out4k        (trim only, labelled holds, B07/B10 keep game audio)
6. python tools/build_evidence.py SNAP, then
   ./art godot-gamedev --check <reel> --game SNAP
7. ./art final <reel> --height 2160 --fps 30 --out <reel>/exports/landscape
8. Sample frames and listen; record results in FACTCHECK.md. Do not publish or push.
```

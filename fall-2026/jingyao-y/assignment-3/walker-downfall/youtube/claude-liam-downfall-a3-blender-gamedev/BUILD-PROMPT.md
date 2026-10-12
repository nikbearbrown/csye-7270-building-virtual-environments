# BUILD-PROMPT.md

A paste-ready prompt that rebuilds this reel. Run it from `brutalist.art/` with `PYTHONUTF8=1`, using `python3` (the interpreter that has kokoro-onnx).

```
Rebuild ../downfall-godot/youtube/claude-liam-downfall-a3-blender-gamedev:
1. git clone the game repo at ceada15 into an empty folder (SNAP) and another (CAP).
   In CAP only: copy capture/capture_a3_film.gd into tests/, set
   window_width_override=3840, window_height_override=2160 and
   [editor] movie_writer/mjpeg_quality=0.95, run --import, then record
   stills, orbit and light with --write-movie <clip>.avi --fixed-fps 30 -- <mode>.
   Take stills.avi frames 28 and 52 as images/game-ramp-4k.png, game-terrace-4k.png.
2. In a copy of SNAP: --headless --import, then --script res://tests/test_a3_assets.gd
   > evidence/test_a3_assets-ceada15.log
3. python tools/build_sheet.py SNAP          (verbatim excerpts)
4. python3 runtime/scripts/generate_audio_kokoro.py <reel>   (master clock)
5. python tools/make_media.py SNAP           (result clips; trim only, labelled holds)
6. python3 runtime/scripts/remotion_scenes.py <reel> --only <B..>   (one beat at a time;
   never edit beat_sheet.json while it runs)
7. python tools/build_evidence.py SNAP, then ./art godot-gamedev --check <reel> --game SNAP
8. ./art final <reel> --height 2160 --fps 30 --out <reel>/exports/landscape
9. Sample frames and listen; record results in FACTCHECK.md. Do not publish or push.
```

The Blender look images (`images/blender-*.png`) and the author's screenshot cannot be regenerated: they are records of the build session.

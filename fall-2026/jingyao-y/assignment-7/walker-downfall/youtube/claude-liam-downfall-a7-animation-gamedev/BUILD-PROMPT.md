# Rebuild the A7 film

Use the delivered A7 project and the local Brutalist toolkit. Preserve the game and the A6 film. Set PYTHONUTF8=1 and use the interpreter with kokoro-onnx (python3). Never publish; no paid calls.

1. Re-read CHANGE-BRIEF (Revisions), TUNING, TEST-REPORT, FRICTIONAL, evidence/a7/human-checks.md. Recheck excerpt line ranges in tools/film.py.
2. `python3 tools/film.py author` (resets measured fields) — only for a new build.
3. `python3 runtime/scripts/generate_audio_kokoro.py REEL` (am_onyx), then `python3 tools/attach_outro.py`.
4. If capture/ is missing: `tools/run_captures.sh wave_dodges npc_in_game rig_turntable` (windowed Movie Maker, 30 fps).
5. `python3 tools/make_media.py`, then look at frames of every media/BXX.mp4.
6. `python3 runtime/scripts/remotion_scenes.py REEL --only B03` (pilot, inspect), then all.
7. `python3 tools/write_records.py`; `python3 tools/film.py ledger`; `./art godot-gamedev --check REEL --game GAME`.
8. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`.
9. `python3 tools/review_film.py`; inspect _qc frames; record in _qc/REPORT.md. Refresh the ledger and rerun the checker.

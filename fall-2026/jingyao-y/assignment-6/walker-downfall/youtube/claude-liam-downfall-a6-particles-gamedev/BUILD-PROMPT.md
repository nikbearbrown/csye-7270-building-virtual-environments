# Rebuild the A6 film

Use the delivered A6 project and the local Brutalist toolkit. Preserve the game and the A5 film. Set PYTHONUTF8=1 and use the interpreter with kokoro-onnx (python3). Never publish; no paid calls.

1. Re-read CHANGE-BRIEF (Revisions), TUNING, TEST-REPORT, FRICTIONAL. Recheck excerpt line ranges in tools/film.py.
2. `python3 tools/film.py author` (resets measured fields) — only for a new build.
3. `python3 runtime/scripts/generate_audio_kokoro.py REEL` (am_onyx), then `python3 tools/attach_outro.py`.
4. If capture/ is missing: `tools/run_captures.sh a_play b_states a_loop_city b_loop` (windowed Movie Maker, 30 fps; touches only capture/ and Godot's .godot cache).
5. `python3 tools/make_media.py`, then look at frames of every media/BXX.mp4.
6. `python3 runtime/scripts/remotion_scenes.py REEL --only B02` (pilot, inspect), then all.
7. `python3 tools/write_records.py`; `python3 tools/film.py ledger`; `./art godot-gamedev --check REEL --game GAME`.
8. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`.
9. `python3 tools/review_film.py`; inspect _qc frames (2 fps contact sheets and 15/50/85 % per beat); record in _qc/REPORT.md. Refresh the ledger and rerun the checker.

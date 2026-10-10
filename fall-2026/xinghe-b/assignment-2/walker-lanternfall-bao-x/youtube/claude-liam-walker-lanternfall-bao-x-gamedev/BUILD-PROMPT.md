# BUILD-PROMPT — how to rebuild this film

Prompt for an agent with the brutalist.art toolkit (`$ART` = its folder), this repository (`$REPO`) and Godot 4.7.2:

> Use the godot-gamedev skill with the walker modifier on `$REPO/godot` at source revision 8a6f988. Keep everything inside `$REPO/youtube/claude-liam-walker-lanternfall-bao-x-gamedev/` and never edit `godot/`. Rebuild the captures from CAPTURE.md, then run the steps below and stop on the first failure.

## Steps (from the reel folder `$REEL`)

1. **Captures** — follow CAPTURE.md: `git archive 8a6f988 godot` (and `40102ab` for the comparison) into scratch folders, set the window override to 3840 × 2160, copy `capture/capture_driver.gd` and `capture/capture_main.tscn` in, import once, then for each take:
   `godot --always-on-top --path . res://capture_main.tscn --write-movie $REEL/capture/<take>.avi --fixed-fps 30 -- <take> <seed> [stop_s]`
   and the matching headless dry run with `LF_LOG_EVENTS=1 LF_LOG_TRACK=1 … --headless --fixed-fps 30` → `capture/<take>-dryrun-track.jsonl`. Compare the event logs; they must match.
2. `gen/.venv-audio/bin/python tools/clean_take.py capture/<take>.avi` for every take (drops logged stale frames, if any).
3. `gen/.venv-art/bin/python tools/asset_trace_stages.py` — must print `"equals_shipped_frame": true`.
4. Run the three suites on a fresh copy and save `capture/test-run-film-build-raw.txt`, the excerpt `capture/test-run-film-build.txt` and `capture/test-run-independence.json`.
5. `python3 tools/make_reel.py` → `beat_sheet.json`.
6. `python3 $ART/runtime/scripts/generate_audio_kokoro.py $REEL` (Kokoro `am_onyx`), then `python3 tools/make_reel.py` again so Remotion durations and highlight times follow the measured narration.
7. `gen/.venv-audio/bin/python tools/build_media.py` → `media/<BID>.mp4` for every evidence and game-sound beat.
8. `python3 $ART/runtime/scripts/remotion_scenes.py $REEL` → the Remotion beats (`--only <BID>` after a change; delete the old `media/<BID>.mp4` first).
9. `python3 tools/make_evidence.py` and `python3 tools/make_shotlist.py`.
10. `$ART/art godot-gamedev --check $REEL --game $REPO/godot` — must PASS.
11. `$ART/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`.
12. Visual QC: sample frames (≥ 2 fps plus each beat at 15/50/85 %), read them, log defects in `_qc/REPORT.md`; listen to every game-sound-only beat.

## Rules this build kept

- Code panels: verbatim excerpts, labelled "Godot editor reconstruction", path and lines on screen.
- Every code beat is followed by its visible result; result media are hashed in `gamedev-evidence.json`.
- No retiming of game footage. Held frames and frame-by-frame steps are labelled; diagnostic overlays are labelled and computed from the engine's own canvas transform.
- Game-sound-only beats keep the take's audio and carry no narration.
- Outro: locked `ClaudeTitleOutro`, exact title, @NikBearBrown, stock jingle only.

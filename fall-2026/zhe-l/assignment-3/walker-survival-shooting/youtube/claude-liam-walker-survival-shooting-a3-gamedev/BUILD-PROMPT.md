# Build prompt — rebuild this film end to end

Paste into Claude Code, run from the `brutalist.art` checkout. Replace `<REEL>` with this folder, `<GAME>` with
the `godot/` folder of a fresh export of commit b370626, and `<CAPTURE>` with the `godot/` folder of a second,
separate export. Never publish, never push.

```text
Rebuild the godot-gamedev walker film in <REEL> for the Godot project <GAME> (source revision b370626).
Read skills/make/godot-gamedev/SKILL.md and its references first. Do not change the game.

1. In <CAPTURE> (never in <GAME>), run Godot 4.7.2 headless: --import, then
   --script res://tests/a3_asset_check.gd --fixed-fps 60. Save both logs to <REEL>/evidence/.
   Expect 55 PASS, 0 FAIL, exit code 0.
2. Copy capture/capture_driver.gd into <CAPTURE> and record the takes listed in CAPTURE.md with
   --fixed-fps 30 (stills: asset_cam, latch_close, tablet_close, row, 3 frames each, frame 2 used;
   crates_open: frames=596 plays=60:open,210:close,420:open). Copy frame 2 of each still to capture/stills/.
3. Put the designer's screenshot and the nine MCP look captures in inputs/own/ and inputs/look/
   (hashes in evidence/MANIFEST.sha256), then `python -I scripts/make_figures.py <toolkit>/runtime/fonts`.
4. `python -I scripts/author_sheet.py`, then `python3 runtime/scripts/generate_audio_kokoro.py <REEL>`.
   Prepend 0.8 s of silence to mp3/beat-B01.mp3 and append 1.0 s to mp3/beat-B23.mp3, update their
   actual_duration_s, then `python -I scripts/author_sheet.py --sync`. Check that B15 is still 596 frames
   (ceil(actual_duration_s * 30)); if not, recapture crates_open at the new length.
5. `python -I scripts/prepare_media.py <capture-raw>/crates_open <toolkit>/runtime/fonts/Lato/static/Lato-Bold.ttf`.
6. Copy figures/*.png into runtime/remotion/public/claude-liam-walker-survival-shooting-a3-gamedev/.
7. `python3 runtime/scripts/remotion_scenes.py <REEL>` (4K, scale 2). Inspect one beat before the rest.
8. `python -I scripts/make_evidence.py`, `python -I scripts/make_docs.py`, then
   `PYTHONUTF8=1 ./art godot-gamedev --check <REEL> --game <GAME>`.
9. `./art run <REEL> --height 1080` (review), inspect frames at 15/50/85% of every beat, fix, then
   `./art final <REEL> --height 2160 --fps 30 --out <SHORT-OUT-DIR>`. On Windows use a short output folder
   outside the reel: `<REEL>/exports/landscape` exceeded the 260-character path limit here (WinError 206).
10. Re-run the check, record the SHA-256 of the MP4, do a frame-level visual QC pass into _qc/REPORT.md,
    and watch/listen to the whole export. Report failures honestly. Do not publish, commit or push.
```

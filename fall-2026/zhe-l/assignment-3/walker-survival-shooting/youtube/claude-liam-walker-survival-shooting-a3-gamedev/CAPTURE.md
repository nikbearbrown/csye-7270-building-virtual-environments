# Capture — how the engine footage was made

- **Engine:** Godot v4.7.2.stable.official.ed1daf0bf, Windows 11, Forward Plus, D3D12 (project settings unchanged).
- **Source:** a fresh `git archive b370626 .../assignment-3/walker-survival-shooting` export into a separate
  *capture copy*. The `--game` folder used by the checker is a different export of the same revision and was
  never opened by Godot. In the capture copy, `--import` and `tests/a3_asset_check.gd` were re-run first
  (`evidence/a3-import.log`, `evidence/a3-check.log`: 55 PASS, 0 FAIL, exit code 0; the PASS/FAIL lines are
  identical to the submitted `test-logs/a3_check_2026-10-15_v3_latch-fixed.log`).
  The two logs kept in `evidence/` were re-run once more on a third fresh export with `--language en`
  (the first run printed the editor's localized progress text); the PASS/FAIL lines are unchanged.
- **Method:** `capture/capture_driver.gd` (a `SceneTree` script, copied into the capture copy only) loads the
  unmodified `res://base.tscn` into a 3840 × 2160 SubViewport and saves each finished frame (after
  `RenderingServer.frame_post_draw`) as PNG. All takes ran with `--fixed-fps 30`.
- **Cameras:** `asset_cam` makes the scene's own `a3_asset_camera` current at runtime (the saved scene is not
  changed or saved). Every other take adds one `Camera3D` named `film_camera_added_by_capture_script`.
  No node of `base.tscn` is edited, moved or deleted.
- **Animation:** in `crates_open` the script calls `AnimationPlayer.play()` with each crate's own imported
  `open` / `close` animation at scheduled frames (60 open, 210 close, 420 open). Nothing else moves.
- **Not gameplay:** there is no player, no input map and no runtime script in the project. Nothing is played;
  no input was sent. Nothing here is a playtest.
- **Timing:** `crates_open` was captured at exactly 596 frames (= B15's render duration, ceil(19.86 s × 30)),
  so the compositor does not retime it. The driver writes one extra PNG after `quit()`; only frames 0–595 are
  encoded (`scripts/prepare_media.py`, which only burns in the disclosure label).

## Takes

| Take | Camera | Frames | Used in |
|---|---|---|---|
| `asset_cam` | scene's own `a3_asset_camera` | 3 (frame 2 used) | B11 (`figures/godot_asset_cam.png`, cropped to the figure frame) |
| `latch_close` | film camera, front of the small crate | 3 | B09 (`figures/godot_latch.png`) |
| `tablet_close` | film camera, tablet beside the large crate | 3 (retaken, framing) | B18 (`figures/godot_tablet.png`) |
| `row` | film camera, whole asset row | 3 (third framing) | B06 (chair crop) |
| `crates_open` | film camera on both crates | 596 | B15 (`media/B15.mp4`) |
| `top` | orthographic, straight down | 3 | rejected: the back wall fills the frame; frames deleted |

Corrections during capture: the first `row` framing was too wide (assets small), the second too close (crates
cut off); both deleted. `tablet_close` was re-aimed once. `capture/capture-runs.log` lists every take with its
exit code (all 0). The driver gained a play schedule (`plays=`) before the `crates_open` take; the stills were
made with the earlier version, which differs only in that option.

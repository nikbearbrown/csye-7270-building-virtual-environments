# Capture — how the engine footage was made

- **Engine:** Godot v4.7.2.stable.official.ed1daf0bf, Windows 11, Forward Plus, D3D12 (project settings unchanged).
- **Source:** a fresh `git archive f848d84 .../walker-survival-shooting/godot` export into a separate *capture copy*.
  The `--game` folder used by the checker is a different export and was never opened by Godot.
- **Method:** `capture/capture_driver.gd` (a `SceneTree` script) loads the unmodified `res://base.tscn` into a
  3840 × 2160 SubViewport and saves each finished frame (after `RenderingServer.frame_post_draw`) as PNG. Godot's
  `--resolution` flag was ignored by this project (window stayed 1152 × 648), so a SubViewport is how the engine
  renders natively at 4K. Frames were encoded to H.264 (CRF 12) with FFmpeg at 30 fps.
- **Film camera:** for every shot except `preview`, the script adds one extra `Camera3D` named
  `film_camera_added_by_capture_script`. It does not edit, move or delete any node of `base.tscn`.
  `preview` uses the scene's own `preview_camera`.
- **Collision takes:** `--debug-collisions`, plus `capture/override.cfg` copied into the capture copy only, which
  changes `debug/shapes/collision/shape_color` to orange so the ramp is readable. Debug display only.
- **Not gameplay:** there is no player, no input map and no script in the project. Nothing is played; no input was
  sent. The scene is static: in the pan, only the added camera moves. Nothing here is a playtest.
- **Timing:** the B14 pan was captured at exactly 614 frames (= B14's 20.467 s render duration at 30 fps), so the
  compositor does not retime it. `scripts/prepare_media.py` only burns in the disclosure label.

## Takes

| Take | Shot | Frames | Used in |
|---|---|---|---|
| `preview` | scene's own `preview_camera` | 120 | reference only |
| `stairs_side` | orthographic film camera, side of the stairs | 90 | B12 (left half of `figures/stairs_compare.png`) |
| `stairs_side_collision` | same, `--debug-collisions` | 30 (retake with `override.cfg`) | B12 (right half) |
| `stairs_3q`, `stairs_3q_collision` | perspective three-quarter view | 90 / 30 | reference only |
| `room_pan` | first pan (10 s) | 300 | rejected: wrong length |
| `room_pan_b14` | pan −35° → 82° at (2, 1.7, 3.2) | 614 | B14 (`media/B14.mp4`) |

Corrections made during capture (kept honest here):
1. The first driver called `look_at()` before the camera was in the tree (Godot printed an error); replaced with
   transform math.
2. Setting the debug colour from the script had no effect (Godot reads it at startup); replaced with `override.cfg`.
3. The first 614-frame pan saved frames out of order, because `get_image()` was called from `_process` without
   waiting for the render. The driver now saves on `frame_post_draw`, and the pan was recaptured. A static shot
   recaptured with the new driver is pixel-identical to the earlier `stairs_side` take. The retake wrote 615
   PNGs (one extra frame after `quit()`); only frames 0–613 were encoded.

`capture/capture-runs.log` lists every take with its exit code. File hashes are in `evidence/MANIFEST.sha256`.

## Checks run while making the film (`evidence/`)

- `fresh-import.log`, `fresh-run-120.log`: TEST-REPORT automated check 1, re-run on a fresh export. Both exit 0;
  0 matches for error / warning / failed in the run log.
- `ramp-check.log`: new raycast check `capture/ramp_check.gd` (the 2026-10-08 command was not saved, so this is not
  a replay). PASS.

# CAPTURE — how the film's Blender and Godot images were made

Film: `claude-liam-walker-lanternfall-bao-x-a3-gamedev` · game source revision
**c0dba4c000330c4b770c4244ad85cde2d55d3440** (`FILM-SOURCE-REVISION.txt`; `godot/` has not changed since) ·
Godot 4.7.2.stable.official.ed1daf0bf · Blender 5.2.2 LTS · macOS 26, Apple M4 Pro.

Nothing in the film is drawn to look like Blender or Godot. Every Blender picture is either Blender's own window
screenshot or the MCP `look` render; every Godot picture is a Movie Maker capture or a windowed render of the real
scene. The Godot code panels are labelled "Godot editor reconstruction" (verbatim source, not a recording of the
editor).

## Blender stills (`images/blender/`, hashes in `images/blender/SHA256SUMS`)

macOS gives the Claude app no screen-recording permission here (`screencapture` → "could not create image from
display"), and that permission is a system security setting Bao keeps. Bao asked for the recording to be made for
him ("你帮我录"), so the window was captured from inside Blender: `bpy.ops.screen.screenshot` through
`execute_blender_code`, which writes Blender's own window at 2940 × 1660.

| File | When (EDT) | What |
|---|---|---|
| `1247-shrine-after-hand-edit-mcp-panel.png` | 2026-10-14 12:47 | Bao's saved `oil_shrine.blend` after his hand edit: OilGem selected, Rotation 0°, Scale 1; MCP panel "Connected on port 9876", every library and generator unchecked. In-memory vertices hashed identical to the saved file before capture. |
| `1249-rerun-0-before.png` … `1250-rerun-6-sidebar-dimensions.png` | 12:49–12:50 | **Film re-run.** The live session was first saved as a scratch file outside the repository (`save_as_mainfile` to the scratchpad), then calls 1–5 of `tools/blender/build_supply_stack.py` were sent again, verbatim, each followed by `get_scene_info` and one screenshot. The shipped stack was built at 11:59–12:01 by the same calls; nothing in `blender/` or `godot/` was written by the re-run. The sidebar was switched to its Item tab for the last still. |

The MCP `look` renders shown in B02, B08 and B09 are the ones made during the real builds (11:56–12:04 EDT),
committed in `evidence/a3/mcp/`.

Bao's hand edit itself (12:19) was **not recorded live**; the film says so and shows before/after captures and the
measured 20.0° check instead.

## Godot takes (`capture/`)

An isolated copy: `git archive c0dba4c godot` into a scratch folder; in the copy only, `project.godot`'s window
override set to 3840 × 2160 (so Movie Maker writes 4K) and `capture/capture_a3_driver.gd` +
`capture/capture_a3_main.tscn` copied in; imported once (exit 0, no `ERROR` lines).

The driver instantiates `res://a3/lantern_gate_room.tscn` and plays it through the room's real input actions
(`Input.action_press` on `a3_orbit_right`, `a3_tilt_down`, `a3_tilt_up`, `a3_zoom_in`, `move_up`, `move_right`). It
labels every frame "Real engine capture · scripted input · <the key held>". For the `block` take it sets
`debug_collisions_hint` before the room enters the tree (the shapes are built on entry). If the window cannot draw,
the driver pauses the room and lists the frame, so those frames can be dropped; both final takes list none.

    godot --always-on-top --path . res://capture_a3_main.tscn --write-movie <take>.avi --fixed-fps 30 -- orbit|block

| Take | Frames | Stale | What the log records |
|---|---|---|---|
| `take-a3-orbit.avi` | 450 (15.0 s) | none | E 45–104 → camera (−5.84, 3.8, −7.57) behind · F 164–186 → (−3.89, −6.45, −5.05), floor mesh hidden · R 261–282 · E 282–341 → front · Z 371–389 → zoomed |
| `take-a3-block.avi` | 210 (7.0 s) | none | collision shapes on · Z 0–18 · D 30–53 → stand-in x −1.97 · W 60–150 → stopped at z = 0.667 m |

Event logs: `capture/take-a3-<take>-events.jsonl` (and the full console in `take-a3-<take>.log`). Hashes:
`capture/takes.sha256`. The AVIs (MJPEG 3840 × 2160, 30 fps) are not committed.

**Rejected:** a first `orbit` take recorded 39 frames while the window could not draw; the first driver did not
pause on them, so the picture would have frozen while the camera kept moving. The driver was changed to pause and
list such frames, and the take was recorded again (0 stale). The first `block` take drove the stand-in into the
base's far side, hidden from the camera; the final take drives into the front face.

A first headless dry run of each timeline produced the same logged camera and stand-in positions as the windowed
takes (headless cannot draw, so it is used only for the logic).

Godot holds: B13 and B15 play each take once, at its own speed, then hold the last frame for the rest of the
narration, labelled "held last frame". Nothing is retimed.

## Recorded test output

`capture/test-run-film-build-raw.txt`: a fresh `git archive c0dba4c godot` copy, imported once, then
`test_a3_assets.gd` 17/17, `test_lantern_gate.gd` 14/14, `test_a3_camera.gd` 9/9 (all `--fixed-fps 60`), and the
Assignment 2 suites 32 + 65 + 25, all passing. Scratch paths are shortened to `…/evidence/`. B11 shows the A3 suite's
PASS lines from this file.

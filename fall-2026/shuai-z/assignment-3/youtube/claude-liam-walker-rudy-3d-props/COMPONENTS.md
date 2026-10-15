# COMPONENTS — Three Props for Walker Rudy.

The Godot project `assignment-3/godot/` at `f6f8acf`: 11 authored files (`.uid` identifiers and `.godot/` excluded by the contract), every one assigned to a component in `gamedev-evidence.json`. No exclusions.

| Component | Files | Beats | What it does |
| --- | ---: | --- | --- |
| `props-glb` | 6 | B02, B03, B05, B06, B07, B08, B09, B11 | The three props as Godot imports them: waystone.glb, teleport_circle.glb and spikes.glb (binary glTF exported from Blender with +Y Up by tools/blender/export_glb.py) and their .import settings. Each origin is the centre of its underside; sizes and budgets come from CHANGE-BRIEF.md. |
| `scene` | 3 | B10, B11, B14, B15 | The small 3D scene: project.godot (main scene, Forward Plus, window size), scenes/props_room.tscn (floor, one light, a camera, the three props at Y = 0 and a 1.2 m post for Rudy's height) and tools/build_props_room.gd, the headless script that builds it. |
| `check` | 1 | B12, B13, B14, B15, BVD1 | tests/check_props.gd: the headless check. Part 1 measures each .glb on its own (bounding box against the brief within 5 mm, height on Y, origin at the underside centre, node scale and rotation, triangles, colours); part 2 checks each prop's lowest point against the floor mesh's top in the scene. |
| `screenshots` | 1 | BVD1 | tests/capture_props.gd: renders the running scene in a window from five views for TEST-REPORT.md. Its first version read the camera before the scene was in the tree, one of the three things Claude got wrong. The film's orbit uses a separate film-only driver on an isolated copy (capture/orbit_driver.gd). |

## Code → result pairs

| Code beat | Source | Result beat | Observed |
| --- | --- | --- | --- |
| B10 | `tools/build_props_room.gd:10–18` | B11 | The real main scene res://scenes/props_room.tscn in Godot 4.7.2 Forward+, Movie Maker at 3840×2160, 30 fps: 45 frames on the scene's own camera, a 600-frame orbit at its radius (4.6 m) and height (2.2 m), 45 frames back home. All three props stand on the floor with shadows from their bases; the waystone's back is plain. |
| B12 | `tests/check_props.gd:62–71` | B13 | Recorded headless output on an isolated copy of godot/ at f6f8acf: the three bounding boxes match the brief to four decimals, heights on Y, origins at (0, 0, 0), 118/130, 280/300 and 82/100 triangles; 44 ok lines, PASS: 0 failed check(s), exit code 0. |
| B14 | `tests/check_props.gd:93–104` | B15 | Recorded output: the scene as built passes (lowest point 0.0000 m); an isolated copy with the waystone's transform Y set to 0.3 reports 'FAIL Waystone sits on the floor (lowest point 0.3000 m above the floor's top)', 'FAIL: 1 failed check(s)', exit code 1. |

## Not shown as Godot code, and why

- `project.godot`, `scenes/props_room.tscn`: the running scene is shown instead (B11); the `.tscn` is what `build_props_room.gd` (B10) writes.
- `tests/capture_props.gd`: named in the verdict (BVD1) for its first-version bug; its screenshots are in TEST-REPORT.md, not in the film.
- `.glb` and `.import` files: inventoried and hashed; shown as the running scene (B11) and measured by the check (B13).
- The Blender code (`assignment-3/tools/blender/*.py`) is outside the Godot project, so the checker's excerpt contract does not cover it. B05 shows `build_waystone.py` lines 301–311 verbatim on a still card, followed by what it built (B06).

# Components — Walker Survival Shooting: First Props in Blender

Source revision **b370626** (`fall-2026/zhe-l/assignment-3/walker-survival-shooting/`). The Godot project
(`godot/`) has **no runtime scripts**: one saved scene, seven imported `.glb` files with their `.import`
sidecars, and one headless check script. The Blender side lives outside `godot/` (`design/item_resource/`,
`tools/blender/`) and is shown through stills, not through the evidence ledger (the checker only accepts
files under `godot/`). Machine-readable version: `gamedev-evidence.json` (14 files, 8 exclusions, 6 components,
4 exact excerpts, 4 code → result pairs).

## In the ledger (`godot/`)

| Component | Files | Beats | What the film explains |
|---|---|---|---|
| `scene-placement` | `base.tscn` | B10 → B11, B17 | Each asset is an instance of its `.glb` with an identity basis (scale 1) at y = 0.25, the top of the floor slab; the tablet is tilted and lifted (display placement). |
| `asset-chair` | `assets/furniture/chair.glb` (+ `.import`) | B06, B11, B13 | ENV-SEAT-02: 9 boxes cut to 6, 72 triangles, script route. |
| `asset-tablet` | `assets/props/tablet.glb` (+ `.import`) | B04, B05, B13, B18 | PROP-TABLET-02: 21 shapes (over the limit, kept by the designer), 804 → 388 triangles, origin in the centre. |
| `asset-crates` | `crate_long.glb`, `crate_cube.glb` (+ `.import`) | B07, B09, B14 → B15 | On the 0.1 m grid; lid on the back hinge; `open` / `close`; the designer's latch/handle edit. |
| `asset-desks` | `computer_desk.glb`, `computer_desk_l.glb` (+ `.import`) | B11, B17 | Extra project assets; on the grid; in the placement checks. |
| `headless-check` | `tests/a3_asset_check.gd` | B12 → B13, B14 → B15, B16 → B17 | Brief table, crate animation angles, floor / grid / overlap checks; 55 PASS, exit 0; cannot judge looks. |

Code → result pairs (`teaching_contract: code-then-result-v1`):

| Code beat | Excerpt | Result beat | Result evidence |
|---|---|---|---|
| B10 | `base.tscn` 137–147 | B11 | `figures/godot_asset_cam.png` (native 4K render, scene's own `a3_asset_camera`) |
| B12 | `tests/a3_asset_check.gd` 15–21 | B13 | `figures/brief_vs_headless.png` (recorded Part 1 output beside the brief) |
| B14 | `tests/a3_asset_check.gd` 89–97 | B15 | `media/B15.mp4` (596-frame native 4K take of the crates' own animations) |
| B16 | `tests/a3_asset_check.gd` 112–122 | B17 | `figures/log_part2.png` (recorded Part 2 output, abridged) |

## Excluded from the ledger (with reasons, also in the JSON)

`.editorconfig`, `.gitattributes`, `.gitignore`, `icon.svg`, `icon.svg.import` (template files, no runtime
effect); `project.godot` (engine configuration: Forward Plus, Jolt, D3D12, main scene `base.tscn`; named only
as the setup); `assets/furniture/test_chair.glb` and its `.import` (the 2026-10-07 test export, no longer
referenced by `base.tscn`).

## Outside `godot/` (shown, not in the ledger)

| Item | Beats | How it is shown |
|---|---|---|
| Designer's prompts (translated from Chinese) | B04, B05, B07 | Prompt cards copied from SOURCES.md rows PROP-TABLET-01 and CRATE-LONG-02 |
| Claude's MCP `look` captures (9 files) | B04–B07 | Labeled "viewport capture by Claude through the MCP look tool" |
| Designer's own screenshot `design/blender-notes/blender-session-01.png` | B08 | Labeled "my own screenshot", title bar cropped, enlarged insets of the same pixels |
| `tools/blender/build_crate_cube.py` lines 150–151 | B07 | Verbatim text (spacing compressed) in the figure's excerpt line |

Not covered: the `.blend` sources (no Blender was opened for the film), `build_tablet.py`, `build_chair.py`,
`build_crate_long.py` and the desk scripts beyond their headers, the desks' design in depth, and the
Assignment 2 assets.

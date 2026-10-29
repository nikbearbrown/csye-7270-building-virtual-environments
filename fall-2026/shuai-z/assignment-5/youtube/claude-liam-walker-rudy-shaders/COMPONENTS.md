# COMPONENTS — Two Shaders for Walker Rudy.

Two Godot projects, two ledgers: the course checker takes one folder holding `project.godot`, so each project has its own `checks/<project>/gamedev-evidence.json` (see `tools/make_evidence.py`). `.uid` identifiers and `.godot/` are left out by the contract.

## `game/` at `a2a3a77` — 15 files in components, 105 excluded

| Component | Files | Beats | What it does |
| --- | ---: | --- | --- |
| `tint-shader` | 2 | B02, B03, B04, B05, B06, B08 | shaders/invulnerable_tint.gdshader, written by shuai-z: canvas_item, three uniforms (tint_amount driven by the game; tint_color and tint_strength set by the material only) and the colour line at line 8, which moves only COLOR.rgb toward the waystone's glow. project.godot names GL Compatibility, the renderer it runs in. |
| `tint-driver` | 9 | B07, B08, B09 | The hearts and what drives them: ui/hud.gd's _tint_hearts() sets tint_amount every frame to Rudy's _invulnerable_left / invulnerable_time; ui/hearts_tint.tres is the ShaderMaterial, local to the scene, on Hud/Hearts (ui/hud.tscn); ui/hearts.gd draws the heart art in ui/art/. content/rudy/rudy.gd owns the window and is unchanged byte for byte. |
| `tint-tests` | 4 | B06, B20, B21, B22, BVD1 | tests/invulnerable_tint_checks.gd/.tscn: 15 headless checks through real input at 30, 60 and 144 fps (uniforms, defaults, where the material is, begin, fade, end, duration, retrigger, time scale, pause, reload). tests/capture_tint.gd/.tscn: the windowed capture at controlled values, with the driver stopped. |

| Code beat | Source | Result beat | Observed |
| --- | --- | --- | --- |
| B05 | `shaders/invulnerable_tint.gdshader:1–9` | B06 | Windowed Compatibility captures with the driver stopped and tint_amount set from code to 0.0, 0.5, 1.0 and 2.0: P1 and P2 equal the brief's predictions at 0.0, 0.5 and 1.0; at 2.0 P1 is one step off the unclamped prediction and 81 from the clamped one; P3 stays the sky. |
| B07 | `ui/hud.gd:108–111` | B08 | The real main scene in Godot 4.7.2 Compatibility, Movie Maker at 3840×2160, 30 fps, scripted input: Enter on the title, the hearts fade in; hit 1 at frame 131 (tint_amount 0.986), a walk back onto the spikes with no heart lost and no rise; hit 2 at 223; hit 3 takes the last heart at 308; the respawn at 343 starts the tint again at 0.972. Then a labelled half-speed replay of frames 30–209. The inset shows the same frames' hearts, 3×. |
| B20 | `tests/invulnerable_tint_checks.gd:347–354` | B21 | Recorded headless output at 30, 60 and 144 fps through scripts/run-test.sh: 15 PASS and 'all checks passed' at each; A9 1.2000, 1.1833 and 1.1806 s against 1.1833 ± one frame, and 2.4 s at time scale 0.5; A10 no rise; A11 the respawn's jump; A12 the pause holds. |

**Excluded, with the reason recorded in the ledger:**

- 105 file(s): `app/main.gd`, `app/main.tscn`, `app/system_keys.gd`, `content/goblin/frames/ENEMY-GOBLIN-SQUASH.png`, `content/goblin/frames/ENEMY-GOBLIN-SQUASH.png.import`, `content/goblin/frames/ENEMY-GOBLIN-WALK-A.png` and 99 more. Assignment 2's game, copied unchanged from tag a3 (84658acf) and not changed by Assignment 5; this film covers the layer Assignment 5 added. The 141 existing checks in tests/checks.gd guard it, and pass.

## `godot/` at `a2a3a77` — 38 files in components, 2 excluded

| Component | Files | Beats | What it does |
| --- | ---: | --- | --- |
| `stone-shader` | 4 | B02, B03, B11, B12, B13, B14 | shaders/weathered_stone.gdshader, written by shuai-z: three samplers with their hints (source_color for colour, hint_normal and none for data), four grouped uniforms with ranges, and fragment() writing ALBEDO, NORMAL_MAP, NORMAL_MAP_DEPTH and ROUGHNESS. scenes/props_room.tscn carries the two surface overrides, set by tools/add_stone_overrides.gd; project.godot names Forward Plus. |
| `stone-materials` | 8 | B03, B12, B14, B17, B18 | materials/waystone_stone.tres and materials/circle_darkstone.tres: one shader, the same three textures, different values (albedo_tint, normal_strength, roughness_offset). They override surface 0 of the waystone's mesh and surface 1 of the circle's, in the Assignment 3 props in assets/props/, whose .glb and .import files are unchanged. |
| `stone-textures` | 11 | B10, B14 | Rock 01 from Poly Haven (Rob Tuytel, CC0) in assets/textures/rock_01/, with ATTRIBUTION.md and explicit import settings; tests/normal_map_check.gd (the assignment's curl check, unchanged) and tests/calibrate_normal_map_check.gd (its calibration on the GL/DX pair and the 0.5 threshold). |
| `hint-experiment` | 10 | B15, B16, B23 | shaders/hint_experiment.gdshader (written by shuai-z), its two materials, scenes/hint_experiment.tscn, the grey strip and the tools that write them, and the windowed captures tests/capture_hint.gd and tests/capture_hint_vs_os.gd. |
| `generated-shader` | 1 | B19 | shaders/standard_generated.gdshader: what Godot 4.7.2 generated from a StandardMaterial3D with Rock 01's textures, annotated by shuai-z; nothing uses it. |
| `stone-tests` | 4 | B22, B23, BVD1 | tests/test_materials.gd (125 headless checks) and MATERIALS.md, the audit's report; tests/capture_sweep.gd, the windowed sweep and two-materials capture; tests/check_props.gd, Assignment 3's 44 checks, unchanged and still passing. |

| Code beat | Source | Result beat | Observed |
| --- | --- | --- | --- |
| B11 | `shaders/weathered_stone.gdshader:3–13` | B12 | Close-up windowed captures under the scene's own lighting, each uniform at min, default and max on the loaded material: albedo_tint black 73.51 steps; uv_scale 0.25 12.51 and 4.0 9.20; normal_strength 2.62 and 2.93; roughness_offset 2.64 and 0.90 (mean largest-channel change). |
| B13 | `shaders/weathered_stone.gdshader:16–22` | B14 | The real main scene res://scenes/props_room.tscn in Godot 4.7.2 Forward+, Movie Maker at 3840×2160, 30 fps: the scene's own camera, one orbit at its radius and height, then two close arcs. The waystone's Stone and the circle's DarkStone show Rock 01's grain, lit by the scene's Sun; the rune, moss and gold keep flat colours; the disc is darker and smoother in relief. |
| B15 | `shaders/hint_experiment.gdshader:2–13` | B16 | The windowed Forward+ capture of hint_experiment.tscn: quad A shows 64, 128, 192 and quad B 137, 188, 225, each flat over 9 × 9 pixels; all six equal the brief's predictions. |
| B17 | `materials/circle_darkstone.tres:8–16` | B18 | Windowed captures from the scene's Camera, in memory only: ALBEDO halved in the loaded shader's line 18 darkens both stones (22.54 and 10.52 steps); the circle's normal_strength at 2.0 moves it 0.76 steps; its albedo_tint at white moves it 19.97 steps and the waystone 0.00. |

**Excluded, with the reason recorded in the ledger:**

- 1 file(s): `tests/capture_props.gd`. Assignment 3's screenshot tool, unchanged; not used by Assignment 5 or this film.
- 1 file(s): `tools/build_props_room.gd`. Assignment 3's scene builder, unchanged; deliberately not re-run, since it would write the scene without the overrides.

## Shown on still cards rather than as Workbench excerpts

- `godot/shaders/standard_generated.gdshader` lines 10–11 and 69–72, beside `weathered_stone.gdshader` lines 3–4 and 19–20 (B19): `tools/make_stills.py` reads the lines from the files.
- `CHANGE-BRIEF.md` section 2's uniform table and colour line (B04), read from the file; the rows are asserted against it.


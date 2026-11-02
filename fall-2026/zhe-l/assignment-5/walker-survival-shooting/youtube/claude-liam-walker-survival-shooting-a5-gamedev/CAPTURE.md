# Capture record — claude-liam-walker-survival-shooting-a5-gamedev

All engine images were rendered by Godot v4.7.2.stable.official.ed1daf0bf, Forward+, D3D12 12_0, NVIDIA GeForce RTX 5070 Ti Laptop GPU, in a **real window** (not headless), inside a 3840x2160 `SubViewport` unless stated. Captures were made in isolated copies of the project; the project itself was never edited, and no scene, material, shader or texture was saved by a capture script.

## Source copies

| Copy | Made from | Used for |
|---|---|---|
| Snapshot A | the working folder's `project-survival-shooting/` at 2026-11-01 21:48 (no `.godot/`) | crate captures, tablet run |
| Snapshot B | the same folder at 22:35 (adds only `standard_generated.gdshader`) | source_color comparison (left image) |
| Mutated copy | snapshot B with `source_color` deleted from `crate_wear.gdshader` line 3 | source_color comparison (right image) only |
| HEAD copy | local commit 08839a7 | hint experiment |

Checked against the course repository at a84cfa23 (`walker-survival-shooting/godot/`): every shader, material, scene, texture, `.import`, `base.tscn` and `project.godot` is byte-identical to snapshot A; the `.gd` files differ only in comments (English translation), except `debug/screen_glow_capture.gd`, whose `OUT_DIR` constant differs (not used by these captures). Game source shown: 2d558bba.

## Scripts (`capture-tools/` in the film work folder)

- `hint_capture.gd`: loads the unchanged `hint_experiment.tscn` in the window's own viewport (1152x648, `get_viewport().get_texture().get_image()`) and in a 4K SubViewport; reads each band centre found with the scene camera's `unproject_position()`, 3x3 uniform. Measured 64/128/192 with `source_color`, 137/188/225 without, in both images.
- `crate_capture.gd`: loads the unchanged `base.tscn`; adds a film camera (made current after the scene tree is live, because the player's own camera takes the view on entering the tree); `shot=pair`, `shot=sweep`, `shot=sweep_glint` (a camera placed so ceiling_light_2 reflects off crate_cube's top). Sweep values are set at runtime with `set_shader_parameter()` on crate_cube's material only. Repeated default images are byte-identical across runs and copies.
- `tablet_capture.gd`: loads the unchanged `base.tscn`; the view is the player's own camera. **Scripted input**: Tab key events through `Input.parse_input_event()` and one mouse-motion event (244 px, about 35°) delivered with `push_input()`. Every physics tick is logged (`tablet-inputs.jsonl`); 10 assertions on the screen value pass. Run with `--fixed-fps 30`: offline rendering, not evidence of real-time frame rate. Run 01 was rejected (the body hid the tablet in one hand).

## Media in the film

| Beat | File | From |
|---|---|---|
| B06 | `media/B06.mp4` (391 frames, 3840x2160, 30 fps, label burned in) | tablet-run-02 frames f00000–f00390, no retiming |
| B02, B10, B12, B14, B16, B18, B20 | `figures/*.png` | crops and side-by-side placement of the captures above; English labels added; aspect ratio kept |
| B04 | `figures/fig_controlled.png` | the user's own in-engine F9 captures `captures/screen_pad_*_marked.png` (2048x1152), scaled |
| B08, B22, B24 | `figures/fig_log_*.png` | lines copied verbatim from the submitted logs |

Hashes: `figures/MANIFEST.json`, `gamedev-evidence.json`, and the film work folder's `CAPTURE-NOTES.md`.

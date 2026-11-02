# Shot list — claude-liam-walker-survival-shooting-a5-gamedev

One row per beat, in order. Durations are measured Kokoro narration (B01 includes 0.8 s lead silence, B28 a 1.0 s tail hold; B06 runs the full 391-frame capture with silence after the narration).
"Reconstruction" = Godot editor reconstruction (source-backed teaching view, not a recording).

| Beat | Act | Dur (s) | Visual | Evidence shown | Label on screen |
|---|---|---|---|---|---|
| B00 | ASK | 21.71 | ClaudeComposerAsk | composer prompt | Reconstructed prompt (illustrative, not a saved session) |
| B01 | BLUF | 7.50 | BrutalistHesitantWriter | — |  |
| B02 | RESULT | 13.92 | GodotDesignFigure | `figures/fig_pair.png` | Native Godot render, 3840x2160 · the two weapon crates · film camera |
| B03 | CODE | 22.71 | GodotDevWorkbench | `shaders/pad_base_light.gdshader  ·  lines 1–7` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B04 | RESULT | 17.54 | GodotDesignFigure | `figures/fig_controlled.png` | In-engine captures (get_viewport().get_texture()), 2048x1152, scaled up here |
| B05 | CODE | 14.83 | GodotDevWorkbench | `characters/human/humanoid/humanoid.gd  ·  lines 137–142` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B06 | RESULT | 13.03 | real footage | `media/B06.mp4` (native 4K Godot render) | burned-in label: scripted input |
| B07 | CODE | 14.79 | GodotDevWorkbench | `items/tablet/tablet_device.gd  ·  lines 42–48` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B08 | RESULT | 14.83 | GodotDesignFigure | `figures/fig_log_screen.png` | Recorded test output, copied verbatim |
| B09 | CODE | 18.96 | GodotDevWorkbench | `assets/furniture/materials/crate_long_wear.tres  ·  lines 1–13` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B10 | RESULT | 11.12 | GodotDesignFigure | `figures/fig_pair.png` | Native Godot render, 3840x2160 · base.tscn unchanged · film camera |
| B11 | CODE | 15.54 | GodotDevWorkbench | `shaders/crate_wear.gdshader  ·  lines 34–42` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B12 | RESULT | 10.79 | GodotDesignFigure | `figures/fig_wear.png` | Native Godot renders, 3840x2160 · value set at runtime, not saved |
| B13 | CODE | 14.96 | GodotDevWorkbench | `shaders/crate_wear.gdshader  ·  lines 22–32` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B14 | RESULT | 11.58 | GodotDesignFigure | `figures/fig_scale.png` | Native Godot renders, 3840x2160 · value set at runtime, not saved |
| B15 | CODE | 16.42 | GodotDevWorkbench | `shaders/crate_wear.gdshader  ·  lines 1–20` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B16 | RESULT | 11.83 | GodotDesignFigure | `figures/fig_interface.png` | Native Godot renders, 3840x2160 · rows 2–3 cropped from a highlight angle |
| B17 | CODE | 11.67 | GodotDevWorkbench | `shaders/hint_experiment.gdshader  ·  lines 1–14` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B18 | RESULT | 15.12 | GodotDesignFigure | `figures/fig_hint.png` | Native Godot render, 3840x2160, scene unchanged |
| B19 | CODE | 12.79 | GodotDevWorkbench | `shaders/standard_generated.gdshader  ·  lines 9–13` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B20 | RESULT | 11.92 | GodotDesignFigure | `figures/fig_mutation.png` | Native Godot renders · right: film-only mutated copy, not the project |
| B21 | CODE | 10.67 | GodotDevWorkbench | `shaders/standard_generated.gdshader  ·  lines 40–45` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B22 | RESULT | 15.17 | GodotDesignFigure | `figures/fig_log_normal.png` | Recorded test output, copied verbatim |
| B23 | CODE | 9.54 | GodotDevWorkbench | `tests/test_materials.gd  ·  lines 208–223` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B24 | RESULT | 15.54 | GodotDesignFigure | `figures/fig_log_mutation.png` | Recorded test output, copied verbatim |
| B25 | LIMITS | 16.00 | GodotDesignFigure | `figures/fig_pair.png` | TEST-REPORT section 6 · MATERIALS.md section 6 |
| B26 | VERDICT | 38.71 | ClaudeVerdictArtifact | — |  |
| B27 | HANDOFF | 21.71 | ClaudeComposerAsk | composer prompt | Walker Survival Shooting |
| B28 | OUTRO | 5.00 | ClaudeTitleOutro | — |  |

Total ≈ 435.9 s (7.3 min) before frame alignment.

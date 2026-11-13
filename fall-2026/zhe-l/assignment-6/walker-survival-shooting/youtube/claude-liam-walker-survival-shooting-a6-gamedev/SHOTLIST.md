# Shot list — claude-liam-walker-survival-shooting-a6-gamedev

One row per beat, in order. Durations are measured Kokoro narration (B01 includes 0.8 s lead silence, B31 a 1.0 s tail hold; B08 and B16 run their full captures).
"Reconstruction" = Godot editor reconstruction (source-backed teaching view, not a recording).

| Beat | Act | Dur (s) | Visual | Evidence shown | Label on screen |
|---|---|---|---|---|---|
| B00 | ASK | 21.21 | ClaudeComposerAsk | composer prompt | Reconstructed prompt (illustrative, not a saved session) |
| B01 | BLUF | 9.00 | BrutalistHesitantWriter | — |  |
| B02 | SETUP | 16.33 | GodotDesignFigure | `figures/fig_game.png` | Native Godot renders, 3840x2160, scripted input · left: Effect A, player camera · right: Effect B, film camera |
| B03 | INTENT | 15.67 | GodotDesignFigure | `figures/fig_a_intent.png` | CHANGE-BRIEF.md, committed before the first agent prompt |
| B04 | CODE | 19.08 | GodotDevWorkbench | `effects/landing_dust.tscn  ·  lines 113–125` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B05 | RESULT | 15.25 | GodotDesignFigure | `figures/fig_a_r0.png` | FIXTURE capture: preview scene, Movie Maker, 30 fps, 2048x1152, cropped; top bright, bottom dark |
| B06 | TUNING | 22.58 | GodotDesignFigure | `figures/fig_a_r1.png` | FIXTURE captures: top row r0, bottom row r1, same frames |
| B07 | CODE | 16.29 | GodotDevWorkbench | `characters/human/humanoid/humanoid.gd  ·  lines 109–115` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B08 | RESULT | 23.40 | real footage | `media/B08.mp4` (native 4K Godot render) | burned-in labels: scripted input, camera, code-set states |
| B09 | CODE | 13.12 | GodotDevWorkbench | `effects/landing_dust_trigger.gd  ·  lines 38–41` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B10 | RESULT | 16.12 | GodotDesignFigure | `figures/fig_a_retrigger.png` | FIXTURE capture, r1: frames 24 · 25 · 26 (top), 27 · 30 · 35 (bottom); second landing at frame 25 |
| B11 | INTENT | 15.33 | GodotDesignFigure | `figures/fig_b_intent.png` | CHANGE-BRIEF.md, Effect B and its 2026-11-12 revision |
| B12 | CODE | 18.50 | GodotDevWorkbench | `effects/light_dust.tscn  ·  lines 12–26` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B13 | TUNING | 21.38 | GodotDesignFigure | `figures/fig_b_r0r1.png` | FIXTURE captures, cropped; difference tiles are computed analysis |
| B14 | TUNING | 17.75 | GodotDesignFigure | `figures/fig_b_redesign.png` | FIXTURE captures, whole frame; computed differences |
| B15 | CODE | 11.67 | GodotDevWorkbench | `effects/light_dust_listener.gd  ·  lines 43–51` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B16 | RESULT | 16.03 | real footage | `media/B16.mp4` (native 4K Godot render) | burned-in labels: scripted input, camera, code-set states |
| B17 | CODE | 19.75 | GodotDevWorkbench | `shaders/particles_generated.gdshader  ·  lines 257–264` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B18 | RESULT | 11.50 | GodotDesignFigure | `figures/fig_b_redesign.png` | FIXTURE capture redesign-2 (right): computed difference, whole frame |
| B19 | CODE | 18.42 | GodotDevWorkbench | `shaders/particles_generated.gdshader  ·  lines 251–255` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B20 | RESULT | 15.08 | GodotDesignFigure | `figures/fig_b_timeline.png` | FIXTURE capture redesign-2: computed differences against the dust hidden |
| B21 | CODE | 11.71 | GodotDevWorkbench | `tests/test_landing_dust_config.gd  ·  lines 100–106` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B22 | RESULT | 13.92 | GodotDesignFigure | `figures/fig_log_tests.png` | Recorded test output, copied verbatim |
| B23 | RESULT | 17.21 | GodotDesignFigure | `figures/fig_log_mutations.png` | Recorded test output, copied verbatim |
| B24 | CODE | 12.04 | GodotDevWorkbench | `tests/cost_effects.gd  ·  lines 102–111` (code mode) | Godot editor reconstruction · source-backed teaching view |
| B25 | RESULT | 20.71 | GodotDesignFigure | `figures/fig_log_cost.png` | Recorded output of cost_effects.gd, copied verbatim |
| B26 | RESULT | 27.46 | GodotDesignFigure | `figures/fig_log_gpu.png` | Recorded output of gpu_price.gd (two runs) · TEST-REPORT Use It |
| B27 | LIMITS | 18.88 | GodotDesignFigure | `figures/fig_a_r1.png` | TEST-REPORT Use It · README Known limitations |
| B28 | JUDGEMENT | 19.42 | GodotDesignFigure | `figures/fig_a_retrigger.png` | TUNING.md Effect A r1 · FRICTIONAL.md Steps 2–4 |
| B29 | VERDICT | 30.08 | ClaudeVerdictArtifact | — |  |
| B30 | HANDOFF | 20.50 | ClaudeComposerAsk | composer prompt | Walker Survival Shooting |
| B31 | OUTRO | 4.92 | ClaudeTitleOutro | — |  |

Total ≈ 550.3 s (9.2 min) before frame alignment.

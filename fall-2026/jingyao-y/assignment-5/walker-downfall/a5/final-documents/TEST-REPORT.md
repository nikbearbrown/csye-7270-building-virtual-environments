# Assignment 5 — Test Report

2026-10-30. Godot **4.7.2.stable.official.ed1daf0bf**; **Forward+ / D3D12**. Real rendering uses NVIDIA GeForce RTX 4060 Laptop GPU, with AMD Radeon(TM) 610M also checked for the hint experiment. Physics stays at 60 Hz. Headless runs use the dummy renderer and prove state/interface behavior rather than pixels.

The development checkout is based on d75b60009b158582b45d65d19bc50177d55ae9f4 plus its existing working-tree game changes. The delivered snapshot is identified file by file in evidence/a5/delivery-manifest.json. The course commit and a5 tag identify the final source. Earlier driver/test evidence was recorded at course commit 7e562a4.

## State and interface checks

| Check | Result |
|---|---|
| Fire at fixed 30 / 60 / 144 fps | 89 checks, 0 failures at each rate |
| Material audit, 60 fps | 120 checks, 0 failures |
| Normal convention / curl | exit 0 |
| Protected sources during full regression | unchanged |
| Real-renderer Esc pause / E looting | 14 checks, 0 failures; four menu captures |

Logs are in evidence/a5/final-regression/. The fire tests use a real thrower, Molotov flight, and landing hazard. They stop the thrower's physics after release to isolate one bottle. A priority-100 observer reads the uniform without calling the driver. Esc and E are injected input events. The boss last-rite boundary uses its hazard parameters rather than a complete boss encounter.

The endpoint is **181 physics steps / 3.016667 game seconds** at all three render rates. Floating-point subtraction leaves a tiny positive residual after step 180. time_scale 0.5 and 2 give 361 and 91 steps. At 30 fps the first process observation is 0.994444; the birth physics observation is exactly 1.0. That distinction follows the dated R1 revision and does not claim a numerically exact first GPU frame. Pause freezes lasting and the driven value; looting continues the timer. Separate fires keep separate materials; floor change frees the hazard and its flame.

## Controlled fire pixels

Seed 2026, city, camera size 24, 1280×720, Linear tone mapping, exposure 1, post-processing and outline disabled on a disposable Environment copy. Flicker is zero. The brief's predictions were kept unchanged.

| Value | A predicted / measured | B predicted / measured |
|---|---|---|
| 1 | (210,210,67) / (210,210,67) | (186,186,67) / (186,186,67) |
| 0.5 | (158,121,67) / (158,121,67) | (142,110,67) / (142,110,67) |
| 0 | (58,58,67) / (58,58,67) | (59,58,67) / (59,58,67) |
| 2 | (210,255,67) / (210,255,67) | no original B prediction; measured (186,248,67) |

A=(640,420), B=(704,420). All seven predicted samples match exactly, within ±2. At r=0 both points return the original background values. Some interface animation continues between full-frame captures. Setting 2 reads back as 2: hint_range does not clamp a code assignment. mix extrapolates while the explicit alpha clamps still apply.

The GDI system capture returned a flat frame. DXGI capture worked after the borderless client size was fixed before capture. Both sample points match the engine image exactly. Full-frame mean absolute differences are about 0.0226 / 0.0174 / 0.0016 RGB8 levels; remaining differences are in moving interface details. I use the engine image for numerical sampling because viewport coordinates and output settings are explicit, without window borders or compositor scaling. The system image corroborates the visible result.

Images and metadata: evidence/a5/use-it/fire-*.png, measurement.json, system-comparison.json.

## Rendered observations

The city run records **nine new fires**, each with Flame and Decal. The bottle flies before the flame appears. The yellow region becomes red and fades; the existing bright ground circle remains visible. Under normal ACES lighting the effect differs from Linear calibration, and the player can hide its lower part. One explosive-slug hazard retains its Warning and burst without a Flame. Pause holds the observed value at 0.9944444444.

gameplay.json and the gameplay-*.png images retain these observations. Film footage uses a native 3840×2160 SubViewport. This establishes the recorded cases, not a complete playthrough or every possible camera/occlusion condition.

## TIME / R5

A diagnostic surface encodes TIME milliseconds into rendered RGB bytes with inverse display transfer.

| time_scale | TIME advance over 120 fixed-60-fps frames |
|---|---|
| 1 | 2.000 s |
| 0.5 | 1.000 s |
| 2 | 4.000 s |
| 0 | 0.000 s |

TIME follows time_scale. Fixed-fps execution can finish faster than wall time; these are simulation intervals, not performance measurements. Ordinary menu pause uses simulation_active rather than time_scale=0, so flicker can continue while lifetime color holds.

## Texture hints and normal convention

The hint experiment retains **two RTX 4060 runs and two AMD 610M runs**, with separate logs, images and measurements under evidence/a5/hint-experiment/runs/. All six samples in every run match exactly: 64/128/192 with source_color and 137/188/225 without. four-runs.json identifies adapters and image hashes.

GL and Y-corrected DX differ by at most 1 level under review light and 2 under raking light; raw DX reaches 8 and 16. See evidence/a5/normal-map-check/measurement.json. Curl separates conventions but does not reach ideal 0/2 ratios. The source is very flat, with about 1 degree mean tilt, so quantization matters.

## Material scan and sharing

| Control | What I see | Limit |
|---|---|---|
| uv_scale .25 / 1 / 8 | .25 magnifies a small patch; 8 creates fine repetition | 8 looks too repetitive here |
| tint_color black / white / white | black removes most diffuse color; white keeps the texture | color has no enforced maximum; white is the chosen upper RGB endpoint |
| roughness_scale 0 / 1 / 2 | direct highlights change; high values flatten the response | B's 1.35 already clamps 91.7% of texels to 1 |
| normal_strength 0 / 1 / 2 | subtle differences, clearest at grazing incidence | a flat source cannot supply large dents |

Other controls use shader defaults; B remains the reference. Both light setups are retained. A/B appearance is primarily a tint and roughness difference; I do not call its normal-strength difference obvious under review light.

Changing the shared ALBEDO statement to multiply by 0.5 changes both panel regions. After restoration, changing only A.tint_color changes A while B stays pixel-identical. shared-shader.json records the measurements and matching source hashes. The shader was restored byte for byte. Base screenshots show the two actual hall crate_stack props under unchanged ACES lighting.

## Mutations, Step 4 and regression

Missing-semicolon and shader-only uniform-rename mutations each exit **1**. Restored fire exits **0**, 89/89. Removing albedo_tex's source_color exits **1**; the restored audit passes 120/120. Tests and wrapper were not changed for those mutations. Evidence: evidence/a5/mutations/ and final-regression/.

Native editor material conversion generated a 48-line comparison shader. It parses and renders with the three textures, and no game material references it. The three cargo import sidecars and three original shaders remained unchanged across conversion. The export program, logs and earlier notes are retained under evidence/a5/step4/. LANGUAGE-NOTES cites actual generated line numbers. Editor shutdown/cleanup errors remain in the original logs.

The 73-suite run produced **69/73 in parallel**. The three baseline failures remain: test_combat, test_loading_screen, and two checks in test_item_icons. The extra test_market failure exceeded its 3-second wall-clock budget (3154/3336 ms). An isolated repeat passes **95 checks / exit 0**, resolving the suite result to the baseline **70/73**. Both receipts are kept: final-regression/summary.json and performance-rerun/summary.json.

The course copy imported from an empty cache in 302.25 seconds, exit 0. All 7,762 existing .import sidecars stayed unchanged; 43 new diagnostic-image sidecars were generated. The import log contains no SCRIPT ERROR or SHADER ERROR. Evidence: evidence/a5/clean-import/. Final-clone and film receipts are retained with the delivery.


## Film delivery

The landscape master is 3840 x 2160 at 30 fps, 418.867 seconds, with 23 beats. It covers the four concepts, exact fire color statement, controlled values, native gameplay, hint experiment, material sweeps, shared-shader behavior and generated comparison. Normal export gates report zero blockers and zero major defects. The final review and SHA-256 receipt are under youtube/claude-liam-downfall-a5-shaders-gamedev/. Video and audio are delivered in Canvas rather than GitHub.

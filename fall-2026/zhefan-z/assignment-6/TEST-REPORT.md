# TEST-REPORT — Assignment 6

- **Godot:** 4.7.2-stable, official build `ed1daf0bf`.
- **Renderer:** Forward+, Vulkan 1.4.312 (printed by every windowed run).
- **GPU used for the GPU price:** NVIDIA GeForce RTX 5060 Laptop GPU; CPU AMD Ryzen 9 8945HX (Visual Profiler header). Display refresh about 165 Hz (FPS 160–167 with vsync on).
- **OS:** Windows, Git Bash. Every test ran through `scripts/run-test.sh` (fixed-fps headless unless stated). Game source revision: the commit that adds this report; the effect scenes were last changed in `35a1f70` (A) and `cc1f2f2` (B).

Human checks are mine, in my words *(translated from my Chinese)*. A headless run uses a dummy renderer: it draws no particles and runs no GPU particle process, so no headless result below says anything about the look. Strips are **fixture captures** from the preview scenes (Movie Maker, 30 fps), not gameplay.

## Machine checks

| Check | Result | Evidence |
|---|---|---|
| Baseline before | 9 earlier suites: player 11, cast 11, wolf 13, flow 14, audio 13, sound_triggers 11, a3_assets 22, materials 32 at 60 fps; hurt_tint 17 at 30/60/144; all 0 failures | `logs/baseline-before/`, `1cebbd8` |
| Baseline after | the same counts and 0 failures after Effect A was wired (`f5743f5`) and after Effect B was wired (`e174c96`). Every run ends with "ObjectDB instances leaked" / "resources still in use" lines; the baseline runs print them too; not failures | commit bodies, `logs/` |
| Configuration, Effect A | `test_fireball_impact_config.gd` at 60: 54 checks / 0 failures. Reads back every setting the brief names for Sparks and Smoke from the loaded resources, including the Smoke ramp offsets (0, 0.125, 1) after r1, and scans the scene for Godot 3 names | `logs/test_fireball_impact_config_60fps.log` |
| Configuration, Effect B | `test_fireball_trail_config.gd` at 60: 32 checks / 0 failures, including turbulence and the sphere emission shape (the features A doesn't use), the scale curve 2 → 0 after r1, and a check that seven brief values equal to engine defaults are actually written in the scene | `logs/test_fireball_trail_config_60fps.log` |
| Mutation a1: Godot 3 name | Sparks `initial_velocity_min = 90.0` renamed to `initial_velocity = 90.0`: **exit 1**, 2 failures (`initial_velocity_min` read back 0.0; the Godot 3 name scan). In 4.7.2 `initial_velocity` still exists as a Vector2 (min, max), so the float is **dropped silently**, with no error or warning in the log, and the effect **still fires** (instances at frames 10 and 16, amount 24) with a speed range of 0–160 instead of 90–160 | `logs/mutation-a1-*`, `ab0784c` |
| Mutation a2: drift | Sparks `lifetime` 0.45 → 0.6, brief unchanged: **exit 1**, 1 failure | `logs/mutation-a2-*`, `ab0784c` |
| State, Effect A | `test_fireball_impact.gd`, fixed-fps headless at 30 / 60 / 144: 14 checks / 0 failures each. Real mouse casts through the real game loop; aliveness by instance. A1 one impact per hit on ground, wall and wolf; A2 none on scene load, on a cast, or on a 2.0 s timeout; A3 at the fireball's last position (0.01 px); **A4 two impacts inside one lifetime both alive (overlap), at most 3 alive in steady casting**; A5 the impact survives the fireball and the wolf being freed; A6 each instance lives 0.9 s rounded up to the next frame | `logs/test_fireball_impact_*fps.log`, `f5743f5` |
| State, Effect B | `test_fireball_trail.gd`, fixed-fps headless at 30 / 60 / 144: 20 checks / 0 failures each. B5 no trail before a cast or on scene load; B1 trail emitting on the fireball's first frame; B2 on a ground hit, a leftward wall hit and the 2.0 s timeout the trail moves to `Main` at the fireball's position and rotation, stops emitting and is freed 0.3 s later; B3 real Esc mid-flight freezes it and it resumes; B2 + B3 a pause right after an impact holds the fading trail; B4 hidden: `emitting` stays true and the node keeps processing | `logs/test_fireball_trail_*fps.log`, `e174c96` |
| Not covered | the `_spent` guard (no fireball touched two bodies in one frame across 17 fireballs); B4 sets `visible` from the test, because no game mechanism hides a fireball | same logs |
| Trail direction | windowed probe on the RTX 5060: `direction` follows the emitter's rotation (a fast copy moved −26.5 px in x at rotation 0 and at π, in its own frame); gravity stays world space (+5.94 / −5.94 in y). The brief's "in world space" was wrong (revision 2026-11-06) | `tests/probe_trail_direction.gd`, `e174c96` |

## Frame strips (fixture captures) and tuning

All strips are listed with Claude's predictions, comparisons and my verdicts in `TUNING.md`:

- **Effect A:** `captures/fireball_impact/r0/`, `r0-retrigger/`, `r0b-retrigger/` (preview seeds fixed, no effect change), `r1/` (Smoke ramp fade-in, kept).
- **Effect B:** `captures/fireball_trail/r0/`, `r1/` (scale curve 2 → 0, kept).

## Human checks

| Check | What I saw *(translated from my Chinese)* |
|---|---|
| Effect A in play, many times and rapid repeats (main scene, 1280×720) | impacts on the ground, on the walls and on the wolf all read well; a hit on the wolf is unmistakable; rapid casting looks fine. After r1, the moment of impact is brighter |
| Effect B in play | casts to the right and to the left both trail behind the fireball; a shot straight up that times out leaves its trail fading where it was; Esc mid-flight freezes the trail and Esc again resumes it. After r1, thicker and brighter |
| Against the background | darkest stretch (the pit): Effect A's smoke clearly visible; Effect B readable. Lightest stretch (the ground cap): both readable |
| Edge of screen | impacts on the left and right walls with the camera at its limits, where the walls are at the screen edge: no sparks cut off or popping out |
| Scene load | no trail in the first frames after the main scene loads |
| Hidden | not reachable in play (nothing hides a fireball); node state checked headless only |
| Size at the window size | at 1280×720: sparks reach about one mage height (my first look of Effect A), the trail is longer than the fireball (my first look of Effect B); in play neither felt too big or too small |

## Claude against me

1. **r0-retrigger sameness.** I saw the two impacts as stamped. Claude measured the second as the first scaled by 0.83 (1.6 px error, 4.1 px for a rotated control) and blamed the preview's seed + 1. After the seed fix (`0069149`) I saw them differ: Claude was right, the effect was not.
2. **r0 frame 20.** Claude read the sparks as too dark too soon (dark-red specks, not orange-red). Watching in slow motion I judged the darkening rhythm right. My verdict stood; nothing was changed for it.

## Price

**Headless CPU** (`tests/cost_effects.gd`, `./scripts/run-test.sh cost_effects.gd 60 300`, 3 rounds × 1200 frames per case, wall time between frames; `f7787c4`):

| Case | Mean µs | σ |
|---|---|---|
| control: empty scene | 3.82 | 0.96 |
| game scene, effects off | 240.83 | 45.38 |
| Effect A, 6 impacts alive | 253.58 | 47.54 |
| Effect B heaviest (6 flying + 6 fading, +6 refilling) | 296.42 | 57.87 |

Each effect's own price, after subtracting a dry case (the same driver with bare `Node2D` placeholders): **A +8.2 µs, B +25.1 µs**, inside the scene's frame-to-frame spread (σ 45 µs): near zero, as predicted, because headless runs no GPU particle process. The control and the off case clearly differ (+237 µs), so the script is not measuring only itself; without the dry cases, Effect B's price would have doubled. `Performance.TIME_PROCESS` gave identical values for different cases under fixed-fps headless and is not used.

**GPU time (Visual Profiler, Debugger panel, `previews/gpu_price.tscn` run from the editor, RTX 5060 Laptop GPU):**

| | Case 1, off | Case 2, Effect A ×6 | Case 3, Effect B heaviest |
|---|---|---|---|
| Update GPUParticles (GPU) | absent (0) | 0.01 ms | 0.09 ms |
| Render Viewport (GPU) | 0.03 ms | 0.04 ms | 0.04 ms |
| **Over case 1** | — | **≈ 0.02 ms** | **≈ 0.10 ms** |
| **Budget (GPU time)** | — | 0.5 ms: **within, about 4%** | 0.3 ms: **within, about 33%** |
| FPS, vsync on | 160 | 161 | 167 |
| FPS, vsync off (F8, command-line run) | 995 | 999 | 985 |

Effect A is under the predicted 0.1 ms; Effect B is about at it, and case 3 carries 18 trails, more than the brief's 6 + 6, so it is an upper bound. With vsync on, FPS sits at the display rate in every case; with vsync off it rises to about 1000 (above the refresh rate, so not capped by the compositor) and differs by under 1% between cases, so FPS hides these costs either way. All three vsync-off cases stopped near 1000 FPS; why was not investigated. The vsync key is F8 in `gpu_price.tscn` only; it changes no project setting.

## The process shader

`walker-magic-zhefan/shaders/particles_generated.gdshader`, converted by me in the editor from a scratch `GPUParticles2D` whose `ParticleProcessMaterial` I gave Sparks' direction (1, 0, 0), spread 180, initial velocity 90–160, gravity (0, 300, 0), a scale curve and a colour ramp. Nothing in the game uses it.

| What | Line |
|---|---|
| `shader_type particles;` | 3 |
| `start()` (runs once when a particle is born) | 225–275 |
| `process()` (runs every frame for every particle) | 277–379 |
| initial velocity from its minimum and maximum | 139: `mix(initial_linear_velocity_min, initial_linear_velocity_max, rand)`, turned into a velocity at 264 |
| gravity changes velocity | 311 `force = gravity;` and 324 `USERDATA1.xyz += force * DELTA;` |
| colour over life sampled | 161 `texture(color_ramp, vec2(lifetime))`, called at 347 with the life fraction, written to `COLOR` at 352 |
| scale over life applied | 160 (`scale_curve` sampled) and 369–371 (multiplied into the transform) |
| a line tied to my brief | 139: Sparks' initial velocity 90 / 160 px/s; also 331, damping (Sparks 40–60) |

**Which of my brief's settings live in this shader, and which belong to the draw step?** *(mine, translated from my Chinese)* Put simply, "process" calculates the data and "draw" paints the image. Process decides each particle's motion and life logic, computing its position, deformation and colour at every moment; draw takes those results together with the texture and the blend mode and actually stamps them onto the screen for the player.

For reference, from the shader's uniforms (lines 6–45): direction, spread, initial velocity, gravity, damping, scale and the scale curve, the colour ramp and hue variation are here; amount, lifetime, one-shot, explosiveness, preprocess and `local_coords` are set on the node (emission), and the texture, the CanvasItemMaterial blend mode and `visibility_rect` belong to the draw step.

## What no headless run shows

Whether either effect is visible or reads well, its colour, size and timing on screen, whether the GPU keeps simulating a hidden emitter, and real (not simulated) frame timing. Those are the strips (fixtures) and my checks in the running game above.

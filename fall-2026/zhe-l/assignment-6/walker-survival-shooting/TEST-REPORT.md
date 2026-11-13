# TEST-REPORT — Assignment 6

Every test runs through `./scripts/run-test.sh`, from this folder. Godot 4.7.2-stable, `--headless`.

## Baseline (before A6, 2026-11-10)
| Test | FPS | Result |
|---|---|---|
| `a3_asset_check.gd` | 60 | 55 passed, exit 0 |
| `screen_glow_check.gd` | 30 / 60 / 144 | 24 passed each, exit 0 |
| `normal_map_check.gd` | 60 | 2 passed, exit 0 |
| `test_materials.gd` | 60 | **168 passed, 1 failed**, exit 1 |

The one failure existed before A6: `base.tscn: 3 Light3D nodes (got 4)`. The test counts every light in the scene; the extra one is `ScreenTabletLight` in `player.tscn`, which lights the on-screen tablet. The checks on the three ceiling lights themselves all pass. I decided not to change this test, so the baseline is recorded as "168 passed, 1 failed", never as all passing.

## Effect A: configuration test `test_landing_dust_config.gd`

### Normal run
```bash
./scripts/run-test.sh test_landing_dust_config.gd 60
```
- Result: **157 passed, 0 failed, exit 0** (`logs/test_landing_dust_config_60fps.log`).
- The test was written by the agent (commit 6f3c739b); I reran it and got the same result.
- It first checks with ClassDB that the 44 property names it reads exist in 4.7.2, then loads the scene and reads back every setting the brief names from the loaded resources, with the brief's values as the expected values.

### Mutation 1: rename a property to its Godot 3 name
- **Change:** in `godot/effects/landing_dust.tscn`, `Dust`'s process material, `initial_velocity_min = 0.6` became `initial_velocity = 0.6`.
- **Test result:** **exit 1**, 156 passed, 1 failed: `FAIL Dust initial_velocity_min = 0.6 (got 0.0)` (`logs/mutation_1_godot3_name_60fps.log`).
- **Any error on load:** none. The log has no error or warning; the scene loads and Godot says nothing.
- **Does the effect still fire:** yes. After `restart()`, `emitting = true`; a headless run of the preview scene triggered at frame 10 as usual, with no error. Effect A is wired into the game only in Step 3, so the preview scene stands in for "run the game" here.
- **Why the old name did not fool the test:** 4.7.2's `ParticleProcessMaterial` does still have a property called `initial_velocity`, but it is a **Vector2** (type 5), not Godot 3's float. Its usage flags are 12: shown in the editor, not stored in the scene file. It looks like the inspector control that shows min and max together; it reads back as `(0.0, 0.9)`, exactly (min, max). Writing a float 0.6 to it in the scene file does not match the type and is silently dropped, so `initial_velocity_min` keeps its default of 0.
- **What this means on screen:** the dust's starting speed range changes from 0.6–0.9 to 0–0.9, so some specks barely move outward. The effect is still there, quietly changed. This is the silent failure the assignment describes; only a test that reads the values back catches it.
- The scene was restored (`git diff` empty).

### Mutation 2: change a value without changing the brief
- **Change:** `Dust`'s `amount = 24` became `amount = 30`; CHANGE-BRIEF unchanged.
- **Test result:** **exit 1**, 156 passed, 1 failed: `FAIL Dust amount = 24 (got 30)` (`logs/mutation_2_value_drift_60fps.log`).
- **Meaning:** the expected values are copied from the brief, so as soon as the scene and the brief disagree, the test fails.
- The scene was restored (`git diff` empty); the clean test rerun: 157 passed, exit 0.

## Fixture captures (preview scene)
- r0: `captures/landing_dust/r0/`, four sets: bright / dark background × full fade / retrigger. Commands and the reading are in TUNING.md.
- PNG numbering starts at `frame00000000.png` and matches the preview script's frame count: triggered at frame 10, the picture first changes on frame 11.

## Effect A: state test `test_landing_dust_events.gd` (Step 3)

```bash
./scripts/run-test.sh test_landing_dust_events.gd 60
```
- Mode: pinned 60 fps (no audio is involved, so not realtime).
- Written by the agent (commit cb911e6e). It loads the real `base.tscn` and presses the real Space and D keys with `Input.parse_input_event`, through the InputMap → `PlayerController` → body → `landed` → trigger script. It never calls the trigger function directly.
- Headless, the particles' lifetime cannot be read from `emitting`, so the test reads the `finished` signal, which fires when a burst ends (see the CLAUDE.md correction, commit ba7d1711).

| # | Assertion | Brief rule it covers |
|---|---|---|
| 1 | 60 frames after load: no `landed`, no burst finished, the effect did not move | Never otherwise, including on scene load |
| 2 | First landing: both emitters triggered on the landing frame, the effect at the feet, y ≈ 0.25 | Fires on every landing, at the landing point |
| 3 | Take-off and flight: the feet rose above 0.75 m (a real jump), the effect did not move, no burst finished | Never otherwise |
| 4 | The second landing is 68 frames (1.133 s) after the first, inside Dust's lifetime of 96 frames | Sets up the retrigger case |
| 5 | Exactly 2 `landed`; the second landing 0.525 m from the first; the effect moved to the new feet; both emitters triggered again | Plays again at the new landing point; both emitters replay |
| 6 | The first Dust burst is cleared without finishing; Dust finishes exactly once, one lifetime after the second landing; GroundRing finishes once after each landing | Must use `restart()`, not just `emitting = true` |
| 7 | 120 frames standing afterwards: no `landed`, no burst finished, the effect did not move | Never otherwise |

### First run: 23 passed, 4 failed (exit 1)
- All 4 failures are one problem: **the dust fired on scene load**.
- Cause: on physics frame 1, Jolt's first `move_and_slide()` leaves the player 2.7 mm inside the floor (y = 0.247278) with `is_on_floor()` false; on frame 2 it is pushed back to y = 0.250177, on the floor, which counted as "coming back to the floor from the air".
- This is exactly the "fires on scene load" the brief forbids, and the test caught it. The agent did not fix it on its own; it stopped and waited for my approval.
- The fix (my choice): a `_has_touched_floor` member in `humanoid.gd`; a landing counts only after the body has been on the floor once. The test's assertions were not changed.

### After the fix: 27 passed, 0 failed (exit 0)
- Log: `logs/test_landing_dust_events_60fps.log`.

### Mutation: `restart()` replaced by `emitting = true` (done by the agent, not kept)
- Result: 22 passed, 5 failed. The extra failure is assertion 6: `Dust finished exactly once, at physics frame 282 +/- 2 (Dust finishes [])`.
- So with only `emitting = true`, a Dust burst that is still alive is not started again, and the test catches it. `restart()` was restored afterwards.

### Existing tests (after Step 3, rerun by Claude)
| Test | FPS | Result |
|---|---|---|
| `a3_asset_check.gd` | 60 | 55 passed |
| `screen_glow_check.gd` | 30 / 60 / 144 | 24 passed each |
| `normal_map_check.gd` | 60 | 2 passed |
| `test_materials.gd` | 60 | **168 passed, 1 failed** (the known light count, same as the baseline) |
| `test_landing_dust_config.gd` | 60 | 157 passed |

- During the agent's runs, a Jolt warning (the physics job system exceeded its maximum number of jobs) appeared in two `screen_glow_check` logs; the tests still passed. Claude's rerun of every test, plus 3 more `screen_glow_check` runs at 60 fps, did not show it again; it looks intermittent.

### What this test proves and does not prove
- **Proves (headless):** the real key → brain → body → `landed` → trigger chain works; each jump landing fires once, at the feet; load, take-off, flight and standing do not fire; a second landing inside the lifetime clears the first burst and restarts both emitters.
- **Cannot prove (headless draws nothing):** that the old dust really vanishes on screen, or that at most 25 particles are on screen; height, spread, colour and fade; frame 10 versus frame 11. Those need the frame strips.
- **Flat floor only:** stairs, ramps and walking off a ledge are not tested.

### What I saw in the game (2026-11-11, editor F5)
- On landing there is dust and the ring; no false trigger at the start.
- Not checked: whether it reads clearly from the normal camera, stairs and ledges, and whether the dust suddenly vanishes when the camera turns (`visibility_aabb`).

## The process shader (Step 6)
- File: `godot/shaders/particles_generated.gdshader` (471 lines). In the editor I copied Effect B's `ParticleProcessMaterial` onto a scratch `GPUParticles3D`, made it unique, used "Convert to ShaderMaterial", and saved the generated code here; it is unedited and nothing in the game uses it (commit b9fb4ab1).
- Line references (found by Claude, checked by me):
  - `shader_type particles;`: line 3.
  - `start()`: line 311 (runs once when each particle is born); `process()`: line 364 (runs every frame).
  - Initial velocity from its minimum and maximum: line 231, `mix(initial_linear_velocity_min, initial_linear_velocity_max, rand_from_seed(alt_seed))`; line 353 multiplies it onto the random direction that `spread` decides.
  - Gravity changing velocity: line 397 `force = gravity;`, line 410 `USERDATA1.xyz += force * DELTA;` (both effects have zero gravity, so in practice it changes nothing).
  - Colour over life: line 253 `parameters.color *= texture(color_ramp, vec2(lifetime));`, written back at line 446 `COLOR = params.color;`.
  - Scale: line 242 picks a value between `scale_min` and `scale_max` at birth; lines 456–463 apply it to the particle's transform. Effect B has no `scale_curve`, so this shader has no scale-over-life sampling; one generated from Effect A would.
  - A line tied to a brief setting: line 261 picks a random birth position inside the box, `... * emission_box_extents`, which is the brief's `emission_box_extents = (7, 1.3, 4.5)` (14 × 2.6 × 9 m); line 263 adds `emission_shape_offset`, the brief's (0, 0.15, 3.2).
- **My answer (which brief settings live in this shader, and which belong to the draw step):** This particle process shader handles each particle's birth position, velocity, turbulence, size range, colour and opacity over its age, and the lifetime randomness. The drawing is done by draw_pass_1's QuadMesh and its material: the 0.03 m base quad, the round fading texture, additive blending, per-pixel lighting and facing the camera; the final speck size is that quad multiplied by the scale value from the shader. The particle count amount, the base lifetime and the preprocess time are set on the GPUParticles3D node and are not part of this shader.

## Headless CPU price (Step 7)
```bash
./scripts/run-test.sh cost_effects.gd 60 300
```
- Script `godot/tests/cost_effects.gd`, written by the agent from `prompt-7.txt` (adapted from the chapter's Example 09), committed unedited. 60 warm-up frames, 300 timed frames, 3 repeats per case, run round-robin, pinned at 60 fps. Log: `logs/cost_effects_60fps.log`, no `SCRIPT ERROR` / `SHADER ERROR`.

| Case | Mean ms / frame | Repeat means | Per-frame sd |
|---|---|---|---|
| 1 empty scene (the control) | 0.0041 | 0.0028–0.0048 | 0.0015 |
| 2 `base.tscn`, both effects off | 0.3110 | 0.3025–0.3153 | 0.0561 |
| 3 Effect A, one burst alive on every timed frame | 0.3167 | 0.3134–0.3209 | 0.0670 |
| 4 Effect B, lights on, emitting (1300) | 0.3356 | 0.3215–0.3619 | 0.0686 |
| 5 added control: one `CPUParticles3D` of 10,000 | 1.8764 | 1.8417–1.9375 | 0.1000 |

- **Reading the control:** the empty scene reads 0.004 ms and the game scene 0.31 ms, and the added 10,000-CPU-particle case reads 1.88 ms. So the script does see CPU work; it is not measuring itself (the chapter's 6.90 ms-for-everything failure did not happen: `--fixed-fps` stops the headless frame from sleeping).
- **The effects:** Effect A adds 0.006 ms and Effect B 0.025 ms over the game scene with both off, both inside the noise (the widest repeat-means range, 0.013 / 0.041 ms). This is expected: both are `GPUParticles3D`, and a headless run uses a dummy renderer, so the GPU simulation, preprocess and drawing never run. What is left is the CPU's share (node processing, the listener and trigger scripts), which is near zero by construction. It matches the brief's prediction of "within 0.05 ms" for both.
- **Limit:** case 3 keeps a burst alive by emitting `Player.landed` itself rather than through input; that is enough for a price, and the real input path is covered by the state test. The budgets are GPU time and are compared in Use It, on the RTX 5070 Ti Laptop GPU.

## Use It: what I saw in the running game (2026-11-12, editor F5, window 2048 × 1152, RTX 5070 Ti Laptop GPU)
(My own words after looking by eye. I tend to phrase things with "should" and similar hedges, but these are what I saw, not guesses.)
1. **Effect A, many landings in normal play, including rapid repeats (HUMAN CHECK):** every normal jump landing shows the dust. With rapid jumps, the previous puff is cleared before it has faded and reappears at the new landing point; it never piles up.
2. **Effect A, darkest and lightest floor (HUMAN CHECK):** the dust itself stays about as bright; it does not turn dark in shadow. But when the background changes, how clearly its outline reads does change; it is not equally clear in light and dark.
3. **Effect A, edge of screen (HUMAN CHECK):** I cannot say this is fine yet. The dust quads were enlarged but the visibility box was not, so whether the dust disappears early when the camera turns needs another check. Claude checked the numbers: `visibility_aabb` is (−0.6, −0.1, −0.6, 1.2, 0.3, 1.2), reaching 0.2 m up and 0.6 m out; since r1 the puffs' top edge is about 0.23 m and they reach about 0.68 m out, both outside the box. So this is a **known limitation**; the next step is to enlarge Effect A's `visibility_aabb` (as a revision of its own).
4. **Effect A, scene load (HUMAN CHECK):** no dust appears on its own at the start, as in the earlier checks. The character has to touch the floor first and then come down from the air to trigger it.
5. **Effect B, the first frames after load (HUMAN CHECK):** the dust is already spread out when it first appears; it does not build up bit by bit. "Full" here means a settled spread across the whole area, not dense dust everywhere on screen.
6. **Effect B, start and stop (HUMAN CHECK):** after lights off the dust disappears at once; after lights on it is back to its full spread quickly. The light and the dust may be one frame apart (the strip shows exactly one frame), but it never takes seconds to build up.
7. **Effect B, dark wall and light wall (HUMAN CHECK):** the dust is fairly faint now and no longer steals the scene. Which wall shows it more clearly also depends on whether the specks are lit; a darker background does not simply make it clearer.
8. **Effect B, edge of screen (HUMAN CHECK):** the visibility box grew with the room and has a margin; ordinary camera turns show no clear problem; whether it never pops at the room's edges I cannot say for sure yet.
9–11. **GPU price, FPS:** to be filled from the Visual Profiler.
12. **Claude against me:** I found nothing that clearly conflicts with Claude's records. One thing to note: the strip set called the "dark background" actually has a very bright light patch, so the two set names cannot be taken as the darkest and lightest places in the game. (My disagreements with Claude are recorded in TUNING, Effect A: the warm tint, the capsule hiding the dust, 6–8 puffs not separate, the cut-off bottoms; in the game I do not see them as problems.)

### GPU price and FPS (Use It, HUMAN CHECK)
- **GPU:** NVIDIA GeForce RTX 5070 Ti Laptop GPU (the discrete GPU; named in the Visual Profiler and the startup line `Using Device #0`). Display refresh rate 144 Hz.
- **Visual Profiler (editor F5, my screenshot):** one selected frame (12619): the whole viewport render about 2.03 ms GPU; "Update GPU particles" 0.01 ms GPU. In the frame-time graph, lights off and lights on differ much more than any effect (three shadowed omni lights), so the effects' own share could not be read from that graph.
- **Effect on / off with the lights kept on:** `godot/debug/gpu_price.gd` (a helper Claude wrote; windowed, vsync off, 300 frames per state after 120 warm-up frames) reads the same engine measurement, `RenderingServer.viewport_get_measured_render_time_gpu`. I ran it once; Claude ran it twice more to read the numbers (`logs/gpu_price.log`):

| State (lights on) | Run 1 mean GPU ms | Run 2 mean GPU ms |
|---|---|---|
| Effect B shown (1300 particles) | 0.540 | 0.542 |
| Effect B hidden | 0.522 | 0.525 |
| Effect B shown + Effect A bursting | 0.542 | 0.542 |

- **Against the budget:** Effect B adds about **0.017–0.018 ms** GPU (budget ≤ 0.3 ms); Effect A adds about **0.000–0.001 ms** (budget ≤ 0.2 ms). Both are well inside their budgets. The helper's total (about 0.54 ms) is lower than the profiler frame (2.03 ms); the profiler frame was taken in a different moment and view during an editor run, so only differences inside one run are compared.
- **FPS (vsync debug key V):** with vsync on, the Monitors FPS reads 144 (the refresh rate). Pressing V prints `[vsync] off` and FPS rises to about 1350; pressing V again prints `[vsync] on` and it returns to 144. So the comparison is not capped by the compositor. I did not record separate FPS values with each effect off and on; the GPU time above is the primary number.

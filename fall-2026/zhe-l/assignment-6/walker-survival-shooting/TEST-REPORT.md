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
- File: `godot/shaders/particles_generated.gdshader` (471 lines). In the editor I copied Effect B's `ParticleProcessMaterial` onto a scratch `GPUParticles3D`, made it unique, used "Convert to ShaderMaterial", and saved the generated code here; it is unedited and nothing in the game uses it (commit 5e977e83).
- Line references (found by Claude, checked by me):
  - `shader_type particles;`: line 3.
  - `start()`: line 311 (runs once when each particle is born); `process()`: line 364 (runs every frame).
  - Initial velocity from its minimum and maximum: line 231, `mix(initial_linear_velocity_min, initial_linear_velocity_max, rand_from_seed(alt_seed))`; line 353 multiplies it onto the random direction that `spread` decides.
  - Gravity changing velocity: line 397 `force = gravity;`, line 410 `USERDATA1.xyz += force * DELTA;` (both effects have zero gravity, so in practice it changes nothing).
  - Colour over life: line 253 `parameters.color *= texture(color_ramp, vec2(lifetime));`, written back at line 446 `COLOR = params.color;`.
  - Scale: line 242 picks a value between `scale_min` and `scale_max` at birth; lines 456–463 apply it to the particle's transform. Effect B has no `scale_curve`, so this shader has no scale-over-life sampling; one generated from Effect A would.
  - A line tied to a brief setting: line 261 picks a random birth position inside the box, `... * emission_box_extents`, which is the brief's `emission_box_extents = (7, 1.3, 4.5)` (14 × 2.6 × 9 m); line 263 adds `emission_shape_offset`, the brief's (0, 0.15, 3.2).
- **My answer (which brief settings live in this shader, and which belong to the draw step):** This particle process shader handles each particle's birth position, velocity, turbulence, size range, colour and opacity over its age, and the lifetime randomness. The drawing is done by draw_pass_1's QuadMesh and its material: the 0.03 m base quad, the round fading texture, additive blending, per-pixel lighting and facing the camera; the final speck size is that quad multiplied by the scale value from the shader. The particle count amount, the base lifetime and the preprocess time are set on the GPUParticles3D node and are not part of this shader.

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

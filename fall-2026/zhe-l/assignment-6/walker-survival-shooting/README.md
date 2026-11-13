# walker-survival-shooting — Assignment 6

A third-person 3D extraction shooter. The player lives in a subway base, carries a rugged military tablet, goes out to fight monsters and extracts. This assignment (Assignment 6) adds two particle effects: **landing dust** at the player's feet whenever the player lands from a jump, and **dust in the air** of the base room, lit by the ceiling lights, that exists only while the lights are on.

## Starting point and versions
- **Starting point:** my Assignment 5 project (course repository `assignment-5/`, tag `zhe-l-a5`), plus the wall light switch, the `CeilingLights` keeper, F to interact and the one-handed tablet window added before this assignment (the first Assignment 6 upload).
- **Godot:** 4.7.2-stable (Windows), renderer **Forward+**, D3D12, Jolt Physics. Window 2048 × 1152.
- **GPU used for the GPU price:** NVIDIA GeForce RTX 5070 Ti Laptop GPU.
- **Claude Code:** Claude Opus 5.5.

## How to run
1. Open `godot/project.godot` in Godot 4.7.2; import once first: `godot --headless --path godot --import`.
2. Run the main scene `base.tscn` (F5).

**Controls:** WASD to move, Shift to sprint, Space to jump, right mouse button to aim, Tab to take out / switch / put away the tablet, **F** to use the wall light switch, **V** to toggle vsync (debug key for the FPS comparison; it prints `[vsync] off` / `[vsync] on`).

**Seeing the effects:**
- **Effect A, landing dust:** jump (Space) anywhere on the floor. A low, slightly warm grey puff and a faint ground ring appear where the player lands; landing again before it has faded clears it and plays it at the new spot.
- **Effect B, light dust:** the room is full of faint, cool-white specks of different sizes, brighter near the ceiling lights. Press F at the wall switch: the lights and the dust go off together; press F again and the dust is back at once, already spread out.
- **Preview scenes (test fixtures):** `godot/previews/landing_dust_preview.tscn` and `godot/previews/light_dust_preview.tscn` replay each effect on a fixed timeline for the frame strips. Effect B's preview also takes `-- hold` to keep the lights on.

## How to run the tests
Every test runs through `scripts/run-test.sh <test file> <fps|realtime> [timeout]`. It always runs headless, adds a timeout, pins the frame rate, keeps a log in `logs/`, and fails on `SHADER ERROR` / `SCRIPT ERROR`. Set `GODOT` to the Godot console executable if `godot_console` / `godot` is not on `PATH`.

```bash
./scripts/run-test.sh a3_asset_check.gd 60
./scripts/run-test.sh screen_glow_check.gd 30
./scripts/run-test.sh screen_glow_check.gd 60
./scripts/run-test.sh screen_glow_check.gd 144
./scripts/run-test.sh normal_map_check.gd 60
./scripts/run-test.sh test_materials.gd 60
./scripts/run-test.sh test_landing_dust_config.gd 60
./scripts/run-test.sh test_landing_dust_events.gd 60
./scripts/run-test.sh test_light_dust_config.gd 60
./scripts/run-test.sh test_light_dust_state.gd 60
./scripts/run-test.sh cost_effects.gd 60 300
```

Expected: 55 / 24 / 24 / 24 / 2 / **168 passed, 1 failed** / 157 / 27 / 110 / 41 passed. The one failure in `test_materials.gd` existed before this assignment: it counts every `Light3D` in `base.tscn` and expects 3; the fourth is the on-screen tablet's light. `cost_effects.gd` prints per-case CPU times (no pass count). Details and the frame strips are in `TEST-REPORT.md` and `TUNING.md`.

Frame strips are captured in a real window with Movie Maker (the output folder must exist first), for example:

```bash
godot_console --path godot res://previews/light_dust_preview.tscn --write-movie "$(pwd -W)/captures/light_dust/redesign-2/dark/frame.png" --fixed-fps 30 --quit-after 100 -- dark
```

## What this assignment added
- **Effect A, landing dust** `godot/effects/landing_dust.tscn`: one `Node3D` with two `GPUParticles3D`, `Dust` (24 soft billboard puffs) and `GroundRing` (one flat ring). Fired by `godot/effects/landing_dust_trigger.gd` on the body's new notify-only `landed` signal in `humanoid.gd`; retrigger uses `restart()`.
- **Effect B, light dust** `godot/effects/light_dust.tscn`: one `GPUParticles3D`, 1300 particles over a 14 × 2.6 × 9 m box, lit per pixel, additive, with turbulence and a twinkling opacity ramp, 6 s preprocess. Driven by `godot/effects/light_dust_listener.gd`, which listens to `CeilingLights.lights_changed`, queries the start state once, and stops on hide.
- **Tests:** configuration tests for both effects, state tests driven by real key presses (Space and D; S and F), and the headless cost script `tests/cost_effects.gd`.
- **Preview scenes** for both effects, and the frame strips in `captures/` (fixture captures).
- **Debug helpers:** `godot/debug/vsync_toggle.gd` (V) and `godot/debug/gpu_price.gd` (prints the GPU time with Effect B shown, hidden, and with Effect A bursting).
- **The generated process shader** `godot/shaders/particles_generated.gdshader`, converted in the editor from Effect B's `ParticleProcessMaterial`; nothing in the game uses it.
- **Textures:** none from outside. Both effects draw with `GradientTexture2D` resources defined in their scene files (a round soft dot and a thin ring).
- **Documents:** `CLAUDE.md` (agent draft plus my review), `CHANGE-BRIEF.md` (with dated revisions), `TUNING.md`, `TEST-REPORT.md`, `../FRICTIONAL.md`, `SOURCES.md`; prompts (`prompt-*.txt`, `approve-*.txt`), session transcripts and labelled excerpts beside them.

## Known limitations
- **Effect A's `visibility_aabb` was not enlarged when its quads grew in r1.** The puffs now reach about 0.23 m up and 0.68 m out, beyond the 0.2 m / 0.6 m box, so they may disappear early near the screen edge. Next step: enlarge it as its own revision.
- Effect A still reads slightly warm and as a ring of soft puffs whose bottoms are cut by the floor; I judged it good enough in the game (TUNING.md).
- Effect B was widened to the whole room by a redesign (dated brief revisions), not by one-setting tuning rounds; its predictions exist only for r1.
- `landing_dust_preview.tscn` also loads `base.tscn`, so any new Effect A strip would now include the light dust.
- The state tests count Effect B restarts through the listener's own counter; headless, a continuous emitter shows no other sign of a restart.
- Stairs, ramps and walking off a ledge were not tested for Effect A.
- The game has no pause feature yet (the pause rule is tested by setting `get_tree().paused`), and no playable combat or extraction yet.

## Explainer film
- To be added: title, media link, file name and SHA-256, and the game-source revision shown.

# Plan: wire Effect B (`RunDust`) and add its state test

I haven't created or edited any file, or run Godot or the tests. I read `CLAUDE.md`, the brief, `game/effects/effects_driver.gd`, `game/app/main.tscn`, `game/content/rudy/rudy.gd`, `game/effects/run_dust.tscn`, `game/tests/test_slash_sparks_state.gd` and the parts of `main.gd` and `level_1.tscn` the test depends on.

## Two facts the plan rests on

- **Draw order and tick order pull in different directions.** The brief wants `RunDust` before Rudy in the tree, so it draws behind him. But the driver (`Main/Effects`) has to stay after Rudy. Effect A's state test (S4) relies on the driver reading Rudy's state on the same tick Rudy changes it, after `move_and_slide()`. So the emitter can't go under `Effects`. It gets its own container between `Level1` and `Rudy`, and the existing driver drives it from where it is.
- **This is not a feedback loop.** Effect B is on/off on a condition, and nothing in the brief scales it by a game value. So the `amount_ratio` rule does not apply, and the driver never touches `amount_ratio` or `amount`. The test still checks every tick that `amount` stays 40 and `amount_ratio` stays 1.0, as a guard. That guard covers ticks at several speeds, while he speeds up and slows down.

## Steps

### Step 1: add the emitter to Main
**Changes:** `game/app/main.tscn`.
- Add an `ext_resource` for `res://effects/run_dust.tscn`.
- Add a `DustTrail` node (`Node2D`, a container like `SlashBursts`) between `Level1` and `Rudy`, with one instance of `run_dust.tscn` as its child, `RunDust`.
- Nothing else in `main.tscn` changes, and none of `RunDust`'s properties are overridden in the instance.

**Brief wording to confirm:** this places the emitter in the scene file, not by code at run time as the brief literally says. I recommend the scene file: it's simpler, and a test can read it. Moving the node from code in `_ready` would need a deferred call.

The existing tests look only for named children of Main, `FlyingGear` children and `ShaderMaterial` users (`checks.gd:59`, `:804-819`; `invulnerable_tint_checks.gd:148-156`). A new `Node2D` with a `GPUParticles2D` child should not change their counts. Step 4 confirms that.

### Step 2: drive the emitter from the existing driver
**Changes:** `game/effects/effects_driver.gd`.
- Add one `@onready var _run_dust: GPUParticles2D = get_node("../DustTrail/RunDust")` and one offset constant, `Vector2(0, -4)`.
- At the end of `_physics_process`, after Effect A's code, call a new `_drive_run_dust()` that:
  1. sets `_run_dust.global_position = _rudy.global_position + offset` on every tick (B2). When he isn't running it moves without emitting, so a respawn jump lays down nothing (B5);
  2. computes `running := _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and absf(_rudy.velocity.x) > 1.0`, which is the brief's condition (B1);
  3. computes `want := running and _run_dust.is_visible_in_tree()` (B4);
  4. assigns `_run_dust.emitting = want` only when it differs, so it doesn't call the renderer on every tick.
- The driver doesn't run while the tree is paused, so `emitting` keeps its value (B3).
- Update the header comment to describe Effect B.
- It reads only game state and writes only `RunDust`'s position and `emitting`. No particle or material property is set, and `rudy.gd` gets no signal.

### Step 3: the state test
**Creates:** `game/tests/test_run_dust_state.gd` (`extends Node`) and `game/tests/test_run_dust_state.tscn`, a one-node scene like `test_slash_sparks_state.tscn`.

**How it records:** the test node is Main's parent, so its `_physics_process` runs first in each tick. Like Effect A's recorder, it reads the state as it stood at the end of the tick before. On each unpaused tick it records:
- the brief's condition, read from Rudy;
- `RunDust.emitting` and `is_visible_in_tree()`;
- the emitter's and Rudy's global positions;
- `amount` and `amount_ratio`;
- `velocity.x`.

Condition and `emitting` are sampled at the same moment. If the driver lagged a tick (for example, if it ran before Rudy), every edge would show up as a mismatch.

**How it drives the game:** only through real input (`move_left`, `move_right`, `jump`, `pause`, `restart`) in the real game loop. It never calls `_drive_run_dust()`. The main sequence writes no game state at all, not even a teleport: it keeps Rudy at the opening, between the left bound (x 0) and SpikesA (x 1065), by running each way in turn. The only nodes it writes are `RunDust.visible` and `DustTrail.visible`, for B4. Those are presentation nodes.

| Check | What it does and asserts | Rule |
|---|---|---|
| D1 | Main with the title showing; `move_right` held 30 ticks: `emitting` false every tick, mode `WAITING` | B1 (load, title) |
| D2 | Tap `restart` to start play; stand 30 ticks: `emitting` false every tick | B1 (stands) |
| D3 | Hold `move_right`: exactly one rising edge of the condition and one of `emitting`, on the same recorded tick | B1 (start) |
| D4 | On every tick the condition holds, emitter = Rudy + (0, −4) within 1 px. Prints the tick count and the largest error | B2 |
| D5 | Release: `emitting` falls on the same tick the condition falls, once speed is ≤ 1 px/s | B1 (stop) |
| D6 | Running right, switch to `move_left`: condition and `emitting` both false on the turn tick (the turn zeroes speed) and through the hold, true again on the same tick once he moves left | B1 (turn) |
| D7 | Running right, tap `jump`: both false from take-off through the air, true again on the landing tick (still holding) | B1 (jump, land) |
| D8 | Running, tap `pause`, wait 30 ticks: `emitting` stays true, `can_process()` false, emitter position unchanged. Tap `pause` again: `can_process()` true, `emitting` true | B3 (node state) |
| D9 | Running, set `RunDust.visible = false`: `emitting` false on the next tick while the condition holds. Set it back to true: `emitting` true on the next tick | B4 (the node hidden) |
| D10 | The same with `DustTrail.visible = false`: `is_visible_in_tree()` false, `emitting` false. This is the parent-hidden case where the probe saw `emitting` stay true without driver code | B4 (a parent hidden) |
| D11 | The whole run: on every unpaused recorded tick, `emitting == (condition and is_visible_in_tree())`. Prints 0 mismatches, plus `amount == 40` and `amount_ratio == 1.0` throughout, with the number of distinct speeds seen | B1 overall; the amount guard |
| D12 | Placement: `RunDust`'s parent is `DustTrail`, `DustTrail` comes before `Rudy` among Main's children, and neither Rudy nor `Look` is its ancestor | Brief §3 draw order; B5 (not under `Look`) |

### Step 3b (optional, approve or drop): knockback and respawn
**Changes:** the same test file.
- **D13, real input only:** run right into SpikesA. On the hit tick (mode `HURT`, knocked back) the condition and `emitting` both go false together. This covers B1's knockback case.
- **D14, a fall and a respawn:** this needs one teleport to about x 4200 on Segment 1, since walking there passes goblins. That writes Rudy's position, as Effect A's test and `checks.gd` already do. Then he holds `move_right` off the cliff and falls past the kill line. `emitting` must be false from the tick he leaves the floor through the respawn. The emitter's jump to the checkpoint must fall on a tick with `emitting` false. When he runs again after control returns, `emitting` must go true.
- Without 3b, knockback, falling out, respawn, defeat and the circle are covered only by the code, which reads `mode`, and by eye.

### Step 4: run everything through the wrapper
**Creates or updates:** logs in `logs/`. No game files change.
- `./scripts/run-test.sh test_run_dust_state.tscn 60`, at a fixed 60 fps. It doesn't wait on audio, so it doesn't need realtime. If 120 s is too short for 3b, I'd add the third argument, 300.
- `./scripts/run-test.sh checks.tscn 60`: expect 141 PASS.
- `./scripts/run-test.sh invulnerable_tint_checks.tscn 30`, then the same at `60` and `144`: expect 15 PASS each.
- `./scripts/run-test.sh test_slash_sparks_state.tscn 60`, `./scripts/run-test.sh test_slash_sparks_config.tscn 60` and `./scripts/run-test.sh test_run_dust_config.tscn 60`. I'll check each file's real name and extension before running it.
- `git diff --stat game/shaders/` must print nothing.
- I'll show the real output of each run and the mode it used. No commit.

### Step 5 (optional): two driver mutations
**Changes:** `effects_driver.gd` temporarily, reverted afterwards and never committed.
1. Drop `is_visible_in_tree()` from the driver: D9, D10 and D11 should fail.
2. Move `DustTrail` after `Effects` in `main.tscn`: D12 should fail.

This mirrors Effect A's `mutation_driver_*` logs.

## What the headless test proves, and what it cannot

**It proves**, for the paths it drives:
- the driver's node state follows the brief on every tick: `emitting` matches the condition with no lag through load, title, standing, run, stop, turn, jump and land, and through knockback and respawn with 3b;
- the emitter sits at his feet within 1 px;
- a pause leaves `emitting` and the position unchanged, and the node doesn't process;
- hiding the node or its parent forces `emitting` false, and showing it restores `emitting` on the next tick;
- the driver never changes `amount` or `amount_ratio`;
- the tree order puts the emitter behind Rudy and outside `Look`.

**It cannot prove**, because the dummy renderer draws nothing and runs no GPU particle process:
- that any puff is drawn, or that one is visible within two frames;
- that the puffs form a world-space band rather than a clump;
- that no puff is born while paused or hidden;
- that puffs freeze visibly and carry on after a pause;
- colour, contrast, size, timing or variation;
- that the dust actually draws behind Rudy and in front of the ground (only the tree order is read);
- culling at the screen edge;
- GPU price.

It also only sees the transitions it drives. Defeat and the teleport circle are covered by reasoning about the `mode` check, not by a test.

## What only a human can check

- **B3:** press Esc while running; the puffs hold still and stay visible, then carry on.
- **B5:** run while invulnerable after a hit and confirm the dust doesn't flash. Die and respawn while holding a direction, and confirm no streak is drawn.
- **How it reads in play** at 1280 × 720, at full speed over the wheat and the ground.
- **Draw order:** behind Rudy's boots, in front of the ground.
- **Scene load:** no dust in the first frames after start and after Enter on the end card.
- **Edge of screen:** at both level ends.
- **GPU price** (brief §8). The F9 debug node is not part of this plan.
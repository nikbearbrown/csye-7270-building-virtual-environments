# TEST-REPORT — Assignment 6, walker-rudy

What each test establishes, what it cannot establish, and the mutations that show it can fail. Sections are added as the steps are done.

**How this file is written.** Claude Code ran the tests and mutations below at my request and drafted this report from their logs; I decided each step. Every run used Godot 4.7.2 headless through `scripts/run-test.sh`, unless the row says otherwise.

---

## Step 2 — Effect A's configuration test

`game/tests/test_slash_sparks_config.gd` (`extends SceneTree`) loads `game/effects/slash_sparks.tscn` and checks 108 things against the brief's values: the root and its two emitters, every emission, process, draw and culling setting in the brief's table for `Flash` and `Sparks` (as revised: 28 sparks), the textures, the curves and the colour ramps. It reads the Godot 4 `_min`/`_max` values from the loaded resources, never whether a name exists. Because Godot 4.7.2 maps some Godot 3 names silently (`CLAUDE.md`, "Godot 4 names"), it also scans the scene's text for Godot 3 class names and property lines.

| Run | Result | Log |
|---|---|---|
| The effect as committed (`fed848b8`), 60 fps | 108 of 108, exit 0 | `logs/test_slash_sparks_config_60fps.log` |
| The same at 30 and 144 fps, after the agent's build (`ea4419ae`, 14 sparks) | 108 of 108 each, exit 0; those two logs were not kept | — |
| The existing tests, after the effect was added | `checks.tscn` 141 of 141 at 60 fps (it now finds 83 `res://` paths, all present); `invulnerable_tint_checks.tscn` 15 of 15 at 30, 60 and 144 | `logs/checks_60fps.log`, `logs/invulnerable_tint_checks_*fps.log` |

**What a pass establishes:** the effect scene is configured as the brief says, with Godot 4 names, and the brief and the scene have not drifted apart.

**What it cannot establish:** that the effect fires on the right event, at the right place, or the right number of times (Step 3's state test); and anything about the look. Headless, nothing is drawn (`CLAUDE.md`, "Headless facts"). The look comes from the frame strips and my verdict (`TUNING.md`).

### Mutations

Each mutation changed one line of `game/effects/slash_sparks.tscn` and left everything else, including the brief and the test, alone. After each one Claude restored the file with `git checkout`; its SHA-1 was `2ebf93f7d46d84267398cdfed28e668c5cafe8ae` before and after both mutations. The test then passed 108 of 108 again, and its log was identical to the committed one.

| Mutation | The line changed | Expected | Result | Log |
|---|---|---|---|---|
| **1. A Godot 3 name.** One property the brief names, renamed to its Godot 3 name | Line 77, in `Sparks`' material: `initial_velocity_min = 260.0` → `initial_velocity = 260.0` | Exit 1: the scene loads without a message, with velocity 0 to 420, not 260 to 420 (CHANGE-BRIEF.md, Revision 2) | **Exit 1, 2 failures:** the text scan found `initial_velocity = 260.0`, and `Sparks initial_velocity_min` read 0.0 instead of 260.0. `initial_velocity_max` still read 420.0. | `logs/mutation_godot3_name_60fps.log` |
| **2. A value changed, the brief not.** | Line 76, in `Sparks`' material: `spread = 30.0` → `spread = 45.0` | Exit 1, on the spread check | **Exit 1, 1 failure:** `Sparks spread is 30.0`, read 45.0 | `logs/mutation_value_drift_60fps.log` |

**Mutation 1 in a window.** The assignment asks to run the game with the mutation and note that the effect still fires. The effect is not wired into the game until Step 3, so Claude ran the preview instead: a 30 fps Movie Maker run of `game/previews/slash_sparks_preview.tscn` with the mutated scene (`logs/capture_mutation_godot3_name.log`; frames 12 and 15 kept in `captures/slash_sparks/mutation_godot3_name/`, fixture captures). The burst fired on frame 10, as before. Beside r1's frames 12 and 15 it still reads as a spray; the only visible difference is a knot of slow sparks left near the hitbox on frame 15. That is the silent failure the test exists for: nothing in the log or the picture announces it.

**Did the version translate the old name?** Not this one. Godot 4.7.2 keeps `initial_velocity` only as an editor range that is never saved, so the number on that line sets both ends of the range to 0, and the `initial_velocity_max` line after it sets the top end back to 420 (`logs/probe_mutation.log:4`). It does translate `Particles2D`, `ParticlesMaterial` and `flag_disable_z` (`logs/probe_mutation.log:7-10`). No loaded value can show those three, so only the text scan would catch them; that is why mutation 1 failed two checks rather than one.

## Step 3 — Effect A's state test

`game/tests/test_slash_sparks_state.tscn` (with `test_slash_sparks_state.gd`) runs the real `Main` at 60 fps through the wrapper, not in realtime, because it does not wait on audio. Every cut comes from the real `slash` action, the sword from walking into the pickup with `move_right`, and the pause from the real `pause` action; the test never calls the driver. The only game state it writes is Rudy's position, and once his velocity for the stomp, the same setup `checks.gd` uses. The driver, `game/effects/effects_driver.gd`, sits after `Rudy` in `game/app/main.tscn`, so it sees the hitbox go live on the tick `_swing()` makes it.

| Check | Rule | Result at 60 fps (`logs/test_slash_sparks_state_60fps.log`) |
|---|---|---|
| S1 no burst on load and on the title, with slash pressed there | A1 | PASS: 0 bursts, state TITLE |
| S2 no burst on load with the title skipped | A1 | PASS: 0 bursts |
| S3 slash without the sword: no burst, no live edge | A1 | PASS |
| S4 one cut: exactly one burst, born on the tick the hitbox went live | A1 | PASS: born on tick 214, edge on tick 214 |
| S5 facing right: on the hitbox within 1 px, not mirrored | A2 | PASS: burst and hitbox both at (2518.0, 764.0), x axis +1 |
| S6 facing left: on the hitbox within 1 px, mirrored | A2 | PASS: both at (2418.0, 764.0), x axis −1 |
| S7 two cuts 19 ticks apart: two bursts alive at the second; the first the same node, not moved, still emitting | A3 | PASS |
| S8 the first burst leaves the tree 25–30 ticks after its birth | A3 | PASS: 27 ticks |
| S9 mashing slash: one burst per live edge per swing, never more than 2 alive | A1, A3 | PASS: 7 swings, 7 edges, 7 bursts, at most 2 alive |
| S10 every burst under `Effects/SlashBursts`, never under Rudy or a goblin | A4 | PASS: 11 bursts, 0 outside |
| S11 a cut defeats a goblin: the goblin hides while the burst is still visible, every tick of its life | A4 | PASS: visible 27 ticks, hidden 0 |
| S12 a stomp with the sword: no burst, no live edge | A1 | PASS |
| S13 slash while paused: no burst then, none in the 10 ticks after resuming | A1 | PASS |
| S14 a burst alive at a pause stays in the tree, visible and emitting, and stops processing until resumed | A5 (headless part) | PASS |

After the effect was wired in, Claude reran the other tests through the wrapper: `checks.tscn` 141 of 141 at 60 fps (it now finds 85 `res://` paths, all present); `invulnerable_tint_checks.tscn` 15 of 15 at 30, 60 and 144; `test_slash_sparks_config.gd` 108 of 108 at 60.

### Mutations of the driver

The approved plan's step 4. The implementation session made each change, ran the state test at 60 fps and restored the file; the two runs' output is in its transcript and was copied out by Claude into the logs below. After the restores, `effects_driver.gd` and `main.tscn` were the same blobs as after step 1 (`0f8c60e6`, `b6ab510bd`), and the test passed 14 of 14 again.

| Mutation | Expected | Result | Log |
|---|---|---|---|
| **a. One reused burst:** the driver keeps one `SlashSparks` and sets `emitting = true` on it again for every cut (predicted failure 4) | S7 and S8 fail | **Exit 1, 6 failures:** S6, S7, S8, S9, S11, S14. No new burst enters the tree after the first, so every check that looks for a new burst fails. S8 fails because no second burst was recorded (`-1 ticks`), not because it measured a restarted life | `logs/mutation_driver_reuse_60fps.log` |
| **b. The driver one tick late:** `Effects` moved before `Rudy` in `main.tscn` | S4 fails | **Exit 1, 2 failures:** S4 (born on tick 215, edge on 214) and S7, which also checks the second burst's birth tick | `logs/mutation_driver_order_60fps.log` |

**What the state test establishes:** each live cut makes exactly one burst on that tick, at the hitbox, mirrored with Rudy's facing; nothing else makes one; two quick cuts overlap without the first being restarted, moved or cut short, with at most two alive; no burst belongs to Rudy or a goblin; and a paused burst stops processing.

**What it cannot establish:** that anything is drawn, since the dummy renderer draws nothing and the 27-tick life is the node's own clock; that the sparks fly the way Rudy faces, since only the node is mirrored (failure 8); that paused sparks really hold still; and real key presses, since the input goes through `Input.action_press`.

**My check in the running game** (2026-11-04, after the effect was wired in): I played the game and found no problem [我已经进到游戏里看过了，没问题]. I did not record which of the eye checks I made one by one: a cut facing left, a cut on a goblin, Esc right after a swing (A5), a cut at the top of a jump and over the pit, both screen edges, and the first frames after loading. Those are still to be recorded item by item.

## Step 5 — Effect B's configuration test, state test and mutations

### The configuration test

`game/tests/test_run_dust_config.gd` (`extends SceneTree`) checks 61 things against the brief as revised (Revision 4): every emission, process, draw and culling setting of `RunDust`, its texture, curve and ramp, and the features Effect A does not use, damping (`damping_min` / `_max` 120 / 180, no damping curve) and the box emission shape (`emission_box_extents` (14, 3, 0)). Like Effect A's, it also scans the scene's text for Godot 3 names. 61 of 61 at 60 fps (`logs/test_run_dust_config_60fps.log`).

| Mutation of `game/effects/run_dust.tscn` | Expected | Result | Log |
|---|---|---|---|
| **1. A Godot 3 name**, line 40: `damping_min = 120.0` → `damping = 120.0` | Exit 1: `damping_min` loads as 0, and the `damping_max` line after it keeps 180 | **Exit 1, 2 failures:** the text scan found `damping = 120.0`, and `RunDust damping_min` read 0.0 instead of 120.0. `damping_max` still read 180.0 | `logs/mutation_dust_godot3_name_60fps.log` |
| **2. A value changed, the brief not**, line 36: `spread = 50.0` → `spread = 70.0` | Exit 1, on the spread check | **Exit 1, 1 failure:** `RunDust spread is 50.0`, read 70.0 | `logs/mutation_dust_value_drift_60fps.log` |

After each one Claude restored the file with `git checkout`; its SHA-1 was `e710ef3513705d3c76c10cc95f4a5ee51458dabf` before and after both, and the test passed 61 of 61 again with a log identical to the committed one.

**Mutation 1 in a window.** Claude captured the preview with the mutated scene (`logs/capture_mutation_dust_godot3_name.log`; frame 25 kept in `captures/run_dust/mutation_godot3_name/`, a fixture capture). The trail still started on frame 10 and still reads as the same band; with some puffs now barely damped it reaches a little higher, its top about 69 px above the walk line against r3's 58, and the frame differs from r3's by at most 37 levels. Nothing in the log or the picture announces the fault.

### The state test

`game/tests/test_run_dust_state.tscn` (with `test_run_dust_state.gd`) runs the real `Main` at 60 fps through the wrapper, not in realtime, because it does not wait on audio. It moves Rudy only with the real `move_left`, `move_right`, `jump`, `pause` and `restart` actions and never calls the driver. It writes game state once, a teleport to x 4200 for D14, the same kind of setup `checks.gd` uses, and it sets `visible` on `RunDust` and `DustTrail`, which are presentation nodes, for B4. `RunDust` sits in `DustTrail` before `Rudy` in `game/app/main.tscn`, so it draws behind him; the driver, after Rudy, places it and switches `emitting` on the tick Rudy's state changes.

| Check | Rule | Result at 60 fps (`logs/test_run_dust_state_60fps.log`) |
|---|---|---|
| D1 on load and on the title, `move_right` held 30 ticks: never emitting | B1 | PASS: 30 ticks, 0 emitting, mode WAITING |
| D2 play started, standing 30 ticks: never emitting | B1 | PASS |
| D3 `move_right` held: one rising edge of the condition and of `emitting`, on the same tick | B1 | PASS: both on tick 64 |
| D4 every running tick, the emitter at Rudy + (0, −4) within 1 px | B2 | PASS: 121 ticks, largest error 0.000 px |
| D5 released: `emitting` falls on the tick the condition falls | B1 | PASS: both on tick 128 |
| D6 a turn while running: both false through the turn, both true again on the same tick | B1 | PASS: fell on 143, rose on 150 |
| D7 a jump while running: both false in the air, both true on the landing tick | B1 | PASS: 41 air ticks, 0 emitting |
| D8 paused while running: `emitting` stays true, the node does not process, the emitter does not move; on resume it processes | B3 (node state) | PASS |
| D9 `RunDust` hidden while running: `emitting` false on the next tick, true again when shown | B4 | PASS |
| D10 `DustTrail`, its parent, hidden: the same | B4 | PASS |
| D11 on every recorded tick, `emitting == (condition and visible in the tree)`; `amount` 40 and `amount_ratio` 1.0 throughout | B1, and the feedback-loop rule's guard | PASS: 380 ticks, 0 mismatches, 13 distinct speeds |
| D12 `RunDust` under `DustTrail`, before `Rudy`, and under neither Rudy nor `Look` | section 3's draw order, B5 | PASS |
| D13 a hit on SpikesA while running: condition and `emitting` fall together on the hit tick | B1 (knockback) | PASS: both on tick 229 |
| D14 off a cliff, out and respawned: no emitting from leaving the floor until control returns, the emitter's jump to the checkpoint on a tick without emitting, emitting again when he runs | B1, B5 | PASS |

Effect B is switched by a condition, not scaled by a game value, so the feedback-loop rule about `amount_ratio` does not apply; D11 checks instead that the driver never changes `amount` or `amount_ratio`.

After Effect B was wired in, Claude reran the other tests: `checks.tscn` 141 of 141 (88 `res://` paths, all present), `invulnerable_tint_checks.tscn` 15 of 15 at 30, 60 and 144, Effect A's configuration test 108 and state test 14, and B's configuration test 61.

### Mutations of the driver

The approved plan's step 5. The implementation session made each change, ran the state test at 60 fps and restored the file; Claude copied the two runs' output out of the session's transcript into the logs below.

| Mutation | Expected | Result | Log |
|---|---|---|---|
| **1.** `is_visible_in_tree()` dropped from the driver | D9, D10 and D11 fail | **Exit 1, 3 failures:** D9, D10 and D11 (12 mismatched ticks) | `logs/mutation_dust_visibility_60fps.log` |
| **2.** `DustTrail` moved after `Effects` in `main.tscn` | D12 fails | **Exit 1, 1 failure:** D12 (DustTrail index 3, Rudy index 1) | `logs/mutation_dust_tree_order_60fps.log` |

**What the state test establishes:** for the paths it drives, `emitting` follows the brief's condition on the same tick through load, title, standing, running, stopping, turning, jumping, landing, a knockback and a fall with its respawn; the emitter is at his feet; a pause leaves the node's state alone and stops it processing; hiding the emitter or its parent stops it emitting; and the emitter sits behind Rudy in the tree, outside `Look`.

**What it cannot establish:** that a puff is drawn, that the puffs form a band, that none is born while paused or hidden, that they freeze visibly, that the dust draws behind him on screen, and the look. Defeat and the teleport circle are covered only by the driver's `mode` check.

**My check in the running game** (2026-11-05, after Effect B was wired in): Claude asked me to check Esc while running (the puffs freeze), running while invulnerable (no flashing), a respawn while holding a direction (no streak) and how the dust reads over the wheat and the ground. I played the game and answered: checked, no problem [检查过了，没问题]. The first frames after loading and both ends of the level were not on that list.

## The process shader

[game/shaders/particles_generated.gdshader](game/shaders/particles_generated.gdshader) was generated by Godot 4.7.2's editor converter from an independent copy of `Sparks`' `ParticleProcessMaterial` in `game/effects/slash_sparks.tscn`. The original effect was unchanged, the temporary scene was not saved, and the game does not use this shader. The line numbers below refer to the saved, unedited 383-line file.

| Item | Shader line(s) | Code and meaning |
|---|---|---|
| Shader type | 3 | `shader_type particles;` declares a particle process shader. |
| `start()` | 225 | `void start() {` begins particle initialization. |
| `process()` | 277 | `void process() {` begins the per-step particle update. |
| Initial velocity chosen between minimum and maximum | 139; applied at 264 | `params.initial_velocity_multiplier = mix(initial_linear_velocity_min, initial_linear_velocity_max, rand_from_seed(alt_seed));` chooses the speed. Line 264 multiplies the random spread direction by that speed and stores the initial velocity in `USERDATA1.xyz`. |
| Gravity changes velocity | 311, 324, 340, 344 | `force = gravity;` at 311 starts the acceleration sum. `USERDATA1.xyz += force * DELTA;` at 324 integrates it into the accumulated velocity. Line 340 adds that velocity to `controlled_displacement`; `VELOCITY = final_velocity;` at 344 writes the result. In this generated version, gravity reaches `VELOCITY` through these intermediate variables. |
| Colour sampled over lifetime | 161; lifetime supplied at 296 and 347; output at 352 | `parameters.color *= texture(color_ramp, vec2(lifetime));` samples the ramp. Line 296 computes `lifetime_percent = CUSTOM.y / params.lifetime`, and line 347 passes it to `process_display_param`. Line 352 writes `COLOR = params.color;`. |
| Scale sampled and applied over lifetime | 160; lifetime supplied at 347; transform scaling at 368–370 and 373–375 | `parameters.scale *= texture(scale_curve, vec2(lifetime)).rgb;` multiplies the scale by the curve sample. After the call at 347, lines 368–370 apply the scale to the three transform axes on the first frame, and lines 373–375 apply it on later frames. |
| One line mapped to a brief setting | 311; uniform declared at 43 | `force = gravity;` uses the `gravity` uniform. `CHANGE-BRIEF.md`, section 2's settings table (line 84), specifies `Sparks` gravity as **(0, 700, 0) px/s²**. |

Most settings are uniforms rather than numeric literals in this source. For example, `gravity` is declared at line 43, and `initial_linear_velocity_min` / `_max` at lines 10–11 correspond to the brief's **260 / 420 px/s** (`CHANGE-BRIEF.md:83`). Those values belong to the material parameters; saving only the shader does not embed them. The mapping above identifies the code that uses each setting, not a hard-coded value in the shader. This section is a source inspection, not a new visual test. The shader is left unchanged so these references remain valid.


**Process settings versus node and draw settings.** The brief's velocity range, gravity, direction/spread, damping, colour ramp, scale range/curve, hue variation and lifetime randomness belong to particle processing: their uniforms appear at shader lines 6–45 and feed the update code. For example, line 139 chooses a speed between the two velocity uniforms, while lines 160–161 sample the scale curve and colour ramp over lifetime; these compute particle motion, size and colour. Some process options are compiled into the code rather than exposed as uniforms: `particle_flag_disable_z` is reflected in line 273's zeroing of velocity Z, and `particle_flag_align_y` in line 355's alignment of the Y axis with velocity. The node's `texture`, by contrast, supplies the visible sprite: the brief's 12 × 40 `GradientTexture2D` for `Sparks` is a draw texture, distinct from the process shader's `color_ramp` and `scale_curve` samplers. Default mix blending and `z_index` also belong to drawing/compositing, with no corresponding process uniform. Other settings remain on the particle node: `amount` controls particle count, `lifetime` sets the base duration, `local_coords` selects the simulation space, and `visibility_rect` supplies the culling bounds. These are node settings, not all draw settings. Absence of a matching uniform alone does not mean a setting has no effect on processing: the node's 0.45 s `lifetime` reaches the shader through the built-in `LIFETIME`, used in `CUSTOM.y += DELTA / LIFETIME;` at line 294, while the material's separate `lifetime_randomness` is a uniform at line 38. The distinction follows both where a setting is stored and what the generated code does with it.

## Step 7 — the headless price

`game/tests/cost_effects.gd` (`extends SceneTree`) adapts Example 09's `particle_cost.gd` to these effects and runs through the wrapper at a fixed 60 fps, so frames are not padded towards Godot's 6.9 ms headless sleep (Chapter 9). Each case is rebuilt and timed in each of 5 rounds of 300 frames, after a warm-up; it reports the mean, the standard deviation, the median, the 95th percentile, the maximum and the range of the five round means. "Effects off" means `Effects` and `DustTrail` are removed from `Main` before it enters the tree; the scene file is not changed. Effect A's case starts each burst the way the driver does, so 2 bursts are alive on every timed frame (the brief's most, 58 particles). Effect B's case holds `move_right` and moves Rudy back to the start of a flat stretch whenever he reaches its end, so `RunDust` emits on every timed frame (40 particles).

| Case (ms of CPU time per frame) | The session's run (`logs/cost_effects_60fps.log`) | Claude's rerun (`logs/cost_effects_60fps_rerun.log`) |
|---|---|---|
| Empty scene (the control) | 0.0038 (round means 0.0037–0.0039) | 0.0038 (0.0036–0.0039) |
| Game, both effects off, Rudy idle | 0.0507 (0.0474–0.0580) | 0.0495 (0.0465–0.0575) |
| Game, both effects off, Rudy running (the control for B) | 0.0521 (0.0482–0.0601) | 0.0479 (0.0466–0.0493) |
| Effect A, 2 bursts alive, Rudy idle | 0.0587 (0.0547–0.0654) | 0.0558 (0.0537–0.0583) |
| Effect B, Rudy running, emitting | 0.0559 (0.0502–0.0632) | 0.0498 (0.0486–0.0508) |
| **Effect A − effects off** | **+0.0079** | **+0.0063** |
| **Effect B − its running control** | **+0.0039** | **+0.0019** |

**Reading it.** The control works: the empty scene and the game with the effects off are about 13 times apart and their round means never overlap, so the script is not measuring itself. Each case reached its state on every timed frame (the log's second table: 2 bursts alive, or `RunDust` emitting on 300 of 300). Both effects cost under 0.01 ms of CPU per frame, as the brief predicted (section 8), and in both runs their round means overlap their controls', so a headless run cannot tell either effect from the game without it. That is the dummy renderer, not a cheap GPU: it runs no particle process and draws nothing (`CLAUDE.md`, "Headless facts"), so this number is only the CPU's share. The budget, 0.25 ms of GPU time per effect, is compared on GPU time in the editor's Visual Profiler (Use It).

## Use It

**Setup.** Measured on 2026-11-06 at source commit `d60fb037`: Godot 4.7.2 (`v4.7.2.stable.official.ed1daf0bf`), GL Compatibility (OpenGL 4.1 on Metal), GPU Apple M3, a 1280 × 720 game window run from the editor.

**Who made the evidence.** At my request, Codex (OpenAI's coding agent) recorded the editor measurements and the captures in `evidence/use-it-code/`. It used a temporary editor plugin in a scratch copy of the game outside this repository; the plugin started the real Visual Profiler, read its and the Monitors' cells, and drove the real `Main` through the game's input actions from fixed starting points (its `README.md` gives the method and its limits). I chose what to measure and reviewed the results. Claude Code checked the folder before this section was written: every file the README cites exists; all 168 files in `game/` still match `source-hashes.json`, so no game file changed; and its three runtime logs have no `SCRIPT ERROR` or `SHADER ERROR`. The main run logged two errors from the instrument itself (`Lambda capture at index 0 was freed`, while it waited for the reloaded `Main`). The screenshots in that folder are half-size copies; the full-size originals stay on this machine, outside git (the folder's README says so). This automated run does not replace my own play; that is recorded separately below.

| Check | Evidence | Result |
|---|---|---|
| Baseline | `logs/`; "Step 2", "Step 3" and "Step 5" above | Before this assignment (tag `a5`): `checks.tscn` 141, `invulnerable_tint_checks.tscn` 15 at 30, 60 and 144 fps. After every change, rerun at `d60fb037` through the wrapper: `checks.tscn` 141 at 60 fps (89 `res://` paths, all present); `invulnerable_tint_checks.tscn` 15 at 30, 60 and 144 |
| Configuration | `logs/test_*_config_60fps.log`, `logs/mutation_*` | Effect A 108 of 108, Effect B 61 of 61, at 60 fps. Effect A's two mutations exited 1, with 2 and 1 failures; so did Effect B's |
| State | `logs/test_*_state_60fps.log` | Both at a fixed 60 fps, not realtime. Effect A 14 of 14, including two cuts 19 ticks apart with both bursts alive (S7) and the first lasting its full 27 ticks (S8). Effect B 14 of 14 |
| Frame strips (fixture) | `captures/slash_sparks/r0–r1/`, `captures/run_dust/r0–r3/`; `TUNING.md` | Every revision's strips, labelled as fixture captures |
| In play (HUMAN CHECK) | My own play; `evidence/use-it-code/20`–`34`, `detail/90`–`91` | **My own play:** after Step 3 I played with Effect A wired in and found no problem; after Step 5 I checked Esc while running, running while invulnerable, a respawn while holding a direction and how the dust reads, and found no problem; on 2026-11-06, after this run, I played myself in the 1280 × 720 window and found the size of both effects and the control feel fine [亲自玩过，大小和手感都没问题]; on 2026-11-07, when Claude asked me to check Effect A over the sky and the pit, at both screen edges and on load, I answered that when attacking there are clearly visible sparks [攻击时，有明显的火花], without saying which of those places I looked at. **Codex's captures** add: repeated slashes with two bursts at once; a cut facing left spraying left; sparks still visible after a cut goblin hides (hiding the burst alone changes 133 pixels); dust starting, stopping, leaving the ground and starting again on landing. Effect B "hidden" has no path in play; the state test covers it (D9, D10) |
| Against the background (HUMAN CHECK) | `supplement/83_sky_visible.png`, `supplement/88_dark_pit_sparks.png`, `30_dust_running.png` | From the captures: sparks read against the sky at the top of a jump and against the dark pit (a slash while falling into it, since a slash over the pit still has sky behind it); dust reads over the lower wheat and the grass |
| Edge of screen (HUMAN CHECK) | `40`–`43`, `supplement/85`–`87`, `detail/92`–`94` | From sampled frames at the left start and at the true right edge (Rudy jumped over the portal's trigger to x 7653 without ending the level): no burst disappeared while it should still be visible, and dust stays visible near both sides. Sampled frames, not a continuous check |
| Scene load (HUMAN CHECK) | `10`–`13`, `70`–`72` | No dust or sparks on the title, in the first frames of play, or after a real level end and restart; the emitter and burst states agree |
| Pause, invulnerability, respawn | My play after Step 5; `50`–`52`, `supplement/80`–`82`, `60`, `64`–`66` | My play found no problem. In the captures, paused dust frames 0.6 s apart and paused spark frames 0.7 s apart are pixel-identical and change again on resume; the dust does not flash with Rudy; after a respawn with a direction held, no trail joins the pit to the checkpoint |
| Boundaries holding (row added on 2026-11-07) | `game/` against Assignment 5's `game/` at tag `a5`, compared with `git diff` by Claude at my request | The only changed file is `game/app/main.tscn`, which gains only presentation nodes: `DustTrail` with `RunDust`, `Effects` with `SlashBursts`, and `VsyncDebug`. Every other difference is a new file in `effects/`, `previews/`, `tests/`, `app/vsync_debug.gd` or `shaders/particles_generated.gdshader`. `rudy.gd`, `rudy.tscn`, `rudy_look.gd`, the goblin, the level, `main.gd`, `system_keys.gd`, `ui/`, `systems/`, `project.godot`, `invulnerable_tint.gdshader` and the existing tests are byte-identical. In my own play the control feel was fine (above) |
| Claude against me | `TUNING.md`, Effect B r2 | Claude read r2 as a continuous band with both measured targets met. My verdict was that the dust should rise at a steeper angle, because it stayed on the ground [尘土扬起的角度还可以高一些，现在基本都只是在地面上]. Round r3 followed from that. In Effect A's r0, Claude and I agreed |
| Headless CPU price | "Step 7" above | Empty scene 0.0038 ms per frame; Effect A +0.006 to +0.008 ms and Effect B +0.002 to +0.004 ms over their controls, inside the spread between rounds |
| GPU price (HUMAN CHECK) | `evidence/use-it-code/summary.json`, `editor-profiler.json`, `runtime.log`, the four `*_editor.png` | See below |
| Process shader | "The process shader" above | The line references from Step 6 |

### The GPU price

The Visual Profiler has a GPU column, and in all four states it read **0.0 ms**, in every row, Update GPUParticles and Render Viewports included; the runtime viewport GPU-time API also returned 0. That is the brief's predicted failure 12. **The 0.25 ms GPU budget per effect cannot be evaluated on this machine. A zero is not evidence of zero cost, and it is not a pass.**

Following the brief's fallback, vsync was turned off with F9 (`VsyncDebug`) for these readings and turned back on afterwards (`VSYNC_RESTORED_MODE 1` in `runtime.log`). Each state had a 1.5 s warm-up and 5 s of readings.

| Reading | A off (idle, with the sword) | A heaviest (a slash about 3 times a second) | B off (idle) | B heaviest (running back and forth, x 2600–2890) |
|---|---:|---:|---:|---:|
| Visual Profiler, GPU | 0.0 ms | 0.0 ms | 0.0 ms | 0.0 ms |
| Monitors → Time → FPS, median (range) | 438 (413–504) | 239 (222–261) | 357 (271–395) | 311 (284–321) |
| Frames counted by the instrument | 427.1 FPS | 229.2 FPS | 347.8 FPS | 296.9 FPS |
| Monitors → Time → Process, median | 11.80 ms | 11.69 ms | 10.94 ms | 9.41 ms |
| Monitors → Raster → Total Draw Calls, median | 9 | 12 | 9 | 10 |

- Every FPS reading was above the display's reported 60 Hz, so the comparison was not capped there.
- In A's heaviest state two bursts were alive on 112 of 300 timed ticks; in B's, the dust emitted on 251 of 300, the rest being the game's turn holds. Neither is a constant peak.
- FPS is not GPU time, and Process time is not either; neither is substituted into the budget. The two idle baselines alone differ by about 80 FPS, so the differences between states are not isolated particle costs. Effect A's heaviest state did add 3 draw calls and lower FPS the most, but this machine cannot say how much of that is GPU time.

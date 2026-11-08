# Plan 3 — trigger Effect A (`hit_spark`) on a landed melee hit, and its state test

Written before any code edit. Contract: `CHANGE-BRIEF.md` Effect A + Revisions r1.
Frozen for this task: `effects/hit_spark.tscn` (settings), `shaders/**`,
`scripts/run-test.sh`, every existing test.

## Step 1 — the trigger (presentation only), `entities/player.gd`

- One `const HIT_SPARK := preload("res://effects/hit_spark.tscn")` and one small
  helper `_hit_spark(target: Enemy)`:
  - returns at once if `game` or `target` is not valid;
  - instantiates a **new** `HitSpark`, sets its `position` to
    `game.to_local(target.global_position)` (the struck enemy's position at this
    instant) and adds it as a child of the `GameManager` (`game`), never of the enemy.
  - It reads `game` and `target.global_position` only; it writes no game state
    (no damage, hitstop, aggro, charge, cooldown, combo or target change).
- Called on the line right after each of the three existing landed-hit
  `CombatVfx.spawn(..., "spark"|"amiya_spark")` calls (basic hit in
  `attack_direction()`, Lappland's cross in `_lappland_cross()`, Amiya's cut in
  `_amiya_cut()`), with the same enemy the mesh spark uses. The mesh spark stays.
- **Retrigger rule (overlap):** every call instances a fresh scene; nothing keeps
  a reference to an earlier burst, so an earlier `HitSpark` is never restarted or
  cut off. Freeing is the effect's own 0.55 s timer (`effects/hit_spark.gd`,
  r1 (b)), unchanged. Because the burst is a child of the `GameManager`, an
  enemy's `queue_free()` on a killing blow cannot take it along (A4).
- Not touched: ranged shots, sword waves, Shadowless strikes, Moonlit, enemy-to-player hits,
  misses — none of those code paths gets the helper.

## Step 2 — new state test `tests/test_hit_spark_state.gd` (60 fps)

Real game (`res://game/main.tscn`), real loop, real input: left mouse events via
`Input.parse_input_event` at the enemy's projected screen point (same method as
`tests/test_lappland_input.gd` / `test_amiya_input.gd`). The test never calls the
helper, `CombatVfx.spawn`, `attack()` or `attack_direction()` in the real-input
checks. Observation: `SceneTree.node_added` / `node_removed` record every node
whose `scene_file_path` is `res://effects/hit_spark.tscn` anywhere in the tree
(its parent, its position, its process-frame number in and out); at `node_added`
it also snapshots every live enemy's `global_position` and `health` (the
"instant" of the hit). Landed hits are counted from enemy health drops each
frame. It never reads `emitting` on the one-shot emitters (r1 (b)).

Fixture setup (not the event): fixed map seed, `_clear_field()`, enemies spawned
with `_spawn_enemy`, big health and `set_physics_process(false)` so they stand
still (as the existing input suites do), `choose_operator` in the base for Amiya.

| Assertion | Brief rule |
|---|---|
| a. From the rig loading through the field loading plus 30 frames after it: zero `HitSpark` nodes created | A1 (never on scene load) |
| b. Lappland, left mouse held on one enemy: each frame's number of new `HitSpark`s equals that frame's landed hits (health drops), ≥ 3 hits; each is a child of the `GameManager`, at the struck enemy's `global_position` at the instant (≤ 0.01) | A1 (once per landed hit, at the position) |
| c. Lappland stage 3 with a second enemy within 2.2 of the first: the cross cut adds a second `HitSpark` at the second enemy's position in the same frame | A1 (third call site), A2 (two alive) |
| d. Left click on empty ground: she walks, no swing, no health drop, no `HitSpark` | A1 (not on a swing at empty ground — see limits) |
| e. Enemy with physics on attacks her (no input from the test): her HP drops, zero `HitSpark` | A1 (not on enemy-to-player hits) |
| f. Amiya, mouse held: her stage-2 double cut lands two cuts ~0.11 s apart → two `HitSpark`s created < 0.45 s apart, both alive at once, distinct nodes; the first one's own `_age` never goes backwards and it is freed ≥ 0.45 s after it was created (not restarted, not cut off) | A2 (overlap), A1 (Amiya call site) |
| g. Every `HitSpark` seen is freed, each within 0.55 s + one frame of creation and not before 0.45 s; at the end none is left | A3 |
| h. A 1-HP enemy killed by a real held-mouse hit: the enemy is freed, its `HitSpark` (parent `GameManager`) is still in the tree after the enemy left it and lives its full 0.45–0.55 s+1 frame | A4 |

Run: `./scripts/run-test.sh test_hit_spark_state.gd 60 600` (no audio, so 60 fps).

## Step 3 — existing suites

`./scripts/run-baseline.sh after-step3 8`, compared line by line with
`logs/baseline-before/summary.txt` (78/89 in the parallel run). Any new failure
rerun alone: `./scripts/run-test.sh <file> 60 600`. A5 (presentation only) rests on this.

## Limits / what needs windowed observation by the user

- **Look and timing on screen** (flash, throw, settle, clear; overlap reading as
  layered bursts; burst at the hit point rather than offset; legibility on city
  and snow; no clipping at the screen edge): windowed play only. Headless uses a
  dummy renderer — no particle process runs, nothing is drawn.
- **A4 "plays in full"** on screen (the sparks keep flying after the enemy
  vanishes): windowed. Headless proves only that the node outlives the enemy
  for its full timer.
- **A2 "both emitting"**: headless cannot read it (`emitting` is false from
  frame 1, r1 (b)); the test proves two live distinct nodes, neither restarted.
- **Swing that misses**: since the user 2026-10-20 a left click on the ground walks
  (no air swings, `game/gm_pointer.gd:105-111`) and a lock only swings when the
  target is in reach and sight (`Player.attack()`), so no real mouse input can
  produce a melee swing that lands on nobody. Check d covers the real input for
  empty ground; an extra, clearly labelled non-input check calls the game's own
  swing API `attack_direction()` away from every enemy (as `tests/test_lappland.gd`
  does) to show an air swing makes no `HitSpark`. It never calls the trigger helper.
- **Ranged/projectile hits**: not driven by this test; covered only by the
  helper being absent from those code paths (diff review).

---

# Implementation log

## Step 1 done — trigger helper in `entities/player.gd`

Checked against the brief: three call sites (A1), new instance per hit under the
`GameManager` (A2 overlap, A4), freeing left to `effects/hit_spark.gd` (A3, r1 b),
mesh spark kept, no state written (A5).

`git diff --stat` (`prompts/plan-3.md` is untracked, so it is not listed):

```
 .../assignment-6/walker-downfall/entities/player.gd      | 16 ++++++++++++++++
 1 file changed, 16 insertions(+)
```

```diff
@@ -912,6 +912,7 @@ func attack_direction(direction: Vector3, target: Enemy = null) -> void:
 		target.hitstop_remaining = maxf(target.hitstop_remaining, stop)
 		hitstop_remaining = stop
 		if is_instance_valid(game): CombatVfx.spawn(game, target.global_position, direction, "spark")
+		_hit_spark(target)
 		if crit and has_trigger(ItemModifier.Trigger.MOON_WAVE) and randf() < 0.35:
@@ -939,6 +940,19 @@ func _after_landed(target: Enemy, raw: float, stage: int) -> void:
+## Effect A `hit_spark` (CHANGE-BRIEF.md, A1-A4): every landed melee hit gets a
+## fresh HitSpark under the GameManager at the struck enemy's position, never
+## under the enemy, so a killing blow's queue_free() cannot take it along and an
+## earlier burst is never restarted (overlap). It frees itself on its own timer
+## (effects/hit_spark.gd). Presentation only: reads `game` and the position.
+const HIT_SPARK := preload("res://effects/hit_spark.tscn")
+
+func _hit_spark(target: Enemy) -> void:
+	if not is_instance_valid(game) or not is_instance_valid(target): return
+	var burst := HIT_SPARK.instantiate() as Node3D
+	burst.position = game.to_local(target.global_position)
+	game.add_child(burst)
+
@@ -960,6 +974,7 @@ func _lappland_cross(...):
 	if is_instance_valid(best): CombatVfx.spawn(game, best.global_position, direction, "spark")
+	_hit_spark(best)
@@ -1766,6 +1781,7 @@ func _amiya_cut(target: Enemy, raw: float, crit: bool, direction: Vector3) -> vo
 	if is_instance_valid(game): CombatVfx.spawn(game, target.global_position, direction, "amiya_spark")
+	_hit_spark(target)
```

## Step 2 done — `tests/test_hit_spark_state.gd` (new, 361 lines, untracked)

`git diff --stat` is unchanged from Step 1 (the new test is untracked, so it is
not listed; `git status --short`: `?? tests/test_hit_spark_state.gd`). No
gameplay file changed in this step.

Changes from the plan, found while running it:

1. **Headless mouse dispatch.** The first run (same `Input.parse_input_event`
   method as `test_lappland_input.gd`) landed 0 hits: measured, the Input
   singleton saw the button (`is_mouse_button_pressed` true a frame later) but
   `GameManager._input` never received the events (`_pointer_position` stayed
   (0,0)), so nothing was under the pointer. This is the same failure as
   `test_lappland_input`'s `HITS 0` in both baseline runs. The test's `send()`
   now feeds each event to `Input.parse_input_event` *and*, only when
   `DisplayServer.get_name() == "headless"`, pushes the same event into the
   root window with `root.push_input(event, true)`, so it travels root Window
   -> SubViewportContainer -> SubViewport -> `GameManager._input` ->
   `pointer_step` -> lock -> `Player.attack()`. No game code changed for this.
2. **Projectile hits.** Default Lappland releases a sword wave on the 4th swing;
   the wave struck the enemy 7 frames later (health -214.5, no HitSpark). The
   accounting now identifies such drops by `SwordWave.hit_ids` and asserts they
   bring **zero** HitSparks, which adds a real-input check of A1's "not on
   ranged/projectile hits".
3. **Dying enemy snapshot.** At the killing blow the enemy has already left the
   `"enemies"` group when the HitSpark is added, so the position snapshot also
   reads the test's watched enemies.
4. **Air swing.** Not done: `attack_direction()` contains the trigger, and the
   prompt forbids calling the trigger path directly. Empty ground is covered
   by the real ground click only (no swing exists for it in the game).

Mutation check (temporary, reverted; `player.gd` diff re-verified identical to
Step 1): `_hit_spark` parenting the burst to the enemy (`target.add_child`) ->
3 FAIL (parent check, A4 "outlives its freed enemy" — spark freed on frame 406
with its enemy, A3 lower bound). Log: `logs/test_hit_spark_state_60fps_mutation_parent.log`.

Final run, `./scripts/run-test.sh test_hit_spark_state.gd 60 600` (fixed 60 fps,
headless; no audio, so not realtime): 22 PASS, 0 FAIL, exit 0. 13 HitSparks
seen; each lived 32 process frames (0.533 s) by the frame counters.

## Step 3 done — existing suites

`./scripts/run-baseline.sh after-step3 8` -> `logs/baseline-after-step3/summary.txt`:
**80 of 91 pass** (before: 78 of 89; the two added suites, test_hit_spark_config
and test_hit_spark_state, both PASS). Differences from `logs/baseline-before`:

- test_audio: FAIL 1 -> PASS (it also passed in the serial before-run; flaky under load).
- test_elevation: PASS -> FAIL 1 ("walking off the terrace edge does not drop the
  body (lowest 1.79, terrace 3.76)"). Rerun alone,
  `./scripts/run-test.sh test_elevation.gd 60 1200`: PASS, exit 0 ("lowest 2.45,
  terrace 2.46"). It does not touch melee hits; treated as parallel-load flakiness.
- Every other line identical (same 10 failures as before: amiya_input, base_crew,
  builds, combat, hotbar_input, item_icons, lappland_input, loot_input, market, ui_v1).

`git diff --stat` (unchanged since Step 1; new files are untracked):

```
 .../assignment-6/walker-downfall/entities/player.gd      | 16 ++++++++++++++++
 1 file changed, 16 insertions(+)
```


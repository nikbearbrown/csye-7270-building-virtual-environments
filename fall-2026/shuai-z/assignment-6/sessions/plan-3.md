*Translation note: the plan session (`sessions/session-3.jsonl`, 2026-11-04) wrote this plan in Chinese. This is Claude Code's English translation of its result event, made in our conversation at my request. Nothing was added or removed; the code block and file names are as the session wrote them. The Chinese original is the `result` field of the last line of `sessions/session-3.jsonl`.*

---

I have read the code and am putting the plan together. I have not created or changed any file, and I have not run Godot.

# Plan for triggering Effect A (a plan only; no file edited)

## The short version

- **How it triggers:** a new, read-only driver node. Every physics tick it reads `Rudy/SwordHitbox/Shape.disabled` once, and on the tick it sees the edge from true to false it creates a new `SlashSparks` instance.
- **The retrigger rule (A3, overlap):** every cut is a new instance; an old one is never restarted. An old burst frees itself on `Sparks.finished`, so at most 2 are alive at once.
- **The test:** a new `test_slash_sparks_state.tscn`. It runs `Main`'s real game loop, presses the real input actions with `Input.action_press`, and runs at 60 fps.

## Three things found in the code that decide the design

1. **Processing order decides "the same tick".** `Shape.disabled` is written in Rudy's own `_physics_process` → `_swing()` (`rudy.gd:229`, `:242`). Siblings are processed in tree order. So the driver must sit after `Rudy` in `main.tscn` to see the edge on the same tick. Placed before Rudy, it would be one tick late, which breaks A1's "on that physics tick". The test checks this specifically (S4 below).
2. **The mirror check reads `global_transform.x.x`, not `scale.x`.** The driver sets `scale.x = facing`. The test reads the sign of `global_transform.x.x`, because Godot sometimes decomposes a negative x scale into a y scale plus a 180° rotation; `global_transform.x.x` is not affected by that.
3. **The state the test sees is the state at the end of the previous tick.** When `await get_tree().physics_frame` resumes, the nodes have not been processed for this tick yet. So every `disabled`, new burst and Shape position the test reads is the value at the end of the previous tick, which is exactly right for comparing "the same tick".

## Steps

### Step 1: the driver node and the container

**New `game/effects/effects_driver.gd`** (`class_name EffectsDriver`, `extends Node2D`), about 30 lines:

```gdscript
const SLASH_SPARKS := preload("res://effects/slash_sparks.tscn")
@onready var _rudy: Rudy = get_node("../Rudy")
@onready var _sword_box: CollisionShape2D = _rudy.get_node("SwordHitbox/Shape")
@onready var _slash_bursts: Node2D = $SlashBursts
var _box_was_disabled: bool   # set from _sword_box.disabled in _ready, so load never fires

func _physics_process(_delta):
    var disabled := _sword_box.disabled
    if _box_was_disabled and not disabled:
        _fire_slash_sparks()
    _box_was_disabled = disabled

func _fire_slash_sparks():
    var burst: Node2D = SLASH_SPARKS.instantiate()   # a new burst per cut: overlap (A3)
    _slash_bursts.add_child(burst)
    burst.global_position = _sword_box.global_position   # A2
    burst.scale.x = _rudy.facing                          # mirror, A2
    (burst.get_node("Sparks") as GPUParticles2D).finished.connect(burst.queue_free)
    for emitter: GPUParticles2D in burst.get_children():
        emitter.emitting = true
```

- **What it reads:** only `disabled`, `global_position` and `facing`. It writes no game state and sets no particle or material property. `emitting = true` counts as "starting" and `scale.x` as "mirroring", both of which CLAUDE.md allows.
- **Why it frees on `Sparks.finished`:** `Sparks` is the longest-lived layer (0.45 s). By the headless probe, `finished` is sent on frame 27 (`logs/probe_particles_headless.log:24-27`). The free happens after the burst's life has ended, not on a swing, so it meets A4.
- **Pause:** the driver and the container inherit the pause. While paused the driver does not read and Rudy does not move, so no edge can appear.

**Change `game/app/main.tscn`:** add only 1 `ext_resource` and 2 nodes, between `Rudy` and `Camera`:

- `Effects` (`Node2D`, with the driver above as its script), at the origin, never moved;
- `Effects/SlashBursts` (`Node2D`), the container for the bursts.

**This step needs your confirmation:** the brief does not set the driver's name and place (CLAUDE.md lists this under Unconfirmed). Later, Effect B's `RunDust` has to draw behind Rudy, so it will need a container before Rudy; that is for later and not part of this step.

### Step 2: run the existing tests and confirm nothing broke

Change no file, and run in turn:

```bash
scripts/run-test.sh checks.tscn 60                   # expect 141 PASS, 0 FAIL
scripts/run-test.sh invulnerable_tint_checks.tscn 30 # 15 PASS
scripts/run-test.sh invulnerable_tint_checks.tscn 60
scripts/run-test.sh invulnerable_tint_checks.tscn 144
scripts/run-test.sh test_slash_sparks_config.gd 60   # unchanged
git diff --stat game/shaders/                        # must be empty
```

`checks.gd` only checks that the nodes listed for `main.tscn` exist, so two more nodes should not affect it. But that only counts once it has actually run.

### Step 3: the state test

**New `game/tests/test_slash_sparks_state.gd`** (`extends Node`) **and `test_slash_sparks_state.tscn`.**

- **Why a `.tscn`:** the test instantiates `Main` and uses the autoloads `Sfx`/`Music`, so it runs as a scene, the way `checks.tscn` does, not with `--script`.
- **Helpers:** `_tap`, `_hold`, `_frames`, `_wait_until` and `_check`, written as in `checks.gd` and copied over; `checks.gd` is not changed.
- **Mode:** `scripts/run-test.sh test_slash_sparks_state.tscn 60`. The test does not wait on audio, so 60 fps, not realtime.

**Recorder (read-only):**

- Connect `SlashBursts.child_entered_tree` and record each burst's birth frame.
- Sample `Shape.disabled` every frame, and record each true → false edge the test itself sees as an "edge frame".
- Record each burst's position, its `global_transform.x.x`, and the frame on which it fires `tree_exited`.

**The only state the test writes:** as in `checks.gd`, `_teleport` puts Rudy next to the sword, a goblin or open ground. That is test setup, not presentation code. The sword is picked up by walking into the pickup (real `move_right`), every cut comes from real `slash` input, and the test never calls `_fire_slash_sparks()`. The goblins' `speed` is not changed; Rudy is teleported to where a goblin is at that moment.

**Assertions and the rules they cover:**

| # | Assertion | Rule |
|---|---|---|
| S1 | Load with the title (`title_shown=false`), wait 60 frames, press slash on the title: 0 bursts | A1 (load, title) |
| S2 | Load with the title skipped, wait 60 frames: 0 bursts | A1 (load) |
| S3 | Tap slash without the sword, wait 30 frames: 0 bursts | A1 (no sword) |
| S4 | Take the sword, stand still, tap slash once: exactly 1 burst, born on the edge frame (one tick late fails) | A1 |
| S5 | On S4's frame: the burst's `global_position` within 1 px of the Shape's `global_position`, `global_transform.x.x > 0`, `facing == 1` | A2 (facing right) |
| S6 | Turn on the spot with `move_left`, then tap slash: position within 1 px, `x.x < 0`, `facing == -1` | A2 (facing left) |
| S7 | Tap again right after a swing ends (the two cuts go live about 20 frames, about 0.33 s, apart): 2 bursts alive on the second edge frame; the first is the same instance, its position unchanged, and its `Sparks.emitting` still true | A3 (overlap, not moved or cut short) |
| S8 | The first burst leaves the tree 25–30 frames after its own birth (about 0.45 s). If the second cut restarted it, that would move to about 47 frames; if it were cut short, earlier | A3 (not restarted, not cut short) |
| S9 | Mash slash for 2 s (like `checks.gd`'s mashing): bursts = edges = swings, and no more than 2 bursts alive on any frame | A1 (no trigger when pressed during a swing), A3 (at most 2) |
| S10 | Every burst's parent is `Effects/SlashBursts`; neither Rudy nor any goblin is its ancestor | A4 |
| S11 | Cut down a goblin: the goblin hides after about 0.4 s, while the burst's `is_visible_in_tree()` is true on every frame for 27 frames after its birth | A4 |
| S12 | With the sword, stomp a goblin from above (`checks.gd`'s stomp): 0 bursts | A1 (stomp) |
| S13 | Pause (the real `pause` action), then tap slash, wait 30 frames: 0 new bursts; also 0 within 10 frames after resuming | A1 (while paused) |
| S14 | Swing, then pause at once: the burst is still in the tree and visible, `emitting` still true, `can_process()` false; after resuming, `can_process()` true | the headless part of A5 |

At the end it prints `all checks passed`, or `N check(s) FAILED` and exits with code 1, in the same format as the existing tests.

### Step 4 (optional, your decision): show that the test can catch a fault

Temporarily change the driver, run the test once, then restore it. Each change comes with its diff and log:

- **a.** Reuse one instance and set `emitting = true` on it again (predicted failure 4): S7 and S8 should fail.
- **b.** Move `Effects` before `Rudy` (one tick late): S4 should fail.

## Rules only a human can check

- **What A5 looks like:** that the sparks really hold still and stay visible while paused, and go on after resuming. Headless can only show that the node does not process (`can_process()` false).
- **Whether the velocity is mirrored when facing left** (failure 8): S6 only shows that the node is mirrored.
- **That the sparks can be seen on a cut that hits a goblin:** the "eyes" part of A4.
- **The look:** timing, contrast, size and change, from the frame strips and from play.
- **Clipping at the edge** (`visibility_rect`): swing facing right at x ≈ 7700 and facing left at x ≈ 300.
- **A clean screen on scene load:** S1 and S2 only show that no burst is created.
- **A swing at the top of a jump, and a swing over a pit** (section 5).

## What this test can and cannot prove

- **It can prove:** through the real game loop and input actions, each live edge creates exactly one burst on the same physics tick, and nothing else creates one. The burst is at the hitbox, with a mirror sign that matches the facing. When two cuts overlap, the first burst is not restarted, moved or cut short, and at most 2 are alive at once. No burst hangs under Rudy or a goblin. While paused, the nodes stop processing.
- **It cannot prove:**
  - Headless uses the dummy renderer, which draws no particles and runs no GPU particle process. `emitting` being true does not mean particles can be seen on screen. S8 and S11 use the node's own clock (from the probe's findings), not the simulation.
  - That the mirror reaches the particles' velocity.
  - That the particles really freeze while paused.
  - `Input.action_press` works at the input-action layer, the path Rudy reads, not at the level of operating-system keyboard events.

## Rules for the next session

- One step at a time, with each step's diff.
- Show the real output of every run, and say which mode it used (60 fps or realtime).
- Run `git diff --stat game/shaders/` after each step.
- Do not commit.

A headless run may make Godot generate `.gd.uid` files automatically. If it does, I will say so.

# Handoff — Task 2 of 3: guard FSM (Patrol / Chase / Search)

## Files changed (all new, except guard.gd and guard_arena.tscn which were modified)

| File | Role |
|------|------|
| `godot/npc/guard.gd` | **Updated** — adds `sight_radius`, `lose_radius`, `last_known_player_pos`, read-only `mode` property, `has_line_of_sight()`, `_ready()` that connects FSM signal to ModeLabel |
| `godot/npc/guard_state.gd` | Base state for all guard FSM states; declares `guard` and `player` vars (injected by GuardFSM) |
| `godot/npc/guard_state.gd.uid` | UID stub |
| `godot/npc/guard_fsm.gd` | Extends `state_machine.gd`; injects `guard`/`player` refs into children in `_enter_tree()`, sets `states_map` in `_ready()` |
| `godot/npc/guard_fsm.gd.uid` | UID stub |
| `godot/npc/states/patrol.gd` | Patrol state: 4-waypoint loop, transitions to Chase when player within `sight_radius` with clear LOS |
| `godot/npc/states/patrol.gd.uid` | UID stub |
| `godot/npc/states/chase.gd` | Chase state: retargets player every 0.2 s; transitions to Search when `dist > lose_radius` OR no LOS |
| `godot/npc/states/chase.gd.uid` | UID stub |
| `godot/npc/states/search.gd` | Search state: navigates to `last_known_player_pos`, waits 1.0 s, transitions to Patrol |
| `godot/npc/states/search.gd.uid` | UID stub |
| `godot/npc/guard_arena.tscn` | **Updated** — adds GuardFSM (with Patrol/Chase/Search children) and ModeLabel under Guard |
| `godot/tests/test_guard_fsm.gd` | Headless test: 6 checks — initial Patrol, full sequence, hidden-player, hysteresis |
| `godot/tests/test_guard_fsm.gd.uid` | UID stub |

No existing files outside `godot/npc/guard.gd` and `godot/npc/guard_arena.tscn` were touched.

---

## Transition table

| From    | To     | Condition |
|---------|--------|-----------|
| Patrol  | Chase  | `dist(guard, player) ≤ sight_radius` **AND** `has_line_of_sight(player)` |
| Chase   | Search | `dist(guard, player) > lose_radius` **OR** `NOT has_line_of_sight(player)` |
| Search  | Patrol | guard reaches `last_known_player_pos` (within 64 px) **AND** waited ≥ 1.0 s |

Hysteresis: `lose_radius (350) > sight_radius (200)`. A player in the zone `(sight_radius, lose_radius]`
with clear LOS holds the current state — Guard will not enter Chase from Patrol (too far) and
will not leave Chase to Search (not far enough, has LOS).

---

## Guard parameters

| Property | Default | Role |
|----------|---------|------|
| `sight_radius` | 200 px | Patrol→Chase threshold |
| `lose_radius`  | 350 px | Chase→Search threshold (must be > sight_radius) |

Both are `@export` on `guard.gd` so they can be tuned from the editor or by a test.

---

## `mode` property

`guard.mode` (String, read-only) derives from `$GuardFSM.current_state.name`, returning
`"Patrol"`, `"Chase"`, or `"Search"`. It never needs to be set directly.
The same value is mirrored on the `ModeLabel` child of Guard via `state_changed` signal.

---

## `has_line_of_sight` implementation

```
PhysicsRayQueryParameters2D.create(guard.global_position, player.global_position)
exclude = [guard]          # self-exclusion
→ result.is_empty()        → true  (nothing in the way)
→ result.collider == player → true  (ray's first hit IS the player)
→ otherwise                → false (obstacle or wall is between guard and player)
```

Works headless because physics simulation runs in headless mode.

---

## Patrol waypoints (4 points, loop)

```
WP0 (160, 160)  top-left
WP1 (1100, 160) top-right
WP2 (1100, 560) bottom-right
WP3 (160, 560)  bottom-left
```

All waypoints are inside the walkable nav region and avoid the obstacle hole (x 500–780, y 240–480).
The guard navigates between them using the Task 1 `NavigationAgent2D` / nav polygon.

---

## Exact test commands and their real output

All four commands are run from the repo root (`godot/` is the Godot project directory):

### New test — guard FSM
```
godot --headless --path godot --script res://tests/test_guard_fsm.gd
```
```
--- Test 1: Patrol -> Chase -> Search -> Patrol ---
[UID warnings omitted — expected, same reason as Task 1]
PASS initial mode is Patrol
FIXTURE: player → (280, 360)  dist=120 < sight_radius=200, LOS clear
PASS mode -> Chase when player in sight (0.1 s)
FIXTURE: player → (800, 560)  dist >> lose_radius=350
PASS mode -> Search when player beyond lose_radius (0.1 s)
PASS mode -> Patrol after Search completes (1.2 s)
--- Test 2: player hidden behind obstacle stays in Patrol ---
[UID warnings omitted]
FIXTURE: player → (900, 360)  behind obstacle, LOS blocked
PASS player hidden behind obstacle does not trigger Chase
--- Test 3: player between sight_radius and lose_radius stays Chase >=1s ---
[UID warnings omitted]
FIXTURE: player → (280, 360)  trigger Chase
FIXTURE: player → (400, 360)  dist≈240, sight_radius<dist<lose_radius, LOS clear
PASS player between sight_radius and lose_radius: mode stays Chase for >=1 s
RESULT 6 checks; 0 failures
```
Exit code **0**.

### Existing test — guard navigation (Task 1)
```
godot --headless --path godot --script res://tests/test_guard_nav.gd
```
```
OBSERVE same-frame: nav_finished_before_tick=false reachable_before_tick=false moved_after_0.3s=true guard.position=(160.0, 323.75)
PASS guard reaches far-side target within 20.0s
PASS guard never enters obstacle collision bounds
PASS target inside obstacle: is_target_reachable() == false
PASS guard rests outside obstacle bounds for unreachable target (pos=(632.7645, 240.1238))
RESULT 4 checks; 0 failures
```
Exit code **0**.

### Existing test — input / state machine
```
godot --headless --path godot --script res://test_input.gd
```
18/18 PASS, exit **0** (identical to previous log).

### Existing test — combo / sword
```
godot --headless --path godot --script res://test_combo.gd
```
11/11 PASS, exit **0** (identical to previous log).

---

## Arena layout (unchanged from Task 1)

```
(0,0)─────────────────────────────(1280,0)
│  walls 20 px thick on all four sides    │
│                                         │
│  Guard start:  (160, 360)               │
│  Player start: (200, 560)               │
│                                         │
│        ┌────────────────┐               │
│        │ StaticBody2D   │               │
│        │ obstacle       │               │
│        │ 240×200        │               │
│        │ centre(640,360)│               │
│        └────────────────┘               │
│                                         │
(0,720)───────────────────────────(1280,720)
```

* Obstacle collision bounds: x 520–760, y 260–460
* Navigation hole (obstacle + 20 px margin): x 500–780, y 240–480
* Walkable nav region: (20,20)–(1260,700) minus the hole

---

## Node tree under Guard (after Task 2)

```
Guard (CharacterBody2D) — guard.gd
├── CollisionShape2D
├── NavigationAgent2D    target_desired_distance=48, path_desired_distance=8
├── GuardFSM (Node)      — guard_fsm.gd (extends state_machine.gd)
│   ├── Patrol (Node)    — states/patrol.gd (extends guard_state.gd)
│   ├── Chase  (Node)    — states/chase.gd  (extends guard_state.gd)
│   └── Search (Node)    — states/search.gd (extends guard_state.gd)
└── ModeLabel (Label)    shows guard.mode above the sprite
```

---

## Implementation notes

### `_enter_tree` injection pattern
`state_machine.gd._enter_tree()` calls `initialize()` → first state's `enter()` before
`_ready()` has run. Guard states need `guard` and `player` references in `enter()`.
`guard_fsm.gd` solves this by setting those properties on all child nodes **before** calling
`super._enter_tree()`. The nav agent is NOT yet `@onready`-set at that point, so
`patrol.gd` defers its first `set_target()` to the first `update()` call instead of `enter()`.

### `states_map` timing
`states_map` is populated in `guard_fsm._ready()`, which always runs before the first
`_physics_process` tick. No state emits `finished` from `enter()`, so no transition is
attempted during `_enter_tree`. By the time any transition can fire, `states_map` is ready.

### UID warnings
New `.uid` stub files contain hand-crafted UIDs not registered in `.godot/uid_cache.bin`.
Godot falls back to text path and prints warnings; all resources load correctly.

---

## What the next task may rely on

* `res://npc/guard_arena.tscn` — loads headless; Guard has a working FSM.
* `guard.mode` — read-only String property; always `"Patrol"`, `"Chase"`, or `"Search"`.
* `guard.sight_radius` (200) and `guard.lose_radius` (350) are `@export` and can be overridden.
* `guard.last_known_player_pos` — updated every Chase frame tick while player is visible.
* `Guard/ModeLabel` — Label child with text matching `guard.mode`.
* Guard navigates using the Task 1 nav polygon; `set_target(pos)` still works.
* The Player node is a sibling of Guard in GuardArena (`get_node("Player")`).

---

## What is still unverified

* Visual appearance (headless only).
* Behaviour when multiple guards share the same arena.
* Edge case: player teleported inside the obstacle while Guard is in Chase.
* Performance of `intersect_ray` at high guard counts.
* Whether UID warnings disappear after a full editor import pass.

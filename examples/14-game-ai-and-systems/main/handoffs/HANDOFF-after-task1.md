# Handoff — Task 1 of 3: guard navigation

## Files changed (all new, nothing modified)

| File | Role |
|------|------|
| `godot/npc/guard.gd` | Guard CharacterBody2D script: `set_target(pos)` + physics-frame NavAgent follow |
| `godot/npc/guard.gd.uid` | UID stub (Godot falls back to path; see note below) |
| `godot/npc/guard_arena.gd` | Root Node2D script: builds NavigationPolygon procedurally in `_ready()` |
| `godot/npc/guard_arena.gd.uid` | UID stub |
| `godot/npc/guard_arena.tscn` | 1280×720 arena scene (walls, obstacle, nav region, Player instance, Guard) |
| `godot/tests/test_guard_nav.gd` | Headless SceneTree test: 4 checks + 1 observation |
| `godot/tests/test_guard_nav.gd.uid` | UID stub |

No existing files were touched.

---

## Exact test commands and their real output

All three commands were run from the repo root (`godot/` is the Godot project directory):

### New test — guard navigation
```
godot --headless --path godot --script res://tests/test_guard_nav.gd
```
```
--- Check 3: same-frame set_target before nav-map sync ---
WARNING: res://npc/guard_arena.tscn:3 - ext_resource, invalid UID: uid://b9n3kx5p1yhmw
         - using text path instead: res://npc/guard_arena.gd
WARNING: res://npc/guard_arena.tscn:4 - ext_resource, invalid UID: uid://cgr1a0dv3npfd
         - using text path instead: res://npc/guard.gd
OBSERVE same-frame: nav_finished_before_tick=false reachable_before_tick=false
                    moved_after_0.3s=true guard.position=(194.1835, 347.9354)
--- Check 1: guard navigates around obstacle ---
[same UID warnings omitted for brevity]
PASS guard reaches far-side target within 20.0s
PASS guard never enters obstacle collision bounds
--- Check 2: unreachable target inside obstacle ---
[same UID warnings omitted]
PASS target inside obstacle: is_target_reachable() == false
PASS guard rests outside obstacle bounds for unreachable target (pos=(632.3198, 240.1188))
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

## Check 3 — actual same-frame behaviour (observation only)

When `set_target()` is called in the same call frame as `root.add_child(arena)`, before a
single physics tick has executed:

* `NavigationAgent2D.is_navigation_finished()` → **false**
* `NavigationAgent2D.is_target_reachable()` → **false** (map not yet synced)
* After 0.3 s: guard **has moved** to ~(194, 348); Godot deferred the path request and
  computed it on the first physics frame. The guard was not stuck at its origin.

Conclusion: Godot 4.7 silently defers the first path query when the nav map has not yet
synced. There is no error; movement begins on the next physics tick.

---

## Arena layout (for Tasks 2 and 3)

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
* Guard: `CharacterBody2D`, `CircleShape2D` radius 16, speed 150 px/s,
  `target_desired_distance = 48`, `path_desired_distance = 8`

---

## Navigation polygon implementation detail

`guard_arena.gd._build_nav_polygon()` sets `NavigationPolygon.vertices` directly and
calls `add_polygon()` 12 times (CCW triangles). The triangulation decomposes the arena
into four rectangular strips (top, left, right, bottom) using a fan from v0 and v10
respectively. Every pair of adjacent strips shares a full edge (same two vertex indices,
reversed), which is required for Godot's navigation graph to connect them:

```
Top strip fan from v0:  T1(0,1,5)  T2(0,5,4)  T3(0,4,3)  T4(0,3,2)
Left strip:             T5(2,3,7)  T6(2,7,6)
Right strip:            T7(4,5,9)  T8(4,9,8)
Bottom strip fan v10:   T9(10,6,7) T10(10,7,8) T11(10,8,9) T12(10,9,11)
```

Key shared edges: T4↔T5 via (3,2)/(2,3); T2↔T7 via (5,4)/(4,5);
T6↔T9 via (7,6)/(6,7); T8↔T11 via (9,8)/(8,9).

`make_polygons_from_outlines()` is **not** used (deprecated in Godot 4.2).

---

## UID warnings

The three new `.uid` stub files contain hand-crafted UIDs that are not registered in
`.godot/uid_cache.bin`. Godot 4 emits `invalid UID — using text path instead` warnings
but loads the resources correctly by path. This does not affect test results. A full
editor import would register the UIDs and silence the warnings.

---

## What the next task may rely on

* `res://npc/guard_arena.tscn` — loads successfully headless; contains a working
  Guard node at path `Guard` with `set_target(Vector2)` and a child
  `NavigationAgent2D`.
* Guard navigates around the centre obstacle without penetrating it.
* `NavigationAgent2D.is_target_reachable()` correctly returns `false` for any point
  inside the nav hole (x 500–780, y 240–480).
* The Player instance is present but stationary (no input given in the test).
* Navigation map synchronises after the first physics frame; same-frame `set_target()`
  works but produces `is_target_reachable() == false` until the first tick completes.

---

## What is still unverified

* Visual rendering, sprite, or colour appearance of the guard or obstacle (headless only).
* Dynamic retargeting: what happens if `set_target()` is called repeatedly while the
  guard is already navigating.
* Physics interaction between Guard and Player (both are CharacterBody2D; no avoidance
  is configured on the NavigationAgent2D).
* Navigation correctness when the guard's start position is very close to the nav-hole
  boundary.
* Performance with multiple simultaneous guards.
* Whether UID warnings disappear after a full editor import pass.

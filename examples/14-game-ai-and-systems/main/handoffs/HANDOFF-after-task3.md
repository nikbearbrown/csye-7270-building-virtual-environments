# Handoff — Task 3 of 3: selectable FSM / behavior tree

## Completed work

The guard supports `Guard.Brain.FSM` (default) and `Guard.Brain.BT`, selected through
its exported `brain` property **before the arena enters the scene tree**. Both brains
use the existing navigation, LOS query, patrol waypoints, sight/lose radii, and
last-known player position. `guard.mode` is read-only to callers and the ModeLabel
tracks it for either brain. Runtime brain switching is not implemented.

| File | Task 3 role |
|---|---|
| `godot/npc/bt/bt_node.gd` | Shared SUCCESS / FAILURE / RUNNING status and tick/reset interface |
| `godot/npc/bt/selector.gd` | Tries children in order until SUCCESS or RUNNING; remembers a running child |
| `godot/npc/bt/sequence.gd` | Runs children until FAILURE or RUNNING; remembers a running child |
| `godot/npc/bt/condition.gd` | Maps a predicate to SUCCESS / FAILURE |
| `godot/npc/bt/action.gd` | Delegates a tick to a callable |
| `godot/npc/guard_bt.gd` | Guard tree, action callbacks, and per-guard blackboard |
| `godot/npc/guard.gd` | Exported brain choice, BT ticking, shared mode/label interface |
| `godot/npc/guard_fsm.gd` | Initializes FSM only when selected; disables its entire process branch in BT mode |
| `godot/tests/test_bt.gd` | 14 checks for composites, leaves, RUNNING memory, and reset |
| `godot/tests/test_guard_fsm.gd` | Runs the behavior checks for both brains, plus startup processing regressions (14 total) |
| `HANDOFF.md` | Task 3 implementation, verification, and transition comparison |

This continuation changes only `guard_fsm.gd`, `test_guard_fsm.gd`, and this handoff.
Neither `res://state_machine/state_machine.gd` nor `state.gd` was edited. No window
was opened and no commit was created.

## Inactive FSM runtime fix

BT mode deliberately skips the base FSM initialization, leaving `current_state`
null. Disabling individual callbacks in `_enter_tree()` did not prevent startup
from enabling inherited processing, so the base `_physics_process()` called
`update()` on that null state. The guard-specific subclass now sets
`process_mode = Node.PROCESS_MODE_DISABLED` before returning. That disables both
processing and input for the inactive FSM branch through startup, without changing
the shared state-machine code. The regression checks run after startup and verify
that the BT's FSM stays uninitialized and cannot process, while the selected FSM
is initialized and can process. Full logs are also scanned for runtime errors.

## Tree and blackboard

```text
Selector
├── Sequence
│   ├── Condition: player within sight_radius and clear LOS
│   └── Action: Chase
├── Sequence
│   ├── Condition: has_last_known_position
│   └── Action: Search
└── Action: Patrol
```

Selector and Sequence resume their RUNNING child; they reset after completion or
explicit `reset()`. Chase stays RUNNING until the player exceeds `lose_radius` or
LOS is blocked. This preserves hysteresis even after the initial sight condition
would fail. Search stays RUNNING until arrival within 64 px and a 1.0-second wait,
then clears the remembered-position flag and returns FAILURE so Patrol runs in
that tick. Patrol returns SUCCESS each tick, allowing sight checks on the next
one. Search is not preempted by renewed visibility, matching the existing FSM.

The blackboard stores `has_last_known_position`, `waypoint`, `retarget_timer`,
`waiting`, `wait_timer`, and `patrol_target_set`. Guard/player references are added
only during a tick and removed afterward to avoid retaining scene references.
The actual last-known position stays on the guard. Chase retargets every 0.2 s.
Defaults remain `sight_radius = 200`, `lose_radius = 350`, and speed 150 px/s.
The patrol loop remains (160,160), (1100,160), (1100,560), (160,560).

## Where transition logic lives: FSM versus BT

The FSM keeps its transition conditions inside each state's `update()` method:
Patrol emits `finished("Chase")` on sight, Chase emits `finished("Search")` on loss,
and Search emits `finished("Patrol")` after arrival and waiting. GuardFSM maps those
names to nodes, and the shared machine performs exit/enter and current-state
bookkeeping. The BT expresses branch priority in the Selector/Sequence structure
in `guard_bt.gd`, with sight and remembered-position conditions gating actions.
Its action return statuses and blackboard values determine when control moves to
another branch; the generic composites manage RUNNING-child memory. Thus BT
transition logic is shared between tree structure, conditions, and action
completion/failure rules, while the FSM's outgoing transitions are explicit in
individual state scripts. `mode` reports the chosen behavior in either design.

## Headless verification

Engine: Godot 4.7.2.stable.official.ed1daf0bf. Every command used `--headless
--fixed-fps 60`; the project physics rate remains unchanged at 120 Hz.

The first pass had all checks passing and exit 0, but every log included a macOS
`get_system_ca_certificates` startup `ERROR:`. Those runs **do not count as clean**.
For the clean rerun, a temporary `godot/override.cfg` supplied the installed PEM
certificate bundle instead of querying the macOS certificate store:

```ini
[network]
tls/certificate_bundle_override="/etc/ssl/cert.pem"
```

The file was removed after the rerun. This is a local test-environment workaround;
no permanent certificate setting or error-output suppression was added. To
reproduce in this sandbox, create this file only if it does not already exist,
run the commands below, and remove the temporary file afterward.

```sh
godot --headless --fixed-fps 60 --path godot --script res://tests/test_guard_fsm.gd
godot --headless --fixed-fps 60 --path godot --script res://tests/test_bt.gd
godot --headless --fixed-fps 60 --path godot --script res://tests/test_guard_nav.gd
godot --headless --fixed-fps 60 --path godot --script res://test_input.gd
godot --headless --fixed-fps 60 --path godot --script res://test_combo.gd
```

Each run captured combined stdout/stderr without filtering. Clean means exit 0
**and** no line containing `SCRIPT ERROR` or `ERROR:`.

| Script | Checks | Failures | Exit | Error lines |
|---|---:|---:|---:|---:|
| `tests/test_guard_fsm.gd` (FSM and BT, 7 each) | 14 | 0 | 0 | 0 |
| `tests/test_bt.gd` | 14 | 0 | 0 | 0 |
| `tests/test_guard_nav.gd` | 4 | 0 | 0 | 0 |
| `test_input.gd` | 18 | 0 | 0 | 0 |
| `test_combo.gd` | 11 | 0 | 0 | 0 |

Total: **61 passing checks**. Full clean logs are recorded below and also at
`/tmp/ch14-task3-tests/clean/`; initial non-clean logs are in
`/tmp/ch14-task3-tests/`. `git diff --check` passed.

## Limits of verification

Visual appearance, multiple guards, and runtime brain switching were not tested.
The existing navigation test ran unchanged with the default FSM; its unreachable
case asserts non-reachability and remaining outside the obstacle, not arrival at
the closest reachable point. Its observed final position in this run was
(160,360), so no stronger claim is made. Navigation observations and timing can
vary with asynchronous navigation synchronization.

## Actual clean-run output

### test_guard_fsm

```text
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

=== Brain: FSM ===
--- Test 1: Patrol -> Chase -> Search -> Patrol ---
PASS initial mode is Patrol
PASS selected FSM is initialized and can process after startup
FIXTURE: player → (280, 360)  dist=120 < sight_radius=200, LOS clear
PASS mode -> Chase when player in sight (0.1 s)
FIXTURE: player → (800, 560)  dist >> lose_radius=350
PASS mode -> Search when player beyond lose_radius (0.1 s)
PASS mode -> Patrol after Search completes (1.1 s)
--- Test 2: player hidden behind obstacle stays in Patrol ---
FIXTURE: player → (900, 360)  behind obstacle, LOS blocked
PASS player hidden behind obstacle does not trigger Chase
--- Test 3: player between sight_radius and lose_radius stays Chase >=1s ---
FIXTURE: player → (280, 360)  trigger Chase
FIXTURE: player → (400, 360)  dist≈240, sight_radius<dist<lose_radius, LOS clear
PASS player between sight_radius and lose_radius: mode stays Chase for >=1 s
=== Brain: BT ===
--- Test 1: Patrol -> Chase -> Search -> Patrol ---
PASS initial mode is Patrol
PASS inactive FSM remains uninitialized and cannot process after startup
FIXTURE: player → (280, 360)  dist=120 < sight_radius=200, LOS clear
PASS mode -> Chase when player in sight (0.1 s)
FIXTURE: player → (800, 560)  dist >> lose_radius=350
PASS mode -> Search when player beyond lose_radius (0.1 s)
PASS mode -> Patrol after Search completes (1.2 s)
--- Test 2: player hidden behind obstacle stays in Patrol ---
FIXTURE: player → (900, 360)  behind obstacle, LOS blocked
PASS player hidden behind obstacle does not trigger Chase
--- Test 3: player between sight_radius and lose_radius stays Chase >=1s ---
FIXTURE: player → (280, 360)  trigger Chase
FIXTURE: player → (400, 360)  dist≈240, sight_radius<dist<lose_radius, LOS clear
PASS player between sight_radius and lose_radius: mode stays Chase for >=1 s
RESULT 14 checks; 0 failures
```

### test_bt

```text
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

PASS Selector stops at first SUCCESS
PASS Sequence stops at first FAILURE
PASS empty Selector fails
PASS empty Sequence succeeds
PASS Condition maps false to FAILURE
PASS Condition maps true to SUCCESS
PASS Selector propagates RUNNING
PASS Selector resumes running child with shared blackboard and delta
PASS Selector restarts after completion
PASS Selector explicit reset forgets running child
PASS Sequence propagates RUNNING
PASS Sequence resumes running child with shared blackboard and delta
PASS Sequence restarts after completion
PASS Sequence explicit reset forgets running child
RESULT 14 checks; 0 failures
```

### test_guard_nav

```text
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

--- Check 3: same-frame set_target before nav-map sync ---
OBSERVE same-frame: nav_finished_before_tick=false reachable_before_tick=false moved_after_0.3s=true guard.position=(160.0, 316.25)
--- Check 1: guard navigates around obstacle ---
PASS guard reaches far-side target within 20.0s
PASS guard never enters obstacle collision bounds
--- Check 2: unreachable target inside obstacle ---
PASS target inside obstacle: is_target_reachable() == false
PASS guard rests outside obstacle bounds for unreachable target (pos=(160.0, 360.0))
RESULT 4 checks; 0 failures
```

### test_input

```text
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

PASS initial Idle
PASS debug stack initially Idle
PASS D moves right in Move
PASS walk speed
PASS Shift run speed
PASS release restores Idle
PASS Space pushes Jump
PASS jump raises body pivot
PASS debug stack shows Jump over Idle
PASS state label follows transition
PASS landing pops Idle
PASS debug stack follows landing pop
PASS X enters Stagger
PASS stagger animation restores Idle
PASS F enters Attack
PASS sword enabled during attack
PASS attack completes and pops Idle
PASS R spawns bullet
RESULT 18 checks; 0 failures
```

### test_combo

```text
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

PASS first attack
PASS animation opens buffer
PASS second F buffered
PASS second swing starts
PASS third swing starts
PASS third swing damage metadata
PASS third swing medium animation
PASS combo finishes despite fourth F
PASS one push/pop for full combo
PASS subsequent combo restarts at one
PASS subsequent single attack ends
RESULT 11 checks; 0 failures
```

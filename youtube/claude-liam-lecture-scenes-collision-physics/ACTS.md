# Scenes, Collision, and Physics in Godot

One self-contained CSYE 7270 Building Virtual Environments lecture. Liam in for Bear. Stage-one layout only, per lecture skill; no audio or film rendered here.

## Coverage map
| Act | Research source | Overview / user prose | Recurring cast |
|---|---|---|---|
| 1 — Compose a Game | Core problem; Parts 1–2; scene conventions | Scenes, nodes, transformations, instances | Level, player, two coins; real scene files |
| 2 — Decide What Interacts | Parts 3–4 | Body taxonomy, shapes, layers/masks | Floor, player rectangle, crate, coin; named matrix |
| 3 — Design the Motion | Part 5, including complete reference controller | Character movement and rigid-body response | Player, floor, jump trajectory, timer windows |
| 4 — Turn Contact into Gameplay | Parts 6–7 | Signals and pickups | Coin latch, enemy sensor, block, tile grid |
| 5 — Make Time and Tests Explicit | Parts 8–9; grading tolerances | Fixed ticks, CCD, determinism | Tick marks, sampled path, measured test output |
| 6 — Transfer and Verify | Parts 10–12; source lineage | 3D geometry, backend, first exercise | Equivalent nodes, minimal lab, review checklist |

Parts 3/4 are prerequisites for Part 5; source order retained. Debugging rows are taught at their mechanisms and revisited through failure tests. All source code blocks are adapted into executable examples or explicitly identified conventions, never represented as a completed reference-game audit. No reference game was supplied.

## Editorial corrections to verify
- Fixed rate is not deterministic; no cross-platform replay guarantee.
- speed/tick-rate is a diagnostic, not a sufficient collision guarantee; swept character movement differs from discrete rigid-body integration.
- Jolt is built in and defaults for new projects in the checked documentation; existing project settings are authoritative.
- Character bodies can affect other bodies; do not state they can never push rigid bodies. Explicit impulses implement a deliberate push policy, and require mask contact.
- Node itself has no transform; Node2D/Node3D inherit transform context with exceptions.
- One-way direction and tile chunking must be checked against the installed engine and matching reference.
- Coin needs an immediate collected latch in addition to deferred monitoring changes.
- A fixed 0.2-second drop-through timer can re-enable too soon; identify as a simple policy with a clearance test required.
- Stomp origin comparison is a heuristic; add falling/top-contact evidence and test side/corner cases.
- Gravity-ratio recipe loses gravity direction and may divide by zero; teach intentional handling of the vector instead.

## Left out, with reasons
- Release-date/4.8 forecast: transient chronology does not teach the mechanisms; pin the lab version instead.
- Scene Paint and AwaitTweener: optional workflow conveniences outside the collision mechanism; included in companion version notes only if corroborated.
- Exact Jolt soft-body/mass/plane changes were corroborated in the live 4.7 migration page and are now included in B46A (Act 6).
- Rapier determinism promise: third-party configuration-dependent alternative, no verified deterministic lab; retain source link as optional research, no guarantee.
- Bibliographic commentary: keep lineage in SOURCES.md; do not narrate a reading list.
- Duplicated prose/code across three supplied sources: consolidated into the same worked example, with all distinct ideas retained.

## Bookends
BOPEN: course → exact film title → short purpose. BIDEA corrects “one physics problem” to “three different responsibilities”. BDEFS: Node, Instance, Shape, Velocity, Tick. Six acts; six recap lines; one complete learner prompt with two checks; exact-title @NikBearBrown outro.

## Beat map

- B01: Three responsibilities — Act 1
- B02: Pin the engine — Act 1
- B03: Read the scene — Act 1
- B04: Transform inheritance — Act 1
- B05: Instance a definition — Act 1
- B06: Composition and variants — Act 1
- B07: Call down, signal up — Act 1
- B08: Stateful blocks — Act 1
- B09: Scene files and ownership — Act 1
- B10: Static and animatable — Act 2
- B11: Simulated bodies — Act 2
- B12: Controlled bodies — Act 2
- B13: Areas detect — Act 2
- B14: Choose the boundary — Act 2
- B15: An interaction matrix — Act 2
- B16: Layer numbers and bits — Act 2
- B17: Test the missing pickup — Act 2
- B18: Shared shape resources — Act 2
- B19: Velocity or displacement — Act 3
- B20: Design a jump — Act 3
- B21: Apply acceleration — Act 3
- B22: Horizontal response — Act 3
- B23: Grace windows — Act 3
- B24: Cut and bounce — Act 3
- B25: Classify surfaces — Act 3
- B26: Moving platforms and pushes — Act 3
- B27: Measure the jump — Act 3
- B28: Handle the callback — Act 4
- B29: One pickup, one award — Act 4
- B30: Stomp or hurt — Act 4
- B31: Wire the enemy — Act 4
- B32: Author tile collision — Act 4
- B33: The quadrant trap — Act 4
- B34: Recover the intended cell — Act 4
- B35: One-way surfaces — Act 4
- B36: Dropping through — Act 4
- B37: Two clocks — Act 5
- B38: Distance is a diagnostic — Act 5
- B39: Continuous detection — Act 5
- B40: Render between ticks — Act 5
- B41: Teleport deliberately — Act 5
- B42: Fixed is not deterministic — Act 5
- B43: Diagnose the symptom — Act 5
- B44: What the run proves — Act 5
- B45: Grade a tolerance — Act 5
- B46: Choose the backend — Act 6
- B46A: Backend migration details — Act 6
- B47: Three D shapes — Act 6
- B48: Version errors in code — Act 6
- B49: Add real simulation — Act 6
- B50: Submit the collision matrix — Act 6
- B51: The first test room — Act 6
- B52: Give agents a contract — Act 6
- B53: Audit the seed — Act 6
- B54: Keep the reference nearby — Act 6

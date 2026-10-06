# Game Design Document — walker-3d-platformer

**Recovered** by `/gdd reverse --path godot` · 2026-09-27  
**Gate — unsigned at time of writing (silent flag)**  
**Revision:** 1 · **Mode:** recovered  

Every claim carries an evidence tag:  
- `[OBSERVED path:line]` — the code does this  
- `[INFERRED]` — the code strongly implies this; evidence stated  
- `[MISSING]` — the code cannot tell you this  

Numbers found in code are `[OBSERVED]` tuning values, not approved design. A recovered GDD describes what exists; it is not an approval of any of it.

---

## 01. METADATA

| Field | Value |
|---|---|
| Game ID | walker-3d-platformer |
| Engine | Godot 4.7 `[OBSERVED godot/project.godot:18]` |
| Physics | Jolt Physics 3D, 120 Hz, interpolated `[OBSERVED godot/project.godot:149-151]` |
| Renderer | Forward+ (default); gl_compatibility (fallback) `[OBSERVED godot/stage/stage.gd:4]` |
| Gravity | 22.0 m/s² `[OBSERVED godot/project.godot:153]` |
| Main scene | res://game.tscn `[OBSERVED godot/project.godot:17]` |
| Scripts | 8 GDScript files (typed) `[OBSERVED]` |
| Scenes | 8 .tscn files `[OBSERVED]` |
| GLB models | 2 (player.glb, enemy.glb) `[OBSERVED]` |
| GDD revision | 1 |
| Recovered | 2026-09-27 |

---

## 02. VISION SUMMARY

**Logline:** `[MISSING]`

**Playable idea** `[OBSERVED godot/GAME-BRIEF.md]`: A blue robot moves through a textured 3D platform environment, jumps between surfaces, collects coins, and shoots projectiles at patrolling enemies. A camera follows the character and responds to obstructing geometry.

**Walker context** `[OBSERVED godot/GAME-BRIEF.md]`: This is a Walker adaptation of Godot's official 3D Platformer demo. The initial change is the project name only. Controls, movement, scenes, art, and sound are preserved from the upstream Godot official demo (tagged `3d`, `demo`, `gridmap`, `official`, `physics`).

**Teaching intent** `[INFERRED from GAME-BRIEF.md]`: The project demonstrates CharacterBody3D 3D movement, camera following with obstruction handling, coin collectibles, and enemy patrol — observable and inspectable by students of the Godot engine. The teaching loop is: Game brief → Build → Playtest → Inspect → Revise → Export.

**No top-level game script establishing a scored win/ending is observed** `[OBSERVED godot/GAME-BRIEF.md]`. Do not invent one.

---

## 03. DESIGN PILLARS

`[MISSING]` No explicit design pillars are documented in any source file.

Zelda's read — pillars inferred from code structure and the Walker brief. These require human confirmation before any design decision references them.

**Pillar A — Grounded Physical Movement**  
*Player experience it protects:* The character must feel like it has mass and respond to momentum.  
*Evidence:* Jolt Physics at 120 Hz; gravity=22.0 m/s² (2.24× Earth); AIR_IDLE_DEACCEL=false (no air stopping); AIR_ACCEL_FACTOR=0.5 (limited air authority); sharp-turn threshold at 140° breaks momentum. The character decelerates into a direction change rather than snapping. `[INFERRED from player.gd constants]`  
*What violates it:* instant-stop air movement, floaty gravity, unrestricted air steering.

**Pillar B — Readable Camera**  
*Player experience it protects:* The player sees what matters without fighting the camera.  
*Evidence:* Three-ray autoturn system pushes camera away from geometry before it clips. Obstruction pull moves camera to collision point as worst case. Top-level detach prevents parenting artifacts. Height clamped [0, 2] prevents floor-skating view. `[INFERRED from follow_camera.gd]`  
*What violates it:* camera clipping into geometry, manual camera rotation added without autoturn integration.

**Pillar C — Inspectability**  
*Player experience it protects (for the Walker/learning audience):* Every mechanism is readable from source.  
*Evidence:* 8 scripts, no AutoLoads, no scene-specific game manager, all feature logic self-contained in owning scene scripts. `[INFERRED from GAME-BRIEF.md and codebase structure]`  
*What violates it:* global state, singletons that hide flow, cross-scene coupling.

---

## 04. CORE LOOP

Diagrams: `design/diagrams/core-loop.svg`

**Micro loop (5–15 seconds)** `[INFERRED from mechanics]`  
Move → Orient via camera → Jump to platform → Shoot enemy OR collect coin → Land → Move  
Reset available at any point (R or fall).

**Macro loop (30–120 seconds)** `[INFERRED from level layout]`  
Start at spawn → Navigate coin cluster → Collect coins (Area3D feedback) → Locate nearby enemy → Shoot (press-edge) → Proceed to next area of the level

**Session loop** `[MISSING win state]`  
Start at spawn → Explore open level → [Fall → auto-reset to spawn] → [No session end observed]  
The session has no designed end state. This is a confirmed gap, not a feature. See OQ-01 in decisions.md.

---

## 05. PLAYER EXPERIENCE GOALS

`[MISSING]` No PX Goals are documented in any source file.

Zelda's read — inferred from the mechanics as built. All require human confirmation.

| ID | PX Goal | Evidence basis |
|---|---|---|
| PX-01 | Feel the weight of a grounded character — momentum builds and costs something to redirect | ACCEL=14, gravity=22, sharp-turn stop, air factor=0.5 `[INFERRED player.gd]` |
| PX-02 | Read the 3D space through a camera that works for you, not against you | Three-ray autoturn, obstruction pull, height clamp `[INFERRED follow_camera.gd]` |
| PX-03 | Control jump height deliberately — hold for distance, cut for precision | Variable jump: JUMP_VELOCITY=12.5, cut×0.7; measured heights 1.53m/3.60m `[INFERRED player.gd, evidence/]` |
| PX-04 | Use coin clusters as breadcrumbs through unfamiliar 3D space | 73 coins in 6–8 clusters across level `[INFERRED game.tscn]` |
| PX-05 | Eliminate a patrolling enemy with a single well-timed shot | One-hit kill: bullet contact → enemy queue_free `[INFERRED enemy.gd]` |

---

## 06. MECHANICS

Diagrams: `design/diagrams/player-state-machine.svg`, `design/diagrams/enemy-patrol.svg`

---

### M-01 — Ground Movement
**Owner scene:** `godot/player/player.tscn`  
**Script:** `godot/player/player.gd`  
**Node:** CharacterBody3D (class Player)  
**Input actions:** `move_forward` (W/↑/LStick-Y-), `move_back` (S/↓/LStick-Y+), `move_left` (A/←/LStick-X-), `move_right` (D/→/LStick-X+)

Camera-relative horizontal movement. `Input.get_vector()` produces a 2D input; it is rotated into the camera's basis then projected onto the XZ plane (Y zeroed, renormalized). Separate `horizontal_direction` and `horizontal_speed` allow smooth arc turning via `adjust_facing()`.

Sharp turn detection: if moving speed >0.1 and angle between movement direction and current heading >140°, acceleration is suppressed. The player must decelerate before reversing direction. `[OBSERVED player.gd:73-74]`

Mesh rotation uses `adjust_facing()` — angular interpolation toward movement direction, rate weighted by `TURN_SPEED / speed`. `[OBSERVED player.gd:97-115, 179-202]`

| Constant | Value | Tag |
|---|---|---|
| MAX_SPEED | 6.0 m/s | `[OBSERVED player.gd:14]` |
| ACCEL | 14.0 m/s² | `[OBSERVED player.gd:18]` |
| DEACCEL | 14.0 m/s² | `[OBSERVED player.gd:19]` |
| TURN_SPEED | 40.0 | `[OBSERVED player.gd:13]` |
| SHARP_TURN_THRESHOLD | deg_to_rad(140°) | `[OBSERVED player.gd:21]` |
| CHAR_SCALE | Vector3(0.3, 0.3, 0.3) | `[OBSERVED player.gd:12]` |

---

### M-02 — Air Movement
**Owner scene:** `godot/player/player.tscn`  
**Script:** `godot/player/player.gd:122-133`

In air, horizontal acceleration is capped at `AIR_ACCEL_FACTOR × ACCEL`. No air deceleration when no input (`AIR_IDLE_DEACCEL = false` — constant, not tunable at runtime). Air max speed capped at `MAX_SPEED`. `[OBSERVED player.gd:122-133]`

| Constant | Value | Tag |
|---|---|---|
| AIR_ACCEL_FACTOR | 0.5 | `[OBSERVED player.gd:20]` |
| AIR_IDLE_DEACCEL | false | `[OBSERVED player.gd:17]` |

---

### M-03 — Variable Jump
**Owner scene:** `godot/player/player.tscn`  
**Script:** `godot/player/player.gd:117-137`  
**Input action:** `jump` (Space / Mouse RMB / Gamepad A)

Jump initiates only when `is_on_floor()` is true and `jumping` flag is false. Sets `vertical_velocity = JUMP_VELOCITY`, sets `jumping = true`, plays SoundJump. Releasing jump before apex while `velocity.y > 0` multiplies vertical velocity by 0.7. `jumping` flag clears when `vertical_velocity < 0` (past apex). Single jump only — no coyote time, no double jump observed.

| Constant | Value | Tag |
|---|---|---|
| JUMP_VELOCITY | 12.5 m/s | `[OBSERVED player.gd:15]` |
| Early-release multiplier | 0.7 | `[OBSERVED player.gd:137]` |
| Measured rise (6-tick hold) | ~1.53 m | `[OBSERVED evidence/baseline-probe.json]` |
| Measured rise (60-tick hold) | ~3.60 m | `[OBSERVED evidence/baseline-probe.json]` |

---

### M-04 — Gravity
**Owner:** project.godot, CharacterBody3D  

`get_gravity()` returns the project gravity setting (22.0 m/s²) — approximately 2.24× Earth standard. Applied every `_physics_process` frame before horizontal velocity resolution. Produces faster falls and tighter arc apexes than standard Earth gravity. Physics runs at 120 Hz with interpolation enabled. `[OBSERVED godot/project.godot:149-153]`

| Setting | Value | Tag |
|---|---|---|
| Gravity | 22.0 m/s² | `[OBSERVED project.godot:153]` |
| Physics Hz | 120 | `[OBSERVED project.godot:149]` |
| Physics interpolation | true | `[OBSERVED project.godot:151]` |

---

### M-05 — Fall Recovery
**Owner scene:** `godot/player/player.tscn`  
**Script:** `godot/player/player.gd:36-43`  
**Input action:** `reset_position` (R / Gamepad Y)

Two triggers: (1) `global_position.y < -12`, or (2) `Input.is_action_pressed("reset_position")`. Both paths: `position = initial_position` (cached in `_ready()`), `velocity = Vector3.ZERO`, `reset_physics_interpolation()` (prevents lerp from old to new position). `[OBSERVED player.gd:36-43]`

Fall threshold: y = -12. `[OBSERVED player.gd:36]`

---

### M-06 — Shooting
**Owner scenes:** `godot/player/player.tscn`, `godot/player/bullet/bullet.tscn`  
**Scripts:** `godot/player/player.gd:153-165`, `godot/player/bullet/bullet.gd`  
**Input action:** `shoot` (F9 / Mouse LMB / Gamepad B / Gamepad L3 / Gamepad Right Trigger)

Press-edge only (`shoot_attempt and not prev_shoot`). Spawns a Bullet (RigidBody3D, class Bullet) as a sibling in the scene tree via `get_parent().add_child(bullet)`. Sets bullet's global transform to the muzzle marker (`$Player/Skeleton/Bullet`) orthonormalized. Applies forward-axis velocity (`BULLET_SPEED`). Excludes player from bullet collision via `add_collision_exception_with(self)`. Plays SoundShoot. Sets `shoot_blend = SHOOT_TIME` for animation fade. `shoot_blend` decays at ×0.97 per frame. `[OBSERVED player.gd:153-165]`

`bullet.enabled = true` on spawn. Set `false` on first enemy contact to prevent multi-hit while the bullet is fading. `[OBSERVED bullet.gd:6, enemy.gd:44]`

| Constant | Value | Tag |
|---|---|---|
| BULLET_SPEED | 20.0 m/s | `[OBSERVED player.gd:16]` |
| SHOOT_TIME | 1.5 | `[OBSERVED player.gd:9]` |
| SHOOT_SCALE | 2.0 | `[OBSERVED player.gd:10]` |

---

### M-07 — Coin Collection
**Owner scenes:** `godot/coin/coin.tscn`, `godot/player/player.tscn`  
**Scripts:** `godot/coin/coin.gd`, `godot/player/player.gd:47-51`  
**Node:** Area3D

On body enter: if `body is Player` and `not taken` → play "take" animation, set `taken = true`, increment `body.coins`. One-time per instance — no respawn. `[OBSERVED coin.gd:7-13]`

Player stores count in `coins: int` (session-only, no persistence). Updates `%CoinCount` Label3D and four parallax shadow copies (`Parallax`, `Parallax2`, `Parallax3`, `Parallax4`) every physics frame for pseudo-3D depth effect. `[OBSERVED player.gd:47-51]`

73 coin instances placed in the scene in spatial clusters. `[OBSERVED game.tscn — 73 Coin nodes counted]`

---

### M-08 — Enemy Patrol
**Owner scene:** `godot/enemy/enemy.tscn`  
**Script:** `godot/enemy/enemy.gd`  
**Node:** RigidBody3D

Floor ray (`_ray_floor: RayCast3D`) and wall ray (`_ray_wall: RayCast3D`) evaluated in `_integrate_forces`. `advance = _ray_floor.is_colliding() and not _ray_wall.is_colliding()`. On advance: accelerate along current facing direction; decelerate on perpendicular (lateral) axis. On not-advance: rotate in place using `Basis(up, rot_dir * ROT_SPEED * delta)`. `rot_dir` initializes to 4.0; resets to 1.0 when the enemy transitions from advance to turn (`prev_advance → false`). `[OBSERVED enemy.gd:49-73]`

4 enemy instances at fixed world positions. `[OBSERVED game.tscn]`

| Constant | Value | Tag |
|---|---|---|
| ACCEL | 5.0 m/s² | `[OBSERVED enemy.gd:4]` |
| DEACCEL | 20.0 m/s² | `[OBSERVED enemy.gd:5]` |
| MAX_SPEED | 2.0 m/s | `[OBSERVED enemy.gd:6]` |
| ROT_SPEED | 1.0 rad/s | `[OBSERVED enemy.gd:7]` |
| Initial rot_dir | 4.0 | `[OBSERVED enemy.gd:11]` |

---

### M-09 — Enemy Death
**Owner scene:** `godot/enemy/enemy.tscn`  
**Script:** `godot/enemy/enemy.gd:34-47, 77-78`

Detected in `_integrate_forces` via contact loop. On contact with a Bullet where `bullet.enabled == true`: set `dying = true`, unlock all rotation axes (`axis_lock_angular_*= false`), set `collision_layer = 0` (removes from collision), apply angular spin (`-contact_normal.cross(up).normalized() * 33.0`), queue animation "impact" then "extra/explode", set `bullet.enabled = false`, stop SoundWalkLoop, play SoundHit. Returns immediately; remaining contacts ignored. `[OBSERVED enemy.gd:34-47]`

`_die()` called by animation signal (end of explode): `queue_free()`. `[OBSERVED enemy.gd:77-78]`

---

### M-10 — Follow Camera
**Owner scene:** `godot/player/player.tscn`  
**Script:** `godot/player/follow_camera.gd`  
**Node:** Camera3D

In `_ready()`: finds ancestor RigidBody3D or CharacterBody3D and stores its RID in `collision_exception` (prevents camera rays from hitting player/enemies). Calls `set_as_top_level(true)` to decouple transform from parent. `[OBSERVED follow_camera.gd:16-29]`

In `_physics_process()`: computes `difference = cam_pos - target`. Clamps length to [min_distance, max_distance]. Clamps Y component to [MIN_HEIGHT, MAX_HEIGHT]. Casts three rays from target to `target + difference` at 0°, +autoturn_aperture°, -autoturn_aperture°. Result: center blocked → move camera to hit point; only left blocked → rotate right; only right blocked → rotate left; both sides blocked, center clear → no autoturn. Applies `look_at_from_position` then optional vertical tilt. `[OBSERVED follow_camera.gd:32-91]`

| Export var | Value | Tag |
|---|---|---|
| min_distance | 0.5 | `[OBSERVED follow_camera.gd:9]` |
| max_distance | 3.5 | `[OBSERVED follow_camera.gd:10]` |
| MIN_HEIGHT | 0.0 (const) | `[OBSERVED follow_camera.gd:4]` |
| MAX_HEIGHT | 2.0 (const) | `[OBSERVED follow_camera.gd:5]` |
| autoturn_ray_aperture | 25.0° | `[OBSERVED follow_camera.gd:12]` |
| autoturn_speed | 50.0°/s | `[OBSERVED follow_camera.gd:13]` |
| angle_v_adjust | 0.0 | `[OBSERVED follow_camera.gd:11]` |

---

### M-11 — Touch Controls
**Owner scenes:** `godot/touch_screen_ui/touch_screen_ui.tscn`, `godot/touch_screen_ui/virtual_joystick/virtual_joystick_scene.tscn`  
**Scripts:** `godot/touch_screen_ui.gd`, `godot/touch_screen_ui/virtual_joystick/virtual_joystick.gd`  
**Node:** CanvasLayer, Control (VirtualJoystickAddon)

CanvasLayer hides initially; shows only when `DisplayServer.is_touchscreen_available()`. `[OBSERVED touch_screen_ui.gd:4-6]`

VirtualJoystick (FIXED mode): maps drag output to `move_left`, `move_right`, `move_forward`, `move_back` via `Input.action_press/release()`. Deadzone 10px, clamp 75px. Jump/shoot on touchscreen: verified by synthetic event injection only; physical hardware unverified. `[OBSERVED virtual_joystick.gd:25, 38-43; FRICTIONAL.md]`

---

## 06b. EDGE CASES

| ID | Condition | Observed behavior | Tag |
|---|---|---|---|
| EC-01 | Jump key released before apex (velocity.y > 0) | vertical_velocity × 0.7 | `[OBSERVED player.gd:135-137]` |
| EC-02 | Jump key pressed while in air | No effect — `not jumping` guard + `is_on_floor()` check | `[OBSERVED player.gd:117]` |
| EC-03 | Movement direction >140° from current heading at speed >0.1 | Acceleration suppressed; normal deceleration continues | `[OBSERVED player.gd:73-74]` |
| EC-04 | Bullet contacts a dying enemy (enabled=false) | No effect | `[OBSERVED enemy.gd:35, bullet.gd:6]` |
| EC-05 | Enemy reaches a ledge (floor ray stops colliding) | Turn; advance stops | `[OBSERVED enemy.gd:49]` |
| EC-06 | Enemy reaches a wall (wall ray collides) | Turn | `[OBSERVED enemy.gd:49]` |
| EC-07 | Player re-enters a collected coin's Area3D | No effect — `taken = true` guard | `[OBSERVED coin.gd:7]` |
| EC-08 | Camera difference vector near zero | Applies normalized minimum offset (0.0001) | `[OBSERVED follow_camera.gd:83-85]` |
| EC-09 | Both side rays blocked, center ray clear | No autoturn — comment in source: "do nothing" | `[OBSERVED follow_camera.gd:80]` |
| EC-10 | Player falls below y = -12 | Automatic reset; no button required | `[OBSERVED player.gd:36]` |
| EC-11 | Bullet spawned while player is on floor | Gets parent (Game root) as scene container, not player child | `[OBSERVED player.gd:156-157]` |
| EC-12 | Enemy rot_dir initialization | Starts 4.0; resets to 1.0 on first advance→turn transition | `[OBSERVED enemy.gd:11, 61]` |

---

## 07. SYSTEMS

### S-01 — Movement System
**Domain:** Player locomotion  
**Design reason:** `[INFERRED]` Decouple movement authority from frame rate via physics interpolation; provide camera-relative control so 3D space feels natural.  
**Owner scene:** `godot/player/player.tscn`  
**Scripts:** `player.gd`, `follow_camera.gd`  
**Input actions:** `move_forward`, `move_back`, `move_left`, `move_right`, `jump`, `reset_position`  
**Core variables:** velocity (Vector3), horizontal_direction, horizontal_speed, jumping (bool), initial_position  
**Physics:** 120 Hz Jolt, interpolated `[OBSERVED project.godot:149-151]`

### S-02 — Combat System
**Domain:** Shooting and enemy elimination  
**Design reason:** `[INFERRED]` Give the player agency over moving obstacles; demonstrates RigidBody3D contact detection in `_integrate_forces`.  
**Owner scenes:** `godot/player/player.tscn`, `godot/player/bullet/bullet.tscn`, `godot/enemy/enemy.tscn`  
**Scripts:** `player.gd:153-165`, `bullet.gd`, `enemy.gd:34-47`  
**`[MISSING]`** No player health. No kill count. No score for eliminations. Enemies pose no threat to the player.

### S-03 — Collection System
**Domain:** Coin pickup and count display  
**Design reason:** `[INFERRED]` Spatial reward for navigation; provides visible progress feedback.  
**Owner scenes:** `godot/coin/coin.tscn`, `godot/player/player.tscn`  
**Scripts:** `coin.gd`, `player.gd:47-51`  
**State:** `Player.coins` (int, session-only — no persistence)  
**`[MISSING]`** Coin total display, collection-complete event, save/load.

### S-04 — Camera System
**Domain:** Third-person follow camera with obstruction avoidance  
**Design reason:** `[INFERRED]` Maintain visibility in complex 3D geometry without requiring manual camera input from the player.  
**Owner scene:** `godot/player/player.tscn`  
**Script:** `follow_camera.gd`  
**Core variables:** difference (orbit vector), three PhysicsServer3D raycasts, collision_exception (Array[RID])

### S-05 — Rendering System
**Domain:** Visual quality and renderer compatibility  
**Design reason:** `[INFERRED]` Support both modern GPU (Forward+) and legacy/mobile (gl_compatibility) without separate projects.  
**Owner scene:** `godot/stage/stage.tscn`  
**Script:** `stage.gd`  
**Forward+ path:** PCF5 directional shadow, standard energy  
**gl_compatibility path:** PCF13 (`SHADOW_QUALITY_SOFT_HIGH`), energy split across sky-only and light-only duplicate `[OBSERVED stage.gd:4-14]`

### S-06 — Audio System
**Domain:** Gameplay sound feedback  
**Design reason:** `[INFERRED]` Reinforce mechanical events — jump, shoot, coin, enemy death.  
**Assets:** `SoundJump` (player), `SoundShoot` (player), `SoundWalkLoop` (enemy loop), `SoundHit` (enemy)  
**Bus layout:** `godot/default_bus_layout.tres`  
**`[MISSING]`** Background music. Coin collect audio not confirmed in player.gd (may be in coin animation).  
**Known issue:** Original captures contain full-scale PCM samples. Measured peak +0.5 dBFS before gain correction. `[OBSERVED FRICTIONAL.md]`

### S-07 — Input System
**Domain:** Control mapping across keyboard, gamepad, touch  
**Design reason:** `[INFERRED]` Single input action layer enables multi-platform control without branching game code.  
**Registered actions** `[OBSERVED project.godot:96-145]`: `move_forward`, `move_back`, `move_left`, `move_right`, `jump`, `shoot`, `reset_position`, `ui_accept`, `ui_cancel`, `ui_left`, `ui_right`, `ui_up`, `ui_down`  
**Touch:** VirtualJoystick → `Input.action_press/release()` for movement  
**`[MISSING]`** Physical gamepad hardware tested. Physical touchscreen hardware tested.

---

## 08. PROGRESSION

**`[MISSING]`** No progression system is implemented. No multiple levels, no checkpoint, no difficulty ramp, no unlock gate, no level transition.

**`[INFERRED]`** Implicit spatial progression: coin clusters distributed across the level at increasing distance from spawn; enemy placement creates soft gates near some coin groups; higher-elevation platforms require multi-jump navigation. The level has one discovered secret area (lower room reachable by normal inputs) `[OBSERVED FRICTIONAL.md]`.

**Skill curve `[MISSING design]`:** Level is open; all areas nominally accessible from spawn. Difficulty is topographic (jump precision and fall recovery) rather than designed gate sequences.

**Resource curve `[OBSERVED]`:** 73 coins, no respawn, session-only count, no maximum displayed.

**Challenge curve `[MISSING]`:** No increasing challenge. 4 enemies at fixed positions with no AI escalation.

---

## 09. WORLD

Diagram: `design/diagrams/level-flow.svg`

**Setting `[INFERRED from assets]`:** Open 3D platformer level. Grassy/tiled outdoor platforms, direct sun, rendered shadows. No skybox or weather system observed in source.

**Terrain `[OBSERVED godot/stage/stage.tscn]`:** GridMap with 2-unit cells, MeshLibrary `tiles.tres`. Collision shapes: `box.tres`, `trunk.tres`. Occupied GridMap cell range (-3,-1,-8) to (40,8,19), parent offset (-16,-6,-12). Approximate world playable footprint: X ≈ -22 to 64, Y ≈ -18 to 10, Z ≈ -28 to 26.

**Player spawn `[OBSERVED game.tscn:267]`:** ~(-9.5, -3.8, 3.9) world

**Coin clusters `[OBSERVED game.tscn]`:** 73 instances arranged in 6–8 clusters of 2×2 to 3×3 coins. Clusters span from near spawn (low elevation) through mid-level elevated platforms to far-side and return-path positions. Grouping implies intended traversal routes.

**Enemy placement `[OBSERVED game.tscn, world = local + Enemies node offset -16,-6,-12]`:**

| Instance | Approx world position | Adjacent feature |
|---|---|---|
| Enemy1 | (2.3, -0.6, -6.0) | Near start coin cluster |
| Enemy2 | (48.1, -0.6, 5.1) | Mid-level, distant from spawn |
| Enemy3 | (48.0, 0.7, 17.8) | Near far coin cluster |
| Enemy4 | (36.7, -0.6, 15.7) | Mid-level return path |

**Secret area `[OBSERVED FRICTIONAL.md; INFERRED label position]`:** Label3D at approximately (17.2, 6, -2.0) world space, text "You have found a secret area!" Reachable by normal movement and jump inputs through lower route; verified by normal-input driver with no position injection. `[OBSERVED FRICTIONAL.md]`

**Fall threshold `[OBSERVED player.gd:36]`:** y < -12 triggers auto-reset.

---

## 10. NARRATIVE

**`[MISSING]`** No narrative is documented in any source file. No story, dialogue, cutscenes, or character backstory. No lore text beyond the secret area label.

**Secret area label `[OBSERVED FRICTIONAL.md]`:** "You have found a secret area!" — the only written world text. No context, no reward, no further story.

**`[INFERRED]`** Visual setting suggests an outdoor platform environment: grassy terrain tiles, directional sun, robot character. No time-of-day progression, weather, or environmental storytelling observed.

**Design gap:** Without narrative, the film has no frame. The audience observes mechanics but has no reason to care about the player character. See OQ-06 in decisions.md.

---

## 11. CHARACTERS

### Player Character — Blue Robot
**Visual:** `godot/player/player.glb` `[OBSERVED]`  
**Materials:** `player_glow.tres` (emission glow), `player_gray.tres` `[OBSERVED]`  
**Skeleton scale:** Vector3(0.3, 0.3, 0.3) applied to `$Player/Skeleton` `[OBSERVED player.gd:12]`  
**Collision shape:** CapsuleShape3D (central capsule; visual head and arms exceed capsule bounds per FRICTIONAL.md collider inspection) `[INFERRED from FRICTIONAL.md]`  
**AnimationTree parameters `[INFERRED from player.gd:168-176]`:**
- `parameters/state/blend_amount` — 0.0 = FLOOR, 1.0 = AIR
- `parameters/run/blend_amount` — 0.0 = idle, 1.0 = full run
- `parameters/speed/blend_amount` — 0.0 = walk, 1.0 = run
- `parameters/air_dir/blend_amount` — 0.0 = falling, 1.0 = rising
- `parameters/gun/blend_amount` — 0.0 = holstered, 1.0 = raised

**Name:** `[MISSING]`  
**Role / story:** `[MISSING]`  
**Player test:** What does it GIVE the player? A grounded physical avatar to move through 3D space. What does it ASK? Spatial navigation, jump timing, shooting precision. `[INFERRED]`

### Enemy — Patrol Bot
**Visual:** `godot/enemy/enemy.glb` `[OBSERVED]`  
**AnimationPlayer clips `[INFERRED from enemy.gd:_animation_player.play() calls]`:**
- `SoundWalkLoop` (walk audio; loop implied by "Loop" suffix)
- `impact`
- `extra/explode`

**Behavior:** Deterministic floor/wall patrol, one-hit death, no player targeting or awareness. `[OBSERVED enemy.gd]`  
**Placement:** 4 instances, fixed positions, no respawn. `[OBSERVED game.tscn]`  
**Name:** `[MISSING]`  
**Threat to player:** None — no contact damage, no projectile. Obstacle only. `[MISSING — health system absent]`  
**Player test:** What does it GIVE? A moving obstacle and an elimination target. What does it ASK? Press-edge shooting at a slow-moving target. `[INFERRED]`

---

## 12. FEATURE LIST

CORE percentage: 11/16 = 69% `[OBSERVED]` — above the 40% threshold. This is a recovered list from an existing build, not a scoped list. See OQ-01 and decisions.md before using this for planning.

| ID | Feature | Priority | Status |
|---|---|---|---|
| F-01 | Camera-relative ground movement | CORE | OBSERVED — tests pass |
| F-02 | Air movement (limited accel, no air decel) | CORE | OBSERVED |
| F-03 | Variable-height jump | CORE | OBSERVED — heights measured |
| F-04 | Fall / button recovery | CORE | OBSERVED — tests pass |
| F-05 | Press-edge shooting (RigidBody3D bullet) | CORE | OBSERVED — tests pass |
| F-06 | Coin collection (Area3D, one-time) | CORE | OBSERVED — 2 coins in test |
| F-07 | Enemy floor/wall patrol | CORE | OBSERVED |
| F-08 | Enemy death (single bullet) | CORE | OBSERVED — enemy hit in test |
| F-09 | Third-person follow camera | CORE | OBSERVED |
| F-10 | Camera obstruction avoidance | CORE | OBSERVED |
| F-11 | Coin counter Label3D (parallax) | CORE | OBSERVED |
| F-12 | Touch controls (virtual joystick) | IMPORTANT | OBSERVED (hardware unverified) |
| F-13 | Rendering compat branch (gl_compat) | IMPORTANT | OBSERVED |
| F-14 | Player animation blending (AnimationTree) | IMPORTANT | OBSERVED |
| F-15 | Particle effects | NICE-TO-HAVE | INFERRED (particle_material.tres present) |
| F-16 | Secret area (Label3D discovery) | NICE-TO-HAVE | OBSERVED (normal-input route verified) |

---

## 13. OUT OF SCOPE

Items absent from the codebase. These are gaps, not design decisions.

| Feature | Reason | Design stakes |
|---|---|---|
| Win condition / level-complete | `[MISSING]` — no game manager | Player has no session goal |
| Player health / damage | `[MISSING]` — no HP variable | Enemies cannot threaten the player |
| Kill score / enemy count | `[MISSING]` — kills not counted | No compound reward |
| Multiple levels / scene transition | `[MISSING]` — single scene | No progression arc |
| Save / load (coin persistence) | `[MISSING]` — no FileAccess | Coins reset on restart |
| Background music | `[MISSING]` — no music node | Session has no audio atmosphere |
| Pause / options menu | `[MISSING]` | No in-session player controls |
| Main menu / title screen | `[MISSING]` | Game begins immediately |
| Coyote time | `[MISSING]` — not in player.gd | Precision required at every ledge |
| Double jump | `[MISSING]` | Single jump limits vertical exploration |
| Coin total display ("X / 73") | `[MISSING]` | Completion state is invisible |
| Narrative / cutscenes | `[MISSING]` | No motivation for collecting or fighting |

---

## 14. TECHNICAL

**Engine:** Godot 4.7 `[OBSERVED project.godot:18]`  
**Physics:** Jolt Physics 3D `[OBSERVED project.godot:150]`  
**Physics Hz:** 120 `[OBSERVED project.godot:149]`  
**Physics interpolation:** true `[OBSERVED project.godot:151]`  
**Gravity:** 22.0 m/s² (2.24× Earth) `[OBSERVED project.godot:153]`  
**Main scene:** `res://game.tscn` `[OBSERVED project.godot:17]`  
**Scripting:** GDScript, typed declarations (`gdscript/warnings/untyped_declaration=1`) `[OBSERVED project.godot]`  

**Renderer:**
| Mode | Shadows | Notes |
|---|---|---|
| Forward+ (default) | Directional 8192px, PCF5 | MSAA 3D 2×, Aniso 4×, Debanding |
| gl_compatibility | PCF13 (`SHADOW_QUALITY_SOFT_HIGH`) | Energy-split light (sky-only + light-only duplicate) |

`[OBSERVED project.godot:155-165, stage.gd:4-14]`

**Window:** `canvas_items` stretch, `expand` aspect `[OBSERVED project.godot:28-29]`  
**3D assets:** player.glb, enemy.glb; GridMap tiles.tres; collision box.tres/trunk.tres  
**Materials:** player_glow.tres, player_gray.tres, coin_material.tres, tile_material.tres, particle_material.tres  
**Audio:** WAV PCM; SoundJump, SoundShoot (player), SoundWalkLoop, SoundHit (enemy); default_bus_layout.tres  
**Platform:** Desktop (Forward+ confirmed), mobile path (gl_compat + touch UI, hardware unverified)  

**Known issues `[OBSERVED FRICTIONAL.md, CAPTURE.md]`:**
- 7 Texture RID shutdown leaks on every run (not suppressed; root cause unclear)
- Original PCM audio peaks at or near 0 dBFS (true peak +0.5 dBFS measured); gain-adjusted candidate at -2.5 dB exists
- Touch hardware unverified (synthetic event tests only)
- Camera obstruction visible in captures (real limitation; not repaired)

---

## 15. RISKS

| ID | Risk | Category | Status | Mitigation |
|---|---|---|---|---|
| R-01 | No win state — player has no designed session goal | Design | Certain / absent | Define win condition before film narration (see OQ-01) |
| R-02 | 73 coins with no total display or completion event | Design | Certain / absent | Add "X/73" display or explicitly scope as cosmetic |
| R-03 | Enemies pose no threat — no health system | Design | Certain / absent | Either add contact damage or reframe enemies as obstacles in narration |
| R-04 | Touch hardware unverified | Technical | Unknown | Verify on physical device; label synthetic tests honestly in film |
| R-05 | 7 Texture RID shutdown leaks | Technical | Known / persistent | Investigate before production; do not suppress warnings |
| R-06 | PCM audio peaks at 0 dBFS | Technical | Known / measured | Apply -2.5 dB gain candidate (exists); listen and confirm before final mix |
| R-07 | No session persistence (coins reset) | Design | Certain / absent | Document as intentional for demo, or add save |
| R-08 | Camera obstruction in captures | Technical | Known / observed | Document as real limitation; do not repair footage |
| R-09 | AIR_IDLE_DEACCEL=false — no air stopping | Design | Certain / observed | Verify against intended feel; document as deliberate if kept |
| R-10 | Secret area discoverable but not narratively framed | Design | Known | Either add reward/context or label as easter egg |

---

## 16. UI/UX

### Diegetic (in 3D world space)
- **Coin counter — Label3D** `[OBSERVED player.gd:47-51]`  
  `%CoinCount` Label3D attached to player hierarchy; 4 parallax shadow copies (`Parallax`–`Parallax4`) simulate depth. Updated every physics frame. Current count only; no total.
- **Secret area label** `[INFERRED FRICTIONAL.md]`  
  Label3D in stage at approx (17.2, 6, -2.0). Text: "You have found a secret area!" No HUD reference; player discovers by proximity.

### Non-Diegetic (screen-space overlay)
- **Touch controls — CanvasLayer** `[OBSERVED touch_screen_ui.gd]`  
  Visible only on touchscreen. VirtualJoystick for movement; jump/shoot buttons (hardware unverified). Labels tiny at native 4K; film requires labeled detail crop.

### `[MISSING]`
- Pause menu
- Settings / options screen  
- Main menu / title screen  
- HUD health bar (no health system)  
- Game over screen  
- Level complete screen  
- Coin total display ("X / 73")  
- Minimap  

---

## Zelda's Notes

*Silent mode — pushback written here, not spoken.*

**Ghost Center (Failure Mode 1 — present).**  
The session has no goal. There is no win state, no fail state, no reason to collect all 73 coins rather than 2. The player can play indefinitely, collect nothing, or quit immediately. This is acceptable for a teaching demo if labeled explicitly. It is a production problem if the film claims this is a "game." Before narration is written, someone must answer OQ-01: what does success look like for the player?

**Mechanic Mirage (Failure Mode 2 — partial).**  
Enemies cannot harm the player. They patrol, they topple when shot, but the only consequence of ignoring them is a moving obstacle in the path of coin collection. This removes meaningful tension from the shoot mechanic. A player who never shoots still collects all 73 coins. If the teaching goal is "demonstrate RigidBody3D contact detection," the mechanic is complete. If the goal is "create challenge," it is not.

**Scope Concentration.**  
11 of 16 listed features are CORE by any reasonable definition — but this is a recovered build, not a scoped list. The core percentage reflects implementation completeness, not design prioritization. Before planning, answer: which of these features the Walker film must demonstrate, and which are present by inheritance from the upstream demo?

**What the code's structure suggests the vision was `[INFERRED]`:**  
A Godot 4.7 CharacterBody3D movement showcase. The quality of the movement system — camera-relative input, physics-interpolated 120 Hz, variable jump, smooth mesh arc rotation, air factor tuning — is the work of someone who cared about character feel. That level of care is absent from the session structure (no win state, no narrative). The Walker brief confirms it: "establish what it actually implements and verify that behavior." This is a proof of mechanics, not a shipped game.

**Next command:**  
Run `/gdd v1` to fill the missing intent — target player, design pillars, win state, and player fantasy. Or run `/gdd draft` to generate rough drafts of all sections with assumptions flagged for iteration.

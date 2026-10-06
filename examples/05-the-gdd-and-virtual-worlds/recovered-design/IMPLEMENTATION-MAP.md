# Implementation Map — walker-3d-platformer

Recovered by `/gdd reverse --path godot` on 2026-09-27.
One row per discovered feature. Tags: `[OBSERVED]` code does this · `[INFERRED]` code implies this · `[MISSING]` not found.

| Feature ID | Feature Name | Scene | Script | Key path:line | Status | Notes |
|---|---|---|---|---|---|---|
| F-01 | Camera-relative ground movement | `godot/player/player.tscn` | `godot/player/player.gd` | `player.gd:63-115` | OBSERVED | WASD/stick input rotated into camera basis, projected to XZ; ACCEL=14, MAX_SPEED=6 |
| F-02 | Air movement (limited) | `godot/player/player.tscn` | `godot/player/player.gd` | `player.gd:122-133` | OBSERVED | AIR_ACCEL_FACTOR=0.5, AIR_IDLE_DEACCEL=false, capped at MAX_SPEED |
| F-03 | Variable-height jump | `godot/player/player.tscn` | `godot/player/player.gd` | `player.gd:117-119, 135-137` | OBSERVED | JUMP_VELOCITY=12.5; early release ×0.7; single jump only |
| F-04 | Fall / button recovery | `godot/player/player.tscn` | `godot/player/player.gd` | `player.gd:36-43` | OBSERVED | y<-12 OR action "reset_position" → initial_position, velocity=ZERO |
| F-05 | Press-edge shooting | `godot/player/player.tscn` + `godot/player/bullet/bullet.tscn` | `player.gd`, `bullet.gd` | `player.gd:153-165`, `bullet.gd:6` | OBSERVED | Spawns Bullet RigidBody3D at muzzle; BULLET_SPEED=20; enabled flag prevents multi-hit |
| F-06 | Coin collection (Area3D) | `godot/coin/coin.tscn` | `godot/coin/coin.gd` | `coin.gd:7-13` | OBSERVED | One-time contact with Player; taken flag; increments Player.coins |
| F-07 | Enemy floor/wall patrol | `godot/enemy/enemy.tscn` | `godot/enemy/enemy.gd` | `enemy.gd:49-73` | OBSERVED | _ray_floor + _ray_wall in _integrate_forces; ACCEL=5, MAX_SPEED=2, ROT_SPEED=1 |
| F-08 | Enemy death (single bullet) | `godot/enemy/enemy.tscn` | `godot/enemy/enemy.gd` | `enemy.gd:34-47, 77-78` | OBSERVED | dying=true, collision_layer=0, impact+explode anim, queue_free() |
| F-09 | Third-person follow camera | `godot/player/player.tscn` | `godot/player/follow_camera.gd` | `follow_camera.gd:32-91` | OBSERVED | Top-level Camera3D, orbits target, distance/height clamped |
| F-10 | Camera obstruction avoidance | `godot/player/player.tscn` | `godot/player/follow_camera.gd` | `follow_camera.gd:50-79` | OBSERVED | Three raycasts ±25°; autoturn 50°/s; center blocked → pull camera to hit |
| F-11 | Coin counter Label3D | `godot/player/player.tscn` | `godot/player/player.gd` | `player.gd:47-51` | OBSERVED | Session-only int; Label3D + 4 parallax copies for pseudo-3D depth |
| F-12 | Touch controls (virtual joystick) | `godot/touch_screen_ui/touch_screen_ui.tscn` | `touch_screen_ui.gd`, `virtual_joystick.gd` | `touch_screen_ui.gd:4-6`, `virtual_joystick.gd:74-161` | OBSERVED (hw unverified) | CanvasLayer shown only on touchscreen; FIXED joystick → action press/release |
| F-13 | Rendering compat branch | `godot/stage/stage.tscn` | `godot/stage/stage.gd` | `stage.gd:4-14` | OBSERVED | gl_compatibility: PCF13 shadows + energy-split directional light |
| F-14 | Secret area label | `godot/game.tscn` | — | (Label3D in stage) | INFERRED | "You have found a secret area!" at approx world (17.2, 6, -2); reachable by normal inputs per FRICTIONAL.md |
| F-15 | Player animation blending | `godot/player/player.tscn` | `godot/player/player.gd` | `player.gd:168-176` | OBSERVED | AnimationTree: state/run/speed/air_dir/gun blend params driven per frame |
| F-16 | Particle effects | `godot/` | — | `godot/particle_material.tres` | INFERRED | particle_material.tres exists; which node uses it not traced without scene read |
| — | Win condition | — | — | — | MISSING | No game manager, no trigger, no level-complete event |
| — | Player health / death | — | — | — | MISSING | No HP variable, no damage handler, no respawn |
| — | Kill / coin score | — | — | — | MISSING | Coins counted; kills not; no compound score |
| — | Multiple levels / scene transition | — | — | — | MISSING | One scene; no get_tree().change_scene() call observed |
| — | Save / load | — | — | — | MISSING | No FileAccess, no ConfigFile, no AutoLoad storage |
| — | Background music | — | — | — | MISSING | No music node in any script or scene |
| — | Coyote time | — | — | — | MISSING | Not observed in player.gd |
| — | Double jump | — | — | — | MISSING | Not observed; single jump via jumping flag |
| — | Pause menu | — | — | — | MISSING | No pause tree calls observed |

## Asset inventory

| Asset | Type | Path | Maturity |
|---|---|---|---|
| player.glb | 3D model (robot) | `godot/player/player.glb` | L3 (integrated, animated) |
| enemy.glb | 3D model (patrol bot) | `godot/enemy/enemy.glb` | L3 (integrated, animated) |
| player_glow.tres | Material | `godot/player/player_glow.tres` | L2 |
| player_gray.tres | Material | `godot/player/player_gray.tres` | L2 |
| coin_material.tres | Material | `godot/coin/coin_material.tres` | L2 |
| tile_material.tres | Material | `godot/stage/tile_material.tres` | L2 |
| tiles.tres | MeshLibrary (GridMap) | `godot/stage/tiles.tres` | L3 |
| box.tres | CollisionShape | `godot/stage/collision/box.tres` | L3 |
| trunk.tres | CollisionShape | `godot/stage/collision/trunk.tres` | L3 |
| particle_material.tres | ParticlesMaterial | `godot/particle_material.tres` | L1 (present, usage untraced) |
| default_bus_layout.tres | AudioBusLayout | `godot/default_bus_layout.tres` | L2 |
| SoundJump (WAV) | Audio | `godot/player/` (referenced) | L3 |
| SoundShoot (WAV) | Audio | `godot/player/` (referenced) | L3 |
| SoundWalkLoop (WAV) | Audio | `godot/enemy/` (referenced) | L3 |
| SoundHit (WAV) | Audio | `godot/enemy/` (referenced) | L3 |

Maturity: L0=placeholder · L1=present, unintegrated · L2=integrated, unverified · L3=integrated, test-verified · L4=final/shipping

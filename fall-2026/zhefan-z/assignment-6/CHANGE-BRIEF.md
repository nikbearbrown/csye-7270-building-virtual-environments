# CHANGE-BRIEF — Assignment 6: fireball impact and fireball trail

Author: Zhefan Zhang (zhefan-z). Original version, 2026-11-05. Dated revisions go at the end; this text is not edited in place. The Assignment 5 brief is in history at commit `2b68e0a`.

Authorship: the choice of both effects, their look (layers, size, feel), every prediction and every verdict are mine. claude.ai (chat) proposed the setting values from my choices, read the project code with me and compiled this file; where it corrected an answer of mine, the correction is noted. Paths are relative to `walker-magic-zhefan/` (`res://`).

Engine: Godot 4.7.2-stable, Forward+, 2D. Viewport 640×360, stretch `viewport`, integer scale, window 1280×720 (`project.godot:23–29`). The camera is fixed at (320, 180) (`game/main.tscn:93–94`), so on-screen size is 2× the pixel values below. The mage's sprite is 62×69 px, her collision box 14×44 px; a fireball's radius is 4 px.

## Facts from the code

| Fact | Reference |
|---|---|
| A fireball flies at 260 px/s and is removed after 2.0 s without a hit, with no burst | `features/fireball/fireball.gd` `SPEED`, `LIFETIME`, `_physics_process` |
| On hitting a wall, the ground or a wolf, `explode()` instances `burst.tscn` at its position into its own parent, then frees itself; `_spent` makes a second call a no-op | `fireball.gd` `_on_body_entered`, `explode` |
| `burst.tscn` is a Sprite2D (`fx_burst.png`) that frees itself after 0.15 s | `features/fireball/burst.tscn`, `burst.gd` |
| Fireballs are added to the player's parent, `Main` | `features/player/player.gd:109` |
| Casts are at least 0.35 s apart | `features/player/tuning.gd` `CAST_COOLDOWN` |
| A wolf that dies is freed 0.6 s later | `features/wolf/wolf.gd` `DOWN_TIME`, `take_damage` |
| The cave background is a Sprite2D on a CanvasLayer at layer −10; the pit is a dark ColorRect | `game/main.tscn:30–35`, `Level/PitDark` |

## Effect A — fireball impact

### The job

Tells the player where and when a fireball landed: on a wolf (a hit) or on a wall or the ground (a miss). The A2 sprite flash is too brief (0.15 s) to read as an impact. Event: `Fireball.explode()`, called from `_on_body_entered`.

### Intent

- **Timing phases** (at 30 fps): frame 0 a bright white-yellow flash; 0–0.15 s sparks fly out fast in all directions; 0.15–0.45 s sparks slow, cool to red, shrink and vanish; 0.1–0.8 s a small grey puff grows, rises a little and fades. Gone before 0.9 s, so a third cast at the cooldown can land on a clean spot.
- **Contrast**: sparks are additive and near-white at birth, so they read over the dark cave and the black pit. The smoke is mid-grey, lighter than the cave, so it reads over the dark rock; over the lightest ground tiles it may disappear, which is acceptable for the faint last phase.
- **Scale**: sparks reach about one mage height from the impact (45–55 px, about 90–110 px on screen); the flash is the A2 sprite's size; the smoke stays within about half a mage height.
- **Change over life**: sparks go white-yellow → orange → dark red → transparent and shrink to nothing; smoke grows from small to about twice its size while fading.
- **Variation**: random direction over 360°, speed range, size range and a little hue range, so repeats do not look stamped.
- **Layers**: `Flash` (the existing `burst.tscn`, unchanged), `Sparks` (GPUParticles2D), `Smoke` (GPUParticles2D), under one root `Node2D`.

### Settings

Scene `effects/fireball_impact.tscn`. Root `Node2D` named `FireballImpact`, which frees itself 0.9 s after it enters the tree.

| Emitter | Setting | Value |
|---|---|---|
| Node type, both | GPUParticles2D | GPU, because Effect B needs turbulence, which CPUParticles2D lacks; same type for both keeps one pricing method |
| Sparks | `amount`, `one_shot`, `explosiveness`, `lifetime` | 24, true, 1.0, 0.45 s |
| Sparks | emission shape | point |
| Sparks | `direction`, `spread` | (1, 0), 180° |
| Sparks | `initial_velocity_min` / `_max` | 90 / 160 px/s |
| Sparks | `gravity` | (0, 300) |
| Sparks | `damping_min` / `_max` | 40 / 60 |
| Sparks | `scale_min` / `_max`, scale curve | 1.0 / 2.0, 1 → 0 over life |
| Sparks | colour ramp | white-yellow (1, 0.95, 0.7) → orange (1, 0.55, 0.15) → dark red (0.6, 0.1, 0.05) → alpha 0 |
| Sparks | `hue_variation_min` / `_max` | −0.03 / 0.03 |
| Sparks | texture, draw material | `assets/textures/fx/spark.png` (4×4, written by code); CanvasItemMaterial, `blend_mode` Add |
| Smoke | `amount`, `one_shot`, `explosiveness`, `lifetime` | 8, true, 0.9, 0.8 s |
| Smoke | `direction`, `spread`, velocity | (0, −1), 180°, 15 / 35 px/s |
| Smoke | `gravity`, `damping_min` / `_max` | (0, −20), 10 / 20 |
| Smoke | `scale_min` / `_max`, scale curve | 1.0 / 1.5, 1 → 2 over life |
| Smoke | colour ramp | grey (0.45, 0.42, 0.40, 0.55) → transparent |
| Smoke | texture, draw material | `assets/textures/fx/smoke.png` (12×12 soft disc, written by code); normal (Mix) blend |
| Both | `local_coords` | false. The root never moves after it spawns; off also keeps particles where they were born if it did |
| Both | `visibility_rect` | set, `Rect2(-96, -96, 192, 192)`, and checked against an impact at the screen edge |
| Both | `preprocess` | 0 (a burst must start at the impact) |

Wiring: `fireball.gd` instances `fireball_impact.tscn` instead of `burst.tscn` in `explode()`, at the same position and into the same parent. `burst.tscn` stays, as the `Flash` child.

### Observable rules

| # | Rule |
|---|---|
| A1 | One impact instance per `explode()`: on a wolf, a wall or the ground |
| A2 | Never otherwise: not on scene load, not on a cast, not when a fireball times out after 2.0 s, not twice for one fireball (`_spent`) |
| A3 | At the fireball's `global_position` at impact |
| A4 | Retrigger: **overlap**. A second impact while the first is alive spawns a second instance; the first keeps running. In steady casting at the cooldown at most 3 are alive (0.9 / 0.35 → 3); the bound is 6, all fireballs that can be alive at once (2.0 / 0.35 → 6) landing within one 0.9 s window |
| A5 | Freed parent: the fireball is freed on the same event; the impact is a child of `Main`, so it survives. A wolf freed 0.6 s after its last hit is not its parent |
| A6 | Each instance frees itself 0.9 s after it spawns |

## Effect B — fireball trail

### The job

A **trail**: it shows the fireball's path and speed, so the player can read where a shot is heading. Condition: the fireball exists and has not exploded. Script: `fireball.gd` (`_ready` to `explode()` or the 2.0 s timeout).

Feature Effect A doesn't use: **turbulence**, plus a **sphere emission shape** (A emits from a point).

### Intent

- **Timing**: starts on the fireball's first frame; a steady short flame behind it while it flies; when the fireball ends, the trail stops emitting and its last particles fade within 0.3 s where they are.
- **Contrast**: additive and bright like the sparks; reads over the dark cave.
- **Scale**: about 60–80 px long at 260 px/s (0.3 s), about one and a half fireball sprites wide at the head, thinning to nothing.
- **Change over life**: same warm ramp as the sparks, scale 1 → 0, so it thins toward the tail.
- **Variation**: turbulence makes the flame flicker and drift instead of a straight line; random scale.
- **Layer**: one emitter.

### Settings

Scene `effects/fireball_trail.tscn`, a GPUParticles2D, instanced as a child of the fireball.

| Setting | Value |
|---|---|
| `amount`, `one_shot`, `explosiveness`, `lifetime` | 32, false, 0, 0.3 s |
| emission shape | sphere, radius 3 px |
| `direction`, `spread`, velocity | (−1, 0) in world space, 30°, 10 / 20 px/s |
| `gravity` | (0, −30) (flames rise) |
| turbulence | `turbulence_enabled` true, `turbulence_noise_strength` 1.0, `turbulence_noise_scale` 2.0, `turbulence_influence_min` / `_max` 0.1 / 0.2 |
| `scale_min` / `_max`, scale curve | 1.0 / 1.5, 1 → 0 |
| colour ramp | same as Sparks |
| texture, draw material | `assets/textures/fx/spark.png`; CanvasItemMaterial, Add |
| `local_coords` | **false**: particles stay where they were emitted, which is what draws a trail; on, the trail would move with the fireball and draw no trail |
| `visibility_rect` | set, `Rect2(-128, -48, 256, 96)` |
| `preprocess` | 0: a new fireball must not start with a ready-made trail at the staff |

Wiring: when the fireball explodes or times out, the trail is moved to the fireball's parent with its global transform kept, `emitting` set to false, and freed 0.3 s later. No other change to `fireball.gd`.

### Observable rules

| # | Rule |
|---|---|
| B1 | Emitting from the fireball's first frame |
| B2 | When the fireball explodes or times out: still in the tree, no longer emitting, child of the fireball's former parent, freed about 0.3 s later |
| B3 | While the tree is paused: emitting state unchanged and the node not processing; on screen the trail freezes and resumes |
| B4 | While hidden: nothing drawn; `emitting` stays true. Whether the GPU keeps simulating while hidden is unconfirmed; checked in the running game |
| B5 | No trail exists before a cast or on scene load |

## Boundaries

Unchanged: collision, movement, input, the player and wolf state machines and every timing in `tuning.gd` and `fireball.gd`, damage, the existing tests and their expectations, my Assignment 5 shaders in `shaders/`, the A3 prop room and every other object. The only gameplay-script change is in `fireball.gd`: which scene `explode()` instances, and stopping and detaching the trail. Presentation code reads game state and never writes it.

## Evidence split

| Rule | Check |
|---|---|
| Every setting above | headless configuration test per effect, reading the loaded resources |
| A1–A6, B1–B3, B5 | headless state tests driven by real casts and real collisions |
| B4 | headless for node state; my eyes in the running game for what is drawn |
| The look (timing, contrast, scale, change over life, variation) | frame strips (fixture) read by Claude, then my verdict in the running game at 1280×720 |
| `visibility_rect` | my eyes: an impact against the left and right walls at the screen edges |

## Frame strips

Preview background: the real cave background and ground from `game/main.tscn`, at in-game camera scale, with a wolf-free stretch next to the pit so both the darkest (pit) and lightest (ground cap) art are in frame.

- **Effect A** (`previews/fireball_impact_preview.tscn`): trigger at frame 10; with its retrigger export on, a second impact 6 frames later (0.2 s, inside the first's lifetime). Read frames 10, 12, 15, 20, 30, 50 at 30 fps: 10 flash and first sparks; 12 sparks spreading, still bright; 15 flash gone, sparks at about half their distance; 20 sparks orange-red, smoke visible; 30 only faint smoke; 50 empty.
- **Effect B** (`previews/fireball_trail_preview.tscn`): a fireball crossing the frame from frame 10, hitting a wall at frame 40. Read 10 (start: one or two particles), 12, 20 and 30 (steady trail), 40 (impact), 45 and 50 (trail fading where it was, then gone).
- Fixed seed: GPUParticles2D has `use_fixed_seed` and `seed` in 4.7; on for the preview instances only, never in the effect scenes.

## Predicted failures

| # | Failure | What it would look like | Check |
|---|---|---|---|
| F1 | Godot 3 names in the scene file (`ParticlesMaterial`, `initial_velocity`, `scale`) | fires, but at default speed and size | configuration test reads each named property; the Godot 3 name mutation |
| F2 | Particles put inside `burst.tscn` | sparks vanish after 0.15 s with the sprite | state test: emitters alive at 0.3 s; strip frame 20 |
| F3 | Trail left as a fireball child when it is freed | trail vanishes instantly on impact | state test B2; strip frames 45–50 |
| F4 | `local_coords` on for the trail | no trail, a blob that follows the fireball | configuration test; strip frames 20–30 |
| F5 | Add blend without a CanvasItemMaterial | sparks look flat, not glowing | configuration test reads the material and blend mode; strip |
| F6 | Smoke too dark | invisible over the cave | strip frame 20 and my eyes over the darkest stretch |
| F7 | `visibility_rect` too small | sparks cut off near the screen edge | my eyes at the walls |

## Price predictions and budget

Both effects are GPU nodes, so their budgets are compared on GPU time (Visual Profiler, Debugger panel, RTX 5060 Laptop GPU). Headless CPU price is recorded too, against an empty-scene control.

| Effect | Peak | Predicted headless CPU price | Predicted GPU time | Budget (GPU time) |
|---|---|---|---|---|
| A | 6 bursts × 32 = 192 particles | within the spread of the game scene with effects off: near zero, because headless runs no GPU particle process | under 0.1 ms | 0.5 ms |
| B | 6 fireballs × 32 = 192, plus up to 6 fading detached trails | near zero, same reason | under 0.1 ms | 0.3 ms |

## Short answers, before building

*(Mine; claude.ai corrected 1, 3, 5 and 6 to match this brief, noted below.)*

1. **Node type and what it lacks.** Both effects are GPUParticles2D. CPUParticles2D lacks the turbulence Effect B depends on (also sub-emitters, attractors, collision and trails), and cannot use a particles-type shader. *(Corrected: my first answer named custom particle shaders and transform feedback but not turbulence, the feature this brief uses.)*
2. **`local_coords` off and a moving parent.** Particles already emitted stay where they are in the world; new ones emit from the emitter's current position.
3. **Bursts alive and peak.** At most 3 in steady casting (0.9 s life, 0.35 s cooldown), 6 at the bound; peak 6 × 32 = 192 particles. *(Corrected: my first answer used a generic 4 × 64.)*
4. **Headless price and FPS.** A headless run uses a dummy renderer and runs no GPU particle process, so a GPU effect's headless CPU price is near zero. With vsync on, FPS reads my display's refresh rate (144 Hz or more) with the effect off and on, unless a frame misses its deadline.
5. **Effect B on its first frame, paused, hidden.** On a new fireball's first frame the trail is one or two particles at the fireball. With `preprocess`, it would start with a full-length trail already sitting at the spawn point, behind a fireball that has not moved yet, which is wrong for a trail; so `preprocess` is 0. Paused: the trail freezes and resumes. Hidden: nothing is drawn; on showing it again, particles that expired meanwhile are gone. *(Corrected: my first answer treated `preprocess` as an improvement here.)*
6. **Emission, process, draw.** Emission: `amount`, `one_shot`, `explosiveness`, `lifetime`, `preprocess`, `emitting`, the emission shape. Process: direction, spread, initial velocity, gravity, damping, turbulence, the scale curve, **the colour ramp** (colour over life is computed in the process shader), hue variation, `local_coords`. Draw: the texture, the CanvasItemMaterial and its blend mode, `visibility_rect`. *(Corrected: I had put the colour ramp under draw.)*

## Revisions

### 2026-11-05 — the A2 flash stays outside the impact

Found while reviewing the CLAUDE.md draft: `tests/test_cast.gd:55–56` counts `Main` children whose names start with `Burst` and expects one after a ground hit (`:115–118`). Putting `burst.tscn` inside `FireballImpact` as `Flash` would fail that earlier suite, which may not be edited.

Revision: `explode()` keeps instancing `burst.tscn` into `Main` exactly as before, and also instances `effects/fireball_impact.tscn` at the same `global_position` into the same parent. `FireballImpact` holds only `Sparks` and `Smoke`. On screen the layers are unchanged: the A2 flash for 0.15 s, the sparks and the smoke. Rule A1 counts `FireballImpact` instances; the `Burst` count stays as `test_cast` expects.

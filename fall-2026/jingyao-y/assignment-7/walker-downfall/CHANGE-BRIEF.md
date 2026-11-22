# CHANGE-BRIEF.md — Assignment 6: particle effects

The Assignment 5 brief (burning-bottle fire shader) is at tag `a5`,
`fall-2026/jingyao-y/assignment-5/walker-downfall/CHANGE-BRIEF.md`. This file
replaces it. Written by the agent (Claude Code) on 2026-11-07, before any build
prompt; the user chose the two effects and where the work lives. Dated
revisions go at the end; nothing above them is edited afterwards.

Pinned engine: Godot 4.7.2-stable (official), Forward+, D3D12 on Windows
(`project.godot:16`, `project.godot:27`). Every name below was checked against
that build's ClassDB on 2026-11-07 (scratch probe; the CLAUDE.md step records it).

## What exists today (audit, 2026-11-07)

Every particle system in the game is a `CPUParticles3D` made in code with
`.new()`: the Sami fire pit (`entities/fire_pit.gd:74`), shower spray, trace
motes, boss bursts (`game/boss_vfx.gd:636`), weather and vault grit. None is a
scene file. The hit "spark" on a landed melee blow is not a particle system at
all: `CombatVfx.spawn(..., "spark")` draws a few unlit meshes
(`game/combat_vfx.gd`). So:

- **Effect A extends nothing that fits**: it is new, a GPU particle scene added
  beside the existing mesh spark (the mesh spark stays; see Boundaries).
- **Effect B rebuilds an existing effect**: the fire pit's two code-made CPU
  emitters become one GPU scene, because the brief's feature (turbulence) and
  its feedback loop (`amount_ratio`) do not exist on `CPUParticles3D` in 4.7.

---

## Effect A — `hit_spark` (one-shot, on a landed melee hit)

### The job

- **What it tells the player:** "that blow connected, here." In a crowd the
  operator's swing animation plays whether or not it hits; damage numbers rise
  late and stack. The burst is the instant, positional confirmation of contact,
  read in the corner of the eye while the player watches something else.
- **Event:** an operator's melee hit lands on an enemy. It is raised in
  `entities/player.gd` at the three places that today call
  `CombatVfx.spawn(game, <target>.global_position, direction, "spark"|"amiya_spark")`:
  the basic combo hit (`player.gd:914`), Lappland's cross cut onto a second
  target (`player.gd:962`) and Amiya's combo cut (`player.gd:1768`). The
  position is the struck enemy's `global_position` at that moment.
- **Node type:** `GPUParticles3D` ×3 under one `Node3D` root. GPU because the
  game is 3D on Forward+ with a real GPU (RTX 4060 per memory of the D3D12
  switch), the burst repeats many times a second in fights, and the price
  question of this assignment is about GPU nodes. The look needs nothing that
  only GPU has; that is Effect B's job.

### Intent

- **Timing phases** (at 30 fps capture; 1 frame = 33 ms):
  1. *Impact, frame 0 (0–0.03 s):* a single white-hot flash the size of the
     operator's head-and-shoulders, the brightest thing on screen for one frame.
  2. *Throw, 0.03–0.12 s:* 10–18 sparks fly outward in all directions fast,
     reaching about half the operator's height from the hit point; the flash
     shrinks and is gone by 0.1 s.
  3. *Settle, 0.12–0.35 s:* damping brakes the sparks hard; they turn orange then
     deep red, droop under gravity, shrink and vanish. A dark puff behind them
     expands slightly and fades.
  4. *Clear, by 0.45 s:* nothing left. A follow-up blow (Amiya's cuts come
     0.08 s apart) layers a fresh flash on top of a settling burst, which is
     what "overlap" should look like.
- **Contrast:** the darkest field ground is the city street, measured in A5 at
  RGB8 (58,58,67) under the game's normal look; the lightest is Sami snow
  (near-white). Additive sparks carry the dark city by value alone. On snow
  additive light has almost nothing to add, so the burst has a third,
  alpha-blended **dark** layer (the puff) that reads as a smudge on white.
  Value contrast, not hue, is the target in both.
- **Scale against the character:** at the default orthographic size 24 on a
  1280×720 window (`game/game_manager.gd:21`, `project.godot:20-21`) one world
  unit is 30 px. Flash quad 0.9 units (~27 px), roughly the upper half of an
  operator; sparks travel 0.4–0.8 units (12–24 px), about half the operator's
  height; spark quads 0.12 units (~4 px, about two of the game's 1/15-unit
  texels). The operator's measured height in
  pixels is read off strip r0 and recorded in TUNING.md.
- **Change over life:** colour ramp white → orange → transparent red on the
  sparks; scale curve 1 → 0 on sparks; flash shrinks 1 → 0.3 while fading;
  puff grows 0.6 → 1.4 while fading. Nothing fades in alpha alone.
- **Variation:** spread 180° (full sphere), speed 3–6, size 0.6–1.2×, lifetime
  randomness 0.4, hue variation ±0.03, puff random rotation 0–360°. The
  scene's `use_fixed_seed` stays **off** so repeated hits differ; only preview
  instances turn it on.
- **Layering:**

  | Emitter | Job | Blend |
  |---|---|---|
  | `Flash` | the impact frame: one big soft white particle | additive |
  | `Sparks` | the direction-less spray that says "contact" | additive |
  | `Puff` | the dark smudge that keeps the burst legible on snow | alpha (mix) |

### Settings (each one is read back by `tests/test_hit_spark_config.gd`)

Scene `res://effects/hit_spark.tscn`, root `HitSpark` (`Node3D`) with a script
that only restarts its children and frees the root when all three have finished
(no settings in code). All three emitters: `emitting = false` in the scene,
`one_shot = true`, `explosiveness = 1.0`, `local_coords = false`,
`fixed_fps = 0` (follow the render rate), `interpolate = true`,
`use_fixed_seed = false`, `preprocess = 0.0`,
`process_material` a `ParticleProcessMaterial` with `particle_flag_disable_z = false`.
Draw for all three: `draw_pass_1` a `QuadMesh` whose material is a
`StandardMaterial3D` with `shading_mode = UNSHADED`,
`billboard_mode = BILLBOARD_PARTICLES`, `vertex_color_use_as_albedo = true`,
`transparency = TRANSPARENCY_ALPHA`, `disable_fog = true`,
`albedo_texture` a `GradientTexture2D` (radial fill, white centre to
transparent edge, 32×32) written in the scene, so no sourced texture.

| Setting | Flash | Sparks | Puff |
|---|---|---|---|
| amount | 1 | 14 | 4 |
| lifetime (s) | 0.10 | 0.35 | 0.45 |
| randomness (lifetime) | 0.0 | 0.4 | 0.2 |
| emission_shape | POINT | SPHERE r 0.10 | SPHERE r 0.15 |
| direction / spread | (0,1,0) / 0° | (0,1,0) / 180° | (0,1,0) / 180° |
| initial_velocity_min–max | 0–0 | 3.0–6.0 | 0.4–0.9 |
| gravity | (0,0,0) | (0,−9.8,0) | (0,0.6,0) |
| damping_min–max | 0–0 | 6.0–10.0 | 1.0–1.0 |
| scale_min–max | 1.0–1.0 | 0.6–1.2 | 0.8–1.2 |
| scale_curve (t:value) | 0:1.0 → 1:0.3 | 0:1.0 → 1:0.0 | 0:0.6 → 1:1.4 |
| color_ramp (t: RGBA) | 0:(1,1,1,1) → 1:(1,0.85,0.5,0) | 0:(1,1,0.9,1) → 0.4:(1,0.6,0.15,1) → 1:(0.6,0.1,0.02,0) | 0:(0.16,0.15,0.18,0.55) → 1:(0.16,0.15,0.18,0) |
| hue_variation_min–max | 0–0 | −0.03–0.03 | 0–0 |
| angle_min–max (°) | 0–0 | 0–0 | 0–360 |
| QuadMesh size | 0.9×0.9 | 0.12×0.12 | 0.5×0.5 |
| blend_mode | BLEND_MODE_ADD | BLEND_MODE_ADD | BLEND_MODE_MIX |
| visibility_aabb (set, not generated) | (−1,−1,−1, 2,2,2) | (−2,−2,−2, 4,4,4) | (−1.5,−1,−1.5, 3,3,3) |

`visibility_aabb` is set by hand from the farthest a spark can get: 6 units/s
with damping 6 stops within about 0.6 units of the emission sphere, so ±2 has
margin. It is checked against the strips (no clipping) and at the screen edge in
play.

`local_coords = false`: the burst is parented to the world (the `GameManager`
node), never to the enemy; once a spark is out it belongs to the world.

### Observable rules

| # | Rule |
|---|---|
| A1 | Fires once per landed melee hit (the three call sites above), at the struck enemy's `global_position` at that instant (tolerance 0.01 units). Never otherwise: not on scene load, not on a swing that misses, not on enemy-to-player hits, not on ranged/projectile hits. |
| A2 | Retrigger rule **overlap**: every landed hit instances a new `HitSpark` under the `GameManager`; an earlier burst is never restarted or cut off. Two hits 0.1 s apart (inside the 0.45 s life) leave **two** `HitSpark` nodes alive, both emitting. Expected peak in normal play: 6 alive (Amiya's 3-cut combo 0.08 s apart, the next swing, Lappland's cross onto a second target); priced at 8. |
| A3 | Each `HitSpark` frees itself after its emitters finish (≤ 0.45 s + one frame at any fixed rate); none accumulate. |
| A4 | Freed parent: if the hit kills the enemy (`queue_free()` on the same call, `entities/enemy.gd:1509`), the burst still plays in full, because it is not a child of the enemy. |
| A5 | Presentation only: the hit's damage, hitstop, aggro, charge and every existing test expectation are unchanged. |

### Evidence split

| Rule | How it is checked |
|---|---|
| A1 | Headless state test (`tests/test_hit_spark_state.gd`, 60 fps) drives real melee attacks on a real enemy through the game loop and real input (left mouse on the enemy), counts `HitSpark` nodes per landed hit (via the enemy's health drop) and compares positions; one swing aimed at empty ground spawns none; the first 30 frames after the field loads spawn none. On screen: the user in play. |
| A2 | Same test: two landed hits inside 0.45 s, assert two live `HitSpark`s, neither restarted. Strip: the preview's retrigger export fires a second burst at frame 16. |
| A3 | Same test: node count returns to 0 within 0.5 s. |
| A4 | Same test: a 1-HP enemy dies on the hit; the `HitSpark` survives and finishes. |
| A5 | Every existing suite before and after (counts in TEST-REPORT.md). |
| Look | Strips (fixture captures) and the user's runtime verdict only. |

### Frame strip (Effect A)

Preview `res://previews/hit_spark_preview.tscn`: the real game loaded headed with
a fixed map seed into the city region (darkest ground), camera at the game's
default size and pitch, an enemy stand-in at the centre, the burst fired at the
enemy's position at frame 10, and (export `retrigger`, on for the strip) again
at frame 16. A second variant over Sami snow is captured for the light-ground
check. `use_fixed_seed = true` on the preview instance only.

Capture at 30 fps: `--write-movie <abs>/captures/hit_spark/r0/frame.png --fixed-fps 30 --quit-after 60`.
Frames to read: **10, 12, 15, 20, 30, 50**.

| Frame | Δt | Prediction |
|---|---|---|
| 10 | 0 | the trigger frame; if the GPU emits one frame late, nothing yet (recorded once) |
| 12 | 0.067 s | flash large and white, sparks a tight bright ring ~0.3 units out |
| 15 | 0.167 s | flash gone; sparks ~0.6 units out, orange, slowing; puff a grey smudge; the frame-16 second burst not yet |
| 20 | 0.333 s | first burst: a few dim red specks, puff faint; second burst at its throw phase |
| 30 | 0.667 s | empty |
| 50 | 1.333 s | empty; the `HitSpark` nodes freed |

---

## Effect B — `fire_pit_flames` (a feedback loop on the fuel left)

### The job

- **What it tells the player:** "this fire is warm, and this is how much fuel
  it has left." In Sami the cold meter rises unless the player stands in a lit
  fire's 4.5-unit radius (`FeatureCatalog.FIRE_RADIUS`); fuel burns down
  (at most 300 s, `FeatureCatalog.FIRE_MAX`) and the boss's hammer knocks fuel
  off (`entities/boss.gd:1728`). Big flames = plenty; a few licks = feed it now;
  none = cold.
- **Job:** a **feedback loop** that follows a game value.
- **Condition and value:** `FirePit.burn_left` (`entities/fire_pit.gd:17`);
  lit while `burn_left > 0` (`lit()`, `fire_pit.gd:105`). It rises in
  `feed()` (fuel, `game/gm_features.gd:227`; boss arena start; the camp rest
  fire is fed to 300 at load, `game/gm_route.gd:225`) and falls in `burn()`,
  called from `GameManager._physics_process` only while
  `simulation_active()` (`game/game_manager.gd:848-853`).
- **Feature Effect A doesn't use:** **turbulence** (`turbulence_enabled`, GPU
  only) and a value-driven **`amount_ratio`** (GPU only in 4.7:
  `CPUParticles3D` has no `amount_ratio`). Also `preprocess`, and continuous
  (non-one-shot) emission.
- **Node type:** `GPUParticles3D` ×2 under one `Node3D` root, for the two
  features above.

### Intent

- **Timing phases:** *lighting* — fire fed from cold: flames are there at full
  size on the next frame (preprocess), no slow fill-in, because the moment of
  lighting matters to a freezing player. *Steady* — flames lick up 0.6–0.9 units
  and waver sideways (turbulence), embers drift higher and wander for ~2 s.
  *Dwindling* — as fuel drops below 120 s the flame count thins in proportion,
  down to 30% at the last second. *Out* — emission stops; the flames already
  alive finish their 0.8 s and embers their 2.2 s, so it dies, it doesn't blink
  off.
- **Contrast:** Sami snow is the lightest ground in the game; the fire's own
  warm ground glow (the existing additive `Glow` halo, kept) darkens nothing, so
  the flames must read by saturation and brightness against near-white. The
  flame core ramp goes to alpha 0.9 orange; the darkest ground near fires is the
  stone ring and charred logs of the pit model, against which the additive
  flames read strongly. Judged in play on both.
- **Scale against the character:** flames 0.6–0.9 units tall (about half an
  operator), within the 1.1-unit stone ring; embers up to ~2 units (above the
  operator's head). The fire's warm radius (4.5 units) is shown by the existing
  ground glow, not by particles.
- **Change over life:** colour ramp transparent yellow → orange (alpha 0.9) at
  30% life → transparent dark red; scale curve 0.6 → 1.0 (at 30%) → 0.2.
- **Variation:** emission sphere, spread 15°, speed range, lifetime
  randomness 0.3, turbulence noise; the two pits on a floor differ because the
  scene seed is not fixed.
- **Layering:**

  | Emitter | Job | Blend |
  |---|---|---|
  | `Flames` | the body of the fire; its count is the fuel gauge | additive |
  | `Embers` | sparks rising and wandering: "warm air here" | additive |

### Settings (read back by `tests/test_fire_pit_flames_config.gd`)

Scene `res://effects/fire_pit_flames.tscn`, root `FirePitFlames` (`Node3D`), no
script. Both emitters: `one_shot = false`, `explosiveness = 0.0`,
`emitting = false` in the scene (the pit turns it on), `local_coords = false`,
`use_fixed_seed = false`, `amount_ratio = 1.0` in the scene,
`process_material` a `ParticleProcessMaterial` with
`emission_shape = SPHERE`, `direction = (0,1,0)`, `spread = 15`,
`gravity = (0,0,0)`, `turbulence_enabled = true`. Draw: `QuadMesh` with a
`StandardMaterial3D` (`UNSHADED`, `BILLBOARD_PARTICLES`,
`vertex_color_use_as_albedo = true`, `TRANSPARENCY_ALPHA`, `BLEND_MODE_ADD`,
`disable_fog = true`) and the same code-free radial `GradientTexture2D` as A.

| Setting | Flames | Embers |
|---|---|---|
| amount | 24 | 10 |
| lifetime (s) | 0.8 | 2.2 |
| randomness | 0.3 | 0.3 |
| preprocess (s) | 0.8 | 2.2 |
| position (local, y) | 0.2 | 0.35 |
| emission_sphere_radius | 0.18 | 0.25 |
| initial_velocity_min–max | 0.5–1.1 | 0.4–0.9 |
| damping_min–max | 0–0 | 0.2–0.2 |
| turbulence_noise_strength | 1.0 | 1.0 |
| turbulence_noise_scale | 2.5 | 4.0 |
| turbulence_influence_min–max | 0.05–0.12 | 0.15–0.30 |
| scale_min–max | 0.8–1.2 | 0.7–1.3 |
| scale_curve | 0:0.6 → 0.3:1.0 → 1:0.2 | 0:1.0 → 1:0.0 |
| color_ramp | 0:(1,0.85,0.4,0) → 0.3:(1,0.6,0.2,0.9) → 1:(0.8,0.2,0.05,0) | 0:(1,0.7,0.3,0) → 0.3:(1,0.5,0.15,0.9) → 1:(0.6,0.15,0.05,0) |
| QuadMesh size | 0.30×0.30 | 0.05×0.05 |
| visibility_aabb (set) | (−0.6,−0.2,−0.6, 1.2,2.0,1.2) | (−1.5,−0.2,−1.5, 3,4,3) |

The colours, sizes and speeds start from today's CPU fire (`fire_pit.gd:38-42`),
so the first strip is "the same fire on the GPU", and tuning starts from there.

**Feedback mapping** (in `FirePit`, presentation only, reads `burn_left`):

```
emitting     = burn_left > 0
amount_ratio = 0.3 + 0.7 * clamp(burn_left / 120.0, 0.0, 1.0)   (both emitters)
```

`burn_left` 0–300 s; ≥ 120 s → 1.0 (24 flames); 60 s → 0.65; 1 s → 0.306
(about 7 flames). `amount` is never written at run time.

### Observable rules

| # | Rule |
|---|---|
| B1 | Starts when the condition begins: the physics frame `burn_left` goes from 0 to > 0, both emitters have `emitting = true`, and thanks to preprocess the first drawn frame already shows a full fire. |
| B2 | Stops when it ends: the frame `burn_left` reaches 0, `emitting = false`; live particles finish (≤ 2.2 s), no new ones. |
| B3 | Feedback: `amount_ratio` equals the mapping above (±1e-4) after every change of `burn_left`, by feeding, burning or the boss's hammer; `amount` stays 24 / 10. |
| B4 | Tree paused (`get_tree().paused = true`): fuel does not burn (physics stops), `emitting` and `amount_ratio` unchanged; the GPU nodes inherit pause and freeze in place (Godot sets their speed scale to 0 on pause). Game menus do **not** pause the tree in this game: they stop `simulation_active()`, so fuel stops burning while the flames keep moving at a constant ratio. Both are asserted. |
| B5 | Hidden (`visible = false` on the pit or the effect root): nothing is drawn, but `emitting` and `amount_ratio` keep following `burn_left`; shown again, the fire is there at the current ratio. |
| B6 | Scene load: a fire already lit when its floor loads (the camp rest fire, the boss arena's first fire) has `emitting = true` from its first frame and, with preprocess, looks steady on the first drawn frame, not empty. |
| B7 | Presentation only: `burn_left`, warmth, cold and every existing expectation unchanged. |

### Evidence split

| Rule | How |
|---|---|
| B1–B3 | Headless state test (`tests/test_fire_pit_flames_state.gd`, 60 fps) on a real Sami floor: real fuel fed through the real E-interaction path, burning through the real physics loop, values set at least two ways (feed, burn), asserting `amount_ratio` and that `amount` never changes. |
| B4 | Same test, pausing the tree and opening a real menu modal. Freezing *on screen* is the user's check. |
| B5 | Same test (state); on screen the user's check. |
| B6 | Same test on the camp floor (state). First frames on screen: the user's check ("Scene load"). |
| B7 | Existing suites before and after. |
| Look | Strips (fixtures) and the user in play. |

### Frame strip (Effect B)

Preview `res://previews/fire_pit_flames_preview.tscn`: a real Sami floor with a
fixed seed, camera at default size, one `FirePit` in view. At frame 10 it is fed
120 s (ratio 1.0); at frame 55 `burn_left` is set to 24 s (ratio 0.44); at
frame 100 to 0 (out). `use_fixed_seed = true` on the preview's emitters.
Capture `--fixed-fps 30 --quit-after 180`. Frames to read:
**10, 12, 40, 54, 70, 99, 105, 130, 175**.

| Frame | Prediction |
|---|---|
| 10 | lit on this frame; preprocess means a full fire (or, if the GPU lags a frame, nothing yet, then full at 11) |
| 12, 40, 54 | steady: ~24 flame quads stacked into an orange cone ~0.8 units tall, wavering; ~10 embers spread to ~2 units |
| 70 | thinner: about 10–11 flames, same height; fewer embers |
| 99 | same as 70 |
| 105 | flames thinning out (no new ones), embers still rising |
| 130 | no flames; a few embers high up |
| 175 | empty above the pit (the `Glow` halo already off since frame 100) |

---

## Predicted failures (whole brief)

| # | Failure | Check that catches it |
|---|---|---|
| F1 | Godot 3 names in the scene (`ParticlesMaterial`, `initial_velocity`, `scale`, `scale_random`) leave settings at defaults; effect fires and looks default. **Caveat found in the audit:** 4.7's ClassDB still lists `initial_velocity` and `scale` on `ParticleProcessMaterial` (compatibility properties), so that mutation may load silently *and* map onto the new pair. | Config tests read every value back; the Step 2 mutation records whether the renamed property is translated. |
| F2 | 3D draw material missing `vertex_color_use_as_albedo` (ramp invisible), `TRANSPARENCY_ALPHA` (no fade), or `BILLBOARD_PARTICLES` (edge-on quads) | Config tests assert all three on every emitter; strip r0 would show white squares. |
| F3 | Dropped retrigger: one shared one-shot node and `emitting = true` while still emitting silently drops the second hit | Overlap design; state test A2 (two hits, two nodes). |
| F4 | Popping feedback loop: writing `amount` restarts the buffer | State test B3 asserts `amount` constant and `amount_ratio` moving; strip frame 54→70 must show no gap. |
| F5 | Freed parent: burst parented to the enemy dies with it | State test A4 with a 1-HP enemy. |
| F6 | Visibility AABB too small: sparks or embers clipped at screen edge | Strips; the user's edge-of-screen check. |
| F7 | No preprocess: camp fire starts empty on every floor load | Config test (preprocess values); B6 state; the user's scene-load check. |
| F8 | Cost script measures itself (same number for every case) | Empty-scene control in `tests/cost_effects.gd`. |

## Price predictions and budget

Peak particle counts: A = 8 bursts × (1 + 14 + 4) = **152**; B = one pit at
ratio 1.0 = **34** (a floor has at most 3–4 pits, ≤ 136; priced for one and for
four).

| | Headless CPU (mean ms/frame over control) | GPU time (Visual Profiler, RTX 4060, 1280×720) | Budget | Compared on |
|---|---|---|---|---|
| A at 8 bursts | +0.02 ms (node bookkeeping only; the dummy renderer runs no particle process) | +0.05 ms | **0.25 ms GPU** | GPU time |
| B, one pit / four pits | +0.005 / +0.02 ms | +0.02 / +0.06 ms | **0.15 ms GPU** for four pits | GPU time |

Both are GPU nodes, so the headless number is expected to sit inside the
control's spread and is reported but not judged against the budget.

## Answers

1. **Node types and missing features.** Both effects use `GPUParticles3D`
   (4.7.2). Checked in ClassDB: it has `amount_ratio`, `preprocess`,
   `use_fixed_seed`/`seed`, `visibility_aabb`, `local_coords`, trails;
   `ParticleProcessMaterial` has turbulence, damping, `scale_curve`,
   `color_ramp`, `alpha_curve`, hue variation. Nothing this brief names is
   missing. `CPUParticles3D` would lack `amount_ratio` and turbulence, which is
   why B moves to GPU.
2. **`local_coords = false`, parent moves after the event.** Effect A's root is
   a child of the `GameManager` (the world) placed at the hit point; it never
   moves. If the struck enemy keeps walking, the burst stays where the blow
   landed. If the world root itself moved, particles already emitted would stay
   in world space and only new ones (none — it is one-shot) would follow.
3. **Bursts alive at once.** Overlap, 0.45 s life. Expected peak 6 in play,
   priced at 8 → 152 particles.
4. **Headless price of a GPU effect.** Near zero above the control: headless
   uses a dummy renderer, so the particle process shader never runs and nothing
   is drawn; only node `_process` bookkeeping is on the CPU. With vsync on, FPS
   reads the display refresh rate both with the effect off and on, because the
   frame is far under budget either way; only GPU time (or FPS with vsync off)
   can show the difference.
5. **Effect B, first frame / paused / hidden.** With preprocess: a lit pit shows
   a full fire on its first drawn frame. Without: empty, filling over 0.8 s
   (flames) and 2.2 s (embers), on every floor load. Tree paused: frozen in
   place, still drawn. Hidden: not drawn; state keeps following `burn_left`.
6. **Emission / process / draw.**
   *Emission:* `amount`, `amount_ratio`, `one_shot`, `explosiveness`,
   `lifetime`, `randomness`, `preprocess`, `emitting`, `emission_shape` and
   its radius (the shape lives on the process material in 4.x but decides where
   particles appear). *Process:* direction, spread, initial velocity, gravity,
   damping, turbulence, `scale_min/max`, `scale_curve`, `color_ramp`, hue
   variation, angle, `local_coords`. *Draw:* `draw_pass_1` QuadMesh and its
   size, the `StandardMaterial3D` (unshaded, billboard particles, vertex colour
   as albedo, transparency, blend mode, fog), the gradient texture, and
   `visibility_aabb` (culling of the draw).

## Boundaries

Unchanged: collision, movement, input, the enemy and player state machines and
their timings, damage, hitstop, aggro, charge, `burn_left` and every rule that
reads it (warmth, cold, fuel values), existing test expectations, the A5
shaders in `shaders/` (only `shaders/particles_generated.gdshader` may be added
in Step 6), every other object, and the source texture files. The existing mesh
`CombatVfx` spark stays as it is; the fire pit's `Glow` halo and model stay.
Presentation code reads game state; it never writes it.

## Revisions

- **2026-11-07 r1 (agent, after the Step 1 review and `tests/a6_probe_headless.gd`).**
  (a) A4's reference `entities/enemy.gd:1509` should read `:1501` (`queue_free()`;
  `died` is emitted at `:1500`). (b) Headless, a one-shot `GPUParticles3D` reads
  `emitting == false` from the first frame after it is set and its `finished`
  signal never fires (`logs/a6_probe_headless_60fps.log`). So `HitSpark` frees
  itself on a timer: its root script counts its own processed time and frees
  the root at the longest emitter lifetime plus 0.1 s, **0.55 s**, not on
  `finished`. A3 becomes "freed within 0.55 s plus one frame". The state test
  counts `HitSpark` nodes and reads their positions; it does not read
  `emitting` on the one-shot emitters. (c) The Godot 3 names `initial_velocity`
  and `scale` exist in 4.7.2 as Vector2 compatibility properties that map onto
  the min/max pair; F1's mutation is recorded with that in mind.
- **2026-11-07 r2 (agent, after the Step 3 review).** Scope stays the three
  `player.gd` sites. Hellagur, Hoshiguma, Lin, Rosa and Santalla make their melee mesh
  spark through `basic_hit` in `entities/kits/*.gd` and get no `HitSpark`;
  this is a known limit, not a regression. A1's "not on a swing that misses"
  is checked only as "a ground click walks and spawns none": since 2026-10-20 a
  click never swings at empty ground, so no real-input miss exists.
- **2026-11-07 r3 (user verdict "kept", TUNING.md Effect B r2).** Effect B
  `Flames` QuadMesh size 0.30×0.30 → **0.55×0.55**, after the user said the
  fire looked "smothered in the wood". The settings table above still reads
  0.30; this line supersedes it. Scene and config test agree.
- **2026-11-07 r4 (user verdict "kept", TUNING.md Effect A r1).** Effect A
  `Puff` QuadMesh size 0.5×0.5 → **1.0×1.0**, from the user's observation that
  the puff barely showed on snow. The settings table above still reads 0.5;
  this line supersedes it. Scene and config test agree. The darker haze stays
  within the stand-in's body; it does not reach the snow around it (miss on
  Claude's prediction, recorded in TUNING.md).

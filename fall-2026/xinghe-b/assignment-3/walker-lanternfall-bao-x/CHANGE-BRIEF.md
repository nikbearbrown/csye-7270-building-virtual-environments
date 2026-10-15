# Lanternfall — Change Brief

`walker-lanternfall-bao-x` · Bao Xing · **v1 written 2026-09-28, before any generation and before any gameplay code**

Starter: blank Godot 4.7.2.stable.official.ed1daf0bf project (character concept from my A1, [walker-jumpman-bao-x](https://github.com/yanxlh/walker-jumpman-bao-x)).

> **Record discipline.** Everything above the **Revisions** heading is frozen at tag `design-v1`. When a prediction turns out wrong, the correction goes into `TEST-REPORT.md` and under Revisions here, with a date. Nothing above that line is rewritten to make a prediction look right.

## 1. Asset list

Every ID below must exist in `godot/assets/manifest.json` with its file present; `scripts/audit_repo.py --stage final` enforces it.

| Asset ID | What | Game file | Size / length | Panels |
|---|---|---|---|---|
| ART-PC-01 | Courier, 12-pose sheet (order as in CHARACTER-SHEET) | `godot/assets/art/pc_sheet.png` | 384 × 32 (12 × 32²) | P1–P9 |
| ART-EN-01 | Moth, 2 frames | `godot/assets/art/enemy_moth.png` | 48 × 24 | P2, P3, P6 |
| ART-EN-02 | Fog-wraith, 2 frames | `godot/assets/art/enemy_wraith.png` | 80 × 40 | P5 |
| ART-ENV-01 | Cobblestone ground tile, seamless | `godot/assets/art/env_ground_tile.png` | 64 × 64 | P2, P3, P8 |
| ART-ENV-02 | Lantern market stall prop | `godot/assets/art/env_stall.png` | 64 × 48 | P1, P2 |
| ART-FX-01 | Beam bolt | `godot/assets/art/fx_beam.png` | 16 × 8 | P3 |
| ART-FX-02 | Orbiting lamp-moth | `godot/assets/art/fx_orbit_moth.png` | 12 × 12 | P4, P6 |
| ART-FX-03 | Sunflare burst ring | `godot/assets/art/fx_sunflare.png` | 128 × 128 | P6 |
| ART-PK-01 | Lamp-oil gem | `godot/assets/art/pickup_gem.png` | 12 × 12 | P3 |
| SFX-01 | Enemy killed | `godot/assets/sfx/sfx_01_kill.wav` | ≤ 0.35 s | P3 |
| SFX-02 | Gem collected | `godot/assets/sfx/sfx_02_pickup.wav` | ≤ 0.3 s | P3 |
| SFX-03 | Player hurt | `godot/assets/sfx/sfx_03_hurt.wav` | ≤ 0.5 s | P5 |
| SFX-04 | Level up | `godot/assets/sfx/sfx_04_levelup.wav` | ≤ 1.2 s | P4 |
| SFX-05 | Sunflare evolution | `godot/assets/sfx/sfx_05_evolve.wav` | ≤ 2.5 s | P6 |
| SFX-06a | Lose stinger | `godot/assets/sfx/sfx_06a_lose.wav` | ≤ 3 s | P7 |
| SFX-06b | Win stinger | `godot/assets/sfx/sfx_06b_win.wav` | ≤ 4 s | P9 |
| MUS-01 | Night-market loop | `godot/assets/music/mus_01_night_market.ogg` | 30–40 s, seamless | P2–P5, P7, P8 |
| MUS-02 | Sunflare layer, same length and tempo | `godot/assets/music/mus_02_sunflare_layer.ogg` | = MUS-01 | P6 |

Models: art — FLUX.1-schnell (mflux, local); SFX — Stable Audio Open 1.0 (local); music — MusicGen medium / melody (local). The four required event sounds are SFX-01 (core action), SFX-04 (success), SFX-03 (hurt) and SFX-06a/06b (completion); SFX-02 and SFX-05 are extra.

## 2. Event → sound

Sounds are triggered by **game signals**, never by input. Throttling uses the **simulation clock** (ticks → ms), so a paused game cannot queue sounds.

| Game event (signal) | Emitted when | Sound | Gate rule |
|---|---|---|---|
| `enemy_killed` | an enemy's HP reaches 0 | SFX-01 | cooldown 60 ms, ≤ 3 voices, pitch ± 5 % |
| `gem_collected` | a gem reaches the courier | SFX-02 | 80 ms merge window, 1 voice |
| `player_hurt` | damage is applied (not during invulnerability) | SFX-03 | once per hit; 800 ms cooldown as a second guard (= the i-frame window) |
| `leveled_up` | each level gained | SFX-04 | once per level |
| `evolved` | Sunflare card taken | SFX-05 | once per run |
| state → LOST | HP reaches 0 | SFX-06a | once (state is terminal) |
| state → WON | timer reaches 3:00 | SFX-06b | once (state is terminal) |

Pause, resume, card navigation and mute toggles have **no** sound.

## 3. How repeated triggering is prevented

1. **No sound is attached to a key.** Holding a direction moves the courier; it never emits a sound signal. Key presses use `is_action_pressed`, which ignores key-repeat echo.
2. **Hurt is gated twice**: by the 0.8 s invulnerability (no second damage event can exist) and by the 800 ms gate.
3. **High-frequency events are throttled**: kills can happen 20 at once (Sunflare); the gate plays at most one kill sound per 60 ms and never more than 3 overlapping. Pickups within 80 ms merge into one.
4. **Once-per-run events** (evolution) are latched; the latch resets on restart.
5. **Voice accounting is logical** (a fixed 300 ms per voice), so tests give the same answer on any machine or audio device.
6. Verified by `godot/tests/test_audio.gd` (burst of 20 kills → 1 sound; 100 ticks of held input → 0 sounds; 20 rapid pause toggles → 0 sounds; per-event counts over a full run).

## 4. Music behaviour

| Situation | MUS-01 | MUS-02 | Bus |
|---|---|---|---|
| Menu | silent | silent | — |
| Run start / restart | from sample 0, 0 dB | from sample 0, −80 dB | filter off, 0 dB |
| Level-up cards | continues | continues | −6 dB |
| Pause | continues | continues | low-pass 900 Hz, −10 dB |
| Resume | continues | continues | filter off, 0 dB |
| Sunflare evolution | continues | fades to 0 dB over 2 s | — |
| Lose | fade to −80 dB over 0.5 s, stop | same | then SFX-06a |
| Win | fade over 1.0 s, stop | same | then SFX-06b |
| Restart during a fade | fade cancelled, restart from 0 at 0 dB | same | filter off |

MUS-01 and MUS-02 have identical length, start together and loop together, so they stay in sync.

## 5. Mute

**M** mutes everything, **9** music only, **0** effects only; the HUD shows `MUSIC on/off  SFX on/off`. Muting changes AudioServer bus flags only; no game logic reads them. `test_audio.gd` proves a full run with every stream removed and the master bus muted ends in exactly the same state as a run with sound.

## 6. Predicted problems and how each will be verified

1. **Kill SFX machine-guns in dense waves** (late game, and the Sunflare burst kills many at once).
   *Verify:* `test_audio.gd` burst check (20 kills in one tick → 1 sound) and minimum-gap check over a full run; listening at ~2:30 in a real run.
2. **Generated poses drift after downscaling** — lamp size changes, the character turns, the satchel swaps sides, a lamp becomes a face.
   *Verify:* `gen/checks/palette_check.py` (palette, alpha, size), the 32-px silhouette strip of the generated sheet next to the blockout, sheet-vs-game screenshots for all 12 poses.
3. **MusicGen output does not loop cleanly** (click, gap, or tempo drift at the wrap).
   *Verify:* `gen/checks/loop_check.py` — wrap jump ≤ the 99th percentile sample step, first/last 50 ms RMS ≥ 25 % of the mean; plus five consecutive loops listened to by me.
4. **The cool fog palette makes enemies unreadable against the ground**, especially muted.
   *Verify:* luminance-difference check between each enemy sprite and the ground tile (moth ≥ 0.25); the muted playtest.
5. **MUS-02 drifts against MUS-01** after evolution.
   *Verify:* equal frame-count check in `loop_check.py`; listening 10 s and 25 s after evolving. *Fallback:* drop MUS-02 and brighten the mix instead, recorded as a Revision.

## Revisions

### R1 · 2026-09-29 · Beam targeting (see CONCEPT R1)

Not one of the five predictions above — a design problem the greybox exposed before any asset existed: firing along the direction of travel made the survival move (running away) aim the Beam away from the threat. The Beam now targets the nearest enemy. No asset, event→sound mapping or music rule changes; storyboard P3 still reads correctly (the bolt goes toward the moth). Counted as the first *observe → change → re-verify* loop; evidence in `evidence/balance-probe-*.txt` and `test_gameplay.gd::beam-aims-nearest`.

### R2 · 2026-09-29 · Pixel-art prompts; ART-PC-01 is 10 poses (see CONCEPT R2, CHARACTER-SHEET R2)

- ART-PC-01 becomes **320 × 32 (10 × 32²)**; everything else in the asset table is unchanged.
- Prediction 2 ("generated poses drift") showed up in a different form than predicted: FLUX kept the identity well but ignored the requested 3 × 4 grid and drew mostly standing poses. Response: frames are now cut per figure (`gen/figures.py`) and each pose is generated with its own prompt around one fixed character description, so a pose can be regenerated alone.

### R3 · 2026-09-29 · Music: 20 s loops; how predictions 3 and 5 turned out

- **Loop length (was 30–40 s):** MusicGen generates at most 30 s per run; after a 1 s skip and the crossfade margin, 8 bars at 95.7 BPM (= **20.0 s**) is the longest clean cut. MUS-01 and MUS-02 are both exactly 882176 frames. A 3-minute run hears the loop 9 times.
- **Prediction 3 (loop seam):** all four MUS-01 candidates passed `loop_check.py`; I listened to each loop three times and picked s5 — the others were "too chaotic, too much noise". Final MUS-01: wrap jump 0.001 vs 99th-percentile step 0.009.
- **Prediction 5 (layer drift) — happened, then fixed:** the planned musicgen-melody layer (conditioned on MUS-01, drum-less "bells + pad" prompt) came out near 106 BPM on 3 of 4 runs and as hiss on the fourth; none could be fitted to the 20 s loop within a ±10% stretch. A second batch from musicgen-medium (which held 96 BPM on every MUS-01 run) gave three in-tempo layers; I picked s34 by ear ("有种远古的感觉"). Stretch 0.9897, frame counts equal (`layer-length-match` PASS). The fallback (drop MUS-02) was not needed.

### R4 · 2026-09-29 · Five new map props (see CONCEPT R4)

| Asset ID | What | Game file | Size | Panels |
|---|---|---|---|---|
| ART-ENV-03 | Lantern post: pole with a hanging paper lantern | `godot/assets/art/env_lantern_post.png` | 24×48 | P1, P2, P3, P8 |
| ART-ENV-04 | Stack of crates and a barrel | `godot/assets/art/env_crates.png` | 40×32 | P1, P2 |
| ART-ENV-05 | Noodle cart with a blue awning (second stall type) | `godot/assets/art/env_noodle_cart.png` | 64×48 | P1, P2 |
| ART-ENV-06 | Rain puddle reflecting lantern light (ground decal) | `godot/assets/art/env_puddle.png` | 32×16 | P2, P3, P8 |
| ART-ENV-07 | Fallen leaves (ground decal) | `godot/assets/art/env_leaves.png` | 16×16 | P2, P3, P8 |

Environment palette: `#8A5A3C` added (wood). No new sounds; the event→sound map and music rules are unchanged. The new props are decoration only, so prediction 4 (readability) is re-checked with the enemy-vs-ground contrast check after they are in.

### R5 · 2026-09-30 · The five props as generated

All five generated with FLUX.1-schnell and accepted by Bao from 3 candidates each (the puddle from a second batch after its prompt was rewritten — the first asked for "dark cobblestones" and FLUX painted them). Collision boxes are measured from the sprites (`SOLID_BOX` in `ground.gd`, checked by `solid-boxes-match-sprites`); the noodle cart is narrower than planned (24 × 41 px solid). Puddles and leaves are drawn at 55 % opacity so that ground decals stay darker than the courier and the pickups (CONCEPT value rule).

### R6 · 2026-10-01 · Changes from the whole-branch code review

- **SFX-04 (level up) now plays when the card screen opens**, not when XP crosses a threshold. One pickup worth two levels used to play two stacked chimes on the same tick and open the second card screen in silence; a level gained on the 3:00 tick chimed with no card at all. Now: one chime per card screen, none at the end of a run (`levelup-sfx-on-card-screen`, `no-levelup-chime-when-run-ends`).
- **A restart silences the previous run's lose/win stinger** (`restart-silences-stingers`).
- **Enemies always spawn off-screen.** Near a wall or in a corner the 400 px spawn ring used to put spawns inside the view (83 of 200 in the test), even on the courier; now the angle is re-rolled with the seeded rng and falls back to the widest strip of arena outside the view (`spawns-arrive-off-screen`).
- **The double-click launcher imports the assets on first run.** A fresh clone or the submission ZIP has no Godot import cache, and ran with placeholder art and no sound; `generated-assets-load` now fails whenever that happens.
- Correction to §2 above: with one voice and a 300 ms voice slot, pickups are effectively merged within **300 ms**, not 80 ms.

---

# Assignment 3 addendum — Lantern Gate (written before the first Blender build)

**Frozen 2026-10-13.** This addendum specifies the Assignment 3 prop before
`tools/blender/build_lantern_gate.py` is run. Later corrections belong under a
dated A3 revision; the table below is not rewritten to match the result.

## Purpose and numerical specification

The Lantern Gate turns the flat lantern-post motif from storyboard panels P1,
P2, P3 and P8 into a 3D landmark for the same fog-bound market. It is a static
blocker in a small 3D prop room: the labelled courier stand-in must stop at its
base while the lantern arms remain non-blocking.

| Property | Frozen requirement |
|---|---|
| Format | `godot/a3/lantern_gate.glb`, rebuilt only by the committed Blender script |
| Axes and size | Blender Z becomes Godot Y; merged visual bounds **1.20 m wide × 0.80 m deep × 2.85 m high**, tolerance 0.01 m |
| Origin | centre of the underside at floor level, within 0.01 m |
| Scale | every imported `MeshInstance3D` has unit scale |
| Triangle budget | at most **240 visual triangles**; justified because the room shows one hero prop and the Assignment 2 pixel art stays deliberately simple |
| Materials | exactly `AgedBrass`, `DarkWood`, `EmberGlass` |
| Collider | two authored boxes: 0.80 × 0.80 × 0.32 m base and 0.42 × 0.42 × 2.55 m post; no collision on the 1.20 m cross-arm or lantern shades |
| Physics role | static blocker |
| Behaviour | a 0.25 m-radius labelled stand-in driven at 2 m/s stops within 120 frames at 60 fps and never crosses the base |

## Layer plan

| Object | Layer number / bit | Mask | Detects or blocks |
|---|---:|---:|---|
| Floor | 1 / 1 | 0 | stand-in |
| Stand-in | 2 / 2 | 5 | floor (1) and prop (4) |
| Lantern Gate | 3 / 4 (`market_prop`) | 0 | stand-in through its mask |

The room owns and frees the prop instance. Existing 2D player tuning, audio,
simulation, layers, masks and tests are invariants and must not change.

## Answers before delegation

- Height is Godot **Y** after Blender's Z-up glTF export.
- Unapplied Blender scale can arrive as a non-unit node transform even when the
  visible dimensions look correct; the test checks both AABB and node scale.
- A copied `.import` can preserve the wrong `nodes/use_node_type_suffixes`
  setting, turning `-convcolonly` geometry into visible geometry instead of a
  collider. Godot must generate the import record itself.
- The stand-in's mask, not the static prop's mask, must include layer 3.
- `body_entered` is irrelevant for a static blocker; if this were an Area3D,
  an overlap that began before signal connection would not emit a new entry.

## Predicted failures and checks

1. **Wrong up axis or unapplied scale.** Merge imported visual AABBs and assert
   1.20 × 2.85 × 0.80 m in Godot, plus unit scale on every mesh node.
2. **Suffix import disabled.** Assert that two `StaticBody3D` nodes and no
   visible collider meshes arrive from the GLB.
3. **Collider feels like an invisible wall under the arms.** Sample the two box
   volumes and drive the stand-in into the base; the cross-arm volume must stay
   free. Confirm visually with Visible Collision Shapes.
4. **Wrong collision bit.** Read the running bodies and assert layer 3 / bit 4;
   a mutation to layer 1 must make the same predicate fail.

## A3 revisions

### A3-R0 · 2026-10-13 · Scope correction before assets two and three

My first reading treated the Assignment 3 deliverable as one hero prop. Reading
the Canvas page directly showed that it requires **three** simple assets and
limits each to no more than six visible basic shapes. The existing Lantern Gate
used 18 visible mesh objects, so it must also be simplified. This correction is
written and committed before building the two missing assets or rebuilding the
gate. The original one-prop brief above remains frozen as evidence of the miss.

The three assets all belong to Lanternfall's midnight market and will appear
side by side in the Assignment 3 prop room:

| Asset | Game purpose and location | Frozen size W x D x H | Origin | Recognisable look / materials | Shape and triangle budget |
|---|---|---|---|---|---|
| Lantern Gate | landmark and static blocker at the market entrance | 1.20 x 0.80 x 2.85 m | centre of underside, on floor | dark base/post, brass cross-arm, two glowing orange lantern blocks | 6 visible primitives, <= 160 triangles |
| Supply Stack | obstacle beside a market stall | 1.20 x 0.80 x 1.10 m | centre of underside, on floor | two offset wood crates, one low-poly brass-bound barrel | 3 visible primitives, <= 180 triangles |
| Lamp-oil Shrine | collectible landmark near the upgrade area | 0.80 x 0.80 x 1.45 m | centre of underside, on floor | dark plinth, brass stem, emissive faceted oil gem | 3 visible primitives, <= 120 triangles |

All three are upright on Blender +Z and Godot +Y, use metre units, have rotation
and scale applied before export, and must import with node scale `(1, 1, 1)`.
The Godot room places them at x = -2.0, 0.0 and 2.0 metres on the same floor.
Only the Lantern Gate needs collision for this assignment; the other two are
display props so the shared camera can move behind and below them unobstructed.

Predicted failures for the three-asset rebuild:

1. **The simplified gate loses its silhouette.** Check it from the front and
   rear in Blender and in the running Godot room; both orange lantern blocks
   must remain separated and readable.
2. **A GLB arrives with the wrong axis, size or unapplied scale.** The headless
   check compares each merged AABB with the table, verifies floor-level origin,
   +Y height in Godot and unit scale on every imported mesh.
3. **Cylinder segments break the budget.** Each build log records the visible
   primitive count and triangulated face count; the check compares those values
   with the frozen per-asset limits.
4. **Materials disappear or the emissive gem/lantern becomes ordinary grey.**
   Inspect the Blender material names, then inspect the running Godot scene and
   enumerate imported active material names in the headless check.
5. **The three assets overlap or float in the shared room.** Ray-check the floor
   beneath each placement, merge their world AABBs, and verify pairwise gaps.

### A3-R1 · 2026-10-13 · First Blender build exceeded two frozen limits

The first script run measured 1.36 m wide and 248 visual triangles. The two
lantern roofs extended 0.08 m past each end of the 1.20 m cross-arm, and the
12-sided post put the otherwise simple prop eight triangles over budget. I did
not change the specification: the lantern centres move from ±0.38 m to ±0.33 m,
their roof radius drops from 0.30 m to 0.27 m, and the post becomes a 10-sided
cylinder. Rebuild must now report exactly 1.20 m and at most 240 triangles.

### A3-R2 · 2026-10-13 · Returning from the room exposed partial input setup

The first Esc → F4 integration check printed missing-action errors. The A3 room
had created the four movement actions; when the 2D session loaded, its old
`_ensure_inputs()` returned as soon as it saw `move_left`, so it never added
start, pause, mute, card, collision-debug or A3-room actions. The early return
is removed. The existing per-action guard remains, so actions are added only
when absent and the 2D controls/tuning do not change.

### A3-R3 · 2026-10-14 · The room camera could not look behind or below

A3-R0 says the shared camera "can move behind and below" the three assets,
and the assignment's human check walks the camera around each asset,
including from behind and below. Checking the room against that sentence
showed a fixed `Camera3D` at (5.8, 3.8, 7.6) aimed at (0, 1.15, 0): only a
front three-quarter view exists in the running scene. The room gains an orbit
camera; nothing else changes.

- Start view: the same position and aim as before.
- Q / E or right-mouse drag orbit around (0, 1.15, 0); R / F or vertical drag
  tilt between −50° and +80°; Z / X or the mouse wheel zoom between 3 and 14 m.
- While the camera is below the floor's top (y < 0), only the floor's mesh is
  hidden so the undersides can be seen; the floor's collider stays, so the
  stand-in still stands on it.
- The stand-in's WASD movement, layers, masks, the props and every 2D control
  are unchanged.

Prediction and check: a new headless suite `test_a3_camera.gd` drives the
orbit inputs. It must find the start view unchanged (within 0.01 m), the
camera behind the props (z < 0) after a half orbit, below the floor with the
floor mesh hidden and its collider still enabled at minimum tilt, the floor
mesh visible again above it, and the zoom clamped. The existing A3 suites must
stay 17/17 and 14/14, and the Assignment 2 suites 122/122.

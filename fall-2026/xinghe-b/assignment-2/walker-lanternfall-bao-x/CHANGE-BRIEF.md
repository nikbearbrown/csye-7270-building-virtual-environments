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

# Lanternfall — Character Sheet: the Lamp-Head Courier

`walker-lanternfall-bao-x` · Bao Xing · **v1 written 2026-09-28, before any generation**

All images on this page are **pre-generation blockouts** drawn by `design/character/make_blockout.py` at true game size (32 × 32) and enlarged with nearest-neighbour scaling. They are the target the generated sprites (asset ART-PC-01) must match; the comparison is added under **Revisions** after generation.

## 1. Identity

The courier from my Assignment 1 ([walker-jumpman-bao-x](https://github.com/yanxlh/walker-jumpman-bao-x)), moved from a side-view platformer to a top-down survivor. Carried over:

- an **oversized brass lamp housing** for a head, lens facing the direction of travel;
- a **narrow navy torso** (long coat);
- a **satchel counterweighting the trailing side**;
- the **light wedge / glow** that is now literally the weapon.

## 2. Silhouette test at game size

Actual size (1×) and the same strip at 3×:

![silhouettes at 32 px](design/character/silhouette-32-actual-size.png)

![silhouettes at 32 px, 3x](design/character/silhouette-32.png)

Rule: **every gameplay pose must be identifiable in solid black at 32 px.** Order: turn_front, turn_side, turn_back, idle, walk_contact, walk_passing, cast, hurt, levelup, sunflare, defeat, victory.

| Riskiest pair | How they differ in silhouette |
|---|---|
| idle vs turn_side | idle: legs apart, front arm hanging; turn_side: legs together, no arm |
| walk_contact vs walk_passing | contact: legs in a wide V; passing: one leg lifted forward |
| levelup vs victory | levelup: both arms up in a V; victory: one fist up, other arm down, wide stance |
| levelup vs sunflare | levelup: arms up; sunflare: arms straight out sideways |
| turn_front vs turn_back | same outline **by design** (a turnaround); told apart by colour (gold lens vs navy back). Both are reference/title poses only, never used for a gameplay state. |

## 3. Facing

- Art is authored **facing right**. Facing left is a horizontal flip done by code (`draw_set_transform` with scale x = −1). The flip is a mirror, **not** counted as a pose.
- Facing follows **horizontal** input with a 0.1 dead-zone. Pure vertical input keeps the last facing, so the sprite never flickers when moving up/down or when a stick drifts.
- turn_front and turn_back exist for the sheet and the title/menu portrait only.

## 4. Poses and game states (12)

![blockout poses](design/character/blockout-poses-x8.png)

| # | Pose | Game state | Trigger | Duration |
|---|---|---|---|---|
| 1 | turn_front | reference / title menu portrait | MENU | while on menu |
| 2 | turn_side | reference | — | — |
| 3 | turn_back | reference | — | — |
| 4 | idle | PLAYING, not moving | no input | while still |
| 5 | walk_contact | PLAYING, moving | input held | alternates with 6 every 8 ticks |
| 6 | walk_passing | PLAYING, moving | input held | alternates with 5 every 8 ticks |
| 7 | cast | PLAYING | each Beam shot / each Sunflare pulse | 8 ticks / 12 ticks |
| 8 | hurt | PLAYING | damage taken | first 12 of the 48 invulnerable ticks |
| 9 | levelup | LEVELUP | level gained | while choosing a card (also the card-screen portrait) |
| 10 | sunflare | PLAYING | Sunflare card taken | 60 ticks, then idle/walk with brightened colours |
| 11 | defeat | LOST | HP reaches 0 | until retry (also the result-panel portrait) |
| 12 | victory | WON | timer reaches 3:00 | until retry (also the result-panel portrait) |

Priority when several apply: levelup/defeat/victory/sunflare override > hurt > cast > walk > idle.

## 5. Collision overlay

![collision overlay](design/character/collision-overlay-x8.png)

- Hurtbox: **circle, radius 10 px, centred at frame pixel (16, 20)** — the torso. In code the frame is drawn at `Rect2(-16, -20, 32, 32)`, so this pixel is the node's origin.
- The lamp top, the glow and the raised arms are **outside** the hurtbox on purpose (pillar "light is power": growing light never makes you easier to hit).
- F3 in game draws this circle over the live sprite.

## 6. Palette

![palette](design/character/palette.png)

| Hex | Role |
|---|---|
| `#F2B84B` | lamp gold — lamp housing, beam core |
| `#FFF1C9` | glow cream — lens, glow, highlights |
| `#2E3A59` | coat navy — torso, back of lamp |
| `#8A5A3C` | satchel brown |
| `#14121C` | outline ink — every outer edge, legs, arms |

## 7. Consistency rules (every frame)

1. 32 × 32 px, transparent background, **binary alpha** (0 or 255).
2. **Only the 5 palette colours** (checked by `gen/checks/palette_check.py`).
3. Feet touch **row 31** (except defeat).
4. Lamp diameter **11–13 px**.
5. Torso centre within **±1 px of (16, 20)**, except hurt (leans back) and defeat.
6. Satchel always on the **trailing side** (left, for the right-facing master).
7. **1-px ink outline** on every outer edge.
8. Lamp lens faces the travel direction (right) in every side pose.
9. Stored frames always face right; a left-facing generated cell may be mirrored once during processing only to restore this rule, and that edit is logged.

## Revisions

### R2 · 2026-09-29 · 10 poses, generated as 2D pixel art

Bao's direction after the first batch: 2D pixel art, not many actions. The sheet keeps the rubric minimum of **10 poses**; the two reference-only turnaround views that no game state uses (**turn_side**, **turn_back**) are dropped. New frame order in `pc_sheet.png` (320 × 32):

| # | Pose | Game state |
|---|---|---|
| 1 | turn_front | title menu portrait |
| 2 | idle | PLAYING, still |
| 3 | walk_contact | PLAYING, moving (alternates with 4 every 8 ticks) |
| 4 | walk_passing | PLAYING, moving |
| 5 | cast | 8 ticks after each Beam shot / 12 after each Sunflare pulse |
| 6 | hurt | first 12 of the 48 invulnerable ticks |
| 7 | levelup | LEVELUP |
| 8 | sunflare | 60 ticks after evolving |
| 9 | defeat | LOST |
| 10 | victory | WON |

Every other rule on this page is unchanged (palette, 32 × 32, binary alpha, feet on row 31, hurtbox r = 10 at (16, 20), right-facing master with code flip). The pre-generation blockout above still shows 12 poses; it is kept as the original record. Verified by `test_gameplay.gd::pose-table-matches-sheet` (10 poses, sheet width = 32 × 10).

### R3 · 2026-09-29 · Generated sheet vs this page vs the game

![sheet vs game](design/character/sheet-vs-game.png)

Rows: pre-generation blockout · generated, palette-locked frame · the frame captured in the running game (`godot/tests/capture.gd`) · silhouette of the generated frame at 32 px. Source runs and every processing step: ASSET-LOG → ART-PC-01; mapping `gen/mappings/ART-PC-01.json`.

**Measured on `pc_sheet.png`:**

| Pose | Height (px) | Coat centre (x, y) | Lamp rows |
|---|---|---|---|
| turn_front | 20 | (15.4, 24.9) | 13–20 |
| idle | 19 | (16.1, 22.8) | 14–21 |
| walk_contact | 23 | (16.2, 22.3) | 11–19 |
| walk_passing | 22 | (16.3, 22.5) | 12–19 |
| cast | 20 | (15.8, 23.6) | 13–21 |
| hurt | 24 | (15.6, 20.2) | 10–19 |
| levelup | 20 | (15.5, 21.7) | 14–21 |
| sunflare | 21 | (15.5, 22.8) | 12–20 |
| defeat | 21 | (15.5, 24.3) | — (lamp recoloured out) |
| victory | 20 | (15.7, 22.3) | 13–21 |

**Rules that held:** 32 × 32, transparent, binary alpha; only the 5 palette colours (`palette_check.py` PASS); feet on row 31; lamp normalised to 12 px (rule 11–13); every stored frame faces right (left-facing sources mirrored once, logged); code flips for left.

**Rules that broke, and what was done:**

1. **Torso centre (rule 5, "±1 px of (16, 20)").** The generated courier is shorter than the blockout (19–23 px tall vs ~30), so the coat centre sits at y ≈ 22–24. Observed in the table above; changed `player.gd` to draw the frame from `SPRITE_ORIGIN = (16, 23)` so the hurtbox is centred on the coat again; verified by the new `test_gameplay.gd::hurtbox-centred-on-torso` (it failed at (16, 20) with every coat centre 1.7–3.6 px low, and passes at (16, 23)). **The hurtbox is now circle r = 10 at frame pixel (16, 23)** ([overlay on the generated frame](design/character/collision-overlay-generated-x8.png)).
2. **"Lamp outside the hurtbox" (section 5).** Because the figure is shorter, an r = 10 circle on the torso also covers the lower half of the lamp. Only partly kept. Not changed yet: shrinking the hurtbox (≈ r = 7) would make the game easier, so it is a playtest decision.
3. **Silhouettes (section 2).** Less distinct than the blockout: idle / walk_contact / walk_passing differ mostly in the legs, and levelup and victory both raise one arm (FLUX did not give "both arms up"). In motion the walk frames alternate every 8 ticks, which reads; levelup and victory are never on screen together.
4. **Glow.** The blockout's soft halo does not survive: FLUX drew none and binary alpha removes soft light. The empowered state is a brighter modulate in code instead.
5. **Satchel side (rule 6).** The satchel is on the hip facing the viewer in most generated poses rather than strictly on the trailing side.

### R4 · 2026-10-02 · Loop or once, both facings and the hurtbox in the engine (added after the slice was built)

Written after generation, from the code at `8a6f988`; it labels the shipped poses and adds evidence, and changes no rule above.

| # | Pose | Game state | Loops or once | How long (60 ticks = 1 s) |
|---|---|---|---|---|
| 1 | turn_front | title-menu portrait (`hud.gd`) | held, static | while the menu is up |
| 2 | idle | PLAYING, not moving | held, static | while still |
| 3 | walk_contact | PLAYING, moving | **loops** with 4 | 8 ticks each (`WALK_FRAME_TICKS`) |
| 4 | walk_passing | PLAYING, moving | **loops** with 3 | 8 ticks each |
| 5 | cast | each Beam shot / each Sunflare pulse | once per shot | 8 ticks (`CAST_POSE_TICKS`) / 12 ticks |
| 6 | hurt | damage taken | once per hit | the first 12 of the 48 invulnerable ticks |
| 7 | levelup | LEVELUP (also the card-screen portrait) | held | while the cards are up |
| 8 | sunflare | Sunflare card taken | once per run | 60 ticks (`EVOLVE_POSE_TICKS`), then idle/walk with the brighter coat |
| 9 | defeat | LOST (also the result-panel portrait) | once, held | until R |
| 10 | victory | WON (also the result-panel portrait) | once, held | until R |

Facing left is the runtime mirror of every frame (`player.gd` line 107); no left-facing art exists. In-engine evidence for both facings and the hurtbox on every pose:

![sheet vs game, facing left and with the F3 hurtbox](design/character/sheet-vs-game-facing.png)

Rows: blockout · generated frame · in game facing right · in game facing left · facing left with the F3 hurtbox (r = 10 at sprite origin (16, 23)), captured by `scripts/capture_facing.gd` on an isolated copy of `8a6f988`. Art outside the hurtbox: the upper lamp in every standing pose (fair: the light never makes the courier easier to hit — section 5); the lamp leaning back in **hurt** (in the player's favour); the lying body in **defeat** (the run is over, nothing collides). Art inside it that the sheet wanted outside: the lower half of the lamp (R3, item 2 — still open, a playtest decision).

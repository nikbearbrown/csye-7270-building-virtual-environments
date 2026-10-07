# Character sheet — Lappland (Assignment 2 summary)

> **Retrospective and incomplete.** This summarizes the existing sprites in
> `godot_assets/`. Silhouette, collision-overlay and pose-sheet images were added on 2026-10-07 by script from the existing runtime atlases (no new generation). There is still no turnaround, and only 7 distinct poses.

**Concept:** a chibi pixel wolf-girl swordswoman with two blades, white hair and a
dark coat.

> **Rights note:** Lappland is a copyrighted Arknights character. The prompts named
> her directly.

## On-screen size and silhouette

The runtime walk cell is 32×32 texels, with `PIXEL_SIZE` 0.06 world units per texel.
The camera shows 15 px per world unit, which works out to about 29 px at 640×360, or
about 58 px in the 1280×720 window.

- **Silhouette image:** `design/character/silhouette.png` (added 2026-10-07, derived by script from the runtime atlases, no new generation). The top row shows each pose filled black at 1× (one texel per pixel at the 640×360 internal resolution). Below it are the same poses at 2× (the 1280×720 window) over the mine, city and snow surfaces.
- **Readability evidence:** the visual test `capture_lappland.gd` writes `design/character/in-engine/lappland-{mine,city,snow}-*.png` at game size on all three surfaces.

## Orientation

**Walk/idle:** 8 directions, all drawn (E, SE, S, SW, W, NW, N, NE).

- Exception: the generated SE row faced the wrong way, so SE is shown as SW flipped (`lappland_animator_3d.gd:26`).

**Combat:** 5 rows drawn (S, SW, W, NW, N). The other three are flipped at runtime:

| Shown | Source |
|---|---|
| E | W, flipped |
| SE | SW, flipped |
| NE | NW, flipped |

Facing is computed relative to the camera, with 6° hysteresis.

## Poses (states that exist in the game)

| # | Pose / state | Source cells | Notes |
|---|---|---|---|
| 1 | Idle | walk frame 0, 8 directions | — |
| 2 | Walk (representative stride) | walk frames 1–3, 8 directions | — |
| 3 | Attack 1 | combat columns 0–2 | — |
| 4 | Attack 2 | combat columns 3–5 | — |
| 5 | Attack 3 (finisher) | combat columns 6–9 | — |
| 6 | Sword-wave release | combat columns 10–12 | — |
| 7 | Hurt | combat column 13 | — |
| 8 | Dash/dodge | walk frame 1 + blue tint | **Not a distinct pose.** Counts with Walk. |

The atlases are `lappland_8dir_walk_32.png` and `lappland_combat_64.png`. Unused
concept images are `lappland_chibi_*.png`.

That gives **7 distinct poses, short of the required 10.** These are missing:

- turnaround with a height bar;
- death/defeat;
- respawn/recover;
- celebrate.

## Collision

The collider is a `CapsuleShape3D` with radius 0.45 and height 1.3 (`entities/player.gd:155-160`).

- The 64-texel combat cells (3.84 world units) share the walk cell's centre and foot line. The blades and slash arcs reach well beyond the capsule.
- That overhang is fair to the player: the hit is resolved by the attack's own reach and arc, not by the body collider, and the player's own hurtbox stays the small capsule.
- **Overlay image:** `design/character/collision.png` (added 2026-10-07). The capsule, 15 × 21.7 texels at `PIXEL_SIZE` 0.06, is drawn over each pose at 4× on the billboard plane, with the foot line marked. It is a diagnostic: the 58° camera tilt is ignored, so in-game the capsule's footprint reads a little shorter.
- **Pose sheet:** `design/character/poses.png`, labelled with the game state of each pose.

## Palette

Measured by median-cut quantization of `lappland_8dir_walk_32.png`, 7 colours
including the key colour:

| Hex | Use |
|---|---|
| `#0f0e0e` | outline / coat |
| `#2a2929` | dark coat |
| `#4d4a4c` | coat mid-tone |
| `#a1a0a4` | blades / grey hair shading |
| `#e0dcdc` | hair |
| `#ede7e6` | hair / skin light |

**Caveat:** the sheet has about 5,500 unique colours. It was downsampled, never
palette-locked.

**Not checked:** contrast against the three ground surfaces (no numeric check exists;
only the visual captures).

## Consistency rules

**As practised:**

- The combat atlas was generated with the walk sheet as its character and style reference (`godot_assets/拉普兰德战斗素材.md`).
- `prepare_combat_atlas.py` aligns the foot line and centre.
- `test_lappland.gd` asserts the foot line and on-screen height.

**Known drift** (from `拉普兰德战斗素材.md`):

- the SW combat row is almost identical to the S row;
- the N-row frames barely differ.

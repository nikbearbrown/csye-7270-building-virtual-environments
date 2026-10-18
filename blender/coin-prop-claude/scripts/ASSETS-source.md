# ASSETS - the three real assets, with the numbers that come out of the real runs

Blender 5.1.2, metric (1 unit = 1 m), Z up. Each asset is built from basic shapes only, joined into ONE object, transforms applied
(rotation 0, scale 1), origin at the centre of the underside = the world origin (lowest point z = 0.0000 m), exported as binary glTF
with the exporter's **+Y Up on**. Each script prints its own table; the log beside it is the film's real terminal output.

Command (run from this folder, exactly as the film shows it):

```
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python build_crate.py
```
(and `build_lantern.py`, `build_coin.py`). Exit code 0 for all three.

| asset | script | log | dimensions (x y z), Blender | triangles | shapes | materials | .glb |
|---|---|---|---|---|---|---|---|
| Crate | build_crate.py | build_crate.log | 0.800 x 0.800 x 0.800 m | 60 | 5 | CrateWood, CrateBand | crate.glb, 6,328 bytes |
| Lantern | build_lantern.py | build_lantern.log | 0.300 x 0.300 x 0.500 m | 202 | 5 | DarkIron, WarmGlass, Flame | lantern.glb, 16,520 bytes |
| Coin | build_coin.py | build_coin.log | 0.300 x 0.300 x 0.040 m | 180 | 3 | CoinGold, CoinFace | coin.glb, 12,416 bytes |

All three are under the course limits (at most 6 shapes, at most 500 triangles). Each printout ends with
`origin at world (0.000, 0.000, 0.000) | lowest point z = 0.0000 m | rotation (0.0, 0.0, 0.0) | scale (1.0, 1.0, 1.0)`.

## What is in each asset (every part is a Blender basic shape)

**Crate (5 shapes, 5 x 12 = 60 triangles).** One cube 0.76 m on a side (z 0.02 to 0.78, "CrateWood") plus four thin cubes in "CrateBand":
a ring round the bottom (0.80 x 0.80 x 0.10, z 0 to 0.10), a ring round the top (z 0.70 to 0.80), and two straps (0.10 x 0.80 x 0.80) that
cross over the top and run down the four sides. Because the top ring is a full 0.80 x 0.80 cube, the top face is band-coloured (it reads as a lid).

**Lantern (5 shapes, 202 triangles).** All cylinders and the cone have 12 vertices, so the footprint is exactly 0.30 x 0.30.

| part | shape | size | z range (m) | triangles | material |
|---|---|---|---|---|---|
| Lantern_Base | cylinder, 12 vertices | radius 0.15, 0.04 high | 0.00 - 0.04 | 44 | DarkIron |
| Lantern_Glass | cylinder, 12 vertices | radius 0.10, 0.23 high | 0.04 - 0.27 | 44 | WarmGlass |
| Lantern_Flame | UV sphere, 8 segments x 5 rings | radius 0.06 | 0.26 - 0.38 | 64 | Flame |
| Lantern_Roof | cone, 12 vertices | radius 0.14, 0.10 high | 0.37 - 0.47 | 22 | DarkIron |
| Lantern_Finial | cylinder, 8 vertices | radius 0.02, 0.03 high | 0.47 - 0.50 | 28 | DarkIron |

The flame is a sphere in the open gap between the glass and the roof so that it is visible (an opaque glass body would hide it). The glass is an
opaque flat colour, not transparent.

**Coin (3 shapes, 180 triangles).** A flat cylinder (24 vertices, radius 0.15, z 0.005 to 0.035, "CoinGold", 92 triangles) with a raised
medallion on each face (cylinder, 12 vertices, radius 0.09, 0.005 high, "CoinFace", 44 triangles each). Overall thickness 0.04 m, lying flat.
If a plain single cylinder is wanted, delete the two medallions: 0.30 x 0.30 x 0.04 m, 92 triangles, 1 shape.

Triangle formulas used (all confirmed by the printouts): cylinder with n vertices = 4n - 4; cone with n vertices = 2n - 2; UV sphere with
s segments and r rings = 2s(r - 1); cube = 12.

## Colours (flat, no textures), and that they survive the export

Set as the Principled base colour AND the viewport colour. sRGB values the exported files carry (from `evidence/godot/glb_colours.log`) and
the albedo Godot reports after import (from `evidence/godot/colours_good.log`) are identical:

| material | sRGB | | material | sRGB |
|---|---|---|---|---|
| CrateWood | #C48A4F | | DarkIron | #3A3A42 |
| CrateBand | #7E5128 | | WarmGlass | #FFB41F |
| CoinGold | #FFC20A | | Flame | #FF5400 |
| CoinFace | #E39A00 | | | |

All materials: metallic 0, roughness 0.9.

## What Godot 4.7.2 reports (headless, `evidence/godot/check_good.log`)

| asset | bounding box size (x y z) | node scale | longest axis | gap to floor |
|---|---|---|---|---|
| crate | 0.8 x 0.8 x 0.8 m | 1, 1, 1 | X=Y=Z | 0.0 m |
| lantern | 0.3 x 0.5 x 0.3 m | 1, 1, 1 | Y | 0.0 m |
| coin | 0.3 x 0.04 x 0.3 m | 1, 1, 1 | X=Z (height Y 0.04) | 0.0 m |

Godot's Y is Blender's Z (the lantern is 0.5 m along Y in Godot because +Y Up was on).

## Renders and other files made from these assets

- `pantry/ev_crate_34.png`, `ev_lantern_34.png`, `ev_lantern_back.png`, `ev_lantern_below.png`, `ev_coin_34.png`, `ev_three_side_by_side.png`: Blender Workbench, transparent PNG, 2400 x 1350 (`evidence/renders/render_assets.py`, log beside it).
- `crate.blend`, `lantern.blend`, `coin.blend` and Blender's own backups `crate.blend1`, `lantern.blend1`, `coin.blend1`: `save_blend_demo.py`, listing in `ls_blend.log`. Preferences > Save & Load > Save Versions is **1** in a factory Blender, so a save keeps ONE backup, `.blend1`; a `.blend2` only appears if that number is raised.
- The `.glb` files are small (6-17 KB) because there are no textures.

## Deliberately wrong exports (for the failure demos; `evidence/godot/build_variants.py`)

`lantern_yup_off.glb`, `crate_scale_unapplied.glb`, `crate_origin_centre.glb`, `lantern_x10.glb`, `crate_colour_lost.glb` live in the scratch Godot project
(`/private/tmp/claude-501/a3film/godot_proj/variants/`), not in the repo; `evidence/godot/setup_project.sh` rebuilds them.

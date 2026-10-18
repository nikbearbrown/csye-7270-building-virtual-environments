# Coin (teaching prop), built by Claude

*A teaching prop for CSYE 7270: a gold coin: a 24-sided disc with a raised 12-sided medallion on each face, from basic shapes only.*

`3 basic shapes · 180 triangles · 2 materials · 0.30 x 0.30 x 0.04 m · Blender 5.1.2`

One of three tiny assets made for Assignment 3 of CSYE 7270 (course limits: at most 6 shapes, at most 500 triangles). It is a gold coin: a 24-sided disc with a raised 12-sided medallion on each face. Flat colours only, joined into one object, origin at the centre of the underside, lowest point at z = 0. These are teaching primitives, not likenesses of any real object.

## Views

### Front three-quarter

From front-left and above, the main view.

<img src="renders/web/coin_front34.jpg" width="720" alt="Front three-quarter">

[Full-size file](renders/coin_front34.png)

### Back three-quarter

From back-right and above, to check the far sides.

<img src="renders/web/coin_back34.jpg" width="720" alt="Back three-quarter">

[Full-size file](renders/coin_back34.png)

### Side, low

Almost level with the floor, to check proportions and that the prop sits on z = 0.

<img src="renders/web/coin_side.jpg" width="720" alt="Side, low">

[Full-size file](renders/coin_side.png)

### Top

Straight down, to check the footprint.

<img src="renders/web/coin_top.jpg" width="720" alt="Top">

[Full-size file](renders/coin_top.png)

### Close-up, medallion and rim

The raised medallion and the faceted rim. The medallion is a plain 12-sided disc: no emblem, lettering or rim bevel.

<img src="renders/web/coin_close.jpg" width="720" alt="Close-up, medallion and rim">

[Full-size file](renders/coin_close.png)

## Compare with references

No photo or drawing reference exists for this prop: it is a primitives-only teaching asset made to the course limits, not a copy of a real object. There is nothing to compare it against.

## Film

Companion film: coming soon

<!-- FILM_URL -->

## Download

| File | Size | What it is | Download |
|---|---|---|---|
| `coin.blend` | 95 KB | Blender scene: one joined mesh, flat-colour materials. No camera or light is stored in it. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/coin.blend) |
| `coin.glb` | 12 KB | glTF binary, exported with +Y Up on; flat base colours, no textures. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/coin.glb) |
| `scripts/build_coin.py` | 4 KB | The script that built the prop (run in background Blender). | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/scripts/build_coin.py) |
| `scripts/build_coin.log` | 1 KB | Terminal output of that run, as recorded. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/scripts/build_coin.log) |
| `scripts/render_props.py` | 4 KB | Renders the five views in renders/ (EEVEE). | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/scripts/render_props.py) |
| `scripts/ASSETS-source.md` | 6 KB | The source folder's ASSETS.md for all three props, copied unchanged. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/scripts/ASSETS-source.md) |
| `scripts/count_scene.py` | 1 KB | Counts meshes, triangles, materials and size from the .blend. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/scripts/count_scene.py) |
| `scripts/make_pages.py` | 11 KB | Generates README.md, BUILD_NOTES.md and index.html. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/scripts/make_pages.py) |
| `BUILD_NOTES.md` | 4 KB | How it was built and what is unverified. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/BUILD_NOTES.md) |
| `index.html` | 124 KB | Self-contained viewer with the renders. | [download](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/index.html) |

coin.glb carries flat base colours only: no textures, no UVs of note. The source's Godot import check reported identical colours after import (per ASSETS.md; not re-run here).

## How to import into Blender

- **`.blend`:** open it in Blender 4.2 or later (File > Open). 
- **`.glb`:** in Blender, File > Import > glTF 2.0 (.glb/.gltf), or drop it into a game engine or a web viewer.

## Viewer

A self-contained interactive viewer is in [`index.html`](index.html) (images embedded, works offline once downloaded):

- GitHub Pages: https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/coin-prop-claude/ (works once Pages is enabled for the repo)
- Fallback through htmlpreview: https://htmlpreview.github.io/?https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/coin-prop-claude/index.html

## Built by

- **Builder:** Claude (no model version is recorded in the source files)
- **Method:** Scripted: build_coin.py was run once in background Blender (`Blender -b --factory-startup --python-exit-code 1 --python build_coin.py`), as ASSETS.md and build_coin.log record. It was NOT built through the Blender MCP: the lecture's BUILD-LOG.md says 'The three assets in the film were built by a Blender script (the assignment's fallback route)' and that nobody has run the MCP route. No render-versus-reference rounds and no hand-modelling rounds: one scripted build, no references. The five renders here were made on 2026-10-18 by scripts/render_props.py (one pass, plus two layout adjustments of the cameras).
- **Tools:** Blender 5.1.2 (read from the .blend by count_scene.py and from the build log); glTF exporter bundled with Blender; Godot 4.7.2 was used by the source film for an import check (evidence/godot logs, not copied here).
- **Build date:** 2026-10-06 (build logs at 12:59, .blend saved 13:27); renders 2026-10-18
- **Human review:** Professor Bear: pending (no verdict is recorded in the source folder).

## Honest limitations

- There is no emblem or lettering; the face is a flat plain medallion. The rim is a 24-sided polygon and visibly faceted.
- The coin is metallic gold in colour only: all materials are metallic 0, roughness 0.9, so it looks matte, not shiny.
- The .blend was saved by Blender 5.1.2 (save_blend_demo.py) and has never been opened in Blender 4.2; Blender 4.2 may refuse or warn.
- The .blend has no camera and no light; the renders use a stage (floor and lights) added at render time, which is not in the file.
- The source folder's own note: the glass, flame and colours are flat Principled base colours, not textured; the .glb is small because there are no textures.

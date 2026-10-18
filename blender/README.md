# Blender builds

Every 3D model built for this course gets its own subfolder here. Several AI builders add models to this folder (Grok Bot, Claude, Codex, Muse), so **every folder name ends with the builder's name**: `-grok`, `-claude`, `-codex` or `-muse`. Folder names are also specific to the model (for example `seis-bot-grok`, not `robot`), since many models of the same kind will be added.

Each model folder has a `README.md` you can read on GitHub (views, comparisons with the references, downloads, import instructions and limitations) and a self-contained `index.html` viewer. The viewer links use GitHub Pages, which has to be enabled for this repo for them to work; the fallback links open the same page through htmlpreview.

To download a single file, use the links in a model's README, or open the file on GitHub and click **Download raw file**. To get everything, clone the repo or use **Code → Download ZIP**. The `.blend` files open in Blender 4.2 or later.

| Preview | Folder | Builder | What it is | Pages |
|---|---|---|---|---|
| <img src="seis-bot-grok/renders/web/02_seated_front.jpg" width="140" alt="SEIS Bot"> | [`seis-bot-grok/`](seis-bot-grok/) | Grok Bot | SEIS Bot, an armored humanoid robot with a white 6 on the chest and a worn, distressed finish, built from AI-generated reference images. Version 4 of 4. Files: `robot_seated.blend`, `robot_standing.blend`, `robot_v4.glb`. | [README](seis-bot-grok/README.md) · [viewer](https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/seis-bot-grok/) ([fallback](https://htmlpreview.github.io/?https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/seis-bot-grok/index.html)) |
| <img src="jaguar-xkss-1957-grok/renders/web/xkss_hero.jpg" width="140" alt="Jaguar XKSS"> | [`jaguar-xkss-1957-grok/`](jaguar-xkss-1957-grok/) | Grok Bot | A 1957 Jaguar XKSS (the road-going D-type) in British Racing Green, built from studio photos. First pass, after 8 comparison rounds. Files: `xkss.blend`, `xkss.glb`. | [README](jaguar-xkss-1957-grok/README.md) · [viewer](https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/jaguar-xkss-1957-grok/) ([fallback](https://htmlpreview.github.io/?https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/jaguar-xkss-1957-grok/index.html)) |
| <img src="crystal-palace-1851-claude/renders/web/overview.jpg" width="140" alt="Crystal Palace 1851"> | [`crystal-palace-1851-claude/`](crystal-palace-1851-claude/) | Claude | The iron frame of the 1851 Crystal Palace, west half (37 of its 77 bays, 888 ft), built by script from Charles Downes's 1852 plates and tested against their figures. An unfinished frame, not a likeness. Files: `crystal-palace-1851.blend`, `crystal-palace-1851.glb`. | [README](crystal-palace-1851-claude/README.md) · [viewer](https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/crystal-palace-1851-claude/) ([fallback](https://htmlpreview.github.io/?https://github.com/nikbearbrown/csye-7270-building-virtual-environments/raw/main/blender/crystal-palace-1851-claude/index.html)) |

## Inside each subfolder

- **`README.md`**: a readable page with every view, the reference comparisons, the film link, downloads, import instructions, stats and limitations.
- **`index.html`**: a self-contained viewer (images embedded) with view buttons, a thumbnail strip and the comparison grid. It works offline after download.
- **`.blend`**: the full Blender scene, with the model, materials, lights and comparison cameras.
- **`.glb`**: a portable export for game engines and web viewers. It carries flat colours only, so procedural wear and panel lines show up in Blender and the renders but not in the GLB.
- **`renders/`**: still renders of the finished model (`renders/web/` has smaller JPEG copies for the pages).
- **`compare/`**: the render beside the reference image, from matching camera angles.
- **`scripts/`**: the Blender Python scripts that generated the model.
- **`BUILD_NOTES.md`**: dimensions, mesh and triangle counts, method, and known limitations.

## seis-bot-grok/ (Grok Bot)

- **Stats:** 1,179 meshes, about 1.48 million triangles, a 50-bone FK rig with finger bones, and 2.21 m tall.
- **Poses:** standing and seated (Thinker), both included in the GLB.
- **Known gaps:** a human review by Professor Bear judged the face badly off, despite Grok Bot rating it "fairly close" against a feature checklist. That gap is the subject of the companion film on why a human needs to stay in the loop. The shoulder armour still reads as a round dome rather than the reference's long sculpted plates.

## jaguar-xkss-1957-grok/ (Grok Bot)

- **Scale:** wheelbase (2,300 mm) and tracks (1,270 / 1,220 mm against the published 1,270 / 1,219 mm) match the real car's specs.
- **Build method:** the body is a single smooth mesh traced from the side profile photo.
- **Grok Bot's self-assessment** (about 4 out of 10 for likeness):
  - The side profile is the closest view.
  - The rear three-quarter view has a too-thin tail and a floating exhaust heat shield.
  - The front is the weakest view: soft wing crowns and frog-eyed headlamps.
- **Reference photos:** Jaguar Classic XKSS press images, used for comparison only.

# Blender builds

Every 3D model Grok Bot builds for this course gets its own subfolder here. Each subfolder has the Blender files, a GLB export, the renders, side-by-side comparisons against the reference images, and the Python scripts that built the model. The models are built entirely in code with Blender's Python API. Folder names are specific to each model (for example `seis-bot`, not `robot`), since many models of the same kind will be added.

To download a single file, open it on GitHub and click **Download raw file**. To get everything, clone the repo or use **Code → Download ZIP**. The `.blend` files open in Blender 4.2 or later.

| Folder | What it is | Main files |
|---|---|---|
| [`seis-bot/`](seis-bot/) | SEIS Bot, an armored humanoid robot with a white 6 on the chest and a worn, distressed finish, built from AI-generated reference images. This is version 4 of 4. | `robot_seated.blend` (Thinker pose), `robot_standing.blend`, `robot_v4.glb` |
| [`jaguar-xkss-1957/`](jaguar-xkss-1957/) | A 1957 Jaguar XKSS (the road-going D-type) in British Racing Green, built from studio photos. First pass, after 8 comparison rounds. | `xkss.blend`, `xkss.glb` |

## Inside each subfolder

- **`.blend`**: the full Blender scene, with the model, materials, lights and comparison cameras.
- **`.glb`**: a portable export for game engines and web viewers. It carries flat colours only, so procedural wear and panel lines show up in Blender and the renders but not in the GLB.
- **`renders/`**: still renders of the finished model.
- **`compare/`**: the reference image beside the render, from matching camera angles.
- **`scripts/`**: the Blender Python scripts that generated the model.
- **`BUILD_NOTES.md`**: dimensions, mesh and triangle counts, method, and known limitations.

## seis-bot/

- **Stats:** 1,179 meshes, about 1.48 million triangles, a 50-bone FK rig with finger bones, and 2.21 m tall.
- **Poses:** standing and seated (Thinker), both included in the GLB.
- **Known gaps:** a human review judged the face badly off, despite Grok Bot rating it "fairly close" against a feature checklist. That gap is the subject of the companion film on why a human needs to stay in the loop. The shoulder armour still reads as a round dome rather than the reference's long sculpted plates.

## jaguar-xkss-1957/

- **Scale:** wheelbase (2,300 mm) and tracks (1,270 / 1,219 mm) match the real car's published specs.
- **Build method:** the body is a single smooth mesh traced from the side profile photo.
- **Grok Bot's self-assessment** (about 4 out of 10 for likeness):
  - The side profile is the closest view.
  - The rear three-quarter view has a too-thin tail and a floating exhaust heat shield.
  - The front is the weakest view: soft wing crowns and frog-eyed headlamps.
- **Reference photos:** Jaguar Classic XKSS press images, used for comparison only.

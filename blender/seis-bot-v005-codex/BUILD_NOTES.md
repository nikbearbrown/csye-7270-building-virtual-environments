# Build notes: SEIS Bot v005 (Codex rebuild)

`1295 mesh objects in the scene (1287 in the source audit) | 2.35 M triangles (scene count) | 14 materials | 49 bones | 8 cameras | 4 lights | about 1.04 x 0.48 x 2.14 m (source audit; the scene also holds a 200 m ground plane) | Blender 5.1.2`

## Provenance

Source: seis-ai-lab/seis-bot/blender/seis-bot-v005-reconstruction/ (copied, originals untouched). Files taken: seis_bot_v005_rebuilt.blend (renamed seis-bot-v005-codex.blend), scripts/, the nine PNG renders (re-saved as 1600 px and 1100 px JPEGs) and review reference frames (used only in compare/).

This is Codex's own model. A separate model, seis-bot-grok, exists in this repo and is not related to or derived from this one.

## What the source says

The source folder records: 18 supplied workshop video frames as primary references; geometry in metres, Z up, forward -Y; an integrity audit with status PASS (names, finite geometry, rigid normalised weights, transforms, materials, triangle integrity; 0 degenerate triangles) that explicitly does not certify visual match; and a list of remaining differences from the reference (see limitations).

## My measurements (count_scene.py on the copied .blend, Blender 5.1.2)

1295 mesh objects, 2,352,011 triangles, 14 materials, 1 armature, 49 bones, 8 cameras, 4 lights; bounding box 200 x 200 x 2.136 m (dominated by the ground plane). Source audit: 1287 evaluated meshes, 2,297,395 triangles, 12 materials, figure bounds 1.045 x 0.485 x 2.136 m.

## Rebuild

`SEIS_OUTPUT="$(pwd)" Blender --background --python scripts/build.py`, then render_final.py, pose.py and audit.py (see scripts/). Note the scripts expect the source folder layout (assets/ fonts, reports/); the Lato fonts are not copied here. export_glb.py produced the .glb.

## Not done

No new render-vs-reference rounds were run for this package; no human review is recorded.

## Built by

- **Builder:** Codex (OpenAI)
- **Method:** Scripted in Blender Python (scripts/build.py plus head, torso, limbs, shoulders, pose, audit modules), rebuilt from Bear's supplied video frames. The source's design report says four integrated on-model rebuilds were rendered and inspected against the frames and repaired; I found no per-round logs, so that count is the source's own claim and I did not verify it. Reference images are not projected onto the model. The builder is identified as Codex from Codex session logs on this machine dated 2026-10-18, not from a label in the source folder.
- **Tools:** Blender 5.1.2 (Cycles, Apple Metal, AgX Medium High Contrast; confirmed by my count_scene.py run and the source's integrity report); Lato font (OFL); Python/Pillow for packaging.
- **Build date:** 2026-10-18 (the .blend was saved 2026-10-18 02:30 local; source manifest 2026-10-18 06:40 UTC)
- **Human review:** Professor Bear: pending. No human verdict is recorded anywhere in the source folder (searched README.txt, reports/, manifest.json, review.html and scripts). The source's own wording is that this is a reconstruction study where visual differences remain.

## Known limitations

- Not a close likeness of the references. The supplied frames show sculpted, layered, enveloping armour with gold edging; this model has flat plates, disc shoulders and smooth glossy surfaces. The source's own report lists the same gaps: shoulders more open and disk-like, face planes more angular with lenses larger than the reference, abdomen with more distinct plates than the flowing reference.
- The .glb has flat base colours only. Procedural Cycles materials (the whole look of the renders) do not export, so it will look plainer than every render here. It was exported for this package with Blender 5.1.2, visible objects only; I re-imported it once to check it opens (1290 meshes, 1 armature).
- The .blend was saved in Blender 5.1.2 and has never been opened in Blender 4.2; it may not open correctly there. Use 5.1 or later.
- Heavy: about 2.35 million triangles in the scene count (the source audit reports 2.30 M evaluated, 1287 meshes; my count includes extra scene objects such as the ground plane and hidden source geometry).
- The scene includes a 200 m ground plane, so the raw bounding box is meaningless; the figure itself is about 2.14 m tall.
- The rig is an FK posing study, not a production animation rig: no IK, facial animation or collision solver. The seated pose lives in a second .blend in the source that is not included here.
- Only five comparison pairs, and angles do not match well; two of them (profile, hands) are poor pairings. Reference frames are AI-generated video frames supplied by Bear, not photographs of a real object.
- Renders are the source's own, not re-rendered for this package.

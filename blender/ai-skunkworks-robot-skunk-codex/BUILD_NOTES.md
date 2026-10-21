# Build notes

151 meshes + 36 curves · 147,860 evaluated triangles · 7 materials · 4.116 × 5.777 × 8.690 design units (XYZ) · Blender 4.2.0 · Codex

## Reference and method

Two supplied PNG line drawings, preserved in `references/`. Reference A is a three-quarter standing view; B is an approximate side view. They are not calibrated orthographic blueprints. Front is −Y, width is X, height is Z. The model uses named editable parts; custom lofts make the muzzle and tail. Armor, joints, knuckles and hydraulic forms are separate meshes. Curves supply cables and panel accents. The mane uses a convex custom silhouette mesh. Material colors are invented for readability, not sampled as design evidence.

## Auditable comparison rounds

1. Draft hero and side renders (`compare/round-01/`). Review found a flat saw-blade crest, buried optical eyes, overly bulbous paired chest plates and small gloves.
2. Revised hero and side (`compare/round-02/`). Convex crest, exposed optics and larger gauntlets improved the read. The paired chest plates became too small and floating; replaced with one broad tapered shield. The crest still reads more like a fan than the drawing.
3. Final six renders and two reference comparisons. The broader chest shield and more side-on hero view show the silhouette and tail better. Recognizable robot-skunk features are present, but organic contours, exact proportions, facial expression and plate shapes remain approximate. Professor Bear has not judged the likeness.

## Validation

Native `.blend` reopened with Blender 4.2.0. GLB reimported: 187 meshes, 147,860 triangles; evaluated native triangle count and dimensions match within 0.0001 design unit. No image textures, skins or animations in GLB. Geometry includes converted native curves. Separate studio excluded. See `audit.json` and `verification.json`. Passing export checks does not establish likeness, printability, animation readiness or manifold topology.

## Known limitations

First interpretation, not a finished likeness. The crest is more fan-like and the face more mechanical than the drawings; the boots are smoother, the armor and glove articulation are simplified, and the pose differs. Black/ivory materials and optical accent colors are proposed because the supplied references are uncolored line art. No rear, front or top drawing establishes depth, so symmetry, rear surfaces and cross-sections are inferred. Arbitrary design units, no verified real-world scale. No rig, animation, working hydraulics or game-ready retopology. Parts overlap; no watertight or 3D-printing suitability claim. Human review: Professor Bear — pending.

Builder: Codex. Method: scripted Blender mesh, curve and loft construction from two user-supplied drawings; three documented visual comparison rounds. Tools: Blender 4.2.0 (Cycles and built-in glTF exporter), Python and Pillow for packaging. Build date: October 21, 2026. Reference drawing authorship was not supplied; reference images provided by Nik Bear Brown. Human review: Professor Bear — pending.

## Reproduce

Run Blender 4.2 in background with `--python scripts/build.py`. Use `-- --draft` for two smaller previews, or omit it for all six final renders. Then run `scripts/verify.py` with Blender and `scripts/package.py` with Python/Pillow. Script paths resolve relative to the package.

## Viewer checks

Opened the self-contained viewer in the browser. Checked view buttons, a thumbnail, arrow-key navigation and dark theme. Narrow 319 px viewport showed wrapping controls and text. Eight embedded JPEG payloads decoded, all local README links resolved, and the HTML is under 1 MB. Full desktop breakpoint automation was not performed.

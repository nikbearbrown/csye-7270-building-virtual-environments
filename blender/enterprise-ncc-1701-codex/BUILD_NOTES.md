# Build notes — Enterprise NCC-1701

270 meshes · 163,798 triangles · 12 materials · 128.0 × 290.3 × 77.192 m (X/Y/Z) · Blender 4.2.0 · Codex

## Source and scope

The user requested a Starship Enterprise through Blender MCP from drawings in the Star Trek folder, then supplied enhanced images. The high-resolution `0001-topaz-denoise.jpg` (12,032 × 3,526 px) was the most useful side reference; its source pixels are preserved as `references/constitution-side-supplied.jpg`. The heavily enhanced 4× small originals were easier to view but contained distorted labels and details. Original general plan, front/rear elevation and nacelle drawings were used for cross-checking. The class drawing says NCC-1700; Enterprise is listed as NCC-1701 on the same sheet. No source mesh, image-to-3D asset or generated picture was used.

Scope: a detailed exterior reconstruction. Interior deck plans informed the overall arrangement but no interiors were built. Palette and illumination are interpretations of monochrome plans. Native units are metres, +Y aft, +Z up, X lateral. Dimensions are chosen reconstruction scale; they are not a canonical-size claim.

## Construction and MCP evidence

Blender 4.2.0 ran in an isolated GUI session. `scripts/start_mcp.py` loaded the pre-existing archived MCP for Blender add-on, bl_info version 1.7, protocol 11. `scripts/mcp_client.py` sent `execute_code` requests through the add-on's localhost port 9876. The Codex tool registry did not expose a Blender tool, so the socket bridge normally used by the stdio MCP relay was called directly. This is disclosed rather than claiming a registered Codex MCP tool.

`build_enterprise.py` makes a contoured revolved saucer, sloped bridge decks, a swept neck, a variable-radius engineering hull loft, diagonal support pylons, longitudinal nacelle shells, hemispherical collectors, copper dish, vents, grilles, segmented hangar doors, windows and registry meshes. Text was converted to mesh and conformed to the saucer surface. Small details and seams are mesh geometry. Pylons overlap the hull shell at their roots; separate components are not boolean-unioned into a single printable solid. Mesh normals were recalculated before export.

The scene includes seven orthographic cameras, four area lights, a world, named components, and a master empty for rigid ship motion. A final `finish_scene.py` pass removed empty collections and unused data and saved an uncluttered material-preview opening view; geometry was unchanged. No animation, bones, collision shapes or LODs exist. Render engine: Cycles, 48 samples, denoising, AgX. Final renders are 1,600 px wide; aspect ratios vary by view.

## Auditable comparison rounds

1. **Initial side/front/hero check.** The main class silhouette was compared to the supplied side and forward elevations. Saucer text partly entered the sloped hull and the collector mesh intersected the pale underlying front shell. Evidence: `compare/round-1/`. Fixed by projecting registry vertices onto the hull surface, removing the overlapping nacelle nose, recalculating normals and adjusting the main camera.
2. **Corrected views and close-ups.** Checked the corrected side/top/front silhouettes and the detailed quarter views. The saucer text and collectors were improved. Close-up review exposed pylon roots sitting slightly above the tapered secondary hull and bridge windows sitting inside the deck shell. Evidence: `compare/round-2/`. Moved pylon roots into the hull, lowered the neck base, and moved bridge panes to the visible surface.
3. **Final exterior review.** Inspected actual final views and side/front/top comparison panels. Pylon connections are continuous at the visible surface, registry is readable and the collector overlap is removed. Overall arrangement is recognizable and follows the main class proportions; it is not a film-miniature match. The bridge and stern profile remain simplified; thin windows and some applied pennants are not exact plan tracings. Human visual acceptance is still pending.

Comparisons are photographic composites of supplied drawing pixels at left and real Blender renders at right. No synthetic evidence. Orthographic projections align view directions; framing and lighting are not identical. Front-reference source is only 450 × 132 px and is visibly enlarged. The side panel preserves the whole sheet, including labels.

## Audit and validation

Read `audit.json`, `glb-structure.json` and `verification.json`. The native scene was reopened independently in Blender 4.2.0. The GLB was then imported into an empty Blender 4.2.0 scene. Mesh count, triangle count, used materials and bounds match; all inspected vertex coordinates are finite. This validates file readability and geometric export consistency, not visual fidelity or animation readiness.

GLB is glTF 2.0, 270 mesh objects, 163,798 triangles, 12 materials, 0 image textures, 0 animations. Geometry carries panel lines, grilles, windows and text. PBR flat colors, roughness, metalness and emission export; `KHR_materials_emissive_strength` is used. Scene cameras, studio lights, world and render settings are excluded. Engine lighting can change its appearance.

## Reproduce

1. Use Blender 4.2+ and an MCP for Blender add-on session listening on localhost:9876. The startup helper records the add-on path used on the build machine; change that path to your installed add-on if needed. Do not load a valuable unsaved scene: the builder clears its active scene.
2. In Blender, set `os.environ['ENTERPRISE_OUTPUT']` to the output directory. Execute `scripts/build_enterprise.py` through `mcp_client.py run /absolute/path/to/build_enterprise.py`. The same file can be run with Blender's `--python` command for reproduction without the MCP transport.
3. Execute `scripts/render_views.py` in the same scene. `ENTERPRISE_VIEWS`, `ENTERPRISE_RESOLUTION` and `ENTERPRISE_SAMPLES` can select view names, percentage and samples. Defaults are all seven views, 100%, and 32 samples; the delivered final run used 48.
4. `scripts/verify_files.py` reopens/imports files when invoked by Blender, and `make_comparisons.py` plus `package_model.py` assemble evidence and documentation with Pillow. Packaging paths reflect this actual build and may be changed for another machine.

## Credit, date and review

Builder: Codex. Created for Nik Bear Brown. Method: scripted Blender mesh construction through the MCP for Blender add-on socket bridge; 3 documented visual comparison/review rounds. Tools: Blender 4.2.0, MCP add-on bl_info 1.7 / protocol 11 (local archived add-on), Python 3.14.6 for packaging, Pillow 12.3.0. Build date: 2026-10-20 (America/New_York). Human review: Professor Bear — pending.

Plans: supplied by Nik Bear Brown; the main sheet credits Franz Joseph Designs and ©1973 Paramount Pictures Corporation. Fan/course reconstruction, not an official asset.

## Remaining limitations

A blueprint-based exterior reconstruction, not a screen-exact studio miniature. Overall proportions were estimated from the supplied views; the 290.3 m length is the chosen working scale, not a verified canonical dimension. Small windows, pennants, grille slats, colors and surface finish are interpretations. The bridge is simplified, the engineering stern is smoother than the plan, and nacelle tail/intercooler details differ. No deck interiors, animated mechanisms, LODs, collision mesh or production rig are included. Separate components are parented to a master transform for rigid movement; this does not constitute animation validation. Human review: Professor Bear — pending.

Companion film: coming soon
<!-- FILM_URL -->

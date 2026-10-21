# Build notes — Planet Express STL assembly

70 visible meshes · 694,382 triangles · 7 materials · 91.39 × 243.94 × 70.97 mm (X/Y/Z) · Blender 4.2.0 · Codex

## Input and scope

The user supplied 26 GOODesign STL files containing 737,487 triangles and 12 reference images. The source kit is credited to GOODesign / GOODesignLabs. Source file hashes are in `source-hashes.json`; reference original filenames, sizes and hashes are in `references/manifest.json`. Source STL filenames and bounds are recorded in `source-audit.json`. The original STL files are not separately duplicated in this package, but the assembled model contains their geometry.

This is a flight presentation. Printed accessories were not all installed. Twelve unused accessory meshes remain in a hidden native collection and are excluded from export. Native numerical coordinates are millimeters, X lateral, Y length and Z up. The audited visible bounds are 91.3865 × 243.9405 × 70.9728 mm. This is the assembled result, not an assertion of fictional full-size ship dimensions or exact physical kit fit.

The creator's listing and portions of the linked assembly video helped interpret the kit. The video was not followed in its entirety. The user images guided palette and visual review. Their appearance differs from the supplied kit, especially in the paneling, fin proportions and engine.

## Construction

Blender 4.2.0 ran in a GUI session with the archived MCP for Blender add-on (bl_info 1.7, protocol 11). The Codex tool registry did not expose a Blender tool; `mcp_client.py` used the same localhost:9876 socket protocol as its MCP relay and sent `execute_code` requests. This was a socket bridge to the add-on, not a registered Codex Blender tool.

The binary STL importer deduplicated exact vertex coordinates. Connected components were split and fitted with scripted matrices, recorded in `assembly-transforms.json`. Hull sections, wings, canopy, engine, rings, portholes, vents and logos use source mesh geometry. The cannon's print-oriented halves were folded into an assembled barrel; six resulting degenerate triangles were omitted during triangulation. Vent depth was compressed to 35% along local Z. These are deliberate modifications, not unmodified archival STL copies. Codex added a slender antenna and mesh PLANET EXPRESS lettering around the source emblems. No generative image model or image-to-3D model was used.

The native scene has a master transform, named component collections, seven presentation cameras, three comparison cameras and studio lights. Cycles renders use 64 samples, denoising and AgX. All final PNGs are 1,600 pixels wide. There is no rig or animation. Separate parts intersect or overlap at some joints and have not been boolean-unioned for printing.

## Three documented review rounds

1. **Hull and source orientation.** Imported parts arrived in print orientations. Hull placement and silhouette were checked against the references before fitting accessories. Saved evidence: `compare/round-1/hull-fit.jpg`.
2. **First complete assembly.** Fitted components and compared the assembled quarter view. Review exposed reversed/mirrored emblem orientation, cannon half-shell layout and protruding hardware. Adjusted those transforms, folded the cannon, compressed vent depth and added readable lettering. Saved evidence: `compare/round-2/assembly.jpg`.
3. **Final views and comparisons.** Rendered seven final views and three focused comparison cameras. Inspected the front, aft and turret panels. The assembly is recognizable but not a close surface match: kit panel grooves are pronounced; cockpit and vents are imperfectly seated; portholes protrude; the engine has more openings than the reference. Camera and illumination differences remain. The evidence does not support a claim of exact likeness.

These are the three documented rounds, not a count of every intermediate render experiment. Human acceptance is pending. Reference pixels are preserved; comparison panels only resize/place images and add factual captions.

## Audit and export verification

`audit.json` records 70 visible meshes, 694,382 triangles, 7 used materials and 12 hidden accessory meshes. Dimension measurements use transformed actual vertices, not rotated object bounding boxes. All checked vertex coordinates are finite. `verification.json` records independent native reopening and GLB import in Blender 4.2.0, with equal mesh/triangle/material counts and equivalent bounds after millimeter-to-meter conversion. This validates file readability and export consistency, not mechanical assembly, visual acceptance, manifoldness or animation readiness.

The GLB contains 7 flat PBR materials and no image textures. Panel grooves, emblems and lettering are mesh geometry and survive export. Cameras, studio lights, world and render settings are excluded. GLB units are meters; the native scene displays millimeters. The master transform supports rigid placement only.

No image textures, bones or animations are present in the GLB. Its 0.091387 × 0.243940 × 0.070973 meter dimensions match the visible native assembly. Hidden accessories are intentionally omitted. See `glb-structure.json` for the container audit.

## Reproduction

The scripts are the actual files used for this build and contain absolute source/output paths. Edit those paths to match your machine. Start with a new empty Blender 4.2+ scene, and retain separate backups of any valuable scene.

Run `import_inspect.py`, then optional `components.py` and `assemble_draft.py` for inspection. Run `split_parts.py`, `assemble_ship.py`, `finish_render.py`, `export_audit.py`, and `render_comparisons.py` in that order in the same Blender session. Send them with `python3 scripts/mcp_client.py run /absolute/path/to/script.py` against an already running MCP add-on. Alternatively execute the Blender scripts directly inside Blender. Do not split an already split scene again. The source files must be available in their original directory or the paths adjusted.

Run Blender in background with the saved final `.blend` and `--python scripts/verify_files.py` for independent file checks. `package_model.py` makes the documentation, comparison panels and offline gallery using Pillow; it records the original build paths and reused gallery template path. It is a packaging record rather than a standalone portable installer. The kit itself is the original author's work.

## Credit and review

Builder: Codex, for Nik Bear Brown. Original mesh geometry: GOODesign / GOODesignLabs. Method: scripted STL assembly and material assignment through the Blender MCP add-on socket bridge, with added antenna and mesh lettering; 3 documented comparison rounds. Tools: Blender 4.2.0, MCP add-on bl_info 1.7 / protocol 11, Python 3.14.6, Pillow 12.3.0. Build date: 2026-10-20 (America/New_York). Human review: Professor Bear — pending.

Original kit: GOODesign / GOODesignLabs, Planet Express Ship – FUTURAMA. Reference images supplied by Nik Bear Brown. This is an assembly study of that kit, not original geometry authored entirely by Codex or an official Futurama asset.

Creator listing: https://thangs.com/designer/GOODesign/3d-model/Planet%20Express%20Ship%20-%20FUTURAMA-1510142

Assembly video: https://www.youtube.com/watch?v=Jqm8zHlQoqY

## Remaining limitations

This is a static flight assembly of the supplied kit, with approximate fitting of several parts. Its long fins, deep panel grooves, cockpit and multi-nozzle engine differ visibly from the smoother reference ship. The vents and portholes protrude more, and some trim and canopy seams remain imperfect. It is recognizable as Planet Express, but is not an exact match to the reference. Twelve accessory meshes, including unused landing and stand parts, remain hidden in the native scene and are excluded from the GLB. No mechanism rig, animation, collision mesh, LOD or print-fit certification is included. Human review: Professor Bear — pending.

Companion film: coming soon
<!-- FILM_URL -->

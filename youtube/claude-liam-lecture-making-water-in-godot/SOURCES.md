# Sources: Making Water in Godot

**What this is.** What the film is built from, with addresses and dates, what was deliberately not stored, and who is credited for what.
**Why.** The arc of the film was proposed by a third-party Unity video. The film follows its order of ideas and teaches them in new words, in another engine, with new shaders and new measurements; this file records that nothing was copied and what each idea's real origin is.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2; every number on screen is a run recorded in `evidence/planning-checks/`. The Unity video is a third-party work whose creator Bear has not named; its transcript was not saved anywhere and none of its wording, jokes, sponsor material or Unity steps is used. The one existing water shader in Bear's repositories (`walker-compute-texture`) was checked for provenance and not used.

## Bear's request (2026-10-16, verbatim)

"I think this shader film, even though it's in Unity, is a good sort of template for Godot. It makes a slightly more complicated shader, it has pretty much all the aspects of making a shader. First, we make the water blue, then we make it a little transparent, then we use some noise to add some foam to it, and then we use some UV manipulation and normal maps to give it a wavy effect. So use this as a model to create another shader for Godot. On making a water shader with Godot."

## Third-party source followed for the progression only (not copied)

- **A Unity Shader Graph water tutorial** (a YouTube video with sponsor reads; the creator is not named in the material Bear passed on). The film follows its ORDER only: a plane, a shader and a material; a base blue as a property; ripples from a cellular noise whose points move with time (density and speed as properties); a power curve to sharpen the cell edges; a brighter colour on top and alpha lowered to about 0.8; a second distortion on the noise's UV; a vertex displacement of the plane from a scrolled noise with a floating object bobbing; reflections, refraction and intersection foam named as further steps.
- **Not stored.** No transcript or text of the video was saved to this folder or anywhere in the repository; Bear's own summary of the arc is quoted above and in `ACTS.md`. No sentence was reused. Every demonstration (the blend arithmetic, the cellular function, the normal-map stages, the wave and the floaters, the shore foam) was written for Godot and run.
- **Where the film differs on purpose.** Alpha 0.7, not 0.8 (the rocks stay visible); the foam is opaque and matte rather than brighter-and-translucent; the waves are two sines with an analytic normal (not a scrolled noise) because the floating objects' script must run the same function; the film adds the depth-based shore foam (the video's last named step) and the Inspector.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film names them.

## Primary

- **Godot 4.7 documentation** (docs.godotengine.org/en/stable), read 2026-10-16 as raw page HTML converted to plain text (kept in the session scratch only for quoting in `FACTCHECK.md`; not stored in the repository): `tutorials/shaders/shader_reference/spatial_shader.html` (render modes, ALPHA, NORMAL_MAP, VERTEX, TIME, the transparency note), `shading_language.html` (hints, `group_uniforms`, functions), `shader_functions.html` (`pow`, `smoothstep`, `mix`, `fract`, `length`, `dot`, `clamp`), `tutorials/shaders/advanced_postprocessing.html` (the depth texture recipe, the Compatibility NDC note, `CURRENT_RENDERER`), `tutorials/shaders/introduction_to_shaders.html` (shader types, `vertex()` and `fragment()`), `tutorials/3d/3d_rendering_limitations.html` (transparency sorting), `classes/class_planemesh.html`, `class_noisetexture2d.html`, `class_fastnoiselite.html`, `class_meshinstance3d.html`, the class index (visual shader nodes).
- **The installed engine:** Godot 4.7.2 stable (official), Apple M4 Pro, macOS, Metal (Forward+) and OpenGL on Metal (Compatibility). The renderer is stated wherever a pixel value is shown.
- **The series' glossary** (`../_godot-shaders-series/GLOSSARY.md`) for every on-screen definition; **the series Shader Lab** (`../_godot-shaders-series/lab/`) for the harness; **the series editor driver** (`../_godot-shaders-series/editor-capture/`) for the Inspector frames.

## Algorithms and idioms (credited, none copied from a video)

- **Cellular noise** is Steven Worley's 1996 algorithm (a point per grid cell, distances to the nearest points); the 3 by 3 neighbour search and the nearest and second-nearest distances are the standard form. The film's code is written for this film.
- **The hash** `fract(sin(dot(p, k)) * 43758.5453)` is a long-standing community idiom (it appears in many shader tutorials and articles, among them Inigo Quilez's cellular-noise write-up). It is not a cryptographic or portable hash: sines of large numbers can differ between graphics cards (not tested here; the film does not claim otherwise). The constants are the usual ones.
- **The depth reconstruction** (screen point, inverse projection matrix, divide by w, negate z) is the recipe in Godot's own documentation (page listed above); the film cites it and runs it.
- **Sum-of-sines waves** with an analytic normal are the textbook form of a simple ocean surface; the specific constants (directions, 0.6 ratios) are this film's.

## Checked and not used

- **`walker-compute-texture/godot/water_plane/water_shader.gdshader`** (Bear's repository): a Walker adaptation of Godot's `compute/texture` demo (a compute shader rewrites a height texture every frame; the material turns it into ripples). Provenance read in its README and `LICENSE.md`: an independent local adaptation of the Godot `compute/texture` demo under the Godot contributors' MIT licence, with the water effect script credited to Bastiaan Olij. It is a different technique (a simulated height field) and needs a RenderingDevice; this film's water uses no simulation, so none of its files is used or copied.

## What this film's pictures come from

Every Godot picture is a Shader Lab harness render (`../_godot-shaders-series/lab/capture_shader.sh`) of a scene built by `capture-scenes/water_scene.gd` (or `gap_scene.gd`, or the evidence scene scripts) from `water-project/scripts/cove_builder.gd`, wearing a tested file in `lab-shaders/`; scripts, raw logs, frames and measured numbers are in `evidence/planning-checks/` (`RESULTS.md` is the index). The Inspector frames are a scripted editor session of the real Godot 4.7.2 editor (`captures/editor/`, `evidence/planning-checks/EDITOR-LABELS.md`). Failed and inconclusive runs are kept and labelled in `RESULTS.md`: the first `pow` demonstration (black specks with moving points: 88 pixels), the fractal-smeared cellular texture, the `INV_PROJECTION_MATRIX` helper error, and the first, wrongly decoded Compatibility depth reading.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab, the editor driver and scratch scenes), Python with Pillow and numpy for pixel measurements, ffmpeg, Manim for the drawings; no paid generation, no model calls from inside the build.

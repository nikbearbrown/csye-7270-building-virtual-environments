# PBR in Godot, course track: series plan (2026-11-13, awaiting Bear's go-ahead to build)

**Executive summary:** Six more CSYE 7270 teaching films that carry on from the three PBR films already built (What Is PBR?, Why PBR Matters, PBR Textures Are Data, Not Pictures). The series thesis comes from the research draft: in Godot, PBR *materials* are the default but physically based *lighting* is opt-in. This track is Godot-only, shows no shading-language code, and is built with the `lecture` skill in the same form as the first three films. Every material and light on screen is a real Godot 4.7.2 render or a real record from the course's own Walker builds. PBR is off the Fall 2026 exam, so these are class material. The public "coming from Unity or Unreal" track waits until this one is done.

## Why the course track looks different from the draft

- **Course projects run on the Compatibility renderer.** Walker Jumpman and walker-jumpman-clawd are both `gl_compatibility` (Chapters 1, 2 and 6), and web export only works on Compatibility. So the renderer film comes first, and every later film says what a Compatibility project actually gets.
- **No Unity or Unreal on this Mac**, and films only show what was actually done. Comparisons stay out of the course track, as the course already handles them in each chapter's "Doing the same thing in Unity / Unreal" section.
- **No 4.6/4.8 claims on screen** unless checked. Only Godot 4.7.2 is installed; the draft's 4.8 features (node groups, contact shadows, multi-bounce AO, alpha-preserving mipmaps) are left out or named as "coming in 4.8" without a demo.
- **No numbers on screen.** The order below is internal; titles and cards carry no film numbers. No runtime targets: each film runs as long as it needs.

## Viewing order (internal)

Already built: What Is PBR? → Why PBR Matters → PBR Textures Are Data, Not Pictures. Then:

| Working title | One line | What the viewer sees (real evidence) | Sources |
|---|---|---|---|
| Pick Your Renderer Before Your Material | Godot's three renderers decide which lighting exists at all; your materials look the same in all three, the light around them does not. | One lab scene rendered in Forward+, Mobile and Compatibility (`--rendering-method`), each missing feature named as it disappears; the course's own `project.godot` lines showing `gl_compatibility`. | Godot "Overview of renderers" (checked 11-13: SSR, SSIL, SDFGI, VoxelGI, volumetric fog, TAA are Forward+ only; decals not in Compatibility; SSAO not in Mobile; reflection probes 2 / 8 / unlimited per mesh; web needs Compatibility; switching renderers needs "manual tweaks"); Chapters 1, 2, 6 |
| StandardMaterial3D, Slot by Slot | The default lit material, group by group, and the transparency modes that trip people up. | The real Godot inspector (captured, not drawn) on the lab sphere; then the Poly Haven ship's sails: alpha scissor set on a JPEG that has no alpha (`FORMAT_RGB8`, chapter's F-2 finding), shown in a render; alpha blend vs scissor vs hash on the same leaf card, with and without shadows. | Godot Standard Material 3D docs; Chapter 7 (ship audit, transparency settings); public `walker-3d-graphics-settings` |
| Texture Import Is Half the Material | Most materials that "look wrong" were imported wrong. | Chapter 7's real ship records: nine textures imported Lossless (the 2D default), "Detect 3D" that only fires when the editor draws (headless reimport left the `.import` files byte-identical); lab renders of mipmaps off vs on (distant shimmer) and a DirectX-style normal map with and without Invert Y. | Godot "Importing images"; Chapter 7 "Texture import" and "What we actually ran"; `examples/07-materials-and-textures/logs` |
| Turning On the Physics: Light Units, Camera, Falloff | Godot's lights are tuned for ease, not physics, until you switch them over. | Verified 4.7.2 defaults on screen (omni and spot attenuation 1.0, omni range 5.0, physical light units off); one lamp at attenuation 1.0 vs 2.0 with the range cutoff visible; physical units on: a 50-lux room vs a 100,000-lux exterior through one physical camera; a 13-lumen candle vs an 800-lumen bulb. | Godot "Physical light and camera units" (checked 11-13: lux, lumens, nits; focal length overrides FOV; DoF enforced on the GPU; "will not automatically make your project look better"); OmniLight3D docs ("Use a value of 2.0 for physically accurate lights") |
| Indirect Light: Sky, Probes and the GI Choice | Direct light is only half the picture; how Godot fills in the rest depends on your renderer and your scene. | Sky as ambient and reflected light; a ReflectionProbe on and off; the public `walker-3d-global-illumination` map under LightmapGI, VoxelGI and SDFGI with a frame-time readout (this also does the GPU viewing its own record lists as unverified); SSAO switched off while judging texture AO (Chapter 7's rule). Which of these a Compatibility project can use. | Godot "Introduction to global illumination"; Chapter 7 GI table; renderer table |
| How Do You Know It's Right? | Test the renderer instead of trusting it. | A furnace test (white spheres of rising roughness in a uniform white sky, brightness measured); the same roughness × metallic grid in Godot and Blender Cycles under one HDRI and exposure, with a difference image (Blender is installed); and Chapter 7's real case: an agent's test passed 100 checks on a hull whose AO was switched off, and only a headless probe told "subtle" from "absent". | Chapter 7 "What we actually ran"; physicallybased.info; local Blender + Godot runs |

## What carries over from the three built films

- The same evidence rig (`_pbr-evidence`), grown into the draft's "PBR Lab" project: one Godot 4.7.2 project, one scene per film, captures sized to each beat's narration.
- The same cast: terracotta sphere family, tile texture set, the three lighting presets (noon, sunset, dim blue room). The sphere grid already rendered is reused in the renderer film.
- The same gate fixes learned today: scene classes named `B##_Name(Scene)`; no thin terracotta rings around text; no `Difference()`; ShaderLab contrast judged on the heading.

## Needed before building (Bear's call)

1. **Clone two public Walker repos** (`walker-3d-graphics-settings` for the ship, `walker-3d-global-illumination` for the GI map) from github.com/nikbearbrown. Both are Bear's own public, MIT-licensed builds; the ship is Poly Haven CC0.
2. **Capture the Godot editor** for the StandardMaterial3D film. macOS may ask for screen-recording permission the first time.
3. **Disk.** About 250 MB per film; check before each render.

## Left for the public track

Same Math, Different Defaults (three-engine comparison) · VisualShader Is ShaderGraph · From Graph to Code · Material Architecture Without Instances · Area Lights · Exposure and Tonemapping · The `light()` Function · Post-processing and Stencil · Porting a Scene End to End. These need Unity and Unreal captures (not installed here) and show shader code.

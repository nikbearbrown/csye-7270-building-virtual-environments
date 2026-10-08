# Module 7 — Helpful links

## Executive summary

This page collects the readings, Godot documentation, Walker projects and tools for Module 7, Materials and textures. Open it when you need the official reference behind a material slot, an import setting or a licence, or when you are auditing an asset and want to check an agent's claim.

## Read first

- [Chapter 7 — Materials and Textures](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/07-materials-and-textures.md) — the long reading behind this module: the full audit-and-change run, what each agent got wrong, and the Unity and Unreal comparison.
- [The reviewed ship audit (MATERIALS.reviewed.md)](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/07-materials-and-textures/files/MATERIALS.reviewed.md) — the agent's audit of the Dutch ship after human review; open it to see what a checked materials table looks like before you write your own.

## Godot documentation

- [Standard Material 3D and ORM Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — the guide to each material slot, texture channel and flag, including the ORM texture layout.
- [BaseMaterial3D class reference](https://docs.godotengine.org/en/stable/classes/class_basematerial3d.html) — exact property names and defaults such as `ao_light_affect`, alpha scissor and cull mode.
- [Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html) — compression modes, mipmaps and the 2D-versus-3D import defaults that the `.import` file stores.
- [Advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html) — the per-material Use External and Extract Materials options used to give the hull an external material.
- [Using decals](https://docs.godotengine.org/en/stable/tutorials/3d/using_decals.html) — what a `Decal` can project and the renderer and shader limits to know before designing around one.
- [Introduction to global illumination](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/introduction_to_global_illumination.html) — the lighting techniques that decide what a material can show, with their renderer support.

## Walker projects

- [walker-3d-graphics-settings](https://github.com/nikbearbrown/walker-3d-graphics-settings) — the settings-menu demo with the Poly Haven ship used in this module's audit; open `godot/polyhaven/` for the ship and its textures and `godot/test_settings.gd` for the 17-check harness. It is an adaptation of a Godot demo and keeps the upstream MIT licence.
- [walker-3d-decals](https://github.com/nikbearbrown/walker-3d-decals) — decals with albedo, normal, ORM and emission textures from four assets under three licences (CC0, CC-BY 3.0, CC-BY-SA 3.0); open its README for the attribution list.
- [walker-3d-global-illumination](https://github.com/nikbearbrown/walker-3d-global-illumination) — VoxelGI, SDFGI, LightmapGI and reflection probes on one map; open it to compare lighting techniques and read its record of what is still unverified.
- [walker-compute-texture](https://github.com/nikbearbrown/walker-compute-texture) — a texture written every frame by a compute shader; open its README and `FRICTIONAL.md` for its record of what the headless checks found and what they could not show.
- [walker-compute-heightmap](https://github.com/nikbearbrown/walker-compute-heightmap) — an island heightmap generated from noise on the CPU or with a compute shader; open it for the out-of-range gradient finding and its fix.

## Tools

- [Godot download page](https://godotengine.org/download/) — choose the regular editor, not the .NET build; the runs behind this module used Godot 4.7.2, so record your version.
- [Claude Code quickstart](https://code.claude.com/docs/en/quickstart) — installing Claude Code and starting a first session.

## Going deeper

- [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html) — the format the ship arrives in; its material section fixes which textures are sRGB colour and which are linear data.
- [Poly Haven: Dutch Ship Medium](https://polyhaven.com/a/dutch_ship_medium) — the asset page for the model in this module, with its credits, licence and texture files.
- [Poly Haven licence](https://polyhaven.com/license) — the CC0 terms the ship is released under, and what they do and do not require of you.

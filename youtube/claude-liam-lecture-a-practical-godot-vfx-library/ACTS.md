# ACTS.md — A Practical Godot VFX Library

Source: Chapter 9 — "Particle Effects" (CSYE 7270 Building Virtual Environments)
Sections covered: demo scenes, CPU/GPU conversion, Unity/Unreal comparison, .tres pattern

---

## Coverage map

| Chapter section | Film section |
|---|---|
| "Two more places to read particle work" — the demo scenes | ACT 1 |
| "Four node types, two families" — conversion, Compatibility renderer | ACT 2 |
| "Doing the same thing in Unity / Unreal" | ACT 3 |
| walker-3d-platformer particle_material.tres | ACT 4 |

---

## ACT 1 — The Godot Catalog (B01–B03)

Beats: B01 · B02 · B03

The godot-demo-projects repository ships two particle scenes — `2d/particles` and `3d/particles` — that function as feature catalogues. Neither is a game. Neither has a Walker adaptation. But both are readable .tscn text files an agent can trace. The 2D catalog has 17 GPUParticles2D nodes on the Mobile renderer. The 3D catalog uses Forward+ to show trails, attractors, SDF collision, and sub-emitters in a single scene. The three-part emission/process/draw frame is the organizer: it tells you what to carry when you port an effect from a catalog into your project.

---

## ACT 2 — Node Conversion (B04–B06)

Beats: B04 · B05 · B06

The Godot editor can convert between CPU and GPU particle nodes. CPU→GPU is additive: the conversion gains access to sub-emitters, trails, and shaders, and the emission settings move into a new ParticleProcessMaterial. GPU→CPU is lossy: sub-emitters, trails, and shaders cannot survive. Compatibility renderer limits matter for any library effect that targets wide hardware: particle trails and SDF collision are unsupported; emit_particle() requires Forward+ or Mobile.

---

## ACT 3 — Cross-Engine Map (B07–B09)

Beats: B07 · B08 · B09

Unity's two particle systems (Built-in CPU / Visual Effect Graph GPU) map to Godot's two families. The Built-in serializes as YAML — readable. VFX Graph assets are binary .vfx files — not diffable as text. Unreal's Niagara uses one system with CPU/GPU selectable per emitter; its .uasset format is also binary. The practical agent difference: a Godot agent can read and verify a particle configuration from the .tscn file. Unity and Unreal agents cannot read the full effect stack from a file.

---

## ACT 4 — Building Your Library (B10–B12)

Beats: B10 · B11 · B12 (GodotDevWorkbench)

The .tres pattern from walker-3d-platformer keeps the draw half in one reusable file. Three effects share particle_material.tres; change one file, all three update. A practical library entry has a name, a renderer requirement, a node type (CPU or GPU), a reference to a .tres draw material, and a test status. The GodotDevWorkbench beat shows particle_material.tres as the editor displays it: four flags, shared across three effects.

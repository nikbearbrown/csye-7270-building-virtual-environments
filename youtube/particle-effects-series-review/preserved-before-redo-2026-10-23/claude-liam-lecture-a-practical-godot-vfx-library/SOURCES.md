# SOURCES.md — A Practical Godot VFX Library

## Primary

| Source | What it provides |
|---|---|
| Chapter 9 — `09-particle-effects.md` | Demo scene catalog, CPU/GPU conversion, node type table, Unity/Unreal comparison, .tres pattern |
| Godot 4.7.2 docs — 2D particle systems | CPU→GPU conversion button, Compatibility renderer limits, CPUParticles2D "no plans to add features" |
| Godot 4.7.2 docs — 3D particle systems | Feature comparison, CPU wider hardware, GPU-only features |
| Godot 4.7.2 docs — Renderers comparison | Particle trails unsupported on Compatibility; SDF collision Forward+/Mobile only |
| Godot 4.7.2 class ref — GPUParticles2D / 3D | sub_emitter, trail_enabled, emit_particle() renderer requirement |
| Godot 4.7.2 class ref — CPUParticles2D / 3D | No sub_emitter, no trail_enabled, no particle shader |
| godot-demo-projects at commit a3b5c113 | `2d/particles` (17 GPUParticles2D, Mobile renderer), `3d/particles` (Forward+) |
| walker-3d-platformer source | particle_material.tres: StandardMaterial3D with additive, unshaded, billboard_particles, proximity_fade |
| Unity docs (checked 2026-09-27) | Built-in Particle System YAML format, VFX Graph binary .vfx, Sub Emitters module, OnParticleSystemStopped |
| Unreal Engine docs (checked 2026-09-27) | Niagara Sim Target, .uasset binary format (Perforce page), events CPU-only, OnSystemFinished |

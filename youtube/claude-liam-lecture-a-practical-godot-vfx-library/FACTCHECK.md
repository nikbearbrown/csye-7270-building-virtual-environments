# FACTCHECK.md — A Practical Godot VFX Library

All claims verified against Chapter 9 text and cited sources.

| Claim | Source | Status |
|---|---|---|
| 2d/particles demo: 17 GPUParticles2D nodes, Mobile renderer, commit a3b5c113 | Ch. 9 "Two more places to read particle work"; [godot-demo-projects] | ✅ |
| 3d/particles demo: Forward+ renderer, has collision / attractors / trails / sub-emitters | Ch. 9 "Two more places to read particle work"; [godot-demo-projects] | ✅ |
| Neither 2d/particles nor 3d/particles has a Walker adaptation | Ch. 9 "Two more places to read particle work" | ✅ |
| Editor can convert CPUParticles2D → GPUParticles2D via 2D toolbar | Ch. 9 "Four node types"; [2D particle systems docs] | ✅ |
| CPU→GPU conversion: emission settings move into new ParticleProcessMaterial | [GPUParticles2D class ref; CPUParticles2D class ref] | ✅ |
| GPU→CPU: sub_emitter / trail_enabled / particle shaders cannot survive | Ch. 9 Table "Four node types"; [class refs] | ✅ |
| Compatibility renderer: particle trails unsupported | Ch. 9 "Four node types"; [renderers comparison] | ✅ |
| Compatibility renderer: SDF collision unsupported | Ch. 9 "Sub-emitters"; [renderers comparison] | ✅ |
| emit_particle() requires Forward+ or Mobile | Ch. 9 "Four node types"; [GPUParticles2D class ref] | ✅ |
| Unity Built-in Particle System: CPU-simulated, YAML format | [Unity docs: choosing a particle system; asset metadata] | ✅ |
| Unity VFX Graph: GPU-simulated, .vfx binary files (not text-diffable) | [Unity docs: VFX Graph; Unity source control] | ✅ |
| Unreal Niagara .uasset: binary, cannot be opened as text | [Unreal docs: Perforce and Unreal source control] | ✅ |
| Niagara Sim Target selects CPU or GPU per emitter | [Unreal docs: emitter settings] | ✅ |
| Niagara events (sub-emitter equivalent) work CPU simulation only | [Unreal docs: events and event handlers in Niagara] | ✅ |
| Godot sub-emitters are GPU only | Ch. 9 "Sub-emitters" | ✅ |
| walker-3d-platformer particle_material.tres: StandardMaterial3D with additive, unshaded, billboard_particles, proximity_fade | Ch. 9 "Two more places to read"; walker-3d-platformer source | ✅ |
| particle_material.tres shared by coin burst, enemy explosion, bullet glow via material_override | Ch. 9 "Two more places to read"; walker-3d-platformer source | ✅ |
| A Godot .tscn file contains particle node configuration and process material in plain text | [Godot .tscn file format docs; walker-3d-platformer coin.tscn] | ✅ |

**No unchecked claims in the film.**

# FACTCHECK.md — Building 3D Particle Effects in Godot

All claims verified against Chapter 9 text and cited sources.

| Claim | Source | Status |
|---|---|---|
| walker-3d-platformer uses CPUParticles3D for coin burst, enemy explosion, bullet glow | Ch. 9 "Two more places to read particle work" | ✅ |
| Coin burst: 16 particles, one-shot, explosiveness=1, sphere emission, lifetime=0.5, lifetime_randomness=0.2 | Ch. 9 "Two more places to read" | ✅ |
| particle_material.tres is StandardMaterial3D with additive blending, unshaded, particle billboarding, proximity fade | Ch. 9 "Two more places to read" | ✅ |
| Animation track keys CPUParticles3D:emitting to true at time 0 for coin and enemy | Ch. 9 "Triggering: a particle node is a node" | ✅ |
| GPU nodes: sub_emitter exists; CPU nodes: no sub_emitter | Ch. 9 Table "Four node types" | ✅ |
| GPU nodes: trail_enabled exists; CPU nodes: no trail | Ch. 9 Table; [3D particle systems docs] | ✅ |
| Particle shaders: GPU nodes only; shader_type particles | Ch. 9 "Particle shaders"; [particle shaders docs] | ✅ |
| sub_emitter_mode enum on 4.7.2: DISABLED, CONSTANT, AT_END, AT_COLLISION, AT_START | Ch. 9 "Sub-emitters" | ✅ |
| Sub-emitter surprises: (1) stops own emitting; (2) amount capped; (3) no self-sub | Ch. 9 "Sub-emitters"; [sub-emitters docs] | ✅ |
| Particle shader: start() / process() functions; writes TRANSFORM, VELOCITY, COLOR, ACTIVE | Ch. 9 "Particle shaders"; [particle shaders docs] | ✅ |
| RESTART_POSITION, RESTART_VELOCITY true for newly emitted particle | Ch. 9 "Particle shaders"; [particle shaders docs] | ✅ |
| Headless dummy renderer compiles shader source; type error `VELOCITY = vec2(1.0)` caught | Ch. 9 "Particle shaders" (probes/shader_probe*.gd) | ✅ |
| CPUParticles3D: "no plans to add new features" (same as 2D note) | [3D particle systems docs] | ✅ |
| visibility_aabb: 3D bounding box for simulation culling | Ch. 9 "Where particle cost lands"; [class ref] | ✅ |
| Overdraw from transparent overlapping quads costs fill rate on mobile | Ch. 9 "Where particle cost lands"; [GPU optimization] | ✅ |
| AT_COLLISION requires SDF collision, Forward+ or Mobile renderer | Ch. 9 "Sub-emitters"; [sub-emitters docs] | ✅ |

**No unchecked claims in the film.**

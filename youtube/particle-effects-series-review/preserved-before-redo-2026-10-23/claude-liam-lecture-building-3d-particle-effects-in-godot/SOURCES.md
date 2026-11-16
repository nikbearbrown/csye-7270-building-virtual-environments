# SOURCES.md — Building 3D Particle Effects in Godot

All claims in this film are sourced from the following primary references.

## Primary

| Source | What it provides |
|---|---|
| Chapter 9 — `09-particle-effects.md` | walker-3d-platformer source, coin burst / enemy explosion / bullet glow configs, animation track triggers, sub-emitter docs, particle shader, cost levers |
| Godot 4.7.2 class reference — CPUParticles3D | Property list, emission shapes, no sub_emitter / no trail_enabled confirmation |
| Godot 4.7.2 class reference — GPUParticles3D | sub_emitter, trail_enabled, process_material docs |
| Godot 4.7.2 docs — 3D particle systems | "work on a wider range of hardware" / "no plans to add new features" to CPUParticles |
| Godot 4.7.2 docs — Particle shaders | shader_type particles; start()/process(); TRANSFORM/VELOCITY/COLOR/ACTIVE built-ins; RESTART_POSITION / RESTART_VELOCITY |
| Godot 4.7.2 docs — Sub-emitters | sub_emitter_mode enum (DISABLED/CONSTANT/AT_END/AT_COLLISION/AT_START); AT_COLLISION needs SDF; stops own emitting; Amount capped; no self-sub |
| Chapter 9 probes — `shader_probe*.gd` | Headless compile evidence: valid shader → OK; VELOCITY=vec2(1.0) → ERROR |
| Godot 4.7.2 docs — GPU optimization | Overdraw from transparent overlapping quads; fill rate on mobile |

## Walker-3d-platformer source

| Claim | File |
|---|---|
| Coin burst: CPUParticles3D, amount 16, one_shot, explosiveness 1, sphere, lifetime 0.5, randomness 0.2 | `walker-3d-platformer/godot/coin.tscn` |
| Enemy explosion: CPUParticles3D, amount 16, mesh particles | `walker-3d-platformer/godot/enemy.tscn` |
| Bullet glow: CPUParticles3D, amount 16, lifetime 0.4, looping | `walker-3d-platformer/godot/bullet.tscn` |
| Animation track keys emitting at t=0 for coin take and enemy explode | `walker-3d-platformer/godot/coin.tscn`, `enemy.tscn` |
| particle_material.tres: additive, unshaded, billboard_particles, proximity_fade | `walker-3d-platformer/godot/particle_material.tres` |
| visibility_aabb used for culling in Chapter 9 cost discussion | Ch. 9 "Where particle cost lands" |

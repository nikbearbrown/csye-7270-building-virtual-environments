# SOURCES.md — Adding Particle Effects to Walker Claude

## Primary

| Source | What it provides |
|---|---|
| Chapter 9 — `09-particle-effects.md` | Death burst build, three agent sessions, lambda bug, cost measurement, headless limits |
| Godot 4.7.2 docs — GPUParticles2D class ref | null texture = 1×1px squares; emit_particle() renderer limit; finished signal |
| Godot 4.7.2 docs — ParticleProcessMaterial | particle_flag_disable_z; spread; sub-emitter modes |
| Godot 4.7.2 docs — 2D particle systems | CPU→GPU conversion; Disable Z note from official demo README |
| Godot 4.7.2 docs — renderers comparison | trails/SDF collision unsupported on Compatibility |
| GDScript basics — lambda functions | "cannot reassign an outer local variable" — lambda capture by value |
| Godot source — core/os/os.cpp + main/main.cpp | low_processor_mode_sleep_usec default 6900 µs; fixed-FPS early return |
| walker-2d-dodge-the-creeps source | main.tscn, player.gd, game_over() structure |
| walker-3d-platformer source | coin.tscn, enemy.tscn — animation-track triggers |
| Unity docs (checked 2026-09-27) | one_shot → Looping off; finished → OnParticleSystemStopped; YAML format |
| Unreal Engine docs (checked 2026-09-27) | Loop Behavior Once; OnSystemFinished; .uasset binary format |
| Ch. 9 probe logs | delta_probe.gd; particle_cost.gd; fixed-fps cost table |

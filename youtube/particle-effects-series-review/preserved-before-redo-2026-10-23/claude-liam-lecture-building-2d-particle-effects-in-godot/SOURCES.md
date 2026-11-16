# SOURCES.md — Building 2D Particle Effects in Godot

## Primary source

Chapter 9 — Particle Effects, CSYE 7270: Building Virtual Environments.  
All session logs, test output, and cost measurements are from the chapter record: `examples/09-particle-effects/` (27 Sep 2026, Apple M4 Pro, Godot 4.7.2).

## Godot documentation (all stable = 4.7, accessed via chapter)

- [GPUParticles2D class reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html)
- [CPUParticles2D class reference](https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html)
- [ParticleProcessMaterial class reference](https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html)
- [2D particle systems tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html)
- [GDScript basics — lambda functions](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)
- [Renderers — feature comparison](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)

## Godot source (via chapter)

- [`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp) — `OS::add_frame_delay`, `low_processor_mode_sleep_usec` default 6900
- [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp) — early return from frame loop on fixed FPS

## Godot demo projects (commit a3b5c113, MIT)

- `2d/dodge_the_creeps` — walker-2d-dodge-the-creeps source
- `2d/particles` README — "Disable Z" flag recommendation for 2D
- `3d/platformer` — CPUParticles3D coin/enemy examples

## Walker repositories (public, MIT)

- [walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps)
- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer)

## Background

- W. T. Reeves, "Particle Systems—A Technique for Modeling a Class of Fuzzy Objects," *ACM TOG* 2(2), 1983. [doi:10.1145/357318.357320](https://doi.org/10.1145/357318.357320)

## Visuals

All Manim scenes are original diagrams. All Remotion beats use toolkit templates.  
No third-party images. GodotDevWorkbench beats are source-backed reconstructions, labeled.  
No Higgsfield or paid-generation beats.

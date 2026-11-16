# SOURCES — What Is a Particle System?

## Primary sources

| Source | Hash / Identifier | Use |
|---|---|---|
| Chapter 9 — Particle Effects | SHA-256 `eefedc3c930771ebec6ffbe23e835ae76c19ffafb90f269f70a837bcbda0746a` (per SOURCE-NOTES.md) | Emission/Process/Draw table; four node types; timing model; process material 3D defaults; triggering |
| Daniel Shiffman, *The Nature of Code* — Particle Systems | Book: natureofcode.com/particles/ (CC BY-NC-SA 4.0) | Conceptual basis for particle state (position/velocity/acceleration), lifespan, collections, emitters, forces. All demonstrations are adapted into original GDScript; the p5.js code is not reproduced. |
| W. T. Reeves, "Particle Systems—A Technique for Modeling a Class of Fuzzy Objects," *ACM ToG* 2(2), 1983 | doi:10.1145/357318.357320 | Credit for naming the technique; Star Trek II genesis demo reference |
| Godot 4.7.2 official docs — 2D particle systems | docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html | CPU/GPU node distinction, near-feature-parity note |
| Godot 4.7.2 official docs — GPUParticles2D class | docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html | Property definitions, null texture behavior |
| Godot 4.7.2 official docs — ParticleProcessMaterial | docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html | 3D defaults; particle_flag_disable_z |

## Demonstration provenance

All GDScript code in this film is **original**, written for this teaching film. It adapts conceptual ideas from Nature of Code (credited) into Godot 4.7.2 GDScript. No p5.js or JavaScript code is reproduced. The Nature of Code book is CC BY-NC-SA 4.0; the adaptation is transformative educational content.

## Visual assets

- Professor Bear portraits: from `brutalist.art/professor-bear/` — existing toolkit assets
- Color palette: Claude palette (stage `#F2F0E9`, ink `#3D3929`, terracotta `#D97757`)
- Manim animations: original, written for this film
- GodotDevWorkbench: Remotion component, source-backed reconstruction labeled as such

## Godot captures

Godot display captures are NOT available in this headless build session. All Godot editor/inspector views use **GodotDevWorkbench** (a labeled Remotion reconstruction from actual source files). This is documented per godot-gamedev skill rules. Source paths and line numbers are provided for every reconstruction.

## Human/AI split

- Source research and synthesis: AI (Claude)
- Narration rewrite (Teardown register): AI
- Teaching simulation design: AI adapted from Nature of Code concepts
- GDScript code: AI (adapted from conceptual basis, verifiable against Godot 4.7.2 docs)
- Visual design choices: AI per lecture skill playset
- Sign-off and fact verification: PENDING human review

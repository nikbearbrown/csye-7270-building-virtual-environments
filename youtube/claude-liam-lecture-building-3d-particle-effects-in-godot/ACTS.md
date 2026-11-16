# ACTS.md — Building 3D Particle Effects in Godot

**Film 3 of 5 — CSYE 7270: Building Virtual Environments**  
**Source:** Chapter 9 — Particle Effects (3D-specific concepts)  
**Slug:** `claude-liam-lecture-building-3d-particle-effects-in-godot`  
**Channel:** @NikBearBrown · Liam in for Bear · Kokoro `am_onyx`

---

## Coverage map (chapter → act)

| Chapter section | Act |
|---|---|
| Four node types (3D specifics); walker-3d-platformer CPUParticles3D examples | Act 1 |
| Sub-emitters — GPU-only; AT_END / AT_COLLISION / AT_START surprises | Act 2 |
| Particle shaders — shader_type particles; start() / process() | Act 3 |
| The draw half — StandardMaterial3D flags; animation-track triggers; cost levers | Act 4 |

---

## Fixed spine

| Beat ID | Type | Content |
|---|---|---|
| BOPEN | Manim | Title card |
| BIDEA | Remotion BrutalistHesitantWriter | "3D particles — same nodes, same surprises, one more axis" |
| BDEFS | Remotion ClaudeDefinitions | 5 terms: sub_emitter · particle shader · billboard · proximity_fade · visibility_aabb |
| BACT1 | Remotion FormACard | "Act 1 — CPU vs GPU in 3D" |
| BACT2 | Remotion FormACard | "Act 2 — Sub-Emitters" |
| BACT3 | Remotion FormACard | "Act 3 — Particle Shaders" |
| BACT4 | Remotion FormACard | "Act 4 — The Draw Half" |
| BVDT | Remotion ClaudeVerdictArtifact | Recap: what 3D adds and what stays the same |
| BHTF | Remotion ClaudeComposerAsk | Your Turn prompt |
| BOUT | Remotion ClaudeTitleOutro | @NikBearBrown outro |

---

## Act 1 — CPU vs GPU in 3D

**Story:** walker-3d-platformer uses CPUParticles3D for three effects: coin burst, enemy explosion, bullet glow. Each has different timing, amount, and emission shape. The chapter shows what you gain from CPU nodes (wider hardware) and what you lose (no sub-emitters, no trails, no particle shaders).

| Beat | Manim class | What it shows |
|---|---|---|
| B01 | B01_ThreeEffects | Three CPUParticles3D nodes in walker-3d-platformer: coin burst, enemy explosion, bullet glow — amounts and lifetimes |
| B02 | B02_CPUvsGPU3D | Feature table: GPU3D vs CPU3D — sub_emitter, trail_enabled, process_material, particle shader |
| B03 | B03_AnimTrack | Animation track trigger: coin take → CPUParticles3D:emitting keyed to true at time 0; "when agent can't find trigger, look in animations" |

---

## Act 2 — Sub-Emitters

**Story:** Sub-emitters are a second GPU particle system that spawns particles from the first one's particles. AT_END means each dying particle spawns a puff. The surprises: the sub-emitter stops its own emitting; total particles capped by sub-emitter's Amount; cannot self-sub. CPU nodes have no sub-emitters at all.

| Beat | Manim class | What it shows |
|---|---|---|
| B04 | B04_SubEmitterChain | Diagram: parent emitter → particle lifetime → AT_END fires child emitter |
| B05 | B05_SubEmitterModes | Table of sub_emitter_mode enum: DISABLED, CONSTANT, AT_END, AT_COLLISION, AT_START |
| B06 | B06_SubEmitterSurprises | Three gotchas: (1) sub-emitter stops own emitting; (2) amount capped; (3) no self-sub |

---

## Act 3 — Particle Shaders

**Story:** Replace ParticleProcessMaterial with a ShaderMaterial whose shader begins `shader_type particles;`. The shader runs before drawing, has start() and process() functions, writes TRANSFORM, VELOCITY, COLOR. The headless dummy renderer still compiles shader source — type errors are catchable without a window.

| Beat | Manim class | What it shows |
|---|---|---|
| B07 | B07_ShaderStructure | Shader anatomy: shader_type particles; start() with RESTART_POSITION/VELOCITY; process() with DELTA |
| B08 | B08_HeadlessCompile | Headless shader compilation: valid shader accepted; type error (`vec2` assigned to `vec3`) rejected with SHADER ERROR |
| B09 | B09_ShaderVsMaterial | What a shader adds over the material: custom forces, procedural emission shapes, CUSTOM channel for data pass-through |

---

## Act 4 — The Draw Half

**Story:** The draw half of an effect is separate from the simulation. `particle_material.tres` in walker-3d-platformer: StandardMaterial3D with additive blending, unshaded shading, particle billboarding, proximity fade. Cost levers: amount, lifetime, fixed_fps, visibility_aabb, texture size, overdraw.

| Beat | Manim class | What it shows |
|---|---|---|
| B10 | B10_DrawMaterial | StandardMaterial3D flags for particles: additive blend mode, shading_mode=unshaded, billboard_mode=particle, proximity_fade |
| B11 | B11_CostLevers | Six cost levers: amount · lifetime · fixed_fps · visibility_aabb · texture_size · overdraw; where each lands (CPU/GPU/fill) |
| B12 | B12_WalkerParticles | GodotDevWorkbench reconstruction — walker-3d-platformer CPUParticles3D coin burst: amount=16, one_shot, sphere emission, lifetime_randomness |

---

## Recap

| Beat | Content |
|---|---|
| BVDT | What 3D adds: sub-emitters (GPU only), particle shaders, visibility_aabb, 3D draw flags. What stays the same: one_shot, explosiveness, process_material traps, headless limits. One new trap: sub-emitter stops its own emitting. |
| BHTF | "Open walker-3d-platformer. Find the coin burst. Change it from CPUParticles3D to GPUParticles3D. What breaks? What becomes possible?" |
| BOUT | @NikBearBrown outro |

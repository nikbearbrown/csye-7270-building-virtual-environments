# SCRIPT.md — Building 3D Particle Effects in Godot

Voice: Liam · Kokoro `am_onyx` · Teardown register (Feynman × MKBHD)

---

## BOPEN

*(no narration — title card only)*

---

## BIDEA — Hesitant Writer

In 3D, particle effects are the same loop: born, move, die.

But you pick up one more axis, one more renderer decision, and three new features that only GPU nodes have.

The traps are the same. The surprises are new.

---

## BDEFS — Key Terms

**sub_emitter** — a second GPU particle system that spawns particles from the first one's particles. When a spark dies, it can leave a puff. CPU nodes have no sub-emitter at all.

**particle shader** — a shader whose first line is `shader_type particles;`. It runs before drawing, not after. It writes TRANSFORM, VELOCITY, and COLOR for each particle per frame. Only GPU nodes support it.

**billboard** — a draw mode where each particle's quad always faces the camera. Required for round soft dots that stay round regardless of camera angle.

**proximity_fade** — a material flag that fades a particle out as it gets close to geometry. Without it, soft particles clip hard into floors and walls.

**visibility_aabb** — the 3D axis-aligned bounding box that the engine checks to decide whether to simulate a particle node at all. Too small: effect vanishes when the node is only partly visible. Too large: simulation runs off-screen.

---

## BACT1

Act 1 — CPU vs GPU in 3D

---

## B01 — Three Effects

The walker-3D-platformer is a Forward+ 3D game. It uses CPU Particles 3D for three distinct effects.

The coin burst: 16 particles, one-shot, explosiveness one, sphere emission shape, lifetime 0.5, lifetime randomness 0.2. The coin fires it when its `take` animation starts.

The enemy explosion: 16 particles, one-shot, explosiveness one. Mesh particles — each one is a full piece of geometry, not a texture quad. The enemy's explode animation fires it.

The bullet glow: 16 particles, lifetime 0.4, looping. It runs continuously behind each bullet.

Three effects, three timing modes, one node type — and none of them have sub-emitters, trails, or particle shaders. CPU nodes don't.

---

## B02 — CPU vs GPU in 3D

The same feature gap from the 2D side exists in 3D.

GPU Particles 3D: process_material is a ParticleProcessMaterial on the node. sub_emitter exists. trail_enabled exists. Particle shaders work.

CPU Particles 3D: the settings that would be on a process material are instead direct properties of the node. No sub_emitter. No trail_enabled. No particle shaders.

Wider hardware, fewer features. The 3D manual says so: CPU particles "work on a wider range of hardware" but "there are no plans to add new features to CPUParticles2D" — same for 3D.

---

## B03 — Animation Track Trigger

Here is where agents get lost. A particle effect starts. Nothing in the code calls restart or sets emitting. The agent searches every script. It can't find it.

Look in the animations.

The coin's `take` animation track has one key at time zero: `CPUParticles3D:emitting` set to true. The enemy's explode animation has the same key for its Explosion node. The animation player is the trigger.

An AnimationPlayer can key any exported property on any node in the scene tree. Emitting is an exported property. When an agent says it "cannot find where the effect starts", check the animation tracks before opening a new prompt.

---

## BACT2

Act 2 — Sub-Emitters

---

## B04 — The Sub-Emitter Chain

A sub-emitter is a GPU particle system that spawns new particles from the first system's particles. Set sub_emitter_mode on the process material, point sub_emitter to a sibling node, and each particle in the parent system can spawn a batch of particles from the child.

AT_END means: when a parent particle dies, fire the sub-emitter at that location. Sparks that each leave a puff as they die are an AT_END sub-emitter.

AT_COLLISION requires the particle to hit geometry — which needs the renderer's SDF collision support. AT_START fires at birth. CONSTANT fires continuously from live particles.

---

## B05 — Sub-Emitter Modes

The sub_emitter_mode enum on Godot 4.7.2:

DISABLED — no sub-emitter.
CONSTANT — sub-particles spawn continuously from live parent particles.
AT_END — sub-particles spawn when a parent particle dies.
AT_COLLISION — sub-particles spawn when a parent particle hits geometry. Needs SDF collision, Forward+ or Mobile renderer.
AT_START — sub-particles spawn when a parent particle is born.

---

## B06 — The Surprises

Three things the sub-emitter documentation says that agents miss.

One: a system used as a sub-emitter stops emitting, even if the Emitting property was checked in the inspector. It only emits when the parent system drives it.

Two: the sub-emitter's own Amount is its total particle budget. The parent's particle count does not multiply it. If the sub-emitter has Amount 8, it has at most 8 particles, however many parents spawn it.

Three: a system cannot be its own sub-emitter.

CPU nodes have no sub-emitters. Full stop.

---

## BACT3

Act 3 — Particle Shaders

---

## B07 — Shader Structure

When the ParticleProcessMaterial's checkboxes run out, replace it with a ShaderMaterial whose shader begins `shader_type particles;`.

The shader runs before drawing — it does not draw anything itself. It has two functions: start, called for a newly born particle, and process, called every frame for every live particle.

You write to built-ins: TRANSFORM gives position and orientation, VELOCITY gives motion, COLOR changes the tint. ACTIVE lets you kill a particle early by setting it to false.

Two booleans tell you when a particle is new: RESTART_POSITION and RESTART_VELOCITY, both true when the particle is first born. EMISSION_TRANSFORM gives you the emitter's transform for positioning.

---

## B08 — Headless Compile

A particle shader compiles in headless mode. The dummy renderer does not simulate particles, but it does compile shader source through its material storage.

That is useful. You can give an agent a shader, run Godot headless, and catch type errors before opening a window.

A minimal working shader parses clean. A deliberately broken copy — with `VELOCITY = vec2(1.0)` — is rejected with: SHADER ERROR, Invalid arguments to operator equals: vec3, vec2. The headless run finds the type error.

What the particles then look like was not checked. The compiler cannot see that.

---

## B09 — What a Shader Adds

Over the process material, a particle shader adds three things.

Custom forces. Turbulence, vortices, attractors based on any math you write — anything that can be expressed in GLSL. The material gives you built-in turbulence and attractors; the shader gives you anything.

Procedural emission shapes. The material's emission shape is a fixed enum. A shader can emit from any shape: a parametric curve, a mesh sampled by UV, a grid.

The CUSTOM channel. Four floats per particle, computed in start or process, readable in the draw shader. It passes per-particle data from the simulation to the visual — a fire particle can pass its temperature as a CUSTOM float and the draw shader uses it to pick colour.

---

## BACT4

Act 4 — The Draw Half

---

## B10 — The Draw Material

Simulation and drawing are separate. The process material or shader runs the loop. A separate material — applied to the particle node's draw passes — decides what each particle looks like.

In walker-3d-platformer, that is `particle_material.tres`. A StandardMaterial3D with four specific flags.

Blend mode: additive. Particles that overlap add their brightness together. Smoke uses alpha blend; sparks and fire use additive.

Shading mode: unshaded. The particle ignores the scene's lights. A spark that dims in shadow looks wrong — leave it unshaded.

Billboard mode: particle. Each quad always faces the camera. Turn this off and a round soft dot becomes an angled diamond as the camera moves.

Proximity fade: enabled. The particle fades out near geometry instead of clipping through it hard.

---

## B11 — Cost Levers

Six levers for particle cost, regardless of CPU or GPU.

Amount — the direct multiplier. Halve the amount, halve the simulation work.

Lifetime — at a fixed amount, a longer lifetime means fewer births per second and a larger spread, but still at most amount particles alive at once.

Fixed FPS — update less often. 30 updates per second instead of 60 halves the simulation calls without halving the visual frame rate (interpolation fills the gaps).

Visibility AABB — if the bounding box is too small, the effect turns off when the node is only partly visible. Too large: simulation runs even when the effect is fully off-screen. Set it to the real footprint.

Texture size — a 512-pixel transparent soft dot costs more fill rate than a 64-pixel one. Overdraw from transparent, overlapping quads is the GPU cost the Profiler needs a real renderer to measure.

Chapter 13 has the Profiler. That is where GPU costs land.

---

## B12 — Walker 3D Particles

Here is the coin burst from walker-3d-platformer as the editor shows it. CPU Particles 3D. Amount 16. One shot. Explosiveness one. Sphere emission shape — particles born from the surface of an invisible sphere, not from a single point. Lifetime 0.5. Lifetime randomness 0.2 — each particle lives between 0.4 and 0.6 seconds.

The draw material: `particle_material.tres`, a StandardMaterial3D with additive blending, unshaded shading, particle billboarding, and proximity fade.

This is a complete minimal effect: the simulation half on the node, the draw half in its own reusable file.

---

## BVDT — Recap

Here is what 3D adds over 2D.

Sub-emitters — GPU nodes only, four trigger modes.
Particle shaders — GPU nodes only; headless compilation catches type errors.
Visibility AABB — the 3D equivalent of visibility_rect; set it to the real footprint.
Draw material flags — additive blend, unshaded, billboard, proximity fade; keep them in a reusable tres file.
Animation track triggers — any exported property, including emitting, can be keyed.

Here is what stays the same.

one_shot, explosiveness, lifetime, restart — identical contracts in 3D.
The process_material is still 3D — no Disable Z trap in a 3D game, but the material's 3D defaults mean gravity is still minus 9.8 on Y.
Headless limits — the dummy renderer still does no GPU simulation and no drawing. State checks work. Visual checks don't.

New trap: the sub-emitter stops its own emitting. Check that before assuming it's broken.

---

## BHTF — Your Turn

Open walker-3d-platformer. Find the coin burst. Convert CPUParticles3D to GPUParticles3D.

What becomes possible? Add a sub-emitter: AT_END, a small puff where each coin particle dies. What breaks if you leave the renderer on Forward+?

Then measure: run the particle_cost script from Chapter 9 with --fixed-fps 60. Does GPUParticles3D still cost near zero headless? Is that useful information?

---

## BOUT

*(Liam outro — @NikBearBrown)*

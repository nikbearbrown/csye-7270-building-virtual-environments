# SCRIPT.md — A Practical Godot VFX Library

Voice: Liam · Kokoro `am_onyx` · Teardown register (Feynman × MKBHD)

---

## BOPEN

*(no narration — title card only)*

---

## BIDEA — Hesitant Writer

You've seen four node types, a timing model, and three sessions with an agent.
What do you reach for next?
Godot ships a catalog. Two demo scenes, not games.
You read them like a library.

---

## BDEFS — Key Terms

**feature catalogue** — a scene whose purpose is to show what a system can do. Not a playable game. Not tested headlessly. A set of configured effects you read and port from.

**Compatibility renderer** — the renderer that runs on the widest hardware: mobile, embedded, older GPUs. Particle trails and SDF collision are unsupported. The class reference confirms.

**draw pass** — one of a particle node's material slots. The process material decides where particles go. The draw pass decides what each particle looks like: its texture, blend mode, and shading.

**tres file** — a Godot resource file stored separately from any node, with a `.tres` extension. A particle draw material in its own file can be shared and referenced by multiple effects.

**FRICTIONAL.md** — the human's record of a build: what the agent did, what you ran, what failed, what you saw on screen. The only evidence that an effect looks like anything.

---

## BACT1

Act 1 — The Godot Catalog

---

## B01 — The 2D Catalog

The godot-demo-projects repository, pinned at commit a3b5c113, has a scene called 2d/particles.

Seventeen GPUParticles2D nodes. One scene. Mobile renderer. Each node is one pattern: a fountain, a fire, a trail, sparks, smoke, a galaxy, a flame thrower.

There is no Walker adaptation. No test harness. No game logic. What it is: a feature catalogue. Every effect in it is readable. Open the .tscn file, trace each node's process material, port it to your project.

That catalogue is the fastest particle library a Godot project can have.

---

## B02 — The 3D Catalog

The same commit has 3d/particles. Forward Plus renderer.

This scene exercises three GPU features that the 2D catalog does not show in action: trails, SDF collision, and attractors.

Trail enabled: GPU nodes only. The class reference lists it. CPUParticles3D has no trail_enabled at all, and Compatibility does not support it even on GPU nodes.

SDF collision: particles that bounce off scene geometry. Needs depth rendering — Forward Plus or Mobile only.

Attractors: velocity fields that shape all live particles. The process material has attractors as well, but the 3D demo shows them operating in a real scene.

Everything in this catalog that uses trails, SDF collision, or sub-emitters requires Forward Plus or Mobile. On Compatibility, those effects don't run.

---

## B03 — The Three-Part Frame as Organizer

When you port an effect from a catalog, the three-part frame tells you what to carry.

Emission: amount, lifetime, explosiveness, one_shot. These are on the node. They port directly between CPU and GPU.

Process: velocity, gravity, spread, turbulence, attractors, sub-emitters. On GPU nodes these live in the ParticleProcessMaterial. On CPU nodes they are node properties. Sub-emitters and particle shaders are GPU only — they cannot port to CPU.

Draw: the texture, the material, the blend mode. This is the draw pass. It is independent of whether you use CPU or GPU. A .tres file for the draw half ports anywhere.

The catalog tells you what effect exists. The frame tells you what to carry when you move it.

---

## BACT2

Act 2 — Node Conversion

---

## B04 — CPU to GPU: What the Conversion Preserves

The Godot editor converts a CPUParticles2D to GPUParticles2D with one button in the 2D toolbar. The 3D toolbar has the same option.

What the conversion preserves: amount, lifetime, explosiveness, one_shot, local_coords, fixed_fps, and the timing model. The emission settings — spread, velocity range, gravity, lifetime_randomness — move from node properties into a new ParticleProcessMaterial.

What you gain: the GPU node now has sub_emitter, trail_enabled, and a process material that supports turbulence, attractors, and collision.

CPU to GPU is additive. You keep the effect and gain features.

---

## B05 — GPU to CPU: What's Lost

Converting from GPUParticles2D to CPUParticles2D is a one-way degradation.

Most emission settings survive. The process material becomes node properties for the settings that have equivalents.

What cannot survive: sub_emitter. trail_enabled. Particle shaders. The process material's turbulence, attractors, and collision.

If an effect uses any of those, converting to CPU changes the effect. A particle shader becomes a plain process material with whatever settings can be matched. A sub-emitter chain disappears entirely.

GPU to CPU is not the same effect on different hardware. It is a simpler effect on wider hardware.

---

## B06 — Compatibility: The Hardware Map

Every effect in your library should carry a renderer tag.

Compatibility: the widest target. Particle trails: unsupported. SDF collision: unsupported. emit_particle(), the scripted spawn method: Forward Plus or Mobile only. Effects built for Compatibility cannot use any of those.

Mobile: modern devices. Trails work. SDF collision works. emit_particle() works.

Forward Plus: the full feature set. Everything works, including the 3D demo's sub-emitter chains and attractor fields.

A library that does not tag renderer requirements will fail on the wrong machine without a clear error. The Godot renderer comparison page has the full table. It is two pages in the documentation. It is worth reading before you promise Compatibility support.

---

## BACT3

Act 3 — Cross-Engine Map

---

## B07 — Unity: Built-in vs VFX Graph

Unity's two particle systems map directly to Godot's two families.

The Built-in Particle System is CPU-simulated. Its scene files serialise as YAML. An agent can read them, diff them, edit them. The sub-emitter mechanism is the Sub Emitters module. The equivalent of Godot's finished signal is OnParticleSystemStopped.

The Visual Effect Graph is GPU-simulated. Its assets are .vfx files. VFX Graph assets are not described as text-diffable by Unity's documentation. An agent cannot inspect the emitter stack the way it reads a .tscn. It can write the C# that spawns the system.

For the death burst: one_shot maps to Looping off; amount plus explosiveness one maps to Spawn Burst Instantaneous with a count; finished maps to OnParticleSystemStopped.

---

## B08 — Unreal: Niagara

Unreal Engine's Niagara is one particle system with CPU and GPU selectable per emitter via the Sim Target setting.

The one-shot burst: Emitter State with Loop Behavior Once — Godot's one_shot. Spawn Burst Instantaneous with a count of 32 — Godot's amount with explosiveness one. The equivalent of finished is UNiagaraComponent.OnSystemFinished.

Niagara systems are stored as .uasset files. Epic's own source-control documentation confirms they are binary and cannot be opened as text or merged with text tools. An agent can write the C++ that spawns the system and can drive the Unreal editor with the Python Editor Script Plugin. It cannot inspect the emitter stack as a diff.

Niagara events — the sub-emitter mechanism — work on CPU simulation only. Godot's sub-emitters are GPU only. The two are mirrors of each other.

---

## B09 — The .tscn Advantage

The practical difference for agent work is file format.

A Godot scene file is plain text. A particle node's configuration, its process material, and its sub-emitter reference are all visible in the .tscn. The draw material is in a .tres. An agent can read both, run a diff, and verify specific properties without running the game.

Unity prefabs are YAML — the Built-in system is readable. VFX Graph assets are not. Unreal's .uasset is binary for all visual content.

That is why the Chapter 9 agent could confirm that DeathBurst is a child of Main, that its process material has particle_flag_disable_z set to true, and that its texture is a GradientTexture2D — from the scene file, before a single test ran.

No other engine in this course gives agents that reach into a particle configuration.

---

## BACT4

Act 4 — Building Your Library

---

## B10 — The .tres Pattern

Walker-3d-platformer's particle_material.tres is a StandardMaterial3D in its own file, with four flags: additive blend mode, unshaded shading mode, particle billboard mode, proximity fade enabled.

The coin burst, the enemy explosion, and the bullet glow all reference the same file via material_override. Change additive to alpha-blend for smoke: one edit, three effects update.

The draw half is stable. For a given art style, the blend mode and billboard mode do not change between effects. What changes is the process material — velocity, spread, lifetime randomness. Keep the draw half in a named file. Reference it everywhere.

That is the library benefit: one draw file, shared. Port it to the next project by copying one file.

---

## B11 — Library Entry Card

A practical VFX library entry has five fields.

Name: what the effect is called in this project.

Renderer: Compatibility, Mobile, or Forward Plus. The minimum needed to run the effect.

Node type: CPU or GPU. CPU runs anywhere within its renderer; GPU gains sub-emitters, trails, and shaders, but only on its renderer.

Draw material: the .tres file this effect uses for its draw pass. Shared effects point to the same file.

Test status: what the headless test establishes. Not what it proves visually — what it checks in state.

Build one card per effect before you build the effect. It answers the questions your prompt needs to ask.

---

## B12 — particle_material.tres

Here is particle_material.tres as the Godot editor shows it. A StandardMaterial3D. Four flags.

Blend mode: additive. Shading mode: unshaded. Billboard mode: particle. Proximity fade: enabled.

Applied via material_override to the coin burst, the enemy explosion, and the bullet glow in walker-3d-platformer.

Copy this file into any 3D particle project. Change additive to alpha-blend for smoke. Change proximity_fade_distance to control the softness of the fade at geometry edges. The pattern holds.

---

## BVDT — Recap

Here is what a practical library gives you.

The Godot catalog: 2D has 17 GPU effects on Mobile. 3D has trails, attractors, SDF collision, and sub-emitters on Forward Plus. Both are plain text .tscn files. Neither has a Walker adaptation.

Conversion: CPU to GPU gains a process material and all GPU features. GPU to CPU loses sub-emitters, trails, and shaders. Compatibility drops trails and SDF collision entirely. Tag every library effect with its renderer requirement.

Cross-engine: Godot's text scene format gives agents the most reach. Unity's Built-in YAML is readable. VFX Graph and Niagara assets are binary. Agents can configure the spawn call in code; they cannot inspect the full effect stack from a file.

The .tres pattern: one draw material file, shared by multiple effects. Change the look once. Port the file to the next project.

---

## BHTF — Your Turn

Open godot-demo-projects at commit a3b5c113. Navigate to 2d/particles. Read the .tscn file.

Which of the 17 effects uses sub-emitters? Which uses collision? Which would stop working on Compatibility?

Pick one effect and convert it to CPUParticles2D in the editor. Which properties survive intact? Which disappear? If a property disappears, where did its settings go?

---

## BOUT

*(Liam outro — @NikBearBrown)*

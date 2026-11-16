# Missing term definitions for the chapters (draft for Bear, 2026-11-09)

**Status: DRAFT. Nothing in the chapters has been changed and nothing is pushed.** These are proposed sentences, each with the place it would go and what it rests on. You decide which go in and in what words.

## Executive summary

The exam questions follow the chapter text, and the chapters do not define several terms you want asked directly. Below are **15 one- or two-sentence definitions**, each placed at the point where the chapter first uses the term. Four are grounded in what the chapter already says or in Godot's own documentation, which I fetched today. The rest rest on general game and graphics usage, and each is marked so you can check the wording against how you teach it.

**Three findings you should know before reading the list**
1. **"Trigger" means two things in the course.** Chapter 4 describes a detection area that "reports overlaps, never blocks or pushes" and never calls it a trigger. Chapter 12 uses "trigger" for the game logic that decides a sound should play. The exam's "collider versus trigger" idea only exists in the first sense. Pick one meaning, or define both (entry 12).
2. **"Rig" is not used in the Godot parts of Chapter 10.** The chapter says "skeleton", "bones" and "skinning"; the word "rig" appears only in the Unity and Unreal sections. Entry 11 ties the two words together.
3. **"Collider" appears only loosely** (Chapter 4, "The art is not the collider"). The chapter says "collision shape" and "collision object". Entry 10 defines it.

**What I did not draft.** "Golden image": the Godot parts of Chapter 8 do not teach that technique (they compare sampled pixel colours with a model's predictions), so asking it would test something the course does not teach. I recommend leaving it out. A sentence is at the end if you want it anyway.

**Sources I could and could not use.** Godot documentation pages fetched 2026-11-09: particle systems, mesh level of detail, optimizing 3D performance, using MultiMesh. The Blender manual pages for "mesh" and "origin" came back without their body text, so entries 3 and 4 are **not** sourced to the Blender manual. The Godot pages do not define "draw call" either.

---

## Chapter 2: Game art and sound assets

### 1. Sprite, texture, resolution, aspect ratio
**Where:** Chapter 2, at the start of the section on what the image model produces versus what Godot needs (before the table around line 37).
**Proposed:** "A **texture** is image data that something is drawn with; a **sprite** is a 2D picture, or one frame of one, drawn as an object in the game. An image's **resolution** is its size in pixels, and its **aspect ratio** is its width divided by its height."
**Basis:** general usage. The chapter uses "sprite" and "pixels" without defining them.
**Check:** your usage of "sprite" versus "texture" in Godot (a sprite node displays a texture).

## Chapter 3: 3D assets and Blender

### 2. Mesh and vertex
**Where:** Chapter 3, step 4 "Apply transforms" (around line 79), where "mesh data (vertices)" is first used.
**Proposed:** "A **mesh** is the shape of a 3D model: points called **vertices** joined by edges into faces, which a game draws as triangles."
**Basis:** the chapter's own line ("a Blender object has a transform ... and mesh data (vertices)"); the rest is general 3D usage. Not sourced to the Blender manual (the page body did not load).

### 3. Origin (pivot)
**Where:** Chapter 3, step 4, or the build prompt that first says "the origin" (around line 179).
**Proposed:** "An object's **origin**, also called its **pivot**, is the point its position and rotation are measured from. A door that should swing on its hinge needs its origin on the hinge edge, and a crate with its origin at its centre sinks halfway into a floor placed at height zero."
**Basis:** general usage; the example is mine. Not sourced to the Blender manual.

### 4. Level of detail (LOD)
**Where:** Chapter 3, at the import-settings block that lists a level-of-detail setting without explaining it (around lines 105 to 110).
**Proposed:** "**Level of detail (LOD)** keeps several versions of a mesh with fewer and fewer triangles and draws a simpler one when the camera is far away, which saves rendering cost. Godot can generate the simpler meshes automatically when it imports a model."
**Basis:** Godot's mesh LOD page, fetched 2026-11-09: "Lower detailed meshes will be used when the camera is far away from the object" and Godot can "automatically generate less detailed meshes for LOD usage on import".

## Chapter 5: Game design documents

### 5. Design pillars and core loop
**Where:** Chapter 5, after the list of sixteen sections (line 23), where "pillars" and "core loop" are named only as section titles.
**Proposed:** "**Design pillars** are the few short statements of what the game must be and feel like, such as 'fast restarts', that every feature is judged against. The **core loop** is the short cycle of player actions repeated most often, for example enter a room, fight, collect a reward."
**Basis:** general game-design usage; no Godot source.
**Check:** the wording Walker's design skill (Zelda) uses for these two sections; I could not read it here.

### 6. Prototype and vertical slice
**Where:** Chapter 5, near the failure-mode list (line 27) where "prototype" appears once.
**Proposed:** "A **prototype** is a quick build made to answer one design question; it may be thrown away. A **vertical slice** is a thin piece of the game built to near-final quality across art, sound, interface and rules, to show what the whole game would be like."
**Basis:** general game-design usage; no Godot source.

## Chapter 6: Shader foundations

### 7. Fragment
**Where:** Chapter 6, after the processor-function bullets (line 65: "`fragment()` runs for every pixel covered by the mesh").
**Proposed:** "A **fragment** is the candidate colour for one screen position that a shape covers. The `fragment()` function runs once for each one and decides its colour."
**Basis:** the chapter's own line and Godot's introduction to shaders, which it quotes. Optional extra sentence, which goes beyond the chapter: "A fragment becomes the pixel you see only if nothing nearer covers it."

### 8. Vertex
**Where:** Chapter 6, same place, line 64.
**Proposed:** "A **vertex** is one corner point of a shape; the `vertex()` function runs once for each and decides where it lands."
**Basis:** the chapter quotes Godot: `vertex()` "runs over all the vertices in the mesh and sets their positions".

## Chapter 9: Particle effects

### 9. Particle, emitter, particle system
**Where:** Chapter 9, "A particle system is a birth–life–death loop, not a picture" (line 19).
**Proposed:** "A **particle** is one short-lived point that the effect creates, moves and removes. An **emitter** is the source that creates particles, which in Godot is the particle node itself. A **particle system** is the whole effect: the emitter, the particles it creates, and how they are drawn."
**Basis:** Godot's 2D particle page, fetched 2026-11-09: particle systems "simulate complex physical effects, such as sparks, fire, magic particles, smoke, mist"; "a 'particle' is emitted at a fixed interval and with a fixed lifetime". The chapter already calls the node the "emitter" (line 42).

## Chapter 4: Scenes, collision and physics

### 10. Collider
**Where:** Chapter 4, "Four collision objects, and one way around them" (line 126), before the table.
**Proposed:** "A **collider** is a collision shape: the geometry the physics engine uses to decide whether two things touch. A solid collider blocks other objects; a detection area uses a shape too but only reports the overlap."
**Basis:** the chapter's own definition in "The art is not the collider" ("A collision shape is geometry the physics engine uses") and the table row for the detection area.

## Chapter 10: Animation foundations

### 11. Rig
**Where:** Chapter 10, "Skeletons and IK" (line 124).
**Proposed:** "A **rig** is a skeleton of connected bones together with the skinning that attaches the picture or mesh to it: moving a bone moves the parts attached to it. Animation then changes the bones' poses instead of swapping in a new drawing for each pose, which is the difference from a sprite sheet."
**Basis:** the chapter's own description (a hierarchy of bones; a polygon skinned to the bones with weights).

## Chapter 12: Audio and triggers

### 12. Trigger (two senses) and one-shot
**Where:** Chapter 12, the opening paragraph (line 5), and the import-settings passage on looping (line 45).
**Proposed (trigger):** "A **trigger** is whatever makes a sound start. It is game logic reacting to an event, such as a hit being scored or the player entering an area. A **trigger area** is a detection area that reports overlap without blocking, which is one common way to produce that event."
**Proposed (one-shot):** "A **one-shot** sound plays from start to end once each time it is triggered. A **loop** returns to its loop point and keeps playing until it is stopped, so a looping sound never reports that it has finished."
**Basis:** the chapter's own lines (trigger system; "`finished` ... never for a looping stream"). The word "one-shot" for sounds is general usage; Godot's particle page uses "One Shot" for particles only.
**Decision for you:** one meaning of "trigger" or two (finding 1).

## Chapter 13: Profiling and optimization

### 13. Draw call
**Where:** Chapter 13, first use at line 42 ("cutting draw calls does nothing for a frame that is waiting on a GDScript loop").
**Proposed:** "A **draw call** is one command from the CPU asking the GPU to draw something. Many small draw calls can keep the CPU busy even when the GPU has little to do, which is why drawing many copies of one mesh in a single call is cheaper."
**Basis:** the chapter's own uses (lines 42, 56, 95: MultiMesh is "one draw call for many instances"). Godot's pages did not define the term. This is general graphics usage.

## Chapter 11: Animation and interaction

### 14. State machine (plain sentence)
**Where:** Chapter 11, "The state machine, as machinery" (line 68).
**Proposed:** "A **state machine** is in one state at a time and moves between states along **transitions** that you define; each state is one situation of the character, such as idle, run, jump or fall."
**Basis:** the chapter's description (states connected in a graph, each connection a transition). "One state at a time" is implied by "current state" and the blend-versus-commit contrast but not stated outright; the exam reader noted this.

## Chapter 8: Shader verification (optional)

### 15. Golden image (not recommended)
**Where:** Chapter 8, after the "bench" description (line 103).
**Proposed, if you want it:** "A **golden image** (reference image) is a saved, approved screenshot that later renders are compared against. It catches changes, but it cannot tell you whether the reference itself was right."
**Why I advise against it:** the Godot parts of Chapter 8 compare sampled colours with a model's table instead. Adding the term would teach a technique the course does not use.

---

## What happens next if you approve

- Each accepted sentence would go into the chapter at the named place, from a clean clone (the local course folder is about 2,000 commits behind and has other sessions' edits). Nothing would be pushed without your word.
- The exam questions that could then ask these terms directly (fragment, collider, trigger, rig, state machine, mesh, draw call) would be added as new questions or replace weaker ones, then re-checked against the chapter text.

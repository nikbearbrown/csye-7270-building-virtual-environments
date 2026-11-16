# ACTS — What Is a Particle System?

Skill: lecture  
Source: Chapter 9 — Particle Effects, `/Users/bear/Downloads/seis-course-publish/chapters/09-particle-effects.md`  
Supporting: Daniel Shiffman, *The Nature of Code* — Particle Systems (conceptual basis; adapted into original Godot demonstrations)  
Series-plan section: "What Is a Particle System?" in SERIES-PLAN.md

## Coverage map

Every section of the source assigned to an act, or listed under LEFT OUT.

| Source section | Act | Notes |
|---|---|---|
| Executive summary (overview paragraph) | Opening/BIDEA framing | Provides the "three separable parts" frame |
| "A particle system is a birth–life–death loop, not a picture" | ACT I + II | Reeves 1983 credit; birth/life/death loop; Emission/Process/Draw table |
| Nature of Code: One particle (position, velocity, acceleration) | ACT I | Adapted into GDScript teaching simulation |
| Nature of Code: Collections, emitters, forces | ACT II + III | Adapted into original Godot demonstration |
| "Four node types, two families" | ACT IV | GPUParticles2D/3D vs CPUParticles2D/3D; feature comparison table |
| "The timing model: one emission cycle" | ACT IV | lifetime, amount, explosiveness, one_shot, randomness |
| "The process material is 3D, even in 2D" | ACT IV | Disable Z; gravity direction; 3D defaults |
| "Triggering: a particle node is a node" | ACT IV | Parenting and visibility; local_coords |
| "Sub-emitters" | LEFT OUT | GPU-only; taught in Film 4 (VFX Library). Mentioned briefly. |
| "Particle shaders" | LEFT OUT | Advanced; taught in separate shader series. Mentioned as extension. |
| "Where particle cost lands" | ACT IV (brief mention) | Full treatment in Film 5 and Assignment 7. |
| Walker example: walker-2d-dodge-the-creeps | LEFT OUT | Taught in Film 5 (Adding Particle Effects to Walker Claude). |
| "What we actually ran" (session record) | LEFT OUT | Belongs to Film 5 context; source-record teaching is Film 5's subject. |
| Unity/Unreal comparisons | LEFT OUT | Optional cross-reference; not Godot-centered. |

## Acts

### Opening (BOPEN, BIDEA, BDEFS)
**Learning goal:** frame the misconception (checkboxes → loop) and establish prerequisite vocabulary.
**Cast:** Professor Bear portrait (BOPEN), BrutalistHesitantWriter (BIDEA), ClaudeDefinitions (BDEFS)

### ACT I — One Moving Element
**Source:** Nature of Code §particle state; Chapter 9 "birth–life–death loop"  
**Learning goal:** understand that position, velocity and acceleration are three different jobs, and trace a particle's state update.  
**What we build:** a single dot in a GDScript teaching scene; expose its position, velocity, acceleration; advance it one frame at a time.  
**Recurring cast:** one white dot on dark background (Manim), GodotDevWorkbench code view  
**Key motion:** the dot moves; its velocity label changes when acceleration is applied; delta-time scaling is shown

### ACT II — Birth, Life and Removal
**Source:** Nature of Code §lifespan; Chapter 9 "birth–life–death loop" (Emission part)  
**Learning goal:** understand the lifecycle and why removal is not optional.  
**What we build:** add age/lifetime to the dot; spawn a small collection; temporarily remove the cleanup step to show unbounded growth.  
**Recurring cast:** collection of dots (Manim), population counter  
**Key motion:** dots fade as they age; counter climbs then stabilizes; un-cleanup sends counter climbing  
**Staged failure:** omit removal → population grows without bound → restore cleanup → population settles

### ACT III — One Emitter, Many Variations
**Source:** Nature of Code §emitter, forces; Chapter 9 "one emission cycle" (birth parameters)  
**Learning goal:** understand that a few rules create variety; randomizing everything destroys readable intent.  
**What we build:** move the emitter; vary initial direction, speed, size in controlled ranges; add a shared wind force; compare stream vs burst.  
**Recurring cast:** emitter dot + particle field (Manim)  
**Key motion:** particles spray left then right; burst vs stream timing comparison

### ACT IV — From Rules to Godot's Nodes
**Source:** Chapter 9 "Four node types, two families"; "The timing model"; "The process material is 3D, even in 2D"; "Triggering: a particle node is a node"  
**Learning goal:** map the observed behavior to Godot's node properties; understand the Emission/Process/Draw split.  
**What we build:** replace the teaching simulation with a built-in particle node in a small Godot scene; show Inspector properties matching the rules; make sparks and rising motes.  
**Recurring cast:** GodotDevWorkbench (code/inspector), Manim diagram (Emission/Process/Draw table)  
**Key motion:** Inspector values correspond to the rules; the node choice affects which settings are available

### Closing (BVDT, BHTF, BOUT)
**Learning goal:** recap the four acts; Your Turn gives a concrete fountain prediction task.

## BIDEA correction
- **Framing text:** "You open Godot's particle system and find seven hundred checkboxes. You start clicking and hoping."
- **triggerWords:** `clicking and hoping`
- **replacementWords:** `running one loop`

## LEFT OUT — summary
Sub-emitters (Film 4), particle shaders (advanced/separate), Walker worked example (Film 5), Unity/Unreal comparison (optional cross-reference), full cost measurement (Film 5 + Assignment 7).

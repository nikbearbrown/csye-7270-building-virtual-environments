# Old Canvas course to new Canvas course

## Executive summary

**What this is.** A line-by-line account of what became of the Spring 2026 Canvas course (the `.imscc` export) in the new Fall 2026 Godot, Walker and Claude Code course: every old module, every old page that carried teaching, every old assignment, and every old quiz.

**Why read it.** You asked for the new course to be "modeled on the old Canvas course." This shows exactly how: which structure was kept, what replaced the Unity and Unreal material, and what was deliberately not carried over, with the reason. If a retired item should come back, this is the list to say so from.

**What it found.** The old course was a skeleton. Of its 13 modules, most were a few short link pages (a Unity page, an Unreal page, a "Helpful links" page) plus one assignment per topic; only three pages (Game AI, Unity ML-Agents and CgFX) carried more than a list of links. The new course keeps the skeleton (Lecture, then Assignment, then Links, in one module per topic) and adds a practice assessment to each module. It replaces the content with the Godot, Walker and Claude Code material that the companion chapters had already tested by running it. Seven old items have no successor, and they are listed under "Not carried over."

**What it did not do.** Nothing from the old export was imported: no media, no student records, no old quizzes, no Unity or Unreal assignments. The export was read only. The new Canvas package has not been imported into a live Canvas yet.

---

## Structure kept, structure added

| Old course | New course |
|---|---|
| One module per topic, in the order Lecture, Assignment, Links | One module per week, same order, with an ungraded **Practice** quiz added between Lecture and Assignment |
| Short wiki pages, many per module | One lecture page per module (two for Module 14), because each now teaches a hands-on task step by step |
| "Helpful Links" pages | One **Links** page per module, with every link checked live |
| Assignments of 5 to 300 points, irregular | Ten assignments of 100 points, one every 10 days, each graded 60 / 10 / 10 / 20 |
| Quizzes and attendance checks | Per-module ungraded practice assessments; attendance is not in the revised syllabus |
| Course Materials page (Springer textbooks for Unity) | Module 0 "Start Here": course map, AI policy, grading, explainers, toolchain |

## Old modules

| Old module | Where it went | What changed |
|---|---|---|
| 1. Game Design Document or GDD | **Module 5** (The GDD and virtual worlds); the first brief in **Module 1** | GDD teaching now ends in a design a coding agent can be held to, built with Walker's `/gdd` skill or its public prompt. "Guidance on Authorship" is covered by the AI policy page and `SOURCES.md`. |
| 2. Learning Unity Game Engine | **Modules 0 and 1** | Replaced by Godot and the command-line toolchain. "Unity C#" became GDScript, taught inside each module. "Awesome Unity Links" is retired. |
| 3. Unreal Engine | Not taught as an engine. Every lesson and chapter has a **If you know Unity or Unreal** section | Unreal is compared, not required. "Unreal Blueprints" maps to Godot scenes and signals (Module 4) and to behavior trees (Module 14). Two Unreal tutorial pages are retired. |
| 4. Projects | **Module 15** and Assignment 10; the "one game all semester" rule from Assignment 2 on | "Prototyping a Project" is absorbed by Modules 5 and 15. The list of student projects from past terms is not carried. |
| 5. Shaders & Materials | **Modules 6, 7 and 8** | Unity Shader Graph, CgFX and Unreal HLSL pages replaced by Godot shaders, materials and a shader-verification module. The ShaderToy video tutorial from the old page stays as a link; the ShaderToy site itself is left off because it blocks automated link checks. |
| 6. 2D Games | **Module 4**, and the 2D starters in Assignments 1 and 2 | The old page was one link list. |
| 7. Particle Effects | **Module 9** | Unity's particle system and VFX Graph replaced by Godot's four particle nodes and a measured cost. |
| 8. Animation | **Modules 10 and 11** | Animation in Blender, Unity and Unreal replaced by Godot's AnimationPlayer and state machines and Blender in Module 3. Spriter tutorials are not carried: the lessons teach Godot's own AnimationPlayer, AnimationTree and state machines. Two engine-neutral animation talks from the old page are carried as links. |
| 9. Audio | **Module 12** | One short page grew into a full module on triggers, buses and playback. |
| 10. Game AI | **Module 14** (main lesson and labs) | Finite state machines, behavior trees, navigation, procedural content and Q-learning are all taught hands-on. Reinforcement-learning pages on policy gradients, PPO and Open AI Gym are not carried as pages. |
| 11. Profiling/Optimization | **Module 13** | "Profiling in Unity and Unreal" replaced by Godot's profiler and a benchmark you run. |
| 12. Game AI with Unity | **Module 14** | NavMesh became Godot navigation; ML-Agents became the Q-learning lab; the Unity AI Planner is retired. |
| 13. Procedural Content Generation | **Module 14**, Lab B | Houdini is retired (the revised syllabus does not require it). |

Modules 2 and 3 of the new course (prompting game art; Blender MCP) have no old module: the old course covered generative art only as three mini-assignments.

## Old assignments and quizzes

| Old item (points) | Fate |
|---|---|
| Create a Game Design Document (5); Professional Game Design Documentation Using AI-Assisted Writing (15) | **Assignment 4** |
| Pitch Your Game Like It Matters (10) | Not carried as its own assignment. The pitch skills are touched by Assignment 4's design brief and Assignment 10's films. Say if it should return. |
| Assignment 2 – Learning Unity (100) | **Assignments 1 and 2** |
| Assignment 3 – Unreal Engine Blueprints (100) | Retired. Its Godot counterpart, a prop with collision and physics behavior in a scene, is part of **Assignment 3**. |
| Assignment 4 – Shaders (100): generative textures, storyboards, character design, deconstruct a PBR shader | Generative art moved to **Assignment 2**; the shader work is **Assignments 5 and 6** |
| Assignment 5 – Particle Effects (100) | **Assignment 7** |
| Assignment 6 – Animation (100) | **Assignment 8** |
| Mini-Assignments 1, 2, 3: generative art, animation, audio (25 each) | **Assignment 2** (art, sound, music) and **Assignment 8** (animation) |
| Show and Tell One, Two, Three (5 each) | The required Brutalist film inside every assignment; selected films are viewed in class |
| Take-Home Midterm: The AI Game Dev Mandate (100); Take-Home Final: Teaching AI in Game Development (100) | Replaced by the 10-day assignment cadence; no exams in the revised syllabus |
| Final Portfolio Piece (300) | **Assignment 10** (100 points, with two films) |
| Quizzes 1 to 3; attendance quizzes; Sample Midterm and Final | Per-module **practice assessments** (ungraded) |
| YouTube ID Submission (5) | Not carried; the film link goes in each assignment's submission note |

## Not carried over

These seven old items have no successor in the new course:

1. **Lecture Participation (100)**, because the revised syllabus lists no participation grade.
2. **Attendance quizzes**, for the same reason.
3. **The Springer textbook list** (Unity books), because the course is no longer built on them.
4. **Extra credit: TRACE survey; Substack article**, which are term-specific.
5. **Practice exams copied in from INFO 7390**, which belong to a different course.
6. **Unity-only and Unreal-only pages** (AI Planner, Unity ML-Agents as a Unity tool, twitch.tv Unreal streams, Endless Runner Unreal tutorial).
7. **Reinforcement-learning theory pages** (DQN, policy gradients, PPO, Open AI Gym), which the Q-learning lab replaces with something you can watch converge.

## What was read, and what was not

The export's modules, page text, assignments and quiz titles were read from a text extraction; its uploaded media (the `web_resources` folder) and any student data were not opened. The package built from the new course uses none of them.

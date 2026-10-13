# CSYE 7270 Building Virtual Environments course layout and writing audit

Audit date: October 12, 2026.

**Same-day update after the audit:** Professor Bear added an unnumbered [Conducting AI preface](chapters/preface-conducting-ai.md) before Module 0. The current sequence is **Preface → Module 0 → Modules 1–15**, seventeen modules/chapter texts. Each numbered lesson now explicitly applies the theme and ends with Unity and Unreal pointers. The original audit counts and cartridge observations below describe the pre-preface snapshot; see [the current module index](modules/README.md) and [teaching foundation](teaching-foundation.md).

The current Godot and Walker course has **all sixteen module and chapter drafts written: setup module 0 and teaching modules 1–15**. Each module maps to a substantial companion chapter. Together the chapter files contain 123,763 whitespace-delimited words, including code, tables and references. There are also sixteen links pages, sixteen six-question practice assessments, ten graded assignments and sixteen worked-example directories. Module 14 has an additional labs page.

Use the Fall 2026 sequence below as the course and companion-book spine. The original Spring 2026 IMSCC has thirteen modules organized around Unity and Unreal; it supplies the historical coverage, rather than the current teaching order. The revised Word syllabus, chapter index, module index and generated Fall cartridge agree on the new sequence.

**Written does not mean release-ready.** The repository records pending human review, visual and audio checks, a live Canvas import test, and specific chapter corrections. The current structural check passes with eleven warnings. No chapter is an empty placeholder, but several claims and demonstrations need correction or completion before their films can be presented as verified instruction.

## Course and chapter order

The numbers below are internal module/chapter identifiers. Public film titles should omit episode numbers and totals. Proposed playlist name: **Building Virtual Environments with Professor Bear**. Keep CSYE 7270 in course metadata and the description.

| Module and chapter | Chapter and proposed lecture subject | What the learner should be able to do | Existing practical work | Assignment connection |
|---|---|---|---|---|
| Preface | [Conducting AI Through Games and Virtual Worlds](chapters/preface-conducting-ai.md) | Direct AI toward a human experience; distinguish technical checks, play and judgment; explain Why Godot. | Ungraded brief and decision exercise; no installation required. | Orientation before Module 0. |
| 0 | [The Toolchain](chapters/00-the-toolchain.md) | Explain the roles of the coding agent, Walker, Godot and Git; establish a reproducible baseline and run checks independently. | Add a score to Walker Pong; investigate why both agents misread a regression test run without the required fixed frame rate. | Setup and practice. |
| 1 | [Walker and Godot](chapters/01-walker-and-godot.md) | Trace input through a scene and script to visible behavior; predict the consequences of a bounded change. | Trace Jumpman's jump input, change run speed, and explain which checks break. | A1: change the character and extend the playable level. The chapter exercise is a smaller prerequisite. |
| 2 | [Prompting Game Art and Sound](chapters/02-prompting-game-art.md) | Specify assets against engine constraints; check readability, import settings, provenance, animation frames, colliders and event-driven audio. | Import the termite reference into the game and connect sound to real events; investigate defects missed by passing tests. | A2: generate art, sound and music for the student's game. |
| 3 | [Blender to Godot](chapters/03-blender-mcp-to-godot.md) | Direct simple asset creation, inspect transforms and dimensions, export glTF, and verify the imported object. | Chapter: scripted checkpoint post and collision audit. Revised assignment: three simple assets through Blender MCP, one hand edit and a Godot display scene. | A3: first 3D assets. Align the chapter with the gentler assignment before filming. |
| 4 | [Scenes, Collision and Physics](chapters/04-scenes-collision-and-physics.md) | Explain scene ownership, nodes, signals, layers, masks and physics timing; distinguish a visual asset from its collision geometry. | Shield pickup in Dodge the Creeps; expose a test that passes despite an incorrect shield duration. | Preparation for A4; no separate graded assignment currently belongs to this module. |
| 5 | [The GDD and Virtual Worlds](chapters/05-the-gdd-and-virtual-worlds.md) | Turn a human intention into a checkable design contract; distinguish observed behavior from inferred or proposed design. | Recover and audit a GDD, then specify and implement a checkpoint interaction. Scope mobile, networking and XR claims carefully. | A4: specify and build one 3D interaction. |
| 6 | [Shader Foundations](chapters/06-shader-foundations.md) | Explain a shader's inputs and effect; specify appearance and timing before asking the agent to implement it. | Failure flash with typed uniforms, gameplay timing checks and a human visual check. | A5, with Module 7. |
| 7 | [Materials and Textures](chapters/07-materials-and-textures.md) | Audit texture channels, import settings, material parameters, lighting and attribution. | Ship-material audit; add ambient occlusion and check that it remains enabled after reimport. | A5: shader and material. |
| 8 | [Shader Verification](chapters/08-shader-verification.md) | Design independent checks for a plausible change that compiles and passes its original tests. | Frame-rate sweep, a model of expected pixel behavior, and a controlled visual comparison of the failure flash. | A6: audit a shader change. |
| 9 | [Particle Effects](chapters/09-particle-effects.md) | Control emission, lifetime, motion and restart behavior; separate CPU measurements from GPU cost and visual quality. | One-shot death burst; investigate misleading test reports and a benchmark that measured idle sleep. | A7: particle effects. |
| 10 | [Animation Foundations](chapters/10-animation-foundations.md) | Establish timing and hitbox behavior before altering animation tracks. | Pin sword timing, move the hitbox window into animation, and detect the lost second-swing hitbox. | A8, with Module 11. |
| 11 | [Animation and Interaction](chapters/11-animation-and-interaction.md) | Connect player actions and physics to animation state transitions; test interruption, landing and rapid state changes. | Ground/jump/fall state machine; reproduce and fix the landing-and-jumping edge case. | A8: animation and state. |
| 12 | [Audio and Triggers](chapters/12-audio-and-triggers.md) | Explain the difference between triggering a sound, routing it through a mix and hearing it correctly. | Rhythm-game hit click, Music/SFX buses, capture-based evidence, mute, pause and restart checks. | A9, with Module 13. |
| 13 | [Profiling and Optimization](chapters/13-profiling-and-optimization.md) | Define a performance question, measure the right instrument, preserve behavior and decide whether optimization is worth its cost. | Compare node-based and server-based bullet systems with parity checks and repeated measurements. | A9: audio and a performance budget. |
| 14 | [Game AI and Systems](chapters/14-game-ai-and-systems.md) | Direct and test autonomous behavior, navigation, reward learning, generated content and multiplayer authority. | Guard navigation, finite state machine and behavior tree; Lab A Q-learning; Lab B seeded generation with a validator; Lab C two-process networking. | A10, with Module 15. This is the largest and most densely packed chapter. |
| 15 | [Final Projects from Brief to Export](chapters/15-final-projects-brief-to-export.md) | Defend a finished game using a design contract, clean-clone reproduction, safe persistence, accessibility checks and a playable export. | Persistent best time; detect tests that contaminate real player saves; reproduce the project and diagnose a failed export. | A10: final project and evidence-based explanation. A successful exported build still needs demonstration. |

## How the teaching should progress

**Establish the working relationship, modules 0–1.** Begin with a runnable game and one small decision. The student is the director: choose the intended experience, set the boundary, predict a failure, delegate implementation and check the result. Explain Walker as a workflow and project context, rather than implying it is an executable students simply run.

**Create assets and specify the world, modules 2–5.** Progress from a usable 2D asset to simple 3D objects, then to scene behavior and a defensible design document. Introduce a short game brief from the start and refine it throughout; the full GDD chapter can remain fifth without postponing design judgment until then. The laboratory examples may use different Walker projects, while assignments develop the student's own continuing game.

**Control appearance and demand evidence, modules 6–9.** Teach a visible effect, its material inputs, an independent audit and its performance cost. Module 8 is an especially valuable explicit Computational Skepticism chapter: the test itself can be wrong, and a successful compile does not establish the intended appearance.

**Make the world respond, modules 10–13.** Move through animation, interaction and audio to measurement. Human playtesting belongs in every module, especially where readability, fairness, timing, sound or feel determines adequacy.

**Integrate behavior and deliver the game, modules 14–15.** Keep module 14 as one chapter under the requested one-module/one-chapter rule, but give it clearly separated internal parts: navigation and decisions; finite state machines and behavior trees; reward learning; procedural generation; networking authority. Start the final-project brief and milestones well before these weeks. Module 15 should close with an export another person can actually launch.

## What is written and what remains

| Material | Present | Readiness finding |
|---|---:|---|
| Companion chapters | 16 | Substantial drafts, approximately 5,700–13,300 words each by raw whitespace count. Human editorial and practical review remains recorded as pending. |
| Main module lessons | 16 | Substantial teaching text, approximately 3,800–4,650 raw words each, including code. |
| Extra module lecture page | 1 | Module 14 labs, in addition to its main lesson. |
| Helpful links pages | 16 | Present. This audit did not repeat the earlier live external-link checks. |
| Practice quizzes | 16 | Six questions each, 96 total; current structural checker passes. |
| Graded assignments | 10 | Present, nominally 100 points every ten days; assignment timing and final-project load need reconciliation. |
| Worked-example directories | 16 | Each has a README and supporting files. Their historical run claims were not rerun in this audit. |
| Generated Fall IMSCC | 1 | Contains 16 modules, 38 wiki pages, 10 assignment-settings files and 16 assessment-metadata files. All XML files parse. Live Canvas import remains unverified. |

### Corrections before release or filming

1. **Reconcile stale overview text.** `book.md` still says later modules are planned rather than written. Historical sections of `STATUS.md` still mark Chapter 1 unfinished, despite its newer opening reporting all chapters complete as drafts. The chapter index mentions only Assignments 1 and 2 even though ten exist. The filesystem and current indices resolve the writing-status question: all sixteen drafts exist.

2. **Update Chapter 3 and prove the MCP route.** The chapter explicitly says its live Blender MCP route was not run. The October 6 status notes report that its named tools and setup steps had already changed, and that the module lesson was updated while the chapter was not. The script-driven prop example is useful evidence, but it does not verify the live MCP workflow required by the revised beginner assignment. The source chapter, lesson, assignment and eventual film need one consistent, tested route.

3. **Finish the export demonstration.** Chapter 15 reports a failed export because matching templates were unavailable. That teaches useful diagnosis, but does not demonstrate the advertised delivery outcome. Add a successful export and actual launch/playtest before describing this as a complete shipping workflow.

4. **Resolve the existing chapter errata.** `STATUS.md` records stale repository-availability claims, a broken code fence in Chapter 7, unsupported wording in Chapter 5, an inaccurate description of one reviewer's shader prediction in Chapter 8, an overstatement of particle test success in Chapter 9, and inconsistent tool-instruction or command details. These are recorded issues, not corrections applied by this audit. Recheck version-sensitive claims against the pinned tools and primary documentation at film-design time.

5. **Reduce the final-project deadline pressure.** The existing plan ties A10 to Modules 14–15 and Day 100. The status report warns that the export lesson arrives around the deadline, while A10 combines game AI, persistence, menus, reproduction, export, updated design and two films. Introduce these requirements and checkpoints earlier, or revise the due date and scope. Do not leave the first export attempt to the last teaching week.

6. **Place the promised group project.** The syllabus promises both a group project and an individual project, while the status report identifies the ten assignments as individual. Specify which work is collaborative, what each student must defend, and how contributions are assessed.

7. **Do not imply full preservation of old advanced AI coverage.** The former course gave Game AI, Game AI with Unity and Procedural Content Generation separate modules. The current Chapter 14 consolidates them. DQN, policy gradients, PPO and Gymnasium receive conceptual treatment; the practical reinforcement-learning lab is tabular Q-learning. The chapter expressly says those neural methods are not run. Houdini and engine-specific production workflows are retired. This is a deliberate depth tradeoff, not a missing chapter file.

8. **Keep hardware-dependent outcomes qualified.** Mobile and XR are scoped in the design and performance discussions; networking has a loopback lab. These do not establish deployment on phones or headsets, real internet multiplayer, accessibility with assistive technology, or visual/audio quality. Those outcomes require their own evidence if a film claims them.

9. **Check student access and rebuild the Canvas artifact after revisions.** The October 6 status records concerns about public chapter/example links, availability of Walker's `/gdd` skill, course-provided film tools and platform-specific setup. Those live states were not rechecked here. Several module and assignment sources have modification times newer than the generated Fall cartridge, so its freshness is not established merely by its presence. Rebuild from the settled sources and perform a sandbox Canvas import before release.

## Original IMSCC module order

Read directly from `course_settings/module_meta.xml` inside the original Spring export, sorted by the module position field. This is the archival order, distinct from the revised Fall sequence above.

| Original position | Original module | Current location |
|---|---|---|
| 1 | Game Design Document or GDD | Module 5, with an initial brief in Module 1 and subsequent assignments. |
| 2 | Learning Unity Game Engine | Godot and Walker onboarding in Modules 0–1; Unity comparison sections remain. |
| 3 | Unreal Engine | Comparison sections throughout; scene behavior in Module 4. |
| 4 | Projects | Modules 5 and 15, plus the continuing assignment project. |
| 5 | Shaders & Materials | Modules 6–8. |
| 6 | 2D Games | Modules 1 and 4 and the 2D Walker examples throughout. |
| 7 | Particle Effects | Module 9. |
| 8 | Animation | Modules 10–11; Blender asset preparation in Module 3. |
| 9 | Audio | Module 12; generated audio also appears in Module 2. |
| 10 | Game AI | Module 14, main lesson and labs. |
| 11 | Profiling/Optimization | Module 13. |
| 12 | Game AI with Unity | Module 14, adapted to Godot; Unity-only tooling is not a required practical route. |
| 13 | Procedural Content Generation | Module 14, especially Lab B; Houdini is not retained as required tooling. |

The original export has 58 wiki HTML pages and 450 manifest resources. Many pages are brief link collections, but the existing `canvas/OLD-TO-NEW.md` claim that only three pages contain more than links is too strong. Direct inspection also finds explanatory prose in the GDD, Q-learning, DQN and policy-gradient pages. Their approximate extracted lengths are 880, 574, 421 and 342 words respectively, including titles and links. Retain that teaching value when deciding what to condense or retire.

## Film series arrangement

Use **one canonical chapter lecture per module**, in the Fall sequence, with Liam narrating for Professor Bear and the Brutalist lecture format. This is a course-level arrangement, not sixteen completed film designs. Detailed film design must read each whole chapter and its evidence, resolve the relevant errata, and map every substantive section into acts.

Existing `youtube/` folders already cover orientation, conducting AI for games, Walker, Godot, Assignment 1, character consistency, first Blender assets and Blender-to-Godot transfer. Treat these as candidates for reuse or supplemental viewing. A generated STATUS file saying all beats are filled is not evidence that a final master is current, watched or published; this audit does not certify those films.

The lecture skill calls for a whole-source, self-contained film with a narrated title, framing, key terms, visual acts, recap, a practical Your Turn prompt and two checks, and the channel outro. Runtime follows the source; no fixed episode duration or public numbering is needed. Chapter 14 may therefore be a long film with distinct acts; do not silently omit labs to make it shorter.

Every lecture should make the three recurring themes concrete:

- **Conducting AI:** the human chooses the intended experience and acceptance criteria; the agent implements and helps gather evidence. Show a decision being made, not simply a prompt being typed.
- **Computational Skepticism:** make a prediction, inspect the actual artifact, challenge the test, and perform an independent check. A green test suite is evidence for specific assertions, not a blanket quality certificate.
- **Irreducibly Human:** the human retains responsibility for value, meaning, fairness, accessibility and the lived experience of play. Show where technical conformance still leaves a judgment unanswered.

When individual films are commissioned, prepare the film directory, design and Claude Code build prompt. Bear pastes the prompt into Claude Code for production, as established for the parallel Claude courses. This audit builds no films and makes no publication changes.

## Evidence and verification

Primary local sources: [module index](modules/README.md), [chapter index](chapters/README.md), [course status](STATUS.md), [course map](modules/00-start-here/course-map.md), [old-to-new mapping](canvas/OLD-TO-NEW.md), [Canvas delivery notes](canvas/README.md), [Word syllabus](CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx), the original Spring IMSCC, and `canvas/package/csye7270-fall-2026-godot-walker.imscc`.

The audit inspected both cartridge module lists, the original manifest and selected original teaching pages, the revised syllabus schedule, chapter inventories/headings/executive summaries and selected issue-bearing sections, module and assignment indices, example-directory presence and existing film status summaries. It is a coverage and readiness audit, not a line-by-line technical review of all 123,763 chapter words.

`python3 scripts/check_course.py` was run on October 12, 2026: **61 files checked, 0 failures, 11 warnings**. The warnings concern missing executive summaries in legacy Assignments 1–2, no recognized assignment tag in A1, excessive length in A2, and five slightly long module lessons. This checker validates source structure and selected local constraints; it does not test the games, verify external claims, or establish Canvas acceptance. Output is preserved in [the audit check log](pantry/reports/course-layout-checks-2026-10-12.txt).

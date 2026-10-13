# CSYE 7270 — Build and review status

Updated: October 12, 2026.

## Remaining assignment pacing — October 12, 2026

The [Fall 2026 assignment schedule](assignments/fall-2026-assignment-schedule.md) records the four existing live CSYE deadlines and the seven reference-course dates read from Canvas. Planned deadlines for Assignments 4–10 are October 25, November 3, November 13, November 23, December 3, December 13 and December 20, all at 11:59 pm America/New_York. They have been added to the local drafts and indexes, not posted to Canvas. Assignment 4 now explicitly refines the retained October 19 five-point GDD and covers Modules 4–5. The final brief starts October 19 with preparation targets throughout the term.

Live CSYE Canvas contains an unpublished 250-point Final Portfolio Piece; the local Assignment 10 draft remains 100 points. This date-planning pass changes neither grading value. The generated package still has ten numbered assignments and blank due-date metadata; it does not recreate the live separate GDD or reconcile legacy Canvas records. The Word syllabus has not been revised in this pass. Course pages were read through the browser; no live import, editing or publication occurred.

## Conducting AI preface and engine comparisons — October 12, 2026

At Professor Bear's direction, the course now begins with an unnumbered **Conducting AI Through Games and Virtual Worlds** preface before Module 0. The [preface chapter](chapters/preface-conducting-ai.md), module lesson, links and six-question practice quiz establish Conducting AI as the recurring method. [Teaching foundation](teaching-foundation.md) maps delegation, evidence and human judgment across all modules.

All numbered lessons now have a Conducting AI decision section and close with separate Unity and Unreal comparison pointers. Existing comparative tables and their historical documentation caveats are preserved. The preface explains Godot's direct file-and-command workflow without requiring MCP, distinguishes other engines' scripting routes, and dates vendor maturity claims to their cited evidence. The existing Why Godot film has a course-alignment note; no film or narration was rendered or regenerated.

The builder includes the preface first without changing existing module identities or numbers. The generated Canvas syllabus receives a preface note; the Word syllabus itself still predates this addition. Historical completion notes below retain their original scope. No human review or book gate is signed by this revision.

Verification: [source checker](pantry/reports/preface-course-checks-2026-10-12.txt) reports 64 files, 0 failures and 22 warnings (six legacy assignment warnings and sixteen lesson-length warnings after the requested closing material). [Local Canvas build](pantry/reports/preface-canvas-build-2026-10-12.txt) reports 17 modules, 40 pages, 10 assignments and 17 quizzes; package integrity passes. Checked the first-module placement, sequential positions, retained Module 0–15 identifiers, unpublished state, generated comparisons and syllabus preface note. There are now 102 ungraded quiz questions. A live Canvas import remains untested.


## Executive summary

**What this is.** The honest build status of the CSYE 7270 course conversion from Unity/Unreal to Godot and Walker.

**What changed on 2026-09-27.** At Professor Bear's request ("this course needs to be adapted for Godot … hands on … a chapter and example for doing this with a CLI like Claude Code or Codex, the Walker tool and Godot … look at the .imscc for what to build … end of each chapter … similarities/differences … Unity … Unreal"), all sixteen companion-book chapters were drafted in [`chapters/`](chapters/README.md). There is one per module of the revised syllabus, plus a Chapter 0 for the command-line toolchain. Each has a hands-on example that was really run with Claude Code and/or Codex against a public Walker project and verified headless, recorded in [`examples/`](examples/). Each ends with Unity and Unreal comparison sections sourced to vendor documentation. The writing contract is [`pantry/chapter-spec.md`](pantry/chapter-spec.md).

**What changed on 2026-10-06.** At Professor Bear's request ("all of the modules need to be reworked … examples using Godot … Walker … Claude Code … build out a full course, step by step, modeled on the old Canvas course"), the chapters were turned into a complete Canvas course: sixteen modules (a setup module and one per week), each with a lecture page, a Helpful-links page and an ungraded practice quiz; Assignments 3 to 10 beside the existing 1 and 2, one per 10 days; and a script that builds an importable Canvas package from all of it. The old export's structure was kept and its Unity and Unreal content was not; [`canvas/OLD-TO-NEW.md`](canvas/OLD-TO-NEW.md) accounts for every old item. See "Canvas course build — 2026-10-06" below, including the decisions that are yours.

**What has not happened.** No human has reviewed the chapters. No AI+1 book gate is signed. Nothing visual or audible has been checked by a person. Unity and Unreal were not run. Nothing from this work has been committed or pushed. The Blueprint checkboxes below remain unsigned.

## Canvas course build — 2026-10-06

- [x] Sixteen module lessons (Modules 0–15; Module 14 has a second page for its labs), each condensed from its chapter with the prompts and commands that were really run, a "what the agents got wrong" section and a Unity/Unreal bridge. [`modules/README.md`](modules/README.md) is the index. Module 1's lesson was restructured into the shared skeleton with its drafted text kept; the original is in `pantry/backups/`.
- [x] Sixteen Helpful-links pages. Every external link was checked live (230 URLs; the one that blocks automated checkers was left off).
- [x] Sixteen ungraded practice quizzes, six questions each. Three independent blind checkers answered all 96 and matched the keys. They also found the quizzes were guessable by length (the correct choice was the longest in 81 of 96 questions); the distractors were rewritten (now 17 of 96), and the checker enforces it.
- [x] Assignments 3 to 10, each fact-checked by an independent agent against the chapters, the example records, the Godot docs and the live Walker repositories. Their errors were fixed; their design concerns are listed below.
- [x] **Assignment 3 was rewritten on 2026-10-06** at Professor Bear's request ("a very basic … Claude, the Blender MCP, and Blender to make a very simple model … a game asset or two, let's say three simple 3D assets, preferably some that they think for their game"). It is now [`03-first-3d-assets-with-blender-mcp.md`](assignments/03-first-3d-assets-with-blender-mcp.md): three simple assets built with Claude through the Blender MCP, one hand edit, exported as `.glb` and shown in a small Godot 3D scene; same 60 / 10 / 10 / 20 grading. The heavier first version (a prop with a collider, physics layers and mutation tests) is saved in `pantry/backups/` and can become part of a later assignment.
- [x] A Canvas package and per-page HTML pastes, built by `scripts/build_course.py` and checked by `scripts/check_course.py`. See [`canvas/README.md`](canvas/README.md).
- [ ] **Import test in a live Canvas.** Never done; nothing here has access to one. The least certain part is quizzes inside modules.
- [ ] Human review of every module, quiz and assignment. No student has tried any assignment.
- [ ] Each lesson's fidelity to its chapter was checked by an agent, not by a person. Visual, audible and feel judgments remain human checks, as in the chapters.

### Decisions that are Professor Bear's

1. **Group project.** The syllabus says "a group project and an individual project." All ten assignments are individual. Say where the group project goes (for example, a team version of Assignment 8 or 10) and it will be written.
2. **Final-project workload and grading.** The October 12 plan releases the final brief with the October 19 GDD, stages the systems feature, persistence, menu and export rehearsal through November, and reserves December 13–20 for integration and delivery. This replaces the old late-release plan. Workload still needs human review. The live unpublished final portfolio is 250 points, while local Assignment 10 is 100; reconcile before posting.
3. **Assignments 4 to 6 and 8 are heavy too,** mostly because each needs a native-4K Brutalist film on a large toolchain (Node/Remotion, a local voice model, ffmpeg), and render time is not budgeted. The chapters' own runs hit Claude Code session limits repeatedly. Consider whether every assignment needs a film.
4. **Push the course repository.** `chapters/` and `examples/` are not on GitHub, so every chapter and example link in the Canvas pages is dead, and Assignment 6 Part A cannot be done without a local `examples/` folder. This needs your word.
5. **Publish Walker's `/gdd` skill,** or accept the public prompt as the permanent route. Public Walker `main` has `prompts/zelda-gdd.md` but no `gdd/` folder. Assignment 4 tells students to keep the skill out of their pushed repositories until you decide.
6. **Licenses.** `walker-jumpman` and `walker-jumpman-clawd` have no license file; the demo adaptations are MIT. The lessons say so and tell students to credit them. Decide whether to license the two Jumpman repositories.
7. **Windows and Linux were never tried.** Every recorded command ran on macOS; `timeout` and the Blender path differ elsewhere.
8. **The Brutalist `godot-*` skills** are referred to as "course-provided." Students need that checkout, and a way to keep game audio in the film (Assignment 9 was reworded to what the skill's audio policy supports).
9. **Assignment 6 Part B** (the student's own agent seeds a flawed change, sealed until the student gives a verdict) and **Assignment 7's** upper-bound method for pricing a one-shot burst are the writers' designs; no chapter ran either.

10. **Assignment 3 depends on a route nobody on this course has run, and the project is moving fast.** Chapter 3 documents the Blender MCP setup as "not run" (it needs the Blender window, and `uv` was not installed on the instructor's Mac). A check on 2026-10-06 found the project had already changed nine days after the chapter: version 2.1.1 became 2.1.9, `get_object_info`, `get_viewport_screenshot` and `export_scene` were removed (`look` was added), the add-on now starts its server automatically, and the README now leads with a one-line installer that finds the MCP clients on the machine and offers to set up each one. The assignment names both versions and tells students to use the manual steps. Before release, someone should run the route once, end to end, and either correct the assignment or pin a version. Students who cannot connect within about two hours switch to the script route and keep up to 6 of the 8 process points. The assignment is also long (about 3,700 words, most of it the shared grading text) for a "very basic" task; trim if you prefer.
11. **Module 4 no longer has an assignment of its own.** Assignment 3 now covers Module 3 only, so the collision, layer and physics material of Module 4 is first used in Assignment 4's interaction. If you want Module 4 graded on its own, the old heavier Assignment 3 (in `pantry/backups/`) is the natural source.

### Chapter errors found while building the course (chapters were not edited)

- **Stale "not public" sentences** in Chapters 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14 and 15 and `examples/14/README.md`: each contradicts its own "Get the builds" paragraph. Every repository named returns 200 on GitHub.
- Chapter 5: "OpenXR is the recommended XR interface" is not on the Godot page (it calls OpenXR "a core interface"); "30 design commands from Forge" but the groups it lists sum to 20; the `design/` folder it calls local-only was pushed on 27 September.
- Chapter 7: a broken code fence near lines 392 to 397; "four licences" for `walker-3d-decals` is four assets under three licences; lines 182 and 353 disagree about the starting copy.
- Chapter 8: "both review agents predicted white" — only Claude Code's review did; Codex said "the default texture sample."
- Chapter 9: "Every state check passed on that version" — that version's own test had one FAIL.
- Chapter 0: says Claude Code reads `AGENTS.md` when there is no `CLAUDE.md`, but only from version 2.1.277; the course's 2.1.150 did not (Chapter 1 records it). "Passed ten out of ten" reads like ten runs; it was ten checks.
- Chapter 3: the concave-shape quotation is a misquote of the Godot page. The MCP passages (about lines 44 and 233 to 236) still name the removed tools and say to "start the server"; Module 3's lesson was updated, the chapter was not.
- Chapter 15 and others: some headless commands lack `timeout`, which the writing contract requires.

## Companion chapters — 2026-09-27

- [x] Sixteen chapter drafts (Ch 0–15), about 140,000 words, in `chapters/`. All pass the spec's structural checks (section order, Unity/Unreal last, example folder present, no local paths).
- [x] Worked-example records for every chapter in `examples/` (about 17 MB, including transcripts with machine paths and account metadata removed).
- [ ] Human review of every chapter, especially the "What we actually ran" sections and the Unity/Unreal comparisons.
- [ ] Human checks each chapter lists (visual, audio, feel), done by a person with a screen.
- [ ] Decision to publish the Walker `/gdd` skill (Chapter 5 and Assignment 2 depend on it; it exists only in the local Walker working copy).
- [ ] Decision on committing and pushing `chapters/`, `examples/` and `pantry/chapter-spec.md` to the course repository.

## Current scope

Rebuild the course around Walker and Godot. **Superseded 2026-10-06:** the requested delivery is now the whole course (Modules 0–15, Assignments 1–10) as an importable Canvas package plus per-page pastes; see "Canvas course build" above. Earlier scope: revised syllabus and manual Canvas pastes for Module 1 and its separate 100-point assignment. The original export and source attachments are preserved. The instructor has replaced the immediate IMSCC request with manual pasting; a companion book chapter remains separate future work.

## Blueprint

- [ ] Vision reviewed by Professor Brown.
- [ ] Architecture and module/chapter sequence approved.
- [ ] Chapter specifications approved.
- [ ] Risks and assessment plan approved.

The initial vision is drafted. Professor Brown confirmed **Fall 2026** and **10% per day** for late work on September 10, 2026 ("10% daily Fall 2026"). The vision records these decisions. Review-draft batching remains awaiting an answer; the policy and term confirmation is not recorded as approval of the entire Blueprint. No formal AI+1 book gate has been signed.

## Requested deliverables

The instructor's grading clarification is recorded in `prerequisites/assessment-policy.md` and `assignments/rubrics/25-point-explainer.md`: 60% assignment-specific work, 10% Frictional, 10% GitHub/Canvas version matching, and 20% Relative Quartile. The 25-point explanation criteria are preserved as 6 + 4 + 3 + 2. These policy artifacts do not constitute completion or approval of the syllabus, Module 1, or IMSCC.

Subsequent instructor directions: **100-point assignments every 10 days**, each including a required explainer using Brutalist's Godot skills. The 25-point rubric remains a reference example only. `prerequisites/ai-policy.md`, `prerequisites/brutalist-godot-explainers.md`, and `assignments/rubrics/100-point-assignment.md` record the adaptation and the clean AI-policy video URL. The 60-point task-specific work includes implementation and explanation; the other categories remain 10 / 10 / 20. No extra video-points category or exact assignment dates have been invented.

- [x] Revised Word syllabus, preserving source typography and institutional boilerplate; rendered and visually reviewed across all 21 pages.
- [x] Module 1 teaching draft: What is Walker? and What is Godot?, learning loop, setup, and ungraded practice.
- [x] Separate teaching draft: Assignment 1 - Extend Walker Jumpman, 100 points.
- [x] Two separate Canvas HTML paste files, with editable Markdown sources.
- [ ] Matching formal book Chapter 1 (not authorized by completion of these course drafts).
- [ ] Human review / actual Canvas paste check.

## Manual Canvas delivery

The instructor requested manual Canvas content rather than an IMSCC, clarified that the 100-point assignment is a second paste, specified the Walker/Godot lesson topics, and named **Assignment 1 - Extend Walker Jumpman**. The lesson is `modules/01-walker-and-godot/lesson.md`; the assignment is `assignments/01-extend-walker-jumpman.md`. The `canvas/` folder holds separate HTML fragments and instructor review notes. No remote Canvas changes, book-gate signatures, or changes to the Word syllabus were made. (On 2026-10-06 the same `canvas/` folder gained a package builder; see above. The three fragments from this earlier delivery remain but are superseded by `canvas/paste/`.)

## Word syllabus delivery — September 10, 2026

Professor Brown explicitly requested corrections and additions to `CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx`, with the boilerplate and typography preserved. That targeted edit is complete; it does not sign any AI+1 book gate. The DOCX now includes Fall 2026, Walker/Godot, the revised first three weeks, one module per chapter, 100-point assignments every 10 days, the 60/10/10/20 rubric, required Brutalist Godot explainers, human/AI attribution, the AI-policy video link, and a consistent 10% daily late penalty. The final course letter-grade curve is unchanged.

The administrative placeholder about an unspecified section/meeting schedule/deadlines was removed from `vision.md` at the instructor's request and is not in the Word syllabus. No Spring 2026 dates were introduced. The original DOCX is retained in `pantry/backups/`; the original IMSCC is untouched. See `pantry/reports/syllabus-fall-2026-qa.md` and the adjacent edit audit for preservation and rendering checks. Module 1, its chapter, and the new Canvas cartridge remain separate unfinished deliverables.

## Source issues to avoid carrying forward

- The pasted syllabus mixes Unity/Unreal requirements with the new Walker framing.
- It contains both 5% and 10% daily late penalties; the instructor has resolved this in favor of 10% per day for the revised syllabus.
- It assumes command adapters and media pipelines that do not describe the current Walker/Godot starter.
- The existing Walker root README and engine guide retain legacy C#/.NET guidance; the standalone walker-jumpman game is GDScript and runs in the regular Godot editor.
- AI1's quick Blueprint recipe is used for course planning. Its canonical library's unrelated biology-specific block is not adopted. AI1's human-signoff constitution takes precedence over conflicting agent-signoff text in its status/verification guidance. No canonical toolkit files are being changed.

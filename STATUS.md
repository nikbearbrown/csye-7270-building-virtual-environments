# CSYE 7270 — Build and review status

Updated: October 6, 2026.

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
- [x] A Canvas package and per-page HTML pastes, built by `scripts/build_course.py` and checked by `scripts/check_course.py`. See [`canvas/README.md`](canvas/README.md).
- [ ] **Import test in a live Canvas.** Never done; nothing here has access to one. The least certain part is quizzes inside modules.
- [ ] Human review of every module, quiz and assignment. No student has tried any assignment.
- [ ] Each lesson's fidelity to its chapter was checked by an agent, not by a person. Visual, audible and feel judgments remain human checks, as in the chapters.

### Decisions that are Professor Bear's

1. **Group project.** The syllabus says "a group project and an individual project." All ten assignments are individual. Say where the group project goes (for example, a team version of Assignment 8 or 10) and it will be written.
2. **Assignment 10 is probably too big for about 8 to 10 days at 100 points.** It replaces a 300-point final and asks for a game-AI element with tests and an audit, persistence, a keyboard-only menu, a clean-clone rebuild, an export attempt, a GDD update, two 4K films, and every earlier layer still working. It opens with Module 14 (about Day 92) and Module 15, which teaches export and persistence, arrives the day before it is due. Options: move the final project's due date, trim the requirements, or give it more weight.
3. **Assignments 4 to 6 and 8 are heavy too,** mostly because each needs a native-4K Brutalist film on a large toolchain (Node/Remotion, a local voice model, ffmpeg), and render time is not budgeted. The chapters' own runs hit Claude Code session limits repeatedly. Consider whether every assignment needs a film.
4. **Push the course repository.** `chapters/` and `examples/` are not on GitHub, so every chapter and example link in the Canvas pages is dead, and Assignment 6 Part A cannot be done without a local `examples/` folder. This needs your word.
5. **Publish Walker's `/gdd` skill,** or accept the public prompt as the permanent route. Public Walker `main` has `prompts/zelda-gdd.md` but no `gdd/` folder. Assignment 4 tells students to keep the skill out of their pushed repositories until you decide.
6. **Licenses.** `walker-jumpman` and `walker-jumpman-clawd` have no license file; the demo adaptations are MIT. The lessons say so and tell students to credit them. Decide whether to license the two Jumpman repositories.
7. **Windows and Linux were never tried.** Every recorded command ran on macOS; `timeout` and the Blender path differ elsewhere.
8. **The Brutalist `godot-*` skills** are referred to as "course-provided." Students need that checkout, and a way to keep game audio in the film (Assignment 9 was reworded to what the skill's audio policy supports).
9. **Assignment 6 Part B** (the student's own agent seeds a flawed change, sealed until the student gives a verdict) and **Assignment 7's** upper-bound method for pricing a one-shot burst are the writers' designs; no chapter ran either.

### Chapter errors found while building the course (chapters were not edited)

- **Stale "not public" sentences** in Chapters 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14 and 15 and `examples/14/README.md`: each contradicts its own "Get the builds" paragraph. Every repository named returns 200 on GitHub.
- Chapter 5: "OpenXR is the recommended XR interface" is not on the Godot page (it calls OpenXR "a core interface"); "30 design commands from Forge" but the groups it lists sum to 20; the `design/` folder it calls local-only was pushed on 27 September.
- Chapter 7: a broken code fence near lines 392 to 397; "four licences" for `walker-3d-decals` is four assets under three licences; lines 182 and 353 disagree about the starting copy.
- Chapter 8: "both review agents predicted white" — only Claude Code's review did; Codex said "the default texture sample."
- Chapter 9: "Every state check passed on that version" — that version's own test had one FAIL.
- Chapter 0: says Claude Code reads `AGENTS.md` when there is no `CLAUDE.md`, but only from version 2.1.277; the course's 2.1.150 did not (Chapter 1 records it). "Passed ten out of ten" reads like ten runs; it was ten checks.
- Chapter 3: the concave-shape quotation is a misquote of the Godot page.
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

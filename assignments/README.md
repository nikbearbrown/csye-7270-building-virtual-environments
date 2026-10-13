# Assignments — CSYE 7270, Fall 2026

## Executive summary

**What this is.** The ten numbered assignment drafts, in order, plus the existing five-point GDD milestone. The numbered drafts retain their **100-point** rubrics and required Brutalist Godot films. The [Fall 2026 schedule](fall-2026-assignment-schedule.md) preserves the first four live deadlines and proposes the remaining dates, close to the reference course’s pacing. Canvas supplies the official deadlines. The live legacy final is 250 points; its difference from the 100-point local final draft remains unresolved.

**Why read it.** It shows which assignment covers which modules, when each is suggested to be due, and which film each one requires. It also states the one rule that ties them together: from Assignment 2 on, every assignment adds a layer to the same game.

**What it decided.** Assignments 1 and 2 were already written. Assignments 3 to 10 were added on 2026-10-06, one per 10-day step, each covering every module released since the last one. The October 12 schedule supersedes those relative day numbers and preserves the separately posted GDD. The final project is Assignment 10. All ten are **individual**; the syllabus line about "a group project and an individual project" has no assignment yet and is an open instructor decision.

---

Read [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz), the [written course AI policy](../prerequisites/ai-policy.md), and the [Godot explainer requirements](../prerequisites/brutalist-godot-explainers.md).

The [100-point grading framework](rubrics/100-point-assignment.md) allocates 60 to implementation and explanation, 10 to Frictional, 10 to GitHub/Canvas version matching, and 20 to Relative Quartile. Late work loses 10% per day.

## The ten assignments

All dates are in 2026 at 11:59 pm America/New_York. Assignments 1–3 and the GDD are confirmed in Canvas; Assignments 4–10 are planned locally and await posting. Release the final brief by October 19 and develop it throughout the remaining assignments.

| # | Assignment | Covers | Due | Required film (`walker` modifier) |
|---|---|---|---|---|
| 1 | [Extend Walker Jumpman](01-extend-walker-jumpman.md) | Module 1 | Sep 24 | `godot-walkthrough` |
| 2 | [Generate Art, Sound, and Music for Your Game](02-generate-art-sound-music-for-your-game.md) | Module 2 | Oct 7 | `godot-gamedev` |
| 3 | [Your First 3D Game Assets with Claude, the Blender MCP, and Blender](03-first-3d-assets-with-blender-mcp.md) | Module 3 | Oct 15 | `godot-gamedev` |
| GDD | Create a Game Design Document or GDD — existing 5-point milestone | Design preparation | Oct 19 | Follow the existing Canvas brief |
| 4 | [Specify It, Then Build One 3D Interaction](04-specify-and-build-a-3d-interaction.md) | Modules 4, 5 | Oct 25 (planned) | `godot-gdd` |
| 5 | [A Shader and a Material That Say Something About Your Game](05-shader-and-material.md) | Modules 6, 7 | Nov 3 (planned) | `godot-gamedev` |
| 6 | [Audit a Plausible but Incorrect Shader Change](06-audit-a-shader-change.md) | Module 8 | Nov 13 (planned) | `godot-gamedev` |
| 7 | [Two Particle Effects, Tuned and Priced](07-particle-effects.md) | Module 9 | Nov 23 (planned) | `godot-walkthrough` |
| 8 | [Animation Wired to Player Actions](08-animation-and-state.md) | Modules 10, 11 | Dec 3 (planned) | `godot-walkthrough` |
| 9 | [Sound That Provably Plays, and a Frame You Can Afford](09-audio-and-a-performance-budget.md) | Modules 12, 13 | Dec 13 (planned) | `godot-gamedev` |
| 10 | [Final Project: From Brief to Export](10-final-project.md) | Modules 14, 15 and the whole course | Dec 20 (planned) | `godot-walkthrough` and `godot-gdd` |

## Open and copy assignments into Canvas

Open an assignment's Markdown link above to read it in the artifact panel. For reliable Canvas formatting, open its HTML file below, copy the entire HTML source, and paste it into the Canvas assignment editor in **HTML editor** mode. Switch back to the rich-content view to inspect the result before saving. Set the due date and points in Canvas's separate fields; copying the description does not set them.

The first three assignment descriptions are included in this repository, with their confirmed due dates. The separate five-point GDD remains the existing Canvas assignment; its body is not duplicated here. The final-project points discrepancy is recorded in the schedule and still needs reconciliation before posting.

| Assignment | Canvas HTML source |
|---|---|
| Assignment 1 - Extend Walker Jumpman | [Open HTML](../canvas/paste/assignment-assignment-1-extend-walker-jumpman.html) |
| Assignment 2 - Generate Art, Sound, and Music for Your Game | [Open HTML](../canvas/paste/assignment-assignment-2-generate-art-sound-and-music-for-your-game.html) |
| Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender | [Open HTML](../canvas/paste/assignment-assignment-3-your-first-3d-game-assets-with-claude-the-blender-mcp-and-blender.html) |
| Assignment 4 - Specify It, Then Build One 3D Interaction | [Open HTML](../canvas/paste/assignment-assignment-4-specify-it-then-build-one-3d-interaction.html) |
| Assignment 5 - A Shader and a Material That Say Something About Your Game | [Open HTML](../canvas/paste/assignment-assignment-5-a-shader-and-a-material-that-say-something-about-your-game.html) |
| Assignment 6 - Audit a Plausible but Incorrect Shader Change | [Open HTML](../canvas/paste/assignment-assignment-6-audit-a-plausible-but-incorrect-shader-change.html) |
| Assignment 7 - Two Particle Effects, Tuned and Priced | [Open HTML](../canvas/paste/assignment-assignment-7-two-particle-effects-tuned-and-priced.html) |
| Assignment 8 - Animation Wired to Player Actions | [Open HTML](../canvas/paste/assignment-assignment-8-animation-wired-to-player-actions.html) |
| Assignment 9 - Sound That Provably Plays, and a Frame You Can Afford | [Open HTML](../canvas/paste/assignment-assignment-9-sound-that-provably-plays-and-a-frame-you-can-afford.html) |
| Assignment 10 - Final Project: From Brief to Export | [Open HTML](../canvas/paste/assignment-assignment-10-final-project-from-brief-to-export.html) |

These HTML files are regenerated from the Markdown sources by `python3 scripts/build_course.py`; edit the Markdown sources when revising an assignment.

## One game all semester

Assignment 1 is the Walker Jumpman starter. In Assignment 2 each student chooses the game they actually want to build, in a repository whose name begins `walker-`. Assignments 3 to 10 each add one layer to that same repository, and each is submitted as a git tag on it (`a3`, `a4`, … `a10`). A student whose game is 2D adds a 3D scene to it when an assignment needs one. A student may change games once, before Assignment 4, with a written justification in `FRICTIONAL.md`.

## Where each assignment is in Canvas

An assignment appears in the first module it covers, and again in the second module of a pair, so a student sees it in every module whose material it uses. The Canvas pastes and the importable package are generated from these Markdown files; see [../canvas/README.md](../canvas/README.md).

## Status

These are review drafts. Assignments 3 to 10 were written by sub-agents from the companion chapters and then fact-checked by independent sub-agents; no human has reviewed them, and no assignment has been tried by a student. Open items for the instructor are in [../STATUS.md](../STATUS.md).

The 25-point rubric in [rubrics/](rubrics/25-point-explainer.md) is a reference example, not a scheduled assignment.

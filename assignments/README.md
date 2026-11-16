# Assignments — CSYE 7270, Fall 2026

The repository now follows the Fall 2026 Canvas export supplied on October 14, 2026. Canvas is authoritative for Assignments 1–9, their titles, point values, deadlines and submission settings. The instructor’s pasted replacement is authoritative for Assignment 10; the export confirms its 250-point value and December 20 deadline.

Assignment 4 is the five-point GDD. It is part of this ten-assignment sequence, not an additional milestone. Assignment 8 is a 50-point pitch. The seven 100-point assignments, GDD, pitch and 250-point final total **1,005 points**. Individual briefs govern their grading; the GDD does not inherit a 100-point rubric.

| # | Assignment | Points | Due (America/New_York) | Modules | Required film |
|---|---|---:|---|---|---|
| 1 | [Assignment 1 - Extend Walker Jumpman](01-extend-walker-jumpman.md) | 100 | 2026-09-24, 11:59 pm | 1 | godot-walkthrough |
| 2 | [Assignment 2 - Generate Art, Sound, and Music for Your Game](02-generate-art-sound-music-for-your-game.md) | 100 | 2026-10-07, 11:59 pm | 2 | godot-gamedev |
| 3 | [Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender](03-first-3d-assets-with-blender-mcp.md) | 100 | 2026-10-15, 11:59 pm | 3 | godot-gamedev |
| 4 | [Assignment 4 - Create a Game Design Document or GDD](04-create-a-game-design-document.md) | 5 | 2026-10-19, 11:59 pm | 5 | No film specified |
| 5 | [Assignment 5 - Shaders, Materials, and the Godot Shading Language](05-shaders-materials-and-godot-shading-language.md) | 100 | 2026-10-29, 11:59 pm | 6, 7 | godot-gamedev |
| 6 | [Assignment 6 - Creating Particle Effects with Godot and Claude](06-creating-particle-effects.md) | 100 | 2026-11-03, 11:59 pm | 9 | godot-gamedev |
| 7 | [Assignment 7 - Doing Animation with Claude and Godot](07-doing-animation.md) | 100 | 2026-11-15, 11:59 pm | 10, 11 | godot-walkthrough |
| 8 | [Assignment 8 - Final Project Pitch Film — Show What You Will Build](08-final-project-pitch-film.md) | 50 | 2026-11-22, 11:59 pm | 5, 15 | Brutalist pitch film |
| 9 | [Assignment 9 - Teach One Game-AI Technique: Explain, Show, Try](09-teach-one-game-ai-technique.md) | 100 | 2026-12-12, 11:59 pm | 14 | godot-walkthrough (Explain → Show → Try) |
| 10 | [Assignment 10 - Final Project: From Brief to Export](10-final-project.md) | 250 | 2026-12-20, 11:59 pm | 15 | godot-walkthrough + godot-gdd |

## One project and its evidence

From Assignment 2 onward, use the chosen `walker-` project and the revisions/tagging required by each brief. The final integrates the semester’s work, Assignment 9’s technique, persistence, a menu, pitch reconciliation and clean-clone/export evidence. Read the exact assignment before treating a lesson exercise as a graded requirement.

Read the [AI policy](../prerequisites/ai-policy.md) and [film requirements](../prerequisites/brutalist-godot-explainers.md). The 10% daily late penalty remains. Canvas’s deadline field is authoritative.

## Sources and generated copies

[canvas-authority.json](canvas-authority.json) records the exported settings and source paths. Public assignment HTML/XML snapshots are in [canvas/assignment-sources](../canvas/assignment-sources/). Superseded local drafts are retained in the dated pantry backup; they are historical and are not generated as active assignments.

Run `python3 scripts/build_course.py` to regenerate local HTML fragments and the importable course package. The builder uses the assignment metadata for actual points, due dates and submission types. Its default generated publication state remains unpublished. No live Canvas records are changed by building.

The exported [TRACE extra-credit assignment](extra-credit-trace-survey.md) is also retained, with its five-point value and unset deadline. [Other gradebook records](../canvas/gradebook-records.md) list attendance and quiz metadata separately from the main assignment sequence.

# Modules — CSYE 7270, Fall 2026

## Executive summary

**What this is.** The sixteen Canvas modules of the rebuilt course: a setup module (0) and one module per week (1–15). Each module has a lecture page that teaches the week's machinery and walks through a hands-on task with Claude Code on a real Walker project, a Helpful-links page, and an ungraded practice assessment. Module 14 has a second lecture page for its three labs.

**Why read it.** It is the index to the whole course content, in the same order Canvas shows it, so you can see what a student sees each week and open any source file.

**How it was made.** The lessons are condensed from the companion chapters in [`../chapters/`](../chapters/README.md), whose hands-on examples were really run on 2026-09-27 and are recorded in [`../examples/`](../examples/). The structure follows the old Spring 2026 Canvas course (Lecture, Assignment, Links per module); [`../canvas/OLD-TO-NEW.md`](../canvas/OLD-TO-NEW.md) maps every old item to its successor. The file formats are in [`../pantry/course-build-spec.md`](../pantry/course-build-spec.md), and `python3 scripts/check_course.py` checks them.

**What it is not.** These are review drafts. No human has reviewed them, no AI+1 gate is signed, and nothing has been imported into Canvas.

---

## The modules

| Mod | Week | Lecture | Links | Practice | Assignment (due) |
|---|---|---|---|---|---|
| 0 | before 1 | [Start Here: the toolchain](00-start-here/lesson.md) · [course map](00-start-here/course-map.md) | [links](00-start-here/links.md) | [quiz](00-start-here/assessment.json) | — |
| 1 | 1 | [Walker and Godot](01-walker-and-godot/lesson.md) | [links](01-walker-and-godot/links.md) | [quiz](01-walker-and-godot/assessment.json) | [A1 Extend Walker Jumpman](../assignments/01-extend-walker-jumpman.md) (Day 10) |
| 2 | 2 | [Prompting game art](02-prompting-game-art/lesson.md) | [links](02-prompting-game-art/links.md) | [quiz](02-prompting-game-art/assessment.json) | [A2 Generate Art, Sound, and Music](../assignments/02-generate-art-sound-music-for-your-game.md) (Day 20) |
| 3 | 3 | [Blender MCP to Godot](03-blender-mcp-to-godot/lesson.md) | [links](03-blender-mcp-to-godot/links.md) | [quiz](03-blender-mcp-to-godot/assessment.json) | [A3](../assignments/03-blender-prop-into-godot.md) (Day 30, with Module 4) |
| 4 | 4 | [Scenes, collision and physics](04-scenes-collision-and-physics/lesson.md) | [links](04-scenes-collision-and-physics/links.md) | [quiz](04-scenes-collision-and-physics/assessment.json) | A3 |
| 5 | 5 | [The GDD and virtual worlds](05-the-gdd-and-virtual-worlds/lesson.md) | [links](05-the-gdd-and-virtual-worlds/links.md) | [quiz](05-the-gdd-and-virtual-worlds/assessment.json) | [A4](../assignments/04-specify-and-build-a-3d-interaction.md) (Day 40) |
| 6 | 6 | [Shader foundations](06-shader-foundations/lesson.md) | [links](06-shader-foundations/links.md) | [quiz](06-shader-foundations/assessment.json) | [A5](../assignments/05-shader-and-material.md) (Day 50, with Module 7) |
| 7 | 7 | [Materials and textures](07-materials-and-textures/lesson.md) | [links](07-materials-and-textures/links.md) | [quiz](07-materials-and-textures/assessment.json) | A5 |
| 8 | 8 | [Shader verification](08-shader-verification/lesson.md) | [links](08-shader-verification/links.md) | [quiz](08-shader-verification/assessment.json) | [A6](../assignments/06-audit-a-shader-change.md) (Day 60) |
| 9 | 9 | [Particle effects](09-particle-effects/lesson.md) | [links](09-particle-effects/links.md) | [quiz](09-particle-effects/assessment.json) | [A7](../assignments/07-particle-effects.md) (Day 70) |
| 10 | 10 | [Animation foundations](10-animation-foundations/lesson.md) | [links](10-animation-foundations/links.md) | [quiz](10-animation-foundations/assessment.json) | [A8](../assignments/08-animation-and-state.md) (Day 80, with Module 11) |
| 11 | 11 | [Animation and interaction](11-animation-and-interaction/lesson.md) | [links](11-animation-and-interaction/links.md) | [quiz](11-animation-and-interaction/assessment.json) | A8 |
| 12 | 12 | [Audio and triggers](12-audio-and-triggers/lesson.md) | [links](12-audio-and-triggers/links.md) | [quiz](12-audio-and-triggers/assessment.json) | [A9](../assignments/09-audio-and-a-performance-budget.md) (Day 90, with Module 13) |
| 13 | 13 | [Profiling and optimization](13-profiling-and-optimization/lesson.md) | [links](13-profiling-and-optimization/links.md) | [quiz](13-profiling-and-optimization/assessment.json) | A9 |
| 14 | 14 | [Game AI and systems](14-game-ai-and-systems/lesson.md) · [labs](14-game-ai-and-systems/labs.md) | [links](14-game-ai-and-systems/links.md) | [quiz](14-game-ai-and-systems/assessment.json) | [A10](../assignments/10-final-project.md) (Day 100, with Module 15) |
| 15 | 15 | [Final projects: from brief to export](15-final-projects-brief-to-export/lesson.md) | [links](15-final-projects-brief-to-export/links.md) | [quiz](15-final-projects-brief-to-export/assessment.json) | A10 |

## What is in each module folder

| File | What it is |
|---|---|
| `lesson.md` | The Canvas lecture page: executive summary, the question, the ideas, the Walker example, Predict → Build It → Use It → Ship It → Verify with the exact prompts that were run, what the agents got wrong, a Unity/Unreal bridge, ungraded practice questions, the next step. |
| `links.md` | The Canvas "Helpful links" page: the chapter, official Godot documentation, the Walker projects used, tools, further reading. Every link was checked live when written. |
| `assessment.json` | The ungraded Canvas practice quiz: six multiple-choice questions with feedback. |

## Build the Canvas course from these files

```bash
python3 scripts/build_course.py
```

That writes a Canvas-importable cartridge and one HTML fragment per page. See [`../canvas/README.md`](../canvas/README.md) for how to import it and what has not been checked.

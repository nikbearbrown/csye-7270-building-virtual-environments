# Assignment 1 - Extend Walker Jumpman

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Your task

Start with [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman). Give its main character a new visual identity and extend its actual playable level. Preserve the basic control/retry experience, test your changes, and explain the result in a rendered film using Brutalist's Godot workflow.

This is an extension of the starter, not a new game built from an empty project. Credit the starter and identify your additions. Your project name must begin with **`walker-`**, for example `walker-jumpman-maya-k`. Do your work in your own copy or course-authorized repository, not directly in the instructor's source repository.

Claude Code assistance is expected. Use your Northeastern access; no purchased API credits or paid asset-generation service is required. You remain responsible for the implementation and must be able to explain the code, design decisions, tests, and film.

## 1. Predict

Before implementation, write a short change brief in `CHANGE-BRIEF.md`:

- Your character concept and the visual features that will distinguish it from the starter.
- The new section of level and the decisions it asks the player to make.
- What must remain unchanged: controls, movement/jump tuning, collision behavior, retry, pause, and completion, unless you explicitly justify a necessary change.
- At least two predicted failure cases and how you will check them.

Retain the original predictions. Add later revisions rather than rewriting the record to make every prediction look correct.

## 2. Build It

### Replace the main character's visual identity

Create a recognizable character concept with a meaningful change in shape, silhouette, or visible features—not only a name or color change. Original geometric drawing is sufficient. Imported art is optional; you must document its source and permission to use it.

The starter draws its character in `godot/features/player/player.gd`; it does not use an existing sprite sheet. Inspect `_draw()` before choosing your approach. Preserve the movement parameters and collider for the initial visual change. Make the new appearance read sensibly against the collision boundary, including while facing left and right and while jumping. Explain any necessary departure from the original collider or behavior and test it explicitly.

### Extend the actual playable level

Add a new playable section beyond the starter route with **at least two new landings that require jumps**. The extension must add a clear player decision or challenge, not merely stretch an empty floor. Move the finish so the player must complete the new section to win. Retain a usable route through the original section and preserve failure/retry behavior.

Inspect `godot/levels/first_steps.json` and the code that reads and draws it in `godot/game/session.gd`. A wider level may require camera, bounds, background, labels, and finish-marker changes. In this starter, some drawing coordinates are hard-coded: moving data alone does not guarantee that a hazard or label will be drawn in the correct place. Keep what the player sees consistent with what the physics checks.

Do not change jump strength or remove collision checks simply to make an impossible extension pass. Revise the geometry first. Keep the scope small enough to inspect and complete in this assignment window. Multiplayer, new game engines, paid assets, and a standalone exported application are not required.

### Work in inspectable increments

Ask Claude to propose a plan before editing, then implement one bounded change at a time. For example:

```text
Read this project's README, build report, and my CHANGE-BRIEF.md.
Use Walker's brief → build → playtest → inspect → revise workflow.
First locate the character drawing and collider, level data, drawing code,
camera bounds, finish logic, and relevant tests. Propose the smallest plan
for my character replacement and level extension. Do not edit yet.
After I approve a step, implement only that step, show the diff, run the
relevant checks, and tell me what still requires human playtesting.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan.

## 3. Use It

Play the modified game yourself using normal controls. Record the actual result of each check in `TEST-REPORT.md`, with the source revision and engine version:

| Check | Evidence to collect |
|---|---|
| Startup and controls | Project runs; movement, jump, pause/resume, and restart still work. |
| Character appearance | Left/right, standing, and jumping views; no misleading visual/collision mismatch. |
| Extended route | A normal playable route reaches both new landings and the relocated finish. |
| Failure and recovery | A real hazard or missed landing produces the expected retry; replay works after completion. |
| Camera and presentation | The extension and important landing/finish information remain visible and readable. |
| Automated checks | Commands, results, and any failed or updated tests, with an explanation. |

Ask Claude to run the existing mechanics and keyboard checks where available. Preserve the earlier results. The supplied route fixture was authored for the original layout; extending the level may require an updated route test. Explain what changed in the fixture and add a check for the extension. Do not delete a failing assertion or weaken an expected result merely to obtain a green report.

Include at least one documented inspect-and-revise cycle based on an observation. It may address clarity or usability even if no crash occurs. If you can have another person play, record their actual feedback; do not invent a playtester. Your own playtest is required, and an automated input route does not replace it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-walkthrough`** workflow with the **`walker`** modifier. The original skill spelling is **`godot-waikthrough`**. Ask Claude Code to read the installed skill instructions and follow them; do not assume the skill name is a standalone executable. If your checkout lacks the skill, request the course-provided version before proceeding.

Make **one** landscape film that:

1. Identifies the starter, your character concept, and your level extension.
2. Shows the actual modified game being played, including the new landings, a failure/recovery, and completion.
3. Explains at least one cause-and-effect connection between a source change and the behavior on screen.
4. States what you tested, what remains uncertain, and one concrete next improvement.
5. Identifies human and AI contributions and the game revision being demonstrated.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed interface views, scripted-input captures, and held frames accurately. Preserve actual gameplay evidence; do not fake a completion or change the game solely to conceal a defect in the film.

Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. Keep important details readable and narration intelligible. Duration should follow the explanation; there is no minimum runtime to fill. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**.

The film is part of the 60-point implementation-and-explanation category below. It is not a fifth grading category and does not substitute for working source.

### Post the version on GitHub

Your submitted source includes:

- The modified Godot project and any permitted source assets; exclude generated caches and credentials.
- `README.md`: project name, starter credit, engine version, run instructions, controls, changes, known limitations, and final-film link.
- `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md`.
- The film's beat sheet, script/prompts, and relevant evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum so its version can be checked. Test reviewer access to the source and media.

Use commit messages that describe a meaningful change and its purpose or check. For example: `Extend final landing; update route test and verify retry`. When useful, add a commit-body note distinguishing your decision from Claude's implementation. Commit count is not a measure of learning.

## 5. Verify and submit to Canvas

Run the project from a fresh copy of the revision you are submitting. Confirm that required assets are present and that the film depicts that game source. Do not treat a working local folder as proof that everything was posted.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with a short `SUBMISSION.md` or equivalent submission note containing:

```text
Assignment: Assignment 1 - Extend Walker Jumpman
Student:
Project name:
GitHub repository/folder URL:
Submitted commit SHA:
Game-source revision shown in the film:
Godot version and operating system:
Final film URL and filename:
Final film SHA-256:
Summary of my changes:
Known limitations:
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit.

Canvas, GitHub, and the film must refer to the same submitted work. Identify later changes as a new revision rather than silently replacing the submitted evidence.

## Rubric — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| Frictional — honest log | 10 |
| GitHub version posting matching Canvas | 10 |
| Relative Quartile | 20 |
| **Total** | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|---|---:|
| Character: distinct visual identity (8); readable states and sensible visual/collision alignment with preserved or justified behavior (7). | 15 |
| Level: two new jump landings and a meaningful extension (12); reachable relocated finish and consistent camera/bounds/visuals (8). | 20 |
| Verification: documented baseline and automated/regression checks (5); actual human playtest of route, failure/recovery, and replay (5); evidence-based revision and an honest limitation (5). | 15 |
| Brutalist explainer: accurate explanation of your changes (4); actual mechanism/gameplay shown (3); traceable evidence and stated limits (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit the starter, assets, collaborators, and tools. Describe what AI contributed to the game, script, beat sheet, visuals, and narration, along with what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to explain any part of your submission. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

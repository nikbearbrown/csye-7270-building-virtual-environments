# Assignment 4 - Specify It, Then Build One 3D Interaction

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 40 after the first class day.

**Covers:** [Module 5 — The GDD and virtual worlds](../modules/05-the-gdd-and-virtual-worlds/lesson.md).

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

You write a game design document (GDD) for your own game, with Walker's `/gdd` skill or its public fallback prompt, and audit what the agent wrote. It keeps proposed, implemented, tested, and human-reviewed claims apart, and scopes mobile, networked and XR versions without building them. Then you write at least four measurable acceptance criteria for **one** 3D interaction, commit them before any code changes, have Claude Code build it, and prove each criterion with a test you run. You hand in the repository tagged `a4` with its `design/` folder, a test report, an honest log, and one `godot-gdd` film. Grading is 60 points for the work and its explanation, 10 for the log, 10 for matching versions, and 20 relative. A passing test shows the build meets your criteria as written, not that they were the right criteria or that a player notices or enjoys the interaction.

## Your task

Describe your game precisely enough that a stranger could build and test it. Then specify, build and prove one small 3D interaction from it.

**The cumulative game.** From Assignment 2 on, you build one game: the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. Assignments 3–10 each add one layer to that same repository and are submitted as a git tag on it (`a4` here), so the final project is the sum of the semester rather than a restart. The one allowed change of game had to happen before this assignment; if you made it, the tags continue on the new repository and your submission note says so. This is an individual assignment.

**One 3D interaction** is one thing the player does in 3D space, through ordinary input, that changes the game's state measurably: a checkpoint pad, a pressure plate that opens a gate, a crate pushed onto a target. Your Assignment 3 prop may be part of it. **If your game is 2D,** build it in your Assignment 3 3D scene; if nothing there is player-controlled, the smallest controllable body that makes it playable is in scope.

**Tools and cost.** Claude Code assistance is expected; use your Northeastern access. Nothing paid is needed or earns credit.

**The `/gdd` skill is an open course decision.** Walker's `/gdd` skill (the Zelda design persona) exists in the instructor's local Walker copy. As of 6 October 2026 the public [Walker repository](https://github.com/nikbearbrown/walker) does not carry it, but its `main` branch carries the reusable prompt [`prompts/zelda-gdd.md`](https://github.com/nikbearbrown/walker/blob/main/prompts/zelda-gdd.md). Whether and when the skill is published is not decided. If your course-provided Walker checkout has `gdd/`, use the skill; otherwise use the prompt. Both routes are graded the same way.

### What the GDD must contain

Walker's GDD has sixteen sections, from the Forge prompt set this course used in Spring 2026. The table shows where each still-sound part of the old course's GDD assignments now lives.

| Section | Carried forward from the old course | What it must say here |
|---|---|---|
| Metadata | Name of the game | Version, date, engine version |
| Vision summary | Concept, genre, audience, pitch; graphics, music and sound | A two-sentence pitch; art and audio direction, linking your Assignment 2 files |
| Pillars | Design pillars | Three or four, each tied to a mechanic |
| Core loop | Game flow | The repeated action, decision, and risk |
| Player-experience goals | Why the player is playing | `PX-` IDs a playtest could check |
| Mechanics | Mechanics, abilities, losing and restarting, in numbers | `M-` IDs: purpose, inputs, state, rules, outputs, three edge cases, scope, evidence |
| Systems | — | `S-` IDs and their Godot owners |
| Progression | Levels, challenges, player skills | What a good player gets good at |
| World | Level purpose, critical path, hazards, win and lose | The spaces in metres |
| Narrative | Story | Or why it does not apply |
| Characters | Main characters | The character sheet, linked |
| Feature list | Game elements and assets | `F-` IDs, priorities, CORE share |
| Out of scope | Non-goals and rejected features | What you will not build, and why |
| Technical requirements | Technical description and constraints | Engine, renderer, input map, collision layer table, formats, the scoping note |
| Risks | — | `R-` IDs |
| Open questions | — | Undecided questions and their stakes |

- **Stable IDs** link goals to mechanics, features to Godot owners, and tests to requirements.
- **Keep four kinds of claim apart.** *Proposed*: not yet built. *Implemented*: the source does it; cite the file. *Tested*: a named check passes on the submitted revision. *Human-reviewed*: a person played or judged it; cite the dated note.
- **A section that does not apply says why.** Never invent lore, testimonials or success metrics.
- **Precision means a stranger could write the test** without asking you anything.

Dropped: the old PDF format, the `gamedoc` command, word quotas, and the production task document.

### The scoping note

In the technical section, scope mobile, networked and XR versions; do not build them. For each, write what it would need, what your hardware could verify, what would stay unverified, and why it is out of scope now. Godot's documentation sets the floor: touch arrives as `InputEventScreenTouch` and `InputEventScreenDrag`, and mouse-emulated touch is not a phone ([Input examples](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html)); an Android export needs specific SDK components ([Exporting for Android](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)); the high-level API "only uses UDP", and client input is untrusted ([High-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)); WebRTC needs a GDExtension on native platforms ([WebRTC](https://docs.godotengine.org/en/stable/tutorials/networking/webrtc.html)); OpenXR ships as a core interface, and a scene needs an `XROrigin3D` with an `XRCamera3D` ([Setting up XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html)). Every sentence must be a requirement, a verified fact about your build, or a named unverified item, as in the Walker builds Chapter 5 tabulates, such as [walker-mobile-sensors](https://github.com/nikbearbrown/walker-mobile-sensors) and [walker-xr-openxr-character-centric-movement](https://github.com/nikbearbrown/walker-xr-openxr-character-centric-movement).

**Tools, cost and sources.** Claude Code through your university access is expected; no purchased API credits or paid service is required, and paid output earns no bonus. Credit every source in `SOURCES.md`: the project you started from, any art, model or sound you reuse or generate (name, version and terms for anything generated), and what Claude Code and any other tool contributed to the GDD and to the build. Do not paste copyrighted material or someone else's unpublished design into a prompt.

## 1. Predict

Nothing under `godot/` changes until these are committed, in order: the GDD (Step A below), the acceptance criteria, and `CHANGE-BRIEF.md`. Retain the originals; add dated revisions.

### The acceptance criteria: `design/AC-01-<interaction>.md`

Write them yourself, before any agent touches the code. Chapter 5's [AC-01 checkpoint pad](../examples/05-the-gdd-and-virtual-worlds/AC-01-checkpoint-pad.md) is the model. You need **at least four** criteria, each linked to the GDD IDs it serves, and each naming:

- **The quantity and its unit**: metres, frames, or counts.
- **A tolerance.** "Returns to the pad" is not checkable; "within 0.2 m of the respawn point" is.
- **A time box in the engine's clock:** frames at `--fixed-fps 60`, with physics ticks per frame stated (two, at 120 ticks per second).
- **How the state is reached:** ordinary input (`Input.action_press` and `action_release`), or a constructed fixture that writes state directly, labelled as one. At least two criteria use input only.
- **The reference it is measured against,** something a person can inspect. Chapter 5's criterion let the code compute its own respawn point, so the test compared the player with a number the code chose. Name it instead, such as a `Marker3D` child of the pad ([Marker3D](https://docs.godotengine.org/en/stable/classes/class_marker3d.html)).
- **What must not change.** At least one criterion requires your existing checks to pass.

End the file with what it leaves to people: whether a player sees and understands the interaction, its look and sound, untestable platforms.

### `CHANGE-BRIEF.md`

- The interaction in plain words, and the GDD IDs it implements.
- The files the agent may change, and the invariants it must not touch.
- Where the hard part will be: code, placement, or the scene edit.
- Two kinds of claim the GDD agent will likely get wrong, and why.
- **At least three predicted failures** and how you will check each. Chapter 5's [timestamped prediction](../examples/05-the-gdd-and-virtual-worlds/author-prediction.md) put numbers on its guesses.

## 2. Build It

### Read first

The [Module 5 lesson](../modules/05-the-gdd-and-virtual-worlds/lesson.md) and [Chapter 5](../chapters/05-the-gdd-and-virtual-worlds.md), which recovered a GDD from [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) (upstream MIT license), audited it, and built a checkpoint pad against six criteria ([record](../examples/05-the-gdd-and-virtual-worlds/)). [walker-jumpman-clawd's design folder](https://github.com/nikbearbrown/walker-jumpman-clawd/tree/main/design) is a recovered GDD with unsigned gates and the error the chapter describes.

### Step A — Write the GDD

**With `/gdd`.** Install only the `gdd` folder, as the chapter does. Here `../walker` is a Walker copy that contains `gdd/`:

```bash
mkdir -p .claude/skills
```

```bash
cp -R ../walker/gdd .claude/skills/gdd
```

```bash
python3 ../walker/scripts/render_dir.py .claude/skills "AGENT_NAME=Claude" "GDD_SKILL_DIR=.claude/skills/gdd" "GDD_SKILL_COMMAND=/gdd" "ASSET_GEN_SKILL_DIR=.claude/skills/asset-gen" "ASSET_SKILL_COMMAND=/asset-gen" "RUNTIME_ASSET_DIR=assets"
```

```bash
grep -rn '\${' .claude/skills/gdd
```

The last command should print nothing. The chapter committed the skill only in a scratch repository. Whether course-provided copies may be published is part of the same open decision, so until the instructor says otherwise, list `.claude/skills/gdd/` in `.gitignore` and record which copy you used in `SOURCES.md`.

Your game already has source, so first recover what exists (`--path` is your Godot project folder). In Claude Code:

```text
/gdd reverse --path godot silent
```

Commit the result as agent output, unreviewed. Then develop the proposed design interactively with Zelda's commands (`v1`–`v4` vision, `s1`–`s4` systems, `w1`–`w3` world, `p1`–`p5` scope), answering her questions yourself, and compile and review with `g1`–`g4`. `/gdd draft` is the silent alternative; each `[ASSUMPTION]` it adds is yours to accept or replace. Zelda never signs a gate; sign one in `design/DESIGN-STATUS.json` only once you have decided what it covers.

**With the fallback prompt.** Clone the public Walker repository and give Claude Code the prompt as instructions. It has no `reverse` spec, so marking each claim's evidence is your job:

```text
Read prompts/zelda-gdd.md in my Walker clone at <path> and follow it as
plain instructions; it is not an installed command. Then read my README.md,
the design files from Assignments 2 and 3, and the Godot project in godot/.
Draft design/GDD.md with the sixteen sections that document lists. Mark
every claim about the existing game with the file and line that supports
it, and mark everything else as proposed. Do not sign any gate and do not
change code. Put each decision you could not make in design/decisions.md
as an open question, and ask me one question at a time where my answer
decides the design.
```

**Audit it, either way.** This part is yours; record each finding in `FRICTIONAL.md`:

1. Every input binding. `project.godot` stores keys as integers; ask Godot (`OS.get_keycode_string()`).
2. Five evidence citations chosen at random. Open the line.
3. Every number attributed to a file. Did the agent open it? The transcript tells you.
4. Every "not found" or `[MISSING]` claim. One `grep` often settles it.
5. Every "tested" or "verified". Which test, and does it exist?
6. The gates: unsigned unless you signed them.

Fix errors with `/gdd changelog` or a dated entry in `design/CHANGELOG.md`, not silent edits.

### Step B — Build the interaction

With the criteria and brief committed, ask for a plan:

```text
Implement design/AC-01-<interaction>.md in this Godot 4.7.2 GDScript
project. Read that file, the GDD sections it cites, CHANGE-BRIEF.md and
AGENTS.md first. Do not edit yet: propose the smallest plan, list the files
you would create or change, and say how each criterion will be tested.

After I approve the plan:
- One concern: the interaction. Edit only the files my CHANGE-BRIEF.md
  allows, and change nothing it lists as an invariant.
- Write godot/tests/test_<interaction>.gd as a SceneTree script that
  drives the player with Input.action_press/action_release only, except
  criteria my file labels as constructed fixtures. Print one JSON line per
  criterion and exit 1 if any fails.
- Run the import, the new test with --fixed-fps 60, and every check in my
  ## Checks paragraph, and read the real output.
- If a criterion cannot be met as written, stop and say which and why; do
  not weaken the criterion or the test. Never invent uid:// or unique_id
  values.
- Finish with git status, git diff --stat, and a list of what still needs
  a person to check in the editor.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan. Give absolute paths for anything outside the project: Claude Code declined to auto-approve a command containing `$PWD`. Keep the allow list narrow, with no `Bash(env *)`.

If a session stops partway (Chapter 5's hit a usage limit), do not start over. Give a fresh session the chapter's preface, then your full prompt:

```text
A previous agent session (Claude Code) was stopped by an account usage
limit partway through the task below, before it ran any test. Its partial
work is in the working tree: see git status and git diff. Review that
partial work critically against design/AC-01-checkpoint-pad.md, keep or
change it, and finish the task. The task, exactly as it was given:
```

Change the file name to yours.

### What the agent is likely to get wrong

Chapter 5 recorded all but the coin.

- **Integers read as keys.** The recovered GDD said shooting was F9. The project binds Ctrl.
- **Evidence cited, never opened.** Jump heights were tagged with a file the agent listed but never read.
- **Absence claimed without looking.** "No skybox"; the stage folder had a skybox shader and texture.
- **Judgment tagged as observation.** A CORE percentage was tagged `[OBSERVED]`; a chat summary called eleven features "test-verified" when six had any check.
- **Confident technical errors.** The clawd GDD's decision D-02 says layer names do not match the code. They do: layer 4 is bit value 8.
- **Unseen wiring.** A coin's handler is connected in its `.tscn`; an agent reading only `.gd` files would call it dead code.
- **A right change for a wrong reason.** Codex said a floor ray had hit the pad's own `Area3D`. Rays ignore areas by default.

## 3. Use It

Run every check yourself. Record actual results in `TEST-REPORT.md` with the source revision, Godot version and operating system.

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_<interaction>.gd --fixed-fps 60
```

| Check | Evidence to collect |
|---|---|
| Each criterion | Output line, command, and exit code on the submitted revision; criterion IDs mapped to tests. |
| Input versus fixture | How each state was reached; every direct state write inside a labelled fixture. |
| References | What each distance is measured against, inspectable by a person. |
| Time | Frames under `--fixed-fps 60`, ticks per frame stated. |
| Regression | Your Assignment 2 and 3 checks still pass. |
| Mutation | One deliberate break, caught, then restored. |
| Log | No `ERROR` lines; exit code 0 is not "no errors". |
| GDD reconciliation | The interaction's IDs relabelled implemented, tested, or human-reviewed, with evidence. |
| Scoping note | Each sentence marked requirement, verified fact, or unverified item. |

Read the test, not just its output. If a criterion compares the player with a value the code computed for itself, it has a gap; revise it in a dated entry. Do not delete a failing assertion or weaken an expected result merely to obtain a green report.

**HUMAN CHECKs.** Play it with normal controls and record what you saw.

- Does the interaction's object sit on the floor, or float or sink?
- Can you tell it happened without reading code? If not, add that gap to the GDD's open questions.
- When the interaction moves the player or camera, does the view snap cleanly?
- Play five minutes as a newcomer. Would they notice it?

Include at least one documented inspect-and-revise cycle driven by an observation. If someone else plays, record their actual feedback; do not invent a playtester. Your own playtest is required; a scripted route does not replace it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gdd`** workflow with the **`walker`** modifier ([Required Brutalist Godot explainers](../prerequisites/brutalist-godot-explainers.md)). Ask Claude Code to read the installed skill instructions and follow them; the skill name is not a standalone executable. If your checkout lacks the skill, request the course-provided version. The film changes no design and builds no feature.

Make **one** landscape film that:

1. Introduces your game, its pillars, and the GDD revision it explains.
2. Walks the interaction's design as a chain: experience goal → mechanic → owning scene → visible feedback → acceptance criterion.
3. Shows each criterion's real test output, labelled as headless, and the interaction in real play.
4. Keeps proposed, implemented, tested and human-reviewed claims visibly distinct, including one proposed feature not built and one human decision pending.
5. Summarizes the scoping note and one claim your audit found wrong.
6. States what the evidence does not establish, one next step, the human and AI contributions, and the source revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed views, scripted-input captures, fixtures, and held frames accurately.

Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. Duration follows the explanation. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with the interaction and its tests; exclude `.godot/`, caches and credentials.
- `design/`: `GDD.md`, the criteria file, `decisions.md`, `DESIGN-STATUS.json`, `CHANGELOG.md`, and anything else the GDD route produced.
- `README.md`: project name, Godot version, how to run the game and every check, controls, what this assignment added, known limitations, and the final-film link.
- `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md` (naming the GDD route and version).
- The film's beat sheet, script/prompts, and relevant evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit each stage separately, naming the criterion ID, for example `AC-01 pressure plate: implementation and test`. Tag the submitted commit `a4` and push the tag.

## 5. Verify and submit to Canvas

Clone the tagged revision into an empty folder and run it there. A working local folder is not proof that everything was posted.

```bash
git clone <your-repository> ../a4-check
```

```bash
git -C ../a4-check checkout a4
```

In the clone, import once, run every check, and play briefly. Confirm the film depicts that source.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 4 - Specify It, Then Build One 3D Interaction
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Game-source revision shown in the film:
Godot version and operating system:
GDD route (/gdd skill copy, or prompts/zelda-gdd.md at Walker commit):
GDD version and gates signed (which, by whom, date):
The interaction in one sentence:
Acceptance criteria file, count, and result (command and output):
Human playtest date and main finding:
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
Changed games before this assignment (yes/no; if yes, FRICTIONAL.md entry):
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit.

Canvas, GitHub, and the film must refer to the same submitted work. Do not move the `a4` tag after you submit; identify later changes as a new revision rather than silently replacing the submitted evidence.

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
| GDD: sixteen sections, stable IDs, mechanics in units with edge cases (6); proposed, implemented, tested and human-reviewed claims kept apart and audited against the source (5); scoping note for mobile, network and XR (3); gates and open questions recorded honestly (2). | 16 |
| Acceptance criteria: at least four, each with unit, tolerance, frame time box, how the state is reached, and what must not change (8); committed before implementation, with predictions (2); named references and out-of-scope judgments (2). | 12 |
| The 3D interaction: works in your game as specified, through ordinary input, within the bounded change (8); traceable to its GDD IDs, with the GDD updated to say what is implemented and tested (4). | 12 |
| Verification: every criterion proved by a test you ran under the pinned clock, plus existing checks (4); a mutation your test catches (2); human playtest with HUMAN CHECKs recorded (2); an evidence-based revision and an honest limitation (2). | 10 |
| Brutalist explainer: accurate explanation of the design contract with game evidence (4); proposed, built, tested and human-reviewed kept distinct on screen (3); limits and scope stated (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing acceptance test establishes that the build meets the criterion as written under scripted input; it does not establish that the criterion was the right one, that a player notices or understands the interaction, or that any mobile, network or XR claim holds on a device.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source and documentation are actually posted.
- **3 points:** Canvas identifies the `a4` tag and the exact submitted commit, and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit your starting point, the GDD route and version, collaborators, and tools. Describe what AI contributed to the GDD, code, tests, and the film's script, beat sheet, visuals, and narration, and what you decided, checked, changed, or rejected. A decision you accepted from Zelda is yours to defend.

The instructor or a TA may ask you to defend a tolerance, show where a GDD claim's evidence lives, or explain why a feature is out of scope. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

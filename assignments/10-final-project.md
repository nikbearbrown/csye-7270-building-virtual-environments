# Assignment 10 - Final Project: From Brief to Export

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 100 after the first class day.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

This is the final project. It covers Modules 14 and 15 and draws on the whole course. You finish the game you have built since Assignment 2: add one game-AI or systems element from Module 14, chosen and justified; add one piece of data that survives a restart, under save rules written first; then take Walker's cycle to its last step, so that anyone can reproduce your build from a clean clone of tag `a10` and you can say honestly whether it is source-ready or export-ready. You defend it in two films with the `walker` modifier: `godot-walkthrough` shows what the finished game does, and `godot-gdd` shows why it is specified that way and names the five Supervisory Capacities with evidence. It replaces the old course's 300-point Final Portfolio Piece, is graded 60 / 10 / 10 / 20 like every assignment, and is individual work. Passing every check shows the build reproduces and its rules hold for the cases tested; it does not show the game is fun, that an export runs where you did not run it, or that a screen reader can use it.

## Your task

Work from the [Module 14 lesson](../modules/14-game-ai-and-systems/lesson.md) and its [labs page](../modules/14-game-ai-and-systems/labs.md), the [Module 15 lesson](../modules/15-final-projects-brief-to-export/lesson.md), and the chapters [Game AI and Systems](../chapters/14-game-ai-and-systems.md) and [Final Projects: From Brief to Export](../chapters/15-final-projects-brief-to-export.md), with their run records in [examples/14-game-ai-and-systems](../examples/14-game-ai-and-systems/) and [examples/15-final-projects-brief-to-export](../examples/15-final-projects-brief-to-export/).

**The sum of the semester.** Since Assignment 2 you have built one game in one repository whose name begins **`walker-`**, tagged `a3` through `a9`. This assignment adds the last layers to that repository and is submitted as the tag **`a10`**. Do not restart. The finished build must still contain, working together, what earlier assignments added: generated art and sound, a Blender prop with collision and physics, a GDD and a 3D interaction, a shader and a material, particle effects, animation wired to player actions, and audio on buses within a frame budget. If a layer had to be removed or replaced, the README says what and why. The old final project judged scope by "using shaders, animation, UX/UI"; your tags are now that list.

**Individual work.** This is an individual project. Credit anyone who playtested or gave feedback in `SOURCES.md`.

**Tools and cost.** Claude Code through your Northeastern access is expected; no purchase of any kind is required. If a usage limit ends a session, `HANDOFF.md` lets a later session continue: in Module 14, Codex finished a task from the handoff file Claude Code left. Name every tool in `SOURCES.md`.

**License.** License your own contributions under the [MIT License](https://opensource.org/license/mit) or a copyright statement of your own, in a `LICENSE` file and the README, as the old final project required. Keep every upstream license: Godot's demos and their Walker adaptations are MIT. `walker-jumpman` and `walker-jumpman-clawd` carry no license file, and the latter's `SOURCES.md` notes that public availability is not a license grant; if you started from either, license only your own additions and say so. Name any asset whose license is unresolved, and do not publish a film that uses it.

### Choose one game-AI or systems element

Choose the one that serves your game's design, and justify it, including why not the others.

| Option (Module 14) | Minimum in your game | What its tests cannot show |
|---|---|---|
| State-machine or behavior-tree character | At least three behaviors with explicit transitions (or tree priorities), hysteresis where a boundary could flicker, and a read-only state property that tests read instead of internals. | Whether it is fun, fair or readable to play against. |
| Navigation | A character that reaches a far target around obstacles and stops at the closest point for an unreachable one (`NavigationAgent2D`/`3D`, or `AStarGrid2D` on a grid), with no test depending on the frame the first path arrives. | Behavior with other agents, moving obstacles, other maps. |
| Procedural content with a validator | A seeded generator whose output enters your real scene; a validator built from the player's measured limits minus a stated margin; hand-made impossible cases rejected; the same output for a seed on Godot 4.7.2. | That an accepted output can be crossed, or is any good. |
| A learning agent | One decision in your game learned from reward, seeded and repeatable, with its learning curve and its greedy policy evaluated separately from the exploring training rate. | Anything about deep reinforcement learning or continuous state. |
| Scoped two-process networking | Two processes on `127.0.0.1` only, one synchronized state change, one rejected unauthorized change, and a written check of every `any_peer` RPC you declare. | Latency, packet loss, NAT, or a modified client. |

A behavior-tree addon (LimboAI or Beehave, both MIT) is allowed if you pin its version, credit it, and can explain what it does for you that Module 14's plain GDScript tree did by hand. Godot RL Agents was not run for this course; if you use it, its setup and claims are yours to verify.

### Take the cycle to export

- **GDD.** Update your Assignment 4 GDD so every feature is labeled **proposed**, **implemented**, **tested** or **human decision pending**. Walker's `/gdd` skill exists only in the local Walker checkout; public [Walker](https://github.com/nikbearbrown/walker) carries the reusable prompt `prompts/zelda-gdd.md`.
- **Persistence.** One piece of data survives a restart: a best time, settings, progress. Module 15 saved a personal best in [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) under rules written before any code.
- **A front door.** A start or pause menu usable by keyboard alone, with focus set when the scene starts.
- **Reproduction.** A clean clone of tag `a10` imports and passes every documented check.
- **Export.** A committed `export_presets.cfg`, an inspected `--export-pack`, and an export attempt, with the state you claim matching the evidence. A public release is not required.

## 1. Predict

Before the first agent run, add an Assignment 10 section to `CHANGE-BRIEF.md` and commit it. Keep earlier sections; add revisions rather than rewriting.

- **The choice:** your option, the design reason, the options you rejected.
- **The test contract:** what tests will read and never read. Module 14's guard tests read only the guard's `mode` and positions, and moved the player only as a printed fixture.
- **Save rules, before implementation:** path, format and version field, and what happens for missing, corrupt, newer-version and unwritable files. Module 15's plan deferred its save feature with "write migration/corruption/reset rules before implementation"; writing them is the design work.
- **Predictions, in writing:** two Predict questions from your option's section of Module 14; where your existing tests' runs will be saved once persistence exists; which files an import of a fresh clone will create that are not committed; what `--export-release` and `--export-pack` will each do without templates.
- **The export target** and the state you expect to claim.
- **At least three predicted failure cases** and how you will check them.

## 2. Build It

What must not change: the earlier layers and their tests, unless your brief first says why. Done means every row of the Use It table has evidence. Split the work into separate agent runs, each ending by writing `HANDOFF.md`: files changed, exact test commands and real results, what the next task may rely on, what is unverified. Each later run starts by reading it and rerunning every test it lists. Sequencing the runs is Tool Orchestration. A sensible order: the AI or systems element (in two or three runs if it has parts, as Module 14's guard did), persistence, the menu, the export preset. Start each run with a plan:

```text
Read README.md, GDD.md, CHANGE-BRIEF.md (Assignment 10 section), HANDOFF.md
if it exists, project.godot, and every script and test this task touches.
Run every test HANDOFF.md lists; if any fails, stop and report.
Task: <one task from my brief>. Propose the smallest plan: the files and
nodes to add or change, what must not change, and the checks that will
prove it, reading only the observable state my test contract names.
Do not edit yet. After I approve, implement only that task, run every
listed test headless (--fixed-fps 60 for frame-counted tests, real time
for audio and networking), paste the real output, and update HANDOFF.md.
A run is clean only if it exits 0 and its log has no "SCRIPT ERROR" or
"ERROR:" lines. Do not open a Godot window. Do not commit.
```

This is a prompt to Claude Code, not an installed shell command. Run agents with `--disallowedTools "Skill"`.

**Your gate between runs.** Read the diff and the new `HANDOFF.md`. Run `godot --headless --path godot --import` once. Rerun every test yourself, wrapped in `timeout`, and read the whole log: a script error does not change Godot's exit code, so `grep -c "SCRIPT ERROR"` should print 0. Commit; that commit is the baseline for the next diff.

**Persistence.** Module 15's rules held once corrected: read `version` before any other field, and never overwrite a newer version whatever else changed; validate the whole file before changing live state; warn and stay playable on any failure; write a temporary file, then rename it over the old one. Tests never touch the player's real `user://`: a test-mode session saves nothing unless the test sets a path, and on macOS every run points `HOME` at a scratch folder (verified on macOS only). Module 15 ran its save test like this:

Create the scratch home first, once:

```bash
mkdir -p ../scratch-home
```

Then run each save-touching test against it:

```bash
HOME="$PWD/../scratch-home" godot --headless --path godot --script res://tests/test_best_time.gd --fixed-fps 60
```

**The menu.** Grab focus in code when the scene starts, for example `$StartButton.grab_focus.call_deferred()`. Text drawn with `draw_string` has no accessible name; a `Label` or `Button` can carry `accessibility_name`. Godot's screen reader support is experimental; testing one is optional.

**Export.** Add one preset for your target, exclude your tests, and commit `export_presets.cfg`; never commit `.godot/export_credentials.cfg`. The Web target needs the Compatibility renderer and GDScript. The output folders must exist, and `--export-pack` needs no templates, so first look at what would ship:

```bash
mkdir -p build/web build/pack
```

```bash
godot --headless --path godot --export-pack "Web" ../build/pack/game.zip
```

`--export-release` needs export templates for the exact engine version (a folder named `4.7.2.stable`), installed from **Editor → Manage Export Templates**. They are a large download: the 4.7.2 template file on [Godot's 4.7.2 release page](https://github.com/godotengine/godot/releases/tag/4.7.2-stable) is about 1.3 GB (1,281,349,702 bytes, checked 6 October 2026). Downloading them is your decision; check your disk first. Without them, run the export anyway and keep the error: it is the evidence for "source-ready, not export-ready". With them, export, launch the exported build, play it, and record the package's SHA-256. Replace `Web` with your preset's name:

```bash
godot --headless --path godot --export-release "Web" ../build/web/index.html
```

**What agents got wrong in Modules 14 and 15**, each while their own tests passed:

- A guard's "never inside the obstacle" check could not fail, because physics stopped the body at the surface. The audit measured clearance instead.
- "Movement begins on the next physics tick" held in 8 of 20 trials; the first path arrived anywhere from frame 2 to frame 9.
- A behavior-tree guard passed 12 of 12 checks on top of 626 lines of `SCRIPT ERROR`.
- Denied `kill` and `lsof`, an agent put `OS.execute("/bin/kill", …)` inside a Godot test. Allowing `godot --script` allows anything GDScript can do.
- The level-generator agent measured the jump under a ceiling (128.3 px; 163.3 px on a flat floor) and tested landing on a hand-built row, not a generated level.
- Module 15's agent wrote that no test touched the player's real save; two unchanged suites wrote to it, leaving a "best" of 0.0667 s. It also checked `level` before `version`, so a newer file was overwritten.

Write at least one audit of your own, in the style of Module 14's [`audit/`](../examples/14-game-ai-and-systems/audit/) scripts, for a case the agent's tests do not cover. Both of Module 14's guard brains ignored a player standing in plain sight for about 165 physics frames, because nobody had specified what Search should do. Look for that kind of gap.

## 3. Use It

Record actual results in `TEST-REPORT.md`, with revision, engine version, operating system and date:

| Check | Evidence to collect |
|---|---|
| Clean clone | Import log; `git status --short` (commit generated `.uid` files); every test's output; a short main-scene run; the Godot version string. |
| The new element | Its tests, repeated, in the right time mode; your own audit's output. |
| **HUMAN CHECK: play against it** | Try to break it. A character: stand at the edge of its sight, hide behind cover, reappear while it searches. A generator: play at least three accepted outputs by hand. A learner: watch its policy in your game. Networking: two instances via **Debug > Customize Run Instances**, one round played in each window. |
| Persistence | Round trip; missing, corrupt, newer-version and unwritable files; the real save folder untouched by tests. HUMAN CHECK: quit, relaunch, confirm. |
| The whole game | One full session from launch to end, every earlier layer seen working or its removal explained. |
| Menu | Start, play, pause and quit by keyboard alone; what a screen reader announced, if you tried one. |
| Export | The pack listing (what ships that should not, what must ship); the release export's output; notes from playing the exported build, if you made one. |
| Frame budget | Your Assignment 9 harness on the final build, against the `a9` numbers. |
| Human playtest | Your own full session; other players only in their actual words. |

For the clean clone's short main-scene run, use the `--quit-after` flag from Chapter 0's table:

```bash
timeout 120 godot --headless --path godot --quit-after 120
```

A scripted route is not a playtest, and your own playtest is required. Never delete a failing assertion or weaken an expected value to get green. Document at least one inspect-and-revise cycle driven by an observation.

## 4. Ship It — source and two explainers

### Make two required Brutalist Godot explainers

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) workflows, both with the **`walker`** modifier and both showing the submitted revision. Ask Claude Code to read each installed skill and follow it; if your checkout lacks one, request the course-provided version. The old final project's rule holds: the films discuss what **you** did.

**Film 1, `godot-walkthrough`** (original spelling `godot-waikthrough`): what the finished game does. Real play from launch: the core loop, the earlier layers in context, the new element in action, a failure and recovery, completion, and the persisted data surviving a restart. Label scripted-input captures; they are not playtests.

**Film 2, `godot-gdd`**: why it is specified that way. Walk the GDD with game evidence, keeping proposed, implemented, tested and human-decision-pending apart. Explain your Module 14 choice, your save rules, and the export state you claim, with its evidence. Its Verdict names the **five Supervisory Capacities**, each with one concrete moment from this project:

- **PA, Plausibility Auditing:** a wrong note you caught that seemed fine until you played it.
- **PF, Problem Formulation:** a task you defined before the agent saw it.
- **TO, Tool Orchestration:** an order of tasks, and the context each run got.
- **IJ, Interpretive Judgment:** meaning you supplied that no check could detect.
- **EI, Executive Integration:** how you held the semester's layers toward one game.

The syllabus makes the final week the week of all five. The same five, with those moments in more detail, go in `FRICTIONAL.md`.

For both films: Walker opening/summary and Verdict → Your Turn → regular outro; AI narration, including Liam, allowed; reconstructed views and held frames labeled; the skill's native **4K landscape** rendering and checks; watch each final export. There is no minimum runtime. A Short, paid media and public YouTube publication are **not required**.

### Post the version on GitHub

- The game source and used assets, with `export_presets.cfg`; no caches, credentials or export output.
- `README.md`: name, starting point and credits, engine version, run instructions, controls, every test command with its time mode, the state claimed and its evidence, the license, both film links.
- `LICENSE`, `GDD.md`, `CHANGE-BRIEF.md`, `HANDOFF.md`, `TEST-REPORT.md`, `PERFORMANCE.md`, and `FRICTIONAL.md` with the five capacities.
- `SOURCES.md`: every asset, model, addon and tool, and the syllabus's labor-separation disclosure with the stage you actually reached and all five capacities.
- Both films' beat sheets, scripts/prompts, and evidence/coverage records.

Keep MP3, MP4, export packages and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify each film, and any export package, by filename and SHA-256 checksum. Test reviewer access. Tag the final submitted commit `a10`.

## 5. Verify and submit to Canvas

Clone tag `a10` into an empty folder, replacing the placeholder, and run every documented check there:

```bash
git clone --branch a10 <your-repository> ../a10-check
```

Then, inside `../a10-check`:

```bash
godot --headless --path godot --import
```

```bash
git status --short
```

Submit a source ZIP of that revision, without caches, credentials or large media, with `SUBMISSION.md`:

```text
Assignment: Assignment 10 - Final Project: From Brief to Export
Student:
Project name:
GitHub repository URL:
Tag a10 commit SHA:
Game-source revision shown in both films:
Godot version and operating system:
Game-AI or systems option, in one sentence:
Persisted data and save rules (one line):
State claimed (source-ready or export-ready) and its evidence:
Export target; templates installed (yes/no):
Export package filename and SHA-256 (if built):
License for my contributions:
Walkthrough film URL, filename, SHA-256:
GDD film URL, filename, SHA-256:
Summary of my work:
Known limitations:
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and both films must refer to the same submitted work.

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
| Game-AI or systems element: a choice justified by the design (3); a working implementation behind a test contract that reads only observable state (6); your own audit of a case the agent's tests missed, plus human play against it (4). | 13 |
| Persistence and reproduction: save rules written first and enforced, including newer-version and corrupt files, with tests isolated from the real save (5); a clean clone of `a10` that imports and passes every documented check, generated files committed (5). | 10 |
| Export: a committed preset, an inspected pack listing, and an honestly reported export result, with the claimed state matching the evidence (6). | 6 |
| The finished game: the semester's layers working together in one build (8); professionalism: runs from the README, clear names, a license for your contributions, attention to detail (4). | 12 |
| Verification: your own full playtest of the finished build (3); an evidence-based revision and honest limitations (2). | 5 |
| Brutalist explainers: a walkthrough of real play covering the new element, persistence, failure and completion (5); a GDD defense with status labels and evidence (5); the five capacities, each with a concrete moment (2); readable, audible films using the required workflows, both showing the submitted revision (2). | 14 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A clean-clone pass shows the build reproduces on your machine and engine version; it does not show that an exported game runs elsewhere or that anyone enjoys it.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit (tag `a10`) and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film links, identified media versions, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit every starter, asset, model, addon, collaborator and tool, what AI contributed to the game, tests, GDD, scripts, beat sheets and narration, and what you personally decided, played, checked, changed or rejected.

The instructor or a TA may ask you to rebuild from your tag, run any test, defend a save rule, or explain how your Module 14 element decides what to do. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship, provenance, playtesting or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

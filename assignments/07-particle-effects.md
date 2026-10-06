# Assignment 7 - Two Particle Effects, Tuned and Priced

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 70 after the first class day.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

**Covers:** [Module 9 — Particle effects](../modules/09-particle-effects/lesson.md) and its companion reading, [Chapter 9 — Particle Effects](../chapters/09-particle-effects.md). The chapter's worked record is in [examples/09-particle-effects](../examples/09-particle-effects/).

## Executive summary

You add two particle effects to your game: a one-shot burst that fires on a gameplay event, and a second effect with a different job (ambience, a trail, or a feedback loop that follows a game value). Before building either, you write down what each must communicate; that intent is what you tune against. You check each effect's state with headless tests, then price it twice: a headless CPU measurement made the chapter's way, and your own measurement in the editor on a real GPU, because a headless run reports GPU particles as nearly free. You hand in the repository tagged `a7`, a test report with both prices, and a `godot-walkthrough` film of the effects in real play. Grading follows the course's 60/10/10/20 split. A passing headless test proves an effect's state, not that a player can see it, that it reads as intended, or what it costs on screen.

## Your task

Add two particle effects to the game you have been building since Assignment 2. Tune each against a written intent, verify its state, and measure its cost.

| Effect | What it must be | Examples |
|---|---|---|
| A — the event burst | A one-shot effect that fires on a real gameplay event, every time, and never otherwise | a hit, a death, a pickup, a landing |
| B — the second job | An effect that runs over time for a different purpose, under a condition you state | ambience; a trail behind something that moves; a feedback loop whose emission follows a game value |

Effect B must not be a second burst: it raises other questions, such as what it does, and costs, while hidden or paused.

**One game, one repository.** From Assignment 2 on, you build one game: the one you chose in Assignment 2, in a repository whose name begins `walker-`. This assignment adds one layer to it and is submitted as the git tag `a7`. If an effect needs a 3D scene and your game is 2D, add one; a project may mix 2D and 3D scenes. If you changed games before Assignment 4, the tag continues on the new repository; say so in your submission note.

**Tools, cost and rights.** Claude Code assistance is expected; use your Northeastern access. No purchased API credits or paid service is required, and paid output earns no bonus. A texture can come from your Assignment 2 assets, a `GradientTexture2D` defined in the scene file (as in the chapter), or art drawn in code. Record every texture and mesh in `SOURCES.md`; Assignment 2's rights rules still apply. You must be able to explain every line.

## 1. Predict

Commit `CHANGE-BRIEF.md` before you ask Claude to build anything. Keep the original; add dated revisions below it rather than rewriting it.

**Visual intent, one block per effect:**

- **The job:** the one thing the player should understand from it ("you were hit here", "this cave is hot").
- **The event or condition** that starts it (code path, signal or animation key) and, for B, what stops it.
- **Size, speed and duration on screen,** relative to your character at in-game size, and **colour and shape,** tied to your Assignment 2 palette.
- **Emission, process, draw:** the chapter's three parts, each of which can be wrong on its own. Name the settings you expect: `amount`, `lifetime`, `explosiveness`, `one_shot`; direction, spread, velocity, gravity, scale and colour over life; texture or mesh and material.
- **Node type, and why.** Sub-emitters, `trail_enabled`, particle shaders and the process material's collision and attractor settings exist only on GPU nodes, and the Compatibility renderer supports neither particle trails nor particle SDF collision. Check your renderer first.
- **Parent and visibility:** which node the effect lives under, and why it is still visible when the effect must be seen.

**Predictions:**

- **At least three predicted failure cases,** each with its check. The chapter's are real: a burst `emitting` but invisible because its parent hid itself on the same event; a null texture, which the class reference says draws 1×1-pixel squares; a 2D process material without Disable Z; a burst that fires at game start, or only once.
- **Price predictions:** each effect's CPU cost per frame, and what a headless run will report for a GPU node.
- **A budget:** the share of a frame you allow each effect at your target frame rate (a 60 fps frame is about 16.7 ms), on what kind of machine.

## 2. Build It

Read the [Module 9 lesson](../modules/09-particle-effects/lesson.md) and [Chapter 9](../chapters/09-particle-effects.md) first. The chapter adds a one-shot death burst to `walker-2d-dodge-the-creeps`, then measures what particle simulation costs the CPU; its prompts, final 9-check test (`tests/test_particles.gd`) and cost script (`tests/particle_cost.gd`) are in the [example record](../examples/09-particle-effects/).

Two Walker projects, each keeping the upstream MIT license, show both kinds of effect:

- [walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps): the `Trail` in `godot/player.tscn` is a continuous `GPUParticles2D` stamping faded copies of the player sprite, not the `trail_enabled` feature. It emits even on the title screen, invisible only because its parent is hidden. Read the node, not its name.
- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer): one-shot `CPUParticles3D` bursts for a coin and an enemy explosion, started by animation tracks that key `emitting` (`godot/coin/coin.tscn`, `godot/enemy/enemy.tscn`), and a steady glow behind each bullet. When an agent cannot find where an effect starts, tell it to look in the animations.

### Work in inspectable increments

One bounded step per prompt, one commit per verified step: baseline (import, run your existing checks); effect A and its test; effect B and its test; the cost script and its output; each tuning change. Start with a plan:

```text
Read my CHANGE-BRIEF.md and README.md, then the scenes and scripts that own
the gameplay event for Effect A and the condition for Effect B. Use Walker's
brief → build → playtest → inspect → revise workflow. Inspect first and tell
me, with file and line references: where the event happens, what the player
or object does at that moment (hide, free, change scene), which renderer the
project uses, and where each effect should be parented so that it is still
visible when it must be seen. Then propose the smallest plan: the nodes and
resources you would add (configured in the scene file, not built in code),
the trigger code, and one headless test per effect. Do not edit yet. After I
approve a step, implement only that step, show the diff, run the checks,
paste their real output, and list what still needs a human at a screen.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan. The chapter's session-1 prompt models the build step: one invariant, one change, what not to touch, and the evidence to bring back.

**What must not change:** movement, collision shapes, timers, scoring, your Assignment 2 audio, and your earlier tests. An effect never decides game state.

**Done** means both effects meet their written intent on your screen, both state tests pass in runs you made, both prices are recorded with their instruments, and every earlier check still passes.

**Tell the agent how to run the checks:** put the exact import and test commands in your `CLAUDE.md` or `AGENTS.md`. In the chapter's first session the agent called Godot by a path its allow list did not permit, was refused, and printed an "Expected headless output" table instead of a result. Two of its three predicted failures were wrong.

### What the agent is likely to get wrong

Each of these happened in the chapter's record.

- **It blames the engine.** The agent called a FAIL a headless limitation. The instructor's earlier probe showed `finished` does fire headless; the bug was in the agent's test, where a GDScript lambda could not reassign an outer local variable. Ask for evidence before you accept "engine limitation."
- **State checks pass on a broken effect.** The first burst had a null texture and Disable Z off, and every state check passed. Reading the documentation found both.
- **It measures the instrument.** Timed headless without a fixed frame rate, the cost script reported 6.90 ms per frame for every case, an empty scene included: headless Godot sleeps toward a 6.9 ms frame unless `--fixed-fps` is set. The prompt, not the agent, was wrong.
- **It leaves residue:** an unsupported claim in its report, and a stale comment contradicting the check below it. Remove both in review.

An agent's "done" is a claim; check it with a command you ran.

## 3. Use It

### State checks (headless)

Write a headless test for each effect (the chapter's is `godot/tests/test_particles.gd`) that reaches it through the game's real path: real input, or a labeled fixture such as the chapter's frozen mob. Print one PASS or FAIL line per check, and `quit(1)` on any failure.

| Effect | Checks to include, adapted to your game |
|---|---|
| A | Configured as intended (one-shot, explosiveness, a non-null texture in 2D, Disable Z on a 2D process material); not emitting before the event; emitting and `is_visible_in_tree()` right after it; at the event's position; `finished` within `lifetime` plus a margin of engine time; fires again on a second event; never fires at game start. |
| B | Emitting while its condition holds and not otherwise; its behavior during pause, on any title or menu screen, and while its parent is hidden, each matching your brief; for a feedback loop, emission follows the game value across at least two values. |

Say which mode each run used: the chapter runs its gameplay tests in real time, because they wait on timers and audio, and its timing script with `--fixed-fps 60`. Wrap every run in `timeout`; a script error before `quit()` leaves headless Godot running forever. Import once after cloning. Exit code 0 is not "no errors": read stderr.

### On-screen checks (HUMAN CHECK)

Open the project in the Godot editor and run it. You are the only instrument that can see.

| Check | Evidence to collect |
|---|---|
| Inspector | Emission, process and draw settings match the brief or its revision. |
| A in play | Triggered three or more times in different places: visible, the intended size, readable, not covered by UI? |
| B in play | Starts and stops with its condition, through a pause and on any menu screen. |
| Intent | One dated verdict per effect, with the machine: does it communicate its job? |
| Automated checks | Commands, modes, real output, and any failed or updated test, explained. |

Tick `Emitting` in the Inspector to preview an effect. Single pixels, or dots that crawl, are problems no state test reports.

### Price each effect

Record both prices in `TEST-REPORT.md` with the machine, operating system, Godot version, renderer and window size.

**CPU price, headless.** Ask Claude for a cost script modeled on the chapter's `particle_cost.gd`. It prints the rendering method, the video adapter name, and a sentence stating that headless Godot uses a dummy renderer, so GPU simulation and drawing are not measured; times an empty-scene baseline; then, per effect, waits 60 warm-up frames, times 300 frames with `Time.get_ticks_usec()`, repeats three times, and reports min, mean and max. Instance your effect's own scene so you price what ships, and also price the worst case your design allows (the most A bursts alive at once). A one-shot burst ends long before 300 frames: time a looping copy with the same `amount` and `lifetime`, and label that number an upper bound. Run it in three fresh processes with `--fixed-fps 60`.

In the chapter's run, 50,000 `CPUParticles2D` cost 1.61 ms per frame; 50,000 `GPUParticles2D` cost about what an empty scene did, because the dummy renderer does no GPU work. That row describes the instrument, not GPU particles, and is not a price.

**GPU and draw price, on a real GPU (HUMAN CHECK).** Run the game from the editor on your own machine. Open **Debugger → Monitors** and compare the same moment with the effect off and on, at the same window size: frame time, draw calls, video memory. The **Profiler** shows script time; recording slows the project, so time nothing while it runs. The **Visual Profiler** shows CPU and GPU render time by stage, but "is not supported when using the Compatibility renderer on macOS": on a Mac, switch renderer temporarily and record that you measured a different renderer, or use Windows or Linux. [Chapter 13](../chapters/13-profiling-and-optimization.md) covers these tools in depth.

The levers are `amount`, `lifetime`, `fixed_fps`, `visibility_rect` (2D) or `visibility_aabb` (3D), and texture size and transparency; overlapping transparent quads cost fill rate, which Godot's GPU optimization page calls "very expensive" on mobile. If an effect is over budget, change one lever, measure again, and say what the change cost the look.

### Inspect and revise

Include **at least one documented inspect-and-revise cycle per effect**, driven by something you saw (a burst that read as a flicker, a price over budget), with the values before and after. Do not delete a failing assertion or weaken an expected result to obtain a green report. If another person plays, record their actual feedback; do not invent a playtester. Your own on-screen check is required.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-walkthrough`** workflow with the **`walker`** modifier. The original skill spelling is **`godot-waikthrough`**. Ask Claude Code to read the installed skill instructions and follow them; it is not a standalone executable. If your checkout lacks the skill, request the course-provided version. The skill captures the real rendered viewport; a headless run draws no GPU particles, so a headless log cannot stand in for footage.

Make **one** landscape film that:

1. Introduces your game and the job of each effect in plain terms.
2. Shows effect A firing on its real event in play, at least twice in different places, and effect B starting and stopping with its condition.
3. Explains at least one cause-and-effect connection between a setting or line of code and what the player sees, such as a parent choice or a tuning change shown before and after.
4. States each effect's price with the instrument that produced it: the headless CPU number, labeled headless, and your on-GPU measurement, with machine and renderer.
5. States what you tested, what you judged by eye, what remains uncertain, one concrete next step, the human and AI contributions, and the game revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label scripted-input captures, reconstructed views, slowed replays and held frames accurately. A capture recorded at a fixed frame rate is not a real-time frame time, so the film's smoothness is not a performance result. Do not fake a trigger or change the game solely to hide a defect.

Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. There is no minimum runtime. A second film, a vertical Short, paid media generation and public YouTube publication are **not required**. The film is part of the 60-point category below and does not substitute for working source.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with both effects and their resources; exclude generated caches and credentials.
- `README.md`: project name, starting point and credit, engine version and renderer, run instructions, controls, how to trigger each effect, both prices, known limitations, and final-film link.
- `CHANGE-BRIEF.md` with its original intents, `TEST-REPORT.md` (state checks, verdicts, both prices), `FRICTIONAL.md`, and `SOURCES.md` (textures, meshes, and the human/AI split of the code).
- The state tests, the cost script and its logs, and the film's beat sheet, script/prompts, and coverage and evidence records.

`FRICTIONAL.md` should hold the prompts, what the agent claimed, what you ran, what failed, what you changed and what you saw on screen.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit in steps, with messages that name a change and its check, for example `Parent burst to Main; verify visible after hide and refires on second hit`. Tag the submitted commit `a7`.

## 5. Verify and submit to Canvas

Clone the `a7` tag into a fresh folder, import once, and run every check yourself. The chapter's commands:

```bash
timeout 120 godot --headless --path godot --script res://tests/test_particles.gd
```

```bash
timeout 300 godot --headless --fixed-fps 60 --path godot --script res://tests/particle_cost.gd
```

A pasted transcript is not a result. Read each log for loading errors, not only PASS lines, and confirm that the film shows the source you are submitting. A working local folder does not prove that everything was posted.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 7 - Two Particle Effects, Tuned and Priced
Student:
Project name:
GitHub repository URL and tag (a7):
Submitted commit SHA:
Game-source revision shown in the film:
Godot version, renderer, and operating system:
Effect A (event, node type, one-line intent):
Effect B (purpose, condition, node type, one-line intent):
CPU price per effect (headless, --fixed-fps 60, machine):
GPU and draw price per effect (machine, GPU, renderer, window size):
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
| Intent before building: a complete block per effect (job, trigger or condition, size, palette, emission/process/draw, node type, parent) (5); three or more predicted failures, price predictions and a budget, committed before the first build step (3). | 8 |
| Effect A: fires on the real event every time and never otherwise, visible and at the right place when it fires (7); meets its written intent on screen, with a working draw setup (5). | 12 |
| Effect B: a different job that starts and stops with its stated condition, including pause and hidden states (6); meets its written intent on screen (4). | 10 |
| Verification: headless state tests for both effects, run by you, mode stated (5); dated on-screen verdicts and one evidence-driven tuning revision per effect (5). | 10 |
| Price: headless CPU measurement with baseline, `--fixed-fps 60`, repeats and worst case, GPU row labeled as the instrument's (5); on-GPU measurement, effect off and on, machine and renderer recorded (4); budget comparison (1). | 10 |
| Brutalist explainer: accurate explanation of both effects and one cause-and-effect link (4); real rendered play of A's trigger and B's condition (3); prices with their instruments, and limits (2); readable, audible film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive effects do not repair an incorrect explanation or a wrong price. A passing headless test establishes an effect's state; it does not establish that a player can see it, that it reads as intended, or what it costs a GPU.

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

Use `SOURCES.md` to credit what you started from, every texture, mesh and asset, collaborators, and tools. Describe what AI contributed to the code, tests, cost script, script, beat sheet, visuals and narration, and what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to trigger an effect and explain a setting or its parent, or to rerun your cost script and explain what its GPU row does not measure. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

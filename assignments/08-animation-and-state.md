# Assignment 8 - Animation Wired to Player Actions

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 80 after the first class day.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

**Covers:** [Module 10 — Animation foundations](../modules/10-animation-foundations/lesson.md) and [Module 11 — Animation and interaction](../modules/11-animation-and-interaction/lesson.md), with their companion readings, [Chapter 10](../chapters/10-animation-foundations.md) and [Chapter 11](../chapters/11-animation-and-interaction.md). The worked records are in [examples/10-animation-foundations](../examples/10-animation-foundations/) and [examples/11-animation-and-interaction](../examples/11-animation-and-interaction/).

## Executive summary

You animate your game's main character, or the main thing the player controls, and connect its animation states to player actions through a state machine. Before you change any animation track, timing or transition, you write a behavior check that pins what the game does now, separating numbers you may change on purpose from facts that must survive. You then test the edges, including an action requested during another action, and judge feel and readability by playing. You hand in the repository tagged `a8`, a test report, and a `godot-walkthrough` film of the states in real play. Grading follows the course's 60/10/10/20 split. A passing check proves that the animation state follows the player under the inputs you scripted; it does not prove that the motion looks right, that the art matches the collision shape, or that the game feels better.

## Your task

**The minimum animation set.** The course's earlier animation assignment asked for three animations, and they remain the floor:

| # | Animation | What counts | Typical Godot form |
|---|---|---|---|
| 1 | Simple animation | Movement with no rig and no frames: a pickup, door, platform or UI element | an `AnimationPlayer` clip keying position, rotation or scale |
| 2 | Sprite sheet or rig | Your main character or object animated from frames or from a rig | `AnimatedSprite2D`, or `Sprite2D.frame` keyed in an `AnimationPlayer`; `Skeleton2D` with `Bone2D`s; a 3D model's skeletal clips |
| 3 | Cycle | A looping movement cycle (walk, run, fly, swim, idle) whose first and last frames match | a clip with a linear `loop_mode` whose values at time 0 and at `length` are equal (a ping-pong clip reverses instead and needs no match) |

**Which of the three your game needs.** A 2D game with drawn or generated frames needs all three, built on your Assignment 2 character states. A 3D game needs all three: item 2 is a rigged clip on a `Skeleton3D`, item 3 a looping locomotion clip. If your main object is not a character (a ship, a piece), all three apply to it; its cycle can be an idle or engine loop. A character drawn entirely in code, as in `walker-jumpman-clawd`, still needs item 2: render its poses into a sheet, or rebuild it on a 2D rig. If an item truly cannot exist in your game, say so in `CHANGE-BRIEF.md`, name the substitute that does the same work, and justify it.

**The state machine.** Connect at least **four animation states** to player actions: rest, movement, your core action, and one of air, hurt, fail or celebrate, taken from your Assignment 2 character sheet. Each is entered from a real player action, or from a physics or game condition an action causes. At least one action must **commit**: once started, it plays to its end or to an interrupt rule you state.

Find where your game's state already lives first; Chapter 11's three Walker builds keep it in three different places. A second state machine that disagrees with the first is worse than none, so drive animation from the existing authority or replace it. Any wiring the chapters teach is acceptable: an `AnimationTree` with an `AnimationNodeStateMachine` (pull, through Auto transitions and advance expressions, or push, through `travel()`), state nodes whose `enter()` calls `AnimationPlayer.play()`, or a selector function evaluated every frame. They fail differently; your brief says why you chose yours.

**One game, one repository.** From Assignment 2 on, you build one game: the one you chose in Assignment 2, in a repository whose name begins `walker-`. This assignment adds one layer to it and is submitted as the git tag `a8`. If you changed games before Assignment 4, the tag continues on the new repository; say so in your submission note.

**Tools, cost and provenance.** Claude Code assistance is expected; use your Northeastern access. No purchased credits or paid generation is required. Generated motion supplies frames or pose data, never the state logic. Record every frame set, rig and motion source in `SOURCES.md` (tool, input, terms, date, your edits), and do not capture motion from anyone who has not agreed. Commit the editable sources of frames you drew or edited (layered images, a rig file) so their layers and keys can be inspected; link any file over 25 MB from your media storage.

## 1. Predict

Commit `CHANGE-BRIEF.md` before you ask Claude to change anything. Keep the original; add dated revisions below it.

- **The animation set:** which of the three items your game needs, the clip for each, and any substitute with its reason.
- **The state table:** each state, what enters and leaves it, its cross-fade, whether it loops, and which states may interrupt which. Write every transition out of every state before you read the agent's list.
- **Where state lives now,** and the wiring you chose, with the reason.
- **At least three edges** you will test, one of them **an action requested during another action**, with the behavior you intend. Others: input held through a landing, a reversal at full speed, an interrupt (reset, death, pause), the same action requested while it plays. Where the answer is a feel decision, decide and write it down: in the finite-state-machine demo, an attack in mid-air hangs the jump for about 0.45 s, which can be a bug or a feature, and a test should pin whichever you choose.
- **Timing predictions:** physics ticks per second, test frame rate, ticks per rendered frame, and the frame on which you expect one of your keys to be observed. In Chapter 10, a key at 0.1 s (frame 12 at 120 fps, on paper) was observed on frame 14.
- **A motion reference** for at least one action: its source, frame rate, and the frame counts you measured. At 30 fps, 0.1 s is three frames.
- **At least three predicted failure cases,** each with its check.

## 2. Build It

Read both module lessons and both chapters first. Then open the chapters' Walker builds; the demo adaptations keep the upstream MIT license, and `walker-jumpman-clawd` has none.

- [walker-2d-finite-state-machine](https://github.com/nikbearbrown/walker-2d-finite-state-machine): state nodes on a pushdown stack, each `enter()` calling `AnimationPlayer.play()`; a sword in `godot/player/weapon/Sword.tscn` and `sword.gd` whose clips carry value and method tracks. Chapter 10 pins its timing.
- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer): an `AnimationTree` blend tree that `godot/player/player.gd` writes every physics tick. Chapter 11 replaces its hard ground/air switch with a state machine.
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd): a priority-list selector, `visual_animation()` in `godot/features/player/player.gd`, choosing among code-drawn animations. Its presentation checks set velocity directly: they test the selector, not that a key press produces the walk.

### Pin first, then change

Work in this order, one bounded step per prompt and one commit per verified step:

1. **Baseline:** import, run existing checks.
2. **Pin.** Write a headless behavior check against the game as it is, and commit it before any track, timing or transition changes. If your game has little animation yet, pin what exists: the character's state on every frame under scripted input, and the timing of anything already keyed. Each new clip gets its pins once you have played and approved it.
3. **Build** the animation set and the state machine, one change per prompt.
4. **Edges:** edge tests, fixes, and a classification of every FAIL.
5. **Re-pin,** only after you have played the changed timing, in its own prompt and commit.

Start with a plan, not an edit:

```text
Read my CHANGE-BRIEF.md and README.md, then the player scene and script,
every AnimationPlayer and AnimationTree in the project, and my existing
tests. Use Walker's brief → build → playtest → inspect → revise workflow.
Inspect first and change nothing. Tell me, with file and line references,
where the character's gameplay state lives now, which code or animation
keys decide each state and transition, and the physics ticks per second.

Then propose, without editing: (1) one headless SceneTree test that pins
the CURRENT behavior before any animation change. It drives the game only
with input events or Input.action_press/action_release; it never calls
state methods, travel() or AnimationPlayer methods and never writes
velocity, position or tree parameters; it steps one frame at a time and
prints PASS/FAIL lines in two groups, TIMING (numbers I may change on
purpose) and INVARIANT (facts that must survive any change). (2) The
smallest plan for my animation set and state machine. If a measurement
contradicts what the code suggests, keep the measured value and list it
under ANOMALIES; do not fix it. After I approve a step, implement only
that step, run the checks, paste the real output, and tell me what still
needs a human to play.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan. The chapters' prompts model the later steps: Chapter 10's pin, one-change and re-pin prompts; Chapter 11's state-machine prompt and its rerun of an edge at both physics-tick offsets.

**Keep the change and the re-pin apart.** An agent that edits the behavior and the expectation in one step can make any change pass. A re-pin changes only TIMING constants, never an INVARIANT or a tolerance.

**Pin the time step.** Frame-counted checks need `--fixed-fps`, and you need to know how many physics ticks fall in a frame: Chapter 10 used 120 for a 120-tick project; Chapter 11 used 60 against 120 ticks, two per frame. Without the flag, Chapter 10's pin test failed 7, 9 and 9 of its 20 checks in three runs; its invariants held every time.

**What must not change:** movement tuning, collision shapes, input actions, your Assignment 2 audio, your Assignment 7 effects, and earlier tests. If an animation key decides a gameplay fact (a hitbox window, a sound), pin it.

**Done** means the pin predates every animation change, the animation set and state machine run in the game, every edge test passes in runs you made, every FAIL is classified, and you have played every state.

### What the agent is likely to get wrong

Each of these happened in the chapters' records.

- **Counting is not watching.** The finite-state-machine build's combo test passed "second swing starts" because a counter reached 2, while the blade sat at 75° for 24 frames: `play()` with the name of the animation already playing does not restart it. Record animation position and how far the keyed property travels. The fix was one line, `$AnimationPlayer.seek(0.0)`.
- **A correct change breaks something else.** Moving the sword's hitbox window into the animation removed swing two's hitbox. Only the pinned check caught it; the two older tests passed. Have the agent classify every FAIL as asked-for or not.
- **Invented API, orphaned process.** Claude Code gave a state machine a `start_node` property that does not exist; the script error stopped the test before `quit()`, and the orphaned Godot process ran for about half an hour. Wrap every run in `timeout`.
- **Defaults that never fire.** Expression transitions left at the default `advance_mode` (Enabled) are used only by `travel()`; the same machine was first stuck in `Start` with no way out.
- **A real bug called a test problem.** A held-jump landing between two `AnimationTree` updates left the machine in `fall` while the robot rose. The agent blamed the test and began editing frame counts. A per-tick trace found the bug; a one-transition fix closed it.
- **Lying comments, lost sessions.** A constant commented "6 frames" counted physics ticks (12 per 0.1 s). A usage limit ended both chapters' Claude Code runs mid-task, leaving uncommitted, unverified work.

An agent's "done" is a claim; check it with a command you ran.

## 3. Use It

Record actual results in `TEST-REPORT.md`, with the source revision, engine version and mode of each run:

| Check | Evidence to collect |
|---|---|
| Pinned baseline | The pin test's output before any animation change, and that commit's SHA. |
| Animation set | Each item (or substitute) running; a headless seam check for the cycle (values at time 0 and at `length` match, loop mode set). |
| State wiring | Every state entered from its real action under scripted input, with the per-frame log. |
| Edges | Each edge test's output, at both physics-tick offsets where a frame holds more than one tick. |
| Mutation check | The strengthened edge test, run on the pre-fix version in a throwaway copy, fails. A test that passes on the broken version has not tested the fix. |
| Change log | Every FAIL after every animation change, labeled asked-for or not, and what you did. |
| Automated checks | Commands, modes, real output, and any failed or updated test, explained. |

If the cycle plays through `AnimatedSprite2D`, write the equivalent seam check against its frames and say how; Chapter 10 prefers keying `Sprite2D.frame` in an `AnimationPlayer` for anything gameplay reads. Read a 3D pose modified after animation (IK) when `skeleton_updated` fires; Chapter 10's IK test failed a working rig by sampling between updates. Import before testing: an un-imported copy in Chapter 10 printed 11 of 11 PASS while its textures failed to load, so read the whole log.

### Play it (HUMAN CHECK)

Play:

1. Every state and every edge at normal speed, then slowed: `godot --path godot --time-scale 0.25`.
2. Switch the Scene dock to **Remote** while the game runs, select the `AnimationPlayer` or `AnimationTree`, and watch the state change as you act.
3. Turn on **Debug > Visible Collision Shapes** and compare the art with the collision shape in every pose, as your Assignment 2 character sheet planned.
4. Compare your motion reference's frame counts with your key times and cross-fades.
5. Can a player tell which state the character is in, with sound muted?

Record each judgment as a dated verdict, not a test result. Approve changed TIMING in `FRICTIONAL.md` only after you have played it, then re-pin. Include **at least one documented inspect-and-revise cycle** driven by play, such as a cross-fade shortened because a landing read as a stumble. Do not delete a failing assertion or weaken an expected result to obtain a green report. If another person plays, record their actual feedback; do not invent a playtester. Your own playtest is required, and no scripted route replaces it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-walkthrough`** workflow with the **`walker`** modifier. The original skill spelling is **`godot-waikthrough`**. Ask Claude Code to read the installed skill instructions and follow them; it is not a standalone executable. If your checkout lacks the skill, request the course-provided version.

Make **one** landscape film that:

1. Introduces your game and its state table in plain terms.
2. Shows each state entered by its real action in play, and the three animations of the minimum set, with the cycle looping several times.
3. Shows your edges played, including an action requested during another action. For a timing-sensitive edge, show the sequence with input or tick evidence, not a still.
4. Explains at least one cause-and-effect connection between a source change (a key time, a transition setting, a restart) and what the player sees, before and after.
5. States what the pins and edge tests establish, what you judged by playing (with your motion-reference numbers), what remains open, one concrete next step, the human and AI contributions, and the game revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label scripted-input captures, slowed replays and held frames accurately; a scripted capture is not a human playtest. Do not change the game solely to hide a defect.

Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. A second film, a vertical Short, paid media generation and public YouTube publication are **not required**. The film is part of the 60-point category below and does not substitute for working source.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with the animation set, state machine and tests; exclude generated caches and credentials.
- `README.md`: project name, starting point and credit, engine version, run instructions, controls, how to reach each state, known limitations, and final-film link.
- `CHANGE-BRIEF.md` with its original state table, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md` with all animation provenance.
- The editable animation sources, the tests and their logs, and the film's beat sheet, script/prompts, and coverage and evidence records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit in the order you worked (baseline, pin, each change, each fix, each re-pin), with messages that name a change and its check, for example `Restart swing on every combo step; pin invariants pass, 10 timing pins await approval`. Tag the submitted commit `a8`.

## 5. Verify and submit to Canvas

Clone the `a8` tag into a fresh folder, import once, and run every check yourself with the time step pinned. The chapters' commands:

```bash
timeout 120 godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
```

```bash
timeout 180 godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
```

A pasted transcript is not a result. Confirm that the film shows the source you are submitting.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 8 - Animation Wired to Player Actions
Student:
Project name:
GitHub repository URL and tag (a8):
Submitted commit SHA:
Commit SHA of the pinned baseline test:
Game-source revision shown in the film:
Godot version and operating system:
Physics ticks per second and test frame rate:
Animation set (simple / sheet or rig / cycle, and any substitute):
State machine (where state lives, wiring, states):
Edges tested:
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
| Pin before change: a brief with animation set, state table, edges, timing predictions and motion reference (5); an input-only behavior check, TIMING separated from INVARIANT, committed before any animation change (7). | 12 |
| Animation set: simple animation (3); sprite sheet or rig, with editable sources and provenance (5); a cycle whose first and last frames match, seam checked (4). | 12 |
| State machine: four or more states, each entered from a real player action or the condition it causes, one authority for state (7); transitions configured and justified, including a committing action and its interrupt rule (5). | 12 |
| Edges and verification: three or more edge tests including an action during another action, both tick offsets where relevant, a mutation check (5); every FAIL classified, re-pins separate and approved after play (3); dated play verdicts against a motion reference, one evidence-driven revision (6). | 14 |
| Brutalist explainer: accurate explanation of the wiring and one cause-and-effect link (4); real play of each state and the edges (3); tests versus feel judgments, and limits (2); readable, audible film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; smooth animation does not repair an incorrect explanation or an unpinned change. A passing check establishes that the animation state follows the player under the inputs you scripted; it does not establish that the motion reads well, that the art matches the collision shape, or that other input rhythms behave.

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

Use `SOURCES.md` to credit your starting point, every frame set, rig, motion source and asset, collaborators, and tools. Describe what AI contributed to the code, tests, animation, script, beat sheet, visuals and narration, and what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to change a key time and predict which pins fail. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

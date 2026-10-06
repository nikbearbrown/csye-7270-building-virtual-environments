# Assignment 9 - Sound That Provably Plays, and a Frame You Can Afford

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 90 after the first class day.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

Covering Modules 12 and 13, this assignment adds two layers to the game you have built since Assignment 2. First, your sounds fire on real events, travel through named buses, and are proved to reach the mix by a headless test that uses the instrument Module 12 showed actually works: a capture effect on the bus, not the bus meter. Then a person listens, because no test can. Second, you state a frame-time budget, measure a baseline in repeated fresh runs, make one optimization you can justify, prove the game still behaves the same, and measure again. "Not worth it" is an acceptable conclusion if the numbers say so. You hand in tag `a9`, its evidence, and one `godot-gamedev` film with the `walker` modifier, graded 60 / 10 / 10 / 20. None of it proves the mix sounds good, that a sound lands on the beat as heard, or that a headless CPU number predicts a frame on a GPU, phone or headset you did not run on.

## Your task

Work from the [Module 12 lesson](../modules/12-audio-and-triggers/lesson.md) and [Module 13 lesson](../modules/13-profiling-and-optimization/lesson.md), with the chapters [Audio and Triggers](../chapters/12-audio-and-triggers.md) and [Profiling and Optimization](../chapters/13-profiling-and-optimization.md) and their run records in [examples/12-audio-and-triggers](../examples/12-audio-and-triggers/) and [examples/13-profiling-and-optimization](../examples/13-profiling-and-optimization/).

**One game, one more layer.** Since Assignment 2 you have built one game in one repository whose name begins **`walker-`**. This assignment adds its audio and performance layer to that repository and is submitted as the git tag **`a9`**. Do not start a new project. If you changed games before Assignment 4, say so in the submission note.

**Tools and cost.** Claude Code through your Northeastern access is expected. No purchased API credits, paid generation service or paid profiling tool is required.

**Sound sources and rights.** Use your Assignment 2 sounds, new generations from free or local models under Assignment 2's rights rules, sounds written by a script you can read (Module 12's `tools/make_click.py` writes a 60 ms click with the Python standard library), or your own recordings. A third-party sound needs a license that permits it, recorded in `SOURCES.md`. Deliver OGG or WAV. A free editor such as [Audacity](https://www.audacityteam.org/) is fine for trims and loop points; record each edit.

### Part A — what your audio must do

Kinds of things; choose the events your game actually has.

| Requirement | Minimum |
|---|---|
| Buses | Master plus at least two named buses (for example Music and SFX) in `res://default_bus_layout.tres`; every player routed by name. |
| Event sounds | At least **five** events with their own sounds, at least two of them from layers added after Assignment 2. |
| A loop | At least one music or ambient loop on its own bus, with no audible seam. |
| A silent case | At least one near-event that must stay silent. In Module 12's rhythm game, a Miss makes no click. |
| Triggers | Each sound plays from the code that already represents its event. Sound never decides game state. |
| Polyphony, pause, restart | Per player: `max_polyphony`, behavior when the tree pauses, behavior on restart. A sound that plays while paused needs a `process_mode` that keeps running. |
| Position | A sound with a place in the world uses `AudioStreamPlayer2D` or `3D`, and you say where the listener is. |

The old course's audio mini-assignment said to "Organize sounds into categories for implementation"; buses are those categories, made real.

### Part B — what your measurement must do

| Requirement | Minimum |
|---|---|
| Budget | Your target refresh rate in milliseconds per frame, the share the measured system may use, and a mobile/XR section. |
| Load case | The heaviest moment your game really has, loadable by a benchmark without changing the default game, plus a stress level if the real load is small. |
| Harness | A headless script printing one CSV line per run: mean, 95th-percentile and maximum frame time, object and node counts, and one counter your game publishes with `Performance.add_custom_monitor()`. |
| Baseline | At least ten fresh-process runs per configuration, alternating, with machine, date and load average. |
| One optimization | One change chosen from evidence, a parity test, the same measurement repeated, and a keep-or-revert decision. |

## 1. Predict

Before any agent edits anything, add an Assignment 9 section to `CHANGE-BRIEF.md` and commit it. Keep earlier sections; add revisions rather than rewriting.

- **Event-to-sound map:** per sound, the event, the signal or function representing it, the player, the bus, `max_polyphony`, pause and restart behavior; plus the silent case and why.
- **Mix intent:** bus levels in decibels and what must be audible over what.
- **Audio predictions:** what does `playing == true` one frame after a trigger prove? What will the bus meter show headless for your shortest sound? What happens on pause mid-sound, and on restart?
- **Measurement predictions:** the budget, the baseline cost at real and stress loads, the optimization you expect and its effect, and what `Performance.TIME_PROCESS` reads after a run shorter than one second.
- **At least three predicted failure cases** and how you will check them, for example a held key firing every frame or an optimized version that stops colliding.

## 2. Build It

Work in inspectable increments: one bounded change, its diff, its check. What must not change: game rules, timing and earlier tests; the benchmark sits beside the default game. Done means every row of the Use It table has evidence. Put the plain command `godot` and your test commands in `CLAUDE.md` or `AGENTS.md`, and run agents with `--disallowedTools "Skill"`; Module 13's agent, refused its absolute Godot path, invoked a skill that edits permission rules.

Start with a plan:

```text
Read my CHANGE-BRIEF.md (Assignment 9 section), README.md, project.godot,
default_bus_layout.tres if it exists, every script that plays a sound or
represents an event in my map, and my existing tests.
Use Walker's brief → build → playtest → inspect → revise workflow.
Part A: propose the smallest plan to create my buses, route every player
by name, play each sound from the code that represents its event, and set
polyphony, pause and restart behavior as my brief says. Part B: propose a
benchmark entry point for my load case that does not change the default
game. List the files and nodes you would create or change. Do not edit yet.
After I approve a step, implement only that step, show the diff, run the
relevant headless check, and tell me what still needs human listening or
a human with a screen.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan.

### Part A — sound on real events, and a test that hears it

The model is [walker-audio-rhythm-game](https://github.com/nikbearbrown/walker-audio-rhythm-game) (MIT). In Module 12's run (27 September 2026), a probe measured its click at −6.12 dBFS on the SFX bus and on Master, the WAV's own peak, while the SFX meter read −200 dB throughout. For a positional 3D sound, read `godot/enemy/enemy.tscn` in [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer).

Your audio test (a `SceneTree` script under `godot/tests/`) uses the module's method:

1. Load the real scene and fire real events (input or the game's own signal), never a player's state directly. Read `playing` **immediately** after each trigger, before any `await`: under the headless Dummy driver a 60 ms sound can start and finish between two frames, and the module's check that waited one frame failed one run in ten.
2. Prove level with an `AudioEffectCapture` added to the bus at run time and removed afterwards, never saved into the layout. The bus meter is the wrong instrument: the Dummy driver mixes 4,096 frames per burst and the meter holds only the last 512, so it misses short sounds. Compare each captured peak with the file's own peak and explain any difference.
3. Test mute on the next bus. A capture hears its bus before that bus's fader and mute, so mute the effects bus and check that a capture on Master stays below −60 dBFS. Mute music while measuring effects.
4. Prove the silent case silent, by capture.
5. Add a check the module's test did not have, a trigger count: drive rapid repeats and a held input, count starts per sound (a counter in the one function that plays it), and assert the count equals the number of real events.
6. Test pause on a long player: its playback position must not advance while paused and must advance after. A pause check on a short sound can pass by testing nothing. Test restart: nothing left over plays.
7. Wait on the wall clock. Never add `--fixed-fps` to audio tests; the audio thread runs in real time. Stop the players and wait about 0.2 s before freeing the scene.

Then adapt the instructor's independent probe, [`verification/verify_levels.gd`](../examples/12-audio-and-triggers/verification/verify_levels.gd), which shares no code with the agent's test.

**What agents got wrong here.** Module 12's first session printed `PASS … (SKIP: Dummy driver …)` for two checks before the test had ever run, believing headless Godot cannot meter audio. Your test prints SKIP, never PASS, for anything it cannot check. The same session hand-wrote a `.import` file with an invented UID (read every `.import`, `.uid` and `.tscn` diff), and a test that errored before `quit()` left Godot running for 19 minutes (use `timeout`). The prompt author's own meter requirement was also wrong: probe before believing anyone about what a headless run can observe.

### Part B — a budget, a baseline, one justified change

The model is [walker-2d-bullet-shower](https://github.com/nikbearbrown/walker-2d-bullet-shower) (MIT) and Module 13's example, whose decision is the standard. At the game's own 500 bullets, servers saved about 0.16 ms of a 16.7 ms budget, so the optimization was **not** justified; at 5,000, 9.9 ms against 2.3 ms, it was.

**Budget.** Compare milliseconds, not frames per second: 16.7 ms at 60 Hz, 13.9 ms at 72 Hz, 11.1 ms at 90 Hz.

**Mobile and XR.** Write this section in `PERFORMANCE.md` even for a desktop game. Name the renderer you would use on a phone or standalone headset and the Godot page you followed (the official pages disagree for Android XR), the budget at the headset's rate for two eye views, and which of your costs a battery-powered, tile-based mobile GPU would punish first: fill rate, transparency, full-screen effects. A desktop CPU ratio is a hypothesis for the device, not a prediction of its milliseconds. Device runs are optional and need export templates and the platform SDK (Module 15).

**Harness.** Make the load configurable without changing the default, and model the benchmark on the module's [`bench/bench.gd`](../examples/13-profiling-and-optimization/bench/bench.gd), which ran like this (yours takes its own modes and counts):

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://bench/bench.gd -- --mode=servers --count=500 --frames=600
```

Under `--fixed-fps 60` each frame advances 1/60 s and the next starts at once, so wall time per frame is CPU work per simulated frame; without it, headless Godot sleeps toward a 6.9 ms frame and hides smaller costs. The dummy renderer reports zero draw calls and video memory, so GPU cost is not in the number. `Performance.TIME_PROCESS` is the worst frame of roughly the last second, and zero before a second has passed; Module 13's agent called it "last frame", and its own output refuted that.

**Repeat.** Adapt the instructor's [`sweep.sh` and `summarize.py`](../examples/13-profiling-and-optimization/verification/): fresh processes, alternating configurations, ten runs each, then the median and range of run means, median p95 and worst frame, with load averages. In Module 13 identical code ranged from 8.5 ms to 39.0 ms between runs on a busy machine.

**Look with a screen.** In the editor's Debugger, **Monitors** show process time, physics time and node count; the **Profiler**, started by hand and off while you time, shows where the time goes; the **Visual Profiler** shows CPU and GPU render stages at a fixed window size, but not with the Compatibility renderer on macOS. A GPU-bound cost only appears here.

**Choose one optimization** from what the profile showed: many nodes replaced by server objects or a `MultiMesh`; a load moved off the main thread with `ResourceLoader.load_threaded_request()`; a costly decision run less often than every tick; less overdraw or render scale (GPU work, measured in the editor). Keep both versions selectable so the sweep alternates them. Write the parity test first, with stated tolerances. Module 13's server version had shipped with bodies falling under gravity, each collision shape 16.05 px below its sprite, a bug no screenshot shows. A faster version that plays differently is not an optimization.

**What agents got wrong here.** Module 13's agent edited a test it was not asked to touch, left a headless process running after a script error, and wrote an 82-line `FRICTIONAL.md` entry repeating its wrong `TIME_PROCESS` definition. Check what an agent says about its own instrument against the output.

## 3. Use It

Play with headphones at a fixed volume, then muted. Record actual results in `TEST-REPORT.md` (audio) and `PERFORMANCE.md` (measurement), with revision, engine version, machine and date:

| Check | Evidence to collect |
|---|---|
| Routing, triggers, silent case | Test output and capture peaks; what the editor's **Audio** panel showed during play. |
| Reaches the mix | Capture peak per bus against the file's peak; Master silent with effects muted. |
| No double triggers | Start counts under rapid repeats and a held input. |
| Pause and restart | Loop position frozen while paused and moving after; nothing left over after restart. |
| Repeated runs | The audio test run ten times, every result kept. A test that passes nine times in ten is a test that fails. |
| **HUMAN CHECK: listening** | Device, volume, date. Per event: audible over the music, masking it, confirming or distracting? Rapid repeats: feedback or noise? Any sound late against the picture? Pause mid-sound; restart right after a sound: does anything survive? Three loop repetitions: click or gap? Muted: still playable? |
| Budget and baseline | Harness CSVs and the summary at real and stress loads, each as a share of the budget. |
| **HUMAN CHECK: profiling with a screen** | Monitors and Profiler observations, window size, renderer; the Visual Profiler result or why it could not run. |
| Parity and after | Parity PASS lines, the repeated sweep, the decision. |
| Earlier layers | Earlier assignments' tests still pass. |

A test that finds samples on a bus is not a listener; your own listening is required, and other listeners' words are recorded only if real. Never delete a failing assertion or weaken an expected value to get green. Document at least one inspect-and-revise cycle driven by an observation, such as a bus re-leveled after listening or an optimization reverted because parity failed.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier. Ask Claude Code to read the installed skill and follow it; if your checkout lacks the skill, request the course-provided version.

Make **one** landscape film that:

1. Introduces your game and both layers in plain terms.
2. Traces one sound: the event in code, the line that plays it, the bus it reaches, the capture result.
3. Includes **at least one clearly labeled segment where the game's own audio is audible at the moment its trigger fires**, recorded from real play with a real audio driver and kept quietly under the narration, as the skill's audio policy allows; a headless log is not audio. Check the skill's audio policy first and ask for the course-provided method rather than dubbing sounds in. Gameplay audio stops before the regular outro.
4. Shows the budget, the baseline, the optimization beside the original, the parity PASS lines, the after numbers and the decision, and says aloud what headless numbers exclude.
5. States your mobile or XR constraint, what you tested, what remains uncertain, one next step, the human and AI contributions, and the source revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed editor views, scripted-input captures and held frames accurately. Follow the skill's native **4K landscape** rendering and checks, then watch and listen to the final export. There is no minimum runtime. A second film, a vertical Short, paid media and public YouTube publication are **not required**.

### Post the version on GitHub

- The Godot project with its used audio, bus layout, audio test, harness and parity test; no caches or credentials.
- `README.md`: engine version, run instructions, controls including mute, the exact test and benchmark commands, limitations, film link.
- `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `PERFORMANCE.md` with its CSVs, and `FRICTIONAL.md`.
- `SOURCES.md`: every sound's origin and license, and the syllabus's labor-separation disclosure naming the capacity you exercised (the syllabus assigns PA to Week 12 and EI to Week 13).
- The film's beat sheet, script/prompts, and evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access. Tag the final submitted commit `a9`. Commit messages name a change and its check, for example `Route pickup sound to SFX; capture test passes 10 of 10`.

## 5. Verify and submit to Canvas

Clone tag `a9` into an empty folder, replacing the placeholders:

```bash
git clone --branch a9 <your-repository> ../a9-check
```

Then, inside `../a9-check`:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/<your-audio-test>.gd
```

Run the audio test several times, the parity test and one harness run, and confirm every used sound is present. Submit a source ZIP of that revision, without caches, credentials or large media, with `SUBMISSION.md`:

```text
Assignment: Assignment 9 - Sound That Provably Plays, and a Frame You Can Afford
Student:
Project name:
GitHub repository URL:
Tag a9 commit SHA:
Game-source revision shown in the film:
Godot version, operating system, machine:
Buses, and the events routed to each:
Sound sources and licenses:
Frame-time budget (target, Hz, ms):
Baseline and after (median of runs, ms, at which load):
Optimization kept or reverted, and why:
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and the film must refer to the same submitted work.

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
| Audio on real events: named buses, every player routed (4); sounds played from their events' code, the silent case silent, sound never deciding state (5); polyphony, pause and restart as briefed (5). | 14 |
| Proof that sound reaches the mix: a repeated capture test covering every event, the silent case and mute, no SKIP counted as PASS (6); a trigger-count check (3); a recorded listening check (3). | 12 |
| Budget and baseline: a budget in milliseconds with mobile/XR constraints (3); a harness with mean, p95, max, counts and a custom monitor (3); ten or more fresh runs per configuration, with headless limits stated (4). | 10 |
| One justified optimization: chosen from profile evidence, with a prediction (3); parity passing before timing is trusted (3); repeated measurement and a defensible keep-or-revert decision (4). | 10 |
| Verification: the `a9` clone runs and earlier tests pass (2); an evidence-based revision and an honest limitation (2). | 4 |
| Brutalist explainer: accurate code-then-result traces for a sound and the optimization (3); a labeled segment of real game audio (3); numbers and decision, headless limits said aloud (3); a readable, audible film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing capture test shows that samples reached a bus, not that anyone heard them, and a headless frame time is CPU work per simulated frame, not a frame on a screen.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit (tag `a9`) and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit every sound, model, script, collaborator and tool, what AI contributed to the code, tests, harness, script, beat sheet and narration, and what you personally decided, heard, measured, changed or rejected.

The instructor or a TA may ask you to run your audio test or a benchmark in front of them, or to explain why a bus meter can miss a sound that a capture records. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship, provenance, listening, or measurement is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.

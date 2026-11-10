# FRICTIONAL — Assignment 6

My Assignment 5 log is in `../assignment-5/FRICTIONAL.md`.

## Entries

<!-- One entry per work session, newest last. Copy the block below. -->

### 2026-11-07 to 2026-11-10 — Choosing the two effects, the wall light switch, the A6 test wrapper and baseline, and writing the brief

- **Date and what I was working on:** 2026-11-07 to 2026-11-10. Starting A6 (particle effects). First choosing the two effects; building a new gameplay feature for Effect B's condition, a light switch on the wall; then replacing `scripts/run-test.sh` with the A6 version and running the baseline; finally writing CHANGE-BRIEF. The project also contains the tablet window built after A5 (2026-11-03 to 11-07); this is its first upload. When the tablet is picked up in one hand, a tablet window slides into the lower right of the screen, to be operated with the mouse later (`screen_tablet.gd`, and the `ScreenTabletLayer` in `player.tscn`). The game has only one tablet; the window is only how it is shown on screen. The window is rendered in its own small 3D world (a SubViewport), so it is drawn in front of everything and cannot clip into walls; that was my idea. Claude set up the window's nodes (its camera, the `ScreenTabletLight` that lights it, and the two slots); I typed the movement part of `screen_tablet.gd` and the `set_shown()` line in `player_controller.gd` with Claude guiding me section by section, and adjusted the slots; the comments and the part that turns the screen off as soon as it starts sliding out were written by Claude.
- **I tried / expected:**
  - Effect A: landing dust (landing is an event that repeats). Effect B: dust under the ceiling lights, with the condition "the ceiling lights are on". The base had no way to switch the lights, so I built one first: a switch on the wall; walk up and press F; one switch for all ceiling lights; the lights are on when the scene loads; I place the switch myself in the editor.
  - I expected the A6 baseline to match A5's final run (55 / 24×3 / 2 / 169, all passing).
- **What happened:**
  - Claude first went by the numbering in the course GitHub's `assignments/` folder and called A6 the shader audit. Only after I pasted the Canvas A6 text did it correct itself: Canvas A6 is particle effects, and the GitHub numbering is an unpublished draft.
  - I added the `interact` action (F) in the editor. Claude first said the `"device":16` in the file was wrong; it then looked up Godot's constants (`DEVICE_ID_KEYBOARD = 16`), admitted it had been wrong, and nothing needed changing.
  - When the switch was first connected to `CeilingLights`, a headless check showed it was not linked (`switch linked: false`): the scene file was missing the `node_paths` entry Godot needs. After that was added, the check passed: pressing F 3 m from the switch leaves the lights unchanged; at the switch, the first press turns the lights off and the second turns them on.
  - The baseline was 55 / 24×3 / 2 / **168 passed, 1 failed**. The failure is `test_materials.gd`'s "`base.tscn`: 3 Light3D nodes (got 4)": the test counts every light in the scene, and the extra one is the `ScreenTabletLight` in the on-screen tablet's SubViewport. The checks on the three ceiling lights themselves all pass.
  - While checking property names with ClassDB, we found that 4.7.2's `ParticleProcessMaterial` still has a property named `initial_velocity`, so the assignment's "rename to the Godot 3 property name" mutation may not fail.
  - While writing the brief, Claude asked whether the answers I pasted had been written by ChatGPT. They had not; they were my own words to Claude ("I suggest you pick these six predicted failures").
- **What I did:**
  - Chose the two effects and how the switch works (on the wall, the F key, all ceiling lights, on at the start); added the `interact` action in the editor; created `light_switch.tscn`.
  - Decided that F does nothing while the tablet is held (in one or both hands).
  - Confirmed the switch stays at (2, 1.55, 4.49); the switch plate was too hard to see, so I had Claude make it near-black (0.03, 0.03, 0.03).
  - Wrote the brief's intent, rules, evidence split, predicted failures, short answers and the prediction for every strip frame; checked and adopted the initial values Claude proposed ("use this version first"); corrected two of Claude's statements: Effect A's peak particle count is the sum of its two emitters, and Effect A's lifetime is longer than 0.92 s so that "landing again before the old effect has finished" can be tested.
  - Agreed to a notify-only `landed` signal in `humanoid.gd`.
  - Decided not to change `test_materials.gd` for now, and to record 168 passed, 1 failed as the baseline before A6, with the reason.
  - Set the division of work: Claude writes the check and capture scripts; I give the final verdict on the effects and also play the game myself.
- **What Claude or another person contributed:**
  - Claude Code (Claude Opus 5.5) completed `light_switch.tscn` (plate, lever, `InteractArea`), and added the `CeilingLights` node, the ceiling-light group and the switch to `base.tscn`;
  - wrote `ceiling_lights.gd`, `light_switch.gd`, and the intent → body → switch chain (the new lines in `character_intent.gd`, `player_controller.gd` and `humanoid.gd`); for these I said "you write it this time", and in A6 I write only the code the assignment requires me to write;
  - wrote the A6 `scripts/run-test.sh`, and ran all the headless checks and the baseline;
  - proposed the initial values from my intent, assembled my answers into the brief, and translated it into English.
- **What I understand now / still do not understand:**
- **Evidence and next step:**
  - `walker-survival-shooting/godot/world/light_switch/`, `godot/world/lights/ceiling_lights.gd`, `godot/base.tscn`;
  - `walker-survival-shooting/scripts/run-test.sh`; baseline logs in `walker-survival-shooting/logs/` (`test_materials_60fps.log` contains the one failure);
  - `walker-survival-shooting/CHANGE-BRIEF.md` (committed before the first agent prompt).
  - Next: A6 Step 1, prompt-1, where the agent revises CLAUDE.md.

---

### 2026-11-10 — A6 Step 1: the agent revises CLAUDE.md, and my review

- **Date and what I was working on:** 2026-11-10. A6 Step 1: having a separate agent session revise CLAUDE.md from the assignment's prompt-1, then reviewing it.
- **I tried / expected:** As the assignment suggests, a non-interactive `claude -p` run with the read-only allow list, started in the course repository's A6 folder (so it reads only the CLAUDE.md there, not my working folder's Chinese CLAUDE.md and memory), keeping `session-1.jsonl`.
- **What happened:**
  - This time `claude -p` ran normally in my own Git Bash; the A5 login error did not come back.
  - Result event: `success`, `end_turn`, 17 turns, about 2 minutes, about USD 1.11; **6 permission denials**: two read commands with `sed` / `for` loops, and four attempts to run Godot `--doctool` to dump the class docs and check property names (once in Bash, three times in PowerShell). After the denials it did not invent output; it wrote in CLAUDE.md that it could not run the engine and had not checked the other property names. The allow list had only `git` and `ls`, yet several `cd … && cat …` read commands ran; I only record that.
  - Only CLAUDE.md changed (`git status`), and `git diff --stat godot/shaders/` printed nothing. The draft was 83 lines, in the right order, with `@CHANGE-BRIEF.md` unchanged. Claude opened and checked each of its roughly 60 file and line references; all were correct.
  - It dropped the whole "Headless facts" block from the A5 CLAUDE.md.
  - Real problems it found on its own: `CeilingLights._ready()` emits nothing, so the dust has to query once; if the dust's `_ready()` runs before `CeilingLights`, it reads the field default; `landed` would fire for every Humanoid; `run-test.sh` always passes `--headless`, so it cannot take the frame strips.
  - The transcript is 294 KB (under about 1 MB) but contained 33 local paths and my user name; the uploaded copy replaces them with placeholders, and the raw transcript stays in my local folder.
- **What I did:** Ran the assignment's command in Git Bash; approved four review changes: restore the Headless facts block (the assignment's three lines, confirmed on this machine, plus A5's `--fixed-fps` line), record that ClassDB confirmed the brief's property names, note that `device 16` is `DEVICE_ID_KEYBOARD`, and note that strips come from a windowed Movie Maker run I start. The draft was committed unedited and the review separately.
- **What Claude or another person contributed:** The draft was written by another Claude Code session (Opus 5.5) from prompt-1. Claude Code (Opus 5.5) in my main session prepared prompt-1.txt and the command, read the result event and the diff, checked every reference, ran the Headless facts checks on this machine, replaced the local paths in the transcript, and wrote the four review changes I approved.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/prompt-1.txt`, `session-1.jsonl`, `CLAUDE.md` (draft 5f766ea4 unedited, review 3a398596). Next: Step 2, building Effect A's scene, configuration test and preview scene.

---

### 2026-11-10 — A6 Step 2: the agent builds Effect A, my first look at it, and the two mutations

- **Date and what I was working on:** 2026-11-10. A6 Step 2: having another agent session build Effect A's (landing dust) scene, configuration test and preview scene from the assignment's prompt-2; looking at the preview myself first, capturing the r0 strips and writing my first verdict; then the two mutations.
- **I tried / expected:** Running the assignment's Step 2 command (file edits and `run-test.sh` allowed, `godot/shaders/` refused) in the A6 folder. I expected to see the effect in the game.
- **What happened:**
  - Result event: `success`, `end_turn`, 26 turns, about 6 minutes, about USD 1.89; 4 permission denials: two compound read commands, one test call with a `GODOT=` prefix, and one direct run of the preview. After the denial it reran through `./scripts/run-test.sh`, so the test really ran. `git diff --stat godot/shaders/` and `scripts/run-test.sh` were unchanged.
  - Configuration test: 157 passed, exit 0; Claude reran it with the same result. Every value in the scene matches the brief's two tables. The agent added one setting the brief does not name, `billboard_keep_scale = true`, and said why; the camera looks down 30°, and the dark background spot was its guess.
  - It did not turn on the fixed seed for the preview's instance as the assignment asks. The review added it (preview instance only, seed 7270); the effect scene itself keeps random seeds.
  - I first started the game: the light switch worked both ways, but I saw no particles. Effect A is wired into the game only in Step 3, and Effect B is not built yet. I saw it once I ran the preview scene from the command line.
  - Watching the preview windowed, the ring seemed to appear "the moment the capsule spawns": a windowed run has no fixed frame rate, so frame 10 came less than 0.1 s after the start. In the strips, with `--fixed-fps 30`, frame 10 is at 0.33 s, and the picture first changes on frame 11.
  - The r0 strips: the dust is specks a few pixels wide, no longer visible after about 0.7 s; many are hidden by the capsule (emission radius 0.2 m, smaller than the capsule's 0.3 m); the ground ring is more noticeable than the dust; the "dark" background is not dark; the retrigger clears the old effect and replays 0.5 m away, as the rule says.
  - Mutation 1 (`initial_velocity_min` renamed to Godot 3's `initial_velocity`): the test exited 1, but **the engine reported nothing** and the effect still fired. In 4.7.2, `initial_velocity` is an editor-only Vector2 (min, max); the float written in the scene file is silently dropped, and min becomes 0.
  - Mutation 2 (`amount` 24 to 30, brief unchanged): the test exited 1. The scene was restored after each; the clean test passed 157.
  - Movie Maker also wrote a `frame.wav` for each run; Claude's deletion was stopped by an automatic permission check and went ahead only after I confirmed.
- **What I did:** Ran the agent command in Git Bash; chose to commit its output unedited first and add the fixed seed afterwards; ran the preview and the four captures and watched them slowed down; wrote my first verdict: the dust is not noticeable, and what I want is "a number of grey cloud-like puffs, not a number of dots"; agreed to deleting the extra frames; agreed to the two mutations.
- **What Claude or another person contributed:** Effect A's scene, configuration test and preview scene were written by another Claude Code session (Opus 5.5) from prompt-2. Claude Code (Opus 5.5) in my main session prepared prompt-2.txt (identical to the assignment text), read the result event and the diff, checked the scene values one by one, added the fixed seed, gave me the capture commands, matched the PNG numbering, read the strips, ran the two mutations and wrote TEST-REPORT, and replaced the local paths in the transcript (the raw transcript stays in my local folder).
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/prompt-2.txt`, `session-2.jsonl`, `godot/effects/landing_dust.tscn`, `godot/tests/test_landing_dust_config.gd`, `godot/previews/` (agent output unedited 6f3c739b, fixed seed 1df1db72); `captures/landing_dust/r0/`, `TUNING.md`, `TEST-REPORT.md`, `logs/mutation_*.log` (9fff7906). Next: Step 3, wiring Effect A to the `landed` signal and testing its state; the "cloud" change is left for Step 4.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-11-10 | Start Assignment 6: the Godot project as the A6 starting point (light switch, `CeilingLights`, on-screen tablet), the A6 `scripts/run-test.sh`, baseline logs (55 / 24×3 / 2 / 168 passed + 1 existing failure), the A5 CLAUDE.md copied unchanged, and SOURCES with the light switch's asset row |
| 2026-11-10 | Add the A6 CHANGE-BRIEF (both effects' intent, settings, rules, strip predictions, predicted failures, budgets and short answers), committed before the first agent prompt |
| 2026-11-10 | A6 Step 1: the agent's CLAUDE.md draft (unedited), prompt-1, the session transcript (local paths replaced), and my review (a separate commit) |
| 2026-11-10 | A6 Step 2: Effect A as built by the agent (scene, configuration test, preview scene; unedited), prompt-2, the session transcript (local paths replaced), the fixed seed on the preview's instance, the r0 strips, my first verdict and Claude's reading (TUNING), and the two mutations (TEST-REPORT) |

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

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-11-10 | Start Assignment 6: the Godot project as the A6 starting point (light switch, `CeilingLights`, on-screen tablet), the A6 `scripts/run-test.sh`, baseline logs (55 / 24×3 / 2 / 168 passed + 1 existing failure), the A5 CLAUDE.md copied unchanged, and SOURCES with the light switch's asset row |
| 2026-11-10 | Add the A6 CHANGE-BRIEF (both effects' intent, settings, rules, strip predictions, predicted failures, budgets and short answers), committed before the first agent prompt |

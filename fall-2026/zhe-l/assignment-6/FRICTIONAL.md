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
- **What I understand now / still do not understand:** I understand now that before making a particle effect I have to think through when it appears, how long it lasts and how it finally disappears. Once the times are turned into frame numbers, it is much easier to judge whether the effect in a capture is what I expected. For example, the landing dust's full fade and the replay on a second landing have to be captured separately; otherwise the old cloud is cleared early and I can never see it fade out on its own. I also learned that a passing headless test only shows that the settings and the trigger logic pass their checks; whether the dust can actually be seen, or is too bright, I still have to check in the game. And when a test fails, I first look for the cause: this time the test also counted the light inside the tablet, so I record that existing failure first and then watch for any new problems.
- **Evidence and next step:** `walker-survival-shooting/prompt-2.txt`, `session-2.jsonl`, `godot/effects/landing_dust.tscn`, `godot/tests/test_landing_dust_config.gd`, `godot/previews/` (agent output unedited 6f3c739b, fixed seed 1df1db72); `captures/landing_dust/r0/`, `TUNING.md`, `TEST-REPORT.md`, `logs/mutation_*.log` (9fff7906). Next: Step 3, wiring Effect A to the `landed` signal and testing its state; the "cloud" change is left for Step 4.

---

### 2026-11-10 to 2026-11-11 — A6 Step 3: wiring Effect A to the landing, and testing its state

- **Date and what I was working on:** 2026-11-10 to 11-11. A6 Step 3: having the agent propose a plan first, and after my approval wire Effect A to the player's landings and write a state test driven by real keys.
- **I tried / expected:** Following the assignment's "plan first, implement after approval", in two invocations: a plan session with read-only tools, then `claude -p --resume` on the same session, with edit tools, after I approved. I expected the test to pass at once.
- **What happened:**
  - Plan session: `success`, 17 turns, about USD 1.03, no permission denials, no file changed. The plan had three steps: the `landed` signal in `humanoid.gd`, the trigger script in `base.tscn`, and a new state test (7 assertions, each tied to a brief rule). It said on its own that `humanoid.gd` would get one more member and one small function, and asked me to confirm.
  - The assignment says to approve one step at a time; I chose to approve all three at once.
  - First implementation: all three steps were done, but the new test gave 23 passed, 4 failed. On physics frame 1, Jolt leaves the player 2.7 mm inside the floor, and on frame 2 pushes it back onto the floor, which counted as a landing: **the dust fired on scene load**, exactly what my brief forbids. The agent did not fix it on its own; it proposed two fixes and waited for my choice.
  - With a headless probe, the agent found that because this effect has `explosiveness = 1`, `emitting` turns false on the frame after `restart()`, so the CLAUDE.md headless fact was not accurate. Claude confirmed this with its own probe: the end of a burst is the `finished` signal.
  - After I chose `_has_touched_floor`: 27 passed, 0 failed. The agent temporarily replaced `restart()` with `emitting = true` and 5 checks failed, so the test tells the two apart; `restart()` was restored.
  - Every existing test matched the baseline: 55 / 24×3 / 2 / 168 passed 1 failed / 157. A Jolt warning appeared once in two logs during the agent's runs; Claude's repeated reruns did not show it again.
  - I ran each approval command twice. The second `>` overwrote the output file, so `session-3-impl.jsonl` and `session-3-fix.jsonl` hold only the repeated runs (the agent answering "already done"). The two runs that really changed code are in Claude Code's own full local transcript (about 1.7 MB, over the assignment's ~1 MB limit), so what is posted is the labelled excerpt `session-3-excerpt.md`.
  - I pressed F5 in the editor and played: on landing there is dust and the ring, and no false trigger at the start.
- **What I did:** Ran the plan session and the resumed sessions; approved all three steps at once (including `_was_on_floor`, with English comments); chose `_has_touched_floor` of the two fixes; played the game to look at the landing effect and the start.
- **What Claude or another person contributed:** The plan, the three steps, the fix and the test were written by another Claude Code session (Opus 5.5) from prompt-3 and my two approvals. Claude Code (Opus 5.5) in my main session prepared prompt-3.txt (identical to the assignment text) and the two approval messages (written in English from my decisions), checked the keys, speed and timing the plan relied on, read the result events and the diff, reran every test itself and found the Jolt warning to be intermittent, confirmed the `emitting` behaviour with a probe and corrected the course CLAUDE.md, built the excerpt from the full local transcript, replaced the local paths, and wrote TEST-REPORT's Step 3 section.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/prompt-3.txt`, `approve-3.txt`, `approve-3b.txt`, `session-3-plan.jsonl`, `session-3-impl.jsonl`, `session-3-fix.jsonl`, `session-3-excerpt.md`; `godot/characters/human/humanoid/humanoid.gd`, `godot/effects/landing_dust_trigger.gd`, `godot/base.tscn`, `godot/tests/test_landing_dust_events.gd`, `logs/test_landing_dust_events_60fps.log` (agent output unedited cb911e6e); the `CLAUDE.md` correction (ba7d1711); TEST-REPORT's Step 3 section. Not yet checked in the game: whether it reads clearly from the normal camera, stairs and ledges, and whether it suddenly vanishes when the camera turns. Next: Step 4, tuning Effect A (the "grey cloud" look I want).

### 2026-11-11 to 2026-11-12 — A6 Step 4: tuning Effect A toward grey cloud puffs, and stopping at r1

- **Date and what I was working on:** 2026-11-11 to 2026-11-12. Tuning Effect A after I said the dust read as dots, not the grey cloud puffs I want.
- **I tried / expected:** I expected to change one number. Because the brief capped the dust at the ankle (0.10 m) with 5–10 cm quads, I first wrote a dated intent revision (6–8 neutral-grey puffs, 0.18–0.25 m, top edge ≤ 0.30 m, still visible at 0.7 s) and then ran the loop interactively.
- **What happened:**
  - The agent took my "start" (meant as "start reading and proposing") as permission for everything: it changed the `Dust` quad 0.08 → 0.32 and the test's expected value, ran the test, and only then sent its reading and prediction (edit 07:56:36 UTC, prediction 07:57:19 UTC). It also read the prompt from `prompt-4-r1.txt` instead of my pasting it.
  - The test then failed one check, "Dust top 0.232 m ≤ 0.10 m". The agent left it failing on purpose, because the brief revision said the limit changes to 0.30 m only once the round is kept.
  - r1: bigger and longer-lasting puffs (frame 30 still visible), but they read as a broken ring of warm smudges around the feet, cut flat by the floor and partly hidden by the capsule.
- **What I did:** approved the change after the fact and recorded that in TUNING; kept r1 after looking in the game; raised the test's height limit to 0.30 m with a dated brief revision; stopped tuning Effect A at r1 ("what lands is a human, not a mech; the dust does not need to be big"); recorded where my verdict differs from Claude's reading (warm tint, capsule hiding, puffs not separate, flat bottoms); moved the colour intent back to "low-saturation, slightly warm grey" because I could not see the difference and Claude noted the warmth is what makes it visible on the grey-blue floor.
- **What Claude or another person contributed:** Claude Code (Opus 5.5, main session) wrote the intent revision from my answers, filled the Step 4 prompts, read the agent's transcript and caught the edit-before-approval, trimmed the strips, checked the agent's numbers, wrote and translated TUNING and the brief revisions, and committed. The reading, proposal, edit and comparison came from another Claude Code session (Opus 5.5).
- **What I understand now / still do not understand:**
- **Evidence and next step:** `CHANGE-BRIEF.md` revisions of 2026-11-11 and 2026-11-12; `TUNING.md` Effect A r1; `captures/landing_dust/r1/`; `prompt-4-r1.txt`, `prompt-4-r1-compare.txt`; commits e121aede, 9799850d, c1ef8d69, c8f2ab0c, 4fe7dbf4. Next: Effect B.

### 2026-11-12 — A6 Step 5: building Effect B, wiring it to the lights, one tuning round, and a redesign

- **Date and what I was working on:** 2026-11-12. The dust under ceiling light 1: build, look, wire, tune.
- **I tried / expected:** the same Steps 2–4 as Effect A.
- **What happened:**
  - Build: the agent built the scene, a configuration test (108 passed) and a preview. I ran it inside the same interactive window as Step 4, so there is no separate `session-5.jsonl`; the record is in that session's local transcript.
  - With F5 I saw no dust at all: the effect was not in the game yet, only in the preview. The preview turned the lights off after a moment, so I could not look long; Claude added a `hold` switch to the preview.
  - My first verdict: small is fine, but the specks should vary in size (I meant 0.003–0.03 m; my first wording "0.003 as the maximum" was ambiguous). A temporary look at 90 particles instead of 150: "At 150, anyone would think a nuclear war had broken out."
  - Wiring: the agent proposed first this time. Claude asked for three changes (no hard-coded amount in the state test, exactly one `restart()` per lights-on, a note that Effect A's preview now also shows the light dust). The agent also noticed the preview would show two copies of the dust and switched it to drive the real instance. State test 41 passed.
  - A recapture into `r0-wired/` produced no files at first: Movie Maker does not create missing folders and says nothing; Claude created them and I recaptured. r0-wired was pixel-identical to r0.
  - r1: amount 150 → 90, proposed and predicted by the agent, approved by me; the strip matched the prediction.
  - I then wanted the dust through the whole room and lit by the lights, and asked for it all at once. To keep the one-setting rule for tuning rounds, this became a dated brief redesign applied at once by Claude Code: box 14 × 2.6 × 9 m via `emission_shape_offset`, lit per pixel, specks 0.003–0.03 m, 3000 particles. Still too dense and too bright: I said "set it to 50" while it was 3000, which was ambiguous; I then chose 900 with half brightness, looked, and finally 1300.
- **What I did:** approved the wiring with changes, approved r1, decided every redesign value after looking in the game, and asked that the records be done only after I had seen the result.
- **What Claude or another person contributed:** The build, the wiring and r1's reading, proposal, edit and prediction were done by another Claude Code session (Opus 5.5) from my prompts and approvals. Claude Code (Opus 5.5, main session) reviewed each step, wrote the approval texts from my decisions, added the preview's `hold` switch, made the temporary 90 look, applied the redesign and its passes, updated the configuration test's expected values to the revised brief, reran every test after each change, compared r1 with the prediction, and wrote and translated the brief, TUNING and TEST-REPORT entries.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `godot/effects/light_dust.tscn`, `light_dust_listener.gd`, `godot/tests/test_light_dust_config.gd`, `test_light_dust_state.gd`, `godot/previews/light_dust_preview.*`; `prompt-5.txt`, `prompt-5-wire.txt`, `approve-5-wire.txt`, `prompt-5-r1.txt`, `prompt-5-r1-compare.txt`; `captures/light_dust/r0/`, `r0-wired/`, `r1/`, `redesign/`, `redesign-2/`; CHANGE-BRIEF revisions of 2026-11-12; TUNING Effect B. Next: Step 6.

### 2026-11-12 — A6 Steps 6 and 7, and Use It: the process shader, the headless price, my playtest and the GPU price

- **Date and what I was working on:** 2026-11-12. Reading the generated process shader, pricing both effects, and checking them in the running game.
- **I tried / expected:** a quick editor conversion, an agent-written cost script, and a GPU reading in the Visual Profiler.
- **What happened:**
  - Step 6: at first the editor's FileSystem dock did not show `effects/light_dust.tscn` (two editors were open on the same project); after closing one and looking in the `effects` folder I found it, converted a unique copy of Effect B's process material, and saved `godot/shaders/particles_generated.gdshader`.
  - Step 7: the agent's script measured an empty scene 0.004 ms, the game scene 0.311 ms, Effect A 0.317 ms, Effect B 0.336 ms and an added 10,000-CPU-particle control 1.88 ms per frame. The control shows the script is not measuring itself; both GPU effects are within the noise, as expected headless.
  - Use It: my first written observations were hedged ("should"), and Claude took them for predictions; they were what I saw by eye, phrased with my usual uncertainty, and are recorded as observations with that note. I raised that Effect A's `visibility_aabb` was not enlarged with its quads; Claude's numbers confirmed it (top 0.23 m and 0.68 m out against a 0.2 m / 0.6 m box), so it is a known limitation and the next step.
  - The vsync key F10 did nothing (on Windows F10 is the system menu key); it was moved to V. With V, FPS went from 144 to about 1350.
  - The Visual Profiler graph mixed the lights going on and off with the effects, so Claude wrote `godot/debug/gpu_price.gd` to read the same engine GPU timing with only the effect changing: Effect B +0.017 ms, Effect A +0.001 ms GPU, both inside budget.
- **What I did:** made the shader conversion and answered the shader question in my own words; played and wrote down what I saw; took the profiler screenshot and the FPS reading; ran the GPU helper.
- **What Claude or another person contributed:** Claude Code (Opus 5.5, main session) wrote the Step 7 prompt (the assignment text) and checked the agent's result; found the shader line numbers and explained them; wrote the vsync key and the GPU helper; ran the helper twice to read the numbers (I had run it once, but its output was in my own terminal); and wrote and translated the TEST-REPORT sections. The cost script was written by another Claude Code session (Opus 5.5).
- **What I understand now / still do not understand:**
- **Evidence and next step:** `godot/shaders/particles_generated.gdshader` (5e977e83); TEST-REPORT "The process shader", "Headless CPU price", "Use It", "GPU price and FPS"; `godot/tests/cost_effects.gd`, `logs/cost_effects_60fps.log`, `prompt-7.txt`; `godot/debug/vsync_toggle.gd`, `godot/debug/gpu_price.gd`, `logs/gpu_price.log`. Next: README, the film, the tag and the fresh-clone check.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-11-10 | Start Assignment 6: the Godot project as the A6 starting point (light switch, `CeilingLights`, on-screen tablet), the A6 `scripts/run-test.sh`, baseline logs (55 / 24×3 / 2 / 168 passed + 1 existing failure), the A5 CLAUDE.md copied unchanged, and SOURCES with the light switch's asset row |
| 2026-11-10 | Add the A6 CHANGE-BRIEF (both effects' intent, settings, rules, strip predictions, predicted failures, budgets and short answers), committed before the first agent prompt |
| 2026-11-10 | A6 Step 1: the agent's CLAUDE.md draft (unedited), prompt-1, the session transcript (local paths replaced), and my review (a separate commit) |
| 2026-11-10 | A6 Step 2: Effect A as built by the agent (scene, configuration test, preview scene; unedited), prompt-2, the session transcript (local paths replaced), the fixed seed on the preview's instance, the r0 strips, my first verdict and Claude's reading (TUNING), and the two mutations (TEST-REPORT) |
| 2026-11-11 | A6 Step 3: Effect A wired to the landing by the agent (`landed` signal, trigger script, state test; unedited), prompt-3 and the two approvals, the session transcripts and the implementation excerpt (local paths replaced), the CLAUDE.md headless-fact correction, TEST-REPORT's Step 3 section, and my "What I understand now" for Step 2 |
| 2026-11-12 | A6 Steps 4-7 and Use It: Effect A r1 (agent edit before my approval, approved afterwards; kept) and stop; Effect B build, preview hold switch, wiring with its listener and state test, r0-wired, r1 (amount 150 -> 90, kept), and the whole-room redesign (3000 -> 900 -> 1300, half brightness) with dated brief revisions; the generated process shader and my answer; the headless cost script; the vsync key V and the GPU helper; Use It observations and the GPU price; README, SOURCES, FRICTIONAL entries and the Step 4-5 session excerpt |

# FRICTIONAL — Assignment 6, walker-rudy

What I tried, what I expected, what happened, how I checked it, what I did about it, and what I learned, with my work and Claude's kept apart.

**How this file is written.** Claude Code drafts each entry from our Claude Code conversation, and I check it against what I actually did. Where I recorded no expectation or lesson, the entry says so instead of inventing one. Each entry says when it was written; entries written after the event are labelled as retrospective.

**Tools.** Claude Opus 5.5 in Claude Code (desktop app), Claude Code 2.1.310; Godot 4.7.2; macOS on an Apple M3.

---

## 2026-11-04 — Reading the assignment, and keeping to the 2D game

*Retrospective, written on 2026-11-04, from the conversation.*

- **Attempt (me):** I pasted the assignment and asked Claude, in Chinese, what it asks me to do step by step. Claude explained the steps.
- **My decision:** Assignment 5 is submitted. This assignment changes only my 2D game, so the 3D props scene from Assignment 3 is not copied into this folder.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude explained the assignment; I decided the scope.

## 2026-11-04 — Setup: the folder, the wrapper and the baselines

*Retrospective, written on 2026-11-04, from the conversation. Commits `e61e8025` and `47ce9e2d`.*

- **Attempt (Claude, at my request):**
  - Branched `shuai-z/assignment-6` from tag `a5`.
  - Copied `assignment-5/game` into `assignment-6/game/` with `git archive`, so only committed files came across: 142 files. After a headless import it did not differ from its source (`diff -rq`, ignoring `.godot/`).
  - Wrote this folder's `.gitignore`: it keeps the `.godot` cache out and lets the game's six `.wav` sound effects past the root `*.wav` rule.
  - At my request, committed `CLAUDE.md` empty, so that Step 1's scoped session writes it from nothing.
- **The wrapper (Claude):** the course's Assignment 6 `scripts/run-test.sh`, changed in four places listed at its top: `--path game`; a `.tscn` test runs as the scene; Godot is found off PATH; it runs from this folder.
- **Baselines (Claude), through the wrapper:** `checks.tscn` 141 PASS and 0 FAIL at 60 fps; `invulnerable_tint_checks.tscn` 15 PASS at 30, 60 and 144 fps; no `SHADER ERROR` or `SCRIPT ERROR`. Each log differs from Assignment 5's only in the random camera-shake offset and the ObjectDB leak warning at exit (`logs/`).
- **A false sentence in a commit message, caught before any push.** The first commit's message said I had reviewed the files before committing. I had read only Claude's summary. Claude amended the local commit (`8f59f3ef` became `e61e8025`) to say it was committed on my word.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude did the setup, the wrapper and the baselines; I asked for them and decided each commit.

## 2026-11-04 — Choosing the two effects, and the Compatibility probe

*Retrospective, written on 2026-11-04, from the conversation. The probe is commit `9e19fe47`.*

- **Attempt (me):** I asked Claude to choose Effect A, and asked for Effect B to be a trail behind Rudy when he runs.
- **Two blockers Claude found:**
  - **Effect A.** Claude's first candidate was a burst when a goblin is defeated. The goblins start 1,500 px or more apart and patrol 400 px, so no two ever come within about 1,100 px (`game/content/level_1/level_1.tscn:69-77`, `game/content/goblin/goblin.gd:27`). Two defeats inside one burst lifetime cannot happen in real play, so the retrigger rule could never be exercised. Rudy's `hit` cannot repeat that fast either, because of his 1.2 s invulnerability.
  - **Effect B.** Claude wrote a throwaway probe (`evidence/compat-probe/`) and ran it under both renderers. Under GL Compatibility, the game's renderer, a `GPUParticles2D` with `trail_enabled` drew nothing, and the engine warned `The Compatibility renderer does not support particle trails.` Under Forward+ the same emitter drew trails. Damping and a box emission shape worked under both.
- **A third finding:** `RenderingServer.viewport_get_measured_render_time_gpu()` read 0.0 ms under both renderers. So the Visual Profiler's GPU time may also be unreadable on this Mac.
- **A probe that proved nothing:** a turbulence emitter in the first version stayed at its origin under both renderers. Its settings were wrong, so it was dropped and the README says so.
- **My choice,** from the options Claude put to me: Effect A is sparks when the sword's hitbox goes live (cuts at least about 0.32 s apart, bursts living 0.45 s, so the retrigger rule is exercised). Effect B is a world-space dust trail, an ordinary emitter with `local_coords` off, as Chapter 9's Dodge the Creeps makes its trail. I kept the renderer, because switching it would change the whole game.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude found the blockers, wrote and ran the probe, and proposed the options; I chose the effects.

## 2026-11-04 — The change brief

*Retrospective, written on 2026-11-04, from the conversation. Commit `cc9f7195`.*

- **Attempt (me):** I asked Claude to draft the whole of CHANGE-BRIEF.md, as I do for course documents, with its authorship stated in the file.
- **The draft (Claude):** the state of the game with file and line references, a background luminance table, both effects' intent, settings and rules (A1-A5, B1-B5), the boundaries, the evidence split, frame-by-frame predictions for both strips, 13 predicted failures, the prices and budget, and the six short answers.
- **Corrected before I read it (Claude):** rechecking its own draft, Claude found two of its statements wrong and fixed them: the yellow sparks' contrast against the sky and the wheat (about 1.1:1 and 1.5:1, which is why each spark has a dark rim), and the goblins' spacing. It also printed every line the brief cites to check it.
- **Review (me):** I read the brief and said to commit it. The probe went in first, then the brief alone, before any Step 1 prompt.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude drafted the whole brief, including the predictions and short answers; I chose the effects, read it and approved the commit.

## 2026-11-04 — Step 1: the CLAUDE.md draft

*Written on 2026-11-04, from the conversation. Prompt `sessions/prompt-1.txt`; transcript `sessions/session-1.jsonl`; commit `998fd175`.*

- **The prompt (Claude):** the course's Step 1 prompt with this folder's paths (`game/` for `godot/`, this folder as the repository root), and "Write" for "Revise", because `CLAUDE.md` was empty. The `game/shaders/` rule is stated in the prompt instead of "keep the existing rule".
- **The command (Claude, at my request):** the course's read-only command, plus a deny rule on `game/shaders/` for Edit and Write written as an absolute path (`//Users/...`), because Assignment 5 found that an agent's `cd` re-anchors relative rules. `CLAUDECODE` was unset, because the run started inside another Claude Code session.
- **The run:**
  - It started at 21:04:12 EST and ended at 21:06:20 EST.
  - Its result event reads `"subtype":"success"`, `"is_error":false` and `"terminal_reason":"completed"`: 13 turns in 121 s, model `claude-opus-5-5`, Claude Code 2.1.310, `total_cost_usd` 1.16.
  - **Permission denials: 2.** Both were Bash commands that counted log lines with `grep -c` inside `$(...)`. The agent read the logs another way instead.
  - Its final reply was in Chinese; the file it wrote is in English.
- **Checks (Claude, in this conversation):**
  - A hash of every file in the folder before and after the run: only `CLAUDE.md` changed, apart from the transcript.
  - `git diff --stat game/shaders/ scripts/run-test.sh` printed nothing.
  - `CLAUDE.md` is 84 lines, byte-identical to its one Write. The first line is a heading, which is right because there is no `AGENTS.md`, and `@CHANGE-BRIEF.md` is on its own line.
  - The transcript holds no e-mail or account field.
  - Claude printed every line the draft cites.
- **Left for the review:** two imprecise references, 18 property names and the `godot` binary listed as unconfirmed, and the "Headless facts" block.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped `claude -p` session wrote `CLAUDE.md`. Claude, in this conversation, wrote the prompt, ran the session and checked it. I approved the commit of the unedited draft.

## 2026-11-04 — Step 1: reviewing the CLAUDE.md draft

*Written on 2026-11-04, from the conversation. The unedited draft is commit `998fd175`; the review is commit `a3242b9d`.*

- **Attempt (Claude, at my request):** check every reference and add the "Headless facts" block, confirmed on this machine.
- **The probe (Claude):** `evidence/headless-probe/probe_particles.gd`, in a throwaway Compatibility project, run headless at `--fixed-fps 60` and once in a window; then the Compatibility probe under Movie Maker with `--headless`. Logs: `logs/probe_particles_headless.log`, `logs/probe_particles_window.log`, `logs/probe_movie_headless.log`.
- **Two mistakes in Claude's probe, fixed before the logs were kept:**
  - The first run stopped at a parse error: Claude called `OS.get_current_rendering_driver_name()`, which is on `RenderingServer` in 4.7.2.
  - The first version hid the container after the burst had already finished, so "hidden: emitting false" said nothing about hiding. Claude restarted a burst before hiding it: hiding leaves `emitting` true.
- **What it found:**
  - Headless, the frame cannot be read back, and the error comes from the dummy renderer. In a window the same probe read back a frame with 2,653 particle pixels.
  - Node state is observable: a 0.45 s one-shot sent `finished` at frame 27 and showed `emitting` false by frame 28; `amount_ratio` reads back; a container's child count gives the instance count.
  - `capture_rect()` returned an empty rectangle headless, and also in a Compatibility window, where the particle buffer could not be read back. A test cannot use it.
  - Headless CPU time per frame: empty scene 0.0028 ms, 20,000 GPU particles 0.0040 ms, 20,000 CPU particles 0.74 ms.
  - Movie Maker under `--headless` crashed with signal 11 and wrote no frame.
  - Every name the brief uses exists in 4.7.2. **The surprise:** the Godot 3 names `initial_velocity`, `scale`, `damping` and `hue_variation` also exist, as editor-only `Vector2` ranges. A scene line `scale = 2.0` loads without an error and sets the scale to 0.
- **Changes to CLAUDE.md** (84 lines, now 91): three references corrected (`is_on_floor()` at `rudy.gd:298`; the music also runs while paused, `music.gd:40`; the "read back" claim replaced by the ClassDB result); the Headless facts block, with the claim that no GPU process runs marked as an inference; the Godot 3 names note; three settled items removed from Unconfirmed.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude did the review and wrote and ran the probe; I read the summary and approved the commit.

## 2026-11-04 — Revision 2 of the brief: Godot 3 names in a scene file

*Written on 2026-11-04, from the conversation. The commit that adds this file.*

- **Why:** the review's probe showed that failure 1 in the brief predicts the wrong result for `scale`. I asked Claude to add the revision and this file.
- **A second probe (Claude):** `evidence/headless-probe/probe_mutation.gd` loads scene files written with Godot 3 lines (`logs/probe_mutation.log`):
  - Godot saves `initial_velocity_min` before `initial_velocity_max`. So the brief's Step 2 mutation, renaming that line to `initial_velocity`, loads as 0 to 420 px/s, not as speed 0. With the lines the other way round it loads as 0 to 0.
  - `scale = 0.7` followed by `scale_max = 1.0` loads as 0 to 1.
  - `flag_disable_z` still sets `particle_flag_disable_z`, but `flag_align_y` is dropped and `particle_flag_align_y` stays false.
  - A `Particles2D` node with a `ParticlesMaterial` sub-resource loads as a `GPUParticles2D` with a `ParticleProcessMaterial`, its values kept.
  - None of these printed a warning or an error.
- **Changes:**
  - CHANGE-BRIEF.md gains Revision 2: the corrected failure 1, the new prediction for the Step 2 mutation (the configuration test fails on `initial_velocity_min`; on screen the burst looks almost the same), and two imprecise references from Revision 1 (`rudy.gd:215`; the music's `music.gd:40`). Revision 1 is unchanged.
  - CLAUDE.md gains one line under "Godot 4 names": the remapped class names and the dropped `flag_align_y`.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude wrote and ran the probe and drafted the revision, the CLAUDE.md line and this file; I asked for them and decided the commit.

## 2026-11-04 — Step 2: Effect A, its configuration test and its preview

*Written on 2026-11-04, from the conversation. Prompt `sessions/prompt-2.txt`; transcript `sessions/session-2.jsonl`; commit `ea4419ae`.*

- **The prompt (Claude):** the course's Step 2 prompt with this folder's paths and the effect's name, plus one sentence saying where the session may write.
- **The command (Claude, at my request):** `dontAsk`, as Assignment 5's implementation runs, with writes allowed only in `game/effects/`, `game/previews/` and `game/tests/test_slash_sparks_config.gd`; the wrapper under four spellings; a headless import; read-only `git`; an absolute deny rule on `game/shaders/`.
- **The run:** 22:06:55 to 22:10:38 EST: `success`, `is_error` false, `terminal_reason` completed, 19 turns, $1.53. **Permission denials: 3**: a chained read of several files, the wrapper with `; echo` after it (it then ran the wrapper alone), and its own headless run of the preview, which no rule allowed.
- **What it built:** the effect scene, a configuration test of 108 checks that also scans the scene text for Godot 3 names, and a preview over Level 1 with the bursts fired on frames 10 and 20. Its first test run hit a GDScript type-inference error in its own test, which it fixed.
- **Checks (Claude, in this conversation):**
  - Only the four new files, their logs and the transcript appeared; nothing existing changed; `game/shaders/` and the wrapper are untouched.
  - Every value in the effect scene matches the brief's table.
  - The configuration test passes at 30, 60 and 144 fps; `checks.tscn` still passes 141 (it now finds 83 `res://` paths, all present) and the tint test 15.
  - Claude ran the preview headless, which the session could not: Burst1 fired on frame 10 and Burst2 on frame 20.
- **Noted:** at zoom 1 the preview frames x 1240–3160, wider than the brief's x 1950–2450, so the frozen goblins and the sword pickup are in the picture.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped session wrote the effect, the test and the preview. Claude wrote the prompt, ran the session and checked it. I approved the commit of its files unedited.

## 2026-11-04 — Step 2: the first strip, my first look, and tuning round r1

*Written on 2026-11-04, from the conversation. The record of the round is `TUNING.md`, "Effect A, revision r1".*

- **The capture:** I asked Claude to run it. It ran the course's Movie Maker command in a window on my screen, into `captures/slash_sparks/r0/`. The 60 frames took 14 s to record, so the window played at about a seventh of real speed.
- **A command that failed:** when I ran the preview myself, Godot said `Invalid project path specified: "game"`. Claude had left the session's shell in `captures/slash_sparks/r0/` after listing the frames. Claude moved it back and played the preview for me three times at real speed instead (`--fixed-fps 30 --max-fps 30`).
- **My first look,** before Claude opened any frame: the sparks are too sparse, too few. Claude wrote it into `TUNING.md` in English, with my Chinese words beside it.
- **The round:** Claude read the six frames and agreed with me, proposed `Sparks` `amount` 14 → 28 with a prediction for each frame, and I approved it. Claude made only that change, moved the test's expected value, ran the test at 60, captured r1 and compared it with its prediction. Frames 10–15 matched; frames 20 and 30 showed more of the first burst than it predicted, and it wrote down why. I watched r1 three times at real speed and kept the change.
- **After the verdict (Claude):** the brief's Revision 3 records the new value and the new peak of 58 particles; only frames 10, 12, 15, 20, 30 and 50 of each strip are kept.
- **Still to do for Step 2:** the two mutations of the effect scene, recorded in TEST-REPORT.md.
- **Expected / learned:** none recorded.
- **Human / AI:** I judged the preview twice and approved the change. Claude ran the captures and the plays, read and compared the strips, made the change and drafted the records.

## 2026-11-04 — Step 2: the two mutations of Effect A

*Written on 2026-11-04, from the conversation. The results are in `TEST-REPORT.md`, "Mutations".*

- **Attempt (Claude, at my request):** the assignment's two mutations of `game/effects/slash_sparks.tscn`, one line each, each followed by the configuration test at 60 fps and a `git checkout` of the file.
- **Results:** the Godot 3 name (`initial_velocity_min` → `initial_velocity`) exited 1 with two failures, the text scan and the value; the changed value (`spread` 30 → 45, brief unchanged) exited 1 with one failure. The file's SHA-1 matched the committed one after each restore, and the test passed again.
- **The game check:** the effect is not in the game yet, so Claude captured the mutated preview in a window instead. The burst still fired and still read as a spray, with a few slow sparks left near the hitbox.
- **Logs:** the wrapper writes every run of the test to the same log, so Claude copied each mutation's log to its own name before restoring the file.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude ran the mutations, the capture and the checks, and drafted TEST-REPORT.md; I asked for them.

## 2026-11-04 — Step 3: the plan for wiring Effect A

*Written on 2026-11-04, from the conversation. Prompt `sessions/prompt-3.txt`; transcript `sessions/session-3.jsonl`; plan `sessions/plan-3.md`.*

- **The prompt (Claude):** the course's Step 3 prompt with `game/` paths, run in two invocations as in Assignment 5: this one asks for the plan only and says no file may change.
- **The command:** `dontAsk`, with Edit, Write and NotebookEdit disallowed, and Bash only for read-only `git` and `ls`.
- **The run:** 22:31:22 to 22:33:54 EST: `success`, `is_error` false, `terminal_reason` completed, 7 turns, $1.06, no permission denials. Only its transcript is new.
- **The plan:** a read-only driver after `Rudy` in `main.tscn` that starts a new `SlashSparks` on each tick the sword's hitbox goes live, a state test of 14 checks through the real game loop, and two optional mutations of the driver.
- **Checks (Claude):** the plan's key claim holds. `Shape.disabled` is written in Rudy's own `_physics_process` (`rudy.gd:223-229`), so only a driver after him sees the edge on the same tick. `checks.gd` only looks for the nodes it lists in `main.tscn` and counts only `FlyingGear` among Main's children, so two new nodes cannot break it.
- **My decisions:** I approved steps 1 to 4. The session wrote the plan in Chinese, and I asked for `sessions/plan-3.md` to be in English: it is Claude's translation, with a note saying so, and the original is in the transcript.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped session wrote the plan. Claude wrote the prompt, ran the session, checked the plan against the code and translated it. I approved the steps.

## 2026-11-04 — Step 3: the driver, the state test and its mutations

*Written on 2026-11-04, from the conversation. Prompt `sessions/prompt-3b.txt`; transcript `sessions/session-3b.jsonl`; results in `TEST-REPORT.md`, "Step 3".*

- **The prompt (Claude):** approves the plan's steps 1 to 4 unchanged, one step at a time with each diff, the course's rules for this step, and "Write your reports in English".
- **The command:** `dontAsk`, with writes allowed only to the four files the plan names, the wrapper under four spellings, a headless import, read-only `git` and `ls`, and an absolute deny rule on `game/shaders/`.
- **The run:** 22:41:43 to 22:48:43 EST: `success`, `is_error` false, `terminal_reason` completed, 49 turns, $2.27. **Permission denials: 2**: the wrapper with commands chained after it, and copying the two files to its scratchpad before the mutations. It restored them with Edit instead.
- **On the way:** a GDScript type-inference parse error in its test, and a detail line in S14 that printed values read after the resume. It fixed both without changing an assertion.
- **Checks (Claude, in this conversation):**
  - Only the four planned files and the logs changed; `game/shaders/` and the wrapper are untouched.
  - The driver is the plan's code with a doc comment. The test calls no driver function, and writes only Rudy's position and once his velocity, as `checks.gd` does.
  - After the mutations, both files hash to their step-1 blobs.
  - Claude's own rerun: the state test 14 of 14 at 60 fps, `checks.tscn` 141, the tint test 15 at 30, 60 and 144, the configuration test 108. A headless import made the two new `.uid` files.
  - The wrapper reuses one log name, so Claude copied the two mutation runs out of the transcript into `logs/mutation_driver_*_60fps.log`.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped session wrote the driver, the scene change and the test, and ran the mutations. Claude wrote the prompt, ran the session, checked it and drafted the report. I approved the plan.
- **Afterwards (me):** I played the game with the effect wired in and found no problem. I did not list which eye checks I made; TEST-REPORT.md says so.

## 2026-11-05 — Step 5: Effect B, its first strip, and tuning rounds r1 to r3

*Written on 2026-11-05, from the conversation. Prompt `sessions/prompt-4.txt`; transcript `sessions/session-4.jsonl`; commit `017e8a52`; the rounds are in `TUNING.md`, "Effect B, revision r1" to "r3".*

- **The build (Claude, at my request):** the course's Step 2 prompt with Step 5's changes, in a `dontAsk` session that could write only the four planned files: `success`, 12 turns, $1.13, no permission denials. Claude checked every value against the brief, reran every test, and ran the preview headless (emitting from frame 10 at x 1950 to frame 40 at x 2510). I approved the commit of its files unedited.
- **The capture and my first look:** Claude ran Movie Maker in a window into `captures/run_dust/r0/`, then played the preview for me six times at real speed. Before Claude opened a frame, I said I could not see the dust trail at all.
- **How Claude measured something I could not see:** it rendered the same preview with `RunDust` hidden, in a scratch copy of the game outside the repository, and compared each strip frame with it pixel by pixel. In r0 the dust changed only 136 pixels by 20 levels or more at frame 25. That method then gave each round's prediction a number to meet.
- **Three rounds,** each one change that I approved and kept after watching the new strip at real speed:
  - r1, a darker, more opaque `color_ramp`: I could see it, but it was not enough and not obvious enough;
  - r2, `amount` 20 → 40: the puffs joined into a band, but it stayed on the ground;
  - r3, `initial_velocity` 40/90 → 80/160: the band rises to about 58 px at its far end.

  Claude's predictions met their measured targets in all three rounds except one: r1's largest change was 87 levels against at least 90. Single frames came out shorter or lower than predicted in r1, r2 and r3, and `TUNING.md` says where and why.
- **After the verdict (Claude):** the brief's Revision 4 records all three changes, the new height and the new peak of 40 particles. Only frames 10, 13, 25, 40, 46 and 56 of each strip are kept.
- **Expected / learned:** none recorded.
- **Human / AI:** I judged every preview and approved every change. The scoped session built the effect. Claude ran the captures, the plays and the measurements, proposed and made each change, and drafted the records.

## 2026-11-05 — Step 5: wiring Effect B, its state test and its mutations

*Written on 2026-11-05, from the conversation. Prompts `sessions/prompt-5.txt` and `prompt-5b.txt`; transcripts `sessions/session-5.jsonl` and `session-5b.jsonl`; plan `sessions/plan-5.md`; results in `TEST-REPORT.md`, "Step 5".*

- **Why I asked:** I opened the game in Godot and found no dust. Claude showed that nothing in `main.tscn` or the driver referred to `RunDust` yet: Effect B had only been built and tuned in its preview, and wiring it in was the step still to do.
- **The plan (Claude's prompt, a read-only session):** the course's Step 3 prompt with Step 5's four test rules, asking for English: `success`, 8 turns, $1.21, no permission denials, nothing changed. The plan puts `RunDust` in a `DustTrail` node before `Rudy`, so it draws behind him, and lets the existing driver, after Rudy, place it and switch it on the same tick. Claude checked that ordering, and the input actions the test would use, against the code, and added one warning of its own: a teleport while emitting could draw a streak, which only the eye can check. I approved every step, including the optional knockback and respawn checks and the two driver mutations.
- **The implementation:** `dontAsk`, writes allowed only to the four planned files: `success`, 53 turns, $2.63, two permission denials (a Python edit through Bash, and a `git diff` piped into `sed`). The session fixed two counting mistakes in its own test without weakening an assertion, and said that it had first written two step-3b checks into step 3 before taking them out again.
- **Checks (Claude, in this conversation):** only the four planned files and the logs changed; the driver and `main.tscn` are as planned; the test calls no driver function and writes only the one planned teleport and the two `visible` flags. Claude reran every test, made the `.uid` with a headless import, and copied the two driver mutation runs out of the transcript into their own logs.
- **A step that had been missed:** Step 5 repeats Step 2's mutations for Effect B, and they had not been done. Claude ran them after the wiring: a Godot 3 name and a changed value in `run_dust.tscn` each failed the configuration test, and the mutated trail still emitted in a window.
- **Expected / learned:** none recorded.
- **Human / AI:** I found the missing dust in the game and approved the plan. The scoped sessions wrote the plan, the driver change, the scene change and the test. Claude wrote the prompts, ran the sessions, checked them, ran B's scene mutations and drafted the report.
- **Afterwards (me):** I played the game and checked the items Claude listed (Esc while running, running while invulnerable, a respawn while holding a direction, how the dust reads); no problem.

## 2026-11-05 — Step 6: the process shader

*Written on 2026-11-05, from the conversation. Commit `8b795772`; my reading is in `TEST-REPORT.md`, "The process shader".*

- **Attempt (me):** after Claude described the steps, I opened the game in the editor, copied `Sparks`' `ParticleProcessMaterial` from `slash_sparks.tscn` into an unsaved scratch scene, made it unique, converted it to a `ShaderMaterial` and saved the code as `game/shaders/particles_generated.gdshader`. I then wrote the line references and my answer in TEST-REPORT.md.
- **Checks (Claude):** only the shader and its `.uid` were new, and no effect scene had changed; every test still passed, with no `SHADER ERROR`. Claude printed each line the section cites, with its surrounding code, and found each one says what the section says. It did not edit the shader or the answers.
- **My question:** I asked whether this assignment had changed anything outside the assignment-6 folder. Claude checked the 22 commits since `a5`, the working tree and every file's modification time: nothing in the repository outside the folder. Outside the repository there are only files that tools write for themselves: Godot's logs and editor settings, one `saved_order.tres` that a probe wrote to its own `user://` folder, Claude's transcripts and memory, and scratch folders.
- **Expected / learned:** none recorded.
- **Human / AI:** I generated the shader and wrote the section. Claude described the editor steps and checked the result.

## 2026-11-05 — Step 7: the headless price

*Written on 2026-11-05, from the conversation. Prompt `sessions/prompt-6.txt`; transcript `sessions/session-6.jsonl`; results in `TEST-REPORT.md`, "Step 7".*

- **The prompt (Claude):** the course's Step 7 prompt with `game/` paths, plus where to read the chapter's script (`git show upstream/main:…`), since Example 09 is not in this folder.
- **The command:** `dontAsk`, with writes allowed only to `game/tests/cost_effects.gd`, the wrapper, a headless import, `git show upstream/main:` and read-only `git` and `ls`, and an absolute deny rule on `game/shaders/`.
- **The run:** 19:38:02 to 19:41:11 EST: `success`, `is_error` false, `terminal_reason` completed, 19 turns, $1.14, no permission denials. Its first run failed because a `--script` test is compiled before the game's autoloads exist; it then loaded the game's scripts at run time instead.
- **What it measured:** an empty scene 0.0038 ms per frame; the game with both effects off about 0.05 ms; Effect A at 2 bursts +0.008 ms and Effect B +0.004 ms over their controls, both inside the spread between rounds. It added a fifth case, the game running with the effects off, as B's fair control.
- **Checks (Claude):** only the script and its log were new. Claude ran it again: the same picture, with differences of +0.006 and +0.002 ms (`logs/cost_effects_60fps_rerun.log`).
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped session wrote and ran the script. Claude wrote the prompt, ran the session, reran the script and drafted the report.

## 2026-11-05 — The F9 vsync key

*Written on 2026-11-06, from the conversation. Commit `d60fb037`; check in `evidence/vsync-check/`.*

- **Attempt (Claude, at my request):** the debug key the brief planned for the GPU price. `game/app/vsync_debug.gd`, on a new `VsyncDebug` node last in `main.tscn`, follows the assignment's example; no project setting, input action or `system_keys.gd` changed, and no action used F9 before.
- **Checks (Claude):** every test still passed. A headless run has no window, so Claude ran the real `Main` in a window from a scratch copy of the game and pressed F9 with injected key events: about 120 FPS with vsync on, 579 with it off, on again after a second press. The display reported 60 Hz yet vsync held about 120 FPS; that was noted, not explained.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude wrote the node and the check; I asked for them and approved the commit.

## 2026-11-06 — Use It: the GPU price and the checks in play

*Written on 2026-11-06, from the conversation. Results in `TEST-REPORT.md`, "Use It"; evidence in `evidence/use-it-code/`.*

- **Attempt (me, with Codex):** after Claude described each check, I had Codex record them. Codex wrote a temporary editor plugin in a scratch copy of the game that started the real Visual Profiler, read its and the Monitors' cells, drove the real `Main` through the game's input actions, turned vsync off with F9 and saved screenshots and logs. Its first two attempts (an embedded game window, and `--editor --script`) failed and were dropped; its README says so.
- **What it found:** the Visual Profiler's GPU column read 0.0 ms in all four states, the brief's predicted failure 12, so the 0.25 ms budget cannot be evaluated on this machine. With vsync off, FPS ranged from 239 to 438 and stayed above the reported 60 Hz. The captures showed no fault in the in-play, background, edge, pause, respawn and load checks.
- **Checks (Claude):** every file the folder's README cites exists; all 168 files in `game/` still match its `source-hashes.json`; its runtime logs have no `SCRIPT ERROR` or `SHADER ERROR`; one profiler screenshot shows the GPU column at 0.0 ms beside non-zero CPU times. The plugin's own `plugin.cfg` names Codex as its author, and Claude asked me who made the evidence before writing it up.
- **My own play:** the folder's README claims no human judgement, and the course requires my own playtest. Asked, I confirmed that I had played the game myself and found the size of both effects and the control feel fine.
- **Expected / learned:** none recorded.
- **Human / AI:** I decided what to measure, had Codex record it, reviewed it, and played the game myself. Codex wrote and ran the instrument. Claude described the checks, checked the evidence and drafted the report.

## 2026-11-07 — Ship It: the film

*Written on 2026-11-07, from the conversation. The film's records are in `youtube/claude-liam-walker-rudy-particles/`.*

- **Attempt (Claude, at my request):** I asked for the film as the assignment requires ("接下来按照作业要求做影片"). Claude followed the course's `godot-gamedev` skill with the `walker` modifier, adapting the Assignment 5 film's tools.
- **The capture:** a film-only input driver on a scratch copy of `game/` recorded the real `Main` with Movie Maker at 3840 × 2160 and 30 fps: fast cuts, cuts facing left, a cut at the top of a jump, a cut that defeats a goblin, running, jumping, stopping, and Esc during both effects. A headless dry run checked the route first; its first version left Rudy waiting 4.5 s for the second goblin, so the order changed. Claude checked by pixel that the log's frame numbers are the video's.
- **The film:** 33 beats, 12:22, narrated by Liam (local Kokoro). Every code excerpt is followed by its result; the strips are labelled as fixtures, the replays and enlargements as such, and Codex's captures as Codex's.
- **Checks (Claude):** the course checker passed (7 code → result pairs); Gate T failed on three code panels' footers and passed after they were shortened; Gate V found no defect; Claude's own frame review found one card whose notes overlapped its captions and that named the wrong commit, both fixed before the final master. Loudness −24.5 LUFS. Claude sampled frames and measured the audio; it did not watch or listen to the whole film.
- **My check:** I watched the film and found no problem ("影片看过了，没问题"), and uploaded the master to the course media storage: [claude-liam-walker-rudy-particles.mp4 on Google Drive](https://drive.google.com/file/d/1qAWW-L9Z0K5cUQ3Nql18tFhFgYpp4KuR/view?usp=sharing). Its SHA-256 is in the film folder's README.
- **Expected / learned:** none recorded.
- **Human / AI:** I asked for the film, watched it and uploaded it. Claude wrote the driver, the beat sheet and narration, the stills and records, and built and checked the film.

## 2026-11-07 — A last look at Effect A, and looking back on the tuning

*Retrospective, written on 2026-11-07. The check and the lesson are in my words; Claude translated them and added the pointers.*

- **Why:** checking the work against the assignment, Claude found that Effect A over the sky and the pit, the screen edges and the first frames after loading were recorded only from Codex's captures, not from my own eyes, and asked me to look.
- **What I said:** when attacking, there are clearly visible sparks [攻击时，有明显的火花]. I did not say which of those places I looked at. TEST-REPORT.md, "Use It", records it with that limit.
- **What I learned:** an effect needs several rounds of adjustment; there is no way to reach the ideal look at the start [effect需要多轮调整，没有办法在一开始就做到理想的效果]. Effect A took one round after its first strip (`TUNING.md`, "Effect A, revision r1"); Effect B took three, from a first strip in which I could not see the dust at all (`TUNING.md`, "Effect B, revision r1" to "r3").
- **Human / AI:** the check and the lesson are mine. Claude asked for the check, and wrote both down.

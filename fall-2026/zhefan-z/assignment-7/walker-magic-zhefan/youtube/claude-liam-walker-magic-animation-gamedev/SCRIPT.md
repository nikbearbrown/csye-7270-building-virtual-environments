# SCRIPT — walker-magic Assignment 7 gamedev film (Brutalist `godot-gamedev` + `walker`)

> Narrator: Liam, in for Bear (local Kokoro `am_onyx`). Native 4K landscape, 30 fps. No burned captions. The final card is silent (this toolkit copy has no stock jingle, as in Assignments 1–6).
> Narration lines are written for the voice: numbers, names and commits are spelled the way they should be spoken. On-screen text keeps the exact spelling and figures of the source named on each card.
> Sources of truth: CHANGE-BRIEF.md (with its revisions, especially 2026-11-13, "the brief in the published structure"), TEST-REPORT.md, TUNING.md, FRICTIONAL.md, README.md, SUBMISSION.md, SOURCES.md, `assets/sprites/mage/ATTRIBUTION.md`, the clips in the scene files, the tests and their logs in `logs/`, `captures/` and `captures/figures/`, and `git log`. Where a document and a log disagree, the film shows the log (FACTCHECK.md, "Corrections"). Game source revision shown: ad7935f.
> Built to the published film requirements (`prompt-9-film.txt`, Part 2); the requirement each beat covers is listed in FACTCHECK.md, "Requirements".

Title: **Keys on the Tick: A Run Cycle and a Wolf Lunge**

Labels used on screen: **Reconstructed prompt** · **Suggested prompt** · **Scripted input · real engine output** (capture/run-02: the real main scene played by capture/driver.gd through key and mouse events; Movie Maker, windowed, 640×360 at 60 fps, one frame per physics tick; shown ×5 nearest neighbour) · **Real speed** · **Replay, ×0.25** · **Last frame held** · **Fixture capture** (the author's committed captures from the capture harnesses, which place the characters; not played gameplay) · **Godot editor reconstruction** (with path and lines) · **Source view — reconstruction, not a screenshot** (exact lines, file:line) · **The author's words** (quoted from CHANGE-BRIEF.md, translated from Chinese by the author) · **Recorded results — not a render** · **Figure from the logs** (`tools/make_figures.py`).

## B00 — Walker opening (Claude composer)
*On screen:* `ClaudeComposerAsk`, greeting "Jambo, Liam". Prompt (**Reconstructed prompt**): "Please use Walker to convert my game design document about a fire mage and a cave wolf into two animation clips: a run cycle that loops and a lunge that commits — each pinned first, keyed as data in the scene files, read back by tests and checked tick by tick against the game." Output lines: the two clips, the pin, the edges test (25 / 0).
*Narration:* "Jambo — this is Liam, in for Bear. The ask: two animation clips for a pixel-art mage and a cave wolf — a run that loops and a lunge that commits — keyed as data and checked tick by tick against the game."

## B01 — Hesitant-writer summary (window ≥ 9 s)
*On screen:* typed, "Two clips: / a run, a lunge. / Animation / is drawing." Correction (one word): "drawing" → "timing".
*Narration:* "Two clips: a run and a lunge. The lesson: animation here is timing, not drawing — keys on the physics tick the game reads, with gameplay pinned before the first key."

## B02 — The game and its two clips
*On screen:* **Fixture capture** — `captures/look/take_lunge_t40_now.png` (the game now); the brief's two-clips table (CHANGE-BRIEF revision 2026-11-13): route, object, cycle or committing, the commits that added them (`72e8d21` clips, `33d78ae` wired, `32eed66` run r2, `b1422ca` step).
*Narration:* "The game: walker-magic, a two-D side-scroller — a fire mage, a cave, a wolf. Two new clips. The mage's run is a Sprite2D frame track, and it loops. The wolf's lunge is a cutout rig keyed as resource text, and it commits: once the dash starts, a hit no longer cancels it."

## B03 — The run, in play
*On screen:* **Scripted input · real engine output** — capture/run-02 frames 15–439 at real speed; **Replay, ×0.25** of the jump and landing (frames 292–372); state chip from the frame log; **Last frame held**.
*Narration:* "Now the real game, played by scripted input — real key presses, real engine output. The mage runs, four cells at ten a second, stops, runs, jumps the pit and lands. At quarter speed: on the landing tick, the run starts again at cell zero."

## B04 — The lunge in both facings, in play
*On screen:* **Scripted input · real engine output** — frames 860–1088 at real speed; **Replay, ×0.25** of frames 876–1030 (both lunges); state chip; **Last frame held**.
*Narration:* "The wolf. It growls where it first sees her, crouching for thirty-one ticks; she steps back, and the lunge misses, trailing orange ghosts. She runs past; it turns and lunges right. One clip, both facings: code flips the Facing node, the clip keys the rig inside."

## B05 — A hit in the growl cancels the lunge
*On screen:* **Scripted input · real engine output** — frames 1380–1619 at real speed; **Replay, ×0.25** of frames 1518–1600; state chip; **Last frame held**.
*Narration:* "Now an interrupt in each phase, from real clicks. First, the growl: the fireball leaves on growl tick two and lands on tick twenty-one. The lunge is cancelled — recovery on the hit tick, clip frame fifty-three, and the hitbox never arms."

## B06 — A hit in the lunge does not cancel
*On screen:* **Scripted input · real engine output** — frames 1930–2148 at real speed; **Replay, ×0.25** of frames 2058–2148; state chip; **Last frame held**.
*Narration:* "Second, the lunge. A click on growl tick sixteen; the fireball lands four ticks into the dash, at clip frame thirty-five. The wolf flashes and loses HP, but the dash runs its full twenty-two ticks, and recovery starts at fifty-three as usual."

## B07 — A hit in the recovery: HP only
*On screen:* **Scripted input · real engine output** — frames 2500–2706 at real speed; **Replay, ×0.25** of frames 2616–2706; state chip; **Last frame held**.
*Narration:* "Third, the recovery: a click during the dash, a hit on recovery tick five, clip frame fifty-eight. Only HP changes; the wolf still stands all thirty-six ticks. Every phase here is read from the frame log, not by eye."

## B08 — Idea 1: what a clip is
*On screen:* **The author's words** — CHANGE-BRIEF.md:197 (the four ideas, first sentence); **Source view**: `features/player/player.tscn:95` (`tracks/2/path = NodePath("Sprite2D:frame")`), `:99` (the key times), and `tests/anim_checks.gd:32–33` (the published `track_problems()` property check); **The author's note** — CHANGE-BRIEF.md:201 (dated 2026-11-13, in the working tree after ad7935f): the "skipped with no error" half is "my understanding, not a measurement"; what was measured is that the read-back catches it (M1 and the earlier a7-4, exit 1).
*Narration:* "Idea one, in the author's words: a clip is a timeline of keys on named node properties; a track resolves its target from a NodePath string at run time — here, Sprite2D colon frame. That a wrong path is skipped with no error is, in the author's own note, an understanding, not a measurement. What was measured: the read-back catches it."

## B09 — Clip 1: the sheet and its slicing
*On screen:* card: `assets/sprites/mage/mage_run_cycle_sheet.png` (248×69) enlarged and sliced 62×69, 4 × 1, order 0 contact, 1 down, 2 passing, 3 up; **Source view** `player.tscn:64–67` (`resource_name = "run"`, `length = 0.4`, `loop_mode = 1`, `step = 0.1`) and `:90` (`hframes` 4); provenance from ATTRIBUTION.md.
*Narration:* "The sheet that track reads: four cells of sixty-two by sixty-nine, four by one — contact, down, passing, up. Drawn in the Gemini app from the author's prompt and own sprite, then cleaned onto the author's palette."

## B10 — The frame track that reads it (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/player/player.tscn` lines 92–103 (the `Sprite2D:frame` track); notes: line 67 `step = 0.1`; lines 65–66 `length = 0.4`, `loop_mode = 1`.
*Narration:* "The frame track: discrete, cells zero to three at zero, point one, point two and point three seconds, looping at point four. Step: point one, ten frames a second. No duplicate across the wrap; the last gap equals the others."

## B11 — The run, cell by cell (result)
*On screen:* **Scripted input · real engine output** — crops of capture/run-02 frames 20–44, each labelled with the sheet cell from the frame log; ticks per cell in this capture and in `captures/run/game-r2-ticks/ticks.jsonl`; `test_clip_run.gd` 17 / 0.
*Narration:* "Tick by tick, in the capture: six, six, six, seven ticks per cell on entry, then five, six, six, seven each loop — the clip wraps on the tick it reaches point four. The read-back: seventeen of seventeen."

## B12 — Idea 2: one authority
*On screen:* **The author's words** — CHANGE-BRIEF.md:197 (second sentence); **Source view**: `features/player/player.gd:147` (`_play(CLIPS[next])`), `:148` (`sprite.flip_h = facing < 0`), `:153–154` (`anim.play(clip)`, `anim.seek(0.0, true)`) and `tests/test_anim_structure.gd:236` (the source-scan check).
*Narration:* "Idea two, in the author's words: one authority means each animated property is written by exactly one player; with two, they overwrite each other every frame and the picture twitches or falls out of step. Here, the state machine only calls play, and a test scans every script for other writers."

## B13 — Land, run, cell zero (result)
*On screen:* **Scripted input · real engine output** — crops of capture/run-02 frames 340–351 around the landing (FALL → RUN at frame 346, cell 0); `test_anim_structure.gd` 11 / 0; the edges check "run → jump → land → run restarts at frame 0".
*Narration:* "In the capture: falling, then on the landing tick, run — from cell zero, not wherever the last run left off. Eleven structure checks agree."

## B14 — Idea 4: feel designed in frames — the phase table
*On screen:* **The author's words** — CHANGE-BRIEF.md:197 (fourth sentence); the phase table of CHANGE-BRIEF.md:163–167 (Phase · Frames · What the player may do · What the game reads), beside the key times built from it (frames 0, 25, 31, 37, 53, 65, 89 → seconds) and `wolf.tscn:64` (`step = 0.016666666666666666`).
*Narration:* "Idea four, in the author's words: designing feel in frames means splitting an action into startup, active and recovery frame counts, not by dragging keys by eye. Startup, the growl, frames zero to thirty: hitbox off, and a hit cancels. Active, the lunge, thirty-one to fifty-two: the game reads the hitbox; dodge — a hit doesn't cancel. Recovery, fifty-three to eighty-eight: the wolf stands; punish freely."

## B15 — The keys built from it (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/wolf/wolf.tscn` lines 101–112 (the `Facing/Rig:scale` track); notes: line 64 `step` = 1/60; key frames ÷ 60.
*Narration:* "In the scene file, the keys built from that table: frames zero, twenty-five, thirty-one, thirty-seven, fifty-three, sixty-five and eighty-nine, each over sixty — crouch, stretch, overshoot. The clip's step is one sixtieth of a second."

## B16 — Each boundary, in a strip and in play (result)
*On screen:* **Fixture capture** — `captures/lunge/game-r0/take_lunge_g+00, +31, +53, +89.png` (a harness places the characters; its overlay and collision shapes are on); **Scripted input · real engine output** — capture/run-02 frames 880, 911, 933, 969 (the first lunge of B04: GROWL tick 0, LUNGE 31, RECOVER 53, PATROL 89 ticks after the growl), crops; `test_clip_lunge.gd` 18 / 0.
*Narration:* "At each phase boundary, in a fixture strip and in play: neutral at zero, the crouch held at thirty-one, the stretch held at fifty-three, and back to patrol at eighty-nine. The read-back: eighteen of eighteen — every track resolves, every key within half a frame."

## B17 — Idea 3: two clocks, measured
*On screen:* **The author's words** — CHANGE-BRIEF.md:197 (third sentence); **Source view**: `wolf.tscn:251–252` (`process_physics_priority = -1`, `callback_mode_process = 0`), `wolf.gd:89` (the hitbox read in the LUNGE branch), `wolf.gd:121` (`set_deferred`); **Recorded results** from `logs/probe_two_clocks_{30,60,144}fps.log`.
*Narration:* "Idea three, in the author's words: the two clocks are the variable-rate process clock and the fixed-step physics clock; my state machines, the hitbox and both clip players run on the physics clock. Measured: clip time equals phase time on all eighty-nine ticks — but the hitbox is read one tick late, frames thirty-two to fifty-three against thirty-one to fifty-two. A sixtieth of a second."

## B18 — The change (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/wolf/wolf.gd` lines 152–163 (`take_damage()`).
*Narration:* "The one behaviour change, in code: a hit that leaves HP during the growl sends the wolf to recover and seeks the clip to the recovery section. Every other phase only loses HP."

## B19 — What the pin saw (result)
*On screen:* **Figure from the logs** — `captures/figures/pin_timeline.png` (`hit_growl` before `a9b4bc1` and after `ff71bbb`); the commit sequence: pin `a9b4bc1` → clips `72e8d21` (unchanged) → wired `33d78ae` (unchanged) → change `72f37b8` → play → re-pin `ff71bbb`.
*Narration:* "Gameplay was pinned before any clip: eight scenarios, every tick, three rates; adding and wiring the clips changed nothing. This change did, from tick twenty-four: growl to recover, no lunge. Kill changed too; its first hit lands in a growl. Played, accepted, re-pinned."

## B20 — Edges: before, on and after every boundary
*On screen:* **Recorded results — not a render** · `logs/test_anim_edges_{30,60,144}fps.log`: the boundary grid (0, 31, 53, 89 × one tick before, on, after) with the hit tick and the outcome; kills in each phase, Esc mid-lunge, run re-entry, clip frame = phase tick on 119 ticks; 25 / 0 at 30, 60, 144.
*Narration:* "The edges: real clicks timed to land one tick before, on, and after every phase boundary. A hit on a boundary is handled before the wolf's update, so it follows the phase before. Cancel in the growl, none in the lunge, HP only after. Twenty-five of twenty-five, at three rates."

## B21 — Broken on purpose: M1 to M4
*On screen:* **Recorded results — not a render** · `logs/mutation-a7-M*_60fps.log`: M1 lunge property renamed (18 checks / 3 failures; "lunge track 4: FrontPivot has no property rotaton"), M2 run `LOOP_NONE` (17 / 2), M3 run frame key 4 (17 / 2), M4 `.godot` deleted and reimported (17 / 0, 18 / 0, 12 / 0, 11 / 0); exit 1 for M1–M3 (TEST-REPORT.md); the five earlier logs `mutation-a7-1…5` noted.
*Narration:* "Broken on purpose: four published mutations, each in a worktree. A misspelt property on a lunge track: exit one — track problems reports FrontPivot has no property rotaton. The run's loop set to none: exit one. A frame key past the sheet: exit one. The import cache deleted and rebuilt: every read-back passes, proving only that the clips don't depend on it."

## B22 — What the read-backs proved, and what no headless run shows
*On screen:* **Recorded results** — read-backs at 60 fps: `test_clip_run` 17 / 0, `test_clip_lunge` 18 / 0, `test_clip_flicker` 12 / 0, `test_anim_structure` 11 / 0, with what each checks (TEST-REPORT.md "Read-back"); **TEST-REPORT.md "What no headless run shows"**, quoted.
*Narration:* "The read-backs proved structure: run seventeen, lunge eighteen, flicker twelve, structure eleven, no failures — tracks resolve, keys within half a frame, step and modes as the brief says. What no headless run shows: whether either motion reads or feels committed, or whether the cycle wraps cleanly to the eye. That took the author, in play."

## B23 — Claude against the author
*On screen:* **Fixture capture** — `captures/run/analysis/run_r1_beats_vs_r0_6x.png`; TEST-REPORT.md "Claude against me" (the waist seam, run r1, the visual upgrades), TUNING.md verdicts; FRICTIONAL.md "Process slips".
*Narration:* "Claude against the author. Claude estimated a two-point-six to three-point-three pixel step at the waist seam; the author saw none. Claude's run r1 hit every predicted hat row; the author rejected it in play. Claude read the visual upgrades as matching; the author found them not noticeable. And the slips the author recorded: an amended local commit, and a backup kept one folder above the assignment for a few seconds."

## B24 — What remains uncertain, and the next step
*On screen:* card: README.md "Known limitations", SUBMISSION.md "Known limitations", what this film could not confirm (a fresh clone of the submitted commit, which comes after this film; the four-ideas claim about a broken path, the author's understanding by the author's own note), and the next step in the author's words (FRICTIONAL.md: "The next test is in-betweens for the planted foot, in the final project").
*Narration:* "Still uncertain: the planted foot slides; the growl window is a fifth of a second, by choice; the hitbox is read a sixtieth late; and a fresh clone of the submitted commit can only come after this film. The author's next step: in-betweens for the planted foot, in the final project."

## B25 — Who did what; the sheet's terms; the revision shown
*On screen:* card: FRICTIONAL.md "Human and AI contributions" and the SUBMISSION.md summary; the sheet's source and terms (ATTRIBUTION.md: Gemini app, model shown as "4 Hydrogen", 2026-11-12, prompt v3, Google Terms of Service and Generative AI Additional Terms of Service, original in `design/a7/`); game source revision ad7935f.
*Narration:* "Who did what. The author chose both clips, the interrupt rule and the window, made the run sheet in the Gemini app — model shown as 4 Hydrogen, under Google's terms — and judged everything in play. Claude Code built the pin, clips, tests, mutations and this film; Claude in chat drafted the documents. Source shown: a d seven nine three five f."

## B26 — Verdict
*On screen:* `ClaudeVerdictArtifact` — Built · Measured · Judged · Open.
*Narration:* "The verdict. Built: two clips, each owned by one animation player on the physics tick, and one designed interrupt. Measured: a pin the clips never moved, edges at every boundary, three mutations caught. Judged in play by the author. Open: the sliding foot."

## B27 — Your Turn
*On screen:* `ClaudeComposerAsk`, greeting "Your turn.", **Suggested prompt**: "Please use Walker to add in-between frames to my mage's run so the planted foot stops sliding. First predict, in pixels, how far the body moves while one cell is held at 110 px/s and 10 fps; then measure the foot in a windowed Movie Maker strip, and show the behaviour pin still matches tick for tick."
*Narration:* "Your turn. Here's a prompt: Please use Walker to add in-between frames to my mage's run so the planted foot stops sliding. First predict, in pixels, how far the body moves while one cell is held at a hundred and ten pixels a second and ten frames a second; then measure the foot in a windowed Movie Maker strip, and show the behaviour pin still matches tick for tick. Liam, in for Bear."

## B28 — Regular outro
*On screen:* `ClaudeTitleOutro` (locked): the title, @NikBearBrown, one slug-seeded mascot. Silent.

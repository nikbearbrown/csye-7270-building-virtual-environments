# SCRIPT — walker-magic Assignment 7 gamedev film (Brutalist `godot-gamedev` + `walker`)

> Narrator: Liam, in for Bear (local Kokoro `am_onyx`). Native 4K landscape, 30 fps. No burned captions. The final card is silent (this toolkit copy has no stock jingle, as in Assignments 1–6).
> Narration lines are written for the voice: numbers, names and commits are spelled the way they should be spoken. On-screen text keeps the exact spelling and figures of the source named on each card.
> Sources of truth: CHANGE-BRIEF.md (with its revisions), TUNING.md, TEST-REPORT.md, FRICTIONAL.md, README.md, SOURCES.md, the clips in the scene files, the tests and their logs in `logs/`, `captures/` and `captures/figures/`, and `git log`. Where a document and a log disagree, the film shows the log (FACTCHECK.md, "Corrections"). Game source revision shown: f860fed.

Title: **Keys on the Tick: A Run Cycle and a Wolf Lunge**

Labels used on screen: **Reconstructed prompt** · **Suggested prompt** · **Scripted input · real engine output** (capture/run-01: the real main scene played by capture/driver.gd through key and mouse events; Movie Maker, windowed, 640×360 at 60 fps, one frame per physics tick; shown ×5 nearest neighbour) · **Real speed** · **Replay, ×0.25** · **Last frame held** · **Fixture capture** (the author's committed captures from the capture harnesses and preview scenes, which place the characters; not played gameplay) · **Godot editor reconstruction** (with path and lines) · **Source view — reconstruction, not a screenshot** · **Recorded results — not a render** · **Figure from the logs** (`tools/make_figures.py`).

## B00 — Walker opening (Claude composer)
*On screen:* `ClaudeComposerAsk`, greeting "Jambo, Liam". Prompt (**Reconstructed prompt**): "Please use Walker to convert my game design document about a fire mage and a cave wolf into two animation clips: a run cycle that loops and a lunge that commits — each pinned first, keyed as data in the scene files, read back by tests and checked tick by tick against the game." Output lines: the two clips, the pin, the edges test.
*Narration:* "Jambo — this is Liam, in for Bear. The ask: two animation clips for a pixel-art mage and a cave wolf — a run that loops and a lunge that commits — keyed as data and checked tick by tick against the game."

## B01 — Hesitant-writer summary (window ≥ 9 s)
*On screen:* typed, "Two clips: / a run, a lunge. / Animation / is drawing." Correction (one word): "drawing" → "timing".
*Narration:* "Two clips: a run and a lunge. The lesson: animation here is timing, not drawing — keys on the physics tick the game reads, with gameplay pinned before the first key."

## B02 — Before and after, the same tick
*On screen:* **Fixture capture** — `captures/look/before_after.png`: the pin scenario `take_lunge` at physics tick 40, before A7 (`2276069`) and now.
*Narration:* "The same scripted moment twice: the pin's take-lunge scenario at tick forty, before Assignment seven and now. Now a keyed rig stretches mid-lunge with an orange afterimage, in a torch-lit cave. Gameplay is identical on every tick."

## B03 — The run, in play (result of the brief's Clip 1)
*On screen:* **Scripted input · real engine output** — capture/run-01 frames 15–441 at real speed; **Replay, ×0.25** of the jump and landing (frames 292–372); **Last frame held**.
*Narration:* "Now the real game, played by scripted input — real key presses, real engine output. The mage runs, four cells at ten a second, stops, runs, jumps the pit and lands. At quarter speed: on the landing tick, the run starts again at cell zero."

## B04 — The lunge in both facings, in play
*On screen:* **Scripted input · real engine output** — frames 850–1090 at real speed; **Replay, ×0.25** of frames 876–1062 (both lunges); the wolf's state, its tick in that state and the clip frame, from the capture's frame log, in a chip under the game; **Last frame held**.
*Narration:* "The wolf. She stops where it first sees her; it growls, crouching, for thirty-one ticks. She steps back, so the lunge misses — a stretch and a dash, trailing orange ghosts. It recovers. She runs past; it growls again, turns to follow, and lunges right. This one hits. One clip, both facings: code flips the Facing node, the clip keys the rig inside."

## B05 — An early cast cancels the growl, in play
*On screen:* **Scripted input · real engine output** — frames 1380–1621 at real speed; **Replay, ×0.25** of frames 1522–1592; state chip from the frame log; **Last frame held**.
*Narration:* "The one behaviour change. The moment the wolf starts to growl, a click: the fireball leaves on growl tick two and lands on tick twenty-one. No lunge — the wolf goes straight to recovery, and its hitbox never arms."

## B06 — Clip 2: route and source
*On screen:* card: `assets/sprites/wolf/wolf_lunge.png` enlarged with the two `region_rect`s (Rear 0,0,40,40; Front 36,0,44,40) and the pivots (hip −11,−22; shoulder 15,−22) from `wolf.tscn`; the node path Facing → Rig → RearPivot / FrontPivot; Muybridge, *Animal Locomotion* plate 707 (dog galloping, 1887, public domain).
*Narration:* "Clip two is a cutout rig, not new art: two regions of the Assignment two wolf, overlapping at the waist, on a hip and a shoulder pivot. The motion reference: Muybridge's galloping dog."

## B07 — The phase table becomes keys (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/wolf/wolf.tscn` lines 99–110 (the `Facing/Rig:scale` track); notes: the measured phase table (31 / 22 / 36 ticks) and key frames 0, 25, 31, 37, 53, 65, 89 ÷ 60.
*Narration:* "The phase table came from the pin: growl thirty-one ticks, lunge twenty-two, recover thirty-six. The keys follow it, in frames over sixty. Here, the rig's scale: crouch, stretch, overshoot."

## B08 — Read back, and logged in the game (result)
*On screen:* **Fixture capture** — `captures/figures/lunge_onion.png` (rig values logged per tick in the game by `tests/capture_lunge.gd`, which places the mage), beside **Recorded results**: `test_clip_lunge.gd` 17 / 0, key times = frame/60 to 1e-6, length 89/60, `LOOP_NONE`.
*Narration:* "The read-back: every track resolves to a real node and property, and every key time equals its frame over sixty. Seventeen checks, zero failures. And in the game, the logged rig matched every key — here as an onion skin."

## B09 — Clip 1: route and source
*On screen:* card: `assets/sprites/mage/mage_run_cycle_sheet.png` (248×69, four cells of 62×69: contact, down, passing, up), enlarged, beside Muybridge plate 60 (a man running, 1887, public domain); provenance from SOURCES.md.
*Narration:* "Clip one, the run: a frame track over four cells — contact, down, passing, up — drawn by Gemini from the author's own sprite and cleaned onto the author's palette."

## B10 — The run clip (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/player/player.tscn` lines 93–101 (the `Sprite2D:frame` track); notes: lines 64–65 `length = 0.4`, `loop_mode = 1`; line 88 `hframes` 4.
*Narration:* "In the scene file: a discrete frame track — cells zero to three at zero, point one, point two and point three seconds — in a looping clip point four seconds long. No duplicate cell across the wrap; the last gap equals the others."

## B11 — The run, cell by cell (result)
*On screen:* **Scripted input · real engine output** — crops of capture/run-01 frames 20–44 (the first cycle after the start), each labelled with the sprite cell from the frame log; the ticks per cell measured in this capture and in `captures/run/game-r2-ticks/ticks.jsonl`; `test_clip_run.gd` 16 / 0.
*Narration:* "Tick by tick, in the capture: six, six, six, seven ticks per cell on entry, then five, six, six, seven each loop — the clip wraps on the tick it reaches point four. The read-back: sixteen of sixteen."

## B12 — One authority (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/player/player.gd` lines 143–154 (`_set_state()`, `_play()`); notes: `test_anim_structure.gd` scans every script for writes to a keyed property.
*Narration:* "One authority. The state machine only calls play: a state's clip starts when the state changes, from zero; flip h stays in code. A structure test scans every script: nothing else writes what a clip keys."

## B13 — Land, run, cell zero (result)
*On screen:* **Scripted input · real engine output** — crops of capture/run-01 frames 342–351 around the landing (FALL → RUN at frame 346, cell 0), labelled from the frame log; `test_anim_structure.gd` 11 / 0; the edges check "run → jump → land → run restarts at frame 0".
*Narration:* "In the capture: falling, then on the landing tick, run — from cell zero, not wherever the last run left off. Eleven structure checks agree."

## B14 — Pin first
*On screen:* card: the commit sequence from `git log` and TEST-REPORT.md: `2276069` baseline → `a9b4bc1` pin (8 scenarios, 16 / 0 at 30, 60, 144) → `72e8d21` clips, not wired: unchanged → `33d78ae` wired: unchanged → `72f37b8` the change: differs only in `hit_growl` and `kill` → play → `ff71bbb` re-pin.
*Narration:* "Pin first. Before any clip, a test recorded eight scripted scenarios, every physics tick, from real input, at three frame rates. Clips added: unchanged. Wired: unchanged. Then one change, in its own commit."

## B15 — The change (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/wolf/wolf.gd` lines 152–163 (`take_damage()`).
*Narration:* "Here it is: a hit that leaves HP during the growl sends the wolf to recover and seeks the clip to the recovery section. Every other phase only loses HP."

## B16 — What the pin saw (result)
*On screen:* **Figure from the logs** — `captures/figures/pin_timeline.png` (`hit_growl` before `a9b4bc1` and after `ff71bbb`); the re-pin: only `hit_growl.json` and `kill.json` changed (`git show --stat ff71bbb`).
*Narration:* "The pin saw it from tick twenty-four: growl to recover, no lunge. The brief expected only that scenario to change; kill changed too, since its first hit lands in a growl. Played, accepted, then re-pinned: two files, sixteen of sixteen at all three rates."

## B17 — Edges at the phase boundaries
*On screen:* **Recorded results — not a render** · `logs/test_anim_edges_{30,60,144}fps.log`: growl from tick 80, lunge 111, recover 133; the cases and results; 13 / 0 at 30, 60, 144.
*Narration:* "Then the edges: real clicks timed to land on a boundary. First or last growl tick: cancel. First or last lunge tick: no cancel. A killing hit wins everywhere. Thirteen of thirteen, at three rates."

## B18 — Two alignment bugs
*On screen:* **Source view — reconstruction**: `wolf.gd:162` (`anim.seek((RECOVER_FRAME - 1) / 60.0, true)`) and `wolf.tscn:248` (`process_physics_priority = -1`); CHANGE-BRIEF revision 2026-11-12 (two clip-alignment fixes); and in this film's capture: the cancel tick shows clip frame 53 (frame 1549), and a growl right after a one-tick patrol starts at clip frame 0 (frames 969–970).
*Narration:* "That found two bugs no read-back could see: a cancel drew clip frame fifty-four, so it now seeks fifty-two; and a growl after a one-tick patrol started at frame one, so both players now run first. This film's capture shows both fixes holding."

## B19 — Broken on purpose
*On screen:* **Recorded results — not a render** · `logs/mutation-a7-*_60fps.log`: a7-1 `loop = true` not caught (loads as `loop_mode` 1, still loops; 16 / 0); a7-2 continuous frame track (1 failure); a7-3 frame key 4 (2 failures); a7-4 missing node (2 failures); a7-5 growl cancel removed (2 failures; hitbox armed 23 ticks).
*Narration:* "Broken on purpose. Godot three's loop equals true: not caught — four point seven point two loads it as a looping clip anyway. A continuous frame track, a cell past the sheet, a missing node, no cancel: all caught."

## B20 — The growl window and a second clock
*On screen:* **Figure from the logs** — `captures/figures/growl_window.png` and `captures/figures/two_clocks.png`.
*Narration:* "Two findings, kept. From sight distance, only a cast in the first twelve growl ticks — a fifth of a second — can cancel. And a second clock: the dead wolf's removal runs on frame time — tick seventy-nine at sixty frames a second, eighty at thirty and one forty-four."

## B21 — The run, r0 and three dead ends
*On screen:* **Fixture capture** — `captures/run/game-r0/` and `captures/figures/run_cycle.png` (r0: two frames); TUNING.md r0: 1 px hat hop, the planted foot slides 13–15 px and snaps back; the failed attempts: `captures/run/analysis/contact_b_compare_8x.png` (Gemini contact B: 103 px differ, all in the trailing leg), leg mirroring, far-leg darkening (19 px).
*Narration:* "The run took longest. Version zero swapped two frames: a one-pixel hat hop while the planted foot slid thirteen to fifteen pixels and snapped back. Three fixes for the other foot failed."

## B22 — r1 rejected in play, r2 kept
*On screen:* **Fixture capture** — `captures/run/analysis/run_r1_beats_vs_r0_6x.png` (r1: hat rows 268 / 270 / 267 / 265, as predicted; reverted `338c8bf`) and `captures/figures/run_cycle.png` (r2: four frames, kept `32eed66`).
*Narration:* "Version one bobbed the body; every hat row landed exactly as predicted, and the author rejected it in play anyway. A correct prediction isn't a good result. Version two, a real four-frame cycle, was kept."

## B23 — Beyond the requirements: the torches (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `effects/cave_lights.tscn` lines 19–30 (the `flicker` clip and its `TorchLeft:energy` track); notes: lines 75–89 the two PointLight2D nodes, energy 1.6 and 1.5; line 95 `autoplay = &"flicker"`.
*Narration:* "Beyond the requirements: the torches flicker on a third clip — continuous tracks on energy and size, two point four seconds, looping. Its seam: the value at zero equals the value at the end."

## B24 — The flicker, measured in the capture (result)
*On screen:* **Scripted input · real engine output** — the mean brightness of the left torch's pool (screen 40–120 × 110–190) in capture/run-01 frames 0–441, plotted against the clip's `TorchLeft:energy` keys (correlation 0.95); three crops; `test_clip_flicker.gd` 11 / 0.
*Narration:* "Measured in this capture: the left torch's pool follows the energy keys, with a correlation of point nine five. The read-back: eleven of eleven."

## B25 — Embers, afterimage, readability
*On screen:* **Scripted input · real engine output** — capture/run-01 frame 926 (six ghosts alive) enlarged; `effects/embers.tscn` amount 144; `wolf.tscn` afterimage settings; TUNING.md visual r0 → r1 (robe-to-cave contrast 2.57 → 3.07; 2.74 before A7); `test_afterimage.gd` 6 / 0 and the pin 16 / 0 at 30, 60, 144.
*Narration:* "Plus a hundred and forty-four embers, and a ghost every three lunge ticks. Version zero was not noticeable; version one is clearly visible, with the mage's contrast measured back up to three point oh seven. The pin stayed eight of eight."

## B26 — Limitations
*On screen:* card: README.md "Known limitations", FRICTIONAL.md "Still open", and this film's own limits.
*Narration:* "The limits: the planted foot still slides; the growl window is a fifth of a second, by choice. And this is scripted input — how it feels is the author's call."

## B27 — Who did what
*On screen:* card: FRICTIONAL.md "Human and AI contributions"; SOURCES.md; game source revision f860fed.
*Narration:* "Who did what. The author chose both clips, the interrupt rule and the window, made the run images, and judged everything in play. Claude Code built the pin, clips, tests and upgrades; Claude in chat drafted the documents. Revision f eight six oh f e d."

## B28 — Verdict
*On screen:* `ClaudeVerdictArtifact` — Built · Measured · Judged · Open.
*Narration:* "The verdict. Built: two clips and a flicker, each owned by one animation player on the physics tick. Measured: a pin the clips never moved, one designed change re-pinned after play, four mutations caught. Open: the sliding foot."

## B29 — Your Turn
*On screen:* `ClaudeComposerAsk`, greeting "Your turn.", **Suggested prompt**: "Please use Walker to add in-between frames to my mage's run so the planted foot stops sliding. First predict, in pixels, how far the body moves while one cell is held at 110 px/s and 10 fps; then measure the foot in a windowed Movie Maker strip, and show the behaviour pin still matches tick for tick."
*Narration:* "Your turn. Here's a prompt: Please use Walker to add in-between frames to my mage's run so the planted foot stops sliding. First predict, in pixels, how far the body moves while one cell is held at a hundred and ten pixels a second and ten frames a second; then measure the foot in a windowed Movie Maker strip, and show the behaviour pin still matches tick for tick. The prediction is the point: if your number's wrong, the strip says so first. Liam, in for Bear."

## B30 — Regular outro
*On screen:* `ClaudeTitleOutro` (locked): the title, @NikBearBrown, one slug-seeded mascot. Silent.

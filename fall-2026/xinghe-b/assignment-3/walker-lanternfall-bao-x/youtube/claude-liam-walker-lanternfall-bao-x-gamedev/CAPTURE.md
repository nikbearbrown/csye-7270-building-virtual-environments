# CAPTURE — how the gameplay footage was made

Film: `claude-liam-walker-lanternfall-bao-x-gamedev` · source revision **8a6f9881e0e2858e523d22bb09f1a423695f04e1** (`FILM-SOURCE-REVISION.txt`) · Godot 4.7.2.stable.official.ed1daf0bf, macOS, Apple M4 Pro.

Every gameplay shot in the film is a real engine capture. Nothing is drawn, re-enacted or retimed.

## Isolated copies, never the repository

| Copy | Made with | Changed in the copy |
|---|---|---|
| film build | `git archive 8a6f988 godot` into a scratch folder, `--import` once | `project.godot` window override 3840 × 2160 (so Movie Maker writes 4K); `capture_driver.gd` and `capture_main.tscn` copied in |
| comparison build | `git archive 40102ab godot` (the build of Bao's first playtest, before the hit-test fix `a51af69`) | the same two changes |

`godot/` in the repository was not edited for the film: `git diff 8a6f988 HEAD -- godot/` is empty.

## The driver (`capture/capture_driver.gd`)

- Plays the game through the **real input map**: movement with `Input.action_press`, discrete keys (cards, Esc, R, M, 9, 0) as `InputEventAction` events. The session reads them exactly as it reads a player's keys.
- One shortcut, disclosed: the run starts with `game.start_run(seed)` instead of Enter, so a take is reproducible from its seed.
- Labels every frame "Real engine capture · scripted input".
- Steering: flee anything within 90 px, else walk to the nearest gem, else circle. Card choice: a fixed priority list (Sunflare first, then weapons, then passives). **Each card screen is held 2 s before the pick**, so it can be read on screen.
- Takes: `main` (pause at run 0:40 for 3 s), `lose` (stops steering at 0:20; presses R 15 physics frames after the loss), `props` (walks to the nearest stall, holds right, then down-right, then presses M, M, 9, 9, 0, 0 two seconds apart), `beam` (steers like `main`, no pause; used with a stop time).
- Read-only diagnostics (they never change the game):
  - every SFX play, copied from `AudioBus.play_log`;
  - bolt-over-sprite overlaps: `pass_through` (a bolt overlapped a monster's visible sprite box and flew on without hitting it) and `edge_hit` (a hit whose bolt centre stayed outside the old 10 px circle), with the engine's own canvas transform so the screen position is exact;
  - optional (`LF_LOG_EVENTS=1`, `LF_LOG_TRACK=1`): every kill and gem, and the courier's screen position and zoom for every movie frame.
- **Occlusion guard.** macOS stops drawing a window it considers occluded (another Space, a full-screen app). Movie Maker then repeats the last picture. The first main take lost 0.7–51.3 s that way (kept in `capture/rejected/`). From then on the driver pauses the whole tree — game and audio — while `DisplayServer.window_can_draw()` is false and logs those iterations as `stale`; `tools/clean_take.py` removes exactly those frames and their audio chunks (1600 samples at 48 kHz / 30 fps), with a 4 ms crossfade at the splice. Only the lose take needed it (28 stale frames: 0–3 and 459–482).

## Takes used

| Take | Build · seed | Command (in the isolated copy) | Frames | Result | Stale |
|---|---|---|---|---|---|
| `take-main-seed11.avi` | 8a6f988 · 11 | `godot --always-on-top --path . res://capture_main.tscn --write-movie … --fixed-fps 30 -- main 11` | 6581 (219.3 s) | won at 3:00, level 15, 923 kills, evolved at run 0:58 | none |
| `take-lose-seed3.avi` → `clean/take-lose-seed3.mov` | 8a6f988 · 3 | `… -- lose 3` | 1770 → 1742 | lost at run 0:47, level 3, 47 kills; R restarts | 28 removed |
| `take-props-seed11.avi` | 8a6f988 · 11 | `… -- props 11` | 751 | stall push, slide, mute keys | none |
| `take-before-40102ab-seed14.avi` | 40102ab · 14 | `… -- beam 14 66` | 2437 | five pass-throughs logged at run 0:52–0:59 | none |

Hashes: `capture/takes.sha256`. The AVIs are MJPEG 3840 × 2160 at 30 fps with 48 kHz stereo PCM, written by Godot's Movie Maker (`--fixed-fps 30`: two physics ticks per frame, deterministic).

## Dry runs and why they match the takes

The simulation is deterministic (fixed tick, seeded RNG, SFX gate on the tick clock). Each take has a headless dry run of the same driver at `--fixed-fps 30` (same two ticks per frame). Their event logs were compared with the takes' own logs:

- main and props: **identical** (every SFX, card, action and end state, frame for frame);
- lose: identical in every tick; after the occlusion hold some events sit one physics frame (16.7 ms) later in real time, because the hold began between the two physics steps of a frame. Labels for the lose take use the take's own log, mapped through the stale list, so they are exact.

The dry runs supply only what a capture log cannot: per-frame courier positions (for crops that follow him) and the kill count (for the dense-wave counter). Files: `capture/*-dryrun-track.jsonl`.

## Rejected takes (`capture/rejected/`, not used)

| Take | Why |
|---|---|
| `take-main-seed11-frozen-0.7-51.3s.avi` | window occluded: frames 21–1538 repeat one picture |
| `*-v2-instant-cards*` | the driver picked a card on the same frame the card screen opened, so cards were never visible; replaced by the 2 s hold |
| `take-main-seed11-v1-timeline-60fps.jsonl` | dry run at 60 fps; input timing differs from a 30 fps capture |

## Recorded test output

`capture/test-run-film-build-raw.txt`: the three suites run on a fresh `git archive 8a6f988 godot` copy (imported once): **logic 32/32, gameplay 65/65, audio 25/25**, no script errors. `capture/test-run-film-build.txt` is the excerpt shown in B28 (absolute scratch paths shortened to `…/evidence/`). `capture/test-run-independence.json` is the independence check's record from that run.

## Not committed

The AVI/MOV takes and the rendered `media/*.mp4` are large and stay out of git (`.gitignore`); everything needed to regenerate them is here: the driver, the scene, the commands above, the seeds and the source revision.

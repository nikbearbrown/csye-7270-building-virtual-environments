# CAPTURE.md — how the gameplay in this film was recorded

**Film:** `claude-liam-walker-rudy-gamedev` · **Game:** `walker-rudy` · **Recorded:** 2026-10-04 ·
**Skill:** `godot-gamedev`, `walker` modifier (capture contract borrowed from `godot-waikthrough`).

## The build being demonstrated

| | |
| --- | --- |
| Repository | `walker-rudy` (course copy: `fall-2026/shuai-z/assignment-2/`) |
| Source revision of `game/` | `3b7aa1c51663c614af1997720223622979ddcfbf` ("Step 5: verify the slice…"). `HEAD` is `c0e8055`, which changes only TEST-REPORT.md; `git diff 3b7aa1c -- game` is empty |
| Source snapshot (`build_id`) | `316c7dcac61ff5a9aa9abfc659224cf769ad2af34550cf8aa6ffdb1008e67c1e` |
| Engine | Godot **4.7.2.stable.official.ed1daf0bf**, GL Compatibility, physics 60 Hz |
| Logical canvas | 1920 × 1080 · `stretch/mode = canvas_items` |
| Machine | Apple M3, macOS 15.1 (Darwin 24.1.0) |

**`build_id` method.** SHA-256 of a JSON object mapping each of the 133 git-tracked paths under `game/`
to its own SHA-256, keys sorted, `json.dumps(..., separators=(',', ':'), sort_keys=True)`.
`game/.DS_Store` is untracked (gitignored) and not part of it.

## What was run, and where

`game/` was copied with `rsync --exclude .godot --exclude .DS_Store` to a scratch directory and imported
there with a separate `HOME`, so the capture had its own user-data folder. The repository's `game/` was never
modified. Three harness-only changes were made to the copy (`capture/project.godot.diff`):

1. `window_width_override` / `window_height_override` 1280 × 720 → **3840 × 2160**. The viewport stays
   1920 × 1080 with `canvas_items`, so the window is an exact 2× scale and every sprite, glyph and shader is
   rasterised natively at 4K. This is not an enlarged 1080p recording, and not a claim that the game's
   logical resolution is 4K.
2. An autoload `FilmDriver` (`capture/film_driver.gd`, copied verbatim here).
3. `movie_writer/mjpeg_quality = 0.95`.

No game script, scene, resource or value was edited.

```bash
HOME="$SCRATCH/home" Godot --path "$SCRATCH/game" --resolution 3840x2160 --always-on-top \
  --write-movie run-01.avi --fixed-fps 30 -- --take golden --log run-01-inputs.jsonl
```

Godot's **Movie Maker** renders offline at a fixed 1/30 s step with physics at 60 Hz (two ticks per
recorded frame), and writes the game's **own audio mix** (48 kHz PCM) into the same file. It is not evidence
of real-time frame rate. The AVI takes were transcoded once to H.264 (`-preset slow -crf 14 -r 30 -fps_mode cfr`,
AAC 320k) and their audio extracted losslessly to WAV; frame counts were checked identical before and after
(632 / 598 / 606 / 632).

## The driver: input only

`film_driver.gd` lets the **real main scene** (`run/main_scene`, the title included) boot as a player sees it, and
presses keys by pushing new `InputEventKey` objects through `Input.parse_input_event`, flushed at once
(`Input.flush_buffered_events`), so a press lands on the tick it was decided and reaches `_unhandled_input`
too (F1). Physics-read keys are pressed on `physics_frame`, before Rudy's `_physics_process`; Enter, Esc, M, N and
F1 on `process_frame`, before `Main`'s `_process`.

It **reads** positions, velocities, modes and states to decide when to press. For the stomps it predicts,
read-only, the tick Rudy's soles come down through a goblin's top, copying the integration in `rudy.gd` and the
patrol in `goblin.gd`. It never writes a position, velocity, state, heart count or collision shape, never calls a
gameplay method and never uses the checks' `_teleport`. One diagnostic exception, labelled on screen: the
`outline` stills take sets the outline material's `width` to 0 at runtime after the first still, to show the
same frame without it.

Every take asserts its outcome and exits non-zero on a failed assertion; all four takes and the stills take
exited 0 with zero failures.

**These are scripted-input captures, not a human playtest.** Every gameplay frame carries the chip
`SCRIPTED INPUT · NATIVE 4K ENGINE CAPTURE · run-0N · frames a–b`. shuai-z's own playtest is reported
separately (TEST-REPORT.md) and was not recorded.

## The logs

`capture/run-0N-inputs.jsonl`: one JSON object per line. `state` rows per rendered frame (`f`, `t = f/30`, x, y,
velocity, floor, facing, pose, mode, hearts, gear, level state, checkpoint, paused, music dB, bus mutes,
**sounds started this frame** from `Sfx.counts`, camera x); `input` rows per key event with the physics tick;
`mark`, `check` and `result` rows. Video frame *n* is log frame *n*: checked on run-01, where the first
CHAR-RISE frame is frame 118 in both. run-01 and run-04 logs are byte-identical: the route is deterministic.

## The takes

| take | frames | what it contains | assertions |
| --- | ---: | --- | --- |
| `run-01` | 632 | Title (music under it) → Enter → jump SpikesA → stomp GoblinA → pickup → slash GoblinB → waystone → cliff 1 → SpikesB → slash GoblinC → cliff 2 → circle → end card → Enter plays again | reached the circle, all 3 goblins defeated, no heart lost, replay starts in play with no title |
| `run-02` | 598 | Walk into SpikesA (3→2) → back off, jump → stomp A → pickup → run into GoblinB with the sword (gear lost, hearts 2) → stomp B → waystone lit → run off cliff 1 (2→1) → respawn at the waystone → walk into GoblinB with the last heart → defeat → start over | each heart change, respawn at x 4120, start-over at x 300 with 3 hearts and the waystone dark |
| `run-03` | 606 | F1 debug line on the title → Enter → tap left, tap right (turn on the spot) → run → jump in place → jump key held 1.5 s → running jump over SpikesA → Esc pause/resume → M mute, jump, M → N mute, jump (silent), N → F1 off | tap turns without moving; held key: one jump, one sound; pause/resume; muted jump still calls Sfx.play once |
| `run-04` | 632 | `run-01`'s route again with `--debug-collisions` (Visible Collision Shapes). A `--stop-after slashB` option was passed in one quoted argument and not parsed, so the full route ran; the log's meta row records `stop_after: ""` | same as run-01 |
| stills | — | Rudy stopped at x 664 over the wheat: one 3840×2160 frame with the outline at width 8, one with width 0 (diagnostic) | `outline.tres` width is 8 |

## Audio

The slice's own mix is part of the evidence. In gameplay beats it plays **under** Liam at −14 dB, aligned
sample-for-sample with the 1.0× frames; in the labelled B03 (**SLICE AUDIO ONLY · NO NARRATION**) it plays
alone at −6 dB, for 17.5 s of uncut play. Slowed REPLAY segments and HELD FINAL FRAMES carry no game sound.
Nothing was dubbed: every sound heard is the engine's recording of its own `AudioStreamPlayer`s. The
`SOUND SFX-… · Sfx.play(&"…")` chips are drawn from the log's `sounds` field, i.e. the calls `Sfx.play` counted on
that frame. The outro card has no game audio.

## Labels burned into the film

| label | means |
| --- | --- |
| `SCRIPTED INPUT · NATIVE 4K ENGINE CAPTURE · run-0N · frames a–b` | provenance of the footage |
| `SLICE AUDIO ONLY · NO NARRATION` | B03: only the game's mix |
| `SOUND SFX-X · Sfx.play(&"x")` | `Sfx.play` was called on that frame (from the log) |
| `DEBUG LINE ON (F1)` / `DEBUG: VISIBLE COLLISION SHAPES` | run-03 shows the game's F1 line; run-04 was recorded with `--debug-collisions` |
| `REPLAY 0.25× — …, no sound` / `REPLAY 0.5× — …` | the same frames again, slowed, outside their real-time interval |
| `HELD FINAL FRAME · N s · no gameplay` | narration still running; the game is not |
| `DIAGNOSTIC` (B19) | the outline width set to 0 at runtime on the copy |

Every 1.0× segment is copied frame for frame from the hashed capture. Nothing was sped up, slowed without a
label, or centre-cut to fit narration.

# CAPTURE — capture/run-02 (scripted input, real engine output)

The only new capture in this film. Everything else of the game on screen is the author's committed captures in `captures/` (fixture captures from harnesses that place the characters, and figures drawn from the logs), each labelled as such.

`capture/run-01` (the previous cut, game source f860fed) is superseded: its input and frame logs stay committed as history; nothing in this cut uses them. run-02 replays run-01's three segments with the same driver code and adds two (a hit in LUNGE, a hit in RECOVER). Rows 0–1622 of the run-02 frame log are identical to run-01's, field for field (run-02 adds a `fireballs` field), so every frame number of those segments carries over.

## What was recorded

| | |
|---|---|
| Game | `walker-magic-zhefan` at **ad7935f** (`ad7935fab018f8acb1ff8c72b55d6642ff921fa4`, tree `b4ea2c1d78edea5cc546224b241cc9aeaa40ebbe`), an isolated copy made with `git archive` (tar to a file, then extract), then `godot --headless --import` once. The working project was not run or changed. |
| Engine | Godot 4.7.2-stable (`ed1daf0bf`), Forward+, Vulkan 1.4.312, NVIDIA GeForce RTX 5060 Laptop GPU (printed by the run) |
| Scene | `res://game/main.tscn`, instanced five times (one fresh instance per segment) by `capture/driver.gd` |
| Method | **scripted input**: `capture/driver.gd`, a SceneTree script adapted from the Assignment 6 film's driver. Key events for D (walk right), A (step back) and Space (jump); mouse motion to the aim point and a left click to cast, all through `Input.parse_input_event` (keys are also pushed into the game's viewport). It observes positions and states to choose its inputs (for example: release D when the wolf enters GROWL); it never moves the player or the wolf, calls `cast()`, `take_damage()` or `play()`, or sets a game, clip or effect value. Not a human playtest. |
| Recording | Movie Maker, **windowed** (not headless): `--write-movie <frames>/frame.png --fixed-fps 60 --resolution 1280x720`. Godot printed "recording movie in 640×360 @ 60 FPS" (the game's 640×360 canvas). **2739 PNG frames** (0–2738), 45.65 s of game time. Offline rendering at a fixed step: not evidence of real-time FPS. |
| Why 60 fps | The film is about physics ticks. At `--fixed-fps 60` each rendered frame is one physics tick, so frame n of a segment is tick n, a ×0.25 replay can show every tick, and the clip frame logged for each frame is the one drawn. The film runs at 30 fps: real speed shows every second captured frame; the ×0.25 replay shows every captured frame twice. |
| Command | `godot --path <isolated copy> --script <reel>/capture/driver.gd --write-movie <frames>/frame.png --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- <reel>/capture/run-02-inputs.jsonl <reel>/capture/run-02-frames.jsonl` |
| Result | exit 0; every expectation in the driver held (below); 5 min 2 s wall time. Before the take, the two click delays were found with headless trial runs of the same driver (`only=cancel,lunge_hit,recover_hit`; the first trial with the delays 14 and 40 hit LUNGE and RECOVER as intended), whose logs stayed in the scratch folder; the take itself passes only the two log paths. |
| Archive | `capture/run-02.mp4`: the 2739 frames encoded losslessly (libx264rgb, crf 0), 640×360, 60/1. SHA-256 `af3cb23bbcdd196d9d1f9d2da727cb0e8404acefa1f386990fbcec20d563d09e`. Kept out of git (`*.mp4`). The PNG frames stay outside the repository (`WALKER_CAPTURE`). |
| Input log | `capture/run-02-inputs.jsonl` (committed): every input and every observed state change, cast, wolf hit and expectation, by frame. SHA-256 `3bb51e9b5f4d42bdca44c6fb2298f9c145a466903ef38b0a979604d51c169491`. |
| Frame log | `capture/run-02-frames.jsonl` (committed): one row per rendered frame — the player's state, position, clip and sheet cell, HP; the wolf's state, position, facing, clip and clip frame, hitbox `monitoring`, HP; afterimage ghosts and fireballs alive; the camera. Row f is Movie Maker PNG f. SHA-256 `71a96586617146f5019af07ac4dbfdde7cc1099f8c3260a37e8b4e2f82b7bac7`. |
| Driver | `capture/driver.gd`, SHA-256 `ef89771ef9cc67736755eb702024bf4fb67460f3bf6da799a87099a96129f960` |
| Audio | Movie Maker also wrote `frame.wav` (the game's music and effects); it is **not used**. Liam's narration is the only sound in the film. |

## Harness, not game (disclosed)

- `Main.test_mode = true`, so a fail would not reload the scene under the driver (`main.gd:79, 95`). Nothing failed.
- **The game runs inside its own 640×360 SubViewport**, shown 1:1 by a TextureRect filling the window (the Assignment 6 method): injected mouse motion is pushed into that viewport, so the real OS cursor never sets the aim and the user's mouse is not warped. The click itself is a `parse_input_event` mouse button at the root's final transform of the aim point. The SubViewport is pausable. Rendering is the game's own 640×360 canvas; the HUD, background layer, lights and camera are the game's.
- The mouse is parked at the top right of the view at each segment start, so the crosshair stays out of the action until the cast.
- Frames **441–442, 1089–1090, 1620–1621, 2178–2179 and 2736–2738** are empty (flat grey: the scene was freed between segments; the frame log row of the first of each pair still names the segment, because the row is written before the scene is freed). `scripts/footage.py` asserts that no beat shows a flat frame.
- No overlay is drawn in the game. The state chip under the action in B03–B07, and the hit chip in B05–B07, are read from the logs and drawn by the film outside the game image.
- **How a hit's phase is read.** A fireball hit is resolved at the start of a physics tick, before the wolf's own update, so the phase a hit counts in is the state the wolf ended the previous tick in. At 60 fps one rendered frame is one tick, so the driver logs, for the frame where the wolf's HP drops, the previous frame's state (`prev_state`), the state and clip frame on the hit tick, and HP (`"kind":"wolf_hit"`). The film shows these values; none is read by eye.

## Timeline (frames of run-02, from the logs)

| Segment | Frames | What happens |
|---|---|---|
| run | 0–441 | idle at x 60 (torches and embers); D held: RUN from frame 20; D released at x 220: IDLE at 118; D again: RUN at 153; Space at x ≥ 492: RISE 301, FALL 323, the landing at **346 (RUN, cell 0)**; D released at x 640: IDLE at 389, x 646.7 |
| lunges | 444–1089 | walk and jump the pit; the wolf sees the mage at **880** (GROWL, facing left, dx 115.56); D released; A held 24 frames (the mage steps back); LUNGE 911–932 (facing left, misses), ghosts from 911 (6 alive at 926); RECOVER 933–968; PATROL one tick at **969**, GROWL at **970 (clip frame 0)** as the mage runs past; the wolf turns: LUNGE facing **right** 1001–1022, hits the mage at 1009 (HURT, HP 5 → 4); RECOVER 1023–1058; PATROL 1059, GROWL 1060 |
| cancel (hit in GROWL) | 1092–1620 | walk and jump the pit; GROWL at **1528** (dx 115.56); click and cast at 1530 (**growl tick 2**); the hit on **1549**: the tick before GROWL, on the hit tick **RECOVER, clip frame 53**, wolf HP 2 → 1, 21 ticks after the growl began; no LUNGE; hitbox `monitoring` false on every frame of the segment; A held 30 frames; PATROL at 1584 |
| lunge_hit (hit in LUNGE) | 1623–2178 | walk and jump the pit; GROWL at **2059**; A held from 2062 to 2086 (the mage steps back); click and cast at **2075 (growl tick 16)**; LUNGE 2090–2111; the hit on **2094**: the tick before LUNGE, on the hit tick **LUNGE, clip frame 35** (35 ticks after the growl began, the lunge's fifth tick), `monitoring` on, wolf HP 2 → 1; the dash runs all **22** LUNGE ticks (misses the mage, HP 5); RECOVER at 2112 with clip frame 53; PATROL 2148, GROWL again 2149 (the mage is still in sight) |
| recover_hit (hit in RECOVER) | 2181–2736 | as above to GROWL at **2617** and LUNGE 2648–2669 (misses the mage); click and cast at **2659** (during LUNGE); RECOVER at 2670 (clip frame 53); the hit on **2675**: the tick before RECOVER, on the hit tick **RECOVER, clip frame 58** (58 ticks after the growl began, recovery tick 5), wolf HP 2 → 1; RECOVER lasts all **36** ticks; PATROL 2706, GROWL again 2707 |

Expectations checked by the driver (all true, `"kind":"expect"` in the input log):
- **run**: 3 RUN entries, 1 RISE, 1 FALL, x 646.7 > 600, not failing, the wolf never growled.
- **lunges**: lunge facings [−1, 1], up to 6 ghosts alive, 2 recoveries, not failing (player HP 4).
- **cancel**: 1 cast, the state after the growl RECOVER, wolf HP 1, 0 lunges, 0 frames with the hitbox monitoring, sight dx 115.56; one hit, phase before GROWL, RECOVER on the hit tick, clip frame 53.
- **lunge_hit**: 1 cast, one hit with LUNGE before and on the hit tick, wolf HP 1, one LUNGE of 22 frames, one RECOVER entered at clip frame 53, not failing.
- **recover_hit**: 1 cast, one hit with RECOVER before and on the hit tick, wolf HP 1, one LUNGE of 22 frames, RECOVER of 36 frames, not failing.

## How the film uses it

`scripts/footage.py` builds B03 (real speed 15–439, ×0.25 replay 292–372), B04 (860–1088, replay 876–1030), B05 (1380–1619, replay 1518–1600), B06 (1930–2148, replay 2058–2148) and B07 (2500–2706, replay 2616–2706). Each plays its interval once at real speed (every second captured frame, in order), then a labelled ×0.25 replay of part of it (every captured frame twice), then the last frame held and labelled, to the exact frame count of the beat's measured narration, so the compiler neither retimes nor cuts it. The canvas is enlarged ×5 with nearest-neighbour scaling (3200×1800) under a header naming the capture and its frames. In B05–B07 the hit chip appears from the hit frame on; `footage.py` asserts its values against the frame log. `scripts/media.py` uses single frames as crops on B11 (20–44), B13 (340–351) and B16 (880, 911, 933, 969).

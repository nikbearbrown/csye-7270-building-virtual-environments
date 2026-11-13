# CAPTURE — capture/run-01 (scripted input, real engine output)

The only new capture in this film. Everything else of the game on screen is the author's committed captures in `captures/` (fixture captures from harnesses and preview scenes that place the characters, and figures drawn from the logs), each labelled as such.

## What was recorded

| | |
|---|---|
| Game | `walker-magic-zhefan` at **f860fed** (tree `0443b97e6581dc2a0e45ade04166c66644018749`), an isolated copy made with `git archive`, then `godot --headless --import` once. The working project was not run or changed. |
| Engine | Godot 4.7.2-stable (`ed1daf0bf`), Forward+, Vulkan 1.4.312, NVIDIA GeForce RTX 5060 Laptop GPU (printed by the run) |
| Scene | `res://game/main.tscn`, instanced three times (one fresh instance per segment) by `capture/driver.gd` |
| Method | **scripted input**: `capture/driver.gd`, a SceneTree script adapted from the Assignment 6 film's driver. Key events for D (walk right), A (step back) and Space (jump); mouse motion to the aim point and a left click to cast. It observes positions and states to choose its inputs (for example: release D when the wolf enters GROWL); it never moves the player or the wolf, calls `cast()`, `take_damage()` or `play()`, or sets a game, clip or effect value. Not a human playtest. |
| Recording | Movie Maker, **windowed** (not headless): `--write-movie <frames>/frame.png --fixed-fps 60 --resolution 1280x720`. Godot printed "recording movie in 640×360 @ 60 FPS" (the game's 640×360 canvas). **1623 PNG frames** (0–1622), 27.05 s of game time. Offline rendering at a fixed step: not evidence of real-time FPS. |
| Why 60 fps (A6 used 30) | The film is about physics ticks. At `--fixed-fps 60` each rendered frame is one physics tick (the frame log's `phys` counter rises by one per frame), so frame n of a segment is tick n, a ×0.25 replay can show every tick, and the clip frame logged for each frame is the one drawn. The film runs at 30 fps: real speed shows every second captured frame; the ×0.25 replay shows every captured frame twice. |
| Command | `godot --path <isolated copy> --script <reel>/capture/driver.gd --write-movie <frames>/frame.png --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- <reel>/capture/run-01-inputs.jsonl <reel>/capture/run-01-frames.jsonl` |
| Result | exit 0; every expectation in the driver held (below). One trial take with the same driver (identical apart from one logging fix) produced the same frame log; it was discarded and the final take re-recorded. |
| Archive | `capture/run-01.mp4`: the 1623 frames encoded losslessly (libx264rgb, crf 0), 640×360, 60/1. SHA-256 `355e10a8c7c3b700a8ba0c529e67349f9bec5ca38bbb10661dc3896815f2ee82`. Kept out of git (`*.mp4`). The PNG frames stay outside the repository (`WALKER_CAPTURE`). |
| Input log | `capture/run-01-inputs.jsonl` (committed): every input and every observed state change, cast and expectation, by frame. SHA-256 `4b72d2e5f59b1a48c9ad6a6fb255cdb21075b045b6e51832ae5b324aefaeed65`. |
| Frame log | `capture/run-01-frames.jsonl` (committed): one row per rendered frame — the player's state, position, clip and sheet cell, HP; the wolf's state, position, facing, clip and clip frame, hitbox `monitoring`, HP; afterimage ghosts alive; the camera. Row f is Movie Maker PNG f (checked: the wolf's switch from the run image to the rig appears first in PNG 880, the frame the log gives for GROWL). SHA-256 `597e819846afcc492e0d9e5e933a0d96a5204db2af5aa27a170e846a2bb259df`. |
| Driver | `capture/driver.gd`, SHA-256 `13060912606b725a51e590829ee4fc2d1be3d8b8102c364ed43566a2682b72de` |
| Audio | Movie Maker also wrote `frame.wav` (the game's music and effects); it is **not used**. Liam's narration is the only sound in the film. |

## Harness, not game (disclosed)

- `Main.test_mode = true`, so a fail would not reload the scene under the driver (`main.gd:79, 95`). Nothing failed.
- **The game runs inside its own 640×360 SubViewport**, shown 1:1 by a TextureRect filling the window (the Assignment 6 method): in a real window Godot reads the aim of any viewport whose section root is the window from the OS cursor, so injected mouse motion would not move it, and warping the cursor would take over the user's real mouse. Keys go through `Input.parse_input_event` (the actions the player reads) and are also pushed into the game's viewport. The SubViewport is pausable. Rendering is the game's own 640×360 canvas; the HUD, background layer, lights and camera are the game's.
- The mouse is parked at the top right of the view at each segment start, so the crosshair stays out of the action until the cast.
- The one click (frame 1530) was aimed at the wolf's body centre, (926.3, 312.9); the game read (928.3, 312.9) one frame later, because the camera follows the mage and she was still decelerating by 2 px. The fireball hit.
- Frames **441–442, 1089–1090 and 1620–1622** are empty (flat grey): the scene was freed between segments. No beat uses them (B03 ends at 439, B04 at 1088, B05 at 1619).
- No overlay is drawn in the game. The state chip under the action in B03–B05 is read from the frame log and drawn by the film outside the game image.

## Timeline (frames of run-01, from the logs)

| Segment | Frames | What happens |
|---|---|---|
| run | 0–440 | idle at x 60 (torches and embers); D held: RUN from frame 20; D released at x 220: IDLE at 118; D again: RUN at 153; Space at x ≥ 492: RISE 301, FALL 323, the landing at **346 (RUN, cell 0)**; D released at x 640: IDLE at 389, x 646.7 |
| lunges | 444–1088 | walk and jump the pit as above; the wolf sees the mage at **880** (GROWL, facing left, dx 115.56); D released; A held 24 frames (the mage steps back); LUNGE 911–932 (facing left, misses), ghosts from 911 (6 alive at 926); RECOVER 933–968; PATROL one tick at **969**, GROWL at **970 (clip frame 0)** as the mage runs past; the wolf turns: LUNGE facing **right** 1001–1022, hits the mage at 1009 (HURT, HP 5 → 4); RECOVER 1023–1058; PATROL 1059, GROWL 1060 |
| cancel | 1092–1619 | walk and jump the pit; GROWL at **1528** (dx 115.56); click at 1530: **cast on growl tick 2**; the fireball lands at **1549 = growl tick 21**: RECOVER, clip frame 53, wolf HP 2 → 1; no LUNGE; hitbox `monitoring` false on every frame of the segment; A held 30 frames (out of sight); PATROL at 1584 |

Expectations checked by the driver (all true, `"kind":"expect"` in the input log):
- **run**: 3 RUN entries, 1 RISE, 1 FALL, x 646.7 > 600, not failing, the wolf never growled.
- **lunges**: lunge facings [−1, 1], up to 6 ghosts alive, 2 recoveries, not failing (player HP 4).
- **cancel**: 1 cast, the state after the growl RECOVER, wolf HP 1, 0 lunges, 0 frames with the hitbox monitoring, sight dx 115.56.

## How the film uses it

`scripts/footage.py` builds B03 (real speed 15–439, ×0.25 replay 292–372), B04 (850–1088, replay 876–1062) and B05 (1380–1619, replay 1518–1600). Each plays its interval once at real speed (every second captured frame, in order), then a labelled ×0.25 replay of part of it (every captured frame twice), then the last frame held and labelled, to the exact frame count of the beat's measured narration, so the compiler neither retimes nor cuts it. The canvas is enlarged ×5 with nearest-neighbour scaling (3200×1800) under a header naming the capture and its frames. `scripts/media.py` uses single frames as crops on B11 (20–44), B13 (340–351), B25 (926) and measures the left torch's pool on frames 0–440 for B24 (`evidence/torch-flicker-measurement.json`).

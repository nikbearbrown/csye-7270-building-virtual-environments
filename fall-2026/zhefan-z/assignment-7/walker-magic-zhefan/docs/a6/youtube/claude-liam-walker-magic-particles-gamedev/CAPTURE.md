# CAPTURE — capture/run-01 (scripted input, real engine output)

The only new capture in this film. Everything else of the game on screen is the author's committed fixture strips in `captures/`.

## What was recorded

| | |
|---|---|
| Game | `walker-magic-zhefan` at **3c37fe0** (tree `66ebc690291ebc8d14cb538eb15413df2d337a5f`), an isolated copy made with `git archive`, then `godot --headless --import` once. The working project was not run or changed. |
| Engine | Godot 4.7.2-stable (`ed1daf0bf`), Forward+, Vulkan 1.4.312, NVIDIA GeForce RTX 5060 Laptop GPU (printed by the run) |
| Scene | `res://game/main.tscn`, instanced by `capture/driver.gd` |
| Method | **scripted input**: `capture/driver.gd`, a SceneTree script. Mouse motion to the aim point and a left click to cast; key events for D (walk), Space (jump), Esc (pause). It observes positions to choose inputs; it never moves the player, calls `cast()` or `explode()`, or sets a game or effect value. Not a human playtest. |
| Recording | Movie Maker, **windowed** (not headless): `--write-movie <frames>/frame.png --fixed-fps 30 --resolution 1280x720 --quit-after 1500`. Godot printed "recording movie in 640×360 @ 30 FPS": the game's 640×360 canvas. 909 PNG frames. Offline rendering at a fixed step: not evidence of real-time FPS. |
| Command | `godot --path <isolated copy> --script <reel>/capture/driver.gd --write-movie <frames>/frame.png --fixed-fps 30 --resolution 1280x720 --quit-after 1500 -- <reel>/capture/run-01-inputs.jsonl` |
| Result | exit 0; every expectation in the driver held (below); 17 clicks, the aim seen by the game equal to the aim sent for all 17 |
| Archive | `capture/run-01.mp4`: the 909 frames encoded losslessly (libx264rgb, crf 0), 640×360, 30/1. SHA-256 `81f207048bb51d6370cc461ba0c00b4c4a4c37d60ca1fac6e240403c23322e80`. Kept out of git (`*.mp4`). The PNG frames stay outside the repository (`WALKER_CAPTURE`). |
| Input log | `capture/run-01-inputs.jsonl` (committed): every input and every observed cast, impact, detached trail, pause state and expectation, by frame. SHA-256 `b3e89bfdbeb9b31b4745aafdd27522e772c23ee94decc95070e25023b8f3dfa4`. Driver SHA-256 `78689295dee38157acf07aaeac8d7a1a7ce9e53cdffab4e201e63ecd6a71d4fc`. |
| Audio | Movie Maker also wrote `frame.wav` (the game's music and effects); it is **not used**. Liam's narration is the only sound in the film. |

## Harness, not game (disclosed)

- `Main.test_mode = true`, so a fail would not reload the scene under the driver (`main.gd:79, 95`). Nothing failed.
- **The game runs inside its own 640×360 SubViewport**, shown 1:1 by a TextureRect filling the window. In a real window, Godot 4.7.2 reads the mouse for any viewport whose section root is the window from the OS cursor, so injected motion could not move the aim, and warping the cursor would have taken over the user's real mouse. A standalone SubViewport uses the last mouse event pushed into it. Keys go through `Input.parse_input_event` (the actions the player reads) and are also pushed into the game's viewport (SessionInput's Esc). The SubViewport is pausable, so the game pauses as in a normal run. Rendering is the same 640×360 canvas; the HUD, background layer and camera are the game's own.
- Two earlier windowed takes were discarded: in the first (game in the root viewport) and the second (game in a SubViewportContainer) the aim stayed at the OS cursor's position, and the driver's expectations failed (no impacts where aimed). Both quit 1; nothing from them is used.

## Timeline (frames of run-01, from the input log)

| Segment | Frames | What happens |
|---|---|---|
| first-impact | 0–69 | the mage at the level start (x 60); a click into the ground at (200, 345): cast at 16, impact and trail released at 29 |
| effect-a-play | 70–528 | a shot into the left wall (cast 86, impact at x 1.3 on frame 92, the screen edge); D held to walk, Space at x ≥ 492 to jump the pit; at x 613.7, three shots at the wolf leading its motion: hits at 311 and 333 (defeated at 333), the third into the ground at 364; nine clicks into the ground every 11 frames (0.367 s; cooldown 0.35 s): nine impacts 393–496 |
| trail | 529–908 | walk to x 300; a shot right at staff height: no hit, trail released on the 2.0 s timeout (cast 623, released 683); a shot left into the wall (cast 706, impact 740); a shot right (cast 765), Esc at frame 787 (paused), Esc at 835 (resumed), released on its timeout at 873: 60 frames (2.0 s) of flight plus the 48 paused frames |

Expectations checked by the driver (all true): first-impact 1 cast / 1 impact / 1 trail released; wolf defeated; 13 casts, 13 impacts, 13 trails released, 9 rapid impacts; trail segment 3 casts, 3 trails released, 1 impact, pause on then off.

## How the film uses it

`scripts/footage.py` builds B04 (frames 6–70), B13 (72–527) and B19 (531–907). Each plays its interval once at real speed, every frame in order, then a labelled ×0.25 replay of part of it (each frame shown four times), then the last frame held and labelled, to the exact frame count of the beat's measured narration, so the compiler neither retimes nor cuts it. The canvas is enlarged ×5 with nearest-neighbour scaling (3200×1800) under a header naming the capture and the frames. B02 shows frames 25 and 32 enlarged ×6.

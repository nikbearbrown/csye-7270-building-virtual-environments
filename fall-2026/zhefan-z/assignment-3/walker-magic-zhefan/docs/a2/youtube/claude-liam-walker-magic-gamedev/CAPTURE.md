# CAPTURE.md — walker-magic gamedev film

> Status: **probe passed and takes run-01…run-04 recorded and gated (2026-10-07).** Updated after every take.

Engine: **Godot 4.7.2.stable.official.ed1daf0bf** (win64 console build), Vulkan 1.4.312, Forward+, NVIDIA GeForce RTX 5060 Laptop GPU, Windows 11.
Capture source: commit **`5266946`** of branch `zhefan-z/assignment-2`. Its runtime files (`game/`, `features/`, `audio/`, `ui/`, `assets/` media, `project.godot`, `default_bus_layout.tres`) are identical to **`74c0443`**, the build that passed the fresh-copy check and playtests 5–6 (only `assets/audio/MUSIC-EDIT-LOG.md`, a text log, differs).

## Method

All takes are **scripted-input** engine runs recorded with Godot's Movie Maker. None is a human playtest, and the film labels every one of them "Scripted-input capture".

```
bash make_capture_copy.sh <commit> <capture-copy>
WALKER_CAPTURE_MODE=<take> WALKER_CAPTURE_LOG=<reel>/capture/<take>-inputs.jsonl \
  Godot_v4.7.2-stable_win64_console.exe --path <capture-copy> \
  --write-movie <reel>/capture/<take>.avi --fixed-fps 60 --quit-after <cap> \
  --resolution 3840x2160 res://capture/capture_main.tscn
```

Movie Maker is offline rendering, **not evidence of real-time frame rate**. The simulation runs at the project's 60 physics ticks per second, so in-game timing and event order are unaffected. Movie Maker records the engine's own audio mix into the AVI with the picture.

## Isolated copy and disclosed capture accommodations

`make_capture_copy.sh` builds the copy outside the repository (`E:\7270\tools\capture\walker-magic-<commit>`) from `git archive` of the committed game folder: no working-tree changes, no `.godot` cache. The game's own code and assets are not modified. Two capture-only accommodations, both in the copy only:

1. **Native 4K for a `viewport`-stretch pixel-art game.** The game renders a 640x360 canvas and its window scales it with stretch mode `viewport`; Movie Maker records that canvas at 640x360 (seen in the first probe: "recording movie in 640×360"). The copy's `project.godot` therefore sets a **3840x2160 root viewport** (stretch mode `viewport` kept, integer scaling dropped, window overrides removed), so the root stays 3840x2160 even when the OS clamps the window to the 2560x1600 screen, and `capture_main.gd` runs the real `game/main.tscn` inside a **640x360 SubViewport drawn at x6 with nearest filtering** (pixel snapping on, as in the game). The preview window shows the whole root scaled down; Movie Maker records the root itself. That is the same integer upscale the game's own window performs, rendered by the engine at 3840x2160; it is not a low-resolution recording enlarged afterwards. **Logical resolution: 640x360; capture: 3840x2160 (x6).**
2. **Two-step import.** A first import from an empty cache with the capture scripts present crashed Godot 4.7.2 at shutdown (segmentation fault, twice in a row); without them it succeeded twice in a row. The script imports the game first, then again with `res://capture/` present.

## Harness and driver

`capture_main.gd` instantiates the real `game/main.tscn` and adds `capture_driver.gd` beside it. Because the game reloads its own scene 1.2 s after a fail, and the reloaded scene here is the harness, an attempt counter on `Engine` metadata tells the driver it is in the second attempt (run-02).

`capture_driver.gd` sends **only real input events** through `Input.parse_input_event`: `InputEventAction` for move, jump, pause and mute, and `InputEventMouseMotion` + `InputEventMouseButton` (left) for aiming and casting, in window coordinates. They reach the game's normal paths: `Input.get_axis` and `is_action_just_pressed` in `player.gd`, `get_global_mouse_position()` for the aim, and `SessionInput._unhandled_input` for Esc, M and N. The driver **reads** player, wolf, HUD and bus state to decide when to press and to assert the result; it **writes nothing** to the game (no position, velocity, HP, state, collision, or the test-only `use_scripted` hook). It runs at physics priority -20. Every press, release, click and game event (cast, hurt, wolf down, fail, clear) is logged against the physics tick in `capture/<take>-inputs.jsonl`. Each take asserts its expected events and exits non-zero on failure; exhausting the frame cap is exit 2, not success.

**Focus rule.** On Windows, Godot releases every held input when its window loses focus. In the second probe the run key was let go about 0.8 s in (x 60 → 148, then standing) while the 4K take recorded at 5% of real-time speed. The harness first treated a focus loss as an invalid take (exit 3); focus losses also occurred at launch, so it now logs each one (`focus_lost`), asks the window back to the front, and re-asserts any held action the OS released (`reassert`), and `gate.py` decides validity (probes 6–9). During a take the machine must not be used.

**Reference gate (as in Assignment 1).** Every 4K take is compared with a headless run of the same driver: the two input logs must match action for action and position for position.

## Probes

| # | Run | Result |
|---|---|---|
| 1 | Headless reference, `probe` | **Pass.** Run pressed at tick 32; jump at x = 507.0; landed past the pit at x = 600.5; click aimed at (922.3, 312.9); the game's cast direction (0.989, 0.150) = the line from the staff tip to the aim point. Exit 0. |
| 2 | Movie Maker, before the SubViewport | Recorded, but at **640x360** (stretch mode `viewport`). Rejected; led to accommodation 1. |
| 3 | Movie Maker 3840x2160, SubViewport | Recorded at **3840x2160 @ 60 fps** (900 frames, 4 min 18 s wall, 5% of real time), but the take **failed its assertion**: the run key was released ~0.8 s in and the mage stood still (frame cap, exit 2). Cause: window focus loss (focus rule above). File deleted; not evidence. |
| 4 | Movie Maker 3840x2160, with focus detection | **Crashed** after 8 s: `ERROR: Parameter "mem" is null. at: alloc_static (core/os/memory.cpp:104)`, then signal 11. A memory allocation failed. At the time 12.2 GB RAM / 9.7 GB commit were free, but Slay the Spire 2 (4.3 GB private, same GPU) and Windows Volume Shadow Copy (5.9 GB working set) were running. The same scripts run headless without error. |
| 5 | Movie Maker 3840x2160, other applications closed | Recorded and passed its own assertion, but **rejected**: the gate failed on the cast (headless dir 0.989, 0.150; 4K dir -0.174, -0.985), and a frame showed only the top-left ~2564x1570 of the game enlarged to 3840x2160. Cause: the screen is 2560x1600, the OS clamped the window to 2564x1570, and with stretch disabled the root viewport followed the window. |
| 6–8 | Windowed debug runs (no recording) | Found the remaining causes: (a) a windowed Godot reads the **OS cursor**, which overrides injected mouse motion; (b) with integer scaling the 4K root was shown 1:1 in the smaller window, so aim points beyond 2564x1570 were clamped; (c) focus losses also occurred at launch. Fixes, all in the harness or the copy: root viewport fixed at 3840x2160 with stretch mode `viewport` kept and integer scaling dropped (the preview window shows the whole 4K root scaled down; Movie Maker records the root at 3840x2160); the driver also moves the real OS cursor with `Input.warp_mouse` to the aim point (measured: `warp_mouse(p)` reads back `p`); input is flushed on the tick it is sent; held actions released by the OS are re-asserted before the player reads them (logged as `reassert`); a focus loss is logged and the window asked back to the front. Validity is decided by `gate.py`. |
| 9 | **Movie Maker 3840x2160 probe — valid** | `capture/probe.avi`: 531 frames, 3840x2160 MJPEG @ 60 fps + PCM 48 kHz stereo, 8.85 s, recorded in 46 s (17% of real time), sha256 `a5b7501059b8d2355ce04780591a028ba3bea2b24fe95dd35fe3f5a034b9ee90`. Assertion passed (landed past the pit, one cast). **Gate: PASS** against the headless run (8/8 compared rows, 0 differing, 0 focus losses, 0 re-asserted presses). Frames at 1.0, 4.85 and 5.95 s show the whole scene: run, jump over the pit, cast with the fireball. Audio: music alone -23.3 dBFS RMS (4.5–5.8 s), the cast window -20.3 dBFS (5.86–6.26 s), peak -5.2 dBFS. |

**Gate tolerance.** A real OS cursor sits on whole window pixels (0.25 game-world px at this window size), so `gate.py` allows ±0.5 world px on the aim the game reads back and ±0.005 on the cast direction; every other value must match exactly, and a change of outcome (a hit or a miss) would still fail through the game-event rows.

## Gameplay audio in the film

The skill's compiler strips footage audio (`-an`); ordinary b-roll is silent under narration. The SLICE AUDIO beats (B18, B20) use, as their `audio_file`, the audio track of the same Movie Maker take cut to exactly the same interval as their video, with no narration. **Approval (verbal):** verbal approval from the instructor the method is acceptable. Recorded 2026-10-07, as reported by the author; there is no written message.

## Takes (approved plan)

All four recorded 2026-10-07 in one sequence with the machine untouched (Steam client open, no game). Each: 3840x2160 MJPEG @ 60 fps + PCM 48 kHz stereo (audio length = video length), own assertion passed (exit 0), and **gate PASS** against its headless reference with **0 differing rows, 0 focus losses, 0 re-asserted presses**. The headless references are kept outside the repo in `E:\7270\tools\capture\ref\`; the take input logs are `capture/<take>-inputs.jsonl`. The AVIs are not in Git.

| Take | Shows | Frames / duration | Wall time | Gate | sha256 |
|---|---|---|---|---|---|
| run-01 | Run, jump the pit, walk into the wolf's sight, one lunge hit, cast until the wolf is down, reach the exit | 991 / 16.52 s | 83 s | PASS 16/16 | `5c75bc9de992123ddc77ae9dbc1cdc5318d778382749a0de360b705ca9afe9f3` |
| run-02 | Walk into the pit, fail, music stops, reload, music back from the top | 556 / 9.27 s (attempt 1: 374 ticks, attempt 2: 181) | 50 s | PASS 4/4 | `a02159af48ca56e51160b1b1eb08ed25e562ae8c2329338ae6f935451dcd844f` |
| run-03 | M (music off), N (effects off, a silent cast), N, a cast, M | 567 / 9.45 s | 51 s | PASS 15/15 | `20807dede84047c36e171725e0ae26930ee8625b6ccc9c57357d172a2d41cc9e` |
| run-04 | Esc pause and resume | 375 / 6.25 s | 32 s | PASS 7/7 | `328ebd6f9283eb9a5b32b06e48bd37d25228bce5338459bc63b61688e8807e91` |

**Event times (take time, from the input logs).** run-01: run pressed 0.78 s; jump 4.90 s (x 507); hurt 8.37 s; casts 8.82 s and 9.18 s; wolf down 9.32 s; walk on 10.18 s; clear 14.02 s (x 1222). run-02: run pressed 0.53 s; fail "Fell into the dark" 5.03 s (x 551); reload 6.23 s; attempt 2 idle with 5 hearts. run-03: M 0.70 s; N 2.22 s; silent cast 2.92 s; N 3.92 s; cast 4.45 s; M 5.45 s. run-04: run 0.53 s; Esc 1.22 s (x 129, frozen while paused); Esc 3.25 s; moves on to x 241.

**Frames checked** (16 frames across the four takes, a contact sheet kept outside the repo): jump over the pit; wolf approach; the mage blinking after the hit (hearts 4); fireball at the wolf; CLEARED at the exit; "Fell into the dark" at the pit; the reloaded start with 5 hearts; the "music off (M)" and "music off (M)  sfx off (N)" labels; a fireball with both muted; labels gone after both restored; PAUSED overlay; motion after resume.

**Audio checked** (RMS / peak, dBFS):

| Take | Window | RMS | Peak | Reading |
|---|---|---|---|---|
| run-01 | music only 3.0–4.5 s | -20.6 | -9.3 | music |
| run-01 | hurt 8.37–8.62 s | -21.3 | -8.5 | SFX-HURT (0.3 s) under the music |
| run-01 | cast 8.82–9.10 s | -16.1 | -3.9 | SFX-CAST above the music |
| run-01 | wolf down 9.32–9.70 s | -14.6 | -0.4 | SFX-WOLF-DOWN; loudest moment, not clipped |
| run-01 | clear 14.02–14.6 s | -21.5 | -4.8 | SFX-CLEAR; music stopped at the exit |
| run-01 | after clear 15.6–16.5 s | silent | silent | silence after the clear, as designed |
| run-02 | fail 5.03–5.5 s | -13.4 | -2.8 | SFX-FAIL |
| run-02 | 5.0–6.5 s in 0.1 s steps | | | SFX-FAIL (1.0 s) to 6.0 s, silent at 6.1 s (music stopped), music from the top from 6.2 s after the reload |
| run-03 | music off 1.0–2.1 s | silent | silent | M muted the music bus |
| run-03 | both off, cast 2.92–3.4 s | silent | silent | the silent cast |
| run-03 | cast, music still off 4.45–4.9 s | -21.3 | -4.7 | SFX-CAST alone after N |
| run-03 | both on 6.0–9.4 s | -20.1 | -8.1 | music back after M |
| run-04 | paused 1.4–3.2 s | silent | silent | music paused |
| run-04 | resumed 3.5–6.2 s | -20.3 | -8.5 | music resumes |

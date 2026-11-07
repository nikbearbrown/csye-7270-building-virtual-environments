# CAPTURE.md — walker-magic Assignment 3 gamedev film

> Status: **probe passed and take run-01 recorded and checked (2026-10-14).**

Engine: **Godot 4.7.2.stable.official.ed1daf0bf** (win64 console build), Vulkan 1.4.312, Forward+, NVIDIA GeForce RTX 5060 Laptop GPU, Windows 11.
Source: commit **`8d8895c`** (`8d8895cf80a68d85e18e9142b6a687c68618c51d`), `walker-magic-zhefan` tree `79ea0965c11386d2b3fac1a8eb39bd20f29f4149`. Its game files are identical to `1bacec8`; `8d8895c` only added documents outside the project folder.

## Method

The one take is a **scripted-camera** engine run of the real `res://showcase3d/prop_room.tscn`, recorded with Godot's Movie Maker. The prop room has no gameplay input; the harness moves only its Camera node. It is not a person looking around the scene (that look is the author's, in TEST-REPORT.md and the B14 screenshots). The film labels the footage "Godot Movie Maker capture · scripted camera".

```
bash make_capture_copies.sh 8d8895cf80a68d85e18e9142b6a687c68618c51d <base>
WALKER_CAPTURE_MODE=<probe|run-01> WALKER_CAPTURE_LOG=<reel>/capture/<take>-camera.jsonl \
  Godot_v4.7.2-stable_win64_console.exe --path <base>/capture \
  --write-movie <reel>/capture/<take>.avi --fixed-fps 60 --quit-after <cap> \
  --resolution 3840x2160 res://capture/capture_prop_room.tscn
```

Movie Maker is offline rendering, **not evidence of real-time frame rate**.

## Isolated copies and disclosed capture accommodations

`make_capture_copies.sh` writes `git archive` of the committed `walker-magic-zhefan` at `8d8895c` to a tar file (not a pipe) and extracts it three times outside the repository, in `E:\7270\tools\capture\walker-magic-a3-8d8895c\`:

| Copy | Use | Changes |
|---|---|---|
| `snapshot/` | the `--game` folder for `./art godot-gamedev --check` | none; never run (no `.godot/`) |
| `ref/` | the headless check (B18) and the `.glb` read (B13) | none; imported once |
| `capture/` | the Movie Maker capture (B16) | two capture-only accommodations, below |

1. **Native 4K.** The project renders at a 640×360 viewport with stretch mode `viewport`. The capture copy's `project.godot` sets a **3840×2160 root viewport** (stretch mode `viewport` kept; window overrides and integer scaling removed), as in Assignment 2. The OS clamps the window to the 2560×1600 screen (the harness logged 2564×1570), but Movie Maker records the fixed 3840×2160 root. The 3D scene is rendered by the engine at 3840×2160; it is not a smaller recording enlarged afterwards. A 1:1 crop of the probe shows 1-pixel edge steps.
2. **The camera harness** under `res://capture/` (`capture_prop_room.gd`, kept in this reel). It instantiates the real `prop_room.tscn` unchanged, holds the scene's saved camera, then orbits the camera around the saved look point (−0.65, 0.45, 0) at the saved radius 4.0 m and height 1.2 m, eased. It writes nothing else. Before the first frame it checks: exactly one Light3D; Rock, Crystal and Chest with their lowest vertex at y = 0 (±0.02 m); the Mage on Y-billboard; it exits 1 on a failure and 0 when the path completes. Every frame's camera pose is logged.

**Line endings.** `git archive` writes CRLF text here (`core.autocrlf=true`); Godot's first import rewrites the `.import` files with LF. Ignoring line endings, `ref/` and `snapshot/` differ in **0** files after the import.

Imports: `ref/` and the capture copy (two steps: game, then with `res://capture/`) all exited 0 with no errors. A headless dry run of both modes passed before any recording.

## Takes

| Take | Shows | Frames / duration | Wall | Result | sha256 |
|---|---|---|---|---|---|
| probe | 1 s hold, 2 s orbit through 60°, 0.5 s held | 210 / 3.50 s · 3840×2160 MJPEG @ 60 fps + PCM | 19 s (17% of real time) | checks passed, exit 0 | `3c3f6367bc1f1c9819dd74ce062481af19e432c748227ce6b17dd8c563ee790b` |
| **run-01** | 2 s hold on the saved camera, 9 s eased orbit through 180° to behind the props, 1 s held | 720 / 12.00 s · 3840×2160 MJPEG @ 60 fps + PCM | 55 s (22% of real time) | checks passed, exit 0; camera log 120 hold + 540 orbit + 60 tail rows, angle non-decreasing 0° → 180° | `d3ec6d17142c06ce8ea931f3dafc31ed1d6fa3d572a156984b575b8c9351a696` |

Both recorded 2026-10-14 with the machine untouched. No Godot process remained afterwards. The AVIs are not in Git (`youtube/*/capture/*.avi`); the camera logs and Godot logs are.

**Audio.** The scene has no sound; run-01's PCM track is digital silence (−91 dB mean and max). The film uses no capture audio.

**Frames checked** (run-01 at 1.0, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 11.9 s): the saved view matches the author's F6 screenshot in framing; background #0F1119 and no floor edge; from the right the props stand on the floor and cast shadows, the chest's gold reads yellow-gold; at about 6 s the orbit passes close to the chest's right end, which is nearly black; from behind the rock and chest are almost black (one light from the front-left), the crystal stays blue, and the mage still faces the camera. Edges show slight aliasing (the project has no anti-aliasing).

## In the film

B16 uses the whole take at normal speed (every second 60 fps frame → 30 fps, 360 frames), then its final frame held for 144 frames, labelled **Held frame**, to the end of the 16.77 s narration. The disclosure label "Godot Movie Maker capture · scripted camera · run-01 · build 8d8895c" stays on screen throughout.

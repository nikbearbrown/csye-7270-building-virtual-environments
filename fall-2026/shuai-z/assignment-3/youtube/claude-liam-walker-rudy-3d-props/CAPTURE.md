# CAPTURE — how the film's evidence was recorded

**Film:** `claude-liam-walker-rudy-3d-props` · **Project:** walker-rudy, Assignment 3 (`fall-2026/shuai-z/assignment-3/`) · **Recorded:** 2026-10-13 (EDT) · **Skill:** `godot-gamedev`, `walker` modifier.

## The source being demonstrated

| | |
| --- | --- |
| Source revision | `f6f8acf09b1c8e737caa1de08db60f61e28c2a2e`, the last commit that touches `godot/`; the working tree was clean when every capture below was made |
| Godot | 4.7.2.stable.official.ed1daf0bf, Forward Plus, Metal 3.2, Apple M3, macOS 15.1 |
| Blender | 5.2.2 LTS with MCP for Blender server 2.1.9, add-on 1.8 |

## 1 · The running scene: `capture/orbit-01.mp4` (B11)

`godot/` was copied with `rsync --exclude .godot` to a scratch directory and imported there with a separate `HOME`. Two harness-only changes were made to the copy (`capture/project.godot.diff`):

1. `window_width_override` / `window_height_override` 1280 × 720 → **3840 × 2160**, so the 3D view renders natively at 4K.
2. An autoload, `OrbitDriver` (`capture/orbit_driver.gd`, copied verbatim here). It lets the real main scene (`res://scenes/props_room.tscn`) boot as F5 runs it, holds the scene's own camera for 45 frames, moves that camera once around the point it looks at (−0.3, 0.25, 0) at its own radius (4.6 m) and height (2.2 m) over 600 frames, holds 45 frames at home, and quits. It changes no prop, light, floor or material.

```bash
HOME="$SCRATCH/home" Godot --path godot --resolution 3840x2160 --write-movie frames/orbit.png --fixed-fps 30
ffmpeg -framerate 30 -i frames/orbit%08d.png -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 30 orbit-01.mp4
```

Movie Maker wrote 691 PNG frames (3840 × 2160) and a WAV that is digital silence (peak 0): the scene has no sound. The PNGs were encoded once to H.264; the MP4 has 691 frames, checked with `ffprobe -count_frames`. Run log: `capture/orbit-01-run.log`. Movie Maker renders offline at a fixed step; it is not evidence of real-time frame rate.

**On screen:** every frame carries `GODOT 4.7.2 · MOVIE MAKER · NATIVE 4K ENGINE CAPTURE · orbit-01 · frames 0–690` and `CAMERA ORBIT ADDED FOR THE FILM · props, light and floor untouched`. No frame was sped up, slowed, cropped or held.

## 2 · The headless check: `capture/checks-pass.log` and `capture/checks-fail-diagnostic.log` (B13, B15)

A second isolated copy of `godot/` (no autoload), imported with its own `HOME`:

```bash
timeout 120 Godot --headless --path godot --script res://tests/check_props.gd --fixed-fps 60
```

- **Pass run:** 44 `ok` lines, `PASS: 0 failed check(s)`, exit 0. Apart from the header line, identical to `evidence/check_props-2026-10-13.txt`.
- **Diagnostic run:** the copy's `scenes/props_room.tscn` had the waystone's transform Y changed from 0 to 0.3 (`capture/fail-diagnostic.diff`), nothing else. Result: `FAIL  Waystone sits on the floor (lowest point 0.3000 m above the floor's top)`, `FAIL: 1 failed check(s)`, exit 1. Labelled DIAGNOSTIC on screen. The project's scene was never changed.

## 3 · Blender images: `blender-looks/` (B05–B09)

There is no screen recording of the Blender session. The Blender images in the film are of two kinds, labelled on screen:

- **shuai-z's own screenshots** (B04): `evidence/blender-notes-cube-selected.png`, `evidence/mcp-panel-connected.png`.
- **The MCP's `look` tool**, called by Claude during the build session on 2026-10-13. The tool returns the image into the conversation; `tools/extract_looks.py` decoded them unchanged from the session transcript into `blender-looks/` (files 1 and 3–8). They are Blender's viewport in material preview, auto-framed; Claude captured them, not shuai-z.

| File | Captured (EDT) | What |
| --- | --- | --- |
| `1-built-rectangle.png` | 19:58 | the waystone as built to revision 1, before the hand edit |
| `2-after-hand-edit.png` | 22:26:56 | see below |
| `3-trial-R.png` | 20:09 | the R trial (after the hand edit) |
| `4-trial-ring-8.png` | 20:15 | the 8-sided ring, in answer to the 20:14 prompt |
| `5-ring-12.png` | 20:18 | 12 sides, thinner band |
| `6-waystone-joined.png` | 20:43 | the joined waystone |
| `7-teleport-circle.png` | 21:02 | the teleport circle |
| `8-spikes.png` | 21:18 | the spikes |

**The hand edit (option b, chosen by shuai-z).** No image was taken between the hand edit and the R trial, so for the "after" still Claude copied `evidence/waystone-after-hand-edit.blend` to a scratch folder (byte-identical, SHA-256 `68079e9d4555d9651dee87f83f41c5984018e5ab60d60dd21bf3b5ec3623299d`), opened the copy in the same Blender through the MCP, read the rune back (`Waystone_Rune` at (0.0, −0.185, 0.4537), 0.2 × 0.02 × 0.3 m), and called `look` with the same arguments as the 19:58 call (angles: front, right, top, three-quarter; material; 768 px). Then it reopened `blender/spikes.blend`, which had been open and saved, and did not save anything. The film shows the front tile of each, labelled as comparison stills, not a recording.

## Hashes (SHA-256)

```
64019404a14b8841803a0a0f4721bd361836d48861bcccb0609b569def1a931c  capture/orbit-01.mp4   (not in git)
28229bfa5a5443f55e1d56f5f4387c7d9210de0376a7ba49f70302a1505fdf24  capture/checks-pass.log
4d319221d6c78e1fa45f7cf8ded374ee1e4ea95eacb11f1982cf518ebe9dc61b  capture/checks-fail-diagnostic.log
670821e020cef91f3b80ad418c477da762c029f08fc408018e443b3c670bd3b3  capture/fail-diagnostic.diff
9d15da2af6b29359fc52c44762b09a813ba52e75c9c74df567b06c3d1127d6a3  capture/project.godot.diff
a1efdc3b9f154790e57194611d9f4d6c99cb25a6fb029cb8315fc3bebd5c828c  capture/orbit_driver.gd
377b86be6e8c7b8c0238a9f95aebd0f1e4af94bc2d168de4848ec828d50d0236  blender-looks/1-built-rectangle.png
b3e487bf0cd49b89153301bc53d6c2c346b2149928ee74f298d997fa684164a2  blender-looks/2-after-hand-edit.png
b70097d1da4282de37edbfa7a6cb81f53d8e829f0d2a96a62ba3fbde101b5d40  blender-looks/3-trial-R.png
c91057adc0ea696c8efe039925c39debadc1344cfd1e818f03134d30050c0ed3  blender-looks/4-trial-ring-8.png
6a8b0052ad8a2dd7934654d73b4552479e1c659922da8508ac09cd1300055974  blender-looks/5-ring-12.png
56c8fd33febd65b4445c5111ae7597e2311c572adc72c9d3642a42441265ffd8  blender-looks/6-waystone-joined.png
b47a4540e6db546a777045e90d4afb91a98634680fbcdbd954287302023622f7  blender-looks/7-teleport-circle.png
d534d7cbb8b78f50af79f7f8be93d57e02e4a9876ee4fe093ff908ffa25d9413  blender-looks/8-spikes.png
```

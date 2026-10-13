# Planning checks: index of runs

**What this is.** The index of every run that backs a claim in this film: which script, which log, what it asked, what it found, and which runs failed or were inconclusive and are kept anyway. Also how to re-run all of it.
**Why.** Films show only what was really done. The fact-check cites runs as `run-NN`; this file says what each one is, so a reviewer (or the build session) can reproduce any number on screen in one command.
**Found.** Eighteen numbered runs (00 to 17) plus the Shader Lab compile checks, all on Godot 4.7.2 stable (official), Apple M4 Pro, Forward+ unless stated; every pixel result was repeated in the Compatibility renderer (`-compat` logs). One run failed on a wrong probe (run-00) and one was inconclusive by design (run-02, rect cases); both are kept and labelled. Four findings came from running rather than reading: the Rect box ignores the node's transform and counts render pixels (run-10, run-13); a copy only serves shaders on its own canvas layer (run-08); equals against 128 over 255 passes in Forward+ and fails in Compatibility (run-06); and half strength reads 0.216 with HDR 2D on (run-06).

**Vocabulary.** The film calls the painted layer of flat colors a **label map** (the series reserves "mask" for a number from 0 to 1 per pixel; ACTS.md, "Naming"). The Godot node is `LabelMap`. These scripts and logs were written first and still say "mask" in identifiers and field names (`mask_coloured_pixels`, `mask_influence`, `make_mask_image`, case names such as `C2b-mask-OVER-ground`): it is the same layer; nothing here is viewer-facing.

Every log starts with the command, the date and the machine. Each capture, and each Rect-mode case, ran in its **own Godot process** (a Rect-mode copy depends on history). All scripts write only into a scratch Godot project (`/private/tmp/claude-501/godot-shaders-reflections/` for the layout run) and into this folder.

## The runs

| Run | Log(s) | Script | Question | Result |
|---|---|---|---|---|
| 00 | `run-00-expD-first-run-wrong-probe-pixel-FAILED.log` | `exp_d_polish.gd` (first version) | alpha of the final shader over water | **FAILED, kept:** the probe pixel (300, 494) was the reflection's bottom edge and read alpha 0.0. Fixed to the centre (300, 422) |
| 01 | `run-01-expA-copy-order[-compat].log` | `exp_a_copy_order.gd` | What does a window that reads the screen texture see, for each place of a BackBufferCopy? | No node: A, B and C. After C: A, B, C. Between B and C: A and B. Between A and B: A. Before A: nothing. A node after the window changes nothing; a disabled node changes nothing (the automatic copy happens); `move_child` at run time gives the same results as building the tree that way |
| 02 | `run-02-expB-modes-and-readers-INCONCLUSIVE-rect[-compat].log` | `exp_b_modes_and_second_reader.gd` | Copy modes; what a second reader sees | **Rect cases INCONCLUSIVE, kept:** several cases in one process left stale pixels in the back buffer, so a rect that copies almost nothing still looked right. Valid in it: viewport mode, a rect covering the screen, disabled, two readers with no copy node (both miss C) and with a copy node between them (the second sees C, the first does not). The rect cases were redone in fresh processes (runs 03, 05, 10) |
| 03 | `run-03-expB2-rect-outside-fresh-process[-compat].log` | `exp_b2_rect_outside.gd` | What does a shader read outside a Rect box, in a process with no history? | R1 to R3: black (0, 0, 0) in Rect mode, the right colours after the switch to Viewport. R4: with history the same read returns stale pixels instead of black. So every capture runs in a fresh process |
| 04 | `run-04-expC-pond[-compat].log` | `exp_c_pond.gd` | The hidden-label-map reflection in the pond | C1 (good order, four x positions): 16,237 of 16,237 reflection pixels at x 300, 0 at x 880, label-map influence 0 px, 0 label-map-coloured pixels in the final frame. C2a (copy after the art) and C2c (no copy node): 0 of 16,237. C2b (label map over the art): 16,237 and a red-and-green sea (409,604 px changed). C3 (art at 0.9): the reflection still works and the label map shows through faintly (409,604 px changed, largest channel change 0.086; the same number as run-07 E4). Also C1 at x 640 and x 1180 (partly over the coast and the far water): mismatch 0. C5 (90 walking frames): mismatch 0, no flicker, no one-frame lag |
| 05 | `run-05-expC4-rect-fresh[-compat].log` | `exp_c4_rect_fresh.gd` | The pond with the copy in Rect mode, in a fresh process | F1 default box: 0 of 16,237 (the box is a corner far from the water). F2 the same node switched to Viewport: 16,237. F3 a box covering the water, Rect2(0, 300, 1280, 420): 16,237 |
| 06 | `run-06-expD-polish[-compat].log` | `exp_d_polish.gd` | The polish act: alpha, tint, equals against distance, read-back, HDR 2D | D1a alpha 0.509 over water (0.491 in Compatibility); D1c 0.300 on the coast ring (0.297); D1b the default tint is mixed raw, (0.3725, 0.6000, 0.7804). D2a equals against (0.5, 0, 0) on water painted 128: 0 of 16,237; D2b a distance within 0.1: 16,237; D2c equals on pure red works (16,237); D2d equals against 128/255 passes in Forward+ (16,237) and fails in Compatibility (0). D3: pure values read back exactly (1.0 and 0.0), painted 128 reads 0.502. With HDR 2D on (Forward+): half strength reads 0.2158 and the distance test finds none; pure values unchanged; no effect in Compatibility |
| 07 | `run-07-expE-extras[-compat].log` | `exp_e_extras.gd` | The claims around the main effect | E1 hiding the LabelMap changes exactly the reflection's 16,237 px and 0 px elsewhere. E2 Camera2D panned and zoomed 1.4: all 32,251 visible reflection px are on label-map red in screen space, 0 hidden-but-red, 0 visible-but-not-red. E3 jump 80 px: the reflection rises 80 px too, 6,903 of 16,237 px visible, none above the shoreline. E4 art opacity 1.0 / 0.9 / 0.8: largest channel change 0.0 / 0.086 / 0.169. E5 RemoteTransform2D: reflection = player + offset every frame, gap 0.0 px. E6 Inspector wording and defaults from ClassDB |
| 08 | `run-08-expF-z-index-and-layers[-compat].log` | `exp_f_z_index_and_layers.gd` | Does the copy follow z index and canvas layers? | z index puts the label map below the Ground against the tree order: 16,237 (Z1). Label map on layer -1 with the copy on layer 0: 16,237 (Z2). Label map and copy on layer -1 with the reader on layer 0: **0** (Z3). Everything on one layer: 16,237 (Z5). Copy on layer 0, reader on layer 1: **0** (Z6). A copy only serves shaders on its own canvas layer; the docs are silent |
| 09 | `run-09-expG-mirror-the-screen[-compat].log` | `exp_g_mirror_the_screen.gd` | Is mirroring the whole screen a working different technique? | Yes: the pixel at (300, 422) equals the character's (300, 278), (100, 380) equals (100, 320), (100, 550) equals (100, 150) |
| 10 | `run-10-expH-rect-region[-compat].log` | `exp_h_rect_region.gd` | Where does a Rect-mode box actually copy (1:1, 1280 x 720)? Eight cases, each in its own process | The default box copies screen x 0..100, y 0..100 for node positions (0, 0), (100, 100), (500, 300), with scale 2, with rotation 0.5. With a parent at (200, 200) and rect (0, 0, 200, 200) it copies 0..200; rect (300, 300, 200, 200) copies 300..500. The node's transform does not move the box |
| 11 | `run-11-scene-checks.log` | `scene_runner.gd` | Each of the 19 captures, 1:1 route (1280 x 720, scale 1): what is on screen at the probe times and at the 50 % and 85 % marks | The numbers in `CAPTURE-PLAN.md`'s last column; frames in the scratch folder, contact sheet `png/contact-sheet-captures.png` |
| 11b | `run-11b-scene-checks-4k-route.log` | `scene_runner.gd` | The same 19 captures on the 4K route (a 3840 x 2160 SubViewport over the 1280 x 720 canvas, scale 3) | Same probes (see run-14) |
| 12 | `run-12-editor-project-verify[-compat].log` | `make-editor-project.sh`, `verify_scene_file.gd` | Build the editor project (a real `pond.tscn`) and check that it behaves like the scripted scene | Tree order `LabelMap`, `BackBufferCopy`, `Ground`, `Player > RemoteTransform2D`, `Reflection`; copy mode Viewport; Flip V on; 16,237 reflection px at x 300, 0 at x 880; both renderers |
| 13 | `run-13-expI-rect-region-4k-route[-compat].log` | `exp_i_rect_region_4k.gd` | Experiment H again on the 4K capture route | **The Rect box counts render pixels:** the default box copied 101 x 101 render pixels, only 34 x 34 canvas units, whatever the node's position; rect (0, 0, 300, 200) copied 301 x 200 render pixels (100 x 67 canvas units); rect (300, 300, 200, 200) copied 299..501. Both renderers. Consequence: C08 (the only Rect-mode capture) is recorded 1:1 |
| 14 | `run-14-route-comparison.log` | `compare_routes.py` | Do the 19 captures give the same probes on both routes? | 65 probes over 19 captures, 65 equal within tolerance, 0 different, 0 missing. None of this film's shaders reads a pixel count (`SCREEN_UV` only) |
| 15 | `run-15-retime-length.log` | `scene_runner.gd --length` | A capture recorded at a different length than planned (audio first): do the probes move? | No. C07 at 15, 12 and 19 s: the same zone labels at 50 % and 85 % of the clip. C11 at 12.5, 9 and 14 s: the same states; the reflection pixel counts differ by 3 to 4 % only because the walker's position is rounded to a 30 fps frame (681.4, 680.4, 680.4). 12 s of a 15 s scene writes exactly 360 frames |
| 16 | `run-16-gate-t-ink-precheck.log` | `gate_t_ink_precheck.py` | Could anything in a capture be read as text by GATE T? The toolkit's own ink mask and blob functions (`type_check.py`, imported read-only) run on the 50 % and 85 % frames of all 19 captures at 3840 x 2160 | 38 frames, 0 text-run blobs. 32 frames have no pixel within 48 RGB of ink or mute at all; C08 at 50 % has one 675-pixel blob (the 3-px blended edge of the corner patch) that the filter rejects as not text-like; the red-filled frames (C02, C03, C13 at 85 %) flip the detector's polarity to dark if a capture fills the frame edge to edge, so the final layout must keep the cream margin around the window. The raw captures carry no text, so this says nothing about the final composition: GATE T on the real frames is the build's job |
| 17 | `run-17-capture-all-end-to-end.log`, `png/contact-sheet-recorded-clips.png` | `capture_all.sh`, `verify_recorded_clips.py`, `capture_contact_sheet.py` | The whole capture pipeline end to end: all 19 clips recorded at their beats' estimated lengths, each in a fresh Godot process | 19 of 19 clips are 3840 x 2160, 30 fps and exactly length x 30 frames (276 to 417 frames); the scenes play 5 to 16 % faster than planned (time scale 1.05 to 1.16), so no `retime_warning`; 12:59.96 with the machine busy (load average about 10), so budget 10 to 15 minutes; the 50 % and 85 % frames of every clip were looked at on the sheet and match the last column of `CAPTURE-PLAN.md` |
| Lab | `lab-results.jsonl`, `png/` | `run-lab-checks.sh` through the series' `check_shader.sh` | Do all five shaders compile in the real Shader Lab (Godot 4.7.2 window), in both renderers? | Eight rows, all exit 0. On the Lab's empty stage the reflection shaders hide themselves (no red anywhere): the expected result there. The Lab cannot add a second node or a BackBufferCopy, so behaviour is checked by the runs above |

## Frames kept

- `png/planning-frame-E1-scene-dock.png`, `png/planning-frame-E2-inspector-copy-mode.png`: crops of the real Godot editor (Light preset, Movie Maker, scratch project) from a trial of `record-editor-frames.sh`. The film's frames are re-recorded by the build; the crops show where the ring boxes in the lanes were measured.
- `png/contact-sheet-captures.png`: the 50 % and 85 % frames of all 19 scenes on the 1:1 route (planning evidence, not film assets).
- `png/contact-sheet-recorded-clips.png`: the 50 % and 85 % frames of the 19 recorded 4K clips (run-17; C08 is the 1:1 route enlarged 3x).
- `png/*.png` from the Lab: one probe each, every shader.

## Tools

| File | What it does |
|---|---|
| `pond_common.gd` | One geometry (grass band, straight shoreline, half-ellipse sandbar with a 40 px coast ring), the label map and the art generated from it, the test character, `build_pond` |
| `capture_scenes.gd` | The 19 capture scenes as data plus a small timeline (`setup`, `build`, `tick`); durations in `TABLE` |
| `scene_runner.gd` | Plays one scene, prints probes at chosen times (`--times 3,50%,85%`), dumps frames; `--route direct\|sv`, `--scale`, `--length`, `--all-frames`, `--full`, `--limit` |
| `capture_scene.sh` | One capture to a 3840 x 2160 30 fps MP4 in a fresh process (1:1 then 3x for C08, the 4K route for the rest), `--length` |
| `capture_all.sh`, `capture_list.py` | All 19 at the length of their beats (measured audio when `beat_sheet.json` has it); `--only`, `--dry-run` |
| `capture_contact_sheet.py`, `verify_recorded_clips.py` | The 50 % and 85 % frames of every recorded clip on one labelled sheet (LOOK before using a capture); size, rate and frame count of every clip |
| `make-editor-project.sh`, `make_editor_project.gd`, `verify_scene_file.gd`, `record-editor-frames.sh` | The editor project for E1 and E2, its check, and the Movie Maker recording of Godot's own editor (Light preset through a scratch HOME) |
| `compare_routes.py` | Compares the probes of two routes (run-14) |
| `gate_t_ink_precheck.py` | The GATE T ink-mask pre-check of all captures (run-16) |
| `contact_sheet.py` | The contact sheet |
| `run-all.sh`, `run-lab-checks.sh` | Re-run everything (below) |

## How to re-run

From this folder (needs `godot` 4.7.2 and `python3`; `ffmpeg` only for `capture_scene.sh`). Everything lands in a scratch project and in this folder; set `PROJ` to choose the scratch project.

```bash
./run-all.sh all            # runs 01 to 16 and rewrites the logs (about five minutes: 5 min 14 s measured)
./run-all.sh experiments    # runs 01 to 10 and 13
./run-all.sh scenes         # runs 11, 11b, 14 and the contact sheet
./run-all.sh route          # runs 11b, 13, 14 only
./run-all.sh editor         # run 12
./run-all.sh retime         # run 15
./run-all.sh gatet          # run 16 (renders 38 frames at 3840 x 2160, about a minute and a half)
./run-all.sh record         # run 17 (all 19 clips end to end, 10 to 15 minutes; not part of `all`)
./run-lab-checks.sh         # the Shader Lab compile checks (serialised by the Lab's own lock)
```

## What is not here

No timing of a copy (the cost was never measured, so the film makes no speed claim). No real-time frame rate (captures are offline at a fixed tick rate). No GPU figure. No recording of anyone's screen: Godot's own frames only.

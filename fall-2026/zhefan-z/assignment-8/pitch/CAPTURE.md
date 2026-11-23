# CAPTURE — real footage in the pitch film

Written by Claude Code, 2026-11-22. Three sources of real captured play; two were recorded for this film, one is reused unchanged. Everything else on screen is a still card (CONSTRUCTED, GENERATED or a FIGURE FROM THE LOGS), labelled as such.

## capture/run-01 — the game today, revision 840b501 (new)

| | |
|---|---|
| Game | `fall-2026/zhefan-z/assignment-7/walker-magic-zhefan` at **840b501** (`840b501d645178013115beb0883764d69e5e9552`, tree `99aa39e2c1bb0dd0d14d4c9a8c01a8efee067296`), from `git archive 840b501:<path>` into a scratch folder outside the repository, copied, then `godot --headless --import` once (exit 0, no error lines). The working tree was not run or changed. |
| Build ID (coverage.json) | `964c57fecefd0aaf2c4a2394765552baaf71a0a47d9ba6e26671b8f88956aba6` = SHA-256 of the output of `git ls-tree -r 840b501:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan` (a content hash of every path and blob in the snapshot; reproducible, unlike the tar's timestamps). |
| Engine | Godot 4.7.2-stable (official, win64 console build `ed1daf0bf`), Forward+, NVIDIA GeForce RTX 5060 Laptop GPU, Windows 11 |
| Driver | `capture/driver.gd` — the Assignment 7 film's driver, **byte-identical** (SHA-256 `ef89771ef9cc67736755eb702024bf4fb67460f3bf6da799a87099a96129f960`, as recorded in that film's CAPTURE.md at 840b501). Scripted input only: key events (D, A, Space) and mouse motion plus a left click through `Input.parse_input_event`; it observes states to choose inputs and never moves a character or sets a game value. Not a human playtest. |
| Recording | Movie Maker, **windowed**: `--write-movie <frames>/frame.png --fixed-fps 60 --resolution 1280x720 --quit-after 4000`. 2739 frames (0–2738) of the game's 640×360 canvas, 45.65 s of game time, recorded in 5 min 12 s. Offline rendering at a fixed step: not evidence of real-time frame rate. |
| Command | `godot --path <capture copy> --script <reel>/capture/driver.gd --write-movie <frames>/frame.png --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- <reel>/capture/run-01-inputs.jsonl <reel>/capture/run-01-frames.jsonl` |
| Result | exit 0; all five driver expectations true (`run`, `lunges`, `cancel`, `lunge_hit`, `recover_hit`; `"failures": []`). |
| Logs | `capture/run-01-inputs.jsonl` SHA-256 `3bb51e9b5f4d42bdca44c6fb2298f9c145a466903ef38b0a979604d51c169491`; `capture/run-01-frames.jsonl` SHA-256 `71a96586617146f5019af07ac4dbfdde7cc1099f8c3260a37e8b4e2f82b7bac7`. Both are **byte-identical to the Assignment 7 film's run-02 logs** (the SHA-256s recorded in its CAPTURE.md for the capture at ad7935f): no game script or scene changed between ad7935f and 840b501, and the run reproduces tick for tick. |
| Archive | `capture/run-01.mp4`: the 2739 frames scaled ×6 nearest neighbour to 3840×2160 (an exact integer multiple of the 640×360 logical canvas, so every game pixel becomes a 6×6 block), lossless (libx264rgb, crf 0), 60/1. SHA-256 `1c9d596cba2cd450fa29be87c56117212a01456fb0c26164e581bbcd9ef94a69`, 1.76 GB, kept out of git. This is the capture `coverage.json` hashes; the godot-waikthrough checker requires a 3840×2160 capture. **Disclosure:** the game renders a 640×360 canvas; the 4K archive is crisp integer scaling of that canvas, not a native 4K render. |
| Used in | B00 (cancel segment, frames 1380–1619 real speed, 1520–1590 replay ×0.25), B08 (lunges 860–1088, cancel 1400–1619 real speed, 1524–1560 replay), B15 (run 140–439 real speed), B01 (frame 15, the title card's background) |
| Audio | Movie Maker's `frame.wav` is not used; the narration is the only sound. |

Harness disclosures (unchanged from the Assignment 7 film): `Main.test_mode = true` so a fail would not reload the scene under the driver; the game runs inside its own 640×360 SubViewport shown 1:1; the crosshair is parked top right at each segment start; frames 441–442, 1089–1090, 1620–1621, 2178–2179 and 2736–2738 are empty gaps between segments, and `scripts/footage.py` refuses to show a flat frame.

Timeline used by the film (from the logs): the wolf growls at 1528 in the cancel segment, the fireball is cast at 1530, the hit lands on 1549 with the wolf in GROWL the tick before and RECOVER on the hit tick (wolf HP 2 → 1, no lunge, hitbox never armed); in the lunges segment the wolf growls again at 970, is facing right from 972, lunges and hurts the mage on 1009; in the run segment the mage starts running again at 153, takes off at 301 and lands at 346.

## capture/a5-run-01 — the Assignment 5 hurt tint, revision 2b68e0a (new)

| | |
|---|---|
| Game | `fall-2026/zhefan-z/assignment-5/walker-magic-zhefan` at **2b68e0a** (`2b68e0ac04fa1259ef1a77bf314205bc7bc3146e`, tree `f499a0ff76f686b229b562340ce4b5c2f50ccb99`), `git archive` into scratch, imported once (exit 0). Content hash of `git ls-tree -r` of the tree: `d7532cda821091d5a3d710a21beae2ae05b9e4718db3bc9879415810cf439bfb`. |
| Driver | `capture/driver_a5.gd`, adapted by Claude Code from `capture/driver.gd`: the same harness, with the clip, afterimage and hitbox fields removed (they did not exist at 2b68e0a). One segment: walk right, jump the pit, keep walking at the wolf after it growls so its lunge lands, then step back (A) to x ≤ 620, out of its sight. It reads the hurt-tint shader's `intensity` uniform for the frame log; `hurt_tint_driver.gd` sets it. |
| Trials | Three headless trials (logs in the scratch folder, not used): the first two failed their expectation (a `null` uniform before its first write; the wolf hit twice because the mage stayed in reach); the driver was fixed for both, and the third trial and the take passed. |
| Recording | Movie Maker, windowed, `--fixed-fps 60 --resolution 1280x720 --quit-after 2000`: 690 frames, exit 0. Expectation `hurt` true: one hit on frame 473 (HP 5 → 4), tint above zero for 59 frames (max 0.9833, back to 0 by frame 534), no fail. |
| Logs | `capture/a5-run-01-inputs.jsonl`, `capture/a5-run-01-frames.jsonl` (committed) |
| Archive | `capture/a5-run-01.mp4`, 640×360 lossless, SHA-256 `d8280a3c2cabe9e9ccab98bf5a7680d1f1d932f38c0d40afb5388c98a9ca2219`, kept out of git |
| Used in | B13 (frames 420–560 real speed, 470–520 replay ×0.25), labelled "Real capture · scripted input · revision 2b68e0a (Assignment 5)" |

## The Assignment 6 capture, revision 3c37fe0 (reused, unchanged)

The Assignment 6 film's `capture/run-01.mp4` (scripted input, windowed Movie Maker, 30 fps, game at **3c37fe0**), recorded and described in that film's CAPTURE.md at 7672d5a. Read from its untracked place in the working tree; SHA-256 checked by `scripts/footage.py` against the recorded `81f207048bb51d6370cc461ba0c00b4c4a4c37d60ca1fac6e240403c23322e80` before use. `git diff 3c37fe0 7672d5a` over that project, excluding documents, tests, previews and film records, is empty, so it shows the particles as submitted. Used in B14 (frames 230–524 at real speed: shots into the wolf, the ground and rapid fire), labelled "Real capture · scripted input · revision 3c37fe0 (Assignment 6)". It is not in `coverage.json` (a different build).

## How the film uses footage

`scripts/footage.py`: each gameplay beat plays its interval once at real speed (60 fps captures: every second frame; the 30 fps capture: every frame), then, where named, a ×0.25 replay of part of it labelled "Slowed replay ×0.25 of the same capture", then the last frame held and labelled, to the exact frame count of the beat's measured narration, so the compiler neither retimes nor cuts it. The canvas is enlarged ×5, nearest neighbour. Chips under the action are read from the frame and input logs and drawn outside the game image. Provenance per beat: `evidence/footage-provenance.json`.

## Added 2026-11-22 — rebuild from the GDD (prompt-2-gdd.txt)

Written by Claude Code. The sections above describe the first cut and stay as written; its beat names (B00–B17) no longer exist. The rebuilt film's per-beat spans are in `evidence/footage-provenance.json`.

### capture/run-02 — losing to the pit, revision 840b501 (new)

| | |
|---|---|
| Game | the same isolated copy of 840b501 as capture/run-01 (build ID `964c57fe…`), so `coverage.json` lists both captures under one build |
| Driver | `capture/driver_fail.gd` (SHA-256 `89447b5aa4a23c700e9bbdc46f0e451abc00362bfceec58c9fad35c4cb220027`), adapted by Claude Code from `capture/driver_a5.gd`. One segment, "pit": D held from the start, no jump, so the mage walks into the pit. Key events only; it never calls `fail()` or sets a game value. `test_mode` keeps the fail from reloading the scene under the driver; the HUD's fail message is shown before that return, as in a normal run. |
| Trials | Two headless trials (logs in scratch, not used). The first failed its own expectation although the fail happened: a GDScript lambda cannot assign an outer local, so the logged reason came back empty; the reason is now stored in the driver's `seen` dictionary. The second trial and the take passed. |
| Recording | Movie Maker, windowed, `--fixed-fps 60 --resolution 1280x720 --quit-after 1500`: 390 PNG frames (0–389), one per frame-log row; exit 0. Movie Maker's summary line printed "386 frames"; the frame files and the log both count 390. |
| Result | expectation `pit` true: FALL from frame 277, fail on frame 291 with the reason "Fell into the dark" (the HUD shows it), state FAIL, HP 5, no hit. |
| Logs | `capture/run-02-inputs.jsonl` SHA-256 `a86d9689f8b9f33d5539bd8de05af5ae57e4bd7ad0d4b47111b5a0707e7b6ecf`; `capture/run-02-frames.jsonl` SHA-256 `42bbb66c348a172f4a2f78e117df96b8760a06b1870c75ff804ec76f6436395b` |
| Archive | `capture/run-02.mp4`, ×6 nearest neighbour to 3840×2160, lossless, SHA-256 `0544cfdfbd9de149adcabf04bf413a455af27c112e80c84200c044fb47c7632e`, 243 MB, kept out of git |
| Used in | G04 (frames 240–385, real speed). The level reload that follows a fail in a normal run is not shown (skipped by `test_mode`); the narration states it from `main.gd` (`_on_player_failed` reloads the scene after `RELOAD_DELAY`). |

### The Assignment 3 prop scene, revision 840b501 (new render)

`res://showcase3d/prop_room.tscn` in the 840b501 copy, rendered with Movie Maker (windowed, `--fixed-fps 30 --resolution 1920x1080 --quit-after 30`; Godot recorded the project's 640×360 canvas). Frame 20 is kept as `capture/props-840b501-frame20.png` (SHA-256 `9585b565a58ebf97f3df311625048801c8940b721dce2c1a6d5e1371196bc2c9`). It shows the rock, crystal and chest from Assignment 3 and, as that scene's scale reference, the mage's idle sprite as a billboarded `Sprite3D`. Used in G10, labelled as a real render at 840b501.

### Reuse in the rebuild

- capture/run-01 (840b501): G04 (run 15–439, jump replay 280–350, cast 1500–1560), G05 (lunges 860–1088, cancel 1400–1619, lunge hit 2040–2148, with ×0.25 replays), A01 (run, lunge, cancel beside the exists-today list), P01 (frame 1544, still), G10 (frame 15 crop, still).
- capture/a5-run-01 (2b68e0a): Q07B, as in the first cut.
- The Assignment 6 capture (3c37fe0): Q07C, as in the first cut, SHA-256 checked again.
- G11's sound is not a capture: it is the game's own audio files at 840b501, listed in `evidence/audio-excerpts.json` and SOURCES.md.

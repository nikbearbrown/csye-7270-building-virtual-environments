# BUILD-PROMPT: Local, World and Screen Space (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, 17 tested shader files and the reference scenes that were run and probed. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it.
**Found.** Layout is complete and lint-clean: 46 beats (40 body), 1,770 spoken words, about 10.1 minutes estimated at Liam's measured pace. Body lanes: 24 Manim, 12 ShaderLab captures, 1 editor capture, 1 terminal log, 2 Remotion cards. Nothing is voiced, recorded, rendered or published. The editor frames E1 (and the optional E2) were recorded by script on 2026-10-13 and FACTCHECK row 23 cites them. Items that need a human: the playlist name (none yet).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`
Absolute path of the film folder: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space`.

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/evidence/planning-checks/RESULTS.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `BUILD-LOG.md` "Mistakes worth not repeating"), and, if it has been built, `claude-liam-lecture-godot-shaders/` (its `BUILD-LOG.md` and its `ShaderLab`).

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the three shared pieces (reuse if they exist, build once if not)

Check first: `./brutalist.art/art scenes --check ShaderLab`; `ls $S/shader_kit.py`; `ls $S/lab/capture.gd $S/lab/capture_shader.sh`. If the Godot Shaders film has been built, all three exist: reuse them and do not edit them. If not, build them from `S/COMPONENT-SPECS.md` (the only place you may edit the toolkit is `ShaderLab`: one file plus its registration, then `./brutalist.art/art scene-index`; say so in `BUILD-LOG.md`). Then add the **four film-local Manim helpers** this film needs (put them in `R/_kit_cast.py`, pasted above the scenes like `shader_kit.py`): `world_window_scene` (world rectangle, window frame, sprite with the corner dot; B03 to B07 and B26 to B34 reuse it), `origin_marker` (a ring with a right arrow and a down arrow), `address_tag` (a number pair attached to a point that can count), `matrix_table` (4 by 4 outline cells, one column or row highlightable). Cell outlines with padding, never fills behind text.

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01 to C11b from the reference scene builders in `R/evidence/planning-checks/` (`scenes_lib.gd`, `sky_lib.gd`; the probes that proved each scene are `verify5.gd` to `verify8.gd`). Use the shader files in `R/lab-shaders/` **unchanged**. Compare each capture against the "verified result to reproduce" column; if a probe disagrees, stop and report (do not edit the shader).
- **Two capture routes (the series rule of 2026-10-13; `R/CAPTURE-PLAN.md` "Canvas and route" has the detail).** Each scene script's `route()` says which: C01 to C09, C11a and C11b use the 4K route (3840 by 2160 SubViewport over the 1280 by 720 logical canvas; `verify8.gd` R1 shows what it does to the numbers); **C10 uses 1920 by 1080 at scale 1** (a SubViewport of 1920 by 1080, no override, the scene laid out on that canvas) because shaders 10, 12 and 13 read window pixels. Check C10's frames against the table (worst difference 0 of 255 from the exact gradient; `verify12.gd` C10 and `verify13.gd` are the reference). No Godot `Label` nodes anywhere; words are ShaderLab readouts.
- Sky texture 1536 px (`sky_lib.make_sky(1536)`, seed 7); blob `scenes_lib.blob_texture(256, true)`; `amount` is set from code before it is tweened (C09).
- B14: re-run `broken.gd` in a scratch project (`godot --path . --script res://broken.gd`) and put its output on `CCPlainShell` verbatim, trimmed of the GDScript backtrace. The output includes one line the script prints itself, "fragment() runs once for each pixel the shape covers; sets its color": it is the definition of fragment on screen where the voice first says the word, so keep it. The lane's `lineCues` and `rings` are frames laid out for the estimated 13.6 s: after the audio is measured, scale them by (measured seconds / 13.6) and keep every cue out of 45 to 55 % of the beat (the error line and its ring settled before 45 %).
- B31: `D2`, the docs screenshot with Playwright (1600 by 900 at 2.4); then set the ring box in the lane's second move round the sentence about (1.0, 1.0).
- Editor frames E1 (and the optional E2) are **already recorded by script** (CAPTURE-PLAN section "Editor frames"); nobody clicks or records by hand. Copy the clean-root pair `local-world_E1-1_child-selected-clean-root.png` and `local-world_E1-2_parent-selected-clean-root.png` from `S/editor-capture/png/1920x1080/local-world-and-screen-space/` (native twins in `png/3456x1944/local-world-and-screen-space/`) and cross-dissolve them at 0.58 of the beat's measured audio into `TK/runtime/remotion/public/local-world-and-screen-space/editor-parent-child.mp4`, exactly as the B11 lane's `capture_spec` says (whole frames; the ring boxes are fractions of the 1920x1080 frame). Label the clip "scripted editor session". Do not use the plan-exact pair (its root shows a warning triangle). Never draw an Inspector that claims to be live: if you must change a frame, record it with the driver (`S/editor-capture/README.md` section 7; copy `S/editor-capture/state-scripts/final/local-world-E1-clean-root.json`). Row 23 already cites these frames; if a frame you record differs, stop and report.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_MoveTheZero`, ..., `B40_TwoMoves`: 24 classes), implementing each `visual_intent`, `motion_claim` and `show` cue in `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` and the film-local helpers. Use the exact numbers in the lanes (they were measured; do not recompute): (-64,-64), (536,336), (286,236), (186,236), (-64,-64,0,1), (600,400), (512,232), (-88,-168), (286.5,236.5), (0.2238,0.3285), 128 and 256. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6).
   **Definitions on screen (GLOSSARY wording, word for word; the lanes say where).** A term is defined where the voice first says it. Manim beats draw the definitions as small outline cards or labels (ink on a pale ground, never terracotta text): B03 ('screen space: pixels of the window, counted from the top left, y growing downward'), B08 ('vertex(): runs once for each vertex; places the corners' with the run counter, and 'built-in: a value the engine hands to a function, or collects from it'), B09 ('matrix: a grid of numbers that moves a point when you multiply by it'), B12 ('vector: a bundle of two to four numbers'), B15 and B17 (the varying and UV cards; UV is spelled `UV` on screen), B18 ('texture(sky, address): reads the sky picture at that address'), B39 (the two small grey labels for `fract` and `step`, which are not spoken). ShaderLab cue `label`s (at most 60 characters, rendered on the highlighted line, per `S/COMPONENT-SPECS.md`) carry B20 (`repeat_enable`, `repeat_disable`), B23 (`TEXTURE_PIXEL_SIZE`), B24 (`distance`, `discard`) and B25 (`amount`, `mix`). The terms card (BDEFS) has six prerequisites: Shader, Pixel, Origin, Space, Vertex, Texture.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). Lanes come from `R/_gen_lanes.py`: if a lane must change, edit that file, run it, then `make_sheet.py`, **before** any audio. **Never re-run `make_sheet.py` after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for "vec four", "frag coord", "U V", "twelve-eighty by seven-twenty", "model matrix", "canvas matrix", "discard", "varying", "repeat enable", "Godot". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: 85 rows, none OPEN; row 23, the Inspector's wording, is passed on `verify11.gd`'s property list and E1 only supplies the picture), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and ones this film adds)

- GATE T: ink-colored rings and dark small shapes beside mid-tones fail; ring with grey (`#8F8A7B`). Terracotta is never text. The sky is mid-tone indigo, the blob teal, the stripes white and teal, the four-tile gradient saturated (no near-black field): none should fail, but check the 50 % and 85 % frames of every capture.
- Gate V underfill: Manim beats are declared sparse in the lanes; ShaderLab beats are not. A capture must never be cropped past the window edge.
- A Pango `Text()` may drop single spaces on this Mac: code lines such as `(MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy` need explicit coordinates and a look at the still. Draw every arrow as a shape (the `->` glyph is under the type floor).
- Dark ink shapes packed together fuse into a text blob: draw bars and cell outlines in greys.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted motion ("scripted run" is in every `videoLabel`).
- In the 4K route screen-pixel built-ins count 4K pixels (3x). This film shows no screen pixel number read from a capture, and C10, whose shaders read window pixels, is captured at 1920 by 1080 at scale 1; if a capture ever has to show a pixel count or a pixel-valued radius or width, it goes on the 1920 by 1080 route too, and its readout says the window size.
- B11's ring boxes and B31's ring box are placeholders until the frames exist: set them from the real images.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example the Inspector wording), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not edit `lab-shaders/` (they are the tested files shown on screen), `lanes/` by hand, `evidence/planning-checks/` (add new evidence beside it instead), any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, and any editor action that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

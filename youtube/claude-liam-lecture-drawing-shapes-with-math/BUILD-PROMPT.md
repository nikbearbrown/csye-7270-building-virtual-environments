# BUILD-PROMPT: Drawing Shapes with Math (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, with estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, and 17 shader files (one fails to compile on purpose) with their logs. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses the three shared pieces the shader-series pilot builds (the `ShaderLab` component, `shader_kit.py`, the capture harness); it needs a few small additions to them (Phase 0): a square result window, square output, and readouts that replace each other.
**Found.** Layout is complete and lint-clean: 50 beats (44 in the body), 1,900 words by the lint's count, about 10.8 minutes estimated at Liam's measured pace (the lint figure is a ceiling). Nothing is voiced, recorded, rendered or published yet. Every cue, readout, ring, Manim event and sweep breakpoint in `lanes/` is an estimate placed from the words, and Phase 1 replaces each with the measured time (one command); the few that are fixed on purpose are named in Phase 1. Open items that need a human: the editor frames E1 only if the proven driver fails for the three states (Phase 2), and the playlist name (none yet; never type one).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`
Absolute form of `R`: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (what to build first), `S/GLOSSARY.md` (the small words `step`, `alpha`, `band`, `abs`, `mask`, `hint`, `max` have fixed on-screen wording; this film's labels already use it).
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"). And the shader-series pilot `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/`: if it has a `BUILD-LOG.md`, read it (it built the shared pieces).
6. `TK/docs/MATH-TYPESETTING.md` (B04 has an equation) and `TK/docs/EXECUTABLE-EVIDENCE.md` (every number on screen is computed, never drawn from memory).

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (they may already exist)

Check first: `./brutalist.art/art scenes --check ShaderLab`; `ls $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh`. If all exist (the pilot was built), go on. If any is missing, build it from `S/COMPONENT-SPECS.md` first (see the pilot's `BUILD-PROMPT.md`, Phase 0), keeping the toolkit change to the one `ShaderLab` file plus its registration, then `./brutalist.art/art scene-index`.

This film needs these **additions** to those pieces (log each in `R/BUILD-LOG.md`):

1. **A square result window in `ShaderLab`.** Every Godot result in this film is 1:1 (the spec shows only 16:9). Add an optional prop (for example `resultAspect: "1:1"`, default `"16:9"`), or an `imageAspect` as `BrowserCapture` has. The window must be centred in its half in the `side` layout and centred on the stage in the `video` layout. Cue lines index into the DISPLAYED `code` (1-based), which is a slice of the shader file for B35 to B42 (the card names the file's line range). Cue `label`s (at most 60 characters) and the one-line `caption` (at most 80) must be rendered: this film defines `Color Rect`, `distance`, `alpha`, `hint`, `mask`, `min`, `max`, `abs` and `function` that way.
2. **Readouts.** `(x, y)` is the centre of the readout's pill in the window's own 0 to 1 coordinates, ink on a pale ground; a readout at the same `(x, y)` **replaces** the earlier one (B10, B18, B19, B23 and B40 to B43 rely on it: `mask −1` becomes `mask 0`, `max gives 1` becomes `adding gives 2`). The status readouts sit at (0.2, 0.06), the top-left of the window, which is clear of every shape in this film; clamp a pill inside the window if its text would cross an edge. The `video` layout must also carry `title` (B01) and `caption` (B01).
3. **Square output**: logical canvas 1080 by 1080, rendered 2160 by 2160 through the SubViewport native-size route.

The rest this film needs is already in the spec: `--animate` piecewise schedules, `--steps` (C24), `--set-at`, keyframes as fractions with `--length SECONDS`, and `--scene PATH.gd` (C20's two backdrops).

## Phase 1: voice first (free), then the word clock

The captures and every on-screen cue are timed to the measured audio, so generate it before recording anything:

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/runtime/scripts/align.py $R                              # the word clock: mp3/words.json, one entry per word of the narration (faster-whisper timing, free)
python3 $R/_gen_lanes.py && python3 $R/make_sheet.py                           # every cue, readout, ring and Manim event time now comes from the measured words
python3 $R/_gen_lanes.py --times                                               # estimated against measured fraction of every phrase, and the sweep breakpoints in the harness's own syntax (Phase 2)
```

`_gen_lanes.py` reads `mp3/words.json` and the measured length of each beat by itself; where a beat has no usable word clock (align.py prints `NO anchors`, or the narration changed) that beat keeps its estimate: report it. The times that stay fixed on purpose: a beat's first cue (2 %), the readout 'predict first' (2 %), the readouts 'arms off' and 'arms alone' (10 %), and the hook's pause across 44 to 56 % in C01 (the 50 % frame must be a hold). The generator still keeps the two rules that protect the sampled frame: **no cue, readout or ring starts between 45 and 55 % of a beat**, and **no Manim motion starts between 30 and 56 %** except a quick one (0.35 s at most, done by 44 %, marked `[quick]` in the lane's `show` list). If a line of the lint or the generator prints `TIMING / SIZE PROBLEMS`, fix that cue in `_gen_lanes.py`, never by editing `lanes/*.json` by hand.

Read each beat's `actual_duration_s` from `R/beat_sheet.json`; those are the `--length` values of the video captures. Voice check now (transcribe with faster-whisper and compare to `narration.py`): listen for "U V", "Hallo", "step", "abs" (it rhymes with "tabs"), "min", "max", "alpha", "uniform", "Godot", "Color Rect", "Inspector", "three hundred eighty-four", "two hundred sixteen", and that the beat is not padded by long pauses where a clause ends in a colon. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Phase 2: record (CAPTURE-PLAN.md)

- Render C01 to C24 into `TK/runtime/remotion/public/godot-shaders/drawing-shapes/` with the names the lanes use, **on a default project (2D HDR off), Forward+**. Video timelines are fractions of the clip (CAPTURE-PLAN.md); use each beat's measured audio as `--length`. **Use the sweep breakpoints that `_gen_lanes.py --times` prints under "Breakpoints"** (C04, C21 to C24 and the two dissolves of E1, in the harness's own `--animate` and `--steps` syntax, fractions of the clip): the code derives them from the measured words and builds in the rules, so the 50 % and 85 % frames fall inside a hold (or a settled stepped state), each dial in C21 to C23 runs 0 then 1 and the first dial of a clip stays at its end value while the second moves. C01's breakpoints are fixed (CAPTURE-PLAN.md); its readout follows the words. Do not move a breakpoint by hand; if one looks wrong, fix `dial()` in `_gen_lanes.py`. Compare each result against the "verified result to reproduce" column: probe colours are size-independent and must match exactly; the coverage figures were measured at 480 by 480 and move in the third decimal at 2160 (the independent model computed at 2160 gives C13 0.0421, C14 0.0301, C15 0.0602, against 0.0408, 0.0292 and 0.0583 here), so compare them within 0.003. If a probe colour or a coverage disagrees beyond that, stop and report (do not edit the shader). The shader files in `R/lab-shaders/` are final: **do not change a character** (the narration and the on-screen code depend on them); `R/evidence/planning-checks/shader-sha256.txt` lists their sums. The 72 planning renders already exist (`R/evidence/planning-checks/lab-results.jsonl`, `png/`); you do not need to repeat them, but `./run-lab-checks.sh` in that folder does, in a few minutes, if you want proof on this machine today.
- Editor frames E1 (and E2, optional): scratch copy only. **The driver is proven:** start from `R/evidence/planning-checks/editor-driver/` (README there) and `R/evidence/planning-checks/png/editor-inspector-check-2d.png` (what the frame should look like); write frames outside the project folder, import first; recording at 3840 by 2160 with display scale 200 % is recommended for a sharp crop (the planning check ran at 1920 by 1080). **Crop to the "Shader Parameters" group** (the six sliders): no Material preview thumbnail (it draws the crosshair stretched into an ellipse) and no viewport. If it fails for the three states, **stop and ask Bear** to record using `S/RECORDING-SESSION.md` (E1's steps are in CAPTURE-PLAN.md). Do not draw an Inspector from memory.
- **The editor's dark theme may fail GATE T** (dark UI beside mid-tones). Order of remedies: crop (done above), keep the dissolve after the 50 % mark (it is), then the Light theme preset. **The theme is a global editor setting of Bear's Godot: never change it in place.** Back the settings file up and restore it after, or ask Bear; never leave it changed. Last resort: the labelled `GodotDevWorkbench` reconstruction, said so on screen.
- Row 69 (six sliders in the Inspector) is already PASS from a planning-check frame; compare the real E1 frames with it and change B44's line only if they disagree (log it).

## Phase 3: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/`, implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects (`ramp_strip`, `pixel_grid`, `plot`, `uv_square`) and film-local helpers (a disc, a slider with a knob, a wall-and-box, a two-circle Venn). The 15 classes: `B02_AskEveryPixel`, `B03_AddressAndCenter`, `B04_ByHand`, `B06_BelowTheLine`, `B07_StepJump`, `B08_StepFlip`, `B11_SubtractMasks`, `B20_DistanceToALine`, `B21_AbsFold`, `B24_ThreeWays`, `B28_NumbersBecomeDials`, `B29_ZeroToOneDials`, `B31_WhoCanSeeUV`, `B33_SquareLimit`, `B34_Staircase`. Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6): **each event of a `show` list starts at its `at` fraction of the beat (the measured one after Phase 1); a motion that starts after 30 % is a quick one (0.35 s) and is marked so; nothing starts between 40 and 56 %; the 45 to 55 % frame is a settled still with every label that matters on it.**
   - **B04 has an equation:** typeset sqrt(0.12 squared + 0.16 squared) = sqrt(0.04) = 0.2 with a real radical and superscripts. LaTeX is installed on this Mac (`/Library/TeX/texbin/latex`, `dvisvgm`), so use `MathTex`; never raw TeX in a text card. Inspect the frame at 15, 50 and 85 % (`MATH-TYPESETTING.md`). The algebra is already verified (FACTCHECK row 12).
   - **B08:** 25 pixel cells with centres at x = 0.02, 0.06, ... 0.98 (cells 5 to 19 are inside the 0.3 radius; no cell sits exactly on it, so the flip is clean); cell 17 (cells are numbered from 0; centre 0.70, distance 0.2) is ringed throughout as "a pixel at distance 0.2" (it is not our own pixel, which is off this row); at the end the teal stretch is labelled "the circle".
   - **B28:** the vertical-pair line from `lab-shaders/14-four-arms.gdshader` (line 6) is 55 characters and does not fit beside a panel at size 32 (Menlo is about 0.246 units per character at that size, so the safe width of 12.6 units is 51 characters): set it as THREE stacked calls, `step(0.1, y) *`, `step(y, 0.35) *`, `step(x, 0.03)`, with the slots to the right; the voice names the numbers in the order gap, end, width.
   - **B34:** draw a small dot at the CENTRE of every cell and fill a cell teal exactly when its centre dot is inside the ideal circle (the shader decides by the pixel centre); never say or draw "cells wholly inside".
   - **B11, B31:** tags and labels sit beside a shape on a leader line, never on a fill.
   - **Words defined on screen** (GLOSSARY wording, word for word): B07 `step`: "0 below the edge, 1 from the edge up"; B20 `band`: "the strip of pixels near a line or an edge, as wide as the thickness or the softness" (set as two lines so no text object runs past 12 words; the tags `UV.x · horizontal address` and `UV.y · vertical address` on the square's axes define the notation); B21 `abs`: "drops the minus sign: -0.3 becomes 0.3"; B31 `built-in`: "a value the engine hands to a function, or collects from it" (two lines); B04 `distance`: "how far apart two points are". The ShaderLab ones are props: B05 alpha and B17/B19/B23 min and max (cue labels), B09 mask and B10 hint (captions), B30 function (cue label).
   - **Terracotta** is dots, rings and thick strokes (at least 8 px at 1080p): the radius line (B06, B08), the edge line (B07) and the segment (B20) are thick strokes; never a hairline, never text. Teal (`#5FA391`) fills for masks that read 1; empty (the stage color) for 0.
   - **Never an arrow glyph**; draw arrows as shapes. Type at least 32; act titles 40. No fill behind text.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.** If you edit a lane, edit `_gen_lanes.py` and run `python3 $R/_gen_lanes.py` first (it is the single source of `lanes/` and `SHOTLIST.md`), then `make_sheet.py`.
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 4: title card, render

```bash
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

## Gates that must PASS

Gate F (`FACTCHECK.md`; no row is OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text. This film's Godot pictures are teal on a warm light-grey stage on purpose (a mid-tone floor): do not recolor them dark.
- The result-only beats (B01, B39, B43) put a square window on a 16:9 stage; they are declared `sparse` with a reason in the beat sheet (underfill waived, nothing else).
- A Pango `Text()` may drop single spaces on this Mac; look at the still. The `->` glyph is under the type floor: draw arrows as shapes. The minus sign and the multiplication sign are used in labels (U+2212, U+00D7): look at them in the still.
- Manim forbidden: `ease_in_quad`/`ease_out_cubic`, `.animate(path_arc=...)`, `MoveAlongPath` plus `.animate` on one object in one `play`. B21's fold: transform the left half into a mirrored copy; B31's bounce: two plain shifts.
- `LectureEvidenceTable` rings ROWS, not cells (B16's wrong value is in a ringed row); its `note` and `title` must stay at 12 words or fewer (GATE T 8.5), as they are.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input (every `videoLabel` already does). Record on default project settings: with 2D HDR on, an alpha above 1 is not clamped and B14's claim would not hold.
- The shader `lab-shaders/16-uv-inside-function-FAILS.gdshader` fails to compile on purpose. It is shown as text (B32); never try to render it.
- The "Your turn" composer chip reads "Opus 5.5 · High", a default of the shared sheet builder (FACTCHECK row 78, EXEMPT): check it against the series default today; if the series changed it, set `BHTF_MODEL_LABEL` and `BHTF_EFFORT_LABEL` in `narration.py` and re-run `make_sheet.py`.
- In zsh, never name a shell variable `path`, an unquoted `$VAR` holding several options is not split into words (use an array), and an unmatched glob aborts a `&&` chain.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` (except the composer label above), the beat order or any file in `lab-shaders/`. If one narration line must change (for example B44's Inspector wording after E1), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), re-run `align.py $R --only <BID>`, and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab` and its registration.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any beat whose word clock fell back to the estimate, any capture that disagreed with its verified result, and any editor action that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

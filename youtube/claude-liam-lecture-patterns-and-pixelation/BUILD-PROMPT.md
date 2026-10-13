# BUILD-PROMPT: Patterns and Pixelation (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, with estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, and tested shader files. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. Nothing is voiced, recorded, rendered or published yet.
**Found.** Layout is complete and lint-clean: 49 beats (43 body), about 1,790 words, about 10.2 minutes estimated at Liam's measured pace. This film is not the first of the series to be built, so the three shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) may already exist: check before building them (Phase 0). No editor frames and no human editor actions are needed. Open items that need a human: none; the playlist name does not exist yet, so nothing viewer-facing carries one.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-patterns-and-pixelation`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Files (absolute paths)

All in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-patterns-and-pixelation/` unless stated:

- `narration.py` (every spoken line and all bookend content), `lanes/act1.json` to `lanes/act5.json`, `_gen_lanes.py` (writes the lanes and `SHOTLIST.md` from the tested shader files; re-run `python3 _gen_lanes.py && python3 make_sheet.py` after any edit), `make_sheet.py`, `beat_sheet.json`, `SCRIPT.md`.
- `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md`, `CHECKS-REPORT.md`, `SOURCES.md`, `PROMPTS.md`, `CAPTURE-PLAN.md`, this file.
- `lab-shaders/01-showcase.gdshader` to `lab-shaders/15-halftone-rounded.gdshader` (every shader shown on screen, each tested in the Lab).
- `evidence/planning-checks/` (`RESULTS.md`, `lab-results.jsonl`, `analysis-summary.txt`, `run-lab-checks.sh`, `verify-patterns.py`, `verify-bhtf.gd`, `png/`, `reference-shaders/`).
- The series folder: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/` (`BUILDER-BRIEF-COMMON.md`, `COMPONENT-SPECS.md`, `GLOSSARY.md`, `lab/`, `lint_series.py`).
- The toolkit: `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/`.

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"). If the pilot film `claude-liam-lecture-godot-shaders/` has been built, its `BUILD-LOG.md` and `scenes.py` are the best model for the shader-film scenes.




## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-patterns-and-pixelation
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-patterns-and-pixelation/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-patterns-and-pixelation/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the three shared pieces (build only what is missing)

Spec: `S/COMPONENT-SPECS.md`. Check first:

```bash
./brutalist.art/art scenes --check ShaderLab            # a renderable composition?
ls $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh
```

If all three exist, read them and go to Phase 1. If one is missing, build it exactly as the pilot's `BUILD-PROMPT.md` Phase 0 says (the only toolkit edit allowed is `ShaderLab` and its registration in `Root.tsx`, then `./brutalist.art/art scene-index`; say so in `BUILD-LOG.md`). This film needs, on top of the spec:

- **`ShaderLab`**: the `cues[].label` field (a short definition that appears with the highlighted lines: `canvas_item: a shader for 2D drawing`, `vec2: a pair of numbers`, `COLOR: the pixel's color`, `mod(x, y): the remainder of x divided by y`, ...; at most about 45 characters, one line, placed beside the code, never over it), `layout: "video"` with a `title` (act titles ride the first beat of an act), `readouts`, one `ring` at a time, `caption`.
- **`shader_kit.py`**: `ramp_strip`, `pixel_grid`, `plot`, `code_card` from the spec, plus three small objects built on them: `cell_grid` (outline cells with a number in each), `block_row` (a strip of blocks of given widths with rings and labels), `lookup_lines` (curved lines from pixel dots to one point).
- **Capture harness**: `--animate`, a stepped sweep (a list of values each held for a time), `--material-at`, and scene scripts (four small ones: C12, C18, C19, C21).

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01 to C22 into `TK/runtime/remotion/public/patterns-and-pixelation/` with the names the lanes use (`hook.mp4`, `cells-floor.png`, ...). Compare each against the "verified result to reproduce" column; if a measurement disagrees, **stop and report** (do not edit the shader). The numbers to match are in `R/evidence/planning-checks/analysis-summary.txt` (re-run `python3 verify-patterns.py` in that folder against your own PNGs if you want to measure a capture).
- Switch times (C07, C08, C19, C21) come from the measured audio: do Phase 3's audio step first if you need them, or use the estimates in CAPTURE-PLAN and fix after audio.
- D1: the docs screenshot with Playwright (the second `TEXTURE_PIXEL_SIZE` row on the page).
- Every capture says "nearest filter" in its label; the harness must draw the sprite with the nearest filter (the Lab does).

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_StretchTheAddress`, `B03_FloorSteps`, `B04_FractSawtooth`, `B05_WhichAndWhere`, `B09_WhatComesNext`, `B11_OneLookupPerCell`, `B14_WhyItDrifts`, `B16_WorkedExample`, `B18_HalfSizeEdges`, `B20_BlockInPixels`, `B25_ShortLastBlock`, `B26_SumsGrid`, `B27_RemainderColors`, `B28_DiagonalStep`, `B30_DiagonalRamp`, `B31_SawtoothCut`, `B35_CellSpace`, `B36_LengthAndRadius`), implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects. Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Terracotta is for dots and rings only, never text; draw every arrow as a shape; draw no fill behind a number.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
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

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for **fract** (should rhyme with "tract"), **mod**, **floor**, **step**, **U V**, "pixelate", "sawtooth" and "canvas item". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- **GATE T at 4K**: ink-colored rings and any dark small shape beside mid-tones fail; ring with grey. Terracotta is never text. The shaders in this film were written with a mid-tone floor (teal, cream, gold, the soft red-green cells); the one dark spot is the corner of the Lab's gradient picture, which is used for measurement only and is not shown in any beat.
- **Gate V**: Manim beats are `sparse: true` by design (one object on a cream stage); capture beats are not: frame the capture in its window on the cream stage and check the 50 % and 85 % marks. Never crop a capture past the frame edge.
- A Pango `Text()` may drop single spaces on this Mac: look at the still. The `->` glyph is under the type floor: draw arrows as shapes (the words `gives` and `becomes` replace arrows in the labels).
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input and scripted sweeps.
- The Lab serializes runs with a lock (`/private/tmp/claude-501/shaderlab.lock`); other sessions may be using it, so a Lab run can wait minutes.
- zsh gotcha seen while planning: never name a shell variable `path` in zsh (it is tied to `PATH`).

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), which shared pieces already existed and which were built here (and where), any slate, any mispronunciation, any capture that disagreed with its verified result, and any editor action that needed Bear (none expected). Report every file by absolute path. Claim nothing you did not verify by looking at frames.

# BUILD-PROMPT: Vertex Shaders (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, sixteen tested shader files, and the scene library the captures run from. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film is one of twenty in a series and reuses three shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) that the pilot film's build creates.
**Found.** Layout is complete and lint-clean: 46 beats (40 body), 1,721 words, about 9.8 minutes estimated at Liam's measured pace. Nothing is voiced, recorded, rendered or published yet. No editor frames and no screenshots are needed. Two things need a human only if they fail: a gate that cannot pass without changing a shader or the narration, and a capture that disagrees with its verified result.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`
`EV` = `$R/evidence/planning-checks`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"), and the pilot `claude-liam-lecture-godot-shaders/BUILD-PROMPT.md` for the shared pieces.




## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the three shared pieces (reuse; build only what is missing)

1. `ls $TK/runtime/remotion/src/scenes/ShaderLab.tsx $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh`. If all four exist (the pilot's build made them), reuse them and go to Phase 1. If one is missing, build it from `S/COMPONENT-SPECS.md` exactly as the pilot's BUILD-PROMPT says (ShaderLab in the toolkit's Remotion scenes, registered, then `./brutalist.art/art scene-index` and `./brutalist.art/art scenes --check ShaderLab`; the Manim kit in `S/shader_kit.py`; the harness in `S/lab/`). Say so in `R/BUILD-LOG.md`.
2. **This film's `shader_kit` additions** (add to `S/shader_kit.py`, never copy it): `vertex_dot(label)` (terracotta dot with a monospace label), `polyline_through(points)`, `dot_grid(cols, rows)` with `count_up(grid)`, `screen_frame(w, h)` (outlined 16:9 frame with a node square inside) and `sine_curve(samples)`. Terracotta only as dots and rings.
3. **Use the harness's `--scene PATH.gd` option** (it is in the spec) with `$EV/scratch-project/capture_scenes.gd` and `vscene.gd`: the scene library defines `build(id, parent, shader_dir, duration)` (called once) and `tick(ctx, t)` (once per frame, `t = frame / 30`) and declares its logical canvas in `ctx.canvas`; pass `--length D` for the beat's audio length. If `--scene` expects one scene per file, write a three-line wrapper per scene id. The scenes make their own shader switches, sweeps and calls, so `--material-at`, `--set-at`, `--call-at`, `--animate` and `--time-origin` are not needed. `$EV/scratch-project/scene_frames.gd` is a working (real-time) example of driving the library.

## Phase 1: record (`R/CAPTURE-PLAN.md`)

- Record C01 to C25 into `$TK/runtime/remotion/public/vertex-shaders/` with the file names the lanes use. **Events are fractions of each beat's measured audio D**, so do this after Phase 3's audio exists, or record with the estimated durations from `beat_sheet.json` and re-record any beat whose audio differs by more than half a second.
- Compare each capture against the "Verified result to reproduce" column and the planning frames in `$EV/png/scene-*.png`. If a probe or a picture disagrees, stop and report; do not edit a shader or the narration.
- B40's terminal text must be the verbatim output of a real run (`R/CAPTURE-PLAN.md`, section "Terminal run").
- No editor frames, no screenshots, no key presses are needed.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_FourCorners`, `B03_InAndOut`, `B04_PixelsFromTheMiddle`, `B08_Address`, `B10_EvenSteps`, `B13_OnlyWhatExists`, `B14_TwoWays`, `B16_CountThem`, `B27_FragmentCannotSee`, `B28_Varying`, `B31_BuiltInVaryings`, `B36_TwoMeanings`), implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects. Numbers in the pictures come from the planning runs: corners at (-64, -64) and (64, 64), the five edge shifts +1, +12, +25, +37, +49 px, vertex counts 4, 9, 25 and 297, the fragment-stage corner (576, 296) on a 1280 x 720 screen. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Assemble with the sibling's `assemble_scenes.py` pattern.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.** `python3 $R/_gen_lanes.py` regenerates `lanes/` and `SHOTLIST.md` from the tested shader files; do not hand-edit them.
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at it before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for "vertex" (and "vertices"), "varying", "interpolates", "uniform", "amplitude", "sine", "U V", "mesh instance two D", "two D", "Godot". The built-ins VERTEX, COLOR and TIME are written as lowercase words in the narration on purpose. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and ones this film adds)

- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text; terracotta dots and rings only.
- **The lit flag.** In the darkest folds the shader multiplies the cream cells by about 0.8, which lands near the stage grey (`#D9D5CA`). The teal cells and the pole keep the picture readable, but check GATE T and Gate V on C01, C20 and the B33 beat at the 50 % and 85 % frames. If a gate fails, put the capture in a window frame or crop; **do not change the shader** (the factor is in the tested file and in `FACTCHECK.md`).
- Code cards: every shader shown is at most 14 lines (the longest is `10-flag-lit`, 13). ShaderLab readouts are at most three words. The definition captions (GLOSSARY wording, listed in `ACTS.md`) go in ShaderLab's `caption`; they must be on screen when the term is first spoken.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes. `->` is below the type floor.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label every scripted event.
- **`TIME` can stop in a real-time run if the window is covered** (seen in planning when other Godot windows opened; the planning scripts now keep their window on top). An offline fixed-tick capture does not have this problem; if a flag capture looks frozen, check the capture, not the shader.
- A `QuadMesh` in a `MeshInstance2D` draws upside down unless its size.y is negative; the film's flag textures have 7 rows so a flipped checker looks the same, and only C22 shows the flip on purpose. A `Polygon2D` only has UV when it has a texture (C24 shows it on purpose).
- The 1280 constant in `14-position-from-fragment.gdshader` is the width of the 1280 x 720 canvas: keep that canvas for C23.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab` (and only if the pilot's build has not made it).

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, and any gate that needed more than a re-crop. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

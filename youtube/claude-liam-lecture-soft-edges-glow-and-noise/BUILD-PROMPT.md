# BUILD-PROMPT: Soft Edges, Glow and Noise (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, and 15 tested shader files. What is left is recording, building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses three shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) that the first shader film's build creates; if they do not exist yet, you build them (Phase 0).
**Found.** Layout is complete and lint-clean: 42 body beats (48 with the six bookends), 1,791 words, about 10.2 minutes by the lint's ceiling formula. Nothing is voiced, rendered or published yet, and no Godot render is recorded, but both editor captures are recorded by script (2026-10-13: E3 for this film, E1 reused from the Textures and Color recording) and the two formerly OPEN fact-check rows (35, 57) are closed from them. Open items that need a human: the playlist name (none yet).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-soft-edges-glow-and-noise`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (what to build first), `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`, `R/evidence/planning-checks/RESULTS.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"), and, if the first shader film has been built, `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/` (its `BUILD-LOG.md` and the shared pieces it made).

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-soft-edges-glow-and-noise
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-soft-edges-glow-and-noise/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-soft-edges-glow-and-noise/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (build once; check first)

Spec: `S/COMPONENT-SPECS.md`. For each piece, look before you build.

1. **`ShaderLab`**: `./brutalist.art/art scenes --check ShaderLab`. If it says NOT RENDERABLE, build it as a Remotion composition in `TK/runtime/remotion/src/scenes/`, register it in `Root.tsx`, run `./brutalist.art/art scene-index` and check again. Props, layouts (`side`, `stack`, `video`, `code`), cue labels (at most 60 characters, rendered), `caption` (one line, at most 80), `ramp.period`: all in the spec. This is the only place you may edit the toolkit; keep the change to this one file plus its registration and say so in `R/BUILD-LOG.md`.
2. **`shader_kit.py`**: `S/shader_kit.py` (ramp strip, pixel grid, plot with a travelling dot and dashed guides, vertex quad, UV square, worker grid, code card). If it exists, extend it only with what this film needs and says so: a **distance-ring spot on a pixel grid** (B11), a **bar through a gate** (B33, B38), a **strip with a sliding window** (B27), a **histogram with its running total** (B32).
3. **Capture harness**: `S/lab/capture.gd` + `S/lab/capture_shader.sh` with `--material-at`, `--animate` (piecewise), `--scene`, `--call-at`, `--time-origin` and the SubViewport native-size route (spec section "Capture harness" and its traps). If it exists, reuse it.

## Phase 1: record (CAPTURE-PLAN.md)

- Record C01 to C23 into `TK/runtime/remotion/public/soft-edges-glow-and-noise/` with the names the lanes use. Compare each against the "verified result to reproduce" column; if a probe disagrees, stop and report (do not edit the shader).
- Scene scripts (14 of the captures): a two-panel script (C10, C15), a NoiseTexture2D script (C11 to C16, C23), a vec2 orbit script (C08), and an HDR 2D / environment / stage-colour switch script (C18 to C22). The node recipes that were already run are `R/evidence/planning-checks/noise_check.gd` (`make_noise`, `make_rect`), `toggle_check.gd` (switching `use_hdr_2d`, adding the environment, toggling `glow_enabled`), `glow_check.gd` and `finale_check.gd`. The glow clips use the stage `#5F7A96`; the others `#D9D5CA`.
- The glow environment is always: `Environment.glow_enabled = true`, `background_mode = Environment.BG_CANVAS`, `glow_intensity = 2.0`, everything else default. Without the Canvas background nothing happens (FACTCHECK 71): if a clip shows no halo, check that first.
- Editor frames E1 and E3 are **already recorded by script** (CAPTURE-PLAN section E); nobody clicks or records by hand. E3 (B19, the bubble's Shader Parameters and its color picker): the two frames are in `S/editor-capture/png/1920x1080/soft-edges-glow-and-noise/`; they were recorded at 1920x1080 only, so re-record them at native 3456x1944 with the archived state script (the recipe is in CAPTURE-PLAN section E; about 30 s, holds the shared Lab lock), crop as the lane's `capture_spec` says and save as `e3-color-pickers.mp4` (a cross-dissolve). E1 (B24): crop the two frames `textures-and-color_E1-3a` and `E1-3b` from `S/editor-capture/png/3456x1944/textures-and-color/` as the lane's `capture_spec` says and save as `e1-noise-inspector.mp4`. Label both clips "scripted editor session".
- D1 and D2: the two documentation screenshots with Playwright (`CAPTURE-PLAN.md`), 1600 x 900 at device scale 2.4; find the ringed sentence and table rows with Playwright and set the `moves` to them.
- Rows 35 and 57 are already closed from the real frames (`R/FACTCHECK.md`). If a frame you record differs from what the rows quote, stop and report; change a narration line only if the label differs (log it).

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` and implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects. The 15 classes: `B02_StepPlot`, `B04_Staircase`, `B05_TwoLines`, `B06_SCurveNumber`, `B09_BandsMeet`, `B10_SwappedLines`, `B11_Falloff`, `B13_PowerCurves`, `B17_Layers`, `B18_MultiplyAdd`, `B21_EvaluationOrder`, `B27_WindowSlides`, `B32_RevealPace`, `B33_ClipAtOne`, `B38_ThreeAgreements`. Real data: B04 reads `R/evidence/planning-checks/staircase-cells.txt` (a real crop of the hard-disc render); B32 uses the histogram and the reveal curve printed in `R/evidence/planning-checks/run-noise.log` (`T-seamless.histogram_20_bins_of_0.05`, `R-curve`). B06 sets 3t^2 - 2t^3 as real typeset math (`TK/docs/MATH-TYPESETTING.md`) beside the monospace code form, and you look at its frames. Manim traps: section 6 of the common brief (no fill behind text, midpoint rule, arrows as shapes, Pango spaces, grey bars).
2. Audition B38 once against `DesignPipelineClaim` with `diagramStyle: "show-tell-isometric"` as the SHOTLIST row says; keep the bar-through-a-gate drawing unless the isometric one shows the height that matters.
3. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
4. Stills first: a last-frame still of every Manim class and 25 / 50 / 95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `R/BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for "smooth step" (two words), "clamp", "sampler two D", "noise texture two D", "fast noise lite", "H D R two D", "U V", "seamless", "Godot", "Mac". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear. If a capture clip is more than a second away from its beat's measured audio, re-record it with the same schedule as fractions (`--length`), not by editing anything else.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text. The glow stage `#5F7A96` was chosen for distance from the gate's MUTE grey; keep it.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- zsh: never name a shell variable `path`; keep option lists in arrays, not strings (an unquoted string is not split). Never `pkill -f` a script name (other films' batches share it); kill by PID. The shared Shader Lab lock serialises Godot windows; hold it for scene-script runs too (`/private/tmp/claude-501/shaderlab.lock`, a directory made with `mkdir`).
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted switches ("scripted"). Every pixel value on screen is Forward+ and labelled so.
- The TIME captures (C12 to C16, C23) must start the shader clock at zero (`--time-origin 0`), or the seam will not sit where the lanes say. A Godot window that another window fully covers is not drawn and the shader clock stands still (met while planning: `R/evidence/planning-checks/run-0-first-runs-transcribed.txt`, item 8): record with the harness's fixed steps, never by waiting, and check that TIME moved.
- On-screen definitions are the series GLOSSARY wording, word for word (the terms card, B03 `step`, B05 `smoothstep` on two lines, B09 `max`, B19 `hint`, B25 `sampler2D`, B26 `TIME`, B35 `HDR 2D`, B40 `linear`); the lint compares the terms card. B07's `band` is a labelled adaptation (CHECKS-REPORT). If a label does not fit, break the line or go down to the type floor; never reword it.
- `HDR 2D` is read when the project starts; the clips switch `Viewport.use_hdr_2d` on the root at a stated second (verified equivalent: `R/evidence/planning-checks/run-toggle.log`).

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example an Inspector label), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, `S/` (shared files), or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, which editor frames were used and any crop you had to change (all should be the driver's real frames), and that no fact-check row is OPEN. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

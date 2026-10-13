# BUILD-PROMPT: Lines and Shine (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, tested shader files and the evidence behind every number. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film needs no editor frames and no docs screenshots; it does need fourteen Manim scenes, nineteen Godot captures (seven of them two-panel scenes) and the three shared pieces every shader film reuses.
**Found.** Layout is complete and lint-clean: 41 beats (35 body), about 1,580 words, about 9.0 minutes estimated at Liam's measured pace. Nothing is voiced, recorded, rendered or published yet. Open items that need a human: none blocking; the third-party source's creator is not named (credit in the description is Bear's call), and no playlist name exists yet.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-lines-and-shine`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (what to build first), `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").
6. The evidence: `R/evidence/planning-checks/RESULTS.md`, `measurements.txt`, and the scene script `two_panels.gd`.




## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-lines-and-shine
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-lines-and-shine/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-lines-and-shine/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the three shared pieces (build once; reuse if another shader film already built them)

Check first: `ls S/shader_kit.py S/lab/capture.gd`, and `./brutalist.art/art scenes --check ShaderLab`. If they exist, read them and add only what this film needs (below). If not, build them from `S/COMPONENT-SPECS.md`.

1. **`ShaderLab`**: a Remotion composition in `TK/runtime/remotion/src/scenes/`, registered in `Root.tsx`, then `./brutalist.art/art scene-index` and `./brutalist.art/art scenes --check ShaderLab`. Follow the toolkit's Remotion rules (`TK/CLAUDE.md` rule 10; install nothing new; render only through `runtime/scripts/remotion_scenes.py`). This is the only place you may edit the toolkit; keep the change to this one file plus its registration, and say so in `BUILD-LOG.md`. **This film's lanes use three things beyond the spec's table:** `caption` for a one-line definition (for example "step(a, b): 0 while b < a, otherwise 1"), `ramp.period` (seconds; the marker restarts every period, used in B27) and a `layout: "stack"` whose code is a short excerpt (two or three lines). The `ShaderLab` result window must fit a 16:9 capture whose card or panels sit inside it; readout and ring coordinates are fractions of that 16:9 frame. If the component cannot do one of these, build the smallest extension and log it.
2. **`shader_kit.py`**: Manim helpers in the Claude palette; put it in `S/shader_kit.py` (`assemble_scenes.py` pastes it above the scenes like the sibling's `kit.py`). This film uses `uv_square` (B03, B04), `plot` (B13, B15) and plain Manim axes, lines, arcs, dots, dashed lines and `MathTex` or `Text` for the rest.
3. **Capture harness**: `S/lab/capture.gd` + `S/lab/capture_shader.sh`, built on `S/lab/runner.gd`, using the Signal Garden SubViewport native-size route and its traps (spec section "Capture harness"). **What this film needs beyond the spec's `--animate name:t0:v0,t1:v1,...` (piecewise linear), `--material-at` and `--set-at`:** the keyframes in `CAPTURE-PLAN.md` are fractions of the clip, so convert them to seconds with the beat's `actual_duration_s`; `--animate` applied per panel (a `0.angle:` or `left.angle:` prefix is enough); a scene option that loads `R/evidence/planning-checks/two_panels.gd` (the still renderer it was verified with: read it and drive the same scene); a scripted call at given times (C16); a clock-origin option for `TIME` (C01).

## Phase 1: audio first (free), then record

1. `python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R` (free; measured durations become the clock). Every capture clip is then cut to its beat's `actual_duration_s`.
2. Record C01 to C20 (`R/CAPTURE-PLAN.md`; C15 is C01 again) into `TK/runtime/remotion/public/lines-and-shine/` with the names the lanes use. Compare each against its "verified result to reproduce" column and against the 640 x 360 stills in `R/evidence/planning-checks/png/`; if a probe disagrees, stop and report (do not edit a shader). Every sweep is a fraction of the clip; no overlay starts inside 45 to 55 percent.
3. Never claim real input: the clips are scripted and labelled.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_SchoolLine`, `B03_CenterTheAddress`, `B04_FlipUp`, `B05_TheTest`, `B06_ThreeDots`, `B07_Parallel`, `B10_TangentIsSlope`, `B13_TanExplodes`, `B15_AbsAndStep`, `B18_TwoGaps`, `B19_RightTriangle`, `B31_UnitStep`, `B32_NormalAndDot`, `B33_SameThing`), implementing each `visual_intent`, `motion_claim` and `show` cue from `R/SHOTLIST.md` and `R/lanes/act*.json` with `shader_kit` objects. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Lines, triangles and dashed gaps are warm grey `#8A8577` (73 from the type gate's MUTE colour; its ink mask tolerance is 48) and thick (at least 6 px at the 4K design size); terracotta only as dots and rings, never a thin stroke or text; the angle is shown by a pale grey filled wedge. Draw arrows as shapes. Numbers on screen are the ones in the lanes; do not recompute them by eye.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: title card, render

```bash
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for U V, "Godot", "tween", "radians", "sine", "cosine", "tangent", "normal", the single letters in "y equals m x plus b" and "p dot n", and "minus twenty-three million". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and ones this film is likely to meet)

- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text. The card greys are safe (the grey card is 127, which is 72 from the type gate's MUTE colour; the gate's ink mask tolerance is 48); do not darken them. Readout labels over the card need a light backing, not ink on mid-grey.
- Warm and cool fields at steep slopes saturate to pure orange and blue (B14, B35): saturated, not near ink, so they pass; do not "fix" them by dimming.
- Gate V underfill: the ShaderLab beats are not sparse; the card is only part of the frame, the code panel and window frame supply the fill. Manim beats are declared sparse in the lanes.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes; the `->` glyph is under the type floor.
- Raw band at 89 degrees is a 2 px hairline on a 1728 px card: do not scale a smaller capture up.
- The Lab window clamps to the screen height (a 3840 x 2160 request gives a 2004 px window; the card keeps its size). The SubViewport route avoids this; do not rely on a window that big.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted calls.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, and which ShaderLab extensions were needed. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

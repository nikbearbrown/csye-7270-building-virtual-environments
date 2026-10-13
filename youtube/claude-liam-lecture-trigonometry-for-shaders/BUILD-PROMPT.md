# BUILD-PROMPT: Trigonometry for Shaders (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, with estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, and 12 shader files that were run in a real Godot. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film is not the pilot: it reuses the three shared pieces the pilot's build makes (`ShaderLab`, `shader_kit.py`, the capture harness), so check they exist before anything else (Phase 0).
**Found.** Layout is complete and lint-clean: 46 beats (40 body, five acts), 1,740 words, about 9.9 minutes estimated at Liam's measured pace. Nothing is voiced, recorded, rendered or published yet. No editor frames and no human action are needed: every Godot picture is a one-shader Lab render and there are two docs screenshots. The one open item for a human is the playlist name (none yet).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`. Shorthand used below:

```bash
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-trigonometry-for-shaders
S=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series
P=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders
TK=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art
```

## Read first (in order)

1. `$TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `/Users/bear/Documents/CoWork/bear-textbooks/books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths, the two-stage rule).
3. `$S/BUILDER-BRIEF-COMMON.md` (sections 4, 6 and 11), `$S/COMPONENT-SPECS.md`, `$S/GLOSSARY.md`.
4. `$R/SCRIPT.md` (the film as Bear will read it), `$R/SHOTLIST.md`, `$R/CAPTURE-PLAN.md`, `$R/FACTCHECK.md`, `$R/ACTS.md`, `$R/evidence/planning-checks/RESULTS.md`.
5. The pilot's `$P/BUILD-PROMPT.md` (its Phase 0 is how the shared pieces are built) and a finished sibling for the Manim scaffolding: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `BUILD-LOG.md` "Mistakes worth not repeating").




## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-trigonometry-for-shaders
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-trigonometry-for-shaders/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-trigonometry-for-shaders/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (check; build only what is missing)

- `./brutalist.art/art scenes --check ShaderLab` must say RENDERABLE. Check it supports the layouts this film uses (`side`, `stack`, `video`, `code`) and the props it uses (`title`, `cues` with `label`, `readouts`, `rings`, `ramp`, `caption`). If it is missing, build it as the pilot's Phase 0 says (the only toolkit change allowed: one component file plus its registration, noted in `BUILD-LOG.md`), then `./brutalist.art/art scene-index`.
- `$S/shader_kit.py` (ramp strip, pixel grid, plot, uv square, code card) and the capture harness `$S/lab/capture.gd` + `$S/lab/capture_shader.sh` must exist. If not, build them from `$S/COMPONENT-SPECS.md`. This film needs from the harness: square (480 x 480) and wide (640 x 360) canvases, live `TIME`, a piecewise `--animate` schedule (C06, C11, C12), still PNG, PNG sequence to MP4.
- **Film-local Manim objects** (write them at the top of `$R/scenes.py`, not into the shared kit): `right_triangle(angle, hyp)` with side highlight and a thick terracotta angle arc; `unit_circle(radius, orientation)` with a terracotta dot, axes and a paper/screen flag; a `wave_plot` (the shared `plot` plus a travelling dashed link from a circle's dot); `radius_tape` (a bar copied end to end round a circle's edge); `vector_chain` (arrows tip to tail with a riding small ring); `compass_readout` (a live number box beside a walking dot); `knob_slider`.

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01 to C13 into `$TK/runtime/remotion/public/godot-shaders/` with the names the lanes use (`trig-hook.mp4`, `trig-moon-fixed.png`, ...). Compare each with the "verified result to reproduce" column; if a probe disagrees, stop and report (do not edit a shader). Use the exact uniform schedules in the plan for C06, C11 and C12.
- C11 and C12 draw a sprite: use the 512-px linear-filtered blob the capture plan describes (the Lab's 128-px nearest sprite would look blocky at 1920 px).
- D1 and D2: the two docs screenshots with Playwright (see the plan); then set the `moves` and `ring` of B08 and B33 in `_gen_lanes.py` from the real screenshots (keep every move out of the 45 to 55 % window), run `python3 $R/_gen_lanes.py && python3 $R/make_sheet.py`, and log it.
- No editor capture and no human recording is needed.

## Phase 2: scenes and sheet

1. Write `$R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` and implementing each `visual_intent`, `motion_claim` and `show` cue: B02_RightTriangle, B03_SameRatio, B04_SohCahToa, B05_Lookup, B06_UnitCircle, B07_LegsAreCosSin, B09_RadiusAndCenter, B10_WorkedExample, B11_Radians, B12_PiTau, B13_DegreesTrap, B14_SineWave, B15_CosineShift, B16_CenterAddress, B17_Planet, B20_Flip, B25_Recipe, B26_Chain, B30_Arm, B31_TwoWays, B32_AtanIdea, B34_Compass, B37_WorkedPixel (23 classes). Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`$S/BUILDER-BRIEF-COMMON.md` section 6): the 50 % frame of every scene is a settled still holding the labels that matter.
2. **Orientation is the correctness risk of this film.** B06 to B15 are drawn on paper (y up, angles counterclockwise; B06 carries a small 'on paper' caption). B16 to B19 and everything after are the screen way (y down, angles clockwise; the 'y' arrow points down). B20 shows both and flips one into the other. Check every still against the direction its beat's SCRIPT.md text says (for example B34: down is plus half pi and the dot walks clockwise; B19: the moon is BELOW the middle).
3. **Colours.** Planet teal `#5EA391`, moon slate-blue `#8099BF`, meteor amber `#E6A640`, shader stage `#D9D6C9`, the same in Manim as in the renders. Terracotta only as dots, thick arcs and small rings: never text, never a thin stroke, never a filled wedge or a large flat shape (GATE T reads those as text).
4. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.** The cue times in `lanes/*.json` were computed from the narration's word positions; if one lands wrong against the measured audio, change its number in `_gen_lanes.py`, run `python3 $R/_gen_lanes.py && python3 $R/make_sheet.py`, and log it.
5. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare with `narration.py`. Listen for: lowercase "pi" must sound like the dessert (the voice dictionary reads all-caps PI as the letters P, I, which is why the script writes it lowercase), "tau", "fract", "vec two", "S O H, C A H, T O A", "U V", "o'clock", "arc tangent", "lookups", "hypotenuse", "Godot". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`, zero OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `$R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- GATE T reads dark UI, dark outlines and flat terracotta objects as text blobs. The render colours here were chosen as mid-tones (no black fields; the angle picture runs teal to amber on purpose). Ink-colored rings next to mid-tones fail: ring with grey. Real captures with dark areas fail at the 50 % frame unless cropped; none of these should.
- Gate A: every Manim scene must add a new non-text, non-Rectangle shape after its first frame; forbidden `ease_in_quad`/`ease_out_cubic` (use the kit's `ease_in`), `.animate(path_arc=...)`, `MoveAlongPath` plus `.animate` on one object in one `play`; stay inside +-6.2 by +-3.3; type 32 or larger (act titles 40); no fill behind text. Draw arrows as shapes (the `->` glyph is under the type floor).
- A Pango `Text()` can drop single spaces on this Mac: double the space at a fused boundary and look at the still. Check `'÷'`, `'×'` and `'°'` render.
- `BrowserCapture` moves take 1.2 s each and then hold: keep every move out of the 45 to 55 % window. `LectureCodeTrace` is not used in this film (its card holds about ten lines); the code-only beats (B18, B27) use `ShaderLab` with `layout: code`.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted values.
- Keep any Godot view even-sized: the docs call the arc tangent undefined at x == 0 (FACTCHECK row 63).

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, the shared series files, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, any BrowserCapture wording that differs from FACTCHECK, and anything that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

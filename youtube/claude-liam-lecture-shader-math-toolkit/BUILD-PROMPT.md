# BUILD-PROMPT: The Shader Math Toolkit (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, with estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, the curve formulas and the tested shader files. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses the three shared pieces the shader films need (`ShaderLab`, `shader_kit.py`, the capture harness); the pilot film's handoff builds them first, so if they exist, reuse them untouched.
**Found.** Layout is complete and lint-clean: 47 beats (41 body), 1,808 words, about 10.3 minutes estimated at Liam's measured pace. Nothing is voiced, recorded, rendered or published yet. Every shader result is verified in a real Godot 4.7.2 window, and every curve to be drawn is proved identical to Godot's render (`evidence/planning-checks/dense-compare.md`). No editor frames and no human action are needed unless a shared piece is missing (Phase 0).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`. Set these once per shell (every path below uses them):

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-math-toolkit   # this film
S=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series                       # the series files
TK=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art                                                                              # the toolkit
```

In prose below, `R/`, `S/` and `TK/` mean those folders.

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `/Users/bear/Documents/CoWork/bear-textbooks/books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (the three shared pieces), `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md` (the standard plot and the must-exist list), `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").
6. `R/evidence/planning-checks/RESULTS.md` (what was run, and the one trap found: the ramp strip, below).

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-math-toolkit
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-math-toolkit/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-math-toolkit/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (reuse; build only what is missing)

1. Check: `ls S/shader_kit.py S/lab/capture.gd S/lab/capture_shader.sh` and `./brutalist.art/art scenes --check ShaderLab` (must say RENDERABLE).
2. If anything is missing, the pilot film's build has not run. Build the missing piece exactly as `S/COMPONENT-SPECS.md` says (the pilot's `BUILD-PROMPT.md`, `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/BUILD-PROMPT.md` Phase 0, has the detail), keep the toolkit change to the `ShaderLab` file plus its registration, run `./brutalist.art/art scene-index`, and say so in `R/BUILD-LOG.md`. Do not fork a shared piece for this film.
3. This film also needs four small Manim helpers. If `S/shader_kit.py` does not have them, write them in `R/_kit_extra.py` (pasted above the scenes like the sibling's `_kit_cast.py`) and tell Bear in the final report so they can be folded into the shared kit: `plot_with_strip` (the **standard plot** defined in `R/SHOTLIST.md`), `number_line`, `vec_arrow`, `chip` (a mono function-name chip).
4. **The ramp strip is a row of narrow tiles, not one gradient.** Draw it as 64 tiles with 6 px gaps at 4K (or 48 with 8 px), each taller than wide, true grays (value v drawn as gray v: 0 black, 1 white). Why: the toolkit's own blob detector reads a continuous black-to-white strip as one text-like run (682 by 130 px at 4K) and tiles as none (`R/evidence/planning-checks/gate-t-advisory.json`, script `run_gate_t_advisory.py`). If GATE T still objects, fall back to a lifted scale (gray 0.50 + 0.50 v), keep the end labels, and log it.
5. The capture harness must accept piecewise keyframes for one uniform (`--animate name:t0:v0,t1:v1,...`, time in seconds : value; exact strings in `CAPTURE-PLAN.md`). If it only has linear sweeps, add keyframes (small) or record segments whose end values meet and join them with ffmpeg. Square pictures use the Lab's `sprite` kind (`CAPTURE-PLAN.md`, "Conventions").

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01 to C16 into `TK/runtime/remotion/public/godot-shaders/math-toolkit/` with the names the lanes use. Compare each against its "verified result to reproduce" column (probe the saved frames); if a probe disagrees, stop and report: do not edit a shader.
- A sweep must be at least as long as the measured beat when it is voiced (the sweeps finish by about 85 % and then hold); after Phase 3's audio, re-record any capture that is more than half a second shorter than its beat, with the keyframes stretched.
- D1: the docs screenshot with Playwright (the 4.7-pinned address in `CAPTURE-PLAN.md`). Read the three quoted lines in the captured image; if the wording differs from `FACTCHECK.md` rows 23 and 24, stop and tell Bear. Fit the lane's `moves` and `ring` numbers (`R/_gen_lanes.py`, beat B12) to the real layout, then re-run `python3 R/_gen_lanes.py && python3 R/make_sheet.py` (only before Phase 3; never after `art final`).
- No editor frames, no GPU timing, no real-time frame-rate claim anywhere.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `R/lanes/` (`B02_RampStrip`, `B04_ReadThePlot`, ... 23 classes), implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`. Draw every curve from `R/evidence/planning-checks/plot_data.py` (import it, or paste the functions): the film's drawings and Godot's pixels were proved identical only for these formulas. Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the **midpoint rule** (`S/BUILDER-BRIEF-COMMON.md` section 6): each Manim lane lists one "midpoint hold" pose; nothing may start moving between 45 and 55 % of the beat. The cue times are fractions of the narration; the voiced durations decide the real times.
2. Numbers and words on screen are fixed: 0.028 and 0.1 (B11), 1.6 (B14), 0.40 / 0.30 / 0.49 / 0.64 / 0.07 (B28), 384 by 192 px (B30), the radii 0.3 and 0.38, "checked in Godot 4.7.2 · Forward+". Terracotta only as the dot and as grey-backed rings, never as text. Draw arrows as shapes (the `->` glyph is under the type floor). The lanes write glyphs such as × − √ ² ≥ · for readability: if the mono or serif face lacks one, use plain ASCII (x, -, sqrt, ^2, >=) and look at the still. A Pango `Text()` may drop single spaces on this Mac: look at the stills.
3. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
4. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render (the midpoint frame must be a settled still with its labels). For every plot, also compare its strip with the real Godot render of the same curve in `R/evidence/planning-checks/png-dense/<curve name>.png` (same values; the curve names are the keys of `CURVES` in `plot_data.py`). Write down what you see in `R/BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books          # and R set as above
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`. Listen for "fract", "abs", "mod", "clamp", "normalize", "F mod", "F pos mod" (fmod and fposmod), "smooth step", "U V dot x", "power" (pow), "sine", "teal", "cubed" and "Godot". Do not edit `TK/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: 75 rows, no OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and this film's own)

- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text.
- The ramp strip as a continuous gradient fails GATE T (Phase 0, item 4). The Lab renders themselves are fine: 0 text-like runs in the render window for all 20 captures in two layouts (`gate-t-advisory.json`).
- ShaderLab cue labels are at most 60 characters (`COMPONENT-SPECS.md`) and must be rendered: B03 carries the GLOSSARY wording of fragment(), COLOR and alpha as labels; B08 carries the first half of the uniform definition as a label and the whole sentence in `caption` (at most 80 characters). Check them at the type floor on the 50 % and 85 % frames.
- Gate V underfill: the Manim beats are declared `sparse`; the ShaderLab beats are not. Never crop a capture past the window.
- Read-outs land on black or white fields (B35, B36, B38 sit on black; B29, B31 on gray ramps): give each a backing pill or light text so it clears the type floor and contrast on both; check the 50 % and 85 % frames. Positions in the lanes are indicative.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. The credit lines say Forward+ (the Compatibility renderer gives the same pixels for these shaders, `renderer-compare.json`; do not add a renderer comparison to the film).
- The two things the docs call undefined (`smoothstep` with a first edge at or above the second; `pow` of a negative base) stay worded "undefined" on screen and in the voice; the Mac's behavior (`function-tables.md`, `OBS-*` rows) is evidence, not a claim.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example a pronunciation fix), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, `S/` beyond the shared pieces named in Phase 0, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where (and which kit helpers were added), any slate, any mispronunciation, any capture that disagreed with its verified result, whether the tile strip passed GATE T or needed the fallback, and any human action that was needed. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

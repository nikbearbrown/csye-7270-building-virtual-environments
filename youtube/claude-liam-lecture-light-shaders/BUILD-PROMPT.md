# BUILD-PROMPT: Light Shaders (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, tested shader files, and 25 ready capture scenes (`evidence/planning-checks/light_scene.gd` driven by `captures.json`). What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film needs the same three shared pieces as every shader film (`ShaderLab`, `shader_kit.py`, a capture loop) but brings its own capture loop, so it can be built before or after the others.
**Found.** Layout is complete and lint-clean: 46 beats (40 body), 1,808 words counted (1,796 spoken), about 10.3 minutes by the lint's ceiling estimate (the real length is known after the voice). Nothing is voiced, recorded, rendered or published. One decision differs from the series default and is deliberate: the Godot captures are 1920 x 1080 at scale 1, not the 3x SubViewport route, because this film's shaders read screen-space pixels and those are physical (FACTCHECK row 75). Needs a human: nothing blocks the build; the playlist name (none yet) and the third-party creator's name are open for Bear.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders` (absolute: `/Users/bear/Documents/CoWork/bear-textbooks/books/$R`)
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (ShaderLab, shader_kit, the capture harness), `S/GLOSSARY.md` (the small-words table and the series conventions: y points down so angles grow clockwise; a pixel value is quoted only with its renderer).
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`, `R/evidence/planning-checks/RESULTS.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: shared pieces (build only what is missing)

1. `./brutalist.art/art scenes --check ShaderLab`. If it says NOT RENDERABLE, build it from `S/COMPONENT-SPECS.md` (a Remotion composition in `TK/runtime/remotion/src/scenes/`, registered in `Root.tsx`, then `./brutalist.art/art scene-index` and `--check ShaderLab`). Everything in the spec matters here: all four layouts, `cues[].label` rendered (at most 60 characters: this film uses about a dozen as definition tags on code lines), `caption` up to 80 characters, `readouts` of at most three words, `rings`, `ramp`. The toolkit's one allowed edit is that component plus its registration; say so in `BUILD-LOG.md`.
2. `S/shader_kit.py` (Manim helpers) if it does not exist yet; this film adds its own helpers in `R/scenes.py` (below).
3. **Capture loop: already written for this film.** Use `R/evidence/planning-checks/record_all.sh`, not `lab/capture.gd`. If the shared harness already exists, its `--scene PATH.gd` option can drive `light_scene.gd` instead (see `CAPTURE-PLAN.md`). Needs `godot`, `ffmpeg` (both installed).

## Phase 1: record (CAPTURE-PLAN.md)

```bash
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders
PUBLIC=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/godot-shaders \
  OUT=/private/tmp/claude-501/ls-capture/out $R/evidence/planning-checks/record_all.sh          # all 25 captures, 9,810 frames, about 15 to 25 minutes
```

- It records 24 clips (MP4, 1920 x 1080, 30 fps) and one still (C21, PNG) under the exact file names the lanes use (`ls-c01-hook.mp4` and so on) and copies each into `PUBLIC`. It deletes each PNG sequence after the MP4 is made (`KEEP_FRAMES=1` keeps them). Pass capture ids to record only some: `record_all.sh C05 C21`. Check `df -h /` first: about 2 GB of PNG frames exist at a time.
- **Check every capture against the "Verified result to reproduce" column of `CAPTURE-PLAN.md`**, then look at frames. For numbers, re-run the probe script on this machine and compare with `R/evidence/planning-checks/run-8-verify8-captures.log`: copy `R/evidence/planning-checks` to a scratch Godot project and run `godot --path <copy> --script res://verify8_captures.gd -- $R/lab-shaders $R/evidence/planning-checks/captures.json`. If a probe disagrees by more than 0.01, stop and report; do not edit a shader.
- **Re-time after the audio exists** (Phase 3): if a beat's measured audio differs from its estimate by more than a second, scale that capture's event times in `captures.json` by the ratio, re-record that capture (`record_all.sh C0X`), and note it in `BUILD-LOG.md`. Never edit the narration.
- **D1, the docs screenshot** (beat B04): Playwright (the BrowserCapture convention), 1600 x 900 at device scale 2.4, of `https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html` with the paragraph that begins "If you need different falloff" scrolled to the middle, saved as `godot-shaders/ls-docs-2d-lights.png`. Then set the two `moves` rings in lane B04 from the real positions (the lane holds placeholders) and re-run `make_sheet.py`.
- No editor frame and no interactive editor action is needed.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_TwoLights`, `B07_Formula`, `B08_PerLamp`, `B11_FunctionBox`, `B12_Order`, `B19_Arrows`, `B23_Sun`, `B24_AimArrow`, `B25_Agree`, `B31_ScreenSpace`, `B32_Subtract`, `B34_RingFromSteps`), implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`. Film-local helpers go at the top of the file: `lamp_dot`, `unit_arrow(from, to)`, `swatch(value)`, `window_frame(w, h)` (an origin dot at the top left and a y axis that points DOWN). Draw every y axis and every angle in screen orientation (y down, angles grow clockwise) and say so in the labels that name it (B24, B31). Draw arrows as shapes, never the `->` glyph. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Definitions go on screen in the GLOSSARY words (they are written into each `visual_intent`).
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25, 50 and 95 % stills of every Remotion beat (all 28 non-Manim beats); make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

(`$R` here is the relative form: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders`.)

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for "Hallo", "Canvas Modulate", "built-ins", "U V", "x" and "y" (said as letters), "tween", "cel shading", "mod", "max", "step" against "smooth step", "light" (the noun against the function), "dot product", "sprite". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: all rows PASS, CORRECTED or EXEMPT; none OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- **Screen-space numbers are physical pixels.** Record at 1920 x 1080 at scale 1 (`record_all.sh` does). Show a capture in a ShaderLab window of about 1,900 px (1:1) and never upscale it more than 1.3x. The 3x route would draw every ring, stripe and grid three times too small.
- **GATE T and dark art.** The floor is a mid-tone dusk blue on purpose (unlit tiles about (111, 119, 145) in 255); do not darken the Canvas Modulate. The first frames of C06 (the grey card on dusk) and the unlit bulbs of C11 are the darkest things in the film: they are still well away from ink. Rings and tags use grey backing, never an ink ring over text; terracotta is never text.
- **Debug-style shaders clip by design.** The lamp's light is added on top of the ambient, so large added values reach white; that is correct, not a bug (FACTCHECK rows 8 and 31).
- **TIME-driven captures** (C01, C10, C15 to C19) use the engine clock: the beam's angle at a given second depends on how long the engine has run. That is cosmetic; do not chase it.
- **The lamp's bulb disc is `render_mode unshaded`** so it stays bright; leave it.
- A Pango `Text()` may drop single spaces on this Mac: LOOK at every still. Draw arrows as shapes. Monospace labels for built-ins in capitals (COLOR, UV, LIGHT_COLOR).
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted switches, sweeps and zooms ("scripted").
- `light()` only runs where a light reaches (the lamp's texture square): if you ever see a shader effect missing in a new capture, check the lamp's scale before suspecting the shader.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), re-time the affected capture if needed, and log it.
- Do not touch any other film's folder, any game or course repository, the shared files in `S/`, or the toolkit beyond `ShaderLab` and its registration.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, which captures were re-timed, any slate, any mispronunciation, any capture that disagreed with its verified result, and any open question for Bear (the playlist name, the third-party creator's name). Report every file by absolute path. Claim nothing you did not verify by looking at frames.

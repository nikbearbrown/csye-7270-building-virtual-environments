# BUILD-PROMPT: Shaders in 3D (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, and 19 tested shader files with six verified scene scripts. What is left is recording, building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses three shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) that the pilot film's build creates; it adds no new shared piece.
**Found.** Layout is complete and `lint_series.py` prints no errors and no warnings: 50 beats, about 1,800 words, about 10.3 minutes estimated by the lint (Liam's measured pace; the lint errs long on purpose). The title is "Shaders in 3D" on the card and "Shaders in three D" in the narrated opening and closing (`SPOKEN_TITLE` in `narration.py`). Nothing is voiced, rendered or published yet, and no Godot render is recorded (B43's four editor frames are already recorded by script, 2026-10-13). Nothing here needs a human before you start; two decisions wait for Bear after the build (the playlist name, none yet; the creators' names for the two third-party works the series follows, none used here).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`P` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders` (the pilot)
`TK` = `brutalist.art`
Evidence and scene references are in `$R/evidence/planning-checks/` (absolute: `/Users/bear/Documents/CoWork/bear-textbooks/books/$R/evidence/planning-checks/`).

Set the shorthand once per shell (the commands below use it):

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
export R=csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d
export S=csye-7270-building-virtual-environments/youtube/_godot-shaders-series
export P=csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders
export TK=brutalist.art
```

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"), and `P/BUILD-PROMPT.md` Phase 0 (the shared pieces).


## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (check; build only what is missing)

```bash
grep -c '"id": "ShaderLab"' $TK/runtime/remotion/src/scenes.json   # 1 if built
ls $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh      # all three must exist
```

If all three exist (the pilot film was built first), use them and say so in `BUILD-LOG.md`. If any is missing, build **only that piece** from `S/COMPONENT-SPECS.md`, following `P/BUILD-PROMPT.md` Phase 0 (the one toolkit edit allowed is `ShaderLab` plus its registration, then `./brutalist.art/art scene-index` and `./brutalist.art/art scenes --check ShaderLab`), and note in `BUILD-LOG.md` that the pilot's build will now find them in place. The capture harness options this film uses are listed per capture in `R/CAPTURE-PLAN.md` ("Harness options") and are the ones in `S/COMPONENT-SPECS.md`: `--scene`, `--frames`, `--fps`, `--animate name:t0:v0,t1:v1,...` (piecewise linear), `--call-at SECONDS:method`, `--set-at SECONDS:name=value`, `--renderer`, PNG-sequence output then ffmpeg to MP4, and an ffmpeg hstack for the two-renderer composites. The lamp's yaw and the meshes' swing and turn are moved by the scene scripts S2 to S4 from the harness clock, not by a harness option.

## Phase 1: record (CAPTURE-PLAN.md)

- Record **C01 to C18 and C03a** (19 clips) into `TK/runtime/remotion/public/shaders-in-3d/` with the file names in the table (the lanes use them). Write the six scene scripts S1 to S6 into `$R/capture-scenes/` (names and the assumed harness interface are in `CAPTURE-PLAN.md`); they copy their node setup from the verified references: S1 `verify2-pad-on-quad-and-box.gd`, S2 `verify9-three-meshes-picture.gd`, S3 `verify4-lamp.gd`, S4 `verify5-cull-turnaround.gd`, S5 `verify3-attach-set-tween.gd`, S6 `verify8-wrong-shader-type.gd`. Use the shader files in `R/lab-shaders/` as they are; never edit one.
- Compare each capture with the "verified result to reproduce" column. If a probe disagrees (beyond one 8-bit step), **stop and report**; do not edit the shader and do not retune the numbers.
- C02 is a **swing** (±50°), not a full turn: a full turn makes the flat square vanish (run 9a, kept).
- C15 to C17: two harness runs (`forward_plus` left, `gl_compatibility` right), each 1920 × 2160, joined by ffmpeg hstack; check both panes have the same frame count.
- More planning runs sit beside the others and are not captures: `verify11-alpha-ends.gd` (alpha 0 reads the stage color, alpha 1 the solid color) and `verify12-light-range.gd` (a lamp that does not reach a surface does not run `light()` for it), which back on-screen definitions; `verify14-color-in-spatial.gd` (a three-D fragment's `COLOR` is the vertex color), which backs the one CORRECTED row; `verify13-framings.gd`, which tried every camera size and object spacing in the table (log and contact sheet beside it); and `run-lab-checks-extra.sh` with `stripe-contrast.py`, the pad at activation 0.3 and why the held stills use it.
- D1 and D2: the two docs screenshots with Playwright (method and anchors in CAPTURE-PLAN), writing each ring box from the measured element. If the live wording differs from the sentence quoted, stop and report. (D3, the docs page for B43, was dropped on 2026-10-13: B43 shows the editor, below.)
- Clip lengths in the table are design lengths: re-time them to the measured beat durations as `CAPTURE-PLAN.md` says ("Audio-first timing"). `ramp.period` in `lanes/` is `__AUDIO__`, so `make_sheet.py` fills it with the beat's duration, which is the swept clip's length.
- **B43's editor frames (E1) are already recorded by script** (CAPTURE-PLAN "Editor frames (B43)"); nobody clicks or records by hand. Copy the four frames `renderer-path_R1-A`, `R1-C`, `R1-D`, `R1-E` from `S/editor-capture/png/1920x1080/renderer-path/` (native 3456x1944 twins in `png/3456x1944/renderer-path/` if a sharper source is wanted) and join them with ffmpeg cross-dissolves at the fractions in `R/lanes/act5.json` (the `show` list of B43) into `TK/runtime/remotion/public/shaders-in-3d/editor-renderer.mp4` at the beat's measured duration. Label the clip "scripted editor session". The ring boxes in the lane are fractions of the whole 1920x1080 frame; if GATE T flags the dark editor UI, crop to the dialog (the `.dialog.png` files in the same folder) and recompute the boxes. If a frame is missing, write a state script by copying `S/editor-capture/state-scripts/followup/rp-editor.json` and run it as `S/editor-capture/README.md` sections 7 and 11.9 say. The film shows no other editor panel.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/`: `B02_Anatomy`, `B03_TwoTypes`, `B04_ThreeFunctions`, `B05_CodeMorph`, `B09_AttachChain`, `B13_LitPipeline`, `B18_TwoChecks`, `B20_Ramp`, `B21_FractRamp`, `B22_StepSwitch`, `B24_MixLine`, `B35_MissingSlots`, `B40_TwoLanes`, `B41_TwoMidpoints`. Implement each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json` with `shader_kit` objects (ramp strip, pixel grid, plot, vertex quad, UV square, code card). Use the real code files from `R/lab-shaders/` in the code cards (`03-skeleton-3d`, `01-flat-teal-2d`, `02-flat-teal-3d`, `12-signal-pad`). Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6): no `show` event starts inside 45 to 55 % of a beat, and no animation may be running at the midpoint: one that would cross the window is finished by 0.44 or started at 0.56, with a hold between (the lanes' event notes say which are already timed that way). The kit's `ramp_strip` is a row of narrow tiles with gaps (a continuous grey bar reads as a text blob to GATE T): never draw one as a solid bar. Every Manim beat that defines a word does it in a caption in the GLOSSARY's exact words, written out in that lane's `visual_intent`, and the caption must be on screen when the voice first says the word. The small-word ones: B05 `alpha: how visible a pixel is: 0 invisible, 1 solid`; B21 `fract(x): the part after the point: x minus floor(x)` with `floor(x): rounds down to the whole number below` under it; B22 `step(edge, x): 0 below the edge, 1 from the edge up`; B24 `mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b`, then the formula `a × (1 − t) + b × t`; B40 `linear: the scale light adds up on, in a straight line` and under it `sRGB: the scale a color picker's numbers use, spaced for the eye`. The ShaderLab beat B38 carries the `caption` `channel: one of red, green, blue or alpha`.
2. The ShaderLab and Remotion beats need only their props, already in `lanes/`; `durationSeconds` fills from the audio. Re-time the `CCPlainShell` frame cues in B06 (24 fps) to the measured audio. ShaderLab features this film relies on (all in `S/COMPONENT-SPECS.md`): cue `label` tags that define a word on the code line using it (B07, B08, B14, B16, B17, B23, B31, B32, B33), a looping `ramp.period` (B25, B34; equal to the beat's duration, matching the sweep), and `stack` with a one-line excerpt (B07 quotes line 1 of `18-two-d-shader-on-a-mesh`, B08 quotes line 5 of `06-uv-colors-3d`; `codeFile` says which line). Cue lines count within the code shown, so the excerpt's cue is line 1.
3. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.** `_gen_lanes.py` is the single source for `lanes/*.json` and `SHOTLIST.md`; if a lane must change, edit it there, run `python3 _gen_lanes.py && python3 make_sheet.py`, and log it.
4. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion and ShaderLab beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for "Forward Plus", "vec three, vec four", "s R G B" (B40 and B42), "U V", "albedo", "unshaded", "fract", "tween", "Godot", and the letters in B24 ("Mix of a, b and t is a times one minus t, plus b times t"): the phonemizer reads the single letter "a" like the article ("uh") and "t" as "tee", so check that B24 is still clear and report it if not. The narrated title is "Shaders in three D" (`SPOKEN_TITLE`); the title card keeps "3D". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`, every row PASS, CORRECTED or EXEMPT, none OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (design around them)

- **The pad's rust frames and GATE T**: rust and its dark stripes are within 48 RGB of ink. Captures are timed so the 50 % and 85 % frames are mid-tone; the held stills of the pad are at activation 0.3 because its stripes cannot be seen at 0.5 (`stripe-contrast.txt`); if a frame is still flagged, hold 0.4, then 0.5, for that beat and log it. Ink-colored rings and any dark small shape beside mid-tones fail; ring with grey. Terracotta is never text.
- **Lab limits**: the Lab's `quad3d` scene (white ambient light, no lamp) makes lit and unshaded identical; lit versus unshaded exists only in the lamp scene S3. Two Lab checks (04 and 05) fail on purpose; their messages are the evidence.
- **A flat square vanishes from behind** (default culling): S2 swings, S4 turns on purpose.
- **Probe positions**: stripe probes go at UV.x 0.03125 (dark) and 0.09375 (light), never at the edges 0.0625 or 0.1875.
- **Forward+ encodes unshaded albedo for the screen**: `ALBEDO = 0.5` reads 0.737, so never quote a UV or albedo number as the pixel; the film quotes only the measured values in `FACTCHECK.md`.
- **Long code lines**: the pad's two `uniform vec4` lines are 70 characters; wrap them in `ShaderLab` (pre-wrap), keep the type floor.
- A Pango `Text()` may drop single spaces on this Mac: look at the still; double the space at a fused boundary (the formula `a × (1 − t) + b × t` in B24 and `x × 8` in B21 are the risks). Draw arrows as shapes.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input (the lanes already do).
- `check_shader.sh` serializes Lab runs with a lock shared by every shader film; a run may wait up to three minutes.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (a docs sentence moved, a mispronunciation that needs a different wording), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, `liam.json`, or the toolkit beyond `ShaderLab` (and only if it was missing).
- Do not edit any file in `R/lab-shaders/` or `R/evidence/planning-checks/`; add new evidence beside them if you need it.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 (or that it already existed) and where, any slate, any mispronunciation, any capture that disagreed with its verified result, and what GATE T did with the pad frames. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

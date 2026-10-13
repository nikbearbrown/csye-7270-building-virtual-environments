# BUILD-PROMPT: SubViewports (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check (74 rows, no OPEN, four corrections), the capture plan with a verified result for every capture, tested shader files, and the editor frames' state scripts. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This session needs judgment only where a gate fails; everything else is a command or a transcription of a file that already exists.
**Found.** Layout is complete and lint-clean: 46 beats, about 10.5 minutes estimated at Liam's pace (1,840 words by the lint's count). Nothing is voiced, recorded, rendered or published. Three things differ from the pilot's build and cost time if missed: **every Godot recording runs with the window on top** (a covered window is drawn on only some frames and Movie Maker writes repeated frames), **frame 0 of a SubViewport scene lacks the pictures** (pre-roll one frame), and **Update Mode Once is spent by the next draw, not the next frame** (the c21 clip needs a draw on every frame). Human items: none unless the editor driver fails (section 1 of Phase 1) and the playlist name (none yet).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`
`PILOT` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders` (the first shader film; it builds the three shared pieces if they do not exist yet)

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (the components and the capture harness), `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md` (**read all of it**: it holds the route, the rules and the numbers), `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`, `R/evidence/planning-checks/RESULTS.md` (the covered window section).
5. `S/editor-capture/README.md` (the series' editor driver, used here for the editor frames).
6. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating") and, if it has been built, `PILOT/BUILD-LOG.md`.


**This film's editor frames** are recorded by the same series driver from this film's own state scripts (Phase 1, step 6). The film also keeps its own earlier driver (`R/evidence/planning-checks/run-editor-labels.sh`, used for the label log); either may be used, the series driver gives the whole editor window and the popups.

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (check; build only what is missing)

Spec: `S/COMPONENT-SPECS.md`. This film needs `ShaderLab` (layouts `side` and `video`, cue `label`, `readouts`, `rings`, `ramp`, `caption`, a PNG still), the Manim kit `shader_kit.py`, and the capture harness (`S/lab/capture.gd` + `S/lab/capture_shader.sh`).

1. Check what exists: `ls S/shader_kit.py S/lab/capture.gd S/lab/capture_shader.sh` and `./brutalist.art/art scenes --check ShaderLab`. If `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/BUILD-LOG.md` shows its Phase 0 DONE, all three exist: reuse them and go to step 3.
2. If any is missing, build it per the spec (ShaderLab as one Remotion composition in `TK/runtime/remotion/src/scenes/` registered in `Root.tsx`, then `./brutalist.art/art scene-index`; this is the only place you may edit the toolkit). Log it in `R/BUILD-LOG.md`.
3. **Add this film's Manim kit objects** to `S/shader_kit.py` (and list them in `R/BUILD-LOG.md`): `viewport_box(label)` (a dashed box that fills), `picture_card`, `blob_sprite` (the teal blob with two cream eyes), `screen_frame`, `shader_tag(text)` (an "inner shader" / "outer shader" tag), `hue_wheel`, `plateau_plot`, `mesh_grid(n)`, `cursor_arrow`. They follow the kit's rules: Claude palette, terracotta only as dots, rings and sparks, never as text; `ramp_strip` as a row of 48 to 64 tiles with gaps (GATE T reads a continuous grey strip as text).
4. The harness must accept the film's scene library (`R/evidence/planning-checks/capture_scene.gd`, `class_name CaptureScene`) through an adapter: `CaptureScene.new(id, shaders_dir)`, `build(canvas)`, `update(t)` with t rising frame by frame from 0, `duration`. `R/evidence/planning-checks/movie_scene.gd` is a working adapter for scale 1 under Movie Maker; the 3x route is the code block in `R/CAPTURE-PLAN.md` section 1.

## Phase 1: record (CAPTURE-PLAN.md)

1. **Check the engine**: `godot --version` must start `4.7.2`. The verified numbers are for 4.7.2 on Apple silicon (Metal). If it differs, stop and report.
2. **Window on top, every time.** Every Godot window you start for a recording gets `--always-on-top` (or `--position 0,0`). Without it a covered window is drawn on only some frames and the clip freezes (`R/evidence/planning-checks/RESULTS.md`, the covered window). After each recording count the distinct frames (`R/evidence/planning-checks/analyze-movie.py distinct <dir> <N>`): it must equal N. A harness that saves the SubViewport's texture itself should use **recipe B** (`CAPTURE-PLAN.md` rule 4: `render_loop_enabled = false`, then one `force_draw(false, 1.0 / 30.0)` per step), which needs no window at all and moves shader `TIME` exactly 1/30 per step; Movie Maker needs the regular loop, so it keeps the window on top.
3. **Record C01 to C21** (22 clips: C04 is C04a and C04b; C15 is one PNG) on the SubViewport native-size route, 30 fps, offline, one real draw per step (`CAPTURE-PLAN.md` section 3, rules 1 to 9), into `TK/runtime/remotion/public/subviewports/` with the names in the "File" column. **Pre-roll one frame** (drop frame 0). Use `speed=` only after the voice is measured, and only for a scene whose event lands more than 0.7 s from its words (rule 6).
4. **Compare each recording with its "verified result" column** in `CAPTURE-PLAN.md` (the same probes are in `R/evidence/planning-checks/verify7_capture_rehearsal.gd`; `./run-all-checks.sh` there reproduces every number in about ten minutes, `SV_SKIP_LAB=1` skips the Lab batch). If a probe disagrees, **stop and report**: do not edit a shader or a scene. Compare c21 and c13 through the real harness first; the Movie Maker half and the 3x half of the route were verified separately, not together (CAPTURE-PLAN.md section 7).
5. **Label scripted moves** (the videos' `videoLabel`s already say "scripted"); no capture scripts input.
6. **Editor frames.** Run `R/evidence/planning-checks/run-series-driver.sh` (the series' editor driver with this film's six state scripts in `editor-driver/state-scripts/`: `subviewports-E1`, `-E4`, `-E3` and the same three `-wide`; it takes the shared Lab lock, turns Single Window Mode on, puts `--always-on-top` on every Godot process through a wrapper, and writes `R/evidence/planning-checks/editor-frames/series-driver/<mark>.png` at 1920 x 1080; about eight minutes). Every run must report `errors=0` in `logs/run-15-series-driver-*.log`; **look at every frame**. Then build `e1-setup.mp4` (B04: `subviewports_E1-1_subviewport-size`, `subviewports_E2-1_texture-dropdown-new-viewporttexture`, `subviewports_E2-4_viewport-path-set`) and `e4-materials.mp4` (B12: `subviewports_E4-1_inner-sprite-material`, `subviewports_E4-2_display-material`, `subviewports_E4-5_shader-editor`) with `ffmpeg`, each frame held for its share of the beat (the `show` times in `lanes/act1.json` and `act2.json`) with a half-second cross-dissolve, and put them in `TK/runtime/remotion/public/subviewports/`. The video label says "scripted editor session". If the driver fails, fall back as `CAPTURE-PLAN.md` section 5 says (the film's own `run-editor-labels.sh`, then **stop and ask Bear** for the short recording listed there).
7. **Re-check two lines of narration against the real frames**: B04 says "open the menu, and under New choose Viewport Texture" (the Texture slot's menu has the heading New and the entry ViewportTexture: `subviewports_E2-1`), and B12 says each sprite's Material slot holds a Shader Material (`subviewports_E4-1`, `E4-2`). Change a line only if a label differs, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py R --only <BID>`), and log it.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/`: `B02_OffScreenBox`, `B05_CodeBuilds`, `B11_TwoPlaces`, `B16_WhichTurns`, `B19_Flattened`, `B21_Diagonal`, `B22_Saw`, `B23_StepStripe`, `B26_ColorWheel`, `B27_HueRamp`, `B28_Plateaus`, `B31_FourCorners`, `B32_CutIntoGrid`, `B36_WholeChain`, `B37_StageToStage`, `B39_ClickBounces` (16). Implement each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects; the code a Manim beat shows is the real lines (B05's five lines are in its `visual_intent`). Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Assemble with the sibling's `assemble_scenes.py` pattern.
2. `python3 R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while the narration is unchanged). **Never re-run it after `art final`.** (`R/_gen_lanes.py` regenerates `lanes/` and `SHOTLIST.md`; run `python3 R/_gen_lanes.py && python3 R/make_sheet.py` only if a lane must change.)
3. Stills first: a last-frame still of every Manim class and 25, 50 and 95 percent stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `R/BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports              # free; measured durations become the clock (already done if you followed HOW TO RUN)
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/opening --sheet $PWD/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/beat_sheet.json --width 3840
mkdir -p csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/media && cp csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/opening/example-opening-*s.mp4 csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports --height 2160 --out csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports
```

**Voice check** (transcribe with faster-whisper, compare with `narration.py`): listen for "Sub Viewport" (the title is spoken "Sub Viewports": `SPOKEN_TITLE`), "Viewport Texture", "U V" (never a lone "U" or "V"), "fract" (rhymes with tract), "Premultiplied Alpha", "Transparent B G", "Mesh Instance two D", "Quad Mesh", "sine", "amplitude", "Hallo", "Godot". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: 74 rows, 0 OPEN, 4 CORRECTED), the PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- **A covered Godot window stalls everything that waits for frames**: Movie Maker writes repeated frames, `await frame_post_draw` can hang, Update Mode Once is spent late, and shader `TIME` stands still on every frame the regular loop skipped (it advances only in a draw, by that draw's frame_step; `force_draw(false)` passes 0). `--always-on-top` for Movie Maker, recipe B for a harness that saves textures itself, and count the distinct frames either way.
- **Frame 0 of a SubViewport scene has no pictures** (14 of 22 scenes): drop it or `skip=1`.
- **Premultiplied alpha is the point of B10 and c06**: do not "fix" a scene's blend. Sprites shown with Premultiplied Alpha need transparent-black padding (`blob_image(size, false)`); default-blend ones need teal padding. The fade is `COLOR = texture(TEXTURE, UV) * UV.x` with `render_mode blend_premul_alpha`, never `COLOR.a = UV.x`.
- **Numbers at scale 1**: pixel counts and display-pixel positions in `CAPTURE-PLAN.md` are on the 1280 x 720 canvas; the 3x route multiplies positions by 3 and counts by 9. Nothing on screen quotes them.
- **`ShaderLab` code is the tested file text** (lines from `R/lab-shaders/`), at most 14 lines; `LectureCodeTrace` at most 10 and its focus only moves down. Cue labels are at most 60 characters in GLOSSARY wording.
- **The series editor driver records popups only with Single Window Mode on** (its README); `run-series-driver.sh` passes that settings file.
- **Inspector labels truncate in the narrow dock** ("Transparent" for Transparent BG, "Subdivide Wi", "Premultiplied A"): ring only labels that show in full, or use the driver's `dock_split` step to widen the Inspector (see `S/editor-capture/state-scripts/final/drawing-shapes-E1-wide-inspector.json`).
- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text. Frame captures in a ShaderLab window on the cream stage and check the 50 and 85 percent marks (the glow ring c06 and the clear-coloured picture box are mid-tones).
- A Pango `Text()` may drop single spaces on this Mac; LOOK at the still. Draw arrows as shapes.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free (a 4K PNG is about 30 MB before ffmpeg).
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted moves. No speed or cost figure appears anywhere in this film; do not add one.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example an Inspector label), change only that line, re-run `make_sheet.py`, re-voice that beat, and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`. Do not edit anything in `S/` (the series folder) except the shared pieces Phase 0 says to build.
- Take the shared Lab lock (`/private/tmp/claude-501/shaderlab.lock`, a directory made with `mkdir`) around any Godot window run that is not the series driver (the driver takes it itself).

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result (with the numbers), the editor frames used, and any editor action that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

# BUILD-PROMPT: Reading the Screen (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, 15 tested shader files, and **all 23 Godot capture scenes, already written and run**. What is left is voicing, recording, building eleven Manim scenes, and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. Recording the captures is one command because the judgment (what each capture shows, when, and what it must measure) is already in the scene scripts.
**Found.** Layout is complete and lint-clean: 44 beats (38 in the body), 1,685 words, 9.6 minutes by the lint's ceiling formula. Nothing is voiced, recorded, rendered or published yet. Of the 23 Godot captures, 22 go through a 3840 x 2160 SubViewport over a 1280 x 720 canvas and one (C13, the mip-level blur) is recorded natively at 1920 x 1080, because a blur level counts texels and is less than half as strong on the 4K route (`R/CAPTURE-PLAN.md`, Routes); `capture_all.py` picks the route for you. Two things may be missing from the toolkit and are built in Phase 0 only if absent: the `ShaderLab` Remotion component and the Manim helper kit `shader_kit.py` (shared by every shader film). Nothing needs a human decision before the build.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reading-the-screen` (absolute: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reading-the-screen`)
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`
`EV` = `$R/evidence/planning-checks`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `EV/RESULTS.md`.
5. A finished sibling for the Manim kit and scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reading-the-screen
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reading-the-screen/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reading-the-screen/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (reuse; build only what is missing)

1. **`ShaderLab`** (Remotion). Check: `./brutalist.art/art scenes --check ShaderLab`. If it is not renderable, build it from `S/COMPONENT-SPECS.md` in `TK/runtime/remotion/src/scenes/`, register it in `Root.tsx`, run `./brutalist.art/art scene-index`, and check again. This film uses layouts `side` and `video`, cues with a rendered `label` (at most 60 characters), `readouts`, `rings`, `title` and `videoLabel`. The toolkit rules apply (`TK/CLAUDE.md` rule 10; render only through `runtime/scripts/remotion_scenes.py`). This is the only place you may edit the toolkit: one file plus its registration; say so in `BUILD-LOG.md`.
2. **`shader_kit.py`** (Manim helpers) at `S/shader_kit.py`. If it is missing, build it from the spec (this film uses `pixel_grid`, `code_card`, `uv_square`, and drawings of bars, frames and panes in the Claude palette). `assemble_scenes.py` pastes it above the scenes like the sibling's `kit.py`.
3. **Not needed:** the shared capture harness (`lab/capture.gd`). This film brings its own driver, `EV/scene_capture.gd`, written and tested (8 frames of C01 and two tiny end-to-end captures: `EV/run-21-*.log`, `EV/run-22-*.log`).

## Phase 1: voice first (the captures are fractions of each beat's length)

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 $R/evidence/planning-checks/capture_all.py --dry-run                    # the 23 captures with their measured lengths
```

Voice check: transcribe with faster-whisper and compare with `narration.py`; listen for "sampler two D", "U V" and "screen U V", "r g b", "texture lod", "mipmap", "Back Buffer Copy", "Full Rect", "set shader parameter", "Godot four", "post-processing", "Forward Plus", "Compatibility", "aspect ratio". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Phase 2: record the 23 Godot captures (no judgment needed)

Every capture is a scene script in `EV/` (`scene_c01_pool.gd` to `scene_c23_finale.gd`) that is a pure function of time. `capture_all.py` reads each lane's video name and scene and each beat's measured length, runs `EV/run-checks.sh capture ...` (a scratch Godot project built from `EV/` and `$R/lab-shaders/`, Forward+, fixed 30 fps tick; 22 captures through a 3840 x 2160 SubViewport over the 1280 x 720 canvas and C13 natively at 1920 x 1080 with `--native`, see `R/CAPTURE-PLAN.md`, Routes), encodes with ffmpeg, and deletes the PNG sequence.

```bash
python3 $R/evidence/planning-checks/capture_all.py --only C02             # try one first
python3 $R/evidence/planning-checks/capture_all.py                         # all 23 into brutalist.art/runtime/remotion/public/reading-the-screen/
```

- Check disk first (`df -h /`; stop under about 15 GB free). One capture at a time; each is a long 4K PNG sequence.
- **LOOK** at the 50 % and 85 % frame of each video and compare it with `EV/frames/<scene>-u50.png` and `-u85.png` (the same scenes at 10, 50 and 85 %; the three C13 frames are 1920 x 1080 because C13 is the native-route capture, and its probe is the mean difference between its 85 % and its 30 % frame inside the window). The "Verified result to reproduce" column of `R/CAPTURE-PLAN.md` gives the probe values; if a recording disagrees, stop and report: do not edit a shader or a scene to make it agree.
- Every capture is a render of a scripted scene at a fixed tick: it says nothing about real-time frame rate. The `videoLabel`s say "scripted" where they are.
- If a probe or label in `R/FACTCHECK.md` needs re-checking (a new Godot patch version, for instance), `EV/run-checks.sh verifyN [forward_plus|gl_compatibility]` re-runs any check, and `EV/editor-labels/run-editor-labels.sh` re-reads the editor's own labels.

## Phase 3: scenes (Manim) and sheet

1. Write `R/scenes.py` (Manim): the eleven classes named exactly as in `lanes/` and `SHOTLIST.md`: `B02_TheCopy`, `B04_ThePieces`, `B05_FilledEveryFrame`, `B06_AddressToColor`, `B07_TwoAddresses`, `B11_FullRect`, `B12_LayerStack`, `B13_ClicksStop`, `B14_WeightedSum`, `B18_StretchedAddresses`, `B30_OnceBeforeTheFirstReader`. Implement each `visual_intent`, `motion_claim` and `show` cue from `lanes/act*.json`, with the on-screen definitions the intents give (they are the GLOSSARY's wording). One cast per act; labels one to three words; arrows drawn as shapes. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). The other 27 body beats are Remotion: 25 `ShaderLab` captures (props already in the lanes), `LectureCodeTrace` (B10) and `LectureEvidenceTable` (B38).
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 4: title card, render, master

```bash
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

## Gates that must PASS

Gate F (`FACTCHECK.md`: 77 rows, none OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and ones to expect)

- GATE T reads dark ink-like colours as text. The flipped meadow (purple and navy) and the gray meadow were checked (`EV/palette-check.py`: at least 61 RGB from INK and MUTE) but LOOK at C04, C18 and C19 frames; do not add ink-coloured outlines or rings: ring with grey. Terracotta is never text.
- The cream window frames are drawn on a high canvas layer on purpose (a frame inside a copy of the screen is flipped to near-black by an invert window). Do not "simplify" them into children of the windows.
- Never crop a capture past the frame edge (C22 has a window flush with the right edge).
- A Pango `Text()` may drop single spaces on this Mac; LOOK at the still. The `->` glyph is under the type floor: draw arrows as shapes. Code in B04 and B05 is set token by token at explicit coordinates.
- `LectureCodeTrace` holds about 10 lines (B10 has 5). `ShaderLab` cue `label` is at most 60 characters.
- BHTF reads the prompt and then the two checks aloud; `props.command` holds only the prompt. That is settled; do not "fix" it.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input. Captures are Forward+. The film names a renderer difference in one place only (B36: Forward Plus obeys `filter_nearest`, Compatibility blends anyway); everything else it claims held in both renderers.
- **Capture size matters for a blur.** Never re-record C13 through the 4K route: the same mip level is less than half as blurred there (`EV/verify10.gd`). `capture_all.py` already records it natively; if you record one scene by hand, use `run-checks.sh capture scene_c13_blur <seconds> forward_plus --native --width 1920 --height 1080`.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), re-record the capture that beat uses (`capture_all.py --only <Cnn>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`. Do not edit shared files in `S/` except creating `shader_kit.py` if it is missing.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, which captures were recorded and whether each matched its verified result, any slate, any mispronunciation, and anything that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

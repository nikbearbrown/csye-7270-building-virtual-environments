# BUILD-PROMPT: Outlines (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan with 27 ready-to-play scene specs, and 14 tested shader files. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film needs no editor frames and no new Godot knowledge: every capture is a small JSON spec played by a reference scene player.
**Found.** Layout is complete and lint-clean: 47 beats (41 body), 1,855 spoken words (the lint counts 1,868 with the terms card), about 10.7 minutes estimated at Liam's pace. Fact-check has 81 rows and none is OPEN. Nothing is voiced, recorded, rendered or published yet. Open items that need a human: none for the build; Bear's decisions are the creator's name for the credit line and whether the film joins a playlist (none is named).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`. In every shell you open, set the three names first (the commands below use `$R`):

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
export R=csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines
export S=csye-7270-building-virtual-environments/youtube/_godot-shaders-series
export OUTLINE_FILM_DIR=$PWD/$R
```

`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (ShaderLab, shader_kit, the capture harness), `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md` (the contract for every capture), `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. `R/evidence/planning-checks/RESULTS.md` (what every number rests on) and, for the capture route, `R/evidence/planning-checks/route_check.gd`.
6. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").


## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (check first; build only what is missing)

Spec: `S/COMPONENT-SPECS.md`. Another shader film (the pilot, `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/`) builds these first. Look for them before writing anything:

```bash
ls brutalist.art/runtime/remotion/src/scenes/ShaderLab.tsx 2>/dev/null
ls csye-7270-building-virtual-environments/youtube/_godot-shaders-series/shader_kit.py csye-7270-building-virtual-environments/youtube/_godot-shaders-series/lab/capture.gd 2>/dev/null
./brutalist.art/art scenes --check ShaderLab
```

If all three exist, use them and skip to Phase 1 (log "Phase 0 skipped: found" in `BUILD-LOG.md`). If one is missing, build it from the spec: **`ShaderLab`** (a Remotion composition in `TK/runtime/remotion/src/scenes/`, registered in `Root.tsx`, then `./brutalist.art/art scene-index`; this is the only toolkit edit you may make, and say so in `BUILD-LOG.md`), **`S/shader_kit.py`** (Manim helpers: ramp strip, pixel grid, uv square, code card; ghost copies here are plain circles), and the **capture harness** `S/lab/capture.gd` + `S/lab/capture_shader.sh`.

Then add this film's one harness piece, described in `R/CAPTURE-PLAN.md` ("One harness addition"): a mode that plays a JSON scene spec with `R/evidence/planning-checks/scene_player.gd` through the SubViewport native-size route and writes a PNG sequence. `R/evidence/planning-checks/route_check.gd` is a working example of exactly that route; copy its setup (3840 by 2160 SubViewport, `size_2d_override` 1280 by 720 with stretch, `input_viewport` set for scripted keys).

## Phase 1: record (CAPTURE-PLAN.md)

- Set `OUTLINE_FILM_DIR` to `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines`. For each of the 27 specs in `R/evidence/planning-checks/scenes/` (C01 to C40; 26 clips, 1 still) render into `TK/runtime/remotion/public/godot-outlines/` as `<spec id>.mp4` or `<spec id>.png`, each clip stretched to its beat's measured audio (see the audio-first section above). Every capture uses the native-size route; none reads window pixels.
- Compare each against the "Verified result to reproduce" column of `CAPTURE-PLAN.md`: measure the saved frames with `R/evidence/planning-checks/ol_measure.py` (colors: line (64, 64, 191), teal (95, 163, 145), stage (217, 213, 202)). At 4K multiply the canvas figures by 3. If a probe disagrees, stop and report; do not edit a shader or a spec.
- D1: the docs screenshot with Playwright (`CAPTURE-PLAN.md`).
- No editor frames are needed for this film.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/`: `B03_TheQuestion`, `B04_NextDoor`, `B05_FourNumbers`, `B06_MixRamp`, `B11_StepInPixels`, `B15_GhostCopies`, `B20_ThreeByThree`, `B22_CostBars`, `B23_Guard`, `B24_Agree`, `B35_BrushShapes`. Implement each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects. Numbers on screen are the ones in `FACTCHECK.md` (B22 bars: 10, 24, 44 and 71 ms, the whole-millisecond medians in `R/evidence/planning-checks/cost-summary.txt`; B35: axis 8 and diagonal 5.1, 11.4, 8.1; B20 and B23 messages from `lab-shaders-check.log`). Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Assemble with the sibling's `assemble_scenes.py` pattern.
2. Remotion beats are in the lanes: B12 `BrowserCapture` (D1), B30 `LectureCodeTrace` (the 10-line function, lines 3 to 12 of `R/evidence/planning-checks/padding_snippet.gd`), B41 `LectureEvidenceTable` (four rows). Check each with `./brutalist.art/art scenes --check <Name>`.
3. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
4. Stills first: a last-frame still of every Manim class and 25, 50 and 95 percent stills of every Remotion and capture beat; make a contact sheet; LOOK at them before any 4K render. Write what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock (skip if already done above)
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for "U V", "vec two", "vec four", "texture pixel size", "blit rect", "region rect", "varying", "modulate", "sine", "cosine", "alpha", "uniform" and "Godot". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: 81 rows, 0 OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- **BHTF narration reads the prompt and then the two checks aloud; `props.command` holds only the prompt and `output` holds the checks.** That is settled (the shipped Why Godot film does exactly this and passed `bookend_check`). Do not "fix" it.
- The BIDEA text has its line break before the trigger phrase on purpose (a break inside the trigger makes the correction never fire).
- **Scripted keys (C26) must be pushed into the SubViewport** (`player.input_viewport`), and the clip is rendered in one pass from t = 0 (events fire once, in order). Label it "scripted input".
- The stress-test numbers in B22 and B36 are from `cost-summary.txt` (wall-clock, vsync off, window kept on top, median of the valid runs; the narration says "about"). Do not re-run that test during the build: a covered window gives garbage (6.9 ms for every shader) and the film's numbers are the audited ones.
- C39's counts (0 and 2,008 half-transparent pixels) are for the whole sprite at 2x, not for the 12x crop on screen; the label says so. Keep that label.
- The thin-part gap (C37) depends on the row: it is on image row 17; do not "improve" the picture by changing the sprite.
- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text. The 3 by 3 block (B20) and the pixel grids (B03, B23, B24) are outline-only cells with padding.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes (the `->` glyph is under the type floor).
- Real captures fail GATE T at the 50 percent frame only if they hold dark regions next to mid-tones; the stage and sprite colors were chosen to avoid it. The 12x close-ups (C38, C39) fill the window with flat teal and indigo: check them at the 50 and 85 percent marks.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where (or that it was found), any slate, any mispronunciation, any capture that disagreed with its verified result, and any decision that needs Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

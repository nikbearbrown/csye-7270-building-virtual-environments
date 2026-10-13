# BUILD-PROMPT: Time and Waves (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, thirteen tested shader files, and eight scene scripts that already run under Movie Maker. What is left is recording, drawing the Manim scenes, voicing and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. Nothing in this folder has been voiced, recorded, rendered or published.
**Found.** Layout is complete and lint-clean: 40 body beats, 1,679 words, about 9.6 minutes estimated at Liam's measured pace. Open items that need a human: none for the film itself; the playlist name does not exist yet (never type one) and the creators of the third-party source are not named (`SOURCES.md`).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-time-and-waves`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`P` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders` (the first film of the group; it builds the shared pieces)
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; films are never numbered) and `TK/skills/make/nopunt/SKILL.md`.
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/ACTS.md`, `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`.
5. `R/evidence/planning-checks/RESULTS.md` (what was run and what it showed) and `docs-quotes.md`.
6. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"), and `P/BUILD-LOG.md` once it exists.

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-time-and-waves
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-time-and-waves/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-time-and-waves/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces

If `S/shader_kit.py`, `S/lab/capture.gd` + `capture_shader.sh` and the `ShaderLab` composition already exist (the first film's build creates them), reuse them. If not, build them first exactly as `P/BUILD-PROMPT.md` Phase 0 and `S/COMPONENT-SPECS.md` say, then continue. This film needs from them:

- `ShaderLab` layouts `side`, `video` and `code` (B17 is `code` only: the real 13-line file with paced line focus; its last cue highlights the blank line 6 and tags it 'a fourth dial waits here: frequency', so a highlight on a blank line must draw, label included) and the props `title`, `cues`, `readouts`, `rings`, `ramp`, `caption`; register it and run `./brutalist.art/art scene-index`; `./brutalist.art/art scenes --check ShaderLab`.
- A harness route for **scene scripts** (a `.tscn` whose root script runs the scene; frame-counted events; one scripted mouse click; `Engine.time_scale`; `paused`; a CurveTexture made in code). The eight scripts and their `.tscn` files are in `R/evidence/planning-checks/scene-project/scenes/` and already record correctly with `godot --path <copy of scene-project> --always-on-top --write-movie out/f.png --fixed-fps 30 --quit-after N res://scenes/<file>.tscn`.
- Four film-local Manim helpers (not in the shared kit; promote them if another film wants them): `knob_slider(label, lo, hi)`, `time_ruler(label, zero_offset)`, `curve_strip(curve)`, `bracket(a, b, label)`.

## Phase 1: record (`CAPTURE-PLAN.md`)

- Copy `R/evidence/planning-checks/scene-project/` to a scratch folder before running (running in place would create a `.godot` cache inside the film folder). `scene_common.gd` holds the absolute path of `R` in its `FILM` constant; change it only if the folder moves.
- Record the eighteen captures listed in `CAPTURE-PLAN.md` (C01, C03, C07, C13, C18, C21, C23, C27, C28, C29, C31, C32, C33, C34, C35, C38, C39, C40) at 3840 × 2160 into `TK/runtime/remotion/public/godot-shaders/time-and-waves/` with the file names the lanes use (`late-join.mp4`, `scale-and-pause.mp4`, `age.mp4`, `pulse.mp4`, `rolling-row.mp4`, `three-shapes.mp4`, `curve-loop.mp4`, `stripes.png`, `travel.mp4`, `rings.mp4`, `ripple.mp4`, `flag.mp4`, `smear.png`, `two-waves.mp4`, `together.mp4`, `breath.mp4`, `banner.mp4`, `wind-click.mp4`, `docs-time.png`).
- **Keep the Godot window drawn** (`--always-on-top`; do not touch the machine): a hidden or covered window stops drawing and `TIME` freezes.
- Compare each recording with the "Verified result to reproduce" column. The decoders `decode_scenes.py` and `decode_scenes2.py` in `scene-project/` show how (they read frames recorded with `-- --verify`, which draws a TIME encoder in the corner: never in a real capture). If a probe disagrees, stop and report; do not edit a shader.
- D1: the docs screenshot with Playwright (`CAPTURE-PLAN.md`); measure the ring box on the real image and put it in the B02 lane's last `moves` entry (a placeholder box is there now).
- Trim, never retime: choose each capture's head trim so the event lands on the spoken word (the lane's `show` cues name the words), and apply the pale-pulse rule in `CAPTURE-PLAN.md` for C13, C23 and C38.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): the 18 classes `B04_RolloverJump`, `B05_TwoZeros`, `B06_Drift`, `B09_SineOfTime`, `B10_TauTurn`, `B11_ClampedHalf`, `B12_HalveAndLift`, `B14_Amplitude`, `B15_Speed`, `B16_Offset`, `B19_Restart`, `B20_Fold`, `B22_CurveStrip`, `B24_SineOrRamp`, `B26_FiveToEvery`, `B30_FourKnobs`, `B36_BreathCurve`, `B37_LookCloser`, named exactly as in `lanes/`, each implementing its `visual_intent`, `motion_claim` and `show` cues from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects and the film-local helpers. Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Numbers printed on pictures must be the measured ones: B05 "0.26, 0.29, 0.26 s" and "about 0.25 s", B06 "+0.5 s", B04 "limit at 2 s". Colors: the Lab stage `#D9D5CA`, teal `#5FA391`, cream `#FAF9F5`; terracotta only as dots, rings and sparks; draw the ramp strip in greys; no large near-black fields; no `->` glyph (draw arrows).
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for **tau**, **fract**, **sine**, **sawtooth**, "thirty-six hundred", "U V", "delta", "curve texture", "tween", "instance uniform" and "Godot". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear. After the audio exists, re-check the cue fractions that rest on word positions (`lanes/` were placed by word count): if a spoken word lands more than half a second from its event, shift the capture's head trim, not the narration.

## Gates that must PASS

Gate F (`FACTCHECK.md`: 85 rows, none OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- GATE T at 4K reads dark UI, dark outlines and flat terracotta as "text blobs": ring with grey, never ink; terracotta is never text. The Lab stage and the teal test sprite were chosen to avoid this; the squares and banner are mid-tone, the checker is teal and cream. Check the 50 % and 85 % frames.
- Gate V underfill and separation: pale cream phases of a pulse against the light stage can fail the separation test; fix with the head trim (`CAPTURE-PLAN.md`), never by editing a shader. Never crop a capture past the frame edge at those samples.
- A Pango `Text()` may drop single spaces on this Mac; look at every still. Draw arrows as shapes. Manim: no `ease_in_quad`/`ease_out_cubic`, no `.animate(path_arc=...)`, no `MoveAlongPath` plus `.animate` on one object in one `play`; stay inside ±6.2 × ±3.3; type at least 32 (act titles 40); each scene must add a non-text, non-Rectangle shape after its first frame; the 45 to 55 % frame is a settled still with its labels.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome's own headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's. Check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input (C40) and say the renderer.
- A tween on a uniform needs the uniform set from code first (the on-screen code sets `wind` first); do not "simplify" it.
- `R/_gen_lanes.py` wrote `lanes/act1.json` to `act5.json` and `SHOTLIST.md` (cue times come from word positions in the narration). **Do not re-run it once the build has started**: it would put the placeholder ring box back on the B02 lane. After you measure that box (Phase 1), edit `lanes/act1.json` by hand; if a changed narration line moves a cue, shift that cue's `at` fraction by hand too, then run `make_sheet.py`.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example a mispronounced word), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond what Phase 0 allows (the `ShaderLab` registration).
- Do not edit `R/lab-shaders/*`: they are the tested files the captures and the code cards show.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where (if it was not already), any slate, any mispronunciation, any capture that disagreed with its verified result, and any trim you chose for Gate V. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

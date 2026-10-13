# BUILD-PROMPT: Matrices and Fake 3D (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, eleven tested shader files and the evidence behind every number. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses the three shared shader-series pieces (the `ShaderLab` component, `shader_kit.py`, the capture harness): if an earlier film's build made them, use them; if not, you build them first (Phase 0).
**Found.** Layout is complete and lint-clean: 47 beats (41 body), about 10 minutes estimated at Liam's measured pace (exact figures in `SCRIPT.md`; the lint's ceiling estimate is 10.2). Nothing is voiced, recorded, rendered or published. Every Godot result is a Lab capture of a tested file; every Manim number is in `FACTCHECK.md`. Needs a human: three small things for Bear, listed at the end of `ACTS.md` (the source's creator, the playlist name, how the voice says tau and the title). Nothing is OPEN in the fact-check; the docs screenshot (D1) should match the sentence quoted from the docs.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-matrices-and-fake-3d`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`.
5. A finished sibling for the Manim scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating"). If another shader film's folder already has a built `scenes.py`, reuse its `shader_kit` and capture harness rather than writing new ones.

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-matrices-and-fake-3d
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-matrices-and-fake-3d/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-matrices-and-fake-3d/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (build only what is missing)

Check: `./brutalist.art/art scenes --check ShaderLab`; `ls $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh`. For anything missing, build it from `S/COMPONENT-SPECS.md` (the only toolkit edit allowed is `ShaderLab` plus its registration and `./brutalist.art/art scene-index`; say so in `R/BUILD-LOG.md`).

The capture harness of the spec already has `--animate` schedules, `--scene`, `--material-at`, stills and fractions of the clip with `--length`. This film needs, on top, listed in `R/CAPTURE-PLAN.md` ("What the harness needs for this film"):

1. a **card scene script** (`--scene`), built from `R/evidence/planning-checks/runner-card.gd` (`make_image("card", n)`): the **`card` texture** drawn at 1024 px; the **unit factor U = 8** (pixel-valued uniforms set multiplied by 8 while the node is scaled by k / 8; the `lab-shaders/` files are never edited); the **origin cross** and the terracotta **hinge dot** markers; and its two-panel variant for C06;
2. **eased breakpoints** for every moving segment (a smoothstep sampled every 1/30 s between the listed points, written by a few lines of Python or done in the scene script);
3. **`--material-at`** (C02) and a **4K still PNG** (C11), both in the spec.

Readouts that share a position replace one another (the earlier fades as the later lands); readouts at different positions stay on screen. A cue `label` is rendered on the highlighted line (at most 60 characters); several beats use it to define a word on the line that uses it.

`ShaderLab` is used four ways here: `side` (code left, render right), `stack` (render above, code below: B22), `video` (render only), and `code` (code only, with free line cues that may climb upwards: B37). Its `caption` prop doubles as a one-line definition under the window (B11, B13, B35).

Film-local Manim helpers (write them in `R/scenes.py`, next to the scenes; specs in `R/SHOTLIST.md`, "Must exist before the build"): `screen_plane` (a grid with **x to the right and y DOWN**; convert a table with y flipped: M' = F M F, F = diag(1, -1)), `matrix_table` (bracketed grid, one `Text` per entry, rings are terracotta `RoundedRectangle` outlines), `card`, `top_view`. Use the true minus sign (U+2212) in tables.

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01 to C15 into `TK/runtime/remotion/public/godot-shaders/` with the names the lanes use (all start `matrices-`). Compare each against its "verified result to reproduce" column (the planning stills in `R/evidence/planning-checks/png/` show what each pose should look like); if a measurement disagrees, stop and report (do not edit a shader).
- D1, the docs screenshot, with Playwright. Then set the `moves` focus and `ring` of B05 by editing the B05 entry in `R/_gen_lanes.py` (the lanes are generated from it) and re-running `python3 $R/_gen_lanes.py && python3 $R/make_sheet.py`; do it before the audio exists or while the narration is unchanged, and log it. Confirm the quoted sentence and its section (`FACTCHECK.md`, the B05 row). Change B05's narration only if the page differs, and log it.
- Sanity: `python3 $R/evidence/planning-checks/geometry_checks.py` re-runs every planning measurement (all PASS expected, about a minute).

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_RowsTimesPoint`, `B04_VecTwoIsAColumn`, ... there are 22), implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with the helpers above and `shader_kit` objects. Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6): the 45 to 55 % frame is a settled still with its labels; no cue starts inside it; draw arrows as shapes (the `->` glyph is under the type floor); no fill behind text; type at least 32 (act titles 40); stay inside +-6.2 by +-3.3.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render (matrix numbers: check every entry against `FACTCHECK.md` and `R/evidence/planning-checks/geometry-summary.txt`). Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

After the audio is measured and before the review cut, compare every capture's length with its beat; re-record any capture that is off by more than 10 % (`CAPTURE-PLAN.md`, "Length").

Voice check: transcribe with faster-whisper and compare with `narration.py`. Listen for **tau**, "vec two", "mat two", "mat three", cosine, sine, radians, the letters x, y and z, pivot, the title read as "Matrices and Fake three D" (in the opening beat and in the outro), and the numbers. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation (tau is the likeliest) to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and this film's own)

- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text. The hinge dot is a small terracotta dot (allowed by the palette); if GATE T flags it, use the deeper `#A64A24` that `BrowserCapture` uses, never an ink ring.
- Real captures fail GATE T at the 50 % frame if they hold dark areas. This film's captures are light on purpose (cream card, teal, warm grey stage); the teal swatch of B03 is flat mid-tone. Never crop a capture past the window at the 50 % and 85 % frames.
- A Pango `Text()` can drop single spaces on this Mac: look at every table and label still (numbers like "1 x 5 + 3 x 6"). Draw the multiplication and equals signs as shapes if text drops them.
- **Matrix pictures: y points DOWN** in every grid, and the first column is the left one. A table drawn row-wise from code (`mat2(vec2(1, 2), vec2(3, 4))`) shows 1 3 on top, 2 4 below.
- The film's title is **"Matrices and Fake 3D"** on every screen; the voice reads `SPOKEN_TITLE`, "Matrices and Fake Three D", in the opening beat and the outro (`narration.py`). Do not change either.
- `LectureCodeTrace` moves its focus only downwards; B37 therefore uses `ShaderLab` in its `code` layout, whose cues may jump anywhere. B40 reads top to bottom and uses `LectureCodeTrace` with the cues in the lane.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted sweeps.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (only B05 is allowed to, and only if the real docs page differs), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not edit any `lab-shaders/` file, any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab` (and the harness files under `S/lab/`, `S/shader_kit.py`).

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation (say how tau sounded), any capture that disagreed with its verified result, whether D1 matched the quoted sentence, and anything that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

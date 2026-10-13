# BUILD-PROMPT: UV Space (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan and tested shader files. What is left is building, recording and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses three shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) that the first shader film's build creates; if they do not exist yet, build them first (Phase 0).
**Found.** Layout is complete and lint-clean: 42 body beats (48 with the bookends), 1,804 words (1,512 in the body), about 10.3 minutes estimated at Liam's measured pace. Lanes: ShaderLab capture 19, Manim 17, Remotion 6 (code traces, tables, one docs capture). No editor frames and nothing for Bear to record. Nothing is voiced, recorded, rendered or published yet.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-uv-space`
`S` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art` (relative to `books/`)

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; films are never numbered) and `TK/skills/make/nopunt/SKILL.md`.
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating") and, for how the shared shader pieces were built, `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/BUILD-PROMPT.md`.

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-uv-space
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-uv-space/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-uv-space/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (skip any that already exist)

Check first: `./brutalist.art/art scenes --check ShaderLab` (must say RENDERABLE), `ls $S/shader_kit.py`, `ls $S/lab/capture.gd $S/lab/capture_shader.sh`. Build whatever is missing from `S/COMPONENT-SPECS.md` (ShaderLab in `TK/runtime/remotion/src/scenes/`, registered, then `./brutalist.art/art scene-index`; the only toolkit edit allowed). This film needs from them: ShaderLab layouts `side` and `video`, a **PNG** as `video` (C02 only), cue `label`s (at most 60 characters; they carry the GLOSSARY wording for TEXTURE, COLOR and length), `readouts`, `rings`, `title`, and `caption` as one static line under the result window (at most 80 characters; it carries the GLOSSARY definitions of fragment on B06, TIME on B17 and alpha on B40, and 'same picture, same file' on B01); the harness with `--animate name:t0:v0,t1:v1,...` schedules, `--set-at` (C14's one-frame step), `--material-at` (C03, C07 and C13), `--tex`, `--sprite-tex`, `--size`, `--length`. `CAPTURE-PLAN.md` shows how each schedule becomes harness options.

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01 to C19 into `TK/runtime/remotion/public/uv-space/` with the names the lanes use (`c01-hook.mp4`, `c02-address-map.png` (the only still), `c03-lookup.mp4`, ...). Schedules are fractions of each beat's measured length `L`, so run Kokoro first (Phase 3, audio step) or scale from the estimates and re-render after. C15 and C16 use a **640 by 360 logical canvas** so their pixel readouts are true. Compare each result against the "verified result to reproduce" column; if a probe disagrees, stop and report (do not edit the shader).
- D1: the docs screenshot with Playwright (`CAPTURE-PLAN.md`); then set the two ring boxes in B16's `moves` from the real image.
- There are **no editor frames** and nothing for Bear to record.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/` (`B02_AddressSquare`, `B03_AnySize`, `B05_Lookup`, `B07_Window`, `B10_WorkedNumbers`, `B11_Reversal`, `B14_WhySmaller`, `B20_Pivot`, `B22_Centered`, `B26_Fold`, `B29_AddressCell`, `B30_OvalMeasured`, `B31_SquareCells`, `B32_CellToSquare`, `B37_EdgeSmear`, `B38_StepFunction`, `B39_Gate`), implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects plus two scene-local drawings (a labelled ruler with ticks, brackets and a marker; a window outline sliding over a picture card with a clipped copy beside it). Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6): at the 45 to 55 % frame every scene is a settled still holding the labels that matter. Labels are one to three words; a definition (GLOSSARY wording) may be a full line. Draw ticks, brackets and grids in greys, never ink, so GATE T does not read them as text.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.** If you change `lanes/` run `python3 $R/_gen_lanes.py` first.
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at it before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`; listen for the title in BOPEN and BOUT (the voice reads `SPOKEN_TITLE`, "U V Space"; the card and the outro props keep "UV Space"; FACTCHECK row 67), "U V", "fragment", "texture", "uniform", "alpha", "absolute value", "step". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- Ink-coloured rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text and never a thin stroke on its own.
- The address map (C02) has a navy top-left corner on purpose (blue is held at half; with blue 0 the corner is black). Check C02 at the 50 % and 85 % marks. All other captures are teal, cream and white on a light grey stage and keep a mid-tone floor.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes (no `->` glyph). No fill behind text.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted values. Do not sweep `flip` through zero (C14): it is one step (`--set-at`). C03 is a before-and-after: no material, then the lookup shader, and the picture must not change.
- The Lab is a shared project; run it only through `S/lab/check_shader.sh` (it locks). The scratch checks live in `R/evidence/planning-checks/` (`run-scratch-checks.sh`).

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab` (and only if Phase 0 needs it).

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation (the spoken title first), any capture that disagreed with its verified result, and what the docs screenshot D1 showed. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

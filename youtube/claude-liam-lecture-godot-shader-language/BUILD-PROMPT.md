# BUILD-PROMPT: Godot Shader Language (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, the tested shader files, and the engine's own error logs that the terminal cards quote. What is left is building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. Nothing is voiced, recorded, rendered or published yet.
**Found.** Layout complete and lint-clean: 47 beats (41 body), 1,910 spoken words, about 10.9 minutes by the lint's cautious estimate (the real figure is known after the voice). The shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) are built by the first shader film's build; if they do not exist yet, build them first (Phase 0). Two new helpers are needed here (`lab_window`, a type-tag helper). Open items that need a human: none. Playlist name: none yet.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shader-language`
`S` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4 and 6), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shader-language
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shader-language/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shader-language/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (skip any that already exist; check first)

```bash
./brutalist.art/art scenes --check ShaderLab        # must say RENDERABLE
ls $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh
```

If any is missing, build it from `S/COMPONENT-SPECS.md` exactly as written there (the first shader film's `BUILD-PROMPT.md` has the full instructions): `ShaderLab` (Remotion; the one toolkit file you may add, plus its registration, then `./brutalist.art/art scene-index`), `S/shader_kit.py` (Manim helpers), the capture harness. This film uses these `ShaderLab` features: layouts `side` and `code`, cue `label` (shown as a chip, at most 60 characters), `readouts`, `caption` (one line, at most 80 characters), a PNG or an MP4 as the result.

Two helpers belong to this film (put them in `R/scenes.py` or add them to `S/shader_kit.py` and say so in `BUILD-LOG.md`):
- **`lab_window(png, width, caption)`**: an outlined frame holding a real Lab PNG with a one-line caption. Used by B07, B08, B29 and B32.
- **A type-tag helper**: a small outlined tag placed under a span of a code line with a drawn bracket (B19, B35 to B39).

## Phase 1: record (CAPTURE-PLAN.md)

- Render C01a, C01b and C02 to C10 into `TK/runtime/remotion/public/godot-shader-language/` with the names in `R/CAPTURE-PLAN.md`. Compare each against its "verified result to reproduce"; if a probe disagrees, stop and report (do not edit the shader).
- **Do not forget `--set tint=#5FA391` for C01a and C01b**, and choose each clip's `--time-origin` from ITS beat's measured audio as the capture plan says (the pale-gray phase fails Gate V on the cream stage; one origin cannot serve B01 and B40).
- **Even widths only**: C10 must be exactly 1920 × 1080 (an odd width can light one column of the "equals" picture and ruin B32).
- D1 and D2: the documentation screenshots with Playwright.
- The terminal cards need no capture: their lines are already in `R/lanes/` word for word from `R/evidence/planning-checks/logs/`. If you change a line, change it from the log, never from memory.

## Phase 2: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `R/lanes/` — `B03_Header`, `B04_Globals`, `B07_ThreeSpellings`, `B08_CommentOut`, `B09_NamesMustMatch`, `B10_ThreeTypes`, `B12_Bundles`, `B13_BuildAVector`, `B14_AllAtOnce`, `B16_Swizzle`, `B19_TypeChain`, `B20_Signature`, `B21_CallAndReturn`, `B23_TheWall`, `B25_InOutInout`, `B29_Collapse`, `B32_NoPixelLands`, `B35_ReadUniforms`, `B36_ReadSignature`, `B37_ReadWave`, `B38_ReadReturn`, `B39_ReadFragment` — implementing each `visual_intent`, `motion_claim` and `show` cue from `R/SHOTLIST.md` and `R/lanes/act*.json`, with `shader_kit` objects. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). Assemble `scenes.py` the way the sibling's `assemble_scenes.py` does (the kit pasted above the scenes; Gate A reads only that one file).
   **Measured widths (Manim 0.20.1, Menlo, no rendering):** at font size 32 a code character is about 0.25 unit wide and a code line about 0.6 unit tall; the usable width is 12.4 units, so at most about 49 characters per line (the squeezed line of B07 is 48 and fills the width; B39's widest line is 45) and about 8 lines per card. At size 36 the limit is about 41 characters (B35 to B38 fit: the widest is 34). Do not shrink below 32 to make something fit: wrap it or drop a line and say so in `BUILD-LOG.md`.
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare to `narration.py`. Listen for: "G L S L" (B09), "U V", "R G B A", "S T P Q", "swizzling", "vec two/three/four", "sampler two D", "bool", "int", "const", "varying", "ternary", "in out" (B25), "G L frag color" (B09), "float of i" (B30), "pi" (said "pie"). Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`, no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met

- **BHTF**: the narration reads the prompt and then the two checks aloud while `props.command` holds only the prompt. That is settled by the shipped precedent; do not "fix" it.
- **GATE T and the terminal cards.** `CCPlainShell` draws a dark window; dark UI can read as a text blob. The dark window lands before 50 % in these beats, so expect trouble; the fallback is the cream `ClaudeCodeBeat` card with the same lines (written in each lane's `why`). Ink rings fail the overlap rule: ring with gray. Terracotta is never text.
- **Gate V and C01.** The pulse passes through a pale gray on the cream stage; place the 50 % and 85 % frames on the teal side (`--time-origin`).
- **Real captures with dark regions.** The only dark corner is the top-left of the saturated picture in B08 (it appears after 50 % of that beat); keep it framed in its window.
- A Pango `Text()` may drop single spaces on this Mac (double the space at the fused boundary and LOOK); draw arrows as shapes; the `->` glyph is under the type floor.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Say "Forward+" next to any pixel value.
- Lab batches are slow when other sessions hold the lock; run `check_shader.sh` once per shader.
- zsh: never name a shell variable `path`.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change, change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, and anything that needed Bear. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

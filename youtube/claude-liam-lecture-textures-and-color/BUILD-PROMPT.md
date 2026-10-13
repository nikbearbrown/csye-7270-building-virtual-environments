# BUILD-PROMPT: Textures and Color (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, and 28 tested shader files. What is left is recording, building and rendering.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film's subject is color, so one habit matters more than any command: **every pixel value on screen is quoted with its renderer**, and a capture that disagrees with the value verified here is a stop, not a fix.
**Found.** Layout is complete and lint-clean: 47 beats (41 body), about 1,918 words, about 10.9 minutes by the lint's ceiling estimate (the real length is known only after the voice). Nothing is voiced, rendered or published yet, and no Godot render is recorded, but the three editor captures are already recorded by script (2026-10-13) and the three formerly OPEN fact-check rows are closed from them (the editor frames corrected two labels: the resource menu is a heading New over bare class names, and a project's renderer is chosen in Project Settings, not by a name in the editor's corner). Open items that need a human: the playlist name (none yet) and the creator credit for the third-party source (none named).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-textures-and-color`
`S` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `brutalist.art`
`P` = `$R/evidence/planning-checks` (every planning run, script and log)

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md` (the shared pieces and the harness options), `S/GLOSSARY.md`.
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md` (every capture, with the value to reproduce), `R/FACTCHECK.md`, `R/ACTS.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the Manim kit and the scene scaffolding: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, `BUILD-LOG.md` "Mistakes worth not repeating").

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-textures-and-color
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-textures-and-color/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-textures-and-color/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (they may already exist)

`ShaderLab` (Remotion), `shader_kit.py` (Manim) and the capture harness (`S/lab/capture.gd` + `capture_shader.sh`) are shared by every shader film and are built once, by whichever shader film is built first (spec: `S/COMPONENT-SPECS.md`). Check first: `./brutalist.art/art scenes --check ShaderLab`, `ls $S/shader_kit.py $S/lab/capture.gd`. If they exist, use them. If not, build them from the spec (the only toolkit edit allowed is `ShaderLab` plus its registration; say so in `R/BUILD-LOG.md`), then add **this film's harness additions** (CAPTURE-PLAN section H): the extra texture kinds, `--rect-color`, `--modulate`, `--hdr2d`, square windows, panel composites and the three small scene scripts. A reference implementation is verified: `$P/runner_plus.gd` (still frames), `$P/plus.sh`, `$P/verify-patches.gd`, `$P/verify-tween-progress.gd`.

## Phase 1: voice first (the captures are timed from the audio)

Sweeps, switch-ons and panel reveals are **fractions of each beat's measured audio**, so measure the audio before you record.

```bash
python3 $R/make_sheet.py          # only if narration.py changed; NEVER after `art final`
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock
```

Voice check: transcribe with faster-whisper and compare with `narration.py`. Listen for: "U V", "s R G B", "H D R two D", "sampler two D", "vec four", "Fast Noise Lite", "Noise Texture two D", "G L compatibility", "tween", "Forward Plus", "Compatibility", "Mobile", "three-D", "two-D", the decimals ("point six"), "dot", "step". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Phase 2: record (CAPTURE-PLAN.md)

- Render C01 to C26 into `TK/runtime/remotion/public/godot-textures-and-color/` with the names the lanes use, each with `--length` set to its beat's audio. Compare each against the "verified result to reproduce" column; if a probe disagrees, **stop and report** (do not edit a shader).
- S1 and S2 (two Lab stills for beat B22) and D1 (the docs screenshot, Playwright).
- Editor frames E1 to E3 are **already recorded by script** (CAPTURE-PLAN section E); nobody clicks or records by hand. Copy them from `S/editor-capture/png/1920x1080/textures-and-color/` (B18: five frames; B34: one frame, cropped) and, for B40, from `S/editor-capture/png/1920x1080/renderer-path/` (the three Project Settings frames R1-C, R1-D, R1-E) into `TK/runtime/remotion/public/godot-textures-and-color/` as `editor-noise.mp4`, `editor-picker.png` and `editor-renderer.mp4`, exactly as each lane's `capture_spec` says (ffmpeg cross-dissolves at the stated fractions of the beat's measured audio; the native 3456x1944 twins are beside the 1920x1080 frames if a sharper source is wanted). Label every such clip "scripted editor session". If a gate asks for a different crop, recompute the lane's ring boxes from the new crop. Only if a state is missing, write a state script by copying `S/editor-capture/state-scripts/final/tc-E1.json` and run it as `S/editor-capture/README.md` section 7 says.
- The formerly OPEN rows 52, 94 and 107 and the docs-versus-run row 106 are already closed from these frames (`R/FACTCHECK.md`). If a frame you record differs from what the row quotes, stop and report; change a narration line only if the real label differs, and log it.

## Phase 3: scenes and sheet

1. Write `R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/`: `B02_LookupTable`, `B08_FourNumbers`, `B21_Band`, `B22_RampLookup` (uses stills S1 and S2), `B28_Probe`, `B29_TwoScales`, `B30_TwoMidpoints`; implement each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json`, with `shader_kit` objects. Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`S/BUILDER-BRIEF-COMMON.md` section 6). The curve in B29 and B30 is the real sRGB decode: `((c + 0.055) / 1.055) ** 2.4` above 0.04045, else `c / 12.92` (checked against Godot's `srgb_to_linear` in `$P/run-8-luminance-and-curve.log`: 0.2 to 0.0331, 0.5 to 0.214, 0.8 to 0.6038).
2. `python3 $R/make_sheet.py` (only if the narration changed). **Never re-run it after `art final`.** The lane files (`lanes/act1.json` to `act5.json`) and `SHOTLIST.md` were written by `$R/_gen_lanes.py`, which holds the tested code lines, the cue labels (each at most 60 characters, none inside 45 to 55 % of a beat) and the verified numbers in one place. To change a lane, edit `_gen_lanes.py` and run `python3 $R/_gen_lanes.py && python3 $R/make_sheet.py`; or edit the JSON by hand and then never run the generator again. Do not mix the two.
3. Stills first: a last-frame still of every Manim class and 25/50/95 % stills of every Remotion and ShaderLab beat; make a contact sheet; LOOK at them before any 4K render. Write down what you see in `R/BUILD-LOG.md`.

## Phase 4: title card, render, gates

```bash
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps for this film (the first four are the likely ones)

- **GATE T and dark pixels.** The 0.2 gray end of the strips in B27 is within 48 RGB of ink; the strips are tall, so the shape filters should skip them, but check the 50 % and 85 % frames. The grey noise appears in B04's third still (after the 50 % mark, by design) and in the real editor frames of B18, B34 and B40 (dark editor UI): look at their 50 % and 85 % frames, and if GATE T flags one, crop to the Inspector (the `.dock.png` crops hold the whole right dock) and recompute that lane's ring boxes. If the gradient (B04's second still, the 50 % frame) fails on its black corner, swap that still for the `swatches` picture and log it.
- **GATE T and the accent color.** No terracotta text, ever; the burn ramp's middle stop is `#F08A2C` (not `#E8742F`) so the rim stays out of the accent tolerance, and the swatch patch is a rose, not a coral, for the same reason. Rings are terracotta over a grey backing.
- **Gate V.** B12's white card on the pale stage and B01's last frame (the sprite almost gone): sweeps are set to end at 97 % of the beat so the 85 % frame still has content; if a frame is flagged underfill, say why it is sparse in the beat's `qc` rather than changing the capture.
- **A pixel value without its renderer is a defect.** The `videoLabel` of every capture that shows a number names the renderer (and HDR 2D when it is on); the tables carry the machine and the engine version.
- zsh: shell variables holding several words must be arrays (`"${ARR[@]}"`), never a quoted string or an unquoted variable; never name a variable `path`.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free. The Lab's lock is shared with other sessions (`/private/tmp/claude-501/shaderlab.lock`): batch renders, one `check_shader.sh` per shader, never a loop that retakes the lock per frame.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input and scripted sweeps.
- BHTF: `narration_text` reads the prompt and then the two checks; `props.command` holds only the prompt. That is settled for this series; do not "fix" it.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example an editor label), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not edit any shader in `R/lab-shaders/`, any other film's folder, any game or course repository, the shared series files, or the toolkit beyond `ShaderLab`.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 (or that it already existed) and where, any slate, any mispronunciation, any capture that disagreed with its verified value, which editor frames were used (all should be the driver's real frames) and any crop you had to change, and that no fact-check row is OPEN. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

# BUILD-PROMPT: Reflections (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort session did the thinking: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, the capture plan, five tested shader files, a tested scene library for all nineteen Godot captures, a capture tool that records them at the length of their beats, and a scripted recording route for the two editor frames. What is left is recording, scene code, voice and render.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film reuses the shared pieces the first shader film builds (`ShaderLab`, `shader_kit.py`) and adds only a few drawing objects and its own capture scenes.
**Found.** Layout is complete and lint-clean (no errors, no warnings): 43 beats (37 body beats), 1557 words, about 8.9 minutes. Nothing is voiced, recorded for the film, rendered or published. Nothing needs Bear's hands. One decision is open for Bear, and it does not block the build: the name of the source course's creator, if he wants a credit in the description (`SOURCES.md`). Two things changed during the layout and are easy to get wrong: the painted layer is called a **label map**, never a "mask" (`ACTS.md`, "Naming"); and **C08 is recorded 1:1**, not on the 4K route (`CAPTURE-PLAN.md`).

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`. Every command below is written for that folder and uses absolute paths; each code block defines its own variables, so it also works when the shell forgets them between calls.

- `R` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections`
- `S` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
- `E` = `$R/evidence/planning-checks`
- `TK` = `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art` (the toolkit; `./brutalist.art/art` is its entry point)

## Read first (in order)

1. `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/skills/make/lecture/SKILL.md` (the governing skill; videos are never numbered).
2. `/Users/bear/Documents/CoWork/bear-textbooks/books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths in every report, the two-stage rule).
3. `$S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `$S/COMPONENT-SPECS.md` (what to build first, the capture harness), `$S/GLOSSARY.md` (the locked wording).
4. `$R/SCRIPT.md` (the film as Bear will read it), `$R/SHOTLIST.md`, `$R/CAPTURE-PLAN.md` (routes, lengths, verified results), `$R/FACTCHECK.md`, `$R/ACTS.md`, `$R/CHECKS-REPORT.md`, `$E/RESULTS.md` (every planning run).
5. A finished sibling for the Manim kit and the scene scaffolding: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot/` (`kit.py`, `assemble_scenes.py`, `preflight.sh`, `still_remotion.py`, and `BUILD-LOG.md`, "Mistakes worth not repeating").


## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections
```

Then read each beat's measured `actual_duration_s` from `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
<!-- /HOW-TO-RUN -->

## Phase 0: the shared pieces (they should already exist)

Check first. If either line fails, build it from `$S/COMPONENT-SPECS.md` (the first shader film's build owns the shared pieces; never build a second copy if one exists).

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
./brutalist.art/art scenes --check ShaderLab
ls /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/shader_kit.py
```

This film adds a few **drawing objects**, in `shader_kit.py` if the shared kit exists and else at the top of `$R/scenes.py`: the pond picture (flat grass band, water, a sand spit, the teal blob and its flipped reflection); a stack of three isometric slabs (label map, art, character) with a top-down thumbnail and a copy frame; a node chip; isometric transparent sheets (canvas layers); the 0 to 1 ramp strip zoomed so its k over 255 ticks show; a colour plane with two circles of radius 0.1. Terracotta only as dots, rings and sparks, never as text.

## Phase 1: record (CAPTURE-PLAN.md)

**Godot captures: nineteen clips, one scene library, one command.** Each clip is recorded at the length of the beat that uses it (the measured audio once the voice exists), in its own fresh Godot process; every scripted event keeps its place as a fraction of the clip. Eighteen use the 4K route; **C08 uses the 1:1 route and is enlarged 3x by whole pixels** (a Rect-mode box counts render pixels; reasons and runs in `CAPTURE-PLAN.md`, "Which route each capture uses"). The tool picks the route itself.

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections
OUT=/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/reflections
$R/evidence/planning-checks/capture_all.sh $OUT --dry-run        # the plan: capture, file, beat, seconds, measured or estimate
$R/evidence/planning-checks/capture_all.sh $OUT                  # records all nineteen (10 to 15 minutes; 13 measured on a busy machine); one clip: --only C07
python3 $R/evidence/planning-checks/verify_recorded_clips.py $OUT   # size, rate and frame count of every clip
python3 $R/evidence/planning-checks/capture_contact_sheet.py $OUT /private/tmp/reflections-captures-sheet.png   # then LOOK at it
```

The files, in capture order:

   - `C01` → `hook-walk.mp4` (beat B01)
   - `C02` → `label-map-only.mp4` (beat B03)
   - `C03` → `label-map-over-art.mp4` (beat B05)
   - `C04` → `three-sprites-window.mp4` (beat B10)
   - `C05` → `copy-moves-1.mp4` (beat B12)
   - `C06` → `copy-moves-2.mp4` (beat B13)
   - `C07` → `two-readers.mp4` (beat B14)
   - `C08` → `rect-trap.mp4` (beat B17)
   - `C09` → `flip-and-place.mp4` (beat B19)
   - `C10` → `copy-in-the-sand.mp4` (beat B21)
   - `C11` → `reflection-walk.mp4` (beat B23)
   - `C12` → `label-map-toggle.mp4` (beat B24)
   - `C13` → `wrong-orders.mp4` (beat B25)
   - `C14` → `see-through-art.mp4` (beat B26)
   - `C15` → `equals-half-red.mp4` (beat B28)
   - `C16` → `distance-half-red.mp4` (beat B29)
   - `C17` → `coast-alpha.mp4` (beat B34)
   - `C18` → `tint-toggle.mp4` (beat B35)
   - `C19` → `jump.mp4` (beat B37)

Every clip must read `measured` in the plan (voice first: the HOW TO RUN section above). The frames of each clip stay in `${TMPDIR:-/private/tmp}/reflections-capture-frames/` (outside the Remotion public folder on purpose; the scratch Godot project is `${TMPDIR:-/private/tmp}/reflections-capture-project`) until you delete them. LOOK at the contact sheet and compare it with the last column of the capture table in `CAPTURE-PLAN.md` and with `$E/png/contact-sheet-captures.png` and `$E/png/contact-sheet-recorded-clips.png` (the same two marks from the planning runs and from a full trial recording, run-17). If a capture disagrees with its verified result, stop and report: do not edit a shader. A `retime_warning` line means the beat is more than 1.4 or less than 0.7 times the scene's planned length: look at that clip for slow motion or a rush.

**Editor frames E1 and E2** are recorded from Godot's own editor by this film's scripts (Light preset and a 2x UI through a scratch HOME, a scratch plugin that selects the node; nothing of Bear's is touched). They supersede the shared-driver sentence in the HOW TO RUN section: this film's route is already proven (`$E/png/planning-frame-E1-scene-dock.png` and `...E2-inspector-copy-mode.png` are trial crops, run-12 checks the project).

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections
E=$R/evidence/planning-checks
SCR=/private/tmp/reflections-editor-scratch
$E/make-editor-project.sh $SCR/pond
$E/record-editor-frames.sh $SCR/pond Pond $SCR/e1 70
$E/record-editor-frames.sh $SCR/pond BackBufferCopy $SCR/e2 70
python3 - <<'EOF'
from PIL import Image
pub = "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/reflections"
e1 = Image.open("/private/tmp/reflections-editor-scratch/e1/f00000069.png").convert("RGB")
e2 = Image.open("/private/tmp/reflections-editor-scratch/e2/f00000069.png").convert("RGB")
e1.crop((0, 60, 440, 420)).save(pub + "/editor-scene-dock.png")
e2.crop((2140, 60, 2560, 420)).save(pub + "/editor-inspector-copy-mode.png")
EOF
```

LOOK at both crops: the Scene dock lists `LabelMap`, `BackBufferCopy`, `Ground`, `Player` (with `RemoteTransform2D` under it) and `Reflection` top to bottom; the Inspector shows `Copy Mode` = `Viewport`. If a label differs from the narration (B09, B18), change only that line, re-voice that beat and log it.

**Docs screenshots D1 and D2** with Playwright, 1600 x 900 at device scale 2.4, URLs and anchors in `CAPTURE-PLAN.md`, saved as `docs-backbuffercopy.png` and `docs-shading-language-compare.png` in the same public folder. The ring boxes in `lanes/act2.json` (B16) and `lanes/act4.json` (B27) are placeholders: measure them on the real captures and change only those numbers, **directly in the lanes files** (never re-run `_gen_lanes.py` once the build has started: it would overwrite them), then re-run `make_sheet.py` (Phase 2, step 2). Also measure the ring boxes of B09 and B18 on the real E1 and E2 crops if they moved.

## Phase 2: scenes and sheet

1. Write `$R/scenes.py` (Manim): one class per Manim beat, named exactly as in `lanes/`, implementing each `visual_intent`, `motion_claim` and `show` cue from `SHOTLIST.md` and `lanes/act*.json` with `shader_kit` objects. The twelve classes:
   - `B02` · `B02_PixelAsks`
   - `B04` · `B04_LinedUp`
   - `B06` · `B06_Layers`
   - `B07` · `B07_CopyMoment`
   - `B08` · `B08_CopyNode`
   - `B11` · `B11_FirstReader`
   - `B15` · `B15_CanvasSheets`
   - `B20` · `B20_FollowsAlong`
   - `B22` · `B22_SameAddress`
   - `B30` · `B30_EightBits`
   - `B32` · `B32_ColorDistance`
   - `B36` · `B36_NoScenery`
   Assemble with the sibling's `assemble_scenes.py` pattern. Obey the Manim laws and the midpoint rule (`$S/BUILDER-BRIEF-COMMON.md`, section 6). B30 and B32 show measured numbers: keep the machine and renderer credit the lanes name. The word on screen is **label map** (and "the map"), never "mask".
2. `python3 $R/make_sheet.py` (rewrites `beat_sheet.json` and `SCRIPT.md`, keeps measured audio while the narration is unchanged). **Never re-run it after `art final`.**
3. Stills first: a last-frame still of every Manim class and 25, 50 and 95 % stills of every Remotion beat; make a contact sheet; LOOK at them before any 4K render. Write what you see in `BUILD-LOG.md`.

## Phase 3: voice, title card, render

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R              # free; measured durations become the clock (skip if the HOW TO RUN step already did it)
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
./brutalist.art/art run   $R --height 2160                                       # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape            # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Voice check: transcribe with faster-whisper and compare with `narration.py`; listen for "Back Buffer Copy", "Remote Transform two D", "screen U V", "H D R two D", "Forward Plus", "Compatibility", "label map", "alpha" and "point five oh two". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.

## Gates that must PASS

Gate F (`FACTCHECK.md`: 71 rows, none OPEN), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `$R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order.

## Traps already met (and ones this film has)

- **A capture must run in a fresh Godot process** (C08 reads black only when the back buffer has no history: run-03 R4). The tool does it; a harness that reuses one process shows stale pixels instead.
- **Route.** The 4K SubViewport route is safe here only because the shaders read `SCREEN_UV`; a Rect-mode box counts render pixels (run-13), so C08 is recorded 1:1 and enlarged by whole pixels. If a shared harness replaces `capture_scene.sh`, keep C08 on the 1:1 route.
- **Audio first.** Record each clip at its beat's measured length (`capture_all.sh` reads it from `beat_sheet.json`); events are fractions of the clip, so the picture lands on the words.
- **GATE T and the black window (B17, C08).** The window is pure black at the 50 % mark (14 % of the capture). Pure black is not within 48 RGB of ink or mute, and the toolkit's own mask finds no text-like blob in any raw capture frame (run-16). If the real frame still fails, shrink the window (`make_window` in `$E/capture_scenes.gd` and the 0.375 factor in `$E/scene_runner.gd`) and re-record C08; the story does not change.
- **Polarity.** Red-filled frames (C02, C03, C13 at 85 %) flip GATE T's polarity detector to "dark" if a capture fills the frame edge to edge: keep the framed window and the cream margin.
- Editor frames use the Light preset on purpose (a dark UI fails GATE T); crop and zoom, never shrink the type.
- Ink-colored rings and any dark small shape beside mid-tones fail GATE T; ring with grey. Terracotta is never text.
- A Pango `Text()` may drop single spaces on this Mac; look at the still. Draw arrows as shapes; the `->` glyph is under the type floor.
- Renders: foreground, `--concurrency=1`, never hand-rolled `npx remotion render`. Chrome 157's headless shell crashes on this Mac; `remotion_scenes.py` prefers Playwright's.
- Disk: check `df -h /` before 4K; stop under about 15 GB free. Capture frame folders are small (about 30 KB a frame) but delete them after you have looked.
- zsh: never name a shell variable `path`. Never kill a process by `pkill -f` on a script name; kill by PID.
- Godot captures are offline at a fixed tick rate: never claim real-time frame rate. Label scripted input and the renderer (Forward+). Quote a pixel value only with its renderer (B30, B31 and B33 do; keep their notes).
- The code on screen is the shader files in `$R/lab-shaders/` (the lanes carry the same text). If a shader file changes, the lane's `code` must change with it and the file must pass `$S/lab/check_shader.sh`.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not change `narration.py` or the beat order. If a line must change (for example an Inspector label), change only that line, re-run `make_sheet.py`, re-voice that beat (`generate_audio_kokoro.py $R --only <BID>`), and log it.
- Do not touch any other film's folder, any game or course repository, or the toolkit beyond what the shared pieces need.

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was built in Phase 0 and where, any slate, any mispronunciation, any capture that disagreed with its verified result, and the ring boxes you measured. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

# BUILD-PROMPT: Making Water in Godot (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A higher-effort Cowork session did the thinking and the doing that needs judgment: the script (`SCRIPT.md`, `narration.py`), the beat sheet (`beat_sheet.json`, estimates only), the picture for every beat (`lanes/`, `SHOTLIST.md`), the fact-check, fourteen shader stages and experiments that were really run, the real Godot captures (`captures/`, recorded at estimated lengths), a scripted editor session, an openable Godot project, and nine Manim scenes that pass Gate A. What is left is voice, re-recording where the audio differs, rendering and the gates.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): Cowork lays the film out; Claude Code builds it. This film is one of the Godot shader series and reuses the three shared pieces (`ShaderLab`, `shader_kit.py`, the capture harness) that the pilot's build created; it adds nothing to them.
**Found.** Layout is complete and lint-clean: 55 beats (49 body), about 2,140 words, about 11 minutes estimated (the series' deliberately long figure is 12.1). Nothing is voiced, rendered or published yet. Nothing needs a human unless a gate fails for a reason that needs a script change, or a capture disagrees with its verified number.

Run everything from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
`R` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot`
`S` = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series`
`TK` = `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art`
`EV` = `$R/evidence/planning-checks`

(Commands below use these as written; from `books/` the relative forms `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot` and `brutalist.art` work too.)

## Read first (in order)

1. `TK/skills/make/lecture/SKILL.md` (governing skill; videos are never numbered).
2. `books/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths; the two-stage rule).
3. `S/BUILDER-BRIEF-COMMON.md` (its sections 4, 6 and 11), `S/COMPONENT-SPECS.md`, `S/GLOSSARY.md`, `S/MORNING-REPORT.md` (the traps of the overnight builds).
4. `R/SCRIPT.md` (the film as Bear will read it), `R/SHOTLIST.md`, `R/CAPTURE-PLAN.md`, `R/FACTCHECK.md`, `R/ACTS.md`, `R/EVIDENCE-INDEX.md`, `R/CHECKS-REPORT.md`.
5. A finished sibling for the build shape: `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders/BUILD-LOG.md` ("the 4K master + publish run" is the part to copy, minus publishing).

## HOW TO RUN THIS BUILD (read before any phase below; it overrides the phase order where they differ)

**Audio first.** The measured narration is the clock for everything else. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot
python3 csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/pad_bout.py        # BOUT's 1.0 s silent tail; run once, before art run
```

Then read each beat's measured `actual_duration_s` from `R/beat_sheet.json` and use it:

- **Captures:** `python3 $R/captures.py --stale` lists the clips whose recorded length differs from the beat's now-measured length by more than half a second; re-record those (`python3 $R/captures.py --only C.. C..`). Every scripted event inside a capture is a fraction of the clip length, so a re-recorded clip lands on its words. If you have the time, re-record all of them (about 40 minutes: the Lab lock is shared with other sessions; a wait is normal).
- **Manim scenes:** each is sized to the ESTIMATED duration; after the audio exists run the preflight again (Phase 3) and read the printed `[pace] ... content=.. target=..` lines: a scene whose content time exceeds the target is the only thing to fix (shorten its last wait, not its narration).
- **Voice check now, not at the end:** `python3 $S/voice_check.py $R` (faster-whisper) and LISTEN. Words to listen for: "Voronoi" (not in the pronunciation dictionary), "albedo", "fract", "smooth step", "Fast Noise Lite", "noise texture", "normal map", "hash", "cellular", "pow" (not said), "U V" (said as letters), "Forward Plus", "Compatibility", "four point seven point two", "Godot", "sine", "vertex", "uniform", "group uniforms", "Inspector", "quad". Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.

**Keep this build resumable.** Write `R/BUILD-LOG.md` as you go (it already holds the layout-stage notes: do not delete them) and after each phase append a line `PHASE <name> DONE <date>`. If a `PHASE` line is already there, resume at the first phase not marked DONE; never redo a finished phase. Log every mistake and its fix ("Mistakes worth not repeating").

**Free steps run straight through.** No approval gate before any free step (Kokoro, Godot captures, Manim, Remotion). There is no paid step in this film.

## What is already done (do not redo)

- `narration.py`, `lanes/act1..5.json`, `beat_sheet.json`, `SCRIPT.md`, `SHOTLIST.md`, `FACTCHECK.md` (131 rows, 0 OPEN), `CHECKS-REPORT.md`, `ACTS.md`, `SOURCES.md`, `EVIDENCE-INDEX.md`, `CAPTURE-PLAN.md`: regenerate nothing unless a line must change (then edit `narration.py` or `_gen_lanes.py`, run `python3 $R/_gen_lanes.py` and `python3 $R/make_sheet.py`, and re-voice only that beat with `generate_audio_kokoro.py $R --only <BID>`; never re-run `make_sheet.py` after `art final`).
- `lab-shaders/` (19 shader files, each compiled in both renderers except the deliberate error shader `06c-builtin-in-helper-error`: `$EV/logs/compile-check.txt`), `water-project/` (the Godot project the viewer can open; its `shaders/` are byte-identical copies: `$EV/logs/project-sha256.txt`), `capture-scenes/` (the harness scene library), `captures.py`, `captures/` (the recorded clips, stills and editor frames), `pantry/` (the real stills the Manim scenes use), `scenes_act1.py` to `scenes_act5.py` (nine Manim classes: B02, B08, B09, B14, B16, B26, B27, B40, B42), `still_remotion.py`, `pad_bout.py`.
- Evidence: `$EV/RESULTS.md` indexes every experiment (sixteen runs and four engine-fact scripts); `$EV/EDITOR-LABELS.md` holds every exact Inspector label from the scripted editor session.

## Phase 0: shared pieces (reuse; build nothing)

```bash
ls $TK/runtime/remotion/src/scenes/ShaderLab.tsx $S/shader_kit.py $S/lab/capture.gd $S/lab/capture_shader.sh $S/assemble_scenes.py $S/preflight.sh
./brutalist.art/art scenes --check ShaderLab ; ./brutalist.art/art scenes --check LectureEvidenceTable ; ./brutalist.art/art scenes --check CCPlainShell
```

All exist and are renderable. This film uses the ShaderLab layouts `side`, `stack` and `video`, and its cue `label` feature on about thirty beats (the overnight builds used it on none): before anything else render stills of B03, B04, B15, B21 and B47 (`python3 $R/still_remotion.py B03 B04 B15 B21 B47 --pcts 25 50 95`, then LOOK) to confirm the labels draw on the right lines and stay inside the card. If ShaderLab needs a fix, say so in `BUILD-LOG.md` and keep the change inside `ShaderLab.tsx`.

## Phase 1: voice (above) and the title card

```bash
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
```

(The standalone film has no playlist field: the card carries the title "Making Water in Godot" and the line "Build a water shader, one layer at a time".)

## Phase 2: captures (CAPTURE-PLAN.md)

1. `python3 $R/captures.py --stale` and re-record what it lists (or everything). Compare each against the "verified result to reproduce" column of `CAPTURE-PLAN.md`; if a probe or a picture disagrees, stop and report (do not edit a shader or the narration). Keep **C22 and C29 at 1280 x 720** (their lane captions quote pixel rows of a 1280 x 720 frame; `captures.py` pins that size).
2. **Ring boxes that must be read off a frame** (look, do not guess): B23's ring is set for the frozen frame (the 258-pixel speck at (221, 545) of the 1080 x 1080 frame = box [0.165, 0.465, 0.245, 0.545]); check it on `captures/power-specks.mp4` at 30 % and correct `rings` in `_gen_lanes.py` only if it misses. B24's ring [0.595, 0.37, 0.735, 0.57] was read off the smudged cross of the right half of `captures/foam-vs-texture.mp4` at 10.5 s; the cross scrolls with the texture, so after re-recording at the measured length look at the 72 % frame and move the ring if it misses. B31's pill is at (0.5, 0.676), the near edge. B38's pill is at (0.5, 0.74): adjust to the rolling near edge if it covers it. After any change: `python3 $R/_gen_lanes.py && python3 $R/make_sheet.py` (before `art run` only).
3. **Re-measure the near-edge spread on the re-recorded clips** after re-recording C22 and C29 (still 1280 x 720): `python3 $EV/scripts/edge_spread.py $R/captures/low-flat.mp4 $R/captures/low-waves.mp4 > $EV/logs/edge-spread.txt`. At the layout stage the flat clip stayed on row 487 or 488 (spread 0) and the wave clip ranged 40 to 96 rows (mean 78); B38 says "up to ninety-five". If the maximum of your clip is outside 85 to 105, tell Bear and do NOT edit the narration.
4. Look at every clip on a contact sheet: `python3 $S/vcontact.py $R/evidence/contact-sheets/<name>.png <clips> --n 5`. The ones from the layout stage are in `$R/evidence/contact-sheets/`.
5. Copy the captures where Remotion can reach them:

```bash
mkdir -p $TK/runtime/remotion/public/making-water
cp $R/captures/*.mp4 $R/captures/editor-inspector-dock.png $TK/runtime/remotion/public/making-water/
grep -oh 'making-water/[A-Za-z0-9_.-]*' $R/lanes/*.json | sort -u      # every file a lane asks for must exist in that folder
```

6. B48 shows the Inspector dock crop (`captures/editor-inspector-dock.png`, 1300 x 1849, a portrait window). The full frame is `captures/editor-inspector.png`; all 22 editor stills and their native twins are in `captures/editor/`. If the portrait window reads too small in the review cut, switch B48 to the full frame (change `video` and `aspect` in `_gen_lanes.py`: the full frame shows a scratch FileSystem dock; say "scripted editor session" in the label either way).

## Phase 3: scenes, sheet, stills

```bash
python3 $S/assemble_scenes.py $R                                   # writes $R/scenes.py from shader_kit.py + scenes_act1..5.py
$S/preflight.sh $R 1 B02_ThreeLinks B08_BlendArithmetic B09_TwoRenderers
$S/preflight.sh $R 2 B14_OnePointEach B16_NineSquares
$S/preflight.sh $R 3 B26_ColorIsDirection B27_Seamless
$S/preflight.sh $R 4 B40_OneClock
$S/preflight.sh $R 5 B42_DepthTexture
python3 $S/gate_t_regions.py $R                                    # qc.typography_regions and contrast_regions on every ShaderLab beat
python3 $R/still_remotion.py <every Remotion beat id> --pcts 25 50 95      # LOOK at all of them, then write what you saw in BUILD-LOG.md
```

(The preflight scratch is private, so the five can run in any order.) B45's terminal card has `lineCues` set for an estimated 14-second beat (the six result lines print by 44 % and a ring lands on the first failing line at 62 %): after the audio exists, scale them to the measured duration (cue frames at the beat's frame rate), keeping every line before 45 % and the ring after 55 %.

## Phase 4: render and final

```bash
./brutalist.art/art run   $R --height 2160                         # review cut: LOOK at frames and qc-sheet.png
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape   # GATE T, then the clean master
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

A long lecture renders act by act if needed; move superseded clips to `R/_superseded/` before re-rendering. Check the master: 3840 x 2160, runtime equals the sum of the audio (the one-second silent tail present), `bookend_check` PASS.

## Gates that must PASS

Gate F (`FACTCHECK.md`: no OPEN rows; `python3 $TK/runtime/qc/factcheck_check.py $R`), PROOF GATE (`CHECKS-REPORT.md`), Gate A (static scene check; run by preflight and `art run`), Gate B (layout audit), Gate V (frame check), GATE T (type), `bookend_check`. Fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`. If a gate fails for a reason that needs a script change, report it; do not change the narration or the beat order. The toolkit's plan-time gates (banned-card, beat-lint, lane-check) pass on the layout (`$R/evidence/gates/layout-stage-gates-2.txt`, re-run after the last narration edit).

## Traps already met (and ones this film adds)

- **ShaderLab underfill** (54 percent against the 55 percent minimum) and **grey-stage low contrast** on real Godot captures were the only Gate V findings of the overnight builds; `gate_t_regions.py` (typography and contrast regions) is the remedy and is already part of Phase 3. The cove is mostly mid-blue and sand on a warm grey stage: expect the same class of MAJOR, not BLOCKERs.
- **GATE T and the editor crop.** The Inspector dock crop has small dark UI text; it is image content inside the framed window (its text is the real editor's). If GATE T flags it, declare the region in the beat's `qc.typography_regions` (the toolkit's own opt-in) rather than shrinking or recolouring it.
- **Ink rings and dark small shapes beside mid-tones fail GATE T**; ring with grey (the ShaderLab ring already has a grey backing). Terracotta is never text.
- **Pango `Text()` can drop single spaces on this Mac**: the Manim scenes already double the space where it happened ("one  point  each"); LOOK at every still again after any edit.
- **Renders:** foreground, `--concurrency=1`, only through `remotion_scenes.py`; never hand-roll `npx remotion render`. Chrome 157's headless shell crashes on this Mac; the toolkit prefers Playwright's.
- **Disk:** check `df -h /` before 4K; about 20 GB free at the layout stage; each 4K render step can need several GB of scratch. Stop under about 15 GB free and report.
- **The Lab lock is shared** (`/private/tmp/claude-501/shaderlab.lock`): other sessions record Godot clips too, so a capture can wait many minutes. Never bypass the lock; never `pkill -f` a script name (kill by PID); never name a zsh variable `path`.
- **Godot captures are offline at a fixed tick rate**: never claim real-time frame rate; label every scripted event. A covered or hidden Godot window stops drawing and its `TIME` stops with it (the offline harness is immune; any real-time run keeps its window on top).
- **Renderer labels.** Every capture is Forward+ except C07b, C24 (right half) and C35 (Compatibility); the lanes' `videoLabel` say so. Do not relabel.
- **Drawings are labelled** (a small grey 'drawing' tag on B14, B16, B40 and B42). B02, B08, B09, B26 and B27 are drawings around REAL images, real labels and measured numbers; do not swap in other numbers.
- **ShaderLab wraps long code lines at any full stop**, which can cut a number in two (0. / 15). The lane generator already re-breaks the nine such lines (whitespace only, `codeFile` says "long lines re-broken": `$EV/scripts/wrap_check.py` finds none left). If a still shows another cut number after any edit, re-run `wrap_check.py`; do not edit the shader files (they are byte-identical to the project's copies).
- **The wave clock.** From `05b-synced-clock` on, the shader reads a `wave_clock` uniform that `water_driver.gd` writes from the capture clock (`W_FOLLOW=1`). If a later capture shows frozen waves, the driver was not attached (the scene script prints no error): check `W_FOLLOW`.
- **`get_shader_parameter` returns null for a uniform never set from code** (facts4): do not "fix" the driver to read it; the driver owns the three wave numbers on purpose.

## Hard stops

- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Do not touch any other film's folder, any game or course repository, or the toolkit beyond (if needed) `ShaderLab.tsx`.
- Do not change `narration.py`, `lanes/` or the beat order except as the rule above allows (one line, one re-voice, logged).
- Do not edit `brutalist.art/runtime/pronunciation/liam.json`.
- Do not delete `evidence/`, `captures/`, `water-project/` or `lab-shaders/`.
- STOP when the master exists and the gates pass. Hand over; Bear decides what happens next (staging and publishing only on his word, from TOPOST).

## Final report (to Bear, concise)

Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), what was re-recorded and why, any slate, any mispronunciation (and the words), any capture that disagreed with its verified number, any gate that needed more than a re-crop, and the B38 clip-spread result. Report every file by absolute path. Claim nothing you did not verify by looking at frames.

# BUILD-PROMPT — Your First Shaders and Materials with Claude and Godot (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A Cowork session did the thinking and the laying out: it read the whole assignment, wrote the act map, the narration (75 body beats plus the six bookends), the beat sheet, every Manim scene and Remotion lane, the fact-check, the shot list, and it ran and captured the real evidence (a wrapper run, three mutations, the hint experiment and the pad values in two renderers, real editor frames where they could be recorded). What is left is mechanical: voice it, build the title card, look at stills, review cut, final 4K master, gates.
**Why.** Bear's two-stage rule (2026-10-11): Cowork lays the film out; Claude Code renders and builds. No approval gate sits in front of free steps (Kokoro, Manim, Remotion, real captures run straight through); nothing is published or staged.
**Found.** Everything on screen traces to a real run or a real file, with its renderer and its origin labelled. The paperwork is written (ACTS, SHOTLIST, FACTCHECK, CHECKS-REPORT, SOURCES, PROMPTS, EVIDENCE-INDEX). 
**Not verified.** No audio exists, so no scene has been paced against real speech; no scene has been rendered at 4K; no gate has run on the assembled film (only the static checks on stills); nobody has listened to the voice. Estimated runtime 957 s, about 16 minutes, at 3.2 words per second (the sibling films run 2.6 to 3.4). That is longer than Bear's 10 to 14 minute target: whether to cut beats is Bear's decision and is made BEFORE this build (candidates in `R/ToDo.md`); this build does not change the narration.

Run every command from `<books>` = `/Users/bear/Documents/CoWork/bear-textbooks/books`. Reel path: `R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot` (every command below uses the absolute `$R`, so nothing depends on the current directory).

## Read first
1. `<books>/brutalist.art/skills/make/lecture/SKILL.md` (governing skill; **videos are never numbered**: the card and the sheet carry no number, no "start here").
2. `<books>/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute-path reporting).
3. `R/ACTS.md`, `R/EVIDENCE-INDEX.md` (what may and may not be claimed), `R/evidence/EVIDENCE-NOTES.md`, `R/BUILDER-BRIEF.md` (the scene laws the scenes were written under), and `R/BUILD-LOG.md` (what the layout stage found and cut).
4. The sibling build that ran this pipeline end to end: `<books>/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-3d-assets-blender-mcp/BUILD-LOG.md` ("Mistakes worth not repeating").

## The commands, in order (all from `<books>`)

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot
df -h /System/Volumes/Data | tail -1           # stop and say so under ~15 GB free (the 4K Manim cache is large)
# 1. the sheet (idempotent; keeps measured audio). NEVER re-run it after `art final` (it wipes the build stamps).
python3 $R/make_sheet.py
# 2. the voice (free, local Kokoro am_onyx), then the declared pauses and the measured durations
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R
python3 $R/prepare_audio.py                    # BIDEA +0.8 s lead, BVDT +0.5 s lead, BOUT +1.0 s tail (the toolkit does NOT honour lead_silence_s / tail_silence_s); re-run after ANY re-voice
python3 $R/make_sheet.py                       # refills every Remotion durationSeconds from the measured audio
python3 $R/retime_cues.py                      # scales the CCPlainShell cue frames of B20 B21 B22 B48 B58 B71 from the estimate to the measured audio; re-run it after EVERY make_sheet.py; `--check` prints without writing
# 3. listen with a machine: what did Liam actually say?
python3 $R/whisper_check.py                    # writes WHISPER-CHECK.md and _qc/asr.json; READ the table
# 4. the title card (BOPEN) needs BOPEN's measured audio, which now exists
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # the file the builder printed
# 5. scenes.py = kit + the ten scenes_act*.py + the midpoint guard
python3 $R/assemble_scenes.py
python3 $R/build_docs.py                       # SHOTLIST.md, FACTCHECK.md, CHECKS-REPORT.md from the sheet, lanes and factcheck rows
# 6. PACE PASS (the scenes were paced from ESTIMATES): every Manim class at low quality, [pace] OVER = the clip outruns its audio
python3 $R/pace_report.py                      # writes _qc/pace.md; fix every OVER (shorten a final wait or a fixed sequence in scenes_act<N>.py, never the narration), then re-run assemble_scenes.py and pace_report.py <BEAT_ID>
# 7. STILLS FIRST: contact sheets, then LOOK at them (Read the PNGs): Manim classes 10/25/50/75/95%, Remotion beats 25/50/95%. `_qc/stills/` is stale the moment a scene file changes: re-run qstill.py before judging a still
python3 $R/qstill.py --scenes scenes.py <Class> ...      # _qc/stills/<Class>.png (all Manim classes: grep the class names from beat_sheet.json)
python3 $R/still_remotion.py <BEAT_ID> ...               # the CCPlainShell / Remotion beats and the bookends
# 8. review cut, then the clean master
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

## Gates that must PASS (fix the smallest unit, re-run only that, log it in `R/BUILD-LOG.md`)
Gate F (`python3 brutalist.art/runtime/qc/factcheck_check.py $R`: FACTCHECK.md, verdicts PASS / CORRECTED / EXEMPT only), PROOF GATE (CHECKS-REPORT.md), Gate L, Gate A (static scene check), Gate B (layout audit), Gate W, Gate V (frame check), **GATE T** (type), `bookend_check.py`, loudness, master and SRT checks. Look at frames and `qc-sheet.png`; the mp4 probe alone proves nothing. Final master checks: 3840x2160, runtime = the sum of the audio (+ frame rounding), the silent tail present (>= 1.0 s), no beat labels on the clean master.

## Traps already met (A3 film, this layout stage) and what to do
- **No audio existed when the scenes were written.** Cues use `until(self, "phrase")` (character share of the narration), so they scale; fixed sequences were finished by ~75% of the estimate. If real audio is SHORTER than the estimate by more than ~20% for a beat, that beat's pace pass will say OVER: shorten the scene, not the voice.
- **`art run` skips a beat as "already filled" when `manim/<BID>.mp4` exists.** To redo one: move `manim/<BID>.mp4`, `clips/<BID>.mp4` and `media/videos/scenes/2160p24/partial_movie_files/<class>` into `_superseded/`, then re-run.
- **GATE T reads any pixel within 48 RGB of ink as text.** The dark engine ground (RGB 20,38,45), the dark teal texture, Godot's dark editor and dark rings become "text blobs". The scenes frame them with a light border and land them after the clip midpoint; if a class still fails at the real 4K gate, crop tighter or move the landing later (never recolour a real capture). Approximations at 1080p/2x pass what the real 4K gate fails: judge from 4K frames.
- **Manim's cache replays old pixels** when an image behind the same path changes: change the file name (the scenes use `crop_img(...)`, which names each crop), clear stale partials before the final render.
- **Pango drops some single spaces** in `Text()` on this Mac (words fuse): look at stills; double the space at the fused boundary in the scene.
- **Code and log text is Menlo at size 20-24** (measured: 24 = 0.20 units/char, x-height 49 px at 4K; 20 = 0.15 units/char, x-height 41 px = GATE T's floor). If GATE T flags a code block at size 20, move the block's last lines to a second picture; do not reflow real code.
- **Kokoro**: "A. I." is joined by the pronunciation dictionary (do not edit `brutalist.art/runtime/pronunciation/liam.json`; report anything heard wrong to Bear). Words to listen for in WHISPER-CHECK.md: "Godot" (dictionary: Go-doe), "uniform", "Compatibility", "Forward Plus", "Ag X", "Aces", "Sobel", "U V", "S R G B", "G L S L", and the BOPEN order (playlist, title, summary) and the greeting "Hallo". The check phonemized the risky phrases already (no audio): all read as intended.
- **Remotion renders only via the toolkit** (`art run` calls `remotion_scenes.py`); never hand-roll `npx remotion render`. Chrome 157 quirk: Playwright's shell is used automatically.
- **Never edit the beat sheet while a compiler runs**, and never re-run `make_sheet.py` after `art final`.
- **Disk**: check `df -h` before the 4K render; `exports/`, `manim/`, `clips/` and `media/` are large. Delete scratch media you made under `/private/tmp/claude-501/`.

## Traps found while laying THIS film out (read before the first gate run)
- **Remotion cues were written against the ESTIMATED duration.** B20, B21, B22, B48, B58 and B71 are `CCPlainShell` beats whose `lineCues` and `rings[].cue` are frames at 30 fps. After the audio exists, `make_sheet.py` restores the estimate-based cues and fills the measured `durationSeconds`; `retime_cues.py` then scales every cue by measured / estimated, keeps clear of the 44-56 % window (GATE T and Gate V sample the 50 % frame) and keeps order. Run it after EVERY `make_sheet.py`, and look at `still_remotion.py` frames for those six beats afterwards. (Older per-beat helpers `evidence/act6/b48_cues.py` and `evidence/act8/cues_b58.py` compute the same thing from phrase positions; use them only if a cue still reads wrong, and write the result into `lanes/`, never into `beat_sheet.json` alone.)
- **GATE T reads a wide terracotta OUTLINE as accent text** (§8.3: aspect 1.5-15, stroke >= 4 % of its box). The builders kept terracotta to code LINES (`ring_line`, aspect > 15), DOTS, pointers and circles round spheres, and used grey rings round boxes; a few rings round shorter pieces of text (for example B33's `UNIFORM_TYPES {}`) passed their 4K runs, but they are the first suspects if 8.3 fails. If a class fails 8.3 for terracotta, change the ring to a dot or a grey ring; never recolour a real capture. The `claude-code` mark (B06, B07, B55) is terracotta too and appears AFTER the clip midpoint on purpose; if GATE T still reads it, report it (a toolkit exemption is Bear's call) and do not edit `brutalist.art/`.
- **Dark engine and editor pictures vs GATE T.** Godot's dark editor, the dark engine ground (20,38,45) and the dark panel (18,31,41; 50 from INK) flip between frames. Real editor frames (`captures/editor/`, `pantry/a5_*`, `a7_*`) are framed in light borders and land after the midpoint; the real Shader Editor strips fail at 4K (light-on-dark glyph halos), so B50 draws the same lines from the file's own text and B49 carries the real editor frames. Prove any dark capture at 4K, not at preview size. Builders left per-act recipes: `evidence/act9/gate4k.sh <Class>` renders one class at 4K, cuts 44/47/50/53/56/85 % and runs GATE T + Gate V on them.
- **The last recorded Act IX 4K run predates the last edit of `scenes_act9.py`.** Re-check B63 and B64 first (85 % rows: label overlap, mean contrast); GATE T itself samples 50 %. B60, B64 and B68 are `sparse: true` (underfill is waived for phased beats). Acts III, VII, VIII, X and the six Remotion beats have had no 4K run.
- **Gate A needs embedded literals.** Code and log text in a scene is written into the scene file as literals (the static check cannot read a file at render time): do not replace those with file reads.
- **Code soft-wrap rows.** A real line longer than the block is shown as a continuation row with a hook (B19/B24 wrapper and flag line, B38/B50/B53 `surface`, `standard_generated`, `hint` lines). The characters are verbatim; do not reflow.
- **B72's last row lands at the very end of its narration** (content 10.0 s of a 10.31 s estimate). If `pace_report.py` calls it OVER, shorten the scene's fixed run_times.
- **`CCPlainShell` and Chrome 157.** `still_remotion.py` passes the Playwright headless shell to Remotion (`--browser-executable`); `art run` uses the toolkit's own path. Never hand-roll `npx remotion render`.
- **Orphaned `remotion still` processes.** An interrupted or hung still run leaves `npm exec remotion still`, `node ...remotion still` and `esbuild --service` processes behind (a dozen were found hanging for over an hour at the end of this layout stage and killed). After any still pass run `ps -axo pid,etime,command | grep -E 'remotion still|esbuild --service'` and kill what is left from your own run; never `pkill` anything you did not start.
- **The lab frames are an EARLIER TAKE (14 Oct 01:52)**, labelled "scripted input · earlier take, 14 Oct". The panel text there differs from today's `verification.gd`; only "Render and play still need checking." is quoted or ringed. Do not replace them with a fresh capture without telling Bear (a fresh capture needs the editor-capture driver and the Lab lock, which this build does not run).

## What is real, what is labelled (do not "fix" these)
- The example is an AI-written INSTRUCTOR EXAMPLE; on-screen `instructor example · A. I.-written` chips are deliberate. Prompts of the assignment carry `documented, not run`. Captures carry their renderer and origin (`the example, 14 Oct` / `re-run for this film` / `scripted input`). Do not remove a label to make a gate pass; move it.
- Pixel numbers differ by renderer on purpose (Compatibility vs Forward+): the film says which.
- The hint fixtures differ on purpose: the example's has no WorldEnvironment node; the re-run adds one.

## Hard stops
- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. No `git add/commit/push`. Free steps run straight through with no approval gate.
- Do not change the narration, the scene design or the beat sheet. If a gate fails, fix the smallest unit and log it. Do not touch `walker-claude/` (read-only evidence) or the toolkit's pronunciation file.
- Do not claim the film is built unless the master exists and the gates passed.

## Final report (to Bear, concise)
Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), any slate, any mispronunciation (quote WHISPER-CHECK.md), any `OVER` you fixed and how, any gate that did not pass. Report every file by absolute path. Do not claim anything you did not verify by looking at frames.

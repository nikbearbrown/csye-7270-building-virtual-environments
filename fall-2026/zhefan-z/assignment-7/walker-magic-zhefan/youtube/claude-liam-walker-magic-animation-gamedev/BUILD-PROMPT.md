# BUILD-PROMPT — Keys on the Tick: A Run Cycle and a Wolf Lunge

How this reel was built, so it can be rebuilt.

**Skill:** Brutalist `godot-gamedev` with the `walker` modifier (the same installation as the Assignment 6 film); the capture follows `godot-waikthrough`'s capture contract
**Subject:** `fall-2026/zhefan-z/assignment-7/walker-magic-zhefan` at **ad7935f** (game source and documents). The previous cut showed f860fed (history: this folder at `670821c` … `78767e5`).
**Output:** native 4K landscape, 3840×2160 @ 30 fps, no captions
**Voice:** Liam in for Bear — Kokoro `am_onyx`, local, free

## Human inputs
- The film brief `prompt-6-film.txt`, and its update `prompt-9-film.txt` Part 2: bring the film in line with the published film requirements (the game and both clips; the four ideas in the author's words, each pointing at a shown line; the sheet, its slicing and the frame track with `Animation.step`; the phase table beside the key times and the strip at each boundary; the state machine in real play with an interrupt in each phase, newly captured; read-backs, M1–M4, edges, two clocks and what no headless run shows; mistakes, overruled readings, uncertainty, next step, contributions, the sheet's terms and the revision), about 6–7 minutes, every number from the sources.
- The author's committed documents, logs, captures and figures that the film draws on.
- Not yet: the author's review of this master. `beat_sheet.json` → `metadata.human_review_approved` is `false`.

## Pipeline
```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 WALKER_ART_HOME=<brutalist.art>
export WALKER_SNAPSHOT=<base>/snapshot WALKER_CAPTURE=<base>/movie
# 0. the snapshot the checker reads, and an isolated copy to play (tar to a file, then extract)
git archive --format=tar -o <base>/snapshot.tar ad7935f:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan
tar --force-local -xf <base>/snapshot.tar -C <base>/snapshot && cp -r <base>/snapshot <base>/capproj
godot --headless --path <base>/capproj --import
# 1. the scripted-input capture (windowed Movie Maker, 60 fps; CAPTURE.md), then its lossless archive
#    (click delays found first with headless trials: ... --script driver.gd --fixed-fps 60 -- <in> <out> only=cancel,lunge_hit,recover_hit)
godot --path <base>/capproj --script <reel>/capture/driver.gd --write-movie <base>/movie/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- <reel>/capture/run-02-inputs.jsonl <reel>/capture/run-02-frames.jsonl
ffmpeg -framerate 60 -i <base>/movie/frame%08d.png -c:v libx264rgb -crf 0 <reel>/capture/run-02.mp4
# 2. sheet from SCRIPT.md, then the narration (durations are the clock)
cd scripts && python sheet.py && cd ..
python $WALKER_ART_HOME/runtime/scripts/generate_audio_kokoro.py . --only <beats without audio>
# 3. gameplay beats (frame-exact), cards and Remotion props, Remotion beats
cd scripts && python footage.py && python media.py
python remotion_win.py .. --force
# 4. ledgers, shot list, checks
python ledgers.py && python shotlist.py && cd ..
$WALKER_ART_HOME/art godot-gamedev --check . --game $WALKER_SNAPSHOT
# 5. master, then frame-level QC
$WALKER_ART_HOME/art final . --height 2160 --fps 30 --out exports/landscape
```
`python` is the system Python with `kokoro-onnx`, Pillow and NumPy (SciPy is not needed).

## Deliberate choices
- **One new capture, scripted input, at 60 fps.** `capture/driver.gd` plays five fresh segments of the real main scene through key and mouse events and asserts its results: the run, both lunge facings, and a fireball hit in GROWL, LUNGE and RECOVER. Its first three segments are run-01's, unchanged, so their frame numbers carry over (rows 0–1622 of the frame log are identical). Labelled "Scripted input · real engine output" on every frame it appears in.
- **The phase of a hit comes from the log.** A hit is resolved before the wolf's update on its tick, so the phase that counts is the state of the previous tick; the driver logs it (`wolf_hit`), `footage.py` asserts it against the frame log and prints it on a chip from the hit frame on.
- **No retiming.** Each gameplay beat is built to the frame count of its narration: the interval once at real speed (every second captured frame), then a labelled ×0.25 replay (every frame twice), then a labelled hold.
- **The four ideas in the author's words.** Each idea card quotes one sentence of CHANGE-BRIEF.md:197 and shows the exact lines it points at (file:line); `media.py` reads every document line with `git show ad7935f:` (the working-tree documents were being revised during the build; FACTCHECK.md) and checks every code line against the snapshot and the working tree. The checker's exact-excerpt rule covers the three workbench beats; the idea cards are labelled "Source view — reconstruction".
- **The author's claim is marked as a claim.** The four-ideas sentence that a broken path is "skipped with no error" is quoted, and the card says no run here played a broken clip (FACTCHECK.md, Corrections).
- **Fixtures are labelled.** Everything from `captures/look`, `captures/lunge`, `captures/run` is labelled "Fixture capture" (the harnesses place the characters); `captures/figures` is labelled "Figure from the logs".
- **Logs over documents.** Where a document and a log disagree, the screen shows the log (FACTCHECK.md, "Corrections").
- **Cards fill the canvas.** Card layouts pick the largest type and the largest whole zoom that pass their own overflow checks (`media.py` `fit`).
- **Excerpts fit the panel.** `GodotDevWorkbench` does not scroll; every workbench shows at most 12 lines and two short notes.
- **Length.** The restructured narration first measured 1422 words; it was cut to 1313 words, 6 min 56 s with the outro. Finishing the requirements (B08 the author's note, B14 the "what the game reads" column, B23 the recorded slips, B24 without an unsourced commit) brought it to 1347 words, 7 min 4 s.
- **Cut from the previous film** for length and to make room for the requirements: before/after (its "now" frame is on B02), the onion skin, two alignment bugs, the growl-window and second-clock figures (their numbers are on B05 and B17), the run r0 dead ends, and the three beyond-the-requirements beats (torches, flicker measurement, embers and afterimage — the torches and embers stay visible behind every gameplay beat).
- **Outro silent.** This toolkit copy has no stock jingle, so B28 is `audio_policy: silence` (as in Assignments 1–6).
- **Scripts adapted** from the Assignment 6 film (`docs/a6/youtube/claude-liam-walker-magic-particles-gamedev/scripts/`); `cards.py` and `remotion_win.py` copied unchanged (provenance line only); `footage.py`, `media.py`, `ledgers.py`, `shotlist.py`, `sheet.py`, `common.py` and the capture driver adapted.
- **Toolkit untouched.** The only writes outside the reel are Remotion's usage index (`runtime/remotion/_bench/consumers.json`, written by `remotion_scenes.py`) and the snapshot, capture copy, PNG frames, trial logs and review images in a scratch folder outside the repository.
- **Nothing else in the project changed:** no game file, test, document or `shaders/` file outside `youtube/`.

## Environment notes
FFmpeg 9.0.2 (Gyan); cards are Pillow PNGs. Kokoro model in `runtime/models/kokoro/`. Node 24 for Remotion. Windows, Git Bash. Godot 4.7.2-stable for the capture.

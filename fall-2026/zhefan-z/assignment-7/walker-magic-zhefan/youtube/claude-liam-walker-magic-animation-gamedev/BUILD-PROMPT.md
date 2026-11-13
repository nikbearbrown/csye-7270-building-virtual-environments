# BUILD-PROMPT — Keys on the Tick: A Run Cycle and a Wolf Lunge

How this reel was built, so it can be rebuilt.

**Skill:** Brutalist `godot-gamedev` with the `walker` modifier (the same installation as the Assignment 6 film); the capture follows `godot-waikthrough`'s capture contract
**Subject:** `fall-2026/zhefan-z/assignment-7/walker-magic-zhefan` at **f860fed** (game source and documents)
**Output:** native 4K landscape, 3840×2160 @ 30 fps, no captions
**Voice:** Liam in for Bear — Kokoro `am_onyx`, local, free

## Human inputs
- The film brief `prompt-6-film.txt`: about 5 to 6 minutes, real engine footage first, the eight sections, labels for fixtures and scripted input, media out of git, commit the records.
- The author's committed documents, logs, captures and figures that the film draws on.
- Not yet: the author's review of the master. `beat_sheet.json` → `metadata.human_review_approved` is `false`.

## Pipeline
```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 WALKER_ART_HOME=<brutalist.art>
export WALKER_SNAPSHOT=<base>/snapshot WALKER_CAPTURE=<base>/movie
# 0. the snapshot the checker reads, and an isolated copy to play (tar to a file, then extract)
git archive --format=tar -o <base>/snapshot.tar f860fed:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan
tar --force-local -xf <base>/snapshot.tar -C <base>/snapshot && cp -r <base>/snapshot <base>/capproj
godot --headless --path <base>/capproj --import
# 1. the scripted-input capture (windowed Movie Maker, 60 fps; CAPTURE.md), then its lossless archive
godot --path <base>/capproj --script <reel>/capture/driver.gd --write-movie <base>/movie/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- <reel>/capture/run-01-inputs.jsonl <reel>/capture/run-01-frames.jsonl
ffmpeg -framerate 60 -i <base>/movie/frame%08d.png -c:v libx264rgb -crf 0 <reel>/capture/run-01.mp4
# 2. sheet from SCRIPT.md, then the narration (durations are the clock)
cd scripts && python sheet.py && cd ..
python $WALKER_ART_HOME/runtime/scripts/generate_audio_kokoro.py .
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
- **One new capture, scripted input, at 60 fps.** The capture contract allows an input-driven, windowed Movie Maker run of the real main scene; `capture/driver.gd` plays three fresh segments through key and mouse events and asserts its results. At 60 fps one frame is one physics tick, which is what the film is about. Labelled "Scripted input · real engine output" on every frame it appears in.
- **No retiming.** Each gameplay beat is built to the frame count of its narration: the interval once at real speed (every second captured frame), then a labelled ×0.25 replay (every frame twice), then a labelled hold.
- **A state chip, not an overlay.** The game draws no overlay; the film reads each frame's state from `capture/run-01-frames.jsonl` and prints it in a chip under the action.
- **Fixtures are labelled.** Everything from `captures/look`, `captures/lunge`, `captures/run` is labelled "Fixture capture" (the harnesses place the characters); `captures/figures` is labelled "Figure from the logs".
- **Logs over documents.** Where a document and a log disagree, the screen shows the log (FACTCHECK.md, "Corrections").
- **Cards fill the canvas.** Card layouts pick the largest type and the largest whole zoom that pass their own overflow checks (`media.py` `fit`); a label-width check was added after the B18 heading ran past the right margin.
- **Excerpts fit the panel.** `GodotDevWorkbench` does not scroll and clips its notes column; the pilot (B07) showed the third note cut off, so every workbench carries at most two short notes. The first full render cut B10, B12, B15 and B23 before their cued lines; those excerpts were narrowed (93–101, 143–154, 152–163, 19–30) and re-rendered.
- **Gate V.** The first `art final` was refused (B01 under-filled, 54 % of the safe area); the writer's type went from 190 to 235 px and the second export passed with 0 BLOCKER / 0 MAJOR.
- **Length.** The first narration measured 7.4 min; it was cut twice to 374.8 s of beats (6 min 15 s with the outro).
- **Outro silent.** This toolkit copy has no stock jingle, so B30 is `audio_policy: silence` (as in Assignments 1–6).
- **Scripts adapted** from the Assignment 6 film (`docs/a6/youtube/claude-liam-walker-magic-particles-gamedev/scripts/`); `cards.py` and `remotion_win.py` copied unchanged (provenance line only); `footage.py`, `media.py`, `ledgers.py`, `shotlist.py`, `sheet.py`, `common.py` and the capture driver adapted.
- **Toolkit untouched.** The only writes outside the reel are Remotion's usage index (`runtime/remotion/_bench/consumers.json`, written by `remotion_scenes.py`) and the snapshot, capture copy, PNG frames and review images in a scratch folder outside the repository.
- **Nothing else in the project changed:** no game file, test, document or `shaders/` file outside `youtube/`.

## Environment notes
FFmpeg 9.0.2 (Gyan); cards are Pillow PNGs. Kokoro model in `runtime/models/kokoro/`. Node 24 for Remotion. Windows, Git Bash. Godot 4.7.2-stable for the capture.

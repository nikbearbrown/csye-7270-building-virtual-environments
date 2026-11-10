# BUILD-PROMPT — A Burst and a Trail: Two Particle Effects for One Fireball

How this reel was built, so it can be rebuilt.

**Skill:** Brutalist `godot-gamedev` with the `walker` modifier (same installation as the Assignment 5 film); the capture follows `godot-waikthrough`'s capture contract
**Subject:** `fall-2026/zhefan-z/assignment-6/walker-magic-zhefan` at **3c37fe0** (game source and documents)
**Output:** native 4K landscape, 3840×2160 @ 30 fps, no captions
**Voice:** Liam in for Bear — Kokoro `am_onyx`, local, free

## Human inputs
- The film brief `prompt-9-film.txt`: requirements, sources of truth and their order, the capture rule and its labels, media out of Git, commit the records.
- The author's committed strips in `captures/` and every document the film draws on.
- Not yet: the author's review of the master. `beat_sheet.json` → `metadata.human_review_approved` is `false`.

## Pipeline
```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 WALKER_ART_HOME=<brutalist.art>
export WALKER_SNAPSHOT=<base>/snapshot WALKER_CAPTURE=<base>/movie
# 0. the snapshot the checker reads, and an isolated copy to play (tar to a file, then extract)
git archive --format=tar -o <base>/snapshot.tar 3c37fe0:fall-2026/zhefan-z/assignment-6/walker-magic-zhefan
tar --force-local -xf <base>/snapshot.tar -C <base>/snapshot && cp -r <base>/snapshot <base>/capproj
godot --headless --path <base>/capproj --import
# 1. the scripted-input capture (windowed Movie Maker; CAPTURE.md), then its lossless archive
godot --path <base>/capproj --script <reel>/capture/driver.gd --write-movie <base>/movie/frame.png \
  --fixed-fps 30 --resolution 1280x720 --quit-after 1500 -- <reel>/capture/run-01-inputs.jsonl
ffmpeg -framerate 30 -i <base>/movie/frame%08d.png -c:v libx264rgb -crf 0 <reel>/capture/run-01.mp4
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

## Deliberate choices
- **One new capture, scripted input.** The repository has no gameplay video, and the skill's capture contract allows an input-driven, windowed Movie Maker run of the real main scene. `capture/driver.gd` plays it through mouse and key events and asserts its results. It runs the game inside a standalone SubViewport so injected mouse motion reaches the aim without taking over the real cursor (CAPTURE.md). Labelled "Scripted input · real engine output" on every frame.
- **No retiming.** Each gameplay beat is built to the frame count of its narration: the interval once at real speed, then a labelled ×0.25 replay, then a labelled hold. The compiler's clip is then exactly the beat's length.
- **Strips are fixtures.** Every strip image is labelled "Fixture capture · preview scene strip, not gameplay".
- **Cards fill the canvas.** Card layouts pick the largest type and the largest whole zoom that pass their own overflow checks (`media.py` `fit`).
- **Excerpts fit the panel.** `GodotDevWorkbench` does not scroll; excerpts were narrowed to what shows at a readable size, with the rest in labelled source notes.
- **Outro silent.** This toolkit copy has no stock jingle, so B31 is `audio_policy: silence` (as in Assignments 1–5).
- **Scripts adapted** from the Assignment 5 film (`docs/a5/youtube/claude-liam-walker-magic-shaders-gamedev/scripts/`); `cards.py` and `remotion_win.py` copied unchanged; `footage.py` and the capture driver are new.
- **Toolkit untouched.** The only writes outside the reel are Remotion's usage index (`runtime/remotion/_bench/consumers.json`, written by `remotion_scenes.py`) and the snapshot, capture copy and PNG frames in a scratch folder outside the repository.
- **Nothing else in the project changed:** no `.gdshader`, `.tres`, `.tscn`, `.import`, test or document outside `youtube/`.

## Environment notes
FFmpeg 9.0.2 (Gyan); cards are Pillow PNGs. Kokoro model in `runtime/models/kokoro/`. Node 24 for Remotion. Windows, Git Bash. Godot 4.7.2-stable for the capture.

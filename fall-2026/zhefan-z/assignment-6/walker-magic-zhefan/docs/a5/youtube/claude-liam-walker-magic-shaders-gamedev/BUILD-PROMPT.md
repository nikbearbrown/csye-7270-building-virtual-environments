# BUILD-PROMPT — A Red Flash, a Frosted Rock: Two Shaders for a Cave Mage

How this reel was built, so it can be rebuilt.

**Skill:** Brutalist `godot-gamedev` with the `walker` modifier (same installation as the Assignment 3 film)
**Subject:** `fall-2026/zhefan-z/assignment-5/walker-magic-zhefan` at **40c42f5** (game source; later commits are documents only)
**Output:** native 4K landscape, 3840×2160 @ 30 fps, no captions
**Voice:** Liam in for Bear — Kokoro `am_onyx`, local, free

## Human inputs
- The film brief `prompt-6-film.txt`: requirements, sources of truth and their order, labels, media out of Git, no commit.
- The author's in-engine captures in `captures/` and every document the film draws on.
- Not yet: the author's review of the master. `beat_sheet.json` → `metadata.human_review_approved` is `false`.

## Pipeline
```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 WALKER_ART_HOME=<brutalist.art>
export WALKER_SNAPSHOT=<base>/snapshot
# 0. the snapshot the checker reads (tar to a file, then extract)
git archive --format=tar -o <base>/snapshot.tar 40c42f5:fall-2026/zhefan-z/assignment-5/walker-magic-zhefan
tar -xf <base>/snapshot.tar -C <base>/snapshot && rm <base>/snapshot.tar
# 1. sheet from SCRIPT.md, then the narration (durations are the clock)
cd scripts && python sheet.py && cd ..
python $WALKER_ART_HOME/runtime/scripts/generate_audio_kokoro.py .
# 2. cards and Remotion props
cd scripts && python media.py
# 3. Remotion beats through the toolkit wrapper (Windows npx fix, in memory)
python remotion_win.py .. --force
# 4. ledgers, shot list, checks
python ledgers.py && python shotlist.py && cd ..
$WALKER_ART_HOME/art godot-gamedev --check . --game $WALKER_SNAPSHOT
# 5. master, then frame-level QC
$WALKER_ART_HOME/art final . --height 2160 --fps 30 --out exports/landscape
```

## Deliberate choices
- **No new capture.** Every image of the game is one of the author's committed captures (640×360), enlarged on a card with the factor stated, labelled "In-engine capture · scripted". There is no footage of the tint in motion; the driver's behaviour over time is shown as the recorded headless results (B07), labelled as not a render.
- **Documents and comparisons are not Godot views.** B03 (CHANGE-BRIEF.md) and B22 (two generated lines beside two of the author's) are reconstructed document/source views, so the checker's excerpt set is the eight GodotDevWorkbench beats, each followed by its result.
- **Checker target.** `--game` is a `git archive` of `40c42f5`, the revision the film names.
- **Outro silent.** This toolkit copy has no stock jingle, so B30 is `audio_policy: silence` (as in Assignments 1–3).
- **Scripts adapted** from the Assignment 3 film (`docs/a3/youtube/claude-liam-walker-magic-3d-assets-gamedev/scripts/`); `remotion_win.py` copied unchanged.
- **Toolkit untouched.** The only writes outside the reel are Remotion's usage index (`runtime/remotion/_bench/consumers.json`, written by `remotion_scenes.py`) and the snapshot under `E:\7270\tools\capture\a5-40c42f5\`.
- **Nothing else in the project changed:** no `.gdshader`, `.tres`, `.tscn`, `.import`, test or document outside `youtube/`.

## Environment notes
FFmpeg 9.0.2 (Gyan); cards are Pillow PNGs. Kokoro model in `runtime/models/kokoro/`. Node for Remotion. Windows, Git Bash.

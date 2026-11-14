# BUILD-PROMPT — Cold Stone, Warm Gold: Three 3D Props for a Cave Mage

How this reel was built, so it can be rebuilt.

**Skill:** Brutalist `godot-gamedev` with the `walker` modifier (the capture follows `godot-waikthrough`'s capture contract)
**Subject:** `fall-2026/zhefan-z/assignment-3/walker-magic-zhefan` at **8d8895c** (game files identical to 1bacec8)
**Output:** native 4K landscape, 3840×2160 @ 30 fps, no captions
**Voice:** Liam in for Bear — Kokoro `am_onyx`, local, free

## Human inputs
- The film brief: requirements, labels ("my screenshot"; nothing reconstructed), facts only from CHANGE-BRIEF.md, TEST-REPORT.md and FRICTIONAL.md, media out of Git.
- Approval of the plan, beat sheet and script, the title, the B04 prompt excerpt, the labelled MCP look renders and the Assignment 2 exclusions; the probe and the take (the author kept the machine untouched); B16's narration written after the capture.
- The author's eight screenshots.

## Pipeline
```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 WALKER_ART_HOME=<brutalist.art>
export WALKER_SNAPSHOT=<base>/snapshot WALKER_REF=<base>/ref
# 1. copies + capture (CAPTURE.md)
bash make_capture_copies.sh 8d8895cf80a68d85e18e9142b6a687c68618c51d <base>
# 2. evidence logs on the reference copy
python -I scripts/read_glb.py $WALKER_REF/assets/models            # -> evidence/glb-read-8d8895c.log
Godot_v4.7.2-stable_win64_console.exe --headless --path $WALKER_REF --script res://tests/test_a3_assets.gd --fixed-fps 60
#                                                                     # -> evidence/test_a3_assets-8d8895c.log
# 3. sheet from the approved SCRIPT.md, then the narration (durations are the clock)
python scripts/sheet.py
python $WALKER_ART_HOME/runtime/scripts/generate_audio_kokoro.py .
# 4. cards, the B16 clip, Remotion props
cd scripts && python media.py
# 5. Remotion beats through the toolkit wrapper (Windows npx fix in memory)
python remotion_win.py .. --only <beat>
# 6. ledgers, shot list, checks
python ledgers.py && python shotlist.py && cd ..
$WALKER_ART_HOME/art godot-gamedev --check . --game $WALKER_SNAPSHOT
# 7. master
$WALKER_ART_HOME/art final . --height 2160 --fps 30 --out exports/landscape
```

## Deliberate choices
- **Blender Python is not shown as Godot.** B05, B08, B10, B12 are source-view cards labelled "Blender Python, run through the MCP — not Godot", as Assignment 2 did for its Python tool. Their exact text and result beats are in `gamedev-evidence.json` → `source_views`; the checker's excerpt set is the two Godot excerpts (B15, B17).
- **No compiler retiming.** B16 is cut to exactly the beat's frame count: the whole 12 s take at normal speed, then a labelled held final frame.
- **Checker target.** `--game` is a `git archive` of `8d8895c`, the revision the film names.
- **Outro silent.** This toolkit copy has no `svg/claude/mp3/` jingle, so B22 is `audio_policy: silence` (as in Assignments 1 and 2).
- **Scripts adapted** from the Assignment 2 film (`docs/a2/youtube/claude-liam-walker-magic-gamedev/scripts/`); `remotion_win.py` copied unchanged.
- **Toolkit untouched.** The only writes outside the reel are Remotion's usage index (`runtime/remotion/_bench/consumers.json`, written by `remotion_scenes.py`) and the copies under `E:\7270\tools\capture\`.

## Environment notes
FFmpeg 9.0.2 (Gyan); labels and cards are Pillow PNGs. Kokoro model in `runtime/models/kokoro/`. Node for Remotion.

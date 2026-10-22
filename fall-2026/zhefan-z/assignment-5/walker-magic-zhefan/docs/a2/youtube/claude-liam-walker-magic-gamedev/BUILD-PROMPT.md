# BUILD-PROMPT — Her Fire Is the Only Warmth: Building a Cave Mage Slice

How this reel was built, so it can be rebuilt.

**Skill:** Brutalist `godot-gamedev` with the `walker` modifier (captures follow `godot-waikthrough`'s capture contract)
**Subject:** `fall-2026/zhefan-z/assignment-2/walker-magic-zhefan`, game revision **74c0443**, captured from **5266946** (identical runtime files)
**Output:** native 4K landscape, 3840×2160 @ 30 fps, no captions
**Voice:** Liam in for Bear — Kokoro `am_onyx`, local, free

## Human inputs

- The film brief (requirements, labels, "never show a raw generation as in-engine footage").
- Approval of the beat sheet B01–B26, the script and the four takes; the title.
- The SLICE AUDIO method: verbal approval from the instructor the method is acceptable.
- Keep run-01 as recorded ("it's honest gameplay"); pick the clearest frames for B15.
- Confirmation that the image prompts were sent unchanged.

## Pipeline

```bash
export PYTHONUTF8=1 WALKER_ART_HOME=<brutalist.art> WALKER_SNAPSHOT=<git archive of the game folder at 74c0443>
# 1. capture: isolated copy, scripted real input, 4K Movie Maker, headless reference + gate (CAPTURE.md)
bash make_capture_copy.sh 5266946 <copy>
# 2. sheet from the approved SCRIPT.md, then the narration (durations are the clock)
python scripts/sheet.py
python $WALKER_ART_HOME/runtime/scripts/generate_audio_kokoro.py .
# 3. frame-exact gameplay cuts, SLICE AUDIO cuts, cards, Remotion props
python scripts/media.py
# 4. Remotion beats through the toolkit wrapper (Windows npx fix in memory)
python scripts/remotion_win.py .
# 5. ledgers, shot list, checks
python scripts/ledgers.py && python scripts/shotlist.py
$WALKER_ART_HOME/art godot-gamedev --check . --game $WALKER_SNAPSHOT
# 6. master
$WALKER_ART_HOME/art final . --height 2160 --fps 30 --out exports/landscape
```

## Deliberate choices

- **No compiler retiming.** `compile.py` retimes clips within ±5 %, slows shorter ones and center-cuts longer ones. Every gameplay slot is cut to exactly the frame count the compiler will give the beat, so none of that runs; the one hold (B20) is a labelled final frame.
- **SLICE AUDIO through `audio_file`, not `audio_policy: preserve`.** `preserve` is reserved for fellows' source reports. B18's `audio_file` is the take audio cut sample-exactly to the same interval as its picture; B20's is the narration over the first part, then the take audio for the slot.
- **Python tool, not a Godot view.** B08 and B12 show `tools/clean_sprites.py` in a source-view card labelled "Python cleanup tool, run outside Godot", because a Godot editor reconstruction of a `.py` file would misrepresent where it runs. They are therefore not in the checker's excerpt set; their exact text is in `gamedev-evidence.json` → `source_views`.
- **Checker target.** `--game` is a `git archive` of `74c0443`, the build the film names, so hashes and line numbers are the shown revision's, not a later working tree.
- **Outro silent.** The locked outro is silent under the stock jingle; this toolkit copy has no `svg/claude/mp3/` jingle, so, as in Assignment 1, B26 is `audio_policy: silence`.
- **Toolkit untouched.** The only writes outside the reel are Remotion's usage index (`runtime/remotion/_bench/consumers.json`, written by `remotion_scenes.py` itself) and the snapshot/capture folders under `E:\7270\tools\capture\`.

## Environment notes

- FFmpeg 9.0.2 (Gyan); its `drawtext` crashes here without a fontconfig file, so labels are Pillow PNG overlays.
- Kokoro model files in `runtime/models/kokoro/`; Node 24 for Remotion.

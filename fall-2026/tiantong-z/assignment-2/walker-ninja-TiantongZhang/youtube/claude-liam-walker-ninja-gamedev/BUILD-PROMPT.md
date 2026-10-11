# BUILD-PROMPT.md — how to rebuild this film from the repository

Everything below runs from the repository root unless stated. The toolkit lives
beside it at `../brutalist.art-main`.

## Environment

```
PYTHONUTF8=1          # Windows console encoding, or the scripts die on a dash
ART_NO_DRAWTEXT=1
ART_HOME=../brutalist.art-main
GODOT=.../Godot_v4.7.2-stable_win64.exe
```

Python 3.12 with numpy, scipy and Pillow. Node 22. `ffmpeg` on PATH.

## 1 — the game's own checks first

```bash
"$GODOT" --headless --path godot --script res://tests/test_game.gd      # 99 / 0
"$GODOT" --headless --path godot --script res://tests/test_keyboard.gd  # 14 / 14
```

## 2 — capture

```bash
python scripts/render_takes.py p t \
    --out youtube/claude-liam-walker-ninja-gamedev/capture \
    --driver res://tests/capture_gamedev.gd
python scripts/encode_captures.py \
    --frames youtube/claude-liam-walker-ninja-gamedev/capture \
    --reel   youtube/claude-liam-walker-ninja-gamedev
```

Each take prints `CAPTURE OK` or fails nonzero; a finished render is not the
claim. `render_takes.py` writes and removes a temporary `godot/override.cfg`,
because Movie Maker fixes its size from the window at startup — check that the
log says **3840×2160**, not 1280×720.

## 3 — beat sheet and ledger

```bash
python scripts/build_beat_sheet.py        # beats, narration, excerpts from source
python scripts/build_beat_bookends.py     # the real component props
python scripts/build_gamedev_ledger.py    # evidence + B09 from the recorded run
```

Order matters: the ledger validates that every beat's `props.code` equals the
file, and refuses to write otherwise.

## 4 — narration, then bind to it

```bash
python $ART_HOME/runtime/scripts/generate_audio_kokoro.py <REEL>
python scripts/finalise_beat_timing.py    # cues at measured fractions, holds derived
```

**Narration first, timing second.** Cue positions are fractions of the
*measured* audio, not of an estimate. If any narration changes, regenerate that
beat's mp3 and re-run the finalise step.

## 5 — gate before rendering

```bash
cd $ART_HOME
./art godot-gamedev --check <REEL> --game <REPO>/godot < /dev/null
```

Expect `"status": "PASS"`. Note the `< /dev/null`: `./art` subcommands read
stdin, and in a `while read` loop they consume the loop's input and report
every component as NOT RENDERABLE. That cost ten minutes once.

## 6 — pilot, then batch

```bash
python $ART_HOME/runtime/scripts/remotion_scenes.py <REEL> --only B02 --force
# LOOK AT IT. Then:
python $ART_HOME/runtime/scripts/remotion_scenes.py <REEL>
```

The pilot exists because the panel clips. **Code excerpts must be ≤ 14 lines
and note values ≤ 100 characters**; the first B02 render showed 14 of 17 lines
with its last cue pointing off-screen and a note cut mid-word. `codeFontSize`
cannot go below 23 — the schema's minimum — so the excerpt comes down to the
panel, not the other way round.

Do **not** pass `--outro`: that flag builds `OutroSeries` / `OutroCTA` from
`ABOUT.MD` / `AUTHOR.MD`, which this reel does not have. The locked
`ClaudeTitleOutro` is an ordinary beat.

## 7 — master

```bash
cd $ART_HOME
./art final <REEL> --height 2160 --fps 30 --out <REEL>/exports/landscape
```

Then re-run the gate at handoff, and inspect the actual master: code at reading
size, highlights on the lines the narration names, the editor disclosure, the
clock and sound, and the regular outro.

## Known trap

`./art final` rewrites `_qc/REPORT.md` and drops the human half. Re-append it
after the final render, as Assignment 1 had to.

It also names its output after the reel **slug**, not the locked title, so the
export has to be renamed to `NewWalkerArt_TiantongZhang.mp4` and its SHA-256
recomputed afterwards. `build-state.json` still records the pre-rename name;
it is gitignored, and `SOURCES.md` holds the hash of the renamed file.

Gate V lives at `$ART_HOME/runtime/qc/final_frame_check.py`, not under
`runtime/scripts/`, and it takes the reel as a positional argument with the
master passed as `--mp4` — there is no `--reel` flag.

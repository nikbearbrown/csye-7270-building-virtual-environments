# BUILD-PROMPT — The Little Flame Witch (pitch film)

How this film was built, so it can be rebuilt. Written by Claude Code, 2026-11-22.

**Toolkit:** Brutalist (`brutalist.art` at `29ba0e8`), free local pipeline only: Kokoro narration, Pillow and ffmpeg pictures, the toolkit's compiler and gates. No paid generation, no API key, no upload.
**Workflow:** `godot-waikthrough` (alias `godot-walkthrough`) with the `walker` modifier, for the real footage: its capture contract (isolated snapshot, scripted input through the normal input path, windowed Movie Maker, logged inputs, asserted results), `coverage.json` and its checker. The checkout has **no show-tell skill**, so the pitch beats' simple pictures are drawn by `scripts/cards.py`.
**Output:** `exports/landscape/zhefan-z-little-flame-witch-pitch.mp4`, 3840×2160, 30 fps, 216.53 s, no captions. Kept out of git.
**Voice:** Liam's voice (Kokoro `am_onyx`, local, free) speaking as the author, Zhefan Zhang, in the first person. No instructor name, persona or credit line anywhere.

## Human inputs

- `prompt-1-pitch.txt` (the author's request: beat order, dialogue lines, labels, rules).
- `PROJECT-BRIEF.md` (the seven answers; every claim in the narration comes from it or from a committed log: FACTCHECK.md).
- `art/` and `ART-PROMPTS.md` (the author's Gemini concept art and prompt record).
- One answer from the author during the build: of the two expression sheets in `art/`, the green one is `witch_expressions.png`; the transparent cut-out is left out (PROMPTS.md).
- Not yet: the author's review of this master (`beat_sheet.json` → `metadata.human_review_approved` is `false`).

## Pipeline

```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1
export BRUTALIST_HOME=<brutalist.art>
GODOT=<Godot_v4.7.2-stable_win64_console.exe>
REEL=fall-2026/zhefan-z/assignment-8/pitch      # from the repository root
BASE=<a scratch folder outside the repository>

# 0. isolated snapshots (git archive of a committed tree; the working tree is never run)
git archive --format=tar -o $BASE/snap840.tar 840b501:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan
git archive --format=tar -o $BASE/snap2b6.tar 2b68e0a:fall-2026/zhefan-z/assignment-5/walker-magic-zhefan
mkdir -p $BASE/cap840 $BASE/cap2b6
tar --force-local -xf $BASE/snap840.tar -C $BASE/cap840; tar --force-local -xf $BASE/snap2b6.tar -C $BASE/cap2b6
$GODOT --headless --path $BASE/cap840 --import; $GODOT --headless --path $BASE/cap2b6 --import
git ls-tree -r 840b501:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan | sha256sum   # coverage build_id

# 1. the two captures (windowed Movie Maker, 60 fps; CAPTURE.md)
$GODOT --path $BASE/cap840 --script $REEL/capture/driver.gd --write-movie $BASE/movie840/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- $REEL/capture/run-01-inputs.jsonl $REEL/capture/run-01-frames.jsonl
$GODOT --path $BASE/cap2b6 --script $REEL/capture/driver_a5.gd --write-movie $BASE/movie2b6/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 2000 -- $REEL/capture/a5-run-01-inputs.jsonl $REEL/capture/a5-run-01-frames.jsonl
ffmpeg -framerate 60 -i $BASE/movie840/frame%08d.png -vf scale=3840:2160:flags=neighbor -c:v libx264rgb -crf 0 -preset veryfast $REEL/capture/run-01.mp4
ffmpeg -framerate 60 -i $BASE/movie2b6/frame%08d.png -c:v libx264rgb -crf 0 $REEL/capture/a5-run-01.mp4
export CAP_840B501=$BASE/movie840 CAP_2B68E0A=$BASE/movie2b6
export A6_RUN01=fall-2026/zhefan-z/assignment-6/walker-magic-zhefan/youtube/claude-liam-walker-magic-particles-gamedev/capture/run-01.mp4

# 2. beat sheet, narration (durations are the clock), padding
cd $REEL/scripts && python sheet.py && cd -
python $BRUTALIST_HOME/runtime/scripts/generate_audio_kokoro.py $REEL --speed 1.05
cd $REEL/scripts && python sheet.py --pad

# 3. pictures: stills, then the gameplay beats (frame-exact), then the records
python cards.py && python footage.py && python records.py && cd -

# 4. gates: the walkthrough checker, then the final export (beat lint, shape gate, paperwork,
#    output decode and duration check, Gate V final-frame check), then the checker again
$BRUTALIST_HOME/art godot-waikthrough --check $REEL > $REEL/_qc/walkthrough-check.json
$BRUTALIST_HOME/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape > $REEL/_qc/final.log
$BRUTALIST_HOME/art godot-waikthrough --check $REEL > $REEL/_qc/walkthrough-check.json
```

`python` is a system Python with `kokoro-onnx`, Pillow and NumPy. FFmpeg 9.0.2 (Gyan build). Windows 11, Git Bash. The Kokoro model sits in the toolkit's `runtime/models/kokoro/`.

## Gate results (this build)

| Gate | Result | Report |
|---|---|---|
| `art godot-waikthrough --check` | PASS: 8 implemented features with evidence intervals in one 3840×2160 capture, 9 planned features with reasons | `_qc/walkthrough-check.json` |
| `art final` preflight: paperwork (FACTCHECK, SHOTLIST, PROMPTS), `beat_lint.py`, `gate_shape.py` | pass | `_qc/final.log` |
| `art final` output check: video and audio decode with `-xerror`, duration equals the timeline, audible | pass | `_qc/final.log` (exit 0) |
| Gate V, `final_frame_check.py` on the final export (the render-integrity gate): 36 frames, each beat at 50% and 85% | **0 BLOCKER, 0 MAJOR** | `_qc/REPORT.md`, `_qc/contact_sheet.png` |

Two builds were exported (the first into a scratch folder, the second into `exports/landscape/`); both gave SHA-256 `00a4dde79db7b48575471d490cbc8bfb39914f11493e99d610e76844e0aea9ce`.

**Fixed before the first export, found by the gates' rules:** the still cards first used 160 px margins and the gameplay canvas reached y 2100, outside Gate V's title-safe inset (x 192–3648, y 108–2052 at 4K); the stills are now composed and scaled to 90 % (`cards.fit_safe`), and the gameplay header was tightened so the ×5 canvas ends at y 2050. A pre-check of the stills alone flagged only B01, the full-bleed title plate, which the sheet declares `qc.full_bleed` with a contrast region on its title text (`qc.contrast_regions`, the gate's documented mechanism; every other check still runs on it). The walkthrough checker failed once on a text-encoding error when run without `PYTHONUTF8=1` (not a film defect); it passes with it.

**Warning printed by the compiler, not a gate:** "SKIN LINT: NO RENDERABLE BEATS". It means no beat uses a Remotion or Manim scene; every slot here is filled from `media/` (18/18 filled, no slates), which the same log confirms.

## Deviations from the toolkit, and why

- **No show-tell skill** in this checkout: the "simple drawn pictures" are Pillow line drawings (`scripts/cards.py`), one picture per beat, minimal text.
- **`walker` bookends not used.** The skill's walker mode opens on a reconstructed Claude prompt (`ClaudeComposerAsk`), then a "what was built" writer, and closes with Verdict and Your Turn. The author's beat order (hook, title, the seven answers, exists/will, outro) replaces them; no Claude response appears on screen.
- **Outro.** OUTRO-LOCK.md's card carries a fixed channel handle (an instructor credit). The author's rules forbid any instructor name, persona or credit line, so the slug is not `claude-liam-*` (the lock's scope) and B17 is a silent card with the title and the author's name only. The toolkit copy has no stock jingle (as in Assignments 1–7), so the outro is silent.
- **Persona.** The skill says "Liam in for Bear"; here the same Kokoro voice speaks as the author, with no instructor reference.
- **4K capture.** The checker requires a 3840×2160 capture; the game renders a 640×360 canvas. `capture/run-01.mp4` is that canvas scaled ×6 nearest neighbour, losslessly (disclosed in CAPTURE.md), not a native 4K render.
- **Narration speed.** Kokoro at `--speed 1.05`, to keep the film near 3½ minutes; some tokens are spelled for speech (`SAY` in `sheet.py`).
- **Remotion not used.** Every beat is a Pillow still or an ffmpeg-encoded gameplay clip in `media/`, compiled by `art final`.

## What was written where

- **In the reel (`pitch/`):** `beat_sheet.json`, `coverage.json`, `SHOTLIST.md`, `FACTCHECK.md`, `PROMPTS.md`, `CAPTURE.md`, `BUILD-PROMPT.md`, `SOURCES.md`, `scripts/`, `capture/` (drivers and logs), `evidence/`, `_qc/`, and, kept out of git, `mp3/`, `media/`, `clips/`, `exports/` and the capture archives.
- **Outside the repository:** the snapshots, capture copies and PNG frames in a scratch folder.
- **Not touched:** no game file, no `shaders/` folder, no earlier assignment folder (the Assignment 6 capture archive was only read and hashed), and nothing in the toolkit checkout.

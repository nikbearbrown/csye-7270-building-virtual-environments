# HANDOFF — walker-magic (CSYE 7270 Assignment 2)

> Written 2026-10-07 for a fresh Claude Code session. Read this first, then `TEST-REPORT.md`, `SOURCES.md`, `youtube/claude-liam-walker-magic-gamedev/CAPTURE.md` and `SCRIPT.md`.

## Where things are
- **Working copy (the only one):** `E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-2\walker-magic-zhefan\`, branch **`zhefan-z/assignment-2`** of `nikbearbrown/csye-7270-building-virtual-environments`. The author opens the PR in the web page (`gh` is not installed).
- Original personal repo `zhef-z/walker-magic-zhefan` is **frozen** at `920d969` (never commit there). Imported SHAs map to originals in `SOURCES.md` → "Original commit SHAs".
- Tools outside the repo: Godot 4.7.2 `E:\7270\godot\Godot_v4.7.2\`; ComfyUI + venv (Pillow, NumPy, SciPy, PyAV) `E:\7270\tools\ComfyUI\`; raw SFX `E:\7270\tools\sfx_raw\`; music source `E:\7270\tools\music_raw\Beneath_the_Unlit_Stone.mp3`; capture copies `E:\7270\tools\capture\`; Brutalist `E:\7270\brutalist.art\` (`./art`, needs Anaconda Python on PATH and `PYTHONUTF8=1`); FFmpeg 9.0.2 on PATH.

## State of the slice (done)
S1–S8 built, tested and documented. Tested build **`74c0443`**; later commits change only docs, tools and the reel. 73 headless checks in 6 suites pass (`tests/test_*.gd`), also on a fresh copy. Six human playtests recorded in `TEST-REPORT.md` (5 = sound on, 6 = muted, both on final audio; Music bus -8 dB confirmed). Final audio: five SFX OGGs (Stable Audio Open, picks and reasons in `SOURCES.md`) and `MUS-LOOP.ogg` (Gemini/Lyria, loop 60.886–115.510 s, seams confirmed by the author). README, SOURCES (with all image prompts), TEST-REPORT, FRICTIONAL (`../FRICTIONAL.md`) are current.

## Rules (the author's)
- **Git:** only push the branch, never `main`; never force-push; `git fetch`/pull before every push; if `main` moved, merge, **never rebase** (rewrites the imported commits). Commit identity `zhefan-z <255424614+zhef-z@users.noreply.github.com>`; every commit ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Never touch other students' folders or the instructor's `assignment-2/README.md`. **No full names** in the course folder (SUBMISSION.md must not repeat A1's full name).
- **Plan first** when asked; stop where the author says STOP; commit after each approved step.
- **Design docs** (CONCEPT, STORYBOARD, CHARACTER-SHEET, CHANGE-BRIEF): never change existing lines; append dated revisions only; verify the original bytes are unchanged with a separate check (a `grep` in an `&&` chain once silently skipped an append).
- **Never log template text** (`<...>`, `[paste ...]`) as the author's answer; say what is missing.
- **FRICTIONAL:** the author's entries keep their wording (formatting only). Claude Code entries: any "What I understand now" line that is a lesson starts with "(Claude Code's summary, not my words)". Rejected `*-thumb.png` thumbnails were made by Claude in claude.ai from the author's screenshots.
- **Media:** MP3, MP4, WAV, FLAC, AVI and anything over 25 MB stay out of GitHub (`.gitignore` covers the reel's `capture/*.avi`, `clips/`, `media/`, `mp3/`, `audio/`, `exports/`). The film goes to course media storage, linked from README by filename and SHA-256.

## Film — approved plan
- Skill: Brutalist **`godot-gamedev` + `walker`**, read from `E:\7270\brutalist.art\skills\make\godot-gamedev\SKILL.md` (captures follow `godot-waikthrough/references/capture-and-coverage.md`). Reel: `youtube/claude-liam-walker-magic-gamedev/`.
- **Title:** Her Fire Is the Only Warmth: Building a Cave Mage Slice.
- **Approved beat sheet:** B01–B26 exactly as in `SCRIPT.md` (Walker opening and hesitant-writer summary; assignment setup; concept and pillars; CHAR-IDLE trace design → prompt → raw output → edits → in engine; palette revision 1 cause and effect; cast; wolf; sound wiring; **SLICE AUDIO B18 and B20, no narration**; mute; the sound-trigger test and its limit; models, contributions and credits incl. **Powered by Stability AI** + license notice in B23; Verdict; Your Turn; locked outro). Labels: Reconstructed prompt · Godot editor reconstruction · Scripted-input capture · RAW GEMINI OUTPUT — not in engine · Asset file preview — not gameplay · Contact sheets — not gameplay · SLICE AUDIO — no narration · Held frame. Never show a raw generation as in-engine footage.
- **SLICE AUDIO method:** the skill's compiler strips footage audio (`compile.py`, `-an`). For B18/B20 each beat's `audio_file` is the audio track of the same Movie Maker take, cut to exactly the same interval as its video, with no narration. **Approval: verbal approval from the instructor the method is acceptable** (recorded 2026-10-07 in CAPTURE.md, FACTCHECK.md, TEST-REPORT.md).
- **Approved takes** (scripted input, capture source `5266946`, runtime-identical to `74c0443`): **run-01** route (run, jump the pit, walk into the wolf's sight, one lunge hit, cast until the wolf is down, exit); **run-02** pit fall → fail → reload → music back from the top; **run-03** M, N (silent cast), N, cast, M; **run-04** Esc pause/resume.

## Capture method (working; details in CAPTURE.md)
```
bash youtube/claude-liam-walker-magic-gamedev/make_capture_copy.sh 5266946 /e/7270/tools/capture/walker-magic-5266946
# headless reference:
WALKER_CAPTURE_MODE=run-01 WALKER_CAPTURE_LOG=<ref>/run-01-headless.jsonl Godot..._console.exe --headless --path <copy> res://capture/capture_main.tscn
# 4K take:
WALKER_CAPTURE_MODE=run-01 WALKER_CAPTURE_LOG=<reel>/capture/run-01-inputs.jsonl Godot..._console.exe --path <copy> \
  --write-movie <reel>/capture/run-01.avi --fixed-fps 60 --quit-after <cap> --resolution 3840x2160 res://capture/capture_main.tscn
python youtube/claude-liam-walker-magic-gamedev/gate.py <ref>/run-01-headless.jsonl <reel>/capture/run-01-inputs.jsonl
```
Learned the hard way: the screen is 2560x1600 (window clamps to 2564x1570); keep stretch `viewport` + 3840x2160 root in the copy; a windowed Godot reads the OS cursor (driver uses `Input.warp_mouse` in window pixels); Windows releases held keys on focus loss (driver re-asserts; the gate decides validity); a first import with the capture scripts present can segfault (script imports in two steps); Movie Maker crashed once with other apps open (close games before takes; the author must not use the PC during takes). The probe passed: `capture/probe.avi` sha256 `a5b75010…9ee90`, gate PASS.

## Pending tasks (in order)
1. ~~Record **run-01…run-04** at 4K~~ — done 2026-10-07, all gate PASS; hashes, event times, frames and audio levels in CAPTURE.md. Shown to the author; assembly waits for their OK.
2. Write `beat_sheet.json` (A1 schema: `metadata` + `beats` with `beat_id`, `narration_text`, `voice: am_onyx`, `engine: kokoro`, `shot`…; `audio_policy: "silence"` only for the outro), `SHOTLIST.md`, `coverage.json` (capture hashes, `method: scripted-input`, input logs), `gamedev-evidence.json` (`teaching_contract: code-then-result-v1`, verbatim excerpts with line ranges), `COMPONENTS.md`, `RIFF.md`, `PROMPTS.md`, `BUILD-PROMPT.md`, film `SOURCES.md`; cut `media/Bxx.mp4` clips deliberately (no compiler retiming) and the SLICE AUDIO `audio_file`s from the same takes and intervals.
3. Kokoro narration, Remotion pilot via `runtime/scripts/remotion_scenes.py`, `./art godot-gamedev --check REEL --game <project>`, then `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`; watch and listen to the master; `_qc/REPORT.md`.
4. README "Film" section and a new `SUBMISSION.md` (no full name): title, course media link (the author uploads), filename `claude-liam-walker-magic-gamedev.mp4` (or the actual export name), SHA-256, resolution, duration, game revision shown. Remove the film items from `TODO.md`.
5. ~~Open author checks in `SOURCES.md` → Image prompts~~ — answered 2026-10-07 and logged there (all sent unchanged; CHAR-RUN v1 draft and the ENEMY-WOLF-DOWN v3 chat not remembered; origins of the four images without their own prompt recorded). Nothing left to ask.
6. FRICTIONAL: add a Claude Code session entry for the film work and a pushes row.
7. Known open engine issues: "2 resources still in use at exit" for MUS-LOOP.ogg; why the S6 import stalled; the capture-copy import segfault.

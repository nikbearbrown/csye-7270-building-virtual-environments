# Build The Smallest Shader

Read the lecture skill at `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/skills/make/lecture/SKILL.md`, this film's ACTS, SHOTLIST, FACTCHECK, SOURCES, CHECKS-REPORT and the shared REVIEW. This is a local film build, never a publication. Do not change the narration or source shader to make a gate pass.

Prepared: complete 14-beat sheet, narration, registered ShaderLab and bookend scenes, actual Godot capture, source excerpts and hash-linked evidence. No new scene registration is needed. The source snapshot is preserved. No audio or master has been built.

Run from books/ in this order:

```bash
python3 '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/install_assets.py'
python3 '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/generate_audio_kokoro.py' '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader'
python3 '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/lock_audio.py' '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader'
python3 '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py' --out '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader/opening' --sheet '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader/beat_sheet.json' --width 3840
```

Copy the generated video-only opening MP4 into `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader/media/BOPEN.mp4` (the title builder emits its measured-duration filename). Before any long render, render low-resolution component stills at 15/50/85 percent, inspect every frame, and log layout findings. The body uses the registered ShaderLab component. All excerpts are actual source. B05's 16-second capture MUST play completely; its audio is padded to at least 16 seconds by lock_audio.py. If narration exceeds the capture, use a freshly captured longer version with the same controls, not a freeze or a loop of an irreversible parameter change. Reposition B05's visual transition relative to the voice only through a documented capture timing change; do not imply that unsynchronized audio has been checked.

Align code highlight cues with actual spoken references after generating word timestamps. Preserve source code and the authored explanation. The original Godot caption remains inside the capture; confirm it clears type limits at final size. Use larger source crops or the full-width layout if needed, without hiding evidence. Ordinary code strings are code, not improperly typeset equations.

```bash
./brutalist.art/art run '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader' --height 2160
./brutalist.art/art final '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader' --height 2160 --out '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader/exports/landscape'
python3 '/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/bookend_check.py' '/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-the-smallest-shader'
```

Run every normal gate including factual, static, layout, visual, type and sharpness checks. Inspect the master, not just its file probe. Hear/transcribe the opening, scientific terms and ending; verify the explicit silence, no truncation, and exact title/handle. Required values: 3840×2160, measured audio clock, no unresolved placeholders, one-second silent outro tail. No paid services and no gate bypasses.

Only 25 GiB was free during preparation: check free space before each film and build serially. Do not delete other files or interfere with the Wikipedia build. Do not stage, push or publish. Report the exact final path and measured runtime only after the master and all applicable gates pass; otherwise report the precise incomplete gate.

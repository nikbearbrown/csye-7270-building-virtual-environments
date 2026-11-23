# The Little Flame Witch — final project pitch

**Zhefan Zhang** (zhefan-z) · CSYE 7270 Fall 2026 · Assignment 8

- **Working title:** The Little Flame Witch
- **What it will be:** an HD-2D cave action game, delivered as a playable Windows desktop build (an .exe in a zip): two to three short levels from title screen to end screen, the last one a great-wolf boss.
- **Target role:** gameplay programmer. **Reader:** a hiring manager or lead gameplay programmer.
- **Runtime:** Godot 4.7.2-stable, GDScript, Forward+ (Vulkan), Windows desktop export. The game that exists today is `walker-magic-zhefan` at `840b501` (branch `zhefan-z/assignment-7`).

## The film

*The Little Flame Witch — pitch*, 3:46 (225.97 s), 3840×2160, 30 fps, narrated by Liam (AI) speaking as me.

- **Link:** https://drive.google.com/file/d/1FofpFGRxPnT_dhhwQYjBPuAhT20T7s20/view?usp=sharing
- **File:** `zhefan-z-little-flame-witch-pitch.mp4` (40,175,652 bytes)
- **SHA-256:** `970b0be3a9b8e61809e91f493882b23c5fbc6aa53731400b4cdcfc16385af843`
- **Gates:** the walkthrough checker passes; the final export's render-integrity gate passed on 62 sampled frames with no blockers and no majors (`_qc/`).
- **Labels:** every frame is marked real (with its revision), generated (Gemini 4) or constructed. Real footage is scripted-input capture of my game at `840b501`, plus earlier captures at `2b68e0a` and `3c37fe0`.

**Which version of the assignment.** Canvas shows the original Assignment 8 text (2–4 minutes, the seven questions). The course repository's updated version (commit `135fc9d0`, 2026-11-20) builds the film from a GDD and adds the game in brief, the sixteen GDD beats and the appendix, with no fixed length. This submission meets both: the film is under four minutes and gives every part of the updated version its own beat; the full detail is in `GDD.md` and `PROJECT-BRIEF.md`.

## What is in this folder

| File | What it is |
|---|---|
| `GDD.md` | The game design document the film is built from (version 2.0, 2026-11-21), including art and sound; updated from my Assignment 4 GDD (`A4-GDD.pdf`) |
| `PROJECT-BRIEF.md` | The game in brief, the seven answers, and the appendix with the asset table, ending with **exists today** and **will exist** |
| `beat_sheet.json` | The narration and visual plan |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, and every third-party item with its licence |
| `ART-PROMPTS.md`, `art/` | The generated concept portraits and how they were made |
| `_qc/` | The toolkit's gate reports |
| `FRICTIONAL.md` | Dated entries as I worked |
| `CAPTURE.md`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `coverage.json`, `scripts/`, `capture/` | The capture record, the claim-by-claim fact check, the shot list and the build scripts |

The MP4, the narration audio and the rendered media are kept out of git.

## How to rebuild the film

`BUILD-PROMPT.md` gives every prompt and command, in order. In short: take a `git archive` snapshot of `840b501`, run the scripted-input captures with the drivers in `capture/`, generate the narration locally with the toolkit's Kokoro voice (Liam), build the stills and footage with the scripts in `scripts/`, run the walkthrough checker, then the toolkit's final export with its render-integrity gate. Everything runs locally and free (Brutalist toolkit, `https://github.com/nikbearbrown/brutalist.art`).

## Tag

No `a8` tag: the course repository is shared, and per the instructor (2026-10-09) per-student tags are not used. The submitted commit is named in the Canvas note.

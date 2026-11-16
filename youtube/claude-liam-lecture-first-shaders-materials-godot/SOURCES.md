# SOURCES.md — Your First Shaders and Materials with Claude and Godot

## Source
The film is built from one document: **Assignment 5, "Shaders, Materials, and the Godot Shading Language"** for CSYE 7270 (Virtual Environments and Real-Time 3D, Nik Bear Brown, Northeastern University, Fall 2026, 100 points): `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/assignments/05-shaders-materials-and-godot-shading-language.md` (byte-identical to `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/assignments/course-briefs/05-shaders-materials-and-godot-shading-language.md`; copy: `evidence/example/sources/assignment-05.md`). Professor Bear asked for a film that walks people through this assignment using his project as the evidence, as the two Assignment 3 films do. The whole document is covered; what the film leaves out, and why, is in `ACTS.md`.

## The worked example (the evidence)
`/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/` (Godot project `godot/`, the course lab `godot/course-series/`, the original Signal Garden `godot/signal-garden/`, its notes and evidence). It is an **instructor example written by an AI (Codex) under Professor Bear's direction**: the shaders, materials, tests, driver, audit, language notes and captures. It is not student work, not hand-written, and no Claude Code session produced it (its own CLAUDE.md, CHANGE-BRIEF, TEST-REPORT and FRICTIONAL say so). Frozen copies of every source file the film shows: `evidence/example/sources/` (+ `SHA256SUMS.txt`). Git facts read (read-only): the change brief was committed in `93be391` (2026-10-14 00:29:13 -0400) with no shader file; shaders first appear in `48c6177` (2026-10-16).

## Primary sources checked
- The assignment's own text (every prompt, the wrapper, the mutation steps, the hint experiment, the curl check, the table of agent mistakes, the Use It table, the rubric).
- Godot 4.7.2.stable.official.ed1daf0bf, run on 2026-10-16 on an Apple M4 Pro: `evidence/runs/` (wrapper, three real-file mutations, the exit-code demonstrations, the hint experiment and the pad values in Forward+ and Compatibility, a constant-colour probe) and `captures/forward-plus/`. Full numeric table: `evidence/EVIDENCE-NOTES.md`.
- The example's own earlier recorded runs of 14 Oct 2026: `evidence/example/` (the first failing driver run, exit 124; the first material test with four failures; mutation logs; controlled predictions; native captures `captures/example-native/`; the conversion receipt; the fresh-cache run).
- Poly Haven "Stone Floor" (Dimitrios Savva, CC0; https://polyhaven.com/a/stone_floor), the `_nor_gl` and `_nor_dx` 1k PNGs, md5 verified against Poly Haven's manifest (`evidence/example/polyhaven-ATTRIBUTION.md`, `polyhaven-files.json`): used only to calibrate the normal-map check.
- Godot documentation (docs.godotengine.org, stable): shading language, spatial shader reference, `Image`, texture import settings, `Environment.TONE_MAPPER_*`.
- The real Godot editor frames, if the editor agent produced them: `evidence/editor/EDITOR-NOTES.md` and `captures/editor/`.

## What was NOT run, and is labelled so on screen
- No Claude Code session: the assignment's prompts (context file, driver, audit, `claude -p` commands, the clean-clone recipe) appear as the assignment's text, "documented, not run".
- No human played the game, listened, or approved anything. The in-play frames are scripted physical-key input (`captures/lab/receipt.json`).
- No operating-system screenshot was compared with an engine capture (the assignment asks students to).
- The Compatibility renderer's 3-5 byte shortfall on dark colours has no known mechanism (a probe for this film narrowed what it is not).
- The example's specimens are plain boxes made in code: the importer's Use External setting is not used. Its materials use no normal map.

## Credits
Narration: Liam, in for Bear (Kokoro, `am_onyx`, free, local). Drawings and layouts: Manim and Remotion from the Brutalist toolkit (Claude palette); logos from `brutalist.art/icons/logos/`; the Professor Bear portrait from `brutalist.art/professor-bear/`. Godot is MIT; Poly Haven assets are CC0. No third-party footage, audio or models.

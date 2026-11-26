# SOURCES — final project pitch

What the pitch film and this folder used, what I made, what Claude contributed, and the third-party assets with their licences. The full generation log of the game's assets (model, prompt, seed and decision for every generation) is in my earlier SOURCES: `assignment-7/walker-survival-shooting/SOURCES.md`. This file lists what this pitch uses and what appears on screen.

## 1. How the film was made (tools and models)
| What | Version | Used for | Licence |
|---|---|---|---|
| Brutalist toolkit (provided by the course) | local checkout, commit 22264a3 (not updated to the latest) | the show-tell drawing kit, assembly, all quality gates | course toolkit; its repository has no separate licence file |
| Manim Community | 0.18.1 | the 10 drawn beats | MIT |
| Remotion | the version in the toolkit | the closing name card (ShowTellCard) | Remotion License (free for individuals) |
| Kokoro, local, voice am_onyx | kokoro-v1.0 ONNX | the narration | Apache 2.0 |
| Godot Movie Maker | Godot 4.7.2-stable | the game footage (scripted input) | MIT |
| Microsoft Edge, headless | as installed with Windows | screenshots of the README key table and the test-log page | system software |
| ffmpeg | 9.0.2 | cutting, labels, encoding | LGPL / GPL |
| Fonts | EB Garamond and Lato (shipped with the toolkit); Segoe UI and Consolas (Windows system fonts, only in the two document frames) | on-screen text | EB Garamond, Lato: SIL OFL; Segoe UI, Consolas: supplied with Windows |

No paid generation service, no API keys, and nothing uploaded to a generation service.

## 2. What I did
- Chose the project direction and the target role, answered the seven questions, and named the comparable games with my own observations (all games I have played).
- Reviewed the 19 beats one by one: what each says, the examples, which sentences to cut; listened to the English voice and approved the pronunciation.
- Decided that Claude would record the footage, that the narration mentions only the landing dust, and that the drawings use the show-tell isometric style.
- Watched the finished film and approved it (2026-11-26).
- The game's design (the tablet system, the clue-chaining memo, the key rules) is mine.

## 3. What Claude (Claude Code, Claude Opus 5.5) contributed
- Sorted out the exists / will-exist lists; drafted PROJECT-BRIEF, README and the beat sheet in Chinese for my review; translated the narration and the documents into English.
- Wrote the capture scripts (`film-scripts/capture/`) and recorded all game footage from a copy of commit f13431bf; wrote the script that lays out the document frames.
- Wrote the 10 Manim scenes and the reel scripts (`make_sheet.py`, `finish_audio.py`, `prepare_media.py`), ran the toolkit's gates and fixed what they flagged.
- Wrote FACTCHECK, SHOTLIST, PROMPTS, CAPTURE and BUILD-PROMPT.
- Its mistakes and their corrections are recorded in `../FRICTIONAL.md`.

## 4. Game assets on screen (commit f13431bf)
| Asset | Source | Licence / rights |
|---|---|---|
| Main character model and rig (`main_character.glb` and its textures) | commissioned from a friend, built from my character design; I posed the animation key poses and Claude made the in-between frames in Blender | copyright belongs to me (the commissioning party); not for use outside this project; see `assets/characters/main_character/ATTRIBUTION.md` |
| Pixel head (taskbar) | generated with Codex (OpenAI) from my prompt, edited by Claude | OpenAI Terms of Use: the output belongs to the user; shared content is marked as AI-generated; see `computer_system/tablet_os/system/pixel_head/ATTRIBUTION.md` |
| Chair, computer desks, crates, tablet model | built by Claude Code in Blender from basic shapes (counted as generated assets; logged in Assignment 3) | my project's assets |
| Crate metal texture Metal041C | ambientCG | CC0 |
| Tablet OS font Noto Sans CJK SC | Google / Adobe | SIL OFL 1.1 (licence file next to the font) |
| Drive and folder icons in This PC (placeholders) | a copy of the Godot engine icon (`icon.svg`) | Godot logo by Andrea Calabró, CC BY 4.0 |
| Game engine | Godot 4.7.2 | MIT |

## 5. Comparable games
The film names Metal Gear Solid V: The Phantom Pain, Subnautica, Abiotic Factor and Escape from Tarkov, with only their names and my own observations from playing them. **No screenshot, footage, music or asset from these games is used**; the "menu tablets" in the drawings are Claude's diagrams.

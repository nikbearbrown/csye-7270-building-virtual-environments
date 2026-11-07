# SUBMISSION — CSYE 7270 Assignment 2

| Field | Value |
|---|---|
| **Assignment** | Assignment 2 — Generate Art, Sound, and Music for Your Game |
| **Student** | zhefan-z (the course rule forbids full names in the repository) |
| **Project name** | walker-magic |
| **Game concept in one sentence** | A young fire mage descends through a dark cave, carrying the only warm light in it at the tip of her staff, and fights past wolves and pits by aiming fireballs with the mouse. |
| **GitHub repository / folder** | Branch: https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/zhefan-z/assignment-2/fall-2026/zhefan-z/assignment-2/walker-magic-zhefan · Pull request: https://github.com/nikbearbrown/csye-7270-building-virtual-environments/pull/6 · Permalink at the submitted commit: in the Canvas note (see the next row) |
| **Started from** | An empty Godot 4 project created for this assignment (not the walker-jumpman starter); the design documents were committed before any generation (`7371b25`). |
| **Submitted commit SHA** | Given in the Canvas submission note, with the folder permalink at that commit. A commit cannot contain its own SHA, so it cannot be written in this file. It is the head of `zhefan-z/assignment-2` when this file was pushed. |
| **Source revision shown in the film** | `74c0443` (the tested build: fresh-copy check, playtests 5 and 6). Gameplay was captured from `5266946`, whose runtime files are identical to `74c0443` (only `assets/audio/MUSIC-EDIT-LOG.md`, a text log, differs). |
| **Revisions compared** | `74c0443` (shown in the film) and the submitted commit (Canvas note): no runtime file differs (`game/`, `features/`, `audio/`, `ui/`, `assets/` media and import settings, `project.godot`, `default_bus_layout.tres`). What changed after `74c0443`: documents and logs (README, SOURCES, TEST-REPORT, TODO, HANDOFF, this file, `assets/audio/MUSIC-EDIT-LOG.md`, `design/IMAGE-PROMPTS-from-chat.md`), the in-engine evidence images in `design/checks/engine/`, the film's records in `youtube/`, and two non-runtime tool files: `tests/capture_scene.gd` (the evidence-screenshot helper; not one of the six test suites) and one log string in `tools/make_music_loop.py`. |
| **Godot version and OS** | Godot 4.7.2-stable (official, win64, `ed1daf0bf`), Vulkan Forward+, on Windows 11 Home (build 26200) with an NVIDIA GeForce RTX 5060 Laptop GPU. |
| **Final film URL** | https://drive.google.com/file/d/1n5IhEftLCKWkrGQrS5hVRhfr4IQRG8Ut/view?usp=sharing |
| **Final film filename** | `claude-liam-walker-magic-gamedev.mp4` — "Her Fire Is the Only Warmth: Building a Cave Mage Slice"; 3840x2160, 30 fps, 344.333 s (5 min 44.3 s), 44,430,567 bytes |
| **Final film SHA-256** | `aec3d57dba3d057b4fb5f944a37d4d9c34f31e181743fcbf617068e8f9442eff` |

## Generative models used

| Model | Version (as shown) | Where it ran | License / terms | Used for |
|---|---|---|---|---|
| Google Gemini (Gemini app, image generation) | model shown in the app: Gemini 3.8 Flash | Google, in the Gemini web app | Google Terms of Service and Generative AI Additional Terms; outputs carry SynthID | Every generated image: mage poses, wolf, fireball and burst, cave background, ground tiles |
| Google Lyria (music generation in the Gemini app) | Gemini 3.8 Flash shown in the app; the Lyria version was not shown | Google, in the Gemini web app | Google Terms of Service and Generative AI Additional Terms; SynthID | The music loop MUS-LOOP |
| Stable Audio Open 1.0 | `model.safetensors` at commit `f21265c1e2710b3bd2386596943f0007f55f802e` | Locally, in ComfyUI v0.38.1 | Stability AI Community License (non-commercial coursework). **Powered by Stability AI.** This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved. | The five sound effects |
| T5-base (text encoder for Stable Audio Open) | commit `a9723ea7f1b39c1eae772870f3b547bf6ef7e6c1` | Locally, in ComfyUI | Apache-2.0 | Text conditioning for the sound effects |
| Suno | v4.5-all and V6 Preview | Suno web app (free plan) | Suno Terms of Service | Tried for the music and rejected; nothing used |
| Claude (Anthropic) via Claude Code | Claude Opus 5.5 (as in the commit trailers) | Claude Code desktop app on this PC | Anthropic terms of service | Code, tools, tests, documents, the capture harness and the film build |
| Claude (Anthropic) via claude.ai | model version not recorded | claude.ai | Anthropic terms of service | Design discussion and document drafts, the image prompts I sent to Gemini, code-drawn SVG blockouts, the rejected-image thumbnails |
| Kokoro-82M (kokoro-onnx), voice `am_onyx` | `kokoro-v1.0.onnx` | Locally, Brutalist toolkit | Apache-2.0 | The film's narration (Liam, in for Bear) |

Full versions, hashes, prompts, accepted and rejected outputs and every edit: `SOURCES.md`.

## Summary of my work

*(Drafted by Claude Code from `../FRICTIONAL.md` and the commit history; the decisions listed are the author's.)*

- I chose the game (a run-and-gun with a fire mage instead of a soldier, mouse aiming), the enemies and HP, and the character's look, and kept the design original (no copyrighted character). The four design documents were committed before any generation.
- I generated every image in the Gemini app from prompts drafted with Claude, accepted or rejected each output with a reason (CHAR-CAST took four attempts; a context-bleed round of wolves was abandoned), and picked one of three Stable Audio Open seeds for each sound and the Lyria track for the music after rejecting Suno.
- I set the slice scope (CHANGE-BRIEF Revision 2), approved each build step S1–S8, and played six playtests, which drove the changes recorded in TEST-REPORT.md; I confirmed the music level and the loop seams by ear.
- Palette revision 1 is the cause-and-effect case: the predicted failure (dark stockings, boots and brim vanishing on the cave) was observed and fixed by lifting those colours one value step.
- For the film I approved the beat sheet, script, title and the four scripted-input takes, obtained the instructor's verbal approval of the SLICE AUDIO method, and watched and listened to the whole master before uploading it.
- Claude Code wrote the Godot code, the cleanup and audio tools, the 73 headless checks, the capture harness and the film build; Claude in claude.ai drafted the prompts and documents with me.

## Known limitations

- **Slice scope:** no boss (storyboard P6), heal spell, spikes, stalactites or title screen (CHANGE-BRIEF Revision 2).
- **Art:** the HUD uses Godot's smooth built-in font; the fixed 14x44 collision box covers part of the head in RISE and FAIL; the wolf's down image keeps the lunge legs; the hurt pose does not lean back. The exit, hearts, crosshair and pit fill are code-drawn, not generated.
- **Engine:** closing the game prints "2 resources still in use at exit" for `MUS-LOOP.ogg` (cause not found); why the project's first import stalled during S6 is unknown; on Godot 4.7.2 a first import of the film's capture copy with the capture scripts present crashed at shutdown (worked around with a two-step import, film tooling only).
- **Tests:** the headless checks run on a dummy audio driver, so they prove sound triggers, not what is heard; audibility comes from playtests 5 and 6 and the capture audio levels.
- **Records:** two prompt details are not remembered (which CHAR-RUN v1 draft was sent; which chat ENEMY-WOLF-DOWN v3 was sent in); the claude.ai model version was not recorded; the Lyria version was not shown. Two Python bytecode caches (`tools/__pycache__/*.pyc`) committed early on were removed from the repository at submission, and `__pycache__/` and `*.pyc` are now in the project's `.gitignore`; they remain in the history of earlier commits, including `74c0443`.
- **Film:** gameplay is scripted-input capture, not a playtest; the outro card is silent because the toolkit copy has no stock jingle; B25's narration adds the skill's sign-off "Liam, in for Bear." to the approved script; the film's run-02 reload and the run-04 pause take were recorded but not used.

# walker-survival-shooting — final project pitch

- **Author:** Zhe Liu
- **Working title:** walker-survival-shooting
- **Target role:** technical game designer
- **In one sentence:** the player uses the apps on a military tablet they carry, above all a memo app, to sort out clues and work out quests; and while the tablet is open, the world does not stop.
- **What exists and what will exist:** see [PROJECT-BRIEF.md](PROJECT-BRIEF.md).

## Runtime
- **Engine:** Godot 4.7.2-stable, Forward+ renderer (D3D12 on Windows), Jolt physics, GDScript.
- **Export target:** Windows desktop. **There is no exported build yet**; for now the project runs from Godot 4.7.2.
- **Where the project is:** `assignment-8/walker-survival-shooting/godot/` in this repository; the film uses commit `f13431bf`. This copy has its code comments removed (the original comments are in Chinese).
- **Machine for the measured numbers:** NVIDIA GeForce RTX 5070 Ti Laptop GPU.

## How to run
1. Install Godot 4.7.2-stable (Windows).
2. Import once first (this generates the translation files; a few errors about a missing `.translation` file at the start are expected):
   `godot --headless --path assignment-8/walker-survival-shooting/godot --import`
3. Run: `godot --path assignment-8/walker-survival-shooting/godot`, or open the project in the editor and press F5.

## Keys
The game shows no key hints, so please read this table before you start.

| Key | What it does |
|---|---|
| W A S D | Walk |
| Shift | Run |
| Space | Jump |
| Mouse move | Turn the camera |
| Right mouse button (hold) | Aim view |
| Tab (short press) | Tablet stowed: raise it in one hand (a small window appears bottom right). One hand: put it away. Two hands: back to one hand |
| Tab (long press, about 0.4 s) | Tablet stowed or in one hand: hold it in both hands, close to the eyes. Two hands: put it away |
| Left mouse button | While holding the tablet: click things on it (double-click an icon or a folder to open it) |
| F | Wall switch: lights on / off (standing at the switch, tablet stowed) |
| Esc | Release the mouse |
| V | Debug: toggle vsync |

**Two design rules:** with the tablet in both hands, the character cannot walk, and every key goes to the tablet; with it in one hand, the keys only control the character.

## Try it (the first 60 seconds)
1. After the game starts, press Tab: the character raises the tablet in one hand, a small tablet window appears bottom right, and the screen lights only once the tablet is in place.
2. Long-press Tab: two hands, and the camera moves close to the tablet.
3. Double-click the "This PC" icon, then a folder inside it; click Up, minimize, the taskbar button, and "Show desktop".
4. With two hands, hold W: the character does not move. Short-press Tab for one hand, hold W again: the character walks.

## Film
- **Link:** https://youtu.be/28eK10Vvqo4 (the MP4 is not in GitHub)
- **File name:** `walker-survival-shooting-pitch-1080p.mp4` (1920 × 1080, 210.9 s; not in git)
- **SHA-256:** `4ab1cd281cbb0afe7f93d5a4129e047a2b6885d6ce32f2261ca65cb577edf980`
- **Footage:** all game footage is **scripted input recorded frame by frame with Godot Movie Maker**, not human play; every clip is labelled SCRIPTED INPUT and commit `f13431bf` on screen. Drawings are labelled CONSTRUCTED, and designs that are not built yet are labelled PLANNED / WILL. The capture method and the problems found are in [CAPTURE.md](CAPTURE.md).
- **Narration:** AI voice (local Kokoro am_onyx); I wrote the script, and it speaks as me.

## How to rebuild the film
See [BUILD-PROMPT.md](BUILD-PROMPT.md). The film scripts and capture tools are in `film-scripts/`.

## What is in this folder
| File | Contents |
|---|---|
| README.md | This file |
| PROJECT-BRIEF.md | The answers to the seven questions, and the "exists today" and "will exist" lists |
| beat_sheet.json | Each beat's narration and visual plan |
| BUILD-PROMPT.md | The prompts and commands that rebuild the film |
| FACTCHECK.md, SHOTLIST.md, PROMPTS.md, CAPTURE.md | The film's claims and sources, shot list, prompts, and capture record |
| film-scripts/ | The reel scripts (`scenes.py`, `make_sheet.py`, `finish_audio.py`, `prepare_media.py`) and the capture tools with their logs |
| SOURCES.md | What I used, what I made, what Claude contributed, third-party assets and licences |
| gate-reports/ | The toolkit's gate reports: Gate B layout audit, Gate V visual QC, Gate T type check, bookend and fact-check gates, run and final logs, the verified-master record |
| FRICTIONAL.md | In `assignment-8/FRICTIONAL.md` |

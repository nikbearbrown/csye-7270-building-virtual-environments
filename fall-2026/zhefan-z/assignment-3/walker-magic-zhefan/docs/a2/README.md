# walker-magic — CSYE 7270 Assignment 2 asset slice

A young fire mage carries the only warm light down into a dark cave. This repository folder holds the design documents, the generated art, sound and music, and a small playable Godot slice that proves those assets work together in the engine.

## What it started from
- An empty Godot 4.7 project created for this assignment (not the walker-jumpman starter). The design documents were written first (`CONCEPT.md`, `STORYBOARD.md`, `CHARACTER-SHEET.md`, `CHANGE-BRIEF.md`), then the assets were generated, then the slice was built.
- The code layout (`features/`, `game/`, `ui/`, `tests/`) and the headless test style (one JSON line per check, `WALKER TESTS: N checks / F failures`) follow my Assignment 1 project, which started from [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman).
- Built with Claude Code using the course's Walker workflow: brief → build → playtest → inspect → revise. Who decided what is in `../FRICTIONAL.md`.
- Original commit history: `zhef-z/walker-magic-zhefan` (frozen at `920d969`); see `SOURCES.md` → "Original commit SHAs".

## Engine
Godot **4.7.2-stable** (win64). 640x360 viewport, integer-scaled into a 1280x720 window, nearest-neighbour filtering.

## Run
From this folder:

```
Godot_v4.7.2-stable_win64.exe --path .
```

or open `project.godot` in the Godot editor and press **F5**. The first run imports the assets (a few seconds).

## Controls
| Input | Action |
|---|---|
| A / D or ← / → | Move |
| Space, W or ↑ | Jump (hold for a full jump, tap for a short hop) |
| Left mouse button | Cast a fireball toward the crosshair (0.35 s cooldown; holding does not repeat) |
| Esc | Pause / resume |
| **M** | Mute / unmute music |
| **N** | Mute / unmute sound effects |
| R | Play again (on the Cleared screen) |

## What the slice demonstrates
About two screens of cave: the start, one narrow pit, one wolf, the exit.
- **Character states** (one static image per state, swapped on state change): idle, run, rise, fall, cast, hurt, fail (pit: fall image; HP 0: kneeling image), win. Facing follows movement and turns toward the cursor when casting. The 14x44 collision box matches `CHARACTER-SHEET.md`.
- **Environment:** the generated cave background fixed to the camera, generated ground tiles with pit edge caps.
- **Enemy and FX:** one wolf (patrol, growl telegraph, lunge, 2 HP, white hit flash, down image, then gone); fireball and burst.
- **Five sound events on real game events**, each one sound per occurrence: SFX-CAST, SFX-WOLF-DOWN, SFX-HURT, SFX-FAIL, SFX-CLEAR. Game code emits signals and an audio node plays the sounds; sound never decides game state.
- **Music:** MUS-LOOP repeats without a click; it pauses with Esc and resumes from the same point, stops on a fail (restarts from the top on reload) and stops at the exit.
- **Readable muted:** hit flash, hurt image, blink and hearts, fail text, Cleared screen.

Generated assets used in the slice: mage poses, wolf, fireball and burst, cave background and ground tiles (Google Gemini app, model shown in the app: Gemini 3.8 Flash); five sound effects (Stable Audio Open 1.0, run locally); the music loop (Google Gemini app, Lyria). Every model, version and license, every edit and rejected output, the music prompt and the image prompts (drafted by Claude, sent by the author in the Gemini app; collected in `design/IMAGE-PROMPTS-from-chat.md`) are in `SOURCES.md`. All image prompts were sent unchanged; two details the author does not remember (which CHAR-RUN v1 draft was sent, and which chat ENEMY-WOLF-DOWN v3 was sent in) are marked there.

## Tests
From this folder, each prints `WALKER TESTS: N checks / 0 failures` and exits 0 on success:

```
Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_sound_triggers.gd
```

Also `test_player.gd`, `test_cast.gd`, `test_wolf.gd`, `test_flow.gd`, `test_audio.gd` (73 checks in all). Results and the human playtests: `TEST-REPORT.md`.

## Known limitations
- Storyboard P6 (boss) is not in the slice, nor are the heal spell, spikes, stalactites and the title screen (CHANGE-BRIEF Revision 2).
- The HUD uses Godot's smooth built-in font, which clashes a little with the pixel art.
- The fixed collision box covers part of the head in the RISE and FAIL poses.
- The exit, HP hearts, crosshair and the dark pit fill are code-drawn, not generated.
- Closing the game prints a harmless "resources still in use at exit" message for the music file.

Full list: `TEST-REPORT.md` → Known limitations.

## Film
**Her Fire Is the Only Warmth: Building a Cave Mage Slice**, made with the course's Brutalist `godot-gamedev` skill and the `walker` modifier.

| | |
|---|---|
| Link | https://drive.google.com/file/d/1n5IhEftLCKWkrGQrS5hVRhfr4IQRG8Ut/view?usp=sharing (anyone with the link can view) |
| File | `claude-liam-walker-magic-gamedev.mp4` |
| SHA-256 | `aec3d57dba3d057b4fb5f944a37d4d9c34f31e181743fcbf617068e8f9442eff` |
| Format | 3840x2160, 30 fps, H.264 + AAC 48 kHz stereo; 5 min 44.3 s (344.333 s); 44,430,567 bytes |
| Game source shown | `74c0443`; gameplay captured from `5266946`, whose runtime files are identical |

Gameplay in the film is scripted-input capture (real input events through Godot Movie Maker, each take checked against a headless run), labelled as such; it is not a playtest. The SLICE AUDIO segments carry the game's own sound from the same take with no narration (verbal approval from the instructor the method is acceptable). Reel records: `youtube/claude-liam-walker-magic-gamedev/` (`SCRIPT.md`, `SHOTLIST.md`, `CAPTURE.md`, `FACTCHECK.md`, `gamedev-evidence.json`). The MP4 and the captures are kept out of GitHub, as the course requires.

## Documents
| File | What it is |
|---|---|
| `CONCEPT.md`, `STORYBOARD.md`, `CHARACTER-SHEET.md`, `CHANGE-BRIEF.md` | Design, written before generation; later changes appended as dated revisions |
| `SOURCES.md` | Every tool and model, versions, licenses, prompts, accepted and rejected outputs, the asset log |
| `TEST-REPORT.md` | Automated checks and human playtests against the assignment's test table |
| `SUBMISSION.md` | The submission fields: revisions, models, film link and SHA-256, known limitations |
| `assets/sprites/EDIT-LOG.md`, `assets/audio/EDIT-LOG.md`, `assets/audio/MUSIC-EDIT-LOG.md` | Every edit to the generated art and audio |
| `../FRICTIONAL.md` | Work log (in the course folder, next to this project) |

## Attribution
Sound effects: **Powered by Stability AI.** This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved. (Stable Audio Open 1.0; coursework, non-commercial.)

Images and music generated in the Google Gemini app carry Google's invisible SynthID watermark.

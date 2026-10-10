# walker-survival-shooting

CSYE 7270 · Fall 2026 · Assignment 2 — Generate Art, Sound, and Music for Your Game · Zhe Liu

A third-person 3D extraction shooter: the player is a survivor who lives in a subway under a ruined city and carries a rugged military tablet; each run they go out, fight monsters, scavenge, and extract. The asset slice for this assignment takes place entirely inside the subway base.

> **Status: incomplete submission.** The design documents, the asset log, the accepted sound effects, and a greybox of the subway base are done. The playable asset slice (controllable character, state images, sounds on real events, music loop, mute) has not been built yet. See "Known limitations".

## Started from
An empty Godot 4 project that I created in Godot 4.7.2-stable (Windows). No code or assets from walker-jumpman or from my Assignment 1 project.

## Engine
Godot 4.7.2-stable (Windows), Forward Plus renderer, Jolt Physics, D3D12.

## How to run
1. Open `godot/project.godot` in Godot 4.7.2.
2. Open `base.tscn` and press **F6** (Run Current Scene). No main scene is set yet, so F5 will ask you to choose one.

## Controls
None yet. There is no player character, so there are no movement controls and no mute controls.

## What the current version demonstrates
- `godot/base.tscn` — the subway base greybox (asset log row ENV-BASE-01): a closed 16 × 10 m room, 3 m high, with a staircase up to a platform, two cool ceiling lights, and a preview camera.
- `godot/assets/furniture/test_chair.glb` — a low-poly test chair (ENV-SEAT-TEST-01).
- Both were built by Claude Code from basic shapes. The professor confirmed to me that assets built this way count as generated assets; note that the written assignment text says code-drawn art does not satisfy the generative-model requirement.
- `design/sfx_sound/` — three accepted terminal UI sound effects generated with Stable Audio 3 Small SFX (power on, power off, button press), as FLAC. They are not in the Godot project yet.

## Repository layout
| Path | Contents |
|---|---|
| `CONCEPT.md` | Concept, core loop, pillars, art and audio direction |
| `STORYBOARD.md`, `design/storyboard/` | 10 panels; sketches for panels 1–5 |
| `CHARACTER-SHEET.md`, `design/character/` | Character specification; turnaround and extra reference views |
| `CHANGE-BRIEF.md` | Asset list, event-to-sound map, music behavior, predicted failures |
| `SOURCES.md` | Models, licenses, tools, contributions, and the asset log with exact prompts |
| `design/rejected/` | Thumbnails of rejected outputs |
| `design/pad/` | Reference images for the rugged tablet |
| `TEST-REPORT.md` | What was checked and what was not |
| `godot/` | The Godot project |
| `youtube/claude-liam-walker-survival-shooting-gamedev/` | Source, script, and evidence for the explainer film (no media) |
| `../FRICTIONAL.md` | Design log |

## Known limitations
- No controllable character and no in-game state images. The 10 poses, the silhouette test image, and the collision overlay image described in `CHARACTER-SHEET.md` have not been made.
- The sound effects are not connected to game events, are not converted to OGG yet, and the error sound is not final (four events are designed; three are accepted).
- No music has been generated.
- No mute controls.
- Storyboard panels 6–10 have text but no sketches.
- Most checks in `TEST-REPORT.md` could not be run because there is no playable slice.

## Final film
- **Title:** Walker Survival Shooting, Before the Slice (Brutalist `godot-gamedev`, walker mode; narrated by Liam, local Kokoro `am_onyx`)
- **File:** `claude-liam-walker-survival-shooting-gamedev.mp4` · 3840 × 2160 · 30 fps · 6:53
- **SHA-256:** `2cde5517c1f96affd17101d9ba1718bc7b689fcc60cdaa16cec5b9c991123e0a`
- **Media link:** to be added after upload to the course media storage (the MP4 is not in GitHub)
- **Source revision shown in the film:** `f848d84`
- **Film source and evidence:** `youtube/claude-liam-walker-survival-shooting-gamedev/` (beat sheet, script and prompts, component/evidence ledger, fact check, capture method, checks)
- **What the film can and cannot show:** there is no playable slice, so the film shows the design documents, the asset log, native 4K Godot renders of the greybox, and the accepted sound files played back and labeled "not in-engine". It does not show the character in two states or the four sound events in real play, because they do not exist yet.

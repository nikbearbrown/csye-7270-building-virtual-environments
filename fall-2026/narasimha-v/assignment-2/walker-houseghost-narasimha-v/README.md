# HOUSEGHOST

> You are the ghost. They are the new family. The house remembers what everyone agreed to forget.

**Project:** `walker-houseghost-narasimha-v` · CSYE 7270 Assignment 2 — Generate Art, Sound, and Music for Your Game
**Author:** Narasimha Reddy Valam · **Engine:** Godot **4.7.2.stable** (GL Compatibility) · **Built on:** macOS, Apple Silicon
**Started from:** an empty Godot 4 project. The world-inversion verb is carried forward as an *idea* from my Assignment 1 game, [walker-jumpman-narasimha-v](https://github.com/narasimhareddyvalam/walker-jumpman-narasimha-v); no code, scenes, or assets are reused.

You play the ghost of a boy the world believes ran away, in the bedroom a new family has just emptied out. Flip between the room as they see it — stripped, grey, boxed up — and the room as you remember it, upside down and lamplit, to reach across and be seen. Every contact tears a day off the calendar toward the anniversary of the night you "ran," and the only adult in the house who believes in ghosts is the man who made you one.

## Run it

Requires Godot 4.7.x. No plugins, no .NET, no downloaded dependencies.

```bash
godot --path godot
```

Or open `godot/project.godot` in the Godot editor and press Play.

## Controls

| Action | Key |
|---|---|
| Move | ← → or A / D |
| Flip the world | Space |
| Contact | E |
| Mute music | M |
| Mute sound effects | N |
| Restart the scene | R |

## What the slice demonstrates

One bedroom, two worlds. The boy exists in two states — a pale, translucent ghost whose legs dissolve into mist in the living world, and a solid, warm, ordinary child in the world he remembers — and the game swaps between those two static images when the world turns over. The room swaps with him: the same window, the same door, the same hanging bulb, stripped bare in one world and lived-in in the other, so the flip reads as one place rather than two pictures. Four sound events fire from real game events, a music-box lullaby loops underneath, and both can be muted independently without changing anything the game does.

## Generated assets in the slice

| Asset | What it is |
|---|---|
| `godot/assets/art/char_ghost.png` | The boy, GHOST state |
| `godot/assets/art/char_remembered.png` | The boy, REMEMBERED state |
| `godot/assets/art/env_room_empty.png` | The bedroom, stripped (upright world) |
| `godot/assets/art/env_room_memory.png` | The bedroom, remembered (inverted world) |

Every one is logged in [SOURCES.md](SOURCES.md) with its model, exact prompt, date, verdict and any hand edits. Rejected attempts are kept as thumbnails in `design/character/rejects/`.

## Documents

[CONCEPT.md](CONCEPT.md) · [STORYBOARD.md](STORYBOARD.md) · [CHARACTER-SHEET.md](CHARACTER-SHEET.md) · [CHANGE-BRIEF.md](CHANGE-BRIEF.md) · [SOURCES.md](SOURCES.md) · [FRICTIONAL.md](../FRICTIONAL.md)

## Status and known limitations

- The slice is in build: the project runs, the world flip and the player are in, and the contact interaction, meters, HUD and audio wiring are still being assembled.
- Audio has not been generated yet, so the four event sounds and the music loop are not in the scene.
- The slice covers storyboard panels 1 to 4. Panels 5 and 6 — the hallway that corrects itself and the father at the cellar door — are semester work beyond this assignment.
- The character sheet lists eleven poses; the model sheet supplies the turnaround and the ghost views, and the remaining poses are not yet generated as separate images.
- At the character's real on-screen size of 96 px the face is not legible; the design deliberately carries its read in the hair mass and posture instead. The silhouette test in `design/character/` records this.

## Credits

See [SOURCES.md](SOURCES.md). Claude Code wrote the engine code, the prompts, and the documents, and performed the local image edits (background keying, silhouette generation). ChatGPT image generation produced the character design, model sheet, both state sprites, and both backgrounds; earlier rejected attempts used Gemini. Every design decision, rejection, and acceptance is mine, argued out in [FRICTIONAL.md](../FRICTIONAL.md).

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
| Jump | Space, W, or ↑ |
| Turn the world over | F or ↓ |
| Contact the music box | E — tap for a gentle touch, hold for a loud one |
| Mute music | M |
| Mute sound effects | N |
| Restart the scene | R |

## What the slice demonstrates

One bedroom, two worlds. The boy exists in two states — a pale, translucent ghost whose legs dissolve into mist in the living world, and a solid, warm, ordinary child in the world he remembers — and the game swaps those static images when the world turns over. The room turns with him: the same window, the same door, the same hanging bulb, stripped bare in one world and lived-in in the other, so the flip reads as one place rather than two pictures. The boy stays upright through the turn, so his controls never reverse and he ends up walking the ceiling of the room as he remembers it.

He walks with a four-frame cycle whose frames advance by ground covered rather than by a clock, so his stride matches his speed and his feet never slide. The cycle belongs to the remembered state alone: **the ghost does not walk, he drifts.** He jumps with coyote time, input buffering and an early-release cut, squashes on landing in proportion to the impact, and leans into a run. All of that motion is engine code moving one static image per state — no animation frames beyond the walk poses, which the character sheet required anyway.

The stacked moving boxes are a one-way platform that is solid **only in the upright world**, because that is the only world they exist in: level geometry obeys the same rule the art does.

At the music box, a tap is a gentle contact and a hold is a loud one. Both raise recognition and tear days off the calendar toward the anniversary; the loud one costs more and wakes the house. The night ends either because the child finally sees you or because the anniversary arrives first.

Four sound events and a music loop are wired to real game events, and both can be muted independently without changing anything the game does.

## Generated assets in the slice

| Asset | What it is |
|---|---|
| `godot/assets/art/char_ghost.png` | The boy, GHOST state |
| `godot/assets/art/char_remembered.png` | The boy, REMEMBERED state |
| `godot/assets/art/char_walk_1..4.png` | Four walk poses, sliced from one generated cycle sheet |
| `godot/assets/art/env_room_empty.png` | The bedroom, stripped (upright world) |
| `godot/assets/art/env_room_memory.png` | The bedroom, remembered (inverted world) |

Every one is logged in [SOURCES.md](SOURCES.md) with its model, exact prompt, date, verdict and any hand edits. Rejected attempts are kept as thumbnails in `design/character/rejects/`.

## Documents

[CONCEPT.md](CONCEPT.md) · [STORYBOARD.md](STORYBOARD.md) · [CHARACTER-SHEET.md](CHARACTER-SHEET.md) · [CHANGE-BRIEF.md](CHANGE-BRIEF.md) · [SOURCES.md](SOURCES.md) · [FRICTIONAL.md](../FRICTIONAL.md)

## Status and known limitations

- **Audio has not been generated yet.** The four event sounds and the music loop are wired to fixed filenames and the slice runs silent without them, printing a notice. This is deliberate: sound must never decide state, and the slice proves it by working without any.
- **The ghost reads faint against the grey upright room.** This was predicted in CHANGE-BRIEF as a failure case and is visible in `evidence/01-upright-ghost.png`. The planned fix is a rim light on the ghost sprite rather than a change to the room; it has not been done.
- The slice covers storyboard panels 1 to 4. Panels 5 and 6 — the hallway that corrects itself and the father at the cellar door — are semester work beyond this assignment.
- Three of the fourteen character-sheet poses (reach, scare, goodbye) are specified but not generated; the slice expresses those states through image swaps and engine motion instead.
- The human playtest with sound on and then muted is still outstanding, and an automated input sequence does not substitute for it.

## Credits

See [SOURCES.md](SOURCES.md). Claude Code wrote the engine code, the prompts, and the documents, and performed the local image edits (background keying, silhouette generation). ChatGPT image generation produced the character design, the eight-view model sheet, both state sprites, the four-frame walk cycle, and both backgrounds; earlier rejected attempts used Gemini. The glow marking the music box is drawn in code and satisfies no generative requirement, which the asset log states. Every design decision, rejection, and acceptance is mine, argued out in [FRICTIONAL.md](../FRICTIONAL.md).

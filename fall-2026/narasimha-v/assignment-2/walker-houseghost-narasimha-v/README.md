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

Or open `godot/project.godot` in the Godot editor and press Play — but if the editor has been left open while the files changed, choose **Reload from disk** when prompted, never "Ignore external changes". An editor holding a stale scene will happily play a build that no longer exists.

## Controls

| Action | Key |
|---|---|
| Move | ← → or A / D |
| Jump | Space, W, or ↑ |
| Turn the world over | F or ↓ |
| Contact a relic | E — tap for a gentle touch, hold for a loud one |
| Mute music | M |
| Mute sound effects | N |
| Read the story again | I |
| Restart the scene | R |

## What the slice demonstrates

**It opens by saying who you are.** The grey, emptied house; a living child sitting on the floor playing with a one-eared rabbit; a ghost hanging from the ceiling above her that she does not look up at. Three lines over the top — *they told everyone I ran away · a new family sleeps in my room now · I need one of them to see me* — and then the memory blooms in over the truth, he fades from ghost to boy, and you have control. None of it explains a mechanic.

**One house, two truths.** The camera never rotates. Flip reverses gravity: he falls upward and stands on the ceiling, and the room cross-dissolves between the warm version he remembers and the stripped one the new family moved into. He walks with an eight-frame cycle in the memory and drifts upside down as a ghost in the truth, hair and mist streaming toward the ceiling.

**Three things of his are still in the house** — the music box his mother wound, his shoes still by the door, a floorboard with his name under it. Each is out of reach from the floor and each calls across the level with the sound of a music box playing by itself, so finding them needs the flip. A relic's light goes out once it has been answered, so the lit ones are always the ones left.

**What blocks you is different in each world.** His bookshelf clutters the memory and was taken out of the real house years ago; the family's moving boxes clutter the truth and were never his. And the floor of the real house has been pulled apart: three gaps must be jumped, and falling through one costs a night, out of the same meter that being seen costs.

The opening is read at your own pace: each line waits for a key, and **I** brings the four lines back at any point during play.

**Nothing is explained in a list of controls.** A prompt appears beside the thing it refers to, only while it can be acted on, and stops appearing once used: the arrow keys until you first move, **F** when you are standing below something you cannot reach from the floor, **E** once you have turned the world over and can take it. That replaced a hint line listing every control at all times, which an external playtester read once and then stopped seeing — she finished a session without ever learning the game's central verb.

**She is how you know it is working.** Absorbed in her rabbit at first; looking up and to one side once you have found one thing; facing you with her eyes wide when you have found all three. She is the recognition meter, and the only saturated colour in a grey room.

**Nine sounds, and the one that matters most is a difference.** The boy has footsteps on carpet; the ghost has none at all, only displaced air that starts when he moves and stops when he stops. A heart begins beating at four nights left and quickens as they run out, and the counter flinches with it. Music ducks beneath every sound; both mute independently without changing anything the game does.

## Generated assets in the slice

| Asset | What it is |
|---|---|
| `godot/assets/art/char_ghost.png` | The boy, GHOST state |
| `godot/assets/art/char_remembered.png` | The boy, REMEMBERED state |
| `godot/assets/art/char_walk_1..4.png` | Four walk poses, sliced from one generated cycle sheet |
| `godot/assets/art/env_room_empty.png` | The bedroom, stripped (upright world) |
| `godot/assets/art/env_room_memory.png` | The bedroom, remembered (inverted world) |
| `godot/assets/music/mus_upright.wav` | Music for the upright world — tense, driving, no warmth |
| `godot/assets/music/mus_memory.wav` | Music for the remembered world — a lullaby over an organic groove |
| `godot/assets/art/char_walk_1..8.png` | Eight-frame walk cycle |
| `godot/assets/art/char_jump_1..4.png` | Crouch, rising, falling, landing |
| `godot/assets/art/char_ghost_inv_1..6.png` | The ghost drifting, drawn upside down |
| `godot/assets/art/child_1..3.png` | The new family's daughter: playing, hearing, seeing |
| `godot/assets/sfx/*.wav` | Nine sound events |

Every one is logged in [SOURCES.md](SOURCES.md) with its model, exact prompt, date, verdict and any hand edits. Rejected attempts are kept as thumbnails in `design/character/rejects/`.

## Documents

[CONCEPT.md](CONCEPT.md) · [STORYBOARD.md](STORYBOARD.md) · [CHARACTER-SHEET.md](CHARACTER-SHEET.md) · [CHANGE-BRIEF.md](CHANGE-BRIEF.md) · [SOURCES.md](SOURCES.md) · [FRICTIONAL.md](../FRICTIONAL.md)

## Status and known limitations

- **The three room tiles repeat.** The middle one is mirrored to break the repetition, which puts two doors adjacent at the seam; it reads as a double doorway rather than an error, and is preferable to a background that repeats exactly while the camera follows the player.
- **The floor gaps exist in both worlds**, although the fiction says only the real house has been pulled apart. Treated as his memory decaying rather than modelled as two separate floors.
- **Three character-sheet poses (reach, scare, goodbye) are specified but not generated**; the slice expresses those states through image swaps and engine motion.
- **The floorboard relic and the floor holes are drawn in code**, not generated. The asset log marks them as such so they are never counted as generated assets.
- **The slice covers storyboard panels 1 to 4.** Panels 5 and 6, the hallway that corrects itself and the father at the cellar door, are semester work.
- **The automated check cannot hear.** It verifies that each event fires exactly once and that muting changes no state, but every audio fault in this project was found by a human listening, not by the check passing.

## Credits

See [SOURCES.md](SOURCES.md). Claude Code wrote the engine code, the prompts, and the documents, and performed the local image edits (background keying, silhouette generation). ChatGPT image generation produced the character design, the eight-view model sheet, both state sprites, the four-frame walk cycle, and both backgrounds; earlier rejected attempts used Gemini. The glow marking the music box is drawn in code and satisfies no generative requirement, which the asset log states. Every design decision, rejection, and acceptance is mine, argued out in [FRICTIONAL.md](../FRICTIONAL.md).

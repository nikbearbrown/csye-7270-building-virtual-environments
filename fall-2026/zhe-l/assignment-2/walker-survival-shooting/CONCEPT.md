# Concept — walker-survival-shooting

> Version 1 — written 2026-10-03, before any asset generation.
> Source: my original game design document (a Chinese .docx, not in this repo) and a Q&A session with Claude Code on 2026-10-03.
> Version 1 will not be rewritten; later changes are added under "Revision history".

## The game in two sentences
The player is a survivor in a ruined city who lives in the subway and carries a military tablet for gathering information, contacting other people, and running software. Each run, the player deploys to the surface or to an abandoned facility connected to the subway, kills monsters, scavenges supplies, and completes tasks inside small but complex buildings, then extracts.

## Core loop
- **Repeated action:** Free exploration, looting, fighting, and using the tablet. The map is open, and there is no set order between fighting and looting, but high-value areas are always guarded by monsters.
- **Decision each time:** Entirely up to the player: whether to go into a high-value area, whether to fight the monsters guarding it, when to open the tablet. The game **does not pause** while the tablet is open, and the tablet can be used for anything, including a few rounds of a mini-game or switching songs.
- **Risk:** The main risk is losing what you carry when you die (the tablet is never lost, and items in the safe container survive). Other stats, such as weapon wear and survival stats, exist mainly for realism and gameplay.

Session loop outside a single run: prepare at the base → deploy → explore, fight, loot, do tasks → extract (or die) → return to the base and read recovered media on the base computer → next run.

## Design pillars
| # | Pillar | Visual or sound choice that honors it |
|---|---|---|
| 1 | **The tablet is gameplay.** The tablet's software is gameplay in itself, not just an information display, and the world keeps going while it is open. | Visual: the transition from the one-handed small window in the bottom-right corner to holding the tablet with both hands and leaning in to look. |
| 2 | **Small but complex maps.** A map is not large and has few buildings, but each building is as complex as a factory or a university. No large stretches of empty forest and no simple little houses. | Visual: large, complex buildings. |
| 3 | **High-risk, high-reward extraction.** The best loot sits where monsters guard it, and dying means losing what you carry. | No single visual or sound choice: a high-risk extraction is the combined result of the whole game design, not something one element can show. |

## Art direction
- **View:** third person, over the shoulder; aiming switches to first person.
- **Style:** low-poly gear, weapons, and environments; anime-style characters, but not cute.
- **Why:** Low-poly gear is easy to generate with AI, keeps the rendering load low so optimization is easier, and is not hard to make. Anime-style characters are my own preference, because low-poly characters don't look good. They are not cute because, if the game gets a story, its overall tone will be serious.
- **Reference notes (in words):**
  1. Dark, cool-toned overall; no overly bright colors.
  2. Technology somewhere between the millennium and today, with a military look overall. The tablet is thick with hard, angular edges, like a rugged tablet used by the military.

## Audio direction
- **What the player should feel:** Runs are tense, so there is **no background music** on the surface, only ambient sound.
- **When music starts, changes, or stops:**
  - **Start menu:** a looping track; its style will be decided after the content is finished. The camera faces the player character, who sits on a bench. After clicking Start, the camera rotates to the third-person over-the-shoulder view and **the music stops**.
  - **On the surface:** no music, only ambient sound.
  - **Spotted by a boss-level enemy:** tense combat music plays.
  - **Pause:** the game has no pause at all.
  - **Death:** black screen and a failure sound.
  - **Successful extraction:** a sound effect only, no music.
  - **Music player:** at any time, music the player plays on the in-game music player overrides all background music. Players can import their own songs.

## Engine
- Godot 4.7.2-stable (Windows)

---
## Revision history
- **2026-10-09 — Audio direction, addition (tablet terminal UI sounds):** the tablet terminal's interface sounds are short, dry electronic tones layered with light radio static, squelch, and communications-equipment noise. Navigation feedback is restrained and low-pitched overall; error feedback uses a shorter, brighter single "di" beep to get attention. The interface should sound like rugged field electronics, not a clean consumer device.

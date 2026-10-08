# Storyboard

> Version 1 — written 2026-10-03 to 2026-10-06, before any asset generation.
> Frame shape: **16:9** for every panel. Panel images will go in `design/storyboard/`.
> The asset slice for this assignment takes place entirely inside the subway base.

## Terms
- **Tablet screen:** the tablet in the character's hands inside the game world, and how it is positioned relative to the character.
- **Computer screen:** what the player sitting at the computer actually sees, including the tablet UI window that takes up part of the view once the tablet is open.

## The three tablet states (the core action)
| Current state | Short Tab | Long Tab |
|---|---|---|
| Not looking | → One-handed | → Two-handed |
| One-handed | → Not looking | → Two-handed |
| Two-handed | → One-handed | → Not looking |

- **Not looking:** the tablet is put away; normal movement.
- **One-handed:** the character takes the tablet out with one hand, and a tablet window appears in the bottom-right corner of the computer screen, taking about 20–40% of the view. You give up part of your view to read information while walking (map, chat history, and so on).
- **Two-handed:** the character switches from one hand to two and leans in to look at the tablet. The small window slides off the computer screen, and the tablet content is shown large and clear. This is for screens that need full interaction, such as sorting the backpack.
- The game **does not pause** while the tablet is open.

## Coverage
| Required moment | Panel |
|---|---|
| First thing the player sees | 1 |
| Core action | 3, 4 |
| Failure | 8 |
| Success | 9 |
| Recovery / retry | 10 |
| End of a session | 9, 10 |

| View | Panels |
|---|---|
| Medium | 1, 2, 3, 4 |
| Close-up | 5, 6 |
| Wide | 7 |

| Angle | Panels |
|---|---|
| Eye level | 1 |
| Over the shoulder | 2, 3, 4, 5 |

---

## Panel 1 — Start menu
- Shot: medium · eye level, facing the character · title screen (in-game, before play)
- Player action: on the start menu, before clicking Start
- See: inside the subway base, the character sits on a bench against the wall, facing the camera, on the right side of the frame; the game title is at the top left, with the menu UI (Start, Settings, and so on) below it
- Hear: looping menu music (style to be decided)
- Assets: CHAR-SIT (sitting pose), ENV-BASE (subway base), UI-TITLE (title and menu), MUS-MENU
- Design reason: the start screen is itself inside the safe house (the subway base). After clicking Start, the camera moves and the player is seamlessly in the safe house, which is better than cutting to a loading screen.

## Panel 2 — Clicking Start
- Shot: medium · rotates from the front to third-person over the shoulder · gameplay view (transition)
- Player action: clicks Start; the camera rotates to the over-the-shoulder view and the player gets control
- See: as the camera turns, the character stands up from the bench; the title and menu UI on the left fade out. (Whether the game will have a "sit down" mechanic is not decided yet.)
- Hear: the menu music **stops**
- Assets: CHAR-SIT, CHAR-IDLE, UI-TITLE, MUS-MENU
- Design reason: same as Panel 1. After clicking Start, the camera move carries the player seamlessly into the safe house, which is better than a loading screen.

## Panel 3 — Core action: one-handed (short Tab)
- Shot: medium · over the shoulder · gameplay view
- Player action: short Tab while not looking; the character takes the tablet out of a pocket (or a tablet pouch on the tactical belt) with one hand, keeps holding it in one hand, and can keep walking
- See: inside the subway base; the character holding the tablet in one hand; a small tablet window in the bottom-right corner of the computer screen (about 20–40%) showing the **desktop**
- Hear: a startup sound when the tablet is picked up, a short "beep" (sound effects focus on the tablet); a cloth-rubbing sound when it is taken out is wanted but low priority
- Assets: CHAR-TAB1 (one-handed hold), UI-TAB-SMALL (small-window desktop), ENV-BASE, SFX-TAB-OUT (rubbing sound), SFX-TAB-BOOT (startup sound)
- Design reason (pillar "The tablet is gameplay"): give up part of the view in exchange for reading information while walking

## Panel 4 — Core action: two-handed (long Tab)
- Shot: medium · over the shoulder (the third-person camera does not deliberately point at the tablet) · gameplay view
- Player action: long Tab; the character switches from one hand to two and leans in to look at the tablet; the small window in the bottom-right corner slides off the computer screen
- See: inside the subway base; the character holding the tablet with both hands; a large, clear tablet interface showing the **desktop**
- Hear: —
- Assets: CHAR-TAB2 (two-handed hold), UI-TAB-FULL (full desktop), ENV-BASE
- Design reason (pillar "The tablet is gameplay"): full interaction with the tablet, for example sorting the backpack, at the cost of giving up the view around you

## Panel 5 — Tablet screen (the character and the tablet)
- Shot: close-up · over the shoulder · design view
- Content: how the character's hands and the tablet relate, drawn in one state only. The tablet is thick with hard edges, like a military rugged tablet.
- Hear: —
- Assets: PROP-TABLET
- Design reason: show how the character and the tablet should look in the game.

## Panel 6 — Sneaking through a dark lab
- Shot: close-up · design view (the focus is on the main character, not on what the level looks like)
- Player action: sneaking through the inside of a lab with no light, avoiding monsters to save resources
- See: the main character sneaking in the dark lab; the monster being avoided is mechanical
- Hear: — (this panel is an image only, with no sound)
- Assets: ENV-LAB, ENEMY-MECH (mechanical monster)
- Design reason: sneaking past monsters saves resources

## Panel 7 — Large boss fight
- Shot: wide · design view
- Player action: destroying a big robot with guns
- See: a large robot boss
- Hear: after the boss spots the player, tense combat music starts
- Assets: MUS-BOSS

## Panel 8 — Failure: death
- Shot: gameplay view
- Player action: torso or head HP drops to 0 and the character dies
- See: the screen goes black
- Hear: failure sound
- Assets: SFX-FAIL

## Panel 9 — Success: extraction
- Shot: gameplay view
- Player action: reaches an extraction point and extracts. Any extraction counts as success; how much you bring back only decides whether the run was worth it.
- Hear: extraction success sound, no music
- Assets: SFX-EXTRACT

## Panel 10 — Back at the base (recovery / retry / end of session)
- Shot: gameplay view
- Player action: whether the player extracted or died, they return to the base. After death, torso and head have only 10% HP and all other body parts 5%. The base is a safe zone: HP never drops there and slowly regenerates. The player can use medicine to heal quickly or simply wait.

---
## Revision history

### 2026-10-07 — Sketches for panels 1–5; camera change in panels 4–5
- **Sketches:** my hand sketches for panels 1–5 are in `design/storyboard/` (`01-title.png`, `02-start.png`, `03-tablet-onehand.png`, `04-tablet-twohand.png`, `05-tablet-fullscreen.png`). They only show the rough idea; the text is what counts.
- **Panel 1:** the seat changes from "bench" to **to be decided** (a chair, a sofa, or something else). The title is a placeholder; the game has no name yet. The menu is Start / Option / Quit.
- **Panel 2:** added: there is no scene transition. Only the camera moves, in one continuous shot, into the third-person over-the-shoulder view. A status bar sits at the top left (something like a health bar; what it is exactly is not decided, so it is a placeholder for now).
- **Panel 4 (changed):** now the **transition animation** from one hand to two hands. The camera moves to focus on the tablet (version 1 said the camera does not deliberately point at the tablet). Shot: medium → push in · over the shoulder · gameplay view (transition).
- **Panel 5 (changed):** from "a design view of the hands and the tablet" to a **gameplay view**: after the camera pushes in, the tablet fills the whole screen and shows information. Shot: close-up · gameplay view. Assets: PROP-TABLET, UI-TAB-FULL. The old panel 5 (how the hands hold the tablet) is no longer a separate panel.

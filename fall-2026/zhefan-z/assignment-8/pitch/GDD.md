# The Little Flame Witch — Game Design Document

**Version 2.0 · 2026-11-21** · Zhefan Zhang (zhefan-z) · CSYE 7270 final project

Updated from my Assignment 4 GDD (submitted on Canvas as a PDF, 2026-10-15; a copy is in `pitch/A4-GDD.pdf`) to the final project's size: a vertical slice of two to three short levels instead of five chapters, a simpler story, and no save system. The sections follow the course GDD tool's sixteen sections plus art and sound, as Assignment 8 asks. claude.ai drafted the text from my answers and my Assignment 4 GDD; every decision in it is mine. **Built** marks what exists in my game today (`zhefan-z/assignment-7`, `840b501`); everything else is a plan, written as "will".

## Vision (the game in brief)

**The Little Flame Witch** is an HD-2D cave action game: the player aims fireballs with the mouse to fight through a cold cave. **The goal** is to reach the bottom of the cave and defeat the great wolf that guards it. A run is two to three short levels; falling into a pit or losing all HP sends the witch back to the start of the level or the last campfire, and beating the great wolf ends the game.

*This game is a short action run for players who like aiming and reading enemies, that delivers the feeling of a small fire in a big dark through mouse-aimed fireballs against wolves that warn before they strike.*

## 1. Design pillars

1. **Your fire is the only warmth.** The cave is cold and low-saturation; only fire and what fire makes safe are warm on screen.
2. **Every failure is fair.** Every danger warns before it strikes, and the heavier the penalty, the easier the challenge.
3. **Readable at a glance, even muted.** The player always knows where she is, what hit her and whether her shot landed.
4. **Small witch, big threat.** She is fragile but capable; the final enemy is far bigger than her.

## 2. Core gameplay loop

- **Moment to moment:** move, jump, aim and fire; read a wolf's growl and decide whether to shoot it early (cancelling its lunge) or step out of reach.
- **In one sitting:** clear a level → reach the campfire and its chest → the next level → the great wolf.
- **What brings the player back:** a run is short, so the reason to replay is a cleaner run: fewer hits, more lunges cancelled.

## 3. Player experience goals

- The player should feel **small but capable** when an early fireball cancels a wolf's lunge mid-growl.
- The player should feel **safe and warm** when she reaches a campfire after a fight.
- The player should feel **tension** when the great wolf's entrance fills the screen.
- The player should feel **relief** when the great wolf is beaten and the cave falls quiet.

## 4. Core mechanics

| Action | Input | What it does | At the edges | Status |
|---|---|---|---|---|
| Move | A / D or the arrow keys | Runs left and right | Stops at walls | **Built** |
| Jump | Space, W or Up | Jumps over pits, rocks and wolves | From the ground, or within 0.08 s of running off an edge; a press up to 0.10 s before landing still counts; no double jump | **Built** |
| Aim | Mouse | A crosshair shows where the fireball goes | — | **Built** |
| Cast | Left mouse | Fires a fireball toward the cursor | Stopped by walls; a hit during a wolf's growl cancels its lunge | **Built** |
| Heal | A key still to be chosen | Restores HP | Only after it is found in the first chest | Will |
| Interact | E | Opens a chest, rests at a campfire | Only when standing beside it | Will |
| Lose and restart | — (R restarts after a clear) | A pit or 0 HP shows the reason on the HUD, then the level reloads | Back to the level start; the last campfire once campfires exist | **Built** (restart at level start) |

## 5. Systems

- **Wolves:** a state machine (patrol, growl, lunge, recover) with a phase table in frames: growl 31 ticks, lunge 22, recover 36. A hit during the growl cancels the lunge. **Built**, pinned and edge-tested in Assignment 7.
- **The great wolf:** the same state machine scaled up, with more HP, a longer, clearer warning and its own entrance. Will.
- **Hazards:** spikes and a rolling boulder that warn before they hurt. Will.
- **Health:** 5 HP shown as hearts in the HUD; the hurt tint, a blink and 1.0 s of invulnerability after a hit (**Built**); the heal spell refills it (will).
- **Campfire:** a rest point and the restart point for the rest of the level; no saving. Will.
- **Camera and light:** an HD-2D camera following the witch; the fireball is a moving light. Will.

## 6. Progression

There is no levelling and no equipment. The witch changes in one way: the **heal spell**, found in the chest beside the campfire at the end of level 1. Difficulty rises by level: more wolves, then spikes and the boulder, then the great wolf.

## 7. World and environment

One cold cave under a mountain, told in **two to three short levels**; the exact number will depend on progress, and the last level is always the great wolf's den.

1. **Cave mouth:** first wolves, easy pits; ends at the campfire and the chest with the heal spell.
2. **Deeper tunnels** (if there are three levels): more wolves, spikes and the rolling boulder.
3. **The den:** the great wolf.

The world's one rule: warmth comes only from fire, so lit places are safe places.

## 8. Narrative

A simple story, told in four short, skippable scenes with portraits: the witch goes down into the cave with the only flame she has; she rests at a campfire after the first fight; the great wolf tells her to turn back; after the fight it lets her pass. There is no larger plot in the final project. (Assignment 4 had a longer story about a Great Hearth; I cut it to fit a short slice.)

## 9. Characters

- **The Little Flame Witch (player):** white twin tails with red ribbons, red eyes, a blue witch hat, a staff tipped with a red crystal (drawn as a red orb in the portraits). Pixel sprite in play (**Built**), generated portraits in dialogue (concept).
- **Wolves (enemies):** grey cave wolves that growl before they lunge. **Built**.
- **The great wolf (boss):** the same kind of wolf, much larger, with glowing eyes; it speaks before and after the fight. Will; a generated concept portrait exists.

## 10. Art direction

- **Style:** HD-2D: 2D pixel sprites standing in a lit, low-poly 3D cave, seen from a tilted camera.
- **Palette:** a cold blue-grey cave; warm colour only on fire and what fire makes safe (from Assignment 2).
- **References** (games I played; techniques only, no assets): Octopath Traveler's depth of field and lighting; Hollow Knight's atmosphere and boss entrances.
- **The look, planned:** tilt-shift depth of field; bloom; volumetric fog and light shafts; the fireball as a moving light; dust, drips, glowing moss and glinting crystals; my Assignment 3 rock, crystal and chest in the level; sprites lit by the scene; hit-stop, camera shake, impact flash and sparks; a boss title card; a lit title screen.
- **The art itself:** the pixel sprites (Assignment 2, Built), the four-frame run cycle and wolf lunge rig (Assignment 7, Built), the 3D props (Assignment 3, Built), the cave lights and embers (Assignment 7, Built), and generated concept portraits for the dialogue (Gemini 4, concept).

## 11. Sound and music

- **Music:** a cave theme generated with Lyria in Assignment 2, cut into a seamless loop (**Built**). A boss theme and a quieter campfire theme will be added.
- **Sound effects:** cast, wolf defeated, hurt, fail and clear, generated with Stable Audio Open 1.0 in Assignment 2 (**Built**). The great wolf's growl, the boulder's rumble and a campfire crackle will be added.
- **What they do for the player:** each event has its own sound, so hurt and fail never sound alike, and the game reads with the eyes off the screen. Sound follows game state; it never decides it.

## 12. Feature list

| Must | Should | Could |
|---|---|---|
| The 3D cave with sprites placed in 3D and the HD-2D camera | The heal spell, the chest and the campfire | A third level |
| Move, jump, aim and cast in 3D | Spikes and the rolling boulder | Volumetric fog and light shafts |
| Wolves with growl, lunge and the growl cancel | The four story scenes with portraits | Dust, drips, moss and crystal glints |
| Two levels from title screen to end screen | Depth of field, bloom, the fireball as a light | Hit-stop, camera shake, impact flash |
| The great wolf boss | Sprites lit by the scene | The boss title card and a lit title screen |
| HP, fail and restart | | |
| The Windows build and a test report a stranger can rerun | | |

**Smallest playable version:** one 3D cave room where the witch runs, jumps and fires at one wolf, with my existing behaviour pin passing against it.

## 13. Out of scope

- No multiplayer.
- No save system: the levels are short, and a campfire is only a rest and restart point.
- No levelling, equipment or shops.
- No web export: Windows desktop only.
- None of Assignment 4's later chapters, extra spells or extra bosses.

## 14. Technical requirements

- **Engine:** Godot 4.7.2-stable, GDScript, Forward+ (Vulkan).
- **Export target:** Windows desktop (.exe in a zip).
- **Frame rate target:** 60 fps at 1080p on my RTX 5060 Laptop GPU, measured with Godot's profiler, not claimed.
- **From greybox to finished:** rooms will be blocked out with boxes first; then low-poly pieces built in Blender from basic shapes (my Assignment 3 rules: metres, origin at the base, exported as .glb); sprites shown as camera-facing Sprite3D billboards.
- **Verification:** behaviour pinned before every change, edge tests at phase boundaries, headless checks through my test wrapper, human checks for what they cannot see.

## 15. Risks

- **Moving the 2D game into 3D** could break the movement, collision and state machines that already work. I will test it on one room first, judged by whether my Assignment 7 pin still passes; if it does not, I keep the 2D gameplay layer and make the 3D cave the backdrop.
- **Scope:** three levels may not fit. The plan already allows two.
- **Cost of the look:** volumetric fog and depth of field may miss 60 fps; each is measured, and the costliest is dropped first.

## 16. Open questions

- 2D gameplay with a 3D backdrop, or 3D bodies held to a plane? I will find out with the one-room test.
- Two levels or three? I will decide after the first level is playable.
- Will the pixel sprites read well under depth of field and coloured light? I will check it in captures from the first room.

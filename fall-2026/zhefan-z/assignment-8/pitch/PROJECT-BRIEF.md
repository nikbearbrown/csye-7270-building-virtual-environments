# PROJECT-BRIEF — The Little Flame Witch

Zhefan Zhang (zhefan-z), CSYE 7270 Fall 2026, final project pitch. Written 2026-11-20 from my answers; claude.ai put them into sentences. Everything in the future tense is a plan.

**Stack.** Godot 4.7.2-stable, GDScript, Forward+ renderer, Windows desktop export; built with Claude Code, verified with headless tests through `scripts/run-test.sh`.

## 1. What is it?

An HD-2D cave adventure shooter: a little witch fights her way through one cave level with fireballs and, at the end, defeats a great wolf. When it is done it will be a **playable Windows desktop build** (a zip with an .exe) of one vertical slice, from title screen to end screen: pixel-art characters in a lit 3D cave.

## 2. Why would anyone care?

It puts **Octopath Traveler's HD-2D look** (pixel sprites in a lit 3D world) together with **Metal Slug-style side-scrolling shooting**, and the fireball is **aimed with the mouse** instead of fired straight ahead. I have played all three of the games named here.

- **What it gives the player:** a short cave run they can finish in one sitting: aim fireballs at a wolf, read its growl and cancel its lunge with an early hit, rest at a campfire beside a chest, and beat the great wolf.
- **What is different:** Octopath Traveler is turn-based; Metal Slug is flat pixel art with fixed-direction shots; Hollow Knight explores a large cave with progression. This gives a player who wants a short action run the HD-2D look with free mouse-aimed shooting, in a few minutes and with no levelling.

## The look (planned)

What will make it look like HD-2D rather than a flat 2D game, all built from Godot's own renderer features and kept visual only (my behaviour pin will still pass after each, and frame time will be measured on an RTX 5060 Laptop GPU):

- **Lighting and post-processing:** tilt-shift depth of field; bloom, with a cold blue cave where only fire is warm (my Assignment 2 palette rule); volumetric fog with light shafts from cracks in the ceiling; **the fireball as a moving light** that lights the cave walls as it flies.
- **Set dressing:** dust, drips, glowing moss and glinting crystals; my Assignment 3 rock, crystal and chest placed in the level; the pixel sprites lit by the scene's lights.
- **Combat and presentation:** hit-stop and a small camera shake on a hit; a white flash and sparks on the impact frame; a boss entrance with a camera push-in and the boss's name as a title card; a title screen over the lit cave with flickering firelight.
- **Story moments:** four short, skippable scenes with 2D character portraits and one or two lines each: the witch's opening monologue, a line at the campfire after the first fight, and the great wolf before and after the boss fight. The portraits will be generated with Gemini under Assignment 2's rules and labelled generated.

These are techniques learned from games I played (Octopath Traveler's depth of field and lighting, Hollow Knight's atmosphere and boss entrances); no asset from any of them is used.

## 3. Who opens it, and what do they do?

**Role:** gameplay programmer. **Reader:** a hiring manager or lead gameplay programmer. **First sixty seconds:** download the zip, unzip it, double-click the .exe; the title screen shows the controls; the opening line can be skipped with one key; they are playing within a minute without reading anything else.

## 4. What does it prove about me?

That I can build and verify gameplay systems, the course skills it will show:
- **Animation and state:** state machines that drive clips with one authority, phase tables in frames, interrupts per phase.
- **Shaders and materials, particle effects:** carried over into the 3D cave.
- **Profiling:** frame and GPU time measured on a named machine (RTX 5060 Laptop GPU), not claimed.
- **Verification habits:** behaviour pinned before a change, edge tests at phase boundaries, headless checks with the human checks they cannot replace, and Claude Code directed with scoped tools.

A reviewer could fairly conclude that the gameplay works as tested. The evidence will be a test report a stranger can rerun, frame captures labelled by revision, and measured costs.

## 5. In, out, first

- **In:** one cave level from title to end screen; the mage's run, jump, aimed fireball and a heal spell; wolves and the great-wolf boss; spikes and a rolling boulder; a chest and a campfire rest point; four short story moments with portraits; a Windows build.
- **Out (deliberately):** no multiplayer.
- **First:** the core loop in one 3D cave room: the mage runs, jumps and casts at a wolf, with HD-2D framing. **How anyone would know it ran:** my existing behaviour pin passes against that room, and a windowed capture of it is labelled with its revision.

## 6. What could sink it?

**Moving the 2D game into a 3D scene could break the movement, collision and state machines that already work.** I don't know yet whether to keep the 2D gameplay layer and render the cave in 3D behind it, or to move the characters to 3D bodies held to a plane. I will find out with a one-room spike first, judged by one test: whether my Assignment 7 pin still passes there. If it doesn't, I keep the 2D layer and the 3D becomes the backdrop.

## 7. Why this project?

Half learning, half showing. **New to me:** HD-2D itself: a 3D cave scene, its lighting and camera, and 2D sprites placed in 3D. **Already have, with evidence:** shaders and materials (Assignment 5, `2b68e0a`), particle effects with measured GPU cost (Assignment 6, `7672d5a`), animation, state machines, pins, edge tests and mutations (Assignment 7, `840b501`).

## Exists today

| What | Where it can be seen |
|---|---|
| The 2D game: mage (run, jump, aimed fireball, hurt), wolf (patrol, growl, lunge, recover), pit, exit | `zhefan-z/assignment-7` at `840b501` |
| The mage's four-frame run cycle and the wolf's keyed lunge rig with a per-phase interrupt | `840b501`; film *Keys on the Tick* |
| Fireball impact and trail particles, measured on an RTX 5060 Laptop GPU (about 0.02 and 0.10 ms) | `zhefan-z/assignment-6` at `7672d5a` |
| A hurt-tint shader and a frosted-rock material | `zhefan-z/assignment-5` at `2b68e0a` |
| 3D props: rock, crystal, treasure chest (shown in a separate 3D scene) | Assignment 3 |
| Cave lights with a flicker clip, embers, the lunge afterimage | `840b501` |
| 38 headless test runs at 30, 60 and 144 fps, all passing in a fresh clone | `840b501`, `TEST-REPORT.md` |
| Concept portraits for the story moments: the witch (full body, four expressions) and the great wolf (two), generated with Gemini 4 in the Gemini app, not yet in the game | `pitch/art/`, `pitch/SOURCES.md` |

## Will exist

The 3D cave level and its camera, the sprites placed in 3D, the look above, the four story moments with the portraits in the game, the heal spell, the great-wolf boss, spikes and a rolling boulder, the chest-and-campfire rest point in the level, a title and an end screen, the Windows export, and a test report for the slice.

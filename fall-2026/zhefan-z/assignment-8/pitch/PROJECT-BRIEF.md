# PROJECT-BRIEF — The Little Flame Witch

Zhefan Zhang (zhefan-z), CSYE 7270 Fall 2026, final project pitch. Written 2026-11-20 from my answers, revised 2026-11-21 for the updated Assignment 8 (game in brief, GDD, appendix); claude.ai put my answers into sentences. Everything in the future tense is a plan. The full design is in `GDD.md` (version 2.0, 2026-11-21).

**Stack.** Godot 4.7.2-stable, GDScript, Forward+ renderer, Windows desktop export; built with Claude Code, verified with headless tests through `scripts/run-test.sh`.

## The game in brief

**The Little Flame Witch** is an HD-2D cave action game: the player aims fireballs with the mouse to fight through a cold cave. **The goal** is to reach the bottom of the cave and defeat the great wolf that guards it; a pit or losing all HP sends the witch back to the level start or the last campfire, and beating the great wolf ends the game. **One picture:** a real frame of my game at `840b501` (the witch's fireball and a growling wolf in the lit cave), with the generated concept portrait beside it, labelled.

## 1. What is it?

An HD-2D cave adventure shooter: a little witch fights her way through a cave with fireballs and, at the end, defeats a great wolf. When it is done it will be a **playable Windows desktop build** (a zip with an .exe) of a vertical slice, from title screen to end screen: two or three short cave levels, the last one the boss, with pixel-art characters in a lit 3D cave.

## 2. Why would anyone care?

It puts **Octopath Traveler's HD-2D look** (pixel sprites in a lit 3D world) together with **Metal Slug-style side-scrolling shooting**, and the fireball is **aimed with the mouse** instead of fired straight ahead. I have played all three of the games named here.

- **What it gives the player:** a short cave run they can finish in one sitting: aim fireballs at a wolf, read its growl and cancel its lunge with an early hit, rest at a campfire beside a chest, and beat the great wolf.
- **What is different:** Octopath Traveler is turn-based; Metal Slug is flat pixel art with fixed-direction shots; Hollow Knight explores a large cave with progression. This gives a player who wants a short action run the HD-2D look with free mouse-aimed shooting, in a few minutes and with no levelling.

## The look and the story moments

Planned in `GDD.md` sections 8 and 10: the HD-2D look (depth of field, bloom, fog and light shafts, the fireball as a moving light, set dressing, hit-stop and the boss entrance) and four short, skippable story scenes with generated portraits. Every look item stays visual only: my behaviour pin will still pass after each, and its frame cost will be measured on the RTX 5060 Laptop GPU.

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

- **In:** two or three short cave levels from title to end screen, the last one the great-wolf boss; the mage's run, jump, aimed fireball and a heal spell; wolves and the great-wolf boss; spikes and a rolling boulder; a chest and a campfire rest point; four short story moments with portraits; a Windows build.
- **Out (deliberately):** no multiplayer, and no save system: the levels are short, and a campfire is a rest and restart point, not a save.
- **First:** the core loop in one 3D cave room: the mage runs, jumps and casts at a wolf, with HD-2D framing. **How anyone would know it ran:** my existing behaviour pin passes against that room, and a windowed capture of it is labelled with its revision.

## 6. What could sink it?

**Moving the 2D game into a 3D scene could break the movement, collision and state machines that already work.** I don't know yet whether to keep the 2D gameplay layer and render the cave in 3D behind it, or to move the characters to 3D bodies held to a plane. I will find out with a one-room spike first, judged by one test: whether my Assignment 7 pin still passes there. If it doesn't, I keep the 2D layer and the 3D becomes the backdrop.

## 7. Why this project?

Half learning, half showing. **New to me:** HD-2D itself: a 3D cave scene, its lighting and camera, and 2D sprites placed in 3D. **Already have, with evidence:** shaders and materials (Assignment 5, `2b68e0a`), particle effects with measured GPU cost (Assignment 6, `7672d5a`), animation, state machines, pins, edge tests and mutations (Assignment 7, `840b501`).

## Appendix: is this realistic?

### Exists today (shown in the film; past tense)

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

### Started, not finished

- The design: `GDD.md` and this brief (written; they will change as I build).
- The story scenes: the concept portraits exist; the dialogue box, the lines in the game and the trigger points are not started.
- Nothing of the 3D cave is started yet.

### Can one person build this by the final?

Yes, at the size of the GDD's Must and Should columns with two levels. If I fall behind, I will cut in this order: the third level, then the Could items (fog and light shafts, ambient particles, hit-stop and shake, the boss title card), then the story scenes, keeping the Must column whole.

### Where every asset comes from

| Asset | Where it comes from | Made, generated, free or bought | Licence |
|---|---|---|---|
| Witch and wolf pixel sprites | Gemini, from my prompts (Assignment 2) | generated | Google's terms, as recorded in Assignment 2's SOURCES.md |
| Run-cycle sheet | Gemini, from my prompt (Assignment 7) | generated | Google's terms (Assignment 7 ATTRIBUTION.md) |
| Wolf lunge rig | cut from my Assignment 2 wolf sprite | made | mine |
| Dialogue portraits (witch, great wolf) | Gemini 4, from my prompts (`ART-PROMPTS.md`) | generated | Google's terms |
| Rock, crystal, treasure chest | my Blender work through the Blender MCP (Assignment 3) | made | mine |
| Cave pieces, torches, campfire, spikes, boulder | my Blender work, same rules | will be made | mine |
| The great wolf's sprites | Gemini, from my wolf sprite | will be generated | Google's terms |
| Cave music | Lyria (Assignment 2) | generated | Google's terms, as recorded in Assignment 2's SOURCES.md |
| Boss and campfire music | Lyria | will be generated | Google's terms |
| Sound effects | Stable Audio Open 1.0, run locally (Assignment 2) | generated | Stability AI's licence, as recorded in Assignment 2's SOURCES.md |
| Shaders and particle effects | my own (Assignments 5 and 6) | made | mine |

Nothing bought and no third-party game assets. Everything goes in my public repository; every row is listed in `SOURCES.md`.

### Will exist (not started)

The two to three 3D cave levels and the HD-2D camera, the sprites placed in 3D, the look (GDD section 10), the four story scenes in the game, the heal spell, the great-wolf boss, spikes and a rolling boulder, the chest-and-campfire rest point in the level, a title and an end screen, the Windows export, and a test report for the slice.

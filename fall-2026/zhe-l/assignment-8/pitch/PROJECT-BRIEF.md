# PROJECT-BRIEF — final project pitch

Zhe Liu · working title: walker-survival-shooting · 2026-11-26

**Stack:** Godot 4.7.2-stable, Forward+ renderer (D3D12 on Windows), Jolt physics, GDScript, Claude Code. Export target: Windows desktop, keeping Forward+ (no build has been exported yet).

## 1. What is it?
In one sentence: in a subway base after the end of the world, the player uses the apps on a military tablet they carry, above all a memo app, to sort out clues and work out quests; and while the tablet is open, the world does not stop.
When it is done: a playable Windows desktop slice with one room, the subway base. The player can walk, raise the tablet in one or both hands, and use the tablet system (This PC and the ThoughtPad memo app) to read testimonies, copy them, and make and save a memo of their own (see "the first piece" in §6).

## 2. Why would anyone care?
Extraction, shooting, looting and RPG systems already have many examples; a game that only does those would be ordinary. My game makes the tablet **the gameplay itself**:
- A quest gives only the final goal (for example "find this thing for me"). It does not show the way, and it does not tick off each step and tell you the next one.
- Different factions write their testimonies in memos. The player copies quest hints and different people's testimonies into their own memo, compares them, finds the logical holes, and then completes the goal in their own way.

## 3. What does it give the player, and how is it different?
Comparable games (I have played each of them for more than 100 hours):
- **Subnautica:** the PDA looks like a tablet, but it can do little; it is mainly one interface that combines the backpack, the logs and the settings. In the story it is a computer with an AI; in play it is not.
- **Metal Gear Solid V: The Phantom Pain** (about 320 hours): the computer is mostly an escape menu inside a computer, and its content is mainly about the stealth gameplay.
- **Abiotic Factor:** mail, a compendium, recipes, the backpack and health management, but mostly as status displays; they are rarely made into separate apps that interact with the world.
- **Escape from Tarkov:** a quest tells you directly to kill so many on a given map, bring back a given item, or kill a given boss.

My difference: the player gets a tool for organising information themselves, not a menu that shows status and keeps the quest steps for them.

## 4. Who opens it, and what do they do in the first 60 seconds?
Target role: **technical game designer**. Readers: recruiters and hiring managers, judging within a few minutes whether I am a suitable technical designer. The film puts the design idea first, then the evidence.
First 60 seconds: read the key table in the README first (the game shows no hints, so it is **not** playable without reading anything) → open the build (once it exists; for now, run the project in Godot 4.7.2) → start in the subway base → press Tab to raise the tablet in one hand (a small window bottom right), long-press Tab for two hands, close to the eyes → double-click This PC on the tablet and open a folder.

## 5. What does it prove about me?
| Course skill | Evidence that exists |
|---|---|
| Shaders and materials | the tablet screen glow shader (written by hand), the crate wear shader, the material audit (tag `zhe-l-a5`) |
| Particles | landing dust and the dust in the light; GPU cost measured on an NVIDIA GeForce RTX 5070 Ti Laptop GPU: light dust +0.017 ms, landing dust +0.001 ms (tag `zhe-l-a6`) |
| Animation and state | the main character's tablet animations, the AnimationTree state machine, rules such as "the screen lights only on frame 20 of the raise, and never if interrupted" written as tests (tag `zhe-l-a7`) |
| Profiling | the GPU measurement above; in A7 a per-frame log showed the screen lighting 2 physics frames late (0.70 s after the press instead of 0.667 s); after finding the cause I changed one thing (TUNING r1) and 1 physics frame = 0.017 s remains (60 fps, `--fixed-fps`), as the brief had estimated (`zhe-l-a7` TUNING.md, TEST-REPORT.md) |
| Verification habits | every assignment has pinned tests and mutation tests; fresh GitHub clones of `zhe-l-a5` and `zhe-l-a7` gave the recorded test counts; agents were directed with scoped prompts, and their drafts were committed unedited before review. At f13431bf the six tests (55 / 29 / 157 / 27 / 110 / 41 PASS) rerun headless; the tablet system and ThoughtPad have no tests yet |
| Design (the focus of this role) | my design document and my "game map" notes (in Chinese, not in this repository), where design rules are written down before they become code, for example "with the tablet in both hands the character cannot walk and every key goes to the tablet; in one hand the keys only control the character" (visible in the game at f13431bf and in the film) |

## 6. What is in, what is out, what comes first?
- **Deliberately not done (the one the film stresses):** for **now**, this demo has no shooting, extraction or looting. They are part of the game and will come later, but they are not what is new about it, so they are not in this slice.
- Also out: RPG numbers; more than one room (only the subway base); multiplayer (single player now, co-op later).
- **The first piece to run:** the smallest clue loop (ThoughtPad steps 5–11): raise the tablet in both hands in the base → in This PC, double-click and open two read-only faction testimonies → copy a few lines with the right-click menu → make a new memo and paste → save it to the desktop. The red pen comes later. The testimony text: (to be written by me).
- **How anyone would know it ran:** a recording from the game, labelled with its commit.

## 7. What could sink it?
Risk: this game is too big for one person; it suits a small studio better.
What I do about it:
- **Build the smallest version first:** leave the RPG and content variety for later, and build only the core design idea (sorting out clues on the tablet yourself) with as little content as possible. Expand once the core works.
- **Code that is easy to fix and easy to extend**, so that adding something later touches one or two places. Examples that can be shown now:
  - shared code instead of new code for every new thing: the right-click menu is one shell shared by every app (`computer_system/ui/`); the tablet in the hands and the small on-screen tablet are the same prefab;
  - every constant has a name, so a value used in several places changes once;
  - every tablet app is a folder that can be lifted out and run on its own with F6, in a debug scene with a stand-in data source (This PC, ThoughtPad);
  - apps send requests through one data entry point and never change data directly; the backend interface is designed like a remote service, so co-op will not change it;
  - software and document definitions are `.tres` files generated from my item spreadsheet by a conversion script, so numbers change only in the spreadsheet (the script and the spreadsheet are in Chinese and not in this repository);
  - a character is a body plus a brain: the player and later human enemies share one body and differ only in the brain; the look sits under a `Visual` node, so a new model needs no code change.
- **The art is commissioned from a friend.** 3D models do not come from generative AI: I tried paid online AI and locally run models, and in my use neither was good enough (I kept no records of those attempts).

## 8. Why this project?
Mostly **to learn**. Before this, I knew almost nothing about game development.
- **New to me:** the Godot engine, shaders, particles, animation and Blender, and using AI to turn my ideas into something real.
- **Already had:** some programming (Python / Java / C / C++ / C#), but it helped little in actual development; this repository holds no work from before the course to show it.
I chose it because it shows what I care about most: gameplay design. Once there is an art direction, AI and collaborators can help make the art; the gameplay I have to think up myself.

**About the film:** every game clip in it is scripted input recorded with Godot Movie Maker, not human play; drawings are labelled CONSTRUCTED, and designs that are not built are labelled PLANNED or WILL.

---

## Exists today (where to see it)
| What | Where |
|---|---|
| Subway base greybox, crates, chair, tablet model | course repository tag `a3` (ec51731a) |
| Shaders, materials, material audit | tag `zhe-l-a5` (0240fcd0) |
| Landing dust, dust in the light, wall switch (F), GPU measurement | tag `zhe-l-a6` (d32191dc) |
| Main character model (commissioned), one-hand raise / put-away animations, pixel head (Codex-generated), AnimationTree | tag `zhe-l-a7` (cd544630) |
| Two-hand raise and first-person view; the tablet system (windows, taskbar, minimize, show desktop); This PC (folders, connected drives list, Up); the right-click menu shell; the in-game clipboard; the ThoughtPad window (shows one document, takes typing, in its debug scene); `.tres` definitions generated from my spreadsheet | `assignment-8/walker-survival-shooting/godot/`, commit f13431bf (comments removed; snapshot of my working project, 2026-11-25 23:19) |

## Will exist
- ThoughtPad: keys into the tablet, typing, copy and paste from the right-click menu, new, manual save, ask to save on close; the red pen (draw, erase, undo)
- File operations: rename, delete, properties, read-only checks
- Faction testimony memos (read-only story documents) and one quest that gives only the final goal
- One app or flow that changes the world: a USB drive into the base computer, or a lock minigame. Which comes first is not decided; I will compare which systems each needs first (computer desk, inventory, a locked target) and then decide
- Walking while raising the tablet (needs animation layers and a walk cycle)
- A Windows desktop build, and a test report a stranger can rerun

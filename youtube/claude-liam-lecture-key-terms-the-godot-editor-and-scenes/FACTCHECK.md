# FACTCHECK - Key Terms: The Godot Editor and Scenes

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter; no beat needed rewording. No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Editor or docs, Computed, Simulation, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `34`, `four groups` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; The editor | PASS | Second-pass check against slide 2 step 1 and 01-walker-and-godot.md | none |
| 5 | B0102 | Explanation of: Scenes and nodes; How a game is built and kept together | PASS | Second-pass check against slide 2 step 2 and 01-walker-and-godot.md | none |
| 6 | B0103 | Explanation of: Clocks, input and signals; When code runs and how parts talk | PASS | Second-pass check against slide 2 step 3 and 01-walker-and-godot.md | none |
| 7 | B0104 | Explanation of: Bodies and contact; What can touch what, and what notices it | PASS | Second-pass check against slide 2 step 4 and 01-walker-and-godot.md | none |
| 8 | B0201 | Figures spoken: `3 nodes`, `7 nodes` | PASS | Each figure is printed on slide 3 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 9 | B0201 | Explanation of: Scene dock, Remote tab; in the book text; TELL THESE APART; Inspector | PASS | Second-pass check against slide 3 step 1 and 01-walker-and-godot.md | none |
| 10 | B0202 | Explanation of: FileSystem dock; editor or docs; Lists every file in the project, under res://.; 3 nodes | PASS | Second-pass check against slide 3 step 2 and 01-walker-and-godot.md | none |
| 11 | B0203 | Figures spoken: `160.0`, `192.0` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 12 | B0203 | Explanation of: in the glossary; The editor panel for viewing and editing properties.; Inspector; 192.0 | PASS | Second-pass check against slide 3 step 3 and 01-walker-and-godot.md | none |
| 13 | B0204 | Explanation of: editor or docs; Shows the selected node's signals and groups.; Node dock; Signals | PASS | Second-pass check against slide 3 step 4 and 01-walker-and-godot.md | none |
| 14 | B0301 | Explanation of: 2D, 3D and Script views; editor or docs; TELL THESE APART; Run Project | PASS | Second-pass check against slide 4 step 1 and 01-walker-and-godot.md | none |
| 15 | B0302 | Figures spoken: `player.gd:12` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 16 | B0302 | Explanation of: Output and Debugger; editor or docs; Error: player.gd:12 null instance | PASS | Second-pass check against slide 4 step 2 and 01-walker-and-godot.md | none |
| 17 | B0303 | Figures spoken: `Four things`, `60`, `2D Physics layer 4` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 18 | B0303 | Explanation of: Project Settings; in the book text; Project Settings; Physics ticks per second | PASS | Second-pass check against slide 4 step 3 and 01-walker-and-godot.md | none |
| 19 | B0304 | Explanation of: Run and Play buttons; editor or docs; Scene; Local | PASS | Second-pass check against slide 4 step 4 and 01-walker-and-godot.md | none |
| 20 | B0401 | Explanation of: Project; in the book text; TELL THESE APART; Scene | PASS | Second-pass check against slide 5 step 1 and 01-walker-and-godot.md | none |
| 21 | B0402 | Figures spoken: `3 [node] lines make 3 nodes` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 22 | B0402 | Explanation of: in the book text; Scene; FILE LINES BECOME NODES; [node name="Main" type="Node"] | PASS | Second-pass check against slide 5 step 2 and 01-walker-and-godot.md | none |
| 23 | B0403 | Explanation of: in the book text; The smallest building block: one object doing one job.; ONE NODE, ONE JOB; Sprite2D | PASS | Second-pass check against slide 5 step 3 and 01-walker-and-godot.md | none |
| 24 | B0404 | Figures spoken: `160 px/s`, `2.0 s`, `320 px` | PASS | Each figure is printed on slide 5 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 25 | B0404 | Explanation of: Script; in the book text; Attaches behaviour to a node; GDScript here.; A SCRIPT ADDS BEHAVIOUR | PASS | Second-pass check against slide 5 step 4 and 01-walker-and-godot.md | none |
| 26 | B0501 | Explanation of: Scene tree; in the book text; The live hierarchy of nodes in a running game.; TELL THESE APART | PASS | Second-pass check against slide 6 step 1 and 01-walker-and-godot.md | none |
| 27 | B0502 | Figures spoken: `0.5 s`, `radius 45`, `all four` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 28 | B0502 | Explanation of: Instance; in the book text; radius 45; 0.5 s | PASS | Second-pass check against slide 6 step 2 and 01-walker-and-godot.md | none |
| 29 | B0503 | Figures spoken: `30`, `radius 45`, `3 of 4` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 30 | B0503 | Explanation of: override | PASS | Second-pass check against slide 6 step 3 and 01-walker-and-godot.md | none |
| 31 | B0601 | Figures spoken: `2 s`, `120` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 32 | B0601 | Explanation of: Polling; in the book text; Asking every tick whether something has happened.; TELL THESE APART | PASS | Second-pass check against slide 7 step 1 and 01-walker-and-godot.md | none |
| 33 | B0602 | Figures spoken: `calls: 1, at tick 72`, `120` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 34 | B0602 | Explanation of: in the glossary; Code runs only when something announces that it happened.; Event-driven; POLLING: 120 ASKS | PASS | Second-pass check against slide 7 step 2 and 01-walker-and-godot.md | none |
| 35 | B0603 | Figures spoken: `5 connections` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 36 | B0603 | Explanation of: Signal; in the book text; A named event a node emits; other nodes connect to it.; 5 connections | PASS | Second-pass check against slide 7 step 3 and 01-walker-and-godot.md | none |
| 37 | B0701 | Figures spoken: `0.25 S`, `30 fps`, `7 frames`, `144 fps`, `36 frames` | PASS | Each figure is printed on slide 8 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 38 | B0701 | Explanation of: _process; in the book text; Runs once per rendered frame; the rate varies by machine.; TELL THESE APART | PASS | Second-pass check against slide 8 step 1 and 01-walker-and-godot.md | none |
| 39 | B0702 | Figures spoken: `60 times a second`, `15 physics ticks` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 40 | B0702 | Explanation of: in the book text; Runs at a fixed rate, 60 times a second by default.; _physics_process; 30 fps machine: 7 frames, 15 physics ticks | PASS | Second-pass check against slide 8 step 2 and 01-walker-and-godot.md | none |
| 41 | B0703 | Figures spoken: `ONE SECOND`, `4 px per frame`, `120 px`, `576 px`, `240 px` | PASS | Each figure is printed on slide 8 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 42 | B0703 | Explanation of: DISTANCE IN ONE SECOND; 30 fps, 4 px per frame; 120 px; 144 fps, 4 px per frame | PASS | Second-pass check against slide 8 step 3 and 01-walker-and-godot.md | none |
| 43 | B0801 | Explanation of: Input action; in the book text; A named intent such as jump, bound to keys or buttons.; TELL THESE APART | PASS | Second-pass check against slide 9 step 1 and 01-walker-and-godot.md | none |
| 44 | B0802 | Figures spoken: `true on 30 ticks`, `true on 1 tick` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 45 | B0802 | Explanation of: Just-pressed vs held; in the book text; ONE PRESS, 60 TICKS (1 S); button down | PASS | Second-pass check against slide 9 step 2 and 01-walker-and-godot.md | none |
| 46 | B0901 | Figures spoken: `0 px` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 47 | B0901 | Explanation of: StaticBody2D; in the book text; Not moved by physics; others collide with it.; TELL THESE APART | PASS | Second-pass check against slide 10 step 1 and 01-walker-and-godot.md | none |
| 48 | B0902 | Figures spoken: `5 bounces` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 49 | B0902 | Explanation of: RigidBody2D; in the book text; tick 239 of 240: 5 bounces. Gravity 960 px/s² moves it.; A rigid body falls and bounces: the engine moves it. | PASS | Second-pass check against slide 10 step 2 and 01-walker-and-godot.md | none |
| 50 | B0903 | Explanation of: in the book text; CharacterBody2D; velocity (200, 160): is_on_floor() true from tick 108. | PASS | Second-pass check against slide 10 step 3 and 01-walker-and-godot.md | none |
| 51 | B0904 | Explanation of: in the book text; Area2D; body_entered at 0.98 s; body_exited at 1.85 s; speed never changed | PASS | Second-pass check against slide 10 step 4 and 01-walker-and-godot.md | none |
| 52 | B1001 | Figures spoken: `counts from 1`, `layer 4 · value 8`, `layer 5` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 53 | B1001 | Explanation of: Collision layer; in the book text; Where an object is: the layers it appears in.; TELL THESE APART | PASS | Second-pass check against slide 11 step 1 and 01-walker-and-godot.md | none |
| 54 | B1002 | Figures spoken: `1, 4 and 5`, `layer 3` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 55 | B1002 | Explanation of: in the book text; Collision mask; mask 25 | PASS | Second-pass check against slide 11 step 2 and 01-walker-and-godot.md | none |
| 56 | B1003 | Figures spoken: `1 + 8 + 16 = 25`, `value 8`, `collision_layer = 4`, `layer 3, not 4` | PASS | Each figure is printed on slide 11 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 57 | B1003 | Explanation of: Bitmask; in the book text; Player mask; 16 | PASS | Second-pass check against slide 11 step 3 and 01-walker-and-godot.md | none |
| 58 | B1101 | Figures spoken: `128 px`, `54 px` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 59 | B1101 | Explanation of: Collision shape; in the book text; The geometry physics uses, separate from the drawn sprite.; TELL THESE APART | PASS | Second-pass check against slide 12 step 1 and 01-walker-and-godot.md | none |
| 60 | B1102 | Figures spoken: `Tick 4`, `Discard 2 ticks` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 61 | B1102 | Explanation of: Area snapshot; in the book text; TICKS; 0 | PASS | Second-pass check against slide 12 step 2 and 01-walker-and-godot.md | none |
| 62 | B1201 | Figures spoken: `all 5 mobs`, `not in it (3)` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 63 | B1201 | Explanation of: Group; in the book text; A named tag on nodes; one call reaches every node in it.; TELL THESE APART | PASS | Second-pass check against slide 13 step 1 and 01-walker-and-godot.md | none |
| 64 | B1202 | Figures spoken: `autoload 12` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 65 | B1202 | Explanation of: in the book text; A script or scene kept loaded across scene changes.; Autoload; menu.tscn | PASS | Second-pass check against slide 13 step 2 and 01-walker-and-godot.md | none |
| 66 | B1203 | Figures spoken: `192`, `160` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 67 | B1203 | Explanation of: in the book text; Resource; Tuning.speed 192; Player | PASS | Second-pass check against slide 13 step 3 and 01-walker-and-godot.md | none |
| 68 | B1204 | Explanation of: Export preset, template; in the book text; Preset; files, output, options | PASS | Second-pass check against slide 13 step 4 and 01-walker-and-godot.md | none |
| 69 | B1301 | Figures spoken: `main.tscn: 1 node`, `at least 13 nodes` | PASS | Each figure is printed on slide 14 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 70 | B1301 | Explanation of: PAIR 1 · LEFT; Scene; A saved tree of nodes, in a file.; main.tscn: 1 node | PASS | Second-pass check against slide 14 step 1 and 01-walker-and-godot.md | none |
| 71 | B1302 | Figures spoken: `7 calls`, `60 a second`, `15 calls` | PASS | Each figure is printed on slide 14 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 72 | B1302 | Explanation of: PAIR 2 · LEFT; _process; Once per frame; the rate varies.; 7 calls, uneven gaps | PASS | Second-pass check against slide 14 step 2 and 01-walker-and-godot.md | none |
| 73 | B1303 | Figures spoken: `layer 2`, `scans layer 1`, `scans layer 4`, `scans layer 5` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 74 | B1303 | Explanation of: PAIR 3 · LEFT; Collision layer; Where an object is.; Player | PASS | Second-pass check against slide 14 step 3 and 01-walker-and-godot.md | none |
| 75 | B1304 | Figures spoken: `54 px`, `128 px` | PASS | Each figure is printed on slide 14 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 76 | B1304 | Explanation of: PAIR 4 · LEFT; Collision shape; What physics uses.; 54 px wide, unchanged | PASS | Second-pass check against slide 14 step 4 and 01-walker-and-godot.md | none |
| 77 | B1401 | Figures spoken: `layer 2 (value 2)`, `add 2`, `1 becomes 3`, `mask 1`, `mask 3` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 78 | B1401 | Explanation of: “make the player touch the coin”; WHAT THE INSTRUCTION DOES; mask 1: coin on layer 2?; no | PASS | Second-pass check against slide 15 step 1 and 01-walker-and-godot.md | none |
| 79 | B1402 | Figures spoken: `60 ticks a second`, `7 in 0.25 s`, `36 in 0.25 s`, `15 in 0.25 s` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 80 | B1402 | Explanation of: “make movement the same on every computer”; _process, 30 fps: 7 in 0.25 s; _process, 144 fps: 36 in 0.25 s; _physics_process, both: 15 in 0.25 s | PASS | Second-pass check against slide 15 step 2 and 01-walker-and-godot.md | none |
| 81 | B1403 | Figures spoken: `0.5 s`, `true on 30`, `true on 1` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 82 | B1403 | Explanation of: “jump when I press space”; is_action_pressed: true on 30; is_action_just_pressed: true on 1; 30 jumps against 1 for a 0.5 s press | PASS | Second-pass check against slide 15 step 3 and 01-walker-and-godot.md | none |
| 83 | B1404 | Figures spoken: `2 s`, `120 questions`, `1 call` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 84 | B1404 | Explanation of: “tell the main scene when the player dies”; polling: asks in 2 s 120; signal: calls in 2 s 1; 120 questions against 1 call | PASS | Second-pass check against slide 15 step 4 and 01-walker-and-godot.md | none |
| 85 | B1405 | Figures spoken: `1 node`, `13 nodes` | PASS | Each figure is printed on slide 15 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 86 | B1405 | Explanation of: “show me what the game really contains”; saved main.tscn: 1 node; running (Remote tab): 13 nodes; 1 + 7 + 2 + 1 + 1 + 1 = 13 nodes, at least | PASS | Second-pass check against slide 15 step 5 and 01-walker-and-godot.md | none |
| 87 | B1501 | Figures spoken: `Six checks` | PASS | Each figure is printed on slide 16 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 88 | B1501 | Explanation of: Before you trust a Godot change | PASS | Second-pass check against slide 16 step 1 and 01-walker-and-godot.md | none |
| 89 | B1502 | Explanation of: Before you trust a Godot change | PASS | Second-pass check against slide 16 step 2 and 01-walker-and-godot.md | none |
| 90 | B1503 | Explanation of: Before you trust a Godot change | PASS | Second-pass check against slide 16 step 3 and 01-walker-and-godot.md | none |
| 91 | B1504 | Explanation of: Before you trust a Godot change | PASS | Second-pass check against slide 16 step 4 and 01-walker-and-godot.md | none |
| 92 | B1505 | Figures spoken: `2^(n−1)` | PASS | Each figure is printed on slide 16 at step 5 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 93 | B1505 | Explanation of: Before you trust a Godot change | PASS | Second-pass check against slide 16 step 5 and 01-walker-and-godot.md | none |
| 94 | B1506 | Figures spoken: `layer 2, mask 3` | PASS | Each figure is printed on slide 16 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 95 | B1506 | Explanation of: Before you trust a Godot change | PASS | Second-pass check against slide 16 step 6 and 01-walker-and-godot.md | none |
| 96 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 97 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 5 (The scene tree and instances), step 2: the caption ends on '4 of 6 instances follow the template (radius 45).' but only four instances are drawn. In renderTree the count vis = Math.floor(t / 0.6 * 4) is never clamped to 4, so it reaches 6 by the end of the step. It should say '4 of 4'. The narration says four.
- Slide 14 step 1 and the last line of slide 15 put the coin on layer 2 ('Put the coin on layer 2 (value 2)', 'layer 2, mask 3'). Slide 10 puts the Player on layer 2 and the Coin on layer 3 (value 4), and Chapter 4 names layer 2 'Player'. By slide 10's own picture the exact instruction would be 'coin on layer 3 (value 4); add 4 to the player's mask'. Slide 14 also starts the player's mask at 1 where slide 10 gives it 25.
- Two different example games share the file name main.tscn and are never told apart. Slides 2 to 4 show main.tscn with 3 nodes (Main, Player, MobTimer, the Dodge the Creeps shape) and 7 nodes in the Remote tab. Slides 13 and 14 say 'main.tscn: 1 node' and 13 running nodes (walker-jumpman). The Inspector on slide 2 also shows Player Layer 1, Mask 1 while slide 10 says the Player is on layer 2 with mask 25. A viewer can take these as contradictions. The narration names Walker on slide 13.
- Slide 1 says '34 terms from Chapters 1 and 4, the glossary and the Godot editor', but export preset and template come from Chapter 15 (slide 12 cites it).
- Slide 14 step 1: the 'yes' label is clipped. It is white text right-aligned at x=580 on a red bar that ends at x=574, so its last letter falls off the bar onto white.
- Slide 10 steps 1 and 2: the Player's own layer ('layer 2 · value 2') is printed at the top left of the picture, far from the Player box, so it looks like a heading and not the Player's label.
- Slide 12 step 4: the caption says of preset and template 'Both must match your engine.' Chapter 15 only says templates are kept by exact engine version; a preset is a recipe for one platform. The same caption runs into the TELL THESE APART box below it, and the step sits under the badge 'Illustrative data' though it shows no data.
- Slide 3 step 4: with player.tscn open in the main screen, the Scene dock still lists Main, Player and MobTimer, the nodes of main.tscn. Slide 3 step 1: the Script view shows 'extends Area2D' (a player script) under the file label main.tscn.
- Slide 9 step 2: the counter stops at 'tick 239 of 240'.
- Slide 11 step 1 and slide 13 pair 4: 'sprite 128 px wide' at 'scale 0.80' implies art 160 px wide, which is never shown, and the caption says 'Swap the art' while the picture scales it.
- Wording differs between the course glossary and the slides: the glossary defines Polling as asking 'every frame' and Just-pressed as true 'on the frame a button went down'; slides 6 and 8 say 'every tick' and 'the tick'. Term names also vary inside the deck: the map says 'Run buttons', 'layer' and 'mask' where the slides say 'Run and Play buttons', 'Collision layer' and 'Collision mask'.

## Open after the second pass

- slide 14 step 1 (and slide 15 step 6): the slide puts the coin on layer 2 and starts the player's mask at 1, while slide 10 puts the Player on layer 2, the Coin on layer 3 (value 4) and the player's mask at 25; chapter 4 names layer 2 Player. The narration follows each slide as printed, so the film repeats the deck's inconsistency; settling it needs a deck change, not a narration change.

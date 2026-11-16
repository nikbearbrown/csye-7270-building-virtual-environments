# Deck problems found while scripting the Key Terms films

**What this is.** Every problem the script writers and second readers found on the 25 CSYE 7270 terminology decks (`glossary/decks/`), deck by deck. None of the decks was changed. The narration never repeats a wrong slide as fact: where a slide is wrong, the film's voice follows the chapters, but the slide itself still shows the problem on screen. Most items are small (a label over a line, a rounding); the ones that teach something wrong are listed in the summary below.

## Summary: slides that teach something wrong

- **11 Shader foundations, slide 3 step 4** (the newer step): draws one vertex shader feeding fragment shaders A, B and C in a chain. Each material's shader has its own vertex stage. Slides 9, 14 and 15 also say `source_color` always decodes; Chapter 6 says Walker's 2D renderer does not.
- **04 Walker and the toolchain, slides 8 and 12**: credit pinning the time step with making walker-jumpman repeatable; Chapter 0 says that fix was Pong's. Slide 10 calls a regression test "protects the behaviour you changed".
- **08 Blender interface, slide 9**: apply transforms "bakes position, rotation and scale"; Chapter 3 applies rotation and scale only. Slide 10 sets right-handed against Y up as opposites.
- **09 Blender to Godot, slide 6 step 3**: shows the unapplied prop's measured size as a red failure beside a caption saying only the scale check catches it.
- **02 Game design B, slide 8**: the 62% and 86% captions are swapped against their bars.
- **19 Game AI perception, slide 2**: the look-alike box says sight range needs a clear line to the target; elsewhere it is distance only.
- **23 Godot Unity Unreal, slide 7**: prints `area_entered` for a body entering an area (Godot emits `body_entered`).
- **14 Particles, slide 13 step 3**: the one-shot and looping labels are swapped.
- **12 Materials, slide 11 step 4**: "16 texels share a pixel" should be 256.
- **17 Animation and interaction, slides 10 and 14**: show the pre-fix scene passing a mutation check that Chapter 11 says failed.


Generated 2026-11-13 from each `extract/NN/narration.json` (`deck_problems`) and `extract/NN/verify.json` (`unresolved`).

## 01 Game design A (Key Terms: What a Game Is)

- Slide 11, pair 1 ('Goal (the experience)': what the player should feel and do) defines Goal differently from slide 2 and the glossary ('The objective the player works toward'). Its partner 'Tactic' is not one of the 22 terms and is defined nowhere else in this set (the source notes assign goals versus tactics to deck C). The narration calls it Goal 'in its other sense'.
- Slide 5 steps 2 and 3: the red blast square includes the cube's own cell, so 9 and then 25 red cells are drawn while the captions say '8 cells hit' and '24 cells hit' (renderTheme colours every cell with |x-3|<=rad and |y-3|<=rad, centre included).
- Slide 6: the alias 'also: Eight Kinds of Fun (Marc LeBlanc)' sits over a list of six kinds (fantasy, thrill, fellowship, mastery, exploration, creativity). The source notes describe LeBlanc's list with names such as challenge, narrative and discovery, so a viewer may expect eight items or take these six as LeBlanc's.
- Slide 10: the badge says Computed, but the note calls the tension curve 'an illustrative shape' (0.25 + 0.75 p cubed), so 0.80 and 0.34 are values of an invented formula. The payload bar and 'the other team' assume a team game the slide never explains.
- Slide 12 step 4: 'last 0.25 s to react' (the dark bar) sits beside 'player gets 0.5 s of warning' with nothing saying what the 0.25 s is. Step 1's caption '60-second minute' is redundant. The badge says Computed while the note says the numbers are examples.
- Slide 1 says '22 terms from four video lectures', but the slides cite two named videos plus 'a game design tips video (title to confirm)', and Goal, Player verb, Core loop and Mechanic are tagged as glossary or book terms. The '(title to confirm)' placeholder is still printed on slides 6 and 9.
- Slide 8 step 2: the 'door' label is drawn across the bottom edge of the door rectangle.

## 02 Game design B (Key Terms: Choices and Challenge)

- Slide 8 (Luck and skill) steps 2 and 3: the right-hand captions are one step out of sync with the bars. Step 2 adds the battle royale bar at 62% but its caption says 'Mostly skill: the stronger player wins 86% of matches.' Step 3 adds the Counter-Strike bar at 86% but its caption says 'A mix: 62%. A weaker player can still win with good loot...'. In renderLuck the second and third entries of the note array are swapped. The narration follows the bars.
- Slide 4 step 1: the caption says the safe player 'scores slower after about 17 s' (a typed-in string), while the chart, computed from the same curves, says 'pays off after 18 s' (80 + 20(t - 13) = 10t gives t = 18). The sentence is also off in meaning: the safe player scores slower from the rescue at 13 s; at 18 s the trade player's total overtakes. The narration says eighteen seconds.
- Slide 5 step 1: the caption ends 'Each differs from the others on both counts.' The grid says otherwise: imp and cacodemon are both dodgeable, and cacodemon and shotgun guy both stay back. Each enemy is in a different cell, but pairs share one count. The row label 'never misses' is also clipped to 'never miss' by the grid box.
- Slide 11 step 3: the Luck panel caption says 'skilled player wins about half', but the drawn squares show the skilled player winning 3 of 12 (seeded draw), a quarter. The narration says 'only part of the time'.
- Slide 11 step 2: the Trade-off and Persistence panels animate the same way (four shapes emptying one after another), so the picture does not show the difference the captions claim ('one swap, done' against 'spent for the whole stage').
- Slide 12 step 2: the chart for the shopkeeper instruction reuses the power-pellet picture from slide 4, with the line 'first four moments: pellets gone', which is not about the shop.
- Slide 12 step 5: the label 'consistent: damage 10 every time' is drawn across the red dots of the unpredictable row above it.
- Slide 3 is badged Illustrative data and its note says 'All inputs illustrative', but the invader and UFO points (10/20/30, 50/100/150, 300 on the 23rd shot) are the real Space Invaders values cited from the source video. The narration follows the badge and says 'made-up example' once; the badge or the note could say which numbers come from the source.
- Slide 4 step 2: two of the four 'moments' the pellets are spent on are a cherry and a 'blue ghost'; neither needs a power pellet, so the example reads oddly.
- Term name varies: the term is 'Personalisation' (slides 1 and 6) but the TELL THESE APART boxes on slides 5 and 6 say 'Personal choice'. The map lists 'unit differentiation' while slide 5 also gives 'orthogonal unit differentiation'.

Second reader, left for the deck author:
- slide 3 step 1: the narration calls the invader and UFO points (10 to 30, 50 to 150, 300 on the 23rd shot) a made-up example, following the Illustrative data badge, but the source notes give the UFO as worth 50 to 300 points from the source video; whether these values are illustrative or real is for the deck author to settle (the writer also flagged it).

## 03 Game design C (Key Terms: Pacing and Guidance)

- Slide 9 (Dynamic play), step 1: the caption says 'Total time 8 s', but the string is hard-coded. The four actions (durations 3, 5, 3 and 7 s, starting at 0, 1, 2 and 0, as the note says) all end by 7 s, and the bars stop at 7 on an 8-second axis. It should say 7 s. The narration does not speak the total.
- Slide 1 says '19 terms from three video lectures on game design', but the slides cite two videos (the tips video and Crash Course 'Game Design') plus the course glossary, and the title slide's note says the terms come from the tips video and the Crash Course lecture.
- 'Dynamic' is defined two ways in the course. The deck says 'Many things happening at once, so play stays fresh'. GLOSSARY-jargon-midterm.md (Game design documents) defines Dynamic as 'Behaviour that emerges when mechanics interact'. The slide does not say that the glossary uses the word differently.
- 'Spacing' also has two meanings in course material. The deck uses it for open against tight level spaces. RIOT-SERIES-TERMS.md (6.12) defines Spacing as how far an object moves between animation frames. 'Anticipation' is consistent between the two.
- Slide 8 (Games can cheat), step 2: the caption 'ambush: the guard never turned' can never appear. The player stops at 80 px from the guard, and that caption needs under 60 px, so the step ends on 'sneaking up from behind' and the ambush is never shown.
- Slide 10: the badge says Computed, but the note says the intensity curves are illustrative (only time in the band is computed from them). Slide 13 is also badged Computed over an assumed reaction time and illustrative curves. On slide 10 step 2 the paced curve dips below the band at the start, while the caption says peaks then rests keep the player in the band.
- Slide 10 step 2 note: 'The tower defence game alternates waves...' uses a definite article for a game that is never named or introduced.
- Slide 13 step 4: 'intensity at 90% of the way: 0.77' comes from a single curve (x to the power 2.5) that appears nowhere else; slide 6 shows the same build-up as three curves with sound 0.85, sparks 0.81, shake 0.73 at 90%.
- Slide 13 step 3: the instruction is '60 s of enemies, 30 s of calm, strongest wave last', but the chart is slide 10's sine curve, with equal high and low halves and four peaks, so it does not show the two-to-one timing or a strongest last wave.
- Slide 5 step 1: the labels 'move right' and 'jump' overlap each other and the red line, and 'blocks' and 'pit' sit on the line.
- Slide 3: one picture (the lit door) serves both Communication and Guiding the focus, so the picture cannot show the difference the TELL THESE APART box asks for. In step 1 the door is already drawn and visible, only unlit, so 'Nothing says where the goal is' is not quite what is shown.
- Slide 7 step 1: '2 of 4 events meet the expectation' counts a right and a wrong version of the same two events, so the fraction is built into the table rather than found.
- Slide 14 item 3 uses 'telegraphed', a word no slide defines. Slide 2's TELL THESE APART box sets Player purpose against Communication before Communication's entry appears (slide 3), and slide 3 step 1 shows the Guiding the focus box before its entry appears.
- GAME-DESIGN-TERMS-source-crashcourse.md lists 'goals versus tactics' among deck C's terms, but the deck has no such term; its 19 terms match the map without it.

## 04 Walker and the toolchain (Key Terms: Walker and the Toolchain)

- Slide 2 step 3: the middle commit is labelled '1 lines changed'; it should read '1 line changed'.
- Slide 4 carries the badge Computed, but its own note says the run lengths are illustrative and the 30 s limit is an example. The badge should be Illustrative data. The narration calls the run lengths made-up.
- Slide 6 step 2 is headed 'WITH AN ALLOW RULE FOR THE TEST' and the caption says the allow rule lets 'the one command you trust run unasked', but 'read a script' also flips from 'asks you' to 'runs' (renderPerm marks rows 0, 2 and 4 as ok). The drop from 6 to 3 prompts depends on that unexplained change. The six actions also list 'run the headless test' twice.
- Slide 12 step 3: the instruction says 'Allow only the test command', but the chart shows read, edit and run test all allowed ('3 allowed, 2 blocked'). On slide 6, even inside the sandbox, the edit still 'asks you'.
- Slide 7 step 2 pairs the vague 'make the ball faster' (the Pong ball) with the Chapter 1 change 'change speed 160.0 to 192.0', which is the walker-jumpman player's run speed in tuning.gd, not a ball. Slide 12 step 5 says 'make the player faster' correctly. The checkable version also says 'and pass the mechanics test' while its own result is 2 fails, and Chapter 1's prompt told the agent not to try to make a failing check pass; slide 12's wording 'then run the mechanics test' is the accurate one.
- Slide 10 step 1 shows the run-speed change as a line 'speed = 160.0' inside a .tscn scene beside position and visible. In walker-jumpman the speed lives in tuning.gd, a resource created in code, not in a scene file. As a conceptual picture it may mislead.
- Slide 10 step 2: the caption 'A regression test then protects the behaviour you changed' conflicts with the definition on the same slide, 'guards a behaviour that worked before'. Regression test is also introduced twice with the same definition, on slide 9 step 4 and slide 10 step 2.
- Slide 8 step 2 and slide 12 step 4 use the walker-jumpman timings (22.4 s real-time, 0.34 s pinned), and slide 8's caption says that with the step pinned the test 'then runs the same way every time'. Chapter 1 says walker-jumpman is immune to the time trap and gave identical results with and without the flag, so the pin bought speed, not repeatability, for this test. The Pong test in Chapter 0 is the case where pinning fixed flakiness.
- Slide 3 step 3: the headless output mixes Pong lines ('ball hits wall', 'score = 1') with '25 checks, 0 failures', the walker-jumpman mechanics-test count; Chapter 0's Pong test has ten checks.
- Slide 8: 'Fixed frame rate' is defined as 'Rendering locked to a set number of frames a second', but Chapter 0 says --fixed-fps forces each frame to be exactly 1/fps of game time and disables real-time sync; in a headless run nothing is rendered. The definition matches the course glossary, so the glossary row may want the same fix.
- Slide 12 step 4: the line '22.4 s real-time becomes 0.34 s' wraps so the unit 's' sits alone on its own line.
- Title slide speaker note says 'Deck 2 of the topic order' while the file and film are deck 04.

Second reader, left for the deck author:
- slide 10 step 1: the slide draws the run-speed change as a line inside a .tscn scene, but in walker-jumpman the speed lives in tuning.gd (a resource made in code, Chapter 1); the narration only describes the conceptual picture and makes no Walker claim, so it is left, but the slide may mislead.
- slide 8 step 2 and slide 12 step 4: the slides pair the walker-jumpman timings with 'the test then runs the same way every time'; Chapter 1 says walker-jumpman gave identical results with and without the flag (pinning bought speed only). The narration says 'identical results' and claims no repeatability gain for walker-jumpman, and attributes the flaky-to-deterministic fix to the Pong test (slide 9 step 4), matching Chapter 0; nothing to change, flagged for the deck.

## 05 Godot editor and scenes (Key Terms: The Godot Editor and Scenes)

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

Second reader, left for the deck author:
- slide 14 step 1 (and slide 15 step 6): the slide puts the coin on layer 2 and starts the player's mask at 1, while slide 10 puts the Player on layer 2, the Coin on layer 3 (value 4) and the player's mask at 25; chapter 4 names layer 2 Player. The narration follows each slide as printed, so the film repeats the deck's inconsistency; settling it needs a deck change, not a narration change.

## 06 2D art and sound assets (Key Terms: 2D Art and Sound Assets)

- Slide 2 step 3: the two ratio labels run into each other with no gap, so the screen shows 'image: 1024 ÷ 873 = 1.17viewport: 640 ÷ 360 = 1.78'. The same label writes 1024 with no comma, where the rest of the deck writes 1,024.
- Slide 7 step 2: the caption 'under one pixel: drawn at 44% strength, a faint smear' is true only if the shrink averages pixels. The course's own worked run resampled with nearest-neighbour and found the legs and antennae became broken dots, not a faint smear. Also the heading says the bugs are 'DRAWN AT HALF SIZE', but the '48 px, magnified ×6' bug is drawn about 288 px tall, which is ×6 at full size, not at the half-size scale of the others.
- Slide 9 step 2: the caption says '2,000 a second gives about 4' while the label above it says '4.5 samples per cycle'. The narration says four and a half.
- Slide 11 step 1: a stray pink dot is left between the 'Master bus' box and the caption at the end of the step (the moving signal dot stops outside the chain).
- Slide 12 step 3: 'peak 0.50 = -6.02 dB' uses an ASCII hyphen where every other negative decibel value in the deck uses the minus sign '−'.
- Slide 4: in renderSheet the four 'walk' frames differ only by a 3-pixel vertical bob, so the walk animation plays as a bounce in place. Step 4's heading says 'REAL TIME, 2 S' but the tick rows show one second of frames (5 and 12 ticks).
- Slide 6 carries the badge 'Simulation' for the whole slide, but only the lossy row in step 2 is modelled; the import lines in step 1 are from Chapter 2 and the mipmap sizes in step 3 are exact arithmetic.
- Naming: the map lists 'fringe' where the slide says 'Fringe (halo)', and pair 2 on the look-alike slide introduces 'Filtering', which is not one of the 34 map terms (the map has 'nearest vs linear').

Second reader, left for the deck author:
- slide 7 step 2: the slide says a 0.44 px leg is 'drawn at 44% strength, a faint smear', which holds only for an averaging shrink; Chapter 2's worked run resampled with Image.NEAREST and found legs and antennae 'reduced to broken dots'. Narration follows the slide ('a faint smear'); left as is.

## 07 Art principles and concept art (Key Terms: Concept Art and Character Art)

- Slide 2 (Clarity, satisfaction and style), step 2: the caption starts a sentence in lower case after a full stop: 'the game answers the press at once. a 40 ms answer feels immediate'.
- Slide 3 step 2: the printed luminances do not reproduce the printed ratio. With 'L 0.03 and 0.90' the formula (0.90 + 0.05) / (0.03 + 0.05) gives 11.88 : 1, not 11.23 : 1; the dark L must be about 0.035 before rounding. Print three decimals or say the L values are rounded. The caption also says 'from Chapter 6' on screen.
- Slide 3 step 4: 'odd 0.76 vs others 0.07, gap 0.68', but 0.76 minus 0.07 is 0.69 as printed (rounding of unrounded values).
- Slide 4 step 2: the knight-and-blob tell-apart score is not monotonic (0.45, 0.44, 0.42, then 0.53 at the smallest size), and the 6 x 6 cell panel shown as the headline is the size where the knight is least recognisable. The size axis (48, 24, 12, 6) has no unit.
- Slide 5 step 1: the heading says the outer squares fade, but renderFocus lowers the contrast of every square except the centre by the same amount, so the board fades evenly, not toward the edges; 'two outer neighbours' means any two neighbouring non-centre squares.
- Badges claim more than the notes: slide 5 and slide 9 are badged Computed, but the notes say the detail counts and the 0.35 falloff (slide 5), and the feature sizes and the 3 px rule (slide 9), are illustrative or invented. The narration calls those numbers made up.
- Slide 9 step 3: the caption says unreadable features are 'Dashed red', but at 64 px and 32 px they show only as small red specks, not visibly dashed.
- Slide 11 step 1: the caption names 'the rigid bar (dashed)', but at the end of the step the arm is fully stretched along the same line and covers the dashed bar, so the bar is not visible in the final picture. The second caption line ('Red rings: within reach ...') also crowds the TELL THESE APART heading below it.
- Slide 12 step 2: the mood board is '5 chosen', while slides 6 and 13 use boards of six images; and only about four of the five dots can be told apart because they overlap.
- Slide 13 step 1: the notes say the numbers are taken from earlier slides, but 1.2 : 1 and 4.2 : 1 appear on no earlier slide.
- Slide 13 step 2: the dashed 0.30 threshold line runs through the labels 'vs enemy blob 0.44' and 'vs near copy 0.06'.
- Slide 8 is badged Simulation (seeded), while step 1 rests on an assumed figure (5 seconds per sketch); the step says so, but the badge does not.

Second reader, left for the deck author:
- slide 3 step 1: the bar label prints 'SIZE × CONTRAST' and the narration says 'size times contrast', but the slide notes say the score is size squared times contrast ratio; the narration follows the printed label, which is true only if 'size' means area.
- slide 5 step 1: the narration says 'The outer neighbours are only two point four to one', following the slide label 'two outer neighbours' and heading 'OUTER SQUARES FADING'; the writer's deck note says every non-centre square is faded equally, so the board does not fade toward the edges. Left as printed; the deck label should be fixed.

## 08 Blender interface and modeling (Key Terms: The Blender Interface and Modeling)

- Slide 6 (Quads, triangles and the polygon count), step 2: the Polygon count entry says 'Three tallies of one mesh', but the chart beside it is titled 'FOUR TALLIES OF THE SAME CUBE' and the note says 'One mesh, four numbers'.
- Slide 10 (Units and the right-handed +Z up axes): the TELL THESE APART box sets 'Right-handed' against 'Y up (Godot)' as if they were opposites. Handedness and the up axis are separate properties, and Chapter 3 says Godot is right-handed too ('Godot is right-handed and Y-up'). The narration says Godot is right-handed as well.
- Slide 10 step 2 prints 'extents 0.2, 1.8, 0.2' and 'extents 0.2, 0.2, 1.8' for full sizes. The course glossary defines Extents as 'The half-sizes of a bounding box', so by that definition these are sizes, and the extents would be 0.1, 0.9, 0.1. The narration says 'Z extent' only as the slide's note and slide 14 do.
- Slide 13 step 2 (pair 2): Size is defined as 'The real dimensions in the mesh', but the picture shows 'size 1.00 m' worked out as 'scale × mesh = what you see' while 'the mesh is still 2 m'. By the printed definition the size in the mesh would be 2 m. The narration says 'the real dimensions you end up with' and leaves out 'in the mesh'.
- Slide 9 step 1: the grey divider line in the table runs through the red 'Size you see (m)' row, so that row looks struck through.
- Slide 9 step 1: the Apply transforms entry says 'Bake position, rotation and scale', but Chapter 3 and slide 14 step 4 apply Rotation & Scale only (the chapter's script passes location=False).
- Slide 12 step 3: the red curve from the checker texture runs across the label '← filled by the texture', striking it through. The image slot it points to stays an empty box.
- Slide 13 step 1 (pair 1): at the end of the step both turned squares overlap their own captions ('origin: the object's own point', 'pivot: set to a corner here'), so the captions are hard to read. Slide 13 step 4: the three unlabelled bars under 'colour, roughness, metal…' end with metal at about 0.8, while slide 12 step 3 shows Metallic 0.0.
- Slide 4 step 2 and slide 5 steps 2 to 4: the hidden back corner of the cube is drawn as a dot on top of the front face, so a vertex seems to float in the middle of a face (most visible at slide 5 step 4).
- Slide 4 step 1: the caption 'All 8 vertices moved together, 5.9 units' sits next to the note 'the mesh is untouched'. In Object Mode only the object's location changes, so 'vertices moved' can read as an edit to the mesh. The 5.9 is a screen distance (410 px over a 70 px drawing scale), not a value Blender would report.
- Slide 11 step 3: the picture is one face's outline whose corners double each level (4, 8, 16), but the labels under it give the whole cube's face counts (6, 24, 96). A viewer can take '24 faces' as the count for the one drawn outline.
- Slide 5 step 1: the Mesh entry and its note say 'the chapter calls it mesh data' and 'what the chapter means by mesh data'. In a standalone film there is no chapter on screen.

Second reader, left for the deck author:
- slide 10 step 2 and slide 14 step 3: the slide prints full sizes (0.2, 1.8, 0.2) as 'extents' and the course glossary defines Extents as half-sizes of a bounding box; the narration says 'Z extent' of one point eight only in Chapter 3's own sense ('puts Blender's Z extent on Godot's Y') and never speaks the slide's 'extents' line, so it is left as is, but the deck label should be checked.
- slide 9 step 1: the on-screen Apply transforms entry (and the course glossary) still read 'Bake position, rotation and scale', while the narration now follows Chapter 3's rotation and scale; the deck entry and glossary row may need aligning with Chapter 3.

## 09 Blender to Godot (Key Terms: Blender to Godot)

- Slide 6 step 3: the no_apply row prints MEASURED SIZE (2.0, 2.0, 2.0) in red as a failure, while the caption below says 'no_apply is drawn at the right size, so only the scale check catches it.' (2.0, 2.0, 2.0) is the mesh AABB; Chapter 3 gives no_apply's in-scene AABB as (0.2, 1.8, 0.2). The column mixes the two, so the size column and the caption contradict each other. Slide 12 step 1 repeats it ('no_apply 2.0 fail' for height in Godot's Y). The narration avoids saying which check catches no_apply.
- Slide 1 says '30 terms from Chapter 3 and the glossary', but four of the 30 (high-poly and low-poly, texture baking, version control, naming conventions) are tagged 'video only' and come from the Riot series, as the slide's own source line says.
- Slide 12 step 5 sets the box's 572 (Chapter 3's physics sampling) beside the hull's 52 (the deck's own 1 cm grid model; the chapter's sampling found 55, as slide 8 step 2 notes) under a 'Computed' badge, with no note that the two numbers come from different methods.
- Slide 3 step 2 shows the headless command 'Blender -b --factory-startup --python build_post.py' without --python-exit-code 1, the flag the next step of the same slide says to always add.
- Group names on the map do not match the slide eyebrows: the map's 'Export, import and collision' is 'Export and import' on slides 7 and 8, and the map's 'Measuring and budget' is split across 'Proving it', 'Budget' and 'Keeping it repeatable'.
- Slide 11 step 3 draws the collision shape as a plain box around base and pole, while slide 8 step 2 shows that box replaced by a tapered hull; the 12-triangle label fits either, but the picture is the superseded collider.

Second reader, left for the deck author:
- slide 6 step 3: the deck prints no_apply's MEASURED SIZE as a red (2.0, 2.0, 2.0) fail beside the caption 'only the scale check catches it'; Chapter 3 gives (2.0, 2.0, 2.0) as the mesh AABB and (0.2, 1.8, 0.2) as the AABB in the running scene. Narration says only that no_apply carries a scale and that only the good build passes, which Chapter 3 supports; the deck itself needs fixing (deck problem, not narration).
- slide 12 step 1: chart shows no_apply '2.0 fail' for height in Godot's Y; consistent with the slide's 'require the mesh to measure', since the mesh AABB is 2.0, but it can read as the drawn height. Narration speaks no no_apply figure; left as is.

## 10 Game design document (Key Terms: The Game Design Document)

- Slide 14 step 3: the exact instruction 'Return the player within 0.2 m of the respawn point within 2 frames at --fixed-fps 60' and its measured 0.0898 m are criterion 5, which Chapter 5 labels a constructed fixture (a direct state write after activation, below y = −12). The instruction leaves out how the state is reached and the activation, which slide 11 step 1 says every criterion must name and slide 12 step 1 is about.
- Slide 11 step 1, row 6 'old probes pass, 4 ≥ 4 checks' counts only input_probe.gd's four checks. Chapter 5's criterion 6 also requires feature_route.gd to still collect a coin, and slide 12 step 2 lists five old probes including 'a coin collected'. The two slides count the same invariants differently.
- Slide 6 steps 1 to 3 and slide 14 step 1: 64%, 17% and 18% add to 99% (rounding of 107, 29 and 30 of 166). Correct, but a viewer may think a claim is unaccounted for.
- Slide 11 step 3: the '0.0882 m: pass' label starts on the dashed 0.2 m ring, so its first digit sits on the line.
- Badges do not match their contents: slide 12 is 'Illustrative data' but step 3's 21, 19 and 2 are real numbers from the Chapter 12 audio session (its own caption says so); slide 8 is 'Computed' but step 2 is captioned 'Illustrative arithmetic'.
- Slide 7 step 2 (Mechanic Mirage) and slide 9 step 1 (Novelist's Trap): the TELL THESE APART box shows a pair that does not include the term just introduced (Ghost Center vs Implementation Void; Completeness Fallacy vs Stagnant Artifact), so the new term gets no look-alike.
- Slide 13 pair 1: 'tags: OBSERVED' for reverse simplifies; a reverse also writes INFERRED and MISSING tags (slide 3 step 1 shows 29 and 30).
- Slide 9 step 2: 'D-02 layer names, no reason recorded' reuses the ID of Chapter 5's real clawd decision D-02, which was a confident wrong decision with a stated reason, not a missing one. The table is labelled illustrative, but the shared ID may confuse.
- Term names vary: the map says 'observed, inferred, missing, assumption' and 'cut/defer/swap' where the slides say '[OBSERVED]' and 'Cut, defer, swap'; the course glossary says 'Brief' and 'Out-of-scope list' where the slides say 'Game brief' and 'Out of scope'.

## 11 Shader foundations (Key Terms: Shader Foundations)

*Filmed from the newer copy in `decks/`; the study copy in `glossary/decks/` is older.*

- Slide 12 step 1: the heading reads 'OUTPUT = MIx(0.2, 0.9, X)'. renderCurves upper-cases the formula and then replace('X', 'x') swaps only the first X, which is the one inside MIX. It should read 'MIX(0.2, 0.9, x)'. The term is also printed 'Mix' while step, smoothstep and clamp are lowercase.
- Slide 9 step 1: the label declares 'uniform float flash_amount' but the note says 'GDScript sets it: amount = 0.5', a different name. On the deck that teaches that a misspelled uniform name silently does nothing, this reads as a mismatch.
- Slide 3 step 4 (the new step): fragment shaders A, B and C are drawn chained one under another below a single vertex shader, and the note says 'The vertex shader placed the geometry once'. Per-material fragment shaders run side by side, not in sequence, each material's shader has its own vertex stage, and a full-screen pass has its own vertex stage too. The picture mixes the two ideas. The step adds no glossary term.
- Slide 3: Fixed-function is defined as 'Old hardware steps that could be configured but not programmed', while the same slide labels today's rasterization and blending as fixed-function. The definition and its use differ.
- Slide 1 says '33 terms from Chapter 6 and the glossary', but vertex colour is tagged 'video only', step, smoothstep and clamp 'editor or docs', and Linear vs sRGB cites Chapter 7.
- Slide 2 step 3: the caption 'color = (221, 119, 91) (156 of 156 pixels)' gives the colour of the last pixel only, but reads as if all 156 pixels are that colour; the disc visibly has a pale glint.
- Slide 4 step 3: the printed weights 0.32, 0.44 and 0.23 add to 0.99 while the caption says 'weights sum to 1.00' (rounding).
- Slide 7: the texture has a fixed red tile at (5, 2) that never matches the probe, which ends on tile (3, 6); a viewer can take the red tile for the probe's texel. The probe at u = 0.50 also sits exactly on a tile boundary, so 'tile (3, 6)' comes from floating-point rounding; slide 8 step 2 has the same boundary case at UV (0.50, 0.80).
- Slides 9 step 3, 14 step 5 and checklist item 5 present the source_color decode as unconditional. Chapter 6 says the Compatibility renderer, which Walker uses, does no sRGB-to-linear conversion for canvas uniforms, and Forward+ and Mobile convert in 2D only when the viewport renders in HDR. So the 'washed out' fix may not apply to the course's own 2D game. The narration uses a 3D example for source_color.
- Slide 10 step 3: node A and node B each get their own bracket, with 'one shared material' between them, so the drawing reads as two materials rather than one.

Second reader, left for the deck author:
- slide 3 step 4: the drawing chains one vertex shader into fragment shaders A, B and C with the captions 'places the geometry once' and 'One vertex shader, then as many fragment shaders as you like', and the note says 'The vertex shader placed the geometry once'; per-material shaders each have their own vertex stage and do not run one after another, and a pass over the finished image works on a 2D picture; the narration no longer repeats the claim but the picture on screen still shows it, so the slide needs redrawing.
- slides 9 step 3, 14 step 5 and 15 step 5: the slide text itself ('decoded to linear for the maths', 'so sRGB values decode to linear before the maths') still presents the source_color decode as unconditional, which Chapter 6 contradicts for 2D; the narration now hedges but the on-screen words do not.
- slide 9 step 1: the slide declares 'uniform float flash_amount' while its 'GDScript sets it' label reads 'amount = 0.5'; the narration follows the chapter's name flash_amount, but the label on screen still shows the other name.
- slide 3 step 2: the narration adds that on older graphics hardware 'every step worked like this'; the glossary says only 'Old hardware steps that could be configured but not programmed', so this is historically plausible but not stated in the reference files; left as written.

## 12 Materials and textures (Key Terms: Materials and Textures)

- Slide 11 step 4: '16 texels share a pixel (minification)'. A 1024 texture drawn 64 pixels wide puts 16 texels per pixel along each axis, so 256 texels share each screen pixel. The code uses tpp = 1024 / 64. The narration says 'many texels'.
- Slide 14 step 1: the chart for the exact instruction 'metallic 1.0, roughness 0.3' shows specular 0.00 as well as diffuse 0.00, so the fix looks like a black surface. The sampled normal [0.3, 0.3, 0.9] lies outside the narrow roughness-0.3 highlight. Slide 3 step 3 shows the metallic-1 sphere with a highlight. The narration speaks only the diffuse drop.
- Slide 14 step 2 says 'tilt must be 0°', while its own chart and slide 4 step 4 give 0.3° for the correct linear read (unpacked +0.004). The narration says 'about zero'.
- Slide 9 step 1: 'texel column 2, row 2 from the top' counts from zero, but the dot sits visibly in the third column and third row of the 4 × 4 checker. Nothing says the count starts at 0. The narration does not speak it.
- Slide 6 carries the badge 'Computed' while its note says the SSAO bars use illustrative inputs. The same SSAO 0.80 case is reused on slide 13 pair 2, also under 'Computed'. The narration calls both a made-up example.
- Slide 13 pair 1 says 'highlight 45° wide' for roughness 0.85, while slide 3 step 2 calls 45° the half-width and gives it for roughness 0.90. In halfWidth() the exponent clamps at 2 from about roughness 0.84 up, so 0.85 and 0.90 both give 45°.
- Slide 12 step 1: the box moves out and back (kf 0, 1, 0), so the step ends with both rows identical and the baked-versus-real-time difference shows only mid-animation. The step sits under the badge 'Illustrative data', though its shadow is computed per cell and only step 2's bounce factor is illustrative.
- Slide 10: step 2 draws the 8 m wall four times taller as well as longer than the 2 m wall, so its checker squares look the same size. Step 3 then draws the same wall as a thin strip the height of the 2 m wall. The caption 'four times coarser' is not visible in step 2's picture.
- Slide 13 pair 2, left: the remaining ambient part is drawn in the same dark ink as the direct part, so the bar reads dark, grey, dark and looks like a gap, not a dimmed ambient part. The right bar uses red for it.
- Term names differ between the map and the slides: the map lists 'linear' and 'green channel', and the slides title them 'Linear and decoding' and 'Green channel convention'. Slide 8 step 3 puts the 'ORM texture → HDRP Mask Map' row under the heading 'Unity URP Lit / HDRP', though that row is HDRP only.

## 13 Shader verification (Key Terms: Shader Verification)

- Slide 9 step 3 shows the Chapter 6 code (version A) against the spec oracle at 30 fps with 'gap 0.000', but slide 10 step 2 and Chapter 8 give the same known-good code an error of .030 (0.0303) at 30 fps. Likewise slide 5 step 4 gives the seeded frame counter 'max gap 0.000' at 60 fps and 0.485 at 30, where slide 10 step 2 shows the same seeded change at '.030' (60) and '.515' (30). The slide 5 and 9 figures look like ideal sampling with no physics-tick lag; nothing on those slides says so, so the two sets read as contradictions.
- Slide 5 step 4 uses a tolerance of one frame (0.061 / 0.030 / 0.013), while slide 10 calls 'one frame or one physics tick' oracle v1 (0.030 at 144 fps) and the corrected v2 'one frame plus one physics tick' (0.043 at 144). The assertion on slide 5 matches neither oracle, and is never told apart from them.
- Slide 13 says 'three pixels within 1 of the model', but the exact instruction on slide 12 step 1 samples body and eye pixels at three amounts, which is six samples (the chart shows only three rows, the body).
- Slide 11 pair 3 names the term 'Frame count', where slide 5 and the map use 'Frame counter'.
- Slide 4 step 2: the labels 'gap 0.25' and 'gap 0: hidden' sit on top of the curves, and the lower 'gap 0' label overlaps the axis 0, so they are hard to make out. Slide 12 step 3: the red tolerance line cuts through the word 'seeded' and touches the '0.037' label.
- Slide 9 step 3: the explanation text breaks 'line 1 − t / 0.55' across two lines after the '1', so the next line starts with a minus sign.
- Slide 1 says '30 terms from Chapter 8 and the glossary', but slide 7 tags pixel diff 'editor or docs', its note says pixel diff is not in the chapters, and the course glossary has no pixel diff row.

Second reader, left for the deck author:
- slide 5 step 1: the slide defines pinned clock as 'a fixed frame rate: every frame the same length' (matching Chapter 8's --fixed-fps), while the midterm glossary row says 'a fixed time value so animated shaders render the same each run'; narration follows the slide and Chapter 8.

## 14 Particles and VFX (Key Terms: Particles and VFX)

- Slide 13 step 3 (pair 3, one_shot vs Looping): the counts and pictures are swapped. renderPairs draws five cycle blocks with '160 born in 3 s' under one_shot and one block with '32 born in 3 s' under Looping. Slide 4 step 3 (correctly) gives one_shot 32 and looping 160. The narration states the correct counts without pointing left or right.
- Slide 12 steps 2 and 3: the colour codes put fire at 30 degrees, only 30 degrees from team A's red at 0 degrees. By step 3's own rule (neighbouring hues within 30 degrees read as related), fire and team A would look related, so the example palette is a weak colour code.
- Glossary and slide define the GPU and CPU nodes differently: the glossary says GPU particles have 'many particles, less control' and CPU particles are 'flexible, fewer particles'; slide 9 says GPU nodes have 'more features' and CPU nodes 'wider hardware support'. Chapter 9's ClassDB table supports the slide.
- Slide 9 step 2 caption says '50,000 took 1.61 ms a frame in Chapter 9.' A chapter reference printed on a slide in a self-contained film. The cost is a headless --fixed-fps 60 measurement on one Mac, which the slide does not say.
- Slide 6 step 1: the caption 'mean drop: 219 px (½ × 300 × 1.2² = 216)' is drawn through the landing dots of the arcs, so the formula is partly covered.
- Slide 6 step 4: the header says 'ORANGE TO RED, FADING OUT', but because alpha falls to zero at the same time the ramp and circles look orange to pale pink; no red is visible.
- Slide 8 step 3: the top lane ('stopped, still on screen') shows only an empty dashed circle, no particles, so the point that particles are still on screen while the effect has stopped is not visible. The dashed circle barely touches the camera box.
- Slide 2 step 2: an emitter firing 12 a second with lifetime 1.5 s (the rules box) can hold at most 18 at steady state, but the counter reads 'alive now: 19 of 36 born' (an inclusive-endpoint count). The speaker note's 'gravity 260' (the arc) differs from the rules box 'gravity: 220' (the fountain); both are right for their own drawing but read as a conflict.
- Slide 14 step 2: the label 'explosiveness 0: births per 0.1 s' sits on the top border line of the chart box.
- TELL THESE APART boxes do not change with the step: slide 5 step 1 (emission shape) shows spread vs initial velocity, slide 7 steps 1 and 3 (texture, billboard) show additive vs alpha, and slide 12 steps 3 and 4 (analogous colours, timing curve) show shape language vs colour coding.

Second reader, left for the deck author:
- slide 13 step 3: the slide's labels are swapped (one_shot sits over five cycle blocks and '160 born in 3 s', Looping over one block and '32 born in 3 s'); Chapter 9 and slide 4 step 3 settle one_shot = 32 and looping = 160, and the narration follows them without pointing left or right, but the picture on screen contradicts the words until the deck is fixed.
- slide 4 step 3: the example calls the 3D platformer's bullet glow 'looping'; Chapter 9 says only 'a steady glow behind each bullet' (lifetime 0.4) and does not state one_shot is off. Left as is: a steady glow implies looping, but the chapter does not print it.

## 15 Animation principles (Key Terms: Animation Principles)

- Slide 5 (Timing, spacing, frame rate and speed scale), step 3: the caption says 'At 12 fps the dot jumps 113 px at the start; at 60 fps it jumps 23 px', but the computed labels on the same picture say 'biggest jump 109 px' and 'biggest jump 22 px' (680 x ease-out of 1/12 is 108.6, of 1/60 is 22.5). The caption numbers are hard-coded and wrong. The narration speaks 109 and 22.
- Slide 8 (Anticipation, squash and stretch, arcs), step 1: the readout ends on 'flight: 1.55 s', which is the time since the wind-up began (0.35 + 1.2), while the line above says 'then flight 1.2 s'. The readout's label should not be 'flight'. Not spoken.
- Slide 9 (Follow-through, overlap, secondary motion), notes: the tail spring is described as 'omega 14, damping ratio 0.22', but the code (SPR) uses w = 9 and z = 0.2. The step 1 caption 'settles in about 1 s' also does not match the graph, where the tail is still swinging visibly past 2 s of the 4 s plot.
- Slide 9 step 3: the caption says 'Keyed by hand: the head, 5 keys (diamonds)', but only three diamonds are visible, because the keys at 0 s, 1 s and 2 s are drawn at the same spot. The narration says only that the head is keyed.
- Slide 3 and slide 15 call step (discrete) an interpolation ('Which interpolation sits between the keys: linear, step or cubic?'). Chapter 10 keeps two settings apart: interpolation per track (nearest, linear, cubic) and update mode per value track (UPDATE_DISCRETE). In Godot's own words the step look is nearest interpolation or the discrete update mode, so the slide's grouping can mislead a student about where the setting lives.
- Slide 12 (Root motion, blend tree, state machine): step 1 gives the root track as '120 px per cycle', step 2 as '120 px/s'. They agree only if one cycle lasts one second, which the slide never states.
- Slide 14 step 1: the 'eased: peak 1.5' label is drawn on the linear line, struck through by it, and well below the red peak it names.
- Slide 2 step 4: 'Keys stored by the clip above: 3 tracks x 3 keys = 9' refers to a clip that is no longer on screen at that step (the tween picture has replaced it). Steps 3 and 4 also have the 'in the book text' badge of Clip sitting on its definition line, so 'tracks of values over time' runs under the badge.
- Slide 10 step 1: the 'joint' label is drawn under the forearm bone, which crosses through the word. Slide 11 step 3: the grey copied-angles arm runs down over the caption 'target scaled by reach ratio'.

Second reader, left for the deck author:
- slide 9 step 1: the follow-through example (the Walker sword's fast attack swings to 85 degrees, then settles at 75, from Chapter 10) is a real keyed overshoot and settle, but the deck defines follow-through as parts moving on after the body stops, and the sword clip animates only the blade with no separate body that stops. Neither the slide nor the references say whether an overshoot of the main moving thing counts. Left unchanged.

## 16 Animation foundations (Key Terms: Animation Foundations)

- Slide 6 step 4 (update mode): the heading says 'READ AT 0.075 S', but the two readouts follow the playhead to 0.300 s, so the final picture shows 'at 0.300 s: 1.00' and 'at 0.300 s: 1' and never the 0.075 s comparison (0.50 against 0) that the heading promises. The narration does not mention 0.075 s.
- Slide 6: the TELL THESE APART box (Immediate call vs Deferred call) belongs to callback modes only, but it is on screen from step 1 (Autoplay) and step 2 (animation_finished), where it does not apply.
- Slide 10: the TELL THESE APART box sets 'Timer wait: reads between updates' against 'Fixed frame rate: reads on a known frame'. In Chapter 10 the timer problem in walker-3d-ik (reading the pose between skeleton updates, 10 of 12) was fixed by reading in skeleton_updated, not by a fixed frame rate, and the chapter says the existing create_timer waits pass at any frame rate but cannot pin a frame. The box joins two separate fixes; the natural partner of 'timer wait' is skeleton_updated.
- Slide 12 step 5: the instruction is 'Run with --fixed-fps 120 and read the pose in skeleton_updated', but the chart (0, 7, 9 and 9 failed of 20) comes from the 2D sword timing test, which has no skeleton, so skeleton_updated played no part in those runs. The '0 of 20' to '9 of 20' labels also run over the chart's right border.
- Badges understate real data: slide 6 is 'Illustrative data' though step 3 (key on paper frame 12, observed frame 14) is a Chapter 10 measurement, and slide 10 is 'Simulation (seeded)' though 10 of 12, requested 2 observed 0, 4 of 8, 20 of 20 and 7, 9, 9 are all real Chapter 10 results; only the frame ticks and the 139 px are simulated. The reverse holds on slides 4, 5, 8 and 9, badged 'Computed' while their notes call the Bezier curve, audio clip, walk-cycle values, bone lengths and chain lengths illustrative.
- Slide 3 step 4: linear at 0.06 s is given as -14.0 degrees, a straight line between the first two keys, but the chapter prints a transition of 0.439427 on the first attack_fast key, so the real sword track would not read -14.0 there. The slide labels the track as the sword's.
- Slide 8 step 3 and slide 12 step 3: 'elbow bends 86°' and 'elbow bend: 41° at reach 100, 149° at 270' give the interior angle at the elbow (law of cosines, 85.7 degrees for 191 of 280), so a straight arm would 'bend' 180 degrees. 'Bend' reads the opposite way; 'elbow angle' would be clearer. The narration says 'bends to' on slide 8 and 'elbow angle' on slide 12.
- Slide 7 step 1 gives the Animation's fixed end value as 2.0, slide 11 pair 1 as 1.0, with the same picture idea; a viewer may take the two as a contradiction.
- Layout: on slide 8 step 4 the lower elbow and its circle are drawn over the caption 'Both elbows reach the target'; on slides 6 and 7 step 4 the caption runs straight into the 'TELL THESE APART' label; on slide 5 step 3 the still ends with all three speed-scale bars full and equal, so the end picture does not show that 0.5 takes longer; slide 9 step 2 says 'both hands within 0.0 px of the target'.

Second reader, left for the deck author:
- slide 3 step 4: narration says nearest 'takes the value of the closest key', which matches the deck's own vNear code, but the slide caption says 'nearest holds' and neither Chapter 10 nor the glossary says whether Godot's nearest picks the closest or the previous key; at 0.06 s both give -80, so the beat was left.
- slide 11 step 2: narration says 'only a loop needs its first and last values to match'; mechanically true (ping-pong reverses, so it never jumps), but Chapter 10's loop-seam test pairs matching values with loop_mode LOOP_LINEAR or LOOP_PINGPONG without separating them; left as is.

## 17 Animation and interaction (Key Terms: Animation and Interaction)

- Slide 8 (Startup, active, recovery): the illustrative split puts the hitbox on from frame 12 to frame 30 (0.10 s to 0.25 s), lined up with the method keys. But slide 7 and slide 14 step 4 show the sword's real keyed window as monitoring true at 0.0 s and false at 0.15 s, which has no startup at all. The notes tie 0.1 s and 0.25 s to 'its method keys', but those keys open the combo buffer and allow the next swing, they are not the hitbox window. A viewer can take slide 8 as the sword's real timing. The narration calls slide 8 a made-up example and does not tie its frames to the sword.
- Slide 8 steps 1 and 2: the caption under the bar names the frame the playhead has reached, not the section the step is about. Step 1, about startup, prints 'frame 12 of 54: active' and 'hitbox live: yes'. Step 2, about active, prints 'frame 30 of 54: recovery' and 'hitbox live: no'.
- Slide 10 step 1 shows the input probe's four assertions ticked in a 'no tree' column, and slide 14 step 5 says 'input probe on the pre-fix scene: 4 of 4 pass'. Chapter 11 only says the four assertions 'would pass' with the AnimationTree deleted, and records the probe run on the final scene, not on the pre-fix scene. The badge on slide 10 is Conceptual illustration, but the ticks look like results. The narration says 'would pass'.
- Slide 10 step 3 and slide 14 step 5: the pre-fix scene passes at the second-tick landing ('pass', '1 of 2 landings pass'). Chapter 11's real mutation check failed 2a and 2b at both offsets, because three hops hit the unlucky tick at least once. The note admits this, but the slide shows a single-landing simulation, so a viewer can think the real check passed at one offset.
- Slide 4 step 3: Condition is defined as 'A test on a parameter', but the caption says the test 'reads floor and vertical speed', which in the chapter's machine are advance expressions (is_on_floor(), velocity.y), not advance conditions on a parameter. The chapter separates the two settings.
- Slide 2 step 3: the bar labelled 'shooting' gets the gun blend's weight, but in Chapter 11 the gun Blend2's input is the clip 'shooting_standing', and that blend is filtered to upper-body bones, so 'weights add up to 1.00' over six whole-body clips is a simplification.
- Slide 3 step 3: 'air_dir is between 0 and 1 for 22 ticks' while Chapter 11 says it blends over 21 ticks; the note says 'near the chapter's 21', but the slide states 22 without that caveat.
- Slide 9: the tick numbers do not match the chapter's trace. In case 1 the floor is true on tick 136 and the take-off is on 137; in Chapter 11's trace the floor is true on tick 137 and vy is 12.50 on tick 138.
- Slide 11 step 1: the Unity table enters Run at speed 0.2 and lands back in Run at speed 0.0, because the drawn graph has no Jump to Idle arrow. It reads oddly for a speed-driven controller.
- Slide 1 says '34 terms' and the map's term lists name 28 terms plus 'Unity, Unreal'; the six engine terms (Animator Controller, Unity transition, Unity blend tree, Animation Blueprint, Transition rule, Conduit) are only on slides 11 and 12. The map also says 'current node' where slide 6 says get_current_node().
- Task numbering: the brief for this film calls the Unity and Unreal slides 12 and 13; in deck.json they are slides 11 and 12 (13 is the look-alike pairs). The narration follows deck.json.

Second reader, left for the deck author:
- slide 2 step 3: the slide gives the bar labelled shooting 0.60 of six whole-clip weights summing to 1; Chapter 11 says the gun Blend2's input is shooting_standing and the blend is filtered to upper-body bones. Narration follows the slide.
- slide 8: the illustrative split (hitbox on frames 12 to 30, tied in the note to the method keys at 0.1 s and 0.25 s) does not match the sword's real keyed window (monitoring true at 0.0 s, false at 0.15 s, Chapter 10; slides 7 and 14). Narration calls slide 8 a made-up example and gives no Walker numbers for it; the slide and note themselves still invite the confusion, and steps 1 and 2 print captions ('frame 12 of 54: active', 'frame 30 of 54: recovery') that describe the next section.

## 18 Camera (Key Terms: Camera)

- Slide 1, row 'Move the camera': the WHAT CHANGES cell says 'The position; the view direction stays', but orbit is in the same row and an orbit turns the camera to keep the subject framed (slide 5 shows the view direction sweeping 140°). True for dolly, truck and pedestal only. The narration says so.
- Slide 7 step 3: 'that is a 18 mm lens on the 36 mm sensor' should read 'an 18 mm lens'.
- Slide 10 step 1: in the perspective drawing the boxes overlap into two solid staircase shapes just under the horizon (renderProj: the 3 m box spans about x 216 to 302 and the 4.5 m box about 270 to 328), so the five separate boxes and the converging rows are hard to see, and the dashed row lines are hidden under the boxes.
- Slide 5: the notes say the pan is 'the same angle' and the step 2 caption says 'The same sweep done as a pan', but the orbit sweeps 140° and the pan turns 70°. The narration says only 'a sweep done as a pan'.
- Slide 15 step 2: 'limits: x between 120 and 520 px, so half the 200 px view stays inside' reads as if only half the view stays in the level. It means the view's half-width (100 px) is kept inside each level edge (20 and 620).
- Slide 4 step 1 and slide 12 step 1 show their TELL THESE APART box (Pedestal vs Tilt; Smoothing vs Deadzone) before the first term in it has been defined on that slide.

## 19 Game AI perception and pathfinding (Key Terms: Game AI, Perception and Pathfinding)

- Slide 2 (Agent, loop, hearing and memory): the TELL THESE APART box says Sight range 'needs a clear line to the target'. Slide 3, its own TELL box, slide 12 pair 1 and the glossary all say sight range is a distance and nothing else, and give the clear line to line of sight. The term is defined two ways. The narration follows slide 3.
- Slide 2 step 1: the caption says the guard patrols at 100 px/s, but the readout at the end of the step shows 'velocity (0, 0) px/s' (renderAgent sets vx to 0 once t reaches 1). Slide 2 step 2: the caption says it senses 168 px, while the still ends on 'd = 32 px'. The captions quote one moment of the animation and the readouts show another.
- Slide 2 step 3: the caption calls the hearing radius the 'dashed ring', but at the end of the step the dashed ring is hidden under the solid red expanding ring of the same 250 px radius.
- Slide 2 step 4: the guard's readout ends on the state 'home'. The chapter's guard states are Patrol, Chase and Search, and slide 13 step 5 says 'return to patrol'.
- Slide 3 step 1: the caption says a dot counts 'even behind a wall', but no wall is drawn until step 3.
- Slide 3 step 2 ends with the same counts as step 1 (G1 4, G2 4, either 6), and slide 13 step 1 shows '+ 70° cone: 6 of 12', so at rest the cone removes nothing. Slide 13 step 1 also captions '6, 6, 3' as 'each test removes targets', but those are the targets that remain.
- Slide 1 says '33 terms from Chapter 14 and the glossary', but nine of the entries are tagged 'outside source' (agent, hearing radius, field-of-view cone, wander, graph, breadth-first search, open and closed set, Euclidean distance, path smoothing).
- Slide 4 step 3: the 'safe 300' label sits on top of the red distance curve and is partly hidden by it.
- Slide 6 step 4: the flock ends jammed into the bottom-left corner of the arena, with its red ring cut off by the border.
- Slide 12 pair 4 gives 'closest pair 108 px' and 'mean distance to centre 26 px', while slide 6 gives 43 px and 19 px for the same two rules. Nothing says pair 4 is a separate run.
- Slide 9 step 2 names cells D2, C2, B2, A2 and slide 9 step 1 names H3, F3, D3, but the grid has no column letters or row numbers printed, so a viewer cannot find them.
- Slide 11 step 1: NavigationAgent2D is defined as following a navmesh path, but the picture shows the agent following the grid-cell route from slides 8 and 9.
- Slide 12 pair 1: the dashed sight-range circle is drawn across the 'Sight range' heading and the caption 'Tests only the distance to the target.'

Second reader, left for the deck author:
- slide 2 steps 1 to 4: the TELL THESE APART box on screen says sight range 'needs a clear line to the target', while slide 3, slide 12 pair 1 and the glossary ('How far an NPC can see') make sight range a distance only; the narration never repeats the slide 2 box and teaches sight range, field-of-view cone and line of sight as three separate tests (slide 3), but the box itself needs a deck fix.
- slide 2 step 4: the readout ends on 'guard state: home' and the renderer sends the guard back to its start point, which the narration describes; the Walker guard in Chapter 14 returns to Patrol instead, and the narration's Walker example says Patrol, so both are true to their source.

## 20 Game AI decisions and systems (Key Terms: Game AI, Decisions and Systems)

- Slide 4 (Conditions, actions, selectors and sequences), step 1: the two leaf rows contradict the slide's own tree. can_see returns FAILURE on tick 1 while chase returns RUNNING on tick 1, but in Sequence[can_see, chase] chase is not ticked when can_see fails. The rows read as if both leaves were ticked independently.
- Slide 7 step 3: the header says 'EACH REWARD × γ TO THE POWER OF ITS STEP', and the steps are numbered 1 to 5, but the last reward counts 0.815 = 0.95^4 and 0.063 = 0.5^4. The power is the step number minus one. The discounted returns 0.78 and 0.04 are right for that rule.
- Slide 11 step 1: 'gap too wide: 8 columns, limit 6'. In the drawing, the last reached column is 7 and the first unreached is 15, so the gap is seven empty columns; 8 is the jump distance, not the gap width.
- Slide 11 step 4 and slide 14 step 2: 44 of 200 accepted and '81 of the 200 levels the last column is a gap' come from the page's own generator, while the notes cite Lab B's limits. Lab B's run in Chapter 14 gave 43 of 200 and 16 levels ending in a gap. Nothing on screen says these levels are the page's own, so a viewer can take 44 and 81 as the course's results.
- Slide 14 step 2: the caption 'only 44 of 200 raw levels can be crossed' overclaims. Chapter 14 says a validator pass 'does not establish that an accepted level can be crossed'. 'pass the validator' would be accurate. The narration says 'pass'.
- Slide 14 is badged Computed, but step 3 shows the utility scores (chase 0.51, flee 0.41, patrol 0.42) whose weights slide 5 badges Illustrative data. The narration says 'made-up example' there.
- Slide 12 notes say '188.6, 113.0 and the 3 of 3 forged points are from the chapter's Lab C logs', but 113.0 appears on no step. Step 3 shows a simulated '13.0 px' instead, so the note looks stale or confused.
- Slide 2 step 1: the guard returns from Search to Patrol after 'wait 2 ticks', under the title 'A GUARD WITH THREE STATES' and a source naming Task 2, where the guard waits 1.0 s at the last known position. The notes call the run an illustrative script, but the picture does not say so.
- Slide 6 step 2: in the open_door row, the NEEDS text 'has_key, at_door' runs into the GIVES text '+door_open' with no space between them.

Second reader, left for the deck author:
- slide 14 step 2: 'In this run, forty-four of two hundred seeds pass' uses the page's own generator, while Chapter 14's Lab B run gave 43 of 200; the narration does not call it the course's result, but 'this run' does not say whose run it is.

## 21 Walkthrough film (Key Terms: The Walkthrough Film)

- Source lines on slides 6, 7, 8, 9, 11 and 12 misspell the skill as 'godot-waikthrough SKILL.md'; Assignment 10 calls it godot-walkthrough.
- Slide 11 step 1: the tall bars of the real-time capture animation are drawn over the heading, so it shows as 'Real-ti  cap re'.
- Slide 10 step 1: the definition places the disclosure 'in the first two shots', while the summary line and the slide 13 checklist say 'first two beats'; the summary line also says 'Say what the model is not' where the film or game is meant.
- Slide 5: Camera move is defined only as 'Pan, tilt, dolly, truck, orbit and the rest, defined in the 18 Camera deck', with the heading '(REF: TERMS - CAMERA)'. The term has no meaning of its own on the slide, and the pointer to another deck by number cannot be spoken in a self-contained film. The narration defines the four moves from the course glossary.
- Badges: slide 3 and slide 8 carry 'Computed', but their beat lengths and the 82 s film are the invented example from slide 2 ('Illustrative data'); only the arithmetic is computed. Slide 3's notes say so; slide 8's do not.
- Slide 7 step 2: under 'FRAMES IN A 10 S FILM' the tick rows still show one second of ticks (24, 30, 60), not 240, 300 and 600 frames; the summary line also breaks '10 / s' across two lines.
- Slide 11 step 4: the beat sheet side says 'words and seconds per beat' but the picture shows only seconds bars, no words.
- Slide 6 step 1: 'mean 24.8 ms = 40.4 fps'. 1000 / 24.8 = 40.3; 40.4 holds only if the unrounded mean is 24.76 ms or less. Worth checking the rounding.
- Slide 12 step 1: 'Linear keys at 1.25 m/s; ease only at rest' is unclear (ease only where the camera starts or stops from rest?). The narration keeps the slide's wording.
- Slide 3 step 2: the example script says Walker 'restarts at the last checkpoint'; the reference files do not mention checkpoints in Walker. The narration does not repeat it.
- Slide 0 notes say 'Deck 10 of the topic order' while the file is deck 21; fine if topic order differs from file order.

Second reader, left for the deck author:
- slide 10 step 1: the slide's What it is not entry says 'placed in the first two shots', while its own summary line, the 18 s of 82 s picture and the checklist (slide 13) say 'first two beats'; the reference files do not settle it; narration follows 'beats'.

## 22 Game trailer (Key Terms: The Game Trailer)

- Slide 1 (map) puts accessibility in the group 'Capture and honesty', but its entry is on slide 9 under the eyebrow 'Cutting and sound'.
- Slide 10 (Call to action and logo sting) carries the eyebrow 'Shape and length' but sits after the three 'Cutting and sound' slides (7 to 9), so the groups do not run in the map's order.
- Slide 12 step 1 marks 'slow motion or speed-up' as not allowed and cites 'Assignment 8, honesty rule', but Assignment 8 allows 'Scripted-input captures and slowed replays' when they are labelled. The narration does not mention slow motion.
- Slide 8 is badged 'Illustrative data', but step 3 is headed 'MEASURED ENERGY (RMS), SHIPPING LANE CUE' and the note says those values are measured, and step 1 is plain arithmetic. Only the rough cut times of step 2 are invented.
- Slide 8 step 2: 'The gate fails a cut with under 60% on the beat.' A single cut cannot be 60% on the beat; it presumably means a film whose cuts are under 60% on the beat fails.
- Slide 12's TELL THESE APART box is Trailer vs Gameplay video, which contrasts none of that slide's three terms (gameplay vs cinematic, honest trailer, viewer test), and gives Trailer as 'sells; keeps its promise' where slide 2 says 'sells; ends on one action'.
- Slide 2 tags Pitch film 'outside source', but the title-slide note defines outside source as the godot-trailer skill or general film vocabulary, and the slide itself says the pitch film comes from Assignment 8.
- Slide 5 step 2: '40 ÷ 4 = bar 10 exactly' is ambiguous. With the first beat at 0 s, beat 40 at 20.0 s is the first beat of the eleventh bar (ten bars completed). The narration says 'exactly ten bars of four, a downbeat'.
- Slide 9 step 3: the strips are titled 'BRIGHT FRAMES' but the flashes are drawn as dark blocks on a light ground, so a viewer can read the dark blocks as dark frames.
- Slide 13 pair 1 gives '12 shots in 60 s' and '3 shots in 20 s' with no source and no illustrative label; the slide's note does not say where the counts come from.
- The title slide's note says 'Deck 11 of the topic order'; this is deck 22 in the film set.

Second reader, left for the deck author:
- slide 10 step 2: the example plays the logo sting 'after the end card'; slide 14 step 4 says 'the logo goes last', but slide 5 and slide 10 step 1 say the trailer ends on the call to action. The deck does not settle whether the sting goes before or after the end card; narration left as written.

## 23 Godot Unity Unreal comparison (Key Terms: Godot, Unity and Unreal)

- Slide 10 (Animation: clip, event key, state machine), step 3: the final readout is 'speed = 0.8 attack = off state = Idle', but the drawn rule sends Idle to Walk when speed > 0.1. In renderAnim the speed stays 0.8 after 'attack finished' returns the state to Idle, so the last frame breaks the slide's own rule. No Walk-to-Idle transition is drawn either. The narration describes the transitions and does not speak 0.8.
- Slide 7 step 3: 'Godot: area_entered 1' for a BODY crossing the zone. In Godot a body entering an Area2D emits body_entered; area_entered is for another area. Chapter 4's Unity table pairs Area2D + body_entered with OnTriggerEnter2D. The narration does not name the signal.
- Slide 12 step 2: 'Personal plan: not available' compares a lifetime gross of US$1,500,000 with Unity's twelve-month finance threshold of US$200,000, two different bases. The step also sits under the badge 'Computed' while its revenue figure is labelled ILLUSTRATIVE. The narration says illustrative and does not speak the Unity verdict.
- Slide 11: the badge 'Simulation (seeded)' covers steps 1 and 2, which show where shaders live and a parameter call, not a simulation.
- Slide 4 step 3: Unreal's 'Sound' and 'Sound (bound twice)' are drawn as two separate listener boxes, so the picture reads as three listeners rather than one listener bound twice; 'Calls received: 3 of 3' reinforces that.
- Slide 9 step 1: the three axis gizmos are drawn identically (two axes each), so handedness, which the step names, cannot be seen in the picture; only the labels differ.
- Slide 13 pair 3: '39 frames in 0.25 s' comes from randomly jittered frame gaps; at the 144 frames a second used on slide 6, a quarter second holds 36 frames. '13 steps in 0.25 s' counts the tick at time zero (0.25 / 0.02 = 12.5).
- Slide 7 step 2: 'Character body' is defined as 'the body you move on purpose', but its Unity column, Rigidbody2D, can be dynamic (moved by physics); Chapter 1 gives 'Rigidbody2D (kinematic or dynamic)'.
- Map names differ from the slide entries: 'Collision Matrix' vs 'Layer Collision Matrix', 'Object Type' vs 'Object Type, response', 'Blueprint' vs 'Blueprint graph', 'C#' vs 'C# and MonoBehaviour', 'Shader', 'Parameter', 'Particles', 'Export' vs 'Shader and material', 'Material parameter', 'Particle system', 'Build and export'. Group 2 lists nine names for eleven terms because 'the clocks' stands for three entries.
- Title slide note says 'Deck 12 of the topic order' while the file is deck 23.

Second reader, left for the deck author:
- slide 7 step 3: the slide prints 'Godot: area_entered 1' for a body crossing the zone; chapter 4's Unity table pairs Area2D with body_entered, while chapter 0 and chapter 4's Unreal table use area_entered; the narration names no signal and says only that each engine reports the entry once, so it was left as is and the writer's body_entered finding is not repeated as fact.
- slide 7 step 2: the slide maps Character body ('the body you move on purpose') to Unity's Rigidbody2D, which chapter 1 lists as 'kinematic or dynamic'; narration follows the slide and does not call it kinematic.
- slide 3 step 4: Walker's tuning resource is a Resource class created with Tuning.new(), not loaded from a .tres file (chapter 1); chapter 1's own table maps it to a ScriptableObject asset, so the example was left.

## 24 Unity editor interface (Key Terms: The Unity Editor)

- Slide 8 (Prefab, Prefab Mode and the Overrides dropdown) step 1: the caption says 'One asset, five copies, each showing Value 1.' but the picture shows instances #2 and #4 with overrides of Value 5 and Value 7, and the counter below says 'Instances showing the prefab's value: 3 of 5'. The narration follows the picture.
- Slide 6 step 3: the label 'W held 2.0 s at 3 units/s: z = 2.0' reads as if 2 s at 3 units/s moved the camera 2 units. In renderNav the camera starts at z = 8 (z = 8 - 3*2*t), so 2.0 is the end position after 6 units of travel; the start position is never shown. The narration gives the time and speed only.
- Slide 6 step 4: the label under the Scene gizmo, which shows the view name in steps 1 to 3 (Right, Persp), switches to the tool name (Move, Rotate, Scale), so the gizmo appears to say 'Scale'.
- Slide 1 says '32 terms ... Each one is matched to its Godot part on the last term slide.' Slide 13 maps 11 rows, not 32 terms.
- Slide 4 step 2: the GAME VIEW strip is drawn over the 'TELL THESE APART' heading, which is half hidden.
- Slide 3 step 2: the Console error is 'NullReference: Player.cs:12', but the Project window lists only Move.cs and the Player's script component is PlayerMove; no Player.cs exists in the drawing. The Inspector's Speed also shows 5.0 again after step 1 set it to 7.5.
- Slide 14 pair 4 shows three people ('all 3 get the change') where slide 11 uses a team of four.
- Term names differ between the map and the term slides: the map says 'Import settings', 'changes lost', 'pivot handles' and 'orbit pan zoom', the slides say 'Asset import settings', 'Play Mode changes lost', 'Pivot and Local handles' and 'Orbit, pan, zoom'.
- Slide 8 cites the glossary for 'Overrides dropdown' with the tag 'in the glossary', but the glossary has Override, Apply, Revert, Prefab asset and Prefab instance rows and no 'Overrides dropdown' row. Likewise slide 1's note says 32 terms while 'Edit Mode', 'Prefab asset' and 'Prefab instance' appear only in TELL THESE APART boxes.

Second reader, left for the deck author:
- slide 6 step 4: the slide defines the Transform tools as 'Move, Rotate, Scale, Rect and Hand: the handles for changing a selection', and the narration repeats that list; in Unity the Hand tool pans the Scene view rather than changing the selection, but no reference file settles it, so the beat follows the slide (it only says Move, Rotate and Scale change the object).

## 25 Unreal editor interface (Key Terms: The Unreal Editor)

- Slide 9 (Material Editor, Niagara and the Animation editors), step 2: the Niagara particles spawn at the bottom edge of the viewport box and fall out of it (renderEditors, k 2: cy = 420 + v[1]*ts*0.6 + 0.5*300*ts*ts). At the end of the step they are scattered over the caption and the TELL THESE APART box, while the viewport, which says 'particles alive: 32', is empty.
- Slide 8 step 2: the Event Graph definition says 'white execution wires set the order', but the wires drawn are red and black; no white wire appears.
- Slide 6 step 5: the tab reads 'filter: Warning, Error', yet the Output Log still lists the plain line 'Door opened', which that filter would hide.
- Slide 6 step 4: the chart has two play markers, a bare play triangle at 1 s where the pink play zone starts and a 'Play' label at 3 s under the ramp where the door is edited. The 'Play' label reads as if play began at 3 s.
- Slide 6 step 3: the caption says 'player stays where it was', but the player is drawn near x 330, not where step 1 left it ('x = 550 px').
- Slide 3 step 1: the perspective cube spills below its box and its lower edge crosses the 'short edge ÷ long edge' label, covering the word 'long'.
- Slide 13 step 1: the Simulate ball comes to rest on the caption 'physics runs, nobody plays' and hides the word 'nobody'. No floor is drawn for it.
- Slide 4 step 1: the Content Drawer bar under the viewport overlaps the 'TELL THESE APART' heading.
- Slide 2 versus slide 5: SM_Cube is an asset in the Content Browser on slide 2 (the placed Actor is called 'Cube' in the Outliner), but on slide 5 SM_Cube is listed in the Outliner as a placed Actor.
- Slide 14 step 4: the exact instruction says only 'enable overlap events', not on both Actors. Chapter 4 says both Actors need Generate Overlap Events, and slide 10's caption says overlap needs both sides.
- Slide 11 step 4 names a pipeline box 'Package' (Cook, Package, Game folder), while slide 13 pair 4 defines Package as one saved asset file. The two senses of the word sit side by side without a note.
- Sources and notes disagree in small ways: slide 7's note cites Chapters 1, 4 and 5 for the binary quote while its source line lists Chapters 0, 1 and 5; slide 11's note says the plugins come from Chapters 0, 1 and 4 while its source line says Chapters 0 and 4; the title slide's note says 'Deck 15 of the topic order' for deck 25.

Second reader, left for the deck author:
- slide 14 step 4: the on-screen exact instruction reads only 'enable overlap events'; the narration now adds 'on both Actors' from Chapter 4, so the spoken words are fuller than the printed line (deck fix belongs to the deck author).
- slide 2 step 2: the narration calls SM_Cube 'a cube mesh' from the asset-name prefix; the slide does not say what SM_Cube is, and slide 5 lists SM_Cube in the Outliner as a placed Actor (already in deck_problems). Left as is.

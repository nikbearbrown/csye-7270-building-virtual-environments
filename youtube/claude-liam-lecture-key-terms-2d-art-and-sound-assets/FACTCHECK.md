# FACTCHECK - Key Terms: 2D Art and Sound Assets

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 1 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Editor or docs, Video only, Computed, Simulation, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `34` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; Size and pixels | PASS | Second-pass check against slide 2 step 1 and 02-prompting-game-art.md | none |
| 5 | B0102 | Explanation of: Frames and cutouts; How frames are cut and how edges stay clean | PASS | Second-pass check against slide 2 step 2 and 02-prompting-game-art.md | none |
| 6 | B0103 | Explanation of: Import, readability, collider; What the engine does to a file, and what the player sees | PASS | Second-pass check against slide 2 step 3 and 02-prompting-game-art.md | none |
| 7 | B0104 | Explanation of: Sound; How a sound is stored, looped, played and mixed | PASS | Second-pass check against slide 2 step 4 and 02-prompting-game-art.md | none |
| 8 | B0201 | Figures spoken: `1,024 × 873`, `893,952` | PASS | Each figure is printed on slide 3 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 9 | B0201 | Explanation of: Resolution; in the glossary; Width and height in pixels.; TELL THESE APART | PASS | Second-pass check against slide 3 step 1 and 02-prompting-game-art.md | none |
| 10 | B0202 | Figures spoken: `1.60`, `2.42`, `640 × 360` | PASS | Each figure is printed on slide 3 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 11 | B0202 | Explanation of: editor or docs; Viewport; SAME SCALE (0.4): FILE AND VIEWPORT; image 1,024 × 873 | PASS | Second-pass check against slide 3 step 2 and 02-prompting-game-art.md | none |
| 12 | B0203 | Figures spoken: `1.17`, `1.78` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 13 | B0203 | Explanation of: Aspect ratio; in the glossary; Width divided by height.; WIDTH ÷ HEIGHT, BOTH DRAWN 150 PX TALL | PASS | Second-pass check against slide 3 step 3 and 02-prompting-game-art.md | none |
| 14 | B0204 | Figures spoken: `0.412` | PASS | Each figure is printed on slide 3 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 15 | B0204 | Explanation of: Uniform vs non-uniform; in the glossary; SCALE FACTORS: 640 ÷ 1,024 AND 360 ÷ 873; Two factors: distorted | PASS | Second-pass check against slide 3 step 4 and 02-prompting-game-art.md | none |
| 16 | B0301 | Figures spoken: `6 × 6`, `36`, `0 (white)` | PASS | Each figure is printed on slide 4 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 17 | B0301 | Explanation of: Texel; in the glossary; One pixel of a texture.; TELL THESE APART | PASS | Second-pass check against slide 4 step 1 and 02-prompting-game-art.md | none |
| 18 | B0302 | Figures spoken: `4 TIMES`, `2 shades`, `24 shades` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 19 | B0302 | Explanation of: Nearest vs linear; in the book text; THE SAME SPRITE DRAWN 4 TIMES LARGER (24 × 24); nearest: 2 shades | PASS | Second-pass check against slide 4 step 2 and 02-prompting-game-art.md | none |
| 20 | B0303 | Figures spoken: `scale 2`, `scale 3`, `2.5`, `50%` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 21 | B0303 | Explanation of: Integer scaling; in the glossary; Scaling by whole numbers so pixel art stays crisp.; ON-SCREEN WIDTH OF EACH SPRITE PIXEL (SCREEN PIXELS) | PASS | Second-pass check against slide 4 step 3 and 02-prompting-game-art.md | none |
| 22 | B0401 | Figures spoken: `4 CELLS`, `48 × 48`, `192 × 48` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 23 | B0401 | Explanation of: Sprite sheet; in the book text; One image of many frames in a grid.; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 02-prompting-game-art.md | none |
| 24 | B0402 | Figures spoken: `144, 0, 48, 48` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 25 | B0402 | Explanation of: Texture atlas; in the book text; A FRAME IS A REGION OF THE SHEET; region = (144, 0, 48, 48) | PASS | Second-pass check against slide 5 step 2 and 02-prompting-game-art.md | none |
| 26 | B0403 | Figures spoken: `0, 1, 2, 3`, `5 FPS` | PASS | Each figure is printed on slide 5 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 27 | B0403 | Explanation of: in the book text; SpriteFrames; ONE ANIMATION: FRAMES, SPEED, LOOP; name: walk | PASS | Second-pass check against slide 5 step 3 and 02-prompting-game-art.md | none |
| 28 | B0404 | Figures spoken: `5 FPS`, `0.80 s`, `12 FPS`, `0.33 s` | PASS | Each figure is printed on slide 5 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 29 | B0404 | Explanation of: Frame rate; in the book text; Frames shown per second.; SAME 4 FRAMES, TWO SPEEDS (REAL TIME, 2 S) | PASS | Second-pass check against slide 5 step 4 and 02-prompting-game-art.md | none |
| 30 | B0501 | Figures spoken: `0.00`, `1.00`, `0.50` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 31 | B0501 | Explanation of: Alpha channel; in the glossary; The extra channel storing opacity.; TELL THESE APART | PASS | Second-pass check against slide 6 step 1 and 02-prompting-game-art.md | none |
| 32 | B0502 | Figures spoken: `alpha 1`, `alpha 0` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 33 | B0502 | Explanation of: in the book text; Transparent background; “TRANSPARENT” REQUEST VERSUS A CUTOUT; asked for “transparent” | PASS | Second-pass check against slide 6 step 2 and 02-prompting-game-art.md | none |
| 34 | B0503 | Explanation of: PNG vs JPEG; in the book text; Lossless with alpha versus lossy without alpha.; CHANNELS STORED PER PIXEL | PASS | Second-pass check against slide 6 step 3 and 02-prompting-game-art.md | none |
| 35 | B0504 | Figures spoken: `0.44`, `0.29` | PASS | Each figure is printed on slide 6 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 36 | B0504 | Explanation of: Fringe (halo); in the book text; ONE EDGE, SAMPLED IN 12 STEPS, OVER A DARK RED LEVEL; transparent texels store white | CORRECTED | Second-pass check against the slide and the chapter: 'until that option is on' implies fix_alpha_border starts off, but Chapter 2's texture-settings table gives process/fix_alpha_border as 'On (the default)', and the probed .import shows process/fix_alpha_border=true. | Reworded. Was: "Two strips sample one sprite edge over a dark red level. Fringe, or halo, is the pale rim of edge colour left around a cutout. Filtering blends in the colour st" |
| 37 | B0601 | Explanation of: Import settings; in the book text; TELL THESE APART; Lossless | PASS | Second-pass check against slide 7 step 1 and 02-prompting-game-art.md | none |
| 38 | B0602 | Figures spoken: `24 PIXELS`, `0.00`, `4 pixels`, `0.40` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 39 | B0602 | Explanation of: Lossless vs lossy; in the glossary; Exact reconstruction versus smaller files with lost detail.; SIMULATION: ONE ROW OF 24 PIXELS | PASS | Second-pass check against slide 7 step 2 and 02-prompting-game-art.md | none |
| 40 | B0603 | Figures spoken: `256 × 256`, `9 sizes`, `33%`, `1/4`, `64 × 64` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 41 | B0603 | Explanation of: Mipmaps; in the book text; A 256 × 256 TEXTURE AND ITS SHRUNK COPIES; 256 × 256 | PASS | Second-pass check against slide 7 step 3 and 02-prompting-game-art.md | none |
| 42 | B0701 | Explanation of: Silhouette; in the book text; TELL THESE APART; Silhouette | PASS | Second-pass check against slide 8 step 1 and 02-prompting-game-art.md | none |
| 43 | B0702 | Figures spoken: `×6`, `436`, `48 px`, `9.08`, `4 px`, `0.44` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 44 | B0702 | Explanation of: video only; Readability; 436 PX → 96 PX → 48 PX (DRAWN AT HALF SIZE); 436 px | PASS | Second-pass check against slide 8 step 2 and 02-prompting-game-art.md | none |
| 45 | B0801 | Figures spoken: `18 × 28`, `12 px` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 46 | B0801 | Explanation of: Collider; in the book text; TELL THESE APART; Collider | PASS | Second-pass check against slide 9 step 1 and 02-prompting-game-art.md | none |
| 47 | B0802 | Explanation of: FLIP THE ART: THE COLLIDER STAYS; keep the collider a sibling of the sprite, not its child | PASS | Second-pass check against slide 9 step 2 and 02-prompting-game-art.md | none |
| 48 | B0803 | Figures spoken: `12 px` | PASS | Each figure is printed on slide 9 at step 3 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 49 | B0803 | Explanation of: THE SPIKE OVERLAPS THE ART, THEN HITS THE BOX; the spike overlaps the art for 12 px before a hit; Art past the box is a design choice. Write down why. | PASS | Second-pass check against slide 9 step 3 and 02-prompting-game-art.md | none |
| 50 | B0901 | Figures spoken: `between −1 and 1`, `440 HZ`, `22,050`, `2.27 ms` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 51 | B0901 | Explanation of: PCM; in the glossary; Uncompressed digital audio samples.; TELL THESE APART | PASS | Second-pass check against slide 10 step 1 and 02-prompting-game-art.md | none |
| 52 | B0902 | Figures spoken: `22,050`, `50.1`, `2,000`, `4.5` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 53 | B0902 | Explanation of: in the glossary; Audio samples per second.; Sample rate; SAME TONE, TWO SAMPLE RATES, ONE CYCLE EACH | PASS | Second-pass check against slide 10 step 2 and 02-prompting-game-art.md | none |
| 54 | B0903 | Figures spoken: `22,050`, `11,025 Hz`, `15,000 Hz`, `7,050 Hz` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 55 | B0903 | Explanation of: in the glossary; Nyquist limit; PITCH HEARD VS PLAYED AT 22,050 A SECOND; Nyquist limit 11,025 Hz | PASS | Second-pass check against slide 10 step 3 and 02-prompting-game-art.md | none |
| 56 | B0904 | Figures spoken: `0.1251`, `440` | PASS | Each figure is printed on slide 10 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 57 | B0904 | Explanation of: Procedural synthesis; in the book text; NO FILE: A FORMULA FILLS THE BUFFER ONE SAMPLE AT A TIME; push_frame(Vector2.ONE * sin(phase * TAU)) | PASS | Second-pass check against slide 10 step 4 and 02-prompting-game-art.md | none |
| 58 | B1001 | Figures spoken: `4 S`, `44,100` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 59 | B1001 | Explanation of: WAV vs Ogg Vorbis; in the book text; TELL THESE APART; Loop point | PASS | Second-pass check against slide 11 step 1 and 02-prompting-game-art.md | none |
| 60 | B1002 | Figures spoken: `BEGIN 0`, `176,399` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 61 | B1002 | Explanation of: in the book text; Loop point; WAV: LOOP MODE FORWARD, BEGIN 0, END 176,399; loop begin | PASS | Second-pass check against slide 11 step 2 and 02-prompting-game-art.md | none |
| 62 | B1003 | Explanation of: in the glossary; Plays once and stops.; One-shot; LOOPING AND ONE-SHOT, PLAYED TOGETHER | PASS | Second-pass check against slide 11 step 3 and 02-prompting-game-art.md | none |
| 63 | B1004 | Figures spoken: `0.22`, `0.00` | PASS | Each figure is printed on slide 11 at step 4 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 64 | B1004 | Explanation of: THE SEAM: END OF THE LOOP, THEN THE START AGAIN; cut at u = 0.90, mid-cycle; jump 0.22 of full scale: a click; cut at the zero crossing | PASS | Second-pass check against slide 11 step 4 and 02-prompting-game-art.md | none |
| 65 | B1101 | Explanation of: AudioStreamPlayer; in the book text; Godot node that plays sound with no position.; TELL THESE APART | PASS | Second-pass check against slide 12 step 1 and 02-prompting-game-art.md | none |
| 66 | B1102 | Figures spoken: `40 ms`, `60 ms`, `default is 1` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 67 | B1102 | Explanation of: in the book text; Polyphony; MAX_POLYPHONY = 1 (DEFAULT): EACH PLAY CUTS THE LAST; three play() calls, 40 ms apart, on a 60 ms click | PASS | Second-pass check against slide 12 step 2 and 02-prompting-game-art.md | none |
| 68 | B1103 | Figures spoken: `MAX_POLYPHONY = 4`, `60 ms`, `20 ms` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 69 | B1103 | Explanation of: MAX_POLYPHONY = 4: THEY OVERLAP; four voices: each heard in full, 60 ms; the overlap is 60 − 40 = 20 ms between neighbours | PASS | Second-pass check against slide 12 step 3 and 02-prompting-game-art.md | none |
| 70 | B1201 | Figures spoken: `−12 dB`, `0 dB` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 71 | B1201 | Explanation of: Bus; in the book text; TELL THESE APART; Headroom | PASS | Second-pass check against slide 13 step 1 and 02-prompting-game-art.md | none |
| 72 | B1202 | Figures spoken: `−6 dB`, `0.501`, `−20 dB`, `0.100`, `−60 dB`, `0.001`, `−12 dB`, `0.251` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 73 | B1202 | Explanation of: Decibel; in the glossary; Logarithmic loudness unit.; AMPLITUDE = 10 ^ (DECIBELS ÷ 20) | PASS | Second-pass check against slide 13 step 2 and 02-prompting-game-art.md | none |
| 74 | B1203 | Figures spoken: `1.0`, `0.50`, `6.02 dB` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 75 | B1203 | Explanation of: in the glossary; Spare level left below the maximum.; Headroom; A SINE WITH PEAK 0.50 | PASS | Second-pass check against slide 13 step 3 and 02-prompting-game-art.md | none |
| 76 | B1204 | Figures spoken: `7.60 dB`, `1.20`, `37.2%` | PASS | Each figure is printed on slide 13 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 77 | B1204 | Explanation of: in the glossary; Distortion when a signal exceeds the maximum level.; Clipping; THE SAME SINE, TURNED UP BY 7.60 DB | PASS | Second-pass check against slide 13 step 4 and 02-prompting-game-art.md | none |
| 78 | B1301 | Figures spoken: `1,024 × 873`, `640 × 360` | PASS | Each figure is printed on slide 14 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 79 | B1301 | Explanation of: PAIR 1 · LEFT; Resolution; Pixels in the image file.; 1,024 × 873 | PASS | Second-pass check against slide 14 step 1 and 02-prompting-game-art.md | none |
| 80 | B1302 | Figures spoken: `4 sizes`, `4 texels` | PASS | Each figure is printed on slide 14 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 81 | B1302 | Explanation of: PAIR 2 · LEFT; Mipmaps; Pre-shrunk copies, chosen by size on screen.; 4 sizes of one texture | PASS | Second-pass check against slide 14 step 2 and 02-prompting-game-art.md | none |
| 82 | B1303 | Figures spoken: `22,050`, `5 a second` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 83 | B1303 | Explanation of: PAIR 3 · LEFT; Sample rate; Audio samples per second.; 22,050 a second: too many to draw | PASS | Second-pass check against slide 14 step 3 and 02-prompting-game-art.md | none |
| 84 | B1304 | Explanation of: PAIR 4 · LEFT; Loop point; Where playback jumps back to.; goes round again | PASS | Second-pass check against slide 14 step 4 and 02-prompting-game-art.md | none |
| 85 | B1401 | Figures spoken: `0.412`, `1.52 : 1` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 86 | B1401 | Explanation of: “make the art fit the game”; WHAT THE INSTRUCTION DOES; two factors: stretch 1.52 : 1; one factor: stretch 1.00 : 1 | PASS | Second-pass check against slide 15 step 1 and 02-prompting-game-art.md | none |
| 87 | B1402 | Figures spoken: `4×`, `24 shades`, `2 shades` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 88 | B1402 | Explanation of: “make the pixels crisp”; linear: 24 shades after 4× enlarging; nearest: 2 shades after 4× enlarging; nearest adds no new colours | PASS | Second-pass check against slide 15 step 2 and 02-prompting-game-art.md | none |
| 89 | B1403 | Figures spoken: `from 12`, `6 FPS`, `4-frame`, `0.67 s` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 90 | B1403 | Explanation of: “the walk is too fast”; 12 FPS: 0.33 s; 6 FPS: 0.67 s; 5 FPS (default): 0.80 s | PASS | Second-pass check against slide 15 step 3 and 02-prompting-game-art.md | none |
| 91 | B1404 | Figures spoken: `begin 0`, `176,399` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 92 | B1404 | Explanation of: “make the music loop”; sample 0; sample 176,399; both ends sit on 0: no click | PASS | Second-pass check against slide 15 step 4 and 02-prompting-game-art.md | none |
| 93 | B1405 | Figures spoken: `6 dB`, `1.20`, `0.60`, `1.0` | PASS | Each figure is printed on slide 15 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 94 | B1405 | Explanation of: “the effect is too loud and crackles”; before: peak 1.20 (clips at 1.0); after −6 dB: peak 0.60; the dashed line is the maximum, 1.0 | PASS | Second-pass check against slide 15 step 5 and 02-prompting-game-art.md | none |
| 95 | B1501 | Explanation of: Do frame count, layout and speed match the SpriteFrames? | PASS | Second-pass check against slide 16 step 1 and 02-prompting-game-art.md | none |
| 96 | B1502 | Figures spoken: `alpha 0` | PASS | Each figure is printed on slide 16 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 97 | B1502 | Explanation of: Before a generated asset goes in the game | PASS | Second-pass check against slide 16 step 2 and 02-prompting-game-art.md | none |
| 98 | B1503 | Explanation of: Before a generated asset goes in the game | PASS | Second-pass check against slide 16 step 3 and 02-prompting-game-art.md | none |
| 99 | B1504 | Explanation of: Before a generated asset goes in the game | PASS | Second-pass check against slide 16 step 4 and 02-prompting-game-art.md | none |
| 100 | B1505 | Explanation of: Before a generated asset goes in the game | PASS | Second-pass check against slide 16 step 5 and 02-prompting-game-art.md | none |
| 101 | B1506 | Explanation of: Before a generated asset goes in the game | PASS | Second-pass check against slide 16 step 6 and 02-prompting-game-art.md | none |
| 102 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 103 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 2 step 3: the two ratio labels run into each other with no gap, so the screen shows 'image: 1024 ÷ 873 = 1.17viewport: 640 ÷ 360 = 1.78'. The same label writes 1024 with no comma, where the rest of the deck writes 1,024.
- Slide 7 step 2: the caption 'under one pixel: drawn at 44% strength, a faint smear' is true only if the shrink averages pixels. The course's own worked run resampled with nearest-neighbour and found the legs and antennae became broken dots, not a faint smear. Also the heading says the bugs are 'DRAWN AT HALF SIZE', but the '48 px, magnified ×6' bug is drawn about 288 px tall, which is ×6 at full size, not at the half-size scale of the others.
- Slide 9 step 2: the caption says '2,000 a second gives about 4' while the label above it says '4.5 samples per cycle'. The narration says four and a half.
- Slide 11 step 1: a stray pink dot is left between the 'Master bus' box and the caption at the end of the step (the moving signal dot stops outside the chain).
- Slide 12 step 3: 'peak 0.50 = -6.02 dB' uses an ASCII hyphen where every other negative decibel value in the deck uses the minus sign '−'.
- Slide 4: in renderSheet the four 'walk' frames differ only by a 3-pixel vertical bob, so the walk animation plays as a bounce in place. Step 4's heading says 'REAL TIME, 2 S' but the tick rows show one second of frames (5 and 12 ticks).
- Slide 6 carries the badge 'Simulation' for the whole slide, but only the lossy row in step 2 is modelled; the import lines in step 1 are from Chapter 2 and the mipmap sizes in step 3 are exact arithmetic.
- Naming: the map lists 'fringe' where the slide says 'Fringe (halo)', and pair 2 on the look-alike slide introduces 'Filtering', which is not one of the 34 map terms (the map has 'nearest vs linear').

## Open after the second pass

- slide 7 step 2: the slide says a 0.44 px leg is 'drawn at 44% strength, a faint smear', which holds only for an averaging shrink; Chapter 2's worked run resampled with Image.NEAREST and found legs and antennae 'reduced to broken dots'. Narration follows the slide ('a faint smear'); left as is.

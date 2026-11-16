# FACTCHECK - Key Terms: Shader Verification

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 1 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Editor or docs, Computed, Simulation, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `30 terms`, `four groups` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; Where a claim stands | PASS | Second-pass check against slide 2 step 1 and 08-shader-verification.md | none |
| 5 | B0102 | Explanation of: Inputs you fix; Making a run repeatable and revealing | PASS | Second-pass check against slide 2 step 2 and 08-shader-verification.md | none |
| 6 | B0103 | Explanation of: Reading the output; Comparing pixels and values | PASS | Second-pass check against slide 2 step 3 and 08-shader-verification.md | none |
| 7 | B0104 | Explanation of: Checks on the checker; Trusting the test itself | PASS | Second-pass check against slide 2 step 4 and 08-shader-verification.md | none |
| 8 | B0201 | Figures spoken: `Five rungs`, `Four rungs run headless` | PASS | Each figure is printed on slide 3 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 9 | B0201 | Explanation of: Evidence ladder; in the book text; Five kinds of proof, each stronger than the last.; TELL THESE APART | PASS | Second-pass check against slide 3 step 1 and 08-shader-verification.md | none |
| 10 | B0202 | Figures spoken: `0 SHADER ERROR lines`, `rungs 2 to 5` | PASS | Each figure is printed on slide 3 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 11 | B0202 | Explanation of: Claim versus evidence; in the book text; What is said works, versus a check that shows it.; Claim: “it compiles”. Evidence: 0 SHADER ERROR lines. | PASS | Second-pass check against slide 3 step 2 and 08-shader-verification.md | none |
| 12 | B0203 | Figures spoken: `Rungs 1 to 4`, `Rung 5` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 13 | B0203 | Explanation of: Observed versus inferred; in the glossary; Seen in your own run, versus guessed from it.; observed | PASS | Second-pass check against slide 3 step 3 and 08-shader-verification.md | none |
| 14 | B0204 | Figures spoken: `exit 0, 11 checks pass`, `25 of 25 pass` | PASS | Each figure is printed on slide 3 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 15 | B0204 | Explanation of: Compile error; in the glossary; The shader fails to build and prints an error.; headless: yes | PASS | Second-pass check against slide 3 step 4 and 08-shader-verification.md | none |
| 16 | B0301 | Figures spoken: `7 checks` | PASS | Each figure is printed on slide 4 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 17 | B0301 | Explanation of: Headless mode; in the book text; A run with no window, so no pixels are drawn.; TELL THESE APART | PASS | Second-pass check against slide 4 step 1 and 08-shader-verification.md | none |
| 18 | B0302 | Figures spoken: `171 px differ`, `177 px differ` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 19 | B0302 | Explanation of: in the glossary; Drawing on the CPU: same output on any machine.; Software renderer; ONE SHADER, FOUR RENDERS | PASS | Second-pass check against slide 4 step 2 and 08-shader-verification.md | none |
| 20 | B0401 | Explanation of: Controlled input; in the book text; Every input fixed, so a run can be repeated.; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 08-shader-verification.md | none |
| 21 | B0402 | Figures spoken: `alpha 0 or 1`, `0.50`, `gap 0.25`, `searched 101 inputs` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 22 | B0402 | Explanation of: Exposing input; in the book text; Where right and wrong answers are far apart.; gap 0: hidden | PASS | Second-pass check against slide 5 step 2 and 08-shader-verification.md | none |
| 23 | B0403 | Figures spoken: `flash_amount 0.0`, `flash_amount 0.5`, `flash_amount 1.0` | PASS | Each figure is printed on slide 5 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 24 | B0403 | Explanation of: in the book text; A scene made to be looked at, inputs fixed.; Bench scene; THE BENCH: THREE CLAWDS, FIXED flash_amount | PASS | Second-pass check against slide 5 step 3 and 08-shader-verification.md | none |
| 25 | B0404 | Figures spoken: `0.0, 0.5, 1.0`, `7 headless checks pass` | PASS | Each figure is printed on slide 5 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 26 | B0404 | Explanation of: in the glossary; Fixed setup that a test starts from.; Test fixture; WHAT THE FIXTURE FIXES | PASS | Second-pass check against slide 5 step 4 and 08-shader-verification.md | none |
| 27 | B0501 | Figures spoken: `33 frames`, `0.23 s`, `0.26 s`, `--fixed-fps 60`, `0.55 s` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 28 | B0501 | Explanation of: Pinned clock; in the book text; A fixed frame rate: every frame the same length.; TELL THESE APART | PASS | Second-pass check against slide 6 step 1 and 08-shader-verification.md | none |
| 29 | B0502 | Figures spoken: `TWELVE RANDOM VALUES PER RUN`, `seed 7375` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 30 | B0502 | Explanation of: Random seed; in the glossary; A fixed starting number so random results repeat.; TWELVE RANDOM VALUES PER RUN | PASS | Second-pass check against slide 6 step 2 and 08-shader-verification.md | none |
| 31 | B0503 | Figures spoken: `1 − n / 33`, `33 frames last 1.10 s at 30 fps`, `0.55 s at 60`, `0.23 s at 144` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 32 | B0503 | Explanation of: in the book text; A fade that counts frames, not game seconds.; Frame counter; FRAME COUNTER AT 60 FPS: flash = 1 − n / 33 | PASS | Second-pass check against slide 6 step 3 and 08-shader-verification.md | none |
| 33 | B0504 | Figures spoken: `60 fps`, `max gap 0.000`, `30 fps`, `max gap 0.485`, `144 fps`, `max gap 0.583` | PASS | Each figure is printed on slide 6 at step 4 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 34 | B0504 | Explanation of: Assertion; in the glossary; A statement a test requires to be true.; COUNTER (RED) AGAINST SPEC LINE (BLACK) | PASS | Second-pass check against slide 6 step 4 and 08-shader-verification.md | none |
| 35 | B0601 | Figures spoken: `stored 128 of 255`, `as colour: 0.216`, `as data: 0.502` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 36 | B0601 | Explanation of: source_color; in the book text; A hint: this texture holds colour, so decode it.; TELL THESE APART | PASS | Second-pass check against slide 7 step 1 and 08-shader-verification.md | none |
| 37 | B0602 | Figures spoken: `(128, 128, 255)`, `lit at 1.000`, `tilt 38.8°`, `lit at 0.779` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 38 | B0602 | Explanation of: Flat normal texel; in the book text; The pixel (128, 128, 255): a surface facing out.; FLAT NORMAL (128,128,255), LIT FROM ABOVE | PASS | Second-pass check against slide 7 step 2 and 08-shader-verification.md | none |
| 39 | B0603 | Figures spoken: `ALPHA 0.5`, `result 0.50`, `result 0.25` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 40 | B0603 | Explanation of: Premultiplied alpha; in the book text; Colour already multiplied by its alpha.; WHITE AT ALPHA 0.5 OVER BLACK | PASS | Second-pass check against slide 7 step 3 and 08-shader-verification.md | none |
| 41 | B0701 | Explanation of: Golden image; in the glossary; also: reference image; A saved correct picture to compare renders with. | PASS | Second-pass check against slide 8 step 1 and 08-shader-verification.md | none |
| 42 | B0702 | Figures spoken: `tolerance 0`, `209 of 256`, `9 real-defect pixels` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 43 | B0702 | Explanation of: editor or docs; A count of the pixels where two images differ.; Pixel diff; new render | PASS | Second-pass check against slide 8 step 2 and 08-shader-verification.md | none |
| 44 | B0703 | Figures spoken: `tolerance 2`, `9 of 256`, `3 × 3` | PASS | Each figure is printed on slide 8 at step 3 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 45 | B0703 | Explanation of: Tolerance; in the book text; The allowed gap between expected and actual.; tolerance 2 (of 255 per pixel) | PASS | Second-pass check against slide 8 step 3 and 08-shader-verification.md | none |
| 46 | B0704 | Figures spoken: `161 px`, `184 px`, `0 px vs its own reference` | PASS | Each figure is printed on slide 8 at step 4 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 47 | B0704 | Explanation of: Per-platform reference; in the book text; One reference per platform, as they differ slightly.; PIXELS DIFFERING FROM A'S GOLDEN (OF 256) | PASS | Second-pass check against slide 8 step 4 and 08-shader-verification.md | none |
| 48 | B0801 | Figures spoken: `30 GOOD, 30 BAD`, `tolerance 14`, `false passes: 30 of 30` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 49 | B0801 | Explanation of: False positive; in the glossary; also called a false pass; A check passes though the thing is wrong. | PASS | Second-pass check against slide 9 step 1 and 08-shader-verification.md | none |
| 50 | B0802 | Figures spoken: `tolerance 1`, `false passes: 0 of 30`, `false fails: 28 of 30` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 51 | B0802 | Explanation of: False negative; in the glossary; also called a false fail; A check fails though the thing is right. | PASS | Second-pass check against slide 9 step 2 and 08-shader-verification.md | none |
| 52 | B0803 | Figures spoken: `tolerance 5`, `2 of 30`, `8 of 30`, `10 wrong of 60` | PASS | Each figure is printed on slide 9 at step 3 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 53 | B0803 | Explanation of: tolerance 5; false passes: 2 of 30 · false fails: 8 of 30 | PASS | Second-pass check against slide 9 step 3 and 08-shader-verification.md | none |
| 54 | B0901 | Figures spoken: `amount 0.0`, `amount 0.5`, `amount 1.0` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 55 | B0901 | Explanation of: CPU model; in the book text; The spec written as arithmetic that runs headless.; TELL THESE APART | PASS | Second-pass check against slide 10 step 1 and 08-shader-verification.md | none |
| 56 | B0902 | Figures spoken: `1 − t / 0.55`, `retry_remaining / 0.55` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 57 | B0902 | Explanation of: Test oracle; in the book text; The source of the right answer a test compares to.; A TEST COMPARES OUTPUT WITH AN ORACLE | PASS | Second-pass check against slide 10 step 2 and 08-shader-verification.md | none |
| 58 | B0903 | Figures spoken: `spec at 30 fps` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 59 | B0903 | Explanation of: Specification oracle; in the book text; An oracle taken from the spec, not the code.; THREE VERSIONS OF THE FADE, TWO ORACLES | PASS | Second-pass check against slide 10 step 3 and 08-shader-verification.md | none |
| 60 | B1001 | Figures spoken: `amount 0.0`, `3 of 3`, `amount 0.5 only` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Computed; file list illustrative. | none |
| 61 | B1001 | Explanation of: Mutation check; in the book text; Break the code on purpose; the test must fail.; TELL THESE APART | PASS | Second-pass check against slide 11 step 1 and 08-shader-verification.md | none |
| 62 | B1002 | Figures spoken: `Oracle v1 failed good code at 144 fps`, `60 fps` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Computed; file list illustrative. | none |
| 63 | B1002 | Explanation of: in the book text; A new check must fail on bad code, pass on good.; Test the test; KNOWN-GOOD / KNOWN-BAD: ERROR VS TOLERANCE | PASS | Second-pass check against slide 11 step 2 and 08-shader-verification.md | none |
| 64 | B1003 | Figures spoken: `default 0.5` | PASS | Each figure is printed on slide 11 at step 3 (machine check, check_narration.py). Badge: Computed; file list illustrative. | none |
| 65 | B1003 | Explanation of: Uniform value check; in the book text; Compare a shader input's value with the spec.; CHECKS ON THREE BROKEN SHADERS (FAIL = CAUGHT) | PASS | Second-pass check against slide 11 step 3 and 08-shader-verification.md | none |
| 66 | B1004 | Figures spoken: `7 FILES CHANGED`, `2 files, 8 changed lines` | PASS | Each figure is printed on slide 11 at step 4 (machine check, check_narration.py). Badge: Computed; file list illustrative. | none |
| 67 | B1004 | Explanation of: Scope violation; in the glossary; Changing something the brief said not to touch.; DIFF OF THE EVIDENCE STAGE: 7 FILES CHANGED | CORRECTED | Second-pass check against the slide and the chapter: The slide defines a scope violation as changing something the brief said not to touch ('A change to a file it ruled out'), but the example's brief never ruled the patrol script out, so it described unrequested extra work (closer to the glossary's scope creep) rather than a true instance. | Reworded. Was: "A diff of seven changed files. A Scope violation is changing something the brief said not to touch. This brief said, do not edit the shader, the player script o" |
| 68 | B1101 | Figures spoken: `SHADER ERROR: 0` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 69 | B1101 | Explanation of: PAIR 1 · LEFT; Claim; “It compiles”.; “it compiles” | PASS | Second-pass check against slide 12 step 1 and 08-shader-verification.md | none |
| 70 | B1102 | Figures spoken: `difference 4`, `difference 9` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 71 | B1102 | Explanation of: PAIR 2 · LEFT; False pass; Check passes, thing is wrong.; bad render, difference 4 | PASS | Second-pass check against slide 12 step 2 and 08-shader-verification.md | none |
| 72 | B1103 | Figures spoken: `33 frames`, `1.10, 0.55, 0.23`, `0.55 at every rate` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 73 | B1103 | Explanation of: PAIR 3 · LEFT; Frame count; 33 frames, any rate.; 33 frames | PASS | Second-pass check against slide 12 step 3 and 08-shader-verification.md | none |
| 74 | B1104 | Figures spoken: `stored 128`, `0.216`, `0.502` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 75 | B1104 | Explanation of: PAIR 4 · LEFT; source_color; Decode as colour.; stored 128, decoded as colour | PASS | Second-pass check against slide 12 step 4 and 08-shader-verification.md | none |
| 76 | B1201 | Figures spoken: `0.0, 0.5, 1.0`, `within 1 of the model` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 77 | B1201 | Explanation of: “check the shader looks right”; WHAT THE INSTRUCTION DOES; 0.0; #dd775b | PASS | Second-pass check against slide 13 step 1 and 08-shader-verification.md | none |
| 78 | B1202 | Figures spoken: `30, 60 and`, `144` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 79 | B1202 | Explanation of: “make sure the fade is the right length”; 30 fps; error 0.030, tolerance 0.091; 60 fps | PASS | Second-pass check against slide 13 step 2 and 08-shader-verification.md | none |
| 80 | B1203 | Figures spoken: `144 fps`, `0.037`, `0.569` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 81 | B1203 | Explanation of: “check the test is any good”; known-good: error at 144 fps; 0.037; seeded (bad): error at 144 fps | PASS | Second-pass check against slide 13 step 3 and 08-shader-verification.md | none |
| 82 | B1204 | Figures spoken: `tolerance of 2 of 255`, `3 × 3`, `209 px at 0`, `9 px at 2` | PASS | Each figure is printed on slide 13 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 83 | B1204 | Explanation of: “ignore tiny differences”; 0; 8; tolerance | PASS | Second-pass check against slide 13 step 4 and 08-shader-verification.md | none |
| 84 | B1205 | Figures spoken: `184 lines`, `8 lines` | PASS | Each figure is printed on slide 13 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 85 | B1205 | Explanation of: “make sure it only touched the flash”; inside the brief: 184 lines; outside the brief: 8 lines; changed lines by path (illustrative) | PASS | Second-pass check against slide 13 step 5 and 08-shader-verification.md | none |
| 86 | B1301 | Explanation of: Which rung of the ladder is my claim standing on?; Are the inputs fixed: clock, seed and bench?; Does my input separate the right answer from the wrong one?; Does my tolerance catch the bug and still pass good code? | PASS | Second-pass check against slide 14 step 1 and 08-shader-verification.md | none |
| 87 | B1302 | Explanation of: Before you trust a shader change | PASS | Second-pass check against slide 14 step 2 and 08-shader-verification.md | none |
| 88 | B1303 | Explanation of: Before you trust a shader change | PASS | Second-pass check against slide 14 step 3 and 08-shader-verification.md | none |
| 89 | B1304 | Explanation of: Before you trust a shader change | PASS | Second-pass check against slide 14 step 4 and 08-shader-verification.md | none |
| 90 | B1305 | Explanation of: Before you trust a shader change | PASS | Second-pass check against slide 14 step 5 and 08-shader-verification.md | none |
| 91 | B1306 | Figures spoken: `within 1 of the model` | PASS | Each figure is printed on slide 14 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 92 | B1306 | Explanation of: Before you trust a shader change | PASS | Second-pass check against slide 14 step 6 and 08-shader-verification.md | none |
| 93 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 94 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 9 step 3 shows the Chapter 6 code (version A) against the spec oracle at 30 fps with 'gap 0.000', but slide 10 step 2 and Chapter 8 give the same known-good code an error of .030 (0.0303) at 30 fps. Likewise slide 5 step 4 gives the seeded frame counter 'max gap 0.000' at 60 fps and 0.485 at 30, where slide 10 step 2 shows the same seeded change at '.030' (60) and '.515' (30). The slide 5 and 9 figures look like ideal sampling with no physics-tick lag; nothing on those slides says so, so the two sets read as contradictions.
- Slide 5 step 4 uses a tolerance of one frame (0.061 / 0.030 / 0.013), while slide 10 calls 'one frame or one physics tick' oracle v1 (0.030 at 144 fps) and the corrected v2 'one frame plus one physics tick' (0.043 at 144). The assertion on slide 5 matches neither oracle, and is never told apart from them.
- Slide 13 says 'three pixels within 1 of the model', but the exact instruction on slide 12 step 1 samples body and eye pixels at three amounts, which is six samples (the chart shows only three rows, the body).
- Slide 11 pair 3 names the term 'Frame count', where slide 5 and the map use 'Frame counter'.
- Slide 4 step 2: the labels 'gap 0.25' and 'gap 0: hidden' sit on top of the curves, and the lower 'gap 0' label overlaps the axis 0, so they are hard to make out. Slide 12 step 3: the red tolerance line cuts through the word 'seeded' and touches the '0.037' label.
- Slide 9 step 3: the explanation text breaks 'line 1 − t / 0.55' across two lines after the '1', so the next line starts with a minus sign.
- Slide 1 says '30 terms from Chapter 8 and the glossary', but slide 7 tags pixel diff 'editor or docs', its note says pixel diff is not in the chapters, and the course glossary has no pixel diff row.

## Open after the second pass

- slide 5 step 1: the slide defines pinned clock as 'a fixed frame rate: every frame the same length' (matching Chapter 8's --fixed-fps), while the midterm glossary row says 'a fixed time value so animated shaders render the same each run'; narration follows the slide and Chapter 8.

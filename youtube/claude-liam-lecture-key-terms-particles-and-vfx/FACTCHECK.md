# FACTCHECK - Key Terms: Particles and VFX

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 3 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Editor or docs, Video only, Computed, Simulation, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `35` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; What spawns, and when | PASS | Second-pass check against slide 2 step 1 and 09-particle-effects.md | none |
| 5 | B0102 | Explanation of: How it moves and looks | PASS | Second-pass check against slide 2 step 2 and 09-particle-effects.md | none |
| 6 | B0103 | Explanation of: Engine parts and cost; Which node, which rules, and where the work lands | PASS | Second-pass check against slide 2 step 3 and 09-particle-effects.md | none |
| 7 | B0104 | Explanation of: Designing the effect (Riot); How a VFX artist makes an effect clear and distinct | PASS | Second-pass check against slide 2 step 4 and 09-particle-effects.md | none |
| 8 | B0201 | Figures spoken: `age 1.1 s`, `dies at 2.2 s` | PASS | Each figure is printed on slide 3 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 9 | B0201 | Explanation of: Particle; in the book text; One small short-lived sprite or mesh in an effect.; TELL THESE APART | PASS | Second-pass check against slide 3 step 1 and 09-particle-effects.md | none |
| 10 | B0202 | Figures spoken: `12 A SECOND`, `alive now: 19 of 36 born` | PASS | Each figure is printed on slide 3 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 11 | B0202 | Explanation of: in the book text; The thing that spawns particles.; Emitter; AN EMITTER FIRING 12 A SECOND | PASS | Second-pass check against slide 3 step 2 and 09-particle-effects.md | none |
| 12 | B0203 | Figures spoken: `speed: 230 to 330`, `gravity: 220`, `lifetime: 1.5 s` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 13 | B0203 | Explanation of: Particle system; in the book text; The emitter plus the rules for its particles.; THE EMITTER PLUS ITS RULES | PASS | Second-pass check against slide 3 step 3 and 09-particle-effects.md | none |
| 14 | B0301 | Figures spoken: `6 s`, `60` | PASS | Each figure is printed on slide 4 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 15 | B0301 | Explanation of: amount; in the book text; TELL THESE APART; amount | PASS | Second-pass check against slide 4 step 1 and 09-particle-effects.md | none |
| 16 | B0302 | Figures spoken: `lifetime = 2 s` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 17 | B0302 | Explanation of: lifetime; in the book text; lifetime = 2 s | PASS | Second-pass check against slide 4 step 2 and 09-particle-effects.md | none |
| 18 | B0303 | Figures spoken: `60 ÷ 2 = 30 born per second` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 19 | B0303 | Explanation of: rate = amount ÷ lifetime = 60 ÷ 2 = 30 born per second; Spread 60 births over 2 s: 30 a second. | PASS | Second-pass check against slide 4 step 3 and 09-particle-effects.md | none |
| 20 | B0304 | Figures spoken: `2 s`, `60` | PASS | Each figure is printed on slide 4 at step 4 (machine check, check_narration.py). Badge: Simulation. | none |
| 21 | B0304 | Explanation of: Steady state; in the glossary; Births equal deaths, so the live count levels off.; steady state: | PASS | Second-pass check against slide 4 step 4 and 09-particle-effects.md | none |
| 22 | B0401 | Figures spoken: `32`, `0.6 s`, `e = 0`, `e = 0.5`, `e = 1` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 23 | B0401 | Explanation of: explosiveness; in the book text; a burst is explosiveness = 1; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 09-particle-effects.md | none |
| 24 | B0402 | Figures spoken: `alive: 32 of 32 at 0.33 s`, `explosiveness = 1` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 25 | B0402 | Explanation of: A BURST: 32 PARTICLES AT ONCE; alive: 32 of 32 at 0.33 s | PASS | Second-pass check against slide 5 step 2 and 09-particle-effects.md | none |
| 26 | B0403 | Figures spoken: `3 SECONDS`, `born in 3 s: 160`, `born in 3 s: 32` | PASS | Each figure is printed on slide 5 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 27 | B0403 | Explanation of: in the book text; Only one emission cycle occurs; otherwise it loops forever.; one_shot; LOOPING VERSUS ONE-SHOT, 3 SECONDS | PASS | Second-pass check against slide 5 step 3 and 09-particle-effects.md | none |
| 28 | B0404 | Figures spoken: `frame 1: 1 alive, or 60 with preprocess`, `preprocess 2 s`, `LIFETIME 2 S` | PASS | Each figure is printed on slide 5 at step 4 (machine check, check_narration.py). Badge: Simulation. | none |
| 29 | B0404 | Explanation of: preprocess; in the book text; also called prewarm; Starts as if the effect had already run this many seconds. | PASS | Second-pass check against slide 5 step 4 and 09-particle-effects.md | none |
| 30 | B0501 | Figures spoken: `40 SPAWN POINTS EACH` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 31 | B0501 | Explanation of: Emission shape; in the glossary; The volume particles spawn in: point, sphere, box.; TELL THESE APART | PASS | Second-pass check against slide 6 step 1 and 09-particle-effects.md | none |
| 32 | B0502 | Figures spoken: `150 to 285 px/s`, `150 to 300` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 33 | B0502 | Explanation of: in the glossary; The speed and direction a particle starts with.; Initial velocity; SPEED AT BIRTH: ARROW LENGTH | PASS | Second-pass check against slide 6 step 2 and 09-particle-effects.md | none |
| 34 | B0503 | Figures spoken: `24 RAYS`, `spread 0`, `spread 45`, `spread 180`, `54%` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 35 | B0503 | Explanation of: in the book text; spread; 24 RAYS EACH, DIRECTION UP; spread 0 | PASS | Second-pass check against slide 6 step 3 and 09-particle-effects.md | none |
| 36 | B0504 | Figures spoken: `10 PARTICLES AFTER 0.6 S`, `seed 7, run 1`, `largest difference 0.0 px`, `seed 8`, `largest difference 117.1 px` | PASS | Each figure is printed on slide 6 at step 4 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 37 | B0504 | Explanation of: Seed, determinism; in the glossary; 10 PARTICLES AFTER 0.6 S, SPREAD 60; seed 7, run 1 | PASS | Second-pass check against slide 6 step 4 and 09-particle-effects.md | none |
| 38 | B0601 | Figures spoken: `12 PARTICLES, 1.2 S, GRAVITY 300`, `219 px`, `216` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 39 | B0601 | Explanation of: Gravity; in the glossary; Constant downward acceleration applied to particles.; TELL THESE APART | PASS | Second-pass check against slide 7 step 1 and 09-particle-effects.md | none |
| 40 | B0602 | Figures spoken: `0.1 S`, `START SPEED 300`, `100`, `damping 150`, `stops after 2.0 s, 299 px from the start` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 41 | B0602 | Explanation of: editor or docs; Damping; A DOT EVERY 0.1 S, START SPEED 300; damping 0 | PASS | Second-pass check against slide 7 step 2 and 09-particle-effects.md | none |
| 42 | B0603 | Figures spoken: `age 0.6: size 0.64, about 64% of full`, `age 1` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 43 | B0603 | Explanation of: Scale curve; in the glossary; A curve for particle size over its life.; SIZE OVER AGE: 1 − AGE² | PASS | Second-pass check against slide 7 step 3 and 09-particle-effects.md | none |
| 44 | B0604 | Figures spoken: `age 0`, `age 1`, `1.0`, `0.0`, `age 0.5`, `alpha 0.50` | PASS | Each figure is printed on slide 7 at step 4 (machine check, check_narration.py). Badge: Simulation. | none |
| 45 | B0604 | Explanation of: Colour ramp; in the glossary; A gradient for particle colour over its life.; COLOUR OVER AGE: ORANGE TO RED, FADING OUT | PASS | Second-pass check against slide 7 step 4 and 09-particle-effects.md | none |
| 46 | B0701 | Figures spoken: `32 squares`, `1 by 1`, `32 px`, `0.009%`, `16 × 16 radial dot`, `6,434 px` | PASS | Each figure is printed on slide 8 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 47 | B0701 | Explanation of: texture; in the book text; TELL THESE APART; Additive blending | PASS | Second-pass check against slide 8 step 1 and 09-particle-effects.md | none |
| 48 | B0702 | Figures spoken: `255` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 49 | B0702 | Explanation of: in the glossary; a blend mode; Adds the new colour to what is behind it; glows and fire.; Additive blending | PASS | Second-pass check against slide 8 step 2 and 09-particle-effects.md | none |
| 50 | B0703 | Figures spoken: `80°`, `17 px`, `100 px` | PASS | Each figure is printed on slide 8 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 51 | B0703 | Explanation of: Billboard; in the glossary; Riot: camera-facing card; A flat quad that always faces the camera. | PASS | Second-pass check against slide 8 step 3 and 09-particle-effects.md | none |
| 52 | B0801 | Explanation of: local_coords; in the book text; off: world coordinates; TELL THESE APART | PASS | Second-pass check against slide 9 step 1 and 09-particle-effects.md | none |
| 53 | B0802 | Figures spoken: `5 times a second`, `128 px stepped`, `8 px interpolated` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 54 | B0802 | Explanation of: fixed_fps, interpolate; in the book text; HEIGHT OF ONE PARTICLE, UPDATED 5 TIMES A SECOND; 0 s | PASS | Second-pass check against slide 9 step 2 and 09-particle-effects.md | none |
| 55 | B0803 | Figures spoken: `rect ±30 px`, `rect ±130 px` | PASS | Each figure is printed on slide 9 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 56 | B0803 | Explanation of: visibility_rect; in the book text; 3D: visibility_aabb; CAMERA VIEW MOVING RIGHT, EFFECT AT X 480 | PASS | Second-pass check against slide 9 step 3 and 09-particle-effects.md | none |
| 57 | B0901 | Figures spoken: `4 of these 5` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 58 | B0901 | Explanation of: GPUParticles2D / 3D; in the book text; TELL THESE APART; GPUParticles | PASS | Second-pass check against slide 10 step 1 and 09-particle-effects.md | none |
| 59 | B0902 | Figures spoken: `1 of 5`, `1,000`, `0.035 ms`, `50,000`, `1.61 ms` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 60 | B0902 | Explanation of: CPUParticles2D / 3D; in the book text; no; no | CORRECTED | Second-pass check against the slide and the chapter: The 0.035 ms and 1.61 ms figures are not one run: Chapter 9 reports the mean of three fresh-process runs (headless, --fixed-fps 60) on the instructor's single Mac, so 'one measured run' misstates the measurement; 'measured on one machine' is what the chapter supports. | Reworded. Was: "The CPU column fills in. CPUParticles2D and its 3D twin are simulated on the CPU, the processor. They run on a wider range of hardware but handle fewer particle" |
| 61 | B0903 | Explanation of: ParticleProcessMaterial; in the book text; THREE PARTS OF AN EFFECT; Emission: on the node | PASS | Second-pass check against slide 10 step 3 and 09-particle-effects.md | none |
| 62 | B1001 | Figures spoken: `6 SPARKS`, `5 PUFFS`, `sparks alive: 0`, `puffs alive: 30` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 63 | B1001 | Explanation of: Sub-emitter; in the book text; TELL THESE APART; Sub-emitter | PASS | Second-pass check against slide 11 step 1 and 09-particle-effects.md | none |
| 64 | B1002 | Figures spoken: `LAST 30 POSITIONS`, `446 px` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 65 | B1002 | Explanation of: video only; Trail (ribbon); A RIBBON OF THE LAST 30 POSITIONS; ribbon length now: 446 px | PASS | Second-pass check against slide 11 step 2 and 09-particle-effects.md | none |
| 66 | B1003 | Figures spoken: `step 22`, `95.6`, `16 px` | PASS | Each figure is printed on slide 11 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 67 | B1003 | Explanation of: Particle shader; in the book text; SHADER_TYPE PARTICLES; start(): VELOCITY = (60, -120) | PASS | Second-pass check against slide 11 step 3 and 09-particle-effects.md | none |
| 68 | B1101 | Explanation of: Primary to tertiary read; video only; TELL THESE APART; Primary read | PASS | Second-pass check against slide 12 step 1 and 09-particle-effects.md | none |
| 69 | B1102 | Figures spoken: `head 57%, tail 43%` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 70 | B1102 | Explanation of: 2. ribbon, a scrolling texture; visual weight (illustrative): head 57%, tail 43% | PASS | Second-pass check against slide 12 step 2 and 09-particle-effects.md | none |
| 71 | B1103 | Figures spoken: `sparks 1%` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 72 | B1103 | Explanation of: 3. a few sparks; visual weight (illustrative): head 57%, tail 42%, sparks 1%; Too many sparks would pull weight from the head.; Tertiary read: a few sparks. Too many steal focus. | PASS | Second-pass check against slide 12 step 3 and 09-particle-effects.md | none |
| 73 | B1104 | Figures spoken: `5 loud effects`, `1 loud, 4 quiet`, `1.0 against 3.3` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 74 | B1104 | Explanation of: Restraint; video only; HOW LOUD EACH EFFECT IS (ILLUSTRATIVE); 5 loud effects | PASS | Second-pass check against slide 12 step 4 and 09-particle-effects.md | none |
| 75 | B1201 | Figures spoken: `4 arms`, `0 corners`, `8 spikes` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 76 | B1201 | Explanation of: Shape language; video only; The same shapes for the same meaning across the whole game.; TELL THESE APART | PASS | Second-pass check against slide 13 step 1 and 09-particle-effects.md | none |
| 77 | B1202 | Figures spoken: `0°`, `138°`, `30°`, `195°` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 78 | B1202 | Explanation of: video only; Colours that signal team, damage type or tone.; Colour coding; FOUR CODES AND THEIR HUE ANGLE | PASS | Second-pass check against slide 13 step 2 and 09-particle-effects.md | none |
| 79 | B1203 | Figures spoken: `20° apart`, `15° apart`, `175° apart`, `within 30°` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 80 | B1203 | Explanation of: Analogous colours; video only; CASTER COLOUR AND EFFECT COLOUR; 20° apart | PASS | Second-pass check against slide 13 step 3 and 09-particle-effects.md | none |
| 81 | B1204 | Figures spoken: `at 40% of the time:`, `constant 40%, eased 78% of size` | PASS | Each figure is printed on slide 13 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 82 | B1204 | Explanation of: Timing curve; video only; EXPLOSION RADIUS OVER TIME; grey: constant rate | CORRECTED | Second-pass check against the slide and the chapter: Spoken without a pause, 'the eased one seventy-eight' is heard as one hundred seventy-eight; the slide says eased 78% of size, so a comma keeps the number right by ear. | Reworded. Was: "Explosion radius over time, grown two ways. A Timing curve varies how fast an effect grows and slows, instead of using a constant rate. The grey line grows at a" |
| 83 | B1301 | Figures spoken: `60`, `lifetime 2 s`, `lifetime 4 s`, `30 a second`, `15 a second` | PASS | Each figure is printed on slide 14 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 84 | B1301 | Explanation of: PAIR 1 · LEFT; amount; How many a cycle holds; the cap on live.; lifetime 2 s | PASS | Second-pass check against slide 14 step 1 and 09-particle-effects.md | none |
| 85 | B1302 | Explanation of: PAIR 2 · LEFT; Local coordinates; Particles travel with the emitter.; carried along | PASS | Second-pass check against slide 14 step 2 and 09-particle-effects.md | none |
| 86 | B1303 | Figures spoken: `32 born in 3 s`, `160 born in 3 s` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 87 | B1303 | Explanation of: PAIR 3 · LEFT; one_shot; One cycle, then it stops.; 160 born in 3 s | PASS | Second-pass check against slide 14 step 3 and 09-particle-effects.md | none |
| 88 | B1304 | Explanation of: PAIR 4 · LEFT; Gravity; Adds speed downward every step.; path bends down | PASS | Second-pass check against slide 14 step 4 and 09-particle-effects.md | none |
| 89 | B1401 | Figures spoken: `2 s`, `1 alive`, `60 alive` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 90 | B1401 | Explanation of: “the smoke should already be rising”; WHAT THE INSTRUCTION DOES; frame 1, no preprocess: 1 alive; frame 1, preprocess 2 s: 60 alive | PASS | Second-pass check against slide 15 step 1 and 09-particle-effects.md | none |
| 91 | B1402 | Figures spoken: `explosiveness to 1`, `amount 32`, `explosiveness 0`, `32 in the first 0.1 s` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 92 | B1402 | Explanation of: “I want a burst, not a stream”; explosiveness 0: births per 0.1 s; explosiveness 1: births per 0.1 s; 32 in the first 0.1 s | CORRECTED | Second-pass check against the slide and the chapter: Explosiveness zero spreads births evenly across the cycle (Chapter 9 timing model; slide 4 entry); 'small batches' describes the chart's 0.1 s bins, not the setting, and suggests clumped emission. | Reworded. Was: "I want a burst, not a stream becomes, set explosiveness to one and one shot to true, with amount thirty-two. With explosiveness zero the births come in small ba" |
| 93 | B1403 | Figures spoken: `16 × 16`, `32 px`, `6,434 px`, `about 200 times the area` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 94 | B1403 | Explanation of: “the burst looks like specks of dust”; null: 32 px (0.009%); 16 × 16 dot: 6,434 px (1.9%); about 200 times the area | PASS | Second-pass check against slide 15 step 3 and 09-particle-effects.md | none |
| 95 | B1404 | Figures spoken: `2,000`, `78%`, `100%` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 96 | B1404 | Explanation of: “the 2D burst looks thin”; → Turn on particle_flag_disable_z so no speed goes into Z; 3D directions: 78% of speed shows; disable_z on: 100% shows | PASS | Second-pass check against slide 15 step 4 and 09-particle-effects.md | none |
| 97 | B1405 | Explanation of: “the test never sees finished”; bool set in lambda: reads false; Dictionary set in lambda: reads true; the signal fired both times | PASS | Second-pass check against slide 15 step 5 and 09-particle-effects.md | none |
| 98 | B1501 | Figures spoken: `Six checks` | PASS | Each figure is printed on slide 16 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 99 | B1501 | Explanation of: Is the effect's parent still visible when it fires?; Is the texture set, and is disable_z on in 2D?; Does a one-shot restart on every later use? | PASS | Second-pass check against slide 16 step 1 and 09-particle-effects.md | none |
| 100 | B1502 | Explanation of: Before you trust a particle effect | PASS | Second-pass check against slide 16 step 2 and 09-particle-effects.md | none |
| 101 | B1503 | Explanation of: Before you trust a particle effect | PASS | Second-pass check against slide 16 step 3 and 09-particle-effects.md | none |
| 102 | B1504 | Explanation of: Before you trust a particle effect | PASS | Second-pass check against slide 16 step 4 and 09-particle-effects.md | none |
| 103 | B1505 | Explanation of: Before you trust a particle effect | PASS | Second-pass check against slide 16 step 5 and 09-particle-effects.md | none |
| 104 | B1506 | Explanation of: Before you trust a particle effect | PASS | Second-pass check against slide 16 step 6 and 09-particle-effects.md | none |
| 105 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 106 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

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

## Open after the second pass

- slide 13 step 3: the slide's labels are swapped (one_shot sits over five cycle blocks and '160 born in 3 s', Looping over one block and '32 born in 3 s'); Chapter 9 and slide 4 step 3 settle one_shot = 32 and looping = 160, and the narration follows them without pointing left or right, but the picture on screen contradicts the words until the deck is fixed.
- slide 4 step 3: the example calls the 3D platformer's bullet glow 'looping'; Chapter 9 says only 'a steady glow behind each bullet' (lifetime 0.4) and does not state one_shot is off. Left as is: a steady glow implies looping, but the chapter does not print it.

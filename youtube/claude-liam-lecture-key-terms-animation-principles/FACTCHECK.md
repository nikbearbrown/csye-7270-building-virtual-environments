# FACTCHECK - Key Terms: Animation Principles

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 3 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Editor or docs, Video only, Outside source, Computed, Simulation, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `34` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; Keys and in-betweens | PASS | Second-pass check against slide 2 step 1 and 10-animation-foundations.md | none |
| 5 | B0102 | Explanation of: Easing and time; How motion speeds up and slows down, and how it repeats | PASS | Second-pass check against slide 2 step 2 and 10-animation-foundations.md | none |
| 6 | B0103 | Explanation of: The craft; What makes motion read as alive | PASS | Second-pass check against slide 2 step 3 and 10-animation-foundations.md | none |
| 7 | B0104 | Explanation of: Bodies and control; How a body is built, posed and driven | PASS | Second-pass check against slide 2 step 4 and 10-animation-foundations.md | none |
| 8 | B0201 | Figures spoken: `20`, `80`, `50`, `0 s`, `1 s`, `2 s` | PASS | Each figure is printed on slide 3 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 9 | B0201 | Explanation of: Keyframe; in the book text; A stored value at a specific time.; TELL THESE APART | PASS | Second-pass check against slide 3 step 1 and 10-animation-foundations.md | none |
| 10 | B0202 | Figures spoken: `0.5 s`, `50` | PASS | Each figure is printed on slide 3 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 11 | B0202 | Explanation of: Interpolation; in the book text; its results are the in-betweens; Computing the in-between values. | PASS | Second-pass check against slide 3 step 2 and 10-animation-foundations.md | none |
| 12 | B0203 | Explanation of: Clip; in the book text; An authored animation: tracks of values over time.; THREE TRACKS MAKE ONE CLIP | PASS | Second-pass check against slide 3 step 3 and 10-animation-foundations.md | none |
| 13 | B0204 | Figures spoken: `0`, `100`, `1.5 s`, `9` | PASS | Each figure is printed on slide 3 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 14 | B0204 | Explanation of: Tween; in the book text; Code-driven interpolation of a property over a duration.; A TWEEN HAS NO KEYS | PASS | Second-pass check against slide 3 step 4 and 10-animation-foundations.md | none |
| 15 | B0301 | Figures spoken: `3 s`, `100` | PASS | Each figure is printed on slide 4 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 16 | B0301 | Explanation of: Linear; in the book text; Constant rate of change.; TELL THESE APART | PASS | Second-pass check against slide 4 step 1 and 10-animation-foundations.md | none |
| 17 | B0302 | Explanation of: Step (discrete); in the book text; The value holds until the next key, then jumps.; Step 100.0 | PASS | Second-pass check against slide 4 step 2 and 10-animation-foundations.md | none |
| 18 | B0303 | Figures spoken: `70`, `100` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 19 | B0303 | Explanation of: editor or docs; A smooth curve through the keys, with no corner at a key.; Cubic; Cubic 100.0 | PASS | Second-pass check against slide 4 step 3 and 10-animation-foundations.md | none |
| 20 | B0401 | Figures spoken: `0.00`, `1.50` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 21 | B0401 | Explanation of: Easing; in the book text; ease-in-out is slow at both ends; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 10-animation-foundations.md | none |
| 22 | B0402 | Figures spoken: `0.00`, `2.00` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 23 | B0402 | Explanation of: in the glossary; Slow start, then it speeds up.; Ease-in; p = t² (ease-in) | PASS | Second-pass check against slide 5 step 2 and 10-animation-foundations.md | none |
| 24 | B0403 | Explanation of: in the glossary; Fast start, then it slows to a stop.; Ease-out; p = 1 − (1 − t)² (ease-out) | PASS | Second-pass check against slide 5 step 3 and 10-animation-foundations.md | none |
| 25 | B0501 | Figures spoken: `60 FPS`, `0.5 s`, `30 frames`, `1.5 s`, `90 frames` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 26 | B0501 | Explanation of: Timing and spacing; video only; TELL THESE APART; Timing | PASS | Second-pass check against slide 6 step 1 and 10-animation-foundations.md | none |
| 27 | B0502 | Figures spoken: `12 FRAMES` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 28 | B0502 | Explanation of: SPACING: SAME 12 FRAMES, DIFFERENT GAPS; even: every gap the same; eased: gaps change; gap: 56.7 px every frame | PASS | Second-pass check against slide 6 step 2 and 10-animation-foundations.md | none |
| 29 | B0503 | Figures spoken: `12 frames per second`, `109 px`, `60 frames per second`, `22 px` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 30 | B0503 | Explanation of: Frame rate; in the book text; Frames shown per second.; FRAME RATE: SAME 1 S OF MOTION, SAMPLED THREE WAYS | PASS | Second-pass check against slide 6 step 3 and 10-animation-foundations.md | none |
| 31 | B0504 | Figures spoken: `2 S CLIP`, `speed 2: plays in 1.0 s`, `speed 0.5: plays in 4.0 s` | PASS | Each figure is printed on slide 6 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 32 | B0504 | Explanation of: Playback speed scale; in the book text; A multiplier on how fast a clip plays.; PLAYBACK SPEED SCALE ON A 2 S CLIP | PASS | Second-pass check against slide 6 step 4 and 10-animation-foundations.md | none |
| 33 | B0601 | Figures spoken: `1 S CLIP`, `3 TIMES`, `3.00 s`, `0.00 s` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 34 | B0601 | Explanation of: Loop; in the book text; A clip that starts again from its first frame when it ends.; TELL THESE APART | PASS | Second-pass check against slide 7 step 1 and 10-animation-foundations.md | none |
| 35 | B0602 | Figures spoken: `40 px`, `0 px` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 36 | B0602 | Explanation of: in the book text; A visible jump where the last frame meets the first.; Loop seam; SAME CLIP LENGTH, TWO ENDINGS | PASS | Second-pass check against slide 7 step 2 and 10-animation-foundations.md | none |
| 37 | B0603 | Figures spoken: `32°` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 38 | B0603 | Explanation of: Cycle (walk, run); in the book text; LEG SWING ANGLE (°) AGAINST CYCLE PHASE; 0.0 | PASS | Second-pass check against slide 7 step 3 and 10-animation-foundations.md | none |
| 39 | B0701 | Explanation of: Pose; video only; A single held body position; animation is a series of them.; TELL THESE APART | PASS | Second-pass check against slide 8 step 1 and 10-animation-foundations.md | none |
| 40 | B0702 | Figures spoken: `228 px`, `38 px` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 41 | B0702 | Explanation of: Silhouette; video only; SAME ACTION, TWO SILHOUETTES; arms out: 228 px wide | PASS | Second-pass check against slide 8 step 2 and 10-animation-foundations.md | none |
| 42 | B0703 | Explanation of: Weight and balance; video only; Where the balance falls; stable when it sits over the feet.; CENTRE OF GRAVITY AGAINST THE FEET | PASS | Second-pass check against slide 8 step 3 and 10-animation-foundations.md | none |
| 43 | B0801 | Figures spoken: `0.35 s`, `21 frames at 60 fps` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 44 | B0801 | Explanation of: Anticipation; video only; A short wind-up that tells the player an action is coming.; TELL THESE APART | PASS | Second-pass check against slide 9 step 1 and 10-animation-foundations.md | none |
| 45 | B0802 | Figures spoken: `1.30`, `0.62`, `1.00` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 46 | B0802 | Explanation of: video only; Squash and stretch; scale x 1.61, y 0.62, x × y = 1.00; TWO HOPS, SHAPE FOLLOWS SPEED | PASS | Second-pass check against slide 9 step 2 and 10-animation-foundations.md | none |
| 47 | B0803 | Figures spoken: `12 frames` | PASS | Each figure is printed on slide 9 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 48 | B0803 | Explanation of: Arcs; outside source; launch up 767 px/s, gravity 1278 px/s², apex 230 px; ONE HOP: THE PATH AND THE SAMPLES | PASS | Second-pass check against slide 9 step 3 and 10-animation-foundations.md | none |
| 49 | B0901 | Figures spoken: `450`, `103 px` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 50 | B0901 | Explanation of: Follow-through, overlap; outside source; TELL THESE APART; Follow-through | PASS | Second-pass check against slide 10 step 1 and 10-animation-foundations.md | none |
| 51 | B0902 | Figures spoken: `0.12 s`, `0.24 s` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 52 | B0902 | Explanation of: SAME MOVE, THREE START TIMES; shoulder; starts 0.00 s, stops 0.80 s; elbow | PASS | Second-pass check against slide 10 step 2 and 10-animation-foundations.md | none |
| 53 | B0903 | Figures spoken: `6 hair points`, `240 frames`, `1440` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 54 | B0903 | Explanation of: Secondary motion; outside source; THE HEAD IS KEYED; THE HAIR IS NOT; Keyed by hand: the head, 5 keys (diamonds). | PASS | Second-pass check against slide 10 step 3 and 10-animation-foundations.md | none |
| 55 | B1001 | Figures spoken: `80°` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 56 | B1001 | Explanation of: Rig and skeleton; in the glossary; TELL THESE APART; Rest pose | PASS | Second-pass check against slide 11 step 1 and 10-animation-foundations.md | none |
| 57 | B1002 | Figures spoken: `0` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 58 | B1002 | Explanation of: Rest pose (bind pose); in the book text; The skeleton's default pose, the one the mesh is fitted to.; RIGID: EACH VERTEX FOLLOWS ONE BONE | CORRECTED | Second-pass check against the slide and the chapter: Voice rule: say.py reads 'tears' as the crying noun (t-ee-rz), so 'tears' became 'splits'; the meaning (a rigid binding opens a gap at the elbow) is unchanged. | Reworded. Was: "Now a mesh is bound to the bones. The Rest pose, also called the bind pose, is the skeleton's default pose, the one the mesh was fitted to. Here every angle is " |
| 59 | B1003 | Figures spoken: `0.50` | PASS | Each figure is printed on slide 11 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 60 | B1003 | Explanation of: in the book text; also: bone weights, vertex weights; How strongly each vertex follows each bone.; Skinning weights | PASS | Second-pass check against slide 11 step 3 and 10-animation-foundations.md | none |
| 61 | B1101 | Figures spoken: `40°` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 62 | B1101 | Explanation of: Forward kinematics (FK); in the glossary; Rotate joints parent-to-child to place the hand.; TELL THESE APART | PASS | Second-pass check against slide 12 step 1 and 10-animation-foundations.md | none |
| 63 | B1102 | Figures spoken: `370 px` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 64 | B1102 | Explanation of: Inverse kinematics (IK); in the book text; Give a target and the solver works out the joint angles.; distance 394 px, reach limit 370 px: out of reach by 24 px | PASS | Second-pass check against slide 12 step 2 and 10-animation-foundations.md | none |
| 65 | B1103 | Figures spoken: `71 px` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 66 | B1103 | Explanation of: Retargeting; in the glossary; copied angles miss the target by 71 px; retargeted: 0.0 px; target scaled by reach ratio 220 ÷ 260 = 0.85 | PASS | Second-pass check against slide 12 step 3 and 10-animation-foundations.md | none |
| 67 | B1201 | Figures spoken: `120 px per cycle`, `480 px`, `4.0 s` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Simulation. | none |
| 68 | B1201 | Explanation of: Root motion; in the book text; The clip moves the character through the world.; TELL THESE APART | PASS | Second-pass check against slide 13 step 1 and 10-animation-foundations.md | none |
| 69 | B1202 | Figures spoken: `150`, `120`, `30 px/s` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Simulation. | none |
| 70 | B1202 | Explanation of: in the book text; The clip stays on the spot; code does the travel.; In-place; SAME WALK CLIP, TWO WAYS TO TRAVEL | PASS | Second-pass check against slide 13 step 2 and 10-animation-foundations.md | none |
| 71 | B1203 | Figures spoken: `0.40`, `0.20`, `0.80` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Simulation. | none |
| 72 | B1203 | Explanation of: Blend tree; in the book text; Weighted mix of clips driven by parameters.; idle | PASS | Second-pass check against slide 13 step 3 and 10-animation-foundations.md | none |
| 73 | B1204 | Figures spoken: `0.1` | PASS | Each figure is printed on slide 13 at step 4 (machine check, check_narration.py). Badge: Simulation. | none |
| 74 | B1204 | Explanation of: State machine; in the book text; One active state; transitions fire on conditions.; STATES AND TRANSITIONS | PASS | Second-pass check against slide 13 step 4 and 10-animation-foundations.md | none |
| 75 | B1301 | Figures spoken: `0.5 s`, `1.0 s` | PASS | Each figure is printed on slide 14 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 76 | B1301 | Explanation of: PAIR 1 · LEFT; Timing; How long the move takes.; 0.5 s | PASS | Second-pass check against slide 14 step 1 and 10-animation-foundations.md | none |
| 77 | B1302 | Explanation of: PAIR 2 · LEFT; Ease-in; Slow start, then it speeds up.; slow start | PASS | Second-pass check against slide 14 step 2 and 10-animation-foundations.md | none |
| 78 | B1303 | Figures spoken: `48°` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 79 | B1303 | Explanation of: PAIR 3 · LEFT; FK; Angles in, hand position out.; shoulder 20°, elbow 40° | PASS | Second-pass check against slide 14 step 3 and 10-animation-foundations.md | none |
| 80 | B1304 | Figures spoken: `0.1` | PASS | Each figure is printed on slide 14 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 81 | B1304 | Explanation of: PAIR 4 · LEFT; Blend tree; How much of each clip.; idle | PASS | Second-pass check against slide 14 step 4 and 10-animation-foundations.md | none |
| 82 | B1401 | Figures spoken: `0.4 s`, `0`, `1.5` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 83 | B1401 | Explanation of: “make it feel smoother”; WHAT THE INSTRUCTION DOES; linear: 1.0; eased: peak 1.5 | PASS | Second-pass check against slide 15 step 1 and 10-animation-foundations.md | none |
| 84 | B1402 | Figures spoken: `12 frames`, `6`, `60 fps`, `0.20 s`, `0.10 s` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 85 | B1402 | Explanation of: “make it snappier”; 12 frames = 0.20 s; 6 frames = 0.10 s; half the frames, half the time: 0.20 s to 0.10 s | PASS | Second-pass check against slide 15 step 2 and 10-animation-foundations.md | none |
| 86 | B1403 | Figures spoken: `40 px`, `0 px` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 87 | B1403 | Explanation of: “the walk jumps when it loops”; before: seam jump 40 px; after: seam jump 0 px; the last key equals the first, so the seam is gone | PASS | Second-pass check against slide 15 step 3 and 10-animation-foundations.md | none |
| 88 | B1404 | Figures spoken: `6 frames`, `0.75`, `1.33`, `1.00` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 89 | B1404 | Explanation of: “make the jump feel heavier”; rest 1.00 × 1.00; squash 1.33 × 0.75; area stays 1.00: 1.33 × 0.75 = 1.00 | PASS | Second-pass check against slide 15 step 4 and 10-animation-foundations.md | none |
| 90 | B1405 | Figures spoken: `130`, `110`, `240`, `200` | PASS | Each figure is printed on slide 15 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 91 | B1405 | Explanation of: “the hand should reach the cup”; cup at 200 px: elbow 67°, shoulder -31°; in reach (200 of 240 px): the solver finds the angles | PASS | Second-pass check against slide 15 step 5 and 10-animation-foundations.md | none |
| 92 | B1501 | Explanation of: Before you ship an animation | PASS | Second-pass check against slide 16 step 1 and 10-animation-foundations.md | none |
| 93 | B1502 | Explanation of: Before you ship an animation | CORRECTED | Second-pass check against the slide and the chapter: Calling step an interpolation repeats the slide's mix-up. Chapter 10 'Between keys' lists interpolation as nearest, linear or cubic, and discrete as a separate update mode, so the question no longer files step under interpolation. | Reworded. Was: "Second, which interpolation sits between the keys? Linear, step and cubic fill the same gaps differently, and only step holds a value and then jumps." |
| 94 | B1503 | Explanation of: Before you ship an animation | PASS | Second-pass check against slide 16 step 3 and 10-animation-foundations.md | none |
| 95 | B1504 | Explanation of: Before you ship an animation | PASS | Second-pass check against slide 16 step 4 and 10-animation-foundations.md | none |
| 96 | B1505 | Explanation of: Before you ship an animation | CORRECTED | Second-pass check against the slide and the chapter: Voice rule: say.py reads 'close' here as the adjective (klohs), so the question was reworded to 'is the loop closed', which it reads correctly. | Reworded. Was: "Fifth, does the loop close? The last key should equal the first, so there is no loop seam each time the clip wraps." |
| 97 | B1506 | Figures spoken: `0.4 s` | PASS | Each figure is printed on slide 16 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 98 | B1506 | Explanation of: Before you ship an animation | PASS | Second-pass check against slide 16 step 6 and 10-animation-foundations.md | none |
| 99 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 100 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 5 (Timing, spacing, frame rate and speed scale), step 3: the caption says 'At 12 fps the dot jumps 113 px at the start; at 60 fps it jumps 23 px', but the computed labels on the same picture say 'biggest jump 109 px' and 'biggest jump 22 px' (680 x ease-out of 1/12 is 108.6, of 1/60 is 22.5). The caption numbers are hard-coded and wrong. The narration speaks 109 and 22.
- Slide 8 (Anticipation, squash and stretch, arcs), step 1: the readout ends on 'flight: 1.55 s', which is the time since the wind-up began (0.35 + 1.2), while the line above says 'then flight 1.2 s'. The readout's label should not be 'flight'. Not spoken.
- Slide 9 (Follow-through, overlap, secondary motion), notes: the tail spring is described as 'omega 14, damping ratio 0.22', but the code (SPR) uses w = 9 and z = 0.2. The step 1 caption 'settles in about 1 s' also does not match the graph, where the tail is still swinging visibly past 2 s of the 4 s plot.
- Slide 9 step 3: the caption says 'Keyed by hand: the head, 5 keys (diamonds)', but only three diamonds are visible, because the keys at 0 s, 1 s and 2 s are drawn at the same spot. The narration says only that the head is keyed.
- Slide 3 and slide 15 call step (discrete) an interpolation ('Which interpolation sits between the keys: linear, step or cubic?'). Chapter 10 keeps two settings apart: interpolation per track (nearest, linear, cubic) and update mode per value track (UPDATE_DISCRETE). In Godot's own words the step look is nearest interpolation or the discrete update mode, so the slide's grouping can mislead a student about where the setting lives.
- Slide 12 (Root motion, blend tree, state machine): step 1 gives the root track as '120 px per cycle', step 2 as '120 px/s'. They agree only if one cycle lasts one second, which the slide never states.
- Slide 14 step 1: the 'eased: peak 1.5' label is drawn on the linear line, struck through by it, and well below the red peak it names.
- Slide 2 step 4: 'Keys stored by the clip above: 3 tracks x 3 keys = 9' refers to a clip that is no longer on screen at that step (the tween picture has replaced it). Steps 3 and 4 also have the 'in the book text' badge of Clip sitting on its definition line, so 'tracks of values over time' runs under the badge.
- Slide 10 step 1: the 'joint' label is drawn under the forearm bone, which crosses through the word. Slide 11 step 3: the grey copied-angles arm runs down over the caption 'target scaled by reach ratio'.

## Open after the second pass

- slide 9 step 1: the follow-through example (the Walker sword's fast attack swings to 85 degrees, then settles at 75, from Chapter 10) is a real keyed overshoot and settle, but the deck defines follow-through as parts moving on after the body stops, and the sword clip animates only the blade with no separate body that stops. Neither the slide nor the references say whether an overshoot of the main moving thing counts. Left unchanged.

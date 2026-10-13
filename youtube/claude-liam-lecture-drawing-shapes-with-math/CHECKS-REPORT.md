# Checks report (PROOF GATE): Drawing Shapes with Math

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks for the build, and the mechanical lint result with a reason for every warning that remains.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 44 body beats, all SHOW; no HOLD; no text-only card (each act title rides on the act's first picture). Lanes: ShaderLab capture 25, Manim 15, Remotion 3 (two tables, one code card), editor 1. Estimated 10.8 minutes by the lint's ceiling formula, 1,900 words by the lint's count (1,545 in the body, no body beat over 40 words). `lint_series.py` prints no errors and no warnings; no fact-check row is OPEN. The capture lane is the largest because this film is about code and its picture; each of those 25 beats was weighed against a drawing in `SHOTLIST.md` and won on evidence. The terms card (BDEFS) has six terms and uses the GLOSSARY's wording word for word for each, so the lint's wording comparison has nothing to report.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 44 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | no beat names a visual that is not on screen |

Lane histogram (information, not a quota): capture 25 · manim 15 · remotion 3 · editor 1.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "a circle image" becomes "a question for each pixel").
- [x] **Framework before the first example.** B02 shows the whole idea, every pixel answering "am I inside?", on a pixel grid, before any distance is computed.
- [x] **Worked example with the framework on screen.** B03 to B09 take one real pixel, (0.62, 0.66), through the framework: address, distance by hand, step, mask. The same pixel is ringed in the real renders (B05, B09). B08 states the swapped order of `step` as two questions (has the distance reached the radius, has the radius reached the distance).
- [x] **Falsifiability and edge cases as full beats.** Two ways the arithmetic fails while the screen hides it (B14 to B19: the hidden two that eats a hole; a bite that takes a mask below zero and eats a spot), a compile error (B32), the square assumption (B33), the hard edge (B34).
- [x] **No tool before its time.** B18 and B19 use only what the viewer has met by then (circles, step, subtraction, min); `max` is introduced in B19 as `min`'s mirror (B16's table shows the broken numbers only, with no `min` column, so the fix is still new in B17), and `abs`, the cross and the arms wait for Act III.
- [x] **One name, one role, one order.** The three conditions of an arm keep their names and their order from B25 to the crosshair: `not_too_far` and `near_line` (B25), `far_enough` added in front (B26), the same three as `gap, end, width` in the one-line pair (B27, B28) and in `make_arms` (B37); vertical pair first, horizontal second, everywhere.
- [x] **Scaffolded viewer task.** The "Your turn" prompt and two checks; a reference answer proves both checks can be met (FACTCHECK 70).
- [x] The lecture spine's six fixed beats are present (identity card, writer, terms; recap, your turn, outro); no composer cold open.
- [x] Every term the film teaches is defined on screen where first spoken, in the GLOSSARY's wording where it has a row: Color Rect (B01, docs wording), distance (B04, B05), step (B07), alpha (B05), mask (B09), hint (B10, the full GLOSSARY wording as the caption), min (B17), max (B19, B23), abs (B21, B22), band (B20, the full GLOSSARY wording), built-in (B31); BDEFS holds prerequisites only (function, shader, fragment, UV, vector, uniform), each card line equals the GLOSSARY row, and "function" is on the card because B02 and B05 speak it before B30 reuses it as a label. The code notation `UV.x` and `UV.y` is tagged on screen in B20 (horizontal and vertical address) before the code uses it.
- [x] Concrete before abstract: the pixel by hand (B04) comes before the function (B05); the render comes before the rule in B14, B15 and B18.
- [x] Every measured number says what machine and renderer (credit lines and `videoLabel`s read "Godot 4.7.2 · Forward+"); scripted input is labelled on every sweep.
- [x] **No source, no verdict.** Every beat that makes a claim carries a real render, a table of values computed in Godot, or a credit line with the measurement; the Manim beats are mechanism drawings whose claims are checked in FACTCHECK rows 5, 9 to 12, 16 to 18, 25, 37, 38, 41, 42, 47, 48, 50 to 52, 54 to 58, 75, 80 and 81.
- [x] Honest limits stated aloud: the square assumption (B33), the hard edge (B34), "in a default project" for the hidden two (B14; with 2D HDR on it would show: FACTCHECK 29).
- [x] **The sampled frame is settled.** No cue, readout or ring starts between 45 and 55 % of a beat; Manim motion starts by 30 %, is a quick one (0.35 s) up to 40 %, or starts at 56 % or later; every dial sweep keeps its 50 % and 85 % frames inside a hold, and every held state was rendered in the Lab (the single dials, and the six held pairs `pair-*`). `_gen_lanes.py` checks the cue rules and builds each sweep so that the holds fall there.
- [x] **Cues follow the words.** Every cue, readout, ring, Manim event and sweep breakpoint is placed by `_gen_lanes.py` from where its phrase falls in the narration (an estimate now, the measured word clock once the build has run it). The times that stay fixed on purpose: a beat's first cue (2 %), the 'predict first' readout (2 %), the 'arms off' and 'arms alone' readouts (10 %), and the hook's pause across 44 to 56 % (C01), because the 50 % frame must be a hold.
- [x] Standalone: no reference to another film, book or course, no numbering, and no use of "part" (lint plus a read).
- [x] No digits in the narration (numbers are words; the screen keeps the figures).

## Risks for the build (not defects of the layout)

1. **Shared components may not exist yet** (`ShaderLab`, `shader_kit.py`, the capture harness). This film also needs a **square result window** in `ShaderLab`, **square output** from the harness and **readouts that replace each other** (BUILD-PROMPT, Phase 0); everything else it uses (`--steps`, `--scene`, fractional keyframes) is in the spec.
2. **GATE T.** Every Godot picture is teal on a warm light-grey stage on purpose (no dark fields). The crosshair's thin lines are teal on grey, not ink: look at them at the 50 % and 85 % marks. Terracotta strokes in the Manim beats must be thick (at least 8 px at 1080p).
3. **Gate V underfill** on the three result-only beats (B01, B39, B43): a square window on a 16:9 stage. They are declared sparse with a reason in the beat sheet; only the underfill check is waived.
4. **Pace.** The longest beats are B08, B18, B19, B20, B24, B31 and B33 (40 words); the lint figure is a ceiling. If the voice check runs long, trim B05 first (its second sentence repeats the picture), then B20.
5. **Fifteen Manim scenes** are the heaviest part of the build. Five need care: B04 (a real equation, `MATH-TYPESETTING.md`), B21 (a fold without a forbidden path arc), B28 (the 55-character line is set as three stacked calls), B31 (a bounce and a pass-through with plain shifts) and B34 (a staircase of outline cells, a centre dot in each, with an arc drawn over them).
6. **Editor frames E1.** The driver is proven and saved (`evidence/planning-checks/editor-driver/`), so Bear should not be needed; the build must record outside the project folder, crop to the six sliders and may record at 3840 by 2160 for a sharp crop (a recommendation, not something the planning check ran). **The editor's dark theme may fail GATE T**: the remedies are in CAPTURE-PLAN.md, and the Light theme preset is a global setting of Bear's Godot, never to be changed in place.
7. **B18 shows a bug as an absence.** The picture of the broken shader has no spot in it; the claim is carried by the ring, the readouts (`mask −1`, then `mask 0`, then `spot: missing`) and the fixed twin in B19. Look at both stills together before the render.
8. **The cue times are estimates until the build runs the word clock.** `_gen_lanes.py` switches to the measured times by itself once `mp3/words.json` exists; a beat that the aligner could not anchor keeps its estimate and must be reported.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py drawing-shapes-with-math` prints no errors and no warnings (it warns on OPEN rows, on a card wording that differs from the GLOSSARY, and on register words such as "just"; there are none). The single claim that needed a real editor window, six sliders in the Inspector (FACTCHECK 69), was observed in a planning-check frame; capture E1 re-records it for the film.

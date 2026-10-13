# Checks report (PROOF GATE): The Shader Math Toolkit

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the advisory type-gate run, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 41 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 23 (plots and diagrams drawn from `plot_data.py`), ShaderLab capture 16 (real Godot renders next to their code), Remotion 2 (the docs capture and the mod table). Estimated 10.3 minutes, 1,808 words in total (1,515 in the body; the checker counts 1,823 because it adds the terms card's own words). `lint_series.py` is clean (result at the end). One build risk was found and designed out early: a continuous black-to-white ramp strip drawn in Manim would be read as a text run by GATE T; drawn as a row of narrow tiles it is not (advisory run, below).

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 41 | every body beat has a motion that carries its claim, and a midpoint pose that is a settled still |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): manim 23 · capture 16 · remotion 2.

## Teaching arc (the nopunt whole-sheet checklist, adapted to a function toolkit)

- [x] **Framework before the first example.** B04 teaches how to read the standard plot and B05 shows that bending the line bends the strip ("read the line, predict the picture"); every later function is an application of it.
- [x] **Worked example that uses the framework visibly.** Act V builds a ring step by step with the code on screen beside the real render (B35 to B41): `distance` makes the ramp, `step` cuts it, two cuts subtract (B37), `mix` colors it, `smoothstep` softens it.
- [x] **Edge cases and corrections as full beats.** `smoothstep` is not a straight line, with the measured number (B11) and the docs' formula and "undefined" warning (B12); `mix` does not pin its weight (B14); the `mod` trap against GDScript (B25); the oval on a wide shape, measured (B30); a negative `pow` base is undefined (B33).
- [x] **Opens on the newcomer's assumption and corrects it with one phrase** (BIDEA: "advanced math" becomes "a dozen small functions").
- [x] **Every term the film teaches is defined on screen where first spoken** (ramp, fragment, COLOR, uniform, mask and each function, in the GLOSSARY or docs wording); BDEFS holds prerequisites only (Shader, Pixel, UV, Function, Vector).
- [x] **Predict-then-reveal.** B05 holds the strip unflipped for a beat after the line bends; B11 states what a straight line would give before the S's number; B35 states "dark inside, light outside" as the cut is made.
- [x] **Scaffolded viewer task.** BHTF is a prompt that makes the viewer build the film's ring on their own shader, with two checks about the look (round and centered; the radius dial moves it with soft edges) because "it compiles" and "it looks right" are furthest apart in a shader.
- [x] **No source, no verdict.** Every claim has an on-screen artifact: a plot drawn from the verified formula, a real Godot render, the docs page, or the three-row table of measured values.
- [x] **Honest limits.** Measured numbers say machine and renderer (credit lines); the two behaviours the docs call undefined are called undefined, never promised; no speed or frame-rate claim anywhere; the plots are drawings of math and the film does not present them as Godot output.
- [x] **Standalone.** No reference to any other film, book or course (lint); no number on any viewer-facing surface.
- [x] **Midpoint rule.** Each of the 23 Manim beats lists exactly one "midpoint hold" pose and no other motion starting between 45 and 55 % of the beat; every ShaderLab cue, read-out, ring, ramp marker, table cue and browser-capture move starts outside that window (`_gen_lanes.py` asserts this when it writes the lanes: the function `check_windows`).

## Advisory type-gate run (not the gate)

`evidence/planning-checks/run_gate_t_advisory.py` runs the toolkit's own blob detector (`type_check.py`, read only) on the real Lab renders pasted into two stand-in layouts at 4K (a 1900 px window beside a code column; a 2900 px result-only window). **0 text-like runs inside the render window for all 20 captures in both layouts** (`gate-t-advisory.json`), including the black fields of the step, pow, disk and ring pictures. It also found the one real trap: a **continuous** black-to-white ramp strip (2000 x 130 px at 4K) yields 1 text-like run (682 x 130 px: the band of dark grays near the ink and mute colors); the same strip drawn as **64 narrow tiles with 6 px gaps** (or 48 tiles with 8 px gaps) yields 0. The text-like band is a gray (red = green = blue) between 27 and 113 of 255 (0.11 to 0.44), because those grays lie within 48 of the ink or mute color (`gate-t-ink-band.json`); **pure black (93 from ink), white, the stage gray, cream, teal and gold are all far outside it**, which is why the black fields of the step, pow, disk and ring pictures do not trigger the detector while a smooth gradient through the band can. So the lanes and `SHOTLIST.md` specify the Manim ramp strip as a row of narrow tiles in true grays (0 black, 1 white), with a lifted-gray fallback (0.50 + 0.50 v) if the real gate still objects. This advisory does not replace GATE T: contrast, overflow and kerning checks still run in the build.

## Risks for the build (not defects of the layout)

1. **The shared pieces may not exist yet** (checked 2026-10-13): `ShaderLab` is not registered, `shader_kit.py` and the capture harness are not written. `lint_series.py` accepts `ShaderLab` because `COMPONENT-SPECS.md` plans it. If the pilot film is built first (its handoff builds them), this film only reuses them; otherwise `BUILD-PROMPT.md` Phase 0 says what to do.
2. **Twenty-three Manim scenes share one plot grammar.** Build `plot_with_strip` (the standard plot) once and reuse it; the formulas are in `plot_data.py`.
3. **Sweeps need piecewise keyframes** on one uniform (`CAPTURE-PLAN.md`); if the harness only has linear sweeps, record segments and join them.
4. **Pace.** The longest beats are B25 (45 words), B32 and B14 (44), B04 and B12 (43). If a voice check runs long, split B32 at "Below one" or trim B25; the cut line in `ACTS.md` names what leaves first.
5. **Voice.** Check the pronunciation of "fract", "abs", "mod", "F mod", "F pos mod", "smooth step", "U V dot x", "power" and "sine"; report problems, never edit `liam.json`.
6. **D1 docs capture** must show the three quoted lines; if the page wording has changed, stop and tell Bear.
7. **Type gate on the ShaderLab labels.** The cue labels (at most 60 characters, checked by `_gen_lanes.py`) carry the GLOSSARY wording of fragment(), COLOR and alpha (B03) and the first half of the uniform definition (B08, whose caption holds the whole sentence); check them at the type floor on the 50 % and 85 % frames.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py shader-math-toolkit` prints no errors and no warnings (run at the end of the layout; see the final report).

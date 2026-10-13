# Checks report (PROOF GATE): Time and Waves

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks for the build, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 40 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 18, ShaderLab capture 18, Remotion 4 (docs capture, two tables, one code layout). Estimated 9.6 minutes, 1,679 words. `lint_series.py` is clean with no warnings. Three risks for the build: the shared components do not exist yet, pale pulse phases at the Gate V sample points, and the pronunciation of "tau" and "fract".

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 40 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | the two table beats (B08, B25) are the registered `LectureEvidenceTable` with a ringed row, not narration set as type |

Lane histogram (information, not a quota): manim 18 · capture 18 · remotion 4. The router put functions reshaping a count and rulers in Manim, shader code with its live result in `ShaderLab`, two tables of parallel facts in `LectureEvidenceTable`, a docs claim in `BrowserCapture`, and a code-only listing in `ShaderLab`'s code layout.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: when my node appears → when the game starts).
- [x] The central idea is shown in motion before it is named: a late node joins in step (B01) before the definition (B02); the real pulse (B13) before the three knobs; five offsets rolling along a row (B18) before the wave travels across a shape (B26 to B28).
- [x] Every term the film teaches is defined on screen where first spoken (table in `ACTS.md`); BDEFS holds six prerequisites only (shader, fragment(), uniform, UV, texture, sine).
- [x] A framework beat comes before the examples that use it: "time times speed counts the cycles; a shape function turns the count into a look" (B15, B17), then loops and curves (Act III), travelling waves (Act IV), the payoff (Act V).
- [x] A worked example uses the framework visibly: the breathing logo and the waving banner (B35 to B40).
- [x] Concrete before abstract: the pulse as a real shader (B13) before amplitude, speed and offset on a plot; stripes (B27) before the formula's four knobs (B30).
- [x] Edge cases and failures get a full beat each: the roll-over jump (B04), the clocks drifting apart (B06), the clamped half of a raw sine (B11), the sine-fed curve that plays backward (B24), rings that squash on a wide shape (B29, said), the edge smear (B33).
- [x] Measured claims name the machine and renderer (B05's credit line; every capture's `videoLabel`); what could not be recorded is said on the picture: the one-hour roll-over was not waited for (B04's credit line).
- [x] Payoff uses the earlier ideas together: a curve read by a restarting ramp, scaling about the middle, a travelling wave pinned at one edge, a wind uniform driven by a tween (B35 to B40).
- [x] Honest limits: scripted input is labelled (B03, B40); the Lab renders are offline at a fixed tick rate and no frame-rate claim is made; the rings are claimed for a square shape only.
- [x] Scaffolded viewer task: BHTF gives a prompt to paste and two checks the viewer runs on the result (amplitude zero holds still; offset one half runs exactly opposite).
- [x] Standalone: no reference to another film, a book, a course or a series (lint); no number appears on any viewer-facing surface; no playlist name is typed.
- [x] No source, no verdict: every beat that asserts something carries a picture of the thing (a run, a plot of measured numbers, the docs row); the recap and your-turn beats assert nothing new.

## Risks for the build (not defects of the layout)

1. **The shared pieces may not exist yet**: `ShaderLab` (layouts `side`, `video`, `code`), `shader_kit.py`, the capture harness (`../_godot-shaders-series/COMPONENT-SPECS.md`). The build starts there if the first film's build has not run.
2. **Pale pulse phases at the Gate V sample points.** The pulse swings between teal and cream on a light stage; at the 50 % or 85 % mark it may sit at its pale end. The fix is a head trim, not a shader edit (rule in `CAPTURE-PLAN.md`).
3. **Pronunciation**: "tau", "fract", "sine" and "sawtooth" are not in the voice dictionary. Voice-check them; report, do not edit `liam.json`.
4. **Pace.** The longest beats are B07 (41 words), then B04, B05, B14, B19, B22, B24 and B28 (39 words each, about 13 s). If the measured audio puts a beat over 15 s, split it.
5. **Manim helpers**: `knob_slider`, `time_ruler`, `curve_strip` and `bracket` are new film-local helpers; Gate A needs every scene to add a non-text, non-Rectangle shape after its first frame (dots, curves and brackets do).
6. **Docs screenshot legibility**: the TIME row is small text on a long page; capture at device scale 2.4 and push in to at least 2 times.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py time-and-waves` prints no errors and no warnings at the time of writing: 46 beats (six bookends and 40 body beats), 1,690 counted words (1,679 are spoken in all; the lint leaves out the seven-word outro and adds three words for each of the six terms-card entries), 9.6 estimated minutes (the real length will be shorter: the lint counts the bookend words at body pace), FACTCHECK 85 verdict rows, a runner-up on every lane entry, every shader file a lane points at exists, and every cue label within 60 characters.

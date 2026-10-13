# Checks report (PROOF GATE): Godot Shaders

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 43 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 18, ShaderLab capture 17, Remotion 6 (code trace, tables, docs capture), editor 2. Estimated 10.5 minutes, 1,851 words. `lint_series.py` is clean. Two risks the build must watch: type-gate on dark game art, and the three components that do not exist yet.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 43 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): manim 18 · capture 17 · remotion 6 · editor 2.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: the whole screen → one pixel).
- [x] The central idea ("a shader decides the color of one pixel") is shown in motion (B03, B08) before it is named in code.
- [x] Every term the film teaches is defined on screen where first spoken; BDEFS holds prerequisites only.
- [x] Concrete before abstract: each function is shown on a real render before its table (B24).
- [x] A measured claim says machine and renderer; what could not be measured is said aloud (B07).
- [x] A thing that surprises is demonstrated by a real run (TIME, B40; typo, B32; tween, B33).
- [x] Payoff uses every earlier idea together (B42, B43).
- [x] Honest limits: scripted input is labelled; GPU time not claimed; the editor widgets pending frames (FACTCHECK 38, 39).
- [x] Standalone: no reference to any other film, book or course (lint).
- [x] No number on any viewer-facing surface.

## Risks for the build (not defects of the layout)

1. **Three components do not exist yet**: `ShaderLab`, `shader_kit.py`, the capture harness (`../_godot-shaders-series/COMPONENT-SPECS.md`). The build starts there.
2. **GATE T on game art.** The Lab stage is a warm light grey and the test sprite is teal on purpose; the gradient shader (B06) and the UV picture (B37) have dark corners: frame them in a window on the cream stage and check at the 50 % and 85 % marks.
3. **Editor frames** may need Bear if the driver does not work in one sitting.
4. **Pace.** B11 (48 words), B17 and B12 (about 45) are the longest beats; if a voice check runs long, split B11 or trim B12.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py godot-shaders` → no errors, no warnings at the time of writing (see `../_godot-shaders-series/LINT-REPORT.md` for the series run).

# Checks report (PROOF GATE): Vertex Shaders

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the build risks, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 40 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: capture 27 (real Godot renders in `ShaderLab`), Manim 12, terminal 1. Estimated 9.8 minutes, 1,721 words. `lint_series.py` is clean. Risks the build must watch: type-gate on the shaded flag, the 25 captures that must land on the words, and the shared components that may not exist yet.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 40 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 27 · manim 12 · terminal 1. The capture share is high because most claims are claims about what Godot draws, and the router sends a result of a real shader to `ShaderLab`; the twelve Manim beats are the ones about a coordinate system, a flow, a count or a measured edge, where a drawing of the idea is the picture.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: changes pixels, moves corners).
- [x] The central idea (a vertex shader can only move the vertices that exist) is shown failing on a four-corner flag (B12) before it is shown working on the mesh (B17).
- [x] Every term the film teaches is defined on screen where first spoken (table in `ACTS.md`); BDEFS holds prerequisites only.
- [x] Concrete before abstract: each effect (slide, squash, lean, ripple) is shown on a real render before it is generalised.
- [x] A measured claim says machine and renderer; the measuring floor is stated (B18: gaps measured at 3x zoom, floor a third of a pixel).
- [x] Things that surprise are demonstrated by real runs: scaling changes the move (B06), 297 and 66 vertices draw the same picture (B19), a varying cannot invent detail (B34), the same word means two things (B36, B37), a shader does not move the collision shape (B39).
- [x] The payoff uses every earlier idea together: the lit, pinned, travelling flag with dials (B32, B33 and the opening beat).
- [x] Honest limits: scripted events are labelled; a vertex shader changes the drawing only (B39); no cost or frame-rate claim anywhere.
- [x] Standalone: no reference to any other film, book or course (lint); no number on any viewer-facing surface.
- [x] Ends on something the viewer can do and check: the BHTF prompt asks Claude for the banner and reports the vertex count; the two checks are the viewer's own (left edge still; 33 by 9).

## Risks for the build (not defects of the layout)

1. **Shared components.** `ShaderLab`, the `shader_kit.py` objects and the capture harness may not exist yet (the pilot's build makes them); this film adds five Manim objects and a scene-script option to the harness (`BUILD-PROMPT.md`, Phase 0).
2. **GATE T and Gate V on the lit flag.** In the darkest folds the cream cells are multiplied by about 0.8 and approach the stage grey; the teal cells and the grey pole keep the picture readable. Check C01, C20 and B33 at the 50 % and 85 % frames; fix by framing or cropping, not by changing the shader.
3. **Capture timing.** Most captures are timed as fractions of each beat's measured audio so the picture lands on the words; they must be recorded (or re-recorded) after the audio exists.
4. **Dense beats.** The longest beats are B01, B10, B18, B23, B27, B30, B31, B33 at 39 words; if the voice check runs long, split B23 after "uniform" or trim B31.
5. **Code cards.** Every shader card is at most 14 lines (the longest is 13); three cards show GDScript (B15, B25, B35) rather than shader code and say so in `codeFile`.
6. **Manim numbers.** Five Manim pictures carry measured numbers (B04, B08, B10, B16, B36); take them from `FACTCHECK.md`, do not recompute.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py vertex-shaders` prints no errors and no warnings at the time of writing.

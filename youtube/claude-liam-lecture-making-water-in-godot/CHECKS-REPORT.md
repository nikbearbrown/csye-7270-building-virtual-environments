# Checks report (PROOF GATE): Making Water in Godot

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the build risks, and the mechanical lint and gate results.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 49 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture; the three tables carry real counted or quoted facts with highlights that land on the words). Lanes: capture 36 (real Godot renders in `ShaderLab`), Manim 9 (drawings around real images and measured numbers), tables 3, terminal 1. Estimated 11 to 12 minutes, 2,144 words (the series lint's estimate is 12.2 and errs long). The series lint is clean; the toolkit's plan-time gates (banned-card, beat-lint, lane-check, factcheck) pass. Risks the build must watch: the cue labels on about thirty ShaderLab beats (never used by the overnight builds), Gate V on pale grey-stage captures, and the captures that must be re-recorded at the measured lengths.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 49 | every body beat has a motion that carries its claim (a sweep, a swap, a count, a transcript printing line by line, a table row lighting on the word) |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 36 · manim 9 · remotion (LectureEvidenceTable) 3 · terminal 1. The capture share is high because most claims are claims about what Godot draws, and the router sends a real shader's result to `ShaderLab`; the nine Manim beats are the ones about a structure or a sum (the three links, the blend arithmetic, the two renderers' numbers, the squares and the nine, the colour-direction code, the seam, the two clocks, the depth ray), each built around a real image or measured numbers; the three tables are counted or quoted facts; the terminal beat is a real transcript.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: a water simulation, six small tricks).
- [x] The film's arc is Bear's: blue, then a little transparent, then noise foam, then UV manipulation and normal maps for ripples, then (added) real waves and (added) shore foam; every layer is shown on a real render before and after.
- [x] Concrete before abstract: each effect is seen (a plane turns blue, the floor appears, the net breathes, the glare breaks into glints, the waves roll) before its code is explained.
- [x] Every term the film teaches is defined on screen where first spoken (table in `ACTS.md`); BDEFS holds prerequisites only.
- [x] Surprises are demonstrated by real runs, not asserted: the same alpha reads 108 or 71 (B09), a plane under the water draws on top of it (B11), 462 pixels go black (B23), a texture without repeat smears (B28), the glare stays one oval without a new normal (B37), a built-in vanishes in a helper (B45), the whole surface turns to foam in Compatibility (B47).
- [x] A measured claim says machine and renderer (every ShaderLab label and caption names Forward+ or Compatibility; the unshaded tests say so).
- [x] The payoff uses every earlier idea together: the finished water with the buoy and crate on the waves and a white shore (B01, B46), and three looks from the one shader (B49).
- [x] Honest limits: scripted events are labelled; captures are offline at a fixed tick rate; the floating objects follow because a script mirrors the function (B39, B40); the docs-only costs are quoted as quoted (B11 uses a real demonstration; B12 quotes the docs and one measurement).
- [x] Standalone: no reference to any other film, book or course (lint); no number on any viewer-facing surface; the Unity video is credited only in `SOURCES.md` (it is not named in the film).
- [x] Ends on something the viewer can do and check: the BHTF prompt asks Claude for the water and the vertex count; the two checks are the viewer's own (see-through at 0.7 with the floor showing; 65 by 65 = 4,225 vertices).

## Risks for the build (not defects of the layout)

1. **ShaderLab cue labels.** About thirty beats use the `label` cue feature; the overnight builds used it on none. Render stills of B03, B04, B15, B21 and B47 first (`BUILD-PROMPT.md` Phase 0).
2. **Gate V and GATE T on real Godot pictures.** The cove is mid-blue and sand on a warm grey stage: expect low-contrast MAJORs on ShaderLab beats; `gate_t_regions.py` declares the authored text regions. The editor crop (B48) has small dark UI text: declare its region if GATE T reads it as text.
3. **Capture timing.** Most captures are timed as fractions of the beat's length, so they must be re-recorded after the audio exists (`captures.py --stale`). C22 and C29 stay at 1280 x 720 (their captions quote pixel rows).
4. **Dense beats.** The longest beats are B04, B08, B17, B24, B40, B42, B43 and B46 at 41 to 45 words; if the voice check runs long, split rather than trim a number.
5. **The B45 terminal card's line timing** is set for an estimated beat; scale it to the measured audio (`BUILD-PROMPT.md` Phase 3).
6. **Pronunciation.** "Voronoi", "albedo", "fract", "Fast Noise Lite" are not in the pronunciation dictionary; listen and report (do not edit the dictionary).

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py making-water-in-godot` prints 0 errors and 0 warnings at the time of writing (55 beats, 2,144 words, 12.2 estimated minutes). Toolkit plan-time gates on the layout: `evidence/gates/layout-stage-gates-2.txt`, re-run after the last narration edit (banned-card PASS, beat-lint clean, lane-check PASS 55 beats, factcheck clean: 131 rows, 0 uncovered beats; the first run is `layout-stage-gates-1.txt`). Manim: Gate A clean on all nine classes and the layout audit prints no warnings (`evidence/gates/preflight-manim-2026-10-16.txt`; pace under target on every class).

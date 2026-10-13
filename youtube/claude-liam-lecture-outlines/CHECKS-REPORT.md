# Checks report (PROOF GATE): Outlines

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks for the build, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 41 body beats, all SHOW; no HOLD, no text-only card, no punt (each act title rides the act's first picture). Lanes: ShaderLab capture 27, Manim 11, Remotion 3 (a docs capture, a code trace, a checks table); no editor frames. Estimated 10.7 minutes by the lint's pessimistic count (1,868 words; 1,855 are spoken). `lint_series.py` is clean: no errors, no warnings. Four risks for the build are listed below; none is a defect of the layout.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 41 | every body beat has a motion that carries its claim (the still-frame test was applied to each lane entry) |
| HOLD | 0 | none: no beat needs a real photograph or a judgment only Bear can make |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 27 · manim 11 · remotion 3.

Beat sizes: 26 to 48 words per body beat (B22 has 48, B32 47), every sentence 19 words or fewer, five acts of 10, 7, 10, 6 and 8 beats.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: a bigger copy behind the sprite becomes a question about neighbors).
- [x] The central idea (a pixel asks its neighbors) is shown in motion (B03) before any code appears (B07), and the first code is a deliberate bug shown running (B07), then fixed one line at a time (B08 to B10).
- [x] Every term the film teaches is defined on screen where first spoken (mix in B06, min in B10, texture pixel size and uniform in B13, hint in B14, offset and for in B19, material in B26, instance uniform in B27, region rect and clamp in B33, varying and modulate in B40); BDEFS holds prerequisites only. The six card wordings were compared with the GLOSSARY: shader, texture and alpha are word for word; opaque, neighbor and padding are not in it.
- [x] Concrete before abstract: each bug is a real render before its fix (B07 then B08, B09 then B10), and the sprite sheet, thin-part and soft-edge traps are shown failing before they are fixed.
- [x] Every measured claim names the machine and renderer; what could not be measured is said aloud and on screen (the card's own timer is unreadable, so B22 is a labelled wall-clock stress test); the formula's limit (hard-edged art) is said in B20 and taught in B38.
- [x] Surprises are demonstrated by a real run: the light diagonals (B09), the stray line from the next frame (B32), the floating copies (B37), the fade that does not fade (B40).
- [x] The payoff uses the earlier ideas together: B41's five checks, and the viewer's own prompt and two checks (BHTF) on an outline written by Claude.
- [x] Honest limits: scripted input is labelled (B26), the stress test is labelled, the scope of the 2,008 count is labelled (B39), no editor widget is claimed (no editor frames).
- [x] Standalone: no reference to any other film, book, course or school (lint).
- [x] The film is not numbered anywhere (no film number, part, episode or "N of X"); only its five acts carry the I to V the series' format requires.

## Risks for the build (not defects of the layout)

1. **Three shared pieces may not exist yet**: `ShaderLab`, `shader_kit.py`, the capture harness (`../_godot-shaders-series/COMPONENT-SPECS.md`). `BUILD-PROMPT.md` Phase 0 says to look first. This film adds one small piece, a mode that plays a JSON scene spec through the SubViewport route (about 40 lines, specified in `CAPTURE-PLAN.md`; `evidence/planning-checks/route_check.gd` is a working example).
2. **GATE T on captures.** The stage is warm grey and the sprite teal on purpose, and the ring is indigo (a mid-tone, nowhere near ink). The 12x close-ups (C38, C39) fill their windows with large flat fields: check them at the 50 and 85 percent marks. The pixel grids and the 3 by 3 block must be outline-only cells with padding.
3. **Pace.** B22 (48 words) and B32 (47) are the longest beats; if the voice check runs long, report it rather than edit (the cut line in `ACTS.md` starts with B14 and B22).
4. **The stress-test numbers are audited, not live.** B22 and B36 quote `cost-summary.txt`. A repeat while another window covers Godot gives 6.9 ms for every shader (the invalid run is kept in `evidence/planning-checks/`); the build must not re-run it.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py outlines`: no errors, no warnings in the final run (the run is the last step of the layout; see the report that accompanies it). Earlier in the work the lint raised two warnings on B32 (53 words, and the word "just"); both were fixed by rewriting the beat, not by waiving them.

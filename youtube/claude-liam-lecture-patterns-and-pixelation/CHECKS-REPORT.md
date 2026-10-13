# Checks report (PROOF GATE): Patterns and Pixelation

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 43 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 22, Manim 18, Remotion 3 (two tables and one docs capture). Estimated 10.2 minutes, 1,790 words by the series checker. `lint_series.py` is clean (details at the end). Three risks the build must watch: the three shared components if they do not exist yet, the four small scene scripts, and eighteen Manim scenes.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 43 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 22 · manim 18 · remotion 3.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: a pattern image → math on the address).
- [x] **FRAMEWORK beat before the first example**: the two-number idea is drawn on a ramp and a grid (B02 to B05) and mapped (B09) before any effect is built.
- [x] **WORKED EXAMPLE** walked through the framework with it on screen: a number carried through the pixelate formula (B16); the checkerboard from a sum and a remainder (B26 to B29).
- [x] **Falsifiability and edge-case beats**: the drift of the obvious lookup (B13, B14); the tempting half-fix that halves the edge blocks (B17, B18); the block size that does not divide the picture (B25); the dots that turn oval on a wide shape (B39, B40); the same rounding trap in dots (B42).
- [x] The central idea is shown in motion before it is named in code (B02 to B05 before B06 to B08).
- [x] Every term the film teaches is defined on screen where first spoken (cue labels on code lines, Manim labels, the docs capture); BDEFS holds prerequisites only.
- [x] Concrete before abstract: each effect is shown as a real render before its recipe table (B19, B34).
- [x] A measured claim says machine and renderer (every `videoLabel` and credit line); what was not measured is not claimed (no frame-rate or GPU claim; the Inspector is never shown).
- [x] A thing that surprises is demonstrated by a real run: the jump (B13), the half-size edge blocks (B18), the ovals (B39), the cut dots (B42).
- [x] Payoff uses both numbers (B41 to B43).
- [x] **SCAFFOLDED viewer task**: the "Your turn" prompt and its two checks were validated in a scratch Godot project against a reference answer (passes both) and two wrong answers (each fails the check meant to catch it): `evidence/planning-checks/verify-bhtf.gd`.
- [x] Honest limits: scripted sweeps and switches are labelled; nearest filter stated (the smooth filter blends neighbours: FACTCHECK row 64); on a texture whose proportions are not whole the far edge holds half dots in any answer, so the edge check is worded "on a square texture" (row 63).
- [x] Standalone: no reference to any other film, book or course (lint); no film number anywhere viewer-facing; every digit on screen is a measured or defined value.

## Risks for the build (not defects of the layout)

1. **Shared components**: `ShaderLab`, `shader_kit.py` and the capture harness may or may not exist when this film is built (`BUILD-PROMPT.md` Phase 0 says how to check). This film adds three small kit objects (numbered `cell_grid`, `block_row`, `lookup_lines`), the `cues[].label` field of `ShaderLab`, a stepped sweep, and four scene scripts (C12, C18, C19, C21).
2. **GATE T on the picture colors.** The shaders use a mid-tone floor (teal, cream, gold, the soft red-green cells); there are no dark pictures in any beat (the Lab's gradient texture, which has a near-black corner, was used only for measurements). Cream dots on the light-grey stage are low-contrast but far from ink; check at the 50 % and 85 % marks.
3. **Eighteen Manim scenes** is the biggest build item; three of them (B14, B18, B25) are small bespoke drawings (a staircase against a line; two rows of blocks; a strip with a short last block) that use no shader picture at all.
4. **Pace.** Longest beats: BHTF (105 words, about 36 s, read in full by design), B06, B09 and B28 (40 to 41 words each). If a voice check runs long, trim B09 or B06; the cut line in `ACTS.md` is ready.
5. **Voice.** `fract` and `mod` are not in the pronunciation dictionary; listen for them (BUILD-PROMPT Phase 3).

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py patterns-and-pixelation` (run 2026-10-13, after the last edit): 49 beats (43 body), 1,790 words, 10.2 estimated minutes, **0 errors, 0 warnings**. Every warning the checker can raise was avoided rather than explained: no beat over 48 words (longest 41), no digits in the narration, no sentence over 30 words, three to six terms, four or six recap lines, two checks, every shader file a lane names exists.

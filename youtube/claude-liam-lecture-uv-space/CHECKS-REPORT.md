# Checks report (PROOF GATE): UV Space

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks for the build, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 42 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 19, Manim 17, Remotion 6 (two code traces, three tables, one docs capture). Estimated 10.3 minutes, 1,812 words by the lint's count (1,512 in the body). `lint_series.py` is clean: no errors and no warnings (no OPEN fact-check rows). Three risks for the build: type-gate on the address map's navy corner, the three material switches (captures C03, C07 and C13), and the two Manim drawings (ruler, window) that are not in the shared kit.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 42 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 19 · manim 17 · remotion 6 · editor 0.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: the screen becomes the shape).
- [x] The central idea ("the address moves, the picture goes the other way") is shown in motion before it is explained: hook (B01), the surprise (B09), then the numbers (B10) and the rule (B11).
- [x] Framework before the first example: the copy-bend-look pattern (B08) precedes every shader that bends an address (B09 on).
- [x] A worked example uses the framework visibly: B10 (the middle pixel reads 0.25) and B21 (subtract, scale, add back).
- [x] Every term the film teaches is defined on screen where first spoken (UV and address B02, fragment B06, TIME B17, aspect ratio B32, mask and step B38, alpha B40); BDEFS holds prerequisites only (Shader, Pixel, Texture, Vector, Uniform).
- [x] Edge cases and failures get full beats: the corner zoom (B19), the oval (B28), the smear (B36), the failure table (B42).
- [x] Concrete before abstract: each rule is seen on a real render before its drawing or table (B09 before B10 and B11; B28 before B29 to B32).
- [x] A measured claim says machine, window and renderer (credit lines on B29, B30, B35; `videoLabel` on every capture).
- [x] A wrong source claim is named and corrected with a measurement (B31, FACTCHECK row 46).
- [x] Payoff uses the earlier ideas together: the opening shader decoded line by line (B41).
- [x] Scaffolded viewer task: a real prompt (scroll a texture left, repeating) and two checks the viewer can see for themselves (direction, and a seamless loop after ten seconds).
- [x] Honest limits: scripted values are labelled; the pixel counts belong to a named window and renderer; the node-setting beat names no Inspector label (no editor frame was captured); the spoken title ("U V Space") is a convention heard only at the build's voice check (FACTCHECK row 67).
- [x] Standalone: no reference to any other film, book or course (lint); nothing is numbered.

## Risks for the build (not defects of the layout)

1. **Shared pieces.** `ShaderLab`, `shader_kit.py` and the capture harness may not exist yet (`BUILD-PROMPT.md` Phase 0). `ShaderLab` must show a PNG as its `video` (C02, C03) and keep a 16:9 result window.
2. **GATE T.** The address map (C02) has a navy top-left corner by design (blue held at half, so it is never black); check it at the 50 % and 85 % marks. All other captures use teal, cream and white on the light grey stage. Manim ticks, brackets and the pixel-square grid (B29, B31) are drawn in greys, not ink.
3. **Three material switches.** C03 (B06) assigns the lookup shader to a plain sprite at 0.58 `L` (the picture must not change), C07 (B15) switches from the no-repeat shader to the repeat shader at 0.60 `L`, and C13 (B25) from the one-eye shader to the two-eye shader at 0.44 `L`; they are the only captures that need `--material-at`. If a switch cannot be timed, fall back to two shorter captures cut together at the same moment.
4. **Pace.** The longest beats are B35 (42 words), B38 (42) and B42 (43); the cut line in `ACTS.md` names what moves out if a voice check runs long (B16, B37, B31, B26, B39).
5. **Title.** BOPEN and BOUT speak `SPOKEN_TITLE`, "U V Space" (the card and the outro props keep "UV Space"): listen for it first. If Kokoro stumbles, report it; do not edit the dictionary.
6. **Logical canvas.** C15 and C16 need a 640 by 360 logical canvas so their pixel readouts (512 by 288, 288 by 288) are true; every other capture can use 1280 by 720.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py uv-space` gives no errors and no warnings (checked again after the shared lint changed on 2026-10-13: SPOKEN_TITLE added).

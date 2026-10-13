# Checks report (PROOF GATE): Light Shaders

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks the build must watch, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 40 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 25, Manim 12, Remotion 3 (one docs capture, two tables); no editor beat. About 10.3 minutes by the lint's ceiling estimate (1,808 words counted, which adds the terms card; 1,796 spoken words, 10:15 by the sheet's own estimate). `lint_series.py` is clean: no errors, no warnings. The risks are the three shared components that do not exist yet, a GATE T watch on the Godot captures, and the capture convention (1920 x 1080 at scale 1) that differs from the series default for a measured reason.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 40 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 25 · manim 12 · remotion 3. The two Remotion tables (B18, B40) and the docs capture (B04) are the only beats without a moving Godot render or a Manim drawing; each was auditioned against a drawn alternative (SHOTLIST.md).

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "You can't touch it" becomes "A shader can replace it").
- [x] FRAMEWORK before the first example: the measured pixel rule (B06, B07: surface times the total of ambient and lamps) and the question light() answers (B08) come before the first function is written (B09).
- [x] WORKED EXAMPLE on the framework: the empty function, the flat answer, then the three-line rebuild that equals the default pixel for pixel (B09, B10, B13), then reshaped (B14 to B16).
- [x] FALSIFIABILITY: a full beat on where the copy fails (B18, normal maps, with measured counts), where a beam cannot go (B30, the lamp's reach) and where a ring does not follow the world (B37, zoom).
- [x] SCAFFOLDED viewer task: the closing exercise is a prompt to paste and two checks the viewer makes on their own result (a stopwatch for the turn, deleting the light node).
- [x] The lecture spine is present: opening card, writer, terms, the body, recap, exercise, outro.
- [x] No source, no verdict: every beat that asserts a Godot behaviour carries a capture, a docs capture or a measured table; the verdict and exercise beats recapitulate.
- [x] Concrete before abstract: the hook (a glow becomes a beam) comes first; each built piece is shown on a real render before it is generalised.
- [x] Every term the film teaches is defined on screen where first spoken (captions, code-line tags and Manim labels in the GLOSSARY wording); BDEFS holds prerequisites only (Shader, Pixel, Texture, Canvas, Vector, Mask).
- [x] A measured claim says machine and renderer (B07 credit, B13 caption, B18 table note); what is scripted is labelled (B36 "scripted run").
- [x] A thing that surprises is demonstrated by a real run: an empty light() (B09), the hard square (B14), the copy that misses normal maps (B18), the ring that ignores zoom (B37), stripes that stay put (B38).
- [x] The payoffs use the earlier ideas together: the lighthouse (direction, step, dot, TIME) and the spreading ring (position, distance, two steps, a uniform, a tween).
- [x] Honest limits: no GPU timing and no real-time frame rate claimed; screen numbers are window pixels; the docs' normal-map fix is for sprites that have a normal map.
- [x] Standalone: no reference to another film, book or course, and no film number, part or count on any viewer-facing surface (lint); the only numbers are the real figures the screen shows.
- [x] Y points down and angles grow clockwise (GLOSSARY convention): said aloud in B26 and drawn that way in B24, B31 and B32.

## Risks for the build (not defects of the layout)

1. **Three shared components may not exist yet**: `ShaderLab`, `shader_kit.py` (the capture loop is already written for this film). `ShaderLab` must render cue `label`s (at most 60 characters) and `caption`s (at most 80); this film uses about a dozen tags (BUILD-PROMPT.md Phase 0).
2. **GATE T on game art.** The floor is a mid-tone dusk blue by design; the darkest pixels in any capture are the tile grout lines (about (92, 98, 118) in 255), the grey card in the first second of C06 (about (89, 98, 128)) and the unlit bulb discs of C11 (about (128, 130, 114)), all well away from ink (61, 57, 41). Check the 50 and 85 % frames of every capture; do not darken the ambient to make lights look better.
3. **Capture scale.** 1920 x 1080 at scale 1, shown at about 1:1. A ShaderLab window much bigger than 1,900 px would force upscaling of a 1920 capture; keep the window at about 1,900 px or less (the `video` layout may need a smaller window than usual).
4. **TIME-driven captures** (C01, C10, C15 to C19): the beam's angle at a given second depends on engine start; cosmetic.
5. **Pace.** B11 (43 words), B36 (44), B38 (44) and B40 (43) are the longest beats; if a voice check runs long, split B36 or B38 first, or use the cut line in ACTS.md.
6. **Pronunciation to listen for**: "tween", "cel shading", "mod", "U V", "x" and "y" as letters, "smooth step", "Canvas Modulate". Report, do not edit the dictionary.
7. **The docs capture (D1)** needs a real Playwright run; the lane's two ring positions are placeholders until the page is captured.
8. **Estimated timing of the captures.** Event times are estimated at 0.34 s per word; re-time a capture if the measured beat differs by more than a second (BUILD-PROMPT.md).

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py light-shaders` → no errors, no warnings at the time of writing (46 beats, 1,808 words, 10.3 minutes, 83 fact-check rows, 0 OPEN). The checker's newer rules were applied: no uppercase PI or TAU, no code call with parentheses, no unspaced acronym in the narration; no "just", "simply", "easy" or "obviously"; GLSL, "pixel shader" and core counts are not mentioned; cue labels are 60 characters or fewer and captions 80 or fewer (asserted in `_gen_lanes.py`).

# Checks report (PROOF GATE): Reading the Screen

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks the build must watch, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 38 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 25, Manim 11, Remotion 2 (a code card with the engine's real error, and the symptom table). 1,685 words and 9.6 minutes by the lint's formula, which is a ceiling (the measured bookend time is shorter than the same words at body pace), so the film should land at about nine and a half. `lint_series.py` is clean with no warnings. Four risks for the build: GATE T on the flipped (purple and navy) and gray captures, the eleven Manim scenes and the shared components that may not exist yet, the voice on a handful of spoken forms, and the capture size of the one blur capture (native 1920 x 1080, not the 4K route).

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 38 | every body beat has a motion that carries its claim (a snapshot, a vanishing fill, a slide, a drain, a walk, a sweep, a pan, a switch) |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | B10 is a real code card with the engine's real message and a moving focus; B38 is a drawn table with the row that matters ringed |

Lane histogram (information, not a quota): capture 25 · manim 11 · remotion 2. The picture a beat needs decided the lane: a shader's live result next to its code is a capture; a quantity or a rule of order (a copy being taken, a weighted sum, a stack of layers, a click that stops) is a drawing.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "its own sprite" becomes "what is already on screen").
- [x] The central idea, a shader reading a copy of what was already drawn, is shown in motion (B01 the live pool, B02 the snapshot, B03 the rectangle that vanishes) before it is written out line by line (B04 to B09).
- [x] Every term the film teaches is defined on screen where first spoken: screen texture (B02), sampler2D and the uniform line (B04), hint (B05), alpha (B06), UV and SCREEN_UV (B07), fragment() (B03, cue label), swizzle (B09), canvas layer (B12), Full Rect (B11), mouse filter (B13), dot (B14), mix (B15), distance (B17), SCREEN_PIXEL_SIZE and aspect ratio (B19), set_shader_parameter (B20), sine (B22), TIME (B23), mipmap and textureLod (B25), source_color (B27), discard (B28), reader (B30), BackBufferCopy and its copy mode (B33), repeat_disable, filter_nearest and renderer (B36). BDEFS holds prerequisites only (texture, UV, uniform, fragment(), draw order, post-processing).
- [x] Concrete before abstract: the effect is on screen before its line is named (B03, B09, B15, B21 to B29).
- [x] A measured claim says its renderer; claims that differ between Forward+ and Compatibility are not made for both (`repeat_enable`, the default filter): B36 says `repeat_disable` (which holds in both) and names the one difference outright (Forward Plus obeys `filter_nearest`, Compatibility blends anyway; `verify9`).
- [x] Things that surprise are demonstrated by a real run: the invisible rectangle (B03), the tiny copy inside a rectangle (B08), the overlap that stays flipped (B32), a filter that does see the pool (B34), a color rect that eats mouse clicks (B13).
- [x] Predict, then reveal: "flipping twice should restore the original; instead..." (B32), "look closely: it is an oval" (B18).
- [x] Payoff uses the earlier ideas together (B29 the pool, B37 the pool, the spotlight and the health bar).
- [x] Honest limits: scripted input is labelled; no GPU time and no frame rate is claimed; the editor's own labels were read from the real editor, not typed from memory.
- [x] Standalone: no reference to any other film, book or course, no film number (lint).
- [x] No digit in the narration; the screen keeps the real figures (320 px, 180 px, 0.01, level 4).

## Risks for the build (not defects of the layout)

1. **Shared components.** `ShaderLab` and `shader_kit.py` come from the shared specs (`../_godot-shaders-series/COMPONENT-SPECS.md`); if the first film of the series has not built them yet, the build starts there. The capture driver is *not* a risk: `scene_capture.gd` is already written and tested. The eleven Manim scenes are new work, specified in `SHOTLIST.md` and `lanes/act*.json`.
2. **GATE T on the new colours.** The flipped meadow is purple and navy, the gray meadow is mid-gray: `evidence/planning-checks/palette-check.py` shows every colour the captures use, flipped, grayed and pool-tinted, stays at least 61 RGB from INK and MUTE (the gate counts under 48 as text). The two entries under 60 (the health bar's backing flipped, the empty stage flipped) never appear in a frame. Even so, look at the 50 % and 85 % frames of C04, C18 and C19 (large flipped areas) before the 4K render. The cream window frames are drawn on a high layer so they are never part of a flipped region (a flipped cream frame would be near-black).
3. **Never crop a capture past the frame edge.** C22 has a window flush with the right edge of the picture; ShaderLab must show the whole 1280 x 720 canvas.
4. **Spoken forms to listen for:** "sampler two D", "U V" and "screen U V", "r g b", "texture lod" (textureLod), "mipmap", "Back Buffer Copy", "Full Rect", "set shader parameter", "Godot four", "post-processing", "Forward Plus", "Compatibility", "aspect ratio". Report any slip to Bear; do not edit the pronunciation dictionary.
5. **Pace.** The longest beats are 40 words (B01, B11, B12, B14, B15, B19, B36): if a voice check runs long, split B12 or B14 first.
6. **Capture size.** 22 captures use the 3840 x 2160 SubViewport route and C13 (the mip-level blur) is native 1920 x 1080: the same level is less than half as blurred on the 4K route (`verify10`; `CAPTURE-PLAN.md`, Routes). `capture_all.py` chooses; do not re-record C13 by hand through the 4K route.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py reading-the-screen` → no errors, no warnings at the time of writing (44 beats, 1,685 words, 9.6 minutes by the lint's formula).

# Checks report (PROOF GATE): Soft Edges, Glow and Noise

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks for the build and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 42 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: capture 23, Manim 15, editor 2, Remotion 2 (both are documentation captures). 1,791 words by the lint's ceiling formula, about 10.2 minutes. `lint_series.py` has no errors and no warnings (the two formerly OPEN fact-check rows were closed from real editor frames recorded by script on 2026-10-13; see the reconciliation note at the end). Three risks for the build: the shared components (`ShaderLab`, `shader_kit.py`, the capture harness) if the first film's build has not made them yet; fourteen captures need scene scripts; the editor frames of B19 need a native-size re-record (about 30 seconds, scripted).

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 42 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture (B01, B11, B17, B24, B33); the bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 23 · manim 15 · editor 2 · remotion 2.

Words per act (body): I 342 (10 beats), II 212 (6), III 241 (7), IV 318 (9), V 358 (10); 1,471 body words in all. Longest beats: B35, B40 and B03 at 40 words; the longest sentence in the body is 22 words (B40).

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "a blur" becomes "a ramp").
- [x] The central idea (a soft edge is a ramp whose width you choose) is shown in motion (B01 swap, B05 to B08) before it is generalised.
- [x] Every term the film teaches is defined on screen where first spoken, in the GLOSSARY wording word for word where the glossary has the term: step and distance (B03), smooth step and t (B05, B06), band (B07, caption; the glossary row is about line thickness, so its opening is kept and the two radii named), max (B09, chip label), falloff (B11), power (B13), clamp (B14), hint (B19, caption), noise and texture (B24), sampler2D and the texture read (B25), TIME (B26), seamless (B30, caption), glow (B34, caption), H D R two D (B35, caption), linear light (B40, caption), threshold (B41, caption). BDEFS holds prerequisites only: ramp, mask, UV, uniform, alpha (all five word for word).
- [x] Concrete before abstract: the hard and soft circle before `step` (B01), the curve before its number (B05 then B06), the curves before the render (B13 then B14), the failure before the fix (B28 then B29).
- [x] Predict-then-reveal where it fits: a straight ramp would say 0.1, smoothstep says 0.028 (B06); what should "dim the bubble" do, then the two real answers (B21, B22); will it glow, then run one and run two (B36, B37).
- [x] A measured claim says machine and renderer: every Godot capture carries `Godot 4.7.2 · Forward+` in its label, and the narration says "on this Mac" where a number depends on the machine (B10, B22, B36, B40, B41).
- [x] A thing that surprises is demonstrated by a real run: equal and swapped edges (B09, B10), streaks without the hint (B28), a seam without Seamless (B29, B30), the tinted rim under HDR 2D (B36), no halo without the Canvas background (B37, row 71).
- [x] The payoff uses every earlier idea together: the finished bubble with soft edge, highlight, drifting noise and the glow dial (B42).
- [x] Honest limits: scripted switches are labelled; the glow demonstration names its stage color and intensity; B39 says the halo is faint on a light stage; Compatibility pixels are not shown because they differ; the docs-versus-run difference about HDR 2D and Compatibility is not claimed (FACTCHECK 86).
- [x] Standalone: no reference to any other film, book or course (lint).
- [x] No film number or count on any viewer-facing surface.

## Risks for the build (not defects of the layout)

1. **Shared components.** `ShaderLab`, `shader_kit.py` and the capture harness (`--material-at`, `--animate` piecewise, `--scene`, `--call-at`, `--time-origin`) are specified in `../_godot-shaders-series/COMPONENT-SPECS.md`. Check `./brutalist.art/art scenes --check ShaderLab` before building anything; if the first film's build already made them, reuse them.
2. **Fourteen captures need scene scripts** (C08, C10, C11 to C16, C18 to C23): a two-panel script, a NoiseTexture2D script, a vec2 orbit script and an HDR 2D / environment / stage-color switch script. The scratch checks in `evidence/planning-checks/` (`noise_check.gd`, `toggle_check.gd`, `finale_check.gd`, `glow_check.gd`) are the node recipes. Record these first, in one session.
3. **Editor frames E1 and E3** are recorded by script (E3 for this film, E1 reused from the Textures and Color recording): copy them, no click and no recording by hand. E3 exists at 1920x1080 only and must be re-recorded at native 3456x1944 for the 4K window (the recipe is in `CAPTURE-PLAN.md`); the dark editor UI is a GATE T risk, so look at the 50 % and 85 % frames of B19 and B24.
4. **GATE T.** The glow stage `#5F7A96` is 79 RGB from the type gate's MUTE grey and 131 from ink; the Lab stage and the teal are far from both. The bubble at brightness 0.6 has a dark teal body (about 79, 119, 105), 91 RGB from ink: look at the 50 % and 85 % frames of B22 anyway.
5. **Code width.** The longest code lines are 71 characters (`08-bubble`); at 44 px monospace that needs a code panel of about 1,900 px at 4K. If `side` cannot give it, use `stack` for B19, B20, B34.
6. **Math.** B06 sets 3t^2 - 2t^3 as real typeset math (`docs/MATH-TYPESETTING.md`): look at the 15 / 50 / 85 % frames and record the check.
7. **B35's caption** carries the H D R definition and the dated provenance on one line; if it does not fit under the browser window, shorten the provenance, never the definition.
8. **After recording**, compare every probe in `CAPTURE-PLAN.md` ("verified result to reproduce"); if one disagrees, stop and report (do not edit a shader).

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py soft-edges-glow-and-noise` runs clean: no errors, no warnings. The two rows that were OPEN, 35 (the editor shows a color picker for a `source_color` uniform) and 57 (the Inspector's wording "Seamless"), were closed on 2026-10-13 from real editor frames and are PASS.

## Editor-frame reconciliation 2026-10-13

**What changed.** The picture and capture description of the two editor beats, B19 and B24, and the two OPEN fact-check rows, were reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, sections 2.3, 2.7 and 11.5). **Why.** The first plan could not show the Inspector, so two rows were OPEN and two lanes described pictures from convention. No narration changed: no spoken label was wrong. Nothing was voiced, rendered or published.

- **B19 (row 35, now PASS).** The bubble material was recorded in the real editor (the one film-specific driver run; scene, state script and log in `evidence/planning-checks/editor-capture/`): Body Color and Highlight Color are color swatches, Brightness a number box with a slider bar, and a click on a swatch opens the picker. The lane now shows the Inspector crop with a ring on the first swatch, then the picker open. "A color picker in the editor" is true: the Inspector row is a swatch that opens one.
- **B24 and B30 (row 57, now PASS).** The row is labelled exactly "Seamless", a checkbox. The B24 lane's old picture (one Inspector view with the preview, the Noise slot and Seamless together) cannot exist: the NoiseTexture2D view has Width, Height, Noise and Seamless but no preview, and the grey clouds appear one click deeper, in the FastNoiseLite view. The lane now shows those two views in that order, reusing two frames recorded for the Textures and Color film; their ring boxes and timings follow the narration.
- Only 1920x1080 frames exist for B19; the build re-records them at native size (CAPTURE-PLAN section E). `lint_series.py`: no errors, no warnings (the one OPEN-row warning is gone).

Beat ids, beat count (42 body), lane types and acts are unchanged; words unchanged (1,791 by the lint, 10.2 minutes).

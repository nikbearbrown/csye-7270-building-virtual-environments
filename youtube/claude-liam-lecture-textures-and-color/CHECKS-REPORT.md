# Checks report (PROOF GATE): Textures and Color

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks the build must watch, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 41 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 27, Manim 7, editor 3, Remotion 4 (tables and a docs page). Estimated 10.9 minutes by the lint's ceiling formula, 1,918 words. `lint_series.py` has no errors and no warnings: the three fact-check rows that were OPEN are closed from real editor frames recorded by script on 2026-10-13 (see the reconciliation note at the end). The build must watch four risks: type-gate on dark pixels (now including the dark editor frames), the accent color near the swatches and the burn rim, the shared components that may not exist yet, and the cross-dissolved editor clips.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 41 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; the bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 27 · manim 7 · remotion 4 · editor 3. Per act: I 7 beats (6 capture, 1 Manim), II 9 (8 capture, 1 Manim), III 10 (7 capture, 2 Manim, 1 editor), IV 6 (1 capture, 3 Manim, 2 table), V 9 (5 capture, 2 editor, 1 table, 1 docs page).

## Best-beat audition (each beat has a runner-up in `SHOTLIST.md`)

The router decided most beats: a real Godot result with its code (ShaderLab) wherever the claim is "this line makes this picture" (Acts I to III and V); Manim wherever the picture is a mechanism no render shows (a lookup, four numbers, a band of values, a ramp lookup, a probe's place in a pipeline, the sRGB curve and its two midpoints); a table for parallel measured facts (two renderer tables, the rule); the docs page itself where the claim is a documentation claim. No lane was chosen for variety. Where a render and a drawing both could carry the beat (B13, B14, B25), the real render won and the drawing is the runner-up.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: pasted onto a shape, looked up by address).
- [x] The framework before the first example: the table, the address and the lookup (B02) come before any shader line (B03).
- [x] A worked example that uses the framework visibly: the dissolve (B17 to B25) reads a noise table and a ramp table by address.
- [x] An edge-case or failure beat, in full: the first version burns pixels at progress zero (B25, 160 pixels, kept); a hinted mask moves a threshold (B38); the missing hint hides in Compatibility (B37); a tween without a start value fails (B26).
- [x] Every term the film teaches is defined on screen where first spoken, in GLOSSARY wording where the GLOSSARY has it (cue labels on the code line, captions, Manim labels, table notes); BDEFS holds prerequisites only.
- [x] Concrete before abstract: each color operation is shown on the four-patch picture before its name is used for anything else; the two-renderer surprise (B27) comes before its explanation (B29 to B31).
- [x] A measured claim says machine and renderer: "On this Mac" aloud, the renderer in every `videoLabel` that shows a number, machine and engine in both tables; what was not tested (lit 3D surfaces, other GPUs) is said ("in this test") or left out.
- [x] A thing that surprises is demonstrated by a real run (modulate thrown away B09, alpha hole B12, the two midpoints B27, washed out B35, the double conversion B36).
- [x] Payoff uses every earlier idea together (B23 and B41: lookup, mask, step, discard, ramp, hint).
- [x] Scaffolded viewer task: BHTF is a prompt to paste plus two checks the viewer makes on the result (the ends of the dissolve; where the hint is).
- [x] Standalone: no reference to any other film, book or course; no number on any viewer-facing surface (lint).
- [x] No source, no verdict: every beat that states a fact carries a capture with its probe values, a table with its credit, a Manim picture drawn from measured numbers, or the docs page; the verdicts are in `FACTCHECK.md`.

## Risks for the build (not defects of the layout)

1. **Shared components.** `ShaderLab`, `shader_kit.py` and the capture harness are built once for all shader films; they may already exist. This film adds harness features (CAPTURE-PLAN section H) with a verified reference implementation.
2. **GATE T on dark pixels.** The 0.2 gray end of the two strips in B27; the grey noise in B04's third still (after the 50 % mark on purpose) and in the editor frame E1's preview; B04's second still (the gradient has a black corner at the 50 % frame): see `BUILD-PROMPT.md` for the fallbacks. In the swatch picture the darkest channel is 0.35, so a patch never nears ink except in B09's left panel (the 50 % modulate), where a square patch is not text-shaped.
3. **GATE T and the accent color.** Terracotta is only rings and dots. The swatch patch is a rose (not a coral) and the burn ramp's middle stop is `#F08A2C` so no flat patch or rim pixel falls within the accent tolerance of `#D97757`.
4. **Gate V.** Pale card on a pale stage in B12; the sprite almost gone at B01's 85 % frame (the sweeps end at 97 % of the beat to keep content in frame).
5. **Editor frames are recorded (by script)**: copy them, no click and no recording by hand; the dark editor UI is the GATE T risk (risk 2).
6. **Pace.** The longest beats are B35 (48 words), B32 (47) and B29 (46): if a voice check runs long, split B29 or trim B32. The cut line in `ACTS.md` would save about 1.2 minutes (72 seconds by the same estimate).
7. **Lab and harness queue.** The Shader Lab's lock is shared: batch renders (about 65 planning renders took 8 to 10 minutes here).

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py textures-and-color` → no errors, no warnings. The three rows that were OPEN (the Inspector's menu wording for a noise texture, B18; how the Inspector draws a hinted and an unhinted color, B34; the renderer menu's labels, B40) were closed on 2026-10-13 from real editor frames: rows 52 (CORRECTED), 94 and 107 (PASS), plus row 106 (CORRECTED, docs versus run).

## Editor-frame reconciliation 2026-10-13

**What changed.** Beats B18 and B40 (narration, lane picture, capture spec) and the picture and spec of B34 were reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, sections 2.7, 2.8 and 11). **Why.** The first plan took its wordings from the docs and from convention; the frames show otherwise. Nothing was voiced, rendered or published.

- **B18.** The Inspector's resource menu is a heading **New** over bare class names (no entry starts with the word New), so "a New Noise Texture two D ... a New Fast Noise Lite" became "choose Noise Texture two D under New. Click it, then open its Noise slot ... choose Fast Noise Lite". The picture is five frames over two Inspector views: the NoiseTexture2D view (Width, Height, Noise, Seamless; no preview) and the FastNoiseLite view (the grey clouds preview, Seed). FACTCHECK row 52 is CORRECTED.
- **B34.** Confirmed, narration unchanged: **Picked** is a color swatch that opens a picker, **Typed** is four boxes x y z w. The lane now names the crop and measured ring boxes. Row 94 is PASS.
- **B40.** The docs say the renderer's name always sits in the editor's upper right corner; the shipped 4.7.2 editor hides it by default (it needs Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector). The beat now gives the path every student can follow: Project Settings, Rendering, Renderer, Rendering Method (forward_plus, mobile, gl_compatibility), then Save & Restart, over the Project Settings frames. Row 106 (the docs sentence) is CORRECTED, docs versus run; row 107 is PASS.

Beat ids, beat count (41 body), lane types and acts are unchanged. The two lines grew by 18 spoken words in all (B18 38 to 46, B40 35 to 45); `lint_series.py` now counts 1,918 words and 10.9 minutes. No fact-check row is OPEN.

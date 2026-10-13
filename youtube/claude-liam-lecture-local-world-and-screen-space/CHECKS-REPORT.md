# Checks report (PROOF GATE): Local, World and Screen Space

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the risks the build must watch, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 40 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: Manim 24, ShaderLab captures 12, editor capture 1, terminal log 1, Remotion 2 (a docs capture and a table). Estimated 10.1 minutes, 1,770 spoken words. `lint_series.py` has no errors and no warnings. No fact-check row is OPEN (the Inspector's wording was settled by Node2D's property list and is confirmed by the real editor frames recorded by script on 2026-10-13). The build's main risks: the shared components may not exist yet, 24 Manim scenes with four film-local helpers, and E1.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 40 | every body beat has a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): manim 24 · capture 12 · remotion 2 · editor 1 · terminal 1.

Why the mix came out this way (each beat was auditioned, see SHOTLIST.md): the film is mostly about coordinate systems and conversions, which the router sends to Manim (24); every claim that is about what Godot does with a moving sprite, a camera or a texture is a real capture (12 plus the editor frames); a code-only beat uses the code card, the one terminal beat is a real compile log, the docs claim is the docs page itself.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "just a position" becomes "an address in some space").
- [x] The framework comes before the first example: B03 draws the three zeros before B04 to B07 give the numbers.
- [x] A worked example walks the framework with the framework on screen: one corner through local, world and screen (B04 to B07), then through the matrices in code (B10 to B16, B27, B28).
- [x] Edge cases get full beats: the compile error (B14), the smear without repeat (B20), the texture-pixel-size shortcut (B23), the wrong order (B29), the documentation that disagrees with the engine (B31), the stretched window (B34).
- [x] Concrete before abstract: the starfield with two behaviours opens the film (B01) before any word of theory; each matrix comes after the numbers it produces.
- [x] Every term the film teaches is defined on screen where first spoken, in the GLOSSARY wording: BDEFS holds the six prerequisites (Shader, Pixel, Origin, Space, Vertex, Texture); vector is defined in B12, matrix in B09, built-in and vertex() in B08, fragment() in B14 (a line the broken-shader script prints), varying in B15, UV in B17, screen space in B03, and the small words (`mix`, `distance`, `discard`, `fract`, `step`, `texture()`) on the lines that use them.
- [x] A measured claim says machine and renderer (every `videoLabel`; FACTCHECK header); scripted motion is labelled; the one place the documentation and the engine disagree is said aloud with the measured number.
- [x] A thing that surprises is demonstrated by a real run: stars that stay put (B21), the same stripes that cannot be told apart in a still (B36, B37), four methods with no seam (B33).
- [x] The payoff uses the earlier ideas together (B25) and the two-move test separates all three spaces (B36, B37).
- [x] The closing prompt is scaffolded: a prompt to paste and two checks the viewer makes by moving the sprite and the camera (BHTF).
- [x] No source, no verdict: every beat that asserts something carries a capture, a measured readout, a table or the docs page.
- [x] Standalone: no reference to any other film, book or course (lint); nothing viewer-facing is numbered.

## Risks for the build (not defects of the layout)

1. **Shared pieces.** `ShaderLab`, `shader_kit.py` and the capture harness may not exist yet (`../_godot-shaders-series/COMPONENT-SPECS.md`); the film also needs four film-local Manim helpers (SHOTLIST.md, "Must exist before the build").
2. **Scale of the Manim work.** 24 scenes, most of them variations on one diagram (`world_window_scene`); build that helper once and reuse it. Two scenes (B12, B18) are code build-ups: each still needs one non-text shape after the first frame (Gate A): a bracket, an arrow or a ring.
3. **GATE T and Gate V on captures.** The sky is mid-tone indigo (not near ink), the blob teal, the stripes white and teal, the tile gradient saturated; none should read as text, but look at the 50 % and 85 % frames of every capture. Rings are grey, never ink.
4. **The capture routes.** The 4K route triples screen-pixel numbers (`verify8.gd` R1), so the series rule (2026-10-13) puts shaders that read window pixels on 1920 by 1080 at scale 1: C10 (the four tiles) does; the other eleven captures read local, world or fraction-of-screen numbers and use the 4K route. Both routes give the same four-tile gradient (`verify13.gd`). Nothing on screen shows a screen pixel number read from a capture.
5. **Editor frame E1** (the picture for B11) is recorded by script: copy the clean-root pair, no click and no recording by hand (the dark editor UI is a GATE T risk: look at the 50 % and 85 % frames). B14's log and B31's screenshot are cheap. B11's ring boxes are measured from the frames; B31's are placeholders until its image exists.
6. **Pace.** The longest beats are B13, B19 and B34 (43 words) and B26 (41); if a voice check runs long, split B19 or B34. The cut line is in ACTS.md and SCRIPT.md.
7. **Pronunciation to listen for:** "vec four", "frag coord", "U V", "twelve-eighty by seven-twenty", "discard", "varying", "repeat enable". The dictionary is not edited here; report what is said wrong.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py local-world-and-screen-space`: 46 beats, 1,779 words by the lint's count (it adds three per terms-card entry and leaves out the outro), 10.1 minutes, 0 errors, 0 warnings (re-run after the shared lint changed on 2026-10-13; row 23, the Inspector's wording, is passed on `verify11.gd`'s property list, so no row is OPEN).

## Editor-frame reconciliation 2026-10-13

**What changed.** Beat B11's picture and capture description, and FACTCHECK row 23's evidence, were reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, section 2.5). **Why.** The first plan could not show the Inspector, so the lane described a picture from the property list (`verify11.gd`) and had a Manim fallback. No narration changed: the real Inspector reads Node2D, Transform, Position with fields x and y, exactly what the line says. Nothing was voiced, rendered or published.

- **B11.** The lane now uses the clean-root pair (Child selected: Position 50.0 px, 0.0 px; Parent selected: 500.0 px, 300.0 px; the Scene dock reads Scene, Parent, Child), whole frames, cross-dissolved, with measured ring boxes. The plan-exact scene (the root node itself is the transformed Parent) shows an editor warning triangle on the root, so it is not used. The dissolve moved from 0.42 to 0.58 of the beat so the parent's numbers appear when the voice reaches "a parent at five hundred, three hundred" (it fell before "a child at fifty, zero" was spoken). Row 23 is PASS with the frames as evidence; the Manim fallback is no longer needed.
- Beat ids, beat count (40 body), lane types and acts are unchanged; words unchanged (1,770 by the lint's count, 10.1 minutes). `lint_series.py`: no errors, no warnings.

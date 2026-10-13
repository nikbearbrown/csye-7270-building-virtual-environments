# Checks report (PROOF GATE): Reflections

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, the two series-consistency decisions (the word "mask", the capture route), the risks for the build, and the lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after a 4K render; and a decision that changes the film's wording or recording route needs its reason written down.
**Found.** 37 body beats, all SHOW; 2 CARD (the opening identity card and the terms card, both mandated); no HOLD, no PUNT. Lanes: capture 19, Manim 12, Remotion 4, editor 2. About 8.9 minutes (1,557 words). `lint_series.py` is clean (no errors, no warnings). Two decisions are recorded below: the painted layer is a **label map**, not a "mask", because the series reserves "mask" for a number from 0 to 1 per pixel; and **C08 alone is recorded 1:1**, because a Rect-mode box counts render pixels. Risks for the build: three shared components that do not exist yet, a pure-black window at the 50 % frame of B17, and the final layout having to keep a cream margin around the capture window.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 41 | the 37 body beats, plus the hesitant writer (BIDEA), the recap (BVDT), the Your Turn (BHTF) and the outro (BOUT), each with a motion that carries its claim |
| HOLD | 0 | none |
| CARD | 2 | the opening identity card (BOPEN) and the terms card (BDEFS): mandated bookends |
| PUNT | 0 | no text-only card stands in for a picture; act titles ride the first picture of each act |

Lane histogram of the 37 body beats (information, not a quota): capture 19 · manim 12 · remotion 4 · editor 2.

Acts: I A Map Nobody Sees (9 beats) · II When the Screen Is Copied (9) · III Building the Reflection (8) · IV Compare With a Range (7) · V Polish and Limits (4). Cut line: B31, B32, then B34 and B35, then B15 (`ACTS.md`, `SCRIPT.md`).

## Decision 1: "label map", not "mask" (2026-10-13, after the series consistency check)

The series `GLOSSARY.md` defines **mask** as a number from 0 to 1 per pixel saying how much of something to show (the Math Toolkit, Soft Edges and Light Shaders films use it so). The brief for this film, and the source course it follows, use "mask" for something else: a picture painted in flat colors where each color is a label (red for water, green for coast). A viewer who had met the series word would be confused, so this film does not use it:

- The painted layer is a **label map**: defined on the terms card (`a layer of flat colors; each color is a label`) and again in B03, called "the map" afterwards. Terms card, BIDEA ("a shader can learn that from a map"; the correction types "a map the shader can read"), recap, Your Turn prompt, the opening description, the on-screen captions and readouts all use it.
- The Godot node is `LabelMap` (the Scene dock frame shows it); the color the shader reads is `label` in the code (`vec3 label = texture(screen_texture, SCREEN_UV).rgb;`: "the color it finds is the label", B23). The shader files were re-compiled in the Shader Lab after the rename (8 of 8 exit 0) and every planning run was repeated (index: `evidence/planning-checks/RESULTS.md`).
- The number the shader computes from each label (`water`, one or zero; then the alpha sum) is a mask in the series' sense. The film does not need the word, so it never says it.
- What still says "mask": the brief's own words quoted inside `FACTCHECK.md`, `ACTS.md` and `SOURCES.md`, and the identifiers and log field names in the evidence scripts (`mask_coloured_pixels`, `make_mask_image`). None of it is viewer-facing.

## Decision 2: which route each capture uses

Eighteen captures are recorded on the 4K route (a 3840 x 2160 SubViewport over the 1280 x 720 canvas) because none of this film's shaders reads a pixel count (`SCREEN_UV` only): all 65 probes of the 19 captures are equal on both routes (run-14). **C08 is recorded 1:1 and enlarged 3x by whole pixels**, because a `BackBufferCopy`'s Rect box counts render pixels: its default box is 101 px of the render target, which is only 34 canvas units on the 4K route (run-13), so the 4K route would show a patch a third the size of the one a game window gives (run-10). Details and evidence: `CAPTURE-PLAN.md`, "Which route each capture uses", and `FACTCHECK.md` rows 30 and 71. The capture pipeline itself was run end to end (run-17): all 19 clips recorded through `capture_all.sh` at their beats' lengths, each 3840 x 2160, 30 fps and exactly length x 30 frames, and looked at on a contact sheet (`evidence/planning-checks/png/contact-sheet-recorded-clips.png`): every 50 % and 85 % frame shows what the last column of the capture table says.

## Terms card against the GLOSSARY

| Term on the card | GLOSSARY row | Wording |
|---|---|---|
| Shader | shader | identical: "a small program the graphics card runs to decide how something is drawn" |
| Screen texture | none (only `SCREEN_UV`) | "a picture of what is drawn so far, readable by a shader" (Godot docs: "a special texture to access the already rendered contents of the screen") |
| Draw order | none | "which things are drawn first; later ones cover earlier ones" (Godot docs: "Canvas items are drawn in tree order on their canvas layer") |
| Label map | none (the series word is mask, a different thing: Decision 1) | "a layer of flat colors; each color is a label" |
| Reflection | none | "a flipped, fainter copy seen in water" |

The lint compares each card term with the GLOSSARY: no differences reported. The film also teaches `BackBufferCopy`, copy modes, `RemoteTransform2D`, screen U V, alpha, distance and mix on screen where first spoken (cue labels and captions); the GLOSSARY has no row for the first four of those, so their wording comes from the Godot docs, and alpha and U V use the GLOSSARY's.

## Teaching arc (checked against `SCRIPT.md`)

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: "a second drawing of the scene" becomes "a map the shader can read").
- [x] The central idea (a shader looks up a hidden map of the water) is shown in motion before it is named in code: the real walk in B01, the map itself in B03, the code from B10 and B23.
- [x] Every term the film teaches is defined on screen where it is first spoken; the terms card holds prerequisites only.
- [x] Concrete before abstract: each rule is shown on a real render (copy positions B12 to B14) before it is generalised (modes B16, layers B15); equals fails on a real pond (B28) before the eight-bit reason (B30).
- [x] Every measured number says machine and renderer (B30 credit line; the renderer table B31; the pure-values table B33); what was not measured is not claimed (no speed claim anywhere).
- [x] Things that surprise are demonstrated by a real run: a black window (B17), a map that is invisible and still does the work (B24), equals failing (B28), 0.502 not 0.5 (B30).
- [x] The payoff uses every earlier idea together: the Your Turn prompt names the map first, the copy node in viewport mode, the opaque ground, the distance within a tenth, and two checks.
- [x] Honest limits (B36, B37): the character only; a jump moves the reflection the wrong way. Which way it flips is said (B19: upside down; B37: it rises where a real one would drop).
- [x] Scripted input is labelled "scripted" on every capture; offline fixed tick rate, so no real-time frame rate is claimed.
- [x] Standalone and unnumbered: no other film, book or course is named (lint); the film carries no number anywhere in its title or description.

## Risks for the build (not defects of the layout)

1. **Three shared components do not exist yet**: `ShaderLab`, `shader_kit.py` and the shared capture harness (`../_godot-shaders-series/COMPONENT-SPECS.md`). This film brings its own capture tool (`evidence/planning-checks/capture_scene.sh`, `capture_all.sh`), which a shared harness may replace, and four small drawing objects of its own (`BUILD-PROMPT.md`, Phase 0).
2. **B17's window is pure black at the 50 % frame** (14 % of the capture's area). GATE T reads pixels within 48 RGB of ink (#3D3929) or mute (#5D584F) as text; pure black is 93 and 150 away, and the toolkit's own mask run on the 50 % and 85 % frames of all 19 captures finds no text-like blob (run-16). If the real frame still fails, shrink the window (`make_window` in `capture_scenes.gd`) and re-record C08; the story does not change.
3. **Polarity.** The red-filled frames (C02, C03, and C13 at 85 %) would flip GATE T's polarity detector to "dark" if a capture filled the frame edge to edge (run-16). The final layout keeps the cream stage margin around the framed window, as `SHOTLIST.md` specifies.
4. **Editor frames and docs screenshots are recorded by the build.** The scripted route works end to end (planning frames E1 and E2 are in `evidence/planning-checks/png/`); the ring boxes of E1 and E2 were measured on those crops, and the two docs-screenshot ring boxes (B16, B27) are placeholders to measure on the real captures.
5. **Pace.** B33 (45 words) and B14 (41) are the longest beats; if the voice check runs long, trim B33 first. The film is 8.9 minutes, below the series' preferred band, by design: nothing is padded, and the cut line is for the opposite case.
6. **Voice.** Listen for "Back Buffer Copy", "Remote Transform two D", "screen U V", "H D R two D", "Forward Plus" and "point five oh two". Do not edit the pronunciation dictionary; report a stumble to Bear.

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py reflections` → no errors, no warnings at the time of writing (the last step of the layout, after every other file was written).

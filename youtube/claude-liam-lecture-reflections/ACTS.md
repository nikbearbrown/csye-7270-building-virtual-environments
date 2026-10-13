# Acts and coverage map: Reflections

**What this is.** How the brief for this film (and the third-party course it follows) is spread over five acts: which part lands where, what moved, what was left out and why, plus the cast per act, the opening correction, the terms card, what the film adds, and the cut line.
**Why.** Bear's rule is at most 15 minutes, preferably about 10, and every idea needs a home. This file is the record that nothing was dropped silently and that every addition was checked.
**Found.** Five acts, 37 body beats, about 8.9 minutes by the lint's ceiling estimate (1,557 words). The brief's four suggested acts are all covered; its fourth ("Polish") became two acts, because the comparison with a tolerance needed seven beats of evidence on its own. Eleven things are in neither the brief nor its source (list below), three claims were corrected, and one finding (the Rect-mode box ignores the node's transform and counts render pixels) is new to the docs as far as the fetched pages go.

## The source (third-party; nothing copied)

A video course on 2D shaders in Godot, about 13 minutes of which cover this topic (creator not named; Bear has not named it). The layout agent saw only the brief's paraphrase in `../_godot-shaders-series/briefs/reflections.md`, never the course's text. See `SOURCES.md`.

## Coverage of the brief

| Brief item | Where it goes | Note |
|---|---|---|
| The one idea: a shader that reads the screen sees everything drawn before it; BackBufferCopy decides when; a hidden mask layer (this film: the label map) between copy and art | **Acts I and II** (B03 to B09, B10 to B18) | Said in the viewer's order: the problem (a map nobody should see), then the fix |
| BIDEA correction `a second drawing of the scene` to `a mask the shader can read` | Opening: `a map the shader can read` | The brief's text had the trigger split by a line break (lint error): the break moved (FACTCHECK row 67). The word is `map`, not `mask`: see Naming below |
| Terms card: screen texture (recap), mask, draw order, reflection | Opening | Plus **shader**, because the film is standalone; **mask** became **label map** (see Naming below) |
| Act 1, The Hidden Mask Problem (the brief's name; the act is titled A Map Nobody Sees): per pixel "is this water?", a flat-color layer (red water, green coast), but not visible | **Act I** | B02 to B05; the pond picture is generated procedurally, nothing painted elsewhere |
| Act 2, BackBufferCopy: three colored sprites and an overlay shader that reads the screen; the copy node after all three, then between sprites; copy modes viewport, rectangle, disabled (docs) | **Act II** | The overlay is a small window showing the whole screen texture (B10 to B14); modes with the docs page (B16); the Rect mode's default box and the black read (B17, B18) |
| Act 3, A Reflection: a copy of the animated character, flipped, below the original, kept in step with RemoteTransform2D; its shader reads the screen at its own position, red means alpha 1, else hidden | **Act III** | B19 to B24. "Animated character": the capture uses the series' test sprite walking (a translation). A copy of an *animated* sprite also needs the same animation frame; RemoteTransform2D pushes position, rotation and scale only. **LEFT OUT** with this reason: it is not shader content and the docs sentence is short; a viewer who animates the character will see it at once |
| Act 4, Polish: compare with a small tolerance, not `==`; a coast value with lower alpha; a blue tint with `mix` | **Acts IV and V** | Tolerance in Act IV (B27 to B33, with the eight-bit reason, the renderer table and the pure-values rule); coast and tint in Act V (B34, B35) |
| Cut line: the coast and tint polish | `CUT_LINE` (below) | |
| Captures: custom scenes only, node trees and scripted movement described exactly | `CAPTURE-PLAN.md`, `evidence/planning-checks/capture_scenes.gd` | Nineteen scenes, each run and checked |
| Source claim to check: exact `==` on floats | **Act IV** | CORRECTED (FACTCHECK 66): works on pure 0 and 1 here, fails on a mid value, and the docs warn |
| Source claim to check: is the mask layer (this film: the label map), drawn before the copy, hidden from the visible result, with no flicker or ordering surprise | **Act III** (B24, B25) | PASS (FACTCHECK 70): 0 label-map-coloured pixels in four positions, 90 walking frames with no mismatch, no one-frame lag |
| Source claim to check: BackBufferCopy modes and the "viewport mode requirement" (quote the docs) | **Act II** (B16 to B18) | CORRECTED (FACTCHECK 68): the docs quote the modes; the measured extra is the Rect box |
| Other films cover: the basics of `hint_screen_texture` and full-screen effects; masks as math | One beat of recap (B10) | The film is standalone, so the hint is explained once on the code line. "Masks as math" (shapes drawn by formulas) is **LEFT OUT**: this film's label map is painted, not computed |

## Added: in neither the brief nor the source (each is checked, FACTCHECK.md)

1. A window that shows the screen texture, and the node moved through the tree: after C, between B and C, between A and B, before A (B10 to B13).
2. The second shader reuses the first copy; a new node between them refreshes it (B14).
3. Z index and canvas layers change the order and the copy follows them, but a copy only serves its own canvas layer (B15).
4. A disabled node is skipped (B16).
5. A new node starts in Rect mode and its default box covers only a corner of the screen, wherever the node is (the box is measured in render pixels, so the capture of this beat is recorded 1:1: CAPTURE-PLAN.md, FACTCHECK 71); outside the box the read is black on a fresh process and stale pixels otherwise (B17).
6. The Label Map node switched off changes exactly the reflection's pixels and nothing else (B24).
7. Both wrong orders in one scene: copy after the art (no reflection) and map over the art (red sea) (B25).
8. Art at ninety percent opacity leaks the map (B26).
9. Equals against a half-strength map fails; against 128 over 255 it passes in Forward+ and fails in Compatibility; a distance passes in both (B28 to B31).
10. Pure values read back the same with HDR 2D on; half strength reads 0.502 or 0.216 (B33).
11. The limits: the character only, and a jump moves the reflection the wrong way (B36, B37).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I A Map Nobody Sees | the pond (grass band, water, sand spit); the teal test sprite and its reflection; the red-and-green label map; the slab stack (map, art, character) with its copy frame |
| II When the Screen Is Copied | the three squares A (teal), B (blue), C (lavender); the window with its border; the BackBufferCopy node chip |
| III Building the Reflection | the teal test sprite and its flipped copy; the node tree (Player, RemoteTransform2D, Reflection); the pond with its sandbar |
| IV Compare With a Range | the half-strength pond; the 0 to 1 ramp strip with ticks; the red and green points of the color plane |
| V Polish and Limits | the pond with the coast ring; the blob jumping at the shore |

## Opening correction and terms

- **BIDEA**: the writer types "A reflection needs a second drawing of the scene." and replaces "a second drawing of the scene" with "a map the shader can read".
- **BDEFS** (prerequisites only): Shader, Screen texture, Draw order, Label map, Reflection. The terms this film exists to teach (BackBufferCopy, copy modes, RemoteTransform2D, screen U V, alpha, distance, mix) are earned in their acts and defined on screen where first spoken (cue labels and captions use the GLOSSARY's wording; the GLOSSARY has no entry for BackBufferCopy, RemoteTransform2D, distance or screen texture, so their wording comes from the Godot docs).
- **Naming: label map, not mask (decided 2026-10-13 after the series consistency check).** The series GLOSSARY defines **mask** as a number from 0 to 1 per pixel saying how much of something to show (defined in the Math Toolkit film, recapped by the others). The brief and the source course use "mask" for the painted layer of flat colors, so a viewer who had met the series word would be confused. This film therefore calls that layer a **label map** (defined on the terms card and again in B03), "the map" afterwards, names the Godot node `LabelMap`, calls the colour the shader reads `label` in the code, and never says "mask". The number the shader computes from each label (water one or zero, then the alpha sum) is a mask in the series' sense; the film does not need the word. The terms card wording for the other terms matches the GLOSSARY (shader) or has no GLOSSARY row (screen texture, draw order, reflection, label map). The evidence scripts and logs still say "mask" in identifiers and field names (`mask_coloured_pixels`, `make_mask_image`): they were written first and are not viewer-facing.

## Order and swaps

No swap against the brief's order. Two moves: the screen-texture recap (the brief's recap) is one beat inside Act II (B10) rather than a section; the brief's Polish act is split into Acts IV and V.

## Cut line

If the film runs long, cut in this order: the renderer-table beat (B31), the color-distance picture (B32), the polish pair (B34 coast, B35 tint), then the canvas-layer beat (B15). Each repeats an idea another beat carries or covers a rarer case. The hidden-map idea (B03 to B09), the copy positions (B12, B13), the Rect trap (B17), the lookup and its code (B22, B23), the map toggle (B24) and the equals failure (B28 to B30) stay: they are the proof and the payoff. Current estimate: about 8.9 minutes, so no cut is needed.

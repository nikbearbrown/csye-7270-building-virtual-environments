# Acts and coverage map: Godot Shaders

**What this is.** How this film is built from its two sources: which part of each lands in which act, which parts move to a later film in the series, and which are left out, each with a reason. Also the cast per act, the opening correction, the terms card, the additions that are not in either source, and the cut line.
**Why.** Bear split a seven-hour course and a short intro into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 43 body beats, about 10.5 minutes. The short intro video is covered end to end except its second half (world-space UVs, screen UVs and the water shader), which belongs two films later. The long course's first nine chapters feed this film for ideas only; its visual-node editor material is left out on purpose. Eight things in the film are in neither source (list below), and five source claims were corrected.

## The two sources (both third-party; nothing copied)

- **A. A short introduction to Godot shaders** (about 8 minutes, pasted by Bear 2026-10-13; the creator is not named in the text). Timestamps below are from that transcript.
- **B. A seven-hour course on 2D shaders in Godot** (28 chapters; the YouTube cut of a paid course; creator not named in the text). Chapter times are Bear's list.

## Coverage

| Source and part | Where it goes | Note |
|---|---|---|
| A 0:00 to 1:05: what a shader is, why it is parallel, the gradient with a GDScript loop versus one shader line | **Act I**, B02 to B08 | The loop and the shader are both run and timed on Bear's Mac; the source's "faster and cheaper" is CORRECTED to measured CPU numbers only |
| A 1:05 to 1:21: creating a shader material in the editor | **Act II**, B09 to B10 | Real editor frames (E1) |
| A 1:21 to 2:40: shader type, uniforms with RGB sliders, the processor functions (vertex, fragment, light) | **Acts II to IV**, B12 to B14, B15, B21, B25 to B31 | Reordered: the smallest working shader first, then the functions, then the dial |
| A 2:40 to 3:10: UV and the gradient | **Act V**, B36 to B37 | |
| A 3:10 to 3:47: TIME, sine, fade-in against Tween | **Act V**, B39 to B41 | The source says TIME is time since the shader or scene was created: CORRECTED (one global clock) |
| A 3:47 to 4:39: UV scaling and tiling | **MOVED** to *UV Space* | UV bending is its own film |
| A 3:47 to 4:39: world-space UV with `MODEL_MATRIX`, `varying` | **MOVED** to *Vertex Shaders* (varying) and *Local, World and Screen Space* (world position) | Needs vertex and matrices first |
| A 4:39 to 5:35: radial fade (distance and radius) | **Act V**, B42 to B43 | Rebuilt as the iris: the payoff of the film |
| A 4:39 to 5:35: clock-hand sweep with `atan`, `smoothstep`, noise reveal | **MOVED** to *Trigonometry for Shaders* (angle) and *Soft Edges, Glow and Noise* (smoothstep, noise) | Math functions are taught where they are used |
| A 5:35 to 6:04: `SCREEN_UV` against `UV` | **MOVED** to *Reading the Screen* | |
| A 6:04 to 8:12: the 2D water shader (waves, screen texture, mix, overlay, foam) | **MOVED** to *Reading the Screen* (screen texture, distortion) and *Time and Waves* (the wave math) | Too large for a ten-minute orientation film; it is the payoff of two later films |
| B ch. 1 (0:00 to 1:20): course introduction and sales | **LEFT OUT** | Promotion, not teaching |
| B ch. 2 Shader theory (1:20 to 5:00) | **Act I** | CPU against GPU; per-pixel thinking. The "oversimplified definition" it promises to repair is repaired here (Acts I and III) |
| B ch. 3 Fragment basics (5:00 to 27:14): editor setup, ports and types, UV concept | **Acts II and V** for the editor path and UV; **MOVED** for step, distance, circle (*Drawing Shapes with Math*) | The **visual shader node editor** content (ports, node types, previews) is **LEFT OUT**: these films teach code shaders, because that is what the docs, shader sites and AI assistants produce; Godot generates the same code from a graph |
| B ch. 4 Fragment colors (27:14 to 39:35) | **MOVED** to *Textures and Color* and *Godot Shader Language* (type conversions); the TIME node idea to Act V | |
| B ch. 5 Textures (39:35 to 55:45) | **MOVED** to *Textures and Color* | |
| B ch. 6 Vertex basics (55:45 to 1:08:27) | **Act III** (vertex idea) and **MOVED** to *Vertex Shaders* | |
| B ch. 7 Variables (1:08:27 to 1:22:06) | **Act IV** (set from GDScript, Tween); `varying` **MOVED** to *Vertex Shaders* | |
| B ch. 8 Shader code (1:22:06 to 1:44:31) | **MOVED** to *Godot Shader Language*; the uniform, hint and texture-uniform lines in **Act IV** | |
| B ch. 9 Shader definition (1:44:31 to 1:55:53) | **Act III**, B15 to B20, B22 | Its three repairs (vertex before fragment; a fragment is a pixel-to-be; the vertex stage works on vertices) are the spine of Act III. Its explanation of why a circle goes oval is CORRECTED and moved to *UV Space* |
| B ch. 10 to 28 (crosshair to light position) | **MOVED** to the later films named in `../_godot-shaders-series/SERIES-PLAN.md` | |

## Corrections to the sources (full detail in FACTCHECK.md)

TIME is one global clock (rows 46 and 47); "faster and cheaper" becomes measured CPU time with the GPU side stated as unreadable (57); the vertex stage moves corners, not pixels (55); fragments-are-stretched is not why circles go oval (56); a light shader *can* read UV in Godot 4.7 (58).

## Added: in neither source (each is checked, FACTCHECK.md)

1. The measured loop against the measured shader hand-over, with the honest GPU gap (B04 to B07).
2. The sourced answer to "pixel or fragment, and why two words" (B19, B20), with the `discard` proof.
3. The measured fifty-pixel lean with its five edge samples (B16, B17).
4. `light()` runs once per light and the results add, measured 0.2, 0.4, 0.6 (B21).
5. A hint does not clamp a value set from code (B30).
6. A misspelled uniform name is a silent no-op, and names are case-sensitive (B31, B32).
7. A tween needs the uniform set from code first (B33, B43), found by a failed run.
8. A late node sees the global clock (B40), shown by a real run.

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I One Pixel, All at Once | the teal test sprite; the pixel grid; the 0 to 1 ramp strip |
| II Setting Up a Shader | the node, ShaderMaterial and Shader boxes (and the same sprite inside the editor frames) |
| III The Three Functions | the test rectangle with four terracotta corner dots; the pixel grid; the checker square |
| IV Dials: Uniforms | the dial (a slider with a knob); the rectangle it colors |
| V Where Am I, and When? | the UV square with its (u, v) dot; the ramp strip; the checker square |

## Opening correction and terms

- **BIDEA**: the writer types "A shader decides the color of the whole screen." and replaces "the whole screen" with "one pixel".
- **BDEFS** (prerequisites only): GPU, Pixel, Vertex, Texture, Material. The terms this film exists to teach (shader, fragment, built-in, uniform, hint, UV, TIME) are earned in their acts, each defined on screen where it is first spoken (wording from `../_godot-shaders-series/GLOSSARY.md`).

## Cut line

If the film runs long, cut in this order: the budget-bars beat (B05), the typo beat (B32), the editor-slider beat (B27), the tween beat (B33). Each repeats an idea another beat carries. The lean pair (B16, B17), the discard beat (B20) and the iris (B42, B43) stay: they are the proof and the payoff. Current estimate: about 10.5 minutes, so no cut is needed.

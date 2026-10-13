# Series plan: Godot shaders

**What this is.** The plan for a series of twenty standalone lecture films on Godot shaders, each no more than 15 minutes and aiming for about 10, made from two sources (a short introduction and a seven-hour course on 2D shaders, both third-party) plus one film added for 3D. Every film is laid out in full: script, beat sheet, the picture for each beat, fact-check, capture plan and build handoff.
**Why.** Bear's verdict on the Signal Garden slate cut was that viewers must first be told what a shader is. This series is that explanation, sized as lectures (the seven-hour original is far too long to watch), and it ends by making the Signal Garden pad shader readable line by line.
**Found.** The seven-hour course regroups into twenty concept films by *idea*, not by chapter order. Sixty-four things the sources, the docs or my own briefs said turned out loose or wrong when run in Godot (see "What the layouts found"). One film (3D) is not in either source and is needed for Signal Garden. All twenty are laid out; nothing is voiced, recorded, rendered or published. Next: Bear reads the scripts; then a medium-effort Claude Code session builds, starting with the pilot.

**Found, in short.**
- Twenty standalone films, 933 beats, about 3.4 hours at the lint's ceiling estimate (nothing is voiced yet, so the real total is shorter), every one between 8.9 and 10.9 estimated minutes. The shortest cut line per film is written down.
- Every Godot claim in them was run in Godot 4.7.2 (1,600+ fact-check rows). **64 claims from the sources, the docs or my own briefs turned out wrong or loose and were corrected**; they are listed below.
- The real Godot editor can be driven by a script and recorded, so **you record nothing by hand**. That also showed several click paths in the sources were wrong.
- Signal Garden: its pad shader reads different pixels in the two renderers, its pad is a thin box not a quad, and at half charge its stripes are nearly invisible. The redo can say all that.
- Needs you: the eight decisions at the end (playlist and titles, credit, scope, build order, the parallel "shading" film, course credit, Signal Garden timing).

## The series at a glance

Order within a group is the order I would watch and build in. Titles other than the first two are working titles. **Nothing viewer-facing carries a number or a count.**

**Foundations**
- **Godot Shaders**: a shader decides the color of one pixel and the card runs it for every pixel; the three functions; dials (uniforms); where a pixel is and what time it is. *(Bear's title. The pilot: fully worked.)*
- **Godot Shader Language**: read any shader by asking "what type is this?"; vectors, strict types, your own functions.
- **The Shader Math Toolkit**: about a dozen functions, each a reshaping of a 0-to-1 ramp.
- **Textures and Color**: a texture is a lookup; color is math; and the color you set is not always the color you see (two renderers, two pixels).
- **Shaders in 3D**: same shape, new names; ends by reading the Signal Garden pad shader. *(Added; not in the course.)*

**Fragment techniques**
- **UV Space**: scale, shift, mirror, center and clip the address before you look.
- **Patterns and Pixelation**: `floor` and `fract` make cells; cells make pixels, checkers, stripes and dots.
- **Drawing Shapes with Math**: a shape is a question each pixel answers; a crosshair with sliders.
- **Soft Edges, Glow and Noise**: `smoothstep` softens a cut; a shield; and the truth about glow.
- **Time and Waves**: one global clock, the sine wave and its four knobs.
- **Trigonometry for Shaders**: angle in, position out; an orbit.
- **Lines and Shine**: a line is a rule; a shine sweeps a sprite.
- **Outlines**: each pixel asks its neighbors.

**Vertex and space**
- **Vertex Shaders**: you can only move the corners that exist; a flag.
- **Matrices and Fake 3D**: a matrix is a saved move; a card flip.
- **Local, World and Screen Space**: the same point, three sets of numbers.

**Screen, textures and light**
- **Reading the Screen**: post-processing and water.
- **Reflections**: `BackBufferCopy` and a hidden mask.
- **SubViewports**: shade the result of shading.
- **Light Shaders**: take over what a light does.

<!-- TABLE:START -->
## The twenty films in numbers

Read from the films' own files (`series_table.py`). Minutes are the lint's ceiling estimate (every spoken word at 0.34 s, plus 4 s); the real length is known only after the voice is generated and usually comes out a little shorter.

| Film | Beats | Words | Est. min | Lanes (manim / capture / remotion / editor) | OPEN rows | Lint |
|---|---|---|---|---|---|---|
| **Foundations** | | | | | | |
| Godot Shaders | 49 | 1868 | 10.7 | 18 / 17 / 6 / 2 | 0 | clean |
| Godot Shader Language | 47 | 1918 | 10.9 | 22 / 8 / 6 / 0 | 0 | clean |
| The Shader Math Toolkit | 47 | 1815 | 10.4 | 23 / 16 / 2 / 0 | 0 | clean |
| Textures and Color | 47 | 1918 | 10.9 | 7 / 27 / 4 / 3 | 0 | clean |
| Shaders in 3D | 50 | 1814 | 10.3 | 14 / 24 / 5 / 1 | 0 | clean |
| **Fragment techniques** | | | | | | |
| UV Space | 48 | 1812 | 10.3 | 17 / 19 / 6 / 0 | 0 | clean |
| Patterns and Pixelation | 49 | 1790 | 10.2 | 18 / 22 / 3 / 0 | 0 | clean |
| Drawing Shapes with Math | 50 | 1900 | 10.8 | 15 / 25 / 3 / 1 | 0 | clean |
| Soft Edges, Glow and Noise | 48 | 1791 | 10.2 | 15 / 23 / 2 / 2 | 0 | clean |
| Time and Waves | 46 | 1690 | 9.6 | 18 / 18 / 4 / 0 | 0 | clean |
| Trigonometry for Shaders | 46 | 1752 | 10.0 | 23 / 13 / 4 / 0 | 0 | clean |
| Lines and Shine | 41 | 1587 | 9.1 | 14 / 21 / 0 / 0 | 0 | clean |
| Outlines | 47 | 1868 | 10.7 | 11 / 27 / 3 / 0 | 0 | clean |
| **Vertex and space** | | | | | | |
| Vertex Shaders | 46 | 1730 | 9.9 | 12 / 27 / 0 / 0 | 0 | clean |
| Matrices and Fake 3D | 47 | 1791 | 10.2 | 22 / 15 / 4 / 0 | 0 | clean |
| Local, World and Screen Space | 46 | 1779 | 10.1 | 24 / 12 / 2 / 1 | 0 | clean |
| **Screen, textures and light** | | | | | | |
| Reading the Screen | 44 | 1685 | 9.6 | 11 / 25 / 2 / 0 | 0 | clean |
| Reflections | 43 | 1557 | 8.9 | 12 / 19 / 4 / 2 | 0 | clean |
| SubViewports | 46 | 1840 | 10.5 | 16 / 22 / 0 / 2 | 0 | clean |
| Light Shaders | 46 | 1808 | 10.3 | 12 / 25 / 3 / 0 | 0 | clean |

**Totals.** 20 films, 933 beats, 35,713 words, about 204 minutes (3.4 hours) of film; 0 OPEN fact-check rows in all.
<!-- TABLE:END -->

## How the seven-hour course maps (all 28 chapters)

Chapter lengths are from Bear's timestamps (the list ends at 7 h 14 min). "Left out" means by design.

| # | Chapter | Time | Length | Goes to |
|---|---|---|---|---|
| 1 | Intro | 0:00:00 | 1:20 | left out (promotion) |
| 2 | Shader theory | 0:01:20 | 3:40 | *Godot Shaders* |
| 3 | Fragment basics | 0:05:00 | 22:14 | *Godot Shaders* (setup, UV idea), *Drawing Shapes with Math* (circle, `step`); the visual-node editor material is left out |
| 4 | Fragment colors | 0:27:14 | 12:21 | *Textures and Color*, *Godot Shader Language* (type conversions), *Godot Shaders* (TIME) |
| 5 | Textures | 0:39:35 | 16:10 | *Textures and Color*, *UV Space* |
| 6 | Vertex basics | 0:55:45 | 12:42 | *Godot Shaders* (the vertex idea), *Vertex Shaders* |
| 7 | Variables | 1:08:27 | 13:39 | *Godot Shaders* (set from code, Tween), *Godot Shader Language*, *Vertex Shaders* (varying) |
| 8 | Shader code | 1:22:06 | 22:25 | *Godot Shader Language*, *Textures and Color* (`sampler2D`) |
| 9 | Shader definition | 1:44:31 | 11:22 | *Godot Shaders* (three repairs to the definition), *UV Space* (the oval, corrected) |
| 10 | Crosshair | 1:55:53 | 27:38 | *Drawing Shapes with Math*, *Godot Shader Language* (functions) |
| 11 | Shield | 2:23:31 | 25:31 | *Soft Edges, Glow and Noise* |
| 12 | Outline | 2:49:02 | 24:27 | *Outlines*, *Godot Shader Language* (if, for) |
| 13 | UV control | 3:13:29 | 22:37 | *UV Space*, *Patterns and Pixelation* |
| 14 | Pixelate | 3:36:06 | 5:58 | *Patterns and Pixelation* |
| 15 | Waves + trigonometry intro | 3:42:04 | 11:52 | *Time and Waves* |
| 16 | Trigonometry | 3:53:56 | 11:25 | *Trigonometry for Shaders* |
| 17 | Orbit | 4:05:21 | 15:41 | *Trigonometry for Shaders* |
| 18 | Shine | 4:21:02 | 14:01 | *Lines and Shine* |
| 19 | Vertex | 4:35:03 | 16:14 | *Vertex Shaders* |
| 20 | Flag | 4:51:17 | 12:23 | *Vertex Shaders*, *Time and Waves* (the wave formula) |
| 21 | Matrix math | 5:03:40 | 16:08 | *Matrices and Fake 3D* |
| 22 | Fake 3D | 5:19:48 | 11:24 | *Matrices and Fake 3D* |
| 23 | Model Matrix | 5:31:12 | 19:24 | *Local, World and Screen Space* |
| 24 | Canvas | 5:50:36 | 18:55 | *Local, World and Screen Space* (coordinates), *Reading the Screen* |
| 25 | Reflection | 6:09:31 | 12:57 | *Reflections* |
| 26 | Subviewport | 6:22:28 | 23:23 | *SubViewports*, *Patterns and Pixelation* (stripes), *Textures and Color* (hue, optional) |
| 27 | Light intro | 6:45:51 | 12:01 | *Light Shaders* |
| 28 | Light position | 6:57:52 | 16:13 | *Light Shaders*, *Patterns and Pixelation* (grid and dots) |

The short introduction (about 8 minutes) feeds *Godot Shaders* (all but its second half), *UV Space*, *Local, World and Screen Space*, *Trigonometry for Shaders*, *Soft Edges, Glow and Noise*, *Reading the Screen* and *Time and Waves*; its beat-by-beat home is in `claude-liam-lecture-godot-shaders/ACTS.md`.

## Why twenty films and not seven hours

About 7.2 hours of live-coded course becomes about 3.5 hours of films, because a lecture shows the idea once, with a picture, and does not wait for the typing. Each film has one idea, one payoff you can see, and one thing it corrects. Each is standalone: a viewer who has seen nothing else can follow it, so the order below is a *suggestion*, never a requirement, and nothing on screen says "next" or "part".

## Sequence and the Signal Garden test

Watching order: down the groups above. Shortest path to reading the Signal Garden pad shader: *Godot Shaders*, *Godot Shader Language*, *The Shader Math Toolkit*, *Shaders in 3D*; add *Textures and Color* for why its two renderers read different pixels. The pad shader, line by line, and which film teaches each part:

| Line of `signal.gdshader` | Taught in |
|---|---|
| `shader_type spatial;` | *Godot Shaders*, *Shaders in 3D* |
| `render_mode unshaded;` | *Shaders in 3D* |
| `uniform float activation : hint_range(0.0, 1.0) = 0.0;` | *Godot Shaders* (uniforms, hints), *Godot Shader Language* |
| `uniform vec4 quiet_color : source_color = ...;` (and `active_color`) | *Godot Shader Language* (`vec4`), *Textures and Color* (`source_color`) |
| `float stripe = step(0.5, fract(UV.x * 8.0));` | *The Shader Math Toolkit* (`step`, `fract`), *UV Space*, *Patterns and Pixelation* |
| `vec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);` | *Godot Shader Language* (swizzle, vector times number), *The Shader Math Toolkit* (`mix`) |
| `ALBEDO = mix(base, active_color.rgb, activation);` | *Shaders in 3D* (`ALBEDO`), *The Shader Math Toolkit* |

**Build order I recommend:** *Godot Shaders* first (it also builds the three shared pieces every film reuses), then the other four Foundations films, then the Signal Garden redo, then the rest group by group.

## The Signal Garden redo (not laid out yet)

It waits for the first films, as Bear said. What the shader work found that the first cut did not know: the pad shader at activation 0.5 reads (0.2588, 0.4392, 0.3059) in the Compatibility renderer the game uses and (0.2980, 0.5373, 0.3804) in Forward+, so the pixel check proves the game's renderer and nothing else. The *Shaders in 3D* layout also found that the game's pad is a thin box (1.55 by 0.10 by 1.55, read from `garden.gd`), not a flat quad, so its top shows only about a third of the stripes; that the shader is ten lines, not eight; that Mobile reads within one 8-bit step of Forward+; and that at half charge the dark and light stripes differ by only 3.5 on the CIE76 colour scale in Forward+, which is too faint to count, so the film's held stills use activation 0.3 (5.7 apart). A better second cut can say what a shader is (by now a viewer knows), read the pad shader line by line, show the 32 headless checks, show the one pixel check, show the seeded fault it alone catches, and say plainly what none of it proves.

## What the layouts found (everything below was run in Godot 4.7.2 on one Apple M4 Pro, unless it says "docs")

Full lists, by film, with the evidence row for each: `FINDINGS-COLLECTED.md` (generated) and each film's `FACTCHECK.md`.

**Where the sources, the docs or my briefs were wrong or loose**
- *Time.* `TIME` is one clock for the whole game, not time since the node or scene appeared; time scale changes it, pausing does not; the tick counter has its own zero and ignores time scale (Time and Waves, Godot Shaders).
- *Vertex.* A vertex shader moves corners, not pixels; four corners can only tilt, so a flag needs a cut mesh (297 vertices for 31 by 7). A box has 24 vertices, not 8.
- *The oval.* The sources say fragments are "stretched" while pixels are square. Wrong: `UV` runs 0 to 1 on both axes whatever the shape's proportions (UV Space, Toolkit, Shapes, Reading the Screen).
- *Math.* `smoothstep(0, 10, 1)` is 0.028, not 0.1; swapping `step`'s arguments is not an exact invert at the edge; `mod` follows `floor` on negatives and `%` is an error on decimals; `max(a, b)` equals `min(a + b, 1)` only for masks of exactly 0 or 1.
- *Patterns.* `floor(UV * n + 0.5) / n` is not centering (17 blocks, half-size ends); the corner lookup drifts half a block toward the bottom right.
- *Lines.* Without the divide a line's band gets thinner as it steepens (the brief said thicker); at 90 degrees nothing visibly breaks, the sign flips (`tan` reads about -23 million on this Mac).
- *Matrices.* Godot reads matrices by columns; translate-scale-rotate gives the same picture only for a uniform scale; "64 is the right edge" holds only for a centered sprite.
- *Light.* A light shader can read `UV` (the source says it cannot); a rebuilt default `light()` matches exactly except with a normal map.
- *Outlines.* The brief's `mix(color, line, outline - color.a)` goes negative on isolated opaque pixels; sprite sheets leak a stray line from the next frame; a sprite trimmed to its shape needs padding; the default texture filter is linear.
- *Colour.* sRGB and linear: a 0.2 to 0.8 blend reads 0.60 in Forward+ and Mobile and 0.50 in Compatibility on an unshaded 3D quad; hinting a mask moves a 0.5 threshold to about 0.74; passing a pre-converted color from code converts twice.
- *Glow.* "Multiply by five and it glows" is wrong: 2D glow needs a number above one, HDR 2D on, a WorldEnvironment with glow on and its background set to Canvas, and a dark surround.
- *Screen.* A canvas layer takes its own copy of the screen; `position / size` is wrong once a Camera2D moves; `filter_nearest` is not obeyed for the screen texture in Compatibility.
- *Reflections.* `==` on half-strength map colors fails; use a distance. A Rect-mode `BackBufferCopy` box counts render pixels.
- *Docs versus the engine.* The docs' operator table writes `vec3 + 2`, which fails; the docs say a `TextureRect` ignores `texture_repeat`, a shader obeys it; the docs give `FRAGCOORD`'s bottom right as (1, 1), the engine counts pixels; the docs say the renderer name is always in the editor's upper right, the 4.7.2 editor hides it by default; "New ViewportTexture" is a heading plus an entry.

**What the editor really shows** (`editor-capture/README.md`, 40 recorded states): the Material menu has a heading New then ShaderMaterial (no "New ShaderMaterial"); the Create Shader dialog starts on Spatial; uniforms sit under Shader Parameters with capitalised names; a `hint_range` float is a number box with a slider bar and a `source_color` vec4 a swatch that opens a picker; a project's renderer is set in Project Settings > Rendering > Renderer > Rendering Method and needs Save & Restart.

**Capture and tooling traps the build must respect** (all in `COMPONENT-SPECS.md` and `BUILDER-BRIEF-COMMON.md`): shaders that read window pixels or mip levels must be captured at 1920 by 1080, not through the 4K SubViewport route; a covered Godot window stops drawing and `TIME` stops with it (keep it on top, step the draw loop by 1/30); Movie Maker frame numbers are `get_process_frames()`; a pixel-ink ramp must be drawn as tiles or GATE T reads it as text.

**Signal Garden** (the redo): see the section above. In short, the pad reads (0.2588, 0.4392, 0.3059) in Compatibility and (0.2980, 0.5373, 0.3804) in Forward+ at half charge; it is a box, and its stripes are barely visible at half charge.

## Decisions for Bear

1. **Read the pilot script first** (`claude-liam-lecture-godot-shaders/SCRIPT.md`). Tone, depth and length changes there carry to the other nineteen, so settle them before reading the rest.
2. **Playlist and titles.** No playlist is named; the opening says only the film's title. Name it and every film is regenerated from one constant. *Godot Shaders* and *Godot Shader Language* are your titles; the rest are working titles.
3. **Editor captures: settled, no recording by you.** The real Godot editor is driven by a script and recorded (40 real states for four films, no human click; `editor-capture/README.md`). It also corrected several click paths the sources and I had wrong (see "What the layouts found"). The only thing a script cannot give is a visible mouse pointer; if you want one in a film, `editor-capture/README.md` section 9 is a five-minute take, optional.
4. **Credit for the two third-party sources.** The pasted text does not name the creators. Give me names and addresses if you want them credited in the YouTube descriptions. Nothing is copied.
5. **Scope.** Twenty is the full regroup. Candidates to drop or merge if you want fewer: *Lines and Shine* (into *Trigonometry for Shaders*), and the three advanced screen films (*Reflections*, *SubViewports*, *Light Shaders*).
6. **Build order**, and whether the Signal Garden redo waits for four films or all twenty.
7. **A parallel film on the same subject exists.** `claude-liam-lecture-godot-shading-language/` (note "shading", not "shader") was created today 13:13 to 15:12 by another session, not by this plan: 58 beats, about 12 minutes, a slate cut already rendered, and its opening names the course (CSYE 7270). It overlaps *Godot Shader Language* here (47 beats, standalone, no course name). I did not touch it. Pick one as the film, or keep both with different jobs.
8. **Course credit.** The shader films here are standalone: no course name anywhere, as the lecture skill says unless the film is for a course. The parallel film above names CSYE 7270. If you want these credited to the course, say so: it is one setting plus a regenerate of the opening and outro.

## What this plan does not claim

- Nothing is voiced, recorded, rendered or published. Estimated minutes come from word count at Liam's pace (0.34 s per word, median of 57 shipped films), not from audio.
- No Manim or Remotion scene is written. Three shared pieces do not exist yet (`ShaderLab`, `shader_kit.py`, the capture harness); the pilot's build creates them.
- The Inspector wording and widgets are checked against real editor frames (recorded by script; no mouse pointer is visible in them, and every such clip is labelled "scripted editor session").
- Every Godot result is for Godot 4.7.2 on one Mac (Apple M4 Pro), mostly in Forward+; where a pixel depends on the renderer, the film says which. Nothing says anything about real-time frame rate or other GPUs.
- Nobody has heard the voice read these scripts. Pronunciation of G L S L, U V, "Godot" and the like is checked at the voice stage.

## Where everything is

All under `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/`:

- `_godot-shaders-series/`: this plan, `REVIEW-ME.md`, `SERIES-TABLE.md`, `LINT-REPORT.md`, `GLOSSARY.md`, `BUILDER-BRIEF-COMMON.md`, `COMPONENT-SPECS.md`, `RECORDING-SESSION.md`, `briefs/` (one per film), `lab/` (the Shader Lab), the shared tools (`lint_series.py`, `make_sheet_shared.py`, `series_table.py`).
- `claude-liam-lecture-<slug>/`: one folder per film with `SCRIPT.md` (read this), `narration.py`, `beat_sheet.json`, `lanes/`, `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md`, `CHECKS-REPORT.md`, `SOURCES.md`, `CAPTURE-PLAN.md`, `BUILD-PROMPT.md`, `lab-shaders/`, `evidence/planning-checks/`.

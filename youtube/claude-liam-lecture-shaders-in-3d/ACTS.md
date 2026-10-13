# Acts and coverage map: Shaders in 3D

**What this is.** How this film is built from its brief and its primary sources: which item lands in which act, what was shrunk or left out and why, the cast per act, the opening correction and the terms card, the additions that are in neither the brief nor any source, and the cut line.
**Why.** This film carries everything from the two-D shader films into `spatial` shaders and ends by reading a real three-D shader; it is added to the series, not cut from a source. A coverage map is the record that no item of the brief was dropped silently, and that six points in the brief were changed or worked around because a run disagreed.
**Found.** Five acts, 44 body beats, about 10.3 minutes by the lint. Every item of the brief is in an act (the render-modes beat is shrunk to a sentence, as the brief allows). Six points of the brief changed or were worked around (listed below): four are statements of fact (a three-D fragment does have a `COLOR`, read-only; the pad shader is ten lines, not eight; the game's pad is a thin box, not a quad; the suggested stripe probes both read the dark stripe) and two are method (the Lab's quad cannot show lit against unshaded; the brief's opening trigger was split by a line break). Sixteen things are in neither the brief nor a source and were added after being run (listed below).

## Sources

- **The brief** (`../_godot-shaders-series/briefs/shaders-in-3d.md`): orientation only. It says the film is not in either third-party source.
- **The two third-party works** (a short introduction to Godot shaders and a long two-D course; both by creators Bear has not named): neither covers three-D. Nothing from them is used; `SOURCES.md` records that.
- **Primary**: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 (every number was measured in `evidence/planning-checks/`), and one real shader from a small game (`lab-shaders/12-signal-pad.gdshader`, byte-identical to the game's file).

## Coverage of the brief

| Brief item | Where | Note |
|---|---|---|
| Act "Same Shape, New Names": `shader_type spatial;`, the same three functions | **Act I**, B03 and B04 | The skeleton file is drawn in B02; B35 shows the pad using one slot of the three |
| Surface outputs (`ALBEDO`, `ALPHA`, `EMISSION`, `ROUGHNESS`, `METALLIC`) | `ALBEDO` and `ALPHA` in **B05**; all five in **B12** (Act II) | The five are named only after lighting makes them mean something. Each was compiled and rendered; the table is a table because `METALLIC` = 1 reads near-black without an environment (verify6) |
| "There is no `COLOR` here" | **B05, B06**: **CORRECTED** | `COLOR` exists in a three-D `fragment()` as a read-only input (the vertex color); the output is `ALBEDO`. Writing `COLOR` gives "Constants cannot be modified." (real message, B06) |
| `UV` follows the mesh's own map; a `QuadMesh` has the same addresses as two-D | **B08** (square, box, sphere), **B19** (corners), **B36** (the box payoff) | Verified from the mesh arrays and from rendered pixels (verify1) |
| Act "Lit or Unlit": lit by default | **B10 to B13** | The Lab's `quad3d` scene cannot show it (white ambient light at energy 1 makes lit and unshaded identical); the lamp scene (verify4) does |
| `render_mode unshaded;` | **B14, B15** | B15 is the docs themselves (SHOW-THE-THING) |
| A few other render modes by name | `cull_disabled` shown in **B17**; `blend_add` named in **B18** | The brief's "by name only" is exceeded for `cull_disabled` because a vanishing surface is the most common 3D "it is invisible" report |
| Act "A Surface That Changes": UV gradient | **B19** | |
| Stripes: `step(0.5, fract(UV.x * 8.0))`, `step` and `fract` glossed once each | **B20 to B23** | A ramp (B20), `fract` (B21), `step` (B22), the stripes on the real quad (B23) |
| Two `source_color` colors mixed by an `activation` uniform from 0 to 1 | **B24 to B26** | `mix` (B24), the dial and the uniform (B25), hints (B26) |
| Setting it from the game | **B27, B28** | `material_override` and `set_shader_parameter`, a tween |
| Act "Read a Real One": the pad shader line by line | **Act IV**, B29 to B34 | Whole shader (B29), lines 1 and 2 (B30), 3 to 5 (B31), 6 and 7 (B32), 8 (B33), 9 (B34) |
| Act "Which Renderer?": the pad at activation 0.5 in two renderers, two measured pixels | **Act V**, B37 and B38 | Forward+ and Compatibility, Apple M4 Pro |
| What it means: the mix happens on different numbers; full explanation left to the color film | **B39 to B41** | A plain grey (0.74 against 0.50), the linear-light curve in one picture, the two midpoints. The film names sRGB only to define it (B40, GLOSSARY wording) and to read the docs' `OUTPUT_IS_SRGB` (B42) |
| Close: "a number read from a pixel is only true for this renderer" | **B44** | |
| Cut line: render modes shrink to a sentence; the stripes build merges with the reading | `CUT_LINE` in `narration.py` | The film cuts the tween, cull, two-questions, `OUTPUT_IS_SRGB` and missing-slots beats first; the stripe build and the reading stay separate because B23 teaches the ingredients that B32 and B33 read |

### Left out, with the reason

| Left out | Why |
|---|---|
| Lighting in depth: normals, roughness effects, shadows, global illumination, environment | Out of scope for the series (the brief). The film shows that lighting exists, how to turn it off, and that writing `light()` replaces it |
| Vertex displacement in 3D, `varying`, matrices | Out of scope (the brief); `vertex()` is named and its count shown (B04) |
| `sampler2D` textures in 3D, `NORMAL_MAP` | Not needed for the pad; the textures film covers reading textures |
| The other spatial outputs and render modes (subsurface, rim, clearcoat, depth modes, the blend family beyond `blend_add` by name) | The docs list them; naming more would not teach the one idea |
| Other shader types (`particles`, `sky`, `fog`) | The film says canvas item and spatial and does not claim there are only two |
| Per-instance uniforms | A real feature (the `ShaderMaterial` docs name it) that needs a second material story |
| The Inspector and editor frames | Only B43 shows the editor, as four frames of the Project menu and the Project Settings dialog recorded by script; no Inspector widget is claimed (the slot's property name `material_override` is, because it was run) |
| The full explanation of color spaces | Left to the color film; this film gives the minimum that explains one measured difference (B38 to B41) |

## Corrections to the brief (detail in `FACTCHECK.md`)

1. "There is no `COLOR` here": it exists, read-only (rows for B06).
2. "UV on a quad": the game's pad is a `BoxMesh` of 1.55 by 0.10 by 1.55, and the game's own pixel test draws the shader on a `QuadMesh`. The stripes differ (6 against 16), which became the payoff beat B36.
3. "The 8-line pad shader": the file is 10 lines (8 statements and the function's two brace lines).
4. "UV.x probes at 0.0625 and 0.1875 for dark and light stripes": both land on the dark side of a stripe edge (a half-pixel offset), so both read dark; the centres 0.03125 (dark) and 0.09375 (light) are used.
5. "Verify in the Lab with an ambient-lit quad and an unshaded one": the Lab's `quad3d` scene has white ambient light at energy 1 and no lamp, which makes lit and unshaded identical; the lamp scene (verify4) is the check.
6. `BIDEA_TEXT` as given in the brief splits its trigger across a line break and would fail the lint; the line break is moved so the trigger sits inside one line.

## Added: in neither the brief nor a source (each run or checked, FACTCHECK.md)

1. The two real compile errors a 2D/3D mix-up produces (B06).
2. A two-D shader on a three-D mesh is silently ignored (B07, verify8).
3. A box lays its map out as 3 by 2 cells, a sphere wraps it once, a square carries the whole map (B08).
4. `material_override` is the three-D slot, and `set_shader_parameter` works through it; the name is case-sensitive; a hint does not clamp (B09, B26, B27).
5. A tween on a never-set uniform fails in 3D too (B28).
6. `light()` runs once per lamp and the results add, in 3D (B04, verify7).
7. An empty `light()` silences the lamp but not the ambient light (B16).
8. A back face is not drawn by default; `cull_disabled` draws it (B17).
9. The same shader draws 6 stripes on the box's top and 16 on a flat square (B36).
10. Forward+ draws an unshaded albedo of one half as 0.74, Compatibility as 0.50, and a two-D `COLOR` of one half as 0.50 in all three renderers (B39).
11. The two renderers' midpoints for the pad's colors match the linear-light and as-written arithmetic to within half an 8-bit step (B41, linear-mix-check).
12. `OUTPUT_IS_SRGB` is true in Compatibility and false in Forward+ and Mobile, in the docs and in a run (B42).
13. Compatibility's endpoints read up to four 8-bit steps off the typed numbers in the low channels (a FACTCHECK note; not said in the film).
14. Mobile reads like Forward+ for the pad (within one 8-bit step); not shown.
15. Alpha 0 reads the stage color and alpha 1 the solid color; 0.5 sits halfway (B05 and B12 captions, verify11).
16. A lamp that does not reach a surface does not run `light()` for it (the `light()` tag in B16, verify12).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Same Shape, New Names | the teal flat square and the four terracotta corner dots; the skeleton code card; the teal color (0.37, 0.64, 0.57); the three meshes |
| II Lit or Unlit | the teal sphere(s) and the one turning lamp; the flat square that turns around |
| III A Surface That Changes | the flat square with its ramp strip; the stripes; the rust-to-green square with its dial |
| IV Read a Real One | the ten-line pad shader and the pad (a flat square, then the thin box) |
| V Which Renderer? | the pad in two panes, the two grey swatches, the red channel's number line |

## Opening correction and terms

- **BIDEA**: the writer types "3D shaders are a different, harder thing." and replaces "a different, harder thing" with "the same shape, new names".
- **BDEFS** (prerequisites only): Mesh, Material, Albedo, Lighting, Renderer. The card uses the GLOSSARY's exact words where the term has a row (mesh, material, renderer; the lint compares them); albedo and lighting have no row, so they keep the film's own short lines. The terms the film exists to teach (shader, spatial, vertex, fragment, light, alpha, UV, uniform, hint, ramp, fract, step, mix, channel, linear, sRGB) are earned in their acts, each defined on screen where first spoken, in the wording of `../_godot-shaders-series/GLOSSARY.md` (a short caption or label, never a text card).

## Cut line

If the film runs long, cut in this order: the tween beat (B28), the cull beat (B17), the two-questions beat (B18), the `OUTPUT_IS_SRGB` beat (B42) and the missing-slots beat (B35): each repeats an idea another beat carries. The lit sphere (B11), the unshaded pair (B14), the box reveal (B36) and the two-renderer comparison (B37 to B41) stay: they are the film's proof. Current estimate about 10.3 minutes, so no cut is needed.

## Editor-frame reconciliation 2026-10-13

**What changed.** Beat B43 (narration, lane picture, capture spec) was reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, section 11). **Why.** The first plan took the docs' sentence "In the editor, you can always switch between renderers by clicking on the renderer name in the upper-right corner of the editor" as true and showed the docs page (capture D3). The shipped 4.7.2 editor hides that name by default; it appears only after Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector is turned on. A viewer who followed the sentence on a fresh install would find nothing in the corner. Nothing was voiced, rendered or published.

- **B43 narration.** "Its name sits in the upper right corner of the editor, and you can switch it there" became "Open Project Settings, then Rendering, Renderer. Rendering Method shows it, and changing it there needs Save and Restart." The second sentence ("Switching can change how a scene looks, so test again afterwards.") is unchanged and now also rests on this film's own measurements (rows 86 and 88).
- **B43 picture.** The docs screenshot D3 is dropped (the beat does not carry a "the docs say X, the editor shows Y" comparison; the title-bar frames stay unused in the series folder). The lane is now an editor lane: four real frames of the editor (the Project menu; Project Settings on Rendering, Renderer; the Rendering Method menu; the restart note), cross-dissolved, with the ring moving step by step, labelled "scripted editor session".
- **FACTCHECK.** Row 97 is CORRECTED (docs versus run); row 104 is new (the Project Settings path, PASS from the frames); row 98 gained this film's own runs as evidence. No row is OPEN.

Beat ids, beat count (44 body), lane types of every other beat, and acts are unchanged. The line grew from 32 to 33 spoken words; `lint_series.py` counts 1,814 words and 10.3 minutes, no errors, no warnings.

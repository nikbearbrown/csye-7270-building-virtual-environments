# Acts and coverage map: Textures and Color

**What this is.** How this film is built from its brief and its third-party source: which idea lands in which act, which ideas move to other films of the shader group, and which are left out, each with a reason. Also the cast per act, the opening correction, the terms card, what the film adds that is in no source, and the cut line.
**Why.** Bear split a seven-hour course into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 41 body beats, about 10.9 minutes. The source's two texture chapters and its color material feed Acts I to III; the source never mentions color spaces, so Acts IV and V are added and are the film's reason to exist. Every number in Acts IV and V was measured in Godot 4.7.2 on three renderers (Forward+, Mobile, Compatibility), in 2D and in 3D, with and without HDR 2D; the statements about the docs are quoted from the docs; the three Inspector or editor labels that were open are closed from real editor frames recorded by script on 2026-10-13, which corrected two of the first plan's wordings (see the reconciliation note at the end). Five source or brief claims were checked, two of them corrected (the last five rows of FACTCHECK.md).

## The source (third-party; nothing copied)

- **A seven-hour course on 2D shaders in Godot** (a YouTube cut of a paid course; creator not named in the text Bear pasted). I was given Bear's own description of its texture and color chapters, in `../_godot-shaders-series/briefs/textures-and-color.md`, not the transcript. The brief's description is the only form of the source used here. Chapter times are not known to me.

## Coverage

| Source item (from the brief) | Where it goes | Note |
|---|---|---|
| A `Texture2D` node with a `sampler2D`, `UV` by default (node editor) | **Act I**, B02 to B04 | Taught as code: `texture(tex, UV)` on a `uniform sampler2D`. The visual-node editor itself is **LEFT OUT**: these films teach code shaders, which is what the docs and AI assistants produce |
| The rule that an assigned texture is scaled to the original texture's UV (aspect ratio matters; squares are easiest) | **Act I**, B04 | Said as "it stretches across the shape, because the address always runs from zero to one" and measured (a square texture fills a 16:9 shape as 80 by 45 pixel cells). Fixing the stretch is **MOVED** to *UV Space* |
| Gradient and noise textures made in the Inspector | **Act III**, B18 (noise, editor frame) and B22 (the gradient as a color ramp) | Real editor frames |
| `one minus` to invert | **Act II**, B11 and B12 | B12 adds what happens when alpha is flipped too |
| `step` on noise for dots | **Act III**, B19 (the cut) | Dots are **MOVED** to *Patterns and Pixelation*; here `step` makes the dissolve |
| `mix` with the original color | **Act II**, B16 | Mixing the picture with its own gray, so it ties to the gray beats |
| float to vec3 gives gray (the value is copied to all three) | **Act II**, B14 | In code: `vec3(gray)` |
| vec4 to vec3 drops alpha | **Act II**, B10 | In code: `.rgb`, alpha left alone |
| vec2 to vec3 pads blue with zero | **LEFT OUT** | Node-editor conversion rule; constructors belong to *Godot Shader Language* |
| Grayscale by taking the red, green or blue channel (the source admits it favors a channel) | **Act II**, B14 and B15 | **Widened**: the crude version is shown, then the weighted one, with the weights derived from the BT.709 primaries |
| Time-based exercise: fade blue in with `clamp` or `min` of time | **LEFT OUT** | Time belongs to *Time and Waves*; the dissolve's `progress` is a uniform the game drives, with its tween trap (B26) |
| A `sampler2D` noise uniform needs `repeat_enable` and a seamless `NoiseTexture2D` to scroll (shield chapter) | **MOVED** to *Soft Edges, Glow and Noise* | `repeat_enable` itself is shown in B07 |
| Noise `step` plus gradient color ramp for an edge | **Act III**, B19 to B23 | The brief's payoff: a dissolve that burns away with a colored edge |
| The source never mentions sRGB against linear | **Acts IV and V** (added) | Measured, sourced, and explained in one picture (B29, B30) |
| Optional: hue | **LEFT OUT** | HSV hue cycling is in *Patterns and Pixelation* |

## Corrections and checks of the source and of Bear's chapter notes (full detail in FACTCHECK.md)

- Grayscale by one channel is a simplification: kept as the crude version and then replaced by the weighted one.
- Bear's chapter note, from reading the 4.7.2 source: Compatibility does no sRGB-to-linear conversion on 2D uniforms, and Forward+ and Mobile convert a `source_color` uniform in 2D only when HDR 2D is on. **Tested and confirmed for 2D.** The brief also asked for 3D separately: in 3D, Forward+ and Mobile convert and Compatibility did not, for an unshaded surface. Lit 3D surfaces were not tested and the film does not claim anything about them.
- The docs already say it: "Using `source_color` hint is required in the Forward+ and Mobile renderers, and in canvas_item shaders when HDR 2D is enabled. The source_color hint is optional for the Compatibility renderer, and for canvas_item shaders if HDR 2D is disabled." The measured matrix agrees with that sentence in every cell.

## Added: in no source (each is checked, FACTCHECK.md)

1. The measured matrix: one blend, three renderers, 2D and 3D, hinted and not, HDR 2D on and off (B27 to B32, B35).
2. A test without a window has no pixels to read (B28).
3. A hint on a mask moves a one-half threshold to about three quarters of the way across (B38).
4. A color passed from code is converted twice if you convert it first (B36).
5. `COLOR` starts as the lookup times the node's modulate, and a plain lookup throws the modulate away (B09).
6. Ordinary 2D drawing cuts every number off at one; HDR 2D keeps numbers past one (B13, B32).
7. The first version of the dissolve failed at progress zero (160 pixels already burning), and the tween needs a start value (B25, B26).
8. A gradient in place of the noise turns the same shader into a wipe (B24).
9. The defaults of a `sampler2D` on a canvas item: linear filter, repeat off (B05, B07).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Reading a Texture | the six-by-six F table (cream letter F on teal) in B02 and B05 to B07, with the checker, the gradient and the noise as the other tables in B03 and B04; a square window |
| II Color Is Math | the four-patch picture (rose, leaf, sky, sand) on the test sprite; the orange swatch with four bars in B08; the teal test sprite for the alpha beat |
| III Noise as a Mask | the noise clouds as a teal Color Rect (B17, B19); the teal test sprite (B20 to B26); the burn ramp; the threshold marker on a number line |
| IV Two Ways to Count Light | the gray strip from 0.2 to 0.8 in two renderers; the sRGB curve with its dashed diagonal |
| V Hint Colors, Not Masks | the three steel-blue patches; the four-patch picture again; the gray ramp strip; the dissolve sprite |

## Opening correction and terms

- **BIDEA**: the writer types "A texture is a picture pasted onto a shape." and replaces "pasted onto a shape" with "looked up by address" (the trigger sits wholly on the second line; the brief's draft split it across a line break, which the correction could not match: reported in the final message).
- **BDEFS** (prerequisites only): Shader, UV, Texture, Channel, Alpha, Renderer. The terms this film exists to teach are earned in their acts, each defined on screen where first spoken: fragment, uniform, sampler2D, built-in, COLOR, vec4, swizzle, mask, step, discard, ramp, tween (Acts I to III); sRGB, linear, probe, HDR 2D (Act IV); hint, source_color (Act V). Wording follows `../_godot-shaders-series/GLOSSARY.md` where it has the term; sRGB, linear, filter, repeat, probe, HDR 2D, tween and modulate are not in it (reported).

## Cut line

If the film runs long, cut in this order: the tween beat (B26), the brighten beat (B13), the alpha-hole beat (B12), the gray pair (B14 and B15), then the from-code beat (B36). Each extends an idea another beat already carries. The dissolve build (B19 to B25), the two-renderer reveal (B27 to B31) and the hint rules (B33 to B39) stay: they are the film. Current estimate about 10.9 minutes, so no cut is needed; removing the five cuts would save about 1.2 minutes (72 seconds by the same estimate).

## Editor-frame reconciliation 2026-10-13

**What changed.** Beats B18 and B40 (narration, lane picture, capture spec) and the picture and spec of B34 were reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, sections 2.7, 2.8 and 11). **Why.** The first plan took its wordings from the docs and from convention; the frames show otherwise. Nothing was voiced, rendered or published.

- **B18.** The Inspector's resource menu is a heading **New** over bare class names (no entry starts with the word New), so "a New Noise Texture two D ... a New Fast Noise Lite" became "choose Noise Texture two D under New. Click it, then open its Noise slot ... choose Fast Noise Lite". The picture is five frames over two Inspector views: the NoiseTexture2D view (Width, Height, Noise, Seamless; no preview) and the FastNoiseLite view (the grey clouds preview, Seed). FACTCHECK row 52 is CORRECTED.
- **B34.** Confirmed, narration unchanged: **Picked** is a color swatch that opens a picker, **Typed** is four boxes x y z w. The lane now names the crop and measured ring boxes. Row 94 is PASS.
- **B40.** The docs say the renderer's name always sits in the editor's upper right corner; the shipped 4.7.2 editor hides it by default (it needs Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector). The beat now gives the path every student can follow: Project Settings, Rendering, Renderer, Rendering Method (forward_plus, mobile, gl_compatibility), then Save & Restart, over the Project Settings frames. Row 106 (the docs sentence) is CORRECTED, docs versus run; row 107 is PASS.

Beat ids, beat count (41 body), lane types and acts are unchanged. The two lines grew by 18 spoken words in all (B18 38 to 46, B40 35 to 45); `lint_series.py` now counts 1,918 words and 10.9 minutes. No fact-check row is OPEN.

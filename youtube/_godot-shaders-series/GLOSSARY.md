# Glossary: the locked vocabulary of the Godot shader films

**What this is.** One agreed definition, one spoken form and one "never say" list for every term the shader films use.
**Why.** Terminology is the hard part of shaders and the part Bear asked for first. If two films define "fragment" or "uniform" differently, a viewer who watches both learns less than one who watches either. Every film takes its on-screen wording from here.
**Found.** The vocabulary is small (about 30 terms). The hardest pair, "pixel" and "fragment", has a clear, sourced answer (below). Several terms in the source material were used loosely; the corrected wording is what is locked here.

Facts below are checked against the Godot 4.7 documentation (docs.godotengine.org/en/stable, read 2026-10-13) and, where marked *run*, against the installed Godot 4.7.2 on Bear's Mac (see `lab/` and each film's `evidence/planning-checks/`).

## How to use this file

- **On screen**, use the *Definition* column word for word (it is short on purpose: it fits a terms card, 72 characters or fewer where marked ◆).
- **In narration**, say the idea in your own Teardown sentence, but never contradict the definition and never use a "Never say" word.
- **The first time a term is spoken in a film**, its definition is on screen in that beat (a label, a caption, or a card). A term that a film exists to teach is *earned* in an act; a term the film merely needs is a *prerequisite* and goes in the terms card (BDEFS, three to six terms, each 17 characters or fewer).
- Code identifiers are always shown exactly as Godot spells them (`fragment()`, `hint_range`, `UV`). Narration uses the spoken forms in the last table, because the voice reads them better.

## The terms

| Term | Definition (on screen) | Notes and checked facts |
|---|---|---|
| **shader** | ◆ a small program the graphics card runs to decide how something is drawn | Godot docs: "Shaders are a special kind of program that runs on Graphics Processing Units (GPUs)." |
| **GPU** | ◆ the graphics chip: many small workers running at once | Do not give core counts (they date). |
| **CPU** | ◆ the main chip: a few fast workers doing one job after another | GDScript runs here. |
| **pixel** | ◆ one dot of the picture on screen | |
| **vertex** (plural **vertices**) | ◆ a corner point of a shape | A plain rectangle has four. *Run:* a Sprite2D rectangle moved only by its four corners; the GPU filled in the rest. |
| **fragment** | a pixel-to-be: the thing `fragment()` colors before it becomes a pixel | See "Pixel or fragment?" below. |
| **mesh** | the set of vertices and triangles that make a shape | 3D meshes and 2D rectangles alike. A `MeshInstance2D` draws a mesh; a `QuadMesh` has (cuts + 2) by (cuts + 2) vertices; a `BoxMesh` has 24 vertices, not 8, so `vertex()` runs 24 times for a box (*run*). |
| **texture** | ◆ an image a shader can read by address | |
| **material** | the resource that tells Godot how to draw a surface; it holds the shader | |
| **ShaderMaterial** | a material that holds your shader and its settings | In the editor (real labels, 4.7.2): the node's Material slot menu has a heading **New** then **ShaderMaterial**; click the new material, and in its Shader slot choose **New Shader...**; the Create Shader dialog starts on Mode Spatial, so pick Canvas Item for 2D (editor-capture README 2.1). |
| **shader type** | the first line; says what the shader is for | `canvas_item` 2D and UI; `spatial` 3D; `particles`, `sky`, `fog`. (Docs also list a sixth, `texture_blit`; do not teach it.) |
| **processor function** | a function the engine calls for you: `vertex()`, `fragment()`, `light()` | Docs: seven exist in total (`vertex`, `fragment`, `light`, `start`, `process`, `sky`, `fog`); which exist depends on the shader type. |
| **`vertex()`** | runs once for each vertex; places the corners | Docs: "runs over all the vertices in the mesh and sets their positions". |
| **`fragment()`** | runs once for each pixel the shape covers; sets its color | Docs: "runs for every pixel covered by the mesh". Docs also say "once or more for each pixel it has to draw": exact for one flat shape, loose where shapes overlap. |
| **`light()`** | runs once per pixel for each light that touches it; replaces the default lighting | Docs 4.7: "In Godot 4.x all lighting is done during the regular draw pass." If you write `light()` it replaces the built-in lighting even when empty. *Run:* an empty `light()` leaves only the ambient look (black only if the ambient is black); `LIGHT_DIRECTION` is a unit arrow from the pixel toward the lamp; three lines rebuild the default exactly (not with a normal map). It runs only inside the lamp's texture square. |
| **built-in** | ◆ a value the engine hands to a function, or collects from it | Written in capital letters: `UV`, `COLOR`, `TIME`. Which ones exist depends on the function. The docs also say "built-in shader functions" (`step`, `mix`, ...): films call those "functions" to avoid the clash. |
| **uniform** | ◆ a value your game sets from outside; every pixel sees the same one | Docs: "Uniforms can't be written from within the shader." Set in the Inspector or with `set_shader_parameter()`; the name must match exactly. *Run:* a misspelled name is a silent no-op (Bear's chapter 6). |
| **hint** | the word after a colon that tells Godot how to treat a uniform | `hint_range(0.0, 1.0)` and `source_color` tell Godot how a uniform is meant to be used and how the editor lets you change it (real frames, `editor-capture/README.md` 2.3: a `hint_range` float is a number box with a slider bar, one widget; a `source_color` vec4 is a color swatch that opens a picker; `hint_enum` is the one the docs call a dropdown); `repeat_enable`/`repeat_disable` and `filter_*` on a `sampler2D` change how the texture is sampled, not how the editor shows it (docs: hints serve the compiler and the editor). A range hint shapes the editor; it does not clamp a value set from code (Bear's chapter 6, run on 4.7.2). Short form for a label (60 characters): "a word after the colon: how Godot treats a uniform". |
| **varying** | a value set at each corner, blended across the shape for `fragment()` to read | Docs: set per vertex in `vertex()`, interpolated per pixel in `fragment()`. Flows one way only, vertex to fragment. A varying written in `fragment()` and read in `vertex()` passes Godot's parser and then fails when the shader is built (*run*); do not teach it. |
| **`UV`** | ◆ a point's address on the shape: 0 to 1 across, 0 to 1 down | In `canvas_item`, 0,0 is the top left and Y points down (*run:* top ≈ 0.04, bottom ≈ 0.96). In `spatial`, `UV` follows the mesh's own UV map. A `Polygon2D` has `UV` only when it has a texture; without one `UV` is zero everywhere (*run*). |
| **`TIME`** | ◆ seconds on one clock shared by the whole game | Docs: "Global time since the engine has started, in seconds"; repeats every 3,600 s (rollover setting). *Run:* a node added three seconds in reads the same `TIME` as one present from the start (12 quarter-seconds lit on both). NOT time since this node appeared. Setting `rendering/limits/time/time_rollover_secs` (default 3600) is the wrap; only pulses with a whole number of cycles in the limit survive the wrap (*run*). Time scale changes `TIME`'s rate (0.5 gives 0.50); pausing the tree does not stop it; `Time.get_ticks_msec()` has its own zero and ignores the time scale (*run*). `TIME` advances only on **drawn** frames: a hidden, minimized or covered window freezes it, so a real-time capture keeps the window on top (`DisplayServer.window_set_flag(WINDOW_FLAG_ALWAYS_ON_TOP, true)`); Movie Maker runs are offline and unaffected. |
| **`COLOR`** | the color of the pixel being drawn; `fragment()` sets it | In `canvas_item` it is the output color. In `spatial`, `COLOR` in `fragment()` is a read-only input, the vertex color (white when the mesh has none; writing it fails with "Constants cannot be modified"), and the output is `ALBEDO` (*run*). In `vertex()`, `COLOR` is the vertex color times `modulate` and `self_modulate`, and it travels on to `fragment()` (*run*). |
| **`SCREEN_UV`** | a pixel's address on the whole screen, not on its own shape | |
| **vector** | ◆ a bundle of two to four numbers | `vec2`, `vec3`, `vec4`. Colors are `vec4`: red, green, blue, alpha. |
| **swizzle** | picking or reordering a vector's parts: `c.rgb`, `p.yx` | Docs: `xyzw`, `rgba`, `stpq` are equivalent; do not mix sets in one swizzle. |
| **sampler2D** | the type of a texture a shader reads | |
| **ramp** | a smooth run of values from 0 up to 1 | Series word, defined in the math film; other films may use it with a half-sentence gloss. |
| **mask** | a number from 0 to 1 per pixel saying how much of something to show | Series word. Every film that uses it defines it in one short phrase on first use (a film cannot assume another was seen); the Math Toolkit film (B16) is the fullest treatment. |

## Small words the math films define (wording checked in the docs and the Lab)

These are not shader jargon but a film that uses one must put its meaning on screen the first time (a cue `label` on the code line, or a Manim label). The wording below is what the Patterns and Lines films verified.

| Word | On-screen wording | Checked facts |
|---|---|---|
| **`floor(x)`** | rounds down to the whole number below | Docs: "Rounds to the integer below." *Run:* floor(2.9) is 2, floor(0.7) is 0. |
| **`fract(x)`** | the part after the point: x minus floor(x) | Docs: "Returns the fractional part of x. This is calculated as x - floor(x)." *Run:* fract(2.9) is 0.9; fract(-0.25) is 0.75 (it never goes negative). |
| **`mod(x, y)`** | the remainder after dividing x by y | Docs: "Modulo (division remainder)", "computed as x - y * floor(x/y)". *Run:* mod(3, 2) is 1, mod(-1, 2) is 1. The `%` operator is for whole numbers only: on decimals it is a shader error. |
| **`mix(a, b, t)`** | blends from a to b: t of 0 gives a, 1 gives b | Docs: "Linear interpolate between a and b by c." |
| **`step(edge, x)`** | 0 below the edge, 1 from the edge up | Docs: `step(a, b)` is "b < a ? 0.0 : 1.0". The edge comes first. |
| **`length(v)`** | the length of a vector; of an offset, the distance | Docs: "Vector length." |
| **`TEXTURE`** | the node's own picture; `texture(TEXTURE, uv)` reads it | Docs, `texture()`: "Performs a texture read." `COLOR` already holds the picture's color when `fragment()` starts. |
| **slope** | how steeply a line rises: up divided by across | |
| **radians** | Godot's angle unit; a full turn is tau, about 6.283 | `radians()` converts degrees. Passing degrees where radians are expected is silent and wrong (*run:* `tan(30.0)` without `radians()` reads -6.4). |
| **normal** | a direction at right angles to a line or surface | |
| **`dot(a, b)`** | multiply the matching parts and add them; with a unit direction, how far a point lies along it | |
| **offset** | an amount added to slide something | In the Lines film a distance (slides a line straight across); in the Time and Waves film where in its cycle a wave starts, counted in cycles. A film that uses it says which. |
| **alpha** | how visible a pixel is: 0 invisible, 1 solid | The fourth part of a color. |
| **band** | the strip of pixels near a line or an edge, as wide as the thickness or the softness | Series word. Short forms: near a line, "the strip of pixels near a line, as wide as the thickness"; near an edge, "...as wide as the softness". |
| **tween** | Godot's way to change a value smoothly over time from GDScript | A tween on `shader_parameter/name` fails if that uniform was never set first (*run*). |
| **cycle** | one full swing of a wave or repeat | `cycles = TIME * speed`. |
| **amplitude** | how far a wave swings from its middle | |
| **speed** (of a wave) | how quickly it repeats: cycles per second | Multiplies `TIME`; frequency multiplies position (Time and Waves film). |
| **frequency** | how many cycles fit across a shape | |
| **sawtooth** | a wave that climbs and snaps back to the start | `fract` of a ramp. |
| **time scale** | how fast the game's clock runs; 1 is normal | |
| **delta** / **age** | seconds since the last frame (docs) / seconds since this node appeared, counted by adding delta | An age from `Time.get_ticks_msec()` minus a start is wrong once the time scale changes (*run*). |
| **instance uniform** | a uniform with its own value on each node that shares the material | The standard fix for per-node timing offsets. Also what separates units that share a material: two units from one scene share a material, so a plain uniform changes both (960 px on both); an instance uniform separates them (960 and 312) (*run*). |
| **ambient light** | the dim base tint of the scene; it stays whether or not a lamp reaches a pixel | In 2D it is what a Canvas Modulate sets. A 2D scene starts fully lit, so lights only show against a dimmed scene. |
| **Canvas Modulate** | a node that tints everything drawn on the canvas | |
| **point light** / **directional light** | a light that shines out from one spot, like a lamp / a light that shines the same way everywhere, like the sun | A directional light's `LIGHT_POSITION` is always zero (docs). |
| **normal map** | an image that says which way each pixel faces | The default lighting reads it; a rebuilt `light()` ignores it unless you add the docs' extra term (*run*). |
| **screen space** | pixels of the window, counted from the top left, with y growing downward | `LIGHT_POSITION`, `LIGHT_VERTEX` and `FRAGCOORD` are in physical pixels: they ignore camera zoom, and they change with the capture size (*run*). |
| **`LIGHT_COLOR`**, **`LIGHT_ENERGY`** | the lamp's color and its strength | |
| **`LIGHT_DIRECTION`** | a unit arrow from this pixel toward the lamp | Docs word it loosely ("Direction of the Light2D in screen space"); measured, it is a unit 3-vector toward the lamp. Same for every pixel under a directional light. |
| **`LIGHT_POSITION`**, **`LIGHT_VERTEX`** | where the lamp is, and where this pixel is, in screen space | Their difference is an arrow from the lamp to the pixel; `length` of it is the distance in pixels. |
| **`unshaded`** | a render mode: nothing lights the surface, so the result is just the base color | In 2D the sprite ignores every light and the ambient tint; in 3D the result is just `ALBEDO`. Right for a lamp's own bulb or a flat graphic look; the docs add that it is faster to render. |
| **`smoothstep(a, b, x)`** | a switch that eases in and out between two edges: 0 below a, 1 above b, a smooth S between | Docs: t*t*(3-2t); results undefined if a >= b. *Run:* `smoothstep(0, 10, 1)` is 0.028, not the 0.1 a straight line would give. Short form for a label (60 characters): "eases from 0 to 1 between two edges". |
| **`max(a, b)`** | the larger of two values | Joining two masks with it lights a pixel if either is lit. |
| **aspect ratio** | width divided by height | 16 by 9 is about 1.78; a square is 1. The address runs 0 to 1 on both sides whatever the ratio, which is why a circle drawn from it is an oval on a wide shape. |
| **absolute value** (`abs`) | drops the minus sign: -0.3 becomes 0.3 | Folds a ramp at zero (the Math Toolkit film). |
| **matrix** | a grid of numbers in rows and columns | `mat2`, `mat3`, `mat4`. Godot reads the grid by **columns**, not rows: `mat2(vec2(1,2), vec2(3,4)) * vec2(5,6)` is (23, 34); reading rows, or writing the point on the left, gives (17, 39) with no error (*run*). Multiplying a point by it moves the point: a matrix is a saved move. |
| **identity matrix** | the matrix that changes nothing | |
| **origin** | where the numbers are zero; the middle of a centered sprite | For a sprite with `centered` off, the origin is its top left corner (*run*). |
| **pivot** | the point a shape turns around | |
| **sine** / **cosine** / **tangent** | for an angle in a right triangle: opposite over hypotenuse / adjacent over hypotenuse / opposite over adjacent | On the unit circle, cosine and sine are the point at that angle. Memory trick: S O H, C A H, T O A. In the wave films, **sine** is also said as "a function that swings smoothly between -1 and 1 as its input grows" (the card wording in Time and Waves); both senses are the same function. |
| **`PI`, `TAU`, `E`** | pi (half a turn), tau (a full turn, two pi), e | Documented only in each shader type page's Global built-ins table, not in the shading-language page. Spoken lowercase: pi, tau, e. |
| **type** | the kind of value something holds: whole number, decimal, bundle | `float` (a decimal number), `int` (a whole number), `bool` (true or false), `vec2`...`vec4`, `sampler2D`. Godot will not quietly turn an int into a float: `vec3(4, 5, 6) + 2` is an error even though the docs' operator table writes it (*run*, 4.7.2); built-in calls and constructors do accept an int. |
| **function** / **argument** | a named block of code you can call / a value you hand it | |
| **signature** | the first line of a function: the type it hands back, its name, and its arguments, each with a type | |
| **const** | a value that never changes | |
| **`discard`** | throws a pixel away | The docs say it has a cost; the Shader Language film measured nothing. |
| **renderer** | the part of Godot that draws | **Forward+** (default on desktop), **Mobile**, **Compatibility** (widest hardware, default on web). The same shader can read different pixels in different renderers (*run*). Real editor path, 4.7.2: a project's renderer is set in Project > Project Settings > Rendering > Renderer > **Rendering Method** (the dropdown reads `forward_plus`, `mobile`, `gl_compatibility`), then **Save & Restart**; a new project picks it in the **Create New Project** dialog. The renderer name in the editor's upper right corner is **hidden by default** (the docs say it is always there); it appears only after Editor > Editor Settings > Interface > Editor > Appearance > **Show Renderer Selector** is on (an advanced setting; searching "renderer" finds it), and choosing another renderer there still asks to Save & Restart. Compatibility does not support HDR 2D (docs, renderers page). See `editor-capture/README.md` section 11. |
| **channel** | one of red, green, blue or alpha | |
| **sRGB** / **linear** | the scale a color picker's numbers use, spaced for the eye / the scale light adds up on, in a straight line | They agree at 0 and 1 and disagree between: a 0.2 to 0.8 blend reads 0.60 in linear light and 0.50 on typed numbers (*run*, unshaded 3D quad in Forward+ and Mobile against Compatibility). |
| **HDR 2D** | a project setting: 2D is drawn in light and numbers past one are kept | A project setting (and a SubViewport option). Glow in 2D needs four things: a shader that sends a number above one; HDR 2D on; a WorldEnvironment with glow on and its background mode set to **Canvas**; and a dark surround (*run*, Soft Edges film: without Canvas nothing happens). The renderers page says Compatibility does not support HDR 2D, yet on 4.7.2 here a Compatibility SubViewport with `use_hdr_2d` held values above one and drew a halo: a film says what it measured. |
| **`source_color`** | a hint on a color uniform or texture: the numbers are sRGB, convert them to light first | Required in Forward+ and Mobile, and in `canvas_item` shaders when HDR 2D is on; optional in Compatibility and when HDR 2D is off (docs, matched cell by cell by the Textures film's runs). Never hint a mask: hinting one moves a 0.5 threshold to about 0.74 (*run*). Passing an already converted color from code converts twice. Short form for a label: "numbers are sRGB: convert to light first". |
| **local / world / screen space** | the same point as three sets of numbers: counted from its own node / from the world's origin / from the window's top left | One corner of a 128 px sprite at (600, 400) with the camera at (890, 460): local (-64, -64), world (536, 336), screen (286, 236); a camera pan changes only the screen number (*run*). The Inspector shows parent-relative positions. |
| **`MODEL_MATRIX`** | local to world: multiplies a corner from the node's own numbers to the world's | Order matters: `CANVAS_MATRIX * MODEL_MATRIX * corner` (right to left); the swapped order lands the corner somewhere else (*run*). A w of 1 is a place, a w of 0 is a direction. |
| **`CANVAS_MATRIX`** | world to screen (Godot calls the screen side canvas space) | |
| **`FRAGCOORD`** | the pixel's position in window pixels | The docs give the bottom right as (1.0, 1.0); the engine counts pixels: the last pixel of a 1280 by 720 window reads (1279.5, 719.5) (*run*). |
| **screen texture** | a copy of the screen made at one moment, which a shader can read | Read with `hint_screen_texture` and `SCREEN_UV`. The old name `SCREEN_TEXTURE` was removed in Godot 4. One copy is made per canvas layer: a reader on the same layer reuses it, a reader on a higher layer gets a fresh one (*run*). |
| **draw order** | what is drawn first; later things cover earlier ones | In 2D it is the scene tree (top of the Scene dock first), then z index and canvas layers. |
| **`BackBufferCopy`** | a node that makes the screen copy at its own place in the draw order | Copy Mode: **Viewport** (whole screen), **Rect** (a box), **Disabled**. A new one starts in Rect mode; outside its box the result is undefined (docs) and read black in a fresh process (*run*). The box ignores the node's position, scale and rotation and counts render pixels. |
| **label map** | a layer of flat colors, each color a label | Series word of the Reflections film (it avoids "mask", which means a 0-to-1 number per pixel). |
| **albedo** (`ALBEDO`) | the base color of a 3D surface | The `spatial` output: three numbers (alpha is a separate output). Lighting turns it, and every lamp, into the pixel you see. |
| **lighting** | how lights change a surface's color | In 3D it is on by default; `unshaded` turns it off, and an empty `light()` makes a lamp stop working (*run*). |
| **`render_mode`** | an optional second line after the type that picks options | Examples: `unshaded`, `cull_disabled`, `blend_add`. |
| **`cull_disabled`** | a render mode: draw both sides of a surface | By default only the front face is drawn, so a flat square turned around vanishes (*run*). |
| **`material_override`** | the 3D node slot that holds the ShaderMaterial | The node holds the material; the material holds the shader. |
| **opaque** | fully visible: nothing shows through |  |
| **neighbor** | the pixel right next to this one | One step in texture units is `TEXTURE_PIXEL_SIZE`. |
| **padding** | empty space added around an image | A shader paints only inside its own rectangle: a sprite trimmed to its shape gets an outline width of 0 at the extremes (*run*). |
| **modulate** | a node's tint color; it multiplies the drawing | A shader that assigns `COLOR` from the texture throws the modulate away; passing the vertex `COLOR` through a varying restores it (*run*). |
| **`min(a, b)`** / **`clamp(x, a, b)`** | the smaller of two values / pins x inside a range | `clamp` is `max` first, then `min`. |
| **viewport** / **SubViewport** | a rectangle the engine draws into; a SubViewport is a separate one inside the scene | Its picture can be used as a texture. A transparent SubViewport stores a half-transparent pixel premultiplied (teal at alpha 0.5 is (0.184, 0.318, 0.282, 0.498)); the default Mix blend then shows it too dark unless the sprite uses Premultiplied Alpha (*run*; the docs are silent). |
| **ViewportTexture** | a texture that shows what a viewport drew | In the Inspector's Texture slot: the menu has a heading **New** then **ViewportTexture** (the docs word it "New ViewportTexture"). |
| **ColorRect** | a control that displays a solid color rectangle | Docs wording. The usual test surface for a canvas item shader that needs no texture; `TEXTURE_PIXEL_SIZE` is (1, 1) on it (*run*). |
| **polygon** | a shape made of straight edges between points | Series word (the Vertex film). |
| **interpolate** | blend smoothly between two known values | What the card does to a varying across a shape. |

Also: "Forward+" is said "Forward Plus", `OUTPUT_IS_SRGB` "output is s R G B", `FRAGCOORD` "frag coord", `SCREEN_PIXEL_SIZE` "screen pixel size", `CANVAS_MATRIX` "canvas matrix", `MODEL_MATRIX` "model matrix".

A lone "U" or "V" read aloud sounds like "you" and "vee": narration says "U V" together, or "the horizontal address" / "the first number" when it means one part (the UV Space film does the latter). Node names with a digit (`Sprite2D`) trip the digit warning: write "a sprite" or spell it out ("sprite two D") in the prompt, and the on-screen prompt shows the same words.

Built-ins written in capitals on screen are said as lowercase words in narration: `VERTEX` "vertex", `COLOR` "color", `TIME` "time", `ALBEDO` "albedo", `TEXTURE` "texture" (an all-caps word in narration risks being spelled out; the series lint errors on it). The exceptions are the letter-names `UV` "U V" and `SCREEN_UV` "screen U V".

Spoken forms: `floor` "floor", `fract` "fract" (rhymes with "tract"; listen for it when voiced and report it if the voice stumbles), `mod` "mod", `mix` "mix", `step` "step", `length` "length", `TEXTURE` "texture", `dot` "dot", `radians` "radians".

## Series conventions (decided so the films agree)

- **Y points down.** Godot's `UV` and screen positions count y downward, so a growing angle turns **clockwise** on screen (the Trigonometry, Matrices and Vertex films all say so). A film that wants the school-maths picture (y up, positive angles counter-clockwise) must say so aloud and flip y in one named line, as the Lines film does (`p.y = -p.y`: "Godot counts the address downward, so flip the second number"). A film never flips silently.
- **A pixel value is only quoted with its renderer.** Forward+ and Compatibility can give different pixels for the same shader. Flat colors agree in default 2D, and when hinted; blends, gradients and unhinted colors can differ a lot (a 0.2 to 0.8 blend reads 0.60 in Forward+ and Mobile and 0.50 in Compatibility on an unshaded 3D quad); a smooth warm/cool map in the Lines film differed by one level of 255. "On this Mac" goes with any measured GPU figure (for example `tan(radians(90.0))` reads about -22.9 million here).
- **Shaders that read physical pixels are captured at the size they are shown.** `FRAGCOORD`, `LIGHT_POSITION`, `LIGHT_VERTEX`, a mip level of the screen texture (`textureLod`: a level-4 blur came out at less than half strength on the 4K route, 0.017 against 0.037) and `SCREEN_PIXEL_SIZE` used as an offset count window pixels (`SCREEN_PIXEL_SIZE` used only as a ratio is route-invariant), so the 3x SubViewport route changes their numbers (a radius-150 ring came out 140 px, not 420 to 440, in a 1920 by 1080 SubViewport over a 640 by 360 canvas). Capture those at 1920 by 1080 at scale 1.
- **The Lab window clamps to the screen height.** A 3840 by 2160 window request gave 2004 px high on this Mac; the capture route is the SubViewport native-size route (COMPONENT-SPECS), never a large window.

## Pixel or fragment? (the locked answer)

They are the same job with two names. **Direct3D** calls the stage a *pixel shader*; **OpenGL, Vulkan and Godot** call it a *fragment shader*. Godot's function is `fragment()`.

The careful word is **fragment**: a fragment is a candidate for a pixel. It carries more than a color (depth, for example), and it can still be thrown away (`discard`, a failed depth test) or blended with others (transparency, multisampling) before it becomes the pixel you see. So several fragments can contribute to one pixel, and some fragments never become a pixel.

- *Run (Godot 4.7.2):* a shader that executes `discard;` for the right half of a rectangle leaves the background showing there; `fragment()` ran, no pixel was produced.
- Sources: Microsoft Learn, "Pixel Shader Stage" (Direct3D 11): "invokes a pixel shader once for each pixel covered by a primitive"; with multisampling the shader runs per covered pixel while the depth/stencil test runs per sample; a pixel shader can output no color "if the pixel is discarded". Khronos OpenGL community threads and the OpenGL specification define a fragment as a grid square with its assigned color, depth and coordinates, not yet a pixel. Godot 4.7 docs name the function `fragment()` and describe it as running "for every pixel covered by the mesh".
- **Do not repeat** the claim (made in the source course) that fragments can be stretched, non-square shapes while pixels are always squares. That is not why a circle drawn from `UV` looks like an ellipse on a wide rectangle; the real reason is that `UV` runs from 0 to 1 on both axes whatever the shape's proportions (see the UV Space film).

In narration: say "pixel" for the thing on screen, `fragment()` for the function, and use "fragment" for the in-between thing only in the film that explains it.

## Never say

| Don't | Say instead | Why |
|---|---|---|
| "pixel shader" | "fragment shader" or `fragment()` | Except in the one beat that explains the two names. |
| "draw call", "rasterizer", "rasterization", "invocation", "kernel" | "the GPU fills in the shape", "runs once for each" | Jargon the viewer does not need. |
| "the vertex shader changes the pixels" | "`vertex()` moves the corners; the GPU fills in the rest" | *Run:* only the four corners moved; the edge between them was interpolated. |
| "TIME starts when the node appears" or "since the shader was created" | "one clock for the whole game" | See `TIME` above. |
| "GLSL" more than once per film | "close to GLSL ES 3.0" once, if at all | Docs: "similar to GLSL ES 3.0". |
| "just", "simply", "easy", "obviously" | (cut) | Teardown register. |
| any core count, speed multiplier or "X times faster" | a measured number from a run, or nothing | Claims must be measured. |
| "the book", "the course", "this chapter", "last time", "next time" | (nothing) | Each film stands alone and is never numbered. |
| "a light shader cannot read UV" | `light()` can read `UV` (docs list `in vec2 UV`; *run*: the four corners read black, red, green, yellow) | The source course's error. |

## Spoken forms (what the narration text should contain for the voice)

Narration text spells numbers as words and spaces the letters of an acronym, because Kokoro reads them better. The screen keeps the real spelling.

| On screen | In narration | | On screen | In narration |
|---|---|---|---|---|
| GPU / CPU | G P U / C P U | | `vec2`, `vec3`, `vec4` | vec two, vec three, vec four |
| UV | U V | | `mat3` | mat three |
| RGB / RGBA | R G B / R G B A | | `sampler2D` | sampler two D |
| sRGB | s R G B | | `fragment()` | fragment |
| HSV / HDR | H S V / H D R | | `vertex()` | vertex |
| GDScript | G D script | | `light()` | light |
| GLSL | G L S L | | `shader_type` | shader type |
| `canvas_item` | canvas item | | `hint_range` | hint range |
| `source_color` | source color | | `set_shader_parameter` | set shader parameter |
| `hint_screen_texture` | hint screen texture | | `SCREEN_UV` | screen U V |
| `TEXTURE_PIXEL_SIZE` | texture pixel size | | `MODEL_MATRIX` | model matrix |
| `ALBEDO` | albedo | | `TIME` | time |
| `smoothstep` | smooth step | | `atan` | arc tangent |
| `sin`, `cos`, `tan` | sine, cosine, tangent | | `pow` | power |
| 4.7.2 | four point seven point two | | 60 fps | sixty frames per second |

`AI` and `Godot` are handled by the voice's pronunciation dictionary; write them normally. **`pi` is case-sensitive in that dictionary: lowercase `pi` is said "pie"; all-caps `PI` is said as the letters P, I (it is the entry for "principal investigator").** So the shader constant `PI` is written lowercase **`pi`** in narration text (the screen shows `PI`). Likewise write `tau` for `TAU` and listen for it when voiced. Do not edit that dictionary; if a word is said wrong when the film is voiced, report it.

More spoken forms: `PI`, `TAU`, `E` → pi, tau, e (the shader constants are documented under each shader type's "Global built-ins" in the shader reference, not in the shading-language page); `atan(y, x)` → "arc tangent"; `radians()` → "radians"; `fract` → "fract"; `mix` → "mix"; `vec2` → "vec two"; `SOH CAH TOA` → "S O H, C A H, T O A".

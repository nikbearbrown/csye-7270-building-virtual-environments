# Prompts and script — claude-liam-walker-survival-shooting-a5-gamedev

## Reconstructed opening prompt (B00)
Illustrative reconstruction written for this film. It is **not** a saved session or a historical transcript.

```text
Please use Walker to convert my game design document about a third-person extraction shooter, where a survivor lives in a subway base and carries a rugged military tablet, into its first shaders: a tablet screen that glows only while the tablet is in hand, and worn paint on the weapon crates, with a specification, tests and in-engine captures.
```

## Your Turn prompt (B27)

```text
Please use Walker on my Godot project. Read my CHANGE-BRIEF and shaders/crate_wear.gdshader. Add a metal mask so the bare-metal scratches write METALLIC, as a new uniform with a hint and a default. Before you change anything, predict which pixels of my crate capture will change, then capture again and compare.
```

No model was run for the film except Kokoro (am_onyx) for the narration.

## Narration script (Kokoro am_onyx, exact text sent to TTS)

**B00 · ASK**

Hola, this is Liam, narrating for Jonathan. The prompt on screen is a reconstruction for this film, not a saved session. It asks Walker to give a subway extraction shooter its first shaders: a tablet screen that glows only in the hand, and weapon crates whose paint has worn through to rust. At source revision two, d, five, five, eight, b, b, a, the answer is two shaders written by hand, two materials, and the tests that pin them.

**B01 · BLUF**

I wrote my first two shaders by hand, and Claude checked every step. The tests prove the wiring; only the captures show the look.

**B02 · RESULT**

The game: a survivor in a subway base, with a rugged tablet. The first shader shows one piece of state: is the tablet in use? Its screen glows only once the tablet reaches the hand. The second shader, with textures, goes on the base's two weapon crates.

**B03 · CODE**

Question one: what does a shader do? This is my whole screen shader, seven lines. The GPU runs fragment, on line five, for every pixel of the screen, all at once; each run has only its own local values and cannot see its neighbours. So the game's state comes in as a uniform, set from GDScript: pad light data, line four. Line six is the colour line from my specification, word for word: mix from black to cold white by that value.

**B04 · RESULT**

My own in-engine captures, with the driver paused and the value set from code. At zero point three nine the screen reads one fifty-one, one sixty-two, one sixty-two, exactly my hand calculation, because the mix happens in linear light. At two point oh it is pure white: hint range limits the slider, not the code.

**B05 · CODE**

The driver, which I wrote in the humanoid body. Every physics frame it asks two things. Is the tablet put away? Then the screen is off, at once. Has the tablet's move reached the hand? Only then is it on. In between, it keeps the last answer, so switching hands never flickers.

**B06 · RESULT**

Here it is in the game, driven by scripted Tab key presses. Out to one hand: dark while it moves, lit as it arrives. Up to two hands: no flicker. Put away: dark at once. Out and straight back: never lit.

**B07 · CODE**

The tablet does the writing. Set screen lit picks the strength, zero point three nine from an exported variable, and writes it into this tablet's own material. The material is local to scene, so every tablet gets a copy, and one player's screen cannot light another's.

**B08 · RESULT**

The headless test drives the same path with real key events at thirty, sixty and a hundred and forty-four frames per second. Lit after zero point three five seconds of game time, within one frame. And the second body's screen stayed at zero on every frame.

**B09 · CODE**

Question two: how is a material different from a shader? The defaults are written in the shader; the current values live in the ShaderMaterial, and two objects that share a material share its values. This is the long crate's material: the same shader, the same two textures, and only two values of its own: wear zero point two, roughness zero point nine five.

**B10 · RESULT**

One shader, two materials. The long crate is more worn and duller than the small one, because I decided it gets dragged around more. The textures and the scale are the same: it is the same sheet metal.

**B11 · CODE**

Question three: why is a texture information, not a picture? Line thirty-six reads a height map, but nobody sees it. Its red channel is a number, and line thirty-eight compares it with wear amount: the low places turn to rust first. Only the rust texture on line thirty-five is a colour.

**B12 · RESULT**

Drag wear amount and the mask decides where. At zero there is no rust. At my default, about one tenth of the surface. At one, all of it. The pattern never moves; only the threshold does.

**B13 · CODE**

The long crate has no UVs at all, and I could not change the model. So vertex makes them. It reads the normal, picks the two axes the face does not point along, and uses the vertex position there, times texture scale. Object space, so the rust moves with the crate.

**B14 · RESULT**

Texture scale is repeats per metre. At zero point one the rust becomes big blotches; at ten it is fine speckle. My default, two, gives patches of roughly twelve to sixteen centimetres.

**B15 · CODE**

Question four: what is the Godot shading language? It is close to GLSL, with things GLSL leaves to you. Group uniforms and hints turn these lines into an Inspector panel, three groups, five values. And it hands you material outputs, albedo and roughness, that Godot's own lighting finishes.

**B16 · RESULT**

The sweep, every value at its minimum, default and maximum. Paint colour swaps the paint and leaves the rust. Roughness only shows from a highlight angle. And at maximum softness the hard paint edge blurs.

**B17 · CODE**

The hint experiment. One three-by-one grey PNG, sampled twice. Line four says source colour; line five does not. That is the only difference. I predicted the numbers by hand before running it.

**B18 · RESULT**

Measured on a real render: sixty-four, one twenty-eight, one ninety-two with the hint. A hundred and thirty-seven, one eighty-eight, two twenty-five without. Every band matches. With the hint, decode and encode cancel; without it, the file's numbers are taken as light and come out brighter.

**B19 · CODE**

Godot can write a shader too. I converted a standard material and annotated what it wrote. Line thirteen samples the albedo with source colour: my comment on line twelve says why. My crate's line three does the same for the rust.

**B20 · RESULT**

And what that hint does to my crate. In an isolated copy made for this film, I removed source colour from line three. The rust turns pale and washed out: the colour texture is read as if it were already linear.

**B21 · CODE**

The second annotated line: forty-two. The normal map has no source colour, because it stores directions, not colours. My crate's line four, the wear mask, leaves it off for the same reason.

**B22 · RESULT**

Directions can be checked. The curl ratio is low when a normal map is read in its own convention and near two in the wrong one. The GL map scores zero point two in GL and one point eight in DirectX, and its DirectX twin the other way round. No flip needed.

**B23 · CODE**

What the tests prove. This check, written in the audit, reads every sampler's hints straight from the shader source and compares them with the plan. Nothing renders; it reads text.

**B24 · RESULT**

So I broke it on purpose. With source colour deleted, the suite fails, exit code one. The screen shader's mutations failed too: a missing semicolon, and a renamed uniform. The rename is the sneaky one: the shader still compiles, and only the uniform-list check notices.

**B25 · LIMITS**

And what no headless run can show: whether any of it looks right. The tests read source, import settings and values written to materials. The colours, the rust, the highlight: those are captures, and a person looking. One known limit: the shader never writes metallic, so the silver scratches are shaded as paint.

**B26 · VERDICT**

Verdict. Built: two shaders I wrote, a driver, two materials, and a hint experiment that matched to the pixel. Caught: Claude's first test had three bugs; its audit misnamed an import option and cited a setting that is not in the file; it once compared numbers from two different runs. Textures: ambient C G, Metal zero four one C, C C zero. Still uncertain: only captures, never a headless run, show that the GPU really decodes s R G B; why the right normal map scores zero point two and not zero, which the report puts down to eight-bit quantisation; and what hint roughness normal does to roughness on import. Next: put the tablet's own interface on its screen through a SubViewport, so the screen shows more than a glow.

**B27 · HANDOFF**

Your turn. Paste this into Claude. Please use Walker on my Godot project. Read my change brief and my crate shader. Add a metal mask so the bare-metal scratches write metallic, as a new uniform with a hint and a default. Before you change anything, predict which pixels of my crate capture will change, then capture again and compare. The prediction is the point. Write down where the change should show before you look. This was Liam, narrating for Jonathan.

**B28 · OUTRO**

claude liam, walker survival shooting, a five, gamedev. At Nik Bear Brown.

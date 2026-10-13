# Film cards (generated)

**What this is.** One card per film in the series: the idea, the wrong assumption the film opens on, its estimated length, what running Godot corrected, and where to read it.
**Why.** So the whole series can be judged on one page before anyone opens twenty scripts.
**Found.** Read from each film's `narration.py` and `FACTCHECK.md` by `make_film_cards.py`; lengths are estimates from word count (0.34 s per word plus 4 s), not from audio.

**Cards.** 20 films laid out of 20.

## Foundations

### Godot Shaders

- **The idea.** Learn what a shader is, the words you will meet along the way, and how to write one that your game can control.
- **Opens on the assumption.** "A shader decides the color of the whole screen." (the hesitant writer corrects it to "one pixel").
- **Length.** 49 beats, 1868 words, about 10.7 minutes. Lanes: capture 17, manim 18, remotion 6, editor 2. lint clean.
- **Corrected by running Godot (8).** In the node's Material slot choose ShaderMaterial under New; click it; in its Shader slot choose New Shader; set the mode to Canvas Item (the dialog s | In the Inspector, under Shader Parameters, there is a control labelled Red | A range hint adds a slider bar to a number box; a source color hint gives a color swatch that opens a picker | SOURCE SAID: TIME is the time since the scene or the shader was created …
- **If it runs long.** Cut, in this order: the budget-bars beat (B05), then the typo beat (B32), the editor-slider beat (B27) and the tween beat (B33): each repeats an idea another beat already carries.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/SCRIPT.md`

### Godot Shader Language

- **The idea.** Learn how a shader file is built, what its types and vectors mean, and how to read any shader line by line, even one an AI wrote for you.
- **Opens on the assumption.** "A shader line works on one number at a time." (the hesitant writer corrects it to "a bundle of numbers").
- **Length.** 47 beats, 1918 words, about 10.9 minutes. Lanes: capture 8, remotion 6, manim 22, terminal 5. lint clean.
- **Corrected by running Godot (5).** SOURCE SAID: Godot's language is based on GLSL 3.0 | DOCS EXAMPLE: the operators table writes vec3(4, 5, 6) + 2 | SOURCE SAID (brief): custom functions cannot see built-ins | DOCS WORDING: in means the argument is only for reading …
- **If it runs long.** Cut, in this order: the overloading beat (B27), the two-performance-notes beat (B33), the global-built-ins half of B24 (keep the pass-it-in half), and the ternary beat (B29): each repeats an idea another beat already carries or is an extra.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shader-language/SCRIPT.md`

### The Shader Math Toolkit

- **The idea.** Learn a dozen small functions that shape what a shader draws, then use three of them to build a soft ring.
- **Opens on the assumption.** "Shaders need advanced math." (the hesitant writer corrects it to "a dozen small functions").
- **Length.** 47 beats, 1815 words, about 10.4 minutes. Lanes: capture 16, manim 23, remotion 2. lint clean.
- **Corrected by running Godot (3).** SOURCE SAID: smoothstep(0, 10, 1) returns 0.1, as if it were a straight line | SOURCE SAID: fragments are stretched, non-square shapes while pixels are always squares (offered as the reason for the oval) | SOURCE SAID: swap the arguments to invert it
- **If it runs long.** Cut, in this order: the toolkit map (B06), the sine beat (B34), the normalize beat (B27), the soft-spot beat (B31), the smooth step docs beat (B12) and the floor-only beat (B21).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shader-math-toolkit/SCRIPT.md`

### Textures and Color

- **The idea.** Learn how a shader reads a texture, how to do math on color, and why the color you type is not always the color you see.
- **Opens on the assumption.** "A texture is a picture pasted onto a shape." (the hesitant writer corrects it to "looked up by address").
- **Length.** 47 beats, 1918 words, about 10.9 minutes. Lanes: capture 27, manim 7, editor 3, remotion 4. lint clean.
- **Corrected by running Godot (4).** In the Inspector, the slot's menu lists Noise Texture two D under a heading New, and the Noise slot's menu lists Fast Noise Lite under New | SOURCE (docs, Overview of renderers) SAID: in the editor the renderer's name sits in the upper right corner and clicking it switches renderers | SOURCE SAID (brief): the source course never mentions sRGB against linear | SOURCE SAID (brief): grayscale by picking a channel (the source admits it favors a channel)
- **If it runs long.** Cut, in this order: the tween beat (B26), the brighten beat (B13), the alpha-hole beat (B12), the gray pair (B14, B15), then the from-code beat (B36): each extends an idea another beat already carries.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-textures-and-color/SCRIPT.md`

### Shaders in 3D

- **The idea.** Learn what changes when a shader draws a three-D surface, how lighting and the renderer change the color you get, and how to read a real one.
- **Opens on the assumption.** "3D shaders are a different, harder thing." (the hesitant writer corrects it to "the same shape, new names").
- **Length.** 50 beats, 1814 words, about 10.3 minutes. Lanes: capture 24, manim 14, remotion 5, editor 1. lint clean.
- **Corrected by running Godot (2).** Color exists in a three-D fragment but can only be read | SOURCE (docs, Overview of renderers) SAID: the renderer's name is in the upper right corner of the editor and can be switched there
- **If it runs long.** Cut, in this order: the tween beat (B28), the cull beat (B17), the two-questions beat (B18), the output-is-s R G B beat (B42) and the missing-functions beat (B35): each repeats an idea another beat carries.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/SCRIPT.md`

## Fragment techniques

### UV Space

- **The idea.** Learn to move, scale, tile and mirror the address a shader looks up, so you can scroll a picture, zoom into it, and keep a circle round on any shape.
- **Opens on the assumption.** "UV says where a pixel is on the screen." (the hesitant writer corrects it to "the shape").
- **Length.** 48 beats, 1812 words, about 10.3 minutes. Lanes: capture 19, manim 17, remotion 6. lint clean.
- **Corrected by running Godot (3).** SOURCE SAID: scaling UV by 2 shows only the top-left corner | SOURCE SAID (docs): TextureRect is not affected by texture_repeat, as it uses its own repeating implementation | SOURCE SAID: the oval is because fragments can be stretched into non-square shapes while pixels are always squares
- **If it runs long.** Cut, in this order: the node-setting beat (B16, a second route to the same repeat switch), the transparent-border beat (B37), the stretched-pixel beat (B31), the fold drawing (B26) and the gate drawing (B39: the mask then takes one beat, B38).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-uv-space/SCRIPT.md`

### Patterns and Pixelation

- **The idea.** Learn the two small functions that cut a shape into cells, and use them to pixelate an image and to draw checkerboards, stripes and dots.
- **Opens on the assumption.** "Patterns need a pattern image." (the hesitant writer corrects it to "math on the address").
- **Length.** 49 beats, 1790 words, about 10.2 minutes. Lanes: capture 22, manim 18, remotion 3. lint clean.
- **Corrected by running Godot (1).** The half inside the floor is not centering: it halves the first and last blocks
- **If it runs long.** Cut, in this order: the scale beat (B24), the worked example (B16) and the diagonal-step beat (B28), then merge the moving stripes (B33) into the stripes beat (B32).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-patterns-and-pixelation/SCRIPT.md`

### Drawing Shapes with Math

- **The idea.** Learn how a shader draws a circle, a ring and a cross using only math, then build a crosshair you can reshape with sliders.
- **Opens on the assumption.** "To draw a circle you need a circle image." (the hesitant writer corrects it to "a question for each pixel").
- **Length.** 50 beats, 1900 words, about 10.8 minutes. Lanes: capture 25, manim 15, remotion 3, editor 1. lint clean.
- **Corrected by running Godot (2).** SOURCE SAID: the oval comes from pixels being always square while fragments can be stretched | SOURCE SAID: an out-of-range mask "will not be visible"
- **If it runs long.** Cut, in this order: the ring-in-numbers table (B13), the hard-edge beat (B34), the second numbers table (B16), then one of the three dial-sweep beats (B42: arm width and arm gap move into B41).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math/SCRIPT.md`

### Soft Edges, Glow and Noise

- **The idea.** Learn how to soften an edge, layer a highlight on top, scroll noise through it, and make glow work for real, so your effects stop looking flat.
- **Opens on the assumption.** "A soft edge needs a blur." (the hesitant writer corrects it to "a ramp").
- **Length.** 48 beats, 1791 words, about 10.2 minutes. Lanes: capture 23, manim 15, editor 2, remotion 2. lint clean.
- **Corrected by running Godot (4).** SOURCE SAID: smoothstep(0, 10, 1) returns 0.1 | SOURCE SAID: multiply a color by five and it glows | SOURCE SAID: normalize(VERTEX) scales the shield out from its center | Docs vs run: the tutorial says HDR 2D is for Forward+ and Mobile
- **If it runs long.** Cut, in this order: the reveal-pace beat (B32), the beat on what else H D R two D changes (B40), the swapped-lines beat (B10) and the beat on glow without H D R two D (B41).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-soft-edges-glow-and-noise/SCRIPT.md`

### Time and Waves

- **The idea.** Learn what a shader's clock really counts, and how one sine wave with four numbers makes a pulse, a loop or a ripple.
- **Opens on the assumption.** "TIME starts at zero when my node appears." (the hesitant writer corrects it to "when the game starts").
- **Length.** 46 beats, 1690 words, about 9.6 minutes. Lanes: capture 18, remotion 4, manim 18. lint clean.
- **Corrected by running Godot (3).** SOURCE SAID: TIME is the time since the scene or the shader was created | BRIEF SAID: use `amp * sin(freq * x + phase) + offset`, where offset is the vertical shift | BRIEF SAID: put Sine, Amplitude, Frequency and Offset in the terms card
- **If it runs long.** Cut, in this order: the two-waves beat (B34), the roll-over beat (B04), the edge-smear beat (B33) and the sine-or-ramp beat (B24): each extends an idea another beat already carries.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-time-and-waves/SCRIPT.md`

### Trigonometry for Shaders

- **The idea.** Learn what sine and cosine really do, then use them to send a moon around a planet and reveal a picture like a clock hand.
- **Opens on the assumption.** "Trigonometry is for triangles on paper." (the hesitant writer corrects it to "turning angles into positions").
- **Length.** 46 beats, 1752 words, about 10.0 minutes. Lanes: capture 13, manim 23, remotion 4. lint clean.
- **Corrected by running Godot (1).** A draft called the eight-lobed shape a gear
- **If it runs long.** Cut, in this order: the flower beat (B40), the three-moons beat (B23), the arm beat (B30) and the oval-limit beat (B24): each is a bonus that repeats an idea another beat already carries.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-trigonometry-for-shaders/SCRIPT.md`

### Lines and Shine

- **The idea.** Learn how a shader draws a line at any angle from one rule, and how to slide that line across a sprite as a shine.
- **Opens on the assumption.** "A line needs two points." (the hesitant writer corrects it to "one rule").
- **Length.** 41 beats, 1587 words, about 9.1 minutes. Lanes: capture 21, manim 14. lint clean.
- **Corrected by running Godot (3).** BRIEF: the tangent near ninety has a visible failure to verify | BRIEF: without the divide the line gets thicker as it steepens | BRIEF: a center uniform moves the line but only works along one axis at 45 degrees
- **If it runs long.** Cut, in this order: Act V (B31 to B35), and with it the last sentence of B14, which promises it; then the center-shift beat (B23); then fold B16 and B17 into one beat (the band, then the tilt).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-lines-and-shine/SCRIPT.md`

### Outlines

- **The idea.** Learn how a shader draws a line around a sprite by asking each pixel about its neighbors, and the traps that make an outline vanish or break.
- **Opens on the assumption.** "An outline is a bigger copy behind the sprite." (the hesitant writer corrects it to "a question about neighbors").
- **Length.** 47 beats, 1868 words, about 10.7 minutes. Lanes: capture 27, manim 11, remotion 3. lint clean.
- **Corrected by running Godot (6).** The form used is a product, line amount times (1 minus own alpha), where the brief subtracts the pixel's own alpha from the amount | The brief's claim: ifs inside a shader are not recommended and slow every fragment | The brief's recipe creates the larger image with the older Image.create | The brief's claim: animated sprites work because the shader sees whatever texture is current …
- **If it runs long.** Cut, in this order: the line-color beat (B14), the loop-cost beat (B22), the branch beat (B24), the modulate beat (B40), then the thin-part beat (B37) and the brush-number beat (B35).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-outlines/SCRIPT.md`

## Vertex and space

### Vertex Shaders

- **The idea.** Learn how a shader moves the corner points of a shape, and how to give a shape enough corners to bend. By the end you can build a waving flag.
- **Opens on the assumption.** "A vertex shader changes pixels." (the hesitant writer corrects it to "moves corners").
- **Length.** 46 beats, 1730 words, about 9.9 minutes. Lanes: capture 27, manim 12, terminal 1. lint clean.
- **Corrected by running Godot (1).** Subdivide width and subdivide depth say how many extra cuts to make across and down
- **If it runs long.** Cut, in this order: the color-shortcut beat (B33), the flat beat (B30), the wind beat (B25), the polygon-needs-a-texture beat (B38) and the upside-down beat (B35): each repeats a lesson another beat already carries or is a trap rather than the main line.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders/SCRIPT.md`

### Matrices and Fake 3D

- **The idea.** Learn what a matrix does to a point, how to combine moves, and how to flip a flat picture like a card.
- **Opens on the assumption.** "A matrix is advanced math you can skip." (the hesitant writer corrects it to "a saved move").
- **Length.** 47 beats, 1791 words, about 10.2 minutes. Lanes: capture 15, manim 22, remotion 4. lint clean.
- **Corrected by running Godot (4).** SOURCE (brief) SAID: combine as translate times scale times rotate times v | BRIEF SAID: for a 128-pixel sprite, 64 is the right edge | BRIEF SAID: BIDEA_TEXT = ('Matrices are advanced math you\ncan skip.', 'advanced math you can skip', ...) | SOURCE (brief) SAID: the result looks like 3D
- **If it runs long.** Cut, in this order: the order-swap pair (B22, B23), the corner spin (B38), the two-turns beat (B31) and the card-versus-box beat (B33): each repeats an idea another beat already carries.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-matrices-and-fake-3d/SCRIPT.md`

### Local, World and Screen Space

- **The idea.** Learn why one point has three sets of numbers, and how a shader switches between them to pin an effect to a sprite, the world or the screen.
- **Opens on the assumption.** "A position is just a position." (the hesitant writer corrects it to "an address in some space").
- **Length.** 46 beats, 1779 words, about 10.1 minutes. Lanes: capture 12, manim 24, editor 1, terminal 1, remotion 2. lint clean.
- **Corrected by running Godot (3).** FRAGCOORD counts pixels: the last pixel of a 1280 by 720 window reads 1279.5, 719.5 | SOURCE SAID: include the zero and the one in the vec four (no reason given) | SOURCE SAID: for a world-locked texture, multiply world position by texture pixel size (the sprite's size, 128 in the example)
- **If it runs long.** Cut, in this order: the hole beat (B24), the wrong-order beat (B29), the turn-and-stretch beat (B22) and the parents warning (B11): each repeats an idea another beat carries, and none leans on its neighbours.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space/SCRIPT.md`

## Screen, textures and light

### Reading the Screen

- **The idea.** Learn how a shader can read what the game has already drawn, so you can filter the whole screen, bend the picture, and build water you can see through.
- **Opens on the assumption.** "A shader only knows its own sprite." (the hesitant writer corrects it to "what is already on screen").
- **Length.** 44 beats, 1685 words, about 9.6 minutes. Lanes: capture 25, manim 11, remotion 2. lint clean.
- **Corrected by running Godot (7).** SOURCE SAID (via the brief): the screen texture holds "everything up to this node" | SOURCE SAID (via the brief): an "overlay" blend gives the natural look | SOURCE SAID: the circle goes oval because fragments can be stretched while pixels are square | SOURCE SAID (docs and Bear's chapter 06): if two screen-reading shaders overlap, the second never uses the result of the first …
- **If it runs long.** Cut, in this order: the symptom table (B38), the finale (B37), the mouse-filter beat (B13), the edge-and-filter beat (B36) and the frosted-glass beat (B25): each repeats an idea another beat already carries, or adds a habit rather than the idea.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reading-the-screen/SCRIPT.md`

### Reflections

- **The idea.** Learn how a shader can read a hidden map of the water, and use it to give a character a reflection that shows only over water.
- **Opens on the assumption.** "A reflection needs a second drawing of the scene." (the hesitant writer corrects it to "a map the shader can read").
- **Length.** 43 beats, 1557 words, about 8.9 minutes. Lanes: capture 19, manim 12, editor 2, remotion 4. lint clean.
- **Corrected by running Godot (3).** THE BRIEF SAID: the source compares the mask (this film: the label map) with == against pure red | THE BRIEF SAID: BIDEA_TEXT = ("A reflection needs a second\ndrawing of the scene.", "a second drawing of the scene", ...) | THE BRIEF SAID: BackBufferCopy modes and a viewport-mode requirement (quote the docs)
- **If it runs long.** Cut, in this order: the renderer-table beat (B31), the color-distance picture (B32), then the polish pair (B34 coast, B35 tint), then the canvas-layer beat (B15).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/SCRIPT.md`

### SubViewports

- **The idea.** Learn how a Sub Viewport draws part of your game into a picture, and how to shade that picture with a second shader.
- **Opens on the assumption.** "Shaders cannot see each other's work." (the hesitant writer corrects it to "can build on").
- **Length.** 46 beats, 1840 words, about 10.5 minutes. Lanes: capture 22, manim 16, editor 2. lint clean.
- **Corrected by running Godot (4).** In the editor: add a SubViewport, give it a size, put a sprite inside, add a second sprite outside; in the second sprite's Texture slot open the menu, | The source's fade `COLOR.a = UV.x` is wrong on a transparent picture; multiply the whole color, not only the alpha, because the picture's colors alrea | The source says Transparent BG is needed to keep the original alpha. | The brief's opening line, "Each node gets one shader", with the replacement "two shaders in a row".
- **If it runs long.** Cut, in this order: the input beat (B39), the update-mode beat (B38), the three-in-a-row beat (B37), the per-pixel beat (B20), then the hue beats (B26 to B29), keeping the stripes at one color.
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/SCRIPT.md`

### Light Shaders

- **The idea.** Learn what the light function does and what Godot hands it, then use it to build a sweeping lighthouse beam and a ring that spreads from a lamp.
- **Opens on the assumption.** "Lighting is built in. You can't touch it." (the hesitant writer corrects it to "A shader can replace it").
- **Length.** 46 beats, 1808 words, about 10.3 minutes. Lanes: capture 25, manim 12, remotion 3. lint clean.
- **Corrected by running Godot (3).** U V is available in light (SOURCE SAID: a light shader cannot read UV) | LIGHT_DIRECTION is an arrow from this pixel toward the lamp, length one | SOURCE SAID: light shaders cannot read UV
- **If it runs long.** Cut, in this order: the grid beat (B39), the stripes beat (B38), the pulse beat (B16), then the limits beat (B18).
- **Read.** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders/SCRIPT.md`


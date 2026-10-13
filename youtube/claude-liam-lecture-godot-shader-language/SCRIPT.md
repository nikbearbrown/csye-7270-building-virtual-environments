# Script: Godot Shader Language

**What this is.** The words Liam will say in *Godot Shader Language*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 47 beats, 1910 words, about **10:53** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: manim 22, capture 8, remotion 6, terminal 5.

**If it runs long.** Cut, in this order: the overloading beat (B27), the two-performance-notes beat (B33), the global-built-ins half of B24 (keep the pass-it-in half), and the ternary beat (B29): each repeats an idea another beat already carries or is an extra. The vectors-and-swizzles beats (B12 to B17), the signature and built-in beats (B20, B23), and the whole reading act (B34 to B41) stay: they are the film.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | The Shape of a File | 9 | 355 | ~2:01 |
| II | Types and Vectors | 10 | 414 | ~2:21 |
| III | Your Own Functions | 8 | 300 | ~1:42 |
| IV | Choices and Loops | 6 | 249 | ~1:25 |
| V | Read One Aloud | 8 | 291 | ~1:39 |

## Opening

### BOPEN · identity card · 32 words · ~11 s

> Godot Shader Language. Learn how a shader file is built, what its types and vectors mean, and how to read any shader line by line, even one an AI wrote for you.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Godot Shader Language", and the line "How to read any shader, one type at a time".

### BIDEA · the question · 49 words · ~17 s

> Hallo. This is Liam, in for Bear. When you first read shader code, it is natural to assume each line works on one number at a time. It does not. Many values in a shader are bundles of numbers, and one operator works on the whole bundle at once.

*Picture.* The hesitant writer types: "A shader line works on
one number at a time." then deletes "one number" and types "a bundle of numbers".

### BDEFS · terms · 54 words · ~18 s

> Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. A type is the kind of value something holds. A function is a named block of code you can call. An argument is a value you hand it.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Pixel** — one dot of the picture on screen; **Type** — the kind of value something holds: whole number, decimal, bundle; **Function** — a named block of code you can call; **Argument** — a value you hand to a function when you call it

## Act I: The Shape of a File

### B01 · 47 words · ~16 s

> Here is a real shader, fourteen lines long. It makes a color breathe between pale gray and teal. Godot refuses a line that breaks the rules. It will not warn you when a legal line does something you did not mean. So you have to read it.

*Picture.* Act title 'The Shape of a File' (serif 40) top-left. The real 14-line file `lab-shaders/01-breathe.gdshader` in the code panel at left with line numbers; at right a framed real Godot render that breathes between pale gray and teal. Window label: 'Godot 4.7.2 · Forward+ · tint set to teal'.

*Motion.* The render swings from pale gray to teal and back while the file stays still beside it.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C01a: Lab rect, lab-shaders/01-breathe.gdshader, --set tint=#5FA391 (the Inspector would set it), live TIME, a clip a little longer than this beat's measured audio (about 16 s) at 30 fps, Forward+, no input. Verified: the pulse swings between about 0.90 gray and (0.38, 0.64, 0.57); period about 3.2 s (evidence/planning-checks/pulse-range.txt). Gate V samples the 50 and 85 percent frames and fails a pale fill on the cream stage, so set --time-origin t0 so that wave = 0.5 + 0.5 * sin(2 * (t0 + t)) is 0.4 or less at t = 0.5 and 0.85 times this beat's measured audio (for 16.0 s, t0 about 0.98 s gives 0.11 at both). B40 needs its OWN clip (C01b): one origin cannot serve both beats.

### B02 · 35 words · ~12 s

> A shader file has three zones, read from the top down. The header says what kind of shader this is. The globals are values declared outside every function. The functions are where the work happens.

*Picture.* The same 14-line file alone on the stage (layout 'code', line numbers on). Three bands light in turn with a one-word chip beside each: line 1 'header', lines 3 to 4 'globals', lines 6 to 14 'functions'.

*Motion.* A highlight band slides down the file and stops on each zone as the voice names it.

*Lane.* remotion · `ShaderLab` · runner-up: manim code card with bands

### B03 · 40 words · ~14 s

> The header starts with shader type, and it must be the first line. Canvas item means two-D drawing and interface. Spatial means three-D. An optional second line, render mode, picks options, such as how a pixel blends with the background.

*Picture.* `shader_type canvas_item;` in monospace (size 40) upper center. Under it a row of tiles: `canvas_item` captioned '2D + interface' and `spatial` captioned '3D' (both outlined), and three small tiles `particles`, `sky`, `fog` under a bracket labelled 'more'. A terracotta ring settles on canvas_item, in the line and on its tile. Serif 32 caption: 'shader type: the first line; says what the shader is for'. Last, a dimmer second line `render_mode blend_add;` slides in below with a tag 'optional' and a drawn pair of overlapping outlined squares whose overlap is tinted lighter, labelled 'blend'.

*Motion.* The first line types in and the tiles line up under it; a ring picks canvas item; then an optional second line slides in below.

*Lane.* manim · `B03_Header` · runner-up: LectureEvidenceTable of shader types

### B04 · 40 words · ~14 s

> Globals sit outside every function. A uniform is a value your game sets from outside. A const never changes. A varying hands a value from a shape's corners to its pixels. Declare each one above the code that uses it.

*Picture.* A band labelled 'globals' with three rows stacked, each a declaration copied from lab-shaders/04-globals.gdshader in monospace with a serif 32 caption beneath in the GLOSSARY wording: `uniform float level = 0.8;` / 'a value your game sets from outside; every pixel sees the same one'; `const vec3 TEAL = vec3(0.37, 0.64, 0.57);` / 'a named value that never changes'; `varying vec2 corner_uv;` / 'a value set at each corner, blended across the shape for fragment() to read'. Below the band a thin bar labelled 'functions' and a drawn downward arrow from the band into it, labelled 'readable below'. Captions may wrap to two lines.

*Motion.* The three declarations land one by one as they are named; a downward arrow then runs from them into the functions bar.

*Lane.* manim · `B04_Globals` · runner-up: LectureEvidenceTable with three rows

### B05 · 43 words · ~15 s

> Then come the functions. Godot calls three of them for you. Vertex places the corners, fragment sets the color of each pixel, and light handles each light that touches a pixel. This film uses fragment. Any other function is one you write yourself.

*Picture.* A three-row table in the GLOSSARY wording, one row ringed as each function is named: vertex(), fragment(), light().

*Motion.* The ring steps down the rows with the voice; fragment() stays ringed longest.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: ShaderLab code layout with two labelled ranges

### B06 · 35 words · ~12 s

> Inside a function, every statement ends with a semicolon, and braces group statements into a block. Forget one semicolon and Godot refuses the whole shader. Here it points at the next line, where it noticed.

*Picture.* A terminal window titled 'Godot 4.7.2 · shader compile error · printed by the engine' holding the engine's own log of lab-shaders/40-err-semicolon.gdshader, word for word: the source lines around the error with the offending line marked, then the error message. A terracotta ring lands on the marked line (the line AFTER the one missing its semicolon) late in the beat.

*Motion.* The log lines land one by one; a ring then settles on the marked line.

*Lane.* terminal · `CCPlainShell` · runner-up: ClaudeCodeBeat (cream code card)

### B07 · 36 words · ~12 s

> Spacing and line breaks are for people. Here is one shader that draws a soft gradient, written three ways: neat, squeezed onto one line, and spread over many. Godot draws the same picture for all three.

*Picture.* Top region: one code card that holds one shader in three spellings in turn: neat (the five lines of 02-spacing-neat), squeezed (two lines: `shader_type canvas_item;` then `void fragment(){COLOR=vec4(0.4+0.6*UV,0.7,1.0);}`, 48 characters, the widest line), and spread (the seven lines of 02-spacing-spread). The characters slide and the line breaks collapse and reopen as one spelling becomes the next. Bottom region, never changing: ONE framed real Godot render (lab_window of png/02-spacing-neat.png, a pastel gradient) captioned 'Godot 4.7.2 · Forward+', with a drawn equals sign (two short bars) between code and picture, labelled 'same picture'. Type at least 32; keep the card inside 12 units.

*Motion.* The code is rewritten three times while the picture below it never changes.

*Lane.* manim · `B07_ThreeSpellings` · runner-up: ShaderLab stack layout with one spelling

### B08 · 34 words · ~12 s

> Comments are notes for people. Two slashes comment out the rest of a line. Slash star starts a block comment, and star slash ends it. Godot skips both, so a commented-out line does nothing.

*Picture.* Left: the nine-line card of lab-shaders/03-comment-on.gdshader with a block comment above the function and a trailing `// soften` comment: both comment spans are grayed from the first frame. Right: a framed real render (lab_window of png/03-comment-on.png, the pastel gradient). Then `//` is typed at the start of the line `c = 0.4 + 0.6 * c;` (the line grays out, as in lab-shaders/03-comment-off.gdshader) and the render cross-fades to the real png/03-comment-off.png (the same colors, much more saturated, dark top-left corner). Captions: 'line comment', 'block comment'.

*Motion.* Typing two slashes grays a line out and the picture beside the code changes at once.

*Lane.* manim · `B08_CommentOut` · runner-up: LectureCodeTrace

### B09 · 45 words · ~15 s

> Godot's language is close to G L S L, the shading language of OpenGL, but not identical. Names must match exactly, capitals included: a capital L makes level a different name. The other language's G L frag color is unknown here. Godot calls it color.

*Picture.* Two panels. Left: two name tags in monospace, `level` with a drawn check and `Level` with a drawn cross, a drawn capital-L highlight on the difference. Right: `gl_FragColor` with a drawn cross, a drawn arrow to `COLOR` with a drawn check, captioned 'Godot's name for the output'. Top caption in serif 32: 'GLSL: the OpenGL Shading Language; Godot's is close to GLSL ES 3.0'. No engine messages on screen (the narration says unknown identifier).

*Motion.* A cross lands on the wrong-case name and on the other language's name; the check lands on Godot's.

*Lane.* manim · `B09_NamesMustMatch` · runner-up: CCPlainShell with two logs

## Act II: Types and Vectors

### B10 · 45 words · ~15 s

> Every value has a type. A float is a decimal number, an int is a whole number, and a bool is true or false. A texture has a type too, called sampler two D. You declare a variable with its type first, then its name.

*Picture.* Act title 'Types and Vectors' (serif 40) top-left. Four outlined tiles in a row, each a type with a sample value in monospace: `float` / 0.5, `int` / 3, `bool` / true, `sampler2D` / a small drawn picture icon (a framed square with a hill shape). Under each tile a plain label: 'a decimal number', 'a whole number', 'true or false', 'the type of a texture a shader reads'. A one-line serif 32 caption under the row, in the GLOSSARY wording: 'texture: an image a shader can read by address'. Below, the declaration `float level = 0.5;` (a line of lab-shaders/32-declaration.gdshader) with three drawn brackets under it labelled 'type', 'name', 'value'.

*Motion.* The tiles pop in as each type is named; the declaration types in and its three parts are bracketed.

*Lane.* manim · `B10_ThreeTypes` · runner-up: LectureEvidenceTable of types

### B11 · 44 words · ~15 s

> Godot is strict about this. A two with no decimal point is an int, and Godot will not quietly turn it into a float. Put it in a float, or add it to one, and the shader will not compile. Write two point zero.

*Picture.* A terminal window holding two short excerpts of the engine's own log, word for word and separated by a blank line: the marked line `float a = 2;` with 'Invalid assignment of 'int' to 'float'.' and the marked line `float a = 1 + 1.0;` with 'Invalid arguments to operator '+': 'int, float'.' A ring lands on each message.

*Motion.* Each marked line lands with its message; a ring settles on the type names in the message.

*Lane.* terminal · `CCPlainShell` · runner-up: Manim code line with a refusal mark

### B12 · 41 words · ~14 s

> Shaders are full of vectors, bundles of two to four numbers: vec two, vec three, vec four. A color is a vec four: red, green, blue and alpha, how solid it is. Reading a texture gives back a vec four too.

*Picture.* Rows of outlined cells (the bundle cast), stacked: `vec2` two cells, `vec3` three cells, `vec4` four cells labelled r g b a, the vec4 cells holding 0.37, 0.64, 0.57, 1.0 with a plain teal swatch to its right labelled 'a color'. Far left of the vec4 row, a framed small drawn texture (gradient square) with a drawn arrow into the row, labelled 'texture lookup'. Serif 32 caption: 'vector: a bundle of two to four numbers'. Under the last cell, in the GLOSSARY wording, 'alpha: how visible a pixel is: 0 invisible, 1 solid'.

*Motion.* Rows of cells pop in one after another as the sizes are named; the texture arrow feeds the vec4 row last.

*Lane.* manim · `B12_Bundles` · runner-up: LectureEvidenceTable

### B13 · 43 words · ~15 s

> You build a vector by naming its type. Give vec three one number and it fills all three parts. Give vec four a vec three and a number and it joins them. The pieces must add up to the size, or Godot refuses.

*Picture.* Three mini-diagrams stacked, using the bundle cells. (1) `vec3(0.5)`: one cell [0.5] sprouts two copies to make [0.5][0.5][0.5]. (2) `vec4(c, 1.0)`: a three-cell bundle c and a one-cell [1.0] slide together into a four-cell bundle, a drawn counter 3 + 1 = 4. (3) `vec3(0.1, 0.2)`: two cells and a dashed empty cell with a drawn cross, counter 2 of 3, labelled 'too few'.

*Motion.* Cells copy, slide together and join into a bundle of the right size; the short one is refused.

*Lane.* manim · `B13_BuildAVector` · runner-up: ShaderLab

### B14 · 37 words · ~13 s

> Arithmetic works on every part at once. Multiply a vec three by two point zero and all three numbers double. Multiply two vectors and each part meets its partner. That is why shader code is so short.

*Picture.* Top: a three-cell bundle (0.2, 0.3, 0.4), a drawn times sign, a single cell 2.0; three parallel drawn arrows leave the 2.0 for each cell at the same instant; the result bundle (0.4, 0.6, 0.8) appears. Bottom: the same bundle times a second bundle (2.0, 1.0, 0.5); three short drawn arrows pair cell to cell, top to bottom; the result (0.4, 0.3, 0.2). Labels in monospace: `* 2.0`, `* vec3(2.0, 1.0, 0.5)`.

*Motion.* Three arrows fire at the same instant and all three numbers change together; then each part meets its partner.

*Lane.* manim · `B14_AllAtOnce` · runner-up: LectureCodeTrace

### B15 · 43 words · ~15 s

> Here it is in use. U V is the address of each pixel, a vec two. Join it with one half to make a vec three, scale by zero point six, add zero point four. Red grows to the right, green grows downward.

*Picture.* Code panel at left with the five-line shader; at right a framed real render: a pastel gradient, red growing to the right and green growing downward, blue constant. Short readouts 'more red' near the top-right corner and 'more green' near the bottom-left corner. Caption under the render: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.

*Motion.* The vector line is highlighted; the two readouts then name the directions the colors grow.

*Lane.* capture · `ShaderLab` · runner-up: manim with the render inset

*Capture to record.* C04: Lab rect, lab-shaders/05-pastel.gdshader, still PNG 1920x1080, Forward+. Probes: (0.02,0.02) (0.4118, 0.4118, 0.702); (0.98,0.02) (0.9882, 0.4118, 0.702); (0.02,0.98) (0.4118, 0.9843, 0.702); (0.98,0.98) (0.9882, 0.9843, 0.702).

### B16 · 38 words · ~13 s

> You can reach into a vector by name. Dot R G B takes red, green and blue from a vec four. Dot X Y takes the first two parts. Picking or reordering parts like this is called swizzling.

*Picture.* A four-cell vec4 row with THREE label rows: x y z w above the cells, r g b a below them, and a fainter s t p q under those (the third set, for texture coordinates). A drawn bracket over the first three cells labelled `.rgb` lifts them out into a three-cell vec3 row; then a bracket over the first two labelled `.xy` lifts them into a two-cell vec2 row. Serif 32 caption: 'swizzle: picking or reordering a vector's parts'.

*Motion.* A bracket closes round the first three cells and lifts them out as a new, smaller bundle; then the first two.

*Lane.* manim · `B16_Swizzle` · runner-up: LectureCodeTrace

### B17 · 44 words · ~15 s

> Order is yours to choose. Dot B G R reverses the order, and the gradient's colors turn over. R G B A, X Y Z W and S T P Q name the same parts, but never mix sets in one swizzle. Godot refuses.

*Picture.* Code panel at left with the five-line shader whose COLOR line reads `vec4(c.bgr, 1.0)`; at right a framed real render that starts as the pastel gradient of the previous picture and dissolves into the same gradient with its colors turned over (top-left salmon, top-right violet, bottom-left lime, bottom-right cyan). Readout 'bgr' on the picture.

*Motion.* The picture dissolves from the earlier colors to the reversed ones while the swizzle is highlighted.

*Lane.* capture · `ShaderLab` · runner-up: manim with both pictures

*Capture to record.* C05: ffmpeg video, 14 s at 30 fps: 1.8 s hold of the real render of 05-pastel, 0.7 s dissolve, then a hold of the real render of 06-pastel-bgr to the end (both Lab stills 1920x1080, Forward+; re-time the dissolve to start at about 14 percent of the beat once the audio is measured). Probes of the second: (0.02,0.02) (0.702, 0.4118, 0.4118); (0.98,0.02) (0.702, 0.4118, 0.9882); (0.02,0.98) (0.702, 0.9843, 0.4118); (0.98,0.98) (0.702, 0.9843, 0.9882).

### B18 · 38 words · ~13 s

> The type on the left must match the type on the right. Color is a vec four. Hand it a vec three and Godot refuses. Fix it by adding alpha: vec four of c and one point zero.

*Picture.* A terminal window with the engine's own log of lab-shaders/44-err-vec3-to-color.gdshader, word for word: the source lines around `COLOR = c;` with that line marked, then 'Invalid arguments to operator '=': 'vec4, vec3'.' A ring lands on 'vec4, vec3'.

*Motion.* The log lands line by line; a ring settles on the two type names that disagree.

*Lane.* terminal · `CCPlainShell` · runner-up: Manim: a vec4 slot refusing a vec3 bundle

### B19 · 41 words · ~14 s

> To read any line, say the type of each piece, from the inside out. U V is a vec two. Joined with one half, a vec three. Times a float, still a vec three. Plus a float, still a vec three.

*Picture.* The expression `0.4 + 0.6 * vec3(UV, 0.5)` (35 characters) centered in monospace with `vec3 c =` to its left. Beneath it nested drawn brackets grow from the inside out, each landing a small type tag: under `UV` a bracket tagged vec2; under `vec3(UV, 0.5)` tagged vec3; under `0.6 * vec3(UV, 0.5)` tagged vec3; under the whole right-hand side tagged vec3; a final arrow into `c` tagged vec3.

*Motion.* Brackets widen outward from UV, and a type tag lands on each as the voice says it.

*Lane.* manim · `B19_TypeChain` · runner-up: LectureCodeTrace

## Act III: Your Own Functions

### B20 · 31 words · ~10 s

> Now your own functions. The first line of a function is its signature. It has three parts: the type it hands back, its name, and its arguments, each with a type.

*Picture.* Act title 'Your Own Functions' (serif 40) top-left. The line `vec3 soften(vec3 c) {` in monospace (size 40) centered, with the body line `return 0.4 + 0.6 * c;` and a closing brace beneath it. Three drawn brackets under the first line land in order, each with a plain label: under `vec3` 'hands back', under `soften` 'name', under `(vec3 c)` 'arguments, each with a type'. Serif 32 caption: 'signature: the first line of a function'.

*Motion.* Three brackets close in turn round the type, the name and the argument list.

*Lane.* manim · `B20_Signature` · runner-up: LectureCodeTrace

### B21 · 35 words · ~12 s

> Calling the function hands values into the arguments, in order. The body runs. Then return hands one value back, and it must have the type the signature promised. Break that promise and Godot says so.

*Picture.* At left the call `soften(vec3(UV, 0.5))`; a small three-cell token travels along a drawn path into the argument slot `c` of a rounded box that holds `return 0.4 + 0.6 * c;`; the box pulses; a new three-cell token leaves the box and returns to the call, tagged 'vec3, as promised'. Then a four-cell token leaves the box instead and bounces off a drawn bar with a cross, with the engine's message in two short lines under it: `Expected return with an expression` / `of type 'vec3'.`

*Motion.* A bundle goes into the function and a bundle comes back out; a bundle of the wrong size bounces.

*Lane.* manim · `B21_CallAndReturn` · runner-up: LectureCodeTrace

### B22 · 36 words · ~12 s

> Godot reads from the top down. A function must be defined above the one that calls it. Call it first and the message says no matching function found. It does not say the order is wrong.

*Picture.* A terminal window with the engine's own log of lab-shaders/47-err-call-before-define.gdshader, word for word: the source lines around the call `COLOR = vec4(soften(vec3(UV, 0.5)), 1.0);` with that line marked, then 'No matching function found for: 'soften'.' A ring lands on the message.

*Motion.* The log lands line by line; a ring settles on the message that does not mention order.

*Lane.* terminal · `CCPlainShell` · runner-up: Manim: two function boxes with an arrow pointing up

### B23 · 41 words · ~14 s

> A function you write cannot see most built-ins. A built-in is a value the engine hands to a function. U V and color are handed to fragment, not to your function. Use U V inside yours and Godot says unknown identifier.

*Picture.* Two rounded boxes: right, `fragment()` containing three outlined chips `UV`, `COLOR`, `TEXTURE`; left, a box `soften()` of your own. A thick gray vertical wall stands between them. The UV chip leaves fragment, crosses toward the function, hits the wall and bounces back; a small drawn bubble near the bounce reads 'unknown identifier'. Serif 32 caption: 'built-in: a value the engine hands to a function, or collects from it'.

*Motion.* A chip travels toward the function, strikes the wall and is thrown back.

*Lane.* manim · `B23_TheWall` · runner-up: ShaderLab with the failing file

### B24 · 40 words · ~14 s

> The fix is to pass what you need in as an argument. Here U V goes in as address, and the same gradient appears. A few built-ins are global, such as time and pi, and any function can read those.

*Picture.* Code panel at left with the nine-line fixed shader: `vec3 soften(vec2 address)` and the call `soften(UV)`; at right a framed real render: the same pastel gradient as before. Caption under the render (one line, 72 characters): 'global: TIME (seconds on one clock shared by the whole game), PI, TAU, E'.

*Motion.* The parameter line is highlighted, then the call; the same gradient sits beside them.

*Lane.* capture · `ShaderLab` · runner-up: manim: UV passing through the wall

*Capture to record.* C06: Lab rect, lab-shaders/10-pass-uv-in.gdshader, still PNG 1920x1080, Forward+ (identical to the 05-pastel render: 0 pixels differ).

### B25 · 36 words · ~12 s

> Arguments come in three modes. In, the default, hands over a copy, so changes stay inside the function. In out hands over the original, so the caller's variable changes. Out is for writing a result back.

*Picture.* Top strip: three chips with one-to-three-word captions, `in` 'a copy', `inout` 'the original', `out` 'writes back'; the active chip is ringed. Middle: the caller's variable box `a = 0.25`. Bottom: the function signature card, which changes with the active mode. IN (`float bump(float x)`): a ghost copy of 0.25 goes into the function, becomes 0.75 and returns to `b`; the box a still reads 0.25. INOUT (`void bump(inout float x)`): a double-headed drawn arrow ties the function to the box a itself, which changes to 0.75. OUT (`void make(out vec3 c)`): the function writes (0.1, 0.5, 0.9) into an empty three-cell box c in the caller.

*Motion.* A copy changes and the original does not; then the original itself changes; then an empty box is filled.

*Lane.* manim · `B25_InOutInout` · runner-up: LectureEvidenceTable of three modes

### B26 · 40 words · ~14 s

> The functions Godot gives you follow the same pattern, and the documentation lists each signature. In it, vec type means a float or a vec two, three or four. Sine takes one of those and hands back the same type.

*Picture.* The real Godot 4.7 'Built-in shader functions' page in a browser window, scrolled to the 'Trigonometric functions' table: three columns 'Return Type', 'Function', 'Description / Return value' with the rows radians, degrees, sin, cos, tan. The camera pushes in on the sin row, `vec_type` / `sin(vec_type x)` / 'Sine.', and a terracotta ring marks the signature.

*Motion.* The camera pushes in on the sin row and the ring marks the type going in and the type coming out.

*Lane.* remotion · `BrowserCapture` · runner-up: LectureEvidenceTable of sin, mix, length signatures

### B27 · 41 words · ~14 s

> A name can be reused if the argument types differ, and Godot picks by type. This call passes one, an int, and gets teal. This one passes one point zero, a float, and gets sand. Same name, same digit, different function.

*Picture.* Code panel at left with the 14-line shader: two functions named get_color (one taking an int, one a float) and two calls, `get_color(1)` and `get_color(1.0)`; at right a framed real render: the left half teal, the right half sand. Readouts 'int: teal' on the left half and 'float: sand' on the right.

*Motion.* The two function lines light, then each call lights as the matching half of the picture is named.

*Lane.* capture · `ShaderLab` · runner-up: manim: one name, two doors

*Capture to record.* C07: Lab rect, lab-shaders/15-overload.gdshader, still PNG 1920x1080, Forward+. Probes: (0.25, 0.5) (0.3686, 0.6392, 0.5686) teal; (0.75, 0.5) (0.949, 0.8, 0.502) sand.

## Act IV: Choices and Loops

### B28 · 43 words · ~15 s

> An if needs a bool. A comparison, like U V dot X less than one half, gives true or false. If true, the first block runs, otherwise the else block. Declare c above: a variable made inside braces ends at the closing brace.

*Picture.* Act title 'Choices and Loops' (serif 40) top-left. Code panel at left with the 13-line shader: `vec3 c;` then an if/else on `UV.x < 0.5`; at right a framed real render: the left half teal, the right half pale. Readouts 'true' over the left half and 'false' over the right half.

*Motion.* The condition line is highlighted and the left half is tagged true; then the declaration above the if is highlighted.

*Lane.* capture · `ShaderLab` · runner-up: manim: a branching arrow

*Capture to record.* C08: Lab rect, lab-shaders/16-split-if.gdshader, still PNG 1920x1080, Forward+. Probes: (0.25, 0.5) (0.3686, 0.6392, 0.5686) teal; (0.75, 0.5) (0.949, 0.949, 0.949) pale.

### B29 · 40 words · ~14 s

> The ternary is a one-line if. Write the condition, a question mark, the value if true, a colon, then the value if false. It gives back a value, so it can sit inside a longer line. Same picture, one line.

*Picture.* Top region: the six-line choice from lab-shaders/16-split-if (`vec3 c;` / `if (UV.x < 0.5) {` / `c = teal;` / `} else {` / `c = pale;` / `}`) collapses into the single line `vec3 c = UV.x < 0.5 ? teal : pale;` (34 characters) with thin drawn brackets labelled 'condition', 'if true', 'if false' under its three parts, the `?` and `:` ringed, and a serif 32 caption 'ternary: a one-line if'. Bottom region, never changing: ONE framed real render (lab_window of png/16-split-if.png: left half teal, right half pale) captioned 'Godot 4.7.2 · Forward+ · same pixels', with a drawn equals sign.

*Motion.* Six lines fold into one while the picture below never changes.

*Lane.* manim · `B29_Collapse` · runner-up: ShaderLab stack layout

### B30 · 43 words · ~15 s

> A for loop repeats a block. This one runs five times, with the counter i going from zero to four, and each pass draws one stripe. The counter is an int, so convert it with float of i before mixing it with decimals.

*Picture.* Code panel at left with the 12-line shader; at right a framed real render: five teal stripes on a pale field, evenly spaced. Readout 'five stripes' near the picture. The cue on the stripe test carries the label 'abs: drops the minus sign: -0.3 becomes 0.3' (the GLOSSARY wording; abs is on screen but not spoken).

*Motion.* The loop line is highlighted, then the stripe test, then the float(i) line as the voice moves on.

*Lane.* capture · `ShaderLab` · runner-up: manim: a counter stepping 0 to 4

*Capture to record.* C09: Lab rect, lab-shaders/18-stripes.gdshader, still PNG 1920x1080, Forward+. Five stripes centered at 0.1, 0.3, 0.5, 0.7, 0.9 of the height (measured at 640x360: rows 25-46, 97-118, 169-190, 241-262, 313-334).

### B31 · 36 words · ~12 s

> Use for when you know the count, and while when you do not. Take care: on modern graphics cards an infinite loop can freeze your application, the editor included, and Godot cannot protect you from it.

*Picture.* The real Godot 4.7 'Flow control' section in a browser window: the for and while snippets with their comments, and the paragraph below them about infinite loops. The camera pushes in on that paragraph and a terracotta ring marks the sentence about freezing the application, including the editor.

*Motion.* The camera drifts from the for and while snippets to the warning paragraph and rings it.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: a loop arrow that never ends

### B32 · 43 words · ~15 s

> Compare floats against a range, not with equals. Light U V dot X equal to exactly one half, and nothing draws here: no pixel center lands on it. A small range draws a thin line. The documentation warns float math varies by hardware.

*Picture.* Top: a schematic row of 12 outlined pixel cells with a dot at each cell center, an axis 0 to 1 and a vertical line at 0.5 that falls BETWEEN cells 6 and 7; the row is labelled 'schematic: 12 pixels'. Two code lines in monospace under it: `if (UV.x == 0.5)` and `if (abs(UV.x - 0.5) < 0.005)`, the second with a serif 32 label in the GLOSSARY wording, 'abs: drops the minus sign: -0.3 becomes 0.3'. A probe sweeps the row for the first test and no cell lights (label 'no pixel center is exactly 0.5'); for the second the two cells nearest 0.5 light teal. Bottom: two framed REAL renders side by side (lab_window of png/19-float-equals-1920.png, a pale field with nothing on it, and png/20-float-range-1920.png, the same field with a thin teal line), each captioned 'Godot 4.7.2 · Forward+ · 1920 pixels wide'.

*Motion.* A probe finds no cell exactly on one half; the range test lights the two nearest; the real renders confirm it.

*Lane.* manim · `B32_NoPixelLands` · runner-up: ShaderLab with the two renders

### B33 · 44 words · ~15 s

> Two performance notes from the documentation. Discard, which throws a pixel away, has a cost. Modern graphics cards handle an if well when every pixel takes the same path, but too many branches can slow a shader down. This film did not measure either.

*Picture.* A two-row table in the documentation's own words, each row ringed as it is spoken: 'discard (throws a pixel away)', 'it has a performance cost'; if, 'handled well when every pixel takes the same path; too many branches can slow a shader down'. The note line names the two documentation pages and says nothing here was measured.

*Motion.* The ring moves from the discard row to the if row as the voice moves on.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: BrowserCapture of the preprocessor page

## Act V: Read One Aloud

### B34 · 27 words · ~9 s

> Now read the file from the top. Use the same method: say the type of each piece, inside out, and check that every line's types fit together.

*Picture.* Act title 'Read One Aloud' (serif 40) top-left. The 14-line file alone on the stage, line numbers prominent (the next beats say 'line three', 'line six'). A focus box rests on line 1, then moves to line 3 where the reading will start.

*Motion.* The focus box leaves the header and settles on line three, ready to read.

*Lane.* remotion · `ShaderLab` · runner-up: LectureCodeTrace

### B35 · 44 words · ~15 s

> Line three is a uniform, a vec four, so a color. Source color is a hint: the editor treats the value as a color. With no default, it is black until something sets it. Line four is a float with a default of two.

*Picture.* Two lines in monospace (size 36), lines 3 and 4 of the file: `uniform vec4 tint : source_color;` and `uniform float speed = 2.0;`. Drawn tags land beneath their pieces: under `uniform` 'set from outside'; under `vec4` 'a color'; a bracket under `: source_color` labelled 'hint' with a small outlined round swatch and the label 'treated as a color'; a tag at the end of line 3 'no default: black'; under `float` 'a decimal number'; a bracket under `= 2.0` labelled 'default'. Serif 32 caption, in the GLOSSARY wording: 'hint: the word after a colon that tells Godot how to treat a uniform'.

*Motion.* Tags fly out to the pieces of line three, then to the pieces of line four, as each is read.

*Lane.* manim · `B35_ReadUniforms` · runner-up: ShaderLab with a label per cue

### B36 · 39 words · ~13 s

> Line six declares breathe. It hands back a vec three. It takes two arguments: a vec three called base, and a float called t. So the body gets a color and a number, and it must return a color.

*Picture.* Line 6 `vec3 breathe(vec3 base, float t) {` in monospace (size 36), centered. Drawn tags land beneath: `vec3` 'hands back a vec3'; `breathe` 'name'; `vec3 base` 'argument: vec3'; `float t` 'argument: float'. Below, a small three-cell token and a one-cell token flow into the parentheses and a three-cell token leaves, with the note 'the body must return a vec3'.

*Motion.* Tags land on the four pieces of the signature, then a token flows through.

*Lane.* manim · `B36_ReadSignature` · runner-up: ShaderLab with a label per cue

### B37 · 36 words · ~12 s

> Line seven. Sine of t is a float that swings between minus one and one. Half of that, plus a half, is still a float, now swinging between zero and one. It is stored in wave.

*Picture.* Line 7 `float wave = 0.5 + 0.5 * sin(t);` in monospace (size 36). Nested drawn brackets from the inside out with tags: `t` float; `sin(t)` float; `0.5 * sin(t)` float; `0.5 + 0.5 * sin(t)` float; into `wave` float. At the right (or below), a small drawn sine curve on axes marked -1 and 1, then squeezed and lifted to span 0 to 1, with a dot riding the curve.

*Motion.* Brackets widen outward with a float tag on each; a sine curve is squeezed from -1..1 into 0..1.

*Lane.* manim · `B37_ReadWave` · runner-up: LectureCodeTrace

### B38 · 40 words · ~14 s

> Line eight. Vec three of zero point nine fills all three parts: a pale gray. Mix blends that gray toward base by the amount wave. Zero gives the gray, one gives base. The result is a vec three, as promised.

*Picture.* Line 8 `return mix(vec3(0.9), base, wave);` in monospace (size 36). Tags: `vec3(0.9)` 'fills all three: a pale gray' with a small gray swatch; `base` 'vec3'; `wave` 'float: 0 to 1'; the whole `mix(...)` 'vec3'; `return` 'matches the signature'. A serif 32 label in the GLOSSARY wording, 'mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b'. Below, a horizontal ramp strip from pale gray (left) to teal (right) with a terracotta dot that rides from the gray end to the teal end as wave goes from 0 to 1, labelled '0 gives the gray, 1 gives base'.

*Motion.* A dot rides a gray-to-teal ramp as wave goes from zero to one while the tags land on the pieces.

*Lane.* manim · `B38_ReadReturn` · runner-up: ShaderLab with a label per cue

### B39 · 37 words · ~13 s

> In fragment, tint dot R G B is a vec three, and time times speed is a float. Breathe turns them into a vec three. Vec four adds tint's alpha, and color, a vec four, takes it.

*Picture.* Lines 12 and 13 in monospace (size 32): `vec3 color = breathe(tint.rgb, TIME * speed);` (45 characters) and `COLOR = vec4(color, tint.a);`. Tags land inside out: `tint.rgb` vec3 (swizzle); `TIME * speed` float; `breathe(...)` vec3; into `color` vec3; then `vec4(color, tint.a)` vec4 into `COLOR`, a vec4. Captions in serif 32: 'TIME: seconds on one clock shared by the whole game' and 'COLOR: the color of the pixel being drawn; fragment() sets it'.

*Motion.* Tags land inside out on line twelve, then on line thirteen, ending on COLOR.

*Lane.* manim · `B39_ReadFragment` · runner-up: ShaderLab with a label per cue

### B40 · 34 words · ~12 s

> Now watch it run. Pale gray blends to teal and back, and speed sets how fast. Every piece has a type, and every type fits. That is what it means to read a shader.

*Picture.* The same file and the same pulsing render as the opening picture, side by side. The wave and mix lines light first, then the two fragment lines.

*Motion.* The pulse keeps running while the lines that make it light up.

*Lane.* capture · `ShaderLab` · runner-up: manim: the file with all tags at once

*Capture to record.* C01b: the same capture as C01a (same shader, same --set tint=#5FA391, live TIME) as a separate clip, with its OWN --time-origin chosen from THIS beat's measured audio by the same rule (for 11.6 s, t0 about 2.38 s gives 0.20 at both sample times).

### B41 · 34 words · ~12 s

> Now change one thing. Make tint a vec three, and keep reading its alpha. A vec three has no alpha, and Godot says invalid member. Reading by types catches that before you run it.

*Picture.* A terminal window with the engine's own log of lab-shaders/57-err-alpha-on-vec3.gdshader (the same file with the uniform changed to `vec3 tint`), word for word: the source lines around `COLOR = vec4(color, tint.a);` with that line marked, then 'Invalid member for 'vec3' expression: '.a'.' A ring lands on the message.

*Motion.* The log lands line by line; a ring settles on the message about the missing member.

*Lane.* terminal · `CCPlainShell` · runner-up: ShaderLab with the changed file

## Closing

### BVDT · recap · 73 words · ~25 s

> Let's recap with Claude. A shader file has a header, globals and functions. Every value has a type, and Godot will not quietly convert between int and float. Many values are vectors, and arithmetic works on every part at once. A function has a signature, and per-pixel built-ins must be passed in. Choices need a bool, and floats are compared against a range. To read a line, say the type of each piece.

*Picture.* The recap card: A shader file has a header, globals and functions. / Every value has a type, and Godot will not quietly convert between int and float. / Many values are vectors, and arithmetic works on every part at once. / A function has a signature, and per-pixel built-ins must be passed in. / Choices need a bool, and floats are compared against a range. / To read a line, say the type of each piece.

### BHTF · your turn · 86 words · ~29 s

> Your turn. Paste this into Claude: Go through the Godot canvas item shader below one line at a time. After each line, add a comment giving the type of each piece. Flag any line where two types do not match. Then say in one sentence what it draws. Put your own shader under it. Now check two things yourself. Pick one line and say the type of each piece before you read Claude's answer. And run the shader: does it draw what Claude's one sentence says?

*Prompt shown and read in full:* Go through the Godot canvas item shader below one line at a time. After each line, add a comment giving the type of each piece. Flag any line where two types do not match. Then say in one sentence what it draws.

*Two checks:* Check: pick one line and say the type of each piece yourself before you read Claude's. · Check: run the shader. Does it draw what Claude's one sentence says?

### BOUT · outro · 7 words · ~4 s

> Godot Shader Language. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


# Script: Godot Shaders

**What this is.** The words Liam will say in *Godot Shaders*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 49 beats, 1859 words, about **10:36** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: manim 18, capture 17, remotion 6, editor 2.

**If it runs long.** Cut, in this order: the budget-bars beat (B05), then the typo beat (B32), the editor-slider beat (B27) and the tween beat (B33): each repeats an idea another beat already carries. The vertex-lean pair (B16, B17), the discard beat (B20) and the iris build (B42, B43) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | One Pixel, All at Once | 8 | 303 | ~1:43 |
| II | Setting Up a Shader | 6 | 242 | ~1:22 |
| III | The Three Functions | 10 | 354 | ~2:00 |
| IV | Dials: Uniforms | 9 | 319 | ~1:48 |
| V | Where Am I, and When? | 10 | 359 | ~2:02 |

## Opening

### BOPEN · identity card · 25 words · ~8 s

> Godot Shaders. Learn what a shader is, the words you will meet along the way, and how to write one that your game can control.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Godot Shaders", and the line "What a shader is, and how to give one a dial".

### BIDEA · the question · 49 words · ~17 s

> Hallo. This is Liam, in for Bear. Most people meet a shader as a strange file of math. One idea makes it readable. A shader does not paint the whole screen. It decides the color of one pixel, and the graphics card asks it about every pixel at once.

*Picture.* The hesitant writer types: "A shader decides the color of
the whole screen." then deletes "the whole screen" and types "one pixel".

### BDEFS · terms · 52 words · ~18 s

> Five terms. The G P U is the graphics chip: many small workers running at once. A pixel is one dot of the picture. A vertex is a corner point of a shape. A texture is an image a shader can read. And a material tells Godot how to draw a surface.

*Picture.* "Terms In This Lecture": **GPU** — the graphics chip: many small workers running at once; **Pixel** — one dot of the picture on screen; **Vertex** — a corner point of a shape; **Texture** — an image a shader can read by address; **Material** — the resource that tells Godot how to draw a surface; it holds the shader

## Act I: One Pixel, All at Once

### B01 · 32 words · ~11 s

> A game can work and still look flat. Same sprite, same background, nothing broken. A shader is the part that decides how it looks: the wobble, the glow, the water, the outline.

*Picture.* Act title 'One Pixel, All at Once' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite sits flat and still for two seconds, then a shader is switched on and it wobbles. Label: 'same scene, shader switched on'.

*Motion.* The sprite is still, then comes alive the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a flat versus lively sprite

*Capture to record.* C01: Lab sprite scene (teal test sprite, scale to fit), shader lab-shaders/02-hook-wobble.gdshader assigned at t=2.0 s (--material-at 2.0), 10 s, 30 fps, Forward+, no input.

### B02 · 38 words · ~13 s

> A shader is a small program that runs on the graphics card, the G P U. It decides how something is drawn. Your game code decides what exists, and where. The shader decides what each part looks like.

*Picture.* Two boxes on the cream stage. Left, 'your game code · CPU' with a small teal sprite icon and the words 'what exists, where'. Right, 'the shader · GPU' with the same icon, now with a wobble drawn around it, and 'how each part looks'. One arrow, left to right.

*Motion.* The sprite icon is placed on the left, travels along the arrow and arrives restyled on the right.

*Lane.* manim · `B02_WhatAndWhere` · runner-up: DesignPipelineClaim, show-tell isometric

### B03 · 43 words · ~15 s

> Why a second chip? The C P U is a few fast workers, doing one job after another. The G P U is a crowd of small workers, all doing the same job at once. A picture is millions of identical little jobs.

*Picture.* A 12-by-6 grid of outline cells. Top: one dot-worker colours the cells one after another, a counter ticking. Bottom: a crowd of dots colours all 72 cells in the same instant. Labels: 'CPU: one job after another', 'GPU: the same job at once'.

*Motion.* One worker sweeps the grid cell by cell while the whole second grid fills at once.

*Lane.* manim · `B03_ManyWorkers` · runner-up: isometric workers on a conveyor (show-tell)

### B04 · 36 words · ~12 s

> Here is the slow way. A G D script loop colors every pixel of a full H D picture, one at a time. That is over two million calls, for one picture. Watch what it costs.

*Picture.* The real loop from evidence/planning-checks/verify.gd on a cream code card, with the call count underneath.

*Motion.* Line focus steps down the loop as it is described; the count lands last.

*Lane.* remotion · `LectureCodeTrace` · runner-up: CCPlainShell

### B05 · 39 words · ~13 s

> On this Mac, that loop took about fifty-five milliseconds. A game running at sixty frames per second has sixteen and a half milliseconds for everything. This is one gradient, and it is more than three times the whole budget.

*Picture.* A horizontal time axis from 0 to 60 ms. A vertical budget line at 16.7 ms labelled 'one frame at 60 per second'. A bar grows along the axis, passes the line and stops at about 55, labelled 'the loop · about 55 ms'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · five runs: 52 to 58 ms'.

*Motion.* The bar grows past the budget line and keeps going.

*Lane.* manim · `B05_FrameBudget` · runner-up: LectureEvidenceTable

### B06 · 36 words · ~12 s

> The shader way describes one pixel. This line says: the red amount is how far across the shape this pixel sits. Nothing loops. The graphics card runs the line for every pixel, and the gradient appears.

*Picture.* Code card with the four-line shader at left; at right a real Godot window showing a black-to-red gradient with a thin 0 to 1 ramp under it.

*Motion.* The line is highlighted, then the red ramp is traced left to right under the gradient.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: Lab rect, lab-shaders/01-gradient.gdshader, still PNG 1920x1080 (probes: 0.0196 / 0.498 / 0.9804 at x = 0.02 / 0.5 / 0.98).

### B07 · 44 words · ~15 s

> Drawing that same gradient this way cost the processor about four hundredths of a millisecond, only to hand over the job. The graphics card did the pixels. Its own time could not be read on this setup, so there is no number for it.

*Picture.* 'game code · CPU' box at left, 'shader · GPU' box at right. An arrow between them labelled 'hands over the job · about 0.04 ms'. Under the GPU box, in grey: 'its own time: not readable on this setup'. Small credit: 'Apple M4 Pro · Godot 4.7.2'.

*Motion.* A tiny package travels the arrow; the GPU box fills with pixels while the CPU box stays nearly empty.

*Lane.* manim · `B07_HandOver` · runner-up: LectureEvidenceTable, two rows

### B08 · 35 words · ~12 s

> So a shader flips the question. Not: for each pixel, do this. Instead: write down what one pixel should do, and let the card do it everywhere. A shader decides the color of one pixel.

*Picture.* A 16-by-9 pixel grid of outline cells. One cell gets a terracotta ring and a small code card beside it ('COLOR = …'). Then every cell takes its ramp color at once, left to right, the card staying put. Label: 'one pixel's rule → every pixel'.

*Motion.* One ringed pixel, then the whole grid changes in the same instant.

*Lane.* manim · `B08_OnePixelThenAll` · runner-up: ShaderLab

## Act II: Setting Up a Shader

### B09 · 30 words · ~10 s

> Where does a shader live? In a file. You attach it to a node through a material. The node holds a Shader Material, and the Shader Material holds your shader.

*Picture.* Act title 'Setting Up a Shader' (serif 40) top-left. Three boxes slide in left to right and link: 'a node (Sprite2D, ColorRect…)' → 'ShaderMaterial' → 'your shader (.gdshader file)'. A small dot travels from the shader back to the node.

*Motion.* Each box slides in as it is named; the dot travels back to the node, meaning 'look'.

*Lane.* manim · `B09_ThreeBoxes` · runner-up: DesignPipelineClaim, show-tell isometric

### B10 · 47 words · ~16 s

> In the editor, that is a few clicks. In the node's Material slot, choose Shader Material under New. Click it, and in its Shader slot choose New Shader. Set the mode to Canvas Item, since it starts on Spatial, and create it. Godot opens the shader editor.

*Picture.* Four real frames of the Godot editor's Inspector for a Sprite2D, one per state: Material empty; ShaderMaterial added; a Shader added; the shader editor open. Slow cross-dissolves between them; a terracotta ring on the slot being named.

*Motion.* The ring moves slot to slot as the voice names each click.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction)

*Capture to record.* E1: four real editor states recorded by the editor driver (editor-capture/README.md): Material empty; Shader Material in the slot (menu: heading New, then ShaderMaterial); a Shader added (New Shader..., Create Shader dialog, mode Canvas Item); the shader editor open in the bottom panel. Scripted editor session; the clicks themselves are not shown.

### B11 · 48 words · ~16 s

> What you type there is Godot's own shader language. It is similar to a standard one called G L S L, but simpler. If you can read a few lines of G D script, you can read it. It is strict about types, and statements end in semicolons.

*Picture.* The real Godot 4.7 shading-language page in a browser window; the camera pushes in on the sentence that says it is similar to GLSL ES 3.0 and a terracotta ring marks it.

*Motion.* The camera pushes in on the sentence the voice is describing.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: GDScript line beside a shader line

### B12 · 46 words · ~16 s

> The first line of every shader says what it is for. Canvas item is for two-D drawing and interface. Spatial is for three-D. Particles, sky and fog are for those. This film uses canvas item. The ideas carry over to three-D with a few different names.

*Picture.* Left: the line `shader_type canvas_item;` over a flat teal sprite icon. Right: `shader_type spatial;` over a small isometric cube. Three small tiles fade in underneath: particles, sky, fog.

*Motion.* The two first lines type in, each over its picture, then the three small tiles arrive.

*Lane.* manim · `B12_TwoWorlds` · runner-up: LectureEvidenceTable

### B13 · 36 words · ~12 s

> The smallest working shader has one function and one line. In the function called fragment, set color to four numbers: red, green, blue, and how visible it is. One, zero, zero, one: pure red, fully visible.

*Picture.* Code card with the five-line shader at left; a real Godot window filled with pure red at right.

*Motion.* The function line then the COLOR line are highlighted; the window is red the whole time.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C03: Lab rect, lab-shaders/03-red.gdshader, still (probe 0.5,0.5 = 1.0, 0.0, 0.0).

### B14 · 35 words · ~12 s

> A shader can have up to three special functions, and the engine calls them for you: vertex, fragment and light. You write what each one does. Godot decides when it runs, and how many times.

*Picture.* A cream code card with the three empty function bodies (ten lines); focus lands on vertex, then fragment, then light as each is named.

*Motion.* Focus steps down the three functions on their names.

*Lane.* remotion · `LectureCodeTrace` · runner-up: manim

## Act III: The Three Functions

### B15 · 30 words · ~10 s

> Vertex runs once for each vertex, each corner point of the shape. A plain rectangle has four corners, so vertex runs four times. Its job is to place the corners.

*Picture.* Act title 'The Three Functions' (serif 40) top-left. A rectangle with four terracotta corner dots, each labelled in turn 'vertex() runs' with a counter 1, 2, 3, 4. Caption: 'its job: place the corners'.

*Motion.* The four corners flash one after another and the counter ticks.

*Lane.* manim · `B15_FourCorners` · runner-up: ShaderLab

### B16 · 34 words · ~12 s

> A real run. This vertex pushes the bottom two corners fifty pixels to the right and leaves the top two alone. The whole picture leans, because the card fills in everything between the corners.

*Picture.* Code card at left; at right a real Godot window with a teal-and-cream checker square (128 px) that, at 1 s, leans: the bottom edge slides 50 px right while the top stays. A terracotta ring on the bottom edge, a readout '+50 px'.

*Motion.* The square shears sideways the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C03b: Lab sprite, checker 128 px at scale 1.0 (--sprite-scale 1.0), lab-shaders/04-lean.gdshader assigned at 1.0 s; measured edge shift 50 px (evidence/planning-checks/lean-edge.txt, white-square render).

### B17 · 40 words · ~14 s

> Between the corners, you calculate nothing. The left edge slides evenly from top to bottom: fifty pixels over a hundred and twenty-eight rows. That is why vertex alone cannot ripple a plain rectangle. Four corners can only make straight edges.

*Picture.* The leaning square's left edge drawn as a slanted line with five sample dots at 2, 25, 50, 75 and 98 percent of the height, labelled with the real measured shifts +1, +12, +25, +37, +49 px. A caption: 'four corners → straight edges'.

*Motion.* The five dots land one after another down the edge, each with its measured number, evenly spaced.

*Lane.* manim · `B17_EvenSteps` · runner-up: ShaderLab with readouts

### B18 · 39 words · ~13 s

> Fragment runs after the corners are placed. It runs once for each pixel the shape covers, and its job is to set that pixel's color. The shape is already decided. Now the card asks about every pixel inside it.

*Picture.* A pixel grid with the rectangle drawn over it. The covered cells tint one by one, each carrying a tiny 'fragment()' tag; then all covered cells hold their tint at once while the tags stay.

*Motion.* Covered cells tint one by one, then the whole shape is filled.

*Lane.* manim · `B18_FillIn` · runner-up: ShaderLab

### B19 · 39 words · ~13 s

> You will hear this called a pixel shader, or a fragment shader. Same job, two names. Microsoft's Direct three D says pixel. OpenGL, Vulkan and Godot say fragment. The careful word is fragment, because a fragment is a pixel-to-be.

*Picture.* Two labels, 'pixel shader' and 'fragment shader', point to one box. Then a strip: 'fragment' → 'tests, blending' → 'pixel', with the caption 'a fragment is a pixel-to-be'. No company names or logos on screen; the voice names the graphics systems.

*Motion.* Both labels slide into the same box, then a fragment travels through the strip and becomes a pixel.

*Lane.* manim · `B19_TwoNames` · runner-up: LectureEvidenceTable

### B20 · 36 words · ~12 s

> It is only a pixel-to-be because it can still be thrown away, or blended with others. This shader says discard for the right half. Fragment ran there. No pixel came out, and the background shows through.

*Picture.* Code card at left with the discard lines; at right a real Godot window: the left half a green-orange gradient, the right half the plain stage color, as if the shape were cut in half.

*Motion.* The discard lines are highlighted and a ring settles on the empty right half.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C04: Lab rect, lab-shaders/05-discard-half.gdshader, still (probes: left colored; right = stage color 0.851, 0.835, 0.792).

### B21 · 40 words · ~14 s

> The third function, light, runs once for each light that touches a pixel. Two lights, two runs, and the results add. If you write light, it replaces Godot's default lighting, even when it is empty. Here we only name it.

*Picture.* Code card at left (a light() that outputs a constant 0.2 red); at right a real Godot window on a dark canvas: a square gets brighter in steps as a white light is added at 1 s, 2.5 s and 4 s. Readouts '1 light · 0.2', '2 lights · 0.4', '3 lights · 0.6'.

*Motion.* The square steps up in brightness each time a light appears.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C05: custom scene from evidence/planning-checks/verify4.gd: CanvasModulate black, white Sprite2D with 13-light-count.gdshader, PointLight2D added at 1.0, 2.5, 4.0 s; 6 s; Forward+. Measured 0.2 / 0.4 / 0.6; empty light() -> black (0.0), no light() -> white (1.0).

### B22 · 29 words · ~10 s

> So the order of work is fixed. First vertex places the corners. Then the card fills in the shape. Then fragment colors each pixel. Information flows one way: forward.

*Picture.* A three-stage strip left to right: 'vertex() places the corners' → 'the GPU fills the shape' → 'fragment() colors each pixel'. A token travels the strip; the arrows are drawn shapes pointing only forward.

*Motion.* A token passes through the three stages in order and never goes back.

*Lane.* manim · `B22_Order` · runner-up: DesignPipelineClaim, show-tell isometric

### B23 · 38 words · ~13 s

> Inside these functions the engine hands you values, called built-ins, written in capital letters. Some come in, like a pixel's address and the time. One goes out: the color you set. Which ones exist depends on the function.

*Picture.* A box labelled 'fragment()'. Arrows come in from the left labelled UV, TIME, TEXTURE (capital letters, in a monospace face) and one arrow goes out to the right labelled COLOR. Caption: 'built-ins · capital letters'.

*Motion.* The inputs slide into the box one by one and the single output leaves on the right.

*Lane.* manim · `B23_FunctionBox` · runner-up: LectureEvidenceTable

### B24 · 29 words · ~10 s

> So far: vertex runs once per corner and places things. Fragment runs once per pixel and colors things. Light runs once per pixel, for each light, and lights things.

*Picture.* A three-row table, one row ringed as each function is named.

*Motion.* The ring moves down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

## Act IV: Dials: Uniforms

### B25 · 40 words · ~14 s

> A shader that always draws the same red is not much use. Your game needs to say: more red now, less red later. But the shader lives on the graphics card, out of reach. How do you talk to it?

*Picture.* Act title 'Dials: Uniforms' (serif 40) top-left. 'your game · GDScript' box at left, 'the shader · GPU' box at right with a pane of glass between them. A terracotta question dot hovers at the glass.

*Motion.* A message dot leaves the game box, stops at the glass and bounces.

*Lane.* manim · `B25_OutOfReach` · runner-up: LectureCodeTrace

### B26 · 38 words · ~13 s

> With a uniform. A uniform is a value you declare outside the functions, and set from outside the shader. Here is one called red, from zero to one. The shader reads it. The shader can never change it.

*Picture.* Code card at left with the uniform line highlighted, then the line that uses it; at right a real Godot window colored by red = 0.5.

*Motion.* Focus lands on the uniform line, then on the line that reads it.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C06a: Lab rect, lab-shaders/06-dial.gdshader at the default (probe 0.502, 0.451, 0.451).

### B27 · 29 words · ~10 s

> In the editor, that line becomes a slider. In the Inspector, under Shader Parameters, there is a control labelled Red. Drag it, and the picture changes while you watch.

*Picture.* Three real frames of the Inspector's Shader Parameters group with the red slider at 0.2, 0.5 and 0.9, and the sprite beside it in the matching color. Readouts show the value.

*Motion.* The slider knob and the color step through the three real states.

*Lane.* editor · `ShaderLab` · runner-up: ShaderLab video of the Lab render with the same values

*Capture to record.* E2: three static editor frames of a scratch project with shader_parameter/red saved at 0.2, 0.5, 0.9 in the scene file; Inspector scrolled to the Material's Shader Parameters group. The 'Shader Parameters' group name is confirmed by this capture.

### B28 · 23 words · ~8 s

> Three uniforms make a color mixer. Red, green, blue, each its own slider. The shader puts the three numbers together into a color.

*Picture.* Code card at left (three uniforms, one COLOR line); at right a real Godot window whose color moves as red, then green, then blue sweep from 0 to 1.

*Motion.* Three sweeps in turn, each changing the color.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C07: Lab rect, lab-shaders/07-mixer.gdshader; red 0 to 1 over 0-2 s, green 0 to 1 over 2-4 s, blue 0 to 1 over 4-6 s (--animate sequence); 6 s, 30 fps. Probe at (1.0, 0.5, 0.0) = (1.0, 0.502, 0.0).

### B29 · 41 words · ~14 s

> The part after the colon is a hint. It tells the editor how to show the uniform. A range adds a slider bar. Source color gives a color swatch that opens a picker. A hint shapes the editor, not the math.

*Picture.* A two-row table pairing each hint with the widget it makes.

*Motion.* Each row lands on its words.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: editor frames

### B30 · 35 words · ~12 s

> A hint does not clamp. If your game code sets the value to seven, the shader receives seven. The slider only guards the editor. If a range matters, enforce it in your code as well.

*Picture.* A slider track from 0 to 1 with a knob. A code line sets 7.0. An arrow shoots past the end of the track to a label 'stored: 7.0'. Caption: 'the slider only guards the editor'.

*Motion.* The value arrow overshoots the end of the track and lands on 7.0.

*Lane.* manim · `B30_NoClamp` · runner-up: ShaderLab

### B31 · 34 words · ~12 s

> From the game, you set a uniform with set shader parameter. Get the node's material, then pass the uniform's name and a value. The name is case-sensitive, and it must match the shader exactly.

*Picture.* A one-line GDScript card at left; at right a real Godot window that changes color from red = 0.5 to red = 0.9 at the moment the call fires.

*Motion.* The color jumps when the highlighted call fires.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace

*Capture to record.* C09: scene with a ColorRect named Rect (06-dial.gdshader); at t=1.0 s a script runs `$Rect.material.set_shader_parameter("red", 0.9)`; 3 s; Forward+.

### B32 · 38 words · ~13 s

> Get the name wrong, and nothing happens. No error. The value is stored as an unused parameter, the real uniform keeps its default, and the effect never appears. When a shader ignores your game, check the spelling first.

*Picture.* A two-line GDScript card (the typo `rd`, then the correct `red`); at right a real Godot window that does not change after the first line and changes after the second. Readouts: 'no change · no error', then 'now it changes'.

*Motion.* Nothing happens on the typo; the color moves on the correct name.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace

*Capture to record.* C10: same scene as C09; at 1.0 s set_shader_parameter("rd", 0.9) (no change), at 2.2 s set_shader_parameter("red", 0.9) (changes); 3.5 s. Verified: red stays 0.2 after the typo; 0.898 after the correct name; no error in the log.

### B33 · 41 words · ~14 s

> You can animate a uniform too. Set its starting value from code, then tween it, and the shader follows, every frame. Skip the first step and the tween has nothing to start from. That is how a shader answers to gameplay.

*Picture.* A three-line GDScript card (set the start value, create the tween, tween the property); at right a real Godot window whose color sweeps smoothly from red = 0 to red = 1 over two seconds.

*Motion.* The color sweeps while the tween lines are highlighted.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C11: scene as C09; set_shader_parameter("red", 0.0) first, then tween_property(material, "shader_parameter/red", 1.0, 2.0); 3 s. Verified start 0.0, mid 0.49 at 0.25 s, end 1.0 (verify3.gd H). A tween on a uniform never set from code fails: 'property does not exist' (run-5a, kept).

## Act V: Where Am I, and When?

### B34 · 38 words · ~13 s

> A uniform is one value, the same for every pixel in the draw. Some inputs must differ, because each pixel needs to know where it is. The engine hands those in, and they are different for every pixel.

*Picture.* Act title 'Where Am I, and When?' (serif 40) top-left. Left panel: a dial with lines running to every cell of a small pixel grid, each cell showing the same number 0.5. Right panel: the same grid where each cell shows its own two numbers (u, v). Captions: 'uniform: the same everywhere', 'address: different for each'.

*Motion.* The dial's lines fan out to every cell, then the second grid fills with a different pair per cell.

*Lane.* manim · `B34_SameForAll` · runner-up: LectureEvidenceTable

### B35 · 38 words · ~13 s

> Two kinds of input, then. A uniform is set by you. A built-in is set by the engine. Both are names the shader can read, and some built-ins, like the time, are the same for every pixel too.

*Picture.* A three-row table with the answer column ringed as each row is named.

*Motion.* The ring steps down the rows.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

### B36 · 38 words · ~13 s

> Now, the pixel's address. U V runs from zero to one across the shape, and zero to one down. The top left is zero, zero. The bottom right is one, one. In two-D, the second number counts downward.

*Picture.* A square with a 0 to 1 axis along the top and down the left side, the second axis pointing DOWN. A terracotta dot moves across it with a live label (u, v), passing (0.25, 0.75) and ending near (1, 1). Corner labels (0, 0) and (1, 1).

*Motion.* The dot moves to several positions and its (u, v) label updates each time.

*Lane.* manim · `B36_Address` · runner-up: ShaderLab

### B37 · 35 words · ~12 s

> Use the address as a color. Red is how far across. Green is how far down. Left to right, red grows. Top to bottom, green grows. The corners give it away: black, red, green, yellow.

*Picture.* Code card at left; at right a real Godot window showing the red-green UV picture; corner labels land in turn: black (top left), red (top right), green (bottom left), yellow (bottom right).

*Motion.* Corner labels land in the order the voice says the colors.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C12: Lab rect, lab-shaders/08-uv-colors.gdshader, still; corner probes 0.0196/0.0196/0 (black), 0.98/0.02/0 (red), 0.02/0.98/0 (green), 0.98/0.98/0 (yellow).

### B38 · 29 words · ~10 s

> Use it as a fade instead. Multiply the alpha by the horizontal address. The left edge is invisible, the right edge solid. One line, no loop, no second image.

*Picture.* Code card at left; at right a real Godot window with a cream square that fades from invisible at its left edge to solid at its right edge over the stage color.

*Motion.* The COLOR.a line is highlighted and a 0 to 1 ramp is traced under the fade.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C13: Lab sprite, white 128 px texture (--sprite-tex white), lab-shaders/09-uv-fade.gdshader, still; probes 0.851 (bg) / 0.859 / 0.992.

### B39 · 35 words · ~12 s

> Now time. Time counts up in seconds. Put it inside a sine and you get a smooth back and forth, between minus one and one. Scale that to zero to one, and the color breathes.

*Picture.* Code card at left; at right a real Godot window pulsing between red-orange and yellow-orange, with a 0 to 1 ramp whose marker rides the pulse value.

*Motion.* The pulse and the ramp marker move together, back and forth.

*Lane.* capture · `ShaderLab` · runner-up: manim sine plot

*Capture to record.* C14: Lab rect, lab-shaders/10-pulse.gdshader, 4 s at 30 fps; probes at two times differ (0.6863 and 0.9882 in the green channel).

### B40 · 35 words · ~12 s

> One catch. Time is not the age of your node. It is one clock for the whole game, started with the engine. Add a node three seconds in, and it already sees three seconds gone.

*Picture.* Two real Godot panels side by side, each a bar that fills from the bottom as time passes: the left present from the start, the right added at 3 s. The instant the right one appears it is already filled to the same height as the left. Readouts: 'present from the start', 'added at 3 s', 'both: 3 s'.

*Motion.* The late bar appears already as full as the early one.

*Lane.* capture · `ShaderLab` · runner-up: manim timeline

*Capture to record.* C15: scene with two ColorRects (left on the start, right added at 3.0 s), both using lab-shaders/11-time-bar.gdshader, 6 s; verified earlier with 32 stripes: both read 12 quarter-seconds (3.0 s) when the late node had existed for two frames (verify2.gd A2).

### B41 · 37 words · ~13 s

> So for a one-time effect, a fade-in, or a reveal that starts when something happens, do not lean on time. Use a uniform, and let your game drive it from zero to one when the moment comes.

*Picture.* A horizontal timeline: the game's clock runs from 0 and keeps going (a long grey bar). A terracotta marker 'something happens' sits at about 3. Below, a second short bar 'progress, 0 to 1' starts exactly at the marker and rises to 1. Labels: 'the clock never restarts', 'a uniform you drive'.

*Motion.* The clock bar runs on; at the event marker the progress bar starts from zero.

*Lane.* manim · `B41_ClockVsDial` · runner-up: ShaderLab

### B42 · 37 words · ~13 s

> Put it together: a circle that opens from the middle. For each pixel, measure the distance to the middle of the shape. If it is more than the radius, discard the pixel. The radius is a uniform.

*Picture.* Code card at left (the uniform, the distance test, discard, the texture line); at right a real Godot window where a checker square opens from a circle in the middle as radius sweeps from 0 to 0.8.

*Motion.* The circle grows outward while the code lines light up in order.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C16: Lab sprite, checker 128 px (--sprite-tex checker) at fit scale, lab-shaders/12-iris.gdshader; radius 0.0 to 0.8 over 3 s; probes: radius 0.0 -> centre = stage; 0.3 -> centre cream; 0.8 -> everything visible.

### B43 · 37 words · ~13 s

> Now drive it from the game. When the player presses a key, tween the radius from zero to point eight, and the picture opens like an iris. The shader holds the rule. The game holds the moment.

*Picture.* A seven-line GDScript card at left (set the radius to 0 in _ready, then a key handler that tweens it to 0.8); at right the same iris scene: nothing until a (scripted) key press at 1 s, then the picture opens over 1.5 s. A label 'scripted input' is always on screen.

*Motion.* The picture opens only after the key press.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with the earlier capture

*Capture to record.* C17: iris scene (C16) with this exact script on the scene root; the capture harness sends one physical-key event at t=1.0 s (logged); 4 s; label scripted input. Verified in verify5.gd run 5b: centre goes from the stage color to the sprite color after the key. Run 5a (no _ready line) failed and is kept.

## Closing

### BVDT · recap · 69 words · ~24 s

> Let's recap with Claude. A shader decides the color of one pixel, and the card runs it for every pixel. A shader lives in a file, on a material, on a node. Vertex places the corners, fragment colors the pixels, light lights them. A uniform is a dial your game sets, the same for every pixel. The address says where a pixel is. Time is one clock for everyone.

*Picture.* The recap card: A shader decides the color of one pixel, and the card runs it for every pixel. / A shader lives in a file, on a material, on a node. / Vertex places the corners, fragment colors the pixels, light lights them. / A uniform is a dial your game sets, the same for every pixel. / The address says where a pixel is. / Time is one clock for everyone.

### BHTF · your turn · 81 words · ~28 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a Color Rect. One float uniform called fill, with a hint range from zero to one. The left part of the rectangle, as wide as fill, is red. The rest is transparent. Then point me to the three lines I should check. Then check two things yourself. Does the Inspector show a Fill control with a slider bar? And at point five, is exactly half the rectangle red?

*Prompt shown and read in full:* Write a Godot canvas item shader for a Color Rect. One float uniform called fill, with a hint range from zero to one. The left part of the rectangle, as wide as fill, is red. The rest is transparent. Then point me to the three lines I should check.

*Two checks:* Check: the Inspector shows a Fill control with a slider bar. · Check: at fill point five, exactly half the rectangle is red.

### BOUT · outro · 6 words · ~4 s

> Godot Shaders. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


# Script: Vertex Shaders

**What this is.** The words Liam will say in *Vertex Shaders*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 46 beats, 1721 words, about **9:49** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 27, manim 12, terminal 1.

**If it runs long.** Cut, in this order: the color-shortcut beat (B33), the flat beat (B30), the wind beat (B25), the polygon-needs-a-texture beat (B38) and the upside-down beat (B35): each repeats a lesson another beat already carries or is a trap rather than the main line. The four-corner tilt (B12), the pair (B17), the travelling and pinned flag (B21, B22) and the lit flag (B32) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Corners | 10 | 349 | ~1:59 |
| II | More Corners | 10 | 352 | ~2:00 |
| III | A Waving Flag | 6 | 205 | ~1:10 |
| IV | Passing Data Forward | 8 | 297 | ~1:41 |
| V | When It Looks Wrong | 6 | 207 | ~1:10 |

## Opening

### BOPEN · identity card · 32 words · ~11 s

> Vertex Shaders. Learn how a shader moves the corner points of a shape, and how to give a shape enough corners to bend. By the end you can build a waving flag.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Vertex Shaders", and the line "How a shader moves corners to bend a shape".

### BIDEA · the question · 45 words · ~15 s

> Hallo. This is Liam, in for Bear. A waving flag looks as if thousands of pixels are moving. They are not. A vertex shader does not change pixels. It moves the corner points of a shape, and the graphics card fills in everything between them.

*Picture.* The hesitant writer types: "A vertex shader
changes pixels." then deletes "changes pixels" and types "moves corners".

### BDEFS · terms · 56 words · ~19 s

> Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. A vertex is a corner point of a shape. A polygon is a shape made of straight edges between points. To interpolate is to blend smoothly between two known values.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Pixel** — one dot of the picture on screen; **Vertex** — a corner point of a shape; **Polygon** — a shape made of straight edges between points; **Interpolate** — blend smoothly between two known values

## Act I: Corners

### B01 · 39 words · ~13 s

> This flag is waving, and not one pixel in it was told to move. One line of code moves its corner points, and the graphics card fills in everything between them. That line lives in a function called vertex.

*Picture.* Act title 'Corners' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a cream and teal checker flag pinned to a grey pole waves smoothly with its folds lit, in a seamless loop. Label: 'live clock'.

*Motion.* The flag is already waving on the first frame: the ripple travels along it while the pole end stays still.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a waving flag

*Capture to record.* C01: scene `final` of evidence/planning-checks/scratch-project/capture_scenes.gd: a MeshInstance2D with a QuadMesh 384 x 168 cut 31 x 7 (297 vertices), cream and teal checker texture of 16 x 7 cells, a grey pole beside the left edge, shader lab-shaders/11-flag-final.gdshader from the first frame; canvas 1280 x 720; record 252 frames (8.4 s: four wave periods at speed 3, so the loop seam is under 1 % of a period out), 30 fps, Forward+, no input.

### B02 · 27 words · ~9 s

> A shape is built from corner points, its vertices. The engine calls vertex once for each one, and asks a single question: where does this corner go?

*Picture.* A rectangle on the cream stage with a terracotta dot on each corner. The dots flash one after another, each with a counter 1, 2, 3, 4 and a small 'where?' tag; then the four dots slide to new places and the rectangle follows as a leaning parallelogram. Caption in the GLOSSARY wording: 'vertex(): runs once for each vertex; places the corners'.

*Motion.* Each corner flashes in turn with its count, then the shape follows the four moved corners.

*Lane.* manim · `B02_FourCorners` · runner-up: ShaderLab with a Lab render

### B03 · 34 words · ~12 s

> The engine hands you the corner's position in a built-in, a value it gives your function. Its name is vertex too, in capital letters. Whatever you leave in it is where the corner goes.

*Picture.* A box labelled vertex(). A terracotta dot labelled VERTEX (monospace) arrives from the left at the corner (-64, -64), passes through the box where the line `VERTEX.x += 40.0;` is shown, and leaves on the right at (-24, -64). Caption in the GLOSSARY wording: 'built-in: a value the engine hands to a function'.

*Motion.* The dot goes in, the line acts on it, and a moved dot comes out the other side.

*Lane.* manim · `B03_InAndOut` · runner-up: LectureCodeTrace with the line highlighted

### B04 · 37 words · ~13 s

> It counts in pixels, from the middle of the sprite. A sprite one hundred twenty-eight pixels wide has corners at minus sixty-four and sixty-four. The y axis points down, so the top corners are the minus ones.

*Picture.* A 128 by 128 square with a small cross at its middle and two axis arrows drawn as shapes: x to the right, y pointing DOWN. The four corners get labels in turn: (-64, -64) top left, (64, -64) top right, (-64, 64) bottom left, (64, 64) bottom right; a scale bar '128 px'. Small grey credit: 'measured in Godot 4.7.2 · Forward+'.

*Motion.* Corner labels land one by one; the y arrow points down and the top corners carry the minus sign.

*Lane.* manim · `B04_PixelsFromTheMiddle` · runner-up: ShaderLab: Lab render coloured by VERTEX

### B05 · 36 words · ~12 s

> Change the number, and the corner moves. Add forty to x, and every corner moves forty pixels to the right. The whole square slides, because the graphics card fills in the shape between the moved corners.

*Picture.* Code card at left with the one line `VERTEX.x += 40.0;` highlighted; at right a real Godot window (640 by 360): the 128 px checker square sits still, then jumps 40 px to the right as the voice says 'add forty to x' (the shader switches on at 22 % of the beat). A terracotta ring on its new left edge, readout '+40 px'.

*Motion.* The square sits still, then slides forty pixels the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C02: scene `slide` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 640 x 360): Sprite2D, checker 128 px at scale 1.0, centred; lab-shaders/01-slide.gdshader assigned at 0.22 of the beat; record from 0 to the event plus 1.5 s and hold the last frame; 30 fps; Forward+. Measured: left edge 256 -> 296.

### B06 · 35 words · ~12 s

> The forty is in the node's own pixels, counted before the node is scaled. Here the right-hand square is scaled to twice its size, so the same forty carries it eighty pixels across the screen.

*Picture.* Same code card. At right, two real Godot squares side by side: one at its own size, one scaled to twice its size, both given the same `VERTEX.x += 40.0` at 52 % of the beat. The small one jumps 40 px, the large one 80 px. Readouts '40 px' and '80 px' under them; label 'same shader'.

*Motion.* Both squares jump at the same instant; the large one travels twice as far.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C03: scene `local` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 640 x 360): two Sprite2D checker squares, scale 1.0 at x 130 and scale 2.0 at x 380; 01-slide on both at 0.52 of the beat; record to the event plus 1.5 s, then hold. Measured: left edge moved 40 px (scale 1.0), 80 px (scale 2.0), 90 px (Lab default scale 2.25).

### B07 · 33 words · ~11 s

> Multiply, and the corners move toward or away from the middle. Here, one and a half times wider and half as tall: the square stretches and flattens. Still only four corners are moving.

*Picture.* Code card at left with `VERTEX *= vec2(1.5, 0.5);` highlighted; at right a real Godot window: the 128 px square, still, then at 35 % of the beat stretches to 192 px wide and flattens to 64 px tall about its middle. Readout '192×64 px'.

*Motion.* The square stretches wide and flattens about its own middle when the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C04: scene `squash` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 640 x 360): Sprite2D checker 128 px at scale 1.0; 02-squash at 0.35 of the beat; record to the event plus 1.5 s, then hold. Measured box 192 x 64, centre unchanged.

### B08 · 36 words · ~12 s

> To treat corners differently, tell them apart. The engine gives each corner an address too, called U V: zero to one across, zero to one down. Top left is zero, zero. Bottom right is one, one.

*Picture.* The same square, now with BOTH numberings at each corner in two rows: pixels from the middle (-64, -64) and address (0, 0), then (64, -64)/(1, 0), (-64, 64)/(0, 1), (64, 64)/(1, 1). A terracotta dot visits the corners. Caption in the GLOSSARY wording: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.

*Motion.* A dot visits the four corners and the address row of numbers lands beside each pixel row.

*Lane.* manim · `B08_Address` · runner-up: ShaderLab: Lab render coloured by UV

### B09 · 33 words · ~11 s

> Now scale a move by the address. Add fifty times the vertical address to x. The top corners add nothing, because their address is zero. The bottom corners add fifty. The square leans.

*Picture.* Code card at left with `VERTEX.x += 50.0 * UV.y;` highlighted; at right a real Godot window: the 128 px checker square, still, then at 72 % of the beat it leans: the bottom edge slides 50 px right while the top stays. A terracotta ring on the bottom edge, readout '+50 px'.

*Motion.* The square shears sideways when the shader switches on: top corners stay, bottom corners go fifty pixels.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C05: scene `lean` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 640 x 360): Sprite2D checker 128 px at scale 1.0; 03-lean at 0.72 of the beat; record to the event plus 1.5 s, then hold. Measured left edge 256 -> 306 (+50 px over 128 rows).

### B10 · 39 words · ~13 s

> Only four corners moved. In between, the card fills the shape in even steps. We measured the left edge: fifty pixels over a hundred twenty-eight rows, on a straight line, to within half a pixel. Remember that straight line.

*Picture.* The leaning square's left edge drawn as a slanted line with five sample dots along it, labelled with the measured shifts +1, +12, +25, +37 and +49 px (rows 2, 31, 63, 95 and 124 of 128). A caption: 'four corners: straight edges'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · Forward+ · straight to within half a pixel'.

*Motion.* The five dots land one after another down the edge, each with its measured number, evenly spaced.

*Lane.* manim · `B10_EvenSteps` · runner-up: ShaderLab with readouts

## Act II: More Corners

### B11 · 32 words · ~11 s

> A slide, a squash, a lean: four corners are enough when the whole shape moves as one. A bend is different. Watch what a ripple does to a flag with four corners.

*Picture.* Act title 'More Corners' (serif 40) top-left. Three real Godot squares in a row: the left slides, the middle squashes, the right leans, all switched on together at 12 % of the beat, as the three words are said. One word under each: slide, squash, lean.

*Motion.* Three squares change at once, each by its own one-line shader.

*Lane.* capture · `ShaderLab` · runner-up: manim: three drawn squares

*Capture to record.* C06: scene `triptych` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 640 x 360): three Sprite2D checker squares at x 130, 320, 510; shaders 01-slide, 02-squash, 03-lean at 0.12 of the beat; record to the event plus 1.5 s, then hold.

### B12 · 28 words · ~10 s

> A ripple is the sine of the address across, scaled and added to y. On this flag, nothing ripples. The right end drops, and every edge stays straight.

*Picture.* Code card at left with `VERTEX.y += sin(UV.x * 8.0) * 24.0;` highlighted; at right a real Godot window: a cream and teal checker flag (four corners), flat for a moment, then at 58 % of the beat its right end drops 24 px and every edge stays straight: a tilt, not a ripple. Terracotta ring on the right end, readout '+24 px'. Caption: 'sine: a smooth wave between -1 and 1'.

*Motion.* The flag does not ripple: its right end drops and the whole shape tilts, edges straight.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C07: scene `tilt` of evidence/planning-checks/scratch-project/capture_scenes.gd: Sprite2D flag 384 x 168 (four vertices), canvas 1280 x 720; 04-ripple assigned at 0.58 of the beat; record to the event plus 1.5 s, then hold. Measured on the Lab's 128 px sprite: right end +24 px (sin 8 x 24 = 23.7), top and bottom edges straight to within 0.49 px.

### B13 · 32 words · ~11 s

> Why? Vertex can only move the vertices that exist. Between two corners, the card draws a straight line. A curve needs corners along the way, for vertex to push up and down.

*Picture.* A sine curve on a grid. Two terracotta vertex dots at its ends joined by a straight chord (label '2 vertices'); then dots are added at 3, 5 and 9 positions and the chord becomes a polyline hugging the curve (labels '3', '5', '9 vertices'). A caption: 'vertex moves only the vertices that exist'.

*Motion.* More dots appear along the curve and the straight chord bends into a polyline that follows it.

*Lane.* manim · `B13_OnlyWhatExists` · runner-up: ShaderLab with the tilted flag

### B14 · 37 words · ~13 s

> So give the shape more vertices. Here are two ways in Godot. A polygon node, where you place the points yourself. Or a mesh node, which draws a mesh: the vertices and triangles that make a shape.

*Picture.* Two panels on the cream stage. Left: a polygon outline whose points appear one at a time as if placed by hand, label 'Polygon2D: you place the points'. Right: a rectangle cut by grid lines into small cells with a dot at every crossing, label 'MeshInstance2D: a mesh cut into a grid'. Caption in the GLOSSARY wording: 'mesh: the vertices and triangles that make a shape'.

*Motion.* Points appear one by one on the left while the right-hand rectangle is cut into a grid.

*Lane.* manim · `B14_TwoWays` · runner-up: GodotDevWorkbench scene tree (labelled reconstruction)

### B15 · 38 words · ~13 s

> A mesh instance two D node draws a mesh. Give it a quad mesh, a flat rectangle you can cut into a grid. Subdivide width and subdivide depth say how many extra cuts to make across and down.

*Picture.* Code card at left with five GDScript lines (quad mesh, size, subdivide width, subdivide depth, assign to the node); at right a real Godot window: a 320 px checker square drawn by a MeshInstance2D with terracotta dots on the mesh's vertices: four dots, then nine as the cuts go to one, then twenty-five as they go to three. Readouts '4 vertices', '9 vertices', '25 vertices'.

*Motion.* Dots multiply on the square as the cuts are raised: four, nine, twenty-five.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C08: scene `mesh-recipe` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 1280 x 720): MeshInstance2D with a QuadMesh 320 x 320, checker texture, subdivide width and depth 0 -> 1 at 0.6 of the beat -> 3 at 0.8 of the beat; a child Node2D draws a terracotta dot at every vertex of the mesh (read from surface_get_arrays); 12 s.

### B16 · 38 words · ~13 s

> Count them. Cut a quad mesh three by three, and each side gets five corner points: twenty-five vertices. Always two more than the cuts, each way. The flag's thirty-one by seven makes thirty-three by nine: two hundred ninety-seven.

*Picture.* A 5 by 5 grid of terracotta dots appears row by row with a running counter up to 25, labelled 'cut 3 by 3'. Beside it the formula '(cuts + 2) x (cuts + 2)'. Then the flag's 33 by 9 grid, drawn small, with its counter ending at 297, labelled 'cut 31 by 7'. Small grey credit: 'counted from the mesh in Godot 4.7.2'.

*Motion.* Dots appear row by row while the counter climbs to twenty-five, then the larger grid counts to two hundred ninety-seven.

*Lane.* manim · `B16_CountThem` · runner-up: LectureEvidenceTable

### B17 · 33 words · ~11 s

> Same ripple. Same picture. On the left, four vertices: a tilt. On the right, two hundred ninety-seven: a ripple. Nothing in the shader changed, only how many corners it had to work with.

*Picture.* Two real Godot flags side by side on the stage, the same cream and teal checker texture and the same `VERTEX.y += sin(UV.x * 8.0) * 24.0;` switched on at 10 % of the beat. Left: four vertices, the flag tilts. Right: 297 vertices, the flag ripples. Readouts '4 vertices' and '297 vertices'; label 'same shader on both'.

*Motion.* Both flags get the same one line at the same instant; the left one tilts, the right one ripples.

*Lane.* capture · `ShaderLab` · runner-up: manim: two drawn flags

*Capture to record.* C09: scene `pair` of evidence/planning-checks/scratch-project/capture_scenes.gd: left Sprite2D flag 384 x 168 at x 340, right MeshInstance2D QuadMesh 384 x 168 cut 31 x 7 at x 940; 04-ripple on both at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold.

### B18 · 39 words · ~13 s

> More vertices, a smoother wave. Four pieces show every joint. Ten soften them. Thirty-two hide them. A rule of thumb: eight pieces per wave leaves the worst gap near eight percent of the wave's height. Sixteen leaves about two.

*Picture.* Three real Godot flags in a row, the same ripple switched on at 10 % of the beat, cut into 4, 10 and 32 straight pieces (subdivide width 3, 9 and 31, depth 0). The first shows every joint, the second softens them, the third has none. Readouts under them: '11 px gap', '2 px gap', 'under 1 px'. Caption: 'measured worst gap · 8 pieces per wave: about 8 % of the wave's height'.

*Motion.* Three flags ripple at once; the joints are plain to see on the left and gone on the right.

*Lane.* capture · `ShaderLab` · runner-up: manim sine with polylines

*Capture to record.* C10: scene `densities` of evidence/planning-checks/scratch-project/capture_scenes.gd: three MeshInstance2D QuadMesh 288 x 126 at x 215, 640, 1065 with subdivide width 3, 9, 31 and depth 0; 04-ripple on all at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold. Measured at 3x zoom: worst gap 10.8, 2.0 and 0.35 px (formula 11.0, 1.9, 0.2).

### B19 · 37 words · ~13 s

> Cut only where it bends. This ripple runs along the flag, never up and down, so rows of vertices add nothing. Thirty-one cuts across and none down gives sixty-six vertices, and the picture matches, pixel for pixel.

*Picture.* Two real Godot flags side by side, the same ripple on at 10 % of the beat: left cut 31 by 7 (297 vertices), right cut 31 by 0 (66 vertices). They look identical. Readouts '297 vertices' and '66 vertices'; a caption 'identical, pixel for pixel'.

*Motion.* The two flags ripple in the same way and cannot be told apart.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grid with the unused rows greyed

*Capture to record.* C11: scene `cut-along` of evidence/planning-checks/scratch-project/capture_scenes.gd: left QuadMesh 384 x 168 cut 31 x 7 at x 340, right the same cut 31 x 0 at x 940; 04-ripple on both at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold. Measured: 0 differing pixels of 288,000.

### B20 · 38 words · ~13 s

> A polygon node gives you one vertex per point you place. With points only around the edge, Godot fills the inside with long thin triangles, and the picture twists. A grid of points, joined into cells, fixes it.

*Picture.* Two real Godot flags side by side, the same ripple on at 10 % of the beat. Left: a Polygon2D with 66 points around its outline; the outline ripples but the checker inside twists along crossing lines. Right: the 297-vertex mesh, clean. A terracotta ring on the twisted crossing lines; readouts 'Polygon2D · 66 points' and 'mesh · 297 vertices'.

*Motion.* Both outlines ripple, but the left flag's inside twists along long diagonal lines.

*Lane.* capture · `ShaderLab` · runner-up: manim: triangles drawn over the polygon

*Capture to record.* C12: scene `polygon` of evidence/planning-checks/scratch-project/capture_scenes.gd: left Polygon2D with 66 outline points (33 on top, 33 on the bottom) and uv in texture pixels, right QuadMesh 31 x 7; 04-ripple on both at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold. Verified: 64 triangles from Geometry2D.triangulate_polygon, one point in 34 of them, longest edge 419 px; the default render equals those triangles pixel for pixel; a grid of points with a cell list (polygons) equals the mesh pixel for pixel.

## Act III: A Waving Flag

### B21 · 31 words · ~10 s

> Now let it travel. Time is seconds on one clock shared by the whole game. Subtract it inside the sine, and the ripple slides to the right as the seconds pass.

*Picture.* Act title 'A Waving Flag' (serif 40) top-left. Code card at left with `VERTEX.y += sin(UV.x * 8.0 - TIME * 3.0) * 24.0;` highlighted; at right a real Godot window: the mesh flag on a grey pole shows the static ripple, then at the 58 % mark the ripple starts to slide to the right. Caption in the GLOSSARY wording: 'TIME: seconds on one clock shared by the whole game'.

*Motion.* A frozen ripple starts to travel to the right along the flag, the left end bobbing with it.

*Lane.* capture · `ShaderLab` · runner-up: manim sine plot with a phase marker

*Capture to record.* C13: scene `travel` of evidence/planning-checks/scratch-project/capture_scenes.gd: MeshInstance2D flag (QuadMesh 384 x 168 cut 31 x 7) with a grey pole at the left edge; 04-ripple from the start, 05-flag-travelling assigned at 0.58 of the beat; canvas 1280 x 720; record the whole beat (D) and hold. Verified: the wave moves right as TIME grows (fitted phase advanced with the clock; mean error 0.25 px).

### B22 · 35 words · ~12 s

> But a flag is held at one end. Multiply the ripple by the address across. At the left edge the address is zero, so nothing is added, and that edge stays put, like a pole.

*Picture.* Code card at left with `VERTEX.y += sin(UV.x * 8.0 - TIME * 3.0) * 24.0 * UV.x;` and the final `* UV.x` highlighted; at right a real Godot window: the travelling flag bobs at its left end as well; at the 30 % mark the new line goes on and the left end, beside the grey pole, stops moving while the rest keeps rippling. A terracotta ring on the left edge, readout 'pinned'.

*Motion.* The left edge stops moving the moment the multiplication goes on; the rest of the flag keeps waving.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C14: scene `pinned` of evidence/planning-checks/scratch-project/capture_scenes.gd: the mesh flag with pole; 05-flag-travelling from the start, 06-flag-pinned assigned at 0.3 of the beat; canvas 1280 x 720; record the whole beat (D) and hold. Verified: the left edge's top row stays at y = 276 in every frame.

### B23 · 39 words · ~13 s

> Three numbers shape the wave: how tall, how many waves fit, how fast. Make each a uniform: a value your game sets from outside the shader, the same for every vertex and pixel. Now the flag has three dials.

*Picture.* Code card at left with the three uniform lines highlighted in turn (amplitude, frequency, speed); at right the real waving flag on its pole, at the defaults. Caption in the GLOSSARY wording: 'uniform: a value your game sets from outside; every pixel sees the same one'. Three small labels as each line lands: how tall, how many waves fit, how fast.

*Motion.* The three uniform lines light up in turn while the flag keeps waving.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C15: scene `dials-rest` of evidence/planning-checks/scratch-project/capture_scenes.gd: the mesh flag with pole; 07-flag-dials from the first frame, uniforms at their defaults (24, 8, 3); canvas 1280 x 720; record 252 frames (8.4 s, four wave periods) and loop them.

### B24 · 28 words · ~10 s

> Raise amplitude, and the waves get taller. Raise frequency, and more waves fit across. Raise speed, and they travel faster. Each one changes only what its name says.

*Picture.* Code card at left (the same nine lines); at right the real flag as amplitude is swept up and back, then frequency, then speed, each with a label naming the dial: 'amplitude', 'frequency', 'speed'. Captions in plain words: 'how tall', 'how many waves fit', 'how fast'.

*Motion.* Each dial moves in turn and only the property its name says changes.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C16: scene `sweeps` of evidence/planning-checks/scratch-project/capture_scenes.gd: the mesh flag with pole and 07-flag-dials; amplitude 24 -> 40 -> 0 -> 24 over 0.03 to 0.28 of the beat, frequency 8 -> 16 -> 2 -> 8 over 0.34 to 0.60, speed 3 -> 8 -> 0 -> 3 over 0.66 to 0.92 (all smoothstep, scripted via set_shader_parameter); canvas 1280 x 720; 12 s.

### B25 · 35 words · ~12 s

> Your game can turn the dials while it runs. When the wind picks up, call set shader parameter on the node's material, with the dial's name and a new value. The flag answers at once.

*Picture.* One-line GDScript card at left, `$Flag.material.set_shader_parameter("amplitude", 40.0)`, highlighted when the call fires; at right the real flag at its defaults, then waves taller from the moment of the call. Readout 'amplitude 40'.

*Motion.* The flag's waves grow taller in the frame after the highlighted call fires.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace

*Capture to record.* C17: scene `wind` of evidence/planning-checks/scratch-project/capture_scenes.gd: the mesh flag with pole and 07-flag-dials; material.set_shader_parameter("amplitude", 40.0) at 0.75 of the beat; canvas 1280 x 720; record the whole beat (D).

### B26 · 37 words · ~13 s

> Read it as one. Three dials at the top. In vertex, the wave: the address across, minus time, through a sine, scaled by the dials, pinned by the address. Nine lines, one of them moving the flag.

*Picture.* The nine-line shader on a code card at left; the three uniform lines highlighted as 'three dials' is said, then the single `VERTEX.y += ...` line held while the voice walks through its parts; at right the real flag waves on its pole.

*Motion.* Focus lands on the three dials, then on the one line that moves the flag, while the flag waves.

*Lane.* capture · `ShaderLab` · runner-up: manim: the line split into labelled parts

*Capture to record.* C15 again (the same recording as B23): scene `dials-rest` of evidence/planning-checks/scratch-project/capture_scenes.gd, 07-flag-dials at its defaults.

## Act IV: Passing Data Forward

### B27 · 39 words · ~13 s

> The flag moves, but it looks like a flat sheet. Nothing shades the folds. Shading is a job for fragment, the function that colors each pixel the shape covers. But fragment runs later, and it never sees the corners.

*Picture.* Act title 'Passing Data Forward' (serif 40) top-left. A three-stage strip left to right: 'vertex()' with four terracotta corner dots, 'the card fills the shape', 'fragment()' drawn as a pixel grid. A small question mark leaves fragment() looking back for the corners and stops at a pane of glass. Caption in the GLOSSARY wording: 'fragment(): runs once for each pixel the shape covers; sets its color'.

*Motion.* A question mark travels back from fragment toward the corners and stops at the glass.

*Lane.* manim · `B27_FragmentCannotSee` · runner-up: DesignPipelineClaim, show-tell isometric

### B28 · 34 words · ~12 s

> The way across is a varying. In vertex, you set a value at each corner. In fragment, you read it. The graphics card interpolates it across the shape, and it flows one way: forward.

*Picture.* A quad with a number on each corner dot (0 at the left corners, 1 at the right ones). The numbers flow right into the filled quad and blend into a smooth ramp as an arrow labelled 'forward' passes from 'set in vertex()' to 'read in fragment()'. Caption in the GLOSSARY wording: 'varying: a value set at each corner, blended across the shape for fragment() to read'.

*Motion.* The corner numbers flow into the quad and spread into a smooth ramp, in the forward direction only.

*Lane.* manim · `B28_Varying` · runner-up: LectureCodeTrace with the three lines

### B29 · 37 words · ~13 s

> Four colors, one per corner, set in vertex. Fragment only reads them. The result is a smooth blend, and an exact one. Halfway along the top edge, red reads one half, the average of its two corners.

*Picture.* Code card at left (varying tint, set in vertex, read in fragment); at right a real Godot window showing a square blended from blue (top left), red (top right), cyan (bottom left) and yellow (bottom right). Readouts above its top edge: 'red 0', 'red 0.5', 'red 1'.

*Motion.* The corner colours blend; the readouts land along the top edge as the voice says one half.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C18: Lab rect/sprite still: `check_shader.sh lab-shaders/08-corner-colors.gdshader --kind sprite --sprite-tex white` (default fit scale), PNG 1920 x 1080 by the harness. Probes (Forward+ and Compatibility agree): top left (0.02, 0.02, 0.98), top right (0.98, 0.02, 0.02), middle of the top edge (0.50, 0.02, 0.50), centre (0.50, 0.50, 0.50).

### B30 · 39 words · ~13 s

> Switch the blending off with flat, and each triangle keeps one corner's value. A mesh cut into a grid shows it: the smooth blend breaks into tiles. A rectangle is two triangles, and the blending happens inside each one.

*Picture.* Code card at left with the one changed line `varying flat vec3 tint;` highlighted; at right two real Godot meshes cut 7 by 7: on the left the smooth four-colour blend, on the right the same colours with flat, broken into diagonal tiles, one per triangle. Labels 'smooth' and 'flat'. Caption: 'flat: the value is not blended'.

*Motion.* The smooth blend on the left breaks into tiles on the right as the flat line is highlighted.

*Lane.* capture · `ShaderLab` · runner-up: manim: two triangles with flat colours

*Capture to record.* C19: scene `flat-mesh` of evidence/planning-checks/scratch-project/capture_scenes.gd: two MeshInstance2D QuadMesh 300 x -300 (size.y negative, so UV.y runs down the screen and the colours sit as on the Lab sprite) cut 7 x 7 with a white texture; 08-corner-colors on the left, 09-corner-colors-flat on the right; still PNG; canvas 1280 x 720. Verified: a four-vertex sprite with flat shows ONE colour (the first vertex's) on both triangles; a QuadMesh 0 x 0 has 6 indices, i.e. two triangles.

### B31 · 39 words · ~13 s

> The engine does this for you, too. U V is set at the corners and blended, which is why it is a smooth ramp. The color from vertex is passed on the same way, and multiplied by the picture.

*Picture.* Top: a 0 to 1 ramp strip with two terracotta corner dots (0 and 1), the values between them filling in, labelled 'U V: set at the corners, blended'. Below: a small tinted block times a checker picture equals a tinted checker, labelled 'color from vertex x the picture = color in fragment'. Caption: 'COLOR: the color being drawn'.

*Motion.* The ramp fills in between its two corner values, then the tint multiplies the picture.

*Lane.* manim · `B31_BuiltInVaryings` · runner-up: LectureEvidenceTable

### B32 · 33 words · ~11 s

> So light the folds. In vertex, work out how the cloth slopes and pass it as a varying. In fragment, darken the cloth where it slopes away. Now the folds read as folds.

*Picture.* Code card at left (thirteen lines: varying fold, set in vertex, used in fragment); at right the real flag on its pole: first flat-looking, then at the 62 % mark the folds darken where the cloth slopes away. Highlight on the `phase` and `fold` lines as 'pass it as a varying' is said, with a rendered tag 'phase: where the wave is · fold: how the cloth slopes', then on the fragment line. Caption in the GLOSSARY wording: 'slope: how steeply a line rises: up divided by across'.

*Motion.* The flag looks flat, then its folds read as folds when the lit shader goes on.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C20: scene `lit` of evidence/planning-checks/scratch-project/capture_scenes.gd: the mesh flag with pole; 06-flag-pinned from the start, 10-flag-lit assigned at 0.62 of the beat; canvas 1280 x 720; record the whole beat (D).

### B33 · 39 words · ~13 s

> There is a shorter way. The color already travels from vertex to fragment, multiplied by the picture. Darken it in vertex, and you need no varying and no fragment function. Same picture, pixel for pixel, with the dials back.

*Picture.* Code card at left (eleven lines: the three dials, the phase, the wave line and one `COLOR.rgb *= ...` line, no varying and no fragment function) with the COLOR line highlighted; at right the same real lit flag as the opening, waving. Readout 'same picture'.

*Motion.* The COLOR line is highlighted while the flag waves, lit exactly as before.

*Lane.* capture · `ShaderLab` · runner-up: manim: the two shaders side by side with a diff

*Capture to record.* C01 again (the same recording as the opening): scene `final` of evidence/planning-checks/scratch-project/capture_scenes.gd, 11-flag-final from the first frame. Verified: the explicit-varying version (10) and this one draw the same picture, 0 differing pixels (scene equiv-lit-color).

### B34 · 37 words · ~13 s

> One limit. A varying is only as detailed as your corners. Six stripes computed in vertex vanish on four corners, because both ends compute the same number. Computed in fragment, at every pixel, the stripes are there.

*Picture.* Code card at left (the stripes computed in vertex and passed as a varying) with the sine line highlighted; at right two real Godot squares on four corners: the left shows plain flat grey, the right shows six clear stripes. Labels 'in vertex()' and 'in fragment()'.

*Motion.* The left square stays plain grey while the right one shows six stripes.

*Lane.* capture · `ShaderLab` · runner-up: manim: sampled sine with two end values

*Capture to record.* C21: scene `stripes` of evidence/planning-checks/scratch-project/capture_scenes.gd: two Sprite2D white squares at scale 3.0 (12-stripes-from-vertex on the left, 13-stripes-from-fragment on the right); still PNG; canvas 1280 x 720. Measured (Lab): the vertex version reads 0.749 at every probe; the fragment version reads 0.58 to 0.92.

## Act V: When It Looks Wrong

### B35 · 32 words · ~11 s

> Some mistakes compile and still look wrong. First: in two D, a quad mesh draws upside down. Give its size a negative y, and it stands up, matching a sprite beside it.

*Picture.* Act title 'When It Looks Wrong' (serif 40) top-left. One-line GDScript card at left, `mesh.size = Vector2(256, -256)`, highlighted when it runs; at right two real Godot pictures of the same blob with two eyes: a sprite on the left (eyes up) and a quad mesh on the right drawn upside down (eyes down) that flips upright at the moment the size goes negative. Labels 'sprite' and 'quad mesh'.

*Motion.* The mesh picture flips to stand upright the moment its size.y goes negative, matching the sprite.

*Lane.* capture · `ShaderLab` · runner-up: manim: a flipped icon

*Capture to record.* C22: scene `flip` of evidence/planning-checks/scratch-project/capture_scenes.gd: left Sprite2D of the blob at scale 2.0, right MeshInstance2D QuadMesh 256 x 256 with the same texture; at 0.6 of the beat mesh.size = Vector2(256, -256); canvas 1280 x 720; record the whole beat (D). Verified: eyes below the middle with +size.y, above it with -size.y, same as the sprite.

### B36 · 32 words · ~11 s

> Second: the word vertex changes meaning. In vertex, it is the corner's position in the node's own pixels. In fragment, it is the pixel's position on the screen. Same word, different numbers.

*Picture.* A 1280 by 720 screen frame (outline) with a 128 px sprite square in its middle. The square's top left is ringed. Two labels on it in turn: 'in vertex(): (-64, -64), from the node's middle' and 'in fragment(): (576, 296), from the screen's top left'. Both name VERTEX in a monospace face. Small grey credit: 'measured in Godot 4.7.2 · Forward+'.

*Motion.* The same corner gets two labels with two different pairs of numbers.

*Lane.* manim · `B36_TwoMeanings` · runner-up: LectureEvidenceTable

### B37 · 35 words · ~12 s

> Move the node and you see it. Colored from the corner position, the gradient travels with the sprite. Colored from the pixel's screen position, the sprite slides across a gradient that stays where it is.

*Picture.* Two real Godot squares stacked, each 256 px, both coloured blue to orange by the same last line. Top: colour from the corner position through a varying. Bottom: colour from VERTEX in fragment. Both slide to the right together: the top gradient moves with its square, the bottom square changes colour as it crosses a gradient that stays on the screen. Labels 'from vertex()' and 'from fragment()'.

*Motion.* Both squares slide right; the top one keeps its colours, the bottom one's colours change.

*Lane.* capture · `ShaderLab` · runner-up: manim: two squares and a ruler

*Capture to record.* C23: scene `vertex-two` of evidence/planning-checks/scratch-project/capture_scenes.gd: two Sprite2D white squares at scale 2.0 (top 15-position-from-vertex, bottom 14-position-from-fragment), canvas 1280 x 720; both slide from x 300 to x 1000 over 0.3 to 0.7 of the beat; 12 s. Verified: corner pixel red = 0.02 (top) against 0.45 (bottom) in both renderers.

### B38 · 37 words · ~13 s

> Third: a polygon node only has U V when it has a texture. A texture is an image a shader can read. Without one, the address is zero everywhere, and a wave multiplied by it never starts.

*Picture.* Code card at left with the pinned flag line (it multiplies by `UV.x`) highlighted; at right two real Godot polygons with the same grid of points: on the left, no texture, a flat teal rectangle that does not wave at all; on the right, with a texture, a waving flag. Labels 'no texture' and 'with texture'. Caption in the GLOSSARY wording: 'texture: an image a shader can read'.

*Motion.* The left polygon stays a still rectangle while the right one waves, under the same shader.

*Lane.* capture · `ShaderLab` · runner-up: manim: UV values on a polygon

*Capture to record.* C24: scene `polygon-uv` of evidence/planning-checks/scratch-project/capture_scenes.gd: two Polygon2D with a 33 x 9 grid of points and a cell list (polygons); left without a texture (colour teal), right with the checker texture and uv in texture pixels; 06-flag-pinned on both at 0.1 of the beat; canvas 1280 x 720; record the whole beat (D). Verified: UV reads 0 everywhere without a texture, even with uv set.

### B39 · 34 words · ~12 s

> Fourth: a vertex shader changes the drawing, not the node. This one draws the sprite two hundred pixels away. The node's rectangle and its collision shape stay exactly where they were. We checked both.

*Picture.* Code card at left with `VERTEX.x += 200.0;` highlighted; at right a real Godot window with a thin grey outline marking the node's own rectangle (from get_rect()). The checker square starts inside it, then the picture slides 200 px to the right while the outline stays. Readouts 'rect unchanged' and 'collision unchanged'. Caption: 'collision shape: what physics collides with'.

*Motion.* The picture slides away from its outline, which does not move.

*Lane.* capture · `ShaderLab` · runner-up: manim: a node and a ghost picture

*Capture to record.* C25: scene `drawing-only` of evidence/planning-checks/scratch-project/capture_scenes.gd (canvas 640 x 360): Sprite2D checker 128 px at scale 1.0 with a grey outline drawn from get_rect(); 16-slide-far assigned at 0.3 of the beat; record to the event plus 1.5 s, then hold. Verified: get_rect() = (-64, -64, 128, 128) before and after; an Area2D collision shape on the node overlaps the probe at the node's position and not the probe where the picture is drawn; the picture's left edge moves from x 156 to 356.

### B40 · 37 words · ~13 s

> Last: when nothing waves, count the vertices. Ask a mesh for its vertex array and print the size: here, two hundred ninety-seven. A polygon has one per point. A plain sprite has four, and four cannot bend.

*Picture.* A plain terminal on the cream stage: the one-line print statement, then the real output of running it in a node's _ready(): the engine banner and the number 297. Caption: 'Mesh.ARRAY_VERTEX: the list of vertex positions'.

*Motion.* The line is typed and the number 297 lands last.

*Lane.* terminal · `CCPlainShell` · runner-up: ShaderLab

## Closing

### BVDT · recap · 78 words · ~26 s

> Let's recap with Claude. Vertex runs once for each corner and decides where it goes. A shape can only bend where it has vertices. Cut a mesh until each wave has eight pieces or more. A flag is a sine of the address and the time, pinned at one end, with dials. A varying carries a value from the corners to every pixel. When it looks wrong, count the vertices, and check what each position is measured from.

*Picture.* The recap card: Vertex runs once for each corner and decides where it goes. / A shape can only bend where it has vertices. / Cut a mesh until each wave has eight pieces or more. / A flag is a sine of the address and the time, pinned at one end, with dials. / A varying carries a value from the corners to every pixel. / When it looks wrong, count the vertices, and check what each position is measured from.

### BHTF · your turn · 94 words · ~32 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a waving banner. Draw it with a MeshInstance two D and a quad mesh cut thirty-one by seven. In vertex, move the corners up and down with a sine of the address across and the time. Make amplitude, frequency and speed float uniforms, and pin the left edge. Then tell me how many vertices the mesh has. Then check two things yourself. Does the left edge stay still while the rest ripples? And does the vertex count match thirty-three by nine?

*Prompt shown and read in full:* Write a Godot canvas item shader for a waving banner. Draw it with a MeshInstance two D and a quad mesh cut thirty-one by seven. In vertex, move the corners up and down with a sine of the address across and the time. Make amplitude, frequency and speed float uniforms, and pin the left edge. Then tell me how many vertices the mesh has.

*Two checks:* Check: the left edge never moves while the rest ripples. · Check: the vertex count matches thirty-three by nine.

### BOUT · outro · 6 words · ~4 s

> Vertex Shaders. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


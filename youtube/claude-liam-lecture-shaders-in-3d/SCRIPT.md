# Script: Shaders in 3D

**What this is.** The words Liam will say in *Shaders in 3D*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 50 beats, 1807 words, about **10:18** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 24, manim 14, remotion 5, editor 1.

**If it runs long.** Cut, in this order: the tween beat (B28), the cull beat (B17), the two-questions beat (B18), the output-is-s R G B beat (B42) and the missing-functions beat (B35): each repeats an idea another beat carries. The lit sphere (B11), the unshaded pair (B14), the box reveal (B36) and the two-renderer comparison (B37 to B41) stay: they are the film's proof.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Same Shape, New Names | 10 | 374 | ~2:07 |
| II | Lit or Unlit | 8 | 269 | ~1:31 |
| III | A Surface That Changes | 10 | 341 | ~1:56 |
| IV | Read a Real One | 8 | 241 | ~1:22 |
| V | Which Renderer? | 8 | 271 | ~1:32 |

## Opening

### BOPEN · identity card · 31 words · ~10 s

> Shaders in three D. Learn what changes when a shader draws a three-D surface, how lighting and the renderer change the color you get, and how to read a real one.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Shaders in 3D", and the line "What changes when a shader goes three-D".

### BIDEA · the question · 38 words · ~13 s

> Hallo. This is Liam, in for Bear. Many people think a three-D shader is a different, harder thing. It is not. It has the same shape as a two-D shader, with new names and one new idea: light.

*Picture.* The hesitant writer types: "3D shaders are
a different, harder thing." then deletes "a different, harder thing" and types "the same shape, new names".

### BDEFS · terms · 49 words · ~17 s

> Five terms. A mesh is the points and triangles that make a three-D shape. A material tells Godot how to draw a surface. Albedo is the base color of a surface. Lighting is how lights change that color. A renderer is the part of Godot that draws the picture.

*Picture.* "Terms In This Lecture": **Mesh** — the set of vertices and triangles that make a shape; **Material** — the resource that tells Godot how to draw a surface; it holds the shader; **Albedo** — the base color of a surface; **Lighting** — how lights change a surface's color; **Renderer** — the part of Godot that draws

## Act I: Same Shape, New Names

### B01 · 35 words · ~12 s

> This shader comes from a small game. It charges a pad from rust to green, and the whole effect is ten lines. By the end of this film, you can read every one of them.

*Picture.* Act title 'Same Shape, New Names' (serif 40) top-left. Left: the ten-line pad shader on a cream code card, no line focus. Right: a framed window holding a real Godot render of a flat square lying flat, seen from the game's camera angle, charging from striped rust-brown to flat green as activation climbs. Caption: 'a shader from a small game'.

*Motion.* The square charges from striped rust to flat green while its ten lines of code sit beside it.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a pad charging

*Capture to record.* C01: custom scene 'pad on a flat square' (CAPTURE-PLAN S1): lab-shaders/12-signal-pad.gdshader on a 1.55 x 1.55 QuadMesh lying flat, orthographic camera size 2.6 from (5.8, 9, 11) toward the origin, activation 0 to 1 across 0 to 0.86 of the clip then held at 1 (the clip is as long as the longer of its two beats), 30 fps, Forward+, stage #D9D5CA. Frame at the 50 % mark reads activation 0.5 (mid-tone), at 85 % reads 0.85.

### B02 · 38 words · ~13 s

> A shader is a small program the graphics card runs to decide how something is drawn. In two-D or three-D, it has the same shape: a first line, up to three functions, and dials your game can turn.

*Picture.* The compiled skeleton file lab-shaders/03-skeleton-3d.gdshader drawn as a cream code card (Menlo, 12 lines). Brackets draw in on the voice's words and each carries a one-word label: 'a first line' brackets line 1 (label 'type'), 'up to three functions' brackets lines 5 to 12, the three empty functions (label 'functions'), 'dials' brackets line 3 where a small dial (a circle with a turning tick) sits at the card's right (label 'dials'). Caption at the top, GLOSSARY wording: 'shader: a small program the graphics card runs to decide how something is drawn'.

*Motion.* A dot steps down the lines like a program, then three brackets draw in one after another, each with its label, and a small dial turns.

*Lane.* manim · `B02_Anatomy` · runner-up: LectureCodeTrace on the skeleton

### B03 · 30 words · ~10 s

> The first line says what the shader is for. Canvas item means two-D. Spatial means three-D, where the shader draws a mesh: the points and triangles that make a shape.

*Picture.* The line `shader_type canvas_item;` in Menlo over a flat teal square (outline icon). On the cue the word canvas_item slides out and spatial slides in, while the flat square turns into an isometric cube in the same teal with faint triangle edges; a one-word label 'mesh' points at the cube. Caption, GLOSSARY wording: 'shader type: the first line; says what the shader is for'.

*Motion.* The word canvas_item is replaced by spatial and the flat square turns into a cube.

*Lane.* manim · `B03_TwoTypes` · runner-up: LectureEvidenceTable

### B04 · 41 words · ~14 s

> Both types use the same three functions. Vertex runs once for each vertex, a corner point of the mesh. A flat square has four. Fragment runs once for each pixel the mesh covers. Light runs once per pixel, for every light.

*Picture.* Left: the test rectangle (a flat square) with four terracotta corner dots. Right: a 12-by-8 pixel grid of outline cells with the square's footprint over it. The four dots flash in order with a counter 1 to 4 and the label 'vertex()'; the covered cells tint one by one, each with a tiny 'fragment()' tag, then all hold; a small lamp icon (drawn bulb with rays) appears and the covered cells brighten once per lamp, two lamps in turn, with the label 'light()'. Captions, GLOSSARY wording: 'vertex: a corner point of a shape' and 'pixel: one dot of the picture on screen'.

*Motion.* Four dots flash in turn, then the covered cells tint one by one, then the cells brighten once for each lamp.

*Lane.* manim · `B04_ThreeFunctions` · runner-up: LectureCodeTrace on the skeleton

### B05 · 30 words · ~10 s

> The other change is the output. A two-D shader sets color: four numbers, red, green, blue and alpha. A three-D shader sets albedo: three numbers. Alpha becomes a separate output.

*Picture.* Two code cards, lab-shaders/01-flat-teal-2d.gdshader at left and lab-shaders/02-flat-teal-3d.gdshader at right (Menlo, 5 lines each), the same positions line for line. The first lines already differ (canvas_item and spatial: label 'type', the idea of the previous beat). On the cues the changed pieces get a terracotta ring in turn: 'COLOR' becomes 'ALBEDO' as the voice says 'the output' (label 'output'); a short ring goes round the four numbers of the two-D color as the voice says 'four numbers'; as it says 'and alpha' the ring moves to the last number, 1.0, and a caption lands, GLOSSARY wording: 'alpha: how visible a pixel is: 0 invisible, 1 solid'; as it says 'three numbers' 'vec4(' becomes 'vec3(' and ', 1.0' dissolves (label 'three numbers'); as it says 'Alpha becomes a separate output' a small 'ALPHA' chip appears beside the card. The unchanged text stays still.

*Motion.* The output and the number of numbers change in turn while everything else stays exactly where it was.

*Lane.* manim · `B05_CodeMorph` · runner-up: ShaderLab

### B06 · 43 words · ~15 s

> Get either one wrong and Godot says so. Write color in a three-D shader and it answers: constants cannot be modified. Color exists there, but you can only read it. Give albedo four numbers and it answers: invalid arguments, vec three, vec four.

*Picture.* A plain terminal window (CCPlainShell, 32 pt) with two real runs, verbatim from the Lab's log. Each run is a comment line with the line that was wrong, then the compiler's two output lines. A terracotta ring (grey-backed) rings each 'SHADER ERROR' line as the voice reads the message. Title: 'Godot 4.7.2 · what the compiler says'. Line cues are frames at 24 fps and are approximate: re-time them to the measured audio.

*Motion.* Each wrong line lands, then the compiler's reply appears under it and is ringed.

*Lane.* remotion · `CCPlainShell` · runner-up: LectureCodeTrace with the message as its note

### B07 · 39 words · ~13 s

> Some mix-ups are silent. Give a three-D mesh a two-D shader, and the running game raises no error. It draws the mesh as if it had no shader at all. When a shader seems ignored, check the first line.

*Picture.* A wide result strip (layout 'stack': result above, and under it a one-line excerpt, the two-D shader's first line `shader_type canvas_item;`, with a tag on that line: 'canvas_item: shaders for 2D and UI'). Real Godot render: two flat squares side by side, both plain grey at first. At the hand-over (0.12 of the clip, as the voice says 'Give a three-D mesh a two-D shader') each is given a red shader: the left one gets the canvas_item shader above, the right one a spatial shader that paints red. The right square turns red; the left stays exactly as it was. Labels land under them: 'canvas_item: ignored' and 'spatial: red'.

*Motion.* Both squares are handed a red shader; only the right one changes.

*Lane.* capture · `ShaderLab` · runner-up: CCPlainShell showing an empty log

*Capture to record.* C18: custom scene 'wrong type' (CAPTURE-PLAN S6): two QuadMesh 1.4 x 1.4 at x -0.95 and +0.95 on the stage, no WorldEnvironment and no lamp (as verify8); both start with no material; at 0.12 of the clip the scene script gives the left lab-shaders/18-two-d-shader-on-a-mesh.gdshader and the right lab-shaders/19-three-d-shader-on-a-mesh.gdshader as material_override (--call-at); the clip is as long as the beat; orthographic size 2.6; Forward+. Verified: no engine error; left stays (0.612, 0.600, 0.569) (the no-material look), right reads (1.0, 0.0, 0.0).

### B08 · 45 words · ~15 s

> U V is a point's address on the shape: zero to one across, zero to one down. Paint it as a color, red across and green down. A square, a box and a sphere each show a different map, because the mesh supplies the address.

*Picture.* A wide result strip (layout 'stack': result above, and under it a one-line excerpt: line 5 of the six-line shader, `ALBEDO = vec3(UV.x, UV.y, 0.0);`, with a tag 'red = UV.x (across), green = UV.y (down)'). Real Godot render: a flat square, a box and a sphere in a row, all swinging side to side about the vertical axis (plus or minus 50 degrees, one swing in eight seconds), every one painted with red-across, green-down address colors. The square shows the whole red-green gradient, the box shows a different patch on each face, the sphere wraps its map around itself. One-word labels land under them: 'square', 'box', 'sphere'. Caption, GLOSSARY wording: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.

*Motion.* The colors stay glued to each surface as the meshes swing, and each mesh shows a different map.

*Lane.* capture · `ShaderLab` · runner-up: manim UV unwrap drawing

*Capture to record.* C02: custom scene 'three meshes' (CAPTURE-PLAN S2): lab-shaders/06-uv-colors-3d.gdshader on QuadMesh 1x1 (x -1.35), BoxMesh 1x1x1 (x 0), SphereMesh r 0.5 (x +1.35); each swings about Y by plus or minus 50 deg (a sine, period 8 s) with a fixed -20 deg tilt about X (NOT a full turn: with default culling the flat square vanishes while its back faces the camera, verify9 run 9a); orthographic size 2.6; the clip is as long as the beat; 30 fps; Forward+. Verified mesh data: quad UV (0,0) top-left; box 3 x 2 cells; sphere U wraps once.

### B09 · 29 words · ~10 s

> To use a shader, give the mesh instance a shader material. In three-D that slot is called material override. The node holds the material. The material holds your shader.

*Picture.* Three boxes slide in left to right and link: a cube icon over 'mesh instance', then 'ShaderMaterial', then 'shader' (a small file icon marked .gdshader). The link between the first two carries a small tab 'material override'. A dot travels from the shader back to the mesh instance (meaning: look here). Captions: 'mesh instance: the node that draws a mesh' (docs: MeshInstance3D is the main node that draws a mesh) and, GLOSSARY wording, 'ShaderMaterial: a material that holds your shader and its settings'.

*Motion.* Each box slides in as it is named, the slot tab lands on the first link, and the dot travels back to the node.

*Lane.* manim · `B09_AttachChain` · runner-up: a real editor frame of the MeshInstance3D Inspector (not recorded)

### B10 · 44 words · ~15 s

> Now run the one-line albedo shader on a sphere. You wrote one flat teal, so you might expect a flat teal disc. Instead one side is bright and one is dim. You wrote no lighting rule. Godot lit the sphere with the scene's lamp.

*Picture.* Left: the five-line shader (ALBEDO = vec3(0.37, 0.64, 0.57)) with its ALBEDO line focused. Right: a real Godot render of one teal sphere, centred. At first the lamp is off and the sphere is a flat dim disc (the 'flat teal disc' the voice says you might expect). At the reveal the lamp switches on, from the upper left: bright on one side, dim on the other, and it stays that way. Labels land on the sphere: 'bright', then 'dim'; a 'lamp' tag lands in the upper left as the voice names the scene's lamp.

*Motion.* A flat dim disc becomes a sphere with a bright side and a dim side the moment the lamp switches on, although the code names one flat color.

*Lane.* capture · `ShaderLab` · runner-up: manim sphere with shading

*Capture to record.* C03a: custom scene 'lamp' (CAPTURE-PLAN S3), one sphere: lab-shaders/02-flat-teal-3d.gdshader on a SphereMesh r 0.5 at the origin, orthographic size 1.8; white ambient light energy 0.25; one DirectionalLight3D tilted 30 deg down at yaw -65 deg, switched off until 0.56 of the clip and on from then (scripted switch, held there); Forward+. Verified: lamp off, the sphere reads one dim value everywhere (0.337, 0.435, 0.412); lamp on at -65 deg, the left side reads about 0.65 to 0.68 red and the right 0.337 (verify4, verify10).

## Act II: Lit or Unlit

### B11 · 37 words · ~13 s

> Back to the lit sphere. A script now moves the lamp. The albedo never changes, but the same surface goes bright, then dim. The color you write is only a starting point. The lighting does the rest.

*Picture.* Act title 'Lit or Unlit' (serif 40) top-left. Left: the same five-line shader, ALBEDO line focused. Right: the real lit sphere while a lamp swings once around it: the bright patch travels around the sphere and the dim side follows. Labels: 'same albedo' (while the lamp moves), then 'new pixel'.

*Motion.* The bright patch travels around the sphere while the code stays put.

*Lane.* capture · `ShaderLab` · runner-up: manim sphere with a lamp icon

*Capture to record.* C03: custom scene 'lamp' (CAPTURE-PLAN S3), one sphere as C03a but the lamp is on throughout and turns: yaw = -65 deg + 360 deg over 14 s at its own pace (scripted), so the clip opens on the pose B10 ended on; the clip is as long as the beat; Forward+. Half-lit at yaw 90 and 270, dim with the lamp behind.

### B12 · 31 words · ~10 s

> In three-D, the fragment function describes a surface. Albedo is its base color. Alpha is how visible it is. Emission is light it gives off. Roughness and metallic describe its finish.

*Picture.* A four-row table on the cream stage, one row ringed as each output is named: ALBEDO, ALPHA, EMISSION and ROUGHNESS with METALLIC (the last two share a row), each with a short plain meaning. The note names the docs page.

*Motion.* The ring steps down the four rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: four spheres, one output changing on each

### B13 · 31 words · ~10 s

> Then Godot's own lighting turns that description, and every lamp, into the pixel you see. You describe the surface. Godot does the lighting. Your color is an input, not the answer.

*Picture.* A left-to-right flow on the cream stage. A box 'fragment()' emits a small card of five monospace chips (ALBEDO, ALPHA, EMISSION, ROUGHNESS, METALLIC) labelled 'surface'. The card travels into a box 'Godot's lighting'. Two lamp icons drop beams into the same box from above. A single teal pixel (a small outlined square) comes out on the right. All arrows are drawn shapes that point only forward.

*Motion.* A surface card enters Godot's lighting, two lamps feed it from above, and one pixel comes out.

*Lane.* manim · `B13_LitPipeline` · runner-up: DesignPipelineClaim, show-tell isometric

### B14 · 29 words · ~10 s

> Sometimes you want no lighting. Add a second line: render mode unshaded. Now the result is only albedo, and the lamp is ignored. Watch the lit sphere beside it.

*Picture.* Left: the six-line shader with line 2, `render_mode unshaded;`, focused and tagged (docs wording: 'render mode: alters the way Godot applies the shader'). Right: a real render of two spheres under the same turning lamp: the lit one on the left keeps changing, the unshaded one beside it stays one flat teal. Labels: 'lit', 'unshaded'.

*Motion.* One sphere keeps changing as the lamp turns; the one beside it never changes.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace

*Capture to record.* C04: custom scene 'lamp' (S3), two spheres: lit 02-flat-teal-3d at x -0.7 and unshaded 07-flat-teal-3d-unshaded at x +0.7, orthographic size 2.4, same lamp turn, 14 s, Forward+.

### B15 · 29 words · ~10 s

> Why choose unshaded? No lamp can change the color, so a flat, graphic look stays flat. Godot's docs add that skipping the lighting makes the surface faster to render.

*Picture.* The real Godot 4.7 'Spatial shaders' page, Render modes table, in a browser window; the camera pushes in on the row for unshaded ('Result is just albedo. No lighting/shading happens in material, making it faster to render.') and one terracotta ring marks it. The ring box is an estimate: recompute it from the real capture.

*Motion.* The camera pushes in on the unshaded row the voice is describing.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: the sentence with the word unshaded highlighted

### B16 · 34 words · ~12 s

> You can write the light function yourself. Then your function replaces Godot's lighting for that surface. An empty one is a trap: the lamp stops working. The sphere stays dim, whatever the lamp does.

*Picture.* Left: the eight-line shader with its empty `void light() { }` focused and tagged (GLOSSARY wording: 'light(): runs once per pixel for each light that touches it', then 'replaces the default lighting, even when empty'). Right: a real render of three spheres under the same turning lamp: lit (changing), unshaded (flat) and the one with the empty light() function: it stays dim and flat, ignoring the lamp. Labels: 'lit', 'unshaded', 'own light()'.

*Motion.* The third sphere stays dim however the lamp turns.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace

*Capture to record.* C05: custom scene 'lamp' (S3), three spheres at x -1.15 / 0 / +1.15: 02-flat-teal-3d, 07-flat-teal-3d-unshaded, 08-flat-teal-3d-empty-light; orthographic size 2.8; same lamp turn; the clip is as long as the beat; Forward+. Verified: the empty-light sphere reads the same dim value as the lit sphere with the lamp off.

### B17 · 36 words · ~12 s

> Another trap. A three-D surface has two sides, and by default only the front is drawn. Turn a flat square around and it vanishes. Add cull disabled to the render mode line, and both sides draw.

*Picture.* Left: the six-line shader with `render_mode unshaded, cull_disabled;` focused and tagged 'cull_disabled: draw both sides of a surface'. Right: a real render of two flat teal squares turning once about the vertical axis: the left one (default culling) blinks out while its back faces the camera, the right one (cull disabled) is always there. Labels: 'default', 'cull disabled'.

*Motion.* The left square vanishes while its back faces the camera; the right square never does.

*Lane.* capture · `ShaderLab` · runner-up: manim quad flipping

*Capture to record.* C06: custom scene 'turnaround' (S4): two QuadMesh 1.2 x 1.2 at x -0.85 (07-flat-teal-3d-unshaded) and x +0.85 (09-two-sided), both turning about Y from 0 to 360 deg across the first 0.8 of the clip, then held at 360 deg (scripted; 225 deg at the 50 % mark, about 310 deg at the cull_disabled cue, front-facing at 85 %), orthographic size 2.4, camera at z = 5, Forward+. Verified: default shows the stage colour at yaw 120, 180, 240.

### B18 · 42 words · ~14 s

> So when a three-D shader looks wrong, ask two quick questions. Is a lamp changing my color? Add unshaded and see. Is the back side being skipped? Add cull disabled and see. Godot's docs list many more modes, such as blend add.

*Picture.* A small decision sketch. At the top a teal square labelled 'looks wrong'. Two branches go down. Left: a lamp icon with a question mark leads to a shaded sphere that turns flat, tagged 'add unshaded'. Right: a flat square seen from behind (empty outline) leads to the same square filled, tagged 'add cull disabled'. A dot travels down each branch in turn; a third tag 'blend add' appears faint at the side with the caption 'more modes in the docs'.

*Motion.* A dot travels down each branch and lights its remedy tag.

*Lane.* manim · `B18_TwoChecks` · runner-up: LectureEvidenceTable

## Act III: A Surface That Changes

### B19 · 36 words · ~12 s

> Now build a surface that changes. Start from a picture you already know: the address as a color. On a flat square, the corners read dark, red, green and yellow. The top left is zero, zero.

*Picture.* Act title 'A Surface That Changes' (serif 40) top-left. Left: the six-line UV-colors shader with its ALBEDO line focused. Right: a real Godot render of a flat square, red across and green down. Corner labels land in the order the voice says them: 'dark' (top left), 'red' (top right), 'green' (bottom left), 'yellow' (bottom right).

*Motion.* The four corner labels land on the corners in the order the voice names them.

*Lane.* capture · `ShaderLab` · runner-up: manim uv_square from the kit

*Capture to record.* C07: scene S5 face-on square (QuadMesh 1.8 x 1.8, orthographic size 2.0 at z = 3; the square fills 90 % of the frame height and the middle 51 % of its width), lab-shaders/06-uv-colors-3d.gdshader, still PNG 3840 x 2160, Forward+. (The Lab's own quad3d fills the whole 16:9 frame: a wide rectangle, not the square the voice says.) Corner probes (0.02/0.98 of the quad): dark (0.149, 0.157, 0), red (0.992, 0.157, 0), green (0.149, 0.988, 0), yellow (0.992, 0.988, 0).

### B20 · 27 words · ~9 s

> Keep only the across part, x. It is a ramp: a smooth run of values from zero up to one. Everything that follows starts from that ramp.

*Picture.* The kit's uv_square (0 to 1 axes, the second axis pointing DOWN) at left, small. Its x axis lights up. Beneath the square a ramp strip in greys grows from the left edge (end labels '0' and '1'); a terracotta dot crosses the square from left to right and a marker rides the strip in step. Caption, GLOSSARY wording: 'ramp: a smooth run of values from 0 up to 1'. Greys only, no near-black field.

*Motion.* A dot crosses the square and its x value rides the strip from 0 to 1.

*Lane.* manim · `B20_Ramp` · runner-up: ShaderLab ramp strip

### B21 · 35 words · ~12 s

> Multiply x by eight and the ramp runs from zero to eight. Fract keeps the part after the decimal point, so it starts over at zero at every whole number: eight ramps in a row.

*Picture.* Three stacked strips on the cream stage: 'x' (the ramp, 0 to 1, greys), 'x × 8' (the same strip relabelled 0 to 8 with eight tick marks) and 'fract(x × 8)' drawn as a sawtooth plot with eight teeth, settled by 0.45, with a terracotta dot waiting at its start until 0.56 and then travelling along it, snapping back to zero at every whole number; under the plot, a strip of eight repeated grey ramps. Caption, GLOSSARY wording: 'fract(x): the part after the point: x minus floor(x)', and under it the one-line gloss of the word it uses, GLOSSARY wording: 'floor(x): rounds down to the whole number below'. Double the space at the fused boundary of 'x × 8' and look at the still.

*Motion.* The strip stretches to eight, then the dot traces a sawtooth with eight teeth.

*Lane.* manim · `B21_FractRamp` · runner-up: plot() alone

### B22 · 40 words · ~14 s

> Step turns a ramp into a switch. Step of point five and x gives zero when x is below one half, and one from one half up. Feed it the repeating ramp and it switches on and off eight times.

*Picture.* The sawtooth plot (eight teeth) with a horizontal threshold line at 0.5. Under it the output plot of step(0.5, ·): a square wave with eight high and eight low segments. A terracotta dot travels along the sawtooth; each time it crosses the threshold the lower plot flips and a small spark flashes. At the bottom, a strip in two greys (light and dark stripes) fills in as the dot passes. Caption (docs wording): 'step(edge, x): 0 below the edge, 1 from the edge up'.

*Motion.* Every time the dot crosses the threshold the lower plot flips and a stripe appears.

*Lane.* manim · `B22_StepSwitch` · runner-up: ShaderLab

### B23 · 34 words · ~12 s

> Put both in a shader. Stripe is step of point five and fract of eight x: zero or one. Scale that into two greys and you get eight dark stripes and eight light ones.

*Picture.* Left: the seven-line stripes shader, line 5 (the stripe) focused with a tag for step and then a tag for fract (GLOSSARY wording), then line 6 (ALBEDO) focused. Right: a real Godot render of the Lab's full-frame flat quad (a wide rectangle) with eight dark grey and eight light grey vertical stripes, a dark one first. Labels: '8 dark' and '8 light' land under the picture.

*Motion.* The focus moves from the stripe line to the albedo line while the label counts land.

*Lane.* capture · `ShaderLab` · runner-up: manim strip stack

*Capture to record.* C08: Lab render, lab-shaders/10-stripes-grey.gdshader, still PNG 3840 x 2160, Forward+. Verified: 16 stripes, 8 dark and 8 light, dark first; dark centre (UV.x 0.03125) reads 0.584, light centre (0.09375) reads 0.953.

### B24 · 39 words · ~13 s

> Mix blends two values. At zero you get the first, at one you get the second, and in between you get a blend. Mix of a, b and t is a times one minus t, plus b times t.

*Picture.* Two strips: 't' (0 to 1) above, and 'mix(a, b, t)' below running from a = 0.2 to b = 0.8, each with a terracotta dot. The dot on t slides from 0 to 1 and the dot below slides from 0.2 to 0.8 in step; the end values 0.2 and 0.8 are labelled. Caption from the first frame, GLOSSARY wording: 'mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b'; a formula caption lands with the voice's 'Mix of a': 'a × (1 − t) + b × t'. Greys only. It is plain numbers on purpose: no colors, so no renderer is implied.

*Motion.* The two dots slide together: t from 0 to 1, the blend from a to b.

*Lane.* manim · `B24_MixLine` · runner-up: LectureEvidenceTable

### B25 · 33 words · ~11 s

> Give mix a dial. A uniform is a value your game sets from outside, the same for every pixel. Call this one activation, from zero to one. Now one number blends two colors.

*Picture.* Left: the ten-line mix-dial shader: the ALBEDO = mix line focused on 'Give mix a dial', the activation uniform line focused while the uniform is defined (the caption carries the definition), then the mix line again on 'Now one number'. Right: a real render of the Lab's full-frame flat quad sweeping from rust to green as activation goes 0 to 1, with a thin 0 to 1 strip under it and a marker riding the value. Caption, GLOSSARY wording: 'uniform: a value your game sets from outside; every pixel sees the same one'.

*Motion.* The surface slides from rust to green while a marker rides the 0 to 1 strip.

*Lane.* capture · `ShaderLab` · runner-up: manim two colors and a slider

*Capture to record.* C09: Lab-style render, lab-shaders/11-mix-dial.gdshader on quad3d, activation 0 to 1 across the whole clip (scripted sweep; the clip is as long as the beat), 30 fps, Forward+. Frame at 50 % reads activation 0.5 (0.298, 0.537, 0.380), at 85 % reads 0.85. Verified: a uniform is the same at every pixel (three probes equal).

### B26 · 35 words · ~12 s

> The word after the colon is a hint. It tells Godot how to treat the uniform. Hint range keeps the dial between zero and one in the editor. Source color says this is a color.

*Picture.* A two-row table pairing each hint with what it tells Godot; the table's note line carries the GLOSSARY definition word for word: 'hint: the word after a colon that tells Godot how to treat a uniform', then the docs page. Each row lands on its words.

*Motion.* Each row lands and is ringed on its words.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: editor frames of the Inspector

### B27 · 33 words · ~11 s

> From the game, one line turns the dial. Take the mesh instance's material override, then call set shader parameter with the dial's name and a value. The name must match exactly, capitals included.

*Picture.* Left: a one-line GDScript card, `$Pad.material_override.set_shader_parameter("activation", 1.0)`. Right: a real render of the striped rust square that jumps to flat green the instant the highlighted call fires. The line is tagged '$Pad: the node named Pad, the pad's mesh instance'. Readout under the square: 'activation = 1'.

*Motion.* The square jumps from striped rust to flat green when the highlighted line fires.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace

*Capture to record.* C10: scene 'set from code' (S5): lab-shaders/12-signal-pad.gdshader on a MeshInstance3D named Pad holding a QuadMesh 1.8 x 1.8, with a ShaderMaterial as its material_override; at 0.34 of the clip the scene script runs the shown line (activation 0 to 1; --call-at); the clip is as long as the beat; 30 fps; Forward+. The 50 % and 85 % frames are flat green.

### B28 · 29 words · ~10 s

> Change the value every frame, or tween it, and the surface animates. Set the starting value first. A tween cannot start from a dial the code has never set.

*Picture.* Left: a three-line GDScript card (set the start value, create the tween, tween the property). Right: a real render of the rust square that slides smoothly to green over two seconds. Caption, GLOSSARY wording: 'tween: Godot's way to change a value smoothly over time from GDScript'. Line 1 is tagged 'material: the pad's ShaderMaterial'; a readout 'set first' lands with it.

*Motion.* The square slides smoothly to green while the tween lines are focused.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C11: scene 'set from code' (S5): at 0.04 of the clip `set_shader_parameter("activation", 0.0)`; at 0.19 the tween to 1.0 starts and keeps the 2.0 s the code shows (--set-at, --call-at); the clip is as long as the beat; Forward+. Verified (verify3 TWEEN): red 0.4 at the start, (0.298, 0.541, 0.384) about a second into the tween, flat green (0.122, 0.722, 0.522) at the end; a tween without the first line fails with 'The tweened property ... does not exist' (run 3b, kept).

## Act IV: Read a Real One

### B29 · 26 words · ~9 s

> Here is the whole pad shader again, ten lines. You know every ingredient now. Read it like a recipe, top to bottom, while the pad charges.

*Picture.* Act title 'Read a Real One' (serif 40) top-left. The ten-line pad shader on the code card at left, no line focus; at right the same real render as the opening: the flat square charging from striped rust to flat green.

*Motion.* The square charges while the whole shader waits to be read.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C01 again (pad-angled-sweep.mp4).

### B30 · 22 words · ~8 s

> Line one: spatial, a three-D surface. Line two: render mode unshaded. No lamp can change this pad's color, whatever the light does.

*Picture.* Left: the ten-line pad code with line 1 then line 2 focused. Right: a real render of the pad face-on at activation 0.3 (held still; the stripes are visible there, see stripe-contrast.txt). Readout on the render when line 2 is focused: 'no lamp'.

*Motion.* The focus steps from line 1 to line 2 on their names.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C13: Lab render, lab-shaders/12-signal-pad.gdshader at --set activation=0.3, still 3840 x 2160, Forward+. Verified light stripe (0.345, 0.435, 0.306), dark stripe (0.282, 0.428, 0.302): a color difference of 5.7 (CIE76), the dark stripe 52 RGB from the ink color.

### B31 · 28 words · ~10 s

> Lines three to five are three dials. Activation, from zero to one. And two colors, rust and green, each marked source color, so Godot knows they are colors.

*Picture.* Left: the pad code with lines 3 to 5 focused, then line 3 alone, then lines 4 and 5 tagged 'rust at activation 0, green at activation 1' and, as the voice says 'each marked source color', 'source_color: this vec4 is a color'. Right: the same held render (no color readouts: the held picture is the olive blend at 0.3, so 'rust' and 'green' belong on the code lines that hold them).

*Motion.* The focus narrows to the activation line, then to the two color lines, which are tagged in turn.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C13 again (pad-face-held.png).

### B32 · 31 words · ~10 s

> Fragment runs once for each pixel the pad covers. Its first line makes the stripe: step of point five and fract of eight x. Zero, one, zero, one, across the pad.

*Picture.* Left: the pad code with line 6 (tagged with the GLOSSARY wording for fragment()) then line 7 focused. Right: the held render; a terracotta ring (grey-backed) hops across the first four stripes, one stripe per spoken number in 'zero, one, zero, one'.

*Motion.* The ring hops across the first four stripes as the voice counts them.

*Lane.* capture · `ShaderLab` · runner-up: manim strip stack

*Capture to record.* C13 again (pad-face-held.png).

### B33 · 34 words · ~12 s

> Next, base. It is the rust color, multiplied by a mix: point six five on stripe zero, full strength on stripe one. Dot r g b keeps red, green and blue, and drops alpha.

*Picture.* Left: the pad code with line 8 focused; when the voice says 'dot r g b' the line is tagged (GLOSSARY wording: 'swizzle: picking or reordering a vector's parts: c.rgb'). Right: the held render with a ring on the first dark stripe and then on the first light stripe; readouts 'x 0.65' and 'x 1.0' land with them (multipliers in the code, not pixel ratios).

*Motion.* A ring moves from a dark stripe to a light stripe, carrying x 0.65 then x 1.0.

*Lane.* capture · `ShaderLab` · runner-up: manim two stripes with weights

*Capture to record.* C13 again (pad-face-held.png).

### B34 · 32 words · ~11 s

> The last line sets albedo: a mix from base to green, steered by activation. At zero it is the striped rust. At one it is flat green, and the stripes are gone.

*Picture.* Left: the pad code with line 9 (`ALBEDO = mix(base, active_color.rgb, activation);`) focused. Right: a real face-on render sweeping activation 0 to 1: the rust stripes fade into flat green; a thin 0 to 1 strip under it carries a marker. A readout 'stripes gone' lands at the end.

*Motion.* The stripes fade out as the marker reaches 1, and the surface ends flat green.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills at 0, 0.5 and 1

*Capture to record.* C12: Lab-style render of lab-shaders/12-signal-pad.gdshader on quad3d, activation 0 to 1 across the whole clip (scripted sweep; the clip is as long as the beat), Forward+. Verified at activation 1: dark and light stripes read the same (0.1216, 0.7216, 0.5216).

### B35 · 28 words · ~10 s

> Notice what is missing. There is no vertex function and no light function. Godot's default places the corners, and unshaded skips the lighting. The pad needs only fragment.

*Picture.* The pad's fragment function as a cream code box in the middle (the real lines 6 to 10, Menlo). Above it a dashed empty slot labelled 'vertex(): Godot's default', below it a dashed empty slot labelled 'light(): skipped by unshaded'. The dashes draw in, the two slots pulse once, and the fragment box gets a solid outline. All three slots share one alignment, as in the skeleton card from the first act.

*Motion.* Two dashed slots draw in around the one filled function.

*Lane.* manim · `B35_MissingSlots` · runner-up: ShaderLab

### B36 · 40 words · ~14 s

> In the game, this pad is not a flat square but a thin box. A box keeps its map in six pieces, so its top shows only about a third of the stripes. Same ten lines, different mesh, different picture.

*Picture.* Real Godot render, game camera angle: on the left a thin box (the pad's own shape), on the right a flat square, both wearing the same shader at activation 0.3 (stripes visible, stripe-contrast.txt). The box's top shows wide stripes (about six), the square shows sixteen narrow ones. Labels: 'thin box', 'flat square', then '6 stripes' and '16 stripes'.

*Motion.* The two surfaces wear the same colors but different stripes, side by side.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a box's six UV cells

*Capture to record.* C14: custom scene 'pad on its box' (S1): lab-shaders/12-signal-pad.gdshader on BoxMesh 1.55 x 0.10 x 1.55 at x -1.1 and on QuadMesh 1.55 x 1.55 lying flat at x +1.1, orthographic size 3.2 from (5.8, 9, 11), activation held at 0.3, the clip as long as the beat, Forward+. Verified: flat quad 16 stripes, box top 6 stripes (activation 0); at size 3.2 the two fill x 0.15 to 0.85 and y 0.20 to 0.78 of the frame.

## Act V: Which Renderer?

### B37 · 29 words · ~10 s

> Now run the same pad in two of Godot's three renderers: Forward Plus on the left, Compatibility on the right. Same file, same activation, no lamp. Watch the greens.

*Picture.* Act title 'Which Renderer?' (serif 40) top-left. A real two-pane render: the same pad file charging face-on from activation 0 to 0.7 (done by 0.44 of the clip) and then held there, Forward+ on the left, Compatibility on the right, in step. Labels: 'Forward+' above the left pane, 'Compatibility' above the right. Once they stop the greens differ visibly: the left is the lighter green.

*Motion.* Two squares charge side by side and stop on two different greens.

*Lane.* capture · `ShaderLab` · runner-up: two stills

*Capture to record.* C15: two harness runs of lab-shaders/12-signal-pad.gdshader on quad3d, one with --renderer forward_plus and one with --renderer gl_compatibility, activation 0 to 0.7 across 0 to 0.44 of the clip, then held at 0.7, in both (the clip is as long as the beat), 30 fps, joined side by side (ffmpeg hstack) into one 3840 x 2160 video, each pane 1920 x 2160 scaled to fit the pane. 50 % and 85 % frames: activation 0.7, where the Compatibility dark stripe is well clear of the ink color (it is not below about 0.5).

### B38 · 31 words · ~10 s

> They do not match. At half charge, the green channel of a light stripe reads point five four in Forward Plus, and point four four in Compatibility. Measured on this Mac.

*Picture.* The same two panes held at activation 0.5. A terracotta ring (grey-backed) marks the first light stripe in the left pane, then in the right pane, with a readout beside each: 'G 0.54' and 'G 0.44'. Caption, GLOSSARY wording, there from the first frame: 'channel: one of red, green, blue or alpha'. Credit line: 'Apple M4 Pro · Godot 4.7.2'.

*Motion.* A ring and a number land first on the left stripe, then on the right.

*Lane.* capture · `ShaderLab` · runner-up: LectureEvidenceTable, two rows

*Capture to record.* C16: the two renderers held at activation 0.5: Forward+ light stripe (0.298, 0.537, 0.380), Compatibility (0.259, 0.439, 0.306) at UV.x 0.09375; composite as C15.

### B39 · 34 words · ~12 s

> Neither is a bug. Take the plainest case: an albedo of one half, unshaded. Forward Plus draws point seven four. Compatibility draws point five. In two-D, the same number draws point five in both.

*Picture.* Two big grey swatches, real Lab renders of lab-shaders/14-grey-3d.gdshader: Forward+ on the left (the lighter grey), Compatibility on the right (the mid grey). Readouts '0.74' and '0.50' land on them, then a third small readout '2D: both 0.50' below.

*Motion.* The lighter swatch and the mid swatch land with their numbers.

*Lane.* capture · `ShaderLab` · runner-up: manim swatches drawn from the numbers

*Capture to record.* C17: Lab stills of lab-shaders/14-grey-3d.gdshader (--renderer forward_plus, --renderer gl_compatibility), side by side with labels. Verified: Forward+ 0.7373, Mobile 0.7373, Compatibility 0.502; 2D COLOR 0.5 reads 0.502 in all three.

### B40 · 35 words · ~12 s

> Forward Plus treats albedo as linear light, then converts it to s R G B for your screen. The curve lifts the dark and middle values. Compatibility skips that, so a half stays a half.

*Picture.* Two horizontal lanes. Top lane 'Forward+': the number chip 0.5 enters, passes a block labelled 'linear to sRGB' (the arrows between the parts are drawn shapes, never a glyph), and leaves as 0.74. Bottom lane 'Compatibility': the same chip passes straight through and leaves as 0.50. Above the lanes a small plot: the diagonal y = x and the screen curve (the standard one that lifts dark and middle values); a dot at x = 0.5 rises to 0.74 on the curve and stays at 0.50 on the diagonal. Two captions, GLOSSARY wording, there from the first frame: 'linear: the scale light adds up on, in a straight line' and, under it, 'sRGB: the scale a color picker's numbers use, spaced for the eye'. Credit: 'measured · Apple M4 Pro · Godot 4.7.2'.

*Motion.* The same chip comes out lighter in one lane and unchanged in the other.

*Lane.* manim · `B40_TwoLanes` · runner-up: plot() alone

### B41 · 36 words · ~12 s

> That moves a mix too. The pad's colors are marked source color, so Forward Plus turns them into linear light first, blends there, then converts back. Compatibility blends the numbers as written. One dial, two midpoints.

*Picture.* A number line for the red channel of the pad's two colors: rust 0.40 at the left end, green 0.12 at the right end. A terracotta dot slides between them. At the middle two markers drop: 'as written 0.26' (labelled 'Compatibility') and 'in linear light 0.30' (labelled 'Forward+'), with a small gap between them. A tag by the two ends, GLOSSARY short form for a label, lands as the voice says 'marked source color': 'source_color: numbers are sRGB: convert to light first'. Credit: 'measured 0.26 and 0.30 · Apple M4 Pro · Godot 4.7.2'. Greys and the one terracotta only.

*Motion.* The dot slides to the middle and two different midpoints drop, a small gap apart.

*Lane.* manim · `B41_TwoMidpoints` · runner-up: ShaderLab

### B42 · 36 words · ~12 s

> Godot even lets a shader ask. A three-D shader can read a value called output is s R G B: true in Compatibility, false in Forward Plus and Mobile. The documentation says so in one line.

*Picture.* The real Godot 4.7 'Spatial shaders' page, Global built-ins table, in a browser window; the camera pushes in on the row `in bool OUTPUT_IS_SRGB` ('true when output is in sRGB color space (this is true in the Compatibility renderer, false in Forward+ and Mobile)') and one terracotta ring marks it. The ring box is an estimate: recompute it from the real capture.

*Motion.* The camera pushes in on the OUTPUT_IS_SRGB row the voice is reading.

*Lane.* remotion · `BrowserCapture` · runner-up: ShaderLab of a shader that paints red or blue by renderer

### B43 · 33 words · ~11 s

> Which renderer is yours? Open Project Settings, then Rendering, Renderer. Rendering Method shows it, and changing it there needs Save and Restart. Switching can change how a scene looks, so test again afterwards.

*Picture.* Four real frames of the Godot editor (a scripted editor session), joined by cross-dissolves: the Project menu open with Project Settings... ringed; the Project Settings dialog on Rendering, Renderer, with the Renderer entry in the left tree and then the Rendering Method row (forward_plus) ringed; the Rendering Method menu open with its three entries forward_plus, mobile, gl_compatibility ringed; then the dialog's note 'Changed settings will be applied to the editor after restarting.' with the Save & Restart button ringed. The ring moves as the voice names each step.

*Motion.* The ring moves from the Project menu to the Renderer page, the Rendering Method row, the three entries and Save & Restart.

*Lane.* editor · `ShaderLab` · runner-up: BrowserCapture of the docs page (the first plan: its sentence about the renderer name in the upper right corner)

*Capture to record.* E1 (DONE by script, 2026-10-13, editor driver; README section 11): four full frames from `_godot-shaders-series/editor-capture/png/1920x1080/renderer-path/` (native 3456x1944 twins in png/3456x1944/renderer-path/): renderer-path_R1-A_Project-menu-open, R1-C_Project-Settings_Rendering-Renderer_menu-closed, R1-D_Project-Settings_Rendering-Method_menu-open, R1-E_Project-Settings_restart-note. Cross-dissolves at the `show` fractions (R1-A to R1-C, then 0.42 to R1-D, then 0.56 to R1-E); ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels, read from the live UI: menu Project > Project Settings...; dialog 'Project Settings (project.godot)'; left tree Rendering > Renderer (a second page named Rendering sits under Internationalization: not that one); rows 'Rendering Method' (forward_plus), 'Rendering Method.web', 'Rendering Method.mobile'; the dropdown lists forward_plus, mobile, gl_compatibility; after a change the note 'Changed settings will be applied to the editor after restarting.' with Save & Restart and X. Save & Restart was never pressed. The editor draws its own menu bar inside the window (Use Embedded Menu on): label the clip 'scripted editor session'. NOT used: the title-bar frames R3-A, R3-B and the OFF-vs-ON composite (the docs say the renderer's name always sits in the editor's upper right corner; in 4.7.2 it is hidden until Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector is on).

### B44 · 37 words · ~13 s

> So a pixel you read is true for one renderer. When you test a shader, or ask an AI to, name the renderer. A number from the wrong one is a correct measurement of the wrong picture.

*Picture.* The two held panes again. A ring moves from the left pane to the right pane as the voice says 'one renderer' then 'the wrong one'. Caption at the end: 'a pixel is true for one renderer'. Labels 'Forward+' and 'Compatibility' stay above the panes.

*Motion.* A ring hops from the left pane to the right pane.

*Lane.* capture · `ShaderLab` · runner-up: manim card with the sentence

*Capture to record.* C16 again (pad-two-renderers-half.png).

## Closing

### BVDT · recap · 91 words · ~31 s

> Let's recap with Claude. A three-D shader has the same shape as a two-D one, with new names. Albedo is the base color, and the address comes from the mesh. Surfaces are lit by default, and unshaded gives you the albedo with no lamp. Fract, step and mix cut stripes and blend colors, and a uniform lets the game steer. The pad is ten lines: a type, a mode, three dials, a stripe, a base and a blend. A pixel is true for one renderer, so name it when you test.

*Picture.* The recap card: A three-D shader has the same shape as a two-D one, with new names. / Albedo is the base color, and the address comes from the mesh. / Surfaces are lit by default, and unshaded gives you the albedo with no lamp. / Fract, step and mix cut stripes and blend colors, and a uniform lets the game steer. / The pad is ten lines: a type, a mode, three dials, a stripe, a base and a blend. / A pixel is true for one renderer, so name it when you test.

### BHTF · your turn · 94 words · ~32 s

> Your turn. Paste this into Claude: Write a Godot spatial shader for a mesh instance, with render mode unshaded. Give it one float uniform called charge, from zero to one, and two color uniforms marked source color. Paint eight stripes in the first color using step and fract on the U V address, and mix toward a plain second color as charge rises. Then tell me which renderer your colors assume. Then check two things yourself. At charge one, are the stripes gone? And when you switch the renderer, does the half-charge color change?

*Prompt shown and read in full:* Write a Godot spatial shader for a mesh instance, with render mode unshaded. Give it one float uniform called charge, from zero to one, and two color uniforms marked source color. Paint eight stripes in the first color using step and fract on the U V address, and mix toward a plain second color as charge rises. Then tell me which renderer your colors assume.

*Two checks:* Check: at charge one, the stripes are gone. · Check: switch the renderer. Does the half-charge color change?

### BOUT · outro · 8 words · ~4 s

> Shaders in three D. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


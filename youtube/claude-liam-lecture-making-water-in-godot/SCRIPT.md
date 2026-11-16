# Script: Making Water in Godot

**What this is.** The words Liam will say in *Making Water in Godot*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 55 beats, 2134 words, about **12:10** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 36, manim 9, remotion 3, terminal 1.

**If it runs long.** Cut, in this order: the renderer-ripples beat (B33: a repeat of the renderer lesson in B09), the power-curve pair (B22 and B23: an alternative to the edge line, with its trap), the baked-texture beat (B24), the sorting and cost beats (B11 and B12: docs only, nothing is measured), and the built-ins-in-a-function beat (B45: a compile error, not the main line). The blend arithmetic (B08, B09), the noise net (B14 to B19), the normal map (B25 to B28), the real waves (B35 to B39) and the shore (B42 to B44, B46) stay: they are the arc.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Blue and Clear | 12 | 464 | ~2:38 |
| II | Foam | 12 | 427 | ~2:25 |
| III | Ripples | 9 | 325 | ~1:51 |
| IV | Real Waves | 8 | 289 | ~1:38 |
| V | The Shore | 8 | 305 | ~1:44 |

## Opening

### BOPEN · identity card · 38 words · ~13 s

> Making Water in Godot. Build a water shader one layer at a time, from flat blue to a see-through, foamy, wavy sea that knows where the shore is. By the end you can restyle it from the Inspector.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Making Water in Godot", and the line "Build a water shader, one layer at a time".

### BIDEA · the question · 44 words · ~15 s

> Hallo. This is Liam, in for Bear. Water in a game looks like it needs a physics simulation. It does not. It is one flat plane wearing a few small tricks, stacked one at a time, and each trick is only a few lines.

*Picture.* The hesitant writer types: "Making water needs
a water simulation." then deletes "a water simulation" and types "six small tricks".

### BDEFS · terms · 68 words · ~23 s

> Six terms before we start. A shader is a small program the graphics card runs to decide how something is drawn. A vertex is a corner point of a shape. A pixel is one dot of the picture. A texture is an image a shader can read by address. U V is a point's address on the shape. And the renderer is the part of Godot that draws.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Vertex** — a corner point of a shape; **Pixel** — one dot of the picture on screen; **Texture** — an image a shader can read by address; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Renderer** — the part of Godot that draws

## Act I: Blue and Clear

### B01 · 35 words · ~12 s

> This water is one shader on one flat square: blue, see-through, foamy, rippling, with real waves and a white edge at the shore. We will build it in six layers, each only a few lines.

*Picture.* Act title 'Blue and Clear' (serif 40) top-left; the finished water fills the framed window: blue and see-through over sand, a foam net, glints, rolling waves, a white shore line on the beach, the teal buoy and the cream crate riding the waves.

*Motion.* The waves roll and the buoy and crate rise and fall with them while the foam net drifts: the whole film's result before any code.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a wave

*Capture to record.* C01: scene water_scene.gd, shader 06-shore-foam, plane cut 127 x 127, iso camera, wave clock driven by the capture clock (W_FOLLOW), Forward+, the whole beat plus 1.0 s tail.

### B02 · 34 words · ~12 s

> A shader draws nothing alone. A mesh gives it a shape, here a flat plane. A material holds the shader, and the mesh node holds the material. Those three links are the whole setup.

*Picture.* Left to right on the cream stage: a flat isometric plane tile labelled 'PlaneMesh'; an outlined slot labelled 'Material Override' holding a round preview tile labelled 'ShaderMaterial'; a small code-card icon labelled 'shader'. An outline box labelled 'MeshInstance3D' encloses the plane and the slot. Arrow shapes link them in turn: mesh to node, material into the slot, shader into the material.

*Motion.* Three links draw in the order the voice names them, ending with the node holding the material.

*Lane.* manim · `B02_ThreeLinks` · runner-up: ShaderLab: a real Inspector frame from the editor driver

### B03 · 40 words · ~14 s

> Here is the first shader, all of it. Shader type spatial means it draws three D surfaces. Fragment runs once for each pixel the plane covers. Albedo is the base color: red, green and blue, each from zero to one.

*Picture.* Code card with all eleven lines of 01-blue.gdshader at left (three cue labels land on lines 1, 8 and 9); at right the real render: a pale unshaded-looking grey plane over the sand until 55 % of the beat, then the plane turns solid blue with the sun's glare.

*Motion.* A plain grey plane turns blue the moment the shader is assigned, while the three code lines light up.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: scene water_scene.gd, W_LATE: the water plane has no material until 55 % of the beat, then 01-blue.gdshader is assigned; iso camera, Forward+.

### B04 · 42 words · ~14 s

> Water color is a uniform: a value the game sets from outside. Source color gives it a color picker. In Forward Plus the numbers you type come out unchanged: point one, point four five, point seven reads twenty-five, one fifteen, one seventy-eight.

*Picture.* Code card with the uniform lines; the real cove whose water turns green-teal, then violet, then back to blue; the pill '25 115 178' lands when the default colour returns, with the caption naming the unshaded test.

*Motion.* The uniform is a dial: the colour changes three times without touching the code.

*Lane.* capture · `ShaderLab` · runner-up: manim: a typed colour and a pixel byte triple

*Capture to record.* C03: scene water_scene.gd, shader 01-blue, water_color set to green-teal at 35 %, violet at 62 %, back to the default 0.10, 0.45, 0.70 at 82 %. The 25, 115, 178 reading is the unshaded test E1 (evidence/planning-checks/RESULTS.md).

### B05 · 34 words · ~12 s

> Roughness runs from zero, a mirror, to one, fully matte. Watch the sun's reflection: it tightens and sharpens as roughness falls, and smears as it rises. Water is smooth, so we keep it low.

*Picture.* Code card (the four fragment lines, ROUGHNESS lit); the real cove with the sun's reflection: a wide soft smear at the start that shrinks to a tight bright oval as the ramp marker runs from 0.9 to 0.03.

*Motion.* The reflection tightens and sharpens as roughness falls.

*Lane.* capture · `ShaderLab` · runner-up: manim: a lobe shrinking

*Capture to record.* C04: scene water_scene.gd, shader 01-blue, roughness swept linearly from 0.9 to 0.03 across the beat.

### B06 · 37 words · ~13 s

> Right now it is solid plastic: the sea floor, the rocks and the buoy's underside are hidden. Write one line, alpha, and the surface turns see-through. Alpha is how visible a pixel is: zero invisible, one solid.

*Picture.* Code card with the stage-two fragment (ALPHA line lit); the real cove: a solid blue plane hiding the floor, then at 40 % the surface turns see-through and the sand, the rock and the buoy's underside appear under it.

*Motion.* One line is added and the sand and the rocks appear through the water.

*Lane.* capture · `ShaderLab` · runner-up: manim: a stack of layers

*Capture to record.* C05: scene water_scene.gd, solid 01-blue on the water, swapped (swap_shader) at 40 % of the beat for 02-transparent on the same material, opacity set to 1.0 then easing to 0.7.

### B07 · 36 words · ~12 s

> Opacity is another dial. At one, the water hides everything. At zero point three, it barely exists. Zero point seven shows the rocks and the floor and still reads as water, so that is our default.

*Picture.* Code card (fragment, ALPHA lit); the real cove going from hiding everything (1.0) through almost invisible (0.3) to the readable default (0.7); the pill shows the opacity at each hold.

*Motion.* The water fades from solid to almost gone and settles at point seven.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab ramp only

*Capture to record.* C06: scene water_scene.gd, shader 02-transparent, opacity 1.0 held to 20 %, down to 0.3 by 42 % (held to 56 %), up to 0.7 by 72 %.

### B08 · 41 words · ~14 s

> Each pixel is seventy percent water plus thirty percent of what is behind it. We checked one pixel, water over sand. The blend predicts one hundred eight, one twenty-nine, one sixty-one. The screen reads one hundred eight, one twenty-nine, one sixty-two.

*Picture.* Left: three flat swatches in the measured colours: water (25, 115, 178), sand (184, 157, 110) and a result swatch (108, 129, 162), joined by the sum '70 percent water plus 30 percent sand' drawn as two proportion bars. Under them two number rows: 'predicted 108, 129, 161' and 'screen 108, 129, 162'. Right: the real Forward+ test render (captures/blend-fp.png through lab_window) with one grey-backed terracotta ring on the probe point (plate over sand). Every number is a measured or computed figure from FACTCHECK.

*Motion.* The bars slide together into the result swatch and the two number rows land one under the other, differing by one in the last place.

*Lane.* manim · `B08_BlendArithmetic` · runner-up: ShaderLab with the test render and readouts

### B09 · 40 words · ~14 s

> But not the way you might compute it. Forward Plus blends in linear light, so mixing the typed numbers would predict seventy-three for red, not one hundred eight. Compatibility blends the typed numbers directly, so the same water reads seventy-one.

*Picture.* Two real test renders side by side (captures/blend-fp.png labelled 'Forward+', captures/blend-compat.png labelled 'Compatibility'), the probe point ringed in each; under them the red channel read: 108 and 71. A number line 0 to 255 under both shows two ticks, 'typed-number mix' at 73 and 'linear-light blend' at 108: the Compatibility reading sits on 73 and the Forward+ reading on 108.

*Motion.* The two readings drop onto the number line one after the other and snap to the tick they match.

*Lane.* manim · `B09_TwoRenderers` · runner-up: ShaderLab video of both renderers

### B10 · 39 words · ~13 s

> The render mode line is optional. These three are the defaults, written out. Blend mix means alpha is transparency. Depth draw opaque means the water does not write depth. Cull back draws only the top side of the plane.

*Picture.* Three rows, one per render mode in the shader's second line, each with the docs' own words in a second column; the row for the mode being spoken is highlighted.

*Motion.* The highlight steps down the table as the voice names each mode.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: BrowserCapture of the docs page

### B11 · 46 words · ~16 s

> Transparency has a price. Godot draws see-through objects after solid ones, sorted by each node's position, not pixel by pixel. This red plane lies under the water, but its node is nearer, so it draws on top. Let the water write depth, and it vanishes instead.

*Picture.* Code card with the two render_mode lines (the default first, depth_draw_always second); the real cove with a red see-through plane lying under the water yet painted over it at the bottom of the frame; at 78 % of the beat the plane vanishes and the water shows blue and clean there.

*Motion.* A red plane that should be under the water is painted on top of it, then disappears when the water is made to write depth.

*Lane.* capture · `ShaderLab` · runner-up: manim: the draw order drawn (kept in _superseded/)

*Capture to record.* C37: scene water_scene.gd, W_EXTRA=sort adds a red see-through plane (alpha 0.6) at y = -0.4 UNDER the water with its node origin nearer the camera; shader 02-transparent swapped at 78 % of the beat for 02a-depth-draw-always on the same material; iso camera, Forward+. Measured in evidence/planning-checks (E16): no render_mode line and the written defaults render pixel-identical; depth_draw_always hides the plane (56,099 pixels differ by more than 8 levels).

### B12 · 40 words · ~14 s

> The docs add two more costs. Transparent materials cast no shadows, and they never appear in the depth or screen textures other shaders read. The second one matters soon: the water will read depth to see what lies beneath it.

*Picture.* Three rows: casts shadows, appears in the depth texture, appears in the screen texture; each answered 'cannot' by the docs; the depth row also carries the measured gap of 0.500 m.

*Motion.* The rows light in the order the voice lists them, the depth row last and longest.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: Manim: a shadow and a depth strip

## Act II: Foam

### B13 · 39 words · ~13 s

> Foam needs noise, and Godot's shading language has none. No noise function, and no Voronoi node: we counted one hundred ten visual shader nodes in Godot four point seven point two, and none makes noise. So we write one.

*Picture.* Act title 'Foam' in the table heading; three rows: the shading language's function list (no noise function), the visual shader's 110 nodes (no Voronoi or noise node, only random range), and the FastNoiseLite resource (yes, a Cellular type).

*Motion.* Rows light one at a time; the first two answer 'none', the third 'yes'.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: LibraryIconRow of Godot nodes

### B14 · 31 words · ~10 s

> Here is the plan. Cut the surface into squares and put one point in each, at a random spot. Foam will live along the lines where two points are equally close.

*Picture.* A grid of six by four outline squares (the series pixel-grid cast) on the cream stage; one terracotta dot (grey-ringed) drops into each of the 24 squares at a different spot; then two neighbouring dots are joined by a thin line and a dashed grey line (the perpendicular bisector between them) is drawn with the label 'equally close'. Labels: 'one point each'. Drawn, not rendered: labelled 'drawing'.

*Motion.* Dots land one per square; then the line of equal distance grows between two neighbours.

*Lane.* manim · `B14_OnePointEach` · runner-up: ShaderLab: the real points render first

### B15 · 33 words · ~11 s

> A hash picks the spot. It turns a square's address into numbers that look random but never change for that square: a dot product, a sine, then fract, the part after the point.

*Picture.* Code card with the four hash lines (cues on dot, sine, fract); at right a real top view: pale squares with a grey grid and a small deep-blue dot in every square, the dots slowly circling.

*Motion.* A dot sits in every square and slowly circles; the same square always has its dot in the same place.

*Lane.* capture · `ShaderLab` · runner-up: manim: a hash drawn as a function box

*Capture to record.* C08: scene water_scene.gd, W_BARE top view of the plane, shader 03a-cells-debug show=0 (points and grid), cell_density 8, 1080 x 1080.

### B16 · 34 words · ~12 s

> A pixel can be closest to a point in a neighboring square, so check all nine squares around it: its own and the eight beside it. Keep the nearest distance, and the second nearest.

*Picture.* The grid from the last act's cast. One pixel (a small cream dot with a dark ring) sits near the border of a square. The 3 by 3 block of squares around it is outlined; the nine points inside are marked and nine thin lines run from the pixel to them; the nearest line is drawn thick, the second nearest medium; labels 'nearest' and 'second'.

*Motion.* The nine lines draw in, then all but two fade, leaving the nearest thick and the second nearest medium.

*Lane.* manim · `B16_NineSquares` · runner-up: ShaderLab with the loop highlighted

### B17 · 42 words · ~14 s

> Length of the offset is the distance to a point. The nearest distance is zero at a point and grows away from it, like a field of cones. On average a pixel is about forty-three hundredths of a square from its point.

*Picture.* Code card with the eight loop lines (length line then the keep-two line lit); at right a real top view: a field of soft cones, pale at every point and deepening away from it, slowly moving; the pill 'mean 0.43' lands near the end.

*Motion.* A field of cones: pale at each point, deepening away from it, while the points circle.

*Lane.* capture · `ShaderLab` · runner-up: manim: cone cross-section plot

*Capture to record.* C09: scene water_scene.gd, W_BARE top view, shader 03a-cells-debug show=1 (the nearest distance as a grey ramp), 1080 x 1080. mean 0.43 is E7 (evidence/planning-checks).

### B18 · 32 words · ~11 s

> The second nearest distance minus the nearest is zero exactly where two points are equally close: along the border between their territories. That thin dark line is where the foam will go.

*Picture.* Code card (the cells return and the fragment's first lines, the foam line lit); at right a real top view: deep-blue cells whose borders are a thin pale net, moving as the points circle.

*Motion.* Thin pale lines trace the borders between the cells and wobble as the points move.

*Lane.* capture · `ShaderLab` · runner-up: manim: two circles and their equal-distance line

*Capture to record.* C10: scene water_scene.gd, W_BARE top view, shader 03a-cells-debug show=2 (second minus nearest as a ramp), 1080 x 1080.

### B19 · 35 words · ~12 s

> Smooth step turns the thin line into a band of the width you choose, and mix paints foam color where the band is. At width point one, foam covers about thirteen percent of the water.

*Picture.* Code card (the fragment: foam line then ALBEDO line lit); at right the real top view of blue water whose thin pale lines swell into white foam bands as edge_width grows; the pill '13 % foam' lands at the end.

*Motion.* Thin lines swell into white bands as the width grows, and settle at thirteen percent of the surface.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab ramp of edge_width

*Capture to record.* C11: scene water_scene.gd, W_BARE top view, shader 03-noise-foam, edge_width 0.02 widening to 0.1 by 75 % of the beat; the 13 % figure is E7.

### B20 · 33 words · ~11 s

> Foam is not see-through, so alpha rises to one where foam is. And foam is matte, so roughness rises too. Without that, the sun's glare streaks along the foam lines like wet paint.

*Picture.* Code card (ALBEDO, ALPHA, ROUGHNESS lines); the real cove: at first the foam lines streak with the sun's glare like wet paint, then as foam_roughness rises the streaks fade to flat white.

*Motion.* The glare streaks along the foam lines die away as the foam turns matte.

*Lane.* capture · `ShaderLab` · runner-up: manim: a lobe on foam vs water

*Capture to record.* C12: scene water_scene.gd, shader 03-noise-foam, foam_roughness swept 0.15 to 0.9 between 15 % and 85 % of the beat.

### B21 · 33 words · ~11 s

> Now move it. Each point circles in place: a sine of time plus its own random start. Speed sets how fast they circle, and density sets how many squares fit across the plane.

*Picture.* Code card (the point's offset line and the call line lit in turn); the real cove: the foam net frozen, then breathing faster, then the cells shrinking as the density rises.

*Motion.* The net starts to breathe, speeds up, then the squares shrink.

*Lane.* capture · `ShaderLab` · runner-up: manim: a point circling in its square

*Capture to record.* C13: scene water_scene.gd, shader 03-noise-foam, cell_speed swept 0 to 2 between 30 % and 60 %, then cell_density 10 to 18 from 62 % to the end.

### B22 · 33 words · ~11 s

> There is another way to sharpen the pattern: one minus the nearest distance, raised to a power. A higher power shrinks the bright blob around each point. It reads as glitter, not foam.

*Picture.* Code card (the power-curve fragment, the pow line lit); the real top view of blue water with a soft white blob around every point that shrinks to a glitter dot as the power rises; pills 'power 2' then 'power 10'.

*Motion.* Soft white blobs shrink into glitter as the power rises.

*Lane.* capture · `ShaderLab` · runner-up: manim: the curve of one minus d to the power p

*Capture to record.* C14: scene water_scene.gd, W_BARE top view, shader 03b-power-curve (clamped), sharpness swept 2 to 10 across the beat, 1080 x 1080.

### B23 · 39 words · ~13 s

> It hides a trap. The nearest distance can pass one, so the base goes negative, and a power of a negative number is undefined: black specks. Here, four hundred sixty-two pixels went black. Clamp the base, and they vanish.

*Picture.* Code card (the two glow lines; the unclamped line lit then the clamp line); the real top view with tiny black specks that blink in the first half and are gone after the clamp at 55 %; a terracotta ring around one speck at 30 % and the pill '88 px'.

*Motion.* Black specks blink on the foam, then vanish when the clamp is applied.

*Lane.* capture · `ShaderLab` · runner-up: manim: a negative base on a number line

*Capture to record.* C15: scene water_scene.gd, W_BARE top view, shader 03b-power-curve unclamped (sharpness 5, cell_speed 0 so the pattern is frozen and the specks stay put), clamped by --set-at at 55 % of the beat; 1080 x 1080. Ring box = the 258-pixel speck at (221, 545) of the 1080 x 1080 frame (evidence/planning-checks/png/pow-static-broken.png).

### B24 · 43 words · ~15 s

> Godot can bake this net into a texture: a noise texture with Fast Noise Lite set to Cellular. One read instead of nine squares, but its points cannot move, it can only scroll. And Godot smudges a cross where it blends the tile.

*Picture.* Wide window with the two top views side by side: the function's crisp net (left) and the baked texture's net (right) with a visible smudge in the middle; code excerpt below (the two texture lines); pills '9 hashes' and '1 read'; a ring on the smudge.

*Motion.* The two nets drift side by side; the right one scrolls rigidly and the cells never change shape.

*Lane.* capture · `ShaderLab` · runner-up: manim: a texture tile and a function box

*Capture to record.* C16: scene water_scene.gd, W_BARE top view, left: 03-noise-foam (function), right: 03d-foam-from-texture (a baked cellular NoiseTexture2D: Cellular, return Distance2 Sub, fractal type None, Seamless), both 1080 x 1080 joined side by side. The ring box [0.595, 0.37, 0.735, 0.57] is the smudged cross where the seamless blend shows, read off the recorded frame at 10.5 s (72 % of the estimated beat); the cross scrolls with the texture, so re-read it if the beat length changes by more than a second.

## Act III: Ripples

### B25 · 40 words · ~14 s

> Foam on a flat sheet is still lit like a flat sheet. A normal map gives every pixel its own direction to face, so the sun meets a different slope at each point, and one big glare breaks into glints.

*Picture.* Act title 'Ripples'; code card (the 04a fragment, NORMAL_MAP lit); the real cove: first one big flat sun glare, then as the strength rises the glare breaks into thousands of small glints.

*Motion.* One big glare breaks into glints as the strength rises.

*Lane.* capture · `ShaderLab` · runner-up: manim: light on a flat and a bumpy line

*Capture to record.* C17: scene water_scene.gd, shader 04a-normal-map, ripple_strength swept 0 to 1.5 across the beat (one static normal map: a NoiseTexture2D, As Normal Map, Seamless).

### B26 · 39 words · ~13 s

> A normal map is an image where color is direction. Red leans left or right, green leans up or down, and blue is how upright. A flat pixel is half, half, one. The steepest pixel here leans thirteen degrees.

*Picture.* Left: the real normal map (captures/normal_a.png, 512 by 512, through lab_window) with two grey-backed rings on two pixels. Right: two swatches in the pixels' real colours: 'flat' (127, 127, 254) with an arrow pointing straight up, and 'leans' (124, 133, 254) with a slightly tilted arrow; a legend with three arrow shapes in the channel colours: 'left or right' (red), 'up or down' (green), 'upright' (blue); a number '13°' for the steepest pixel.

*Motion.* The two arrows draw from the swatches (one upright, one tilted) as the voice says flat and leans; the legend arrows draw with red, green, blue.

*Lane.* manim · `B26_ColorIsDirection` · runner-up: ShaderLab still of the texture

### B27 · 39 words · ~13 s

> You do not paint one. A noise texture wraps a Fast Noise Lite; switch on As Normal Map and Godot makes this image. Also switch on Seamless, or the tile edges show a jump fifty-three times a normal step.

*Picture.* Two real 2 by 2 tilings of the normal map side by side (captures/tiles-not-seamless.png labelled 'Seamless off', captures/tiles-seamless.png labelled 'Seamless on'), each with the tile-crossing lines marked by two thin grey lines; a ring on the visible jump in the left one. Under them the measured edge jump: '53 times a normal step' for off and 'about 1 time' for on; at the top the two switch names 'As Normal Map' and 'Seamless' as outlined chips.

*Motion.* The two chips light; the ring appears on the left tiling's seam; the numbers land under each picture.

*Lane.* manim · `B27_Seamless` · runner-up: ShaderLab with a tiling video

### B28 · 32 words · ~11 s

> In the shader, hint normal says the picture holds directions, not colors. Repeat enable lets the address run past one and wrap around. Without it, Godot stretches the edge pixels into streaks.

*Picture.* Code card (the group and the sampler line lit twice); the real cove: first long smeared streaks of glare across most of the water, then at 55 % the streaks resolve into fine ripples.

*Motion.* Long smeared streaks turn into fine ripples the instant repeat is enabled.

*Lane.* capture · `ShaderLab` · runner-up: manim: a tile with clamped edges

*Capture to record.* C19: scene water_scene.gd, shader 04e-no-repeat (repeat_disable) swapped at 55 % of the beat for 04b-scrolling-normals (repeat_enable), iso camera.

### B29 · 31 words · ~10 s

> Add time to the address and the ripples slide. Ripple speed is how far the address moves each second, and scale is how many times the image repeats across the plane.

*Picture.* Code card (the 04b fragment, the scrolled address line lit); the real cove: the glints drift steadily across the water in one direction.

*Motion.* The whole glitter pattern drifts one way across the water.

*Lane.* capture · `ShaderLab` · runner-up: manim: a window sliding over a tile

*Capture to record.* C20: scene water_scene.gd, shader 04b-scrolling-normals, iso camera, TIME runs from the capture start.

### B30 · 35 words · ~12 s

> One layer slides in a line, and you can see the repeat. So add a second layer, scaled differently, moving the other way, and average the two. Now the ripples cross and no direction wins.

*Picture.* Code card (the 04c fragment; the two address lines then the mix line lit); the real cove: one steadily drifting glint pattern, then after the swap the glints cross and shimmer with no single direction.

*Motion.* A steady drift turns into crossing shimmer when the second layer arrives.

*Lane.* capture · `ShaderLab` · runner-up: manim: two sliding windows

*Capture to record.* C21: scene water_scene.gd, shader 04b-scrolling-normals swapped at 50 % of the beat for 04c-two-layers, iso camera.

### B31 · 36 words · ~12 s

> Look from the water's edge. The glints move, but the edge of the plane is ruler straight: the same pixel row in every column. A normal map changes how light hits the water, never its shape.

*Picture.* The framed window shows a flat plane seen from just above the waterline: the glints and the foam net move across it, and the near and far edges stay ruler straight; a pill 'same row' sits on the near edge.

*Motion.* Everything on the plane moves; its edge never does.

*Lane.* capture · `ShaderLab` · runner-up: manim: a straight line over a bumpy normal

*Capture to record.* C22: scene water_scene.gd, W_BARE low camera (1.1 m above the water, fov 30), shader 04d-warped-foam, plane NOT cut; the near edge was measured at row 487 of a 1280 x 720 frame in every column (evidence/planning-checks).

### B32 · 36 words · ~12 s

> Now bend the foam. The normal map also says which way the surface leans, so shift the foam's address that way before measuring the cells. The net sloshes with the ripples. Warp strength is the dial.

*Picture.* Code card (the warp lines lit); the real cove: a straight-edged foam net that bends and sloshes with the ripples as the warp rises.

*Motion.* The foam lines bend and slosh as the warp rises.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grid bent by arrows

*Capture to record.* C23: scene water_scene.gd, shader 04d-warped-foam, warp_strength swept 0 to 0.4 across the beat, iso camera.

### B33 · 37 words · ~13 s

> Check every renderer you ship. The same water on the same clock reads one hundred thirty-two for red in Forward Plus and one hundred in Compatibility: bluer, more saturated. The shader is identical; the pictures are not.

*Picture.* Wide window: two identical scenes side by side, both moving on the same clock: left Forward+ (a lighter, greyer blue), right Compatibility (a deeper, more saturated blue); pills 'red 132' and 'red 100'.

*Motion.* Both scenes ripple in step; the right one is a deeper blue.

*Lane.* capture · `ShaderLab` · runner-up: manim: two swatches

*Capture to record.* C24: scene water_scene.gd, shader 04d-warped-foam, iso camera, recorded twice (Forward+ and Compatibility) at 1080 x 1080 and joined side by side. The medians (132, 163, 204 against 100, 158, 205) are E15, measured on a top view of the bare plane at the same clock (evidence/planning-checks/logs/e15-renderers-ripples.txt).

## Act IV: Real Waves

### B34 · 39 words · ~13 s

> Normal maps fake the light. To move the water itself, move its vertices. A plane has four. Cut it a hundred twenty-seven times each way and it has sixteen thousand six hundred forty-one: two more than the cuts, squared.

*Picture.* Act title 'Real Waves'; two framed views of the same wave shader from just above the waterline: the uncut plane only tilts (straight edges), the cut plane rolls with real waves; pills '4 vertices' and '16,641 vertices'.

*Motion.* The left plane tilts like a board; the right plane rolls like water.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dot grid counting up

*Capture to record.* C25: scene water_scene.gd, W_BARE low camera, shader 05-vertex-waves (TIME): left an UNCUT plane, right cut 127 x 127; both 1080 x 1080 joined. Vertex counts are read from the mesh (facts1_classdb.gd: 4, 25, 4225, 16,641).

### B35 · 35 words · ~12 s

> A wave is a sine of position minus speed times time. Two waves, in different directions and lengths, make the surface lumpy. The function returns the height, and the slope along x and along z.

*Picture.* Code card with the last six lines of wave() (the phase line, the sine line and the return line lit in turn); the real low view of the plane with a lumpy rolling surface.

*Motion.* Two waves of different lengths roll through each other.

*Lane.* capture · `ShaderLab` · runner-up: manim: two sines adding

*Capture to record.* C26: scene water_scene.gd, W_BARE low camera, shader 05-vertex-waves cut 127, TIME from the capture start.

### B36 · 31 words · ~10 s

> In vertex, add that height to each vertex's y. One line moves sixteen thousand corners, and the graphics card fills in everything between them. Time passes in, and the surface rolls.

*Picture.* Code card (the vertex function; the wave call then the add-to-y line lit); the real cove with rolling waves: the shoreline against the beach wobbles, the floaters stay at y 0.

*Motion.* The water surface rolls and the shoreline wobbles.

*Lane.* capture · `ShaderLab` · runner-up: manim: vertices rising and falling

*Capture to record.* C27: scene water_scene.gd, shader 05-vertex-waves cut 127, iso camera, TIME from the capture start; floaters not following (still).

### B37 · 35 words · ~12 s

> But the light does not know the surface moved. Leave the normal alone and the glare stays one flat oval. Compute the normal from the slope, and the glare breaks into glints on the crests.

*Picture.* Code card (the vertex function, NORMAL line lit); the real cove with rolling waves: first the sun's glare is one flat oval whatever the waves do, then after 55 % it breaks into glints along the crests; pills 'old normal' and 'new normal'.

*Motion.* The one flat glare shatters into crest glints when the normal line arrives.

*Lane.* capture · `ShaderLab` · runner-up: manim: normals drawn on a wave

*Capture to record.* C28: scene water_scene.gd, W_FOLLOW, shader 05c-no-normal-update (NORMAL line removed) swapped at 55 % for 05b-synced-clock; ripples and foam turned down (ripple_strength 0, edge_width 0.01) so the glare is the only light effect.

### B38 · 33 words · ~11 s

> From the water's edge again: now the edge bends. The near edge spans up to ninety-five pixel rows, lowest to highest, against none for the flat plane. That is real height, not lighting.

*Picture.* The framed window shows the plane from just above the waterline: the near edge is a rolling line; the pill 'up to 95' sits below it.

*Motion.* The near edge of the water rolls up and down.

*Lane.* capture · `ShaderLab` · runner-up: manim: a straight line and a wavy line

*Capture to record.* C29: scene water_scene.gd, W_BARE low camera, shader 05b-synced-clock cut 127, wave_clock from the script (W_FOLLOW); the 95-row figure is the maximum over the recorded clip (40 to 96 rows, mean 78, logs/edge-spread.txt) and the still (95).

### B39 · 36 words · ~12 s

> The shader moves the drawing, not the nodes. A buoy knows nothing about it. So a script runs the same wave function and sets each floater's height, and the buoy and the crate ride the waves.

*Picture.* Code card with the eight GDScript lines of the height function (first line lit); the real cove: the teal buoy and the cream crate rise and fall exactly with the waves.

*Motion.* The buoy and the crate ride the crests and troughs.

*Lane.* capture · `ShaderLab` · runner-up: manim: a node and the invisible surface

*Capture to record.* C30: scene water_scene.gd, W_FOLLOW: water_driver.gd drives wave_clock and sets the buoy and the crate to WaveMath.height each frame; shader 05b, iso camera.

### B40 · 47 words · ~16 s

> Give both the same clock. The shader's time and the script's clock start at different moments: on repeated runs here they differed by about three tenths of a second, never quite the same. So the script writes its clock into a uniform, and the shader reads that.

*Picture.* Two horizontal time lines labelled 'shader time' and 'script clock' with tick marks; the script's line starts later: a bracket between the two starts is labelled with the three measured gaps '0.32 s', '0.28 s', '0.31 s' (three of the six logged real-time runs, which ranged 0.28 to 0.32 s); then a box labelled 'wave_clock' (a uniform) receives an arrow from the script line, and the shader line is redrawn lined up with it; the final state shows both lines aligned with 'one number' between them.

*Motion.* The script line slides to the right to show the gap, three gap labels appear one per run, then an arrow into the uniform box pulls the two lines into alignment.

*Lane.* manim · `B40_OneClock` · runner-up: ShaderLab with GDScript code

### B41 · 33 words · ~11 s

> Run the same function on the graphics card and in the script and they agree to about three millimeters, on waves nineteen centimeters tall. Wave height, length and speed are three more dials.

*Picture.* Code card (the driver's set_clock lines; the three uniform writes lit one by one); the real cove: the waves grow taller, then longer, then faster, with the floaters still riding them; pills 'within 3 mm', 'height', 'length', 'speed'.

*Motion.* Height, length and speed are swept in turn and the buoy keeps riding.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab ramp per dial

*Capture to record.* C31: scene water_scene.gd, W_FOLLOW, shader 05b: the driver's wave_height, wave_length and wave_speed are swept one after another between 56 % and 95 % of the beat; the 3 mm agreement is E9 (evidence/planning-checks).

## Act V: The Shore

### B42 · 43 words · ~15 s

> Real water foams where it meets things. To know that, the water must know how deep it is. A texture with the hint depth texture holds the depth of everything solid. The water itself is not in it, so it can look beneath.

*Picture.* Act title 'The Shore' (serif 40) top-left. A side-on diagram on the cream stage: a small camera icon at the left, a horizontal blue line for the water surface, a sand line below it; one view ray runs from the camera through the surface to the sand. Two labelled distances along the ray: 'water 6.0 m' and 'floor 6.5 m'. A box labelled 'depth texture' sits above and holds a single value '6.5 m' fed from the floor point; a crossed-out grey arrow from the surface point to the box is labelled 'not in it'. The numbers are the measured test geometry (FACTCHECK).

*Motion.* The ray draws from the camera, a dot marks each hit, only the floor value flows into the box, and the water's arrow is struck out.

*Lane.* manim · `B42_DepthTexture` · runner-up: ShaderLab: a depth image render

### B43 · 41 words · ~14 s

> A depth value is not a distance. Turn it into one: rebuild the screen point, multiply by the inverse projection, divide by w, and flip the sign of z. Now you know how far the solid thing is from the camera.

*Picture.* Code card with the ten lines of scene_depth (depth, inverse projection and the sign flip lit in turn); the real cove drawn as a map: blue water with white along the beach's edge, around the rocks and under the floaters.

*Motion.* White glows along every place where the solid scene is close under the water.

*Lane.* capture · `ShaderLab` · runner-up: manim: the matrix multiply as boxes

*Capture to record.* C32: scene water_scene.gd, shader 06a-gap-view (unshaded gap map: white = close under the water), uncut plane, iso camera.

### B44 · 38 words · ~13 s

> The water's own distance is minus its view z. Subtract, and you have the gap: how far the water sits above whatever is beneath it. Over a floor half a meter down, the gap reads zero point five.

*Picture.* Wide window, a camera straight down on a plate: the left half over a floor goes from bright (floor close) to dark (floor deep) to mid as the floor moves; the right half over nothing stays dark; pills '0.2 m', '0.9 m', '0.5 m'; one code line below.

*Motion.* The left half brightens and darkens as the floor rises and sinks, and the number follows.

*Lane.* capture · `ShaderLab` · runner-up: manim: a number line with the gap

*Capture to record.* C33: scene gap_scene.gd, a plate wearing 06a-gap-view over a floor under its left half; the floor height steps 0.2 m, then 0.9 m, then 0.5 m (G_STEPS); measured gap (e8-depth-gap): 0.200, 0.500, 0.902 m on Forward+ (evidence/planning-checks/logs/e8b-gap-three-heights.txt).

### B45 · 38 words · ~13 s

> Hand a built-in to a helper function and Godot answers unknown identifier. Time and the constants are visible everywhere. Built-ins that belong to one function, like U V, vertex and screen U V, are not: pass them in.

*Picture.* A plain terminal card whose lines are the verbatim output of a script that compiled six one-line helper shaders on Godot 4.7.2: TIME and TAU compile, UV, VERTEX, SCREEN_UV and INV_PROJECTION_MATRIX each give 'Unknown identifier in expression'; a ring on the first failing line.

*Motion.* The six result lines print one after another; the first failure line is ringed.

*Lane.* terminal · `CCPlainShell` · runner-up: ShaderLab with the real engine error block

### B46 · 45 words · ~15 s

> Foam where the gap is small. The reach is wider where the nearest cell point is far, so the edge scallops instead of drawing a ruler line. Max joins it to the net, and the beach, the rock and the buoy gain a white edge.

*Picture.* Code card (the six lines that make the shore band; reach, shore and max lit in turn); the real finished cove: a thin white edge along the beach and around the rock and the floaters that widens into a ragged band as shore_width grows.

*Motion.* The white edge along the shore widens into a ragged band.

*Lane.* capture · `ShaderLab` · runner-up: manim: gap thresholds on a profile

*Capture to record.* C34: scene water_scene.gd, W_FOLLOW, shader 06-shore-foam cut 127, shore_width swept 0.05 to 1.0 across the beat, iso camera.

### B47 · 38 words · ~13 s

> One more trap. Compatibility counts depth from minus one to one; Forward Plus counts from zero to one. A single preprocessor line picks the right math. Leave it out in Compatibility and the whole surface turns to foam.

*Picture.* Code card (the six depth lines; the preprocessor line lit); the real cove in Compatibility: foam only along the shore, then after 66 % the whole surface washes to white foam.

*Motion.* The whole surface washes to white foam when the renderer branch goes.

*Lane.* capture · `ShaderLab` · runner-up: manim: two NDC ranges as bars

*Capture to record.* C35: scene water_scene.gd, renderer gl_compatibility, shader 06-shore-foam swapped at 66 % of the beat for 06b-no-renderer-branch; the 0.000 reading is E8 (evidence/planning-checks/logs/e8-compat-direct-decode.txt).

### B48 · 35 words · ~12 s

> Every dial is a uniform, and group uniforms turned them into folders. In the Inspector they appear as folders named Color, Clarity, Foam, Ripples, Waves and Shore, with sliders for ranges and pickers for colors.

*Picture.* The real Godot editor's Inspector (a tall portrait crop) showing the water's ShaderMaterial: folders Color, Clarity, Foam, Ripples, Waves, Shore; colour swatches for Water Color and Foam Color; number boxes with a thin slider bar for the ranged floats; two texture slots for Normal A and Normal B.

*Motion.* The real Inspector holds still while the voice names the folders and the widget types.

*Lane.* capture · `ShaderLab` · runner-up: GodotDevWorkbench reconstruction (labelled)

*Capture to record.* C38: the series editor driver (editor-capture/) in a scratch copy of water-project/: scenes/water.tscn open in the real Godot 4.7.2 editor, Water selected, its Material Override's ShaderMaterial opened, all six folders unfolded (state script capture-scenes/editor-states/water-W.json, mark W2-all); the Inspector dock cut from the NATIVE 3456 x 1944 frame (1300 x 1849) so the scratch FileSystem dock is not shown; labelled 'scripted editor session'. The uncropped frame is captures/editor-inspector.png.

### B49 · 27 words · ~9 s

> Same shader, three looks. Lagoon: clear, turquoise, fine foam. Pond: dark green, nearly opaque, no foam. Storm: grey, tall fast waves, thick foam. Only the numbers changed.

*Picture.* Three framed views side by side of the same finished cove: Lagoon (clear turquoise, fine foam, small waves), Pond (dark green, nearly opaque, no foam), Storm (grey, tall fast waves, thick foam); labels land under each name as the voice says it.

*Motion.* Three different waters move side by side from one shader.

*Lane.* capture · `ShaderLab` · runner-up: manim: a table of three parameter sets

*Capture to record.* C36: scene water_scene.gd, shader 06-shore-foam, W_FOLLOW, three recordings (Lagoon, Pond, Storm) at 1080 x 1080 joined side by side; the parameter sets are in captures.py.

## Closing

### BVDT · recap · 77 words · ~26 s

> Let's recap with Claude. Blue is albedo, and a uniform makes it a dial. Writing alpha makes water see-through, and the renderer decides how it blends. Foam is cellular noise: the gap between the nearest and second nearest point. A normal map lights the ripples, and it can push the foam's address too. Real waves move vertices, and a script runs the same function for floaters. The depth texture tells the water where it meets the shore.

*Picture.* The recap card: Blue is albedo, and a uniform makes it a dial. / Writing alpha makes water see-through, and the renderer decides how it blends. / Foam is cellular noise: the gap between the nearest and second nearest point. / A normal map lights the ripples, and it can push the foam's address too. / Real waves move vertices, and a script runs the same function for floaters. / The depth texture tells the water where it meets the shore.

### BHTF · your turn · 89 words · ~30 s

> Your turn. Paste this into Claude: Write a Godot spatial shader for water on a plane mesh cut sixty-three times each way. Make it blue with an opacity uniform, foam from cellular noise that moves with time, and waves in vertex that also fix the normal. Group the uniforms for the Inspector, then tell me how many vertices the plane has. Then check two things yourself. Is the water see-through at opacity zero point seven, with the floor showing through? And does the vertex count match sixty-five by sixty-five?

*Prompt shown and read in full:* Write a Godot spatial shader for water on a plane mesh cut sixty-three times each way. Make it blue with an opacity uniform, foam from cellular noise that moves with time, and waves in vertex that also fix the normal. Group the uniforms for the Inspector, then tell me how many vertices the plane has.

*Two checks:* Check: the water is see-through at opacity zero point seven, and the floor shows through. · Check: the vertex count is sixty-five by sixty-five, four thousand two hundred twenty-five.

### BOUT · outro · 8 words · ~4 s

> Making Water in Godot. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


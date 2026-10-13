# Script: SubViewports

**What this is.** The words Liam will say in *SubViewports*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 46 beats, 1831 words, about **10:27** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 22, manim 16, editor 2.

**If it runs long.** Cut, in this order: the input beat (B39), the update-mode beat (B38), the three-in-a-row beat (B37), the per-pixel beat (B20), then the hue beats (B26 to B29), keeping the stripes at one color. The origin and cut-off pair (B07, B08), the dark-edges beat (B10), the predict-and-reveal pair (B16, B17) and the wobble beats (B33 to B35) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | A Picture Off to the Side | 10 | 390 | ~2:13 |
| II | Two Shaders, One Result | 10 | 395 | ~2:14 |
| III | Stripes and Hue | 10 | 387 | ~2:12 |
| IV | Wobble the Result | 10 | 367 | ~2:05 |

## Opening

### BOPEN · identity card · 25 words · ~8 s

> Sub Viewports. Learn how a Sub Viewport draws part of your game into a picture, and how to shade that picture with a second shader.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "SubViewports", and the line "Draw into a picture, then shade the picture".

### BIDEA · the question · 43 words · ~15 s

> Hallo. This is Liam, in for Bear. Most people think shaders cannot see each other's work: one shader, one node, and no way to build on what another drew. A Sub Viewport changes that. One shader can shade the picture another shader made.

*Picture.* The hesitant writer types: "Shaders cannot see
each other's work." then deletes "cannot see" and types "can build on".

### BDEFS · terms · 53 words · ~18 s

> Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A texture is an image a shader can read. A viewport is a rectangle the engine draws into. U V is a point's address on a shape. And alpha is how visible a pixel is.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Texture** — an image a shader can read by address; **Viewport** — a rectangle the engine draws into; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Alpha** — how visible a pixel is: 0 invisible, 1 solid

## Act I: A Picture Off to the Side

### B01 · 43 words · ~15 s

> A sprite spins. Rainbow stripes slide across it, and a ripple runs through the whole picture. Two shaders made this, one after the other. The second shades what the first one drew. The trick is drawing into a picture, not onto the screen.

*Picture.* Act title 'A Picture Off to the Side' (serif 40) top-left. A real Godot render on the cream stage: the teal blob turns, rainbow stripes slide across it, and the whole picture ripples like cloth. Nothing is labelled yet; the effect is the hook.

*Motion.* The blob turns, the stripes slide and the picture ripples the whole time.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of the finished look

*Capture to record.* C01 (scene c01): picture 512, blob 448 with 01-inner-gradient (turned by a script at 0.9 rad/s), shown on a QuadMesh 512 x -512, 31 x 31, with 09-rainbow-wobble. 18 s, 30 fps, Forward+.

### B02 · 43 words · ~15 s

> That picture comes from a Sub Viewport: a node that draws its children into a picture of its own, not onto the screen. Drawn, but not shown directly: that is what off-screen means. Sprites, text, interface, even a three-D scene can go inside.

*Picture.* Two frames on the cream stage. Right: a large outline rectangle labelled 'screen', empty. Left: a smaller dashed square labelled 'SubViewport'. A teal blob fades into the small square, then a text glyph 'Aa', a small button outline and a three-line cube join it. The screen stays empty the whole time. Caption under the square: 'off-screen: drawn, not shown directly'; a one-line definition on the square: 'draws its children into a picture of its own'.

*Motion.* Children drop into the small square one by one while the screen frame stays empty.

*Lane.* manim · `B02_OffScreenBox` · runner-up: DesignPipelineClaim, show-tell isometric

### B03 · 33 words · ~11 s

> On its own, a Sub Viewport shows nothing. Its picture is a Viewport Texture: a texture that keeps the latest drawing. Give that texture to a sprite, and the sprite shows the picture.

*Picture.* Code card with the one real line at left; at right a real Godot window on the cream stage: empty for seven seconds, then the picture appears (a teal blob in a mid-grey box, the viewport's clear colour) at the moment the line runs.

*Motion.* The stage is empty until the texture is handed over, then the picture appears.

*Lane.* capture · `ShaderLab` · runner-up: manim: a drawn box feeding a screen

*Capture to record.* C02 (scene c02): picture 512 opaque (clear colour #A8A090), blob 448, a Sprite2D whose texture is empty until 7.0 s, then `display.texture = sub.get_texture()`. 14 s, 30 fps, Forward+. Verified (run-7a): the centre is the stage (0.851, 0.835, 0.792) at 6 s and the teal blob (0.373, 0.639, 0.569) in the clear-coloured box at 8.5 s.

### B04 · 43 words · ~15 s

> In the editor, add a Sub Viewport node and give it a size. Put a sprite inside it. Add a second sprite outside. In the second sprite's Texture slot, open the menu, and under New choose Viewport Texture. Then pick the Sub Viewport.

*Picture.* Three real frames of the whole Godot editor window, cross-dissolving: (1) subviewports_E1-1_subviewport-size: Scene dock Main > SubViewport > Sprite2D, Display; the SubViewport selected; the Inspector with its picture preview and Size 512 x 512, ring on Size; (2) subviewports_E2-1_texture-dropdown-new-viewporttexture: the Display sprite's Texture slot menu open (a Search box, the heading New, ViewportTexture highlighted), ring on ViewportTexture; (3) subviewports_E2-4_viewport-path-set: the ViewportTexture with Viewport Path = SubViewport, ring on Viewport Path.

*Motion.* The ring moves slot to slot as the voice names each step.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction)

*Capture to record.* E1-1, E2-1, E2-4: three static editor frames of the scratch project, recorded by the series' editor driver from this film's state script (evidence/planning-checks/editor-driver/state-scripts/subviewports-E1.json, run-15; the -wide variant widens the Inspector so long labels read in full). The clicks themselves are not shown, only the resulting states; the menu frame is the real Texture slot menu.

### B05 · 29 words · ~10 s

> In code, it is five lines. Make the viewport, give it a size, add it to the scene, put the sprite inside, and hand its texture to the display.

*Picture.* Left: a code card with five real lines (monospace): var sub := SubViewport.new() / sub.size = Vector2i(512, 512) / add_child(sub) / sub.add_child(inner_sprite) / display.texture = sub.get_texture(). Right: a diagram that builds with the focused line: a small tree 'Main' on top, a dashed box, a screen frame at the lower right. Line 1 draws the dashed box ('sub'); line 2 writes '512 x 512' along its edges; line 3 hooks it under 'Main'; line 4 drops a teal blob into it; line 5 draws an arrow from the box to a display sprite on the screen, and the blob appears on the screen.

*Motion.* Each line, when focused, makes its piece appear on the right.

*Lane.* manim · `B05_CodeBuilds` · runner-up: LectureCodeTrace beside a static diagram

### B06 · 45 words · ~15 s

> The size is the picture's resolution, in pixels. A new Sub Viewport is five hundred twelve pixels square. Shrink it to a hundred twenty-eight, draw it four times bigger, and the pixels show. Set the sprite's Filter to Nearest, and they turn into crisp blocks.

*Picture.* Two real displays of the same blob, both 512 px across on the stage: left a 512 px picture drawn 1:1 (crisp), right a 128 px picture drawn 4x (soft with the Linear filter). Partway, the right display's Filter switches to Nearest and the soft edge turns into hard blocks.

*Motion.* The right picture is soft, then snaps into crisp blocks when the filter changes.

*Lane.* capture · `ShaderLab` · runner-up: manim pixel grid

*Capture to record.* C03 (scene c03): two opaque viewports, 512 and 128 px (blob drawn natively at each size), displays at x = 100 and x = 668, the right at scale 4; Filter Linear until 12.5 s (on the words "Filter to Nearest"), then Nearest. 19 s, Forward+. Verified (run-7a): soft edge 8 pixels on the blob row with Linear at 7 s, 0 with Nearest at 14 s, runs 104 / 304 / 104 (multiples of 4).

### B07 · 37 words · ~13 s

> Inside the viewport, the top-left corner is the origin, and the picture covers only positive x and y from there. A centered sprite placed at zero, zero has three quarters of itself outside. The eyes are gone.

*Picture.* A real display of a 512 px picture (mid-grey box). The blob starts in the middle, slides to the top-left corner and settles there: only its bottom-right quarter is in the picture and its eyes are gone. A terracotta ring marks the corner; a readout 'origin (0, 0)'.

*Motion.* The blob slides into the corner and three quarters of it vanish, eyes first.

*Lane.* capture · `ShaderLab` · runner-up: manim: axes with a clipped sprite

*Capture to record.* C04a (scene c04a): opaque picture 512, blob 448 centred at (256, 256), stays in the middle while the voice explains the origin, slides to (0, 0) between 6.4 s and 8.6 s (on "placed at zero, zero"), then holds; 16 s, Forward+. Verified (run-7a): 55,202 teal and 1,546 eye pixels at 5 s; at (0, 0) from 8.6 s the picture holds 14,187 teal pixels = 25.7 % of the whole blob and 0 eye pixels.

### B08 · 38 words · ~13 s

> Slide it to the middle, and all of it appears. Slide it off an edge, and it is cut off. The picture is only as big as the viewport, and anything outside is not in it at all.

*Picture.* The same display. The blob slides from the corner to the middle (all of it appears), holds, then slides off the right edge and is cut off sharply at the picture's edge. Readouts 'all of it' then 'cut off'.

*Motion.* The blob arrives whole in the middle, then is sliced by the picture's right edge.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C04b (scene c04b): opaque picture 512, blob slides from (0, 0) to (256, 256) between 0.3 s and 3.3 s, holds, then to x = 560 between 4.0 s and 7.0 s; 16 s, Forward+. Verified (run-7a): 14,187 teal pixels at 0.2 s, 55,202 in the middle at 3.7 s, 15,470 when the blob is cut by the right edge at 9 s and at the end (centre at x = 560).

### B09 · 36 words · ~12 s

> See the box around the sprite? That is the picture's background, filled with the project's clear color. Turn on Transparent B G, and the empty parts become see-through. Now whatever is behind the picture shows through.

*Picture.* Code card with one line at left; at right the display over a faint grey grid: first the picture's mid-grey box hides the grid, then at the moment the line runs the box vanishes and the grid shows through, leaving only the blob.

*Motion.* The box disappears and the grid behind it shows through.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C05 (scene c05): grid of 2 px lines every 64 px behind the display, opaque picture until 8.0 s then `transparent_bg = true`; 15 s, Forward+. Verified (run-7a): the empty pixel is the clear colour (0.659, 0.627, 0.565) before and the stage (0.851, 0.835, 0.792) after; the picture's empty pixel alpha goes from 1 to 0.

### B10 · 43 words · ~15 s

> One catch with see-through pictures, which hard edges hide. A half-transparent pixel is stored already multiplied by its alpha. Draw it the usual way, and soft edges come out too dark. Set the Blend Mode to Premultiplied Alpha, and they come out right.

*Picture.* One real display of a soft gold glow over the faint grid. It starts with Blend Mode Mix: a muddy dark ring surrounds the glow. At the moment the blend mode changes to Premultiplied Alpha the dark ring vanishes and the glow is clean. A terracotta ring marks the dark ring; readouts name the two blend modes.

*Motion.* The dark ring around the glow vanishes the moment the blend mode changes.

*Lane.* capture · `ShaderLab` · runner-up: manim: two swatches and arithmetic

*Capture to record.* C06 (scene c06): picture 512 transparent, glow image (gold, alpha falling to 0 over the outer 45 % of its radius) over the grid; the display uses a CanvasItemMaterial, Blend Mode Mix until 10.5 s then Premultiplied Alpha; 18 s, Forward+. Verified (run-7a, run-5 G1) at ring pixel (807, 360): Mix (0.655, 0.608, 0.490), Premultiplied (0.890, 0.800, 0.576), the glow drawn directly (0.890, 0.796, 0.576).

## Act II: Two Shaders, One Result

### B11 · 39 words · ~13 s

> Now give each side a shader. The inner shader sits on the sprite inside the viewport. The outer shader sits on the sprite that shows the picture. The inner one draws first. The outer one gets the finished picture.

*Picture.* Act title 'Two Shaders, One Result' (serif 40) top-left. Left: the SubViewport square with the teal blob inside and a small tag 'inner shader' on the blob. A wide arrow labelled 'picture' runs right to a display sprite on a screen frame carrying a tag 'outer shader'. A token (a few teal dots) starts on the blob, turns gold passing the inner tag, rides the arrow, and on reaching the display passes the outer tag and is re-tinted. Small words 'first' under the left half and 'then' under the right.

*Motion.* A token passes the inner shader first, travels as a picture, then passes the outer shader.

*Lane.* manim · `B11_TwoPlaces` · runner-up: DesignPipelineClaim, show-tell isometric

### B12 · 37 words · ~13 s

> In the editor, that is each sprite's Material slot. The inner sprite's Material holds a Shader Material with the inner shader. The display's Material holds one with the outer shader. Each shader sits on its own node.

*Picture.* Three real frames of the whole Godot editor window, cross-dissolving: (1) subviewports_E4-1_inner-sprite-material: the inner Sprite2D selected, its Inspector's Material group open with the Material slot holding a ShaderMaterial, ring on Material; (2) subviewports_E4-2_display-material: the Display sprite selected, the same slot, ring on Material; (3) subviewports_E4-5_shader-editor: the shader editor open at the bottom showing the outer shader's text (04-stripes).

*Motion.* The ring moves from the inner sprite's Material slot to the display's, then to the shader text.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction)

*Capture to record.* E4-1, E4-2, E4-5: static editor frames of the scratch project (shaders.tscn), recorded by the series' editor driver from evidence/planning-checks/editor-driver/state-scripts/subviewports-E4.json (run-15; the -wide variant widens the Inspector).

### B13 · 41 words · ~14 s

> The inner shader is an ordinary one. Its fragment function runs once for each pixel and sets the color. This one blends the sprite from teal at the top to gold at the bottom, using U V, the sprite's own address.

*Picture.* Code card with the seven-line inner shader at left; at right a real display of the picture: a plain teal blob that, at the moment the voice names the gradient, turns teal at the top to gold at the bottom. Readouts 'UV.y 0' at the top of the blob and 'UV.y 1' at its bottom.

*Motion.* The plain blob takes on the teal-to-gold gradient when the shader goes on.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C07 (scene c07): picture 512 transparent, blob 448; the plain sprite until 7.0 s, then 01-inner-gradient; the display uses 02-outer-passthrough; 17 s, Forward+. Verified (run-2 F1): the picture's colour at sprite UV.y 0.265 / 0.501 / 0.738 is (0.522, 0.671, 0.510) / (0.651, 0.698, 0.459) / (0.784, 0.729, 0.408) = mix(teal, gold, UV.y).

### B14 · 42 words · ~14 s

> The outer shader gets the picture as its texture. It starts with one line that sets Premultiplied Alpha, and one line that copies the picture through unchanged. The result matches the picture exactly. Everything the inner shader made is already in there.

*Picture.* Code card with the six-line pass-through at left; at right two real displays of the same moving picture side by side: the picture shown directly (Premultiplied Alpha) and the picture shown through the pass-through shader. They are identical frame by frame while the blob slides. Readout 'same pixels'.

*Motion.* The two displays follow the sliding blob identically.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C08 (scene c08): picture 512 transparent, gradient blob sliding x = 256 + 60 sin(0.9 t); left display a Sprite2D with CanvasItemMaterial Premultiplied Alpha, right display 02-outer-passthrough; 18 s, Forward+. Verified: largest channel difference between the two displays 0.0 (run-7a); and all 262,144 pixels of the display equal the picture (run-2 F2).

### B15 · 45 words · ~15 s

> Now change something only the outer shader can. Multiply the picture by U V x, and it fades from nothing at the left edge to full at the right. Multiply the whole color, not only the alpha, because the picture's colors already carry their alpha.

*Picture.* Code card with the six-line fade shader at left; at right the display: the full gradient blob until the fade goes on, then it fades from nothing at the picture's left edge to full at its right edge. A thin 0-to-1 ramp strip under the display is traced as the fade appears.

*Motion.* The picture fades left to right the moment the shader goes on, and the ramp underneath is traced.

*Lane.* capture · `ShaderLab` · runner-up: manim ramp strip

*Capture to record.* C09 (scene c09): picture 512 transparent, gradient blob; the display uses 02-outer-passthrough until 4.5 s then 03-outer-fade; 19 s, Forward+. Verified (run-7b) at picture x = 196 / 256 / 316: the multiplier is 0.389 / 0.500 / 0.622 (expected 0.384 / 0.501 / 0.618); on an opaque white picture it is x / 512 from edge to edge (run-2 F3).

### B16 · 28 words · ~10 s

> Here is a question. The sprite now turns inside the viewport. Which effect turns with it: the inner gradient, the outer fade, or both? Decide before you look.

*Picture.* The picture frame with the teal blob at the centre. A short vertical ramp strip beside the blob labelled 'inner gradient' (teal at the top, gold at the bottom) and a horizontal ramp strip under the frame labelled 'outer fade' (0 to 1, left to right). A curved arrow circles the blob. Two grey question marks and two terracotta dots hover by the strips.

*Motion.* The curved arrow sweeps around the blob while both strips stay where they are, and the question dots pulse.

*Lane.* manim · `B16_WhichTurns` · runner-up: FormACard with the question

### B17 · 41 words · ~14 s

> The gradient turns with the sprite. The fade stays put. A shader's U V belongs to the thing it draws. The inner shader draws the sprite, and the sprite turns. The outer shader draws the picture, and the picture does not.

*Picture.* A real display of the faded gradient blob. The sprite inside the viewport turns half a turn: the gold half swings from the bottom to the top and the eyes end up below, while the fade (transparent at the picture's left, solid at its right) does not move. Readouts 'gradient turns' and 'fade stays'.

*Motion.* The gold swings round with the sprite while the fade stays left to right.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C10 (scene c10): as C09 with the fade on from the start; the sprite turns half a turn (0 to pi) between 0.3 s and 3.3 s by script; 17 s, Forward+. Verified (run-7b): red 100 px above / below the centre goes 0.529 / 0.776 to 0.776 / 0.525 (gold flips); the multiplier at picture x = 196 / 256 / 316 stays 0.387 / 0.500 / 0.612; probes at two rotations in run-2 F4.

### B18 · 42 words · ~14 s

> Add a second sprite, and the same fade runs across both. The outer shader does not know how many things are inside. It sees one picture. Put a fade on each sprite instead, and every sprite starts over at its own edge.

*Picture.* Two framed panels. Left: two blobs with no viewport, each carrying its own fade shader: every blob fades from its own left edge to its own right edge. Right: a viewport holding the same two blobs, shown with one fade across the whole picture: the left blob is faint, the right blob solid. Both pairs slide left and right: the left fades ride along with their sprites, the right fade stays still and the sprites brighten as they move through it.

*Motion.* On the right the blobs brighten as they slide through a fixed fade; on the left each fade rides along.

*Lane.* capture · `ShaderLab` · runner-up: manim two panels

*Capture to record.* C11 (scene c11): left panel Rect(40, 210, 600, 300): two 200 px blobs, each with 03-outer-fade (premultiplied) directly on the Sprite2D; right panel Rect(660, 210, 600, 300): a 600 x 300 transparent viewport holding the same blobs, shown with 03-outer-fade; sprites slide dx = 70 sin(0.8 t) in both; 18 s, Forward+. Verified (run-7b): per sprite 0.5 and 0.5; on the picture 0.254 and 0.754.

### B19 · 37 words · ~13 s

> That is also the limit. By the time the outer shader runs, the sprites are gone. Only their pixels remain, already flattened together. It cannot ask a sprite where it is, or reach what hides behind another.

*Picture.* Three overlapping cards in the SubViewport square, drawn as a small exploded stack: the blob, a second blob and a rounded rectangle. They slide together and collapse into one flat picture card on the right. A circle-with-a-dot eye labelled 'outer shader' looks at the flat card; a dashed line from the eye back to the original stack is crossed out by two short bars.

*Motion.* The stack collapses into one flat card; the eye sees only the card, and the line back to the sprites is crossed out.

*Lane.* manim · `B19_Flattened` · runner-up: LectureEvidenceTable

### B20 · 43 words · ~15 s

> Resolution splits the same way. The inner shader works in the picture's pixels. The outer shader works in the display's pixels. Here a small picture is drawn big under an outer shader that draws stripes: the picture is coarse, the stripes are sharp.

*Picture.* A real display of a 64 px picture drawn eight times bigger with the Nearest filter: the blob is built from big square blocks, while moving stripes drawn by an outer shader slide across it with crisp one-pixel edges that cut through the blocks at any position. Readouts 'picture pixels' and 'display pixels'.

*Motion.* The stripes' edges slide smoothly through the blocks of the blob, never snapping to them.

*Lane.* capture · `ShaderLab` · runner-up: manim pixel grid

*Capture to record.* C12 (scene c12): transparent viewport 64 px (blob 64 px wide), display at scale 8 (512 px) with Nearest filter and 05-stripes-moving; 18 s, Forward+. Verified (run-6 X4, run-7b): the blob's own edges fall on multiples of 8 display pixels (x = 104 and 408 in run-6); the stripe edges do not (mod 8 = 7, 2, 5, 7, 2, 5, 7 in run-6; other values in run-7b, since the stripes move with TIME). Numbers are at scale 1; the 3x route multiplies them by 3.

## Act III: Stripes and Hue

### B21 · 43 words · ~15 s

> A fade is one kind of mask. Stripes are another. Start with a diagonal: add the two U V numbers together. The sum climbs from zero at the top left to two at the bottom right, and equal values line up along diagonals.

*Picture.* Act title 'Stripes and Hue' (serif 40) top-left. A square picture (the kit's UV square: 0 to 1 axes, y pointing down) with thin grey isolines along its diagonals at u + v = 0.5, 1 and 1.5. A ramp strip along the diagonal reads 0 to 2 with end labels '0' and '2'. A terracotta dot travels from the top-left corner to the bottom-right corner with a live label 'u + v'.

*Motion.* The dot moves along the diagonal while its sum climbs from 0 to 2, lighting each isoline as it crosses.

*Lane.* manim · `B21_Diagonal` · runner-up: ShaderLab

### B22 · 39 words · ~13 s

> Fract keeps only what comes after the decimal point. Feed it a climbing number and you get a saw: up from zero to one, drop back, climb again. Multiply first, and the saw repeats faster. Times six, six saws.

*Picture.* The series' signature object: a ramp strip (0 to 1) at the top; below it a plot of fract(x * 6) as a six-tooth saw wave on grey axes; a terracotta dot rides the ramp and its twin rides the plot. Label 'fract(x × 6)' and a one-line definition 'the part after the point: x minus floor(x)'.

*Motion.* The dot climbs the ramp while its twin climbs a tooth, drops, climbs again, six times.

*Lane.* manim · `B22_Saw` · runner-up: LectureEvidenceTable

### B23 · 40 words · ~14 s

> Step makes a hard edge: zero while the saw is below the width, one once it passes. Take that from one, and you get a stripe: on while the saw is under the width. A wider width means thicker stripes.

*Picture.* One saw tooth drawn large; a horizontal threshold line labelled 'width' at 0.5 with a handle; below it the step result as a square wave (0 then 1) with the definition '0 below the edge, 1 from the edge up'; below that '1 - step' as a bar of alternating on and off segments. The threshold handle slides from 0.25 up to 0.75 and the on segments thicken.

*Motion.* The width line slides up and every stripe on the bar thickens in step.

*Lane.* manim · `B23_StepStripe` · runner-up: ShaderLab

### B24 · 38 words · ~13 s

> Put it together in the outer shader. Multiply the picture by the stripe, and the sprite shows only inside the stripes. Count and width are uniforms: values your game sets from outside, from the Inspector or from code.

*Picture.* Code card with the twelve-line stripe shader at left; at right the display: diagonal stripes cut the gradient blob so it shows only inside them; the stripes thicken (width 0.08 up to 0.5), hold, then get finer (count 6 up to 12).

*Motion.* The stripes thicken, then multiply, as the dials move; the empty parts stay empty.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C13 (scene c13): picture 512 transparent, gradient blob, display uses 04-stripes; width sweeps 0.08 to 0.5 (0.5 s to 4.5 s), count 6 to 12 (8 s to 12 s); 16 s, Forward+. Verified (run-7b) at 2 / 6 / 10 s: width 0.213 / 0.5 / 0.5, count 6 / 6 / 9, 0 stripe mismatches over about 2,900 pixels each; on a plain rectangle the on-fraction equals width (0.500, 0.247, 0.800) and `count` complete stripes fit across.

### B25 · 35 words · ~12 s

> To move them, subtract time. Time is the seconds on one clock shared by the whole game. Take speed times time off the diagonal, and every stripe slides along it, while the sprite turns underneath.

*Picture.* Code card with the twelve-line moving-stripes shader at left; at right the display: diagonal stripes slide down and right across the blob while the blob turns slowly underneath and the stripes keep their direction.

*Motion.* The stripes slide steadily; the sprite turns and the stripes do not.

*Lane.* capture · `ShaderLab` · runner-up: manim sine plot

*Capture to record.* C14 (scene c14): as C13 with 05-stripes-moving (count 6, width 0.5, speed 0.12), the blob turning at 0.8 rad/s by script; 15 s, Forward+. Verified (run-7b): the stripe formula with the TIME read in the same draw predicts every probe (0 mismatches over about 2,900 pixels).

### B26 · 36 words · ~12 s

> Now color. Screens mix red, green and blue, but people think in hue, saturation and value. Hue is the angle around a color wheel: which color. Saturation is how far from grey. Value is how bright.

*Picture.* A colour wheel of 72 coloured wedges (full saturation and value) at the left. A marker arrow rotates around it, labelled 'hue: which color'; a radial bar from the centre to the rim, labelled 'saturation: how far from grey' (white at the centre, vivid at the rim); and a short vertical swatch ramp at the right, labelled 'value: how bright'. Three small terracotta dots mark the three controls.

*Motion.* An arrow sweeps round the wheel, a marker slides from centre to rim, a swatch brightens.

*Lane.* manim · `B26_ColorWheel` · runner-up: LibraryIconRow

### B27 · 42 words · ~14 s

> Call the hue a number from zero to one, once around the wheel. Zero is red. A sixth is yellow, a third is green, a half is cyan, two thirds is blue, five sixths is magenta. Then it wraps back to red.

*Picture.* A ramp strip filled with the hue spectrum from 0 to 1 with seven ticks labelled 0, 1/6, 1/3, 1/2, 2/3, 5/6, 1 and a terracotta marker riding along. Under the marker a swatch shows its colour and a small triple of numbers updates: (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0). A small wheel beside the strip turns its arrow with the marker. Credit: 'Godot 4.7.2 · same in Forward+ and Compatibility'.

*Motion.* The marker rides the strip and stops at each sixth while the swatch and its numbers change.

*Lane.* manim · `B27_HueRamp` · runner-up: LectureEvidenceTable

### B28 · 36 words · ~12 s

> Red, green and blue each follow the same plateau around the wheel: full for a third, zero for a third, with ramps between. Green is red's plateau pushed a third along. Blue is pushed two thirds.

*Picture.* A plot with hue 0 to 1 on x and 0 to 1 on y. One red plateau curve (full for a third, zero for a third, ramps between, wrapping round at the edges) draws first; a ghost copy slides a third to the right and becomes the green curve; another slides two thirds and becomes the blue curve. A vertical marker moves along the hue axis and reads three values off the curves into a swatch.

*Motion.* The red plateau slides along to become green, then blue; a marker reads the three curves.

*Lane.* manim · `B28_Plateaus` · runner-up: ShaderLab

### B29 · 43 words · ~15 s

> In code, an absolute value and a clamp build the plateau, and fract wraps the hue. Mixing toward white sets the saturation, and the value scales the result. Tested at the six hues, it gives pure red, yellow, green, cyan, blue and magenta.

*Picture.* Code card with the ten real lines (plateau and hsv_to_rgb) at left; at right a still of the hue strip above six flat swatches. As the voice names each pure colour its swatch gets its RGB triple: 1 0 0, 1 1 0, 0 1 0, 0 1 1, 0 0 1, 1 0 1.

*Motion.* The six swatches take their exact numbers one by one.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C15 (scene c15): the hue strip (06-hsv-strip) on a 1000 x 130 rectangle above six 160 px swatches, each a rectangle with 06b-hsv-probe and `hue` = 0, 1/6, 2/6, 3/6, 4/6, 5/6; one PNG frame (scene time 3 s; the scene is 8 s long), Forward+. Verified (run-3 H1, H1b, run-7c): the six swatches read (1,0,0) (1,1,0) (0,1,0) (0,1,1) (0,0,1) (1,0,1) exactly in both renderers; over 65,536 + 65,536 pixels the function agrees with the engine's Color.from_hsv within 0.002, and over 640 columns with Python's colorsys within 0.0019.

### B30 · 35 words · ~12 s

> Now give the stripes a hue. Use the diagonal itself as the hue, and each stripe cuts out a band of the rainbow. The diagonal slides with time, so the colors travel with the stripes.

*Picture.* Code card with the seven-line fragment function at left; at right the display: rainbow stripes slide across the turning gradient blob, the gaps between them showing the gradient, the colours travelling with the stripes.

*Motion.* The rainbow slides with the stripes while the gradient shows through the gaps.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C16 (scene c16): as C14 with 07-rainbow-stripes (count 6, width 0.5, speed 0.12); 15 s, Forward+. Verified (run-3 H4, run-7c): stripe pixels equal Color.from_hsv(fract(diagonal)) within 0.002 over about 2,400 pixels; every gap pixel equals the picture (2,496 of 2,496 in run-3 H4).

## Act IV: Wobble the Result

### B31 · 37 words · ~13 s

> A shader can move corners too. Its vertex function runs once for each vertex, each corner of a shape, and sets where it goes. A sprite has four corners, so it can lean, but it cannot bend.

*Picture.* Act title 'Wobble the Result' (serif 40) top-left. A rectangle (the sprite) with four terracotta corner dots and the definition 'vertex: a corner point of a shape'. 'vertex' flashes on each dot in turn; the top-right and bottom-right dots slide down and the rectangle leans into a parallelogram with straight edges. A faint dashed curve tries to bend the top edge but the edge stays straight. Caption 'four corners, straight edges'.

*Motion.* Two corners slide and the whole shape leans; the edge between them stays a straight line.

*Lane.* manim · `B31_FourCorners` · runner-up: ShaderLab

### B32 · 38 words · ~13 s

> To bend a picture, give it more corners. A Quad Mesh, drawn by a Mesh Instance two D node, is a rectangle you can cut into a grid. Thirty-one cuts each way makes one thousand and eighty-nine corners.

*Picture.* A rectangle with four corner dots; cut lines appear in steps of 0, 1, 7, 15 and 31 cuts each way, the grid getting finer and a corner counter reading 4, 9, 81, 289 and 1,089 while the dots multiply and shrink. Labels 'Subdivide Width' and 'Subdivide Depth' beside the last two steps; caption 'Quad Mesh, drawn by Mesh Instance 2D'; the definition 'mesh: the set of vertices and triangles that make a shape'.

*Motion.* The grid gets finer in steps and the corner counter climbs to 1,089.

*Lane.* manim · `B32_CutIntoGrid` · runner-up: editor frame of the QuadMesh Inspector

### B33 · 32 words · ~11 s

> Same wobble, two meshes. On a plain quad, only four corners move, so the edge stays straight. On the grid, every corner moves on its own, and the edge becomes a wave.

*Picture.* Two real meshes side by side showing one picture (a cream card with a teal frame and the gradient blob), both under the same wobble shader. Left, a plain quad: the card only leans, its edges straight. Right, the 31 x 31 grid: its edges ripple as a wave. Readouts '4 corners' and '1,089 corners'.

*Motion.* The left card tilts with straight edges while the right card ripples.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C17 (scene c17): one transparent 512 px viewport with a card (teal frame 20 px, cream inside) and the gradient blob; two MeshInstance2D, QuadMesh 480 x -480, subdivide 0 at (330, 360) and 31 at (950, 360), both with 08-wobble (amplitude 16, frequency 10, speed 3) and the Linear filter; 17 s, Forward+. Verified (run-7c): plain quad second differences of the top edge in {-1, 0, 1} (straight); grid edge within 0.23 to 0.26 px (rms) of 120 + sin(UV.x * 10 + TIME * 3) * 16 (the shape depends on TIME).

### B34 · 40 words · ~14 s

> The wobble is one line in the outer shader's vertex function. Move each corner up or down by a sine of its U V x, plus time. Sine swings smoothly between minus one and one, and amplitude sets how far.

*Picture.* Code card with the fourteen-line wobble shader at left; at right the 31 x 31 mesh carrying the card and the blob, rippling continuously. The vertex function and the VERTEX.y line are highlighted in turn.

*Motion.* The card ripples continuously while the highlighted line is the one that does it.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C18 (scene c18): the C17 picture on one MeshInstance2D, QuadMesh 512 x -512, 31 x 31, with 08-wobble; 17 s, Forward+. Verified (run-7c): top edge within 0.2 to 0.33 px (rms) of 104 + sin(UV.x * 10 + TIME * 3) * 16 (the shape depends on TIME).

### B35 · 38 words · ~13 s

> One catch in two-D. A Quad Mesh is built for three-D, where y points up, but in two-D y points down, so the picture lands upside down. Give the Quad Mesh a negative height, and it lands upright.

*Picture.* One real mesh showing the card and the blob: first upside down (the eyes below the centre), then at the moment the height goes negative the picture is upright (eyes above). Readouts 'height 512' and 'height -512'.

*Motion.* The face flips from upside down to upright when the height goes negative.

*Lane.* capture · `ShaderLab` · runner-up: manim vertex arrows

*Capture to record.* C19 (scene c19): the C17 picture on a QuadMesh with size (512, 512) until 9.5 s, then (512, -512), pass-through shader; 16 s, Forward+. Verified (run-4 M1, M4, M6, both renderers; run-7c): with (512, 512) the picture's top-left marker lands at the screen's bottom-left; with a negative height it lands at the top-left; the mesh's own layout puts UV (0, 0) on the vertex with y = +1 (up in 3D, down in 2D).

### B36 · 34 words · ~12 s

> So the chain is this. Nodes draw into the viewport, and the inner shader colors them. The outer shader paints stripes on the picture and bends it. The sprite inside knows nothing about either.

*Picture.* A left-to-right chain on the cream stage: a dashed square holding the blob and card icons, then a tag 'inner shader', then the picture card, then a tag 'outer fragment: stripes', then a tag 'outer vertex: bend', then a screen frame with a wobbling frame on it. A token (the blob thumbnail) changes at each stage: plain, gradient, striped, striped and bent.

*Motion.* The token passes each stage and changes its look: plain, gradient, striped, bent.

*Lane.* manim · `B36_WholeChain` · runner-up: DesignPipelineClaim, show-tell isometric

### B37 · 30 words · ~10 s

> Nothing stops at two. Show a picture inside another Sub Viewport, and that picture can take a third shader. Each stage is a picture, and the next stage shades it.

*Picture.* Three picture frames in a row: 'viewport' (the blob with an inner shader) leads to a picture, shown inside a second 'viewport' by a sprite with a fade shader, which leads to a second picture, shown on the screen by a sprite with a stripes shader. Three tags 'inner', 'middle' and 'outer'. A token flows along and picks up each shader's look.

*Motion.* The token passes three shaders in a row, each time through a picture.

*Lane.* manim · `B37_StageToStage` · runner-up: ShaderLab

### B38 · 43 words · ~15 s

> It is not free. A Sub Viewport is a picture the engine draws every frame it is shown. For a picture that never changes, set Update Mode to Once. It draws one time, then keeps that picture, however much the sprite inside moves.

*Picture.* Code card with one line at left; at right two real displays of two identical viewports whose sprite wanders about in a Lissajous path. Both follow it until the right one is set to Once; from then on the right picture freezes while the left keeps moving. Readouts 'default' and 'Update Mode: Once'.

*Motion.* The right picture freezes while the left one keeps following the wandering sprite.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C21 (scene c21): two opaque 512 px viewports, a 269 px blob in each moving as (256 + 150 sin 0.9 t, 256 + 90 cos 0.7 t); displays at x = 100 and 668; viewport 1 gets `render_target_update_mode = UPDATE_ONCE` at 8.5 s (on "set Update Mode to Once"); 18 s, Forward+. Verified (run-7c, run-11 O1, recorded through Movie Maker in run-13): at 12 s the left picture's first teal pixel is at x = 29 (formula 28); the right is at 323, frozen at its 8.5 s position (formula 322).

### B39 · 37 words · ~13 s

> One more limit. Mouse and key events do not reach a standalone Sub Viewport. Put it inside a Sub Viewport Container, and the container passes them in. Without that, a button inside the picture will not respond.

*Picture.* A screen frame with the display showing the picture of a small SubViewport square that holds a button icon. A cursor arrow (a drawn shape) clicks on the picture; the click ring bounces off the picture's edge and the button icon stays unlit. Then a wrapper frame labelled 'SubViewportContainer' appears around the square; the cursor clicks again, a dotted line carries the click through the container into the square and the button icon lights teal.

*Motion.* The click bounces off a standalone viewport, then passes through the container and lights the button.

*Lane.* manim · `B39_ClickBounces` · runner-up: ShaderLab

### B40 · 38 words · ~13 s

> The picture is only a texture, so it fits wherever a texture does. A sprite, a panel in your interface, a flat plane in a three-D scene, or a sampler in any other shader. One picture, four places.

*Picture.* Four real panels in a row showing one live picture (a cream card with the turning gradient blob): a Sprite2D, a panel in the interface (a TextureRect inside a teal-bordered panel), a flat plane in a 3D scene (swaying about its vertical axis, rendered by its own 3D viewport), and a plain rectangle whose own shader reads the picture through a sampler uniform. Readouts name each place as the voice does.

*Motion.* The same turning blob appears in all four places at once; the 3D plane sways.

*Lane.* capture · `ShaderLab` · runner-up: manim: four icons receiving one picture

*Capture to record.* C20 (scene c20): one 280 px opaque viewport (cream card, gradient blob turning at 0.7 rad/s) shown by a Sprite2D at (40, 220), a TextureRect in a PanelContainer at (332, 212), a flat QuadMesh with an unshaded StandardMaterial3D in a 280 px transparent 3D viewport shown as a Sprite2D at (640, 220), and a ColorRect at (940, 220) whose shader reads the picture through `uniform sampler2D picture`; 16 s, Forward+. Verified (run-7c) at 0 s: gold is below the centre in all four panels (red 0.773 below, 0.533 above in the flat ones; 0.792 / 0.510 in the 3D plane).

## Closing

### BVDT · recap · 69 words · ~24 s

> Let's recap with Claude. A Sub Viewport draws its children into a picture, and a Viewport Texture shows it anywhere. An inner shader makes the picture, and an outer shader shades it, using the picture's own U V. Stripes are a saw wave cut by a step, and a hue function colors them. Cut a mesh into a grid, and the outer vertex function can bend the whole picture.

*Picture.* The recap card: A Sub Viewport draws its children into a picture, and a Viewport Texture shows it anywhere. / An inner shader makes the picture, and an outer shader shades it, using the picture's own UV. / Stripes are a saw wave cut by a step, and a hue function colors them. / Cut a mesh into a grid, and the outer vertex function can bend the whole picture.

### BHTF · your turn · 96 words · ~33 s

> Your turn. Paste this into Claude: Write a Godot four scene as a text file. A Sub Viewport, five hundred twelve pixels square with a transparent background, holds the Godot icon, its lower half painted red by its own shader. A second sprite shows the viewport's texture with Premultiplied Alpha, and its shader keeps only vertical stripes. Also tell me where each shader goes. Then check two things yourself. With the outer shader off, is the icon's lower half red, with no box around it? And when you turn the icon, do the stripes stay still?

*Prompt shown and read in full:* Write a Godot four scene as a text file. A Sub Viewport, five hundred twelve pixels square with a transparent background, holds the Godot icon, its lower half painted red by its own shader. A second sprite shows the viewport's texture with Premultiplied Alpha, and its shader keeps only vertical stripes. Also tell me where each shader goes.

*Two checks:* Check: with the outer shader off, the picture shows the icon with its lower half red, and no box around it. · Check: turn the icon inside the viewport. The red turns with it, and the stripes stay still.

### BOUT · outro · 6 words · ~4 s

> Sub Viewports. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


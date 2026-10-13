# Script: Light Shaders

**What this is.** The words Liam will say in *Light Shaders*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 46 beats, 1796 words, about **10:15** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 25, manim 12, remotion 3.

**If it runs long.** Cut, in this order: the grid beat (B39), the stripes beat (B38), the pulse beat (B16), then the limits beat (B18). Each repeats an idea another beat already carries, or sits outside the film's one idea. The rebuild (B13), the lighthouse (B26) and the expanding ring (B36) stay: they are the proof and the two payoffs.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Lights in 2D | 8 | 306 | ~1:44 |
| II | The Light Function | 10 | 380 | ~2:09 |
| III | Which Way Is the Light? | 5 | 193 | ~1:06 |
| IV | A Lighthouse | 7 | 224 | ~1:16 |
| V | Where Is the Light? | 10 | 369 | ~2:05 |

## Opening

### BOPEN · identity card · 30 words · ~10 s

> Light Shaders. Learn what the light function does and what Godot hands it, then use it to build a sweeping lighthouse beam and a ring that spreads from a lamp.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Light Shaders", and the line "Take over what a light does to every pixel".

### BIDEA · the question · 41 words · ~14 s

> Hallo. This is Liam, in for Bear. Lighting in a two-D game feels built in: you place a light, and Godot does the rest. Most people think that is where your control ends. It is not. A shader can replace it.

*Picture.* The hesitant writer types: "Lighting is built in.
You can't touch it." then deletes "You can't touch it" and types "A shader can replace it".

### BDEFS · terms · 75 words · ~26 s

> Six terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. A texture is an image a shader can read. The canvas is the surface two-D things are drawn on. A vector is a bundle of two to four numbers. And a mask is a number from zero to one, for each pixel, saying how much of something to show.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Pixel** — one dot of the picture on screen; **Texture** — an image a shader can read by address; **Canvas** — the surface that 2D things are drawn on; **Vector** — a bundle of two to four numbers; **Mask** — a number from 0 to 1 per pixel saying how much of something to show

## Act I: Lights in 2D

### B01 · 41 words · ~14 s

> In a two-D game, a light is a soft glow. Same scene, same light, and one function later, that glow is a beam sweeping the ground. The function is called light, and before this film ends, you will have written it.

*Picture.* Act title 'Lights in 2D' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a dusk-blue tiled floor, a teal blob and a lamp. For a few seconds the lamp is a soft round glow. At the words 'one function later' the floor's shader switches on and the glow becomes a soft-edged beam sweeping round. Caption: 'light(): runs once per pixel for each light that touches it'.

*Motion.* The glow turns into a sweeping beam at the moment the voice says 'one function later'.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a glow becoming a beam

*Capture to record.* C01: Dusk tiled floor, one warm lamp (scale 7: reach 896 px) at the centre, the teal blob at lower right on default lighting. The lamp bulb disc marks the lamp. Scene = evidence/planning-checks/light_scene.gd with captures.json id C01; 1920 x 1080 window at scale 1, 30 fps, 15 s, Forward+. Expected: before the switch a soft round glow on the tiles; after it a soft-edged wedge turning clockwise from the lamp, the blob unchanged.

### B02 · 36 words · ~12 s

> Godot has two kinds of two-D light. A point light shines out from one spot, like a lamp. A directional light shines the same way everywhere, like the sun. This film works mostly with the lamp.

*Picture.* Two panels on the cream stage, each a short strip of six outlined floor tiles. Left: a pale lamp disc above the strip with rays fanning out to every tile, label 'point light'. Right: a sun disc far up with parallel rays slanting the same way onto the strip, label 'directional light'. Grey captions under them: 'like a lamp', 'like the sun'.

*Motion.* Rays fan out from the lamp in every direction; on the right they arrive side by side, all parallel.

*Lane.* manim · `B02_TwoLights` · runner-up: isometric lamp and sun drawing (show-tell)

### B03 · 43 words · ~15 s

> A light needs a dim scene to show against. A two-D scene starts fully lit, so a light can only brighten what is already bright. Add a Canvas Modulate node, which tints everything, and set it dim. That tint is the ambient light.

*Picture.* A real Godot render in a framed window: a cream-tiled floor already fully lit, a lamp that barely shows. At 'set it dim' the tint eases in, the floor goes dusk blue and the lamp's glow blooms. Caption: 'ambient light: the tint where no lamp reaches'; a label 'Canvas Modulate' lands as the node is named.

*Motion.* The scene dims and the lamp suddenly stands out.

*Lane.* capture · `ShaderLab` · runner-up: manim: floor strip with a tint slider

*Capture to record.* C02: Dusk floor with ONE lamp (scale 4) at (760, 520) and the blob at (1180, 660). No tint for the first part (a white CanvasModulate: the scene is fully lit); the tint eases to dusk (0.50, 0.55, 0.72) over one second. Scene = evidence/planning-checks/light_scene.gd with captures.json id C02; 1920 x 1080 window at scale 1, 30 fps, 16 s, Forward+. Expected: no tint: far floor (1500, 300) = tile colour (0.867, 0.847, 0.788), lit centre clipped to white; dusk: far floor (0.435, 0.467, 0.569), lit (900, 520) = (0.980, 0.910, 0.804).

### B04 · 39 words · ~13 s

> A soft glow is a texture. Godot's docs give the recipe. Give the light a gradient texture, set its fill to radial, and run the gradient from opaque white to transparent white. The transparent part becomes the soft edge.

*Picture.* The real Godot 4.7 'Point lights' section in a browser window. The camera pushes in on the paragraph that gives the recipe (gradient texture, fill radial, opaque white to transparent white) with one terracotta ring, then closes in on the words 'opaque white to transparent white'.

*Motion.* The camera pushes in on the recipe paragraph, then on the two colors the voice names.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: a gradient strip from white to transparent

### B05 · 41 words · ~14 s

> A point light has a few settings. Its texture sets its shape. Its scale sets how far it reaches. Color tints it, and energy is how strong it is. Change each one, and the same lamp lights the same ground differently.

*Picture.* A real Godot render: one lamp on the dusk floor. Its glow first grows (scale), then shifts from warm to cool (color), then dims and brightens (energy); a small label names each setting as the voice says it. Caption: 'reach: how far the light spreads · energy: how strong it is'.

*Motion.* The same lamp grows, changes color, then dims and brightens, one setting at a time.

*Lane.* capture · `ShaderLab` · runner-up: manim: three dials

*Capture to record.* C03: Dusk floor, one warm lamp at the centre, blob at lower right. In turn: scale 2 to 6 (smooth), colour warm to cool blue-white, energy 1.0 to 0.2 then to 1.5 (smooth). Scene = evidence/planning-checks/light_scene.gd with captures.json id C03; 1920 x 1080 window at scale 1, 30 fps, 15 s, Forward+. Expected: lamp settings read back from the scene: scale 2.0 at 4.0 s and 6.0 at 6.5 s; colour from warm (1.0, 0.86, 0.55) to cool (0.55, 0.85, 1.0) by 8.3 s; energy 0.21 at 8.7 s and 1.5 at 10.5 s (render_captures state print). No pixel probe: these are lamp settings, not shader results.

### B06 · 29 words · ~10 s

> Lights add. Two lamps overlapping make the overlap brighter, and three make it brighter still. Underneath, the dim ambient stays put, whether a light reaches a pixel or not.

*Picture.* A real Godot render: dusk floor and three warm lamps in a triangle that switch on one after another. The overlap gets brighter with each lamp while the far floor stays at its dim ambient look. Small labels '1 lamp', '2 lamps', '3 lamps' and 'ambient' (on the far floor).

*Motion.* The overlap brightens in steps as each lamp appears; the far floor does not change.

*Lane.* capture · `ShaderLab` · runner-up: manim: three overlapping circles

*Capture to record.* C04: Dusk tiled floor. Three warm lamps (scale 3.5, energy 0.4) close together in a triangle: the first is on from the start, the second appears at 'overlapping', the third at 'three make it brighter still'. Scene = evidence/planning-checks/light_scene.gd with captures.json id C04; 1920 x 1080 window at scale 1, 30 fps, 11 s, Forward+. Expected: overlap point (960, 540) steps up with each lamp (verify9 B: far floor (0.435, 0.467, 0.569) stays the same; the overlap rises from dusk to near white).

### B07 · 40 words · ~14 s

> Godot's rule, measured. The pixel is the surface color times the total of the ambient and every light. A grey surface of one half, an ambient of point two, two lamps of point four each: the pixel reads one half.

*Picture.* The rule as outlined swatch boxes on the cream stage: [surface 0.5] x ( [ambient 0.2] + [lamp 0.4] + [lamp 0.4] ) = [pixel 0.5], each swatch filled with the grey of its own number. Small grey credit: 'measured · Godot 4.7.2 · Forward+ · 0, 1, 2, 3 lamps: 0.1, 0.3, 0.5, 0.7'.

*Motion.* The two lamp boxes slide in one after the other and the result swatch fills to the sum, ending on one half.

*Lane.* manim · `B07_Formula` · runner-up: LectureEvidenceTable

### B08 · 37 words · ~13 s

> A two-D shader can have three functions. Vertex places corners, and fragment colors each pixel. The third, light, runs for every pixel and every light that reaches it, and asks: how much does this lamp add here?

*Picture.* A header strip of three outlined boxes, 'vertex()  corners', 'fragment()  pixels', 'light()  lamps'; the third is ringed. Below, one pixel cell on a small floor strip with two lamp dots; an arrow runs from each lamp to the pixel and a small 'light()' box answers each arrow with its own swatch, the swatches piling up. Caption: 'light(): once per pixel, for each light that touches it'.

*Motion.* The two arrows travel from the lamps to the pixel; each is answered by a swatch and the swatches pile up.

*Lane.* manim · `B08_PerLamp` · runner-up: DesignPipelineClaim, show-tell isometric

## Act II: The Light Function

### B09 · 42 words · ~14 s

> Add a function called light to a shader, and it replaces Godot's default lighting for that sprite. Even an empty one. The lamp still lights the blob, but the ground ignores it. The function belongs to the sprite, not to the lamp.

*Picture.* Act title 'The Light Function' (serif 40) top-left. Code card at left with the empty light() function and a definition tag on its first line ('light(): runs once per pixel for each light that touches it'); at right a real Godot window: the lit floor and the blob. At 'Even an empty one' the glow leaves the floor (only the dusk look is left) while the blob stays lit. A ring settles on the blob, labels 'default lighting' (blob) and 'empty light()' (ground).

*Motion.* The glow vanishes from the floor but stays on the blob the instant the empty function is added.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C05: Dusk tiled floor, one warm lamp (scale 5) at the centre, the blob at (1250, 700). The floor starts on default lighting; at 'Even an empty one' it switches to 01-light-empty. The blob never changes. Scene = evidence/planning-checks/light_scene.gd with captures.json id C05; 1920 x 1080 window at scale 1, 30 fps, 16 s, Forward+. Expected: floor (1100, 540) = (1.000, 0.949, 0.824) before and (0.400, 0.427, 0.518) after (tile x dusk); blob centre (0.365, 0.616, 0.561) before and after (verify8 C05).

### B10 · 38 words · ~13 s

> The smallest light function returns one flat answer: point two grey. Add a lamp, and this card brightens by point two. Add another, and it brightens again. Light runs once for each lamp, and Godot adds the answers.

*Picture.* Code card at left with the flat light() (LIGHT = vec4(0.2, 0.2, 0.2, 1.0)); at right a real Godot window: a grey card on the dusk floor. Each lamp that switches on lifts the card by one more flat step, with no soft falloff, while the floor around it shows the lamps' soft glows. Readouts '+0.2', '+0.4', '+0.6'.

*Motion.* The card brightens by the same step each time a lamp appears.

*Lane.* capture · `ShaderLab` · runner-up: manim: three stacked swatches

*Capture to record.* C06: Dusk tiled floor with three warm lamps (scale 3.4, energy 0.4) stacked near the centre that switch on at 'Add a lamp', 'Add another' and 'once for each lamp'. A grey card (0.7, 640 x 400 px) at the centre wears 02-light-flat; the floor stays on default lighting. Scene = evidence/planning-checks/light_scene.gd with captures.json id C06; 1920 x 1080 window at scale 1, 30 fps, 14 s, Forward+. Expected: card at (700, 700): (0.349, 0.384, 0.502) with no lamp, then (0.549, 0.584, 0.702), (0.749, 0.784, 0.902), (0.949, 0.984, 1.000): +0.2 per lamp (verify8 C06).

### B11 · 43 words · ~15 s

> Inside light, Godot hands you built-ins, values written in capital letters. Color is this pixel's own color, and U V is its address. Light color and light energy describe the lamp. You hand back one value, also called light: what this lamp adds.

*Picture.* A box labelled light(). Four arrows come in from the left, labelled in monospace capitals COLOR, UV, LIGHT_COLOR, LIGHT_ENERGY; one arrow leaves to the right labelled LIGHT. Caption: 'built-in: a value the engine hands to a function, or collects from it'. A grey note: 'more in the docs: NORMAL, SCREEN_UV ...'.

*Motion.* The four inputs slide into the box one after another and the single answer leaves on the right.

*Lane.* manim · `B11_FunctionBox` · runner-up: BrowserCapture of the docs table

### B12 · 42 words · ~14 s

> Light runs last. Fragment runs first and sets the pixel's color, which arrives in light as the built-in color. Then light runs once for each lamp, and Godot adds all the answers to the dim ambient look. That sum is the pixel.

*Picture.* A strip left to right on the cream stage: 'fragment()  sets color' -> 'light()  once per lamp' (two small lamp dots feed it, each answer a small swatch) -> '+ dim ambient look' -> a pixel swatch. A token travels the strip; the arrows are drawn shapes pointing only forward.

*Motion.* A token passes fragment, splits into one pass per lamp, and the answers join the ambient look to make the pixel.

*Lane.* manim · `B12_Order` · runner-up: DesignPipelineClaim, show-tell isometric

### B13 · 34 words · ~12 s

> Rebuild Godot's default. The color is the surface, times the lamp's color, times its energy. The fourth number, alpha, passes straight through. Rendered both ways, the same scene differs in no pixel at all.

*Picture.* Code card at left (the three-line light()); at right a real Godot window: one floor, one lamp on the seam. The left half uses Godot's default lighting, the right half the shader, and the join is invisible. Labels 'default' (left) and 'this shader' (right) land at the last sentence, with the caption '0 of 1,036,800 pixels differ · Forward+'. The alpha line carries the tag 'alpha: how visible a pixel is: 0 invisible, 1 solid' as alpha is spoken.

*Motion.* The two halves read as one picture; the label 'this shader' lands on the right half only.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C07: Dusk tiled floor in two halves of one picture (left half default, right half wears 03-light-default); one warm lamp (scale 6) on the seam at the centre; the blob at (1250, 700) on default lighting. Scene = evidence/planning-checks/light_scene.gd with captures.json id C07; 1920 x 1080 window at scale 1, 30 fps, 13 s, Forward+. Expected: right half against an all-default render of the same scene: max difference 0.000, 0 of 1,036,800 pixels differ (Forward+); Compatibility within one step of 255 (verify8 C07, verify3 R1).

### B14 · 37 words · ~13 s

> That fourth number is the lamp's soft edge: the texture fades from one to zero. Force it to one, and every pixel the texture covers is lit at full strength. The soft glow becomes a hard square.

*Picture.* Code card at left (rgb line, then LIGHT = vec4(rgb, 1.0)); at right a real Godot window with the soft round glow until 'Force it to one', when it snaps to a hard square exactly as wide as the lamp's texture. Labels 'soft edge' (glow) and 'hard square'. Caption: 'alpha: how visible a pixel is: 0 invisible, 1 solid'.

*Motion.* The soft glow snaps into a hard-edged square the instant alpha is forced to one.

*Lane.* capture · `ShaderLab` · runner-up: manim: a fading disc against a flat square

*Capture to record.* C08: Dusk tiled floor, one warm lamp (scale 3.2: a 819 px square texture) at the centre. Default lighting first; at 'Force it to one' the floor switches to 04-light-hard-edge. Scene = evidence/planning-checks/light_scene.gd with captures.json id C08; 1920 x 1080 window at scale 1, 30 fps, 14 s, Forward+. Expected: after the switch the lit area is a hard square ending exactly at the texture's half-width 409.6 px: added red 0.60 at 390 px and 0.0 at 430 px (verify8 C08).

### B15 · 30 words · ~10 s

> Now reshape it. Round the fade down to quarters, and the glow becomes bands, like cel shading. Same lamp, same ground. Only the light function changed how the light fades.

*Picture.* Code card at left (the bands line with the tag 'floor(x): rounds down to the whole number below', then LIGHT = vec4(rgb, bands)); at right a real Godot window: the smooth glow turns into three concentric bands like cel shading, the blob still smoothly lit beside it.

*Motion.* The smooth glow snaps into concentric bands when the fade is rounded.

*Lane.* capture · `ShaderLab` · runner-up: manim: a ramp turning into a staircase

*Capture to record.* C09: Dusk tiled floor, one warm lamp (scale 5), the blob. Default glow first; at 'the glow becomes bands' the floor switches to 05-light-bands. Scene = evidence/planning-checks/light_scene.gd with captures.json id C09; 1920 x 1080 window at scale 1, 30 fps, 12 s, Forward+. Expected: three lit bands plus the dark outer ring; on a grey 0.5 surface (verify7 C) the red channel reads 0.475, 0.349, 0.224, then 0.098 (ambient only).

### B16 · 34 words · ~12 s

> Or let time shape it. Multiply the light by the absolute value of a sine of time, and the lamp breathes. No animation player and no game code: the shader does it every frame.

*Picture.* Code card at left (the pulse line, then the rgb line that multiplies by it); at right a real Godot window where the lamp breathes brighter and dimmer. Caption: 'TIME: seconds on one clock shared by the whole game'.

*Motion.* The glow swells and fades on its own, over and over.

*Lane.* capture · `ShaderLab` · runner-up: manim sine plot

*Capture to record.* C10: Dusk tiled floor, one warm lamp (scale 5), the blob. Default glow first; at 'the lamp breathes' the floor switches to 06-light-pulse. Scene = evidence/planning-checks/light_scene.gd with captures.json id C10; 1920 x 1080 window at scale 1, 30 fps, 13 s, Forward+. Expected: red at 150 px from the lamp swings between 0.698 and 1.0 (clipped) over two seconds (verify8 C10).

### B17 · 36 words · ~12 s

> One more switch. Put render mode unshaded at the top, and the sprite ignores every light, and the ambient tint too. That is right for the lamp's own bulb. Otherwise it goes dim with the room.

*Picture.* Code card at left (shader_type and render_mode unshaded; two lines); at right a real Godot window: two pale bulb discs on the dusk floor, both dull. At 'unshaded' the right one lights up to its own bright yellow while the left stays dim. Labels 'shaded' and 'unshaded'. Caption: 'unshaded: ignores lights and the ambient tint'.

*Motion.* The right bulb jumps to full brightness the moment unshaded is added; the left one stays dim.

*Lane.* capture · `ShaderLab` · runner-up: manim: two swatches

*Capture to record.* C11: Dusk tiled floor, no lamps. Two pale bulb discs (scale 1.9, about 120 px) at (700, 540) and (1220, 540) on default lighting; at 'unshaded' the right one gets 07-unshaded. Scene = evidence/planning-checks/light_scene.gd with captures.json id C11; 1920 x 1080 window at scale 1, 30 fps, 14 s, Forward+. Expected: bulb 1 stays (0.502, 0.510, 0.447); bulb 2 goes from that to its own colour (1.0, 0.929, 0.620) (verify8 C11).

### B18 · 44 words · ~15 s

> One caution. This copy matches the default, shadows included. But the default also reads normal maps, images that say which way each pixel faces, and this copy ignores them. The docs show the extra term that fixes it. Change one thing at a time.

*Picture.* A three-row table of measured pixel counts, each row ringed as the voice reaches it. The table note defines the word: 'normal map: an image of the direction each pixel faces · Forward+'. The counts are pixels that differ by more than one step in 255, from 320 x 180 test scenes (FACTCHECK rows 38 to 41).

*Motion.* The ring steps down the three rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: two renders side by side

## Act III: Which Way Is the Light?

### B19 · 38 words · ~13 s

> Now, direction. Light direction is a vector, an arrow from this pixel toward the lamp, always length one. A pixel left of the lamp gets an arrow pointing right. A pixel above it gets an arrow pointing down.

*Picture.* Act title 'Which Way Is the Light?' (serif 40) top-left. A lamp dot in the middle of a pixel-grid field; eight pixel dots on a ring around it; from each pixel dot a short arrow of the same length points at the lamp. Labels 'LIGHT_DIRECTION' and 'length 1'. The dot left of the lamp has its arrow pointing right, the dot above has its arrow pointing down, each ringed in turn. Caption: 'vector: a bundle of two to four numbers'.

*Motion.* An arrow sprouts from every pixel dot and every one of them aims at the lamp.

*Lane.* manim · `B19_Arrows` · runner-up: ShaderLab colour wheel

### B20 · 41 words · ~14 s

> To see a number, use it as brightness. Take the arrow's x number, from minus one to one, and squeeze it into zero to one. Multiply the lamp by it. Left of the lamp, full strength. Right of the lamp, nothing.

*Picture.* Code card at left (the across line, the rgb line that multiplies by it); at right a real Godot window: the smooth glow becomes a lamp that is strongest on its left and fades to nothing on its right. Labels 'full' (left of the lamp) and 'none' (right of it).

*Motion.* The glow slides to the left half of the lamp, fading smoothly toward the right.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grey ramp strip

*Capture to record.* C12: Dusk tiled floor, one warm lamp (scale 5). Default glow first; at 'Multiply the lamp by it' the floor switches to 08-direction-ramp. Scene = evidence/planning-checks/light_scene.gd with captures.json id C12; 1920 x 1080 window at scale 1, 30 fps, 15 s, Forward+. Expected: share of the lamp left at 300 px: left 1.00, right 0.00, above 0.49, below 0.50, up-left steep 0.70 (verify8 C12).

### B21 · 41 words · ~14 s

> Turn that number into a mask with step. Step gives zero below an edge, and one at or above it. Use an edge of zero, multiply the light by the result, and only the left half of the lamp stays on.

*Picture.* Code card at left (mask = step(0.0, LIGHT_DIRECTION.x), the rgb line, LIGHT); at right a real Godot window: the smooth left-to-right fade snaps into a sharp half lamp, the left half on and the right half dark, with a clean vertical edge through the lamp. The mask line carries the tag 'step(edge, x): 0 below the edge, 1 from the edge up'.

*Motion.* The smooth fade snaps into a hard half the moment step is applied.

*Lane.* capture · `ShaderLab` · runner-up: manim: a ramp becoming a staircase

*Capture to record.* C13: Dusk tiled floor, one warm lamp (scale 5). Starts on 08-direction-ramp (the previous beat's picture); at 'multiply the light by the result' the floor switches to 09-half-light. Scene = evidence/planning-checks/light_scene.gd with captures.json id C13; 1920 x 1080 window at scale 1, 30 fps, 15 s, Forward+. Expected: share of the lamp at 300 px: left 1, right 0, above 0, below 0, up-left steep 1 (verify8 C13).

### B22 · 37 words · ~13 s

> Take the absolute value, and both sides count. Raise the edge close to one, and only pixels where the arrow is nearly sideways survive. That leaves a wedge on the left, and a wedge on the right.

*Picture.* Code card at left (mask = step(0.9, abs(LIGHT_DIRECTION.x)), the rgb line, LIGHT); at right a real Godot window: the half lamp becomes a bow-tie, one wedge pointing left and one pointing right, dark above and below.

*Motion.* The half lamp splits into two opposite wedges.

*Lane.* capture · `ShaderLab` · runner-up: manim: two cones

*Capture to record.* C14: Dusk tiled floor, one warm lamp (scale 5). Starts on 09-half-light; at 'both sides count' the floor switches to 10-bowtie-light. Scene = evidence/planning-checks/light_scene.gd with captures.json id C14; 1920 x 1080 window at scale 1, 30 fps, 14 s, Forward+. Expected: share of the lamp at 300 px: left 1, right 1, above 0, below 0, up-left steep 0 (verify8 C14).

### B23 · 36 words · ~12 s

> A directional light is different. Its arrow is the same for every pixel on screen, and its position is always zero. So a direction mask lights everything or nothing. For a beam, use a point light.

*Picture.* Two panels. Left: a lamp with five pixel dots, each with its own arrow toward the lamp (five different directions). Right: a sun disc with the same five pixel dots, every arrow identical and pointing up toward the sun. Captions: 'point light: a different arrow per pixel', 'directional light: the same arrow everywhere'. Grey note: 'its position is always (0, 0, 0) · Godot docs'.

*Motion.* On the left the five arrows differ; on the right they appear one after another and all match.

*Lane.* manim · `B23_Sun` · runner-up: ShaderLab

## Act IV: A Lighthouse

### B24 · 31 words · ~10 s

> To aim a beam, you need an arrow of your own. Cosine and sine of an angle make one, always length one. Turn the angle, and the arrow turns with it.

*Picture.* Act title 'A Lighthouse' (serif 40) top-left. A unit circle drawn in screen orientation (the vertical axis points DOWN, labelled 'y points down'); an arrow from the centre to the circle at angle a, labelled '(cos a, sin a)'; its horizontal and vertical grey projections shown as segments whose lengths change as the arrow turns clockwise through a quarter turn; the angle drawn as a small arc.

*Motion.* The arrow turns clockwise around the circle while its two projections lengthen and shorten.

*Lane.* manim · `B24_AimArrow` · runner-up: plot of sine and cosine curves

### B25 · 38 words · ~13 s

> Then compare two arrows with the dot product. It is one when they point the same way, zero at right angles, and minus one when they point opposite ways. Keep the pixels where it is close to one.

*Picture.* Two arrows from one point: a grey 'pixel arrow' fixed at 25 degrees clockwise from right, and an ink 'aim' arrow with a terracotta tip dot that sweeps from -40 to 90 degrees. A two-line caption 'dot(a, b): multiply the matching parts and add them; with a unit direction, how far a point lies along it'. A live number 'dot = 0.97' beside a horizontal bar from -1 to 1 with a marker and a tick at 0.95. The sector between the two arrows lights up, labelled 'kept', whenever the number passes the tick.

*Motion.* The aim arrow sweeps and the live number rises to one as the arrows line up, crossing the 0.95 tick.

*Lane.* manim · `B25_Agree` · runner-up: LectureEvidenceTable of three dot values

### B26 · 37 words · ~13 s

> Let time turn the angle, and the wedge turns with it: a lighthouse. Two details. Our arrow points at the lamp, so flip its sign. And because y points down, a growing angle turns the beam clockwise.

*Picture.* Code card at left (aim from cos and sin of TIME, agree = dot(-LIGHT_DIRECTION.xy, aim), the step, the rgb line, LIGHT); at right a real Godot window: a hard-edged beam turning clockwise round the lamp with the blob beside it. Caption: 'TIME: seconds on one clock shared by the whole game'. The dot line carries the tag 'dot(a, b): multiply the matching parts and add them'.

*Motion.* The wedge turns round the lamp, clockwise, while the code lines light up in turn.

*Lane.* capture · `ShaderLab` · runner-up: manim: a wedge turning on a circle

*Capture to record.* C15: Dusk tiled floor, one warm lamp (scale 7: reach 896 px) at the centre, blob at lower right. 11-lighthouse is on the floor from 0.5 s and runs on TIME; the beam turns clockwise from the +x axis at one radian per second. Scene = evidence/planning-checks/light_scene.gd with captures.json id C15; 1920 x 1080 window at scale 1, 30 fps, 14 s, Forward+. Expected: wedge span on a 300 px ring = 36 degrees (expected 36.4 for a 0.95 cutoff); the wedge centre equals TIME in radians, clockwise from +x (verify5 T, verify8 C15).

### B27 · 28 words · ~10 s

> Make the cutoff, the number inside step, a uniform: a dial your game sets from outside. Lower it, and the beam widens. Raise it, and the beam narrows.

*Picture.* Code card at left (the uniform line at the top, the step line using it); at right a real Godot window: the beam turning round the lamp gets wider as the cutoff is lowered and narrower as it is raised. Readouts 'cutoff 0.95', 'cutoff 0.7', 'cutoff 0.99'. Caption: 'uniform: a value your game sets from outside; every pixel sees the same one'.

*Motion.* The beam widens and then narrows as the dial moves.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dial next to a wedge

*Capture to record.* C16: Dusk tiled floor, one warm lamp (scale 7), blob. 12-lighthouse-width on the floor; the cutoff uniform holds 0.95, eases down to 0.7 at 'Lower the cutoff', then up to 0.99 at 'Raise it'. Scene = evidence/planning-checks/light_scene.gd with captures.json id C16; 1920 x 1080 window at scale 1, 30 fps, 11 s, Forward+. Expected: wedge span on a 300 px ring: 17, 37, 52, 74, 92 degrees for cutoff 0.99, 0.95, 0.9, 0.8, 0.7 (expected 16.2, 36.4, 51.7, 73.7, 91.1) (verify8 C16).

### B28 · 28 words · ~10 s

> Swap step for smooth step, which ramps between two edges instead of cutting, and the edge of the beam goes soft. Same lamp, same beam, a better look.

*Picture.* Code card at left (the smoothstep line); at right a real Godot window: a hard-edged beam turns, then at 'goes soft' its edge feathers while it keeps turning at the same angle. Labels 'step' then 'smooth step'; the code line carries the tag 'smoothstep(a, b, x): a smooth ramp from a to b'.

*Motion.* The beam's sharp edge feathers while the beam keeps turning.

*Lane.* capture · `ShaderLab` · runner-up: manim: a step curve and a smoothstep curve

*Capture to record.* C17: Dusk tiled floor, one warm lamp (scale 7), blob. The beam starts on 11-lighthouse (hard edge); at 'the edge of the beam goes soft' the floor switches to 13-lighthouse-soft. Both run on TIME, so the beam keeps its angle across the switch. Scene = evidence/planning-checks/light_scene.gd with captures.json id C17; 1920 x 1080 window at scale 1, 30 fps, 11 s, Forward+. Expected: hard: lit out to +-18.2 degrees, nothing beyond; soft: smoothstep 0.9 to 0.99 fades between 8 and 26 degrees (verify7 D masks 1.0, 1.0, 0.98, 0.8, 0.61, 0.44, 0.02, 0.0 at 0, 5, 10, 15, 18, 20, 25, 30 degrees).

### B29 · 34 words · ~12 s

> Add a second lamp, and light runs again for it, with its own arrows. Two beams from one shader, each starting at its own lamp, each in its own color, and no extra code.

*Picture.* Code card at left (the soft lighthouse, unchanged); at right a real Godot window: one warm lamp with its beam, then a second cool lamp appears and a second beam starts from it, each in its own color. Labels 'lamp 1', 'lamp 2'.

*Motion.* A second beam, in the second lamp's color, starts from the second lamp the moment it appears.

*Lane.* capture · `ShaderLab` · runner-up: manim: two lamps and one function

*Capture to record.* C18: Dusk tiled floor, no blob. One warm lamp (scale 5) at (560, 540) with 13-lighthouse-soft on the floor; a second, cool lamp (colour 0.6, 0.85, 1.0, scale 5) at (1360, 540) appears at 'second lamp'. Scene = evidence/planning-checks/light_scene.gd with captures.json id C18; 1920 x 1080 window at scale 1, 30 fps, 13 s, Forward+. Expected: strongest added colour on a 150 px ring: warm lamp (0.565, 0.533, 0.329), cool lamp (0.369, 0.506, 0.482) (verify8 C18); beams are parallel because both lamps aim at the same TIME angle.

### B30 · 28 words · ~10 s

> A beam exists only where a lamp reaches. Outside the lamp's texture, Godot never calls light at all. For a longer beam, scale the lamp, not the shader.

*Picture.* A real Godot window, result only: the turning beam stops at a thin grey square marking the lamp's texture; outside the square nothing is lit. At 'scale the lamp' the square and the beam grow together. Labels 'lamp reach', 'no light() here', 'scale'.

*Motion.* The beam is cut off at the square; when the lamp is scaled up the square and the beam grow together.

*Lane.* capture · `ShaderLab` · runner-up: manim: a square with a wedge

*Capture to record.* C19: Dusk tiled floor. One warm lamp (scale 2.5: reach 320 px) with 13-lighthouse-soft; a thin grey square outlines the lamp's texture; from 'scale the lamp' the lamp's scale eases from 2.5 up to 7 and the outline grows with it. Scene = evidence/planning-checks/light_scene.gd with captures.json id C19; 1920 x 1080 window at scale 1, 30 fps, 11 s, Forward+. Expected: with alpha forced to one the lit square ends exactly at the texture's half-width: added red 0.565 at 300 and 315 px, 0.0 at 325 and 340 px for half-width 320 (verify8 C19).

## Act V: Where Is the Light?

### B31 · 36 words · ~12 s

> Two more numbers. Light position is where the lamp is, and light vertex is where this pixel is. Both are in screen space: pixels of the window, counted from the top left, with y growing downward.

*Picture.* Act title 'Where Is the Light?' (serif 40) top-left. A 16:9 rectangle (the window) with an origin dot at its top-left labelled (0, 0); an x arrow along the top pointing right and a y arrow down the left side pointing DOWN. A lamp dot at (960, 540) labelled LIGHT_POSITION and a pixel dot at (1130, 640) labelled LIGHT_VERTEX, each with its coordinates. Caption: 'screen space: pixels of the window, from the top left'. Small grey: 'window 1920 x 1080'.

*Motion.* The two dots appear one after the other and their coordinates count up from the corner.

*Lane.* manim · `B31_ScreenSpace` · runner-up: ShaderLab readouts over a capture

### B32 · 34 words · ~12 s

> Subtract the lamp's position from the pixel's, and you get an arrow from the lamp to this pixel. Its length is the distance between them, in pixels. That is what the length function measures.

*Picture.* The same window frame. A lamp dot at (960, 540) and a pixel dot at (1130, 640). An arrow grows from the lamp dot to the pixel dot (terracotta dot at its tip), labelled 'pixel - lamp'; a brace along it counts up to 'length 197 px'. Under it in grey: '(170, 100)'. Caption: 'length(v): the length of a vector; of an offset, the distance'.

*Motion.* The arrow grows from the lamp to the pixel while the brace counts the distance up to 197.

*Lane.* manim · `B32_Subtract` · runner-up: ShaderLab

### B33 · 28 words · ~10 s

> Use that distance as brightness. Nothing at the lamp, a little more with every step away. Now every pixel knows exactly how far it is from the light.

*Picture.* Code card at left (d = length(LIGHT_VERTEX.xy - LIGHT_POSITION.xy), then LIGHT = vec4(vec3(d / 1000.0), 1.0)); at right a real Godot window: nothing added at the lamp and more and more brightness with every step away, filling the lamp's square. A thin ramp under the window with a marker travelling from 0 to 0.5.

*Motion.* The brightness grows outward from the lamp; the marker travels along the ramp.

*Lane.* capture · `ShaderLab` · runner-up: manim: a distance ruler

*Capture to record.* C20: Dusk tiled floor, one warm lamp (scale 4: a 1024 px square texture). 14-distance-map on the floor from the start. Scene = evidence/planning-checks/light_scene.gd with captures.json id C20; 1920 x 1080 window at scale 1, 30 fps, 11 s, Forward+. Expected: added red at 250 px = 0.247 and at 500 px = 0.498 (d / 1000); at the lamp 0 (verify8 C20).

### B34 · 36 words · ~12 s

> Step the distance against a radius, and the ground splits in two: inside and outside. Do it for two radii, subtract one from the other, and what is left is the band between them. A ring.

*Picture.* A lamp dot at the centre. Two outlined circles centred on it, radius 390 and radius 450, with chips 'step(390, d)' and 'step(450, d)'. The ground outside the small circle fills pale grey ('inside / outside'), then the ground outside the large circle is subtracted from it, and the band between the two circles is left: a ring. Labels 'radius 390', 'radius 450', 'a ring'. Caption: 'step(edge, x): 0 below the edge, 1 from the edge up'.

*Motion.* The outside of the big circle is subtracted from the outside of the small one and a ring remains.

*Lane.* manim · `B34_RingFromSteps` · runner-up: ShaderLab ring capture

### B35 · 35 words · ~12 s

> Put it together, and the lamp lights only a band of ground: the distance, two steps, one subtraction, multiplied into the light. The radius and the thickness are uniforms, so the game can change both.

*Picture.* Code card at left (two uniforms, the distance, the two steps, the rgb line); at right a real Godot window (a still): a ring of light round the lamp on the dusk floor. Labels 'radius 450' and 'thickness 60'.

*Motion.* Highlight steps from the distance and steps to the two uniform lines while the ring stays still.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C21: Still frame: dusk tiled floor, one warm lamp (scale 7), blob; 15-ring-light at its defaults (radius 450, thickness 60). One PNG at t = 0.5 s. Scene = evidence/planning-checks/light_scene.gd with captures.json id C21; 1920 x 1080 window at scale 1, 30 fps, 1 s, Forward+. Expected: lit at 395, 440, 445 px from the lamp; unlit at 370, 380, 455, 470 px (verify8 C21).

### B36 · 44 words · ~15 s

> Now the game drives it. A tween moves a value smoothly over time. Set the radius to zero from code, then tween it out to the edge of the lamp, and a ring spreads from the light. This run is scripted, not player input.

*Picture.* A three-line GDScript card at left (set the radius to zero, create a tween, tween the property to 880 over 3 seconds); at right a real Godot window: nothing at first, then a ring spreads from the lamp, thinning as it nears the lamp's edge, then does it again. A label 'scripted run' is always on screen. Caption: 'tween: Godot's way to change a value smoothly over time from GDScript'.

*Motion.* The ring spreads out from the lamp as the tween runs.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with the earlier still

*Capture to record.* C22: Dusk tiled floor, one warm lamp (scale 7: reach 896 px), blob. 15-ring-light with radius set to 0; the radius ramps 0 to 880 over 3 s (a linear tween) at 'then tween it out', and once more over 3 s as the last sentence begins. Scene = evidence/planning-checks/light_scene.gd with captures.json id C22; 1920 x 1080 window at scale 1, 30 fps, 16 s, Forward+. Expected: at 1, 2 and 3 s of a real tween the radius reads 298, 594, 880 and the ring's outer edge follows it (verify9 C); a tween on a uniform never set from code fails (verify9 C2).

### B37 · 37 words · ~13 s

> One warning. These are window pixels, so the ring does not follow your world. Zoom the camera in, and the ground doubles in size, but a ring of four hundred fifty pixels stays four hundred fifty pixels.

*Picture.* Code card at left (the ring shader, unchanged); at right a real Godot window: the ring of 450 px round the lamp; the camera zooms in, the tiles, bulb and blob double in size, but the ring does not change size. Readouts 'ring 450 px', 'zoom 1', then 'zoom 2'.

*Motion.* The world doubles around a ring that stays exactly the same size.

*Lane.* capture · `ShaderLab` · runner-up: manim: a ruler against a zooming grid

*Capture to record.* C23: Dusk tiled floor, one warm lamp (scale 7), blob; 15-ring-light at its defaults. At 'Zoom the camera in' a Camera2D zooms from 1 to 2 (smooth) over three seconds and stays at 2. Scene = evidence/planning-checks/light_scene.gd with captures.json id C23; 1920 x 1080 window at scale 1, 30 fps, 14 s, Forward+. Expected: the ring is lit at the same screen pixels (395 and 440 px lit; 380 and 455 unlit) at zoom 1 and at zoom 2 (verify6 Z, verify8 C23); the floor tiles, bulb and blob double in size.

### B38 · 44 words · ~15 s

> One more tool: mod. It counts up to a number, then starts over. Mod the pixel's x by one hundred twenty-eight, keep the first sixteen, and you get stripes. They belong to the screen, not the sprite: slide the ground, and they stay put.

*Picture.* Code card at left (the stripe line with mod and step, the rgb line, LIGHT); at right a real Godot window: vertical stripes of light inside the lamp's reach; the tiled floor slides left and right underneath while the stripes stay exactly where they are. The stripe line carries the tag 'mod(x, y): the remainder after dividing x by y'. Label 'stripes stay'.

*Motion.* The tiles slide under stripes that do not move.

*Lane.* capture · `ShaderLab` · runner-up: manim: a number line wrapping round

*Capture to record.* C24: Dusk tiled floor (2,520 px wide so it can slide), one warm lamp (scale 5). Default glow first; at 'you get stripes' the floor switches to 16-stripes-light; during the last sentence the floor slides 250 px right, then 500 px left. Scene = evidence/planning-checks/light_scene.gd with captures.json id C24; 1920 x 1080 window at scale 1, 30 fps, 16 s, Forward+. Expected: 160 lit columns (ten stripes of 16 px, 384 to 399, 512 to 527 ...) at t = 0.5 s and at t = 6 s with the floor moved: identical (verify8 C24).

### B39 · 32 words · ~11 s

> Do the same for y, and join the two with max. You get a grid of light: lines sixteen pixels wide, every one hundred twenty-eight pixels, drawn only where the lamp reaches.

*Picture.* Code card at left (cell = mod(LIGHT_VERTEX.xy, 128.0), lines = max of two steps, the rgb line, LIGHT); at right a real Godot window: the vertical stripes gain horizontal lines and become a grid of light inside the lamp's reach.

*Motion.* Horizontal lines join the stripes and make a grid.

*Lane.* capture · `ShaderLab` · runner-up: manim: two number lines crossing

*Capture to record.* C25: Dusk tiled floor, one warm lamp (scale 5). Starts on 16-stripes-light; at 'Do the same for y' the floor switches to 17-grid-light. Scene = evidence/planning-checks/light_scene.gd with captures.json id C25; 1920 x 1080 window at scale 1, 30 fps, 12 s, Forward+. Expected: horizontal line runs at x = 1000: y 384 to 399, 512 to 527, 640 to 655, 768 to 783; lines 16 px wide every 128 px, anchored to the screen (verify8 C25).

### B40 · 43 words · ~15 s

> So when does a job belong in light? When it depends on a lamp: its direction, its distance, its color. A pattern on the surface alone belongs in fragment, and a wobble in the corners in vertex. Ask where the effect comes from.

*Picture.* A three-row table, one row ringed as each kind of effect is named.

*Motion.* The ring steps down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

## Closing

### BVDT · recap · 77 words · ~26 s

> Let's recap with Claude. A pixel is its surface times the total of the ambient and every light. Writing light replaces the default, and you can rebuild it exactly. Light direction is an arrow from the pixel toward the lamp. Aim an arrow, compare it with a dot, and a mask becomes a beam. Light position and light vertex give a distance, and distance makes rings. Those positions are window pixels, so they ignore your camera zoom.

*Picture.* The recap card: A pixel is its surface times the total of the ambient and every light. / Writing light replaces the default, and you can rebuild it exactly. / Light direction is an arrow from the pixel toward the lamp. / Aim an arrow, compare it with a dot, and a mask becomes a beam. / Light position and light vertex give a distance, and distance makes rings. / Those positions are window pixels, so they ignore your camera zoom.

### BHTF · your turn · 95 words · ~32 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader with a light function, for a sprite. A narrow beam sweeps clockwise around the lamp, once every two seconds. Use the built-in light direction and the built-in time, and keep the lamp's soft edge, color and energy. Add a uniform called width. Then point me to the lines that decide where the beam is. Then check two things yourself. Does the beam turn clockwise, once every two seconds, by your own stopwatch? And when you delete the light node, does the beam disappear?

*Prompt shown and read in full:* Write a Godot canvas item shader with a light function, for a sprite. A narrow beam sweeps clockwise around the lamp, once every two seconds. Use the built-in light direction and the built-in time, and keep the lamp's soft edge, color and energy. Add a uniform called width. Then point me to the lines that decide where the beam is.

*Two checks:* Check: the beam turns clockwise, once every two seconds, by your own stopwatch. · Check: delete the light node, and the beam disappears.

### BOUT · outro · 6 words · ~4 s

> Light Shaders. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


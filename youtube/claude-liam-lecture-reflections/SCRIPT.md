# Script: Reflections

**What this is.** The words Liam will say in *Reflections*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 43 beats, 1547 words, about **8:50** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 19, manim 12, remotion 4, editor 2.

**If it runs long.** Cut, in this order: the renderer-table beat (B31), the color-distance picture (B32), then the polish pair (B34 coast, B35 tint), then the canvas-layer beat (B15). Each repeats an idea another beat carries or covers a rarer case. The hidden-map idea (B03 to B09), the copy positions (B12, B13), the rect trap (B17), the lookup and its code (B22, B23), the map toggle (B24) and the equals failure (B28, B29, B30) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | A Map Nobody Sees | 9 | 294 | ~1:40 |
| II | When the Screen Is Copied | 9 | 303 | ~1:43 |
| III | Building the Reflection | 8 | 271 | ~1:32 |
| IV | Compare With a Range | 7 | 246 | ~1:24 |
| V | Polish and Limits | 4 | 113 | ~0:38 |

## Opening

### BOPEN · identity card · 27 words · ~9 s

> Reflections. Learn how a shader can read a hidden map of the water, and use it to give a character a reflection that shows only over water.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Reflections", and the line "How a hidden map makes a reflection in Godot".

### BIDEA · the question · 44 words · ~15 s

> Hallo. This is Liam, in for Bear. Most people think a reflection means drawing the scene a second time. You do draw the character twice. But the hard part is knowing where the water is, and a shader can learn that from a map.

*Picture.* The hesitant writer types: "A reflection needs
a second drawing of the scene." then deletes "a second drawing of the scene" and types "a map the shader can read".

### BDEFS · terms · 68 words · ~23 s

> Five terms. A shader is a small program the graphics card runs to decide how something is drawn. The screen texture is a picture of what has been drawn so far, which a shader can read. Draw order says which things are drawn first. A label map is a layer of flat colors, each color a label. And a reflection is a flipped, fainter copy, seen in water.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Screen texture** — a copy of the screen made at one moment, which a shader can read; **Draw order** — what is drawn first; later things cover earlier ones; **Label map** — a layer of flat colors, each color a label; **Reflection** — a flipped, fainter copy seen in water

## Act I: A Map Nobody Sees

### B01 · 36 words · ~12 s

> Watch the reflection. The character walks along the shore, and its reflection follows in the water. Over the sandbar, the reflection disappears. No script decides that. A shader looks up a map the player never sees.

*Picture.* Act title 'A Map Nobody Sees' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal blob walks along the shoreline from left to right and its flipped reflection follows in the water, thins out over the sandbar until it is gone, and returns on the far side. Readouts 'over water' and 'over sand'.

*Motion.* The reflection follows the walker, disappears over the sandbar and comes back.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a character and its mirror image

*Capture to record.* C01: capture_scenes.gd id C01 (the pond: LabelMap, BackBufferCopy in viewport mode, Ground, Player with RemoteTransform2D, Reflection with lab-shaders/02-reflection.gdshader); the Player walks x 150 to 1200 over 11.5 s; 13.5 s, 30 fps, Forward+, 4K SubViewport route, scripted walk, fresh process.

### B02 · 35 words · ~12 s

> A shader works one pixel at a time. For each pixel of the reflection, it has to decide: show this pixel, or hide it. To decide, it needs one fact. Is there water under me?

*Picture.* A framed flat picture of the pond (grass band, water, sand spit, teal blob with its reflection area under it). Over the reflection area a grid of 8 by 6 cells appears (the pixel grid); a terracotta dot visits the cells one by one asking 'water?'; each cell then fills teal (show) where it lies over water and stays empty (hide) where it lies over the sand. Label 'show or hide?'.

*Motion.* A dot visits cell after cell and each answer decides the cell: teal where yes, empty where no.

*Lane.* manim · `B02_PixelAsks` · runner-up: ShaderLab capture with a probe overlay

### B03 · 33 words · ~11 s

> Here is that fact, drawn as a map. Water is red. The coast is green. Everything else is left empty. Each flat color is a label, so this picture is a label map.

*Picture.* The real label map layer alone on the stage colour: the water region flat red, a ring of flat green around the sandbar, everything else empty. It fades in over 2.5 s. Labels land in turn: 'water' on the red, 'coast' on the green ring (with one terracotta ring around the ring), 'empty' on the bare stage.

*Motion.* The map fades in and its labels land on the red, the green and the empty part in the order the voice says them.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of the same map

*Capture to record.* C02: capture_scenes.gd id C02 (LabelMap node only; Ground, Player, Reflection hidden; LabelMap modulate alpha 0 to 1 over 2.5 s); 13 s, 30 fps, Forward+, scripted fade.

### B04 · 40 words · ~14 s

> You could hand this map to the shader as an ordinary texture. Then, for every pixel, you must work out where it sits on the map, whatever the camera is doing. The screen is already lined up with every pixel.

*Picture.* Two panels on the cream stage. Left, 'an ordinary texture': a pixel of the pond in the world, a camera frame sliding sideways, and a chain of arrows from the pixel through a box 'your math' to a spot on the map. Right, 'the screen': the same pixel with one straight arrow to the same spot in a screen-sized copy, no box. A small label 'texture: an image a shader can read'.

*Motion.* The camera frame slides and the left chain stretches and re-routes through the math box; the right arrow stays straight.

*Lane.* manim · `B04_LinedUp` · runner-up: DesignPipelineClaim, show-tell isometric

### B05 · 28 words · ~10 s

> There is one problem. Draw the map over the game, and the player sees a red and green sea. The shader should read the map. Nobody else should.

*Picture.* The real pond with the label map drawn on top of the Ground: a red and green sea covers the water area and the ring around the sandbar, while the blob keeps walking and its reflection still works. Readout 'player sees this'.

*Motion.* The red and green sea sits over the game while the blob keeps walking.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of the stacked layers in the wrong order

*Capture to record.* C03: capture_scenes.gd id C03 (tree order Ground, LabelMap, BackBufferCopy, Player, Reflection; shader 02); the Player walks x 300 to 620 over 10 s; 10.5 s, 30 fps, Forward+, scripted walk.

### B06 · 35 words · ~12 s

> The fix is draw order. A game paints in layers, and later layers cover earlier ones. Paint the map first and the art second, and the art covers it. The player sees only the art.

*Picture.* An isometric stack on the cream stage, three flat slabs landing one after another: 'map' (red and green) first, then 'art' (the pond picture), then 'character' (the teal blob). Beside the stack a top-down thumbnail updates after each slab: after the map, red and green; after the art, only the pond (the red and green gone); after the character, the pond with the blob. Label 'later covers earlier'.

*Motion.* The art slab lowers onto the map slab and the thumbnail's red and green vanish.

*Lane.* manim · `B06_Layers` · runner-up: ShaderLab capture with layers switched on one by one

### B07 · 37 words · ~13 s

> A shader reads the screen texture: a copy of the screen made at one moment. Make it after the art, and the map is gone. Make it before the art, and the map is still in it.

*Picture.* The same slab stack. A copy frame (a camera-like rectangle) slides along the stack. Above the art slab its thumbnail shows only the pond ('no map'); slid down between the map and the art, its thumbnail shows the red and green map. Label 'copy of the screen'.

*Motion.* The frame slides down the stack and its thumbnail turns from the pond into the map.

*Lane.* manim · `B07_CopyMoment` · runner-up: LectureEvidenceTable

### B08 · 23 words · ~8 s

> Godot has a node for choosing that moment: Back Buffer Copy. It makes its copy at its own place in the draw order.

*Picture.* The slab stack with a node chip labelled 'BackBufferCopy' sliding in between the map slab and the art slab; the copy frame snaps onto the chip and its thumbnail shows the map. A one-line label from the docs: 'copies the screen for a shader to read'.

*Motion.* The chip slides between the slabs and the copy frame snaps onto it.

*Lane.* manim · `B08_CopyNode` · runner-up: BrowserCapture of the BackBufferCopy docs page

### B09 · 27 words · ~9 s

> And the draw order is the scene tree. The top of the Scene dock is drawn first. So the order is: map, copy node, art, character, reflection.

*Picture.* A real frame of Godot's Scene dock for the pond scene: Pond, then LabelMap, BackBufferCopy, Ground, Player (with RemoteTransform2D under it) and Reflection, top to bottom. A readout 'drawn first' by the top row, then one terracotta ring moves down the rows as the voice names map, copy node, art, character, reflection.

*Motion.* The ring steps down the rows in the order the voice names them.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench tree mode (labelled reconstruction)

*Capture to record.* E1: Godot's own editor on the scratch pond project (evidence/planning-checks/make-editor-project.sh builds it; verified by verify_scene_file.gd): one frame (Pond selected) recorded at 2560 x 1440 with the Light preset and a 2x UI by evidence/planning-checks/record-editor-frames.sh, cropped to the box (0, 60) to (440, 420). The ring boxes are measured on that crop (rows LabelMap, BackBufferCopy, Ground, Player, Reflection); a planning frame of exactly this crop is png/planning-frame-E1-scene-dock.png.

## Act II: When the Screen Is Copied

### B10 · 39 words · ~13 s

> Three flat sprites: A drawn first, then B, then C on top. The window shows what a shader reads when it asks for the screen texture. A hint after the colon tells Godot to fill it with the screen.

*Picture.* Act title 'When the Screen Is Copied' (serif 40) top-left. Code card at left (the six-line preview shader); at right a real Godot window: three flat overlapping squares A (teal), B (blue), C (lavender), drawn in that order on the stage colour. At about a quarter of the way in a small framed window appears at top right showing a miniature of the whole screen with A, B and C in it.

*Motion.* The window appears and shows the three squares in miniature while the code lines are highlighted.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C04: capture_scenes.gd id C04 (Sprite2D A, B, C, then ColorRect preview with lab-shaders/01-screen-preview.gdshader and a border panel drawn after it; no BackBufferCopy node; the window is switched on at 3.5 s); 14.5 s, 30 fps, Forward+, scripted.

### B11 · 32 words · ~11 s

> By default, Godot makes that copy the first time a shader asks for it, right before that shader's node is drawn. So the shader sees everything drawn before it, and nothing after.

*Picture.* A stack of three flat sprites A, B, C (the act's three colours) with a window-shaped 'shader' chip hovering above. As the chip drops toward the stack a copy frame appears automatically right under the chip and captures A, B and C; a thumbnail shows all three. Caption 'the first shader that reads the screen triggers the copy'.

*Motion.* The shader chip drops toward the stack and, just before it lands, a copy frame appears under it and captures A, B and C.

*Lane.* manim · `B11_FirstReader` · runner-up: BrowserCapture of the screen-reading docs page

### B12 · 38 words · ~13 s

> Now add a Back Buffer Copy. After C, the window shows all three. Move it between B and C, and C vanishes from the window. C is still on the screen. It is only missing from the copy.

*Picture.* The same three squares and window. At 2.5 s a BackBufferCopy node is added after C: the window still shows A, B and C. At 5.5 s the node is moved between B and C: C vanishes from the window while C stays in the main picture. Readouts 'copy after C' then 'B copy C' (the draw order, copy node between the two); one terracotta ring on the window after the change.

*Motion.* C vanishes from the window while it stays on the screen.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with the preview code

*Capture to record.* C05: capture_scenes.gd id C05 (three squares and window; BackBufferCopy in viewport mode added after C at 2.5 s, move_child to between B and C at 5.5 s); 14 s, 30 fps, Forward+, scripted tree changes.

### B13 · 28 words · ~10 s

> Between A and B, only A is left. Before A, the window is empty. The node never changes what is drawn. It only changes what the copy contains.

*Picture.* The same scene continued: the node starts between B and C, is moved between A and B at 1 s (only A is left in the window) and before A at 3.6 s (the window is empty), while the main picture never changes. Readouts 'A copy B' then 'before A'.

*Motion.* The window empties step by step while the main picture stays full.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with the preview code

*Capture to record.* C06: capture_scenes.gd id C06 (three squares and window; BackBufferCopy starts between B and C, move_child to between A and B at 1.0 s and to first at 3.6 s); 10.5 s, 30 fps, Forward+, scripted.

### B14 · 41 words · ~14 s

> Only the first shader that reads the screen triggers a copy. Here it sits before C, so it misses C. The second shader, after C, reuses that copy and misses C too. A new Back Buffer Copy between them refreshes it.

*Picture.* The three squares with two windows on the right, one above the other. The first window sits between B and C in the tree, the second after C; with no copy node both windows miss C. At 10.5 s a BackBufferCopy is added between C and the second window: the second window now shows A, B and C, the first still does not. Readouts 'first reader', 'second reader', 'new copy'.

*Motion.* The second window gains C the moment a copy node appears; the first window never does.

*Lane.* capture · `ShaderLab` · runner-up: BrowserCapture of the Back-buffer logic paragraph

*Capture to record.* C07: capture_scenes.gd id C07 (tree A, B, preview 1 with border, C, preview 2 with border; BackBufferCopy added between C and preview 2 at 10.5 s); 15 s, 30 fps, Forward+, scripted. The lower window's miniature also shows the upper window (it is part of the screen by then): expected.

### B15 · 33 words · ~11 s

> Tree order is not the only lever. Z index and canvas layers change the draw order too, and the copy follows them. But a copy only serves shaders on its own canvas layer.

*Picture.* Three transparent sheets stacked in isometric view, labelled 'layer -1', 'layer 0', 'layer 1' (a small note 'a CanvasLayer node'). On layer -1 the map; on layer 0 the copy node, the art and the reflection (a window chip); on layer 1 a second window chip. A glowing arrow runs from the copy node to the reflection on its own sheet; an arrow toward the chip on layer 1 stops at the sheet edge with a cross. A side chip 'z index' reorders items inside one sheet.

*Motion.* The copy's arrow reaches the reflection on its own sheet and the arrow to the other sheet stops at the edge.

*Lane.* manim · `B15_CanvasSheets` · runner-up: LectureEvidenceTable (z index, layers, same layer)

### B16 · 27 words · ~9 s

> Back Buffer Copy has three modes. Viewport copies the whole screen. Rect copies only a box. Disabled copies nothing, so Godot falls back to its automatic copy.

*Picture.* The real Godot 4.7 BackBufferCopy class page in a browser window; the camera pushes in on the three CopyMode constants (Disabled, Rect, Viewport) with their one-line descriptions and one terracotta ring marks the list. The ring box is a placeholder: set it from the real capture.

*Motion.* The camera pushes in on the three modes the voice is naming.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: three small boxes (whole screen, a box, nothing)

### B17 · 40 words · ~14 s

> A new Back Buffer Copy starts in Rect mode. The box covers only a corner of the screen, wherever the node is. Outside it, the docs call the result undefined. Here the window reads black until the mode becomes Viewport.

*Picture.* The three squares and the window, with the node in Rect mode at its defaults: the window is black except a tiny stage-coloured patch at its top-left corner (the only part copied). At 9 s the mode is switched to Viewport and the window fills with A, B and C. Readouts 'Rect mode' then 'Viewport'; one terracotta ring on the tiny patch.

*Motion.* A black window with a tiny patch fills with the three squares when the mode becomes Viewport.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with the pond and the reflection

*Capture to record.* C08: capture_scenes.gd id C08 (three squares and window; BackBufferCopy with copy_mode Rect at its default rect, node at (100,100); copy_mode set to Viewport at 9.0 s); 14.5 s planned, 30 fps, Forward+. MUST run in a fresh Godot process (the black needs an empty back buffer). 1:1 ROUTE, not the 4K route: a Rect box is measured in render pixels (run-13: on the 4K route the default box is only 34 canvas units), so capture_scene.sh renders C08 in the 1280 x 720 window itself, where the default box is the 100 px corner of the screen (run-10), and enlarges the frames 3x by whole pixels. The corner patch is 38 x 38 px in the window (0.578 to 0.608 of the frame's width, 0.078 to 0.131 of its height); the rect does not follow the node.

### B18 · 25 words · ~8 s

> In the editor, select the node and set Copy Mode to Viewport. If the map spreads over the whole screen, that is the safe choice.

*Picture.* A real frame of Godot's Inspector with the BackBufferCopy node selected: the Copy Mode property reads Viewport. One terracotta ring settles on the Copy Mode row.

*Motion.* The ring settles on the Copy Mode row.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench inspector mode (labelled reconstruction)

*Capture to record.* E2: Godot's own editor on the scratch pond project, BackBufferCopy selected, recorded with record-editor-frames.sh and cropped to the box (2140, 60) to (2560, 420) of the 2560 x 1440 frame; the ring is measured on that crop. The planning frame png/planning-frame-E2-inspector-copy-mode.png already shows 'Copy Mode: Viewport' (label and value confirmed, and the options Disabled, Rect, Viewport are in the ClassDB list of run-07).

## Act III: Building the Reflection

### B19 · 31 words · ~10 s

> Back to the pond. A reflection is the character again: the same picture, flipped upside down, placed right under its feet. On a Sprite two D, switch on the vertical flip.

*Picture.* Act title 'Building the Reflection' (serif 40) top-left. The real pond with the blob standing on the shoreline. At about 2 s a flipped copy of the blob fades in right under its feet (the copy has no shader yet); a terracotta ring marks where the feet meet the copy and a label 'Flip V' lands beside the copy.

*Motion.* A flipped copy fades in directly under the feet.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a blob and its mirror image

*Capture to record.* C09: capture_scenes.gd id C09 (pond; Reflection is a plain flipped copy, no material, modulate alpha 0 to 1 over 2.0 to 3.0 s; Player static at x 520); 11 s, 30 fps, Forward+, scripted.

### B20 · 34 words · ~12 s

> To keep it in step, give the character a Remote Transform two D. It pushes the character's position to another node whenever the character moves, so the reflection can sit anywhere in the tree.

*Picture.* A small scene-tree diagram: 'Player' (teal blob icon) with a child chip 'RemoteTransform2D'; a separate branch 'Reflection' (a flipped blob icon); a dashed line from the chip to the Reflection node. Under the diagram, a strip of shoreline: the blob slides right along it and the flipped blob under it follows in lockstep while the dashed line pulses each time. A label from the docs: 'pushes its transform to another node'.

*Motion.* The blob slides right and the flipped blob under it follows in lockstep, the dashed line pulsing.

*Lane.* manim · `B20_FollowsAlong` · runner-up: GodotDevWorkbench tree mode (labelled reconstruction)

### B21 · 30 words · ~10 s

> Walk the character along the shore and the reflection follows, but it knows nothing about water. Over the sandbar, it hangs in the sand. Something has to hide it there.

*Picture.* The real pond with the plain flipped copy following the blob along the shoreline: over the open water it looks right, but when the blob passes the sandbar the copy is drawn right over the sand. Readouts 'no map yet' then 'in the sand'; one terracotta ring on the copy over the sand.

*Motion.* The copy slides over the sandbar and stays visible on the sand.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of the failure

*Capture to record.* C10: capture_scenes.gd id C10 (pond; Reflection plain flipped sprite, no material; Player walks x 300 to 1000 over 10.5 s); 11.5 s, 30 fps, Forward+, scripted walk.

### B22 · 37 words · ~13 s

> So the shader on the reflection looks up the same spot in the screen texture, using screen U V: a pixel's address on the whole screen. That texture holds the map, so the spot holds the label.

*Picture.* Two linked panels of the pond: left 'the screen' with a terracotta dot on one pixel of the reflection, right 'the copy' (the red and green map) with its twin dot at the same place; a dashed link between the dots and the tag 'screen UV: the same address in both'. The dot moves along the reflection and its twin moves with it; the colour under the twin changes the small label from 'water' to 'sand' as the dot crosses onto the sandbar. A label 'screen UV: a pixel's address on the whole screen'.

*Motion.* The dot on the reflection moves and its twin on the map moves with it; the label under the twin turns from 'water' to 'sand'.

*Lane.* manim · `B22_SameAddress` · runner-up: ShaderLab with the preview window

### B23 · 33 words · ~11 s

> The color it finds is the label. If it is close to red, this pixel is over water, so keep it. If not, set its alpha, how visible the pixel is, to zero.

*Picture.* Code card at left (the ten-line reflection shader); at right the real pond with the shader on the reflection: the blob walks, the reflection shows over water and is gone over the sandbar. The lines light up as the voice reads: the lookup line, the water test, the alpha line. Readouts 'keep' over water and 'alpha zero' near the sandbar.

*Motion.* The lookup, test and alpha lines light up in turn while the reflection shows over water and vanishes over the sand.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C11: capture_scenes.gd id C11 (pond; shader lab-shaders/02-reflection.gdshader; Player walks x 300 to 1000 over 11.5 s); 12.5 s, 30 fps, Forward+, scripted walk.

### B24 · 36 words · ~12 s

> Here is the proof that the map is hidden. Switch the Label Map node off, and the picture does not change, except the reflection is gone. The map is invisible, and it is doing the work.

*Picture.* The real pond with the blob walking over open water. At 4.5 s the LabelMap node is switched off: the picture does not change except that the reflection disappears. At 9.5 s it is switched on again and the reflection returns. Readouts 'Map on', 'Map off', 'Map on'.

*Motion.* The reflection vanishes and returns as the LabelMap node is switched off and on, and nothing else in the picture changes.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of two frames and what differs between them

*Capture to record.* C12: capture_scenes.gd id C12 (pond; shader 02; Player walks x 180 to 620 over 12.5 s over open water; LabelMap.visible false from 4.5 s to 9.5 s); 13 s, 30 fps, Forward+, scripted.

### B25 · 36 words · ~12 s

> If the reflection never shows, check the order. Copy after the art: the shader reads the art, finds no red, and hides everything. Map over the art: the reflection works, and so does the red sea.

*Picture.* The real pond. State one: map, copy, art (the reflection shows). At 4 s the copy node is moved after the art: the reflection disappears and nothing else changes. At 9.5 s the LabelMap is moved over the art: a red and green sea covers the pond and the reflection is back. Readouts show the order ('map · copy · art', 'map · art · copy', 'art · map · copy') and the outcome ('reflection', 'no reflection', 'red sea').

*Motion.* The reflection disappears when the copy moves after the art; a red sea covers the pond when the map moves over it.

*Lane.* capture · `ShaderLab` · runner-up: manim stack with the copy frame moving

*Capture to record.* C13: capture_scenes.gd id C13 (pond; shader 02; Player walks x 300 to 560; move_child(BackBufferCopy, Ground's index) at 4.0 s; move_child(LabelMap, Ground's index) at 9.5 s); 13.5 s, 30 fps, Forward+, scripted.

### B26 · 34 words · ~12 s

> The art must be opaque. At ninety percent, the red and green show through faintly, and the ring around the sandbar gives it away. Cover the map completely, or the player will see it.

*Picture.* The real pond. At 3 s the art layer's opacity eases from 100 to 90 percent: the water turns a faint periwinkle and a pale green ring shows around the sandbar, the map leaking through. At 9.5 s it returns to 100 percent and the leak is gone. Readouts 'art 100%', 'art 90%', 'art 100%'; a terracotta ring on the leaking green ring while it shows.

*Motion.* A faint purple tint and a green ring appear when the art drops to ninety percent and disappear when it returns to full.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of an overlay with alpha

*Capture to record.* C14: capture_scenes.gd id C14 (pond; shader 02; Ground modulate alpha 1.0, eased to 0.9 over 3.0 to 4.0 s, back to 1.0 at 9.5 s); 13 s, 30 fps, Forward+, scripted. The stage colour shows through the art at 0.9, so the whole picture lightens a little: expected.

## Act IV: Compare With a Range

### B27 · 39 words · ~13 s

> A moment ago, the shader asked whether the color was close to red, not equal to red. That was on purpose. Godot's documentation warns that comparing decimal numbers with equals may not come out true. Compare against a range.

*Picture.* Title 'Compare With a Range' (serif 40) on the real Godot 4.7 shading-language page, scrolled to the Flow control paragraph that says to compare floating-point values against a range instead of an exact number; the camera pushes in and one terracotta ring marks the sentence. The ring box is a placeholder: set it from the real capture.

*Motion.* The camera pushes in on the warning the voice is describing.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: 'a == b' with a cross over it

### B28 · 32 words · ~11 s

> Here is what goes wrong with equals. Same pond, but the water is painted at half strength, and the shader asks for exactly point five. Nothing matches, so the reflection never shows.

*Picture.* Title 'Compare With a Range'. Code card at left (the nine-line equals shader, the compare line lit as the voice says 'exactly point five'); at right the real pond whose water was painted at half strength: the blob walks and no reflection ever appears. Readouts 'water: half red' at the top and 'no reflection' below the blob.

*Motion.* The blob walks and the reflection never appears while the equals line is lit.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C15: capture_scenes.gd id C15 (pond with the water painted (128,0,0); shader lab-shaders/04-compare-equal.gdshader; Player walks x 250 to 700 over 10.5 s); 12 s, 30 fps, Forward+, scripted walk.

### B29 · 28 words · ~10 s

> Ask for a distance instead, and the same map works. How far is this color from half red? Within a tenth counts as water. The reflection is back.

*Picture.* Code card at left (the same nine lines with a distance test, the changed line lit); at right the same half-strength pond: the reflection is there as the blob walks. Readouts 'water: half red' and 'reflection back'.

*Motion.* The reflection shows as the blob walks while the distance line is lit.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C16: capture_scenes.gd id C16 (the same half-red pond; shader lab-shaders/05-compare-distance.gdshader; Player walks x 250 to 700 over 10 s); 10.5 s, 30 fps, Forward+, scripted walk.

### B30 · 37 words · ~13 s

> Why did equals fail? The screen stores each color channel in eight bits, so two hundred fifty-six steps. Half strength lands on step one hundred twenty-eight, which reads back as point five oh two. Not point five.

*Picture.* The series' 0 to 1 ramp strip zoomed around 0.5 so tick marks are visible at k/255, with the ticks 127 and 128 labelled 0.498 and 0.502. A terracotta marker 'asked for 0.5' sits between the two ticks, on no tick. The painted value snaps to the 128 tick and a readout shows '0.502'. A small label '256 steps per channel' and a grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ and Compatibility read the same'.

*Motion.* The marker lands between two ticks while the painted value snaps to the 128 tick and reads 0.502.

*Lane.* manim · `B30_EightBits` · runner-up: LectureEvidenceTable

### B31 · 28 words · ~10 s

> You can make equals pass by writing one hundred twenty-eight over two hundred fifty-five. It passed in Forward Plus and failed in Compatibility. The distance passed in both.

*Picture.* A two-row table, one row ringed as each renderer is named.

*Motion.* The ring moves down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

### B32 · 37 words · ~13 s

> Think of a color as a point. Red is one corner, green another. A radius of a tenth around each is wide enough to catch the painted color, and narrow enough to keep red and green apart.

*Picture.* A square colour plane (red channel across, green channel up) with the red point at the bottom right and the green point at the top left, each with a terracotta circle of radius 0.1 (labelled 'water' and 'coast'). A small dot, the pixel's colour, slides from red toward green: inside the red circle the label reads 'water', outside both 'neither', inside the green circle 'coast'. A tiny ruler shows the radius 0.1 and the distance between red and green, about 1.4.

*Motion.* The dot slides from red toward green and the label changes as it enters and leaves the two circles.

*Lane.* manim · `B32_ColorDistance` · runner-up: LectureEvidenceTable

### B33 · 45 words · ~15 s

> Better still, paint the map in pure values, zero or full. They read back the same in both renderers, and with the H D R two D setting on. Half strength does not: point five oh two normally, point two one six with it on.

*Picture.* A two-row table, one row ringed as each painted value is named.

*Motion.* The ring moves from the full row to the half row with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim ramp strip

## Act V: Polish and Limits

### B34 · 34 words · ~12 s

> Now the coast. Paint it green, read it the same way, and give it a lower alpha. The shader adds the two. The reflection is stronger in open water and fainter around the sandbar.

*Picture.* Title 'Polish and Limits' (serif 40). Code card at left (the fourteen-line final shader; the coast constant, the coast test and the alpha sum lit in turn); at right the real pond: the reflection stands in open water at half strength, then the blob walks toward the sandbar and the reflection grows fainter across the green ring before the sand hides it. Readouts 'open water' and 'coast'.

*Motion.* The reflection is stronger in open water and fainter as it crosses the ring around the sandbar.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C17: capture_scenes.gd id C17 (pond; shader lab-shaders/03-reflection-final.gdshader with the tint uniform set to the sprite's own colour so only the alpha shows; Player static at x 420 until 7.0 s, then walks to x 900 by 12.5 s); 13 s, 30 fps, Forward+, scripted.

### B35 · 27 words · ~9 s

> Last, a tint. Mix blends two colors by an amount. Here it is halfway toward blue. Now the reflection reads as water, not as a second character.

*Picture.* Code card at left (the same fourteen lines; the mix line lit, then the tint uniform); at right the real pond with the blob standing still: the reflection is teal-grey, then turns a clearer blue as the tint is switched on, off, and on again. Readouts 'no tint' and 'tint'.

*Motion.* The reflection's color shifts toward blue each time the tint is switched on.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C18: capture_scenes.gd id C18 (pond; shader 03; Player static at x 420; the tint uniform set to the sprite colour (no effect) or to (0.2, 0.5, 1.0): blue from 1.8 s to 3.2 s and from 4.6 s on); 10.5 s, 30 fps, Forward+, scripted.

### B36 · 25 words · ~8 s

> Two limits. This reflects the character only, so the sky and the shore are not in it. Mirroring the whole screen is a different technique.

*Picture.* The pond picture with a waterline drawn across it: sky, grass and the blob above; below it the reflection area. Under the line a flipped teal blob stays; dashed flipped outlines of the sky band and the grass band try to appear under the line and are each crossed out. A small label 'the character only'.

*Motion.* Dashed flipped outlines of the sky and the grass appear under the waterline and are crossed out; only the flipped blob stays.

*Lane.* manim · `B36_NoScenery` · runner-up: ShaderLab capture of the mirror-the-screen technique

### B37 · 27 words · ~9 s

> And the reflection moves with the character. When the character jumps, the reflection rises too, where a real one would drop, and the shoreline cuts it off.

*Picture.* The real pond with the blob standing at the shore. It jumps 80 px up, twice. Each time the reflection also moves up (where a real one would move down) and the top part of it is cut off at the shoreline. Readouts 'jump' and a terracotta ring on the cut part.

*Motion.* The blob jumps up and the reflection rises with it and is cut off at the shoreline.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a mirror image dropping

*Capture to record.* C19: capture_scenes.gd id C19 (pond; shader 03; Player static at x 300; Player.y lifted 80 px by a half sine over 3.0 to 4.0 s and again over 6.5 to 7.5 s); 10.5 s, 30 fps, Forward+, scripted.

## Closing

### BVDT · recap · 85 words · ~29 s

> Let's recap with Claude. A label map is a layer of flat colors, drawn first and covered by the art. A Back Buffer Copy makes the screen texture at its own place in the draw order. The reflection is a flipped copy that follows the character and shows only where the map says water. Compare map colors with a distance, never with equals. Paint the map in pure values: zero or full. Coast and tint polish the look, and the reflection shows the character only.

*Picture.* The recap card: A label map is a layer of flat colors, drawn first and covered by the art. / A Back Buffer Copy makes the screen texture at its own place in the draw order. / The reflection is a flipped copy that follows the character and shows only where the map says water. / Compare map colors with a distance, never with equals. / Paint the map in pure values: zero or full. / Coast and tint polish the look, and the reflection shows the character only.

### BHTF · your turn · 91 words · ~31 s

> Your turn. Paste this into Claude: Give my Godot two D character a reflection that shows only over water, using a hidden label map. Draw the map first, in pure red. Then a Back Buffer Copy in viewport mode, then my opaque ground. The reflection's shader should keep only pixels within a tenth of red. Then point me to the three lines I should check. Then check two things yourself. Does the red map ever show in the running game? And does the reflection show over water and disappear over land?

*Prompt shown and read in full:* Give my Godot two D character a reflection that shows only over water, using a hidden label map. Draw the map first, in pure red. Then a Back Buffer Copy in viewport mode, then my opaque ground. The reflection's shader should keep only pixels within a tenth of red. Then point me to the three lines I should check.

*Two checks:* Check: the red map never shows in the running game. · Check: the reflection shows over water and is gone over land.

### BOUT · outro · 5 words · ~4 s

> Reflections. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


# Script: Local, World and Screen Space

**What this is.** The words Liam will say in *Local, World and Screen Space*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 46 beats, 1770 words, about **10:06** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: manim 24, capture 12, remotion 2, editor 1, terminal 1.

**If it runs long.** Cut, in this order: the hole beat (B24), the wrong-order beat (B29), the turn-and-stretch beat (B22) and the parents warning (B11): each repeats an idea another beat carries, and none leans on its neighbours. Only if that is not enough, drop the frag coord beat (B31) and its tile in capture C10, and change 'four' to 'three' in B26 and B33 and the counting words in B30 to B32 (re-voice those beats). The sky window (B21), the world colors (B16), the four-tile agreement (B33) and the two-move test (B36, B37) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Three Addresses | 7 | 252 | ~1:26 |
| II | From Local to World | 9 | 346 | ~1:58 |
| III | Locked to the World | 9 | 320 | ~1:49 |
| IV | Where Is the Screen? | 9 | 323 | ~1:50 |
| V | Choosing a Space | 6 | 215 | ~1:13 |

## Opening

### BOPEN · identity card · 33 words · ~11 s

> Local, World and Screen Space. Learn why one point has three sets of numbers, and how a shader switches between them to pin an effect to a sprite, the world or the screen.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Local, World and Screen Space", and the line "One point, three sets of numbers, and how to switch".

### BIDEA · the question · 46 words · ~16 s

> Hallo. This is Liam, in for Bear. A shader is handed a position, and it is tempting to treat that as a plain fact. It is not. A position is an address in some space, and the same point has a different address in every space.

*Picture.* The hesitant writer types: "A position is just a position." then deletes "just a position" and types "an address in some space".

### BDEFS · terms · 68 words · ~23 s

> Six terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture on screen. An origin is where the numbers are zero. A space is a way of measuring positions from one origin. A vertex is a corner point of a shape. And a texture is an image a shader can read by address.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Pixel** — one dot of the picture on screen; **Origin** — where the numbers are zero; the middle of a centered sprite; **Space** — a way of measuring positions from one origin; **Vertex** — a corner point of a shape; **Texture** — an image a shader can read by address

## Act I: Three Addresses

### B01 · 38 words · ~13 s

> Two sprites, one starfield. The left sprite carries its stars along as it slides. The right one slides over a sky that stays put. Same picture, same motion. The only difference is what each position is measured from.

*Picture.* Act title 'Three Addresses' (serif 40) top-left. A real Godot render in a framed window: a faint copy of a star sky (indigo, cream stars, a ringed planet) behind two test sprites in one row. Both slide right together, slowly. Stars inside the left sprite travel with it; the right sprite uncovers the planet and stars that stay where they are, lining up with the faint copy. Labels: 'from the sprite' under the left, 'from the world' under the right.

*Motion.* Both sprites make the same slide, but only the left one's stars move with it; the right one uncovers a planet that does not move.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of two sprites with dots inside

*Capture to record.* C01: scene script capture-scenes/capture-c01.gd (CAPTURE-PLAN.md): faint backdrop ColorRect (02-sky-world, alpha 0.35), blob sprites (256 px art, scale 1) at y=240, left with 01-sky-local.gdshader from x=220, right with 02-sky-world.gdshader from x=700; both slide +300 over 10 to 56 % of the beat (ease in-out) and rest; 14 s, 30 fps, Forward+, no input (CAPTURE-PLAN.md).

### B02 · 39 words · ~13 s

> A position is two numbers, and they mean nothing until you say where zero is. From this zero, the dot is five across and four down. Move the zero, and the same dot is one across and three down.

*Picture.* A plane of outline cells (pixel grid, no fill). A terracotta dot sits fixed at one cell. A zero marker (a ring with a right arrow and a down arrow) sits at the top-left with a live readout '5 across · 4 down'. The zero marker then slides to a cell four across and one down; the readout counts to '1 across · 3 down' while the dot never moves.

*Motion.* The zero slides across the grid and the two numbers change continuously while the dot stays where it is.

*Lane.* manim · `B02_MoveTheZero` · runner-up: LectureEvidenceTable (two coordinate pairs)

### B03 · 34 words · ~12 s

> Godot gives you three zeros that matter. The sprite's own center: local space. The world's origin: world space. The window's top-left corner: screen space. One corner of one sprite has an address in each.

*Picture.* One scene on the cream stage: a large outlined rectangle for the world with a zero marker at its top-left labelled 'world space'; inside it a smaller outlined rectangle for the window; inside that a sprite (square outline with the test blob) with a zero marker at its center labelled 'local space'; a third zero marker at the window's top-left labelled 'screen space'. Short definitions appear with each label: 'from the node's own zero', 'from the world's origin' and, for the third, the glossary wording 'pixels of the window, counted from the top left, y growing downward'. A terracotta dot marks the sprite's top-left corner and stays through the act.

*Motion.* The three zero markers land one by one, each with its label, in the same picture.

*Lane.* manim · `B03_ThreeZeros` · runner-up: DesignPipelineClaim, show-tell isometric

### B04 · 35 words · ~12 s

> Start local. A sprite's zero sits at its center, and this one is one hundred twenty-eight pixels wide. So its top-left corner is minus sixty-four, minus sixty-four. Slide the sprite anywhere, and that answer holds.

*Picture.* The same diagram zoomed on the sprite: its center zero marker with a right arrow and a down arrow, a '128' dimension across the top, and a grey arrow from the zero to the terracotta corner dot with the tag '(-64, -64)'. The sprite, its zero and its arrow then slide to the right across the world; the tag does not change.

*Motion.* The sprite slides away with its zero and its arrow; the tag '(-64, -64)' stays exactly the same.

*Lane.* manim · `B04_LocalAddress` · runner-up: ShaderLab capture of a color-coded sprite

### B05 · 37 words · ~13 s

> In world space, zero is the world's origin. Put the sprite at six hundred, four hundred, and the same corner reads five thirty-six, three thirty-six. Slide the sprite, and these numbers change. The local ones did not.

*Picture.* The world rectangle with its zero marker at the top-left. A long grey arrow runs from the world zero to the terracotta corner dot with the tag '(536, 336)'; a small grey tag '(-64, -64)' stays beside the sprite. The sprite slides right by a hundred: the arrow stretches and the world tag counts up to '(636, 336)' while the small local tag does not move.

*Motion.* The long arrow from the world's origin stretches as the sprite slides; its tag counts up while the local tag stays put.

*Lane.* manim · `B05_WorldAddress` · runner-up: LectureEvidenceTable (two rows)

### B06 · 32 words · ~11 s

> On screen, zero is the window's top-left corner, and the camera decides which part of the world the window shows. With the camera here, the corner lands at two eighty-six, two thirty-six.

*Picture.* The world rectangle, with the window rectangle (the camera's view) drawn on it and its own top-left zero marker labelled 'screen space'. A grey arrow runs from the window's zero to the terracotta corner dot with the tag '(286, 236)'. A small camera mark sits at the window's center; the world zero and its '(536, 336)' tag stay faintly visible.

*Motion.* The arrow from the window's corner draws out to the dot and its tag lands; the world tag stays where it was.

*Lane.* manim · `B06_ScreenAddress` · runner-up: ShaderLab capture of the same scene

### B07 · 37 words · ~13 s

> Pan the camera right by a hundred. The corner slides left on screen, to one eighty-six. Its world address does not move at all. The window slid over the world, and the world stayed where it was.

*Picture.* A real Godot render: a faint star sky as the world, a 128 px test sprite in a thin cream box with a terracotta dot on its top-left corner, and a camera that pans right by a hundred. Readouts: 'world 536, 336' stays; 'screen 286, 236' changes to 'screen 186, 236' as the sprite and the whole sky slide left.

*Motion.* The corner dot slides left on screen while its world readout never changes.

*Lane.* capture · `ShaderLab` · runner-up: manim: a window sliding over the world with ticking numbers

*Capture to record.* C02: scene script capture-scenes/capture-c02.gd: Camera2D (890,460) to (990,460) over 12 to 40 % of the beat (ease in-out), sprite (600,400) 128 px art scale 1 with a drawn cream box and a terracotta corner dot (radius 6), backdrop sky ColorRect (alpha 0.5) covering world (0,0) to (2000,1000); 13 s (CAPTURE-PLAN.md).

## Act II: From Local to World

### B08 · 44 words · ~15 s

> A shader starts out in local space. The vertex function runs once for each corner, and a built-in called vertex holds that corner's position in pixels. Its zero is the node's own: the center of a sprite, the top-left corner of a color rect.

*Picture.* Act title 'From Local to World' (serif 40) top-left. On the left a sprite (square outline, test blob) with a zero marker at its center; its four corners flash in turn with the tags '(-64,-64)', '(64,-64)', '(-64,64)', '(64,64)', a chip 'VERTEX' riding each tag, and a small card 'vertex(): runs once for each vertex; places the corners' with a counter 'run 1, 2, 3, 4' that steps as each corner flashes. On the right a color rect (outlined rectangle) with its zero marker at its top-left corner and the tags '(0, 0)', '(300, 0)', '(0, 200)', '(300, 200)'. A second small card: 'built-in: a value the engine hands to a function, or collects from it'.

*Motion.* The four corners of the sprite flash one after another, each with its local numbers; then the color rect's zero sits at its corner instead.

*Lane.* manim · `B08_CornersInLocalSpace` · runner-up: ShaderLab

### B09 · 39 words · ~13 s

> Why a matrix at all? Adding the node's position handles a plain shift. Add a turn and a change of size, and the corner lands somewhere else entirely. One matrix holds the shift, the turn and the size together.

*Picture.* A sprite outline at the world's zero with its corner dot. Step one: it is shifted to (600, 400) and a grey ghost corner lands at (536, 336), labelled 'add the position'. Step two: the sprite is also turned and doubled in size; the true corner dot lands somewhere else at (553, 225) while the ghost stays at (536, 336), with a short grey arrow between them. A small 4x4 table appears with the card 'matrix: a grid of numbers that moves a point when you multiply by it' and the caption 'one matrix holds shift, turn and size'.

*Motion.* The ghost corner stays where 'add the position' puts it while the real corner swings away once the sprite is turned and doubled.

*Lane.* manim · `B09_WhyAMatrix` · runner-up: LectureEvidenceTable (add the position against the real answer)

### B10 · 30 words · ~10 s

> That matrix is called model matrix. It stores the node's whole placement: position, turn and size, parents included. Multiply a corner by it, and the corner's world numbers come out.

*Picture.* A labelled table (4 by 4 outline cells) captioned 'model matrix: local to world' in the middle. At the left, a dimmed sprite sits at the world's zero with the tag '(-64, -64)'. The sprite travels along an arrow through the table and lands at its place at the right with the tag '(536, 336)'. A small 'parents included' chip appears under the table.

*Motion.* The sprite is carried from the world's zero through the table to its place; its corner tag changes on the way.

*Lane.* manim · `B10_ModelMatrix` · runner-up: DesignPipelineClaim, show-tell isometric (a machine on a conveyor)

### B11 · 40 words · ~14 s

> One warning. The position shown in the editor is measured from the node's parent, not from the world. A child at fifty, zero, inside a parent at five hundred, three hundred, sits at five fifty, three hundred in the world.

*Picture.* Two real frames of the Godot editor (a scripted editor session), the Scene dock reading Scene, Parent, Child and the Inspector open on Node2D, Transform, Position: the Child (a Sprite2D) selected shows Position x 50.0 px, y 0.0 px; the Parent (a Node2D) selected shows x 500.0 px, y 300.0 px. A slow cross-dissolve between them; a terracotta ring on the Position row being named in each frame; a readout 'world 550, 300' lands last.

*Motion.* The ring moves from the child's Position row to the parent's, and the world number lands last.

*Lane.* editor · `ShaderLab` · runner-up: manim: a parent platform sliding right while the child's editor tag stays 50, 0 and its world tag counts up

*Capture to record.* E1 (DONE by script, 2026-10-13, editor driver; README 2.5): two whole frames from `_godot-shaders-series/editor-capture/png/1920x1080/local-world-and-screen-space/` (native 3456x1944 twins in png/3456x1944/local-world-and-screen-space/): local-world_E1-1_child-selected-clean-root and local-world_E1-2_parent-selected-clean-root. Cross-dissolve at 0.58 of the beat; the ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels: category Node2D, group Transform, row Position with fields x and y and a px suffix, then Rotation, Scale (with a link toggle), Skew; the Scene dock reads Scene, Parent, Child. Use the clean-root pair. The plan-exact pair (`..._plan-exact-root-is-Parent`, where the root node itself is the transformed Parent) shows a warning triangle on the root, 'The root node of a scene is recommended to not be transformed, since instances of the scene will usually override this.', and is not used. No pointer is visible (Movie Maker records the window): label 'scripted editor session'.

### B12 · 33 words · ~11 s

> Here is that as code. Wrap the corner in a vec four, multiply by the model matrix, and keep the first two numbers. The result is a vec two: the corner's world position.

*Picture.* The line world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy; assembled token by token in monospace. Under it a data strip: the corner '(-64, -64)' becomes '(-64, -64, 0, 1)' as vec4 closes round VERTEX, then '(536, 336, 0, 1)' as MODEL_MATRIX multiplies in, then '(536, 336)' as .xy keeps two. A grey bracket moves under each token as it lands, and a small grey label 'vector: a bundle of two to four numbers' appears under vec4 as the two numbers become four.

*Motion.* The corner's two numbers grow to four, get multiplied, and shrink back to two as each token of the line lands.

*Lane.* manim · `B12_BuildTheLine` · runner-up: LectureCodeTrace

### B13 · 43 words · ~15 s

> Why a zero and a one? The matrix keeps the node's shift in its last column. The final one switches that column on, so the corner counts as a place. With a zero instead, the shift is skipped: a direction, not a place.

*Picture.* A 4 by 4 grid of outline cells with the last column outlined and filled with the node's numbers '600, 400, 0, 1' beside the vector '(-64, -64, 0, w)'. With w = 1 a terracotta ring sits on the one and the result reads '(536, 336)' labelled 'a place'. The one then flips to zero: the last column dims and the result falls back to '(-64, -64)' labelled 'a direction'.

*Motion.* The final one flips to zero, the last column dims, and the answer drops from (536, 336) to (-64, -64).

*Lane.* manim · `B13_TheLastColumn` · runner-up: ShaderLab (03-direction-not-place on the sprite)

### B14 · 40 words · ~14 s

> Fragment runs once for each pixel, and it cannot read this matrix. Ask, and the compiler stops you: unknown identifier. Only the vertex function can see model matrix. So how does a pixel learn where it is in the world?

*Picture.* A plain terminal window with the real output of the broken-shader script: the command, the engine banner, the script's one printed line 'fragment() runs once for each pixel the shape covers; sets its color' (the definition, in full ink), then the engine's own five marked source lines with the offending line flagged E and ringed, and the line 'SHADER ERROR: Unknown identifier in expression: MODEL_MATRIX.' with a second ring. The title says the log was trimmed of its backtrace.

*Motion.* The log lines land one after another; the offending line gets a ring, then the error line lands and gets one.

*Lane.* terminal · `CCPlainShell` · runner-up: editor capture of the shader editor's own error panel (E2, optional)

### B15 · 39 words · ~13 s

> With a varying: a value set at each corner, blended across the shape. Vertex stores the world position at the four corners. The graphics card blends them, so every pixel gets its own world position for fragment to read.

*Picture.* A rectangle with four terracotta corner dots; each corner shows its world number ('536, 336', '664, 336', '536, 464', '664, 464'). Inside, a pixel grid of outline cells tints from the corners inward: the red channel as a smooth ramp from the left pair to the right pair, each cell showing a tiny blended value. Card: 'varying: a value set at each corner, blended across the shape for fragment() to read'.

*Motion.* The four corner values flow inward and the cells between them fill with smoothly blended values.

*Lane.* manim · `B15_Varying` · runner-up: ShaderLab (05-world-field video)

### B16 · 38 words · ~13 s

> Here it is working. The world position becomes the color: red for across, green for down. Slide the sprite, and its colors change, because the sprite is a window onto a color field that stays where it is.

*Picture.* Code card at the left with the varying and the vertex line highlighted, then the fragment line; at the right a real Godot window: a faint color field (red grows left to right, green top to bottom) and a test sprite sliding over it, filled with the same field at full strength. Readouts '0' and '1' at the field's edges.

*Motion.* As the sprite slides right it turns redder, because it shows the part of the field that is at its new place.

*Lane.* capture · `ShaderLab` · runner-up: Manim color-field plane

*Capture to record.* C03: scene script capture-scenes/capture-c03.gd: faint backdrop ColorRect (05-world-field, alpha 0.35), blob sprite (256 px art) at y=360 with 05-world-field.gdshader, resting at x=300 then sliding to x=980 over 52 to 80 % of the beat; 13 s (CAPTURE-PLAN.md).

## Act III: Locked to the World

### B17 · 38 words · ~13 s

> Back to the stars. A texture is normally looked up by U V, which is local space squeezed to run from zero to one. Local in pixels or local in U V, the picture belongs to the sprite.

*Picture.* Act title 'Locked to the World' (serif 40) top-left. A sprite square with local numbers on its axes (-64 to 64) and a zero marker at its center; a second set of numbers '0 to 1' along its top and left edge. The zero marker slides from the center to the top-left corner while the center's numbers squeeze: '(-64,-64)' becomes '(0, 0)' and '(64, 64)' becomes '(1, 1)'. Card: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'. A small 'stuck to the sprite' chip.

*Motion.* The zero slides from the sprite's center to its corner and the numbers squeeze from minus sixty-four to sixty-four down to zero to one.

*Lane.* manim · `B17_UVIsLocalToo` · runner-up: LectureEvidenceTable (local pixels against U V)

### B18 · 36 words · ~12 s

> To pin the picture to the world, look it up by world position instead. In the code, one line changes: the varying is set from the model matrix, not from vertex. Fragment's line stays the same.

*Picture.* Two code lines morph. 'position = VERTEX;' transforms into 'position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;' while the fragment line 'COLOR.rgb = texture(sky, position / tile_size).rgb;' stays grey and unchanged beneath. A chip over the changing line flips from 'local' to 'world'; a grey bracket outlines the unchanged line, with the small grey label 'texture(sky, address): reads the sky picture at that address' under it.

*Motion.* The right side of the first line transforms into the matrix expression while the fragment line below does not change at all.

*Lane.* manim · `B18_OneLineChanges` · runner-up: LectureCodeTrace (a diff)

### B19 · 43 words · ~15 s

> World position counts pixels, but a texture wants an address from zero to one. So divide by a tile size you choose. At five hundred twelve, one copy of the picture covers five hundred twelve world pixels, and then the next copy starts.

*Picture.* A horizontal world axis from 0 to about 1500 with tick marks at 512 and 1024. A terracotta dot travels along it; below, a plot of 'address' against world x: a sawtooth that rises from 0 to 1 and wraps back to 0 at every 512, with the dot's current address as a live readout. Label: 'tile size 512'.

*Motion.* The dot rides along the world axis while the address ramps from zero to one and wraps back to zero at every five hundred twelve.

*Lane.* manim · `B19_TileAddress` · runner-up: ShaderLab (02-sky-world with a gradient)

### B20 · 30 words · ~10 s

> Past one, the address runs off the picture's edge. Mark the texture repeat enable, and the picture tiles forever. Leave it off, and the edge pixels smear outward, like this.

*Picture.* A code card at the left with the two setting lines, each tagged with what it does (comments name the files); at the right a real Godot window filled by the star sky read by world position: first the picture tiles across the whole view (the ringed planet repeats every 512 pixels); at the switch the setting changes to repeat_disable and everything beyond the first tile smears into horizontal and vertical streaks.

*Motion.* The picture tiles, then at the switch it collapses into streaks past the first copy.

*Lane.* capture · `ShaderLab` · runner-up: two stills side by side

*Capture to record.* C04: scene script capture-scenes/capture-c04.gd: full-view ColorRect with 02-sky-world.gdshader, switched to 06-sky-no-repeat.gdshader at 64 % of the beat; 10 s (CAPTURE-PLAN.md).

### B21 · 34 words · ~12 s

> Now slide the sprite. The stars inside do not move; the sprite uncovers different ones as it passes. A faint copy of the same sky sits behind it, and the two line up exactly.

*Picture.* Code card at the left (the world-locked sky shader); at the right a real Godot window: a faint star sky and a test sprite filled with the same sky at full strength, sliding right across the ringed planet and coming to rest over it. The stars and the planet inside the sprite line up exactly with the faint copy behind it, all the way to the sprite's edge.

*Motion.* The sprite slides over the planet and its stars never shift against the faint copy behind it.

*Lane.* capture · `ShaderLab` · runner-up: Manim

*Capture to record.* C05: scene script capture-scenes/capture-c05.gd: one sprite at y=240, x 640 to 880 over 10 to 50 % of the beat, then at rest over the planet (the planet and most of its ring sit inside the sprite, the ring's left tip outside it); faint backdrop (alpha 0.35); 12 s (CAPTURE-PLAN.md).

### B22 · 35 words · ~12 s

> Turn the sprite, or stretch it, and the sky still holds still. World position already includes the sprite's turn and size, so the pattern ignores both. Only where a pixel sits in the world matters.

*Picture.* A real Godot window: the faint star sky and a plain white square sprite (a window) over the ringed planet. The square turns forty-five degrees, then stretches wide and low; the planet and stars inside it never move. Readouts 'turned' and 'stretched' appear as each happens.

*Motion.* The square's corners swing around and its shape stretches while the stars and the planet inside it stay exactly where they are.

*Lane.* capture · `ShaderLab` · runner-up: Manim

*Capture to record.* C06: scene script capture-scenes/capture-c06.gd: white 128 px art at (852,240), scale 2; rotation 0 to 45 degrees over 6 to 22 % of the beat, then scale (2,2) to (2.5,1.6) over 24 to 38 %; 12 s (CAPTURE-PLAN.md).

### B23 · 37 words · ~13 s

> A shortcut you will see multiplies by texture pixel size instead of dividing by a tile size. That built-in is one over the sprite's own art size, so swap in smaller art, and the whole pattern shrinks.

*Picture.* Code card at the left (position times texture pixel size); at the right a real Godot window: a test sprite filled with a checker pattern by world position. At the swap its art changes from 128 pixels to 64 pixels (drawn at the same size on screen) and the checks shrink to half. Readouts '128 px art' then '64 px art'.

*Motion.* The sprite stays the same size on screen but the checks halve as the art is swapped.

*Lane.* capture · `ShaderLab` · runner-up: Manim: two sprites with different art sizes and their tiles

*Capture to record.* C07: scene script capture-scenes/capture-c07.gd: blob sprite, art 128 px at scale 2, 07-pattern-texel-size with a checker texture; at 78 % of the beat the texture is swapped to a 64 px blob drawn at scale 4; 12.6 s (CAPTURE-PLAN.md).

### B24 · 32 words · ~11 s

> A world position can also decide what exists. Discard throws a pixel away. Discard everything within sixty pixels of a fixed point, and the sprite walks across a hole that stays put.

*Picture.* Code card at the left (the distance test and discard); at the right a real Godot window: a thin grey circle marks a hole fixed in the world; a test sprite slides across it: a bite appears at its edge, grows into a round hole inside the sprite while the two overlap, and slides out of the other side, whole again.

*Motion.* The hole stays still while the sprite slides across it: a bite, then a round hole inside the sprite, then whole again.

*Lane.* capture · `ShaderLab` · runner-up: Manim

*Capture to record.* C08: scene script capture-scenes/capture-c08.gd: blob sprite (256 px art) at y=360 sliding x 440 to 840 over 40 to 92 % of the beat across a hole at (640,360) radius 60; a thin grey ring (3 px, #8F8A7B) drawn by the scene; 11.5 s (CAPTURE-PLAN.md).

### B25 · 35 words · ~12 s

> Put it together. A mix amount, from zero to one, blends the sprite's own color with the sky. Animate it up as the sprite walks, and the character turns into a window onto the stars.

*Picture.* Code card at the left (the mix amount and the sky lookup); at the right a real Godot window: the faint star sky and the test sprite walking right across the ringed planet. As it walks the sprite's teal and eyes dissolve into stars: when it passes the planet it is a sprite-shaped window onto the sky.

*Motion.* The sprite's own color dissolves into the stars as the amount climbs, while it walks across the fixed sky.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C09: scene script capture-scenes/capture-c09.gd: one sprite at y=240, x 560 to 1000 over 50 to 95 % of the beat; amount set to 0.0 from code first, then a tween 0 to 1 over 52 to 78 %; 12 s (CAPTURE-PLAN.md).

## Act IV: Where Is the Screen?

### B26 · 39 words · ~13 s

> Some effects belong to neither the sprite nor the world. A darkened edge, a damage flash: they stay on the glass wherever the camera points. They need the pixel's screen address, and there are four ways to read it.

*Picture.* Act title 'Where Is the Screen?' (serif 40) top-left. A window frame (the glass) with a soft grey tint along its four inner edges and a small terracotta flash mark in a corner, over a field of dots that is the world. The world slides left and right behind the window; the tint and the flash mark do not move. Label 'stays on the glass'.

*Motion.* The world's dots slide behind the window while the edge tint and the flash mark stay fixed on the glass.

*Lane.* manim · `B26_StaysOnTheGlass` · runner-up: ShaderLab capture of a vignette

### B27 · 35 words · ~12 s

> The first way you already know: the canvas matrix turns world numbers into screen numbers. The camera lives in it: pan or zoom, and only this matrix changes. Godot's reference calls the result canvas space.

*Picture.* Two labelled 4 by 4 tables side by side: 'model matrix' with its last column '600, 400, 0, 1' ringed and 'canvas matrix' with its last column '-250, -100, 0, 1' ringed. The window slides right over the world (a camera pan); the canvas table's last column ticks to '-350, -100, 0, 1' while the model table does not change. Then the camera zooms in: the canvas table's two diagonal ones become twos while the model table stays. A card: 'canvas matrix: world to screen (Godot calls it canvas space)'.

*Motion.* The window pans and zooms and only the canvas matrix's numbers change; the model matrix's numbers stay put.

*Lane.* manim · `B27_CanvasMatrix` · runner-up: LectureEvidenceTable (matrix, what it does, what changes it)

### B28 · 40 words · ~14 s

> Chain the two: canvas matrix times model matrix times the corner. Read it right to left, so the corner meets the model matrix first. With the camera zoomed in on the sprite, the corner lands at five twelve, two thirty-two.

*Picture.* The expression CANVAS_MATRIX * MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0) across the middle, with a grey arrow under it pointing right to left. A small token '(-64, -64)' starts at the right, passes into the model matrix box and comes out '(536, 336)', passes into the canvas matrix box (the camera zoomed in on the sprite) and comes out '(512, 232)' inside a window frame.

*Motion.* The corner's token passes through the model matrix, then the canvas matrix, from right to left, and ends inside the window at (512, 232).

*Lane.* manim · `B28_RightToLeft` · runner-up: LectureCodeTrace line focus

### B29 · 28 words · ~10 s

> Swap the order and the answer is wrong, not slightly off. The same corner now lands at minus eighty-eight, minus one sixty-eight, far outside the window. Order matters.

*Picture.* The same picture with the two boxes swapped in the expression MODEL_MATRIX * CANVAS_MATRIX * vec4(VERTEX, 0.0, 1.0). The token '(-64, -64)' now passes the canvas box first and then the model box and flies out beyond the window's left and top edges to '(-88, -168)', outside the frame, with a grey 'outside the window' mark.

*Motion.* The token leaves the window and lands far off its top-left corner.

*Lane.* manim · `B29_WrongOrder` · runner-up: ShaderLab capture of 11-wrong-order under a zoomed camera

### B30 · 33 words · ~11 s

> The second way is shorter. Inside fragment, vertex means something new: not the local corner, but the pixel's screen position, in pixels. Same name, different space, so check which function you are in.

*Picture.* Two function boxes stacked, vertex() above and fragment() below, each holding a chip with the same name VERTEX. A pixel on a small sprite icon (the corner pixel) has two grey arrows: to vertex(), where the chip reads '(-64, -64)' with the tag 'local'; to fragment(), where the chip reads '(286.5, 236.5)' with the tag 'screen, in pixels'.

*Motion.* The same name VERTEX sits in both boxes and changes its number and its tag as it moves from one to the other.

*Lane.* manim · `B30_SameNameTwoSpaces` · runner-up: LectureEvidenceTable (two rows)

### B31 · 40 words · ~14 s

> The third is frag coord: the pixel's place in the window, counted in pixels. The reference page says its far corner is one, one. Measured here, in a twelve-eighty by seven-twenty window, the last pixel reads twelve seventy-nine point five.

*Picture.* The real Godot 4.7 canvas item shader reference in a browser window, scrolled to the FRAGCOORD row; the camera pushes in on the sentence about the bottom-right corner being one, one and a terracotta ring marks it. The caption carries the measured reading.

*Motion.* The camera pushes in on the one-one sentence and the ring closes on it; the caption holds the measured number.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: a quoted line beside a measured number

### B32 · 33 words · ~11 s

> The fourth is screen U V: the same place as a fraction, from zero to one. Screen pixel size is one over the window's size, so pixels times it give that same fraction.

*Picture.* A window frame with a terracotta dot at a pixel and its tag '(286.5, 236.5) pixels'. Beside it a small card 'screen pixel size = (1/1280, 1/720)'. The tag multiplies down through the card and becomes '(0.2238, 0.3285)', labelled 'SCREEN_UV'; the dot gets a second tag in the same place. A ramp strip from 0 to 1 along the window's top shows the fraction.

*Motion.* The pixel tag multiplies by the pixel-size card and shrinks into the fraction tag at the same dot.

*Lane.* manim · `B32_PixelsToFraction` · runner-up: LectureEvidenceTable

### B33 · 34 words · ~12 s

> Four tiles, one method each, each painting itself with its own screen address. Watch the gradient grow tile by tile. If any method disagreed, a seam would show. There is none: all four agree.

*Picture.* Code card at the left (the key line of each of the four shaders, comments name the method); at the right a real Godot window in four tiles outlined in thin grey. Each tile starts flat grey and switches on in turn, painting itself red-green-blue by its own screen address; after the fourth the whole window is one seamless gradient. Tile labels 'canvas matrix', 'vertex', 'frag coord', 'screen UV'.

*Motion.* Each tile joins the gradient in turn with no seam.

*Lane.* capture · `ShaderLab` · runner-up: LectureEvidenceTable of four probe values

*Capture to record.* C10: scene script capture-scenes/capture-c10.gd: four 960x540 ColorRects on a 1920x1080 canvas (top-left 10, top-right 12, bottom-left 13, bottom-right 14) on flat grey (#BDB8AA), switched on in that order at 20, 32, 42 and 58 % of the beat; thin grey tile outlines (3 px) drawn by the scene; 11.6 s. ROUTE: 1920x1080 at scale 1, not the 3x SubViewport route, because shaders 10, 12 and 13 read window pixels (series rule; CAPTURE-PLAN.md).

### B34 · 41 words · ~14 s

> A pixel here is a real window pixel. In canvas items stretch mode, doubling the window doubles the sprite's width in screen pixels, while its world numbers stay put. A fraction of the screen, from screen U V, does not care.

*Picture.* A small window and the same window doubled with a small chip 'stretch mode: canvas items', side by side, each holding the same sprite. Under each: 'world 128' and 'screen 128' for the small one; for the large one 'world 128' stays and 'screen 256' counts up as the window grows. A ramp strip labelled 'SCREEN_UV' under both stays at 0 to 1 in each.

*Motion.* The window doubles; the sprite's screen width counts from 128 to 256 while its world width stays 128 and the 0-to-1 strip stays 0-to-1.

*Lane.* manim · `B34_RealPixels` · runner-up: capture of a stretched window

## Act V: Choosing a Space

### B35 · 37 words · ~13 s

> So which space? Ask what the effect should stay stuck to. The sprite: local. A place in the level: world. The glass: screen. One experiment tells you which you built: slide the sprite, then pan the camera.

*Picture.* Act title 'Choosing a Space' (serif 40) top-left. Three columns, each a small drawing with a terracotta pin: 'the sprite' (a sprite square, the pin on it), 'a place in the level' (a map outline with the pin on a spot), 'the glass' (a window frame with the pin on the glass). Under them two grey arrows appear: 'slide the sprite' and 'pan the camera'.

*Motion.* The pin lands on the sprite, then on a place in the level, then on the glass; the two test arrows appear last.

*Lane.* manim · `B35_StuckTo` · runner-up: LibraryIconRow (three marks)

### B36 · 31 words · ~10 s

> Three sprites, the same stripes, three spaces. Slide them right. The local stripes ride along with their sprite. The world and screen stripes stay put, and each sprite slides over them.

*Picture.* A real Godot window: three test sprites in a row, each filled with white stripes by a different shader; column labels 'local', 'world' and 'screen' above them. At the start the three stripe patterns look identical. The three sprites slide right by 160; the left one's stripes move with it, the middle and right stripes stay put on the screen and each sprite slides over them.

*Motion.* At the end of the slide the left sprite's stripes are the opposite phase of the other two.

*Lane.* capture · `ShaderLab` · runner-up: Manim stripes

*Capture to record.* C11a: scene script capture-scenes/capture-c11a.gd: three blob sprites (256 px art, scale 1) at x = 256, 640, 1024 (y 360) with 15-anchor-local, 16-anchor-world, 17-anchor-screen; Camera2D at (640,360); slide +160 over 24 to 60 % of the beat; 10.5 s (CAPTURE-PLAN.md).

### B37 · 37 words · ~13 s

> Now leave the sprites and pan the camera. The local and world stripes travel with their sprites, because both belong to the world. Only the screen stripes stay on the glass. Two moves tell all three apart.

*Picture.* The same three sprites at their start positions, same column labels. The camera pans right by 160, so the sprites slide left on screen; the left and middle sprites carry their stripes with them, the right sprite slides left over stripes that stay where they were on the glass.

*Motion.* The left and middle sprites keep their stripes as they slide left; the right sprite slides over stripes that do not move.

*Lane.* capture · `ShaderLab` · runner-up: Manim stripes

*Capture to record.* C11b: scene script capture-scenes/capture-c11b.gd: the camera goes from (640,360) to (800,360) over 22 to 60 % of the beat; 12.6 s (CAPTURE-PLAN.md).

### B38 · 39 words · ~13 s

> Here is the map. Local numbers come straight from vertex. World numbers come from the model matrix. Screen numbers come from the canvas matrix, or ready-made from screen U V. Say which space you mean, and the code follows.

*Picture.* A three-row table, one row ringed as each space is named: local, world, screen, with what each is stuck to and where its numbers come from.

*Motion.* The ring moves down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

### B39 · 31 words · ~10 s

> The code barely changes. The line that sets the position picks the space: vertex for local, the model matrix for world. For the screen, read screen U V in fragment instead.

*Picture.* Three code cards stacked: the stripe shader's key lines for local ('position = VERTEX;'), world ('position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;') and screen ('float stripe = step(0.5, fract(SCREEN_UV.x * 20.0));'). In each the line that picks the space is highlighted with a grey bracket and the rest is grey. A chip names each: local, world, screen. Under the screen card two small grey labels give the glossary wording of the two small words that line uses (they are not spoken): 'fract(x): the part after the point' and 'step(edge, x): 0 below the edge, 1 from the edge up'.

*Motion.* A bracket moves down the three cards and lands on the one line that differs in each.

*Lane.* manim · `B39_OneLineDecides` · runner-up: LectureCodeTrace

### B40 · 40 words · ~14 s

> This is also how to check a shader an AI wrote for you. It can compile, look right in a still, and be stuck to the wrong thing. Slide the sprite, pan the camera, and watch where the pattern goes.

*Picture.* A short checklist drawn as outline rows: 'compiles' (check mark drawn), 'looks right in a still' (check mark drawn), 'survives the two moves' (empty box). A small striped sprite icon to the right slides right (a grey arrow) and then a window frame slides over it (a second grey arrow): after both the third box gets its check mark, or a cross drawn in grey.

*Motion.* The first two boxes tick at once; the third waits while the sprite slides and the camera pans, and only then settles.

*Lane.* manim · `B40_TwoMoves` · runner-up: ClaudeCodeBeat (a prompt and a reply)

## Closing

### BVDT · recap · 83 words · ~28 s

> Let's recap with Claude. A position is an address, and each space has its own zero. The model matrix turns local numbers into world numbers, and a varying carries them to fragment. Look a texture up by world position and it stays put while the sprite moves. Four ways read a pixel's screen address, and all four agree. Slide the sprite, then pan the camera, to see which space a pattern is stuck to. Pick the space the effect should stay stuck to.

*Picture.* The recap card: A position is an address, and each space has its own zero. / The model matrix turns local numbers into world numbers, and a varying carries them to fragment. / Look a texture up by world position and it stays put while the sprite moves. / Four ways read a pixel's screen address, and all four agree. / Slide the sprite, then pan the camera, to see which space a pattern is stuck to. / Pick the space the effect should stay stuck to.

### BHTF · your turn · 75 words · ~26 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a sprite: white vertical stripes, thirty-two pixels wide, over the sprite's own colors. Fix the stripes to the world, not to the sprite or the screen. Then show me what to change to fix them to the screen instead. Then check two things yourself. Slide the sprite: do the stripes hold still? Pan the camera: do the stripes travel with the sprite?

*Prompt shown and read in full:* Write a Godot canvas item shader for a sprite: white vertical stripes, thirty-two pixels wide, over the sprite's own colors. Fix the stripes to the world, not to the sprite or the screen. Then show me what to change to fix them to the screen instead.

*Two checks:* Check: slide the sprite, and the stripes hold still. · Check: pan the camera, and the stripes travel with the sprite.

### BOUT · outro · 9 words · ~4 s

> Local, World and Screen Space. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


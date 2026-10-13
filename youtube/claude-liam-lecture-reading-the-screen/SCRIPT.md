# Script: Reading the Screen

**What this is.** The words Liam will say in *Reading the Screen*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 44 beats, 1674 words, about **9:33** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 25, manim 11, remotion 2.

**If it runs long.** Cut, in this order: the symptom table (B38), the finale (B37), the mouse-filter beat (B13), the edge-and-filter beat (B36) and the frosted-glass beat (B25): each repeats an idea another beat already carries, or adds a habit rather than the idea. The window (B03 to B09), the spotlight with its oval fix (B16 to B20), the pool (B27 to B29) and the overlap with its fix (B32, B33) stay: they carry the idea.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | A Copy of the Screen | 10 | 371 | ~2:06 |
| II | Full-Screen Effects | 10 | 365 | ~2:04 |
| III | Bend What Is Behind | 9 | 302 | ~1:43 |
| IV | What It Can See | 9 | 314 | ~1:47 |

## Opening

### BOPEN · identity card · 32 words · ~11 s

> Reading the Screen. Learn how a shader can read what the game has already drawn, so you can filter the whole screen, bend the picture, and build water you can see through.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Reading the Screen", and the line "How a shader reads what is already drawn".

### BIDEA · the question · 37 words · ~13 s

> Hallo. This is Liam, in for Bear. Most people think a shader only knows its own sprite. One line of code breaks that rule. A shader can read what is already on screen, and build on it.

*Picture.* The hesitant writer types: "A shader only knows
its own sprite." then deletes "its own sprite" and types "what is already on screen".

### BDEFS · terms · 74 words · ~25 s

> Six terms. A texture is an image a shader can read. U V is a point's address on a shape: zero to one across, zero to one down. A uniform is a value your game sets from outside. Fragment is the function that runs once for each pixel and sets its color. Draw order is what gets drawn first; later things cover earlier ones. And post-processing is changing the picture after it is drawn.

*Picture.* "Terms In This Lecture": **Texture** — an image a shader can read by address; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Uniform** — a value your game sets from outside; every pixel sees the same one; **fragment()** — runs once for each pixel the shape covers; sets its color; **Draw order** — what is drawn first; later things cover earlier ones; **Post-processing** — changing the picture after it is drawn

## Act I: A Copy of the Screen

### B01 · 40 words · ~14 s

> Give a sprite a shader, and it can color that sprite. But glass, heat haze and water do something different. They change what is behind them. For that, a shader has to read the picture the game has already drawn.

*Picture.* Act title 'A Copy of the Screen' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a meadow of green checker tiles, a sand path, flowers, and in the lower left a pool whose wavy top edge ripples and whose water bends the checker lines and the path behind it. The teal player stands to the right. A terracotta ring settles on the pool.

*Motion.* The water ripples and the checker lines behind it wobble, live; the ring marks where the picture behind is being read.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a glass pane over a scene

*Capture to record.* C01: scene_c01_pool.gd (evidence/planning-checks), canvas 1280 x 720 through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Nothing moves but the water (TIME). Same capture serves B28.

### B02 · 37 words · ~13 s

> There is a catch. Graphics hardware cannot properly read a picture while it is drawing into it. So Godot copies the picture drawn so far, and your shader reads the copy. That copy is the screen texture.

*Picture.* On the cream stage a 16:9 screen frame, left, fills in the order the game draws it: the green checker ground, a tree, a flower, then a small rectangle labelled 'shader'. Just before that rectangle is drawn, a camera-flash snapshot copies the whole frame into a second frame on the right, labelled 'screen texture: a copy of everything drawn so far'. A drawn arrow runs from the shader rectangle to the copy.

*Motion.* The frame is copied in one flash and the shader's arrow reads from the copy, not from the live frame.

*Lane.* manim · `B02_TheCopy` · runner-up: DesignPipelineClaim, show-tell isometric

### B03 · 39 words · ~13 s

> Here is the smallest use. In the fragment function, each pixel's color becomes whatever the screen holds at that pixel's spot. Switch it on, and the rectangle vanishes. It is still there. It only shows what is behind it.

*Picture.* Code card at left with the 7-line shader; at right a real Godot window on the meadow: a plain teal rectangle in a cream frame. At 58 percent the shader switches on and the teal fill vanishes, leaving the cream frame around meadow. Label: 'still there'.

*Motion.* The teal rectangle vanishes at the cue; the cream frame stays, empty, showing the meadow.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: scene_c02_window.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. A teal rectangle (0.38, 0.22, 0.30 x 0.30 of the canvas) in a cream frame; 01-window is assigned at u = 0.58. Verified: the rectangle's interior equals the meadow exactly (8,820 samples, worst channel difference 0).

### B04 · 35 words · ~12 s

> Now take the uniform line apart. A uniform is a value that comes from outside. Sampler two D is the type of a texture a shader can read. And the name is yours to choose.

*Picture.* The line `uniform sampler2D screen_texture : hint_screen_texture;` set in monospace on the cream stage, each token its own object at explicit coordinates. A bracket is drawn under `uniform` with the label 'from outside'; one under `sampler2D` with 'sampler2D: the type of a texture a shader reads'; one under `screen_texture` with 'your name'. The `hint_screen_texture` token stays grey until the next beat.

*Motion.* Each bracket is drawn under its token on the word that names it, so the line is read left to right.

*Lane.* manim · `B04_ThePieces` · runner-up: ShaderLab

### B05 · 38 words · ~13 s

> Then the hint, after the colon. A hint is a word that tells Godot how to treat a uniform. This one says: fill it with the screen. Godot refreshes it every frame, so you never set it yourself.

*Picture.* The same line again with the `hint_screen_texture` token ringed (terracotta ring, grey backing) and the labels 'hint: the word after a colon that tells Godot how to treat a uniform' and 'this one: fill it with the screen'. Below, a slot labelled `screen_texture`. On three frame ticks (a small counter 1, 2, 3) a fresh miniature of the meadow drops into the slot, replacing the last one; in each the flower has moved a little. A small cursor arrow outside the slot is crossed out: 'you never set it'.

*Motion.* A new copy drops into the slot on every tick, replacing the old one, with nobody placing it.

*Lane.* manim · `B05_FilledEveryFrame` · runner-up: DesignPipelineClaim, show-tell isometric

### B06 · 33 words · ~11 s

> Now read it. The function texture takes a texture and an address, and returns the color stored there. Four numbers come back: red, green, blue, and alpha, which is how visible it is.

*Picture.* The screen texture drawn as a 12 by 7 grid of outline cells in the meadow colours (cells are never filled behind text). A terracotta probe ring sits on one cell with a live label 'address (0.62, 0.40)'; a drawn arrow runs to a swatch showing that cell's colour. The probe hops to two more cells and the swatch follows. After the third hop the swatch splits into four chips R, G, B, A; the A chip carries 'alpha: how visible a pixel is (0 invisible, 1 solid)'.

*Motion.* The probe hops from cell to cell and the swatch changes colour to match; then the swatch splits into four numbers.

*Lane.* manim · `B06_AddressToColor` · runner-up: LectureCodeTrace

### B07 · 38 words · ~13 s

> A pixel has two addresses. U V is its place on its own shape. Screen U V is its place on the whole screen. Slide the shape, and U V stays the same, while screen U V changes.

*Picture.* A 16:9 screen outline with a smaller 4:3 shape inside it and one pixel dot on the shape. Two live labels follow the dot: 'UV (0.5, 0.5)', measured on the shape ('UV: a point's address on the shape'), and 'screen UV (0.31, 0.62)', measured on the screen ('SCREEN_UV: a pixel's address on the whole screen, not on its own shape'). The shape then slides right: the first label stays (0.5, 0.5) while the second counts up to (0.62, 0.62).

*Motion.* The shape slides and one label never changes while the other counts up.

*Lane.* manim · `B07_TwoAddresses` · runner-up: ShaderLab with the two colour pictures

### B08 · 38 words · ~13 s

> Read the screen with U V, and the rectangle fills with a tiny copy of the whole screen. Read it with screen U V, and the rectangle becomes a window onto what is behind it, wherever it slides.

*Picture.* Two 16:9 rectangles in cream frames, one above the other, slide right together over the meadow. The top one (UV) holds a tiny copy of the whole screen that does not move with the picture; the bottom one (screen UV) is a window onto the meadow. Right-margin labels 'UV' and 'screen UV'.

*Motion.* Both rectangles slide; the top one keeps showing the same tiny copy, the bottom one shows different parts of the meadow.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of the two cases

*Capture to record.* C03: scene_c03_addresses.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Top rectangle 02-miniature, bottom 01-window, both 0.28 x 0.28, sliding from x = 0.04 to 0.56 between u = 0.15 and 0.90. Verified: inside the miniature the colour at a fraction of the rectangle equals the screen at the same fraction (4 of 4 points); inside the window it equals the screen at the same place.

### B09 · 39 words · ~13 s

> Now change the color. Adding r g b after it keeps red, green and blue. One minus each of them flips every color. Slide the window, and the flipped picture stays pinned to the screen. Only the opening moves.

*Picture.* Code card at left (the 8-line invert shader); at right a real Godot window: one 16:9 window in a cream frame holds the meadow with every colour flipped (greens turn purple, the sand path turns navy). It sits still, then slides diagonally across the meadow; the flipped picture inside stays pinned to the screen while the opening moves. Label 'pinned to screen'.

*Motion.* The window slides and the flipped picture inside does not slide with it; only the opening moves.

*Lane.* capture · `ShaderLab` · runner-up: manim sliding frame over a picture

*Capture to record.* C04: scene_c04_invert.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. 03-invert in a 0.28 x 0.28 window that is still until u = 0.56, then slides from (0.08, 0.10) to (0.62, 0.58) by u = 0.96. Verified: every sampled pixel equals 1 minus the meadow (worst channel difference 0).

### B10 · 34 words · ~12 s

> Older tutorials use a shortcut called screen texture, in capital letters. Godot four removed it. The compiler says so, and points you to the hint instead. If an old line fails, this is why.

*Picture.* A cream code card with the five-line shader that uses the capital-letters shortcut; focus lands on the line that uses it. Under the card the engine's own message, verbatim from a real run, is the note.

*Motion.* Focus steps down to the old line and stays on it while the compiler's message is read.

*Lane.* remotion · `LectureCodeTrace` · runner-up: BrowserCapture of the docs row 'SCREEN_TEXTURE: Removed in Godot 4'

## Act II: Full-Screen Effects

### B11 · 40 words · ~14 s

> A full-screen effect, or post-processing, needs a node covering every pixel. A color rect with your shader on it can do that: set its layout to Full Rect. Its edges follow the screen's corners, even when the game is resized.

*Picture.* Act title 'Full-Screen Effects' (serif 40) top-left. A screen outline (the game screen) with a small teal rectangle labelled 'ColorRect' inside it. Four terracotta anchor dots on the rectangle's corners fly out to the screen's four corners and the rectangle stretches to fill it; the label 'Layout > Anchors Preset: Full Rect' (the editor's own words) appears. The screen outline then grows wider and narrower in turn and the rectangle follows.

*Motion.* Four dots fly to the four corners, the rectangle fills the screen, and it keeps filling it when the screen is resized.

*Lane.* manim · `B11_FullRect` · runner-up: an editor capture of the Layout menu (E1, optional)

### B12 · 40 words · ~14 s

> Put that color rect in a canvas layer. A canvas layer is a group drawn together, with a number. The game is at zero. A layer numbered one is drawn after it, so it can read everything the game drew.

*Picture.* Two panes in an exploded side view: the lower pane 'game · 0' with a tiny meadow and player; the upper pane 'canvas layer 1' holding the full-rect colour rect, tinted pale grey, with the definition 'canvas layer: a group drawn together, with a number; higher is drawn later'. The lower pane slides in first, then the upper one is drawn on top of it with its number. A drawn arrow runs from the upper pane down through the lower: 'reads everything below'.

*Motion.* The panes arrive in order, zero then one, and the arrow shows the upper layer reading everything beneath it.

*Lane.* manim · `B12_LayerStack` · runner-up: LibraryIconRow of layer icons

### B13 · 28 words · ~10 s

> One catch: a color rect catches mouse clicks, so your game never hears them. Set its mouse filter to Ignore, and the clicks pass through to the game.

*Picture.* The two panes again, side view: the game pane below, the full-rect colour rect pane above, labelled 'Mouse > Filter: Stop' (the editor's own words). A click (a drawn arrow tip with an expanding ring) comes down from above and stops at the colour rect, which flashes. The label changes to 'Mouse > Filter: Ignore' and the next click passes through the colour rect to the game pane, which flashes.

*Motion.* The first click stops at the rect; after the label changes the second click passes straight through.

*Lane.* manim · `B13_ClicksStop` · runner-up: ShaderLab with a scripted click

### B14 · 40 words · ~14 s

> Start with gray. A gray pixel has equal red, green and blue. The function dot multiplies each by a weight and adds them up. Green weighs most and blue least, because that is how bright each color looks to us.

*Picture.* One meadow pixel as a green swatch. Three horizontal bars show its red, green and blue values. Each bar is multiplied by a weight chip (0.299, 0.587, 0.114) and shrinks to a partial bar; the three partial bars then slide together end to end into one gray bar and a gray swatch appears beside the green one. The 0.587 chip is ringed last. Caption 'dot(a, b): multiply the matching parts and add them' (the GLOSSARY's wording).

*Motion.* Three bars shrink by their weights and join end to end into one gray bar, and the gray swatch appears.

*Lane.* manim · `B14_WeightedSum` · runner-up: plot of luma against green

### B15 · 40 words · ~14 s

> Then mix. Mix blends two values by an amount: zero gives the first, one gives the second. Make the amount a uniform with a range hint, and your game can drain the color from the whole picture with one dial.

*Picture.* Code card at left (the 10-line gray shader); at right a real Godot window: the meadow and the teal player under a full-screen filter. The amount uniform sweeps from 0 to 1 and the colour drains out of the whole picture, grass, path, flowers and player together.

*Motion.* The colour drains from everything at once as the dial turns.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills of amount 0 and 1

*Capture to record.* C05: scene_c05_gray.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Meadow + player, 05-gray on a full-screen ColorRect in a CanvasLayer (layer 1); amount 0 until u = 0.62, then 1 by u = 0.95. Verified: amount 0, 0.5, 1 match the weights and mix exactly (within 1/255, 9 of 9).

### B16 · 31 words · ~10 s

> Now a spotlight: color near the player, gray everywhere else. The shader needs two numbers from your game: where the player is, and how big the circle is. Both are uniforms.

*Picture.* Code card at left (the 12-line spotlight shader with the plain distance test); at right a real Godot window: the meadow in gray with a coloured area around the teal player, who walks one lap of a flat ellipse. The uniform lines light up as the voice names them.

*Motion.* The coloured area follows the walking player.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C06: scene_c06_spot_oval.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. The player walks one lap of an ellipse (0.20 x 0.12 of the canvas) round the middle; every frame the scene's _process sends player position / canvas size to the filter; radius 0.25. The same capture serves B17. Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).

### B17 · 31 words · ~10 s

> Measure each pixel's distance from the player. The function distance gives the gap between two addresses. If it is more than the radius, make the pixel gray. Otherwise, leave it alone.

*Picture.* The same capture as the previous beat with different lines lit: the distance test, the gray line, the final colour line.

*Motion.* The coloured area keeps following the player while the lines of the test light up in order.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C06 again (see B16): reuse the same video file.

### B18 · 38 words · ~13 s

> Look closely: it is an oval. Addresses run zero to one across and zero to one down, but the screen is wider than tall. So a step across is longer than a step down, and the circle stretches.

*Picture.* A unit square labelled 'addresses: 0 to 1 across, 0 to 1 down' with a circle of radius 0.25 drawn inside it. The square stretches sideways into a 16:9 screen rectangle and the circle becomes an ellipse. Two measurements appear along the ellipse: sideways '0.25 × 1280 = 320 px', up and down '0.25 × 720 = 180 px'. Caption 'oval'.

*Motion.* The square stretches into the wide screen and the circle stretches with it into an oval.

*Lane.* manim · `B18_StretchedAddresses` · runner-up: ShaderLab with readouts on the oval capture

### B19 · 40 words · ~14 s

> Screen pixel size is the size of one pixel, as a fraction of the screen. Its y divided by its x is the aspect ratio: width divided by height. Stretch both addresses across by that, and distances come out equal.

*Picture.* Code card at left (the 14-line fixed spotlight); at right the same walk: the coloured area is an oval until 72 percent of the beat, when the shader is swapped and it becomes a circle.

*Motion.* The oval snaps to a circle at the cue.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with a split view of both shaders

*Capture to record.* C07: scene_c07_spot_swap.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. As C06; at u = 0.72 the material is swapped from 06-spotlight-oval to 07-spotlight (radius 0.25 carried over). Verified: 07 reaches 180 px both ways. Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).

### B20 · 37 words · ~13 s

> The shader cannot see your player. So every frame, your game takes the player's position on screen, divides it by the screen size, and sends it with set shader parameter. Move the player, and the circle follows.

*Picture.* Code card at left with the four-line GDScript _process; at right the finished circular spotlight following the walking player.

*Motion.* The lines light up as the voice names them while the circle follows the player.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace on the GDScript

*Capture to record.* C08: scene_c08_spot_game.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. The scene's own _process is exactly the four lines shown. Verified: the centroid of the lit area sits on the player within 1 px (verify7 C08); with a moved Camera2D the canvas-transform version lands on the player while plain position / size does not (verify8). Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).

## Act III: Bend What Is Behind

### B21 · 35 words · ~12 s

> So far, each pixel read the screen exactly where it sits. Read somewhere else, and the picture bends. Add a small number to the address, and every pixel shows what lies a little further right.

*Picture.* Act title 'Bend What Is Behind' (serif 40) top-left. Code card at left (the 9-line shift shader); at right a real Godot window: one large window in a cream frame over the meadow. The shift uniform sweeps from 0 to 0.1 and the picture inside the frame slides sideways against the picture outside; the sand path breaks at the frame's edges. Label 'shift 0.1'.

*Motion.* The picture inside the frame slides to the left while the picture outside stays put.

*Lane.* capture · `ShaderLab` · runner-up: manim arrow on a picture

*Capture to record.* C09: scene_c09_shift.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Window 0.52 x 0.42 at (0.20, 0.12); shift 0 until u = 0.56, then 0.10 by u = 0.90. Verified: 3,640 of 3,640 sampled pixels show the meadow at x + shift (for 0.1 and for -0.05).

### B22 · 36 words · ~12 s

> Make the number depend on the row. Sine is a smooth wave between minus one and one. Feed it the vertical address, and each row gets a different push, left, then right. Straight lines now ripple.

*Picture.* Code card at left (the 10-line ripple shader without time); at right a real Godot window: a large window in a cream frame; as the amount grows the straight tile edges inside become a chevron of ripples and the flowers stretch sideways.

*Motion.* Straight lines inside the frame start to ripple as the amount grows.

*Lane.* capture · `ShaderLab` · runner-up: manim plot of sin(y) with rows shifted

*Capture to record.* C10: scene_c10_ripple_still.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Window 0.56 x 0.52 at (0.20, 0.08); amount 0 until u = 0.44, then 0.012 by u = 0.92. Verified: the tile edge in ten rows sits at 560 minus 0.01 sin(60 y) times 1280, within 0.5 px (0.6 in Compatibility; the edge is found to a whole pixel).

### B23 · 26 words · ~9 s

> Add time inside the sine, and the ripples travel. Time is seconds on one clock shared by the whole game, so every pixel ripples in step.

*Picture.* Code card at left (the 10-line ripple shader with TIME); at right the same large window with the ripples now travelling, live. Label 'time: one clock'.

*Motion.* The ripples travel through the window, in step across it.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C11: scene_c11_ripple_time.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick, so TIME is repeatable), Forward+, length = the beat's audio. Same window as C10, amount 0.01.

### B24 · 29 words · ~10 s

> Keep the push small. It is a fraction of the screen's width. About one hundredth looks like water. Much more, and the picture stops rippling and starts to tear.

*Picture.* Code card at left with the amount line lit; at right the travelling-ripple window while amount sweeps: calm ripples at 0.01, then the picture shears into streaks at 0.06. Readouts '0.01' then '0.06'.

*Motion.* The ripples grow from calm to torn as the number grows.

*Lane.* capture · `ShaderLab` · runner-up: manim plot of amplitude

*Capture to record.* C12: scene_c12_amount.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. As C11; amount 0.002 rising to 0.01 by u = 0.30, held to u = 0.60, then to 0.06 by u = 0.95.

### B25 · 34 words · ~12 s

> You can also read a blurred copy. Add the hint filter linear mipmap, and Godot builds smaller, blurrier copies of the screen. Read a higher level with texture lod, and you get frosted glass.

*Picture.* Code card at left (the 9-line blur shader; the declaration runs over two lines); at right a real Godot window: a large window in a cream frame; as the blur level rises from 0 to 4 the meadow inside turns to frosted glass while the picture outside stays sharp. Label 'level 4' once the level has reached it.

*Motion.* The picture inside the frame blurs progressively as the level rises.

*Lane.* capture · `ShaderLab` · runner-up: manim stack of shrinking images

*Capture to record.* C13: scene_c13_blur.gd, NATIVE route: a 1920 x 1080 SubViewport at scale 1, the scene built for a 1920 x 1080 canvas (--native; NOT the 4K route, see CAPTURE-PLAN.md 'Routes'), 30 fps, Forward+, length = the beat's audio. Window 0.56 x 0.56 at (0.20, 0.14); blur 0 until u = 0.58, then exactly 4.0 by u = 0.84, held. Verified: largest step between neighbouring pixels 0.377 at level 0, 0.012 at level 2, 0.008 at level 4 (1280 x 720 window, verify4 L8a); mean difference between the level-4 picture and the sharp one inside the window 0.028 on this route, 0.017 on the 4K route, 0.037 in a plain 1280 x 720 window (verify10 A).

### B26 · 37 words · ~13 s

> Which address drives the waves matters. Use the window's own U V, and the ripples ride along when it moves. Use screen U V, and they stay put on the screen while the window slides over them.

*Picture.* Two windows in cream frames over a meadow that scrolls down and back. Left: ripples from the window's own address (UV.y); right: ripples from the screen address (SCREEN_UV.y). Both ripple fields are frozen. Labels 'UV: rides along' and 'screen UV: stays'; small labels 'UV.y' and 'SCREEN_UV.y' under the windows.

*Motion.* On the left the ripples move down with the window; on the right they stay at the same screen rows while the window slides over them.

*Lane.* capture · `ShaderLab` · runner-up: manim two sine plots

*Capture to record.* C14: scene_c14_ride_glued.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. WorldRoot (meadow with a 2-cell bleed + both windows) moves down 140 px between u = 0.12 and 0.52 and back by u = 0.96. Windows 0.30 x 0.46 at (0.08, 0.14) with 13-ripple-ride and at (0.58, 0.14) with 09-ripple-still; no TIME. Verified: after a 100 px move the glued window's edge offsets are unchanged in 6 of 6 rows; the ride window's changed in 6 of 6.

### B27 · 35 words · ~12 s

> A pool is the same trick with a water color. Mix the bent picture halfway toward blue. The source color hint gives you a color picker in the Inspector, so an artist can change it.

*Picture.* Code card at left (the 12-line water shader); at right a real Godot window: the pool, a plain rectangle in the lower left, tinted blue over the bent meadow, rippling live. Near the end the water colour changes blue to violet, as an artist would with the colour picker.

*Motion.* The pool ripples and, at the end, its colour changes from blue to violet.

*Lane.* capture · `ShaderLab` · runner-up: manim blend diagram

*Capture to record.* C15: scene_c15_pool_tint.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. Pool 0.40 x 0.40 at (0.06, 0.52) with 11-water; water = (0.2, 0.5, 0.8) until u = 0.78, then to (0.6, 0.3, 0.8) by u = 0.94. Verified: pool pixel = 0.5 x meadow + 0.5 x water (both renderers); the shader reports a colour hint (no alpha) for water.

### B28 · 36 words · ~12 s

> A pool needs a top edge. Compare the pool's own vertical address with a sine of its horizontal address. Above that wavy line, discard the pixel. Discard throws a pixel away, so the grass shows through.

*Picture.* Code card at left (the 14-line pool shader); at right the same pool capture as the opening: the wavy top edge ripples, and above it the grass shows through.

*Motion.* The top edge of the pool undulates while the grass above it stays untouched.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C01 again (see B01): reuse the same video file. Verified: the first changed row down the pool is a different UV.y at five columns (0.080 to 0.115 in Forward+) and the meadow above it is untouched.

### B29 · 34 words · ~12 s

> Put it together. The pool bends the grass behind it, tints it, and ripples along its own edge. Scroll the world, and the pool scrolls with it, because its waves belong to the pool.

*Picture.* A real Godot window: the meadow, the finished pool and the player all scroll down together and back. The pool's ripples travel with the pool. Label 'pool scrolls too'.

*Motion.* The whole scene pans and the pool stays glued to the ground, rippling.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C16: scene_c16_pan.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. WorldRoot (meadow with a 2-cell bleed, the 12-pool pool, the player) moves down 110 px between u = 0.54 and 0.74 and back between u = 0.80 and 0.98.

## Act IV: What It Can See

### B30 · 38 words · ~13 s

> A shader can only read what exists when the copy is taken. Godot takes it once, right before the first reading node on a layer is drawn. Everything drawn earlier is in it. Everything drawn later is not.

*Picture.* Act title 'What It Can See' (serif 40) top-left. A row of draw-step tiles inside a bracket 'layer 0': ground, tree, reader 1 (a window), player, reader 2 (a second window); 'reader: a node whose shader reads the screen texture'. A camera flash fires just before 'reader 1' and a copy tile drops below the row, labelled 'the copy'. Tiles before the flash get a check mark; the tiles after it do not. An arrow from reader 2 points at the same copy tile, not a new one.

*Motion.* The flash fires once, before the first reader; checks land on the earlier tiles only; the second reader's arrow points at the same copy.

*Lane.* manim · `B30_OnceBeforeTheFirstReader` · runner-up: BrowserCapture of the docs 'Behind the scenes' paragraph

### B31 · 38 words · ~13 s

> To see what is in the copy, put a tiny copy on screen. It shows the mustard block, drawn before it, and not the violet one, drawn after. Move the lens later, and the violet block appears too.

*Picture.* A real Godot window: the meadow with a big mustard block at lower left (drawn before the lens) and a violet block at lower centre (drawn after it); top right, a lens in a cream frame shows a tiny copy of the screen, with the mustard block in it and no violet block. Labels 'drawn before' and 'drawn after'. At 76 percent the lens moves later in the tree and the violet block appears inside it.

*Motion.* The violet block appears inside the lens when the lens moves later in the draw order.

*Lane.* capture · `ShaderLab` · runner-up: manim two copies side by side

*Capture to record.* C17: scene_c17_xray.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Tree order World, X (mustard block, 0.16 x 0.26 at (0.08, 0.60)), Lens (02-miniature, 0.30 x 0.30 at (0.60, 0.06)), Y (violet block at (0.52, 0.58)); at u = 0.76 the lens is moved to the end of the tree. Verified: before the move the lens shows X and not Y (red and blue test blocks in verify2 M1 give the same result).

### B32 · 38 words · ~13 s

> A second reading node on the same layer reuses that copy. Overlap two windows that each flip the colors. Flipping twice should restore the original. Instead the overlap stays flipped, because the second window never saw the first.

*Picture.* A real Godot window: window A (cream frame) flips the colours over the meadow. At 30 percent window B (cream frame) appears, overlapping A's lower right. The overlap looks exactly like the rest of A and B, flipped once. A terracotta ring settles on the overlap; labels 'expected: original' and 'got: flipped'.

*Motion.* B appears over A and the overlap is flipped once, not twice.

*Lane.* capture · `ShaderLab` · runner-up: manim two layered panes

*Capture to record.* C18: scene_c18_overlap.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. A = 03-invert at (0.16, 0.12), B = 03-invert at (0.38, 0.30), both 0.34 x 0.46, same canvas; B hidden until u = 0.30. Overlap region (0.38, 0.30) to (0.50, 0.58). Verified: the overlap reads inverted once (1 minus meadow), in both renderers.

### B33 · 39 words · ~13 s

> The fix is a node called Back Buffer Copy, placed between them, with its copy mode set to Viewport. It takes a fresh copy of the whole screen right there. Now the overlap flips back to the original colors.

*Picture.* The same two windows from the start; a BackBufferCopy node sits between them in the tree and is switched on at 76 percent. Before it, the overlap is flipped once; after it, the overlap shows the original meadow colours. Label 'Back Buffer Copy · Viewport' appears early; a ring settles on the overlap at the end.

*Motion.* The overlap snaps back to the original colours at the cue.

*Lane.* capture · `ShaderLab` · runner-up: manim node between two panes

*Capture to record.* C19: scene_c19_overlap_fix.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. As C18 with both windows visible from the start and a BackBufferCopy (copy_mode Viewport) between A and B, visible (switched on) from u = 0.76. Verified: with it the overlap reads as the original meadow; with a default BackBufferCopy (Rect mode) it does not.

### B34 · 35 words · ~12 s

> A canvas layer takes its own copy. So the gray filter on its own layer sees everything below it, even the pool, with no Back Buffer Copy. Pool, player and grass all turn gray together.

*Picture.* A real Godot window: the meadow, the live pool and the player on the game layer; a gray filter on its own layer starts at amount 0. At 72 to 90 percent the amount rises and the whole picture, pool and player included, turns gray together. Label 'own layer'; a ring on the pool.

*Motion.* Pool, player and grass all go gray together.

*Lane.* capture · `ShaderLab` · runner-up: manim layered panes

*Capture to record.* C20: scene_c20_fresh_layer.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. Meadow, 12-pool, player on layer 0; 05-gray on a full-screen ColorRect in a CanvasLayer (layer 1), amount 0 until u = 0.72, then 1 by u = 0.90. No BackBufferCopy. Verified: the player's pixel and the pool's pixel equal their luma grays (player 0.5529 against 0.5514; pool 0.5804 against 0.5795).

### B35 · 27 words · ~9 s

> Anything on a higher layer is untouched. Put the health bar on layer two, above the filter, and it keeps its color while the game turns gray.

*Picture.* A real Godot window: the game is already gray. The health bar, top left, starts on layer 0 and is gray with it; at 58 percent its layer index is set to 2 and it turns mustard while the game stays gray. Labels 'layer 0: gray' and 'layer 2: color'.

*Motion.* The health bar regains its colour at the cue while the game stays gray.

*Lane.* capture · `ShaderLab` · runner-up: manim stacked panes

*Capture to record.* C21: scene_c21_hud.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Meadow + player; 05-gray on layer 1 at amount 1 from the first frame; the health bar in its own CanvasLayer, index 0 until u = 0.58, then 2. Verified: a bar on layer 2 keeps its colour (0.902, 0.722, 0.251), a bar below the filter is flipped or grayed.

### B36 · 40 words · ~14 s

> The docs' examples add two more hints. Repeat disable means reading past the screen's edge gives the edge pixel, not the far side. Filter nearest asks for the exact pixel, no blending. The Forward Plus renderer obeys; Compatibility blends anyway.

*Picture.* Code card at left (the 10-line shader with the full declaration over two lines); at right a real Godot window: a window flush with the right edge of the screen; as the shift grows its right part reads past the edge and fills with horizontal streaks, the edge pixels repeated. The third label defines 'renderer' where the narration first says it; the capture is Forward+ (the video label says so), so the Compatibility half of the sentence is carried by the narration alone.

*Motion.* The window's right part smears into streaks as it reads past the edge of the screen.

*Lane.* capture · `ShaderLab` · runner-up: BrowserCapture of the docs declaration

*Capture to record.* C22: scene_c22_edge.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps, Forward+, length = the beat's audio. Window 0.40 x 0.44 at (0.60, 0.20) flush with the right edge, 15-edge-clamp; shift 0 until u = 0.28, then 0.30 by u = 0.62. Verified: with repeat_disable (and with no repeat hint) a read past the edge returns the edge pixel in both renderers. filter_nearest is a Forward+ result only: magnified 50 times, Forward+ gives a hard step where filter_linear gives 35 distinct colours; Compatibility reads all three alike (34), so the narration names the renderer (verify4 L7b, verify9). This capture does not show that difference.

### B37 · 32 words · ~11 s

> Put them together. Water that bends the grass. A spotlight that follows the player. A health bar the filter never touches. Two shaders, each reading a copy of what was already drawn.

*Picture.* A real Godot window: the pool, the player walking a wide flat ellipse, the spotlight following him (gray outside, colour inside), the health bar above everything in colour. Where the player passes the pool, the pool turns to colour as the light arrives and the water keeps rippling.

*Motion.* The light follows the player across the pool, which turns to colour and ripples under it, while the health bar never changes.

*Lane.* capture · `ShaderLab` · runner-up: manim three icons

*Capture to record.* C23: scene_c23_finale.gd, 1280 x 720 canvas through the 4K SubViewport route, 30 fps (fixed tick), Forward+, length = the beat's audio. Layer 0: meadow, 12-pool, the player on a wide ellipse (0.34 x 0.10 of the canvas around (0.50, 0.62)); layer 1: 07-spotlight (radius 0.25) fed by the scene's _process; layer 2: the health bar. Route check: the spotlight scenes look the same on the 4K route as in a plain 1280 x 720 window (verify10 B, within 1 canvas pixel).

### B38 · 27 words · ~9 s

> When a screen shader misbehaves, check four things. The old name. The draw order. The copy for each layer. And which layer your health bar sits on.

*Picture.* A four-row table, one row ringed as the voice names each cause.

*Motion.* The ring steps down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim checklist

## Closing

### BVDT · recap · 70 words · ~24 s

> Let's recap with Claude. The screen texture is a copy of what was drawn so far, read with screen U V. A color rect on a canvas layer covers every pixel, so one shader can filter the whole game. Read the screen at a shifted address, and the picture behind it bends. One copy is made for each layer, so draw order and layers decide what a shader can see.

*Picture.* The recap card: The screen texture is a copy of what was drawn so far, read with screen UV. / A color rect on a canvas layer covers every pixel, so one shader can filter the whole game. / Read the screen at a shifted address, and the picture behind it bends. / One copy is made for each layer, so draw order and layers decide what a shader can see.

### BHTF · your turn · 102 words · ~35 s

> Your turn. Paste this into Claude: Write a Godot four canvas item shader for a full-screen color rect that turns everything behind it gray. One float uniform called amount, from zero to one: at zero nothing changes, at one it is fully gray. Read the screen with a screen texture hint, never the old built-in. Then point to the line that reads the screen. Now check two things yourself. Does the line that reads the screen use a screen texture hint, and not the old name? And at zero is the game untouched, and at one is everything gray, the player too?

*Prompt shown and read in full:* Write a Godot four canvas item shader for a full-screen color rect that turns everything behind it gray. One float uniform called amount, from zero to one: at zero nothing changes, at one it is fully gray. Read the screen with a screen texture hint, never the old built-in. Then point to the line that reads the screen.

*Two checks:* Check: the line that reads the screen uses a hint screen texture uniform, not SCREEN_TEXTURE. · Check: at amount zero the game is untouched; at one everything, the player too, is gray.

### BOUT · outro · 7 words · ~4 s

> Reading the Screen. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


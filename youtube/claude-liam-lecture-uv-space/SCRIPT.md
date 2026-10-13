# Script: UV Space

**What this is.** The words Liam will say in *UV Space*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 48 beats, 1804 words, about **10:17** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 19, manim 17, remotion 6.

**If it runs long.** Cut, in this order: the node-setting beat (B16, a second route to the same repeat switch), the transparent-border beat (B37), the stretched-pixel beat (B31), the fold drawing (B26) and the gate drawing (B39: the mask then takes one beat, B38). Each repeats or decorates an idea another beat already carries. The reversal beats (B09 to B11), the centered zoom (B19 to B21), the oval and its fix (B28, B29, B32, B33) and the mask result (B40) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | The Address Book | 8 | 300 | ~1:42 |
| II | Move Where You Look | 10 | 363 | ~2:03 |
| III | Center and Mirror | 9 | 299 | ~1:42 |
| IV | Fixing the Squash | 8 | 292 | ~1:39 |
| V | Staying Inside the Picture | 7 | 258 | ~1:28 |

## Opening

### BOPEN · identity card · 33 words · ~11 s

> U V Space. Learn to move, scale, tile and mirror the address a shader looks up, so you can scroll a picture, zoom into it, and keep a circle round on any shape.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "UV Space", and the line "Move, scale and mirror the address a shader looks up".

### BIDEA · the question · 51 words · ~17 s

> Hallo. This is Liam, in for Bear. Many people read U V as where a pixel sits on the screen. It is where the pixel sits on its shape. And since it is only a pair of numbers, you can change it before you use it. Everything else follows from that.

*Picture.* The hesitant writer types: "UV says where a pixel is on
the screen." then deletes "the screen" and types "the shape".

### BDEFS · terms · 60 words · ~20 s

> Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. A texture is an image a shader can read by address. A vector is a bundle of two to four numbers. And a uniform is a value your game sets from outside the shader.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Pixel** — one dot of the picture on screen; **Texture** — an image a shader can read by address; **Vector** — a bundle of two to four numbers; **Uniform** — a value your game sets from outside; every pixel sees the same one

## Act I: The Address Book

### B01 · 34 words · ~12 s

> One picture, and it never changes. Yet here it slides, shrinks and repeats. The picture file is untouched. The shader only changed where it looks. That is the trick behind scrolling, zooming and tiling.

*Picture.* Act title 'The Address Book' (serif 40) top-left. A real Godot render in a framed window on the stage: the teal test sprite sits still, then slides left and wraps around, then shrinks into a three by three grid of copies. Label: 'same picture, same file'.

*Motion.* The picture slides, then shrinks and tiles, while the label says the file never changes.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a picture moving behind a window

*Capture to record.* C01: Lab sprite (--sprite-tex white) with --tex pic=sprite, lab-shaders/01-hook-controls.gdshader. Keyframes as fractions of the beat length L (about 11.6 s): shift = 0 until 0.17 L, then 0 to 1.0 over 0.17-0.28 L, hold; zoom = 1 until 0.28 L, then 1 to 3 over 0.28-0.42 L, hold. Render L + 1 s, 30 fps, Forward+, no input. End state (shift 1.0, zoom 3.0): nine whole copies, aligned (probes hook-tiled-fill).

### B02 · 41 words · ~14 s

> Every pixel on a shape has an address: two numbers, called U V. The first says how far across, the second how far down, each from zero to one. The top left is zero, zero. The bottom right is one, one.

*Picture.* A square with U labelled along the top (a drawn arrow pointing right) and V labelled down the left side (a drawn arrow pointing down), corner labels (0, 0) at the top left and (1, 1) at the bottom right, and a terracotta dot whose live (u, v) label updates as it moves. Caption (GLOSSARY wording): 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.

*Motion.* The dot slides across (U grows), then down (V grows), then jumps to the top-left corner and to the bottom-right corner, its label updating each time.

*Lane.* manim · `B02_AddressSquare` · runner-up: ShaderLab with the address-map render

### B03 · 43 words · ~15 s

> Notice that the second number counts down, the opposite of a school graph. And size does not matter: a tiny shape and a huge one both run zero to one. An address is a fraction of the shape, not a count of pixels.

*Picture.* Two squares side by side, one small and one large, both labelled with the same corner values (0, 0) and (1, 1) and both carrying a dot at (0.5, 0.8) with an identical label. A grey up arrow marked 'school graph' beside the small square and a terracotta down arrow marked 'V' beside the large one. Caption: 'fraction, not pixels'.

*Motion.* The grey up arrow appears and is replaced by the terracotta down arrow; then the large square grows beside the small one and its dot lands on the same label.

*Lane.* manim · `B03_AnySize` · runner-up: LectureEvidenceTable of three shape sizes

### B04 · 40 words · ~14 s

> Here is every address at once, drawn as a color. Red is the first number, so it grows to the right. Green is the second, so it grows downward. Blue is held at half. Each pixel paints its own address.

*Picture.* Code card at left with the one-line address-map shader; at right a real Godot window with a centered square showing the red-green picture (red grows to the right, green grows downward, blue held at half), corner labels outside the square landing in turn: (0, 0), (1, 0), (0, 1), (1, 1).

*Motion.* The corner labels land with the words: red grows to the right (top right), green grows downward (bottom left).

*Lane.* capture · `ShaderLab` · runner-up: manim: a UV square drawn with a colour gradient

*Capture to record.* C02: Lab sprite (--sprite-tex white), lab-shaders/02-address-map.gdshader, still PNG 3840x2160 (16:9 window, the square quad centered at 0.45 of the width). Corner colours (probes): top left (0.02, 0.02, 0.50), top right (0.98, 0.02, 0.50), bottom left (0.02, 0.98, 0.50), bottom right (0.98, 0.98, 0.50).

### B05 · 35 words · ~12 s

> To color a pixel, the shader can read a picture at that pixel's address. The texture function takes a picture and an address, and hands back the color stored there. That color becomes the pixel's.

*Picture.* Left, a small grid of outline pixel cells labelled 'the shape' with one cell ringed in terracotta and tagged with its address (0.7, 0.5); right, the picture (a cream card with the teal test sprite) labelled 'TEXTURE: the node's own picture' (GLOSSARY wording). An arrow runs from the ringed pixel to the same relative spot on the picture, where a terracotta dot lands; a teal swatch travels back along the arrow and the ringed pixel fills with teal. Small tag on the arrow: 'texture()'.

*Motion.* An arrow goes out from the pixel to a spot on the picture, and the color found there travels back and fills the pixel.

*Lane.* manim · `B05_Lookup` · runner-up: DesignPipelineClaim, show-tell isometric

### B06 · 34 words · ~12 s

> Inside fragment, which Godot runs once for every pixel the shape covers, we read the picture at that pixel's own address. Nothing is changed, so the picture comes out exactly as it went in.

*Picture.* Code card at left with the three-line lookup shader; at right a real Godot window showing the test sprite drawn plainly, with no shader. At 'Nothing is changed' the lookup shader is switched on and the picture does not change at all. A caption defines fragment (GLOSSARY wording): 'fragment(): runs once for each pixel the shape covers; sets its color'. Readout 'shader on' at the switch; then a terracotta ring settles on the sprite's square with the readout 'unchanged'.

*Motion.* The shader switches on and nothing changes: the picture is pixel for pixel the same.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C03: Lab sprite (--sprite-tex sprite). No material until 0.58 L, then --material-at assigns lab-shaders/03-lookup.gdshader; the picture must not change. Render L + 1 s (L about 11.6 s), 30 fps, Forward+. Verified: with the shader and without it, 0 of 230,400 pixels differ, largest channel difference 0.0 (verify-identity.gd D1). Probes (fill-window): middle (0.372, 0.639, 0.569) teal, eyes (0.980, 0.977, 0.961) at (0.4, 0.44) and (0.6, 0.44), corner (0.851, 0.835, 0.792) = stage.

### B07 · 36 words · ~12 s

> Here is a way to hold it in your head. The picture stays put. The shape is a window onto it, and the address says where the window sits. Change the address, and the window slides.

*Picture.* Left, a large cream card labelled 'the picture' holding the teal test sprite and a small terracotta tick at its top-left corner; over it a terracotta-outlined rectangle labelled 'the shape'. Right, a framed panel labelled 'what you see' showing the part of the picture inside the outline. Caption: 'address moves it'.

*Motion.* The outlined window slides right across the fixed picture while the panel's contents shift left, then it slides back.

*Lane.* manim · `B07_Window` · runner-up: ShaderLab: a real render with the quad ringed

### B08 · 37 words · ~13 s

> In fragment, the address is read-only. So the pattern never changes: copy it into a variable, bend the copy, and look up the picture with the bent copy. Every trick from here fills in the middle line.

*Picture.* A cream code card with the real seven-line template; focus lands on the function, then the copy line, then the empty bend line, then the lookup line as each is named.

*Motion.* Line focus steps through copy, bend, look up on the words.

*Lane.* remotion · `LectureCodeTrace` · runner-up: ClaudeCodeBeat

## Act II: Move Where You Look

### B09 · 32 words · ~11 s

> Predict first. We subtract a quarter from the horizontal address. Which way does the picture go? Watch. It slides right, even though we subtracted. That feels backwards, so let's check the numbers.

*Picture.* Act title 'Move Where You Look' (serif 40) top-left. Code card at left with the shift shader; at right a real Godot window: the teal test sprite sits still while the voice asks which way it will go, then, on 'Watch', slides right inside its square while the readout counts amount 0 to 0.25. A terracotta ring marks the sprite's fixed square.

*Motion.* The picture slides right, clipped by the square's edge, though the code subtracts.

*Lane.* capture · `ShaderLab` · runner-up: manim: the window slides over the picture (as B07)

*Capture to record.* C04: Lab sprite (--sprite-tex sprite), lab-shaders/05-shift-x.gdshader. Keyframes (L about 10.9 s): amount = 0 until 0.52 L, then 0 to 0.25 over 0.52-0.72 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.3, 0.5) stage, (0.9, 0.5) teal, eyes at (0.65, 0.44) and (0.85, 0.44).

### B10 · 36 words · ~12 s

> Here is why. The pixel in the middle now looks up the spot a quarter of the way across. So whatever lives at that spot shows up in the middle. Everything lands a quarter further right.

*Picture.* Two horizontal rulers from 0 to 1 with ticks at 0, 0.25, 0.5, 0.75, 1: the top one labelled 'the picture' with a teal dot at 0.25, the bottom one labelled 'the shape' with a terracotta pixel marker at 0.5. An arrow runs from the pixel marker up to 0.25 on the picture ruler (tag 'looks up 0.25'), and the teal dot then slides down the arrow to land at 0.5 on the shape ruler (tag 'lands at 0.5').

*Motion.* The pixel at 0.5 reaches back to 0.25, and the teal dot found there lands at 0.5: everything moved a quarter right.

*Lane.* manim · `B10_WorkedNumbers` · runner-up: LectureEvidenceTable of the lookup

### B11 · 34 words · ~12 s

> So the rule is a reversal. Subtract from the horizontal address, and the picture moves right. Add to it, and it moves left. Change the address one way, and the picture goes the other.

*Picture.* Two stacked horizontal rulers as in the previous drawing: the picture (with a teal dot) above, what the shape shows below. First a terracotta arrow pointing right labelled 'subtract from U' with the dot moving right on the lower ruler; then an arrow pointing left labelled 'add to U' with the dot moving left. Persistent small tag: 'the opposite way'.

*Motion.* On 'subtract' the dot moves right; on 'add' it moves left, always against the arrow.

*Lane.* manim · `B11_Reversal` · runner-up: ShaderLab with both signs swept

### B12 · 32 words · ~11 s

> The same goes for the vertical address, with one twist. It counts downward, so subtracting from it sends the picture down. Subtract from both, and the picture moves right and down together.

*Picture.* Code card at left with the two-shift shader; at right a real Godot window where the teal sprite first slides straight down inside its fixed square (shift_y from 0 to 0.25), then also slides right (shift_x from 0 to 0.25), ending right and down. Two readouts count the shifts.

*Motion.* The picture slides down first, then right as well.

*Lane.* capture · `ShaderLab` · runner-up: manim: a diagonal arrow

*Capture to record.* C05: Lab sprite (--sprite-tex sprite), lab-shaders/06-shift-xy.gdshader. Keyframes (L about 10.9 s): shift_y = 0 until 0.36 L, then 0 to 0.25 over 0.36-0.56 L, hold; shift_x = 0 until 0.66 L, then 0 to 0.25 over 0.66-0.86 L, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window): shift_y only: eyes cream at (0.4, 0.69) and (0.6, 0.69), (0.4, 0.44) stage; both: eyes at (0.65, 0.69) and (0.85, 0.69).

### B13 · 40 words · ~14 s

> Now scale. Multiply the address by two. The picture shrinks to half its width and half its height, a quarter of its area, and sits in the top left corner. The rest of the shape has no picture to read.

*Picture.* Code card at left with the scale shader; at right a real Godot window where the teal sprite shrinks, pinned toward the top left of its fixed square, as zoom grows from 1 to 2. A terracotta ring settles on the top-left quarter of the square (readout 'one quarter'), then on the empty rest (readout 'nothing to read').

*Motion.* The picture shrinks toward the top-left corner and ends in the quarter of its square.

*Lane.* capture · `ShaderLab` · runner-up: manim: a ramp doubling

*Capture to record.* C06: Lab sprite (--sprite-tex sprite), lab-shaders/07-scale.gdshader. Keyframes (L about 13.6 s): zoom = 1 until 0.12 L, then 1 to 2 over 0.12-0.45 L, hold. Render L + 1 s, 30 fps, Forward+. End state: blob area = 0.2506 of the zoom-1 area (22,865 to 5,731 teal pixels, 640x360 look run), blob centre at (0.25, 0.25) of its square.

### B14 · 36 words · ~12 s

> Why smaller? Doubled, the address runs from zero to two across the shape. The picture only covers zero to one. So it fills the first half of each side, where the address is still below one.

*Picture.* Two equal-length horizontal rulers: the top one labelled 'the shape' from 0 to 1, the bottom one labelled 'the address' whose scale grows from 0-1 to 0-2 as the dial turns. The first half of the address ruler (0 to 1) is filled teal and labelled 'the picture'; the second half (1 to 2) is grey and labelled 'no picture'. A dashed vertical line joins the middle of the shape ruler to 1 on the address ruler.

*Motion.* The address ruler's labels stretch from 0-1 to 0-2, the teal part is squeezed into the left half and the dashed line lands on 1 at the middle.

*Lane.* manim · `B14_WhySmaller` · runner-up: ShaderLab with an address ramp underneath

### B15 · 37 words · ~13 s

> What lies beyond one? By default, the lookup keeps returning the picture's edge pixels. Declare the texture with repeat enable, and the picture starts over instead. Scale by three, and you get a three by three grid.

*Picture.* Code card at left with the tile shader; at right a real Godot window where the sprite first shrinks alone into the top-left quarter (nothing repeats), then, when the repeat switch comes on, the copies appear at once as a two by two grid and grow to three by three as zoom reaches 3.

*Motion.* The empty space fills with copies the moment repeat switches on.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace for the one hint line

*Capture to record.* C07: Lab sprite (--sprite-tex white) with --tex pic=sprite. Material A (lab-shaders/08-tile-no-repeat.gdshader) until 0.60 L, then --material-at assigns material B (lab-shaders/09-tile.gdshader). Keyframes (L about 12.6 s): zoom = 1 until 0.02 L, then 1 to 2 over 0.02-0.30 L, hold at 2 until 0.72 L, then 2 to 3 over 0.72-0.84 L, hold. Render L + 1 s, 30 fps, Forward+. Probes: no-repeat at zoom 2 shows one blob in the top-left quarter and stage elsewhere; repeat at zoom 3 shows nine teal centres.

### B16 · 38 words · ~13 s

> A node's own texture has the same switch. It is called texture repeat. Set it to enabled, in the node's settings or in code, and that texture repeats too. Mirror is another setting: every other copy is flipped.

*Picture.* The real Godot 4.7 CanvasItem page scrolled to the TextureRepeat list in a browser window; the camera pushes in on TEXTURE_REPEAT_ENABLED, a terracotta ring marks it, then it moves to TEXTURE_REPEAT_MIRROR. (Ring fractions are estimates: the build sets them from the real capture.)

*Motion.* The camera pushes in on the line the voice names, then moves to the mirror line.

*Lane.* remotion · `BrowserCapture` · runner-up: LectureCodeTrace: texture_repeat = TEXTURE_REPEAT_ENABLED

### B17 · 38 words · ~13 s

> Now let it move on its own. Add a tenth of the time to the horizontal address. Time is seconds on one clock the whole game shares. The picture scrolls left, a tenth of its width every second.

*Picture.* Code card at left with the scroll shader; at right a real Godot window where the sprite grid slides steadily to the left and wraps around forever. A caption defines TIME (GLOSSARY wording): 'TIME: seconds on one clock shared by the whole game'.

*Motion.* The grid slides left at a steady speed, a tenth of a picture each second.

*Lane.* capture · `ShaderLab` · runner-up: manim: a ruler sliding

*Capture to record.* C08: Lab sprite (--sprite-tex white) with --tex pic=sprite, lab-shaders/10-scroll.gdshader, live TIME, repeat enabled by the shader, zoom fixed by the sprite fit (the picture repeats once per quad width). Render L + 1 s (L about 12.9 s), 30 fps, Forward+. Measured: the picture position under a fixed pixel advances about 0.10 per second (run-3-scroll.log: 0.100 on each of three steps; an earlier run read 0.095 to 0.105).

### B18 · 40 words · ~14 s

> Four moves, then. Subtract, and the picture moves one way. Add, and it moves the other. Multiply by more than one, and it shrinks. Multiply by less than one, and it grows. Always the opposite of what the address does.

*Picture.* A four-row table, one row ringed as each move is named.

*Motion.* The ring steps down the four rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: four arrows

## Act III: Center and Mirror

### B19 · 33 words · ~11 s

> Now zoom in: multiply by less than one. Try one half. The picture grows, but it swells toward the bottom right and slides out of frame. That is not the zoom we wanted.

*Picture.* Act title 'Center and Mirror' (serif 40) top-left. Code card at left with the scale shader; at right a real Godot window where, as zoom falls from 1 to 0.5, the sprite swells and slides toward the bottom right of its fixed square until only an arc with one eye remains.

*Motion.* The picture grows but drifts away from the top left corner and out of frame.

*Lane.* capture · `ShaderLab` · runner-up: manim: the corner pivot (B20)

*Capture to record.* C09: Lab sprite (--sprite-tex sprite), lab-shaders/07-scale.gdshader. Keyframes (L about 11.2 s): zoom = 1 until 0.24 L, then 1 to 0.5 over 0.24-0.66 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.5, 0.5) stage, (0.9, 0.9) teal, (0.8, 0.88) cream (the left eye).

### B20 · 34 words · ~12 s

> Scaling keeps zero fixed, so zero is the pivot. Here zero is the top left corner, so everything grows away from that corner. To grow from the middle, the middle has to be zero.

*Picture.* Two side-by-side panels. Left, labelled 'corner is zero': a small pattern (a cream square with the teal sprite icon) at the panel's top-left corner with a terracotta pivot dot on the corner. Right, labelled 'middle is zero': the same pattern centered with the pivot dot at its middle. Tag on each pivot: 'zero'.

*Motion.* On the left the pattern grows away from the corner; on the right the same pattern grows in place.

*Lane.* manim · `B20_Pivot` · runner-up: ShaderLab with an overlay dot at zero

### B21 · 26 words · ~9 s

> Three steps: subtract a half so the middle is zero, scale, then add the half back. Now the picture grows in place, around its own middle.

*Picture.* Code card at left with the centered zoom shader; at right a real Godot window where, as zoom falls from 1 to 0.5, the sprite grows in place around the middle of its square until the two eyes are large.

*Motion.* The picture grows around its own middle and stays put.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace on the one line

*Capture to record.* C10: Lab sprite (--sprite-tex sprite), lab-shaders/11-zoom-centered.gdshader. Keyframes (L about 8.8 s): zoom = 1 until 0.62 L, then 1 to 0.5 over 0.62-0.92 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.5, 0.5) teal, eyes at (0.3, 0.38) and (0.7, 0.38).

### B22 · 34 words · ~12 s

> Many shaders skip adding the half back and stay centered. Double the address and subtract one. Now the range is minus one to one, zero is the middle, and left and up are negative.

*Picture.* A square with 0 to 1 labels at its corners, (0, 0) top left and (1, 1) bottom right. A tag 'x 2' then 'minus 1' appears; the labels animate to (-2..2) then to (-1, -1) top left, (1, -1) top right, (-1, 1) bottom left, (1, 1) bottom right, with a terracotta dot at the middle labelled (0, 0). The left half and the top half get a small 'negative' tag.

*Motion.* The corner labels slide from 0-1 to minus one to one and the dot settles at the middle, labelled zero, zero.

*Lane.* manim · `B22_Centered` · runner-up: ShaderLab with the sign shader

### B23 · 35 words · ~12 s

> In these coordinates, the length of the address is its distance from the middle. Closer than the radius means inside a circle. So a circle is one comparison, and the radius is the only number.

*Picture.* Code card at left with the disc shader; at right a real Godot window where a teal disc grows in the centered square as the radius readout sweeps from 0.15 to 0.8.

*Motion.* The disc grows from the middle as the radius dial turns.

*Lane.* capture · `ShaderLab` · runner-up: manim: a circle from a distance

*Capture to record.* C11: Lab sprite (--sprite-tex white), lab-shaders/12-disc.gdshader. Keyframes (L about 11.9 s): radius = 0.15 until 0.10 L, then 0.15 to 0.8 over 0.10-0.85 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.5, 0.5) and (0.85, 0.5) teal, (0.95, 0.5) and (0.9, 0.9) stage.

### B24 · 35 words · ~12 s

> Now put two eyes on that circle. One test finds the right eye, and the left stays empty. We could write a second test for the left. But everything symmetric would need two of everything.

*Picture.* Code card at left with the one-eye shader; at right a real Godot window with a teal head and one white eye on the right; as eye x sweeps from 0.3 to 0.5 the right eye drifts outward and the left side stays empty. A terracotta ring on the empty left side with the readout 'nothing here'.

*Motion.* The right eye moves; the left stays empty.

*Lane.* capture · `ShaderLab` · runner-up: manim: two circles, one crossed out

*Capture to record.* C12: Lab sprite (--sprite-tex white), lab-shaders/13-face-one-eye.gdshader. Keyframes (L about 11.9 s): eye_x = 0.3 until 0.30 L, then 0.3 to 0.5 over 0.30-0.75 L, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window, eye_x 0.3): (0.65, 0.425) white, (0.35, 0.425) teal (head, no eye).

### B25 · 33 words · ~11 s

> Absolute value drops the minus sign: minus point three becomes point three. Apply it to the horizontal address, and the left half reads exactly like the right. One test now draws both eyes.

*Picture.* Code card at left with the two-eye shader (one added line, p.x = abs(p.x)); at right the real Godot window: the head with one white eye, then, on 'the left half reads exactly like the right', the left eye appears and, as eye x sweeps from 0.3 to 0.5, the two eyes slide apart together. Readouts: '-0.3 to 0.3', then 'both eyes'.

*Motion.* The left eye appears when abs is applied, and both eyes move apart together under one test.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace on the abs line

*Capture to record.* C13: Lab sprite (--sprite-tex white). Material A (lab-shaders/13-face-one-eye.gdshader) until 0.44 L, then --material-at assigns material B (lab-shaders/14-face-two-eyes.gdshader). Keyframes (L about 11.2 s): eye_x = 0.3 until 0.60 L, then 0.3 to 0.5 over 0.60-0.90 L, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window): eye_x 0.3: (0.65, 0.425) and (0.35, 0.425) white; eye_x 0.5: (0.75, 0.425) and (0.25, 0.425) white.

### B26 · 35 words · ~12 s

> Think of absolute value as folding the shape down its middle. The left half lands on the right half. Every pixel on the left gets the same answer as its mirror twin on the right.

*Picture.* A square (the shape) with a dashed vertical line down its middle and two small white eye circles at minus 0.3 and 0.3 on a horizontal centered axis. The left half hinges over the dashed line and lands on the right half; the left eye lands exactly on the right eye. Tag: 'abs: fold'. A small caption 'mirror twins' lands at the end.

*Motion.* The left half swings over the middle line and the left eye lands on the right eye.

*Lane.* manim · `B26_Fold` · runner-up: ShaderLab with a fold marker

### B27 · 34 words · ~12 s

> A different mirror: scale the centered address by minus one. On the vertical address, the picture turns upside down, and the eyes drop below the middle. On the horizontal one, left and right swap.

*Picture.* Code card at left with the flip shader; at right a real Godot window where the sprite sits upright, then at the words 'turns upside down' it flips in one step: the two eyes drop below the middle. Readouts 'flip = 1', then 'flip = -1', and a ring on the lowered eyes.

*Motion.* The picture turns upside down in one step and the eyes land below the middle.

*Lane.* capture · `ShaderLab` · runner-up: manim: the sprite icon mirrored across a line

*Capture to record.* C14: Lab sprite (--sprite-tex sprite), lab-shaders/15-flip.gdshader. Keyframes (L about 11.6 s): flip = 1 until 0.34 L, then a one-frame step to -1, hold. Render L + 1 s, 30 fps, Forward+. Probes (fill-window): flip 1: eye at (0.4, 0.44); flip -1: eyes at (0.4, 0.56) and (0.6, 0.56), (0.4, 0.44) teal. (A sweep through zero is NOT used: at flip 0 the picture is one stretched row, see flip-v-0-look.)

## Act IV: Fixing the Squash

### B28 · 30 words · ~10 s

> Back to the circle. Same test, same radius, but now on a wide shape. Predict the result. We get an oval, as much wider than tall as the shape is.

*Picture.* Act title 'Fixing the Squash' (serif 40) top-left. Code card at left with the same disc shader as before; at right a real Godot window filling a 16:9 frame, empty at first, ringed as 'the wide shape' (readout '16 : 9'); then, as the voice reveals the result, a teal oval grows as the radius readout sweeps from 0 to 0.8. A terracotta ring settles around the oval.

*Motion.* The oval grows from nothing on the wide shape, as wide-to-tall as the shape itself.

*Lane.* capture · `ShaderLab` · runner-up: manim: an ellipse over a rectangle

*Capture to record.* C15: Lab rect (ColorRect filling a 640x360 logical canvas, rendered at 3840x2160), lab-shaders/12-disc.gdshader. Keyframes (L about 10.2 s): radius = 0 until 0.56 L, then 0 to 0.8 over 0.56-0.80 L, hold. Render L + 1 s, 30 fps, Forward+. End state: teal bounding box 512 x 288 of 640 x 360 (measure.py bbox disc-640x360-oval; the same in Compatibility).

### B29 · 40 words · ~14 s

> Here is why. The address runs zero to one on both sides, however long the sides are. This shape is six hundred forty wide and three hundred sixty tall. A tenth across is sixty-four pixels. A tenth down is thirty-six.

*Picture.* A 16:9 rectangle labelled 'the shape' with tick marks every tenth along its top and left edges. The first tenth by tenth cell at the top left is outlined in terracotta: a wide box. A bracket over the top edge reads '64 px', a bracket down the left edge reads '36 px'. Small grey credit: 'Godot 4.7.2 · Forward+ · 640 × 360 window'.

*Motion.* The ticks draw in, the first cell lights up as a wide box and its two brackets measure it.

*Lane.* manim · `B29_AddressCell` · runner-up: ShaderLab with ruler overlays

### B30 · 39 words · ~13 s

> So the radius, point eight of the way from the middle to the edge, is two hundred fifty-six pixels sideways. Up, it is only one hundred forty-four. Measured from the render: five hundred twelve wide, two hundred eighty-eight tall.

*Picture.* The same 16:9 rectangle with the teal oval drawn over it, centered. A terracotta arrow from the middle to the right end of the oval tagged '0.8 = 256 px' and one from the middle up tagged '0.8 = 144 px'; then outer brackets '512 px' across and '288 px' down. Small grey credit: 'Godot 4.7.2 · Forward+ and Compatibility · 640 × 360 window'.

*Motion.* The oval grows, the two radius arrows reach out unequally, and the outer brackets read 512 and 288.

*Lane.* manim · `B30_OvalMeasured` · runner-up: LectureEvidenceTable of radii

### B31 · 35 words · ~12 s

> You may hear that the shape's pixels get stretched. They do not. Every pixel is the same square. It is the address that is uneven: one step of address covers more pixels across than down.

*Picture.* A grid of equal outline squares labelled 'square pixels' (each drawn square stands for four pixels, noted in a grey credit line). Two terracotta brackets cross the grid: a long one across, tagged '64 px', and a short one down, tagged '36 px', both for one tenth of the address.

*Motion.* The squares settle; the long bracket and the short bracket then measure the same address step differently.

*Lane.* manim · `B31_SquareCells` · runner-up: ShaderLab zoomed on pixels

### B32 · 32 words · ~11 s

> The fix: make a step across cover as many pixels as a step down. Multiply the horizontal address by the aspect ratio, which is width divided by height. Here, sixteen over nine.

*Picture.* The wide address cell from the previous drawing (64 by 36 px) with a tag 'x aspect' and a definition line 'aspect ratio: width divided by height = 640 / 360'. The wide cell squeezes horizontally into a square cell labelled '36 × 36 px'.

*Motion.* The wide cell squeezes into a square while the definition of aspect ratio lands.

*Lane.* manim · `B32_CellToSquare` · runner-up: ShaderLab with aspect swept

### B33 · 33 words · ~11 s

> In code, it is one line. Multiply the centered x by aspect, then measure the length as before. The oval becomes a circle, two hundred eighty-eight pixels wide and two hundred eighty-eight tall.

*Picture.* Code card at left with the corrected disc shader; at right a real Godot window filling a 16:9 frame showing the oval from before, which turns into a circle as the aspect readout sweeps from 1 to 1.78. A terracotta ring settles on the circle with the readout '288 × 288'.

*Motion.* The oval turns into a circle as aspect goes from one to one point seven eight.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace on the one line

*Capture to record.* C16: Lab rect (640x360 logical canvas, rendered at 3840x2160), lab-shaders/16-disc-aspect.gdshader, radius 0.8. Keyframes (L about 11.2 s): aspect = 1.0 until 0.50 L, then 1.0 to 1.7778 over 0.50-0.76 L, hold. Render L + 1 s, 30 fps, Forward+. End state: teal bounding box 288 x 288 (measure.py bbox disc-aspect-640x360-round; the same in Compatibility).

### B34 · 41 words · ~14 s

> A shader has no direct way to ask the shape's size, so tell it. Make aspect a uniform, and set it from the node's width over height. Set it again whenever the node is resized, or the circle goes oval again.

*Picture.* A cream code card with the real GDScript (the exact text verified in verify-aspect.gd): focus lands on the function that sets aspect from size, then on the lines that call it again whenever the node is resized.

*Motion.* Line focus lands on the set line, then on the resize hook.

*Lane.* remotion · `LectureCodeTrace` · runner-up: ClaudeCodeBeat

### B35 · 42 words · ~14 s

> Two engine values hold proportions, but each has a catch. Texture pixel size is the texture's, and on a color rect it is one by one. Screen pixel size is the screen's, not your shape's. Only the uniform was right every time.

*Picture.* A four-row, three-column table of measured circle width over height, one row ringed as each source is named; 1.00 means round.

*Motion.* The ring steps down the rows: the uniform row is the only one that reads 1.00 in both columns.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: bars

## Act V: Staying Inside the Picture

### B36 · 39 words · ~13 s

> Back to scaling, with a picture that has a solid edge. Multiply the address by two, and the edge pixels smear across the rest of the shape. Outside the picture, the lookup keeps returning its last row and column.

*Picture.* Act title 'Staying Inside the Picture' (serif 40) top-left. Code card at left with the scale shader; at right a real Godot window where a teal-and-cream checker picture shrinks toward the top left as zoom goes from 1 to 2 and its edge rows and columns stretch into stripes across the rest of the square. A terracotta ring on the stripes with the readout 'edge pixels'.

*Motion.* The picture shrinks and its edge pixels streak across the space it leaves.

*Lane.* capture · `ShaderLab` · runner-up: manim: an edge row streaking

*Capture to record.* C17: Lab sprite (--sprite-tex checker), lab-shaders/07-scale.gdshader. Keyframes (L about 13.3 s): zoom = 1 until 0.30 L, then 1 to 2 over 0.30-0.62 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.25, 0.25) cream, (0.6, 0.05) and (0.9, 0.05) the same teal (constant along the row), (0.9, 0.9) cream (the corner pixel).

### B37 · 34 words · ~12 s

> A sprite with a transparent border hides this, because the pixels being stretched are transparent. Godot's documentation suggests exactly that: a fully transparent border, one pixel wide. The other cure is in the shader.

*Picture.* Two rows of edge pixels at the right edge of two pictures. Top row: a column of solid teal and cream edge pixels with horizontal stripes streaming outward to the right, labelled 'solid edge: stripes'. Bottom row: the same column drawn as dashed transparent cells, with nothing streaming outward, labelled 'transparent edge: nothing'. Small grey credit: 'Godot docs: a one pixel transparent border'.

*Motion.* Stripes stream out of the solid edge; from the transparent edge nothing streams.

*Lane.* manim · `B37_EdgeSmear` · runner-up: ShaderLab with a transparent-border texture

### B38 · 42 words · ~14 s

> We want the picture inside its edges and nothing outside. That is a mask: a number from zero to one for each pixel, saying how much to show. The step function can build one: zero below its edge, one at or above.

*Picture.* A plot with the horizontal axis from -1 to 2 and the vertical axis from 0 to 1: the curve of step(0, x), flat at 0 for x below 0 and flat at 1 from 0 on, with a terracotta dot travelling along it. Definition lines (GLOSSARY wording): 'mask: a number from 0 to 1 per pixel saying how much of something to show' and 'step(edge, x): 0 below the edge, 1 from the edge up'.

*Motion.* The dot travels along the flat line at 0, jumps to 1 at the edge, and stays at 1.

*Lane.* manim · `B38_StepFunction` · runner-up: LectureCodeTrace on the step function

### B39 · 35 words · ~12 s

> Two steps make a gate. One turns on at zero, the other turns off at one. Multiply them, and you get one only between zero and one. Do it for both axes, and multiply again.

*Picture.* The same plot axes. The first step (turns on at 0) and the second step (turns off at 1) are drawn in two greys; they multiply into a terracotta box of height 1 between x = 0 and x = 1. Then a square picture-frame in the plane: ones inside, zeros outside, labelled 'both axes'.

*Motion.* The two steps slide together and the product is a box between zero and one; the box then becomes a square in the plane.

*Lane.* manim · `B39_Gate` · runner-up: ShaderLab with the mask line

### B40 · 30 words · ~10 s

> Multiply the picture's alpha by that mask. Inside the picture, nothing changes. Outside, alpha is zero, so the smear is gone. Scale by two, and you see one clean picture.

*Picture.* Code card at left with the mask shader (ten lines); at right the real Godot window with the same checker picture as the smear beat: as zoom goes from 1 to 2 it shrinks into the top-left quarter and the space it leaves stays empty, with no stripes. A terracotta ring on the empty space with the readout 'no smear'. A caption defines alpha (GLOSSARY wording): 'alpha: how visible a pixel is: 0 invisible, 1 solid'.

*Motion.* The picture shrinks and the space it leaves stays clean.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace on the mask line

*Capture to record.* C18: Lab sprite (--sprite-tex checker), lab-shaders/17-mask.gdshader. Keyframes (L about 10.2 s): zoom = 1 until 0.40 L, then 1 to 2 over 0.40-0.66 L, hold. Render L + 1 s, 30 fps, Forward+. End state probes (fill-window): (0.25, 0.25) cream, (0.75, 0.25) and (0.9, 0.9) stage colour (0.851, 0.835, 0.792), (0.495, 0.495) cream, (0.505, 0.505) stage.

### B41 · 35 words · ~12 s

> Now the opening shader reads like a sentence. Slide the address. Scale it. Look up the picture, with repeat on. Two lines bend the address, one looks it up, and that is the whole effect.

*Picture.* Code card at left with the opening shader (twelve lines); at right the real Godot window repeating the opening render: the sprite slides left and wraps, then shrinks into a three by three grid, while the highlighted lines follow the voice.

*Motion.* The highlighted line moves from slide to scale to lookup as the picture slides, shrinks and tiles.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C19: the same shader and capture setup as C01 (lab-shaders/01-hook-controls.gdshader, --tex pic=sprite) with timing re-keyed to this beat (L about 11.9 s): shift = 0 until 0.26 L, then 0 to 1.0 over 0.26-0.34 L; zoom = 1 until 0.35 L, then 1 to 3 over 0.35-0.55 L, hold. Render L + 1 s, 30 fps, Forward+. End state: nine whole copies (probes hook-tiled-fill).

### B42 · 43 words · ~15 s

> When a U V effect looks wrong, check four causes. Moving the wrong way: you added, not subtracted. Zooming to a corner: zero is not in the middle. Smearing at the edges: no repeat, no mask. A circle gone oval: no aspect fix.

*Picture.* A four-row symptom-and-cause table, one row ringed as each is named.

*Motion.* The ring steps down the four rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: a checklist

## Closing

### BVDT · recap · 63 words · ~21 s

> Let's recap with Claude. U V is a pixel's address on its shape, from zero to one. Change the address one way, and the picture goes the other. Scale around zero, so put zero in the middle. Absolute value folds one side onto the other. Multiply by the aspect ratio, and a circle stays round. Repeat or a mask keeps the edges clean.

*Picture.* The recap card: U V is a pixel's address on its shape, from zero to one. / Change the address one way, and the picture goes the other. / Scale around zero, so put zero in the middle. / Absolute value folds one side onto the other. / Multiply by the aspect ratio, and a circle stays round. / Repeat or a mask keeps the edges clean.

### BHTF · your turn · 78 words · ~26 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a sprite that scrolls its texture to the left, one tenth of the picture every second, and repeats forever. Then point me to the line that sets the direction and the setting that makes it repeat. Then check two things yourself. Does the picture move left, not right? And after ten seconds, does it line up with where it started, with no gap or smear?

*Prompt shown and read in full:* Write a Godot canvas item shader for a sprite that scrolls its texture to the left, one tenth of the picture every second, and repeats forever. Then point me to the line that sets the direction and the setting that makes it repeat.

*Two checks:* Check: the picture moves left, not right. · Check: after ten seconds it lines up with where it started, with no gap or smear.

### BOUT · outro · 7 words · ~4 s

> U V Space. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


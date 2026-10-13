# Script: Drawing Shapes with Math

**What this is.** The words Liam will say in *Drawing Shapes with Math*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 50 beats, 1890 words, about **10:47** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 25, manim 15, remotion 3, editor 1.

**If it runs long.** Cut, in this order: the ring-in-numbers table (B13), the hard-edge beat (B34), the second numbers table (B16), then one of the three dial-sweep beats (B42: arm width and arm gap move into B41). The min and max act shrinks to the sum bug and its fix (B14, B15, B17) plus one beat for the negative case (B18 and B19 merge). The circle by hand (B04, B08), the cross by max (B23), and the crosshair build (B35 to B38) stay: they are the idea and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Inside or Outside | 10 | 383 | ~2:10 |
| II | Rings and Cutouts | 9 | 328 | ~1:52 |
| III | Lines and Crosses | 8 | 270 | ~1:32 |
| IV | Make It a Tool | 7 | 258 | ~1:28 |
| V | The Crosshair | 10 | 306 | ~1:44 |

## Opening

### BOPEN · identity card · 28 words · ~10 s

> Drawing Shapes with Math. Learn how a shader draws a circle, a ring and a cross using only math, then build a crosshair you can reshape with sliders.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Drawing Shapes with Math", and the line "How a pixel decides if it is inside a shape".

### BIDEA · the question · 45 words · ~15 s

> Hallo. This is Liam, in for Bear. To draw a circle on screen, you might reach for a circle image. A shader does not need one. It asks every pixel a single question: are you inside the shape? All the answers together are the shape.

*Picture.* The hesitant writer types: "To draw a circle you need
a circle image." then deletes "a circle image" and types "a question for each pixel".

### BDEFS · terms · 71 words · ~24 s

> Six terms. A function is a named block of code you can call. A shader is a small program the graphics card runs to decide how something is drawn. Its fragment function runs once for each pixel and sets its color. U V is a pixel's address, from zero to one across and down. A vector is a bundle of numbers. A uniform is a value your game sets from outside.

*Picture.* "Terms In This Lecture": **Function** — a named block of code you can call; **Shader** — a small program the graphics card runs to decide how something is drawn; **fragment()** — runs once for each pixel the shape covers; sets its color; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Vector** — a bundle of two to four numbers; **Uniform** — a value your game sets from outside; every pixel sees the same one

## Act I: Inside or Outside

### B01 · 38 words · ~13 s

> Our goal: a crosshair with six dials, drawn by one shader on a Color Rect. No picture file sits behind it. Every piece is a rule, and each dial changes one rule. We start with the smallest rule.

*Picture.* Act title 'Inside or Outside' (serif 40) top-left of the stage. A real Godot render of the finished crosshair in a SQUARE framed window on the cream stage; a script moves the six dials one after another, each out to 1.0 and back to its default (dot size, ring distance, ring width, then a pause at the defaults, then arm gap, arm length, arm width). At the top-left of the window a readout 'no picture file' lands as the pause begins; under the window a one-line caption defines the node the shader paints: 'Color Rect: a flat rectangle the shader paints'.

*Motion.* Each dial moves in turn and the crosshair reshapes with it, so the shape is plainly made by rules and not by a picture; the pause lands on the words 'no picture file'.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a crosshair with six dial icons

*Capture to record.* C01: lab-shaders/17-crosshair.gdshader, a ColorRect on a square canvas, Forward+, 30 fps, `--length` = the measured audio of B01 (about 13 s). Keyframes as fractions of the clip, the dials in file order: hold the defaults to 4 %; dot_size, ring_distance, ring_width one after another from 4 % to 44 % (13.3 % each: 4.4 % up to 1.0, 4.4 % hold, 4.4 % back to its default); hold the defaults from 44 % to 56 % (the 50 % frame is inside this hold; the voice says 'No picture file sits behind it'); arm_gap 56 to 67 % (up to 59.5, hold to 63.5, back to 67), arm_length 67 to 78 % (up to 70.5, hold to 74.5, back to 78), arm_width 78 to 96 % (up to 83, hold at 1.0 to 91 so the 85 % frame is a hold, back to 96); hold 96 % to 100 %. Scripted.

### B02 · 39 words · ~13 s

> Here is the catch. The fragment function runs once for every pixel, and each run is handed its own pixel's address. So it does not draw a circle. It answers a question about itself: am I inside the circle?

*Picture.* A 13-by-13 grid of outline cells centred on the stage (the pixel grid), the label 'fragment() · once per pixel' above it. One cell near the middle gets a terracotta ring and a small tag 'my address'; the tag then changes to 'inside?'. Then every cell answers at once: cells within five cells of the middle fill teal ('yes'), the rest stay empty ('no'), and a circle with a stepped edge appears out of the answers. Caption: 'yes: on · no: off'.

*Motion.* One cell is handed its own address and asks 'inside?', then every cell answers yes or no at the same instant and a circle appears out of the answers.

*Lane.* manim · `B02_AskEveryPixel` · runner-up: ShaderLab with the circle capture

### B03 · 39 words · ~13 s

> To answer, a pixel needs two facts: its own address, U V, and where the center is. The center is at zero point five, zero point five. Our pixel sits at zero point six two, zero point six six.

*Picture.* A square (the UV square) on the cream stage with an 'across · 0 to 1' axis along the top and a 'down · 0 to 1' axis down the left side, the second axis pointing DOWN. A terracotta cross at the middle labelled 'center · 0.5, 0.5'. A teal dot drops in to the lower right of the center, labelled 'this pixel · 0.62, 0.66'.

*Motion.* The center marker appears, then the pixel's dot drops onto the square and its address label counts up to 0.62, 0.66.

*Lane.* manim · `B03_AddressAndCenter` · runner-up: ShaderLab with a UV picture

### B04 · 36 words · ~12 s

> Work out its distance by hand. It is zero point one two to the right of the center, and zero point one six below. Square both, add them, take the square root: exactly zero point two.

*Picture.* The square zooms to the center and the pixel; a caption defines the word: 'distance: how far apart two points are'. A right triangle is drawn between them: the horizontal leg labelled 0.12, the vertical leg labelled 0.16, the long side between center and pixel. Beside it the arithmetic types in as MathTex, line by line: 0.12² + 0.16², then = 0.0144 + 0.0256 = 0.04, then √0.04, then = 0.2. The long side takes the label 'distance 0.2' and a terracotta ring.

*Motion.* The two legs draw in, the arithmetic lands line by line, and the long side takes its label.

*Lane.* manim · `B04_ByHand` · runner-up: LectureEvidenceTable of the numbers

### B05 · 39 words · ~13 s

> In a shader, that whole calculation is one function: distance. Give it the pixel's address and the center. Feed the answer into the color's alpha, how visible it is, and the middle fades out while the edges fill in.

*Picture.* Code card at left (the six-line shader, blank line and braces included; the distance line, then the color line, highlighted in turn); at right a real Godot window with the radial picture: nothing visible in the middle, more teal toward the edges. A label on the distance line glosses vec2(0.5) as the center; a label on the color line defines the new word: 'alpha: how visible a pixel is: 0 invisible, 1 solid'. A ring on the pixel worked by hand (0.62, 0.66) with the readout 'd = 0.2', and 'd = 0.7' near a corner; a thin 0 to 0.7 strip under the window with a marker.

*Motion.* The highlight moves from the distance line to the color line while a marker runs up the strip as the picture fills in toward the edges.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: lab-shaders/01-distance.gdshader, still on a square canvas, Forward+ (probes: (0.5, 0.2) reads 0.7059, 0.7765, 0.7255; corner reads 0.5098, 0.698, 0.6353; the middle is the stage color).

### B06 · 38 words · ~13 s

> Pick a radius, say zero point three. A pixel is inside when its distance is no more than the radius. Along the middle row, the distance dips to zero at the center. Everything under the line is inside.

*Picture.* A plot on the cream stage: the x axis 'across the shape' from 0 to 1, the y axis 'distance from the middle' from 0 to 0.5. A V-shaped teal curve (0.5 at both ends, 0 at x = 0.5). A horizontal terracotta line at 0.3 labelled 'radius 0.3'. A grey dot starts on the V at the left end, above the line; it then rides the V to the right, turning teal under the line, and the stretch of the x axis where the V lies under the line (x from 0.2 to 0.8) lights up and is labelled 'inside'.

*Motion.* The V draws in, the radius line slides down to 0.3, a dot rides the V and turns teal under the line, and the stretch of the axis beneath it lights up as 'inside'.

*Lane.* manim · `B06_BelowTheLine` · runner-up: ShaderLab with a ramp strip

### B07 · 39 words · ~13 s

> To turn that into a number, use step. Give it an edge and a value. It returns zero while the value is below the edge, and one once the value reaches it. A switch that flips at the edge.

*Picture.* A small plot: the x axis 'value' from 0 to 0.6, the y axis 'output' from 0 to 1. A vertical terracotta line at 0.3 labelled 'edge'. A dot labelled 'value' starts left of the edge with a readout beside it. The step curve draws in two stretches: output 0 left of the edge, then output 1 from the edge on, labelled 'step(edge, x)'. The dot slides across the edge and the readout flips from 0 to 1. Caption (the glossary's wording): '0 below the edge, 1 from the edge up'.

*Motion.* A dot slides along the axis and the output jumps from 0 to 1 at the edge.

*Lane.* manim · `B07_StepJump` · runner-up: LectureEvidenceTable of three inputs and their outputs

### B08 · 40 words · ~14 s

> Mind the order. With the radius first, step asks: has the distance reached the radius? Inside the circle, no: zero. Outside, yes: one. Swap them, and step asks: has the radius reached the distance? Inside, yes: one. That's our circle.

*Picture.* A row of 25 pixel cells with centres at x = 0.02, 0.06, ... 0.98 (cells 5 to 19, the ones within 0.3 of the middle, are inside; no cell lies exactly on 0.3) with the V profile above it and the radius line. Below, a row of 0 and 1 values. First the label 'step(0.3, d)' and the small question 'd ≥ radius?': inside cells read 0 (empty), outside cells read 1 (teal), a hole. Then the two inputs trade places in the label to 'step(d, 0.3)', the question becomes 'radius ≥ d?' and the row flips: inside cells read 1 (teal), outside cells 0 (empty). Cells are numbered from 0. A terracotta ring marks cell 17, a pixel at distance 0.2 like ours (our own pixel is off this row), throughout. At the end the teal stretch is labelled 'the circle'.

*Motion.* The two inputs trade places and the row of ones and zeros flips inside out.

*Lane.* manim · `B08_StepFlip` · runner-up: ShaderLab with a capture of the hole

### B09 · 39 words · ~13 s

> Put it together. Our pixel: distance zero point two, radius zero point three, so step says one: inside. A pixel at distance zero point four says zero: outside. Those ones and zeros are a mask: how much to show.

*Picture.* Code card at left (the seven-line circle shader; the distance, step and color lines highlighted in turn); at right a real Godot window with a teal circle (radius 0.3) on the stage. A ring on our pixel (0.62, 0.66, inside) with the readout 'step: 1', then a ring on a pixel at distance 0.4 (0.5, 0.9, outside) with 'step: 0'; the caption defines the new word in the glossary's wording: 'mask: a number from 0 to 1 per pixel saying how much of something to show'.

*Motion.* The highlight steps from the distance line to the step line to the color line while one ring visits our pixel (step says 1) and then a pixel outside (step says 0).

*Lane.* capture · `ShaderLab` · runner-up: manim circle with the per-pixel numbers

*Capture to record.* C03: lab-shaders/02-circle.gdshader, still on a square canvas, Forward+ (probes: middle, (0.5, 0.25) and our pixel (0.62, 0.66) teal 0.3686, 0.6392, 0.5686; (0.5, 0.15), (0.5, 0.9) at distance 0.4, and the corner stage 0.851, 0.8353, 0.7922).

### B10 · 36 words · ~12 s

> Make the radius a uniform and the circle gets a dial. The shader reads it but never changes it. Turn the dial and the circle grows. What follows the colon asks the editor for a slider.

*Picture.* Code card at left (the uniform line, then the line that reads it, then the uniform line again, labelled with what this hint does); at right a real Godot window where the circle shrinks to radius 0.1 and then grows to 0.45 as a script moves the radius; the value reads out at the top-left of the window. A caption under the window defines the new word in the glossary's wording: 'hint: the word after a colon that tells Godot how to treat a uniform'.

*Motion.* The circle shrinks and then grows as the radius value changes, and ends large.

*Lane.* capture · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction of the Inspector)

*Capture to record.* C04: lab-shaders/03-circle-slider.gdshader, 30 fps, `--length` = the measured audio of B10 (about 12 s), Forward+. `radius` as fractions of the clip: radius: default 0.3 held to 11 %, down to 0.1 by 29 %, hold at 0.1 to 56 %, up to 0.45 by 76 %, hold to 100 %; the voice says 'Turn the dial and the circle grows' as it rises. The 50 % frame is inside the hold at 0.1 and the 85 % frame in the final hold. Scripted. Harness: `--animate radius:0.00:0.3,0.11:0.3,0.29:0.1,0.56:0.1,0.76:0.45,1.00:0.45`.

## Act II: Rings and Cutouts

### B11 · 37 words · ~13 s

> A ring is a big circle with a smaller circle taken out. Draw the big mask, draw the small mask, and subtract. Where both say one, one minus one leaves zero. Only the strip between them survives.

*Picture.* Act title 'Rings and Cutouts' (serif 40) top-left. A big teal disc labelled 'outer mask'. A smaller teal disc labelled 'inner mask' hovers above it with a minus sign between them. The small disc drops onto the big disc's center and cuts: the middle turns empty (the stage color), leaving a ring labelled 'ring'. Two number tags, set beside the shapes on leader lines and never on a fill: '1 − 1 = 0' by the hole and '1 − 0 = 1' by the band.

*Motion.* The small disc drops into the big one and the middle empties, leaving a ring.

*Lane.* manim · `B11_SubtractMasks` · runner-up: ShaderLab with the ring capture

### B12 · 32 words · ~11 s

> In code, that is two steps and a minus. The outer circle has radius zero point three five, the inner one zero point three. Their difference is a ring, five hundredths wide.

*Picture.* Code card at left (the ring shader; the outer line, the inner line and the subtraction highlighted in turn); at right a real Godot window with a teal ring (outer radius 0.35, inner 0.3) on the stage. Readouts 'outer 0.35' above the ring, 'inner 0.3' in the hole, 'width 0.05' below; one ring marks the top of the band.

*Motion.* The highlight moves line by line and the three readouts land on the ring as each number is named.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C05: lab-shaders/04-ring.gdshader, still on a square canvas, Forward+ (probes: middle = stage; (0.5, 0.18) teal; (0.5, 0.13) stage).

### B13 · 37 words · ~13 s

> Check three pixels by hand. At distance zero point two, both circles say one, so the ring is zero. At zero point three three, only the outer circle says one. At zero point four five, neither does.

*Picture.* A four-column table, one row per pixel (distance 0.20, 0.33, 0.45), each row revealed and ringed as the voice reaches it; the last column is the ring mask.

*Motion.* The ring steps down the three rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: a row of cells with the numbers above them

### B14 · 38 words · ~13 s

> Now overlap two circles and add their masks. Where they overlap, both say one, so the sum is two. In a default project the screen cannot tell: an alpha of two looks exactly like one. The mistake hides.

*Picture.* Code card at left (two circle masks and their sum); at right a real Godot window with two overlapping teal circles that read as one solid shape. One ring marks the overlap lens; readouts 'sum = 2' inside it and 'looks like 1' at the top-left of the window.

*Motion.* The ring settles on the overlap and the readouts say two, then 'looks like 1'.

*Lane.* capture · `ShaderLab` · runner-up: manim: two circles with number labels

*Capture to record.* C06: lab-shaders/05-overlap-sum.gdshader, still on a square canvas, Forward+ (probes: middle and (0.3, 0.5) teal; (0.9, 0.5) stage).

### B15 · 35 words · ~12 s

> Cut a small hole in the middle of the overlap by subtracting a third mask. The hole should appear. It does not. One plus one minus one is still one, so the hole is filled.

*Picture.* Code card at left (the same two circles, a third mask for a hole, and a + b - hole); at right a real Godot window: two overlapping circles, solid, with NO hole. One ring marks the spot in the middle where the hole should be; readout 'hole: missing' at the top-left of the window.

*Motion.* The ring lands on the middle of the solid shape, exactly where the hole was supposed to be.

*Lane.* capture · `ShaderLab` · runner-up: manim: three masks and their sum

*Capture to record.* C07: lab-shaders/06-overlap-hole-bug.gdshader, still on a square canvas, Forward+ (probe: the middle (0.5, 0.5) is TEAL: the hole is absent).

### B16 · 32 words · ~11 s

> The same pixels, in numbers. Inside one circle: one. In the overlap: two. In the hole: two minus one, which is one, when we wanted zero. The hidden two ate the cutout.

*Picture.* A three-column table, one row per kind of pixel (one circle, the overlap, the hole), each row revealed and ringed as the voice reaches it; the third column reads 1, 2, 1 and the hole row (the whole row is ringed: the table rings rows, not cells) shows 1 where 0 is wanted. No fix is in the table: min arrives in the next beat.

*Motion.* The ring steps down the rows and lands on the hole row, where the third column reads 1 and 0 was wanted.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: a number line from -1 to 2

### B17 · 37 words · ~13 s

> The fix is to cap the sum at one with min before subtracting. Min of two and one is one, so the overlap counts once, and the hole takes it down to zero. Now the hole appears.

*Picture.* Code card at left (the same shader; the mask line now reads min(a + b, 1.0) - hole, highlighted); at right a real Godot window: the same two circles, now WITH the hole in the middle, ringed; readout 'hole: there' at the top-left of the window.

*Motion.* The min line lights up and the ring settles on the hole that now exists.

*Lane.* capture · `ShaderLab` · runner-up: manim: a number line with the cap at one

*Capture to record.* C08: lab-shaders/07-overlap-hole-fixed.gdshader, still on a square canvas, Forward+ (probe: the middle (0.5, 0.5) is STAGE: the hole is there).

### B18 · 40 words · ~14 s

> Subtraction has a mirror-image bug. Cut a bite from the disc, reaching past its edge. There the disc says zero, the bite says one: minus one. Add a spot there: minus one plus one is zero, so it never shows.

*Picture.* Code card at left (a disc, a bite cut from it, a small spot, and disc - bite + spot); at right a real Godot window: a teal disc with a round bite out of its right side and NOTHING in the stretch of the bite that reaches past the disc's edge. One ring marks that stretch, then a smaller ring marks where the spot should be. A readout just below the ring (at the foot of the bite, under the spot's place) reads 'mask −1' and then 'mask 0'; 'spot: missing' lands at the top-left of the window.

*Motion.* The ring marks the stretch of the bite past the disc, the readout there says minus one, and then the spot's place stays empty.

*Lane.* capture · `ShaderLab` · runner-up: manim: a number line with minus one marked

*Capture to record.* C09: lab-shaders/08-negative-eats-dot.gdshader, still on a square canvas, Forward+ (probes: (0.88, 0.5), where the spot should be, reads the STAGE color 0.851, 0.8353, 0.7922; (0.7, 0.5) stage; (0.4, 0.5) teal; (0.9, 0.35) stage).

### B19 · 40 words · ~14 s

> The fix is max, min's mirror: it keeps the larger number. Max of minus one and zero is zero, and then the spot adds one. The rule for both bugs: after adding, cap at one; after subtracting, floor at zero.

*Picture.* Code card at left (the same shader; the mask line now reads max(disc - bite, 0.0) + spot, highlighted); at right a real Godot window with the same disc and bite and the spot now THERE, ringed. A readout below the spot (so it does not cover it) reads 'mask 0' (after the max) and then 'mask 1' (after the spot adds one); 'spot: there' lands at the top-left; a caption states the rule: 'after adding, cap at one · after subtracting, floor at zero'.

*Motion.* The max line lights up, the readout goes from 0 to 1 and the ring settles on the spot that now shows.

*Lane.* capture · `ShaderLab` · runner-up: manim: a strip from -1 to 2 with the 0 to 1 zone shaded

*Capture to record.* C10: lab-shaders/09-negative-fixed.gdshader, still on a square canvas, Forward+ (probes: (0.88, 0.5) reads TEAL 0.3686, 0.6392, 0.5686: the spot is there; (0.7, 0.5) stage; (0.4, 0.5) teal; (0.9, 0.35) stage).

## Act III: Lines and Crosses

### B20 · 40 words · ~14 s

> A circle measures distance to a point. A band measures it to a line. Take the vertical line down the middle. Subtract a half from the pixel's horizontal address, and you get how far right of the line it sits.

*Picture.* Act title 'Lines and Crosses' (serif 40) top-left. The UV square with a grey dot at its center ringed by a thin circle (a circle measures distance to a point); its top axis is tagged 'UV.x · horizontal address' and its left axis 'UV.y · vertical address', which defines the code notation where it is first used. The circle fades and the vertical middle line draws in grey; a caption defines the new word in the glossary's wording, set as two lines so no text object runs past twelve words: 'band: the strip of pixels near a line or an edge,' / 'as wide as the thickness or the softness'. A teal dot at (0.7, 0.4); a horizontal terracotta segment runs from the dot to the line, labelled 'UV.x − 0.5'. When the voice says how far right it sits, the length label 0.2 appears; the dot then moves to two other places on the right and the segment and its length follow.

*Motion.* The circle gives way to a line, and the dot moves while the horizontal segment to the middle line stretches and shrinks with a live length label.

*Lane.* manim · `B20_DistanceToALine` · runner-up: ShaderLab with the distance picture

### B21 · 27 words · ~9 s

> On the left that number is negative. The function abs drops the minus sign: it folds the left onto the right, so one formula measures both sides.

*Picture.* A horizontal number line from -0.5 to 0.5 labelled 'UV.x − 0.5' with a vertical tick at 0. A dot at -0.3 reads -0.3. A caption (the glossary's wording) 'abs: drops the minus sign: -0.3 becomes 0.3'. The left half of the line folds over the zero tick onto the right half (a mirror), the dot lands at +0.3 and reads 0.3. A V-shaped plot of the folded values sits under the line.

*Motion.* The left half folds over onto the right and the dot lands on the positive side.

*Lane.* manim · `B21_AbsFold` · runner-up: LectureEvidenceTable of before and after values

### B22 · 25 words · ~8 s

> Compare that distance with half the band's width, and step gives a vertical band. Same recipe as the circle: measure, compare, get one or zero.

*Picture.* Code card at left (across, band, color); at right a real Godot window with a vertical teal band down the middle, 0.1 wide. Readout 'half-width 0.05' at the top-left of the window as the voice says 'half the band's width'.

*Motion.* The highlight moves from across to band to color as each is named, and the band is already on screen.

*Lane.* capture · `ShaderLab` · runner-up: manim: the band drawn over the V plot

*Capture to record.* C11: lab-shaders/10-band.gdshader, still on a square canvas, Forward+ (probes: (0.5, 0.1) and the middle teal; (0.7, 0.5) stage).

### B23 · 38 words · ~13 s

> A cross is every pixel in either band. Take the larger of the two masks, with max: for ones and zeros it does what add-then-cap did, in one step. Adding alone would put a two in the middle.

*Picture.* Code card at left (the two band masks and the max); at right a real Godot window with a teal cross whose arms run to the edges. A readout on the middle reads 'max gives 1'; later, in the same place, it becomes 'adding gives 2'.

*Motion.* The highlight lands on the max line, then the readout on the middle shows what max gives and then what a sum would give.

*Lane.* capture · `ShaderLab` · runner-up: manim: the cross assembled from two bands

*Capture to record.* C12: lab-shaders/11-cross.gdshader, still on a square canvas, Forward+ (probes: middle, (0.5, 0.1), (0.1, 0.5) teal; (0.1, 0.1) stage).

### B24 · 40 words · ~14 s

> So there are three ways to combine masks. For either, take the max. For both, multiply. For a cutout, subtract, then take the max with zero. Max and multiply stay between zero and one. Adding and subtracting can leave it.

*Picture.* Two overlapping circle outlines, a (left) and b (right), in grey with a faint label each. Three captions arrive in turn under the pair, each with the region it names shaded teal: 'either · max(a, b)' (the union), 'both · a × b' (the lens), 'cutout · max(a − b, 0)' (a with b taken out, a crescent). Then a strip from -1 to 2 with the zero-to-one zone shaded: tags 'max' and 'a × b' sit inside the zone; tags 'a + b' and 'a − b' slide out of it, to 2 and to -1.

*Motion.* The same two circles light up three different regions as each combination is named, then two tags stay in the zero-to-one zone and two leave it.

*Lane.* manim · `B24_ThreeWays` · runner-up: LectureEvidenceTable of three formulas

### B25 · 32 words · ~11 s

> To make an arm, ask for two things at once: not too far along the line, and close to it. Two masks, multiplied. Both must be one, so you get a rectangle.

*Picture.* Code card at left (not_too_far, near_line and their product); at right a real Godot window with one tall thin teal rectangle in the middle (0.06 wide, 0.7 tall). One ring settles on it; readout 'both are 1' beside it.

*Motion.* The highlight moves to the product line and the ring settles on the rectangle.

*Lane.* capture · `ShaderLab` · runner-up: manim: two masks multiplying

*Capture to record.* C13: lab-shaders/12-arm-rectangle.gdshader, still on a square canvas, Forward+ (probes: middle and (0.5, 0.25) teal; (0.5, 0.1) and (0.6, 0.5) stage).

### B26 · 37 words · ~13 s

> An arm should start away from the center. Add a third condition: at least this far out. Far enough, not too far, near the line. Because of abs, one formula draws the top arm and the bottom.

*Picture.* Code card at left (far_enough, not_too_far, near_line and their product); at right a real Godot window with two short thin vertical teal bars, above and below the middle, and an empty gap between them. One ring marks the gap (readout 'gap'), then one ring on the top arm and one on the bottom arm.

*Motion.* Each condition lights in turn, the ring settles on the gap, then the same formula is ringed on both arms.

*Lane.* capture · `ShaderLab` · runner-up: manim: the three conditions on a number line

*Capture to record.* C14: lab-shaders/13-arms-gap.gdshader, still on a square canvas, Forward+ (probes: (0.5, 0.3) and (0.5, 0.7) teal; the middle, (0.5, 0.95), (0.3, 0.5) stage).

### B27 · 31 words · ~10 s

> Swap the two addresses for the horizontal pair, then take the max of the two pairs. Four arms around an empty middle. Measure, compare, combine: that is every shape so far.

*Picture.* Code card at left (the vertical pair v, the horizontal pair h, and the max that joins them); at right a real Godot window with four short teal arms around an empty middle. Under the window: 'measure, compare, combine'.

*Motion.* The vertical pair, then the horizontal pair, then the max that joins them, each highlighted as it is named.

*Lane.* capture · `ShaderLab` · runner-up: manim: the arms assembled from two pairs

*Capture to record.* C15: lab-shaders/14-four-arms.gdshader, still on a square canvas, Forward+ (probes: four arms teal at (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7); middle and (0.3, 0.3) stage).

## Act IV: Make It a Tool

### B28 · 35 words · ~12 s

> Every number here is baked in: the gap, the end, the width. A tool needs dials. Turn each number into a uniform with a range, and the editor gives you a slider for each one.

*Picture.* Act title 'Make It a Tool' (serif 40) top-left. At left, the vertical-pair line set as three STACKED calls in monospace on a cream card (the whole line is 55 characters and does not fit beside a panel at size 32): `step(0.1, y) *`, `step(y, 0.35) *`, `step(x, 0.03)`. At right, an empty panel with three labelled slots 'gap', 'end', 'width'. As each number is named it lifts out of its call and lands in its slot as a slider knob on a short track, leaving the name in its place: the calls then read `step(gap, y) *`, `step(y, end) *`, `step(x, width)`. The sliders get end labels '0' and '1' (a range) and the tag 'uniform'; the panel is labelled 'in the editor'.

*Motion.* Each baked-in number lifts out of its call and lands as a slider, leaving its name behind.

*Lane.* manim · `B28_NumbersBecomeDials` · runner-up: LectureCodeTrace

### B29 · 38 words · ~13 s

> A habit worth having: every slider runs from zero to one, whatever it controls. Inside the shader, multiply by the biggest value that makes sense. Then every dial behaves the same way, and you never memorize a range.

*Picture.* Left, under 'three scales': sliders 'radius 0 to 0.5', 'width 0 to 0.05' and 'gap 0 to 0.2', each with different tick labels. They morph into three identical 0 to 1 sliders with the same ticks; to the right of each a multiplier tag ('× 0.5', '× 0.05', '× 0.2') and a small teal shape showing the real size at slider = 1. At the end the three knobs travel from 0 to 1 together.

*Motion.* Three differently scaled sliders turn into three identical zero-to-one sliders with the real size beside each, and the knobs move as one.

*Lane.* manim · `B29_ZeroToOneDials` · runner-up: ShaderLab with the scaled crosshair

### B30 · 32 words · ~11 s

> Next, give each shape a name. A function can return a mask. This one takes an address, a radius and a width, and returns the ring. The fragment function only calls it.

*Picture.* Code card at left (make_ring and the fragment function that calls it); at right a real Godot window with the teal ring. The function's first line carries the definition of the word 'function'; the signature, the body and the call line are highlighted in turn; one ring marks the top of the band at the call.

*Motion.* The highlight moves from the function's name to its inputs, its body and the call that uses it.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C16: lab-shaders/15-ring-tool.gdshader, still on a square canvas, Forward+ (probes: middle stage; (0.5, 0.18) teal).

### B31 · 40 words · ~14 s

> One catch. Built-in values like U V work in the engine's own functions, but not in yours. A few, like time, are global and work anywhere. So fragment hands U V in as an input, under a name you choose.

*Picture.* A large box labelled 'fragment()' holding three values in monospace: UV, COLOR, TIME. To its right a smaller box labelled 'make_ring()' inside a thick wall. A caption in the glossary's wording, set as two lines beside the first box and never on a fill ('built-in: a value the engine hands' / 'to a function, or collects from it'). UV tries to travel into the second box and bounces off the wall; TIME slips through, tagged 'global: works anywhere'; then a small teal packet (its label 'uv', the input's own name, set beside it on a leader line) travels from fragment() through an input slot in the wall into make_ring().

*Motion.* UV bounces off the wall of the second function, TIME slips through, and a packet named uv carries the address in through the input slot.

*Lane.* manim · `B31_WhoCanSeeUV` · runner-up: LectureCodeTrace

### B32 · 37 words · ~13 s

> Use U V directly inside your own function and Godot refuses to compile. The message names the word it does not recognize: unknown identifier, U V. The version from a moment ago passes it in, and compiles.

*Picture.* A cream code card with the eight real lines of the failing shader (UV used directly inside make_ring); focus lands on line 3, the line the engine names, and the engine's own message sits under the card.

*Motion.* Focus lands on the line Godot names and stays there, then jumps to the call that passes nothing in.

*Lane.* remotion · `LectureCodeTrace` · runner-up: CCPlainShell with the engine's log

### B33 · 40 words · ~14 s

> One honest limit: these shapes assume a square. On a wide rectangle, U V still runs from zero to one both ways, so a circle becomes an oval. We measured it: three hundred eighty-four pixels wide, two hundred sixteen tall.

*Picture.* Left: a square with a teal circle inside it. Right: the same shape stretched into a 16:9 rectangle; the circle stretches into an oval with it. Corner labels (0, 0) and (1, 1) stay at the same corners on both. A label 'oval' lands beside the stretched circle. Credit, small and grey, set as two lines: 'Godot 4.7.2 · Forward+ · 640 × 360 view' / 'measured 384 × 216 px'.

*Motion.* The square stretches wide and the circle stretches into an oval with it.

*Lane.* manim · `B33_SquareLimit` · runner-up: ShaderLab with a capture of the oval

### B34 · 36 words · ~12 s

> And the edge is hard. Every pixel is fully in or fully out, so the circle's edge is a staircase of pixels. The whole picture has exactly two colors. A softer edge needs a different tool.

*Picture.* A zoomed pixel grid (14 columns by 9 rows) showing a quarter of a circle's edge, a small dot at the CENTRE of every cell. A cell is teal when its centre dot lies inside the ideal circle and empty when it lies outside (the pixel's centre decides, as in the shader). A smooth terracotta arc, the ideal circle, is drawn over the grid and the cells step along it like a staircase; a cell that the arc cuts through is teal or empty by its centre alone. Caption 'in or out · nothing between'. Credit, small and grey, set as two lines: 'Godot 4.7.2 · Forward+ · 480 × 480 render' / 'the whole picture has 2 colors'.

*Motion.* The cells fill in or out by their centres, then the ideal arc draws over them and the cells step along it like a staircase.

*Lane.* manim · `B34_Staircase` · runner-up: ShaderLab with a crop of the real render

## Act V: The Crosshair

### B35 · 32 words · ~11 s

> Now the crosshair. Six uniforms: dot size, ring distance, ring width, arm gap, arm length and arm width. Each runs from zero to one, with a default that draws a sensible crosshair.

*Picture.* Act title 'The Crosshair' (serif 40) top-left. Code card at left (the shader type line and the six uniform lines, lines 1 to 8 of the file; each uniform highlighted as its name is spoken; then all six with a label on the range); at right a real Godot window with the finished crosshair at its defaults.

*Motion.* The highlight walks down the six uniform lines while the finished crosshair sits at its defaults.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C17: lab-shaders/17-crosshair.gdshader, still on a square canvas, Forward+, defaults (probes: middle and (0.35, 0.5) teal; (0.5, 0.2) stage). Also used by B38.

### B36 · 31 words · ~10 s

> Three small functions return the three masks. The first two: the dot is the circle from before, and the ring is the outer circle minus the inner. Same code, new names.

*Picture.* Code card at left (make_dot and make_ring, lines 10 to 17 of the file); at right a real Godot window with the crosshair's dot and ring only (arm length dialled to 0, labelled). One ring lands on the dot when make_dot is highlighted, then on the ring top when make_ring is.

*Motion.* The ring marker lands on the dot, then on the ring, as each function is highlighted.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C18: lab-shaders/17-crosshair.gdshader, still on a square canvas, Forward+, arm_length = 0 (probes: the dot and the ring drawn, no arms).

### B37 · 35 words · ~12 s

> The arms function is the four-arm rule from before. Gap, length and width come in; gap plus length is the end. Abs folds each side, and max joins the vertical pair with the horizontal pair.

*Picture.* Code card at left (make_arms, lines 19 to 26 of the file); at right a real Godot window with the four arms alone (dot size and ring width dialled to 0, labelled). The vertical and horizontal pair lines, the signature, the end line (gap plus length), the two abs lines and the final max are highlighted in turn.

*Motion.* The highlight moves from the two pair lines to the function's inputs to the folding lines to the max that joins the pairs.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C19: lab-shaders/17-crosshair.gdshader, still on a square canvas, Forward+, dot_size = 0 and ring_width = 0 (probes: four arms drawn; the dot gone).

### B38 · 32 words · ~11 s

> The fragment function scales each slider to a real size, then joins the three masks with max. Where the ring and arms cross, nothing doubles. The mask goes straight into the alpha.

*Picture.* Code card at left (the fragment function, lines 28 to 39 of the file); at right a real Godot window with the finished crosshair at its defaults. The six scaling lines, the three mask lines and the color line are highlighted in turn; where an arm crosses the ring, one ring and the readout 'still 1' land.

*Motion.* The highlight moves from the six scaling lines to the three max lines, a ring lands where an arm crosses the ring, then the color line lights.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C17 again (the same defaults still, no new capture).

### B39 · 31 words · ~10 s

> Here it is over two different backdrops. Wherever the mask is zero, none of the shape is drawn, so whatever is behind shows through. That is what a mask is for.

*Picture.* A real Godot window: the finished crosshair over two flat backdrops, cream on the left half and sand on the right half. One ring marks a see-through patch on the left (readout 'mask = 0' at the top-left), then one on the right (readout 'see-through' at the top-right).

*Motion.* The ring lands on a patch of each backdrop showing through, one after the other.

*Lane.* capture · `ShaderLab` · runner-up: manim: a layer diagram

*Capture to record.* C20: a **scene script** (`--scene`, as the harness spec describes) builds two ColorRect backdrops (left half #FAF9F5, right half #C9B79C) and the crosshair ColorRect on top at the defaults; still, Forward+. Copy the structure of evidence/planning-checks/verify-a.gd, check 2: a pixel outside the shape reads exactly the backdrop color on each side.

### B40 · 31 words · ~10 s

> Now the dials, one at a time. Dot size grows the dot. Ring distance pushes the ring outward while the arms stay put. Each dial changes one number in one rule.

*Picture.* Code card at left (lines 1 to 8: the six uniforms; the one being moved is highlighted); at right a real Godot window: dot size drops to 0 and grows to 1, then ring distance drops to 0 and grows to 1 while the arms stay put. A readout names the dial and its value at each hold, at the top-left of the window.

*Motion.* The dot grows from nothing; then the ring moves out from the middle while the arms stay put.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dial icon driving a drawn crosshair

*Capture to record.* C21: 17-crosshair at defaults, 30 fps, `--length` = the measured audio of B40 (about 10.5 s). Two dials back to back, each from 0 to 1 and ending on 1 (the voice says 'grows' and 'pushes the ring outward'); the first dial stays at 1.0 while the second moves. dot_size: default 0.5 held to 9 %, down to 0 by 15 %, hold at 0 to 19 %, up to 1 by 37 %, hold to 100 %; then ring_distance: default 0.55 held to 38 %, down to 0 by 44 %, hold at 0 to 56 %, up to 1 by 74 %, hold to 100 %. The 50 % frame is inside ring_distance's hold at 0 (with dot_size at 1.0) and the 85 % frame in the final hold (both at 1.0). Scripted. Harness: `--animate dot_size:0.00:0.5,0.09:0.5,0.15:0,0.19:0,0.37:1,1.00:1` and `--animate ring_distance:0.00:0.55,0.38:0.55,0.44:0,0.56:0,0.74:1,1.00:1`.

### B41 · 28 words · ~10 s

> Ring width thickens the ring from nothing to a band. Arm length stretches the arms until they cross the ring and run on. Nothing doubles where they cross.

*Picture.* Code card at left (lines 1 to 8; the dial being moved is highlighted); at right a real Godot window: ring width drops to nothing and grows to a thick band, then arm length drops to 0 and stretches the arms until they cross the ring and run on past it, ending on 1 (the ring stays thick). Readouts name the dial and value at each hold.

*Motion.* The ring thickens from nothing to a band; the arms lengthen across the ring and the picture ends with nothing doubled where they cross.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dial icon driving a drawn crosshair

*Capture to record.* C22: 17-crosshair at defaults, 30 fps, `--length` = the measured audio of B41 (about 9.5 s), the same shape as C21 (the first dial stays at 1.0 while the second moves). ring_width: default 0.3 held to 2 %, down to 0 by 8 %, hold at 0 to 12 %, up to 1 by 30 %, hold to 100 %; then arm_length: default 0.6 held to 38 %, down to 0 by 44 %, hold at 0 to 56 %, up to 1 by 74 %, hold to 100 %. The arms cross the ring at about 0.5 on the dial, near 65 % of the beat; the voice says 'Nothing doubles where they cross' over the final hold. The 50 % frame is inside arm_length's hold at 0 (with ring_width at 1.0) and the 85 % frame in the final hold (both at 1.0). Scripted. Harness: `--animate ring_width:0.00:0.3,0.02:0.3,0.08:0,0.12:0,0.30:1,1.00:1` and `--animate arm_length:0.00:0.6,0.38:0.6,0.44:0,0.56:0,0.74:1,1.00:1`.

### B42 · 24 words · ~8 s

> Arm width thickens the arms. Arm gap opens the middle, from arms that run into the dot to arms that start far from it.

*Picture.* Code card at left (lines 1 to 8; the dial being moved is highlighted); at right a real Godot window: arm width drops to 0 and thickens the arms to 1, then arm gap drops to 0 (arms that run into the dot) and opens the middle to 1 (arms that start far from it). Readouts name the dial and value.

*Motion.* The arms thicken from nothing; then they slide away from the middle, opening a gap.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dial icon driving a drawn crosshair

*Capture to record.* C23: 17-crosshair at defaults, 30 fps, `--length` = the measured audio of B42 (about 8 s), the same shape as C21 (the first dial stays at 1.0 while the second moves). arm_width: default 0.4 held to 2 %, down to 0 by 6 %, hold at 0 to 10 %, up to 1 by 22 %, hold to 100 %; then arm_gap: default 0.35 held to 38 %, down to 0 by 44 %, hold at 0 to 68 %, up to 1 by 82 %, hold to 100 %. The voice says 'arms that run into the dot' over the hold at 0 and 'arms that start far from it' as the gap opens. The 50 % frame is inside arm_gap's hold at 0 (with arm_width at 1.0) and the 85 % frame in the final hold (both at 1.0). Scripted. Harness: `--animate arm_width:0.00:0.4,0.02:0.4,0.06:0,0.10:0,0.22:1,1.00:1` and `--animate arm_gap:0.00:0.35,0.38:0.35,0.44:0,0.68:0,0.82:1,1.00:1`.

### B43 · 38 words · ~13 s

> Predict first. Arm length at zero: what is left? The dot and the ring. Ring width at zero? The dot and the arms. Push any dial to either end and nothing breaks, because every piece is a mask.

*Picture.* A real Godot window, result only. The crosshair at its defaults ('predict first'); the readout 'arm length 0?' asks, then the state jumps to arm length 0 (dot and ring) as the answer is voiced; the picture goes back to the defaults while 'ring width 0?' asks, then jumps to ring width 0 (dot and arms) as that answer is voiced; then every dial at 1 (everything at its largest). Readouts sit at the top-left of the window and name each state.

*Motion.* The crosshair jumps between states and the readout names each one, so the viewer can check the prediction.

*Lane.* capture · `ShaderLab` · runner-up: manim: four small crosshairs in a row

*Capture to record.* C24: 17-crosshair, 30 fps, `--length` = the measured audio of B43 (about 13 s), STEPPED (`--steps`: instant changes, no ramps), as fractions of the clip: defaults to 27 %; arm_length = 0 from 27 % to 38 % (the voice says 'The dot and the ring'); the defaults again from 38 % to 50 % while 'Ring width at zero?' is asked (the 50 % frame is a settled state); ring_width = 0 from 50 % to 61 % ('The dot and the arms'); all six dials = 1.0 from 61 % to the end (the 85 % frame). Scripted. Harness: `--steps dot_size:0:0.5,0.61:1 --steps ring_distance:0:0.55,0.61:1 --steps ring_width:0:0.3,0.5:0,0.61:1 --steps arm_gap:0:0.35,0.61:1 --steps arm_length:0:0.6,0.27:0,0.38:0.6,0.61:1 --steps arm_width:0:0.4,0.61:1`.

### B44 · 24 words · ~8 s

> In the Godot editor, the six uniforms appear as six sliders in the Inspector. A designer can tune the crosshair without opening the code.

*Picture.* Three real frames of the Godot editor's Inspector, cropped to the ShaderMaterial's 'Shader Parameters' group (no thumbnail, no viewport): the six uniforms as six sliders at their defaults; then dot size at 1.0; then ring distance at 0.2 (dot size stays 1.0). Slow cross-dissolves between the frames; one terracotta ring on the group, then on the slider being named.

*Motion.* The slider knobs step through three real states.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction)

*Capture to record.* E1: three static editor frames of a scratch project via Movie Maker (method proven 2026-10-09; driver for this exact view proven 2026-10-13 in evidence/planning-checks/editor-driver/): ColorRect 480 x 480 with a ShaderMaterial on lab-shaders/17-crosshair.gdshader, the values saved in the scene file (state 1: defaults; state 2: dot_size 1.0; state 3: dot_size 1.0 and ring_distance 0.2, as in the proven frame); Inspector scrolled to the material's six uniforms, then CROPPED to the 'Shader Parameters' group. The clicks themselves are not shown, only the resulting states. Output `editor-inspector.mp4`: the three stills joined by two 0.4 s cross-dissolves (for example ffmpeg `xfade`), the first from 56 % and the second from 72 % of the beat. At the default dock width the label 'Ring Distance' loses its last letter (see `png/editor-inspector-check-2d.png`): widen the Inspector dock by hand in the scratch project's layout (editor-driver/README.md) or crop so the cut label is not the one being named. Recording the editor at 3840 by 2160 is a recommendation for a sharp crop, not something the planning check did (it ran at 1920 by 1080).

## Closing

### BVDT · recap · 92 words · ~31 s

> Let's recap with Claude. A shape is a question each pixel answers: inside is one, outside is zero. Distance from a point, compared with a radius by step, draws a circle. Subtract masks for a ring. After adding, cap at one; after subtracting, floor at zero. Distance from a line, folded with abs, draws a band; max joins masks and multiply intersects them. Put each shape in a function, and give every slider a range of zero to one. A crosshair is a dot, a ring and four arms, joined with max.

*Picture.* The recap card: A shape is a question each pixel answers: inside is one, outside is zero. / Distance from a point, compared with a radius by step, draws a circle. / Subtract masks for a ring. After adding, cap at one; after subtracting, floor at zero. / Distance from a line, folded with abs, draws a band; max joins masks and multiply intersects them. / Put each shape in a function, and give every slider a range of zero to one. / A crosshair is a dot, a ring and four arms, joined with max.

### BHTF · your turn · 101 words · ~34 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a square Color Rect that draws a ring. Use distance from the center and step. Two float uniforms, radius and thickness, each with a hint range from zero to one, scaled inside the shader so the biggest ring still fits the square. Everything outside the ring must be transparent. Then point me to the line that decides inside or outside. Then check two things yourself. With thickness at zero, is anything drawn? And is the ring round on a square Color Rect, and oval on a wide one?

*Prompt shown and read in full:* Write a Godot canvas item shader for a square Color Rect that draws a ring. Use distance from the center and step. Two float uniforms, radius and thickness, each with a hint range from zero to one, scaled inside the shader so the biggest ring still fits the square. Everything outside the ring must be transparent. Then point me to the line that decides inside or outside.

*Two checks:* Check: with thickness at zero, nothing is drawn. · Check: the ring is round on a square, and oval on a wide Color Rect.

### BOUT · outro · 8 words · ~4 s

> Drawing Shapes with Math. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


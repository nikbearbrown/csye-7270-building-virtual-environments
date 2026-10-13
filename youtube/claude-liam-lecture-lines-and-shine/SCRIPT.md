# Script: Lines and Shine

**What this is.** The words Liam will say in *Lines and Shine*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 41 beats, 1579 words, about **9:01** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 21, manim 14.

**If it runs long.** Cut, in this order: Act V (B31 to B35), and with it the last sentence of B14, which promises it; then the center-shift beat (B23); then fold B16 and B17 into one beat (the band, then the tilt). The wide-shape limit (B30) stays unless the film is far over: it is the honest edge of the whole method. The shine itself (B01, B22, B24 to B29) never goes.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | A Line as a Test | 9 | 317 | ~1:48 |
| II | Slope from an Angle | 5 | 180 | ~1:01 |
| III | Distance to the Line | 7 | 255 | ~1:27 |
| IV | Shine | 9 | 325 | ~1:51 |
| V | The Angle-Safe Way | 5 | 182 | ~1:02 |

## Opening

### BOPEN · identity card · 28 words · ~10 s

> Lines and Shine. Learn how a shader draws a line at any angle from one rule, and how to slide that line across a sprite as a shine.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Lines and Shine", and the line "How to draw a line at any angle and make it shine".

### BIDEA · the question · 38 words · ~13 s

> Hallo. This is Liam, in for Bear. Most people think a line needs two points, one at each end. A shader has no pen. It gets one rule, and every pixel asks it: am I on the line?

*Picture.* The hesitant writer types: "A line needs two points." then deletes "two points" and types "one rule".

### BDEFS · terms · 54 words · ~18 s

> Five terms. A pixel is one dot of the picture. U V is a pixel's address on the shape: zero to one across, zero to one down. A uniform is a value your game sets, the same for every pixel. Slope is how steeply a line rises. Alpha is how visible a pixel is.

*Picture.* "Terms In This Lecture": **Pixel** — one dot of the picture on screen; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Uniform** — a value your game sets from outside; every pixel sees the same one; **Slope** — how steeply a line rises: up divided by across; **Alpha** — how visible a pixel is: 0 invisible, 1 solid

## Act I: A Line as a Test

### B01 · 39 words · ~13 s

> This glint is where we are heading. No stripe is drawn anywhere. Every pixel measures how far it sits from a line, and the pixels that are close light up. By the end, you will write that rule yourself.

*Picture.* Act title 'A Line as a Test' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite with a white diagonal glint that slides across it from upper left to lower right, rests for a moment off the sprite, and repeats. Label: 'the finished shine'.

*Motion.* The white band sweeps across the sprite and stays inside its outline.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a stripe crossing a blob

*Capture to record.* C01: Lab blob sprite (teal test sprite, scale to fit), lab-shaders/11-shine-clock.gdshader (TIME-driven, angle 35, thickness 0.1 as in the file); 12 s at 30 fps, Forward+, offline fixed tick; the sweep period is 2 s so the 12 s clip loops seamlessly; no input.

### B02 · 39 words · ~13 s

> From school: a line is y equals m x plus b. The m is the slope, the climb for each step across. The b is its starting height. Make the line pass through the middle, and b is zero.

*Picture.* Axes on the cream stage with a warm-grey line y = m x + b crossing the vertical axis above the origin, a terracotta dot marking b. A right triangle (one step across, m up) rides along the line under the label 'slope m: up per step across'. Then the line slides down until it passes through the origin: the b dot lands on 0 and the label becomes 'y = m x'.

*Motion.* The slope triangle rides along the line, then b shrinks to zero as the line settles through the middle.

*Lane.* manim · `B02_SchoolLine` · runner-up: LectureEvidenceTable listing m and b

### B03 · 35 words · ~12 s

> A pixel's address, U V, has its zero at the top left corner. Double it, subtract one, and the zero lands in the middle. The address now runs from minus one to one, both ways.

*Picture.* A square with corner labels (0, 0) at the top left and (1, 1) at the bottom right and its second axis pointing down (shader_kit uv_square). A terracotta dot sits at the top-left corner. The labels morph to -1, 0 and 1 and the dot glides to the middle; the formula 'p = UV × 2 − 1' appears under the square.

*Motion.* The zero moves from the corner to the middle of the square.

*Lane.* manim · `B03_CenterTheAddress` · runner-up: ShaderLab with the line `vec2 p = UV * 2.0 - 1.0;` over a gradient

### B04 · 30 words · ~10 s

> One more change. Godot counts the address downward, so flip the second number. Now up is up, and a positive slope climbs to the right, the way you learned it.

*Picture.* The centered square with its vertical axis pointing down (+1 at the bottom). A terracotta dot sits in the upper right labelled (0.5, -0.5). The vertical axis flips to point up and the dot's label becomes (0.5, 0.5) while the dot stays where it is on screen; a short warm-grey line y = 0.5 x then draws, climbing to the right, under the label 'p.y = -p.y'.

*Motion.* The vertical axis flips and the dot's second number changes sign while the dot does not move.

*Lane.* manim · `B04_FlipUp` · runner-up: ShaderLab showing the signed map upside down then upright

### B05 · 35 words · ~12 s

> Now turn the line into a question. Move everything to one side: y minus m times x. On the line, the answer is exactly zero. Anywhere else, it is not, and any pixel can check.

*Picture.* Left: the equation 'y = m x'. The 'm x' term travels across the equals sign and the equation becomes 'y − m x = 0', captioned 'the test'. Right: the square with the line m = 0.5 and a terracotta dot riding along it, labelled '0'; then a second dot off the line reads +0.6.

*Motion.* A term crosses the equals sign while a dot rides the line with the value 0 on it.

*Lane.* manim · `B05_TheTest` · runner-up: LectureCodeTrace of the single line y - m * x

### B06 · 39 words · ~13 s

> Try a slope of one half. A point on the line gives zero. Straight above it, plus point six. Straight below, minus point six. The sign tells you the side. The size is the gap, straight up or down.

*Picture.* The test square with the line m = 0.5. Three terracotta dots land at across = 0.4: on the line (label 0), above it (label +0.6) and below it (label -0.6). Warm-grey dashed vertical connectors then run from the two outer dots to the line, labelled 'straight up' and 'straight down', each 0.6 long.

*Motion.* Dots land one at a time with their numbers; dashed verticals then measure the gap straight up and down.

*Lane.* manim · `B06_ThreeDots` · runner-up: ShaderLab with three probe readouts

### B07 · 34 words · ~12 s

> Slide a point along a parallel line, and the answer never changes. Plus point six stays plus point six. So the test gives one number to a whole line of pixels, parallel to ours.

*Picture.* The same square: the line m = 0.5 and a warm-grey dashed parallel line through the 'above' dot. A terracotta dot slides along the parallel line while its label stays '+0.6'. Then three parallel warm-grey lines appear labelled -0.6, 0 and +0.6.

*Motion.* The dot moves along the parallel line and its number does not change.

*Lane.* manim · `B07_Parallel` · runner-up: ShaderLab signed map with a moving probe

### B08 · 40 words · ~14 s

> As a shader, fragment runs once for every pixel of the card. Red rises where the answer is positive, so that side looks warm. Blue rises where it is negative, so it looks cool. Pixels on the line stay grey.

*Picture.* Code card at left (the ten-line shader) whose first two lines carry one-line labels ('shader_type canvas_item: the first line says this shader is for 2D drawing', 'fragment(): runs once for each pixel the shape covers; sets its color'); at right a real Godot window with a square card showing the signed test: warm at the upper left, cool at the lower right, a grey strip between. Three readouts land on the card at the three points from the drawing: +0.6, 0 and −0.6.

*Motion.* Readouts land on the warm, cool and grey regions in the order the voice names them.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: Lab card, lab-shaders/01-signed-test.gdshader, slope 0.5, still PNG (640 x 360 frame, card 288 px centred). Probes: p = (0.40, 0.80) reads +0.593, (0.40, 0.20) reads +0.005, (0.40, -0.40) reads -0.603.

### B09 · 26 words · ~9 s

> Change the slope, and the whole card pivots around the middle. Slope zero is flat. Slope one climbs at a diagonal. Same rule, one number different.

*Picture.* Code card at left with the uniform line highlighted; at right a real Godot card whose warm and cool halves pivot around the middle as slope sweeps from 0 to 1.5: flat at 0, a diagonal at 1.

*Motion.* The grey strip rotates about the centre as the slope grows.

*Lane.* capture · `ShaderLab` · runner-up: manim line pivoting about the origin

*Capture to record.* C03: Lab card, 01-signed-test, slope 0 to 1.5 linearly over the clip (6 s), Forward+; slope is 1 at 67 percent of the clip.

## Act II: Slope from an Angle

### B10 · 35 words · ~12 s

> We think in angles, not slopes, and the tangent connects them. Go one step across, along a line turned by the angle. The height you climb is the tangent, and that height is the slope.

*Picture.* Act title 'Slope from an Angle' (serif 40) top-left. Axes, a warm-grey line through the origin and a pale grey filled wedge for its angle. At across = 1 a warm-grey dashed vertical runs from the axis up to the line, ending in a terracotta dot; its height is a live number. The angle grows from 0 to 60 degrees and the height reads 0, 0.58, 1.0 and 1.73. Labels: 'angle', 'one step across', 'tangent of the angle = the slope'.

*Motion.* The line turns and the height at one step across grows with live numbers.

*Lane.* manim · `B10_TangentIsSlope` · runner-up: ShaderLab with tangent readouts

### B11 · 34 words · ~12 s

> In the shader, the slope is the tangent of the angle. Godot's tangent works in radians, where a full turn is about six point two eight, so the radians function converts our degrees first.

*Picture.* Code card at left with the slope line highlighted; at right a real Godot card whose grey strip turns, climbing to the right, as the angle sweeps from 0 to 60 degrees. Readouts: '0°: m = 0' at the start and '45°: m = 1' as it passes 45.

*Motion.* The strip turns and the readouts give the slope at 0 and 45 degrees.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C04: Lab card, 02-angle-line, angle 0 to 60 linearly over the clip (6 s); angle is 45 at 75 percent. GPU slopes: 0.57735 (30), 1.0 (45), 1.73205 (60).

### B12 · 36 words · ~12 s

> What if we skip that conversion? Godot reads thirty degrees as thirty radians. The slope becomes minus six point four: a steep line, leaning the wrong way. If an angle looks wrong, check the radians first.

*Picture.* Two real Godot cards side by side on the stage, the same angle sweeping to 30 degrees. Left: the grey strip climbs gently to the right (m = 0.58). Right: the strip is steep and leans the other way (m = -6.4). Below, the two code lines that differ; a terracotta ring settles on the right card.

*Motion.* Both lines start together; the right one jumps steep and backwards while the left turns smoothly.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace of the two lines

*Capture to record.* C05: custom scene two_panels.gd (cards 256 px at (170, 190) and (470, 190)): left 02-angle-line, right 03-no-radians; angle 0 to 30 over the first 4 s, then hold 2 s (6 s). GPU slope at 30 without radians(): -6.40533.

### B13 · 35 words · ~12 s

> Watch the slope as the angle grows. At forty-five degrees, it is one. At seventy-five, three point seven. At eighty-nine, fifty-seven. Toward ninety it has no limit: a vertical line climbs with no step across.

*Picture.* A plot (shader_kit plot) of tan(angle) against the angle from 0 to 90 degrees, y axis clipped at 10. A terracotta dot rides the curve from 0 degrees; numbers land at 45 (1), 75 (3.7) and 89 (57); the dot leaves the top of the plot as the curve shoots up and a label reads 'no limit'. A small grey line at the left turns with the angle.

*Motion.* The dot rides the curve and then shoots off the top of the plot as the angle nears ninety.

*Lane.* manim · `B13_TanExplodes` · runner-up: LectureEvidenceTable of angle and slope

### B14 · 40 words · ~14 s

> Right at ninety, the slope flips sign. On this Mac, Godot's tangent there is near minus twenty-three million, and warm and cool trade sides in one frame. A slope has a seam at vertical. We fix that at the end.

*Picture.* Code card at left; at right a real Godot card held at 89.9, then 90, then 91 degrees. The warm and cool halves meet at a vertical edge each time (the grey strip has shrunk to nothing), but at 90 they trade sides and stay traded at 91. Readouts: '89.9°: +573', '90°: −23 million', '91°: −57'.

*Motion.* Warm and cool swap sides between 89.9 and 90 degrees.

*Lane.* capture · `ShaderLab` · runner-up: manim two-line diagram of tan jumping from plus to minus

*Capture to record.* C06: Lab card, 02-angle-line, angle held at 89.9 (0 to 33 percent of the clip), 90.0 (33 to 67), 91.0 (67 to 100); 6 s. GPU tan: +572.967, -22877334, -57.2901.

## Act III: Distance to the Line

### B15 · 40 words · ~14 s

> A line has no thickness, so we cannot see it. Keep every pixel whose answer is near zero, and you get a band around the line. Two tools do that: absolute value drops the sign, and step is a switch.

*Picture.* Act title 'Distance to the Line' (serif 40) top-left. Left: the test square with the warm-grey line m = 0.5; a pale grey band grows out around the line (the pixels whose answer is near zero), labelled 'a band'. Right, arriving after the band: two small plots. abs(x) as a V with a terracotta dot sliding along x and its height mirrored, labelled 'abs: drop the sign'; step(a, b) as a flat zero that jumps to one where b reaches a, a dot sliding along b, labelled 'step(a, b): 0 until b reaches a, then 1' and the docs rule 'b < a ? 0.0 : 1.0'.

*Motion.* The band grows out of the line, then dots slide along the two plots: the V folds the negative side up, the step jumps from 0 to 1.

*Lane.* manim · `B15_AbsAndStep` · runner-up: LectureEvidenceTable of the two functions

### B16 · 38 words · ~13 s

> Take the absolute value of the test and call it d, for distance. Then step: distance first, thickness second. It answers one when the thickness has reached the distance, so the pixel is inside the band. Otherwise, zero.

*Picture.* Code card at left; at right a real Godot card with a white diagonal band across a grey card, climbing to the right. Two readouts on the card: '1' on the band and '0' beside it.

*Motion.* The distance line then the step line are highlighted; '1' lands on the band and '0' off it.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C07: Lab card, 04-band-raw, angle 45, thickness 0.1, still PNG. Probes: on the line reads white (1.0), off it grey (0.502).

### B17 · 37 words · ~13 s

> Tilt the line. Does the band keep its thickness? Watch. At zero degrees the band is ten percent of the card wide. At forty-five, seven percent. At seventy-five, under three. It thins out as the line steepens.

*Picture.* Code card at left; at right the same card with the white band while the angle sweeps: the band is a clear stripe at 0 degrees, visibly thinner at 45, a thin line at 75. Three readouts on the right of the card: '10%', '7%', 'under 3%'.

*Motion.* The band thins to a hairline as the angle grows.

*Lane.* capture · `ShaderLab` · runner-up: manim plot of width against angle

*Capture to record.* C08: Lab card, 04-band-raw, thickness 0.1; angle keyframes as fractions of the clip: 0 until 28 percent, 45 at 62, 75 at 78, 85 at 95. Measured widths (percent of card): 9.7 (0), 6.9 (45), 2.7 (75), 0.7 (85), 0.0 (89, 90).

### B18 · 38 words · ~13 s

> Why? The test measures straight up from the line. Distance means the shortest way, at a right angle. Tilt the line, and the shortest way gets shorter than straight up. The steeper the line, the bigger the difference.

*Picture.* A warm-grey line through the origin and a terracotta dot above it. A light-grey dashed vertical from the dot to the line (label 'straight up 0.6') and a darker solid grey segment at a right angle (label 'shortest way'). The line tilts from 0 to 60 degrees while the point rides with it so the vertical gap stays 0.6; the right-angle segment shrinks and its label reads 0.60, 0.42, 0.30.

*Motion.* The vertical gap stays at 0.6 while the shortest-way segment shrinks as the line tilts.

*Lane.* manim · `B18_TwoGaps` · runner-up: ShaderLab with a drawn overlay on the raw band

### B19 · 38 words · ~13 s

> The fix is one right triangle. Along the line, one step across climbs m, so that step is the square root of one plus m squared long. Divide the test by that, and you have the shortest distance.

*Picture.* A right triangle with legs 1 (across) and 0.5 (up) along a warm-grey line, the long side labelled 'sqrt(1 + 0.5²) = 1.118' (sqrt: the square root). Beside it a second, same-shaped triangle at the point: the straight-up gap 0.6 as its long side. An arrow labelled '÷ 1.118' turns 0.6 into 0.54, 'the shortest distance'.

*Motion.* The small triangle's long side scales the big one; the arrow turns 0.6 into 0.54.

*Lane.* manim · `B19_RightTriangle` · runner-up: LectureCodeTrace of the formula

### B20 · 35 words · ~12 s

> In code: absolute value of the test, divided by the square root of one plus m times m. Thickness is now a real distance. Point one makes the band a tenth of the card wide.

*Picture.* Code card at left with the distance line highlighted; at right the white band across the grey card, with a readout '10% wide' on the band.

*Motion.* The distance line is highlighted, then '10% wide' lands on the band.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C09: Lab card, 05-band-true, angle 45, thickness 0.1, still PNG. Measured width 9.8 percent of the card (theory 10).

### B21 · 29 words · ~10 s

> Tilt it again, now beside the old version. Fifteen degrees, forty-five, seventy-five, even eighty-five. The new band stays ten percent of the card wide. The old one fades away.

*Picture.* Two real Godot cards side by side: left the old band, right the new one. The angle sweeps through 15, 45, 75 and 85 degrees: the left band thins to a hairline while the right keeps its width. Readouts: the angle at the centre, 'new: 10%' under the right card and 'old: under 1%' under the left.

*Motion.* The left band fades to a hairline while the right band never changes.

*Lane.* capture · `ShaderLab` · runner-up: manim plot of both widths against angle

*Capture to record.* C10: custom scene two_panels.gd, cards 256 px at (170, 190) and (470, 190): left 04-band-raw, right 05-band-true, thickness 0.1; angle keyframes (fractions of the clip): 0 until 20 percent, 15 at 30, 45 at 35, 75 at 40, 85 at 44, hold. Measured widths: raw 9.7, 6.6, 2.4, 0.8 percent; true 9.7, 10.0, 9.7, 10.2 percent.

## Act IV: Shine

### B22 · 39 words · ~13 s

> To slide the line, add an offset to the distance, before the absolute value. The distance is true, so the line moves exactly that far, straight across, at any angle. Offset point five is a quarter of the card.

*Picture.* Act title 'Shine' (serif 40) top-left. Code card at left with the distance line highlighted; at right the white band on the grey card sliding from the upper left to the lower right at 35 degrees, then again at 70 degrees at the same speed. Final hold: readouts 'offset 0.5' and '¼ of card'.

*Motion.* The band slides straight across the card, at the same speed at both angles.

*Lane.* capture · `ShaderLab` · runner-up: manim line sliding with distance labels

*Capture to record.* C11: Lab card, 07-slide, thickness 0.1: angle 35 with offset -0.8 to 0.8 over 5 to 40 percent of the clip; angle 70 with offset -0.8 to 0.5 over 55 to 80 percent, then hold at 0.5; 8 s. Measured: offset 0.5 moves the band 0.250 of the card width at 0, 35 and 70 degrees.

### B23 · 38 words · ~13 s

> You may see another way: subtract a center point before testing. How far that slides the line depends on the angle. Shift a flat line sideways, and nothing moves. The offset slides it straight across, whatever the angle.

*Picture.* Two real Godot cards side by side, a flat white band across each. Left: the center shifted across from -0.6 to 0.6; the band does not move. Right: the offset swept the same way; the band slides up and down. Readouts under the cards: 'center: no move' and 'offset: slides'.

*Motion.* The flat band on the left never moves while the one on the right slides.

*Lane.* capture · `ShaderLab` · runner-up: manim arrows showing how far each shift moves a tilted line

*Capture to record.* C12: custom scene two_panels.gd, cards 256 px at (170, 190) and (470, 190), angle 0 on both: left 08-center-shift with center.x -0.6 to 0.6, right 07-slide with offset -0.6 to 0.6, over 30 to 78 percent of the clip. Measured: the left band stays at 0.0 px, the right moves 77 px at 0.6.

### B24 · 34 words · ~12 s

> Now the sprite. Where the band is, blend the sprite's color toward white. Mix takes two colors and a weight: zero gives the first, one gives the second. Here, the weight is the band.

*Picture.* Code card at left (first attempt, mix on the whole color); at right a real Godot window with the teal test sprite and a white band sweeping across it. The mix line is highlighted.

*Motion.* The white band sweeps across the sprite as the band and mix lines light up.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C13: Lab blob sprite, 09-shine-leak, angle 35, thickness 0.1; offset -1.5 to 1.5 linearly over the whole clip (6 s). The white stripe also crosses the empty parts of the sprite's square.

### B25 · 30 words · ~10 s

> But watch the empty corners. The stripe crosses them too. Mix blended the alpha as well, so transparent pixels turned white and solid. The highlight has leaked off the sprite.

*Picture.* The same capture and code as before. A readout 'leaks' lands at the upper left where the white stripe crosses the empty part of the sprite's square; the mix line stays highlighted.

*Motion.* The stripe is visible on the empty corners of the sprite's square while the voice names the leak.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with a ring on the stripe

*Capture to record.* C13 again (same file, no new recording). Measured: the empty pixel on the band line reads white (1.0, 1.0, 1.0) instead of the stage color (0.851, 0.835, 0.792), in both renderers.

### B26 · 33 words · ~11 s

> The fix is one multiplication. Alpha is zero where the sprite is empty and one where it is solid. Multiply the band by alpha, and the highlight lives only where the sprite does.

*Picture.* Two real Godot windows side by side with the teal sprite and a sweeping band: left the first attempt (the stripe spills onto the empty parts), right the fixed shader (the band stays on the sprite). Code card shows the fixed shader with the band line highlighted. Readouts: 'leaks' under the left and 'stays inside' under the right.

*Motion.* The left stripe spills off the sprite; the right band stops at the sprite's edge.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab single capture of the fixed shader

*Capture to record.* C14: custom scene two_panels.gd, blob sprites 256 px at (170, 190) and (470, 190): left 09-shine-leak, right 10-shine, angle 35, thickness 0.1; offset -1.5 to 1.5 over 5 to 95 percent of the clip (6 s). Measured: the right panel's empty pixel on the band line equals the stage color.

### B27 · 40 words · ~14 s

> To make it move, give the offset a clock. Time is one clock for the whole game. Time times a half, keeping only the fractional part, ramps from zero to one every two seconds. Mix stretches that across the sprite.

*Picture.* Code card at left with the offset line highlighted; at right the sprite with the glint looping every two seconds (the same capture as the opening) and a thin 0 to 1 ramp strip beneath it whose marker runs from 0 to 1 and restarts every two seconds. A readout 'fract: 0–1' lands at the ramp.

*Motion.* The marker runs along the ramp and restarts as the glint crosses the sprite each cycle.

*Lane.* capture · `ShaderLab` · runner-up: manim sawtooth plot of fract(TIME * 0.5)

*Capture to record.* C01 reused (11-shine-clock, 12 s loop). The ramp marker repeats with the clip's 2 s period (ShaderLab ramp needs a period; see BUILD-PROMPT).

### B28 · 40 words · ~14 s

> To start a shine when something happens, let your game drive the offset. Set the start, then tween to the end; a tween glides a value over time. Skip that first line, and the tween has nothing to start from.

*Picture.* A four-line GDScript card at left (the function that sets the start and tweens the offset); at right the sprite at rest, then one glint crossing it each time the scripted call fires. A label 'scripted call' stays on screen.

*Motion.* The sprite rests, the call fires, one glint crosses, and it rests again.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace of the GDScript alone

*Capture to record.* C16: custom scene (verify1.gd T1): Sprite2D 'Sprite' with 10-shine, scene script exactly the four lines shown; the harness calls shine() at 1.0 s and again every 3 s; 12 s loop, Forward+. Verified: the band covers the blob centre 0.388 to 0.429 s after the call (expected 0.373 to 0.427); offset ends at 1.5; resting offset is the default -2.0.

### B29 · 34 words · ~12 s

> That is the whole shine. Center the address. Turn the angle into a slope. Divide for true distance, and slide it by the offset. Step into a band, weighted by alpha. Mix in white.

*Picture.* The finished fourteen-line shader at left with focus stepping down it as each step is named; at right the sprite with the glint sweeping across once.

*Motion.* Focus steps down the lines in the order the voice names the steps while the glint crosses.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C17: Lab blob sprite, 10-shine, angle 35, thickness 0.1; offset -1.5 to 1.5 over 10 to 90 percent of the clip (8 s). Measured: band on the blob at offset 0, off the sprite at +-1.5.

### B30 · 37 words · ~13 s

> One limit. U V runs zero to one even on a wide shape, so the line gets stretched. On sixteen by nine, forty-five degrees comes out near twenty-nine. Scale the across part by width over height first.

*Picture.* Two real 16:9 Godot panels side by side. Left: the band at 45 degrees runs shallow, near 29 degrees on screen. Right, with the across part scaled: 45 degrees really is 45. Readouts: '45° shows 29°' under the left, '45° shows 45°' under the right. Three code lines below.

*Motion.* The left band stays shallow as the angle reaches 45 while the right band reaches a true diagonal.

*Lane.* capture · `ShaderLab` · runner-up: manim rectangle with the address square stretched over it

*Capture to record.* C18: custom scene two_panels.gd, wide panels 304 x 171 at (160, 180) and (480, 180): left 05-band-true, right 06-wide-fix (aspect 1.7778), thickness 0.1; angle 0 to 45 over 5 to 38 percent of the clip, then hold. Measured: 29.2 degrees on screen without the fix, 44.7 with it; thickness drifts 17.8, 20.8, 27.1 px at 20, 45, 70 degrees without it, constant 17.1 with it.

## Act V: The Angle-Safe Way

### B31 · 34 words · ~12 s

> Slope has a seam at vertical. So describe the line by its direction instead: a step of length one, turned by the angle. Across is the cosine of the angle. Up is the sine.

*Picture.* Act title 'The Angle-Safe Way' (serif 40) top-left. A grey arrow of length one from the origin at 35 degrees; its across part is drawn along the horizontal axis labelled 'cosine: across' and its up part labelled 'sine: up' (for a step of length one). The arrow turns from 0 to 60 degrees and the two legs grow and shrink.

*Motion.* The arrow turns and its two legs trade length.

*Lane.* manim · `B31_UnitStep` · runner-up: ShaderLab with sine and cosine readouts

### B32 · 40 words · ~14 s

> Turn that arrow a quarter turn and it points straight away from the line: the normal. Dot multiplies across by across and up by up, then adds. Dot a pixel's address with the normal, and you get its signed distance.

*Picture.* The warm-grey line at 35 degrees with its unit arrow along it; a second arrow turned a quarter turn, labelled 'the normal'. A terracotta dot P drops a warm-grey dashed line onto the normal's axis, labelled 'dot(p, n)' with a signed number; P then moves to the other side of the line and the number turns negative. Under it: 'dot: across × across + up × up'.

*Motion.* The point crosses the line and its dot value changes sign while its distance changes smoothly.

*Lane.* manim · `B32_NormalAndDot` · runner-up: LectureCodeTrace of the dot line

### B33 · 35 words · ~12 s

> It is the same distance in disguise. In our triangle, the cosine is one over that square root, so dividing by it is multiplying by the cosine. What is left is exactly p dot n.

*Picture.* An equation chain, one line at a time, each line rewriting the one above: '(y − m x) ÷ sqrt(1 + m²)' → '(y − m x) × cosine' → 'y × cosine − x × sine' → 'p · n'. Beside it the earlier triangle (1, m, sqrt(1 + m²)) with cosine = 1 ÷ sqrt(1 + m²) marked on it.

*Motion.* Each line of the chain rewrites itself into the next, ending on p dot n.

*Lane.* manim · `B33_SameThing` · runner-up: LectureEvidenceTable of the two forms

### B34 · 40 words · ~14 s

> In code, the normal is minus sine, cosine of the angle, and the distance is the absolute value of p dot n. No tangent, no divide. At thirty, sixty and eighty-nine degrees, it matches the slope version pixel for pixel.

*Picture.* Code card at left (the thirteen-line direction shader); at right two real Godot cards side by side with the slope version on the left and the direction version on the right, the same angle sweeping through 30, 60 and 89 degrees: the two white bands are identical. Labels 'slope form' and 'direction form' under them and 'identical' at the end.

*Motion.* Both bands turn together and stay identical.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C19: custom scene two_panels.gd, cards 256 px at (170, 190) and (470, 190): left 05-band-true, right 12-direction, thickness 0.1; angle 0 to 89 linearly over 5 to 95 percent of the clip (6 s). Measured: 0 of 230,400 pixels differ at 30, 60 and 89 degrees.

### B35 · 33 words · ~11 s

> And it keeps going through ninety. The slope version swaps warm and cool. The direction version never does, because the normal turns smoothly. Anything that cares which side it is on needs that.

*Picture.* Two real Godot cards side by side on the stage, held at 89.9, 90 and 91 degrees. Left (slope form): the warm and cool halves trade sides at 90. Right (direction form): they never move. Angle labels at the centre.

*Motion.* The left halves swap at ninety while the right halves stay put.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab single capture of the direction form

*Capture to record.* C20: custom scene two_panels.gd, cards 256 px: left 02-angle-line, right 13-direction-signed; angle held at 89.9 (0 to 33 percent of the clip), 90.0 (33 to 67), 91.0 (67 to 100); 6 s. Measured: left swaps between 89.9 and 90 in both renderers; right never swaps from 80 to 100 degrees.

## Closing

### BVDT · recap · 101 words · ~34 s

> Let's recap with Claude. A line is a test: y minus m times x is zero on it, positive on one side, negative on the other. The slope is the tangent of the angle, and it blows up at vertical. Divide the test by the square root of one plus m squared and it becomes the true distance. A step makes the band, an offset slides it, and alpha keeps the shine on the sprite. A direction and a dot give the same distance, with no seam at vertical. A line is one rule, and a shine is that rule, slid.

*Picture.* The recap card: A line is a test: y minus m times x is zero on it, positive on one side, negative on the other. / The slope is the tangent of the angle, and it blows up at vertical. / Divide the test by the square root of one plus m squared and it becomes the true distance. / A step makes the band, an offset slides it, and alpha keeps the shine on the sprite. / A direction and a dot give the same distance, with no seam at vertical. / A line is one rule, and a shine is that rule, slid.

### BHTF · your turn · 92 words · ~31 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a sprite. Uniforms: angle in degrees, thickness, offset. Center the address and flip it so up is up. Draw a white band along a line through the middle at that angle, slid sideways by the offset, the same thickness at every angle, only on visible pixels. Finally, point me to the distance line. Then check two things yourself. At forty-five degrees, does the band climb to the right? And is it as thick at eighty degrees as at ten?

*Prompt shown and read in full:* Write a Godot canvas item shader for a sprite. Uniforms: angle in degrees, thickness, offset. Center the address and flip it so up is up. Draw a white band along a line through the middle at that angle, slid sideways by the offset, the same thickness at every angle, only on visible pixels. Finally, point me to the distance line.

*Two checks:* Check: at forty-five degrees the band climbs to the right. · Check: the band is as thick at eighty degrees as at ten.

### BOUT · outro · 7 words · ~4 s

> Lines and Shine. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


# Script: The Shader Math Toolkit

**What this is.** The words Liam will say in *The Shader Math Toolkit*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 47 beats, 1808 words, about **10:19** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: manim 23, capture 16, remotion 2.

**If it runs long.** Cut, in this order: the toolkit map (B06), the sine beat (B34), the normalize beat (B27), the soft-spot beat (B31), the smooth step docs beat (B12) and the floor-only beat (B21). Each repeats or previews an idea carried elsewhere. The plot-reading pair (B04, B05), the smooth step correction (B11), the whole-and-leftover split (B22), the mod trap (B25) and the whole ring build (Act V) stay: they are the method, the two corrections and the payoff. A cut beat also leaves its name in the recap line (BVDT_LINES[3] for normalize and sine), so trim that line and its spoken twin too.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Ramps and Plots | 6 | 235 | ~1:20 |
| II | Cut and Blend | 10 | 379 | ~2:09 |
| III | Repeat and Fold | 9 | 328 | ~1:52 |
| IV | Distance and Curves | 9 | 342 | ~1:56 |
| V | Build a Ring | 7 | 231 | ~1:19 |

## Opening

### BOPEN · identity card · 25 words · ~8 s

> The Shader Math Toolkit. Learn a dozen small functions that shape what a shader draws, then use three of them to build a soft ring.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "The Shader Math Toolkit", and the line "A dozen small functions behind shader effects".

### BIDEA · the question · 42 words · ~14 s

> Hallo. This is Liam, in for Bear. People think shaders need advanced math. They need about a dozen small functions, and each one reshapes a smooth run of numbers. Learn what each does, and you can predict what a shader will draw.

*Picture.* The hesitant writer types: "Shaders need advanced math." then deletes "advanced math" and types "a dozen small functions".

### BDEFS · terms · 64 words · ~22 s

> Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. U V is a point's address on a shape: zero to one across, zero to one down. A function takes numbers in and gives one number out. And a vector is a bundle of two to four numbers.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Pixel** — one dot of the picture on screen; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Function** — a rule: numbers go in, one number comes out; **Vector** — a bundle of two to four numbers

## Act I: Ramps and Plots

### B01 · 35 words · ~12 s

> This ring is not an image. Three small functions draw it: one measures distance, one softens an edge, one blends two colors. By the end, you will be able to read every line of it.

*Picture.* Act title 'Ramps and Plots' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a soft teal ring on cream, centred, that grows smoothly from small to large. No code yet.

*Motion.* The ring grows outward the whole time the voice names the three functions that draw it.

*Lane.* capture · `ShaderLab` · runner-up: manim: a ring outline with three function names around it

*Capture to record.* C01: Lab render of lab-shaders/15-ring-final.gdshader on a 720x720 square centred in the 1280x720 logical canvas (stage #D9D5CA either side). radius swept 0.12 to 0.38 linearly from 0.5 s to 11.0 s, then held; 13 s, 30 fps, Forward+, no input. Verified: radius 0.12 -> teal at d = 0.16; 0.38 -> teal at d = 0.42.

### B02 · 41 words · ~14 s

> Start with a ramp: a smooth run of values from zero up to one. The simplest ramp is a pixel's address across the shape: zero at the left edge, one at the right. In code, that is U V dot x.

*Picture.* A wide horizontal RAMP STRIP on the cream stage (a row of 64 narrow tiles with thin cream gaps, true grays: value v drawn as gray v, 0 black and 1 white), end labels '0' and '1', and a terracotta dot riding it with a live value label. Under the strip, in mono: 'UV.x · across the shape'. Caption in serif, the GLOSSARY wording: 'ramp · a smooth run of values from 0 up to 1'.

*Motion.* The dot slides along the strip from 0 to 1 and its value label climbs; the strip is the ramp.

*Lane.* manim · `B02_RampStrip` · runner-up: ShaderLab: the real gradient with a marker

### B03 · 36 words · ~12 s

> A shader can show a number as gray. Fragment runs once for each pixel the shape covers, and sets its color. Here the color is three copies of the ramp: zero is black, one is white.

*Picture.* Code card at left (the five-line shader), at right a real Godot window showing the black-to-white gradient with a thin 0 to 1 ramp strip under it. Labels on the highlighted lines carry the GLOSSARY definitions of fragment() and COLOR word for word (60 characters at most each, so they fit on one line or wrap to two); a last label on the COLOR line gives the GLOSSARY wording of alpha for the final number, 1.0 (the word alpha is on screen only, not spoken).

*Motion.* The fragment line is highlighted, then the COLOR line; the ramp marker sweeps the gradient from 0 to 1 as the voice says 'zero is black, one is white'.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: Lab rect, lab-shaders/01-ramp.gdshader, still PNG 1920x1080 (probes 0.0196 / 0.498 / 0.9804 at x = 0.02 / 0.5 / 0.98; red = green = blue).

### B04 · 43 words · ~15 s

> From here on, every function gets the same picture. The input runs along the bottom, the output up the side. A dot travels the line, and the strip below shows the output as gray. A function that changes nothing is a straight diagonal.

*Picture.* The STANDARD PLOT (defined once in SHOTLIST.md) on the cream stage: square axes, 'input' along the bottom with 0 and 1, 'output' up the side with 0 and 1, the straight diagonal of f(x) = x, a terracotta dot riding it, a thin dashed drop line from the dot to the ramp strip placed under the axes at the same x scale, and the ramp strip filling with its tiles up to the drop line. Mono formula tag 'f(x) = x'. A small gray credit under the plot: 'curves drawn from the formulas · checked against Godot 4.7.2 renders'.

*Motion.* The dot travels the diagonal; the drop line keeps its x on the strip and the strip fills up to there.

*Lane.* manim · `B04_ReadThePlot` · runner-up: ShaderLab: the real gradient with a marker

### B05 · 39 words · ~13 s

> Bend the line and the strip follows. Here the function is one minus x. The line runs downhill, so the strip runs from white to black. Read the line, and you can predict the picture before you see it.

*Picture.* The standard plot as in B04, now with f(x) = 1 - x: the line starts as the diagonal and swings to run downhill from (0, 1) to (1, 0); the strip beneath flips from dark-to-light to light-to-dark with it. Mono tag 'f(x) = 1 - x'. A small caption 'predict the strip'.

*Motion.* The diagonal pivots to run downhill and the strip under it flips; the dot then rides the new line.

*Lane.* manim · `B05_BendTheLine` · runner-up: ShaderLab: the real flipped gradient

### B06 · 41 words · ~14 s

> About a dozen functions come in three families. Cut and blend: step, smooth step, mix, clamp. Repeat and fold: abs, fract, floor, mod. Distance and curves: length, normalize, distance, power, sine. Then we use three of them to build a ring.

*Picture.* Three columns of small mono function chips on the cream stage, each under a serif family title: 'Cut and blend' (step, smoothstep, mix, clamp), 'Repeat and fold' (abs, fract, floor, mod), 'Distance and curves' (length, normalize, distance, pow, sin). At the right a ring outline; thin lines run from the chips distance, smoothstep and mix to it.

*Motion.* Each family's chips pop in as the voice names it; then three lines draw from distance, smoothstep and mix to the ring and it fills.

*Lane.* manim · `B06_ToolkitMap` · runner-up: LibraryIconRow of the function names

## Act II: Cut and Blend

### B07 · 36 words · ~12 s

> Step is a switch. Give it an edge and a ramp. Where the ramp is below the edge, the answer is zero. At the edge or above, it is one. The plot is a single jump.

*Picture.* Act title 'Cut and Blend' (serif 40) top-left. The standard plot with a dashed vertical line at x = 0.5 labelled 'edge'. The curve is 0 until the edge, then 1; at the edge an open dot at (0.5, 0) and a closed dot at (0.5, 1) mark that the value AT the edge is 1. Mono tag 'step(edge, x) · 0 below the edge, 1 from the edge up' (the GLOSSARY wording). Strip beneath: left half black tiles, right half white tiles.

*Motion.* The dot rides the 0 level up to the edge, jumps to 1 at the edge and rides on at 1; the strip's hard split lands with it.

*Lane.* manim · `B07_StepSwitch` · runner-up: ShaderLab step render

### B08 · 33 words · ~11 s

> In a shader, the edge goes first, then the ramp. Here the edge is a uniform, a dial your game can turn from outside. Slide it, and the hard split slides with it.

*Picture.* Code card at left (the eight-line shader); at right a real Godot window split into a black half and a white half by a hard vertical line. A label on the uniform line gives the first half of the GLOSSARY definition ('a value your game sets from outside') and the caption under the result gives all of it ('uniform: a value your game sets from outside; every pixel sees the same one'). The split slides left and right as the edge dial is swept.

*Motion.* The hard split slides along the window as the edge value is swept.

*Lane.* capture · `ShaderLab` · runner-up: manim: the edge marker sliding on the plot

*Capture to record.* C03: Lab rect, lab-shaders/02-step.gdshader; edge held at 0.5 until 4.0 s, then 0.5 -> 0.2 over 4.0-6.5 s, then 0.2 -> 0.8 over 6.5-10.5 s, held to 12.5 s; 30 fps, Forward+. Verified: edge 0.5 -> 0 at x = 0.45 and 1 at x = 0.55; edge 0.2 -> 0 at 0.15, 1 at 0.25; edge 0.8 -> 0 at 0.75, 1 at 0.85.

### B09 · 35 words · ~12 s

> Clamp pins a number inside a range. Below the low end, you get the low end. Above the high end, you get the high end. In between, nothing changes. It is max first, then min.

*Picture.* The standard plot with two horizontal guide lines at y = 0 and y = 1 labelled 'low end' and 'high end'. A dashed overshooting ramp y = 2x - 0.5 runs from (0, -0.5) to (1, 1.5) beyond the guides; the solid curve is clamp(2x - 0.5, 0, 1): flat at 0 until x = 0.25, a ramp to 1 at x = 0.75, flat at 1 after. Short labels 'max · the higher of two' and 'min · the lower of two' on the two ends, mono tag 'clamp(x, low, high) = min(max(x, low), high)'. Strip beneath: black tiles, a ramp of tiles, white tiles.

*Motion.* The dashed ramp overshoots; the solid curve cuts it flat at the low end, then at the high end; the dot rides the pinned curve.

*Lane.* manim · `B09_ClampPins` · runner-up: ShaderLab clamp render

### B10 · 34 words · ~12 s

> Smooth step is a switch that eases in and out. Give it two edges and a ramp. Below the first edge, zero. Above the second, one. Between them, a smooth S with no corners.

*Picture.* The standard plot with two dashed vertical edges at x = 0.3 and 0.7 labelled 'first edge' and 'second edge'. The curve is flat at 0, a smooth S rising to 1 between the edges, flat at 1 after. Mono tag 'smoothstep(a, b, x) · a smooth S between two edges'. Strip beneath: black tiles, a soft ramp of tiles, white tiles.

*Motion.* The curve flattens at 0, swells through a smooth S and lands flat at 1; the dot rides it and the strip's edge is soft.

*Lane.* manim · `B10_SoftSwitch` · runner-up: ShaderLab smoothstep render

### B11 · 42 words · ~14 s

> It is not a straight line, and one number shows it. Say the edges are zero and ten, and the input is one. A straight line would give point one. The S gives point zero two eight, because it starts out slowly.

*Picture.* A plot with the input from 0 to 10 and the output from 0 to 1. A dashed straight line from (0, 0) to (10, 1) labelled 'a straight line' and the solid S curve of smoothstep(0, 10, x) labelled 'the S'. A vertical guide at x = 1 drops; two dots land on the two curves; read-outs '0.1' on the line and '0.028' on the S. A terracotta ring (grey-backed) rings the slow start of the S near x = 0 to 2. Small grey credit: 'checked in Godot 4.7.2 · Forward+'.

*Motion.* The guide at x = 1 lands two dots on the two curves; the line's reads 0.1, the S's reads 0.028, and the S visibly lies below the line near the start.

*Lane.* manim · `B11_NotALine` · runner-up: LectureEvidenceTable (0.1 against 0.028)

### B12 · 43 words · ~15 s

> The docs spell out the formula. Squeeze the input between the edges into zero to one, call that t, and return three t squared minus two t cubed. They also warn that a first edge at or above the second gives undefined results.

*Picture.* The real Godot 4.7 'Built-in shader functions' page (the /en/4.7/ address) at the smoothstep entry in a browser window; the camera pushes in on the formula (clamp, then t * t * (3.0 - 2.0 * t)) and a terracotta ring marks it; later it pushes to the sentence 'Results are undefined if a >= b' and the ring moves there. Ring and camera numbers are fitted to the real capture.

*Motion.* The camera pushes in on the formula the voice describes, then on the warning sentence.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: the formula typed out

### B13 · 33 words · ~11 s

> In code, the edges are the first two numbers. Here they sit either side of one half, and a dial sets how far. Pull them together and the S tightens toward a step.

*Picture.* Code card at left (the eight-line shader with the width dial); at right a real Godot window with a soft black-to-white transition across the middle that sharpens into a near-hard split as the width is swept down.

*Motion.* The soft edge tightens into a hard split while the voice says 'pull them together'.

*Lane.* capture · `ShaderLab` · runner-up: manim: the S tightening on the plot

*Capture to record.* C04: Lab rect, lab-shaders/03-smoothstep.gdshader; width held at 0.4 until 3.5 s, then 0.4 -> 0.03 over 3.5-10.0 s, held to 13 s; 30 fps, Forward+. Verified: width 0.45 -> 0.1255 / 0.498 / 0.8745 at x = 0.25 / 0.5 / 0.75; width 0.3 -> 0.0196 / 0.498 / 0.9804; width 0.03 -> 0 / 0.4824 / 1.

### B14 · 44 words · ~15 s

> Mix slides between two values. Give it a start, an end, and a weight. Weight zero returns the start, one returns the end, one half lands halfway. It does not pin the weight: a weight of two overshoots the end, so clamp it first.

*Picture.* The standard plot with the weight (the ramp, axis label 't · weight') as input from 0 to 2 and the output going from a start value to an end value: a straight line from (0, 0.2) through (1, 0.9), continuing dashed to (2, 1.6); tick labels 'a · start' and 'b · end' on the y axis at 0.2 and 0.9. Read-outs on the line at weights 0, 1 and one half: 'start', 'end', 'halfway'; then at weight 2 the read-out 'overshoots: 1.6'. Mono tag 'mix(a, b, t) · blends from a to b: t of 0 gives a, 1 gives b' (the GLOSSARY wording) and a smaller 'a x (1 - t) + b x t'. A small bracket 'clamp(t, 0, 1)' lands on the weight axis between 0 and 1. Strip beneath, for weights 0 to 1 only, from the gray of 0.2 up to the gray of 0.9.

*Motion.* The dot rides the line from the start value to the end value, stops at three read-outs, then runs on past the end to 1.6 where the clamp bracket marks the safe range.

*Lane.* manim · `B14_MixSlides` · runner-up: ShaderLab mix render

### B15 · 37 words · ~13 s

> A color is a vector, so mix blends all of its numbers at once. Here it blends teal into gold, with the ramp as the weight. The function that slid one number now slides a whole color.

*Picture.* Code card at left (the seven-line shader), at right a real Godot window showing a smooth teal-to-gold gradient with the thin 0 to 1 ramp under it.

*Motion.* The mix line is highlighted, then the two colour lines; the ramp marker sweeps the gradient as the voice says 'with the ramp as the weight'.

*Lane.* capture · `ShaderLab` · runner-up: manim: two colour dots mixing

*Capture to record.* C05: Lab rect, lab-shaders/04-mix-colors.gdshader, still PNG 1920x1080. Verified: x = 0.02 -> (0.3804, 0.6431, 0.5686); 0.5 -> (0.6627, 0.7216, 0.5098); 0.98 -> (0.949, 0.7961, 0.451).

### B16 · 42 words · ~14 s

> The weight can be any reshaped ramp. The plain ramp gives a smooth blend. Step gives a hard cut. Smooth step gives a soft one. A weight like this, a number from zero to one for each pixel, is called a mask.

*Picture.* Three stacked rows. Each row: a small plot of a weight curve (the plain ramp; step at 0.5; smoothstep 0.4 to 0.6), an arrow drawn as a shape, then a teal-to-gold strip blended with that weight (hard cut for step, soft edge for smoothstep). Row captions 'plain ramp', 'step', 'smoothstep'. At the end a grey-backed bracket round the three weight plots and the GLOSSARY wording in serif: 'mask · a number from 0 to 1 per pixel saying how much of something to show'.

*Motion.* Each row builds left to right on its spoken word; the bracket and the word 'mask' land last.

*Lane.* manim · `B16_AnyWeight` · runner-up: ShaderLab: three real renders

## Act III: Repeat and Fold

### B17 · 34 words · ~12 s

> A ramp can be stretched and shifted. Multiply by two and subtract one, and it runs from minus one to one, with zero in the middle. Now negative numbers are part of the picture.

*Picture.* Act title 'Repeat and Fold' (serif 40) top-left. The ramp strip with tick labels 0 and 1 and a terracotta dot at its middle. Mono formula tag 'x × 2 − 1' appears; the tick labels first stretch to 0 and 2 (the '× 2' step), then slide to −1 and 1 (the '− 1' step), with a zero marker landing at the centre under the dot. A small caption 'zero here'.

*Motion.* The strip's tick labels stretch to 0..2 and then shift to −1..1 while the strip itself stays put; zero lands under the dot.

*Lane.* manim · `B17_Recenter` · runner-up: LectureEvidenceTable of before and after ranges

### B18 · 38 words · ~13 s

> Absolute value, written abs, drops the minus sign. Fold the ramp at zero and the left half lands on top of the right half. The plot is a V, and the strip is a mirror: bright, dark, bright.

*Picture.* The ramp strip with ticks −1, 0, 1 (from B17), a terracotta dot at 0. The strip's left half folds over onto the right half like a page about the zero line (a half-turn Transform, finished by 0.44). Below it the standard plot of abs(x) over −1..1: a V with the dot riding down the left arm and up the right arm. Mono tag 'abs(x) · drops the minus sign'. Strip beneath the plot: white, black, white tiles.

*Motion.* The left half of the strip folds onto the right half; then the dot rides the V and the strip beneath reads white, black, white.

*Lane.* manim · `B18_FoldAtZero` · runner-up: ShaderLab abs render

### B19 · 36 words · ~12 s

> Fract keeps only what comes after the decimal point. Two point seven five becomes point seven five. Multiply the ramp by four first, and fract gives four ramps in a row, each starting over at zero.

*Picture.* A small inset number line with a dot at 2.75 splitting into '2' and '.75' and the arrow '2.75 → 0.75'; mono tag 'fract(x) · the part after the point: x minus floor(x)'. Then the standard plot: a steep dashed ramp 4x leaves the top of the plot, and the solid curve is fract(4x): four saw teeth (each climbing 0 to 1, falling back to 0 at x = 0.25, 0.5, 0.75) with open and closed dots at the jumps. The dot rides the teeth; the strip beneath shows four ramps in a row.

*Motion.* The dot climbs a tooth, drops back to zero at each whole number and climbs again; the strip repeats four times.

*Lane.* manim · `B19_RampRestarts` · runner-up: ShaderLab fract render

### B20 · 33 words · ~11 s

> Fract is one line in a shader. The number you multiply by is how many copies you get. Turn that dial from one up to six, and the picture fills with repeating ramps.

*Picture.* Code card at left (the eight-line shader with the count dial); at right a real Godot window showing one black-to-white ramp that splits into 2, 3, 4 ... 6 repeating ramps as the count is swept up.

*Motion.* The picture fills with more and more repeating ramps while the voice says 'from one up to six'.

*Lane.* capture · `ShaderLab` · runner-up: manim: the count changing on the plot

*Capture to record.* C06: Lab rect, lab-shaders/05-fract.gdshader; count held at 1 until 4.5 s, then 1 -> 6 over 4.5-10.5 s, held to 12.5 s; 30 fps, Forward+. Verified: count 1 -> 0.098 / 0.298 / 0.6 / 0.898 at x = 0.1 / 0.3 / 0.6 / 0.9; count 4 -> 0.3961 / 0.1961 / 0.3961 / 0.5961; count 6 -> 0.5961 / 0.7961 / 0.5961 / 0.3961.

### B21 · 34 words · ~12 s

> Floor keeps the whole part instead. It rounds down to the whole number below. Multiply the ramp by four and take floor: zero, one, two, three, four flat steps with a jump between each.

*Picture.* Mono tag 'floor(x) · rounds down to the whole number below' with a tiny inset '2.75 → 2'. The standard plot with output 0 to 4: a dashed diagonal 4x and the solid staircase floor(4x) with values 0, 1, 2, 3 (closed dot at the left end of each step, open dot at the right end). Strip beneath: four flat bands (shown divided by 3, note '÷ 3 to fit') labelled 0 1 2 3.

*Motion.* The staircase builds one step at a time as the voice counts zero, one, two, three; the strip gets four flat bands.

*Lane.* manim · `B21_RoundDown` · runner-up: ShaderLab floor render

### B22 · 38 words · ~13 s

> Every number splits in two. Floor is the whole part, fract is the leftover. Two point seven five is two plus point seven five. So floor says which section you are in, and fract says where inside it.

*Picture.* A number line from 0 to 4 with a dot at 2.75. Two brackets under it: from 0 to 2 labelled 'floor = 2' and from 2 to 2.75 labelled 'fract = 0.75'; equation in serif '2.75 = 2 + 0.75'. Then the dot slides from 0 to 4 with two live read-outs: 'floor' stepping 0, 1, 2, 3 and 'fract' climbing and resetting.

*Motion.* The dot splits into a whole part and a leftover; then it slides along the line while 'floor' steps and 'fract' resets at each whole number.

*Lane.* manim · `B22_WholeAndLeftover` · runner-up: LectureEvidenceTable (x, floor, fract)

### B23 · 35 words · ~12 s

> Combine fract with step. Fract makes the ramp restart, and step cuts each copy in half. Dark, light, dark, light: stripes, from two functions and no image. Change the multiplier and you change the count.

*Picture.* Code card at left (the six-line shader), at right a real Godot window of black and white vertical stripes (sixteen bands: eight ramps, each cut in half). The step(...fract(...)) line is highlighted with a short label (one or two words) that changes to name each function's job.

*Motion.* The same line is highlighted while three labels name what fract does, what step does, and what the multiplier sets.

*Lane.* capture · `ShaderLab` · runner-up: manim: stripes built from two plots

*Capture to record.* C07: Lab rect, lab-shaders/06-stripes.gdshader, still PNG 1920x1080. Verified: x = 0.05 -> 0; 0.1 -> 1; 0.15 -> 0; 0.2 -> 1.

### B24 · 35 words · ~12 s

> Mod gives the remainder after dividing: x minus y times floor of x over y. With y equal to one, it is exactly fract. With y of point two five, the ramp repeats every quarter.

*Picture.* A mono tag 'mod(x, y) · the remainder after dividing x by y' (the GLOSSARY wording) and the formula 'mod(x, y) = x − y · floor(x / y)' assembling term by term. Then a small card 'y = 1: same as fract(x)' and the standard plot of mod(x, 0.25): four teeth of height 0.25 (plot output 0 to 0.25) with the dot riding them; caption 'y = 0.25: repeats every 0.25'. Strip beneath: four ramps.

*Motion.* The formula assembles; then the dot rides four teeth that each repeat every quarter.

*Lane.* manim · `B24_Remainder` · runner-up: LectureCodeTrace of the formula

### B25 · 45 words · ~15 s

> One trap. In a shader, mod of minus point two five and one is point seven five: it follows floor. G D script's F mod keeps the sign and says minus point two five. F pos mod matches the shader. Check which one you wrote.

*Picture.* A three-row table: the shader row, then GDScript's fmod row (keeps the sign), then fposmod (matches the shader); the active row is ringed as the voice names it.

*Motion.* The ring moves down the rows with the voice; the minus sign on the fmod result is the surprise.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: number line with a floor arrow

## Act IV: Distance and Curves

### B26 · 35 words · ~12 s

> Now two numbers at once. A vector bundles them, and length says how long that bundle is, measured from zero. Three across and four down has length five: the square root of nine plus sixteen.

*Picture.* Act title 'Distance and Curves' (serif 40) top-left. A pair of axes with the origin at the top left, x to the right and y counting DOWN (a small label 'y counts down', as the address does), and a vector arrow from the origin to (3, 4): dashed legs 3 across and 4 down, hypotenuse labelled 5; mono tag 'length(v) · the length of a vector' (the GLOSSARY wording, cut before its 'of an offset' clause because the film never says offset) and the formula '√(x² + y²)', plus 'v = (3, 4)'.

*Motion.* The legs draw (three across, then four down), the arrow follows, and the length 5 lands last.

*Lane.* manim · `B26_HowLong` · runner-up: LectureEvidenceTable

### B27 · 33 words · ~11 s

> Normalize keeps a vector's direction and sets its length to one. Take the arrow three across, four down. Normalize it and you get point six across, point eight down: same direction, length one.

*Picture.* The axes of B26 (origin top left, y counting down) with the vector (3, 4) in grey and a unit circle (radius 1, the quarter that lies in the picture) drawn at the origin. The arrow shrinks along its own line until its tip rests on the circle at (0.6, 0.8). Labels change from 'length 5' to 'length 1'; mono tag 'normalize(v) · same direction, length 1'.

*Motion.* The arrow slides back along its own line onto the unit circle: the direction stays, the length becomes one.

*Lane.* manim · `B27_UnitArrow` · runner-up: ShaderLab normalize render

### B28 · 39 words · ~13 s

> Distance is the length of the gap between two points. Pick the middle of the shape, and ask every pixel how far it is from there. Pixels near the middle get small numbers, pixels far away get big ones.

*Picture.* The UV square (0 to 1 across, 0 to 1 down, y pointing down) with a terracotta dot at the middle labelled 'middle'. Mono tag 'distance(a, b) = length(a − b)'. Five pixel dots appear one at a time, each joined to the middle by a dashed line and carrying its real distance: (0.9, 0.5) 0.40, (0.5, 0.2) 0.30, (0.15, 0.85) 0.49, (0.95, 0.95) 0.64, (0.55, 0.55) 0.07.

*Motion.* Pixel dots land one by one with dashed lines to the middle and their distances; near dots read small, far dots read big.

*Lane.* manim · `B28_AskEveryPixel` · runner-up: ShaderLab distance render

### B29 · 40 words · ~14 s

> That is one line of shader: the distance from the pixel's address to the middle. The result is a ramp that grows outward in every direction. The middle of each edge is half away; the corners are about point seven.

*Picture.* Code card at left (the six-line shader); at right a real Godot window with a square picture: black in the middle growing to light grey at the edges and corners, like a cone seen from above. Two read-outs: '0.5' at the middle of the right edge and '0.71' near a corner.

*Motion.* The distance line is highlighted, then the COLOR line; read-outs land on the edge middle and on a corner.

*Lane.* capture · `ShaderLab` · runner-up: manim: the UV square shaded

*Capture to record.* C08: Lab square render of lab-shaders/08-distance.gdshader (720x720 centred in the 1280x720 canvas), still. Verified (360x360 Lab): middle 0.0039; (0.75, 0.5) 0.2471; edge middle 0.4941; corner 0.7059 (the exact corner value is 0.7071).

### B30 · 41 words · ~14 s

> A warning before we draw circles: use a square shape. On a wide one, the circle turns into an oval. The address always runs from zero to one on both sides, whatever the proportions, so the circle stretches with the shape.

*Picture.* A square UV picture with the ticks '0 → 1' across the top and '0 → 1' down the left side (y counts down, as everywhere in the film) and an outlined circle of radius 0.3 drawn in it, label 'square: round'. The square then stretches horizontally into a 2:1 rectangle and the circle stretches with it into an oval; the ticks across and down still read '0 → 1'. Labels 'wide: oval' and a small grey credit 'measured: 384 × 192 px · Godot 4.7.2 · Forward+'.

*Motion.* The square stretches into a wide rectangle and carries the circle with it into an oval while the tick labels stay 0 to 1.

*Lane.* manim · `B30_RoundOnSquare` · runner-up: ShaderLab: a real wide render

### B31 · 36 words · ~12 s

> Distance is another ramp, so everything so far applies. One minus a smooth step of the distance gives a soft spot of light. It is brightest in the middle and fades to nothing at the edge.

*Picture.* Code card at left (the seven-line shader); at right a real Godot window with a square picture: a soft white spot in the middle fading to black at the edges. Read-outs '1' in the middle and '0' near the edge.

*Motion.* The distance line is highlighted, then the glow line; read-outs land on the middle and the edge.

*Lane.* capture · `ShaderLab` · runner-up: manim: the three curves multiplied

*Capture to record.* C09: Lab square render of lab-shaders/09-glow.gdshader, still. Verified (360x360 Lab): middle 1.0; (0.75, 0.5) 0.5059; edge middle 0.0; corner 0.0.

### B32 · 44 words · ~15 s

> Power, written pow in code, raises each value to a power. On a ramp from zero to one, a power above one pulls the curve down, so only the far end stays bright. Below one, it pushes the curve up. Exactly one changes nothing.

*Picture.* The standard plot with three curves: the diagonal (power 1), a sagging curve (power 3) and a bowing curve (power 1/2), each labelled in mono ('x^3', 'x', 'x^0.5') and mono tag 'pow(x, y) · x to the power y'. The dot rides power 3 with a strip that is bright only near the right end; then power 1/2 with a brighter strip; then power 1 (the diagonal).

*Motion.* The dot rides the sagging curve and the strip stays dark until the far end; on the bowing curve the strip is bright early; on power 1 nothing changes.

*Lane.* manim · `B32_BendTheCurve` · runner-up: ShaderLab pow render

### B33 · 41 words · ~14 s

> In code, pow takes the ramp and a power. Turn the power up and the bright part squeezes toward the right edge, like a highlight tightening. Keep the first number at zero or above; the docs call a negative one undefined.

*Picture.* Code card at left (the eight-line shader with the power dial); at right a real Godot window with a black-to-white gradient whose bright part squeezes toward the right edge as the power is swept from 1 up to 6. The pow line carries the short label 'first number ≥ 0' (the docs' warning is in the voice).

*Motion.* The bright region shrinks toward the right edge while the voice says 'squeezes toward the right edge'.

*Lane.* capture · `ShaderLab` · runner-up: manim: the bright region shrinking

*Capture to record.* C10: Lab rect, lab-shaders/07-pow.gdshader; power held at 1 until 3.0 s, then 1 -> 6 over 3.0-11.0 s, held to 15.5 s; 30 fps, Forward+. Verified: power 1 -> 0.498 / 0.898 at x = 0.5 / 0.9; power 3 -> 0.1255 / 0.7255; power 6 -> 0.0157 / 0.5294.

### B34 · 33 words · ~11 s

> One more curve. Sine repeats smoothly, rolling between minus one and one. Half of sine, plus a half, squeezes it into zero to one. Think of it as the smooth cousin of fract.

*Picture.* A plot of sin over two cycles with the output from −1 to 1 and a dot riding it; range ticks −1 and 1. Mono tag 'sin(x) · a smooth wave between −1 and 1'. The curve is then squeezed and lifted into 0..1 ('0.5 + 0.5 · sin(x)') and the strip beneath shows two soft bands. A faint grey ghost of the fract saw teeth appears behind it with the caption 'smooth cousin'.

*Motion.* The wave rolls between −1 and 1, is squeezed into 0 to 1, and a ghost of fract's sharp teeth shows the smooth version beside it.

*Lane.* manim · `B34_SmoothRepeat` · runner-up: ShaderLab sine render

## Act V: Build a Ring

### B35 · 34 words · ~12 s

> Time to build. Take the distance to the middle and cut it with step at point three. Closer than that is zero, farther is one. The result is a circle: dark inside, light outside.

*Picture.* Act title 'Build a Ring' (serif 40) top-left. Code card at left (the six-line shader); at right a real Godot window with a square picture: a black disk on white. Read-outs '0' in the disk and '1' outside; a terracotta ring (grey-backed) round the disk's edge at the end.

*Motion.* The distance line, then the step line, are highlighted; the read-outs name the two sides and the ring marks the edge.

*Lane.* capture · `ShaderLab` · runner-up: manim: the cone cut at 0.3

*Capture to record.* C11: Lab square render of lab-shaders/10-disk.gdshader, still. Verified (360x360 Lab): middle 0; d = 0.2 -> 0; d = 0.4 -> 1; corner 1; the disk spans 0.6 of the width (216 of 360 px).

### B36 · 27 words · ~9 s

> Swap the two inputs and the circle flips: one inside, zero outside. The edge always comes first, so this reads: is the radius at least the distance?

*Picture.* Code card at left (the six-line shader with the arguments swapped); at right a real Godot window with a square picture: a white disk on black. Read-outs '1' inside and '0' outside.

*Motion.* The swapped step line is highlighted; the disk is now white inside; read-outs name the two sides.

*Lane.* capture · `ShaderLab` · runner-up: manim: the two argument orders side by side

*Capture to record.* C12: Lab square render of lab-shaders/11-disk-flip.gdshader, still. Verified (360x360 Lab): middle 1; d = 0.2 -> 1; d = 0.4 -> 0; corner 0. Edge case: step(0.3, 0.3) and step(0.3, 0.3) swapped are both 1 (function-tables: step_args_swapped).

### B37 · 38 words · ~13 s

> For a ring, cut twice and subtract. Step at point three is one from there outward. Step at point three eight is one from there outward. The first minus the second is one only in between: a pulse.

*Picture.* The standard plot with the input as the distance d from 0 to 0.7 (axis label 'distance'). Curve A: step(0.3, d) in light grey; curve B: step(0.38, d) in mid grey; then the bold curve A − B: a pulse of height 1 between d = 0.3 and 0.38. Mono tag 'ring = step(0.3, d) − step(0.38, d)'. Strip beneath: a bright band in the middle.

*Motion.* Curve A rises at 0.3, curve B rises at 0.38, and their difference is a one-wide pulse that lights a band on the strip.

*Lane.* manim · `B37_TwoCuts` · runner-up: ShaderLab ring render

### B38 · 37 words · ~13 s

> In code, that is step minus step. Here is the ring: a mask that is one on the ring and zero everywhere else. The edges are hard, since each pixel is either all in or all out.

*Picture.* Code card at left (the seven-line shader); at right a real Godot window with a square picture: a white ring on black with hard edges. Read-outs '1' on the ring and '0' in the middle; a terracotta ring (grey-backed) round a piece of the hard outer edge at the end.

*Motion.* The ring line is highlighted; read-outs name the mask's one and zero; the ring marks a hard edge.

*Lane.* capture · `ShaderLab` · runner-up: manim: the pulse spun around the middle

*Capture to record.* C13: Lab square render of lab-shaders/12-ring-hard.gdshader, still. Verified (360x360 Lab): d = 0.2 -> 0; 0.34 -> 1; 0.45 -> 0.

### B39 · 33 words · ~11 s

> Now color it with mix, using the ring as the weight. Where the mask is zero, you get cream. Where it is one, you get teal. The mask decides how much of each.

*Picture.* Code card at left (the nine-line shader); at right a real Godot window with a square picture: a teal ring on a cream background. Labels 'cream' on the background and 'teal' on the ring.

*Motion.* The mix line, then the cream line, then the teal line are highlighted as the voice names them; the two labels land on the picture.

*Lane.* capture · `ShaderLab` · runner-up: manim: a mix dial

*Capture to record.* C14: Lab square render of lab-shaders/13-ring-color.gdshader, still. Verified (360x360 Lab): d = 0.2 -> cream (0.9804, 0.9608, 0.9216); 0.34 -> teal (0.3686, 0.6392, 0.5686); 0.45 -> cream.

### B40 · 30 words · ~10 s

> Swap each step for a smooth step. Each edge now has a width, so the ring fades in and fades out instead of snapping. The same ring, with soft edges.

*Picture.* Code card at left (the ten-line shader); at right a real Godot window with a square picture: the same teal ring on cream, now with soft edges. A read-out 'soft' beside the outer edge; a terracotta ring (grey-backed) round the fading inner edge at the end.

*Motion.* The two smoothstep lines are highlighted, then the mix line; the read-out and ring mark the soft edge.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab hard and soft ring side by side

*Capture to record.* C15: Lab square render of lab-shaders/14-ring-soft.gdshader, still. Verified (360x360 Lab): d = 0.2 -> cream; 0.28 -> (0.6941, 0.8118, 0.7569) (half way); 0.34 -> teal; 0.40 -> (0.6431, 0.7843, 0.7255); 0.45 -> cream.

### B41 · 32 words · ~11 s

> Here is the finished shader. Distance makes the ramp, smooth step shapes it twice, mix paints it. The radius is a uniform, so your game can turn it, and the ring grows.

*Picture.* Code card at left (the twelve-line finished shader); at right a real Godot window with the soft teal ring from B40 that first holds still, then shrinks and grows as the radius dial is swept. Each highlighted line is named by the voice.

*Motion.* Each function's line lights up as it is named; then the ring grows as the radius is turned.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C16: Lab square render of lab-shaders/15-ring-final.gdshader; radius held at 0.30 until 6.0 s, then 0.30 -> 0.12 over 6.0-8.5 s, then 0.12 -> 0.38 over 8.5-11.5 s, held to 12.5 s; 30 fps, Forward+. Verified (360x360 Lab): radius 0.12 -> cream / teal / cream at d = 0.06 / 0.16 / 0.32 ... see lab-summary.txt; radius 0.3 -> teal at d = 0.34; radius 0.38 -> teal at d = 0.42.

## Closing

### BVDT · recap · 73 words · ~25 s

> Let's recap with Claude. A ramp is a smooth run from zero to one, and every function reshapes it. Step cuts, smooth step cuts softly, mix blends, clamp pins. Abs folds, fract repeats, floor counts, mod repeats at any length. Length and distance measure, normalize keeps a direction, power bends a curve. Distance, smooth step and mix together draw a ring. Read the line of a function and you can predict the picture.

*Picture.* The recap card: A ramp is a smooth run from zero to one, and every function reshapes it. / step cuts, smoothstep cuts softly, mix blends, clamp pins. / abs folds, fract repeats, floor counts, mod repeats at any length. / length and distance measure, normalize keeps a direction, pow bends a curve. / Distance, smoothstep and mix together draw a ring. / Read the line of a function and you can predict the picture.

### BHTF · your turn · 81 words · ~28 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a square Color Rect: a soft teal ring around the center, built from distance, smoothstep and mix. Give it one float uniform called radius, limited to a range that keeps the ring inside the square. Then tell me which line does which job. Then check two things yourself. Is the ring round and centered? And does the radius dial move the ring in and out, with soft edges?

*Prompt shown and read in full:* Write a Godot canvas item shader for a square Color Rect: a soft teal ring around the center, built from distance, smoothstep and mix. Give it one float uniform called radius, limited to a range that keeps the ring inside the square. Then tell me which line does which job.

*Two checks:* Check: the ring is round and centered in the square. · Check: the radius dial moves the ring in and out, with soft edges.

### BOUT · outro · 8 words · ~4 s

> The Shader Math Toolkit. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


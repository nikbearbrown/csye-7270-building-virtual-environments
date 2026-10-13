# Script: Trigonometry for Shaders

**What this is.** The words Liam will say in *Trigonometry for Shaders*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 46 beats, 1744 words, about **9:57** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: manim 23, capture 13, remotion 4.

**If it runs long.** Cut, in this order: the flower beat (B40), the three-moons beat (B23), the arm beat (B30) and the oval-limit beat (B24): each is a bonus that repeats an idea another beat already carries. Then the start-at-the-top beat (B39). The triangle-to-circle beats (B06, B07), the orbit (B19 to B21), the meteor (B26 to B29) and the worked pixel with the sweep (B37, B38) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | One Angle, Two Numbers | 5 | 193 | ~1:06 |
| II | Angle In, Position Out | 10 | 371 | ~2:06 |
| III | An Orbit | 10 | 361 | ~2:03 |
| IV | An Orbit Around an Orbit | 5 | 160 | ~0:54 |
| V | Angle from a Position | 10 | 374 | ~2:07 |

## Opening

### BOPEN · identity card · 28 words · ~10 s

> Trigonometry for Shaders. Learn what sine and cosine really do, then use them to send a moon around a planet and reveal a picture like a clock hand.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Trigonometry for Shaders", and the line "Turn an angle into a position, and back again".

### BIDEA · the question · 33 words · ~11 s

> Hallo. This is Liam, in for Bear. Most of us met trigonometry as triangles on paper, and forgot it. In a shader it does one job. It turns an angle into a position.

*Picture.* The hesitant writer types: "Trigonometry is for
triangles on paper." then deletes "triangles on paper" and types "turning angles into positions".

### BDEFS · terms · 58 words · ~20 s

> Five terms. An angle is an amount of turn. A radian is an angle measured so that a full turn is about six point two eight. The hypotenuse is the longest side of a right triangle. A vec two is a bundle of two numbers. And U V is a pixel's address, zero to one across and down.

*Picture.* "Terms In This Lecture": **Angle** — an amount of turn, in degrees or radians; **Radian** — an angle where a full turn is about 6.28; **Hypotenuse** — the longest side of a right triangle; **Vec2** — a bundle of two numbers; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down

## Act I: One Angle, Two Numbers

### B01 · 40 words · ~14 s

> A moon circles a planet, and a meteor circles the moon. Nobody animated it by hand. In the shader, an angle goes in, and two numbers come out that say where the moon is. Those numbers come from a triangle.

*Picture.* Act title 'One Angle, Two Numbers' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a teal planet in the middle, a slate-blue moon circling it clockwise and a small amber meteor circling the moon, all on the warm grey stage color. No code is shown yet.

*Motion.* The moon laps the planet and the meteor laps the moon, continuously, from the first frame.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a planet, moon and meteor on orbit rings

*Capture to record.* C01: Lab rect, lab-shaders/06-meteor-orbit.gdshader, square (480 x 480 logical canvas captured at 1920 x 1920), live TIME, 14 s, 30 fps, Forward+, no input. The moon laps the planet in 6.28 s, so about two laps show.

### B02 · 39 words · ~13 s

> Start with a triangle that has a right angle in one corner. Its longest side is the hypotenuse. Now pick another corner. The side across from it is the opposite side. The side touching it is the adjacent side.

*Picture.* A right triangle in grey outline on the cream stage, right angle at the lower right marked with a small square, the other angles at the lower left (30 degrees, marked by a thick terracotta arc and a small terracotta dot) and the top right. As each word is spoken the matching side thickens to ink and takes a 1 to 3 word serif label placed outside the outline: 'hypotenuse' on the long slanted side, 'opposite' on the right-hand vertical (across from the marked angle), 'adjacent' on the bottom (touching the marked angle). The 50 % frame holds the settled picture with the hypotenuse label and the marked angle.

*Motion.* Each side thickens and takes its name exactly when the voice says it.

*Lane.* manim · `B02_RightTriangle` · runner-up: LectureEvidenceTable (a three-row glossary)

### B03 · 39 words · ~13 s

> Here is the useful part. Fix the angle, and the ratio of any two sides stays fixed, whatever the size. At thirty degrees, the opposite side is always half the hypotenuse. At fifty, about point seven seven of it.

*Picture.* The same 30-degree triangle anchored at its marked lower-left corner. At the right, a readout in serif: 'opposite ÷ hypotenuse' over a large number. First the triangle scales (about 1.0, then 0.55, then 1.3) while thin grey ghosts of the earlier sizes stay nested at the same corner and the number stays 0.50 the whole time. After a hold (settled still at the 50 % frame: three nested outlines, '30°' and 0.50), the marked angle opens to 50 degrees: the hypotenuse swings up, the triangle reshapes, the angle label reads '50°' and the number settles at 0.77. A terracotta dot rides the top corner.

*Motion.* The triangle grows and shrinks and the number does not move; the angle opens and the number does.

*Lane.* manim · `B03_SameRatio` · runner-up: LectureEvidenceTable (angle against ratio, two rows)

### B04 · 35 words · ~12 s

> Those ratios have names. Opposite over hypotenuse is the sine. Adjacent over hypotenuse is the cosine. Opposite over adjacent is the tangent. The memory trick is S O H, C A H, T O A.

*Picture.* Left: the 30-degree triangle in grey, smaller. Right: three stacked outlined rows (padding, no fill behind text): 'sine · opposite ÷ hypotenuse', 'cosine · adjacent ÷ hypotenuse', 'tangent · opposite ÷ adjacent'. As each name is spoken its row lands and the two sides it uses thicken to ink on the triangle (sine: opposite and hypotenuse; cosine: adjacent and hypotenuse; tangent: opposite and adjacent) while the others return to grey. At the end 'SOH CAH TOA' sets under the rows with each first letter aligned to its row.

*Motion.* Two sides of the triangle light up for each ratio as the voice names it.

*Lane.* manim · `B04_SohCahToa` · runner-up: LectureEvidenceTable

### B05 · 40 words · ~14 s

> So sine and cosine are lookups. Hand one an angle, and it hands back a ratio. Sine of thirty degrees is one half. Cosine of thirty degrees is about point eight seven. An angle goes in, a number comes out.

*Picture.* Two outlined boxes stacked on the cream stage, labelled 'sine' (upper) and 'cosine' (lower). At the left a small wedge token marked '30°' slides along a short drawn arrow into the sine box; a number token '0.50' slides out at the right. The same 30-degree token then enters the cosine box and '0.87' leaves it. One short line under the boxes: 'angle in, number out'. Arrows are drawn shapes, not glyphs; the 50 % frame holds with the sine result '0.50' settled.

*Motion.* A 30-degree token enters each box and a number leaves it.

*Lane.* manim · `B05_Lookup` · runner-up: DesignPipelineClaim, show-tell isometric

## Act II: Angle In, Position Out

### B06 · 35 words · ~12 s

> Now put that triangle inside a circle. Walk out from the middle at your angle until you reach the circle. The triangle's two short sides say where you stand: so far across, so far up.

*Picture.* Act title 'Angle In, Position Out' (serif 40) top-left. On paper orientation (y up, a small grey caption 'on paper'): a circle with a faint cross of axes, 'radius 1' on a radius. A radius line sweeps from the right-hand axis up to 30 degrees and a terracotta dot lands on the circle where it ends. Then the triangle from before draws in: a dashed vertical drop from the dot to the horizontal axis and the horizontal leg along the axis. The marked angle is a thick terracotta arc, never a filled wedge.

*Motion.* The radius turns to the angle, the dot lands on the circle, and the triangle's two short sides drop from it.

*Lane.* manim · `B06_UnitCircle` · runner-up: ShaderLab (a shader drawing a circle)

### B07 · 41 words · ~14 s

> Make the radius one and you have the unit circle. The hypotenuse is one, so dividing by one changes nothing. The opposite side is the sine itself, the adjacent side the cosine itself. The point sits at cosine across, sine up.

*Picture.* The same circle, dot and triangle (paper orientation, y up, as in the previous beat). The tag 'unit circle' lands beside the circle. The horizontal leg takes the label 'cos' and the vertical leg 'sin'; the hypotenuse keeps 'radius 1'. Beside the circle a live readout in serif: 'cos 0.87' over 'sin 0.50'. A faded '÷ 1' on each ratio shrinks away as the voice says dividing by one changes nothing. After a hold (settled at 30 degrees through the midpoint) the angle swings to 60 degrees and back to 30, the legs resizing and both readout numbers following (0.50 and 0.87 at 60 degrees); the point label '(cos, sin)' sits at the dot.

*Motion.* As the angle opens, the two legs and the two readout numbers change together: the point's across and up are exactly the cosine and sine.

*Lane.* manim · `B07_LegsAreCosSin` · runner-up: LectureEvidenceTable

### B08 · 39 words · ~13 s

> Godot's own manual says the same. Vector two has a function, from angle, that builds a point from an angle. The manual calls it equivalent to cosine of the angle, sine of the angle. The engine knows the recipe.

*Picture.* The real Godot 4.7 Vector2 class page scrolled to from_angle(); the camera pushes in on the sentence 'This is equivalent to doing Vector2(cos(angle), sin(angle)) or Vector2.RIGHT.rotated(angle).' and one terracotta ring marks it. The move and ring coordinates are set from the real screenshot at build time.

*Motion.* The camera pushes in on the sentence the voice is describing and a terracotta ring marks it.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: GDScript line Vector2.from_angle(a) beside Vector2(cos(a), sin(a))

### B09 · 33 words · ~11 s

> Want a bigger circle? Multiply by the radius. Want it somewhere else? Add the center. So center plus radius times cosine and sine puts a point on a circle of any size, anywhere.

*Picture.* The circle from before (paper orientation, y up) with its terracotta dot at 30 degrees. A formula builds under it, term by term, in the monospace face (32 or larger): 'c + r * vec2(cos(a), sin(a))'. As 'r *' lands the circle grows from radius 1 to 1.8 with the dot riding on it at the same angle; as 'c +' lands the whole circle slides to a new center (a small terracotta cross marks the center and travels with it). The 50 % frame holds the grown and moved circle with the whole formula landed.

*Motion.* The circle grows when the radius lands and slides when the center lands, with the dot riding along at the same angle.

*Lane.* manim · `B09_RadiusAndCenter` · runner-up: LectureCodeTrace (the formula as code)

### B10 · 38 words · ~13 s

> Try one by hand. Radius point six, angle thirty degrees. The first number is point six times cosine, about point five two. The second is point six times sine, exactly point three. Hold on to those two numbers.

*Picture.* A circle drawn as a labelled ring of radius 0.6 (the number 0.6 on its axis) with the terracotta dot at 30 degrees. Two lines of arithmetic build beside it as the voice reads them, serif 32 or larger: '0.6 × cos 30° = 0.52' (the horizontal drop lights up in ink) and '0.6 × sin 30° = 0.30' (the vertical drop lights up). The two results end boxed together as '(0.52, 0.30)' beside the dot with a small grey line 'hold on to these'. Paper orientation (up positive); the dot is not mirrored.

*Motion.* The two drops light up in turn as each product is read, and the two results meet as one point.

*Lane.* manim · `B10_WorkedExample` · runner-up: LectureCodeTrace (the two lines of code)

### B11 · 41 words · ~14 s

> One catch. Shaders measure angles in radians, not degrees. Lay one radius along the edge of the circle, and the angle it covers is a radian. A full turn takes a little over six of them: about six point two eight.

*Picture.* A circle (paper orientation, y up) with its radius drawn as a thick ink bar from the middle. The bar copies itself onto the circle's edge as a bent arc of exactly its own length, starting at the right-hand axis; a thick terracotta arc marks the angle it covers, labelled 'radian' (a thick arc, never a filled wedge). Copies lay end to end around the circle while a counter ticks 1, 2, 3, 4, 5, 6, and a short leftover piece closes the loop; the label ends '6.28 = a full turn'. The 50 % frame holds with about three copies laid and the counter at 3.

*Motion.* The radius is laid end to end around the circle: six whole copies and a short remainder.

*Lane.* manim · `B11_Radians` · runner-up: plot / ramp strip with a marker

### B12 · 34 words · ~12 s

> Godot names the big ones. Pi is half a turn. Tau is a full turn, which is two pi. And the function radians converts degrees, so forty-five degrees comes out as pi over four.

*Picture.* The same circle after the walk (paper orientation: the sweep goes counterclockwise, y up). A radius sweeps once round from the right-hand axis; tick marks land at the quarter points in turn with code-font labels: 'PI / 2' at the top, 'PI' at the left, '3 * PI / 2' at the bottom and 'TAU' back at the start. Then a wedge outline of 45 degrees draws and a line appears beside the circle: 'radians(45.0)' = 'PI / 4.0'. A small grey credit line under it: 'Godot 4.7 docs · Global built-ins'. The 50 % frame holds with the sweep finished and all four labels landed.

*Motion.* The radius sweeps once round, dropping a label at each quarter, then a 45-degree wedge is named pi over four.

*Lane.* manim · `B12_PiTau` · runner-up: BrowserCapture of the docs page

### B13 · 39 words · ~13 s

> Skip the conversion and the shader still compiles. That is the trap. Thirty radians is almost five full turns, so sine of thirty comes out near minus one. Convert first, and sine of thirty degrees is one half again.

*Picture.* Two small circles side by side on the cream stage (paper orientation, y up). Left, titled 'sin(30.0)': a terracotta dot spins round the circle again and again with a turn counter ticking 1, 2, 3, 4 and stops a little short of the fifth turn near the bottom, with a mid-grey bar beside it (never a dark ink bar) that settles at '-0.99'. Right, titled 'sin(radians(30.0))': the dot moves a short way up to a 30-degree mark and its mid-grey bar shows '0.50'. A small grey credit line: 'math values · checked in a Godot 4.7.2 shader'. The 50 % frame holds with the left dot stopped near the bottom and its counter at 4; the left bar settles just after.

*Motion.* The left dot spins almost five times before it stops near the bottom; the right dot moves a short way.

*Lane.* manim · `B13_DegreesTrap` · runner-up: ShaderLab (two swatches in a real render)

### B14 · 36 words · ~12 s

> Why is sine a wave? Plot the point's height against its angle as it goes round. The height climbs to one, falls through zero to minus one, and comes home. That curve is the sine wave.

*Picture.* Left: the circle with its terracotta dot (paper orientation, y up). Right: a plot with the angle along the bottom (faint ticks at pi/2, pi, 3pi/2, tau) and 'height' up the side. As the dot goes once round, a thin dashed line runs from the dot across to the plot and a curve draws behind it: up to 1, back through 0, down to -1, home. The finished curve is labelled 'sine'. The 50 % frame holds with the dot at the left of the circle (half turn) and the curve drawn to pi.

*Motion.* A dashed line carries the dot's height across to a curve that grows into the sine wave as the dot goes round.

*Lane.* manim · `B14_SineWave` · runner-up: ShaderLab (a shader drawing the wave)

### B15 · 35 words · ~12 s

> Cosine is the across distance, and it draws the same wave, a quarter turn earlier. When one is at its peak, the other is at zero. Two waves, a quarter turn apart, make a circle.

*Picture.* The plot from before with the sine curve in ink. A second curve, cosine, draws in a lighter grey-brown starting at 1 and peaking a quarter turn before sine; a bracket between the two peaks reads 'quarter turn'. A vertical cursor then sweeps along the angle axis; at each position two small dots ride the two curves while, on a small circle at the left, a dot at (cos, sin) is placed by those two values and traces the circle. The 50 % frame holds with both curves drawn and the bracket.

*Motion.* Two curves a quarter turn out of step set a dot's across and up together, and the dot traces the circle.

*Lane.* manim · `B15_CosineShift` · runner-up: LectureEvidenceTable (sine against cosine at four angles)

## Act III: An Orbit

### B16 · 39 words · ~13 s

> Now a shader. It runs once for each pixel, and U V says where that pixel is. Double it and subtract one, and the range becomes minus one to one, with zero, zero in the middle. Call that p.

*Picture.* Act title 'An Orbit' (serif 40) top-left. A square drawn the shader way (the second number counts DOWN, small grey 'y' arrow pointing down): corner labels (0, 0) top left and (1, 1) bottom right, a terracotta dot at the middle labelled (0.5, 0.5) and a short tag 'UV'. A small code card lands beside it with 'void fragment() {', the line 'vec2 p = UV * 2.0 - 1.0;' and '}', and a 3-word tag 'once per pixel' on the function line. As the line lands the labels slide to the centered numbers: corners (-1, -1) and (1, 1), middle (0, 0); the dot visits the top-left corner and the middle, showing both numbers. The 50 % frame holds with the line landed and the labels still 0 to 1.

*Motion.* The square's labels slide from 0 to 1 to minus one to one while the dot stays put.

*Lane.* manim · `B16_CenterAddress` · runner-up: ShaderLab (code beside a render that colors p)

### B17 · 35 words · ~12 s

> The planet is a distance test. Length of p is how far a pixel sits from the middle. Under the radius, paint planet color. A circle is every point at one distance from its center.

*Picture.* The centered square (screen orientation, y down) as a 12-by-12 grid of outline-only cells (no fill behind text). A faint teal circle of radius 0.25 (of the half-width) outlines the planet at the middle. A terracotta probe dot starts at the middle and moves outward along a drawn line; a live readout 'length(p) 0.10 ... 0.25 ... 0.40' follows it. When the readout passes 0.25 the probe's own cell changes from teal to the stage grey; at the end every cell whose center is inside the circle is tinted teal. A code line lands under the grid: 'if (length(p) < 0.25)'. The 50 % frame holds with the probe inside the circle and the readout at about 0.20.

*Motion.* The probe moves out from the middle, its length readout grows, and its cell flips from planet to stage at exactly 0.25.

*Lane.* manim · `B17_Planet` · runner-up: ShaderLab still of the planet

### B18 · 39 words · ~13 s

> The moon is the same test around another center. That center is point six times cosine and sine of an angle. Distance measures how far apart two points are: within point zero eight of it, a pixel is moon.

*Picture.* The shader file as a code card on the cream stage (the card the next beat shows beside its render). Focus lands on the planet test, then on the moon's center line and its angle line, then on the distance test with the label 'distance: how far apart two points are', and finally on the COLOR line with the label 'COLOR: the pixel's color'. No render yet.

*Motion.* Line focus steps from the planet test to the moon's center to the distance test.

*Lane.* remotion · `ShaderLab` · runner-up: LectureCodeTrace (about ten lines fit; this file has eleven and a different look)

### B19 · 30 words · ~10 s

> Run it at thirty degrees. Across, point five two, as calculated. But the second number, point three, put the moon below the middle, not above. That is the next catch.

*Picture.* Code card at the left with the focus stepping from the angle line to the moon line; at the right a real Godot window (square) with a teal planet in the middle and the slate-blue moon at the lower right, right of the middle and BELOW the middle line. Readouts land: '0.52 across' above the moon's column, then a terracotta ring on the moon and '0.30 down'.

*Motion.* The moon is already at the predicted spot, and a ring and a '0.30 down' readout show it sits below the middle line.

*Lane.* capture · `ShaderLab` · runner-up: manim: the p-square with the predicted dot

*Capture to record.* C02: Lab rect, lab-shaders/01-moon-fixed.gdshader, still PNG (480 x 480 captured at 1920 x 1920), Forward+. Probes: moon (0.502, 0.600, 0.749) at uv (0.7598, 0.65); the y-up mirror spot (0.7598, 0.35) is empty stage (0.851, 0.839, 0.788); planet (0.369, 0.639, 0.569) at the middle.

### B20 · 34 words · ~12 s

> On paper, up is positive. On a screen, y counts downward. The formulas stay the same and the picture flips: down is a quarter turn, and a growing angle turns clockwise. Godot's manual agrees.

*Picture.* Two circles side by side, each with the same terracotta dot at a quarter turn. Left, labelled 'on paper': the y axis arrow points UP and the dot sits at the top. Right, labelled 'on a screen': the y axis arrow points DOWN and the dot sits at the bottom. The left circle flips top-to-bottom into the right one (the dot rides the flip); then on the right the dot travels a full turn and a thick terracotta arc arrow shows the direction: clockwise. A small grey credit: 'Godot docs · y is down in 2D'. The 50 % frame holds with both circles and the flipped dot settled.

*Motion.* One circle turns over into the other, and the dot on it then runs clockwise.

*Lane.* manim · `B20_Flip` · runner-up: BrowserCapture of the Vector2 docs (DOWN.angle() = PI / 2)

### B21 · 33 words · ~11 s

> Now let the angle be time, the game's clock in seconds. As time counts up, the angle grows, and the moon goes round, clockwise. One line changed, and nothing is animated by hand.

*Picture.* Code card at the left with the changed line 'float a = TIME;' focused; at the right the real Godot window: the planet in the middle and the moon circling it clockwise on its own, one lap in 6.28 s. A 'clockwise' readout lands under the orbit.

*Motion.* The moon goes round clockwise while the code is on screen, with no animation in the file.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dot going round a circle

*Capture to record.* C03: Lab rect, lab-shaders/02-orbit.gdshader, square, live TIME, 14 s, 30 fps, Forward+. Measured: the moon turns clockwise at +0.99 to +1.00 rad/s at a constant 0.600 of the half-width (batch run, 4 intervals).

### B22 · 30 words · ~10 s

> Scale the time and you scale the speed. Time times two, and the moon goes round twice as fast. The speed of an orbit is how fast the angle grows.

*Picture.* Code card at the left with 'float a = TIME * 2.0;' focused; at the right the same scene with the moon going round visibly faster, a lap every 3.14 s. Caption under the window: 'one lap every 3.14 s · before: 6.28 s'.

*Motion.* The moon laps the planet twice as fast as in the previous clip.

*Lane.* capture · `ShaderLab` · runner-up: manim: two moons at different speeds

*Capture to record.* C04: Lab rect, lab-shaders/03-orbit-fast.gdshader, square, live TIME, 12 s, 30 fps, Forward+. Measured +2.00 rad/s clockwise (batch run, 3 intervals).

### B23 · 42 words · ~14 s

> An angle names a spot on the circle, so you can add to it. Add a third of a turn, tau over three, and a moon sits a third of the way round. Loop three times, and three moons sit evenly spaced.

*Picture.* Code card at the left (a 'for' loop of three) with the line 'float a = TIME + float(i) * TAU / 3.0;' focused, then the 'for' line; at the right the real window: the planet and three slate-blue moons circling together, always a third of the way round from each other. Readouts land: 'TAU / 3' then '120° apart'.

*Motion.* Three moons circle as a rigid triple, each a third of a turn behind the next.

*Lane.* capture · `ShaderLab` · runner-up: manim: three dots on a ring

*Capture to record.* C05: Lab rect, lab-shaders/05-moons-evenly.gdshader, square, live TIME, 12 s, 30 fps, Forward+. Measured: three moons with gaps of 120.0, 120.0, 120.0 degrees at two times (batch run).

### B24 · 43 words · ~15 s

> One limit: the shape has been a square. On a wide one, U V still runs zero to one both ways, so circles come out oval. Scale p's x by width over height, passed in as a uniform, and they are round again.

*Picture.* Layout stacked: a real wide (16:9) Godot window above the code card. The planet is an oval and the moon's orbit is stretched sideways; as the line 'p.x *= aspect;' is focused the capture raises the aspect uniform from 1.0 to 1.78 and the planet and orbit turn round. Then the uniform line is focused with the caption 'uniform: a value your game sets from outside'. A readout 'aspect 1.78' lands once the circle is round.

*Motion.* The oval planet and orbit turn into true circles as the aspect number rises to width over height.

*Lane.* capture · `ShaderLab` · runner-up: manim: an oval and a circle in the same square

*Capture to record.* C06: Lab rect, lab-shaders/04-orbit-aspect.gdshader on a 640 x 360 logical canvas captured at 1920 x 1080, live TIME, 16 s, Forward+. aspect holds 1.0 until 0.58 of the beat, rises linearly to 1.7778 by 0.82, holds. Measured: planet 160 x 90 px at aspect 1.0 (ratio 1.778) and 90 x 90 px at aspect 1.7778 (batch run).

### B25 · 36 words · ~12 s

> That is the whole recipe: a center, a radius, and an angle that grows. The radius sets the size. The center sets the place. The angle's speed sets the pace. Change one and the orbit follows.

*Picture.* At the left the planet and the moon on its ring (screen orientation, y down), drawn flat in the same teal and slate-blue as the renders. Across the top the line 'center + radius * vec2(cos(a), sin(a))' with three parts tinted in turn ('center', 'radius', 'a'). Beside it three small outlined sliders with knobs, labelled 'radius', 'center' and 'speed' (1 to 3 words each). As the voice names each part its slider's knob turns and the orbit responds: the ring grows (0.4 to 0.8), then the whole orbit slides to the right, then the moon speeds up (a pair of small speed marks). The 50 % frame holds with the ring grown.

*Motion.* Each knob turns in turn and the orbit grows, slides, then speeds up.

*Lane.* manim · `B25_Recipe` · runner-up: ShaderLab (the orbit shader with three uniforms swept)

## Act IV: An Orbit Around an Orbit

### B26 · 36 words · ~12 s

> Now a meteor around the moon. The moon moves, so the meteor's center moves with it. Take the moon's position and add the meteor's own circle on top. Positions add, so circles can ride on circles.

*Picture.* Act title 'An Orbit Around an Orbit' (serif 40) top-left. Screen orientation (y down), the same teal planet and slate-blue moon as the renders: the planet in the middle, the moon on its ring, and a smaller ring around the moon with the amber meteor on it. A thick ink arrow runs from the planet to the moon and a second, shorter ink arrow from the moon to the meteor, tip to tail, labelled 'moon' and 'meteor' (1 word each). Both angles advance: the second arrow's tail stays on the moon's tip, the small ring rides along, and a dashed line from the planet to the meteor follows. The 50 % frame holds with both arrows and the dashed line settled.

*Motion.* The short arrow stays attached to the moving tip of the long one, so the meteor's small circle rides around the moon's big one.

*Lane.* manim · `B26_Chain` · runner-up: ShaderLab

### B27 · 36 words · ~12 s

> In code, that is one more line. The meteor is the moon plus a small radius times cosine and sine of its own angle. Give that angle time times three, and the meteor outpaces the moon.

*Picture.* The meteor shader as a code card on the cream stage (fourteen lines). Focus lands on 'vec2 meteor = moon + 0.2 * vec2(cos(b), sin(b));', then on that line together with its angle line, then on 'float b = TIME * 3.0;'. No render.

*Motion.* Line focus lands on the new meteor line and then on its angle.

*Lane.* remotion · `ShaderLab` · runner-up: LectureCodeTrace (about ten lines fit; this file has fourteen)

### B28 · 27 words · ~9 s

> Watch it run. The meteor laps the moon three times for every lap the moon makes around the planet. Two ordinary circles, one riding on the other.

*Picture.* A real Godot render filling the framed window: the teal planet, the slate-blue moon on its orbit and the amber meteor circling the moon, clearly faster. Caption under the window: 'meteor angle TIME * 3.0 · moon angle TIME'. Readout 'three to one' lands near the bottom.

*Motion.* The meteor circles the moon three times for every lap the moon makes around the planet.

*Lane.* capture · `ShaderLab` · runner-up: manim: orbit with a path trail

*Capture to record.* C07: Lab rect, lab-shaders/06-meteor-orbit.gdshader, square, live TIME, 14 s, 30 fps, Forward+ (same file as C01). Measured: moon +1.00 rad/s around the planet; meteor +3.00 rad/s around the MOON (batch run).

### B29 · 26 words · ~9 s

> Negate the meteor's angle, and it circles the other way while the moon keeps its direction. The minus sign mirrors the point. Same circle, opposite spin.

*Picture.* Code card at the left with 'float b = -TIME * 3.0;' focused; at the right the real window: the moon still going clockwise around the planet while the meteor circles the moon the other way (counterclockwise on screen). Readout 'meteor reversed' lands.

*Motion.* The meteor turns counterclockwise around the moon while the moon keeps turning clockwise.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills of both directions

*Capture to record.* C08: Lab rect, lab-shaders/07-meteor-reverse.gdshader, square, live TIME, 14 s, 30 fps, Forward+. Measured: moon +1.00 rad/s, meteor around the moon -3.00 rad/s (batch run).

### B30 · 35 words · ~12 s

> Any depth works. Each level is a center plus a radius times cosine and sine of an angle. Chain two, and you have an arm with an elbow. Chain three, and you have a tentacle.

*Picture.* A two-segment arm in ink: a fixed shoulder (terracotta dot), a first segment to an elbow, a second segment to a hand. The two segment angles drift in turn so the arm waves. Beside it the pattern line 'center + radius * vec2(cos(a), sin(a))' appears once per segment; for the second segment the word 'center' is replaced by 'elbow'. Then a third segment grows from the hand (a tentacle) and the whole chain waves. Labelled 'elbow' and 'hand' (1 word each). The 50 % frame holds with the two-segment arm and both pattern lines.

*Motion.* Each segment starts where the last one ended, so adding a segment adds one more circle's worth of motion.

*Lane.* manim · `B30_Arm` · runner-up: ShaderLab (a three-segment chain in a shader)

## Act V: Angle from a Position

### B31 · 31 words · ~10 s

> So far an angle went in and a position came out. Now run it backwards. A pixel knows where it is. What angle does it sit at, seen from the middle?

*Picture.* Act title 'Angle from a Position' (serif 40) top-left. A circle drawn the screen way (small grey axes, the y arrow pointing DOWN) with a terracotta dot at a fixed place at the lower right. Along the top a drawn arrow shape (not a glyph) runs left to right labelled 'angle in, position out' while a thick arc grows from the right-hand axis to the dot; then a second arrow shape runs back along the bottom labelled 'position in, angle out', and a question mark sits on the arc and turns into the word 'angle'. The 50 % frame holds with the forward arrow done and the arc drawn.

*Motion.* A forward arrow runs once, then a backward arrow runs and the angle becomes the unknown.

*Lane.* manim · `B31_TwoWays` · runner-up: FormACard

### B32 · 36 words · ~12 s

> Tangent was opposite over adjacent. Arc tangent undoes it: give it the two sides, and it hands back the angle. For a pixel, the two sides are how far across it sits and how far down.

*Picture.* Screen orientation (y down). A pixel dot at the lower right of the middle (p = (0.5, 0.35)); a right triangle from the middle whose legs are first labelled 'opposite' and 'adjacent' (the first act's words), and a thick terracotta arc at the middle for the angle labelled 'angle?'. A function box 'arc tangent' lands at the right; the two leg numbers travel into it and an arrow carries 'angle' out, the arc's label changing from 'angle?' to '0.61 rad'. After a hold, the leg labels change to 'down' and 'across' for a pixel. The 50 % frame holds with the box settled and the old labels.

*Motion.* The two legs travel into a box and the angle comes out the other side.

*Lane.* manim · `B32_AtanIdea` · runner-up: LectureCodeTrace (atan(p.y, p.x))

### B33 · 37 words · ~13 s

> In a shader, arc tangent takes two numbers: y first, then x. Their signs pick the quarter of the circle, so the answer covers the whole turn, from minus pi to pi. Godot's reference says exactly that.

*Picture.* The real Godot 4.7 built-in functions page scrolled to the two-argument atan(y, x) entry; the camera pushes in on its description ('Calculates the arc tangent given a numerator and denominator. The signs of y and x are used to determine the quadrant that the angle lies in.') and the return line ('in the range [-PI, PI]'), and one terracotta ring marks them. Coordinates are set from the real screenshot at build time.

*Motion.* The camera pushes in on the entry's description and range while the voice reads them.

*Lane.* remotion · `BrowserCapture` · runner-up: LectureCodeTrace: atan(p.y, p.x)

### B34 · 41 words · ~14 s

> Zero is straight right. Straight down is half pi, a quarter turn clockwise. Straight left is where it wraps: nearly plus pi right below that line, nearly minus pi right above it. Past the wrap, straight up is minus half pi.

*Picture.* Screen orientation circle (y down) with a terracotta dot at the right-hand axis and a readout box at the side titled 'arc tangent' with the live number. The dot walks clockwise a full turn in the order the voice says it, pausing at each compass point while the readout lands: right '0', down '1.57', then on to just below the left axis where the readout has climbed to 3.14; once the dot passes the left axis the readout JUMPS to -3.14 (a brief flash on the jump); then up '-1.57', and back to '0' at the right. A short thick mark on the left axis is labelled 'seam'. The 50 % frame holds with the dot paused just below the left axis and the readout at 3.14.

*Motion.* The readout climbs to 3.14 as the dot nears the left, jumps to -3.14 as it passes, and climbs back to zero.

*Lane.* manim · `B34_Compass` · runner-up: ShaderLab (the angular color picture)

### B35 · 40 words · ~14 s

> See it as a picture. Divide by tau and add one half, and minus pi to pi becomes zero to one. Then mix from teal at zero to amber at one. The hard edge on the left is the seam.

*Picture.* Code card at the left with the line 'float t = atan(p.y, p.x) / TAU + 0.5;' focused, then the COLOR line; at the right a real Godot window with a conic color picture: teal at the start, amber at the end, a hard edge along the left half of the horizontal axis (the seam). A thin 0 to 1 ramp under the render with a marker that sweeps from teal to amber, and a terracotta ring on the seam at the end. Caption: 'mix: blend two colors by a number from 0 to 1'.

*Motion.* The ramp marker sweeps from zero to one under the picture, then a ring settles on the hard edge at the left.

*Lane.* capture · `ShaderLab` · runner-up: manim: a color wheel

*Capture to record.* C09: Lab rect, lab-shaders/08-atan-colors.gdshader, still PNG (480 x 480 captured at 1920 x 1920), Forward+. Probes: right (0.635, 0.643, 0.412), down (0.769, 0.647, 0.329), up (0.502, 0.643, 0.490); just above the left axis teal (0.373, 0.639, 0.569), just below amber (0.898, 0.651, 0.251).

### B36 · 33 words · ~11 s

> A common slip is passing one number, y divided by x. Dividing throws away the signs, so opposite directions get the same answer, and the left half repeats the right. Pass both numbers.

*Picture.* Code card at the left with the changed line 'float t = atan(p.y / p.x) / PI + 0.5;' focused; at the right a real Godot window with a butterfly-like color picture: the upper-left and lower-right quadrants are identical, and so are the upper-right and lower-left. Two terracotta rings land in turn on opposite quadrants with the readout 'same' in each.

*Motion.* Rings land on opposite quadrants in turn and both read 'same'.

*Lane.* capture · `ShaderLab` · runner-up: manim: two opposite arrows with equal arcs

*Capture to record.* C10: Lab rect, lab-shaders/09-atan-one-argument.gdshader, still PNG (480 x 480 captured at 1920 x 1920), Forward+. Probes: lower right and upper left both (0.769, 0.647, 0.329); upper right and lower left both (0.502, 0.643, 0.490). The docs say it too: 'cannot determine with certainty in which quadrant the angle falls'.

### B37 · 40 words · ~14 s

> Work one pixel. Up and to the left, at minus point three, minus point three. Arc tangent says minus three quarters of pi. Divide by tau: minus point three seven five. Add one half: point one two five. One eighth.

*Picture.* The centered square (screen orientation) with one terracotta dot at p = (-0.3, -0.3), up and to the left, labelled 'p'. Three lines of arithmetic build beneath it as the voice reads them, in the monospace face (32 or larger): 'atan(-0.3, -0.3) = -3 * PI / 4', then '÷ TAU = -0.375', then '+ 0.5 = 0.125'. The last result lands on a thin 0-to-1 ramp strip drawn under the square as a terracotta marker at 0.125 labelled '1/8'. The 50 % frame holds with the first line done.

*Motion.* The three lines of arithmetic build in turn and the result lands as a marker on the ramp.

*Lane.* manim · `B37_WorkedPixel` · runner-up: LectureCodeTrace

### B38 · 40 words · ~14 s

> Now compare. A uniform is a number your game sets from outside, and this one is called sweep. If a pixel's number is below sweep, show the picture. Raise sweep from zero to one, and a clock hand reveals it.

*Picture.* Code card at the left (the sweep uniform, the comparison, the texture line) with focus stepping uniform line, comparison and texture lines, then the comparison again; at the right a real Godot window: the teal test sprite is revealed by a growing wedge from the left, over the top and round, like a clock hand. A thin 0 to 1 ramp under the render whose marker rides the sweep value. Caption: 'uniform: a value your game sets from outside'.

*Motion.* The wedge grows clockwise from the left as the ramp marker rises from 0 to 1.

*Lane.* capture · `ShaderLab` · runner-up: manim: a wedge growing on a circle

*Capture to record.* C11: Lab sprite (test sprite scaled to fit, square 480 x 480 captured at 1920 x 1920), lab-shaders/10-sweep.gdshader, Forward+, 16 s, scripted sweep: 0.30 until 0.68 of the beat (a partial reveal, so the window is never empty while the uniform and the test are explained), then 0.0 and a linear rise to 1.0 by 0.97 (the beat's cue 'Raise sweep'). Verified: at sweep 0.5 the upper half of the blob is shown (UL, UR) and the lower half hidden (LR, LL); the worked pixel appears between sweep 0.12 and 0.13.

### B39 · 35 words · ~12 s

> That hand starts at nine o'clock, where the seam is. To start at twelve, move the seam: add a quarter turn, point two five, and keep only the part after the decimal point, with fract.

*Picture.* Code card at the left with the changed line 'float t = fract(atan(p.y, p.x) / TAU + 0.25);' focused; at the right the same reveal, now starting at the top (twelve o'clock) and going clockwise. A terracotta ring marks the start line at the top and a readout '12 o'clock' lands.

*Motion.* The wedge now grows clockwise from the top instead of from the left.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab still of both starts side by side

*Capture to record.* C12: Lab sprite, lab-shaders/11-sweep-top.gdshader, square, Forward+, 16 s, scripted sweep: 0.30 until 0.60 of the beat (a partial reveal from twelve o'clock), then 0.0 and a linear rise to 1.0 by 0.97. Verified at sweep 0.5: the right half is shown (UR, LR) and the left half hidden (UL, LL).

### B40 · 41 words · ~14 s

> The angle is a number, so feed it to cosine again. Multiply it by eight, and the edge of a circle swells and shrinks eight times as you go round: a flower. Subtract time from the angle, and the flower turns.

*Picture.* Code card at the left with the angle line, then 'float edge = 0.55 + 0.15 * cos(8.0 * (a - TIME));' focused; at the right a real Godot window: a teal flower with eight rounded petals on the stage, turning clockwise at one radian per second. Readout '8 petals' lands.

*Motion.* A teal eight-petal flower turns steadily, its edge swelling and shrinking eight times round.

*Lane.* capture · `ShaderLab` · runner-up: manim: a polar plot of the radius against the angle

*Capture to record.* C13: Lab rect, lab-shaders/12-flower.gdshader, square, live TIME, 14 s, 30 fps, Forward+. Measured: edge radius between 0.398 and 0.700 (expected 0.40 to 0.70); the pattern turns +1.00 rad/s clockwise; 32 edge probes for a 8-petal static twin all PASS.

## Closing

### BVDT · recap · 76 words · ~26 s

> Let's recap with Claude. An angle fixes the ratios of a right triangle: sine, cosine and tangent. On the unit circle, cosine and sine are the point at an angle: angle in, position out. Shader angles are radians, and a full turn is tau. An orbit is a center, a radius and an angle that grows. A circle's center can itself be on an orbit. Arc tangent runs it backwards: a position gives back its angle.

*Picture.* The recap card: An angle fixes the ratios of a right triangle: sine, cosine and tangent. / On the unit circle, cosine and sine are the point at an angle: angle in, position out. / Shader angles are radians, and a full turn is tau. / An orbit is a center, a radius and an angle that grows. / A circle's center can itself be on an orbit. / Arc tangent runs it backwards: a position gives back its angle.

### BHTF · your turn · 83 words · ~28 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a square Color Rect: a teal planet in the middle and a smaller moon that circles it once every four seconds. Place the moon with cosine and sine of an angle in radians, and point me to the line that sets the speed. Then check two things yourself. Does the moon finish a lap in about four seconds? And does it turn clockwise, so that negating the angle reverses it?

*Prompt shown and read in full:* Write a Godot canvas item shader for a square Color Rect: a teal planet in the middle and a smaller moon that circles it once every four seconds. Place the moon with cosine and sine of an angle in radians, and point me to the line that sets the speed.

*Two checks:* Check: the moon completes one lap in about four seconds. · Check: it turns clockwise, and negating the angle reverses it.

### BOUT · outro · 7 words · ~4 s

> Trigonometry for Shaders. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


# Script: Time and Waves

**What this is.** The words Liam will say in *Time and Waves*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 46 beats, 1679 words, about **9:35** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 18, manim 18, remotion 4.

**If it runs long.** Cut, in this order: the two-waves beat (B34), the roll-over beat (B04), the edge-smear beat (B33) and the sine-or-ramp beat (B24): each extends an idea another beat already carries. The late-join demo (B01), the clock-mixing pair (B05, B06), the three knob beats (B14 to B16), the travel beat (B28) and the wind click (B40) stay: they are the proof and the payoff. The curve-texture pair (B22, B23) stays because the breathing logo reads one; if both must go, the logo breathes from a sine and B36 to B38 shrink to two beats.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | One Clock | 8 | 290 | ~1:39 |
| II | The Wave | 10 | 350 | ~1:59 |
| III | Loops and Curves | 7 | 241 | ~1:22 |
| IV | Waves on a Shape | 9 | 294 | ~1:40 |
| V | One Clock, Two Effects | 6 | 198 | ~1:07 |

## Opening

### BOPEN · identity card · 26 words · ~9 s

> Time and Waves. Learn what a shader's clock really counts, and how one sine wave with four numbers makes a pulse, a loop or a ripple.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Time and Waves", and the line "Pulses, loops and ripples from one clock".

### BIDEA · the question · 41 words · ~14 s

> Hallo. This is Liam, in for Bear. Every shader can read a clock, called time. Most people expect it to start when their node appears. It does not. It starts when the game starts, and every shader reads the same one.

*Picture.* The hesitant writer types: "TIME starts at zero
when my node appears." then deletes "when my node appears" and types "when the game starts".

### BDEFS · terms · 69 words · ~24 s

> Six terms. A shader is a small program the graphics card runs to decide how something is drawn. Fragment is the function that runs once for each pixel. A uniform is a value your game sets from outside. U V is a point's address on the shape. A texture is an image a shader can read. And sine is a function that swings smoothly between minus one and one.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **fragment()** — runs once for each pixel the shape covers; sets its color; **Uniform** — a value your game sets from outside; every pixel sees the same one; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Texture** — an image a shader can read by address; **Sine** — a function that swings smoothly between -1 and 1

## Act I: One Clock

### B01 · 36 words · ~12 s

> Two squares run the same pulse shader. The second one joins late. If time began when a node appears, its pulse would start over from the beginning. Watch. It arrives already in step with the first.

*Picture.* Act title 'One Clock' (serif 40) top-left. A real Godot render in a framed window on the cream stage: two squares that pulse between teal and cream, the left one pulsing alone from the first frame, the right one added late. Labels 'from the start' under the left and 'added late' under the right. Caption: 'TIME · seconds on one clock shared by the whole game'.

*Motion.* The right square appears in the middle of its pulse already the same color as the left, and the two keep pulsing together.

*Lane.* capture · `ShaderLab` · runner-up: manim: two dots reading one clock bar

*Capture to record.* C01: evidence/planning-checks/scene-project/scenes/scene_c01_late_join.gd. Two 02-pulse squares (left centred at 0.30, 0.50; right at 0.70, 0.50; each 0.30 of the frame height). The right square is added at frame 300 (10.0 s). 15 s, 30 fps, Forward+, no input. Event times may be shifted by holding the first frame so the join lands on the spoken word 'Watch'.

### B02 · 36 words · ~12 s

> A shader cannot count: every frame it starts fresh, remembering nothing from the last. So the engine hands it a clock called time, the seconds since the engine started. One clock, shared by the whole game.

*Picture.* The real Godot 4.7 canvas item shader page in a browser window, scrolled to the Global built-ins table. The camera pushes in on the TIME row and a terracotta ring marks 'Global time since the engine has started, in seconds.' The first line of the row is also the glossary wording on screen: 'TIME · seconds on one clock shared by the whole game'.

*Motion.* The camera pushes in on the TIME row and the ring lands as the voice says 'the seconds since the engine started'.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: three nodes reading one clock (a fan of lines)

### B03 · 34 words · ~12 s

> Two things you might expect to matter. The game's time scale does: at one half, the clock runs at half speed for every shader. Pausing does not. Scripts freeze, but the shimmer carries on.

*Picture.* A real render: a grey track with a teal marker that a script moves by delta (top), and below it a square pulsing on TIME. At about 25 percent of the beat the time scale drops to one half: the marker and the pulse both slow. At about 60 percent the tree is paused: the marker freezes and the pulse carries on. Labels 'time scale 0.5' then 'paused'. Caption: 'time scale: how fast the game's clock runs · 1 is normal'.

*Motion.* Both things slow under the time scale; under the pause the marker freezes and the pulse keeps going.

*Lane.* capture · `ShaderLab` · runner-up: manim: two clocks, one at half rate

*Capture to record.* C03: evidence/planning-checks/scene-project/scenes/scene_c03_scale_pause.gd. A marker (a ColorRect moved by delta, 0.2 of the width per game second) on a grey track at y 0.28, and a 02-pulse square centred (0.50, 0.68), 0.34 of the height. Frame-counted events: time scale 0.5 from frame 84 (2.8 s) to 209, 1.0 from 210, paused from frame 228 (7.6 s) to the end. 12 s, 30 fps, Forward+. The controller runs while paused (process mode always); the marker is pausable.

### B04 · 39 words · ~13 s

> The clock also has a limit. It wraps back to zero after thirty-six hundred seconds, one hour, by default. A pulse that repeats a whole number of times in that hour will not notice. Any other pulse jumps once.

*Picture.* A horizontal clock bar labelled 'default limit: 3,600 s · one hour' with a terracotta marker that runs to the right end and wraps back to 0. Beneath it a zoom, labelled 'shown with the limit at 2 s so it fits on screen' (the measured check): time from 0 to 4 s, the wrap marked at 2 s and at 4 s. Two curves on it: the upper one (speed 1, two whole cycles in 2 s) carries on unbroken through each wrap; the lower one (speed 0.7, 1.4 cycles) snaps to a different height at each wrap, a vertical gap ringed in terracotta. Labels: 'a whole number of cycles: no jump' and 'any other: one jump'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · limit set to 2 s · pulse change at the wrap: 4 steps against 44 (of 255)'.

*Motion.* The marker runs to the end of the bar and wraps; in the zoom the upper curve carries on through the wrap unbroken while the lower curve snaps to a different height.

*Lane.* manim · `B04_RolloverJump` · runner-up: capture: a real run with the limit set to two seconds

### B05 · 39 words · ~13 s

> To time a node from its birth, you might reach for the engine's tick counter, and subtract. Do not. It starts earlier than time: about a quarter of a second on this Mac, and a little different every run.

*Picture.* Two horizontal rulers in seconds, one above the other. The top, labelled 'tick counter' (with the real call name in grey, Time.get_ticks_msec()), starts at 0 on the left. The bottom, labelled 'TIME', has its 0 a little to the right. Terracotta markers run along both at the same pace. A bracket between the two zeros reads 'about 0.25 s on this Mac'. A small cross over a subtraction sign between the two ruler labels lands on the words 'Do not'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · three runs: 0.26, 0.29, 0.26 s'.

*Motion.* Both markers move together, always a quarter second apart: the zeros never line up.

*Lane.* manim · `B05_TwoZeros` · runner-up: LectureEvidenceTable of the three measured gaps

### B06 · 28 words · ~10 s

> It also ignores the time scale. Run one second at half speed, and the tick counter ends up half a second ahead. The two clocks never agree again.

*Picture.* The two rulers from the previous picture. For one second the bottom marker (TIME) slows to half speed while the top marker (tick counter) keeps its pace; then both run normally again. The bracket between the zeros grows from 0.25 s to 0.75 s and stays there. Labels: 'time scale 0.5 for one second' and 'gap +0.5 s'.

*Motion.* The bottom marker lags for a second and the bracket widens by exactly half a second, then stays.

*Lane.* manim · `B06_Drift` · runner-up: capture: two number readouts side by side

### B07 · 41 words · ~14 s

> To start counting when a node appears, count it yourself. Add delta, the seconds since the last frame, to an age, and pass the age to the shader as a uniform. Now the late square starts its pulse from the beginning.

*Picture.* GDScript card at left (the age counter, five lines). At right a real render: the left square pulses on TIME; a second square is added late and starts its pulse from the beginning, out of step with the first. Labels 'TIME' under the left square and 'age' under the right. Caption: 'delta: seconds since the last frame'.

*Motion.* The late square starts at the beginning of its own pulse while the first carries on, so the two are visibly out of step.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace of the GDScript alone

*Capture to record.* C07: evidence/planning-checks/scene-project/scenes/scene_c07_age.gd. Left square: 02-pulse (TIME). Right square: 01-age (uniform age), added at frame 324 (10.8 s), its own _process adds delta to age and passes it with set_shader_parameter. Squares centred (0.30, 0.50) and (0.70, 0.50), 0.30 of the height. 14 s, 30 fps, Forward+, no input.

### B08 · 37 words · ~13 s

> So choose by the job. A loop that never needs to start: use time. An effect that begins with a node: use an age. A one-time effect: use a uniform your game moves when the moment comes.

*Picture.* A three-row table, one row ringed as each job is named, the clock beside it.

*Motion.* The ring moves down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: three tracks

## Act II: The Wave

### B09 · 37 words · ~13 s

> Now the wave. Put the clock inside a sine, and the value swings smoothly between minus one and one. Sine counts in angles, so one full swing takes six point two eight seconds. That number is tau.

*Picture.* Act title 'The Wave' (serif 40) top-left. Axes: time in seconds along x (0 to 13), value from -1 to 1 up the side. A terracotta dot travels along y = sin(TIME) at the pace of the clock, tracing the curve. A bracket under the first full swing reads 'one swing = 6.28 s'. At the end a label 'TAU = 6.28 · one full turn' lands beside the bracket (glossary: the number of radians in a full turn).

*Motion.* The dot traces the curve up to 1 and down to -1; the bracket closes around the first full swing.

*Lane.* manim · `B09_SineOfTime` · runner-up: ShaderLab capture of sin(TIME) as a color

### B10 · 22 words · ~8 s

> That is awkward. Multiply time by tau first, so one second becomes one full turn. Now each swing takes exactly one second.

*Picture.* The same axes. The curve squeezes horizontally to a sixth of its width as the label changes from 'sin(TIME)' to 'sin(TIME × TAU)': the bracket under the first swing shrinks from '6.28 s' to '1 s', and tick marks at 1, 2 and 3 seconds each land where a swing begins (the curve crossing zero on its way up).

*Motion.* The curve compresses: one swing now fits in one second.

*Lane.* manim · `B10_TauTurn` · runner-up: LectureCodeTrace of one line

### B11 · 38 words · ~13 s

> A color cannot go below zero, and sine does, half the time. Send a raw sine to a color and every negative value is clamped to zero. The pulse sits at its darkest for half of each swing.

*Picture.* The sine curve again, with the ramp strip (0 to 1, drawn in greys) under it and a terracotta marker riding the strip with the dot. While the curve is below zero the curve is drawn grey and flattened onto the zero line, and the marker waits at the dark end of the strip. Labels: 'below zero → 0' and 'a color cannot be negative'.

*Motion.* The marker rides the strip with the dot, then waits at the dark end for half of every swing.

*Lane.* manim · `B11_ClampedHalf` · runner-up: capture: a raw sine shader (a large dark field)

### B12 · 36 words · ~12 s

> So squeeze it into zero to one. Halve the swing, then lift it by a half. Zero point five plus zero point five times sine never leaves the range, and it still swings once per second.

*Picture.* The curve shrinks to half its height, then slides up by a half until it fills 0 to 1 exactly; the strip's marker now travels the whole strip. A formula caption builds as '0.5 + 0.5 × sine', the first 0.5 lighting up with the lift and the second with the halving.

*Motion.* Two moves in order, shrink then lift; afterwards the marker travels the whole strip.

*Lane.* manim · `B12_HalveAndLift` · runner-up: LectureCodeTrace

### B13 · 32 words · ~11 s

> Here is that line as a shader. The pulse blends two colors: at zero, all teal; at one, all cream. Mix does the blending. The square swings between them once a second.

*Picture.* Code card at left (02-pulse.gdshader, eight lines); at right a real Godot window filled with a color that swings between teal and cream once a second. The pulse line is highlighted first, then the two color lines (label 'vec3: a bundle of three numbers: red, green, blue'), then the COLOR line (label 'vec4: red, green, blue, alpha (1 is solid)'). Caption: 'mix(a, b, t) blends from a to b: t of 0 gives a, 1 gives b'.

*Motion.* The window swings between teal and cream while the highlight moves from the pulse line to the two colors and then to the blend.

*Lane.* capture · `ShaderLab` · runner-up: manim: the plot with a marker

*Capture to record.* C13: Lab rect, lab-shaders/02-pulse.gdshader, 12 s, 30 fps, Forward+, no input.

### B14 · 39 words · ~13 s

> Four numbers describe a sine wave. The first is amplitude: how far it swings from its middle. Shrink it and the pulse gets shallow; at zero it stops. A half is the most that fits in zero to one.

*Picture.* The plot with the ramp strip (middle line at 0.5). A slider labelled 'amplitude' moves 0.5, 0.25, 0 and back to 0.5: the curve's height changes around the middle line, and the strip's marker travels a shorter and shorter stretch around the middle, resting there at 0. A bracket from the middle to a crest is labelled 'amplitude'. Caption: 'amplitude: how far the wave swings from its middle'. A grey note: 'a half is the most that fits in 0 to 1'.

*Motion.* The curve flattens as the slider falls and the marker parks at the middle.

*Lane.* manim · `B14_Amplitude` · runner-up: ShaderLab sweep capture

### B15 · 36 words · ~12 s

> The second is speed: how quickly it repeats. Time times speed counts the cycles, one cycle being one full swing. Speed one half gives a swing every two seconds. Speed two gives two swings every second.

*Picture.* The plot. A slider labelled 'speed' moves 0.5, 1, 2: the curve compresses in time, with brackets under the first swing reading '2 s', '1 s', '0.5 s'. A caption builds: 'cycles = TIME × speed' and 'one cycle = one full swing'. Caption: 'speed: how quickly it repeats'.

*Motion.* The curve compresses horizontally as the slider rises and the dot's pace quickens.

*Lane.* manim · `B15_Speed` · runner-up: ShaderLab sweep capture

### B16 · 38 words · ~13 s

> The third is offset: where in its cycle the wave starts. Offset a quarter starts it at the top. Offset a half swings exactly opposite to a wave with none: when one is brightest, the other is darkest.

*Picture.* Two curves on one plot and two ramp strips with two markers: a plain one (offset 0) and one with offset 0.25, slid left by a quarter cycle so it starts at its crest; then the second curve slides to offset 0.5, exactly mirrored: it has a crest where the first has a trough. The two markers travel the strips in opposite directions. Caption: 'offset: added to slide the wave', second line 'here: where in its cycle it starts'.

*Motion.* The second curve slides sideways until it mirrors the first, and the markers move opposite ways.

*Lane.* manim · `B16_Offset` · runner-up: ShaderLab: two squares

### B17 · 38 words · ~13 s

> Here are all three as uniforms, dials your game can set. Time times speed, plus offset, counts the cycles. Offset is an instance uniform, so each node can keep its own. The fourth number waits for a shape.

*Picture.* The real 03-dials.gdshader (thirteen lines) on a cream code card: the three uniform lines, then the line that counts the cycles, then the instance uniform line again; at the end the empty line under the three uniforms is highlighted as the slot for a fourth dial. Cue labels: 'hint_range: the editor limits it to 0 to 0.5' on the amplitude line, 'instance uniform: each node keeps its own value' on the offset line and 'a fourth dial waits here: frequency' on the empty line.

*Motion.* Line focus steps down the dials, then to the cycle count, then back to the instance uniform.

*Lane.* remotion · `ShaderLab` · runner-up: LectureCodeTrace (it holds about ten lines and this file has thirteen)

### B18 · 34 words · ~12 s

> Five squares, one shader, one clock. Each gets its own offset: zero, a fifth, two fifths, and so on. Their pulses no longer match, and together they roll along the row, like a wave.

*Picture.* GDScript card at left (the two-line loop that sets each node's offset); at right a real render: five squares in a row, all pulsing, each a fifth of a cycle behind its neighbour, so the brightest square moves along the row like a wave. Labels under the squares: 0, 0.2, 0.4, 0.6, 0.8.

*Motion.* The brightest square travels along the row: a wave rolls from one end to the other.

*Lane.* capture · `ShaderLab` · runner-up: manim: five dots

*Capture to record.* C18: evidence/planning-checks/scene-project/scenes/scene_c18_rolling_row.gd. Five ColorRects (0.13 of the width) at x = 0.18, 0.34, 0.50, 0.66, 0.82, y 0.50, sharing ONE ShaderMaterial of 03-dials.gdshader (amplitude 0.5, speed 0.5); each node gets set_instance_shader_parameter('offset', i / 5.0). 12 s, 30 fps, Forward+. In the capture the bright crest moves toward the left end.

## Act III: Loops and Curves

### B19 · 39 words · ~13 s

> Sine always swings back. For a loop that starts over, like a loading bar, use fract. It keeps only the part after the decimal point, so the cycle count becomes a ramp from zero to one, restarting every cycle.

*Picture.* Act title 'Loops and Curves' (serif 40) top-left. A rising straight line (the cycle count TIME × speed, which never stops) with whole-number ticks 0, 1, 2, 3 up the side. A copy of the line is cut at every whole number and drops back to 0, becoming a sawtooth between 0 and 1. A ramp strip with a marker under it jumps back to the left at every restart. Labels (glossary wording): 'fract(x): the part after the point: x minus floor(x)' and 'ramp: a smooth run of values from 0 up to 1'.

*Motion.* The straight line is cut at each whole number and folds back to zero; the strip's marker restarts every time.

*Lane.* manim · `B19_Restart` · runner-up: ShaderLab capture of a loading bar

### B20 · 36 words · ~12 s

> To go back and forth at a steady pace, fold the ramp: double it, subtract one, take the absolute value, and subtract that from one. You get a triangle, rising and falling at the same rate.

*Picture.* The sawtooth from the previous picture transforms in four small steps, each labelled: '× 2' (it now runs 0 to 2), '− 1' (−1 to 1), 'abs' (a V shape), '1 −' (flipped into a triangle). The strip marker now moves back and forth at a steady pace. Caption: 'abs(x): drops the minus sign'.

*Motion.* The sawtooth folds step by step into a triangle and the marker turns around at each end.

*Lane.* manim · `B20_Fold` · runner-up: LectureCodeTrace of the formula

### B21 · 33 words · ~11 s

> Same pace, three personalities. The sine eases into each turn. The triangle turns sharply. The sawtooth never turns back: it climbs, then jumps to the start. Pick the one whose motion you want.

*Picture.* Code card at left (04-three-shapes.gdshader); at right a real render of three horizontal teal bars on light tracks, separated by thin gaps, each filling from the left to its wave's value: top sine, middle triangle, bottom sawtooth, all with the same two-second period. Labels at the left of the rows: 'sine', 'triangle', 'sawtooth'. Caption: 'sawtooth: a ramp that restarts'.

*Motion.* The sine bar eases at each end, the triangle bar turns sharply, the sawtooth bar fills and snaps back to empty.

*Lane.* capture · `ShaderLab` · runner-up: manim: three plots with three markers

*Capture to record.* C21: Lab rect, lab-shaders/04-three-shapes.gdshader, 12 s (six loops), 30 fps, Forward+, no input.

### B22 · 39 words · ~13 s

> Sometimes no formula gives the shape you want: a slow start, a quick snap, a gentle settle. Draw it as a curve. A curve texture bakes the curve into a strip of pixels, brighter where the curve is higher.

*Picture.* A drawn curve (the breath: a slow rise, a short hold, a long fall) above a thin horizontal strip whose brightness follows the curve (drawn in greys: dark where the curve is 0, light where it is 1). A vertical scan line slides along the strip with a dot on the curve at the same position. Labels: 'CurveTexture: a curve baked into a strip of pixels' and the call 'texture(curve, vec2(t, 0.0)).r' in monospace.

*Motion.* The scan line slides along the strip and the dot follows the curve: the strip's brightness equals the curve's height.

*Lane.* manim · `B22_CurveStrip` · runner-up: ShaderLab capture of a scripted CurveTexture

### B23 · 31 words · ~10 s

> The lookup is one line. Hand the strip a position from zero to one, and read its red channel. Feed it the restarting ramp, and the curve plays on a loop.

*Picture.* Code card at left (05-curve-loop.gdshader); at right a real render: a square whose color follows the breath curve (a slow rise to cream, a short hold, a long fall back to teal), looping every two seconds. The lookup line is highlighted first, then the ramp line.

*Motion.* The square follows the curve's shape, loop after loop.

*Lane.* capture · `ShaderLab` · runner-up: manim: a dot riding the curve

*Capture to record.* C23: evidence/planning-checks/scene-project/scenes/scene_c23_curve_loop.gd. A square (0.5 of the height, centred) with lab-shaders/05-curve-loop.gdshader; the 'curve' uniform is a CurveTexture of the breath curve (points (0,0), (0.40,1), (0.55,1), (1,0), flat tangents). 12 s, 30 fps, Forward+, no input.

### B24 · 39 words · ~13 s

> Feed the same curve from a sine and it plays forward, then backward, every cycle. Feed it from the ramp and it plays one way, then restarts. Use the ramp when the motion should always go the same way.

*Picture.* Two tracks, each with a copy of the breath curve and a dot on it, and the input drawn as a strip above each. Top track: the input is a sine, the dot runs along the curve to its end and then back along it. Bottom track: the input is the restarting ramp, the dot runs to the end and jumps back to the start. Labels: 'sine input: forward, then backward' and 'ramp input: one way, then restart'.

*Motion.* The top dot goes out and comes back; the bottom dot goes out and jumps back.

*Lane.* manim · `B24_SineOrRamp` · runner-up: ShaderLab two squares

### B25 · 24 words · ~8 s

> So one count gives four looks. Sine swings smoothly. Triangle swings at a steady rate. Sawtooth restarts. And a curve is whatever you draw.

*Picture.* A four-row table, one row ringed as each look is named, with the code that makes it.

*Motion.* The ring steps down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim: four small plots

## Act IV: Waves on a Shape

### B26 · 36 words · ~12 s

> The row of squares gave each one a different offset. A shape has a different position at every pixel. So let the address supply the offset, and every pixel gets its own place in the wave.

*Picture.* Act title 'Waves on a Shape' (serif 40) top-left. The five squares from the row, each with its offset label (0, 0.2, 0.4, 0.6, 0.8) and the pulse curve under it shifted accordingly. The squares merge into one continuous strip; the row of labels becomes the address strip 0 to 1 (U V x) and the five curves become one wave across the strip, each pixel column carrying its own offset. Caption: 'offset from the address'.

*Motion.* Five separate offsets blur into a continuous strip in which every pixel column has its own offset from where it sits.

*Lane.* manim · `B26_FiveToEvery` · runner-up: ShaderLab capture of the stripes

### B27 · 35 words · ~12 s

> Use the address across the shape as the count, and the sine becomes stripes. The number of stripes is the fourth number, frequency: how many cycles fit across the shape. Three cycles, three bright stripes.

*Picture.* Code card at left (06-stripes.gdshader); at right a real still: the banner crossed by three bright cream stripes on teal, with three terracotta rings landing on the stripes in turn. Caption: 'frequency: how many cycles fit across the shape'.

*Motion.* The cycles line is highlighted, then the frequency line, and the rings count the three stripes one by one.

*Lane.* capture · `ShaderLab` · runner-up: manim: a plot of three cycles over the strip

*Capture to record.* C27: Lab rect, lab-shaders/06-stripes.gdshader at frequency 3 (the default), still PNG 1920x1080 (rect = the banner). Bright stripe centres at x = 0.083, 0.417, 0.750 (the rings).

### B28 · 39 words · ~13 s

> Now subtract time from the address, and the stripes slide right. Speed is how far they travel each second, as a fraction of the shape: one half means half the shape every second. A negative speed slides them left.

*Picture.* Code card at left (07-travel.gdshader); at right the same stripes now sliding to the right, with a readout 'speed 0.5' at the top; in the last seconds the speed flips to minus one half and they slide left ('speed -0.5').

*Motion.* The stripes slide right at half the shape each second, then reverse.

*Lane.* capture · `ShaderLab` · runner-up: manim: a plot with a crest tracked

*Capture to record.* C28: evidence/planning-checks/scene-project/scenes/scene_c28_travel.gd. A full-frame rect (the Lab rect) with lab-shaders/07-travel.gdshader, frequency 3, speed 0.5 until frame 330 (11.0 s), then -0.5 (a step: no pop, because 2 x 0.5 x 3 x 11 = 33 whole cycles). 13 s, 30 fps, Forward+. The step lands on the spoken words 'A negative speed'.

### B29 · 34 words · ~12 s

> The count does not have to come from the address across. On a square shape, use the distance from the middle, and the stripes become rings that spread outward, like a drop in water.

*Picture.* Code card at left (08-rings.gdshader); at right a real render of rings spreading outward from the middle of a square. The distance call is highlighted; caption 'distance(a, b): how far apart two points are'.

*Motion.* Rings are born at the middle and spread outward to the edge.

*Lane.* capture · `ShaderLab` · runner-up: manim: concentric circles growing

*Capture to record.* C29: Lab sprite (square, texture ignored: --sprite-tex white), lab-shaders/08-rings.gdshader, frequency 4, speed 0.25, 10 s, 30 fps, Forward+. A circle on a square only: on a wide shape the rings squash.

### B30 · 32 words · ~11 s

> That is all four. Amplitude is how tall. Frequency is how many cycles across. Speed is how fast they slide. Offset is where they start. Each can change without touching the others.

*Picture.* A wide strip showing a traveling wave (stripes) and four sliders in a row: amplitude, frequency, speed, offset, each captioned in one to three words ('how tall', 'how many', 'how fast', 'where it starts'). Each slider moves alone while the other three stay put, and only its own property of the wave changes: the height, the number of cycles across, the sliding pace, the starting shift.

*Motion.* Each slider moves alone and only its own property of the wave changes.

*Lane.* manim · `B30_FourKnobs` · runner-up: LectureEvidenceTable

### B31 · 33 words · ~11 s

> Brightness is only one use. Add the wave to the address you look up, and the picture itself ripples. No new corners are needed: the rectangle stays put, and only the lookup moves.

*Picture.* Code card at left (09-ripple.gdshader, the lookup line labelled 'TEXTURE: the node's own picture; texture() reads it'); at right a real render of the teal-and-cream checker picture rippling vertically in waves that slide across it, with a terracotta ring around the picture's rectangle (the rectangle itself never moves). Readout 'same rectangle'.

*Motion.* The squares of the checker wobble up and down in a wave while the rectangle around them stays still.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grid whose rows shift

*Capture to record.* C31: Lab sprite with the Lab's checker picture (--sprite-tex checker), lab-shaders/09-ripple.gdshader, amplitude 0.05, frequency 3, speed 0.5, offset 0, 10 s, 30 fps, Forward+. The ring marks the 288 px picture rectangle (0.275 to 0.725 of the width, 0.10 to 0.90 of the height in a 640x360 window).

### B32 · 24 words · ~8 s

> Multiply the wave by the address across, and the left edge cannot move. The right end waves freely, like a flag on a pole.

*Picture.* Code card at left (10-flag.gdshader); at right the checker picture waving, the left edge perfectly still and the ripple growing toward the right end. A ring on the left edge ('pinned') and a ring on the right end ('free').

*Motion.* The left edge holds still while the ripple grows to the right, like a flag on a pole.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grid pinned at one side

*Capture to record.* C32: Lab sprite with the checker picture, lab-shaders/10-flag.gdshader, amplitude 0.05, frequency 3, speed 0.5, 10 s, 30 fps, Forward+. Rings: left edge box [0.275, 0.10, 0.31, 0.90], right end box [0.69, 0.10, 0.725, 0.90].

### B33 · 31 words · ~10 s

> One limit. The rectangle itself does not bend, so a big ripple drags in edge pixels, and the edges smear. Leave empty margin around the art, or move real corners instead.

*Picture.* Code card at left (09-ripple.gdshader); at right a real still of the checker picture with a very large amplitude: the top and bottom edges are smeared into tall stretched bars. A ring on the top edge and a readout 'edge pixels stretch'.

*Motion.* A ring settles on the smeared top edge while the voice says the edges smear.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grid pushed past its frame

*Capture to record.* C33: Lab sprite with the checker picture, lab-shaders/09-ripple.gdshader, amplitude 0.20, frequency 3, speed 0.5, tv 0.3 (still), PNG 1920x1080, Forward+. Ring around the top 12 percent of the picture rectangle.

### B34 · 30 words · ~10 s

> Add two waves with different frequencies and speeds, and the pattern stops repeating so plainly. Each wave has its own amplitude, frequency and speed, and the shader adds the results.

*Picture.* Code card at left (11-two-waves.gdshader); at right the checker picture rippling with a slow wide wave and a fast narrow wave added together, so the pattern no longer looks like a plain repeat. The two wave lines are highlighted in turn, then the line that adds them.

*Motion.* Two ripples of different size and pace pass through each other and the picture's motion never settles into an obvious repeat.

*Lane.* capture · `ShaderLab` · runner-up: manim: two curves summed

*Capture to record.* C34: Lab sprite with the checker picture, lab-shaders/11-two-waves.gdshader, 10 s, 30 fps, Forward+.

## Act V: One Clock, Two Effects

### B35 · 26 words · ~9 s

> Now use everything at once. A logo breathes, and a banner waves. Two shaders read the same clock, and the game adds one thing: a click.

*Picture.* Act title 'One Clock, Two Effects' (serif 40) top-left. A real render: the teal test sprite (a blob with two cream eyes) swelling and settling above a striped banner whose wave travels, pinned at the left. Labels 'logo' and 'banner'.

*Motion.* The logo swells and settles while the banner's wave travels: two effects running together.

*Lane.* capture · `ShaderLab` · runner-up: manim: a drawing of the two effects

*Capture to record.* C35: evidence/planning-checks/scene-project/scenes/scene_c35_together.gd (--part together). Logo (12-breath, the breath CurveTexture) centred (0.50, 0.30) at 0.5 of the height; banner (13-banner, wind 1.0) centred (0.50, 0.72) at 0.55 of the width. 12 s, 30 fps, Forward+, no input.

### B36 · 33 words · ~11 s

> The breath is a curve: a slow rise, a short hold, a long fall. The restarting ramp plays it once per cycle. The logo's size is one plus a quarter of the curve.

*Picture.* The breath curve (a slow rise, a short hold, a long fall) drawn on axes, with the restarting ramp as a strip above it feeding a dot that rides the curve. Beside the plot, the teal logo blob whose size follows 1 + 0.25 × curve: it swells as the dot rises, holds, and settles as the dot falls. Caption: 'size = 1 + 0.25 × curve'.

*Motion.* The dot rides the curve as the ramp restarts, and the logo swells and settles in step with it.

*Lane.* manim · `B36_BreathCurve` · runner-up: ShaderLab capture of the logo alone

### B37 · 38 words · ~13 s

> To make a picture bigger, look it up from closer in. Measure the address from the middle, divide it by the scale, and measure back. A scale of one and a quarter shows the picture a quarter bigger.

*Picture.* A picture (the blob with eyes) in a square frame with a five-by-five grid of small dots on it showing where the shader looks up the picture. The dots pull in toward the middle (the address measured from the middle, divided by the scale 1.25) and the part of the picture they read now fills the frame, so the picture appears a quarter bigger. Caption: 'bigger picture = look up closer in'. Readout: 'scale 1.25'.

*Motion.* The lookup dots draw in toward the middle and the picture seen through them grows.

*Lane.* manim · `B37_LookCloser` · runner-up: ShaderLab capture with code

### B38 · 31 words · ~10 s

> Here is the logo live. The curve is a texture, the ramp reads it, and the logo swells and settles about its middle. The art keeps empty margin, so nothing smears.

*Picture.* Code card at left (12-breath.gdshader); at right a real render of the teal blob swelling and settling about its middle on the stage, with a ring around its rectangle showing the margin around the art.

*Motion.* The logo swells and settles about its middle and never touches the edge of its rectangle.

*Lane.* capture · `ShaderLab` · runner-up: manim: the logo and a plot

*Capture to record.* C38: evidence/planning-checks/scene-project/scenes/scene_c35_together.gd (--part logo). Logo centred (0.50, 0.50) at 0.5 of the height, lab-shaders/12-breath.gdshader with the breath CurveTexture. 10 s, 30 fps, Forward+, no input.

### B39 · 34 words · ~12 s

> The banner is the traveling wave from before, pinned at the left, drawn as stripes so you can see the cloth move. A wind uniform scales the wave: at zero, the banner hangs still.

*Picture.* Code card at left (13-banner.gdshader); at right a real render of the striped banner with a wave that travels along it, the left end still. The pinned line is highlighted, then the wind uniform; a readout 'wind 1'.

*Motion.* The wave travels along the banner from the pinned end while the voice describes it.

*Lane.* capture · `ShaderLab` · runner-up: manim: the banner drawn flat then waved

*Capture to record.* C39: evidence/planning-checks/scene-project/scenes/scene_c35_together.gd (--part banner). Banner centred (0.50, 0.50) at 0.55 of the width, lab-shaders/13-banner.gdshader, wind 1.0, amplitude 0.06, frequency 3, speed 0.5. 10 s, 30 fps, Forward+, no input.

### B40 · 36 words · ~12 s

> When the player clicks, set wind to one, then tween it back to zero. The banner snaps into motion, then settles. A moment belongs to your game. Time keeps the beat; a uniform picks the moment.

*Picture.* GDScript card at left (the click handler, five lines, word for word the handler in scene_c40_wind_click.gd); at right a real render: the striped banner hangs still, a scripted click lands, the banner snaps into motion and settles over four seconds. A label 'scripted input' stays on screen. Caption: 'tween: Godot's way to change a value smoothly over time from GDScript'.

*Motion.* The banner is still until the click, then waves and settles back to still.

*Lane.* capture · `ShaderLab` · runner-up: manim: a timeline with an event marker

*Capture to record.* C40: evidence/planning-checks/scene-project/scenes/scene_c40_wind_click.gd. Banner (13-banner, wind 0.0) centred (0.50, 0.50) at 0.55 of the width; one scripted left click pushed at frame 135 (4.5 s) sets wind to 1.0 and tweens it to 0.0 over 4.0 s. 14 s, 30 fps, Forward+. The label 'scripted input' is an overlay.

## Closing

### BVDT · recap · 78 words · ~26 s

> Let's recap with Claude. Time is one clock for the whole game; count your own with an age. Time times speed counts cycles, and a sine turns the count into a pulse. Fract, a fold or a curve turns the same count into another loop. Feed the count from the address, and the wave travels across a shape. Four numbers set any sine wave: amplitude, frequency, speed and offset. Time keeps the beat; a uniform picks the moment.

*Picture.* The recap card: Time is one clock for the whole game; count your own with an age. / Time times speed counts cycles, and a sine turns the count into a pulse. / Fract, a fold or a curve turns the same count into another loop. / Feed the count from the address, and the wave travels across a shape. / Four numbers set any sine wave: amplitude, frequency, speed and offset. / Time keeps the beat; a uniform picks the moment.

### BHTF · your turn · 85 words · ~29 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a Color Rect that pulses between two colors with a sine of time. Use three float uniforms: amplitude, speed in cycles per second, and offset in cycles. Keep the result between zero and one, and show me the line where time becomes a pulse. Then check two things yourself. With amplitude at zero, does the color hold still? And does a second copy with offset one half pulse exactly opposite the first?

*Prompt shown and read in full:* Write a Godot canvas item shader for a Color Rect that pulses between two colors with a sine of time. Use three float uniforms: amplitude, speed in cycles per second, and offset in cycles. Keep the result between zero and one, and show me the line where time becomes a pulse.

*Two checks:* Check: with amplitude at zero, the color holds still. · Check: a second copy with offset one half pulses exactly opposite the first.

### BOUT · outro · 7 words · ~4 s

> Time and Waves. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


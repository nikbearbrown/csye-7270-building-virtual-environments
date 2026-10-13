# Script: Soft Edges, Glow and Noise

**What this is.** The words Liam will say in *Soft Edges, Glow and Noise*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 48 beats, 1785 words, about **10:11** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 23, manim 15, editor 2, remotion 2.

**If it runs long.** Cut, in this order: the reveal-pace beat (B32), the beat on what else H D R two D changes (B40), the swapped-lines beat (B10) and the beat on glow without H D R two D (B41). Each is a true caveat that another beat or the docs already carry. The S-curve pair (B05, B06), the parentheses pair (B21, B22), the seam pair (B29, B30), the two glow runs (B36, B37) and the finale (B42) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | From Cut to Ramp | 10 | 342 | ~1:56 |
| II | Falloff and Highlight | 6 | 212 | ~1:12 |
| III | Layering | 7 | 241 | ~1:22 |
| IV | Noise That Moves | 9 | 318 | ~1:48 |
| V | Glow, Honestly | 10 | 358 | ~2:02 |

## Opening

### BOPEN · identity card · 32 words · ~11 s

> Soft Edges, Glow and Noise. Learn how to soften an edge, layer a highlight on top, scroll noise through it, and make glow work for real, so your effects stop looking flat.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Soft Edges, Glow and Noise", and the line "How to soften edges, layer effects, and add glow".

### BIDEA · the question · 52 words · ~18 s

> Hallo. This is Liam, in for Bear. Most people think a soft edge needs a blur. It does not. A soft edge is a ramp: a value that climbs from zero to one over a distance you choose. We will build one bubble a layer at a time, and finish with glow.

*Picture.* The hesitant writer types: "A soft edge needs a blur." then deletes "a blur" and types "a ramp".

### BDEFS · terms · 54 words · ~18 s

> Five terms. A ramp is a smooth run of values from zero to one. A mask is a number from zero to one for each pixel: how much to show. U V is a pixel's address on the shape. A uniform is a value your game sets. Alpha is how visible a pixel is.

*Picture.* "Terms In This Lecture": **Ramp** — a smooth run of values from 0 up to 1; **Mask** — a number from 0 to 1 per pixel saying how much of something to show; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Uniform** — a value your game sets from outside; every pixel sees the same one; **Alpha** — how visible a pixel is: 0 invisible, 1 solid

## Act I: From Cut to Ramp

### B01 · 34 words · ~12 s

> One circle, drawn two ways. First, an edge sharp enough to cut a finger. Then the same circle with the edge fading softly into the background. Nothing was blurred. One function made the difference.

*Picture.* Act title 'From Cut to Ramp' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a teal disc with a razor-sharp edge sits still, then at the swap the same disc keeps its size and colour but its edge fades softly into the grey stage. Labels 'hard edge' then 'soft edge'.

*Motion.* The sharp rim melts into a fade the moment the shader is swapped, with nothing else changing.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a sharp and a soft circle

*Capture to record.* C01: square target (ColorRect 576 x 576 logical px centred on the 1280 x 720 canvas), lab-shaders/01-hard-disc.gdshader from 0 s, material swapped to lab-shaders/02-soft-disc.gdshader at 6.0 s (`--material-at 6.0`), 10 s, 30 fps, Forward+, stage #D9D5CA, no input. Verified: 01 draws exactly two colors in a 256 px render; 02 has 16,780 in-between pixels of 65,536.

### B02 · 34 words · ~12 s

> The hard edge comes from a function called step. Give it a line in the sand, and a value. Below the line, it answers zero. At the line or above, one. Nothing in between.

*Picture.* Axes on the cream stage: horizontal x from 0 to 1, vertical result 0 to 1. A grey dashed vertical line at the edge 0.4, labelled 'edge'. A terracotta dot slides along the bottom at height 0 from the left; when it crosses the line it jumps up to height 1 and runs on along the top, leaving a cliff-shaped curve behind it. Beneath the axes the GLOSSARY wording: 'step(edge, x): 0 below the edge, 1 from the edge up'.

*Motion.* The dot slides along zero, jumps to one at the line, and the curve behind it is a cliff.

*Lane.* manim · `B02_StepPlot` · runner-up: LectureCodeTrace on the docs line 'b < a ? 0.0 : 1.0'

### B03 · 40 words · ~14 s

> A circle is a distance test. Distance asks how far apart two points are. Ask it how far each pixel's address is from the middle. One minus a step on that answer is one inside the radius, and zero outside.

*Picture.* Code card at left (the hard-disc shader); at right a real Godot window with the teal disc and its razor-sharp edge. A terracotta ring settles on the right-hand part of the rim. A label on each highlighted line defines distance and step (GLOSSARY wording).

*Motion.* The distance line is highlighted, then the step line; the ring lands on the rim as 'inside / outside' is said.

*Lane.* capture · `ShaderLab` · runner-up: manim rings of equal distance around the middle

*Capture to record.* C02: the same square target, lab-shaders/01-hard-disc.gdshader, still PNG at 3840 x 2160, Forward+. Verified in the 256 px Lab render: the pixel at UV x 0.8965 is body (alpha 1.0), the pixel at 0.9043 is stage (alpha 0.0).

### B04 · 32 words · ~11 s

> Zoom in on that edge. Every pixel is either all color or none. With nothing in between, the rim becomes a staircase of square steps. That is why hard edges look jagged.

*Picture.* A 10-by-7 block of big outline cells cut from the REAL hard-disc render (data in evidence/planning-checks/staircase-cells.txt: columns 196 to 205, rows 51 to 57): cells that are teal in the render are filled teal and labelled 1, empty ones are stage grey and labelled 0. A terracotta outline walks along the boundary one step at a time. Caption: 'no in-between values'.

*Motion.* The outline climbs the staircase one square step at a time along the real boundary.

*Lane.* manim · `B04_Staircase` · runner-up: ShaderLab zoom of the hard-disc capture

### B05 · 31 words · ~10 s

> Smooth step takes two lines. Below the first, zero. Above the second, one. Between them, it climbs along a smooth curve: slow to start, fastest in the middle, slow to finish.

*Picture.* Axes: horizontal x from 0 to 0.5, vertical result 0 to 1. Two grey dashed vertical lines at a = 0.25 and b = 0.4, labelled 'a' and 'b'. A terracotta dot rides along the x axis; the curve behind it is flat at 0, S-shaped between the two lines, then flat at 1. Rule label under the plot in two lines, in the GLOSSARY wording (the two edges are the dashed lines a and b): 'smoothstep(a, b, x): a switch that eases in and out between two edges:' then '0 below a, 1 above b, a smooth S between'.

*Motion.* The dot rides along and the curve it leaves is flat, then an S, then flat again.

*Lane.* manim · `B05_TwoLines` · runner-up: ShaderLab ramp strip

### B06 · 38 words · ~13 s

> That curve is not a straight line. Ten percent of the way along, a straight ramp reads zero point one. Smooth step reads zero point zero two eight. The formula is three t squared minus two t cubed.

*Picture.* The same plot in unit form: t (labelled 'how far along the band, 0 to 1') from 0 to 1, a grey dashed diagonal (the straight ramp) and the terracotta S-curve. At t = 0.1 a vertical marker with two dots: the straight ramp at 0.1 and the curve at 0.028, a bracket between them. At t = 0.5 the dots coincide at 0.5. Typeset at top right: 3t^2 - 2t^3 (real MathTex, per docs/MATH-TYPESETTING.md) and under it, in monospace and labelled as code, t * t * (3.0 - 2.0 * t).

*Motion.* The marker lands at ten percent and the two dots split: 0.1 on the line, 0.028 on the curve.

*Lane.* manim · `B06_SCurveNumber` · runner-up: LectureEvidenceTable of t, line, curve

### B07 · 35 words · ~12 s

> Swap step for smooth step and give it two radii. Inside zero point two five, fully on. Beyond zero point four, fully off. In between, the value glides down. That band is the soft edge.

*Picture.* Code card at left (the soft-disc shader, one line changed from the hard disc); at right the real render: the teal disc whose edge fades over a band. A terracotta ring on the band at the right side, small labels '0.25' and '0.4' at the band's two ends.

*Motion.* The smoothstep line is highlighted and the ring settles on the fading band.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C03: the square target, lab-shaders/02-soft-disc.gdshader, still PNG 3840 x 2160. Verified in the 256 px render: body alpha 0.966 / 0.496 / 0.026 at t = 0.100 / 0.500 / 0.900 (formula 0.972 / 0.500 / 0.028); every pixel within 0.008 of the formula.

### B08 · 29 words · ~10 s

> Tie the inner radius to a uniform and you get a softness dial. Small values give a crisp rim. Large ones give a cloud. The outer radius never moves.

*Picture.* Code card at left (the soft-width shader); at right a real Godot window whose disc starts with a crisp rim and, as softness is swept up, spreads into a cloud while the outer edge stays put. Labels 'crisp' then 'cloud'.

*Motion.* The fade widens inward from the same outer edge as the dial climbs.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C04: the square target, lab-shaders/03-soft-width.gdshader, softness 0.02 held 1 s, swept to 0.4 by 7 s, held (`--animate softness:0:0.02,1:0.02,7:0.4`); 12 s, 30 fps, Forward+. Verified stills: softness 0.05 gives 6,448 in-between pixels, 0.15 gives 16,780, 0.4 gives 27,400; outer edge unchanged.

### B09 · 37 words · ~13 s

> Squeeze the band to nothing, and smooth step becomes step. But the docs call equal lines undefined, and the range on that uniform cannot stop code from sending zero. So keep the width above zero with max.

*Picture.* The S-curve plot with its two lines a and b. The lines slide together; the S-curve steepens into a vertical cliff, a step, at the moment they touch. At the touch a label 'a = b: undefined (docs)' and, in grey, 'this Mac: a hard cut' with the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ and Compatibility'. Then a code chip slides in beside it: max(softness, 0.01), with the label 'max(a, b): the larger of two values'.

*Motion.* The two dashed lines slide together and the smooth curve collapses into a cliff.

*Lane.* manim · `B09_BandsMeet` · runner-up: BrowserCapture of the docs sentence 'Results are undefined if a >= b.'

### B10 · 32 words · ~11 s

> You will also meet smooth step with its lines swapped, to flip the ramp. On this Mac that worked. The docs still call it undefined, so write one minus smooth step instead.

*Picture.* The smooth-curve plot with lines a = 0.25 and b = 0.4. The two lines swap places (b now left of a) and the S-curve flips to fall from one to zero. Label 'smoothstep(0.4, 0.25, x): flipped on this Mac, undefined in the docs' with the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ and Compatibility'. Then, beneath the same flipped curve, the safe form slides in: '1.0 - smoothstep(0.25, 0.4, x)'.

*Motion.* The curve flips when the lines swap, then the safe one-minus form draws the very same curve.

*Lane.* manim · `B10_SwappedLines` · runner-up: ShaderLab render of the swapped shader

## Act II: Falloff and Highlight

### B11 · 34 words · ~12 s

> A falloff is how quickly a value fades as you move away from a point. The simplest is one minus the distance: one at the point, dropping steadily to zero a whole unit away.

*Picture.* Act title 'Falloff and Highlight' (serif 40) top-left. An 11-by-11 pixel grid of outline cells with a terracotta spot on the cell left of centre. Concentric distance rings expand from the spot; each cell fills teal in proportion to 1 minus its distance, with its number written on one row: 1.0, 0.8, 0.6, 0.4, 0.2, 0.0. At right a profile: value against distance, a straight line falling from 1 to 0 at distance 1. Label 'falloff: how quickly a value fades with distance'.

*Motion.* The rings spread from the spot and the cells behind them fill less and less, down to zero at distance one.

*Lane.* manim · `B11_Falloff` · runner-up: ShaderLab render of the spot

### B12 · 39 words · ~13 s

> As the alpha of a teal color, that is a soft spot of paint, thickest at the point. Notice where it stops: it does not. At the edge of the picture it is still more than a third on.

*Picture.* Code card at left (four lines); at right the real render: a teal haze thickest at the spot near the upper left and still clearly teal at the right edge and the bottom of the picture, where it ends in a hard straight cut. A terracotta ring on the right edge with the label 'still 0.35'.

*Motion.* The haze spreads from the spot to the picture's edge, and the ring marks the cut.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C05: the square target, lab-shaders/04-spot.gdshader, still PNG 3840 x 2160. Verified in the 256 px render: alpha 0.351 at the right edge on the spot's row (formula 0.352), 0.082 at the far corner (0.084).

### B13 · 38 words · ~13 s

> Raise it to a power above one, and numbers between zero and one shrink. Zero point seven becomes zero point three four three at power three, and zero point one one eight at power six. The spot tightens.

*Picture.* Axes 0 to 1. Three curves drawn in turn: the straight line x^1, then x^3, then x^6, each labelled at its end. A vertical guide at x = 0.7 with a dot landing on each curve: 0.7, 0.343, 0.118. Label 'pow(x, p): x raised to the power p'.

*Motion.* Each curve sags further below the straight line, and the dots on the guide drop: 0.7, 0.343, 0.118.

*Lane.* manim · `B13_PowerCurves` · runner-up: ShaderLab power sweep

### B14 · 37 words · ~13 s

> Make the power a uniform and watch the spot shrink as it climbs. Power one is a haze, three a soft highlight, eight a pinpoint. The clamp stops the number going negative, where a power is undefined.

*Picture.* Code card at left (the power shader); at right a real Godot window whose teal spot shrinks from a broad haze to a pinpoint as power sweeps from 1 to 8. Labels 'power 1', 'power 3', 'power 8' as the values pass; the clamp line is highlighted with its one-line definition at the end.

*Motion.* The spot contracts as the power climbs; the clamp line lights up last.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C06: the square target, lab-shaders/05-spot-power.gdshader, power 1 held 1.5 s, swept to 8 by 8.5 s, held (`--animate power:0:1,1.5:1,8.5:8`); 14 s, 30 fps, Forward+. Verified stills: alpha 0.895 / 0.722 / 0.422 at 0.1 from the spot for power 1 / 3 / 8.

### B15 · 38 words · ~13 s

> A falloff never stops by itself, so cut it to a shape. Multiply it by the circle's mask, the disc. Where the disc is zero, the product is zero, and the highlight can only show on the bubble.

*Picture.* Code card at left (the spot-in-disc shader); at right a real Godot window: first the teal spot with its faint tail running past where the bubble will be, then at the swap the tail beyond the disc vanishes and the highlight is confined to the disc. A terracotta ring on the tail beyond the disc with readouts '0.09' then '0'.

*Motion.* The tail outside the disc disappears the moment the shader is swapped.

*Lane.* capture · `ShaderLab` · runner-up: manim mask product

*Capture to record.* C07: the square target, lab-shaders/05-spot-power.gdshader (power 3) from 0 s, swapped to lab-shaders/06-spot-in-disc.gdshader at 3.0 s (`--material-at 3.0`), 8 s, 30 fps, Forward+. Verified: at the pixel (230, 89) the alpha is 0.090 before and 0.000 after (formulas 0.091 and 0).

### B16 · 26 words · ~9 s

> A point is two numbers. Make them a uniform and the highlight follows. Slide it around, and you decide where the light seems to come from.

*Picture.* Code card at left (the spot-moves shader); at right a real Godot window where the highlight travels once around inside the disc. A small terracotta dot marks spot_center's position on the render.

*Motion.* The highlight circles inside the disc while the highlighted line says where it comes from.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C08: the square target, lab-shaders/07-spot-moves.gdshader, spot_center driven by a scene script (`--scene`) along a circle of radius 0.18 around (0.5, 0.5), one turn in 6 s starting at the upper left, 9 s, 30 fps, Forward+. Verified stills: spot_center (0.35, 0.35) and (0.65, 0.4) match the formula within 0.008 on all pixels.

## Act III: Layering

### B17 · 38 words · ~13 s

> A layer is a color plus a mask: how much of that color to show. The body is teal, masked by the disc. The highlight is pale, masked by the spot. Stack them and you have a bubble.

*Picture.* Act title 'Layering' (serif 40) top-left. Two sheets slide in over the stage: a teal disc sheet labelled 'body · mask: the disc' and a pale highlight sheet labelled 'highlight · mask: the spot'. They slide together into one bubble (a teal disc with a pale highlight) that settles where they met.

*Motion.* The two sheets slide together and settle into one bubble.

*Lane.* manim · `B17_Layers` · runner-up: isometric stack of two sheets (show-tell)

### B18 · 37 words · ~13 s

> Two ways to combine masks. Multiply, and you keep only where both are on. Add, and you get where either is on, up to a cap of one. Multiply by zero erases. Add zero and nothing changes.

*Picture.* Two overlapping discs A (teal outline) and B (pale outline) with four sample points: in both, only A, only B, in neither. A left column 'multiply' lights the lens where both are one and writes each point's product: 1, 0, 0, 0. A right column 'add' lights the union and writes the sums: 2 (capped to 1), 1, 1, 0.

*Motion.* The lens lights up under 'multiply', the whole union under 'add', and each point shows its number.

*Lane.* manim · `B18_MultiplyAdd` · runner-up: LectureEvidenceTable of products and sums

### B19 · 38 words · ~13 s

> Each layer's color is a uniform with the hint source color. A hint is the word after the colon that tells Godot how to treat a uniform. For a color, that is a color picker in the editor.

*Picture.* Code card at left with the two color-uniform lines highlighted; at right a real still of Godot's Inspector from a scripted editor session, the material's Shader Parameters group showing two color swatches (Body Color and Highlight Color) and a Brightness number box with a slider bar, with a terracotta ring on the first swatch; then the same swatch clicked, its picker open (color wheel, brightness bar, RGB, HSV, Linear, Hex). The one-line definition of a hint (GLOSSARY wording) sits under the result.

*Motion.* The uniform lines light up, the ring lands on the color swatch they produce, and the swatch opens its picker.

*Lane.* editor · `ShaderLab` · runner-up: ShaderLab render of the bubble (labelled)

*Capture to record.* E3 (DONE by script, 2026-10-13: the one film-specific editor run; state script, scene and log in evidence/planning-checks/editor-capture/): the bubble material (lab-shaders/08-bubble.gdshader, byte-identical in the scratch project) on a 480 x 480 ColorRect. Frames in `_godot-shaders-series/editor-capture/png/1920x1080/soft-edges-glow-and-noise/`: soft-edges_E3-1_bubble-shader-parameters-two-color-swatches-and-slider (group Shader Parameters: rows Body Color and Highlight Color, both color swatches, and Brightness, a number box with a slider bar) and soft-edges_E3-2_body-color-picker-popup-open (the picker after a scripted click on the Body Color swatch: R 94, G 163, B 145, Hex 5ea391, Swatches, Recent Colors). Only 1920x1080 was recorded (one run); a 640 x 360 crop of it would blur in the 4K window, so re-record at native size (recipe in CAPTURE-PLAN.md section E, about 30 s) and crop the native frames: E3-1 x 1275 to 1915, y 195 to 555 (1920 coordinates, times 1.8 for native), E3-2 x 1275 to 1915, y 410 to 770, which ends above the line 'Screen Recording permission missing!' (the eyedropper needs a macOS permission). The ring box is a fraction of the E3-1 crop. Cross-dissolve at 0.86. No pointer is visible (the picker was opened by a scripted click): label 'scripted editor session'.

### B20 · 32 words · ~11 s

> Now the sum. The body color, plus the highlight color times the highlight mask. Where the mask is zero, nothing is added. Where it is one, the highlight color lands in full.

*Picture.* Code card at left (the 14-line bubble shader); at right the real render: the teal bubble with its pale highlight at the upper left. The rgb line is highlighted first, then the highlight line.

*Motion.* The sum line lights up, then the highlight mask line.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C09: the square target, lab-shaders/08-bubble.gdshader at its defaults (brightness 1.0), still PNG 3840 x 2160, Forward+. Verified: the highlight's centre reads (0.918, 1.000, 1.000) on screen (the shader's rgb is 0.919, 1.159, 1.019 before the screen clips it); the body away from the highlight reads (0.514, 0.776, 0.690).

### B21 · 36 words · ~12 s

> A trap. Add a brightness dial for the whole bubble. Multiplication always happens before addition. So a plus b times c multiplies b and c first, and only the highlight dims. Wrap the sum in parentheses.

*Picture.* The expression a + b * c as a small tree: b * c is ringed first (terracotta), then the plus. Beneath it the parenthesised (a + b) * c with the plus ringed first. Numbers on the leaves: a = 0.64 (the body, green channel), b = 0.52 (the highlight, green channel), c = 0.6 (brightness); results written under each: 0.95 and 0.70. Label 'multiply binds first'.

*Motion.* The ring lands on b * c first in the left tree and on a + b first in the right one, and the two results differ.

*Lane.* manim · `B21_EvaluationOrder` · runner-up: BrowserCapture of the docs operator table

### B22 · 34 words · ~12 s

> Real numbers from this Mac, brightness point six. With the parentheses, the highlight's center reads point seven in green, and the whole bubble dims. Without them, point nine five, and the body barely moves.

*Picture.* Two real Godot panels side by side on the cream stage: the left bubble uses the shader with the parentheses, the right one the shader without. Brightness is swept from 1.0 to 0.6 on both; the left bubble dims all over, the right one keeps its teal body and only its highlight dims. Readouts under each: 'with: green 0.70' and 'without: green 0.95'.

*Motion.* Both bubbles are dialled down together: one dims all over, the other barely changes.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C10: two-panel scene script (`--scene`, as the Lines film's two_panels.gd): two square targets side by side (left lab-shaders/08-bubble.gdshader, right lab-shaders/09-bubble-bug.gdshader), brightness 1.0 held 1.5 s then swept to 0.6 by 4.5 s on both (`--animate left.brightness:0:1,1.5:1,4.5:0.6` and the same for right), held; 12 s, 30 fps, Forward+, stage #D9D5CA. Verified: at brightness 0.6 the highlight centre reads green 0.694 (with parentheses) and 0.953 (without); the body away from the highlight reads green 0.467 and 0.722; at 1.0 both read 0.776.

### B23 · 26 words · ~9 s

> Godot's own table says the same. Parentheses come first, then multiply and divide, then add and subtract. When in doubt, add a pair. They cost nothing.

*Picture.* The real Godot 4.7 'Operators' table in a browser window; the camera pushes in on the first four rows (parenthetical grouping, unary, multiplicative, additive) and a terracotta ring marks the multiplicative and additive rows.

*Motion.* The camera pushes in on the table and the ring lands on 'multiplicative' above 'additive'.

*Lane.* remotion · `BrowserCapture` · runner-up: manim table redrawn

## Act IV: Noise That Moves

### B24 · 33 words · ~11 s

> Noise is a texture of smooth random values: nearby pixels look alike, far ones do not. Godot makes it for you: a noise texture two D, filled by a fast noise lite generator.

*Picture.* Act title 'Noise That Moves' (serif 40) top-left. Code card at left with the sampler line highlighted twice, each time with its definition label (noise, then texture). At right two real stills of Godot's Inspector from a scripted editor session, one after the other: first the NoiseTexture2D itself (Width 512 px, Height 512 px, its Noise slot holding a FastNoiseLite, a Seamless row; this view has no preview), with a terracotta ring on the NoiseTexture2D header and then on the Noise slot; then the FastNoiseLite itself, where the grey clouds preview appears, with the ring on the preview.

*Motion.* The ring lands on the NoiseTexture2D, then on its Noise slot, then on the cloud preview of the generator, as the voice names them.

*Lane.* editor · `ShaderLab` · runner-up: ShaderLab render of the noise texture as teal alpha (labelled)

*Capture to record.* E1 (reused; DONE by script, 2026-10-13): two frames recorded in the same scratch project for the Textures and Color film and shown here because they show the same thing (the resource itself, not the slot's label, so the other film's shader does not show): `_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/textures-and-color_E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite.png` (the NoiseTexture2D view: Width, Height, Generate Mipmaps, Noise = FastNoiseLite, Color Ramp, Seamless, Invert, In 3D Space, As Normal Map, Normalize; NO preview) and `textures-and-color_E1-3b_inside-FastNoiseLite-preview-clouds.png` (the FastNoiseLite view: the grey clouds preview with a 3D button, Noise Type Simplex Smooth, Seed 0, Frequency 0.01, Offset, Fractal, Domain Warp). Both also exist as native 3456x1944 twins in png/3456x1944/textures-and-color/: crop those, x 1275 to 1915, y 195 to 555 in 1920 coordinates (times 1.8 for native). Cross-dissolve at 0.84; the ring boxes are fractions of that crop. (This film's own scene with a `noise` slot was never recorded: the frames above show the same two views.) No pointer: label 'scripted editor session'.

### B25 · 38 words · ~13 s

> A shader reads it through a sampler two D uniform, the type for a texture. The function texture does a lookup: what value sits at this address? Multiply that into the alpha, and the disc turns to cloud.

*Picture.* Code card at left (the noise-cloud shader); at right the real render: the teal disc turned to cloud, bright patches where the noise is high and see-through patches where it is low.

*Motion.* The three lines light up in turn while the clouds sit in the disc.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C11: scene script (`--scene`; the Lab only binds a plain image): NoiseTexture2D with FastNoiseLite defaults, 512 x 512, seamless on, bound to the 'noise' uniform of lab-shaders/10-noise-cloud.gdshader on the square target; still PNG 3840 x 2160, Forward+. Node setup as in evidence/planning-checks/noise_check.gd (make_noise, make_rect).

### B26 · 34 words · ~12 s

> To move it, add time to the address. Time is seconds on one clock shared by the whole game. Each second, the lookup slides a tenth of the way along, and the clouds drift.

*Picture.* Code card at left (the scroll shader: the lookup now adds TIME times a tenth to the address); at right the real render: the clouds drift steadily sideways inside the disc. The TIME definition is on screen.

*Motion.* The clouds drift while the lookup line is highlighted.

*Lane.* capture · `ShaderLab` · runner-up: manim sliding lookup

*Capture to record.* C12: scene script as C11 (NoiseTexture2D seamless on) with lab-shaders/11-noise-scroll.gdshader; 12 s, 30 fps, Forward+, `--time-origin 0` so TIME is 0 at the first frame (no scripted input). Verified: a 3.0 s clock step moves the shader's TIME by 3.01 s and the pattern by 0.3 of the width, i.e. 0.1 per second (noise_check Z); the natural clock matched the engine's ticks in an earlier run (run-0 transcription, item 7).

### B27 · 34 words · ~12 s

> Watch the direction. Adding to the address slides the lookup right, so the picture moves left. Measured here: add one eighth, and the clouds moved thirty-two pixels left, exactly one eighth of the width.

*Picture.* A long strip of noise bars (grey tones) with a terracotta window frame laid over it, the picture seen through the frame shown above. The frame slides right along the strip while the pattern seen through it shifts left. Labels 'lookup moves right' and 'picture moves left'; a readout '+0.125 → 32 px left' with the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+'.

*Motion.* The frame slides right and the pattern inside it slides left.

*Lane.* manim · `B27_WindowSlides` · runner-up: ShaderLab with a direction arrow

### B28 · 36 words · ~12 s

> Now delete the hint on that uniform and let it run. Past the edge of the texture, a lookup returns the edge pixel, row after row. The right side smears into streaks, and the motion stops.

*Picture.* Code card at left: the same scroll shader with the hint removed from the uniform line; at right the real render: the clouds drift for a moment, then the right side of the disc smears into horizontal streaks that grow leftward as time passes. A terracotta ring on the streaks.

*Motion.* Streaks grow from the right edge and take over the picture while the clouds stop moving there.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C13: scene script as C11 with lab-shaders/12-noise-no-repeat.gdshader; 12 s, 30 fps, Forward+, `--time-origin 0`. Verified: a raw greyscale check with lookups past 1.0 has row standard deviation 0.0 in the clamped half (identical along every row) and 0.1485 with repeat_enable (noise_check C).

### B29 · 33 words · ~11 s

> Put the hint back: repeat enable. A lookup past one now wraps around to the start, so the scroll never ends. But look at the line where the right edge meets the left.

*Picture.* Code card at left (the hint is back on the uniform line); at right the real render with a plain, non-seamless noise texture: the clouds scroll forever, and a straight vertical line, a seam, crosses the disc and travels left. A terracotta ring on the seam.

*Motion.* The seam travels left across the disc as the clouds scroll.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C14: scene script: NoiseTexture2D with FastNoiseLite defaults, 512 x 512, seamless OFF, bound to lab-shaders/11-noise-scroll.gdshader on the square target; 12 s, 30 fps, Forward+, `--time-origin 0` (the seam then sits at UV x 0.9 at 1 s and 0.2 at 8 s). Verified: the plain texture's wrap difference is 14.25x the normal neighbour difference; the render's biggest column jump sits at the wrap position (ratio 7.4 to 7.7) and moves as 1 - 0.1 * TIME (77 px per 3 s step).

### B30 · 36 words · ~12 s

> That line is real: this texture's edges do not match. In the noise texture, switch on seamless, and Godot blends the edges so they meet. The docs warn it may cost some contrast. Here, a little.

*Picture.* Two real Godot panels side by side showing the scrolling disc: the left uses a plain noise texture and a seam crosses it; the right uses the same settings with Seamless switched on and no seam appears. Labels 'seamless off' and 'seamless on'.

*Motion.* The seam crosses the left disc while the right disc scrolls cleanly.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C15: two-panel scene script (`--scene`): two square targets side by side with lab-shaders/11-noise-scroll.gdshader, left NoiseTexture2D seamless off, right seamless on (same FastNoiseLite defaults, 512 x 512); 12 s, 30 fps, Forward+, `--time-origin 0`. Verified: wrap difference 14.25x the neighbour difference (off) against 1.07x (on); contrast (standard deviation) 0.168 against 0.158; the render has no outlier column with seamless on (ratio 1.3 to 1.6).

### B31 · 36 words · ~12 s

> Noise can also hide and show. Compare it with a number climbing from zero to one: wherever the noise is below the number, show the pixel. The disc blooms in blotches. That number is a uniform.

*Picture.* Code card at left (the reveal shader); at right the real render: as progress climbs from 0 to 1 the disc blooms in blotches, small islands first, then merging until the whole disc is on. A label with the progress value.

*Motion.* Islands of teal appear, grow and merge as the number climbs.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C16: custom scene as C11 (seamless on) with lab-shaders/13-noise-reveal.gdshader, progress held 0 for 1 s, swept to 1 by 9 s, held (`--animate progress:0:0,1:0,9:1`); 12 s, 30 fps, Forward+. Verified: coverage of the disc interior 1.3 % / 43.7 % / 93.1 % at progress 0.25 / 0.5 / 0.75 (noise_check R).

### B32 · 38 words · ~13 s

> Progress is not percent shown. Noise values bunch near the middle. At one quarter, about one percent of the disc is on. At one half, forty-four percent. At three quarters, ninety-three. Remap the number for an even pace.

*Picture.* Top: a bell-shaped histogram of the noise values from 0 to 1 (20 bars, real data from noise_check T-seamless), centred near 0.5. Below it the cumulative curve from the same noise (real data, noise_check R-curve): an S rising slowly, then fast, then slowly. Three terracotta dots on the curve at progress 0.25, 0.5 and 0.75, labelled '1 %', '44 %' and '93 %'. Label 'progress is not percent shown' and the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ · NoiseTexture2D defaults'.

*Motion.* The bars rise into a bell, the curve draws as their running total, and the three dots land at 1, 44 and 93 percent.

*Lane.* manim · `B32_RevealPace` · runner-up: ShaderLab with a percent readout

## Act V: Glow, Honestly

### B33 · 35 words · ~12 s

> The trick you will see everywhere: multiply a color by a number above one. Teal times six puts green and blue well above one. The screen cuts everything above one, so the bubble turns white.

*Picture.* Act title 'Glow, Honestly' (serif 40) top-left. Three vertical bars (red, green, blue channels of teal times six: heights 2.2, 3.8 and 3.4) grow past a horizontal line at 1.0 labelled 'the screen stops here'. The parts above the line are cut away in hatched grey and all three bars end at 1. A swatch at right turns from teal to white. Label 'teal × 6'.

*Motion.* The bars grow past the line, the tops are cut off, and the swatch turns white.

*Lane.* manim · `B33_ClipAtOne` · runner-up: ShaderLab render of the flat white bubble

### B34 · 36 words · ~12 s

> In the shader, the dial is one plus glow times five, in parentheses, as before. Turn glow up, and the bubble does not glow. It goes flat white. The teal and the highlight are both gone.

*Picture.* Code card at left (the 14-line glow shader); at right a real Godot window on a slate-blue stage: the teal bubble with its highlight turns paler and then flat white as glow is swept from 0 to 1. Readouts 'glow 0' and 'glow 1'.

*Motion.* The bubble loses its teal and its highlight and ends as a flat white disc.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C17: the square target, lab-shaders/14-glow-bubble.gdshader, default 2D rendering (no HDR 2D, no environment), stage #5F7A96, glow 0 held 1 s, swept to 1 by 7 s, held (`--animate glow:0:0,1:0,7:1`; stage via `--clear`/the scene script); 12 s, 30 fps, Forward+. Verified: glow 0 body (0.514, 0.776, 0.690); glow 1 body (1, 1, 1), spot (1, 1, 1) (glow-results G0, G1).

### B35 · 40 words · ~14 s

> H D R means high dynamic range: colors allowed to go brighter than one. Godot's two D drawing does not allow them by default. The setting is H D R two D, under Rendering, Viewport. Restart after switching it on.

*Picture.* The real 'Using glow in 2D' section of the Godot 4.7 documentation in a browser window; the camera pushes in on 'To enable HDR in 2D, open the Project Settings, enable Rendering > Viewport > HDR 2D then restart the editor.' and a terracotta ring marks it. The caption under the browser window is the GLOSSARY definition of HDR 2D, one line; the real address in the window's bar and SOURCES.md carry the provenance.

*Motion.* The camera pushes in on the sentence the voice is describing.

*Lane.* remotion · `BrowserCapture` · runner-up: GodotDevWorkbench reconstruction of Project Settings (labelled)

### B36 · 41 words · ~14 s

> Run one: H D R two D on, glow off. Still white, with a tinted rim, because green and blue are cut off before red. On this Mac the frame holds the real numbers: green reads about two and a half.

*Picture.* A real Godot window on the slate-blue stage showing the flat white bubble (glow 1), then at 2 s H D R 2D is switched on: the disc stays white but its rim picks up a teal-cyan tint. Readouts 'HDR 2D on', 'frame: green 2.57' and 'screen: 1.0'.

*Motion.* The rim turns cyan the moment the setting is switched on, and the two readouts show what the frame holds and what the screen shows.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C18: custom scene: the square target with lab-shaders/14-glow-bubble.gdshader (glow 1.0), stage #5F7A96, root Viewport.use_hdr_2d set to true at 2.0 s (`--call-at 2.0:enable_hdr_2d`, scripted), no environment; 8 s, 30 fps, Forward+. Verified (toggle_check, glow-results G1 and G3): the soft band reads (0.678, 0.733, 0.788) before and (0.726, 1.000, 1.000) after; a 256 px SubViewport with use_hdr_2d holds green 2.572 at the sample pixel (format RGBAH) while the screen shows 1.0; with it off the frame holds 1.0.

### B37 · 36 words · ~12 s

> Run two: add a world environment, switch glow on, and set its background to canvas. Now the bright disc bleeds a halo, tinted teal. The halo belongs to the environment. Your shader only supplied the number.

*Picture.* The same window, H D R 2D already on, flat white bubble on the slate-blue stage. At 2 s a world environment with glow on, background Canvas and intensity 2 comes into effect: a soft teal halo blooms around the disc. Readouts 'glow on', 'background: Canvas' and 'intensity 2'.

*Motion.* A teal halo blooms around the white disc the moment the environment's glow is switched on.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C19: custom scene: as C18 with use_hdr_2d already true; at 2.0 s a WorldEnvironment with an Environment (glow_enabled true, background_mode Canvas, glow_intensity 2.0, everything else default) is added (`--call-at 2.0:add_environment`, scripted); 8 s, 30 fps, Forward+. Verified (toggle_check step 2, glow-results G6): the stage next to the disc reads (0.373, 0.478, 0.588); 6 px beyond the band the halo reads (0.419, 0.553, 0.629), 16 px beyond (0.394, 0.513, 0.607), 28 px beyond (0.382, 0.494, 0.596). Without the Canvas background the same environment changes nothing (G4).

### B38 · 30 words · ~10 s

> So glow is three agreements. Your shader makes a number above one. The viewport keeps it. The environment turns it into light. Break any one, and you get plain white.

*Picture.* A flow of three stages left to right with a tall bar (the number above one) travelling through them: 'shader · makes a number above one', 'viewport · keeps it (H D R 2D)', 'environment · turns it into light (glow, Canvas)'. Run A: the bar passes all three and a halo blooms at the end. Run B: the viewport stage is off, a gate at height 1 cuts the bar to a stub and the picture ends flat white. Run C: the environment stage is missing, the tall bar arrives intact and nothing blooms.

*Motion.* A tall bar travels the chain: it blooms at the end when every stage is on, and is cut or ignored when one is off.

*Lane.* manim · `B38_ThreeAgreements` · runner-up: DesignPipelineClaim, show-tell isometric

### B39 · 35 words · ~12 s

> The halo grows with how far above one you go. At glow point five, it is faint. At one, clear. And glow adds light, so on a light background it has almost nowhere to go.

*Picture.* The slate-blue stage with the white-hot bubble: as glow is swept from 0 to 1 the teal halo is absent, then faint around 0.5, then clear at 1. Near the end the stage colour is switched to the pale warm grey and the halo almost vanishes. Readouts 'glow 0.5', 'glow 1', 'light stage'.

*Motion.* The halo swells as the dial climbs, then fades into a pale stage when the stage colour is switched.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C20: custom scene: as C19 (H D R 2D on, environment from the start), glow held 0 for 1 s, swept to 1 by 7 s, held (`--animate glow:0:0,1:0,7:1`), then at 9.0 s the clear colour switched from #5F7A96 to #D9D5CA (`--call-at 9.0:use_light_stage`, scripted); 12 s, 30 fps, Forward+. Verified (glow-results G11 to G15): halo at 6 px beyond the band: glow 0.1 and 0.3 none, 0.5 +0.003/+0.006/+0.003, 1.0 +0.046/+0.075/+0.041; on the light stage +0.008/+0.020/+0.020.

### B40 · 40 words · ~14 s

> Turning on H D R two D changes more than glow. Two D now renders in linear light. On this Mac, a color without the source color hint came out washed out: red point six four, not point three seven.

*Picture.* Two flat teal squares side by side on the stage, one whose color uniform has the source color hint and one without, identical at first. At 2 s H D R 2D is switched on: the left one stays teal, the right one turns pale. Readouts 'hinted: red 0.37' and 'unhinted: red 0.64'.

*Motion.* The right square washes out at the switch while the left one stays the same.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C21: custom scene: two 60 x 60 flat-color squares (uniform vec4 flat_color = vec4(0.37, 0.64, 0.57, 1.0), left with source_color, right without; evidence/planning-checks/shaders/ev-flat-hint.gdshader and ev-flat-nohint.gdshader), root use_hdr_2d set to true at 2.0 s (`--call-at 2.0:enable_hdr_2d`, scripted); 6 s, 30 fps, Forward+. Verified: SDR both read (0.369, 0.639, 0.569); H D R 2D with the hint (0.370, 0.640, 0.570), without (0.642, 0.821, 0.780). The Compatibility renderer shows no difference (not shown).

### B41 · 39 words · ~13 s

> Without H D R two D, the docs say to lower the glow threshold below one, so ordinary white glows. On this Mac that gave a faint halo with no color. H D R two D gives you both.

*Picture.* The slate-blue stage with the white bubble in the default pipeline and a world environment with glow on, background Canvas, threshold 0.5, intensity 2: only a faint, colourless halo. At 3 s H D R 2D is switched on and the threshold returns to 1: the halo grows and turns teal. Readouts 'threshold 0.5' then 'HDR 2D'.

*Motion.* A faint grey halo becomes a clear teal one at the switch.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C22: custom scene: the square target with lab-shaders/14-glow-bubble.gdshader (glow 1.0), stage #5F7A96, WorldEnvironment (glow on, Canvas background, intensity 2) with glow_hdr_threshold 0.5 and no HDR 2D; at 3.0 s use_hdr_2d true and the threshold back to 1.0 (`--call-at 3.0:enable_hdr_2d_and_reset_threshold`, scripted); 8 s, 30 fps, Forward+. Verified (glow-results G8 against G6): 6 px beyond the band the halo is +0.008/+0.004/+0.004 (no tint) against +0.046/+0.075/+0.041.

### B42 · 26 words · ~9 s

> Now all the layers together: the soft edge, the highlight, the noise drifting through, and the glow dial. One bubble, built a layer at a time.

*Picture.* The slate-blue stage with the finished bubble: a teal disc with a soft edge, a pale highlight at the upper left, clouds of noise drifting through it, and the glow dial sweeping from 0 to 1 so the bubble brightens toward white with a soft halo. Readouts 'glow 0' and 'glow 1'. No code panel: the shader is 16 lines (lab-shaders/15-bubble-complete.gdshader) and every line has been on screen already.

*Motion.* The finished bubble drifts and brightens as the dial climbs, all five layers at once.

*Lane.* capture · `ShaderLab` · runner-up: manim exploded view of the five layers

*Capture to record.* C23: scene script (`--scene`): the square target with lab-shaders/15-bubble-complete.gdshader and a seamless NoiseTexture2D (FastNoiseLite defaults, 512 x 512) bound to `noise`, H D R 2D on and a WorldEnvironment (glow on, Canvas background, intensity 2) from the first frame, stage #5F7A96, glow held 0 for 2 s, swept to 1 by 9 s, held (`--animate glow:0:0,2:0,9:1`), `--time-origin 0`; 12 s, 30 fps, Forward+. Verified (finale_check.gd, run-finale.log): the body at the sample pixel shows about (0.45, 0.66, 0.61) at glow 0, (0.66, 0.96, 0.87) at 0.3, (0.80, 1, 1) at 0.6, (0.98, 1, 1) at 1 (the scrolling noise moves each value by about 0.02 from run to run); the highlight centre reaches (1, 1, 1) by glow 0.6; 6 px beyond the band the stage (0.373, 0.478, 0.588) reads (0.383, 0.494, 0.597) at glow 1 (a faint halo: the noise thins the alpha).

## Closing

### BVDT · recap · 74 words · ~25 s

> Let's recap with Claude. A soft edge is a ramp, and smooth step lets you choose its width. A falloff fades with distance, and a power tightens it. Multiply masks to keep both, add them to show either. Wrap a sum in parentheses before you scale it. Noise gives structure, time scrolls it, repeat and seamless keep it going. A color above one glows only when the shader, the viewport and the environment agree.

*Picture.* The recap card: A soft edge is a ramp, and smoothstep lets you choose its width. / A falloff fades with distance, and a power tightens it. / Multiply masks to keep both, add them to show either. / Wrap a sum in parentheses before you scale it. / Noise gives structure, time scrolls it, repeat and seamless keep it going. / A color above one glows only when the shader, the viewport and the environment agree.

### BHTF · your turn · 93 words · ~32 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader for a square Color Rect. Draw a teal disc with a soft edge, using smooth step on the distance from the middle. Add a float uniform called softness with a hint range from zero point zero two to zero point four, and keep the width above zero with max. Then point me to the three lines I should check. Then check two things yourself. Does dragging softness widen and narrow the fade? And is the shape a circle, not an oval?

*Prompt shown and read in full:* Write a Godot canvas item shader for a square Color Rect. Draw a teal disc with a soft edge, using smooth step on the distance from the middle. Add a float uniform called softness with a hint range from zero point zero two to zero point four, and keep the width above zero with max. Then point me to the three lines I should check.

*Two checks:* Check: dragging softness in the Inspector widens and narrows the fade, with no hard jump at the lowest setting. · Check: the shape is a circle, not an oval.

### BOUT · outro · 9 words · ~4 s

> Soft Edges, Glow and Noise. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


# Script: Outlines

**What this is.** The words Liam will say in *Outlines*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 47 beats, 1855 words, about **10:35** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 27, manim 11, remotion 3.

**If it runs long.** Cut, in this order: the line-color beat (B14), the loop-cost beat (B22), the branch beat (B24), the modulate beat (B40), then the thin-part beat (B37) and the brush-number beat (B35). The corner beat (B17), the padding beats (B29 to B31) and the checks table (B41) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Ask the Neighbors | 10 | 378 | ~2:09 |
| II | Pixel-Sized Steps | 7 | 261 | ~1:29 |
| III | Say It with a Loop | 10 | 383 | ~2:10 |
| IV | Room to Draw | 6 | 241 | ~1:22 |
| V | Where It Breaks | 8 | 299 | ~1:42 |

## Opening

### BOPEN · identity card · 28 words · ~10 s

> Outlines. Learn how a shader draws a line around a sprite by asking each pixel about its neighbors, and the traps that make an outline vanish or break.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Outlines", and the line "How a shader draws a line around a sprite".

### BIDEA · the question · 42 words · ~14 s

> Hallo. This is Liam, in for Bear. Most people picture an outline as a bigger copy of the sprite, hiding behind it. A shader has no second copy. Each pixel asks a question about its neighbors, and the answers draw the line.

*Picture.* The hesitant writer types: "An outline is
a bigger copy behind the sprite." then deletes "a bigger copy behind the sprite" and types "a question about neighbors".

### BDEFS · terms · 55 words · ~19 s

> Six terms. A shader is a small program the graphics card runs to decide how something is drawn. A texture is an image a shader can read. Alpha is how visible a pixel is. Opaque means fully visible. A neighbor is the pixel next to this one. And padding is empty space around an image.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **Texture** — an image a shader can read by address; **Alpha** — how visible a pixel is: 0 invisible, 1 solid; **Opaque** — fully visible: nothing shows through; **Neighbor** — the pixel right next to this one; **Padding** — empty space added around an image

## Act I: Ask the Neighbors

### B01 · 34 words · ~12 s

> A sprite can melt into a busy background. Watch what an outline does: one clean line around its shape, in any color you like. The picture file never changes. A shader draws the line.

*Picture.* Act title 'Ask the Neighbors' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite sits plain, then the outline shader switches on and a clean indigo line appears around its whole shape. Labels under the sprite: 'shader off', then 'shader on'.

*Motion.* The sprite is plain, then a line appears around it the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a sprite gaining a line

*Capture to record.* C01-hook: scene spec evidence/planning-checks/scenes/C01-hook.json, 11.6 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The same sprite; the outline shader (08-loop, thickness 3) switches on as the voice says 'outline'. Verified: no outline pixels before the switch, a 12 px (3 image px x 4) line after it (planning check C01)

### B02 · 41 words · ~14 s

> The old trick draws a bigger copy of the sprite behind it. Scale a plus sign up a fifth: the tips get a thick border, the sides a thin one. Each edge moves in proportion to its distance from the middle.

*Picture.* A plus-shaped teal sprite on the stage with a tinted (indigo) copy behind it that grows by a fifth as the voice says it. The copy shows as a thick border at the four tips and a thin one along the sides. Labels 'tip: thick' and 'side: thin' with one ring on each.

*Motion.* The copy swells out from behind the sprite: the border is fat at the tips and thin along the sides.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing with measured tick marks

*Capture to record.* C02-bigcopy: scene spec evidence/planning-checks/scenes/C02-bigcopy.json, 13.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. A plus-shaped sprite (drawn 6x) with a tinted copy behind it that grows by a fifth (6x to 7.2x): tips thick, sides thin. Verified: tip border 10 px, side border 3 px, ratio about 3 (analyze_bigcopy H1); the scene frame at 6x to 7.2x reads 29 and 9 px (analyze_scenes C02)

### B03 · 40 words · ~14 s

> The shader asks something else. The graphics card runs one small program for every pixel, and each pixel checks its own alpha and the pixels around it. Am I empty, with an opaque neighbor? Then I am on the outline.

*Picture.* A pixel grid (outline-only cells, no fill behind text) with the teal test sprite's silhouette as filled cells in the middle. One empty cell beside the sprite gets a terracotta ring and four short arrows to its four neighbors; the right neighbor is a filled cell and lights up. The ringed cell takes the line color (indigo) and a label reads 'on the outline'. Then a cell inside the sprite is asked: its own cell is opaque, label 'keeps its color', and it stays teal.

*Motion.* A ring visits one empty cell, four arrows reach out, the right neighbor lights, the cell turns the line color; then a sprite cell is asked and keeps its color.

*Lane.* manim · `B03_TheQuestion` · runner-up: ShaderLab result

### B04 · 36 words · ~12 s

> To look next door, a pixel reads the sprite's image at another address. The function is texture. U V is the pixel's own address, so U V plus a small step is the spot beside it.

*Picture.* The series' uv_square: a square with a 0 to 1 axis across the top and down the left side (the second axis pointing DOWN). A terracotta dot rests at the middle with the glossary line 'UV: a point's address on the shape, 0 to 1 across, 0 to 1 down'. A second dot hops one small step to the right with a short arrow and the label 'UV + step'. A one-line code label 'texture(TEXTURE, UV + step)' types in under the square, with the glossary line 'TEXTURE: the node's own picture; texture(TEXTURE, uv) reads it' beside it.

*Motion.* The address dot hops one small step to the right, and the code line names exactly that hop.

*Lane.* manim · `B04_NextDoor` · runner-up: LectureCodeTrace with the single line

### B05 · 40 words · ~14 s

> What comes back is a color: four numbers, red, green, blue and alpha. Dot a picks the last one. Alpha zero is empty, alpha one is opaque. That one number is all the outline needs to know about a neighbor.

*Picture.* One pixel's color drawn as four outline boxes in a row: r, g, b, a (monospace labels). The fourth box lifts out and drops onto a 0 to 1 scale with two marks: 0 'empty' (a swatch showing stage color through) and 1 'opaque' (a solid teal swatch). The code fragment '.a' is drawn beside the lifted box.

*Motion.* The fourth box lifts out of the row and lands on a 0 to 1 scale, once at 0 and once at 1.

*Lane.* manim · `B05_FourNumbers` · runner-up: ClaudeCodeBeat with the line of code

### B06 · 34 words · ~12 s

> Now the color. Mix blends two colors by an amount. Amount zero keeps the sprite's color, amount one gives the line color, and anything between is a blend. Outside zero to one, mix overshoots.

*Picture.* The series' ramp strip as a color strip: the sprite's teal at the left end, the line indigo at the right end, end labels 0 and 1 and the glossary line 'mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b' above. A terracotta marker rides it to 0, then 0.5 (a blend), then 1. Then it continues past the right end to 2 and a small label 'overshoot' appears where the strip has ended.

*Motion.* A marker rides a color strip from teal to indigo and then keeps going past the end of the strip.

*Lane.* manim · `B06_MixRamp` · runner-up: LectureEvidenceTable

### B07 · 40 words · ~14 s

> First try, one question: is the pixel on my right opaque? If so, mix in the line color. Look what happens. Almost the whole sprite turns blue, because its own pixels have opaque neighbors too, and they all said yes.

*Picture.* Code card at left (the nine-line shader); at right a real Godot window: the plain sprite, then, as the voice says 'look what happens', the first try switches on and the whole sprite turns indigo except a thin teal crescent on its right edge.

*Motion.* The around line is highlighted, then the COLOR line; then the plain sprite turns blue the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C07-paints-the-sprite: scene spec evidence/planning-checks/scenes/C07-paints-the-sprite.json, 13.6 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The plain sprite; the first try (02-paints-the-sprite) switches on as the voice says 'look what happens': almost the whole sprite turns line colour. Verified: no outline pixels before the switch, then 95.8 percent of the sprite's pixels (71,112 of 74,192 at x4; 4,406 of 4,637 = 95.0 percent at 1:1) come out line coloured (analyze_scenes C07; analyze_lab A10)

### B08 · 39 words · ~13 s

> So ask one more thing: am I empty? Multiply by one minus my own alpha. Opaque pixels have alpha one, so they get zero and keep their color. Only empty pixels, on the left of the sprite, stay blue.

*Picture.* The same code card with the COLOR line highlighted and '* (1.0 - color.a)' marked; at right a real Godot window: the blue sprite of the first try, then, as the voice says 'multiply by one minus my own alpha', the fix switches on, the blue drains off and the sprite keeps its teal with only a thin indigo line along its left edge. One ring on the line, readout 'left side only'.

*Motion.* The multiplication is highlighted and the blue fill drains off the sprite, leaving a line on its left edge.

*Lane.* capture · `ShaderLab` · runner-up: manim pixel grid

*Capture to record.* C08-one-question: scene spec evidence/planning-checks/scenes/C08-one-question.json, 13.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The blue sprite of the first try; as the voice says 'multiply by one minus my own alpha' the fix (03-one-question) switches on: the blue drains off, a line on the left only. Verified: before the fix 71,112 of 74,192 sprite px are line coloured; after it 3,080 outline px (x4), all left of the sprite's centre, none on the right, none on the sprite (analyze_scenes C08; 231 at 1:1, analyze_lab A2)

### B09 · 34 words · ~12 s

> Now ask all four sides, and add the answers. Almost right, but the diagonal stretches come out lighter. There, two neighbors are opaque, the sum is two, and mix overshoots past the line color.

*Picture.* Code card (the four reads added into one number, no cap); at right a real Godot window: the one-sided line of the last beat, then, as the voice says 'all four sides', a ring appears around the sprite, its diagonal stretches visibly lighter (periwinkle) than the rest. Two rings on the lighter stretches, readout 'sum = 2'.

*Motion.* The four sides switch on and a ring appears; the sum lines are highlighted, rings land on the lighter diagonal stretches, then the COLOR line.

*Lane.* capture · `ShaderLab` · runner-up: manim ramp strip (the overshoot)

*Capture to record.* C09-lighter-diagonals: scene spec evidence/planning-checks/scenes/C09-lighter-diagonals.json, 11.6 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The one-sided line; as the voice says 'all four sides' the four reads (04-lighter-diagonals) switch on: a ring with lighter stretches on the diagonals. Verified: the one-sided line (3,080 px, all left of the centre) becomes a ring of 8,992 px of which 3,328 (37.0 percent) are (128,128,255) (analyze_scenes C09); at 1:1 252 of 672 (37.5 percent), the line colour doubled and clamped, on the diagonal stretches (analyze_lab A3, A11, A14)

### B10 · 40 words · ~14 s

> Cap the sum with min. Min of the sum and one can never be more than one, so mix never overshoots. Now every pixel of the ring is the same blue. Four reads, one cap, one mix: a complete outline.

*Picture.* The same code card with min(around, 1.0) marked; at right a real Godot window: the ring with lighter stretches, which settles, as the voice says 'so mix never overshoots', into a clean ring of one blue all the way round the sprite. Readout 'same blue'.

*Motion.* min(...) is highlighted and the lighter stretches settle to the same blue as the rest.

*Lane.* capture · `ShaderLab` · runner-up: manim 'min' clamp drawing

*Capture to record.* C10-four-questions: scene spec evidence/planning-checks/scenes/C10-four-questions.json, 13.6 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The ring with lighter stretches; as the voice says 'so mix never overshoots' the cap (05-four-questions) switches on: a uniform ring. Verified: before the cap 3,328 of 8,992 ring px are the wrong colour, after it 0 (analyze_scenes C10; analyze_lab A3)

## Act II: Pixel-Sized Steps

### B11 · 40 words · ~14 s

> So far the step was point oh two: two percent of the picture. In pixels, that depends on the image: two and a half here, less than one on a thirty-two pixel sprite. Pixel art needs steps of whole pixels.

*Picture.* Act title 'Pixel-Sized Steps' (serif 40) top-left. Three horizontal image strips stacked, drawn the same width and made of 32, 64 and 128 outline cells; on each a terracotta bracket spans two percent of the width and a grey label counts the cells it covers: 0.64, 1.28 and 2.56. The 128 strip's bracket covers two and a half cells; the 32 strip's covers less than one. Caption 'step 0.02'.

*Motion.* A bracket of the same relative width settles on three strips and covers a different number of cells on each.

*Lane.* manim · `B11_StepInPixels` · runner-up: capture of three real renders at three sizes

### B12 · 34 words · ~12 s

> Godot hands your shader a built-in for exactly this: texture pixel size, the size of one image pixel, in address units. For a sixty-four by thirty-two image, one over sixty-four and one over thirty-two.

*Picture.* The real Godot 4.7 'CanvasItem shaders' page in a browser window, scrolled to the fragment built-ins table; the camera pushes in on the TEXTURE_PIXEL_SIZE row and one terracotta ring marks it. The caption under the window gives the film's definition of a built-in and says where and when the page was captured.

*Motion.* The camera pushes in on the row the voice is naming.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: a text card with the formula

### B13 · 38 words · ~13 s

> Multiply it by a thickness, a uniform: a value your game sets, the same for every pixel. Thickness one, two, three, four: the line is exactly one, two, three, four pixels wide. I measured it on this render.

*Picture.* Code card at left (the four-read shader with TEXTURE_PIXEL_SIZE * thickness); at right a real Godot window: the line around the sprite steps from one image pixel wide to two, three and four as the voice counts. Readouts '1 px' ... '4 px'; a caption carries the glossary line for 'uniform'.

*Motion.* The dx and dy lines are highlighted, then the thickness uniform; the ring thickens in steps.

*Lane.* capture · `ShaderLab` · runner-up: manim ramp strip with a thickness marker

*Capture to record.* C13-thickness-steps: scene spec evidence/planning-checks/scenes/C13-thickness-steps.json, 12.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Thickness 1, then 2, 3, 4 as the voice counts; the line is that many image pixels wide (x4 on the canvas). Verified: axis widths exactly 1, 2, 3, 4 canvas px x scale at thickness 1 to 4 (analyze_lab A4; scene C13 measured at x4: 4, 8, 12, 16)

### B14 · 38 words · ~13 s

> The line color is a uniform too. The word after the colon, source color, is a hint: it says this vec four is a color. Change the value and the line follows. Nothing else in the shader moves.

*Picture.* The same code card with the line_color uniform line highlighted ('source_color' marked); at right a real Godot window: the line around the sprite changes from indigo to magenta to amber while nothing else moves. Caption carries the glossary line for 'hint'.

*Motion.* The uniform line is highlighted and the line color changes twice.

*Lane.* capture · `ShaderLab` · runner-up: manim colour chips

*Capture to record.* C14-line-color: scene spec evidence/planning-checks/scenes/C14-line-color.json, 12.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The same shader, the line_color uniform changing: indigo, magenta, amber. Verified: the ring colour read from the frames is the uniform's value each time (scene check C14)

### B15 · 35 words · ~12 s

> Another way to see it: each read is the whole picture, slid by the step. Four reads are four slid copies, added together. The outline is wherever the copies stick out past the sprite itself.

*Picture.* The teal test circle drawn in the middle. Four ghost copies (grey circle outlines, each with a small terracotta dot at its center) slide out one step up, down, left and right and overlap. Where the ghosts stick out past the circle, the union is shaded in the line color: a ring. The original circle sits on top, teal, subtracting itself. Labels (1 to 3 words): 'read right', 'copy goes left', 'four copies', 'minus the sprite'.

*Motion.* Four ghost copies slide out of the sprite, overlap, and the part that sticks out past the sprite fills with the line color.

*Lane.* manim · `B15_GhostCopies` · runner-up: ShaderLab capture of the slid copies

### B16 · 41 words · ~14 s

> The step counts pixels of the image, not of the screen. Draw the sprite twice as big, and thickness two becomes four screen pixels. Three times as big, six. The line grows with the sprite, which is what pixel art needs.

*Picture.* One real sprite at three sizes in turn (drawn 1x, 2x, 3x) with the same thickness 2: the line around it is two, then four, then six canvas pixels wide. Readouts '2 px', '4 px', '6 px' under it.

*Motion.* The sprite doubles, then triples, and its line grows with it.

*Lane.* capture · `ShaderLab` · runner-up: manim: three sprites in a row

*Capture to record.* C16-scales: scene spec evidence/planning-checks/scenes/C16-scales.json, 13.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Thickness 2 at sprite scale 1, 2, 3: the line is 2, 4, 6 canvas pixels. Verified: thickness 2 reads 2, 4, 6 canvas px at scales 1, 2, 3 (analyze_lab A7)

### B17 · 35 words · ~12 s

> Four reads have one flaw. On a square sprite they leave the corners empty: at thickness three, a three by three hole in each one. Add the four diagonal neighbors, and the corners fill in.

*Picture.* Two real square sprites (teal squares with the two cream eyes) side by side with the outline thickness stepping up to three: the left one (four reads) shows a square notch in each corner of its line, the right one (eight reads) is a complete frame. A ring on one empty corner and the readout '3×3 hole'.

*Motion.* The line grows around both squares; the left one's corners stay empty while the right one's fill.

*Lane.* capture · `ShaderLab` · runner-up: manim: a square with the missing corner cells drawn

*Capture to record.* C17-corners: scene spec evidence/planning-checks/scenes/C17-corners.json, 11.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Left four reads, right eight reads, thickness 1 to 3: the four-read corners stay empty (3 x 3 image pixels each at thickness 3). Verified: eight reads draw exactly 4 x t x t more pixels than four reads on a square: 4, 16, 36, 64 at t = 1 to 4 (analyze_crate K1)

## Act III: Say It with a Loop

### B18 · 26 words · ~9 s

> Eight reads, written out: the four sides and the four corners. It works. It is also eight nearly identical reads, which is exactly where typos hide.

*Picture.* Act title 'Say It with a Loop' (serif 40) top-left. Code card at left: the eight-read shader (14 lines); the first two lines of reads are marked, then the two lines of corner reads, then all four read lines together. At right a real Godot window with the square sprite: with the four sides only, the corners of its line stay empty; as the voice says 'the four corners' they fill in and the frame is complete.

*Motion.* Focus lands on the side reads, then the corner reads, and the empty corners of the line fill in; then all eight reads at once.

*Lane.* capture · `ShaderLab` · runner-up: manim: eight arrows around a cell

*Capture to record.* C18-eight-reads: scene spec evidence/planning-checks/scenes/C18-eight-reads.json, 8.8 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The square sprite at thickness 3: with the four sides only, the corners of the line stay empty; as the voice says 'the four corners' the eight reads (07-eight-reads) switch on and the corners fill in. Verified: on the square sprite at thickness 3 the eight reads add exactly 576 canvas px (4 x 3 x 3 x 16) to the four-read line, the corner holes (analyze_scenes C18); same picture as the loop (analyze_lab A6: 0 pixels differ at thickness 1, 2, 3, 4, 8)

### B19 · 38 words · ~13 s

> A loop says it once. For each y from minus one to one, and each x from minus one to one, read the alpha at that offset. Add it all up. Nine offsets, a three by three block.

*Picture.* Code card at left: the loop shader (14 lines); focus lands on the outer for, the inner for, the line that reads and adds, then the loop as a whole. At right the same complete frame on the square sprite, unchanged by rewriting the reads as a loop. A caption carries one plain line for 'for'.

*Motion.* Focus steps into the loop: outer for, inner for, the read.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C19-loop: scene spec evidence/planning-checks/scenes/C19-loop.json, still PNG, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. 08-loop at thickness 3 on the square sprite: the same complete frame the eight written-out reads drew. Verified: draws the same picture as the eight written-out reads: 0 pixels differ from the last frame of the previous capture (analyze_scenes C19; analyze_lab A6)

### B20 · 38 words · ~13 s

> The block's middle is the pixel itself, an extra read that changes nothing on hard-edged art. And those float calls are not decoration: Godot refuses to build a vec two from two whole numbers. Here is its message.

*Picture.* A 3 by 3 block of outline cells with offsets (-1,-1) to (1,1) written small in each cell and a terracotta center cell labelled 'me'. The nine cells light in loop order, row by row, and a '9 offsets' count ticks up. Beside it the one-line code 'vec2(float(x), float(y))' with the labels 'float: a decimal number' and 'vec2: a bundle of two numbers' on it, and under it a plain-shell box with the message the Shader Lab printed ('SHADER ERROR:' is the Lab's own prefix, the rest is the engine's text): SHADER ERROR: Invalid arguments for the built-in function: "vec2(int,int)".

*Motion.* The nine cells light one after another in loop order and the middle one is marked as the pixel itself.

*Lane.* manim · `B20_ThreeByThree` · runner-up: CCPlainShell for the message

### B21 · 33 words · ~11 s

> Same picture? I rendered both, at thickness one, two, three, four and eight, and compared every pixel. Zero pixels differ. On hard-edged art, the loop does exactly what the eight written-out reads did.

*Picture.* Two real sprites side by side, the eight-read shader on the left and the loop on the right, their lines growing together through thickness one, two, three, four and eight; the two pictures stay identical at every step. Labels under each; at the end the readout '0 pixels differ'.

*Motion.* Both rings grow in lockstep and stay identical.

*Lane.* capture · `ShaderLab` · runner-up: manim table of five zeros

*Capture to record.* C21-same-picture: scene spec evidence/planning-checks/scenes/C21-same-picture.json, 11.2 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Left eight written-out reads, right the loop; thickness 1, 2, 3, 4, 8 as the voice counts; zero pixels differ at every step. Verified: 0 pixels differ at thickness 1, 2, 3, 4 and 8, hard-edged sprite (analyze_lab A6; scene C21 frames)

### B22 · 48 words · ~16 s

> Count the work: nine reads in the loop, plus one for the pixel itself, ten per pixel. In a stress test on this Mac, four hundred million pixels a frame, ten reads took about ten milliseconds; a nine by nine block, eighty-two reads, about seventy. Time follows reads.

*Picture.* A horizontal bar chart on the cream stage: four bars grow left to right for a 3 by 3, 5 by 5, 7 by 7 and 9 by 9 block (10, 26, 50 and 82 reads per pixel), labelled with the measured milliseconds per frame (10, 24, 44 and 71, the whole-millisecond medians of the valid runs); a thin dashed floor line at 7.5 ms is labelled 'no shader'. A small grey credit: 'stress test: 403 million pixels a frame · Apple M4 Pro · Godot 4.7.2 · Forward+ · wall-clock, vsync off, median of runs · the card's own timer unreadable'. A last small caption: 'a 300 x 300 sprite: 90,000 pixels'.

*Motion.* The bars grow in turn, each longer than the last, as the read count goes up.

*Lane.* manim · `B22_CostBars` · runner-up: LectureEvidenceTable

### B23 · 40 words · ~14 s

> Many outline shaders wrap the loop in an if on the thickness. Thickness zero means off: the loop is skipped, and one read is left. Godot gives you no early exit here: a return inside fragment is a compile error.

*Picture.* A code card (monospace, 17 lines) of the guard shader with the line 'if (thickness > 0.0) {' and its closing brace highlighted. Beside it a small pixel grid where every cell follows the same arrow: with thickness 0 all cells go to 'skip: one read'; a switch flips to thickness 2 and all cells go to 'read ten'. Under the card a plain-shell box with the message the Shader Lab printed ('SHADER ERROR:' is the Lab's own prefix, the rest is the engine's text): SHADER ERROR: Using 'return' in the 'fragment' processor function is incorrect.

*Motion.* One switch flips and every cell changes its arrow together; the loop lines dim when the guard is false.

*Lane.* manim · `B23_Guard` · runner-up: ShaderLab with 09-guard code

### B24 · 44 words · ~15 s

> Is an if slow? Godot's shading language docs warn about discard and endless loops, not about if. A graphics book from two thousand five says a branch costs extra when neighboring pixels disagree. Here every pixel reads the same thickness, so they all agree.

*Picture.* Two pixel grids side by side. Left, titled 'per-pixel test': cells are split in two colors along the sprite's edge and the boundary cells hold different arrows (they disagree) and are ringed in terracotta. Right, titled 'thickness > 0.0': every cell holds the same arrow (they agree). Grey attribution under the left grid: 'GPU Gems 2, chapter 34, 2005'. Grey line under the right: 'shading language docs: no warning for if'.

*Motion.* Arrows appear in each cell; on the left the edge cells point two ways, on the right every arrow is the same.

*Lane.* manim · `B24_Agree` · runner-up: LectureEvidenceTable of the two quotes

### B25 · 35 words · ~12 s

> The guard does more than save work. Without it, thickness zero still paints line color into the half-transparent rim of a soft-edged sprite: two hundred and twenty-four pixels in my test. With the guard, none.

*Picture.* Two real soft-edged sprites side by side, both ringed at thickness two; then thickness drops to zero: the right one (guard) returns to its plain look, the left one (no guard) keeps a thin tinted rim. Labels 'no guard' and 'guard', one ring round the left sprite's rim, readout '224 pixels'.

*Motion.* Both rings switch off; one sprite is clean, the other still has a tinted rim.

*Lane.* capture · `ShaderLab` · runner-up: manim: pixel row of the rim with alpha values

*Capture to record.* C25-zero-means-zero: scene spec evidence/planning-checks/scenes/C25-zero-means-zero.json, 11.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Soft-edged sprites; thickness 2 (both ringed) then 0: the unguarded one keeps a tinted rim, the guarded one is clean. Verified: no guard: 224 rim pixels change colour (216 change alpha); guard: 0; hard-edged sprite: 0 either way (planning check B2)

### B26 · 39 words · ~13 s

> Your game turns the dial. When the unit is selected, set thickness to two. When it is not, set it back to zero. The call is set shader parameter on the material, with the uniform's name and a value.

*Picture.* Code card at left: the 11-line GDScript (a selected flag, _ready setting thickness 0, a key handler that sets 2 or 0); at right the real Godot window running it: no line, then a scripted key press at the word 'selected' draws the outline, a second press removes it. A label 'scripted input' stays on screen.

*Motion.* The key handler lights up and the line around the sprite appears and disappears with each press.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace with the script alone

*Capture to record.* C26-select: scene spec evidence/planning-checks/scenes/C26-select.json, 13.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The script on screen sets thickness 0 in _ready; a scripted key press selects (thickness 2) as the voice says 'selected', another deselects on 'not'. Verified: 0 outline px before, 632 after the first key, 0 after the second; thickness reads back 0.0 (verify_j J1)

### B27 · 42 words · ~14 s

> One trap. Set shader parameter changes the material, and units made from one scene share it, so every unit lights up at once. Declare the uniform as instance, and set it on the node instead. That value belongs to this instance only.

*Picture.* Two real units side by side that share one material. The dial is set on the left unit and BOTH light up (readout 'both lit'); then the shader declares the uniform as instance, each node gets its own value, and only the left unit stays lit (readout 'one lit'). A caption gives the film's definition of an instance uniform (the series' wording).

*Motion.* One unit is selected and both light up; after the fix, one unit is selected and only it lights up.

*Lane.* capture · `ShaderLab` · runner-up: manim: two boxes pointing at one material

*Capture to record.* C27-shared-material: scene spec evidence/planning-checks/scenes/C27-shared-material.json, 14.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Two units share one material. Until the voice says 'instance' the dial is an ordinary uniform: setting thickness 2 on the left outlines both. After it, an instance uniform: left 2, right 0, one material, one ring. Verified: shared material: setting 3 on one unit draws 960 px on it and 960 px on the other; instance uniform on a shared material: 960 px on one, the other keeps its own value (verify_j J2, J3)

## Act IV: Room to Draw

### B28 · 41 words · ~14 s

> Read a step to the right, and each pixel shows what is on its right, so the picture slides left. Slide it far enough, and its left side is cut off flat. A shader paints only inside the sprite's own rectangle.

*Picture.* Act title 'Room to Draw' (serif 40) top-left. Code card at left: the seven-line look-right shader. At right a real Godot window: the sprite slides left as the step grows, and when it reaches the left edge of its rectangle it is sliced off flat. A ring marks the whole image rectangle at the end; caption credits the docs.

*Motion.* The sprite slides left and the left side of it is cut off flat at the edge of the rectangle.

*Lane.* capture · `ShaderLab` · runner-up: manim: a rectangle with a shape pushed past its edge

*Capture to record.* C28-slide-clip: scene spec evidence/planning-checks/scenes/C28-slide-clip.json, 13.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The picture slides left as look goes 0 to 0.4; past about 0.2 the left of the sprite is cut flat by the rectangle. Verified: look 0.125 slides the sprite 16 image px left exactly; at 0.25 the left 6.4 image px are cut by the rectangle (analyze_lab A1; scratch A)

### B29 · 39 words · ~13 s

> That is the trap for outlines. Here the art was trimmed to its shape, with no empty border. Turn the outline up to four, and nothing appears where the shape touches the edge. The line has nowhere to go.

*Picture.* A real sprite whose image was trimmed to its round shape (no transparent border). The outline is turned up from zero to four; the line shows in the corners but is cut flat where the circle touches the top, right, bottom and left edges of the image. Four rings on those four places, readout 'no empty border'.

*Motion.* The outline grows around the circle and is missing at the four places where it touches the edge of the image.

*Lane.* capture · `ShaderLab` · runner-up: manim: a circle inside its square with arrows blocked

*Capture to record.* C29-tight: scene spec evidence/planning-checks/scenes/C29-tight.json, 13.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The sprite trimmed to its shape (77 x 77): thickness 0 to 4; nothing appears where the shape touches the edge. Verified: axis widths 0, 0, 0, 0 on the trimmed sprite at thickness 4; 808 line px against 1,296 for the padded art (analyze_padding P1)

### B30 · 31 words · ~10 s

> The fix is padding: transparent pixels around the image. In code, make a bigger transparent image, copy the original into the middle with blit rect, and make a texture from it.

*Picture.* A cream code card with the ten-line add_padding function: line focus walks through the signature and the get_image line, then the bigger transparent image (create_empty and fill), then the blit_rect copy, then the texture it returns. A caption gives the meaning of blit_rect in the film's own words: 'copy a piece of one image into another'.

*Motion.* Focus steps down the function as the voice describes it.

*Lane.* remotion · `LectureCodeTrace` · runner-up: manim code card with an image diagram

### B31 · 42 words · ~14 s

> Same shader, thickness four. No padding: the line is cut off. Two pixels of padding: cut at two. Four: the full ring. Pad by at least your thickest line. A centered sprite stays put; one that is not moves by the padding.

*Picture.* Three real copies of the trimmed sprite in a row at the same thickness four, padded by none, two and four pixels with the function from the previous beat: the left line is cut off, the middle cut at two pixels, the right a complete ring. Labels under each.

*Motion.* The line grows around all three; only the one padded by four gets a full ring.

*Lane.* capture · `ShaderLab` · runner-up: manim: three squares with a ring growing

*Capture to record.* C31-padding: scene spec evidence/planning-checks/scenes/C31-padding.json, 14.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The trimmed sprite with 0, 2 and 4 pixels of padding (the add_padding function on screen), thickness 0 to 4. Verified: axis widths 0, 2, 4 at thickness 4 with padding 0, 2, 4; line pixels 808, 1,104, 1,296; the padded art matches the original 1,296 (analyze_padding P1); a non-centered Sprite2D moves by the padding (4, 4) (verify_a log)

### B32 · 47 words · ~16 s

> A sprite sheet adds a twist: U V covers the whole sheet, not one frame. Godot's docs say so for regions; I measured it for frames. A read past a frame's edge lands in the next frame and draws a stray line. Separate frame images avoid it.

*Picture.* At left the whole packed sheet (a solid teal frame with two eyes beside the disc frame); at right only frame 1 on its own, outlined at thickness four: a tall stray line runs down its left edge, drawn from the solid frame next door. Ring on the stray line, readouts 'whole sheet', 'frame 1', 'stray line', a caption crediting the docs.

*Motion.* The outline switches on and a stray line appears along the frame's left edge.

*Lane.* capture · `ShaderLab` · runner-up: BrowserCapture of the Sprite2D docs

*Capture to record.* C32-sheet: scene spec evidence/planning-checks/scenes/C32-sheet.json, 16.0 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Left: the whole packed sheet; right: frame 1 only, outlined at thickness 4: a stray line along its left edge is frame 0's pixels. Verified: UV.x runs 0.506 to 0.996 across frame 1 (the whole sheet's space); a 4 image px (16 canvas px at x4) stray line; the same with region_enabled and with AtlasTexture frames; separate frame images follow the shown frame, outline margin 3 on every side for both (analyze_sheets C3); verify_c C1 to C4

### B33 · 41 words · ~14 s

> Padding is the simple cure. When you cannot pad, Godot gives the shader region rect, the visible frame. Clamp each read into it, and the stray line is gone: zero stray pixels in my test, and the sprite's own ring untouched.

*Picture.* Code card at left: eight lines of the sheet-safe shader (the lo and hi corners from REGION_RECT, and the clamp around each read). At right the same two-panel sheet scene: the stray line is there, then as the clamp is named it disappears while the disc's own ring stays. Readout 'stray line' then 'gone'.

*Motion.* The clamp line is highlighted and the stray line vanishes from the frame's edge.

*Lane.* capture · `ShaderLab` · runner-up: manim: arrows bent back at the frame border

*Capture to record.* C33-sheet-clamp: scene spec evidence/planning-checks/scenes/C33-sheet-clamp.json, 13.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The same frame; as the voice says 'clamp' the reads are clamped into REGION_RECT and the stray line disappears; the disc's own ring stays. Verified: REGION_RECT = (0.5, 0, 0.5, 1) (read as 0.502, the 8-bit value of 0.5) for hframes, region_enabled, an AtlasTexture sprite and an AnimatedSprite2D atlas frame; with the clamp the stray line is 0 px and the disc's ring is intact (verify_f F1 to F4, verify_i I3)

## Act V: Where It Breaks

### B34 · 29 words · ~10 s

> Now push the thickness. At eight, the four-read line pinches in at the diagonals. The eight-read line bulges into a rounded square. A ring of sixteen reads stays round.

*Picture.* Act title 'Where It Breaks' (serif 40) top-left. Three real sprites in a row, each with a different outline shader, the thickness growing together from one to eight: the left (four reads) pinches in at the diagonals, the middle (eight reads) bulges into a rounded square, the right (sixteen reads) stays round. Labels under each.

*Motion.* Three lines grow together and take three different shapes.

*Lane.* capture · `ShaderLab` · runner-up: manim: three outlines drawn from the formula

*Capture to record.* C34-brushes: scene spec evidence/planning-checks/scenes/C34-brushes.json, 9.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Four reads, eight reads, a ring of sixteen; thickness 1 to 8 as the voice says 'push the thickness ... at eight'. Verified: at thickness 8 the line is 8 px on the axes and about 5.1, 11.4 and 8.1 px on the diagonal for four, eight and sixteen reads, measured on the capture's own frames at x3 (analyze_scenes C34; the 1:1 Lab renders read 5.1, 11.4 and 8.5, analyze_lab A5)

### B35 · 33 words · ~11 s

> The reads are the brush. Four make a diamond, eight a square, sixteen a circle. Straight across, each line is eight pixels wide. On the diagonal I measured about five, eleven, and eight.

*Picture.* Three dot patterns around a center pixel: four terracotta dots in a diamond, eight in a square, sixteen on a circle, each with a faint grey ghost footprint behind it. Under each pattern a small disc outline with two tags, one on the axis and one at 45 degrees, carries the measured numbers: 'axis 8' on all three and 'diagonal 5.1' (four), 'diagonal 11.4' (eight), 'diagonal 8.1' (sixteen). Caption 'thickness 8 · measured on this render'.

*Motion.* The dots appear in a diamond, a square and a circle, and the measured numbers land under them.

*Lane.* manim · `B35_BrushShapes` · runner-up: LectureEvidenceTable of the numbers

### B36 · 41 words · ~14 s

> The ring is the loop with a different offset: sixteen angles around a full turn, one distance. Seventeen reads. Sine and cosine at every read cost extra: about thirty-seven milliseconds in the stress test, sixteen with the directions written as constants.

*Picture.* Code card at left: the 14-line ring shader; focus lands on the for, then the angle and direction lines, then the read. At right the ring on the sprite growing to thickness eight. Two readouts under it, 'sin/cos: 37 ms' and 'constants: 16 ms', with the stress-test credit as caption.

*Motion.* Focus lands on the loop, the angle and the read; the line grows round.

*Lane.* capture · `ShaderLab` · runner-up: manim code card

*Capture to record.* C36-ring: scene spec evidence/planning-checks/scenes/C36-ring.json, 13.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. The ring of sixteen reads, thickness 1 to 8. Verified: the ring and the constant-directions ring draw identical pictures (0 pixels differ); stress test about 37 ms against about 16 ms per frame (cost-summary.txt)

### B37 · 35 words · ~12 s

> Thin parts break it too. This stem is three pixels wide. At thickness eight, eight reads jump clean over it, and the line comes apart into floating copies. The ring of sixteen holds it together.

*Picture.* Two real sprites, each a disc with a three-pixel-wide stem ending in a small ball, the outline growing from one to eight. On the left (eight reads) the line around the stem comes apart into floating copies of the ball and detached stripes; on the right (ring of sixteen) the line wraps the stem as one piece. Labels under each, a ring on the floating copies.

*Motion.* The line grows; on the left it breaks into floating copies around the stem, on the right it holds together.

*Lane.* capture · `ShaderLab` · runner-up: manim: ghost copies of a thin shape

*Capture to record.* C37-stem: scene spec evidence/planning-checks/scenes/C37-stem.json, 11.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. A sprite with a 3-pixel stem: eight reads come apart into floating copies at thickness 6 to 8, the ring of sixteen holds. Verified: at thickness 8, on image row 17 (the stem just under the ball) eight reads leave five empty pixels each side of the stem and the line floats as copies, the ring of sixteen leaves none (analyze_scenes C37); over the whole sprite eight reads draw 96.0 percent of the true outline and sixteen 100.0 percent (analyze_mascot D1); on row 21 the diagonal reads reach the ball and the disc and fill the gap (D2)

### B38 · 39 words · ~13 s

> Soft edges are the next trap. Smooth art has half-transparent pixels on its rim. Mix blends alpha too, so the rim stays see-through: a quarter transparent at worst in my test. Compute the alpha yourself, and the seam closes.

*Picture.* Code card at left: the 14-line composite shader (edge, alpha and the vec4 line marked). At right two real 12x close-ups of the rim of a soft-edged sprite, both on the plain mix: pale, see-through pixels sit between the teal and the line. As the voice says 'compute the alpha yourself' the right one switches to the composite and its rim pixels turn solid; the left stays pale. Readouts 'alpha 0.75' and 'alpha 1.0'.

*Motion.* Focus lands on the three composite lines and the pale rim on the right turns solid while the left stays pale.

*Lane.* capture · `ShaderLab` · runner-up: manim: a row of rim cells with alpha values

*Capture to record.* C38-soft-edges: scene spec evidence/planning-checks/scenes/C38-soft-edges.json, 13.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. A 12x look at the rim of the soft-edged sprite: plain mix leaves pale, see-through rim pixels (alpha 0.75 at worst) on both sides; as the voice says 'compute the alpha yourself' the right side switches to the composite, which makes them opaque. Verified: 224 rim pixels all see-through with plain mix (output alpha 0.75 to 0.95, mean 0.82), 0 with the composite (alpha 1.00); on hard-edged art the two give the same picture (analyze_soft B1; analyze_lab A13); in the capture 7,056 canvas px of the right panel change at the switch and none of the left (analyze_scenes C38)

### B39 · 41 words · ~14 s

> And the texture filter. Linear filtering blends four pixels on every read, so the alpha you ask about turns blurry. In my test, linear made two thousand half-transparent pixels; nearest made none. Godot's default is linear. For pixel art, set nearest.

*Picture.* Two real 12x close-ups of the same outlined rim, both on the default linear filter and blurred. As the voice says 'nearest made none' the left one switches to the nearest filter: crisp one-pixel steps in one flat blue; the right one stays a blurred, soft-edged line of many shades. Labels 'nearest' and 'linear', the counts '0 half-transparent' and '2,008 half-transparent' (counted over the whole sprite at 2x, as the frame label says), a caption crediting the docs.

*Motion.* Both close-ups start blurred; the left one switches to nearest and turns crisp while the right one stays blurred.

*Lane.* capture · `ShaderLab` · runner-up: manim: four texels blended into one read

*Capture to record.* C39-filter: scene spec evidence/planning-checks/scenes/C39-filter.json, 13.9 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, texture filter as the note says. A 12x look at the rim, both sides on the default linear filter and blurred; as the voice says 'nearest made none' the left side switches to nearest: crisp one-pixel steps, while the right stays a blurred line. Verified: half-transparent pixels 0 with nearest, 2,008 with linear (86 distinct alpha values at 2.25x); a node with no filter set behaves exactly like linear (analyze_filter E1); in the capture the left panel's blurred pixels go from 10,342 to 0 at the switch, the right stays at 10,342 (analyze_scenes C39)

### B40 · 39 words · ~13 s

> One more thing a shader can ignore: modulate, the node's own tint and fade. Fade a sprite whose shader assigns color from the texture, and nothing fades. Pass the vertex color on through a varying, and multiply it in.

*Picture.* Code card at left: the 13-line modulate-safe shader (the varying tint, the one-line vertex function, and the final multiply by tint marked). At right two real sprites whose node modulate fades to half: the left one (its shader assigns color from the texture) stays fully solid with its line, the right one (vertex color kept) fades, line included. Readouts 'fade ignored' and 'fade works'.

*Motion.* Both sprites are asked to fade; the left one does not, the right one does.

*Lane.* capture · `ShaderLab` · runner-up: manim: a tint arrow skipping the shader

*Capture to record.* C40-modulate: scene spec evidence/planning-checks/scenes/C40-modulate.json, 13.3 s clip (stretched to the measured audio), 30 fps, 1280x720 canvas rendered at 3840x2160, Forward+, nearest filter. Two sprites with the node's modulate faded to alpha 0.5: the left shader assigns COLOR from the texture and ignores the fade, the right passes the vertex COLOR on as a varying and fades with its line. Verified: with modulate alpha 0.5: no shader draws alpha 0.50; a shader assigning COLOR from the texture draws 1.00 (sprite) and 1.00 (line); the varying version draws 0.50 and 0.50 (verify_m M1)

### B41 · 42 words · ~14 s

> So four checks for any outline shader, yours or an AI's. Is there padding at least as thick as the line? Does the step count image pixels? How many reads per pixel? Is the filter nearest, and does modulate still fade it?

*Picture.* A four-row table, one row ringed as each check is asked.

*Motion.* The ring moves down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

## Closing

### BVDT · recap · 68 words · ~23 s

> Let's recap with Claude. An outline is a question each pixel asks its neighbors. Steps count image pixels, from texture pixel size. A loop reads the neighbors, and the cost follows the reads. A shader paints only inside its rectangle, so pad the image. Thick lines bend the brush; thin parts and soft edges break it. Check padding, step size, reads, filter and modulate, yours or an AI's.

*Picture.* The recap card: An outline is a question each pixel asks its neighbors. / Steps count image pixels, from texture pixel size. / A loop reads the neighbors, and the cost follows the reads. / A shader paints only inside its rectangle, so pad the image. / Thick lines bend the brush; thin parts and soft edges break it. / Check padding, step size, reads, filter and modulate, yours or an AI's.

### BHTF · your turn · 95 words · ~32 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader that outlines a sprite. Give it a color uniform called line color, and an instance uniform called thickness, a float in image pixels from zero to four. Read the neighbors in a three by three loop. Thickness zero must change nothing. Then tell me how much empty border the image needs. Now check two things yourself. At thickness two, is the line exactly two image pixels wide on every side? And at thickness zero, does the sprite look identical to having no shader?

*Prompt shown and read in full:* Write a Godot canvas item shader that outlines a sprite. Give it a color uniform called line color, and an instance uniform called thickness, a float in image pixels from zero to four. Read the neighbors in a three by three loop. Thickness zero must change nothing. Then tell me how much empty border the image needs.

*Two checks:* Check: at thickness two the line is exactly two image pixels wide on every side. · Check: at thickness zero the sprite looks identical to having no shader.

### BOUT · outro · 5 words · ~4 s

> Outlines. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


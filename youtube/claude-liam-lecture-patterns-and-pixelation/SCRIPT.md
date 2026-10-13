# Script: Patterns and Pixelation

**What this is.** The words Liam will say in *Patterns and Pixelation*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 49 beats, 1779 words, about **10:09** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 22, manim 18, remotion 3.

**If it runs long.** Cut, in this order: the scale beat (B24), the worked example (B16) and the diagonal-step beat (B28), then merge the moving stripes (B33) into the stripes beat (B32). Each repeats an idea another beat already carries. The drift pair (B13, B14), the rounding pair (B17, B18), the wide-shape trap (B39, B40) and the dot screen with its edge check (B41, B42) stay: they are the proof and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Which Cell, and Where in It | 9 | 302 | ~1:43 |
| II | Pixelate Without the Drift | 10 | 337 | ~1:55 |
| III | Blocks of Any Size | 6 | 209 | ~1:11 |
| IV | Checkerboards and Stripes | 9 | 300 | ~1:42 |
| V | Dots, and Both Numbers at Once | 9 | 299 | ~1:42 |

## Opening

### BOPEN · identity card · 28 words · ~10 s

> Patterns and Pixelation. Learn the two small functions that cut a shape into cells, and use them to pixelate an image and to draw checkerboards, stripes and dots.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Patterns and Pixelation", and the line "How cells make blocks, checkers, stripes and dots".

### BIDEA · the question · 42 words · ~14 s

> Hallo. This is Liam, in for Bear. Most people think a checkerboard, a stripe or a grid of dots needs a pattern image. It does not. A pattern is math on the address, and the graphics card runs it for every pixel.

*Picture.* The hesitant writer types: "Patterns need a pattern image." then deletes "a pattern image" and types "math on the address".

### BDEFS · terms · 70 words · ~24 s

> Six terms. A shader is a small program the graphics card runs to decide how something is drawn. U V is a point's address on the shape: zero to one across, zero to one down. A texture is an image a shader can read. A uniform is a value your game sets from outside. A cell is one square of a grid. A remainder is what is left after dividing.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Texture** — an image a shader can read by address; **Uniform** — a value your game sets from outside; every pixel sees the same one; **Cell** — one square of a grid; **Remainder** — what is left after dividing

## Act I: Which Cell, and Where in It

### B01 · 32 words · ~11 s

> Chunky pixel blocks. A checkerboard. Moving stripes. A grid of dots. Four effects, and none of them needs a pattern image. All four come from one trick: cut the address into cells.

*Picture.* Act title 'Which Cell, and Where in It' (serif 40) top-left. A real Godot render in a framed window on the cream stage: one square split in four panels, all drawn by one shader: top left the teal test sprite going from smooth to chunky blocks, top right a teal-and-cream checkerboard scrolling, bottom left gold-and-cream diagonal stripes sliding, bottom right a grid of teal dots that swell and shrink. One-word labels land beside each panel as the voice names it.

*Motion.* All four panels are alive at once: blocks coarsen, the checkerboard scrolls, the stripes slide, the dots pulse.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of four small pattern icons

*Capture to record.* C01: Lab sprite scene (teal test sprite, scale to fit), lab-shaders/01-showcase.gdshader with the uniform phase swept linearly 0 to 1 over 12 s (--animate phase:0:1), 30 fps, Forward+, nearest filter, no input. At 50 %: all four panels visible, pixelation mid-way. At 85 %: blocks coarse, dots mid-swell.

### B02 · 37 words · ~13 s

> Start with the address. Across a shape it runs from zero to one. Multiply it by four and the address is stretched: it runs from zero to four. Each whole number it passes starts a new cell.

*Picture.* The series ramp strip across the stage (a bar of light-to-mid greys, never near-black), end labels 0 and 1, caption 'UV.x' above it. It stretches: the right end label counts 1, 2, 3, 4 and the caption becomes 'UV.x × 4'; vertical tick lines grow at 1, 2 and 3, cutting the bar into four spans, and the whole numbers 0, 1, 2, 3 appear under the left end of each span. Midpoint still (45 to 55 %): the strip is stretched and labelled 0 to 4, caption 'UV.x × 4'; the ticks have not appeared yet.

*Motion.* The right label counts up to 4 while the ticks grow at each whole number.

*Lane.* manim · `B02_StretchTheAddress` · runner-up: ShaderLab: a Lab gradient render

### B03 · 36 words · ~12 s

> Floor tells you which cell you are in. Floor rounds down: zero point seven becomes zero, two point nine becomes two. So floor of the stretched address is the cell number: zero, one, two or three.

*Picture.* The same ramp, now 0 to 4 with ticks at 1, 2, 3 (cast continues). A terracotta dot rides it with a live value above it; at the right a large readout 'floor = 0' (monospace) steps up only when the dot crosses a tick. The dot pauses at 0.7 (readout shows 0.7 and 0), runs on, pauses at 2.9 (readout shows 2.9 and 2). The span under the dot is underlined by a terracotta bar. Label under the bar: 'floor: rounds down'. Midpoint still (45 to 55 %): the dot is settled at 2.9 with the readout 'floor = 2' (it runs there between 36 and 44 %); the label 'floor: rounds down' is on screen.

*Motion.* The dot slides and the floor readout changes only at the ticks: 0, 1, 2, 3.

*Lane.* manim · `B03_FloorSteps` · runner-up: plot of the staircase floor(x)

### B04 · 29 words · ~10 s

> Fract keeps what floor throws away: the part after the point. Two point nine leaves point nine. Inside every cell it climbs from zero to one, then starts over.

*Picture.* Axes on the cream stage: x from 0 to 4 along the bottom with ticks at the whole numbers, y from 0 to 1. A terracotta dot travels along x and draws the sawtooth of fract(x) behind it: a ramp from 0 to 1 that drops back to 0 at each whole number. At x = 2.9 the dot pauses at height 0.9 with the label 'fract(2.9) = 0.9'. The formula 'fract(x) = x − floor(x)' sits above the plot. Midpoint still (45 to 55 %): the dot is paused at 2.9, height 0.9, with the label 'fract(2.9) = 0.9'; the curve is drawn as far as 2.9.

*Motion.* The curve draws itself, climbing from 0 to 1 and snapping back to 0 at every whole number.

*Lane.* manim · `B04_FractSawtooth` · runner-up: ramp strip with a second strip below

### B05 · 31 words · ~10 s

> Together they pin down a spot exactly. Floor says which cell: column two, row one. Fract says where inside it: three tenths across, seven tenths down. That is the whole idea.

*Picture.* A square 4 by 4 grid of outline cells at left (no fill behind text), column numbers 0 to 3 along the top, row numbers 0 to 3 down the left side. A terracotta dot travels to the point 2.3 across and 1.7 down. Cell (2, 1) gets a heavy outline. At right, that one cell is magnified as a unit square with the dot inside it. Labels: 'cell (2, 1)' beside the grid and 'inside (0.3, 0.7)' beside the magnified cell. Midpoint still (45 to 55 %): the dot sits at (2.3, 1.7), cell (2, 1) has its heavy outline and the label 'cell (2, 1)'; the magnified cell has not opened yet.

*Motion.* The dot lands, its cell lights up, and the cell opens out to show where inside it the dot sits.

*Lane.* manim · `B05_WhichAndWhere` · runner-up: ShaderLab with a Lab render

### B06 · 41 words · ~14 s

> Here is floor, drawn by a shader for two-D, which Godot calls canvas item. The address is a pair of numbers, so floor works on both. Red follows the column, green follows the row, and every cell is one flat color.

*Picture.* Code card at left (the stretched address, floor, the color line); at right a real Godot window: a square of sixteen flat-colored cells, red growing with the column and green with the row. The highlighted lines carry short labels: canvas_item, vec2, COLOR.

*Motion.* The floor line is highlighted, then the color line, while sixteen flat cells sit in the window.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: Lab sprite, white 128 px texture (--sprite-tex white), lab-shaders/02-cells-floor.gdshader, still PNG. Verified: 16 distinct colors; cell (0,0) = 0.25, 0.25, 0.55; cell (3,3) = 1.0, 1.0, 0.55; every pixel matches the formula (verify-patterns.py).

### B07 · 29 words · ~10 s

> Now fract. Every cell holds its own copy of the same gradient. Red grows left to right, green grows top to bottom, and both start over at every border.

*Picture.* Code card at left; at right a real Godot window: the square of four by four cells again, but every cell holds the same small gradient (red growing left to right, green top to bottom), restarting at each border.

*Motion.* The fract line, then the color line, are highlighted while sixteen identical gradients fill the window.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of sixteen gradients

*Capture to record.* C03: Lab sprite, white texture, lab-shaders/03-cells-fract.gdshader, still PNG. Verified: all sixteen 90 px tiles of the 360x360 render are pixel-identical; the render matches the formula at every pixel.

### B08 · 26 words · ~9 s

> Read a picture with fract as the address, and the picture repeats in every cell. Here: three across, three down. A tiled floor, from two lines.

*Picture.* Code card at left; at right a real Godot window: the teal test sprite repeated three times across and three down inside its square, the stage showing through its transparent padding.

*Motion.* Nine copies of the sprite sit in a three by three grid; the fract line is highlighted, then the texture line.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of nine copies

*Capture to record.* C04: Lab sprite (sprite texture), lab-shaders/04-tile.gdshader, still PNG. Verified: nine copies; tiles differ from the first by at most 21 of 9,216 pixels (edge pixels).

### B09 · 41 words · ~14 s

> Here is the map for the rest of the film. Floor gives one value per cell: that is pixelation and checkerboards. Fract gives a shape that repeats: that is stripes and dots. Use both, and you get a screen of dots.

*Picture.* A map diagram. At left a ramp strip splits (two drawn arrow shapes) into two panels. Panel one, title 'floor', text 'one per cell', with two small drawn icons: pixel blocks and a checkerboard. Panel two, title 'fract', text 'repeats', with two small drawn icons: diagonal stripes and a dot grid. Below, both panels send an arrow to one last icon, a dot screen, labelled 'both'. Midpoint still (45 to 55 %): the strip has split into the two panels and the floor panel is full (block and checker icons); the fract panel is still empty.

*Motion.* The strip splits, each panel fills with its icons in turn, and the two arrows merge on the dot screen.

*Lane.* manim · `B09_WhatComesNext` · runner-up: FormBCard with library icons

## Act II: Pixelate Without the Drift

### B10 · 31 words · ~10 s

> To pixelate is to show a picture as big blocks. Inside a block, every pixel has the same color. So how does a shader pick one color for a whole block?

*Picture.* Act title 'Pixelate Without the Drift' (serif 40) top-left. A real Godot render: the teal test sprite, smooth at first, then coarser in five steps until it is a chunky grid of blocks. Caption: 'pixelate: show a picture as big blocks'.

*Motion.* The sprite loses detail in steps, each step a coarser grid of flat blocks.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of blocks

*Capture to record.* C05: Lab sprite (teal sprite, fit scale), lab-shaders/06-pixelate-center.gdshader; blocks stepped 128, 64, 32, 16, 8, each held 1.6 s (8 s), 30 fps, Forward+, nearest filter. Verified still renders at all five values (06-center-n128 to n8-sprite-fit).

### B11 · 31 words · ~10 s

> Make every pixel in a cell look up the picture at the same spot. One cell, one spot, one color. That is all pixelating is. The only question is which spot.

*Picture.* A cell drawn as a four by four grid of pixel dots above a horizontal strip that stands for the picture (a teal-to-cream gradient bar). Sixteen thin curved lines run from the pixel dots down to ONE terracotta lookup point on the strip, with the words 'which spot?' beside it. Then the cell's pixels all take the one color found there. Label: 'one cell, one spot'. Midpoint still (45 to 55 %): all sixteen lines have converged on the one lookup point; the cell has not taken its color yet.

*Motion.* All sixteen lines converge on a single point and the cell takes one color.

*Lane.* manim · `B11_OneLookupPerCell` · runner-up: ShaderLab render of a pixelated sprite

### B12 · 38 words · ~13 s

> First guess: the corner where the cell starts. Floor the stretched address, divide by the same number, and every address snaps to its cell's top left corner. All the pixels in a cell now read the same spot.

*Picture.* Code card at left (uniform blocks, the snapped address, the texture lookup); at right a real Godot window: the sprite pixelated into sixteen by sixteen blocks.

*Motion.* The floor-and-divide line is highlighted, then the texture line, with the blocky sprite in the window.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C06: Lab sprite (fit scale), lab-shaders/05-pixelate-corner.gdshader, blocks = 16, still PNG. Verified: 16 blocks of 8 picture pixels each way.

### B13 · 34 words · ~12 s

> Which way will the picture slide? Watch the sprite when the shader switches on. It jumps down and to the right, by about three and a half picture pixels. That is half a block.

*Picture.* Code card at left; at right a real Godot window: the plain teal sprite sits still for a few seconds with a terracotta ring (grey backing) on its silhouette, then the shader switches on and the sprite jumps down and to the right out of the ring. Readouts '3.5 px right' and '3.5 px down' land beside it.

*Motion.* The sprite is still, then jumps down and to the right the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim animation of an arrow shifting a sprite

*Capture to record.* C07: Lab sprite (fit scale), lab-shaders/05-pixelate-corner.gdshader, blocks = 16, no material until the voice says "It jumps" (about 36 % of the beat) then the shader is assigned (--material-at, set from the audio), about 12 s, 30 fps, Forward+, nearest filter. Verified (verify-patterns.py): the sprite's centre moves +3.5, +3.5 picture pixels at 8-pixel blocks (+7.5 at 16-pixel blocks, +1.5 at 4-pixel blocks): half a block, less the half-pixel of the measurement. At 50 %: shader on. At 85 %: shader on.

### B14 · 30 words · ~10 s

> Why? A block shows what sits at its own top left corner. So the picture arrives late: on average half a block further right, and half a block further down.

*Picture.* One dimension, drawn large. A straight diagonal line (the picture, a ramp) over eight cells marked on the axis. A terracotta dot sits on the line at the left edge of each cell with a short drop line down to a flat tread: together the treads form a staircase under the line. A double-headed arrow shape between the line and the middle of a tread is labelled 'half a block'. Labels: 'the picture', 'what the blocks show'. Midpoint still (45 to 55 %): the line, the staircase and the double arrow 'half a block' are all settled; the two labels arrive after the midpoint.

*Motion.* The lookup dots drop one by one, the staircase builds under the line, and the half-block gap is marked.

*Lane.* manim · `B14_WhyItDrifts` · runner-up: ShaderLab with an overlay

### B15 · 36 words · ~12 s

> The fix: look up the middle of the cell. Add one half to the cell number before you divide back. Now a block shows what sits at its center, and the picture stays where it was.

*Picture.* Code card at left (the snapped address now with + 0.5 added to the floor before the divide); at right the same scene: the plain sprite with its ring, then the shader switches on and the sprite turns blocky but stays inside the ring. Readout 'stays put'.

*Motion.* The sprite turns blocky at the switch but does not move: it stays inside its ring.

*Lane.* capture · `ShaderLab` · runner-up: manim animation of a sprite staying put

*Capture to record.* C08: Lab sprite (fit scale), lab-shaders/06-pixelate-center.gdshader, blocks = 16, material assigned at the voice's 'Add one half' (about 25 % of the beat, --material-at, set from the audio), about 11 s, 30 fps, Forward+, nearest filter. Verified: the sprite's centre moves -0.5, -0.5 picture pixels (less than one pixel). At 50 %: shader on. At 85 %: shader on.

### B16 · 39 words · ~13 s

> Walk one pixel through it. Address point six, four blocks. Times four is two point four. Floor gives two. Add a half: two and a half. Divide by four: point six two five, the middle of the third cell.

*Picture.* A number line from 0 to 1 cut into four cells (ticks at 0.25, 0.5, 0.75). A terracotta marker sits at the address 0.6. Beside it an arithmetic stack types in line by line (monospace): '0.6 × 4 = 2.4', 'floor gives 2' (a word, never an arrow glyph), '+ 0.5 = 2.5', '÷ 4 = 0.625'. The third cell (0.5 to 0.75) gets a heavy outline and a terracotta lookup dot lands at its middle, 0.625. Midpoint still (45 to 55 %): the stack shows '0.6 × 4 = 2.4' and 'floor gives 2'; the marker is at 0.6; the '+ 0.5' line has not typed yet.

*Motion.* The marker's number is carried through the four steps and the lookup dot lands exactly in the middle of its cell.

*Lane.* manim · `B16_WorkedExample` · runner-up: LectureCodeTrace with annotations

### B17 · 37 words · ~13 s

> Here is a tempting variant: put the half inside the floor instead. That rounds to the nearest grid line. The picture no longer drifts, so it looks fixed. But there is a second problem, at the edges.

*Picture.* Code card at left (the half is now inside the floor); at right a real Godot window: the sprite pixelated, centered where the original was, with the terracotta ring (grey backing) around the original silhouette.

*Motion.* The plus-half is highlighted inside the floor while the sprite sits inside its ring: no drift.

*Lane.* capture · `ShaderLab` · runner-up: manim code trace without the render

*Capture to record.* C09: Lab sprite (fit scale), lab-shaders/07-pixelate-round.gdshader, blocks = 16, still PNG. Verified: the sprite's centre -0.5, -0.5 px (no drift); the edge problem is not visible on the sprite (transparent padding) and is shown in B18 from the gradient run.

### B18 · 34 words · ~12 s

> Look at the edges. The grid is shifted half a block against the picture, so the first and last blocks are only half as wide. Measured: four pixels at each edge, eight everywhere else.

*Picture.* Two rows of blocks across a bracket labelled 'picture, 128 px' (the pixel-grid cast; outline cells with padding, no fill behind text). Top row, 'middle of the cell': sixteen equal blocks, each labelled 8 px at the first one. Bottom row, 'nearest grid line': the same grid shifted half a block, so seventeen blocks: the first and last are half width and wear terracotta rings with the label '4 px'; a middle block is labelled '8 px'. A small grey credit: 'Godot 4.7.2 · Forward+ · 16 blocks'. Midpoint still (45 to 55 %): both rows are settled: sixteen equal blocks above, seventeen blocks below with half-width ends; the rings arrive after the midpoint.

*Motion.* The grid slides half a block and the first and last blocks are cut to half width inside their rings.

*Lane.* manim · `B18_HalfSizeEdges` · runner-up: ShaderLab on a gradient render

### B19 · 27 words · ~9 s

> So only one of the three is right. The corner drifts. The nearest grid line gives half-size edge blocks. The middle has neither problem. Use the middle.

*Picture.* A three-row table, the row for each lookup ringed as the voice names it; the last row (the middle) ends ringed in terracotta.

*Motion.* The ring steps down the three rows with the voice and settles on the last.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim table drawn on cue

## Act III: Blocks of Any Size

### B20 · 37 words · ~13 s

> So far you typed how many blocks to draw. But you think in how big a block is: eight pixels of the picture, say. For that, the shader has to know how many pixels the picture has.

*Picture.* Act title 'Blocks of Any Size' (serif 40) top-left. A pixel grid of 16 by 8 outline cells for the picture (the series pixel-grid cast). An eight-by-eight group of the pixels is outlined heavily and labelled 'a block: 8 pixels across'. Beside the grid a terracotta question mark with the words 'how many pixels does the picture have?'. Midpoint still (45 to 55 %): the pixel grid with the eight-pixel block outlined and labelled 'a block: 8 pixels across'; the question has not landed yet.

*Motion.* The heavy outline grows over eight pixels of the grid and the question lands beside it.

*Lane.* manim · `B20_BlockInPixels` · runner-up: LectureCodeTrace

### B21 · 41 words · ~14 s

> It can ask, if what you are drawing has a texture. Texture pixel size is the size of one picture pixel, in address units. One divided by it is the picture's size in pixels: a hundred and twenty-eight, for this sprite.

*Picture.* The real Godot 4.7 canvas item shader page, Fragment built-ins table, in a browser window; the camera pushes in on the TEXTURE_PIXEL_SIZE row ('Normalized pixel size of the default 2D texture ... 64×32 pixels ... vec2(1.0 / 64.0, 1.0 / 32.0)') and a terracotta ring marks it.

*Motion.* The camera pushes in on the row the voice is describing.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: a sprite with its pixel size marked

### B22 · 36 words · ~12 s

> Multiply texture pixel size by a block size, and you get one cell in address units. Divide, floor, add a half, multiply back: the same recipe, now counted in picture pixels. Eight means eight pixels across.

*Picture.* Code card at left (an int uniform block with a range, the cell in address units, the snapped address with the half); at right a real Godot window: the sprite pixelated with blocks of eight picture pixels.

*Motion.* The cell line is highlighted, then the snap line, with the blocky sprite in the window.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C10: Lab sprite (fit scale), lab-shaders/08-pixelate-block.gdshader, block = 8, still PNG. Verified: identical to blocks = 16 of the middle-lookup version (0 of 230,400 pixels differ on the gradient at scale 1.0); the uniform is an int with hint_range(1, 32).

### B23 · 29 words · ~10 s

> Make the block size a uniform, and your game can animate it. One is the original picture. Thirty-two is chunky. A pixelating transition is this one number, counting up.

*Picture.* Code card at left with the uniform line highlighted; at right a real Godot window: the sprite from the original picture (block 1) to six steps of growing blocks up to 32. A readout shows the current block size.

*Motion.* The picture coarsens in six steps as the block size doubles.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab: one still per block size

*Capture to record.* C11: Lab sprite (fit scale), lab-shaders/08-pixelate-block.gdshader; block stepped 1, 2, 4, 8, 16, 32, each held 1.2 s (7.2 s), 30 fps, Forward+, nearest filter, scripted. Verified: block 1 is pixel-identical to the untouched sprite; stills at all six values exist.

### B24 · 30 words · ~10 s

> Blocks are counted in picture pixels, so they scale with the sprite. Draw it bigger and the blocks grow too: still sixteen across. This pixelates the picture, not the screen.

*Picture.* A real Godot window: the pixelated sprite (block 8) grows from its own size to more than twice as large; the blocks grow with it and there are always sixteen across. One readout, '16 across', stays on screen the whole time.

*Motion.* The sprite swells and its blocks swell with it, but the count stays sixteen.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of growing blocks

*Capture to record.* C12: custom scene (script): Sprite2D with lab-shaders/08-pixelate-block.gdshader, block = 8; the node's scale tweens 1.0 to 2.25 over 5 s, 30 fps, Forward+, nearest filter, scripted. Verified: blocks are 8 screen pixels at scale 1.0 and 18 at 2.25 (runs of 54, 180, 54 pixels along the middle row).

### B25 · 36 words · ~12 s

> One catch. If the block size does not divide the picture, the last block comes up short. Blocks of six on a picture a hundred and twenty-eight wide: twenty-one whole blocks, then one of two pixels.

*Picture.* A horizontal strip 128 pixels wide drawn as outline cells grouped in blocks of six (the series pixel grid, shown as a row). Twenty-one full blocks fill the strip from the left; at the right end a narrow block of two pixels, wearing a terracotta ring and the label '2 px'. A running sum under the strip: '21 × 6 + 2 = 128'. Midpoint still (45 to 55 %): the 128-pixel strip with its first block of six outlined and labelled 'block = 6'; the remaining blocks fill in after the midpoint.

*Motion.* The blocks fill the strip and the last one lands short inside its ring.

*Lane.* manim · `B25_ShortLastBlock` · runner-up: ShaderLab on the gradient render

## Act IV: Checkerboards and Stripes

### B26 · 35 words · ~12 s

> A checkerboard alternates. So give each cell two numbers, column and row, and add them. One cell to the right, the sum goes up by one. One cell down, it goes up by one again.

*Picture.* Act title 'Checkerboards and Stripes' (serif 40) top-left. A four by four grid of outline cells (no fill behind text) with the sum of column and row written in each cell: 0 1 2 3 / 1 2 3 4 / 2 3 4 5 / 3 4 5 6; column numbers along the top, row numbers down the left. A terracotta dot steps one cell right (the number pops from 2 to 3 with '+1') then one cell down (+1 again). Midpoint still (45 to 55 %): the dot has stepped one cell to the right and the number shows '+1'; the step down comes after the midpoint.

*Motion.* The dot steps right and down and the number in its cell goes up by one each time.

*Lane.* manim · `B26_SumsGrid` · runner-up: ShaderLab render of the finished checkerboard

### B27 · 34 words · ~12 s

> Take the remainder after dividing by two. An even sum leaves zero, an odd sum leaves one: exactly the number that picks between two colors. Mod gives the remainder. Three mod two is one.

*Picture.* The same grid of sums. Under each sum a small remainder after two appears, 0 or 1. Beside the grid a second, text-free four by four checkerboard fills cell by cell in teal and cream as each remainder is found (teal for 0, cream for 1). The label 'mod(x, y): the remainder after dividing' and the line '3 mod 2 = 1' sit below. Midpoint still (45 to 55 %): the remainders are under the sums and the plain checkerboard beside the grid is complete; the line '3 mod 2 = 1' has not typed yet.

*Motion.* Each sum gets its remainder and the second grid fills with the checkerboard cell by cell.

*Lane.* manim · `B27_RemainderColors` · runner-up: LectureEvidenceTable

### B28 · 40 words · ~14 s

> Move diagonally and the sum goes up by two. The color flips on every rise of one, so two flips bring you back to the same color. That is why a square touches its own color only at the corners.

*Picture.* The same grid, now showing the checkerboard colors as outlines (teal and cream rings, no fill behind numbers). A terracotta dot jumps from cell (0, 0) to cell (1, 1) with the label '+2' on the jump; two flip marks (one per step of one) appear on the way, the two cells carry the same color and a small bracket joins them. A corner point where four cells meet is marked with a small terracotta dot and the label 'corners touch'. Midpoint still (45 to 55 %): the dot sits on cell (1, 1) with the '+2' label, two flip marks on the way and the bracket joining the pair; the corner mark arrives after the midpoint.

*Motion.* The dot jumps diagonally and lands on a cell of its own color; the bracket joins the pair.

*Lane.* manim · `B28_DiagonalStep` · runner-up: ShaderLab render of the finished checkerboard

### B29 · 29 words · ~10 s

> In the shader: floor gives column and row, add them, take mod two, and let that mix two colors. Use mod, not percent: a shader refuses percent on decimals.

*Picture.* Code card at left (cell, parity with mod, two colors, the mix); at right a real Godot window: an eight by eight teal-and-cream checkerboard. The mod and COLOR lines carry short labels: mod(x, y): the remainder of x divided by y; mix(a, b, t): zero gives a, one gives b.

*Motion.* The cell line, the mod line and the mix line are highlighted in turn while the checkerboard sits in the window.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C13: Lab sprite, white texture, lab-shaders/09-checker.gdshader, still PNG. Verified: all 64 cells match mod(column + row, 2); top-left cell teal; probes (0,0) teal, (1,0) cream, (0,1) cream, (1,1) teal. Lab: percent on decimals is a shader error (chk-percent-on-floats).

### B30 · 36 words · ~12 s

> Stripes need only one number per pixel: how far along a direction you are. Add the two address numbers and you get a diagonal ramp, from zero in one corner to two in the opposite one.

*Picture.* A square (the shape) shaded with a diagonal gradient in mid-tone greys, with five grey isolines running along the other diagonal at x + y = 0.5, 1, 1.5 ... and a ramp strip below labelled 0 and 2 with the word 'ramp'. A terracotta dot slides along the main diagonal with a live label 'UV.x + UV.y = ...' counting from 0 up to 2. Midpoint still (45 to 55 %): the dot is held at the middle of the diagonal with the label 'UV.x + UV.y = 1.0' (it slides there between 36 and 44 %); the far corner comes after the midpoint.

*Motion.* The dot slides corner to corner and the sum counts from zero to two.

*Lane.* manim · `B30_DiagonalRamp` · runner-up: ShaderLab render of the finished stripes

### B31 · 32 words · ~11 s

> Multiply the ramp by a stripe count, then take fract. The ramp restarts again and again: a sawtooth. Cut each tooth with step at a width, and every tooth becomes one stripe.

*Picture.* A plot over the diagonal 0 to 2: the sawtooth of fract(ramp × 4) with eight teeth, drawing left to right. A horizontal threshold line at 0.5 labelled 'width'. Under the plot a one-dimensional bar fills in gold where a tooth is below the threshold and cream above it. Then the threshold moves to 0.25 and back to 0.75 and the gold parts thin and thicken. The label 'step(edge, x): 0 below the edge, 1 from the edge' sits above, and the word 'sawtooth' labels the curve. Midpoint still (45 to 55 %): the full sawtooth of eight teeth is drawn and labelled 'sawtooth'; the threshold line and the stripe bar arrive after the midpoint.

*Motion.* The sawtooth draws, the threshold cuts every tooth, and the stripe bar below fills; moving the threshold changes the stripe widths.

*Lane.* manim · `B31_SawtoothCut` · runner-up: LectureCodeTrace

### B32 · 30 words · ~10 s

> Run it, and there are the stripes. Count is how many pairs fit across the shape. Width is how much of each pair is gold: at one half, equal shares.

*Picture.* Code card at left (count and width uniforms, the diagonal, fract, step, the mix of gold and cream); at right a real Godot window: gold-and-cream diagonal stripes, four pairs across. Two readouts 'count 4' and 'width 0.5'.

*Motion.* The fract line, then the step line, are highlighted while four gold stripes run across the square.

*Lane.* capture · `ShaderLab` · runner-up: manim strip of stripes

*Capture to record.* C14: Lab sprite, white texture, lab-shaders/10-stripes.gdshader, count 4, width 0.5, still PNG. Verified: four gold stripes end along the top row; gold share 0.500 (0.253 at width 0.25, 0.753 at 0.75); edges follow lines of constant x + y.

### B33 · 36 words · ~12 s

> To make them move, subtract time times a speed inside the fract. Time is one clock for the whole game. The pattern slides toward the bottom right, and fract still works when the number goes negative.

*Picture.* Code card at left with the TIME line highlighted; at right a real Godot window: the same gold-and-cream stripes sliding toward the bottom right. The highlighted line carries the label 'TIME: seconds on one clock for the game'.

*Motion.* The stripes slide steadily toward the bottom right the whole time.

*Lane.* capture · `ShaderLab` · runner-up: manim animation of sliding stripes

*Capture to record.* C15: Lab sprite, white texture, lab-shaders/11-stripes-moving.gdshader, defaults, 8 s live TIME, 30 fps, Forward+, nearest filter. Verified: the render equals the formula for the engine's TIME (0.00 % pixels differ in three of four renders; one fit less well, 1.1 %, kept), and the pattern moves toward larger x + y as TIME grows. fract(-0.25) = 0.75 (chk-negative-fract-mod).

### B34 · 28 words · ~10 s

> Same recipe both times. Make one number per pixel: column plus row, or the diagonal. Make it repeat, with mod or with fract. Cut it into two colors.

*Picture.* A three-row table with a row per step and a column per pattern; the row for each step is ringed as the voice names it.

*Motion.* The ring steps down the three steps with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim table drawn on cue

## Act V: Dots, and Both Numbers at Once

### B35 · 30 words · ~10 s

> Dots need to know where you are inside a cell, and fract says that, from zero to one. Subtract one half, and zero sits in the middle of the cell.

*Picture.* Act title 'Dots, and Both Numbers at Once' (serif 40) top-left. One cell drawn large as a unit square. Its corner labels read 0 and 1; they change to -0.5 and +0.5 with a small terracotta origin mark appearing in the middle as the voice says subtract one half. A terracotta dot moves around inside with a live label giving its two numbers. Midpoint still (45 to 55 %): the dot is held inside the cell with its two numbers (0.3, 0.7) and the corner labels still read 0 and 1; the re-centering comes after the midpoint.

*Motion.* The labels shift from 0 to 1 over to minus a half to plus a half and the origin moves to the middle of the cell.

*Lane.* manim · `B35_CellSpace` · runner-up: ShaderLab render of one dot in a cell

### B36 · 35 words · ~12 s

> Length of that pair is the distance from the middle of the cell. Compare it with a radius. Step gives zero inside the circle and one outside, and that picks between dot color and background.

*Picture.* The same cell, centered. A terracotta dot with a line to the middle labelled 'length'. A grey circle of radius r around the middle. As the dot moves across the circle's edge the label flips between 'inside: step gives 0' and 'outside: step gives 1'. The label 'length: the distance from the middle' is drawn above. Midpoint still (45 to 55 %): the dot, its line to the middle and the circle of radius r are all settled with the label 'length'; the dot crosses the edge after the midpoint.

*Motion.* The dot crosses the circle's edge and the label flips from step gives 0 to step gives 1.

*Lane.* manim · `B36_LengthAndRadius` · runner-up: ShaderLab render of the dot grid

### B37 · 31 words · ~10 s

> In code: fract of the stretched address, minus a half. Length of that. Step against the radius, and mix the two colors. Eight cells across, eight down, one dot in each.

*Picture.* Code card at left (cells and radius uniforms, fract minus a half, length, the step-and-mix line); at right a real Godot window: an eight by eight grid of teal dots on cream.

*Motion.* The fract line, the length line and the color line are highlighted in turn while the dot grid sits in the window.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C16: Lab sprite, white texture, lab-shaders/12-dots.gdshader, cells 8, radius 0.35, still PNG. Verified: dots cover 38.4 % of the picture (geometry: 38.5 %).

### B38 · 32 words · ~11 s

> Grow the radius and the dots swell. At one half they touch their neighbors. By seven tenths they fill the whole cell, because a cell's corner is that far from its middle.

*Picture.* Code card at left with the radius uniform highlighted; at right a real Godot window: the dot grid with the radius sweeping from small to large, the dots swelling until they touch and finally fill their cells. Readouts: 'touch: 0.5' and 'full: 0.71'.

*Motion.* The dots swell, touch, and then fill the whole picture.

*Lane.* capture · `ShaderLab` · runner-up: manim plot of covered area

*Capture to record.* C17: Lab sprite, white texture, lab-shaders/12-dots.gdshader, cells 8; radius swept linearly 0.05 to 0.75 over 8 s (--animate radius:0.05:0.75), 30 fps, Forward+, nearest filter, scripted. Verified: coverage 12.4 / 38.4 / 78.9 / 95.1 / 100 / 100 % at radius 0.2 / 0.35 / 0.5 / 0.6 / 0.7 / 0.72 (geometry: 12.6 / 38.5 / 78.5 / 95.1 / 100 / 100); half the diagonal is 0.7071.

### B39 · 39 words · ~13 s

> One trap. On a wide rectangle the dots turn into ovals. The address runs zero to one across and down, whatever the shape, so cells stretch with the shape. These dots are one point eight times wider than tall.

*Picture.* Code card at left (the same dots shader, eight cells each way); at right a real Godot window: a square of round dots whose rectangle widens from square to sixteen by nine, the dots stretching into ovals. Readouts: 'round' at the start, '1.8 × wider than tall' at the end.

*Motion.* The rectangle widens and the round dots stretch sideways into ovals.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a stretched circle

*Capture to record.* C18: custom scene (script): a ColorRect with lab-shaders/12-dots.gdshader, cells = 8 (its default), height 360, width tweening 360 to 640 over 4 s, 30 fps, Forward+, scripted. Verified at the end state (640x360): each dot is 56 by 31 pixels (ratio 1.81 on whole pixels; the cells are 80 by 45, ratio 1.78); at the start (360x360) the dots are round.

### B40 · 33 words · ~11 s

> The fix: give each direction its own count, in the shape's proportions. Sixteen across and nine down for a sixteen by nine rectangle, and every cell is square again. Every dot is round.

*Picture.* Code card at left (cells is now a vec2, sixteen by nine); at right a real Godot window on the sixteen by nine rectangle: the eight-by-eight oval dots switch to a sixteen-by-nine grid of round dots. Readout '16 by 9' and 'round again'.

*Motion.* The ovals snap into round dots at the switch.

*Lane.* capture · `ShaderLab` · runner-up: manim before-and-after drawing

*Capture to record.* C19: custom scene (script): the 640x360 ColorRect of C18 with lab-shaders/12-dots.gdshader (cells 8, its default) until the voice says 'Sixteen across' (about 36 % of the beat, set from the audio), then lab-shaders/13-dots-square.gdshader (cells 16, 9) assigned; about 11 s, 30 fps, Forward+, scripted. Verified: after the switch each dot is 28 by 28 pixels, ratio 1.00 (cells 40 by 40).

### B41 · 32 words · ~11 s

> Now use both numbers at once. Floor picks the cell, and we read the picture at the cell's middle: the pixelate lookup. Fract draws the dot, and the dot takes that color.

*Picture.* Code card at left (cells and radius with ranges, the stretched address, the middle of the cell, the picture read there, the distance, the color); at right a real Godot window: the teal test sprite drawn as a screen of round dots, with its two cream eyes as two cream dots.

*Motion.* The middle-lookup line, the distance line and the color line are highlighted in turn over the dot screen.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C20: Lab sprite (fit scale), lab-shaders/14-halftone.gdshader, cells 24, radius 0.4, still PNG. Verified: on the gradient picture at 16 cells every dot, including the four corners, is the same size (6 by 6, 32 pixels) and its color equals the picture at the cell's middle in 256 of 256 cells.

### B42 · 39 words · ~13 s

> Same trap, in dots. Round the cell number and the dots sit on grid lines, so the ones along the edge are cut in half. Floor it, and the grid starts at the picture's edge: every dot is whole.

*Picture.* Code card at left: the rounded variant of the dot screen, the half added inside the floor and inside the fract (those two lines highlighted); at right a real Godot window: an eight by eight dot screen of the teal-and-cream checker picture, drawn first with the rounded variant (the dots along the four edges cut in half, the corners cut to quarters, a terracotta ring on one edge) and then, when the voice says 'Floor it', with the floored dot screen: all sixty-four dots whole. Readouts: 'cut in half', then 'whole'.

*Motion.* The edge dots are cut in half, then the shader switches and every edge dot becomes whole.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of half dots

*Capture to record.* C21: custom scene (script): Lab sprite (checker texture, fit scale), cells = 8; lab-shaders/15-halftone-rounded.gdshader until the voice says 'Floor it' (about 64 % of the beat, set from the audio), then lab-shaders/14-halftone.gdshader assigned; about 13 s, 30 fps, Forward+, nearest filter, scripted. Verified (scale 1.0, 128 px picture): the rounded version has 81 separate shapes, 32 of them cut by the picture's edge (areas 31 and 62 against 124); the floored version has 64 whole dots of 124 pixels each.

### B43 · 28 words · ~10 s

> Few cells give chunky dots. More cells bring the picture back. One shader: a lookup per cell, a dot per cell, and one number to turn between them.

*Picture.* Code card at left with the cells uniform highlighted; at right a real Godot window: the dot-screen sprite with the cell count sweeping from 8 up to 48, the dots shrinking and the sprite coming back into focus. A readout shows the count.

*Motion.* The dots shrink and multiply and the picture comes back.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab: stills at four cell counts

*Capture to record.* C22: Lab sprite (fit scale), lab-shaders/14-halftone.gdshader; cells swept linearly 8 to 48 over 8 s (--animate cells:8:48), 30 fps, Forward+, nearest filter, scripted. Verified: stills at 8, 16, 24, 48 cells exist (14-halftone-c8 to c48-sprite-fit).

## Closing

### BVDT · recap · 80 words · ~27 s

> Let's recap with Claude. Floor says which cell, and fract says where inside it. To pixelate, look up the middle of each cell, not its corner. The texture can tell you its size, so blocks can be counted in picture pixels. A checkerboard is column plus row, reduced by mod two. Stripes are fract of a diagonal ramp, cut in two with step. A dot is a distance in a cell's own space, and each direction needs its own count.

*Picture.* The recap card: Floor says which cell, and fract says where inside it. / To pixelate, look up the middle of each cell, not its corner. / The texture can tell you its size, so blocks can be counted in picture pixels. / A checkerboard is column plus row, reduced by mod two. / Stripes are fract of a diagonal ramp, cut in two with step. / A dot is a distance in a cell's own space, and each direction needs its own count.

### BHTF · your turn · 105 words · ~36 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader that shows a sprite's texture as a grid of round dots. One float uniform called cells, from four to sixty-four, sets how many dots fit along the shorter side. Each dot takes the texture's color at the middle of its cell. Keep the dots round, even on a wide texture. Then check two things yourself. With cells at eight, do you count eight round dots along the shorter side? And on a square texture, are the dots along every edge whole? Half dots on the edge mean the cells were rounded, not floored.

*Prompt shown and read in full:* Write a Godot canvas item shader that shows a sprite's texture as a grid of round dots. One float uniform called cells, from four to sixty-four, sets how many dots fit along the shorter side. Each dot takes the texture's color at the middle of its cell. Keep the dots round, even on a wide texture.

*Two checks:* Check: with cells at eight, you count eight round dots along the shorter side. · Check: on a square texture, the dots along every edge are whole.

### BOUT · outro · 7 words · ~4 s

> Patterns and Pixelation. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


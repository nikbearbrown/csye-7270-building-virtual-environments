# Script: Matrices and Fake 3D

**What this is.** The words Liam will say in *Matrices and Fake 3D*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 47 beats, 1785 words, about **10:11** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: manim 22, capture 15, remotion 4.

**If it runs long.** Cut, in this order: the order-swap pair (B22, B23), the corner spin (B38), the two-turns beat (B31) and the card-versus-box beat (B33): each repeats an idea another beat already carries. The columns trio (B04 to B06), the product-order beat (B21), the flip itself (B28, B29) and the door (B35, B41) stay: they are the stumbling blocks and the payoff.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | A Table That Moves Points | 10 | 341 | ~1:56 |
| II | Three Moves | 7 | 284 | ~1:37 |
| III | Moves Together | 7 | 249 | ~1:25 |
| IV | Fake 3D | 10 | 370 | ~2:06 |
| V | The Pivot | 7 | 231 | ~1:19 |

## Opening

### BOPEN · identity card · 27 words · ~9 s

> Matrices and Fake Three D. Learn what a matrix does to a point, how to combine moves, and how to flip a flat picture like a card.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Matrices and Fake 3D", and the line "A matrix is a saved move, and it can flip a card".

### BIDEA · the question · 40 words · ~14 s

> Hallo. This is Liam, in for Bear. Matrices have a reputation: advanced math, the part you skip. They are simpler than that. A matrix is a saved move, a small table of numbers that moves any point you give it.

*Picture.* The hesitant writer types: "A matrix is
advanced math you can skip." then deletes "advanced math you can skip" and types "a saved move".

### BDEFS · terms · 60 words · ~20 s

> Five terms. A vector is a bundle of numbers, here a point's position. A matrix is a grid of numbers in rows and columns. A vertex is a corner point of a shape. A uniform is a value your game sets from outside. And a radian is Godot's angle unit: a full turn is tau, about six point two eight.

*Picture.* "Terms In This Lecture": **Vector** — a bundle of two to four numbers; **Matrix** — a grid of numbers in rows and columns; **Vertex** — a corner point of a shape; **Uniform** — a value your game sets from outside; every pixel sees the same one; **Radian** — Godot's angle unit; a full turn is tau, about 6.283

## Act I: A Table That Moves Points

### B01 · 42 words · ~14 s

> Watch a flat picture turn over like a card. No three-D model, no animation file. Every corner of the shape is multiplied by a small table of numbers. Learn that table, and you can spin, shrink, slide and flip anything you draw.

*Picture.* Act title 'A Table That Moves Points' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a cream card with a teal arrow pointing right and a small teal square in its top left corner sits still, then turns over like a card: it narrows to an edge, comes back mirrored (the arrow now points left, the square sits top right), then turns back to the front. Label under the window: 'scripted sweep'.

*Motion.* The flat card turns over, narrows to nothing, comes back mirrored, and turns to the front again.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a card turning

*Capture to record.* C01: 08-flip.gdshader on a Sprite2D; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 17 s. flip keyframes (fraction of the beat, ease in-out on each move): 0.0 at 0.00 to 0.10, 0.5 at 0.38, 0.5 until 0.62, 1.0 at 0.80, 1.0 to the end. At the 50 % mark: the mirrored back, fully visible (arrow points left). At 85 %: the front. Verified: widths 128 x |cos(TAU x flip)|, mirrored at 0.5 (geometry-summary.txt).

### B02 · 38 words · ~13 s

> Take a point: five across, six down. Multiply it by a table of four numbers. Top row first: one times five plus three times six is twenty-three. Bottom row: two times five plus four times six is thirty-four.

*Picture.* Left to right on the cream stage: a bracketed two-by-two table (1 3 over 2 4) labelled 'table', a bracketed column (5 over 6) labelled 'point', an equals sign and an empty bracketed result column. A terracotta ring outlines the table's top row (labelled 'row'); the small products '1 x 5' and '3 x 6' appear beneath and add up to '23', which lands in the first result slot. The ring drops to the bottom row: '2 x 5' and '4 x 6' add up to '34'. Last, a drawn arrow runs from the point column to the result column.

*Motion.* A ring walks down the table one row at a time, and each row collapses into one number of the answer.

*Lane.* manim · `B02_RowsTimesPoint` · runner-up: Remotion card with the arithmetic typed out

### B03 · 27 words · ~9 s

> In Godot, that is one multiplication. Mat two builds the table, the star multiplies, and this shader checks its answer against twenty-three, thirty-four. Teal means they agree.

*Picture.* Code card at left with the real ten-line shader; at right a framed Godot window that is the plain stage colour at first, then turns teal when the check line is highlighted. A small readout 'teal: agrees' lands under the window.

*Motion.* Focus steps from the table line to the multiplication to the check, and then the window turns teal.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: a ColorRect filling the result window; no material for the first 60 % of the beat, then 01-table-check.gdshader assigned (harness option --material-at); 11 s; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input. At the 50 % mark: the plain stage colour (shader not yet on) with line 5 in focus. At 85 %: teal. Verified: probe (0.3686, 0.6392, 0.5686); the disagree colour is (0.85, 0.2, 0.2).

### B04 · 36 words · ~12 s

> Look at the numbers in the code: one, two, then three, four. Godot reads each vec two as a column. So one, two stands upright on the left, and the table's top row is one, three.

*Picture.* On the left a code card (Menlo, at least 32) holds the real line mat2(vec2(1.0, 2.0), vec2(3.0, 4.0)); the two vec2 groups are outlined, one solid and one dashed. On the right an empty bracketed two-by-two table. The first vec2 (1, 2) lifts out of the code and stands upright as the table's left column, labelled 'column'; the second (3, 4) becomes the right column. Then the top row is outlined and labelled 'row: 1, 3'.

*Motion.* Each vec2 lifts out of the code and stands upright as a column of the table.

*Lane.* manim · `B04_VecTwoIsAColumn` · runner-up: LectureCodeTrace alone

### B05 · 32 words · ~11 s

> The documentation says it plainly: build a matrix from vectors, and they are read as columns. Whoever wrote the shader, a person or an AI, this is the first thing to check.

*Picture.* The real Godot 4.7 shading-language page in a browser window, scrolled to the 'Constructing' section; the camera pushes in on the sentence that says matrix types are built from vectors 'interpreted as columns' and one terracotta ring marks it.

*Motion.* The camera pushes in on the sentence the voice is quoting.

*Lane.* remotion · `BrowserCapture` · runner-up: manim: a quote card

### B06 · 36 words · ~12 s

> Mix it up and nothing complains. Read the numbers as rows, and the answer is seventeen, thirty-nine. Put the point on the left of the table, and you get seventeen, thirty-nine again. Table first, point second.

*Picture.* Three stacked lines on the cream stage. Top (ink): the right reading, table x point = (23, 34). Middle (grey, with a terracotta strike line): the numbers read as ROWS, so the table becomes 1 2 over 3 4 (the 2 and the 3 swap places) and the result is (17, 39); label 'rows'. Bottom (grey, with a strike line): the point written on the LEFT of the table, (5, 6) x table, result (17, 39); the code label 'p * table' beside it. At the end the top line is ringed and a label 'table first' lands.

*Motion.* The 2 and the 3 swap places, and the answer changes to (17, 39); then the point hops to the other side of the table and gives the same wrong answer.

*Lane.* manim · `B06_TwoWrongReadings` · runner-up: LectureEvidenceTable

### B07 · 38 words · ~13 s

> Here is why columns make sense. The first column is where one step across lands. The second is where one step down lands. Five steps of the first and six of the second add up to twenty-three, thirty-four.

*Picture.* A grid in Godot's screen directions (x to the right, y DOWN; small axis labels). The unit square with an 'across' arrow (solid) and a 'down' arrow (dashed). At the top right the table 1 3 over 2 4 with its first column outlined solid and its second dashed. The grid warps: the across arrow lands at (1, 2), the down arrow at (3, 4), the square becomes a parallelogram with corners (0,0), (1,2), (4,6), (3,4); tip labels '1, 2' and '3, 4'. Then the view zooms out and a staircase of five across-steps then six down-steps walks from the origin to a terracotta dot labelled '23, 34'.

*Motion.* The square warps into a parallelogram on the two columns, then a staircase of five and six steps walks to (23, 34).

*Lane.* manim · `B07_WhereArrowsLand` · runner-up: ShaderLab

### B08 · 33 words · ~11 s

> The plainest table leaves both arrows where they started: one, zero, then zero, one. That is the identity matrix, and it moves nothing. In Godot, mat two of one gives exactly that table.

*Picture.* The warped grid of the previous picture on the same screen-direction axes, with the table 1 3 over 2 4. The four entries change to 1 0 over 0 1 and the grid relaxes back into the plain unit square while both arrows spring back onto (1, 0) and (0, 1). A label 'identity: moves nothing'. A small code card then shows mat2(1.0).

*Motion.* The warped grid relaxes back into a square as the numbers settle to one, zero, zero, one.

*Lane.* manim · `B08_IdentityMovesNothing` · runner-up: ShaderLab with the identity table

### B09 · 30 words · ~10 s

> Stretch the arrows and the table scales. Two, zero, then zero, two lands each arrow twice as far out, so every point ends up twice as far from the middle.

*Picture.* The same screen-direction grid. The table 1 0 over 0 1 becomes 2 0 over 0 2; both arrows stretch to (2, 0) and (0, 2) and the unit square grows into a square twice as wide and tall, centred on the origin's corner. A label 'scale: twice as far' defines the word.

*Motion.* Both arrows stretch to twice their length and the square grows with them.

*Lane.* manim · `B09_ScaleStretchesArrows` · runner-up: LectureEvidenceTable

### B10 · 29 words · ~10 s

> A shape is made of its corners. Multiply every corner by the same table and the whole shape follows. Four corners, one table: a move saved in four numbers.

*Picture.* The test rectangle (a wide rectangle, 3 by 2 grid units, centred on the origin of the screen-direction grid) with four terracotta corner dots; the table 2 0 over 0 2 at the side. The four dots fly outward one after another to their doubled positions and the rectangle's edges redraw between them; a faint ghost of the old rectangle stays. A label 'one table, four corners'.

*Motion.* Four dots fly outward one after another and the rectangle's edges follow them.

*Lane.* manim · `B10_ShapeIsItsCorners` · runner-up: isometric workers on a conveyor (show-tell)

## Act II: Three Moves

### B11 · 44 words · ~15 s

> Now something real. Godot calls the vertex function once per corner of a shape, and hands it the corner's position in pixels from the node's origin. On a centered sprite, that is the middle. Multiply it by the scale table, and the picture grows.

*Picture.* Act title 'Three Moves' (serif 40) top-left. Code card at left with the real eight-line shader; at right a framed Godot window with the card, a small grey cross at its origin, a readout 'origin' next to the cross, and the line 'VERTEX: a corner's position, in pixels from the node's origin' as the caption. The card grows when the scale line is highlighted.

*Motion.* Focus lands on vertex(), then on VERTEX, then on the scale table, and the card grows.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C03: 02-grow.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a small grey cross at the node's origin drawn by the scene; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 18 s. grow keyframes: 1.0 at 0.00 to 0.58, 1.5 at 0.72 (ease in-out), 1.5 to the end. At the 50 % mark: the card at its original size. At 85 %: the card grown by half. Verified at node scale 1.0: 128 px becomes 192 px at grow 1.5 (geometry-summary.txt).

### B12 · 42 words · ~14 s

> Turning is a table too. Turn by an angle, and the across arrow lands at cosine, sine. Those are how far across and how far down you get on a circle of radius one. The down arrow lands at minus sine, cosine.

*Picture.* The screen-direction grid with a grey circle of radius one. The across arrow (solid) and the down arrow (dashed) swing together clockwise from the start position to 45 degrees; the across tip is labelled 'cos, sin' with its live numbers 0.71, 0.71 and the down tip 'minus sin, cos' (-0.71, 0.71). At the right the table cos -sin over sin cos with its four live entries (0.71 -0.71 over 0.71 0.71), first column outlined solid and second dashed. A small label under the circle: 'across and down on a circle of radius one'.

*Motion.* The two arrows swing together clockwise round the circle while the table's four entries change with them.

*Lane.* manim · `B12_TurnIsATable` · runner-up: plot of cosine and sine

### B13 · 38 words · ~13 s

> Angles are in radians, so a full turn is about six point two eight, which Godot calls tau. Sweep the angle up to an eighth of tau and the picture turns clockwise, because on screen y points down.

*Picture.* Code card at left with the real nine-line shader; at right a framed Godot window with the card and its origin cross. The caption defines TAU; the card turns clockwise by an eighth of tau (45 degrees) while the readouts 'TAU: full turn', 'angle 0.79' and 'clockwise' land.

*Motion.* The card turns clockwise as the angle sweeps up to an eighth of tau.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C04: 03-turn.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a small grey cross at the node's origin drawn by the scene; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 15 s. angle keyframes: 0.0 at 0.00 to 0.58, 0.7854 at 0.72 (ease in-out), 0.7854 to the end. At the 50 % mark: the card upright. At 85 %: the card turned 45 degrees clockwise (arrow pointing down and to the right). Verified: bbox of a turned 128 px square matches the corner maths; pixel-identical to Node2D.rotation (verify1 R1).

### B14 · 38 words · ~13 s

> Sliding is different. Whatever two by two table you pick, the point at zero, zero stays at zero, zero, because zero times anything is zero. A two by two table can scale and turn, but it cannot slide.

*Picture.* The screen-direction grid with the origin pinned by a terracotta dot and a small pin drawn from lines. Three different two-by-two tables act in turn (a scale, a turn, a squash): the grid stretches, spins and squashes, but the origin dot never leaves its spot. At the end the whole grid tries to slide right (a dashed arrow) and snaps back; label '0, 0 stays 0, 0'.

*Motion.* The grid stretches, spins and squashes around a dot that never moves; a slide is attempted and snaps back.

*Lane.* manim · `B14_OriginNeverMoves` · runner-up: LectureEvidenceTable

### B15 · 44 words · ~15 s

> The fix is one extra number. Give the point a third number, always one, and use a three by three table. Put the slide in the last column: the top row now gives x plus the slide, and the bottom row keeps the one.

*Picture.* A bracketed three-by-three table (1 0 100 / 0 1 0 / 0 0 1) with its last column outlined and labelled 'slide'; beside it a bracketed column (30 / 20 / 1) with its last slot ringed, labelled 'point, plus a one'; an equals sign and a result column. The ring walks down: the top row gives 1 x 30 + 0 x 20 + 100 x 1 = 130 (the 100 pairs with the one); the middle row gives 20; the bottom row gives 0 + 0 + 1 = 1, so the result column reads (130 / 20 / 1).

*Motion.* The ring walks down the rows: the slide in the last column is multiplied by the one, and the one survives in the last slot.

*Lane.* manim · `B15_ThirdNumberIsOne` · runner-up: LectureEvidenceTable

### B16 · 37 words · ~13 s

> In the shader, put a one on the end of the corner's position, multiply, and keep the first two numbers. The slide sits in the last column, and the picture moves a hundred pixels to the right.

*Picture.* Code card at left with the real ten-line shader; at right a framed Godot window with the card and its origin cross. When the offset line is highlighted the card slides one hundred pixels to the right; a readout 'slide 100 px' lands.

*Motion.* The card slides to the right when the offset line is highlighted.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C05: 04-slide.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a small grey cross at the node's origin drawn by the scene; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 15 s. slide keyframes (x, y): (0, 0) from 0.00 to 0.58, (100, 0) at 0.74 (ease in-out, pass (100 x U, 0)), then hold. At the 50 % mark: the card at the origin. At 85 %: the card one hundred card-pixels to the right. Verified: centre moves by exactly (100, 0) (geometry-summary.txt).

### B17 · 41 words · ~14 s

> Three moves, three tables. Scale puts its numbers on the diagonal. Turn puts cosine and sine in the first two columns. Slide puts the offset in the last column. None of them bends an edge, so four moved corners are enough.

*Picture.* A four-row table: scale, turn and slide, each with where its numbers go, and a last row 'all three: keep straight edges straight'; one row is ringed as each is named.

*Motion.* The ring steps down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

## Act III: Moves Together

### B18 · 33 words · ~11 s

> A slide alone is simpler as plain addition. Tables pay off when moves combine: a scale, a turn and a slide saved as one table. Then every corner needs one multiplication, not three.

*Picture.* Act title 'Moves Together' (serif 40) top-left. Three small bracketed grids labelled 'scale', 'turn' and 'slide' drift together from the left and merge, with a drawn multiplication sign between them, into one grid labelled 'one table'. Under the one table the test rectangle's four corner dots each get one arrow from the one table; under the three small grids a ghost of the same corners shows three arrows each, crossed out.

*Motion.* Three small tables slide together and merge into one; then each corner needs one arrow instead of three.

*Lane.* manim · `B18_ManyMovesOneTable` · runner-up: DesignPipelineClaim, show-tell isometric

### B19 · 44 words · ~15 s

> To multiply tables, they must be the same size. Copy a two by two into the corner of a three by three, with zeros around it and a one in the bottom right. Godot does it for you: mat three of a mat two.

*Picture.* At the top a small grey strip of the REAL compiler message from the Lab for the line mat3(1.0) * mat2(1.0): SHADER ERROR: Invalid arguments to operator '*': 'mat3, mat2'. Below it, on the left, the quarter-turn table 0 -1 over 1 0 (two by two) and at the right an empty three-by-three frame. The two-by-two slides into its top left corner; zeros fill the rest of the grid in grey and a terracotta ring settles on the bottom right entry, which becomes 1: the table reads 0 -1 0 / 1 0 0 / 0 0 1. A small code card then shows mat3(turn).

*Motion.* The two-by-two table slides into the corner of a three-by-three, grey zeros fill in, and a one lands bottom right.

*Lane.* manim · `B19_TwoByTwoInAThreeByThree` · runner-up: LectureCodeTrace

### B20 · 34 words · ~12 s

> Multiply two tables and you get one table that does both moves. The rule is the one you know: each entry is a row of the left table times a column of the right.

*Picture.* Three bracketed three-by-three tables in a line: slide (1 0 100 / 0 1 0 / 0 0 1), a multiplication sign, quarter turn (0 -1 0 / 1 0 0 / 0 0 1), an equals sign and an empty result table. A terracotta ring outlines the slide table's top row and the turn table's last column; the arithmetic 1 x 0 + 0 x 0 + 100 x 1 = 100 appears and 100 lands in the result's top right entry. The rest of the result fills in: 0 -1 100 / 1 0 0 / 0 0 1.

*Motion.* A row and a column are ringed, their products add to 100, and the whole result table fills in.

*Lane.* manim · `B20_TablesMultiply` · runner-up: LectureEvidenceTable

### B21 · 30 words · ~10 s

> Which move happens first? The one nearest the point. Slide times turn, times point, turns first, then slides. Read it from the right, the way the point meets the tables.

*Picture.* A line: the code-style expression slide x turn x point with the first two as small bracketed boxes and the point as a terracotta dot at the far right. A token (the dot's copy) travels right to left: it passes through the turn box first, where a small card icon spins in place, then through the slide box, where it shifts right; drawn arrow shapes point left between the stages. Labels 'turn first', 'slide second'.

*Motion.* A token starting at the point passes through the turn first, then the slide, travelling right to left.

*Lane.* manim · `B21_NearestTableFirst` · runner-up: LectureCodeTrace

### B22 · 34 words · ~12 s

> Same two tables, two orders. Turn a quarter, then slide a hundred pixels right: the picture spins in place, then shifts across. Slide first, then turn: it ends a hundred pixels below the middle.

*Picture.* Result window above (two equal panels, each with its origin cross and its own card) and the two product lines below. Left panel labelled 'turn, then slide': the card spins a quarter in place, then slides right and ends at one hundred card-pixels across. Right panel labelled 'slide, then turn': the card slides right first, then swings round the origin along an arc and ends one hundred card-pixels below the cross.

*Motion.* Both cards start at the origin; the left one spins and slides right, the right one slides right and then swings down along an arc.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C06: custom scene with two panels (each 640 x 720 logical, origin cross at its centre) inside one 1280 x 720 canvas; left panel 05-turn-then-slide.gdshader, right panel 06-slide-then-turn.gdshader; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 1.5 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 14 s. Left keyframes: angle 0 to 1.5708 over 0.10-0.24, then slide (0, 0) to (100, 0) over 0.24-0.38. Right keyframes: slide (0, 0) to (100, 0) over 0.58-0.70, then angle 0 to 1.5708 over 0.70-0.82 (so its card swings round the origin). All moves eased in-out; everything holds after. At the 50 % mark: left card at (100, 0) with its arrow pointing down, right card still at the origin. At 85 %: right card at (0, 100) with its arrow pointing down. Verified (end states): centres (100, 0) and (0, 100) (geometry-summary.txt).

### B23 · 36 words · ~12 s

> Why? A turn swings everything around the middle of the node. Slide first, and the picture sits off to one side, so the turn carries it round in an arc. Order is part of the move.

*Picture.* The screen-direction grid with a small cross at the origin and the card (a small cream rectangle with a terracotta dot at its centre) at the origin. The card slides one hundred units right (an arrow), then a dashed quarter-circle arc around the origin appears and the card travels along it, turning as it goes, to the point one hundred units below the origin. A faint ghost marks where 'turn then slide' would have left it. Labels 'slide first' and 'then turn'.

*Motion.* The card slides out, then swings along an arc around the origin and ends below it.

*Lane.* manim · `B23_TurnSwingsAroundTheMiddle` · runner-up: ShaderLab with the earlier capture

### B24 · 38 words · ~13 s

> Real shaders stack all three: scale, then turn, then slide. Write the product with scale nearest the point and slide farthest away. The slide is never scaled or turned, so it stays exactly as long as you asked.

*Picture.* Code card at left with the four-line vertex function (scale_by, turn_by and slide_by are the small functions of the same file); at right a framed Godot window with the card and its origin cross. Three scripted sweeps in turn: the card grows by half, turns thirty degrees, then slides right and slightly up; readouts 'scale', 'turn', 'slide' land as each begins.

*Motion.* Three sweeps in turn, each changing the picture, ending in one combined pose.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C07: 07-three-moves.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 1.5 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a small grey cross at the node's origin drawn by the scene; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 15 s. Keyframes (ease in-out each): grow 1.0 to 1.5 over 0.08-0.20; angle 0 to 0.5236 over 0.20-0.32; slide (0, 0) to (100, -40) over 0.32-0.44; hold. At the 50 % and 85 % marks: the final pose (card 192 px, turned 30 degrees clockwise, centred 100 right and 40 up of the origin). Verified: bounding box x -31 to 231, y -171 to 91 (expected -31.1, 231.1, -171.1, 91.1) and centre exactly (100, -40) (geometry-summary.txt).

## Act IV: Fake 3D

### B25 · 37 words · ~13 s

> To flip a card you need a direction that runs through the screen, toward you and away. Call it depth, or z. Give every corner a third number for it. A flat card sits at depth zero.

*Picture.* Act title 'Fake 3D' (serif 40) top-left. Axes drawn obliquely: x to the right, y down, and a z axis crossing the screen plane (solid toward the lower left, dashed the other way, labelled 'z: depth'). A flat card (a rectangle outline in the x-y plane) with four terracotta corner dots; one corner shows its three numbers '(x, y, 0)'.

*Motion.* The z axis grows through the screen plane, and the corner dots take a third number: zero.

*Lane.* manim · `B25_DepthAxis` · runner-up: DesignPipelineClaim, show-tell isometric

### B26 · 32 words · ~11 s

> Careful: this three by three is a different animal. Before, the third number was a one, a trick for sliding. Now it is real depth. Same size of table, a different job.

*Picture.* Two bracketed three-slot columns side by side. Left: (x / y / 1) with the 1 ringed and the label 'slide trick'. Right: (x / y / z) with the z ringed and the label 'depth'. Between them a drawn double bar (not equal). Under each a small three-by-three outline. The ring pulses on the left 1, then on the right z.

*Motion.* The same three-slot column appears twice, and the ring on its last slot pulses first as a one and then as a depth.

*Lane.* manim · `B26_TwoKindsOfThirdNumber` · runner-up: LectureEvidenceTable

### B27 · 42 words · ~14 s

> Look down on the card from above, and it is a line. Turn it around the vertical axis, and the width the screen sees is the card's width times cosine of the angle. At a quarter turn you see only its edge.

*Picture.* A top view. A horizontal screen line at the bottom (label 'screen'). Above it a thin card drawn as a horizontal line segment centred on a small ring-and-dot that marks the vertical axis end-on (label 'vertical axis'); the segment's left end is a terracotta dot, its right end an ink dot. Light grey vertical lines drop from the two ends to the screen line, where two shadow dots mark the width (label 'the screen sees this'). The segment turns about the centre: the shadow dots slide together, shrink to one point at a quarter turn (label 'edge-on'), with the live caption 'width x cos'.

*Motion.* The card's line turns and its shadow on the screen line shrinks to a point.

*Lane.* manim · `B27_TopViewOfTheTurn` · runner-up: ShaderLab

### B28 · 36 words · ~12 s

> Here is the table for that turn. The middle column stays zero, one, zero, because the y arrow does not move. Multiply the corner, with depth zero, keep the first two numbers, and the card flips.

*Picture.* Code card at left with the real twelve-line shader; at right a framed Godot window with the card turning about its vertical axis. A readout 'y arrow stays' lands when the middle column is highlighted; the card ends at a forty-five degree turn, narrower, with the same height.

*Motion.* The card narrows from the sides as the angle grows, while the middle column stays zero, one, zero.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C08: 08-flip.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 15 s. flip keyframes: 0.0 from 0.00 to 0.10, 0.125 at 0.34 (ease in-out), then hold 0.125. At the 50 % and 85 % marks: the card at 45 degrees, 90 card-pixels wide and 128 tall. Verified: width 90 x 128 (geometry-summary.txt); planning still png/still-flip-0.125.png.

### B29 · 34 words · ~12 s

> At a quarter turn the card is edge-on, zero wide, and nothing is drawn. Past it, cosine goes negative, which mirrors the picture. You are seeing the front from behind, not a different back.

*Picture.* A framed Godot window, full width. The card narrows to nothing: for a moment the window shows only the stage and the readout 'edge-on: nothing drawn'; then the card reappears on the far side of the turn, mirrored (arrow pointing left, small square top right) with the readout 'mirrored'.

*Motion.* The card narrows to nothing, the window is empty for a beat, and the card comes back mirrored.

*Lane.* capture · `ShaderLab` · runner-up: manim top view with shadow dots swapping sides

*Capture to record.* C09: 08-flip.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 14 s. flip keyframes: 0.15 from 0.00 to 0.10, 0.25 at 0.26 (ease), hold 0.25 until 0.34 (empty window), 0.5 at 0.44 (ease), hold 0.5. At the 50 % and 85 % marks: the mirrored card, fully visible. Verified: nothing drawn at flip 0.25 and 0.75; corner colours swap left to right at 0.5 (gradient texture); planning stills png/still-flip-0.25-edge-on.png and png/still-flip-0.5-mirrored.png.

### B30 · 38 words · ~13 s

> Turn around x instead, and the card tips: its height shrinks. Turn around z, and it spins flat, like the first turn we built. Three axes, three tables, and the axis you turn around keeps its own column.

*Picture.* Three small cards side by side, each with its own label under it: 'around x', 'around y', 'around z'. They turn together: the first tips (its height shrinks), the second flips (its width shrinks), the third spins flat. Under each card a small bracketed column of three numbers is ringed: (1 / 0 / 0), (0 / 1 / 0), (0 / 0 / 1), captioned 'stays put'.

*Motion.* Three cards turn at once: one tips, one flips, one spins; the column that stays put is ringed under each.

*Lane.* manim · `B30_ThreeAxesThreeTables` · runner-up: LectureEvidenceTable

### B31 · 41 words · ~14 s

> Turn around two axes at once by multiplying the two tables, same right to left rule. The card flips and leans, and its outline slants. One turn alone is only a squeeze; stacked turns are where the tables earn their keep.

*Picture.* Code card at left with the four-line vertex function (around_x and around_y are the two small functions of the same file); at right a framed Godot window. The card first flips by an eighth of a turn, then leans forward; its outline ends as a slanted parallelogram. A readout 'a parallelogram' lands.

*Motion.* The card flips and then leans, and its outline slants.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C10: 09-flip-and-tip.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 17 s. Keyframes (ease in-out): flip 0 to 0.125 over 0.12-0.30; tip 0 to 0.1 over 0.30-0.44; hold. At the 50 % and 85 % marks: the final pose. Verified: bounding box x -45 to 45, y -78 to 78; left and right edges both 103.6 card-pixels (geometry-summary.txt); planning still png/still-flip-and-tip.png.

### B32 · 39 words · ~13 s

> It is still fake. In a real three-D view the nearer edge looks bigger. Here, at an eighth of a turn, both edges are one hundred twenty-eight pixels tall. No perspective, no depth, only the shadow of a turn.

*Picture.* A framed Godot window with the card held at an eighth of a turn. A terracotta ring settles on the card's left edge and another on its right edge; readouts '128 px' land beside each, then 'no perspective' lands under the window.

*Motion.* Two rings land on the two edges, each with the same number.

*Lane.* capture · `ShaderLab` · runner-up: manim comparing a trapezoid with a rectangle

*Capture to record.* C11: still PNG (3840 x 2160) of 08-flip.gdshader at flip 0.125; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; Forward+. Verified: the card is 90 card-pixels wide and its two vertical edges are each 128 card-pixels tall (columns 44.5 px either side of centre measure 128 and 128). The rings and readouts are drawn by ShaderLab, not by the scene.

### B33 · 36 words · ~12 s

> So it suits flat things: a card, a coin, a sign. It fails for a box, whose sides would have to appear as it turns. This table turns a flat shape; it cannot invent the sides.

*Picture.* The same top view as the earlier picture, now with a box: a square footprint centred on the end-on vertical axis, its front edge a terracotta line and its other three edges grey. The screen line below shows two shadow bars: an ink bar for 'what the table draws' (the front edge only) and a grey bar for 'what a box would show' (the whole footprint). The box turns a quarter turn: the ink bar shrinks to a point while the grey bar stays wide.

*Motion.* The box turns; the table's bar shrinks to nothing while the bar the box should show stays wide.

*Lane.* manim · `B33_WhatABoxWouldShow` · runner-up: ShaderLab

### B34 · 35 words · ~12 s

> To drive it from your game, make flip a uniform from zero to one, and multiply by tau. Zero faces you. One half shows the back. One is a full turn, and the front again.

*Picture.* Code card at left with the real twelve-line shader; at right a framed Godot window with the card. Readouts land as the sweep runs: 'flip 0' (front), 'flip 0.5' (the back, mirrored), 'flip 1' (the front again).

*Motion.* The card goes front, back, front as the flip value passes zero, one half and one.

*Lane.* capture · `ShaderLab` · runner-up: manim number line from 0 to 1

*Capture to record.* C12: 08-flip.gdshader on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 14 s. flip keyframes: 0.0 until 0.56, 0.5 at 0.66 (ease), hold, 1.0 at 0.82 (ease), hold. At the 50 % mark: the front (flip 0). At 85 %: the front again (flip 1). Verified: set_shader_parameter drives the uniform (verify3 D1); flip 1.0 equals flip 0.0 (identity).

## Act V: The Pivot

### B35 · 38 words · ~13 s

> A door does not turn around its middle. It turns around its hinge. These tables only know one pivot, the origin, the middle of the node. To turn around an edge, move that edge to the middle first.

*Picture.* Act title 'The Pivot' (serif 40) top-left. A framed Godot window: the card swings like a door about its LEFT edge, a terracotta dot marks that edge (the hinge) and does not move while the rest of the card narrows toward it. Readout 'pivot' beside the dot; the caption reads 'pivot: the point it turns around'.

*Motion.* The card swings about its left edge; the terracotta hinge dot never moves.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C13: 11-door.gdshader with pivot (-64, 0) x U on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a terracotta dot (radius 6 logical px) at the pivot, placed at the card's left edge midpoint; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 15 s. flip keyframes: 0.0 from 0.00 to 0.10, 0.15 at 0.36 (ease), hold 0.15. At the 50 % and 85 % marks: the card at 54 degrees, its left edge at the hinge dot. Verified: left edge stays at -64; right edge at -64 + 128 cos (geometry-summary.txt).

### B36 · 30 words · ~10 s

> So: three steps. Slide the pivot to the middle. Turn. Slide back. The order matters again: the slide back has to come last, or the card ends up somewhere else.

*Picture.* The screen-direction grid with a small cross at the origin and a card whose left edge carries a terracotta pivot dot. Step 1 (label '1 slide in'): the card slides so that the pivot dot lands on the origin cross. Step 2 ('2 turn'): the card's width narrows and widens about the origin (a flip). Step 3 ('3 slide back'): the card slides back by the same amount, and the pivot dot returns to its original place; label 'the pivot never moved'.

*Motion.* The card slides so the hinge dot sits on the origin, flips there, then slides back to where it was.

*Lane.* manim · `B36_SlideTurnSlideBack` · runner-up: DesignPipelineClaim, show-tell isometric

### B37 · 28 words · ~10 s

> As tables, read it from the right: slide in, then turn, then slide back. Multiply the three once, and one table swings any flat shape around any point.

*Picture.* A full-frame code card with the real six-line vertex function (the product written over three lines, one table per line). Focus climbs the product from the bottom line (slide in) to the middle (turn) to the top (slide back), then all three lines glow together.

*Motion.* Focus climbs the three lines from the bottom up, the way the point meets the tables.

*Lane.* remotion · `ShaderLab` · runner-up: LectureCodeTrace

### B38 · 25 words · ~8 s

> Put the pivot on the top left corner, and a flat spin swings the sprite like a pendulum. The corner stays exactly where it was.

*Picture.* A framed Godot window: the card swings like a pendulum about its TOP LEFT corner while a terracotta dot marks that corner and does not move. Readout 'pivot' beside the dot early, 'corner stays' when it has swung.

*Motion.* The card swings round its top left corner; the terracotta dot stays put.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C14: 10-spin-about-corner.gdshader with pivot (-64, -64) x U on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a terracotta dot at the pivot; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 10 s. angle keyframes: 0 from 0.00 to 0.10, 0.7854 at 0.36 (ease), hold until 0.62, 1.5708 at 0.80 (ease), hold. At the 50 % mark: the card turned 45 degrees about the corner. At 85 %: a quarter turn. Verified: bbox x -155 to 26, y -64 to 117 at 0.7854 (expected -154.5, 26.5, -64, 117); the top left corner stays at (-64, -64) (geometry-summary.txt).

### B39 · 43 words · ~15 s

> The pivot is in pixels from the node's origin. A centered sprite has its origin in the middle, so a one hundred twenty-eight pixel sprite has its right edge at sixty-four. If it is not centered, the origin is its top left corner.

*Picture.* Two cards side by side, each with a ruler along its top edge. Left card 'centered': the origin dot in the middle, ruler ticks -64, 0, 64; a terracotta tick on the right edge reads '64'. Right card 'not centered': the origin dot at its top left corner, ticks 0 and 128; its right edge reads '128'. The right card appears later.

*Motion.* Each card shows its origin dot and the number on its right edge: sixty-four for one, one hundred twenty-eight for the other.

*Lane.* manim · `B39_PixelsFromTheOrigin` · runner-up: LectureEvidenceTable

### B40 · 33 words · ~11 s

> For the flip, the turning table already uses the third number for depth, so the slides become plain subtraction and addition. Subtract the pivot from the corner, turn it, add the pivot back.

*Picture.* A cream code card with the real nine-line vertex function of the door shader; focus runs down the three arrow lines, then lands on the subtraction line, the turn line and the add-back line as each is named.

*Motion.* Focus steps down the lines: the three arrows, then subtract the pivot, then turn, then add it back.

*Lane.* remotion · `LectureCodeTrace` · runner-up: manim

### B41 · 34 words · ~12 s

> Pivot on the left edge, and the card swings like a door. That edge never moves while the rest folds toward it. Past the quarter turn the card lies on the other side, mirrored.

*Picture.* A framed Godot window: the card swings like a door about its left edge, which carries the terracotta hinge dot. It folds toward the hinge to a door-ajar pose, then passes edge-on and ends flat on the far side of the hinge, mirrored (arrow pointing left). Readouts 'edge stays put' and 'far side, mirrored'.

*Motion.* The card folds toward the hinge, vanishes for an instant, and ends lying on the other side, mirrored.

*Lane.* capture · `ShaderLab` · runner-up: manim

*Capture to record.* C15: 11-door.gdshader with pivot (-64, 0) x U on the card; card texture drawn at 1024 px (U = 8 times the 128 px card; a clean cream card, warm grey border, teal arrow pointing right, small teal square top left), node scale k/8 with k = 2.0 in a 1280x720 logical canvas, every pixel-valued uniform multiplied by U; a terracotta dot at the pivot; 4K SubViewport route, Forward+, 30 fps, offline fixed tick, no input; 14 s. flip keyframes: 0.0 from 0.00 to 0.10, 0.125 at 0.30 (ease), hold until 0.60, 0.5 at 0.80 (ease; passes edge-on near 0.68), hold. At the 50 % mark: the card at 45 degrees with its left edge at the hinge. At 85 %: the card lies on the far side (left of the hinge), mirrored. Verified: left edge fixed at -64 at flip 0.0625, 0.125, 0.1875; at flip 0.5 the card spans -192 to -64 and its gradient corners are mirrored (geometry-summary.txt).

## Closing

### BVDT · recap · 76 words · ~26 s

> Let's recap with Claude. A matrix is a saved move: a table that moves any point. Scale, turn and slide are tables, and Godot writes tables by columns. Multiply tables to combine moves; the table nearest the point acts first. Turning around an axis fakes a flip: no perspective, no depth. To turn around a pivot, slide it to the middle, turn, slide back. Check the columns, the order and the pivot, whoever wrote the shader.

*Picture.* The recap card: A matrix is a saved move: a table that moves any point. / Scale, turn and slide are tables, and Godot writes tables by columns. / Multiply tables to combine moves; the table nearest the point acts first. / Turning around an axis fakes a flip: no perspective, no depth. / To turn around a pivot, slide it to the middle, turn, slide back. / Check the columns, the order and the pivot, whoever wrote the shader.

### BHTF · your turn · 98 words · ~33 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader that swings a sprite like a door. A float uniform called flip, from zero to one, is the fraction of a full turn around the vertical axis. A uniform called pivot, in pixels from the sprite's origin, is the hinge. Then point me to the lines that move the pivot. Now check two things yourself. At flip zero, does the sprite look exactly as it did before the shader? And with the pivot on the left edge, does that edge stay put while the card swings?

*Prompt shown and read in full:* Write a Godot canvas item shader that swings a sprite like a door. A float uniform called flip, from zero to one, is the fraction of a full turn around the vertical axis. A uniform called pivot, in pixels from the sprite's origin, is the hinge. Then point me to the lines that move the pivot.

*Two checks:* Check: at flip zero, the sprite looks exactly as it did before the shader. · Check: with the pivot on the left edge, that edge stays put while the card swings.

### BOUT · outro · 9 words · ~4 s

> Matrices and Fake Three D. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.


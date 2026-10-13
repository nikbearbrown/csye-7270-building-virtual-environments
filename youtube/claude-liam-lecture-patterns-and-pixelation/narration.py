"""narration.py: every spoken line of "Patterns and Pixelation". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party course on 2D shaders in Godot (ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted sweeps are labelled; the captures use the
nearest texture filter and say so; no frame-rate claim is made (the captures are offline renders).
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-patterns-and-pixelation"
TITLE = "Patterns and Pixelation"
TITLE_LINES = ["Patterns and", "Pixelation"]
OPENING_DESCRIPTION = "How cells make blocks, checkers, stripes and dots"
SUMMARY = ("Learn the two small functions that cut a shape into cells, and use them to pixelate an image "
           "and to draw checkerboards, stripes and dots.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · CELLS"
TAGS = ["Godot", "Shaders", "Pixelation", "Checkerboard", "Stripes", "Dots", "floor", "fract", "mod", "UV", "Fragment shader",
        "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Which Cell, and Where in It"),
    ("II", "Pixelate Without the Drift"),
    ("III", "Blocks of Any Size"),
    ("IV", "Checkerboards and Stripes"),
    ("V", "Dots, and Both Numbers at Once"),
]

BODY = [
    # ── ACT I · which cell, and where in it ────────────────────────────────────────────────────────────────────────────────
    ("B01", 0, "Chunky pixel blocks. A checkerboard. Moving stripes. A grid of dots. Four effects, and none of them needs a pattern image. "
               "All four come from one trick: cut the address into cells."),
    ("B02", 0, "Start with the address. Across a shape it runs from zero to one. Multiply it by four and the address is stretched: "
               "it runs from zero to four. Each whole number it passes starts a new cell."),
    ("B03", 0, "Floor tells you which cell you are in. Floor rounds down: zero point seven becomes zero, two point nine becomes two. "
               "So floor of the stretched address is the cell number: zero, one, two or three."),
    ("B04", 0, "Fract keeps what floor throws away: the part after the point. Two point nine leaves point nine. "
               "Inside every cell it climbs from zero to one, then starts over."),
    ("B05", 0, "Together they pin down a spot exactly. Floor says which cell: column two, row one. "
               "Fract says where inside it: three tenths across, seven tenths down. That is the whole idea."),
    ("B06", 0, "Here is floor, drawn by a shader for two-D, which Godot calls canvas item. The address is a pair of numbers, so floor works on both. "
               "Red follows the column, green follows the row, and every cell is one flat color."),
    ("B07", 0, "Now fract. Every cell holds its own copy of the same gradient. "
               "Red grows left to right, green grows top to bottom, and both start over at every border."),
    ("B08", 0, "Read a picture with fract as the address, and the picture repeats in every cell. "
               "Here: three across, three down. A tiled floor, from two lines."),
    ("B09", 0, "Here is the map for the rest of the film. Floor gives one value per cell: that is pixelation and checkerboards. "
               "Fract gives a shape that repeats: that is stripes and dots. Use both, and you get a screen of dots."),

    # ── ACT II · pixelate without the drift ───────────────────────────────────────────────────────────────────────────────────
    ("B10", 1, "To pixelate is to show a picture as big blocks. Inside a block, every pixel has the same color. "
               "So how does a shader pick one color for a whole block?"),
    ("B11", 1, "Make every pixel in a cell look up the picture at the same spot. One cell, one spot, one color. "
               "That is all pixelating is. The only question is which spot."),
    ("B12", 1, "First guess: the corner where the cell starts. Floor the stretched address, divide by the same number, "
               "and every address snaps to its cell's top left corner. All the pixels in a cell now read the same spot."),
    ("B13", 1, "Which way will the picture slide? Watch the sprite when the shader switches on. "
               "It jumps down and to the right, by about three and a half picture pixels. That is half a block."),
    ("B14", 1, "Why? A block shows what sits at its own top left corner. "
               "So the picture arrives late: on average half a block further right, and half a block further down."),
    ("B15", 1, "The fix: look up the middle of the cell. Add one half to the cell number before you divide back. "
               "Now a block shows what sits at its center, and the picture stays where it was."),
    ("B16", 1, "Walk one pixel through it. Address point six, four blocks. Times four is two point four. "
               "Floor gives two. Add a half: two and a half. Divide by four: point six two five, the middle of the third cell."),
    ("B17", 1, "Here is a tempting variant: put the half inside the floor instead. That rounds to the nearest grid line. "
               "The picture no longer drifts, so it looks fixed. But there is a second problem, at the edges."),
    ("B18", 1, "Look at the edges. The grid is shifted half a block against the picture, so the first and last blocks "
               "are only half as wide. Measured: four pixels at each edge, eight everywhere else."),
    ("B19", 1, "So only one of the three is right. The corner drifts. The nearest grid line gives half-size edge blocks. "
               "The middle has neither problem. Use the middle."),

    # ── ACT III · blocks of any size ────────────────────────────────────────────────────────────────────────────────────────
    ("B20", 2, "So far you typed how many blocks to draw. But you think in how big a block is: eight pixels of the picture, say. "
               "For that, the shader has to know how many pixels the picture has."),
    ("B21", 2, "It can ask, if what you are drawing has a texture. Texture pixel size is the size of one picture pixel, in address units. "
               "One divided by it is the picture's size in pixels: a hundred and twenty-eight, for this sprite."),
    ("B22", 2, "Multiply texture pixel size by a block size, and you get one cell in address units. Divide, floor, add a half, multiply back: "
               "the same recipe, now counted in picture pixels. Eight means eight pixels across."),
    ("B23", 2, "Make the block size a uniform, and your game can animate it. One is the original picture. Thirty-two is chunky. "
               "A pixelating transition is this one number, counting up."),
    ("B24", 2, "Blocks are counted in picture pixels, so they scale with the sprite. Draw it bigger and the blocks grow too: "
               "still sixteen across. This pixelates the picture, not the screen."),
    ("B25", 2, "One catch. If the block size does not divide the picture, the last block comes up short. "
               "Blocks of six on a picture a hundred and twenty-eight wide: twenty-one whole blocks, then one of two pixels."),

    # ── ACT IV · checkerboards and stripes ──────────────────────────────────────────────────────────────────────────────────
    ("B26", 3, "A checkerboard alternates. So give each cell two numbers, column and row, and add them. "
               "One cell to the right, the sum goes up by one. One cell down, it goes up by one again."),
    ("B27", 3, "Take the remainder after dividing by two. An even sum leaves zero, an odd sum leaves one: "
               "exactly the number that picks between two colors. Mod gives the remainder. Three mod two is one."),
    ("B28", 3, "Move diagonally and the sum goes up by two. The color flips on every rise of one, so two flips bring you back to the same color. "
               "That is why a square touches its own color only at the corners."),
    ("B29", 3, "In the shader: floor gives column and row, add them, take mod two, and let that mix two colors. "
               "Use mod, not percent: a shader refuses percent on decimals."),
    ("B30", 3, "Stripes need only one number per pixel: how far along a direction you are. "
               "Add the two address numbers and you get a diagonal ramp, from zero in one corner to two in the opposite one."),
    ("B31", 3, "Multiply the ramp by a stripe count, then take fract. The ramp restarts again and again: a sawtooth. "
               "Cut each tooth with step at a width, and every tooth becomes one stripe."),
    ("B32", 3, "Run it, and there are the stripes. Count is how many pairs fit across the shape. "
               "Width is how much of each pair is gold: at one half, equal shares."),
    ("B33", 3, "To make them move, subtract time times a speed inside the fract. Time is one clock for the whole game. "
               "The pattern slides toward the bottom right, and fract still works when the number goes negative."),
    ("B34", 3, "Same recipe both times. Make one number per pixel: column plus row, or the diagonal. "
               "Make it repeat, with mod or with fract. Cut it into two colors."),

    # ── ACT V · dots, and both numbers at once ──────────────────────────────────────────────────────────────────────────────
    ("B35", 4, "Dots need to know where you are inside a cell, and fract says that, from zero to one. "
               "Subtract one half, and zero sits in the middle of the cell."),
    ("B36", 4, "Length of that pair is the distance from the middle of the cell. Compare it with a radius. "
               "Step gives zero inside the circle and one outside, and that picks between dot color and background."),
    ("B37", 4, "In code: fract of the stretched address, minus a half. Length of that. "
               "Step against the radius, and mix the two colors. Eight cells across, eight down, one dot in each."),
    ("B38", 4, "Grow the radius and the dots swell. At one half they touch their neighbors. "
               "By seven tenths they fill the whole cell, because a cell's corner is that far from its middle."),
    ("B39", 4, "One trap. On a wide rectangle the dots turn into ovals. The address runs zero to one across and down, "
               "whatever the shape, so cells stretch with the shape. These dots are one point eight times wider than tall."),
    ("B40", 4, "The fix: give each direction its own count, in the shape's proportions. "
               "Sixteen across and nine down for a sixteen by nine rectangle, and every cell is square again. Every dot is round."),
    ("B41", 4, "Now use both numbers at once. Floor picks the cell, and we read the picture at the cell's middle: the pixelate lookup. "
               "Fract draws the dot, and the dot takes that color."),
    ("B42", 4, "Same trap, in dots. Round the cell number and the dots sit on grid lines, so the ones along the edge are cut in half. "
               "Floor it, and the grid starts at the picture's edge: every dot is whole."),
    ("B43", 4, "Few cells give chunky dots. More cells bring the picture back. "
               "One shader: a lookup per cell, a dot per cell, and one number to turn between them."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people think a checkerboard, a stripe or a grid of dots needs a pattern image. "
         "It does not. A pattern is math on the address, and the graphics card runs it for every pixel.")
BIDEA_TEXT = ("Patterns need a pattern image.", "a pattern image", "math on the address")

BDEFS = ("Six terms. A shader is a small program the graphics card runs to decide how something is drawn. "
         "U V is a point's address on the shape: zero to one across, zero to one down. A texture is an image a shader can read. "
         "A uniform is a value your game sets from outside. A cell is one square of a grid. "
         "A remainder is what is left after dividing.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Texture", "an image a shader can read by address"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
    ("Cell", "one square of a grid"),
    ("Remainder", "what is left after dividing"),
]

BVDT_HEADING = "Patterns and Pixelation"
BVDT_LINES = [
    "Floor says which cell, and fract says where inside it.",
    "To pixelate, look up the middle of each cell, not its corner.",
    "The texture can tell you its size, so blocks can be counted in picture pixels.",
    "A checkerboard is column plus row, reduced by mod two.",
    "Stripes are fract of a diagonal ramp, cut in two with step.",
    "A dot is a distance in a cell's own space, and each direction needs its own count.",
]
BVDT_NARRATION = ("Let's recap with Claude. " + " ".join(BVDT_LINES))

BHTF_PROMPT = ("Write a Godot canvas item shader that shows a sprite's texture as a grid of round dots. "
               "One float uniform called cells, from four to sixty-four, sets how many dots fit along the shorter side. "
               "Each dot takes the texture's color at the middle of its cell. Keep the dots round, even on a wide texture.")
BHTF_CHECKS = ["Check: with cells at eight, you count eight round dots along the shorter side.",
               "Check: on a square texture, the dots along every edge are whole."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. With cells at eight, do you count eight round dots along the shorter side? "
                  "And on a square texture, are the dots along every edge whole? Half dots on the edge mean the cells were rounded, not floored.")
BHTF_SEGMENT = "Turn a Picture into Dots"

CUT_LINE = ("Cut, in this order: the scale beat (B24), the worked example (B16) and the diagonal-step beat (B28), then merge the moving "
            "stripes (B33) into the stripes beat (B32). Each repeats an idea another beat already carries. The drift pair (B13, B14), "
            "the rounding pair (B17, B18), the wide-shape trap (B39, B40) and the dot screen with its edge check (B41, B42) stay: "
            "they are the proof and the payoff.")

"""narration.py: every spoken line of "Matrices and Fake 3D". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured or
checked in evidence/planning-checks/), and a third-party video course on matrices and fake 3D in Godot shaders (ideas followed, nothing
copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted sweeps are labelled; the picture is flat, so the film says
plainly that there is no perspective and no depth.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
The title is "Matrices and Fake 3D" on every screen; SPOKEN_TITLE spells it "Three D" for the voice and is what BOPEN and the outro narration use.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-matrices-and-fake-3d"
TITLE = "Matrices and Fake 3D"
TITLE_LINES = ["Matrices and", "Fake 3D"]
SPOKEN_TITLE = "Matrices and Fake Three D"
OPENING_DESCRIPTION = "A matrix is a saved move, and it can flip a card"
SUMMARY = "Learn what a matrix does to a point, how to combine moves, and how to flip a flat picture like a card."
BOPEN = S.bopen(SPOKEN_TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · MATRICES"
TAGS = ["Godot", "Shaders", "Matrix", "Matrices", "Vertex shader", "mat3", "Transform", "Rotation matrix", "Fake 3D", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "A Table That Moves Points"),
    ("II", "Three Moves"),
    ("III", "Moves Together"),
    ("IV", "Fake 3D"),
    ("V", "The Pivot"),
]

BODY = [
    # ── ACT I · a table that moves points ───────────────────────────────────────────────────────────
    ("B01", 0, "Watch a flat picture turn over like a card. No three-D model, no animation file. Every corner of the shape is multiplied by a small table of numbers. Learn that table, and you can spin, shrink, slide and flip anything you draw."),
    ("B02", 0, "Take a point: five across, six down. Multiply it by a table of four numbers. Top row first: one times five plus three times six is twenty-three. Bottom row: two times five plus four times six is thirty-four."),
    ("B03", 0, "In Godot, that is one multiplication. Mat two builds the table, the star multiplies, and this shader checks its answer against twenty-three, thirty-four. Teal means they agree."),
    ("B04", 0, "Look at the numbers in the code: one, two, then three, four. Godot reads each vec two as a column. So one, two stands upright on the left, and the table's top row is one, three."),
    ("B05", 0, "The documentation says it plainly: build a matrix from vectors, and they are read as columns. Whoever wrote the shader, a person or an AI, this is the first thing to check."),
    ("B06", 0, "Mix it up and nothing complains. Read the numbers as rows, and the answer is seventeen, thirty-nine. Put the point on the left of the table, and you get seventeen, thirty-nine again. Table first, point second."),
    ("B07", 0, "Here is why columns make sense. The first column is where one step across lands. The second is where one step down lands. Five steps of the first and six of the second add up to twenty-three, thirty-four."),
    ("B08", 0, "The plainest table leaves both arrows where they started: one, zero, then zero, one. That is the identity matrix, and it moves nothing. In Godot, mat two of one gives exactly that table."),
    ("B09", 0, "Stretch the arrows and the table scales. Two, zero, then zero, two lands each arrow twice as far out, so every point ends up twice as far from the middle."),
    ("B10", 0, "A shape is made of its corners. Multiply every corner by the same table and the whole shape follows. Four corners, one table: a move saved in four numbers."),

    # ── ACT II · three moves ────────────────────────────────────────────────────────────────────────
    ("B11", 1, "Now something real. Godot calls the vertex function once per corner of a shape, and hands it the corner's position in pixels from the node's origin. On a centered sprite, that is the middle. Multiply it by the scale table, and the picture grows."),
    ("B12", 1, "Turning is a table too. Turn by an angle, and the across arrow lands at cosine, sine. Those are how far across and how far down you get on a circle of radius one. The down arrow lands at minus sine, cosine."),
    ("B13", 1, "Angles are in radians, so a full turn is about six point two eight, which Godot calls tau. Sweep the angle up to an eighth of tau and the picture turns clockwise, because on screen y points down."),
    ("B14", 1, "Sliding is different. Whatever two by two table you pick, the point at zero, zero stays at zero, zero, because zero times anything is zero. A two by two table can scale and turn, but it cannot slide."),
    ("B15", 1, "The fix is one extra number. Give the point a third number, always one, and use a three by three table. Put the slide in the last column: the top row now gives x plus the slide, and the bottom row keeps the one."),
    ("B16", 1, "In the shader, put a one on the end of the corner's position, multiply, and keep the first two numbers. The slide sits in the last column, and the picture moves a hundred pixels to the right."),
    ("B17", 1, "Three moves, three tables. Scale puts its numbers on the diagonal. Turn puts cosine and sine in the first two columns. Slide puts the offset in the last column. None of them bends an edge, so four moved corners are enough."),

    # ── ACT III · moves together ────────────────────────────────────────────────────────────────────
    ("B18", 2, "A slide alone is simpler as plain addition. Tables pay off when moves combine: a scale, a turn and a slide saved as one table. Then every corner needs one multiplication, not three."),
    ("B19", 2, "To multiply tables, they must be the same size. Copy a two by two into the corner of a three by three, with zeros around it and a one in the bottom right. Godot does it for you: mat three of a mat two."),
    ("B20", 2, "Multiply two tables and you get one table that does both moves. The rule is the one you know: each entry is a row of the left table times a column of the right."),
    ("B21", 2, "Which move happens first? The one nearest the point. Slide times turn, times point, turns first, then slides. Read it from the right, the way the point meets the tables."),
    ("B22", 2, "Same two tables, two orders. Turn a quarter, then slide a hundred pixels right: the picture spins in place, then shifts across. Slide first, then turn: it ends a hundred pixels below the middle."),
    ("B23", 2, "Why? A turn swings everything around the middle of the node. Slide first, and the picture sits off to one side, so the turn carries it round in an arc. Order is part of the move."),
    ("B24", 2, "Real shaders stack all three: scale, then turn, then slide. Write the product with scale nearest the point and slide farthest away. The slide is never scaled or turned, so it stays exactly as long as you asked."),

    # ── ACT IV · fake three-D ───────────────────────────────────────────────────────────────────────
    ("B25", 3, "To flip a card you need a direction that runs through the screen, toward you and away. Call it depth, or z. Give every corner a third number for it. A flat card sits at depth zero."),
    ("B26", 3, "Careful: this three by three is a different animal. Before, the third number was a one, a trick for sliding. Now it is real depth. Same size of table, a different job."),
    ("B27", 3, "Look down on the card from above, and it is a line. Turn it around the vertical axis, and the width the screen sees is the card's width times cosine of the angle. At a quarter turn you see only its edge."),
    ("B28", 3, "Here is the table for that turn. The middle column stays zero, one, zero, because the y arrow does not move. Multiply the corner, with depth zero, keep the first two numbers, and the card flips."),
    ("B29", 3, "At a quarter turn the card is edge-on, zero wide, and nothing is drawn. Past it, cosine goes negative, which mirrors the picture. You are seeing the front from behind, not a different back."),
    ("B30", 3, "Turn around x instead, and the card tips: its height shrinks. Turn around z, and it spins flat, like the first turn we built. Three axes, three tables, and the axis you turn around keeps its own column."),
    ("B31", 3, "Turn around two axes at once by multiplying the two tables, same right to left rule. The card flips and leans, and its outline slants. One turn alone is only a squeeze; stacked turns are where the tables earn their keep."),
    ("B32", 3, "It is still fake. In a real three-D view the nearer edge looks bigger. Here, at an eighth of a turn, both edges are one hundred twenty-eight pixels tall. No perspective, no depth, only the shadow of a turn."),
    ("B33", 3, "So it suits flat things: a card, a coin, a sign. It fails for a box, whose sides would have to appear as it turns. This table turns a flat shape; it cannot invent the sides."),
    ("B34", 3, "To drive it from your game, make flip a uniform from zero to one, and multiply by tau. Zero faces you. One half shows the back. One is a full turn, and the front again."),

    # ── ACT V · the pivot ───────────────────────────────────────────────────────────────────────────
    ("B35", 4, "A door does not turn around its middle. It turns around its hinge. These tables only know one pivot, the origin, the middle of the node. To turn around an edge, move that edge to the middle first."),
    ("B36", 4, "So: three steps. Slide the pivot to the middle. Turn. Slide back. The order matters again: the slide back has to come last, or the card ends up somewhere else."),
    ("B37", 4, "As tables, read it from the right: slide in, then turn, then slide back. Multiply the three once, and one table swings any flat shape around any point."),
    ("B38", 4, "Put the pivot on the top left corner, and a flat spin swings the sprite like a pendulum. The corner stays exactly where it was."),
    ("B39", 4, "The pivot is in pixels from the node's origin. A centered sprite has its origin in the middle, so a one hundred twenty-eight pixel sprite has its right edge at sixty-four. If it is not centered, the origin is its top left corner."),
    ("B40", 4, "For the flip, the turning table already uses the third number for depth, so the slides become plain subtraction and addition. Subtract the pivot from the corner, turn it, add the pivot back."),
    ("B41", 4, "Pivot on the left edge, and the card swings like a door. That edge never moves while the rest folds toward it. Past the quarter turn the card lies on the other side, mirrored."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Matrices have a reputation: advanced math, the part you skip. They are simpler than that. "
         "A matrix is a saved move, a small table of numbers that moves any point you give it.")
BIDEA_TEXT = ("A matrix is\nadvanced math you can skip.", "advanced math you can skip", "a saved move")

BDEFS = ("Five terms. A vector is a bundle of numbers, here a point's position. A matrix is a grid of numbers in rows and columns. "
         "A vertex is a corner point of a shape. A uniform is a value your game sets from outside. "
         "And a radian is Godot's angle unit: a full turn is tau, about six point two eight.")
BDEFS_TERMS = [
    ("Vector", "a bundle of two to four numbers"),
    ("Matrix", "a grid of numbers in rows and columns"),
    ("Vertex", "a corner point of a shape"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
    ("Radian", "Godot's angle unit; a full turn is tau, about 6.283"),
]

BVDT_HEADING = "Matrices and Fake 3D"
BVDT_LINES = [
    "A matrix is a saved move: a table that moves any point.",
    "Scale, turn and slide are tables, and Godot writes tables by columns.",
    "Multiply tables to combine moves; the table nearest the point acts first.",
    "Turning around an axis fakes a flip: no perspective, no depth.",
    "To turn around a pivot, slide it to the middle, turn, slide back.",
    "Check the columns, the order and the pivot, whoever wrote the shader.",
]
BVDT_NARRATION = ("Let's recap with Claude. " + " ".join(BVDT_LINES))

BHTF_PROMPT = ("Write a Godot canvas item shader that swings a sprite like a door. A float uniform called flip, from zero to one, "
               "is the fraction of a full turn around the vertical axis. A uniform called pivot, in pixels from the sprite's origin, "
               "is the hinge. Then point me to the lines that move the pivot.")
BHTF_CHECKS = ["Check: at flip zero, the sprite looks exactly as it did before the shader.",
               "Check: with the pivot on the left edge, that edge stays put while the card swings."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Now check two things yourself. At flip zero, does the sprite look exactly as it did before the shader? "
                  "And with the pivot on the left edge, does that edge stay put while the card swings?")
BHTF_SEGMENT = "Swing a Sprite on a Hinge"

CUT_LINE = ("Cut, in this order: the order-swap pair (B22, B23), the corner spin (B38), the two-turns beat (B31) and the card-versus-box beat (B33): "
            "each repeats an idea another beat already carries. The columns trio (B04 to B06), the product-order beat (B21), the flip itself "
            "(B28, B29) and the door (B35, B41) stay: they are the stumbling blocks and the payoff.")

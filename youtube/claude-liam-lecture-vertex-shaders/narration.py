"""narration.py: every spoken line of "Vertex Shaders". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party course (ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted events are labelled; a shader changes the drawing, never the node,
and the film says so; a wave on a plain rectangle is shown failing before it is shown working.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
Capital-letter built-ins (VERTEX, COLOR, TIME) are written as lowercase words in speech; the screen shows the real spelling.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-vertex-shaders"
TITLE = "Vertex Shaders"
TITLE_LINES = ["Vertex Shaders"]
OPENING_DESCRIPTION = "How a shader moves corners to bend a shape"
SUMMARY = "Learn how a shader moves the corner points of a shape, and how to give a shape enough corners to bend. By the end you can build a waving flag."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · VERTEX"
TAGS = ["Godot", "Shaders", "Vertex shader", "Varying", "Mesh", "Polygon2D", "Game development", "2D", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Corners"),
    ("II", "More Corners"),
    ("III", "A Waving Flag"),
    ("IV", "Passing Data Forward"),
    ("V", "When It Looks Wrong"),
]

BODY = [
    # ── ACT I · Corners ─────────────────────────────────────────────────────────────────────────────
    ("B01", 0, "This flag is waving, and not one pixel in it was told to move. One line of code moves its corner points, and the graphics card fills in everything between them. That line lives in a function called vertex."),
    ("B02", 0, "A shape is built from corner points, its vertices. The engine calls vertex once for each one, and asks a single question: where does this corner go?"),
    ("B03", 0, "The engine hands you the corner's position in a built-in, a value it gives your function. Its name is vertex too, in capital letters. Whatever you leave in it is where the corner goes."),
    ("B04", 0, "It counts in pixels, from the middle of the sprite. A sprite one hundred twenty-eight pixels wide has corners at minus sixty-four and sixty-four. The y axis points down, so the top corners are the minus ones."),
    ("B05", 0, "Change the number, and the corner moves. Add forty to x, and every corner moves forty pixels to the right. The whole square slides, because the graphics card fills in the shape between the moved corners."),
    ("B06", 0, "The forty is in the node's own pixels, counted before the node is scaled. Here the right-hand square is scaled to twice its size, so the same forty carries it eighty pixels across the screen."),
    ("B07", 0, "Multiply, and the corners move toward or away from the middle. Here, one and a half times wider and half as tall: the square stretches and flattens. Still only four corners are moving."),
    ("B08", 0, "To treat corners differently, tell them apart. The engine gives each corner an address too, called U V: zero to one across, zero to one down. Top left is zero, zero. Bottom right is one, one."),
    ("B09", 0, "Now scale a move by the address. Add fifty times the vertical address to x. The top corners add nothing, because their address is zero. The bottom corners add fifty. The square leans."),
    ("B10", 0, "Only four corners moved. In between, the card fills the shape in even steps. We measured the left edge: fifty pixels over a hundred twenty-eight rows, on a straight line, to within half a pixel. Remember that straight line."),

    # ── ACT II · More Corners ───────────────────────────────────────────────────────────────────────
    ("B11", 1, "A slide, a squash, a lean: four corners are enough when the whole shape moves as one. A bend is different. Watch what a ripple does to a flag with four corners."),
    ("B12", 1, "A ripple is the sine of the address across, scaled and added to y. On this flag, nothing ripples. The right end drops, and every edge stays straight."),
    ("B13", 1, "Why? Vertex can only move the vertices that exist. Between two corners, the card draws a straight line. A curve needs corners along the way, for vertex to push up and down."),
    ("B14", 1, "So give the shape more vertices. Here are two ways in Godot. A polygon node, where you place the points yourself. Or a mesh node, which draws a mesh: the vertices and triangles that make a shape."),
    ("B15", 1, "A mesh instance two D node draws a mesh. Give it a quad mesh, a flat rectangle you can cut into a grid. Subdivide width and subdivide depth say how many extra cuts to make across and down."),
    ("B16", 1, "Count them. Cut a quad mesh three by three, and each side gets five corner points: twenty-five vertices. Always two more than the cuts, each way. The flag's thirty-one by seven makes thirty-three by nine: two hundred ninety-seven."),
    ("B17", 1, "Same ripple. Same picture. On the left, four vertices: a tilt. On the right, two hundred ninety-seven: a ripple. Nothing in the shader changed, only how many corners it had to work with."),
    ("B18", 1, "More vertices, a smoother wave. Four pieces show every joint. Ten soften them. Thirty-two hide them. A rule of thumb: eight pieces per wave leaves the worst gap near eight percent of the wave's height. Sixteen leaves about two."),
    ("B19", 1, "Cut only where it bends. This ripple runs along the flag, never up and down, so rows of vertices add nothing. Thirty-one cuts across and none down gives sixty-six vertices, and the picture matches, pixel for pixel."),
    ("B20", 1, "A polygon node gives you one vertex per point you place. With points only around the edge, Godot fills the inside with long thin triangles, and the picture twists. A grid of points, joined into cells, fixes it."),

    # ── ACT III · A Waving Flag ─────────────────────────────────────────────────────────────────────
    ("B21", 2, "Now let it travel. Time is seconds on one clock shared by the whole game. Subtract it inside the sine, and the ripple slides to the right as the seconds pass."),
    ("B22", 2, "But a flag is held at one end. Multiply the ripple by the address across. At the left edge the address is zero, so nothing is added, and that edge stays put, like a pole."),
    ("B23", 2, "Three numbers shape the wave: how tall, how many waves fit, how fast. Make each a uniform: a value your game sets from outside the shader, the same for every vertex and pixel. Now the flag has three dials."),
    ("B24", 2, "Raise amplitude, and the waves get taller. Raise frequency, and more waves fit across. Raise speed, and they travel faster. Each one changes only what its name says."),
    ("B25", 2, "Your game can turn the dials while it runs. When the wind picks up, call set shader parameter on the node's material, with the dial's name and a new value. The flag answers at once."),
    ("B26", 2, "Read it as one. Three dials at the top. In vertex, the wave: the address across, minus time, through a sine, scaled by the dials, pinned by the address. Nine lines, one of them moving the flag."),

    # ── ACT IV · Passing Data Forward ───────────────────────────────────────────────────────────────
    ("B27", 3, "The flag moves, but it looks like a flat sheet. Nothing shades the folds. Shading is a job for fragment, the function that colors each pixel the shape covers. But fragment runs later, and it never sees the corners."),
    ("B28", 3, "The way across is a varying. In vertex, you set a value at each corner. In fragment, you read it. The graphics card interpolates it across the shape, and it flows one way: forward."),
    ("B29", 3, "Four colors, one per corner, set in vertex. Fragment only reads them. The result is a smooth blend, and an exact one. Halfway along the top edge, red reads one half, the average of its two corners."),
    ("B30", 3, "Switch the blending off with flat, and each triangle keeps one corner's value. A mesh cut into a grid shows it: the smooth blend breaks into tiles. A rectangle is two triangles, and the blending happens inside each one."),
    ("B31", 3, "The engine does this for you, too. U V is set at the corners and blended, which is why it is a smooth ramp. The color from vertex is passed on the same way, and multiplied by the picture."),
    ("B32", 3, "So light the folds. In vertex, work out how the cloth slopes and pass it as a varying. In fragment, darken the cloth where it slopes away. Now the folds read as folds."),
    ("B33", 3, "There is a shorter way. The color already travels from vertex to fragment, multiplied by the picture. Darken it in vertex, and you need no varying and no fragment function. Same picture, pixel for pixel, with the dials back."),
    ("B34", 3, "One limit. A varying is only as detailed as your corners. Six stripes computed in vertex vanish on four corners, because both ends compute the same number. Computed in fragment, at every pixel, the stripes are there."),

    # ── ACT V · When It Looks Wrong ─────────────────────────────────────────────────────────────────
    ("B35", 4, "Some mistakes compile and still look wrong. First: in two D, a quad mesh draws upside down. Give its size a negative y, and it stands up, matching a sprite beside it."),
    ("B36", 4, "Second: the word vertex changes meaning. In vertex, it is the corner's position in the node's own pixels. In fragment, it is the pixel's position on the screen. Same word, different numbers."),
    ("B37", 4, "Move the node and you see it. Colored from the corner position, the gradient travels with the sprite. Colored from the pixel's screen position, the sprite slides across a gradient that stays where it is."),
    ("B38", 4, "Third: a polygon node only has U V when it has a texture. A texture is an image a shader can read. Without one, the address is zero everywhere, and a wave multiplied by it never starts."),
    ("B39", 4, "Fourth: a vertex shader changes the drawing, not the node. This one draws the sprite two hundred pixels away. The node's rectangle and its collision shape stay exactly where they were. We checked both."),
    ("B40", 4, "Last: when nothing waves, count the vertices. Ask a mesh for its vertex array and print the size: here, two hundred ninety-seven. A polygon has one per point. A plain sprite has four, and four cannot bend."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. A waving flag looks as if thousands of pixels are moving. They are not. "
         "A vertex shader does not change pixels. It moves the corner points of a shape, and the graphics card fills in everything between them.")
BIDEA_TEXT = ("A vertex shader\nchanges pixels.", "changes pixels", "moves corners")

BDEFS = ("Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. "
         "A vertex is a corner point of a shape. A polygon is a shape made of straight edges between points. To interpolate is to blend smoothly between two known values.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Pixel", "one dot of the picture on screen"),
    ("Vertex", "a corner point of a shape"),
    ("Polygon", "a shape made of straight edges between points"),
    ("Interpolate", "blend smoothly between two known values"),
]

BVDT_HEADING = "Vertex Shaders"
BVDT_LINES = [
    "Vertex runs once for each corner and decides where it goes.",
    "A shape can only bend where it has vertices.",
    "Cut a mesh until each wave has eight pieces or more.",
    "A flag is a sine of the address and the time, pinned at one end, with dials.",
    "A varying carries a value from the corners to every pixel.",
    "When it looks wrong, count the vertices, and check what each position is measured from.",
]
BVDT_NARRATION = ("Let's recap with Claude. Vertex runs once for each corner and decides where it goes. A shape can only bend where it has vertices. "
                  "Cut a mesh until each wave has eight pieces or more. A flag is a sine of the address and the time, pinned at one end, with dials. "
                  "A varying carries a value from the corners to every pixel. When it looks wrong, count the vertices, and check what each position is measured from.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a waving banner. Draw it with a MeshInstance two D and a quad mesh cut thirty-one by seven. "
               "In vertex, move the corners up and down with a sine of the address across and the time. Make amplitude, frequency and speed float uniforms, and pin the left edge. "
               "Then tell me how many vertices the mesh has.")
BHTF_CHECKS = ["Check: the left edge never moves while the rest ripples.",
               "Check: the vertex count matches thirty-three by nine."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does the left edge stay still while the rest ripples? "
                  "And does the vertex count match thirty-three by nine?")
BHTF_SEGMENT = "Wave a Banner with Vertices"

CUT_LINE = ("Cut, in this order: the color-shortcut beat (B33), the flat beat (B30), the wind beat (B25), the polygon-needs-a-texture beat (B38) and the "
            "upside-down beat (B35): each repeats a lesson another beat already carries or is a trap rather than the main line. "
            "The four-corner tilt (B12), the pair (B17), the travelling and pinned flag (B21, B22) and the lit flag (B32) stay: they are the proof and the payoff.")

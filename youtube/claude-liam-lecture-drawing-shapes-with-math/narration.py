"""narration.py: every spoken line of "Drawing Shapes with Math". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every picture and number below was
rendered or computed there, see evidence/planning-checks/), and one third-party video course on 2D shaders that is known here only through
the content brief's description in its own words (ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: every Godot picture is a render of a file in lab-shaders/; sweeps and stepped values are moved by a script and
labelled as such; the shapes assume a square and the film says so (B33); the hard edge is stated (B34).
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-drawing-shapes-with-math"
TITLE = "Drawing Shapes with Math"
TITLE_LINES = ["Drawing Shapes", "with Math"]
OPENING_DESCRIPTION = "How a pixel decides if it is inside a shape"
SUMMARY = ("Learn how a shader draws a circle, a ring and a cross using only math, "
           "then build a crosshair you can reshape with sliders.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · DRAWING SHAPES"
TAGS = ["Godot", "Shaders", "GPU", "Shapes", "Distance", "Mask", "Crosshair", "Fragment shader", "Uniform", "Game development",
        "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Inside or Outside"),
    ("II", "Rings and Cutouts"),
    ("III", "Lines and Crosses"),
    ("IV", "Make It a Tool"),
    ("V", "The Crosshair"),
]

BODY = [
    # ── ACT I · inside or outside: a circle is a question each pixel answers ──────────────────────────────
    ("B01", 0, "Our goal: a crosshair with six dials, drawn by one shader on a Color Rect. No picture file sits behind it. Every "
               "piece is a rule, and each dial changes one rule. We start with the smallest rule."),
    ("B02", 0, "Here is the catch. The fragment function runs once for every pixel, and each run is handed its own pixel's "
               "address. So it does not draw a circle. It answers a question about itself: am I inside the circle?"),
    ("B03", 0, "To answer, a pixel needs two facts: its own address, U V, and where the center is. The center is at zero point "
               "five, zero point five. Our pixel sits at zero point six two, zero point six six."),
    ("B04", 0, "Work out its distance by hand. It is zero point one two to the right of the center, and zero point one six "
               "below. Square both, add them, take the square root: exactly zero point two."),
    ("B05", 0, "In a shader, that whole calculation is one function: distance. Give it the pixel's address and the center. Feed "
               "the answer into the color's alpha, how visible it is, and the middle fades out while the edges fill in."),
    ("B06", 0, "Pick a radius, say zero point three. A pixel is inside when its distance is no more than the radius. Along the "
               "middle row, the distance dips to zero at the center. Everything under the line is inside."),
    ("B07", 0, "To turn that into a number, use step. Give it an edge and a value. It returns zero while the value is below the "
               "edge, and one once the value reaches it. A switch that flips at the edge."),
    ("B08", 0, "Mind the order. With the radius first, step asks: has the distance reached the radius? Inside the circle, no: "
               "zero. Outside, yes: one. Swap them, and step asks: has the radius reached the distance? Inside, yes: one. That's "
               "our circle."),
    ("B09", 0, "Put it together. Our pixel: distance zero point two, radius zero point three, so step says one: inside. A pixel "
               "at distance zero point four says zero: outside. Those ones and zeros are a mask: how much to show."),
    ("B10", 0, "Make the radius a uniform and the circle gets a dial. The shader reads it but never changes it. Turn the dial "
               "and the circle grows. What follows the colon asks the editor for a slider."),

    # ── ACT II · rings and cutouts: masks add and subtract, and the screen hides a mistake ────────────────
    ("B11", 1, "A ring is a big circle with a smaller circle taken out. Draw the big mask, draw the small mask, and subtract. "
               "Where both say one, one minus one leaves zero. Only the strip between them survives."),
    ("B12", 1, "In code, that is two steps and a minus. The outer circle has radius zero point three five, the inner one zero "
               "point three. Their difference is a ring, five hundredths wide."),
    ("B13", 1, "Check three pixels by hand. At distance zero point two, both circles say one, so the ring is zero. At zero point "
               "three three, only the outer circle says one. At zero point four five, neither does."),
    ("B14", 1, "Now overlap two circles and add their masks. Where they overlap, both say one, so the sum is two. In a default "
               "project the screen cannot tell: an alpha of two looks exactly like one. The mistake hides."),
    ("B15", 1, "Cut a small hole in the middle of the overlap by subtracting a third mask. The hole should appear. It does not. "
               "One plus one minus one is still one, so the hole is filled."),
    ("B16", 1, "The same pixels, in numbers. Inside one circle: one. In the overlap: two. In the hole: two minus one, which is "
               "one, when we wanted zero. The hidden two ate the cutout."),
    ("B17", 1, "The fix is to cap the sum at one with min before subtracting. Min of two and one is one, so the overlap counts "
               "once, and the hole takes it down to zero. Now the hole appears."),
    ("B18", 1, "Subtraction has a mirror-image bug. Cut a bite from the disc, reaching past its edge. There the disc says zero, "
               "the bite says one: minus one. Add a spot there: minus one plus one is zero, so it never shows."),
    ("B19", 1, "The fix is max, min's mirror: it keeps the larger number. Max of minus one and zero is zero, and then the spot "
               "adds one. The rule for both bugs: after adding, cap at one; after subtracting, floor at zero."),

    # ── ACT III · lines and crosses: distance to a line, abs, max, multiply ──────────────────────────────
    ("B20", 2, "A circle measures distance to a point. A band measures it to a line. Take the vertical line down the middle. "
               "Subtract a half from the pixel's horizontal address, and you get how far right of the line it sits."),
    ("B21", 2, "On the left that number is negative. The function abs drops the minus sign: it folds the left onto the right, so "
               "one formula measures both sides."),
    ("B22", 2, "Compare that distance with half the band's width, and step gives a vertical band. Same recipe as the circle: "
               "measure, compare, get one or zero."),
    ("B23", 2, "A cross is every pixel in either band. Take the larger of the two masks, with max: for ones and zeros it does "
               "what add-then-cap did, in one step. Adding alone would put a two in the middle."),
    ("B24", 2, "So there are three ways to combine masks. For either, take the max. For both, multiply. For a cutout, subtract, "
               "then take the max with zero. Max and multiply stay between zero and one. Adding and subtracting can leave it."),
    ("B25", 2, "To make an arm, ask for two things at once: not too far along the line, and close to it. Two masks, multiplied. "
               "Both must be one, so you get a rectangle."),
    ("B26", 2, "An arm should start away from the center. Add a third condition: at least this far out. Far enough, not too far, "
               "near the line. Because of abs, one formula draws the top arm and the bottom."),
    ("B27", 2, "Swap the two addresses for the horizontal pair, then take the max of the two pairs. Four arms around an empty "
               "middle. Measure, compare, combine: that is every shape so far."),

    # ── ACT IV · make it a tool: dials, functions that return masks, two honest limits ───────────────────
    ("B28", 3, "Every number here is baked in: the gap, the end, the width. A tool needs dials. Turn each number into a uniform "
               "with a range, and the editor gives you a slider for each one."),
    ("B29", 3, "A habit worth having: every slider runs from zero to one, whatever it controls. Inside the shader, multiply by "
               "the biggest value that makes sense. Then every dial behaves the same way, and you never memorize a range."),
    ("B30", 3, "Next, give each shape a name. A function can return a mask. This one takes an address, a radius and a width, and "
               "returns the ring. The fragment function only calls it."),
    ("B31", 3, "One catch. Built-in values like U V work in the engine's own functions, but not in yours. A few, like time, are "
               "global and work anywhere. So fragment hands U V in as an input, under a name you choose."),
    ("B32", 3, "Use U V directly inside your own function and Godot refuses to compile. The message names the word it does not "
               "recognize: unknown identifier, U V. The version from a moment ago passes it in, and compiles."),
    ("B33", 3, "One honest limit: these shapes assume a square. On a wide rectangle, U V still runs from zero to one both ways, "
               "so a circle becomes an oval. We measured it: three hundred eighty-four pixels wide, two hundred sixteen tall."),
    ("B34", 3, "And the edge is hard. Every pixel is fully in or fully out, so the circle's edge is a staircase of pixels. The "
               "whole picture has exactly two colors. A softer edge needs a different tool."),

    # ── ACT V · the crosshair: a dot, a ring and four arms, joined with max ─────────────────────────────
    ("B35", 4, "Now the crosshair. Six uniforms: dot size, ring distance, ring width, arm gap, arm length and arm width. Each "
               "runs from zero to one, with a default that draws a sensible crosshair."),
    ("B36", 4, "Three small functions return the three masks. The first two: the dot is the circle from before, and the ring is "
               "the outer circle minus the inner. Same code, new names."),
    ("B37", 4, "The arms function is the four-arm rule from before. Gap, length and width come in; gap plus length is the end. "
               "Abs folds each side, and max joins the vertical pair with the horizontal pair."),
    ("B38", 4, "The fragment function scales each slider to a real size, then joins the three masks with max. Where the ring and "
               "arms cross, nothing doubles. The mask goes straight into the alpha."),
    ("B39", 4, "Here it is over two different backdrops. Wherever the mask is zero, none of the shape is drawn, so whatever is "
               "behind shows through. That is what a mask is for."),
    ("B40", 4, "Now the dials, one at a time. Dot size grows the dot. Ring distance pushes the ring outward while the arms stay "
               "put. Each dial changes one number in one rule."),
    ("B41", 4, "Ring width thickens the ring from nothing to a band. Arm length stretches the arms until they cross the ring and "
               "run on. Nothing doubles where they cross."),
    ("B42", 4, "Arm width thickens the arms. Arm gap opens the middle, from arms that run into the dot to arms that start far "
               "from it."),
    ("B43", 4, "Predict first. Arm length at zero: what is left? The dot and the ring. Ring width at zero? The dot and the arms. "
               "Push any dial to either end and nothing breaks, because every piece is a mask."),
    ("B44", 4, "In the Godot editor, the six uniforms appear as six sliders in the Inspector. A designer can tune the crosshair "
               "without opening the code."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. To draw a circle on screen, you might reach for a circle image. A shader does not need one. "
         "It asks every pixel a single question: are you inside the shape? All the answers together are the shape.")
BIDEA_TEXT = ("To draw a circle you need\na circle image.", "a circle image", "a question for each pixel")

BDEFS = ("Six terms. A function is a named block of code you can call. A shader is a small program the graphics card runs to decide how "
         "something is drawn. Its fragment function runs once for each pixel and sets its color. U V is a pixel's address, from zero to one "
         "across and down. A vector is a bundle of numbers. A uniform is a value your game sets from outside.")
BDEFS_TERMS = [
    ("Function", "a named block of code you can call"),
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("fragment()", "runs once for each pixel the shape covers; sets its color"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Vector", "a bundle of two to four numbers"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
]

BVDT_HEADING = "Drawing Shapes with Math"
BVDT_LINES = [
    "A shape is a question each pixel answers: inside is one, outside is zero.",
    "Distance from a point, compared with a radius by step, draws a circle.",
    "Subtract masks for a ring. After adding, cap at one; after subtracting, floor at zero.",
    "Distance from a line, folded with abs, draws a band; max joins masks and multiply intersects them.",
    "Put each shape in a function, and give every slider a range of zero to one.",
    "A crosshair is a dot, a ring and four arms, joined with max.",
]
BVDT_NARRATION = ("Let's recap with Claude. " + " ".join(BVDT_LINES))

BHTF_PROMPT = ("Write a Godot canvas item shader for a square Color Rect that draws a ring. Use distance from the center and step. "
               "Two float uniforms, radius and thickness, each with a hint range from zero to one, scaled inside the shader so the biggest "
               "ring still fits the square. Everything outside the ring must be transparent. Then point me to the line that decides "
               "inside or outside.")
BHTF_CHECKS = ["Check: with thickness at zero, nothing is drawn.",
               "Check: the ring is round on a square, and oval on a wide Color Rect."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. With thickness at zero, is anything drawn? "
                  "And is the ring round on a square Color Rect, and oval on a wide one?")
BHTF_SEGMENT = "Draw a Ring with Two Sliders"

CUT_LINE = ("Cut, in this order: the ring-in-numbers table (B13), the hard-edge beat (B34), the second numbers table (B16), then one of the "
            "three dial-sweep beats (B42: arm width and arm gap move into B41). The min and max act shrinks to the sum bug and its fix "
            "(B14, B15, B17) plus one beat for the negative case (B18 and B19 merge). The circle by hand (B04, B08), the cross by max (B23), "
            "and the crosshair build (B35 to B38) stay: they are the idea and the payoff.")

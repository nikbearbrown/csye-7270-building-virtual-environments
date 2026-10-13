"""narration.py: every spoken line of "The Shader Math Toolkit". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (built-in functions, shading language, canvas item reference; read 2026-10-13), the installed Godot 4.7.2 on
Bear's Mac (Apple M4 Pro, Forward+: every claim below was probed in evidence/planning-checks/), and a third-party long course on 2D shaders in Godot
whose order of ideas is followed (nothing copied; see SOURCES.md).
Honesty rules for this film: a value read from a render says which renderer; the film never claims a speed; behaviour the docs call "undefined"
is named as undefined, never promised.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures
and the real identifiers (smoothstep, fract, pow, F mod and F pos mod are fmod and fposmod).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-shader-math-toolkit"
TITLE = "The Shader Math Toolkit"
TITLE_LINES = ["The Shader Math", "Toolkit"]
OPENING_DESCRIPTION = "A dozen small functions behind shader effects"
SUMMARY = "Learn a dozen small functions that shape what a shader draws, then use three of them to build a soft ring."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · SHADER MATH"
TAGS = ["Godot", "Shaders", "Shader math", "smoothstep", "mix", "fract", "distance", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation (built-in functions); Godot 4.7.2 runs on Apple M4 Pro, Forward+ (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Ramps and Plots"),
    ("II", "Cut and Blend"),
    ("III", "Repeat and Fold"),
    ("IV", "Distance and Curves"),
    ("V", "Build a Ring"),
]

BODY = [
    # ── ACT I · ramps and plots ─────────────────────────────────────────────────────────────────────
    ("B01", 0, "This ring is not an image. Three small functions draw it: one measures distance, one softens an edge, one blends two colors. By the end, you will be able to read every line of it."),
    ("B02", 0, "Start with a ramp: a smooth run of values from zero up to one. The simplest ramp is a pixel's address across the shape: zero at the left edge, one at the right. In code, that is U V dot x."),
    ("B03", 0, "A shader can show a number as gray. Fragment runs once for each pixel the shape covers, and sets its color. Here the color is three copies of the ramp: zero is black, one is white."),
    ("B04", 0, "From here on, every function gets the same picture. The input runs along the bottom, the output up the side. A dot travels the line, and the strip below shows the output as gray. A function that changes nothing is a straight diagonal."),
    ("B05", 0, "Bend the line and the strip follows. Here the function is one minus x. The line runs downhill, so the strip runs from white to black. Read the line, and you can predict the picture before you see it."),
    ("B06", 0, "About a dozen functions come in three families. Cut and blend: step, smooth step, mix, clamp. Repeat and fold: abs, fract, floor, mod. Distance and curves: length, normalize, distance, power, sine. Then we use three of them to build a ring."),

    # ── ACT II · cut and blend ──────────────────────────────────────────────────────────────────────
    ("B07", 1, "Step is a switch. Give it an edge and a ramp. Where the ramp is below the edge, the answer is zero. At the edge or above, it is one. The plot is a single jump."),
    ("B08", 1, "In a shader, the edge goes first, then the ramp. Here the edge is a uniform, a dial your game can turn from outside. Slide it, and the hard split slides with it."),
    ("B09", 1, "Clamp pins a number inside a range. Below the low end, you get the low end. Above the high end, you get the high end. In between, nothing changes. It is max first, then min."),
    ("B10", 1, "Smooth step is a switch that eases in and out. Give it two edges and a ramp. Below the first edge, zero. Above the second, one. Between them, a smooth S with no corners."),
    ("B11", 1, "It is not a straight line, and one number shows it. Say the edges are zero and ten, and the input is one. A straight line would give point one. The S gives point zero two eight, because it starts out slowly."),
    ("B12", 1, "The docs spell out the formula. Squeeze the input between the edges into zero to one, call that t, and return three t squared minus two t cubed. They also warn that a first edge at or above the second gives undefined results."),
    ("B13", 1, "In code, the edges are the first two numbers. Here they sit either side of one half, and a dial sets how far. Pull them together and the S tightens toward a step."),
    ("B14", 1, "Mix slides between two values. Give it a start, an end, and a weight. Weight zero returns the start, one returns the end, one half lands halfway. It does not pin the weight: a weight of two overshoots the end, so clamp it first."),
    ("B15", 1, "A color is a vector, so mix blends all of its numbers at once. Here it blends teal into gold, with the ramp as the weight. The function that slid one number now slides a whole color."),
    ("B16", 1, "The weight can be any reshaped ramp. The plain ramp gives a smooth blend. Step gives a hard cut. Smooth step gives a soft one. A weight like this, a number from zero to one for each pixel, is called a mask."),

    # ── ACT III · repeat and fold ───────────────────────────────────────────────────────────────────
    ("B17", 2, "A ramp can be stretched and shifted. Multiply by two and subtract one, and it runs from minus one to one, with zero in the middle. Now negative numbers are part of the picture."),
    ("B18", 2, "Absolute value, written abs, drops the minus sign. Fold the ramp at zero and the left half lands on top of the right half. The plot is a V, and the strip is a mirror: bright, dark, bright."),
    ("B19", 2, "Fract keeps only what comes after the decimal point. Two point seven five becomes point seven five. Multiply the ramp by four first, and fract gives four ramps in a row, each starting over at zero."),
    ("B20", 2, "Fract is one line in a shader. The number you multiply by is how many copies you get. Turn that dial from one up to six, and the picture fills with repeating ramps."),
    ("B21", 2, "Floor keeps the whole part instead. It rounds down to the whole number below. Multiply the ramp by four and take floor: zero, one, two, three, four flat steps with a jump between each."),
    ("B22", 2, "Every number splits in two. Floor is the whole part, fract is the leftover. Two point seven five is two plus point seven five. So floor says which section you are in, and fract says where inside it."),
    ("B23", 2, "Combine fract with step. Fract makes the ramp restart, and step cuts each copy in half. Dark, light, dark, light: stripes, from two functions and no image. Change the multiplier and you change the count."),
    ("B24", 2, "Mod gives the remainder after dividing: x minus y times floor of x over y. With y equal to one, it is exactly fract. With y of point two five, the ramp repeats every quarter."),
    ("B25", 2, "One trap. In a shader, mod of minus point two five and one is point seven five: it follows floor. G D script's F mod keeps the sign and says minus point two five. F pos mod matches the shader. Check which one you wrote."),

    # ── ACT IV · distance and curves ────────────────────────────────────────────────────────────────
    ("B26", 3, "Now two numbers at once. A vector bundles them, and length says how long that bundle is, measured from zero. Three across and four down has length five: the square root of nine plus sixteen."),
    ("B27", 3, "Normalize keeps a vector's direction and sets its length to one. Take the arrow three across, four down. Normalize it and you get point six across, point eight down: same direction, length one."),
    ("B28", 3, "Distance is the length of the gap between two points. Pick the middle of the shape, and ask every pixel how far it is from there. Pixels near the middle get small numbers, pixels far away get big ones."),
    ("B29", 3, "That is one line of shader: the distance from the pixel's address to the middle. The result is a ramp that grows outward in every direction. The middle of each edge is half away; the corners are about point seven."),
    ("B30", 3, "A warning before we draw circles: use a square shape. On a wide one, the circle turns into an oval. The address always runs from zero to one on both sides, whatever the proportions, so the circle stretches with the shape."),
    ("B31", 3, "Distance is another ramp, so everything so far applies. One minus a smooth step of the distance gives a soft spot of light. It is brightest in the middle and fades to nothing at the edge."),
    ("B32", 3, "Power, written pow in code, raises each value to a power. On a ramp from zero to one, a power above one pulls the curve down, so only the far end stays bright. Below one, it pushes the curve up. Exactly one changes nothing."),
    ("B33", 3, "In code, pow takes the ramp and a power. Turn the power up and the bright part squeezes toward the right edge, like a highlight tightening. Keep the first number at zero or above; the docs call a negative one undefined."),
    ("B34", 3, "One more curve. Sine repeats smoothly, rolling between minus one and one. Half of sine, plus a half, squeezes it into zero to one. Think of it as the smooth cousin of fract."),

    # ── ACT V · build a ring ────────────────────────────────────────────────────────────────────────
    ("B35", 4, "Time to build. Take the distance to the middle and cut it with step at point three. Closer than that is zero, farther is one. The result is a circle: dark inside, light outside."),
    ("B36", 4, "Swap the two inputs and the circle flips: one inside, zero outside. The edge always comes first, so this reads: is the radius at least the distance?"),
    ("B37", 4, "For a ring, cut twice and subtract. Step at point three is one from there outward. Step at point three eight is one from there outward. The first minus the second is one only in between: a pulse."),
    ("B38", 4, "In code, that is step minus step. Here is the ring: a mask that is one on the ring and zero everywhere else. The edges are hard, since each pixel is either all in or all out."),
    ("B39", 4, "Now color it with mix, using the ring as the weight. Where the mask is zero, you get cream. Where it is one, you get teal. The mask decides how much of each."),
    ("B40", 4, "Swap each step for a smooth step. Each edge now has a width, so the ring fades in and fades out instead of snapping. The same ring, with soft edges."),
    ("B41", 4, "Here is the finished shader. Distance makes the ramp, smooth step shapes it twice, mix paints it. The radius is a uniform, so your game can turn it, and the ring grows."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. People think shaders need advanced math. They need about a dozen small functions, "
         "and each one reshapes a smooth run of numbers. Learn what each does, and you can predict what a shader will draw.")
BIDEA_TEXT = ("Shaders need advanced math.", "advanced math", "a dozen small functions")

BDEFS = ("Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. "
         "U V is a point's address on a shape: zero to one across, zero to one down. A function takes numbers in and gives one number out. "
         "And a vector is a bundle of two to four numbers.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Pixel", "one dot of the picture on screen"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Function", "a rule: numbers go in, one number comes out"),
    ("Vector", "a bundle of two to four numbers"),
]

BVDT_HEADING = "The Shader Math Toolkit"
BVDT_LINES = [
    "A ramp is a smooth run from zero to one, and every function reshapes it.",
    "step cuts, smoothstep cuts softly, mix blends, clamp pins.",
    "abs folds, fract repeats, floor counts, mod repeats at any length.",
    "length and distance measure, normalize keeps a direction, pow bends a curve.",
    "Distance, smoothstep and mix together draw a ring.",
    "Read the line of a function and you can predict the picture.",
]
BVDT_NARRATION = ("Let's recap with Claude. A ramp is a smooth run from zero to one, and every function reshapes it. "
                  "Step cuts, smooth step cuts softly, mix blends, clamp pins. "
                  "Abs folds, fract repeats, floor counts, mod repeats at any length. "
                  "Length and distance measure, normalize keeps a direction, power bends a curve. "
                  "Distance, smooth step and mix together draw a ring. "
                  "Read the line of a function and you can predict the picture.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a square Color Rect: a soft teal ring around the center, built from distance, smoothstep and mix. "
               "Give it one float uniform called radius, limited to a range that keeps the ring inside the square. "
               "Then tell me which line does which job.")
BHTF_CHECKS = ["Check: the ring is round and centered in the square.",
               "Check: the radius dial moves the ring in and out, with soft edges."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Is the ring round and centered? "
                  "And does the radius dial move the ring in and out, with soft edges?")
BHTF_SEGMENT = "Draw a Soft Ring"

CUT_LINE = ("Cut, in this order: the toolkit map (B06), the sine beat (B34), the normalize beat (B27), the soft-spot beat (B31), the smooth step "
            "docs beat (B12) and the floor-only beat (B21). Each repeats or previews an idea carried elsewhere. The plot-reading pair (B04, B05), the "
            "smooth step correction (B11), the whole-and-leftover split (B22), the mod trap (B25) and the whole ring build (Act V) stay: they are "
            "the method, the two corrections and the payoff. A cut beat also leaves its name in the recap line (BVDT_LINES[3] for normalize and sine), so trim that line and its spoken twin too.")

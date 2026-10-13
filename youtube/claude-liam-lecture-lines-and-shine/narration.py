"""narration.py: every spoken line of "Lines and Shine". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and one third-party video on drawing a line and a shine in a shader (ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input is labelled; widths are given as a percent of
the card because pixels depend on the capture size; the card is a square, and the film says what changes on a wide shape.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-lines-and-shine"
TITLE = "Lines and Shine"
TITLE_LINES = ["Lines and Shine"]
OPENING_DESCRIPTION = "How to draw a line at any angle and make it shine"
SUMMARY = "Learn how a shader draws a line at any angle from one rule, and how to slide that line across a sprite as a shine."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · LINES AND SHINE"
TAGS = ["Godot", "Shaders", "Shine effect", "Line", "Slope", "Distance", "Sprite", "Fragment shader", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "A Line as a Test"),
    ("II", "Slope from an Angle"),
    ("III", "Distance to the Line"),
    ("IV", "Shine"),
    ("V", "The Angle-Safe Way"),
]

BODY = [
    # ── ACT I · a line as a test ────────────────────────────────────────────────────────────────────
    ("B01", 0, "This glint is where we are heading. No stripe is drawn anywhere. Every pixel measures how far it sits from a line, and the pixels that are close light up. By the end, you will write that rule yourself."),
    ("B02", 0, "From school: a line is y equals m x plus b. The m is the slope, the climb for each step across. The b is its starting height. Make the line pass through the middle, and b is zero."),
    ("B03", 0, "A pixel's address, U V, has its zero at the top left corner. Double it, subtract one, and the zero lands in the middle. The address now runs from minus one to one, both ways."),
    ("B04", 0, "One more change. Godot counts the address downward, so flip the second number. Now up is up, and a positive slope climbs to the right, the way you learned it."),
    ("B05", 0, "Now turn the line into a question. Move everything to one side: y minus m times x. On the line, the answer is exactly zero. Anywhere else, it is not, and any pixel can check."),
    ("B06", 0, "Try a slope of one half. A point on the line gives zero. Straight above it, plus point six. Straight below, minus point six. The sign tells you the side. The size is the gap, straight up or down."),
    ("B07", 0, "Slide a point along a parallel line, and the answer never changes. Plus point six stays plus point six. So the test gives one number to a whole line of pixels, parallel to ours."),
    ("B08", 0, "As a shader, fragment runs once for every pixel of the card. Red rises where the answer is positive, so that side looks warm. Blue rises where it is negative, so it looks cool. Pixels on the line stay grey."),
    ("B09", 0, "Change the slope, and the whole card pivots around the middle. Slope zero is flat. Slope one climbs at a diagonal. Same rule, one number different."),

    # ── ACT II · slope from an angle ────────────────────────────────────────────────────────────────
    ("B10", 1, "We think in angles, not slopes, and the tangent connects them. Go one step across, along a line turned by the angle. The height you climb is the tangent, and that height is the slope."),
    ("B11", 1, "In the shader, the slope is the tangent of the angle. Godot's tangent works in radians, where a full turn is about six point two eight, so the radians function converts our degrees first."),
    ("B12", 1, "What if we skip that conversion? Godot reads thirty degrees as thirty radians. The slope becomes minus six point four: a steep line, leaning the wrong way. If an angle looks wrong, check the radians first."),
    ("B13", 1, "Watch the slope as the angle grows. At forty-five degrees, it is one. At seventy-five, three point seven. At eighty-nine, fifty-seven. Toward ninety it has no limit: a vertical line climbs with no step across."),
    ("B14", 1, "Right at ninety, the slope flips sign. On this Mac, Godot's tangent there is near minus twenty-three million, and warm and cool trade sides in one frame. A slope has a seam at vertical. We fix that at the end."),

    # ── ACT III · distance to the line ──────────────────────────────────────────────────────────────
    ("B15", 2, "A line has no thickness, so we cannot see it. Keep every pixel whose answer is near zero, and you get a band around the line. Two tools do that: absolute value drops the sign, and step is a switch."),
    ("B16", 2, "Take the absolute value of the test and call it d, for distance. Then step: distance first, thickness second. It answers one when the thickness has reached the distance, so the pixel is inside the band. Otherwise, zero."),
    ("B17", 2, "Tilt the line. Does the band keep its thickness? Watch. At zero degrees the band is ten percent of the card wide. At forty-five, seven percent. At seventy-five, under three. It thins out as the line steepens."),
    ("B18", 2, "Why? The test measures straight up from the line. Distance means the shortest way, at a right angle. Tilt the line, and the shortest way gets shorter than straight up. The steeper the line, the bigger the difference."),
    ("B19", 2, "The fix is one right triangle. Along the line, one step across climbs m, so that step is the square root of one plus m squared long. Divide the test by that, and you have the shortest distance."),
    ("B20", 2, "In code: absolute value of the test, divided by the square root of one plus m times m. Thickness is now a real distance. Point one makes the band a tenth of the card wide."),
    ("B21", 2, "Tilt it again, now beside the old version. Fifteen degrees, forty-five, seventy-five, even eighty-five. The new band stays ten percent of the card wide. The old one fades away."),

    # ── ACT IV · shine ──────────────────────────────────────────────────────────────────────────────
    ("B22", 3, "To slide the line, add an offset to the distance, before the absolute value. The distance is true, so the line moves exactly that far, straight across, at any angle. Offset point five is a quarter of the card."),
    ("B23", 3, "You may see another way: subtract a center point before testing. How far that slides the line depends on the angle. Shift a flat line sideways, and nothing moves. The offset slides it straight across, whatever the angle."),
    ("B24", 3, "Now the sprite. Where the band is, blend the sprite's color toward white. Mix takes two colors and a weight: zero gives the first, one gives the second. Here, the weight is the band."),
    ("B25", 3, "But watch the empty corners. The stripe crosses them too. Mix blended the alpha as well, so transparent pixels turned white and solid. The highlight has leaked off the sprite."),
    ("B26", 3, "The fix is one multiplication. Alpha is zero where the sprite is empty and one where it is solid. Multiply the band by alpha, and the highlight lives only where the sprite does."),
    ("B27", 3, "To make it move, give the offset a clock. Time is one clock for the whole game. Time times a half, keeping only the fractional part, ramps from zero to one every two seconds. Mix stretches that across the sprite."),
    ("B28", 3, "To start a shine when something happens, let your game drive the offset. Set the start, then tween to the end; a tween glides a value over time. Skip that first line, and the tween has nothing to start from."),
    ("B29", 3, "That is the whole shine. Center the address. Turn the angle into a slope. Divide for true distance, and slide it by the offset. Step into a band, weighted by alpha. Mix in white."),
    ("B30", 3, "One limit. U V runs zero to one even on a wide shape, so the line gets stretched. On sixteen by nine, forty-five degrees comes out near twenty-nine. Scale the across part by width over height first."),

    # ── ACT V · the angle-safe way ──────────────────────────────────────────────────────────────────
    ("B31", 4, "Slope has a seam at vertical. So describe the line by its direction instead: a step of length one, turned by the angle. Across is the cosine of the angle. Up is the sine."),
    ("B32", 4, "Turn that arrow a quarter turn and it points straight away from the line: the normal. Dot multiplies across by across and up by up, then adds. Dot a pixel's address with the normal, and you get its signed distance."),
    ("B33", 4, "It is the same distance in disguise. In our triangle, the cosine is one over that square root, so dividing by it is multiplying by the cosine. What is left is exactly p dot n."),
    ("B34", 4, "In code, the normal is minus sine, cosine of the angle, and the distance is the absolute value of p dot n. No tangent, no divide. At thirty, sixty and eighty-nine degrees, it matches the slope version pixel for pixel."),
    ("B35", 4, "And it keeps going through ninety. The slope version swaps warm and cool. The direction version never does, because the normal turns smoothly. Anything that cares which side it is on needs that."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people think a line needs two points, one at each end. A shader has no pen. "
         "It gets one rule, and every pixel asks it: am I on the line?")
BIDEA_TEXT = ("A line needs two points.", "two points", "one rule")

BDEFS = ("Five terms. A pixel is one dot of the picture. U V is a pixel's address on the shape: zero to one across, zero to one down. "
         "A uniform is a value your game sets, the same for every pixel. Slope is how steeply a line rises. Alpha is how visible a pixel is.")
BDEFS_TERMS = [
    ("Pixel", "one dot of the picture on screen"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
    ("Slope", "how steeply a line rises: up divided by across"),
    ("Alpha", "how visible a pixel is: 0 invisible, 1 solid"),
]

BVDT_HEADING = "Lines and Shine"
BVDT_LINES = [
    "A line is a test: y minus m times x is zero on it, positive on one side, negative on the other.",
    "The slope is the tangent of the angle, and it blows up at vertical.",
    "Divide the test by the square root of one plus m squared and it becomes the true distance.",
    "A step makes the band, an offset slides it, and alpha keeps the shine on the sprite.",
    "A direction and a dot give the same distance, with no seam at vertical.",
    "A line is one rule, and a shine is that rule, slid.",
]
BVDT_NARRATION = ("Let's recap with Claude. A line is a test: y minus m times x is zero on it, positive on one side, negative on the other. "
                  "The slope is the tangent of the angle, and it blows up at vertical. "
                  "Divide the test by the square root of one plus m squared and it becomes the true distance. "
                  "A step makes the band, an offset slides it, and alpha keeps the shine on the sprite. "
                  "A direction and a dot give the same distance, with no seam at vertical. "
                  "A line is one rule, and a shine is that rule, slid.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a sprite. Uniforms: angle in degrees, thickness, offset. Center the address and flip it so up is up. "
               "Draw a white band along a line through the middle at that angle, slid sideways by the offset, the same thickness at every angle, "
               "only on visible pixels. Finally, point me to the distance line.")
BHTF_CHECKS = ["Check: at forty-five degrees the band climbs to the right.",
               "Check: the band is as thick at eighty degrees as at ten."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. At forty-five degrees, does the band climb to the right? "
                  "And is it as thick at eighty degrees as at ten?")
BHTF_SEGMENT = "Make a Band Slide Across a Sprite"

CUT_LINE = ("Cut, in this order: Act V (B31 to B35), and with it the last sentence of B14, which promises it; then the center-shift beat (B23); "
            "then fold B16 and B17 into one beat (the band, then the tilt). The wide-shape limit (B30) stays unless the film is far over: "
            "it is the honest edge of the whole method. The shine itself (B01, B22, B24 to B29) never goes.")

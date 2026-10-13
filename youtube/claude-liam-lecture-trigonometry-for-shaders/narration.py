"""narration.py: every spoken line of "Trigonometry for Shaders". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party course chapter and short intro video on the same ideas (followed for order of ideas only,
nothing copied; see SOURCES.md).
Honesty rules for this film: a drawn picture says it is a drawing; every Godot picture is a Shader Lab render of a file in lab-shaders/;
measured numbers say what machine and renderer; the film never claims a real-time frame rate.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"pi" is written lowercase on purpose (the voice dictionary reads lowercase pi as "pie" and all-caps PI as the letters P, I);
"tau" is lowercase so it is read as a word. Arc tangent is spoken as "arc tangent", never the identifier.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-trigonometry-for-shaders"
TITLE = "Trigonometry for Shaders"
TITLE_LINES = ["Trigonometry", "for Shaders"]
OPENING_DESCRIPTION = "Turn an angle into a position, and back again"
SUMMARY = "Learn what sine and cosine really do, then use them to send a moon around a planet and reveal a picture like a clock hand."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · TRIGONOMETRY"
TAGS = ["Godot", "Shaders", "Trigonometry", "Sine and cosine", "Radians", "Arc tangent", "Orbit", "Game development", "Fragment shader", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "One Angle, Two Numbers"),
    ("II", "Angle In, Position Out"),
    ("III", "An Orbit"),
    ("IV", "An Orbit Around an Orbit"),
    ("V", "Angle from a Position"),
]

BODY = [
    # ── ACT I · one angle, two numbers (the triangle) ────────────────────────────────────────────────
    ("B01", 0, "A moon circles a planet, and a meteor circles the moon. Nobody animated it by hand. In the shader, an angle goes in, and two numbers come out that say where the moon is. Those numbers come from a triangle."),
    ("B02", 0, "Start with a triangle that has a right angle in one corner. Its longest side is the hypotenuse. Now pick another corner. The side across from it is the opposite side. The side touching it is the adjacent side."),
    ("B03", 0, "Here is the useful part. Fix the angle, and the ratio of any two sides stays fixed, whatever the size. At thirty degrees, the opposite side is always half the hypotenuse. At fifty, about point seven seven of it."),
    ("B04", 0, "Those ratios have names. Opposite over hypotenuse is the sine. Adjacent over hypotenuse is the cosine. Opposite over adjacent is the tangent. The memory trick is S O H, C A H, T O A."),
    ("B05", 0, "So sine and cosine are lookups. Hand one an angle, and it hands back a ratio. Sine of thirty degrees is one half. Cosine of thirty degrees is about point eight seven. An angle goes in, a number comes out."),

    # ── ACT II · angle in, position out (the circle, radians, the wave) ──────────────────────────────
    ("B06", 1, "Now put that triangle inside a circle. Walk out from the middle at your angle until you reach the circle. The triangle's two short sides say where you stand: so far across, so far up."),
    ("B07", 1, "Make the radius one and you have the unit circle. The hypotenuse is one, so dividing by one changes nothing. The opposite side is the sine itself, the adjacent side the cosine itself. The point sits at cosine across, sine up."),
    ("B08", 1, "Godot's own manual says the same. Vector two has a function, from angle, that builds a point from an angle. The manual calls it equivalent to cosine of the angle, sine of the angle. The engine knows the recipe."),
    ("B09", 1, "Want a bigger circle? Multiply by the radius. Want it somewhere else? Add the center. So center plus radius times cosine and sine puts a point on a circle of any size, anywhere."),
    ("B10", 1, "Try one by hand. Radius point six, angle thirty degrees. The first number is point six times cosine, about point five two. The second is point six times sine, exactly point three. Hold on to those two numbers."),
    ("B11", 1, "One catch. Shaders measure angles in radians, not degrees. Lay one radius along the edge of the circle, and the angle it covers is a radian. A full turn takes a little over six of them: about six point two eight."),
    ("B12", 1, "Godot names the big ones. Pi is half a turn. Tau is a full turn, which is two pi. And the function radians converts degrees, so forty-five degrees comes out as pi over four."),
    ("B13", 1, "Skip the conversion and the shader still compiles. That is the trap. Thirty radians is almost five full turns, so sine of thirty comes out near minus one. Convert first, and sine of thirty degrees is one half again."),
    ("B14", 1, "Why is sine a wave? Plot the point's height against its angle as it goes round. The height climbs to one, falls through zero to minus one, and comes home. That curve is the sine wave."),
    ("B15", 1, "Cosine is the across distance, and it draws the same wave, a quarter turn earlier. When one is at its peak, the other is at zero. Two waves, a quarter turn apart, make a circle."),

    # ── ACT III · an orbit (the first shader) ─────────────────────────────────────────────────────────
    ("B16", 2, "Now a shader. It runs once for each pixel, and U V says where that pixel is. Double it and subtract one, and the range becomes minus one to one, with zero, zero in the middle. Call that p."),
    ("B17", 2, "The planet is a distance test. Length of p is how far a pixel sits from the middle. Under the radius, paint planet color. A circle is every point at one distance from its center."),
    ("B18", 2, "The moon is the same test around another center. That center is point six times cosine and sine of an angle. Distance measures how far apart two points are: within point zero eight of it, a pixel is moon."),
    ("B19", 2, "Run it at thirty degrees. Across, point five two, as calculated. But the second number, point three, put the moon below the middle, not above. That is the next catch."),
    ("B20", 2, "On paper, up is positive. On a screen, y counts downward. The formulas stay the same and the picture flips: down is a quarter turn, and a growing angle turns clockwise. Godot's manual agrees."),
    ("B21", 2, "Now let the angle be time, the game's clock in seconds. As time counts up, the angle grows, and the moon goes round, clockwise. One line changed, and nothing is animated by hand."),
    ("B22", 2, "Scale the time and you scale the speed. Time times two, and the moon goes round twice as fast. The speed of an orbit is how fast the angle grows."),
    ("B23", 2, "An angle names a spot on the circle, so you can add to it. Add a third of a turn, tau over three, and a moon sits a third of the way round. Loop three times, and three moons sit evenly spaced."),
    ("B24", 2, "One limit: the shape has been a square. On a wide one, U V still runs zero to one both ways, so circles come out oval. Scale p's x by width over height, passed in as a uniform, and they are round again."),
    ("B25", 2, "That is the whole recipe: a center, a radius, and an angle that grows. The radius sets the size. The center sets the place. The angle's speed sets the pace. Change one and the orbit follows."),

    # ── ACT IV · an orbit around an orbit ─────────────────────────────────────────────────────────────
    ("B26", 3, "Now a meteor around the moon. The moon moves, so the meteor's center moves with it. Take the moon's position and add the meteor's own circle on top. Positions add, so circles can ride on circles."),
    ("B27", 3, "In code, that is one more line. The meteor is the moon plus a small radius times cosine and sine of its own angle. Give that angle time times three, and the meteor outpaces the moon."),
    ("B28", 3, "Watch it run. The meteor laps the moon three times for every lap the moon makes around the planet. Two ordinary circles, one riding on the other."),
    ("B29", 3, "Negate the meteor's angle, and it circles the other way while the moon keeps its direction. The minus sign mirrors the point. Same circle, opposite spin."),
    ("B30", 3, "Any depth works. Each level is a center plus a radius times cosine and sine of an angle. Chain two, and you have an arm with an elbow. Chain three, and you have a tentacle."),

    # ── ACT V · angle from a position ─────────────────────────────────────────────────────────────────
    ("B31", 4, "So far an angle went in and a position came out. Now run it backwards. A pixel knows where it is. What angle does it sit at, seen from the middle?"),
    ("B32", 4, "Tangent was opposite over adjacent. Arc tangent undoes it: give it the two sides, and it hands back the angle. For a pixel, the two sides are how far across it sits and how far down."),
    ("B33", 4, "In a shader, arc tangent takes two numbers: y first, then x. Their signs pick the quarter of the circle, so the answer covers the whole turn, from minus pi to pi. Godot's reference says exactly that."),
    ("B34", 4, "Zero is straight right. Straight down is half pi, a quarter turn clockwise. Straight left is where it wraps: nearly plus pi right below that line, nearly minus pi right above it. Past the wrap, straight up is minus half pi."),
    ("B35", 4, "See it as a picture. Divide by tau and add one half, and minus pi to pi becomes zero to one. Then mix from teal at zero to amber at one. The hard edge on the left is the seam."),
    ("B36", 4, "A common slip is passing one number, y divided by x. Dividing throws away the signs, so opposite directions get the same answer, and the left half repeats the right. Pass both numbers."),
    ("B37", 4, "Work one pixel. Up and to the left, at minus point three, minus point three. Arc tangent says minus three quarters of pi. Divide by tau: minus point three seven five. Add one half: point one two five. One eighth."),
    ("B38", 4, "Now compare. A uniform is a number your game sets from outside, and this one is called sweep. If a pixel's number is below sweep, show the picture. Raise sweep from zero to one, and a clock hand reveals it."),
    ("B39", 4, "That hand starts at nine o'clock, where the seam is. To start at twelve, move the seam: add a quarter turn, point two five, and keep only the part after the decimal point, with fract."),
    ("B40", 4, "The angle is a number, so feed it to cosine again. Multiply it by eight, and the edge of a circle swells and shrinks eight times as you go round: a flower. Subtract time from the angle, and the flower turns."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most of us met trigonometry as triangles on paper, and forgot it. "
         "In a shader it does one job. It turns an angle into a position.")
BIDEA_TEXT = ("Trigonometry is for\ntriangles on paper.", "triangles on paper", "turning angles into positions")

BDEFS = ("Five terms. An angle is an amount of turn. A radian is an angle measured so that a full turn is about six point two eight. "
         "The hypotenuse is the longest side of a right triangle. A vec two is a bundle of two numbers. "
         "And U V is a pixel's address, zero to one across and down.")
BDEFS_TERMS = [
    ("Angle", "an amount of turn, in degrees or radians"),
    ("Radian", "an angle where a full turn is about 6.28"),
    ("Hypotenuse", "the longest side of a right triangle"),
    ("Vec2", "a bundle of two numbers"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
]

BVDT_HEADING = "Trigonometry for Shaders"
BVDT_LINES = [
    "An angle fixes the ratios of a right triangle: sine, cosine and tangent.",
    "On the unit circle, cosine and sine are the point at an angle: angle in, position out.",
    "Shader angles are radians, and a full turn is tau.",
    "An orbit is a center, a radius and an angle that grows.",
    "A circle's center can itself be on an orbit.",
    "Arc tangent runs it backwards: a position gives back its angle.",
]
BVDT_NARRATION = ("Let's recap with Claude. An angle fixes the ratios of a right triangle: sine, cosine and tangent. "
                  "On the unit circle, cosine and sine are the point at an angle: angle in, position out. "
                  "Shader angles are radians, and a full turn is tau. "
                  "An orbit is a center, a radius and an angle that grows. "
                  "A circle's center can itself be on an orbit. "
                  "Arc tangent runs it backwards: a position gives back its angle.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a square Color Rect: a teal planet in the middle and a smaller moon that circles it once every four seconds. "
               "Place the moon with cosine and sine of an angle in radians, and point me to the line that sets the speed.")
BHTF_CHECKS = ["Check: the moon completes one lap in about four seconds.",
               "Check: it turns clockwise, and negating the angle reverses it."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does the moon finish a lap in about four seconds? "
                  "And does it turn clockwise, so that negating the angle reverses it?")
BHTF_SEGMENT = "Put a Moon on an Orbit"

CUT_LINE = ("Cut, in this order: the flower beat (B40), the three-moons beat (B23), the arm beat (B30) and the oval-limit beat (B24): each is a bonus "
            "that repeats an idea another beat already carries. Then the start-at-the-top beat (B39). The triangle-to-circle beats (B06, B07), the orbit "
            "(B19 to B21), the meteor (B26 to B29) and the worked pixel with the sweep (B37, B38) stay: they are the proof and the payoff.")

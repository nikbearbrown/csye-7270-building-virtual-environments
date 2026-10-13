"""narration.py: every spoken line of "Soft Edges, Glow and Noise". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party video build of an energy-shield effect (its order of ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted switches are labelled; the glow demonstration says what
stage color and intensity it used; what the docs call undefined is called undefined.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-soft-edges-glow-and-noise"
TITLE = "Soft Edges, Glow and Noise"
TITLE_LINES = ["Soft Edges, Glow", "and Noise"]
OPENING_DESCRIPTION = "How to soften edges, layer effects, and add glow"
SUMMARY = ("Learn how to soften an edge, layer a highlight on top, scroll noise through it, and make glow work for real, "
           "so your effects stop looking flat.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · SOFT EDGES, GLOW AND NOISE"
TAGS = ["Godot", "Shaders", "smoothstep", "Glow", "Noise", "HDR 2D", "Game development", "Fragment shader", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "From Cut to Ramp"),
    ("II", "Falloff and Highlight"),
    ("III", "Layering"),
    ("IV", "Noise That Moves"),
    ("V", "Glow, Honestly"),
]

BODY = [
    # ── ACT I · from a cut to a ramp ─────────────────────────────────────────────────────────────────
    ("B01", 0, "One circle, drawn two ways. First, an edge sharp enough to cut a finger. Then the same circle with the edge fading softly into the background. Nothing was blurred. One function made the difference."),
    ("B02", 0, "The hard edge comes from a function called step. Give it a line in the sand, and a value. Below the line, it answers zero. At the line or above, one. Nothing in between."),
    ("B03", 0, "A circle is a distance test. Distance asks how far apart two points are. Ask it how far each pixel's address is from the middle. One minus a step on that answer is one inside the radius, and zero outside."),
    ("B04", 0, "Zoom in on that edge. Every pixel is either all color or none. With nothing in between, the rim becomes a staircase of square steps. That is why hard edges look jagged."),
    ("B05", 0, "Smooth step takes two lines. Below the first, zero. Above the second, one. Between them, it climbs along a smooth curve: slow to start, fastest in the middle, slow to finish."),
    ("B06", 0, "That curve is not a straight line. Ten percent of the way along, a straight ramp reads zero point one. Smooth step reads zero point zero two eight. The formula is three t squared minus two t cubed."),
    ("B07", 0, "Swap step for smooth step and give it two radii. Inside zero point two five, fully on. Beyond zero point four, fully off. In between, the value glides down. That band is the soft edge."),
    ("B08", 0, "Tie the inner radius to a uniform and you get a softness dial. Small values give a crisp rim. Large ones give a cloud. The outer radius never moves."),
    ("B09", 0, "Squeeze the band to nothing, and smooth step becomes step. But the docs call equal lines undefined, and the range on that uniform cannot stop code from sending zero. So keep the width above zero with max."),
    ("B10", 0, "You will also meet smooth step with its lines swapped, to flip the ramp. On this Mac that worked. The docs still call it undefined, so write one minus smooth step instead."),

    # ── ACT II · falloff and highlight ───────────────────────────────────────────────────────────────
    ("B11", 1, "A falloff is how quickly a value fades as you move away from a point. The simplest is one minus the distance: one at the point, dropping steadily to zero a whole unit away."),
    ("B12", 1, "As the alpha of a teal color, that is a soft spot of paint, thickest at the point. Notice where it stops: it does not. At the edge of the picture it is still more than a third on."),
    ("B13", 1, "Raise it to a power above one, and numbers between zero and one shrink. Zero point seven becomes zero point three four three at power three, and zero point one one eight at power six. The spot tightens."),
    ("B14", 1, "Make the power a uniform and watch the spot shrink as it climbs. Power one is a haze, three a soft highlight, eight a pinpoint. The clamp stops the number going negative, where a power is undefined."),
    ("B15", 1, "A falloff never stops by itself, so cut it to a shape. Multiply it by the circle's mask, the disc. Where the disc is zero, the product is zero, and the highlight can only show on the bubble."),
    ("B16", 1, "A point is two numbers. Make them a uniform and the highlight follows. Slide it around, and you decide where the light seems to come from."),

    # ── ACT III · layering ───────────────────────────────────────────────────────────────────────────
    ("B17", 2, "A layer is a color plus a mask: how much of that color to show. The body is teal, masked by the disc. The highlight is pale, masked by the spot. Stack them and you have a bubble."),
    ("B18", 2, "Two ways to combine masks. Multiply, and you keep only where both are on. Add, and you get where either is on, up to a cap of one. Multiply by zero erases. Add zero and nothing changes."),
    ("B19", 2, "Each layer's color is a uniform with the hint source color. A hint is the word after the colon that tells Godot how to treat a uniform. For a color, that is a color picker in the editor."),
    ("B20", 2, "Now the sum. The body color, plus the highlight color times the highlight mask. Where the mask is zero, nothing is added. Where it is one, the highlight color lands in full."),
    ("B21", 2, "A trap. Add a brightness dial for the whole bubble. Multiplication always happens before addition. So a plus b times c multiplies b and c first, and only the highlight dims. Wrap the sum in parentheses."),
    ("B22", 2, "Real numbers from this Mac, brightness point six. With the parentheses, the highlight's center reads point seven in green, and the whole bubble dims. Without them, point nine five, and the body barely moves."),
    ("B23", 2, "Godot's own table says the same. Parentheses come first, then multiply and divide, then add and subtract. When in doubt, add a pair. They cost nothing."),

    # ── ACT IV · noise that moves ────────────────────────────────────────────────────────────────────
    ("B24", 3, "Noise is a texture of smooth random values: nearby pixels look alike, far ones do not. Godot makes it for you: a noise texture two D, filled by a fast noise lite generator."),
    ("B25", 3, "A shader reads it through a sampler two D uniform, the type for a texture. The function texture does a lookup: what value sits at this address? Multiply that into the alpha, and the disc turns to cloud."),
    ("B26", 3, "To move it, add time to the address. Time is seconds on one clock shared by the whole game. Each second, the lookup slides a tenth of the way along, and the clouds drift."),
    ("B27", 3, "Watch the direction. Adding to the address slides the lookup right, so the picture moves left. Measured here: add one eighth, and the clouds moved thirty-two pixels left, exactly one eighth of the width."),
    ("B28", 3, "Now delete the hint on that uniform and let it run. Past the edge of the texture, a lookup returns the edge pixel, row after row. The right side smears into streaks, and the motion stops."),
    ("B29", 3, "Put the hint back: repeat enable. A lookup past one now wraps around to the start, so the scroll never ends. But look at the line where the right edge meets the left."),
    ("B30", 3, "That line is real: this texture's edges do not match. In the noise texture, switch on seamless, and Godot blends the edges so they meet. The docs warn it may cost some contrast. Here, a little."),
    ("B31", 3, "Noise can also hide and show. Compare it with a number climbing from zero to one: wherever the noise is below the number, show the pixel. The disc blooms in blotches. That number is a uniform."),
    ("B32", 3, "Progress is not percent shown. Noise values bunch near the middle. At one quarter, about one percent of the disc is on. At one half, forty-four percent. At three quarters, ninety-three. Remap the number for an even pace."),

    # ── ACT V · glow, honestly ───────────────────────────────────────────────────────────────────────
    ("B33", 4, "The trick you will see everywhere: multiply a color by a number above one. Teal times six puts green and blue well above one. The screen cuts everything above one, so the bubble turns white."),
    ("B34", 4, "In the shader, the dial is one plus glow times five, in parentheses, as before. Turn glow up, and the bubble does not glow. It goes flat white. The teal and the highlight are both gone."),
    ("B35", 4, "H D R means high dynamic range: colors allowed to go brighter than one. Godot's two D drawing does not allow them by default. The setting is H D R two D, under Rendering, Viewport. Restart after switching it on."),
    ("B36", 4, "Run one: H D R two D on, glow off. Still white, with a tinted rim, because green and blue are cut off before red. On this Mac the frame holds the real numbers: green reads about two and a half."),
    ("B37", 4, "Run two: add a world environment, switch glow on, and set its background to canvas. Now the bright disc bleeds a halo, tinted teal. The halo belongs to the environment. Your shader only supplied the number."),
    ("B38", 4, "So glow is three agreements. Your shader makes a number above one. The viewport keeps it. The environment turns it into light. Break any one, and you get plain white."),
    ("B39", 4, "The halo grows with how far above one you go. At glow point five, it is faint. At one, clear. And glow adds light, so on a light background it has almost nowhere to go."),
    ("B40", 4, "Turning on H D R two D changes more than glow. Two D now renders in linear light. On this Mac, a color without the source color hint came out washed out: red point six four, not point three seven."),
    ("B41", 4, "Without H D R two D, the docs say to lower the glow threshold below one, so ordinary white glows. On this Mac that gave a faint halo with no color. H D R two D gives you both."),
    ("B42", 4, "Now all the layers together: the soft edge, the highlight, the noise drifting through, and the glow dial. One bubble, built a layer at a time."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people think a soft edge needs a blur. It does not. "
         "A soft edge is a ramp: a value that climbs from zero to one over a distance you choose. "
         "We will build one bubble a layer at a time, and finish with glow.")
BIDEA_TEXT = ("A soft edge needs a blur.", "a blur", "a ramp")

BDEFS = ("Five terms. A ramp is a smooth run of values from zero to one. A mask is a number from zero to one for each pixel: how much to show. "
         "U V is a pixel's address on the shape. A uniform is a value your game sets. Alpha is how visible a pixel is.")
BDEFS_TERMS = [
    ("Ramp", "a smooth run of values from 0 up to 1"),
    ("Mask", "a number from 0 to 1 per pixel saying how much of something to show"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
    ("Alpha", "how visible a pixel is: 0 invisible, 1 solid"),
]

BVDT_HEADING = "Soft Edges, Glow and Noise"
BVDT_LINES = [
    "A soft edge is a ramp, and smoothstep lets you choose its width.",
    "A falloff fades with distance, and a power tightens it.",
    "Multiply masks to keep both, add them to show either.",
    "Wrap a sum in parentheses before you scale it.",
    "Noise gives structure, time scrolls it, repeat and seamless keep it going.",
    "A color above one glows only when the shader, the viewport and the environment agree.",
]
BVDT_NARRATION = ("Let's recap with Claude. A soft edge is a ramp, and smooth step lets you choose its width. "
                  "A falloff fades with distance, and a power tightens it. "
                  "Multiply masks to keep both, add them to show either. "
                  "Wrap a sum in parentheses before you scale it. "
                  "Noise gives structure, time scrolls it, repeat and seamless keep it going. "
                  "A color above one glows only when the shader, the viewport and the environment agree.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a square Color Rect. Draw a teal disc with a soft edge, using smooth step on the distance from the middle. "
               "Add a float uniform called softness with a hint range from zero point zero two to zero point four, and keep the width above zero with max. "
               "Then point me to the three lines I should check.")
BHTF_CHECKS = ["Check: dragging softness in the Inspector widens and narrows the fade, with no hard jump at the lowest setting.",
               "Check: the shape is a circle, not an oval."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does dragging softness widen and narrow the fade? "
                  "And is the shape a circle, not an oval?")
BHTF_SEGMENT = "Make a Soft Edge with a Dial"

CUT_LINE = ("Cut, in this order: the reveal-pace beat (B32), the beat on what else H D R two D changes (B40), the swapped-lines beat (B10) and the "
            "beat on glow without H D R two D (B41). Each is a true caveat that another beat or the docs already carry. The S-curve pair (B05, B06), the "
            "parentheses pair (B21, B22), the seam pair (B29, B30), the two glow runs (B36, B37) and the finale (B42) stay: they are the proof and the payoff.")

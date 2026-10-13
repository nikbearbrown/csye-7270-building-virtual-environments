"""narration.py: every spoken line of "UV Space". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party long course on 2D shaders (ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine, window size and renderer; the pixel counts belong to a 640 by 360 window;
every Godot picture is a Shader Lab render of a file in lab-shaders/.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
The title card and the outro props keep the real spelling "UV Space"; the voice reads SPOKEN_TITLE ("U V Space", letters spaced) in BOPEN and BOUT.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-uv-space"
TITLE = "UV Space"
SPOKEN_TITLE = "U V Space"                      # the voice reads the letters; the card and the outro keep TITLE
TITLE_LINES = ["UV Space"]
OPENING_DESCRIPTION = "Move, scale and mirror the address a shader looks up"
SUMMARY = ("Learn to move, scale, tile and mirror the address a shader looks up, so you can scroll a picture, zoom into it, "
           "and keep a circle round on any shape.")
BOPEN = S.bopen(SPOKEN_TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · UV SPACE"
TAGS = ["Godot", "Shaders", "UV", "Texture", "Fragment shader", "Tiling", "Scrolling", "Aspect ratio", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "The Address Book"),
    ("II", "Move Where You Look"),
    ("III", "Center and Mirror"),
    ("IV", "Fixing the Squash"),
    ("V", "Staying Inside the Picture"),
]

BODY = [
    # ── ACT I · the address book ─────────────────────────────────────────────────────────────────────
    ("B01", 0, "One picture, and it never changes. Yet here it slides, shrinks and repeats. The picture file is untouched. The shader only changed where it looks. That is the trick behind scrolling, zooming and tiling."),
    ("B02", 0, "Every pixel on a shape has an address: two numbers, called U V. The first says how far across, the second how far down, each from zero to one. The top left is zero, zero. The bottom right is one, one."),
    ("B03", 0, "Notice that the second number counts down, the opposite of a school graph. And size does not matter: a tiny shape and a huge one both run zero to one. An address is a fraction of the shape, not a count of pixels."),
    ("B04", 0, "Here is every address at once, drawn as a color. Red is the first number, so it grows to the right. Green is the second, so it grows downward. Blue is held at half. Each pixel paints its own address."),
    ("B05", 0, "To color a pixel, the shader can read a picture at that pixel's address. The texture function takes a picture and an address, and hands back the color stored there. That color becomes the pixel's."),
    ("B06", 0, "Inside fragment, which Godot runs once for every pixel the shape covers, we read the picture at that pixel's own address. Nothing is changed, so the picture comes out exactly as it went in."),
    ("B07", 0, "Here is a way to hold it in your head. The picture stays put. The shape is a window onto it, and the address says where the window sits. Change the address, and the window slides."),
    ("B08", 0, "In fragment, the address is read-only. So the pattern never changes: copy it into a variable, bend the copy, and look up the picture with the bent copy. Every trick from here fills in the middle line."),

    # ── ACT II · move where you look ─────────────────────────────────────────────────────────────────
    ("B09", 1, "Predict first. We subtract a quarter from the horizontal address. Which way does the picture go? Watch. It slides right, even though we subtracted. That feels backwards, so let's check the numbers."),
    ("B10", 1, "Here is why. The pixel in the middle now looks up the spot a quarter of the way across. So whatever lives at that spot shows up in the middle. Everything lands a quarter further right."),
    ("B11", 1, "So the rule is a reversal. Subtract from the horizontal address, and the picture moves right. Add to it, and it moves left. Change the address one way, and the picture goes the other."),
    ("B12", 1, "The same goes for the vertical address, with one twist. It counts downward, so subtracting from it sends the picture down. Subtract from both, and the picture moves right and down together."),
    ("B13", 1, "Now scale. Multiply the address by two. The picture shrinks to half its width and half its height, a quarter of its area, and sits in the top left corner. The rest of the shape has no picture to read."),
    ("B14", 1, "Why smaller? Doubled, the address runs from zero to two across the shape. The picture only covers zero to one. So it fills the first half of each side, where the address is still below one."),
    ("B15", 1, "What lies beyond one? By default, the lookup keeps returning the picture's edge pixels. Declare the texture with repeat enable, and the picture starts over instead. Scale by three, and you get a three by three grid."),
    ("B16", 1, "A node's own texture has the same switch. It is called texture repeat. Set it to enabled, in the node's settings or in code, and that texture repeats too. Mirror is another setting: every other copy is flipped."),
    ("B17", 1, "Now let it move on its own. Add a tenth of the time to the horizontal address. Time is seconds on one clock the whole game shares. The picture scrolls left, a tenth of its width every second."),
    ("B18", 1, "Four moves, then. Subtract, and the picture moves one way. Add, and it moves the other. Multiply by more than one, and it shrinks. Multiply by less than one, and it grows. Always the opposite of what the address does."),

    # ── ACT III · center and mirror ──────────────────────────────────────────────────────────────────
    ("B19", 2, "Now zoom in: multiply by less than one. Try one half. The picture grows, but it swells toward the bottom right and slides out of frame. That is not the zoom we wanted."),
    ("B20", 2, "Scaling keeps zero fixed, so zero is the pivot. Here zero is the top left corner, so everything grows away from that corner. To grow from the middle, the middle has to be zero."),
    ("B21", 2, "Three steps: subtract a half so the middle is zero, scale, then add the half back. Now the picture grows in place, around its own middle."),
    ("B22", 2, "Many shaders skip adding the half back and stay centered. Double the address and subtract one. Now the range is minus one to one, zero is the middle, and left and up are negative."),
    ("B23", 2, "In these coordinates, the length of the address is its distance from the middle. Closer than the radius means inside a circle. So a circle is one comparison, and the radius is the only number."),
    ("B24", 2, "Now put two eyes on that circle. One test finds the right eye, and the left stays empty. We could write a second test for the left. But everything symmetric would need two of everything."),
    ("B25", 2, "Absolute value drops the minus sign: minus point three becomes point three. Apply it to the horizontal address, and the left half reads exactly like the right. One test now draws both eyes."),
    ("B26", 2, "Think of absolute value as folding the shape down its middle. The left half lands on the right half. Every pixel on the left gets the same answer as its mirror twin on the right."),
    ("B27", 2, "A different mirror: scale the centered address by minus one. On the vertical address, the picture turns upside down, and the eyes drop below the middle. On the horizontal one, left and right swap."),

    # ── ACT IV · fixing the squash ───────────────────────────────────────────────────────────────────
    ("B28", 3, "Back to the circle. Same test, same radius, but now on a wide shape. Predict the result. We get an oval, as much wider than tall as the shape is."),
    ("B29", 3, "Here is why. The address runs zero to one on both sides, however long the sides are. This shape is six hundred forty wide and three hundred sixty tall. A tenth across is sixty-four pixels. A tenth down is thirty-six."),
    ("B30", 3, "So the radius, point eight of the way from the middle to the edge, is two hundred fifty-six pixels sideways. Up, it is only one hundred forty-four. Measured from the render: five hundred twelve wide, two hundred eighty-eight tall."),
    ("B31", 3, "You may hear that the shape's pixels get stretched. They do not. Every pixel is the same square. It is the address that is uneven: one step of address covers more pixels across than down."),
    ("B32", 3, "The fix: make a step across cover as many pixels as a step down. Multiply the horizontal address by the aspect ratio, which is width divided by height. Here, sixteen over nine."),
    ("B33", 3, "In code, it is one line. Multiply the centered x by aspect, then measure the length as before. The oval becomes a circle, two hundred eighty-eight pixels wide and two hundred eighty-eight tall."),
    ("B34", 3, "A shader has no direct way to ask the shape's size, so tell it. Make aspect a uniform, and set it from the node's width over height. Set it again whenever the node is resized, or the circle goes oval again."),
    ("B35", 3, "Two engine values hold proportions, but each has a catch. Texture pixel size is the texture's, and on a color rect it is one by one. Screen pixel size is the screen's, not your shape's. Only the uniform was right every time."),

    # ── ACT V · staying inside the picture ───────────────────────────────────────────────────────────
    ("B36", 4, "Back to scaling, with a picture that has a solid edge. Multiply the address by two, and the edge pixels smear across the rest of the shape. Outside the picture, the lookup keeps returning its last row and column."),
    ("B37", 4, "A sprite with a transparent border hides this, because the pixels being stretched are transparent. Godot's documentation suggests exactly that: a fully transparent border, one pixel wide. The other cure is in the shader."),
    ("B38", 4, "We want the picture inside its edges and nothing outside. That is a mask: a number from zero to one for each pixel, saying how much to show. The step function can build one: zero below its edge, one at or above."),
    ("B39", 4, "Two steps make a gate. One turns on at zero, the other turns off at one. Multiply them, and you get one only between zero and one. Do it for both axes, and multiply again."),
    ("B40", 4, "Multiply the picture's alpha by that mask. Inside the picture, nothing changes. Outside, alpha is zero, so the smear is gone. Scale by two, and you see one clean picture."),
    ("B41", 4, "Now the opening shader reads like a sentence. Slide the address. Scale it. Look up the picture, with repeat on. Two lines bend the address, one looks it up, and that is the whole effect."),
    ("B42", 4, "When a U V effect looks wrong, check four causes. Moving the wrong way: you added, not subtracted. Zooming to a corner: zero is not in the middle. Smearing at the edges: no repeat, no mask. A circle gone oval: no aspect fix."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Many people read U V as where a pixel sits on the screen. It is where the pixel sits on its shape. "
         "And since it is only a pair of numbers, you can change it before you use it. Everything else follows from that.")
BIDEA_TEXT = ("UV says where a pixel is on\nthe screen.", "the screen", "the shape")

BDEFS = ("Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. "
         "A texture is an image a shader can read by address. A vector is a bundle of two to four numbers. "
         "And a uniform is a value your game sets from outside the shader.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Pixel", "one dot of the picture on screen"),
    ("Texture", "an image a shader can read by address"),
    ("Vector", "a bundle of two to four numbers"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
]

BVDT_HEADING = "UV Space"
BVDT_LINES = [
    "U V is a pixel's address on its shape, from zero to one.",
    "Change the address one way, and the picture goes the other.",
    "Scale around zero, so put zero in the middle.",
    "Absolute value folds one side onto the other.",
    "Multiply by the aspect ratio, and a circle stays round.",
    "Repeat or a mask keeps the edges clean.",
]
BVDT_NARRATION = ("Let's recap with Claude. U V is a pixel's address on its shape, from zero to one. "
                  "Change the address one way, and the picture goes the other. "
                  "Scale around zero, so put zero in the middle. "
                  "Absolute value folds one side onto the other. "
                  "Multiply by the aspect ratio, and a circle stays round. "
                  "Repeat or a mask keeps the edges clean.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a sprite that scrolls its texture to the left, one tenth of the picture every second, "
               "and repeats forever. Then point me to the line that sets the direction and the setting that makes it repeat.")
BHTF_CHECKS = ["Check: the picture moves left, not right.",
               "Check: after ten seconds it lines up with where it started, with no gap or smear."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does the picture move left, not right? "
                  "And after ten seconds, does it line up with where it started, with no gap or smear?")
BHTF_SEGMENT = "Scroll a Texture Without Smearing"

CUT_LINE = ("Cut, in this order: the node-setting beat (B16, a second route to the same repeat switch), the transparent-border beat (B37), "
            "the stretched-pixel beat (B31), the fold drawing (B26) and the gate drawing (B39: the mask then takes one beat, B38). "
            "Each repeats or decorates an idea another beat already carries. "
            "The reversal beats (B09 to B11), the centered zoom (B19 to B21), the oval and its fix (B28, B29, B32, B33) and the mask result (B40) "
            "stay: they are the proof and the payoff.")

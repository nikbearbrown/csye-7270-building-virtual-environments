"""narration.py: every spoken line of "Textures and Color". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party video course on 2D shaders whose texture and color chapters set the order of ideas
(ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input is labelled; a pixel read from one renderer is
never presented as true for another; what was not tested (lit 3D surfaces, other GPUs) is not claimed.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-textures-and-color"
TITLE = "Textures and Color"
TITLE_LINES = ["Textures and Color"]
OPENING_DESCRIPTION = "How a shader reads images, and why colors shift"
SUMMARY = "Learn how a shader reads a texture, how to do math on color, and why the color you type is not always the color you see."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · TEXTURES AND COLOR"
TAGS = ["Godot", "Shaders", "Textures", "Color space", "sRGB", "Linear color", "Noise", "Dissolve effect", "GDScript", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Reading a Texture"),
    ("II", "Color Is Math"),
    ("III", "Noise as a Mask"),
    ("IV", "Two Ways to Count Light"),
    ("V", "Hint Colors, Not Masks"),
]

BODY = [
    # ── ACT I · reading a texture (B01-B07) ────────────────────────────────────────────────────────────
    ("B01", 0, "Watch this sprite burn away. One number drives it, and a picture of soft clouds decides where it burns first. By the end of this film you will build that effect, and know why the colors you pick can look different in another renderer."),
    ("B02", 0, "First, the table. A texture is a grid of colors, and every entry has an address: U V, zero to one across, zero to one down. Hand the table an address, and it hands back the color stored there."),
    ("B03", 0, "In code, the lookup is one function: texture, then the table's name, then the address. It returns a color. Fragment runs once for each pixel, so every pixel asks with its own address, and the shape fills in."),
    ("B04", 0, "Where does the table come from? A uniform of type sampler two D is a slot you fill from outside. Any texture fits: a small picture, a gradient, noise. It stretches across the shape, because the address always runs from zero to one."),
    ("B05", 0, "That small picture came out smeared. An address can land between two entries, and by default the graphics card blends the four nearest. Add filter nearest, and it takes the closest entry only: crisp blocks, which is what pixel art wants."),
    ("B06", 0, "Because it is a lookup, you can ask for any address you like. Ask for one minus the horizontal address, and the picture flips. The table never changed. Only where you looked."),
    ("B07", 0, "Ask for twice the address, and half the lookups fall off the end of the table. With repeat disable, the edge entries stretch outward. With repeat enable, the table starts over, and tiles."),

    # ── ACT II · color is math (B08-B16) ───────────────────────────────────────────────────────────────
    ("B08", 1, "What comes back from a lookup is a vec four: four numbers, each from zero to one. Red, green, blue, and alpha. Orange is one, one half, zero, one. A color is only numbers, so you can do arithmetic on it."),
    ("B09", 1, "A sprite brings a table of its own, named texture, in capitals. Before your code runs, color already holds that lookup, multiplied by the node's modulate. Overwrite color with a plain lookup, and the modulate is thrown away."),
    ("B10", 1, "Multiply the color by a tint. A channel times one stays, times a half it halves. This tint keeps all the red, most of the green, and half the blue, so the picture turns warm."),
    ("B11", 1, "One minus the color flips it. Zero becomes one, one becomes zero, and a half stays put. Do it to red, green and blue, and every patch turns into its opposite."),
    ("B12", 1, "Careful with the fourth number. Flip alpha too, and the sprite turns see-through, while the empty space around it becomes a solid white card. Alpha is a channel like the others: only a number."),
    ("B13", 1, "Add instead of multiply, and the picture brightens. Add a ramp that grows to one, and every patch ends in flat white. Ordinary two-D drawing cuts every number off at one, so the extra is lost."),
    ("B14", 1, "To make gray, give red, green and blue the same number. The crude way copies one channel. Copy red, and the rose turns bright, while the leaf and the sky turn dark."),
    ("B15", 1, "Better: weigh the channels by how bright each looks to the eye. About twenty-one percent red, seventy-two percent green, seven percent blue. Dot multiplies and adds them up. Now the rose, the leaf and the sky land on close grays."),
    ("B16", 1, "Mix blends two colors by an amount from zero to one. Here it blends the picture with its own gray: zero is all color, one is all gray. The amount can be one number for everything, or a different number at every pixel."),

    # ── ACT III · noise as a mask (B17-B26) ────────────────────────────────────────────────────────────
    ("B17", 2, "Not every texture is a picture. This one is noise: soft clouds made of numbers, one from zero to one at every pixel. Read each number as an amount of teal, and you have a mask: how much of something to show."),
    ("B18", 2, "You do not draw it. In the Inspector, open the slot's menu and choose Noise Texture two D under New. Click it, then open its Noise slot the same way, and choose Fast Noise Lite. Godot generates the clouds, at the size and seed you choose."),
    ("B19", 2, "Now cut with it. Step compares each number with a threshold: below it, zero; at or above it, one. Slide the threshold up, and the clouds shrink into blobs that disappear."),
    ("B20", 2, "Use that cut on a sprite. If a pixel's noise is below the threshold, discard it, and the background shows through. Call the threshold progress. As it climbs from zero to one, the sprite is eaten away."),
    ("B21", 2, "To make it burn, color the pixels that are about to go. They sit right above the threshold: a thin band of noise values, a tenth wide. Everything in that band is next to disappear."),
    ("B22", 2, "What color? Look it up in a second table: a ramp from dark red through orange to yellow. The nearer a pixel is to the edge, the hotter it is, and the further along the ramp you read. The address is a number you computed."),
    ("B23", 2, "Here is the whole shader. Noise decides who goes first. Progress is the dial. The ramp colors the edge. Twelve lines of code, and the sprite burns away."),
    ("B24", 2, "Now swap the table. Put a left to right gradient where the noise was, and the same shader wipes instead of dissolves. Nothing in the code changed. A mask is only a table of amounts."),
    ("B25", 2, "Check the ends. At zero the sprite should be untouched. The first version of this shader failed that: some pixels already burned, because at zero the band covered the darkest clouds. The fix: start the threshold a band's width below zero."),
    ("B26", 2, "To drive it from the game, tween progress. One trap: a tween needs a starting value, so set progress from code first. Skip that, and Godot answers that the property does not exist."),

    # ── ACT IV · two ways to count light (B27-B32) ─────────────────────────────────────────────────────
    ("B27", 3, "Now the part that surprises people. Here is one three-D shader, run in two renderers. It blends two grays, point two and point eight, halfway. You would expect point five. On this Mac, Forward Plus reads point six in the middle. Compatibility reads point five."),
    ("B28", 3, "Neither renderer is broken. A pixel probe measures one thing: what this renderer drew for this shader. And a test that runs without a window has no pixels to read at all."),
    ("B29", 3, "Why do they differ? There are two ways to count brightness. A color picker's numbers are spaced for the eye: that is s R G B. Light adds up in a straight line: that is linear. The two agree at zero and one, and disagree between."),
    ("B30", 3, "Blend point two and point eight halfway. Average the typed numbers, and you get point five. Convert to light, average there, and convert back, and you get point six. Same two colors, two different answers."),
    ("B31", 3, "Forward Plus and Mobile work in light, and convert to s R G B only to show the picture. In this test, Compatibility blends the numbers as typed. That is why one reads point six and the other point five."),
    ("B32", 3, "In two-D, the default is different. Every renderer blends the typed numbers, and all three read point five. Turn on the project setting H D R two D, which works in light and keeps numbers past one for glow, and Forward Plus and Mobile read point six."),

    # ── ACT V · hint colors, not masks (B33-B41) ───────────────────────────────────────────────────────
    ("B33", 4, "The fix is a hint: source color, written after a color's name. Godot's docs say where it matters. Required in Forward Plus and Mobile, and in two-D when H D R two D is on. Optional in Compatibility, and in two-D when it is off."),
    ("B34", 4, "What does it do? It tells the engine the numbers are s R G B, so red, green and blue are converted to light before your math. Alpha stays a plain amount. And the Inspector shows a color picker, not four number boxes."),
    ("B35", 4, "Leave the hint off, and the engine takes typed numbers for light. In Forward Plus with H D R two D on, a color typed as point two, point four, point six comes out near point five, point seven, point eight. Washed out. Plain nodes need no hint."),
    ("B36", 4, "Setting a color from code works the same way. Pass the color exactly as you picked it, and let the hint convert it. Convert it yourself first, and it converts twice: that blue turns almost navy."),
    ("B37", 4, "Textures follow the rule. A color texture gets the hint. Without it, in Forward Plus, the picture comes out lighter, the same washed out look. In Compatibility it makes no difference, so the mistake can hide."),
    ("B38", 4, "A mask must not have the hint. Hint a mask in Forward Plus, and every number in it shifts. A threshold of one half then cuts about three quarters of the way across the ramp, not halfway."),
    ("B39", 4, "So the rule is short. Hint every color you give a shader, uniform or texture. Never hint a mask. And if you ship on more than one renderer, look at each, because a number read from one may not hold in the others."),
    ("B40", 4, "To change a project's renderer, open Project Settings, then Rendering, Renderer. Set Rendering Method to forward plus, mobile or G L compatibility, then Save and Restart. Look at your colors in each renderer you ship on, because the same shader can show a different pixel."),
    ("B41", 4, "Back to the burn. Its ramp is a color texture, so it carries the hint. Its noise is a mask, so it does not. Check those two lines whenever an AI hands you a shader like this."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people picture a texture as a picture pasted onto a shape. "
         "A shader never pastes anything. For every pixel, it looks a color up in a table, by address.")
BIDEA_TEXT = ("A texture is a picture\npasted onto a shape.", "pasted onto a shape", "looked up by address")

BDEFS = ("Six terms. A shader is a small program the graphics card runs to decide how something is drawn. "
         "U V is a point's address on a shape, from zero to one across and down. A texture is an image a shader can read by address. "
         "A channel is one of red, green, blue or alpha. Alpha is how visible a pixel is: zero invisible, one solid. And the renderer is the part of Godot that draws.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Texture", "an image a shader can read by address"),
    ("Channel", "one of red, green, blue or alpha"),
    ("Alpha", "how visible a pixel is: 0 invisible, 1 solid"),
    ("Renderer", "the part of Godot that draws"),
]

BVDT_HEADING = "Textures and Color"
BVDT_LINES = [
    "A texture is a table you look up by address.",
    "A color is four numbers, so you can tint it, flip it, gray it and mix it.",
    "A noise texture is a mask: compare it with a threshold, and a sprite dissolves.",
    "The number you type is not always the color you see: there are two scales.",
    "Hint every color with source color, and never hint a mask.",
    "A number read from one renderer may not hold in another.",
]
BVDT_NARRATION = ("Let's recap with Claude. A texture is a table you look up by address. "
                  "A color is four numbers, so you can tint it, flip it, gray it and mix it. "
                  "A noise texture is a mask: compare it with a threshold, and a sprite dissolves. "
                  "The number you type is not always the color you see: there are two scales. "
                  "Hint every color with source color, and never hint a mask. "
                  "A number read from one renderer may not hold in another.")

BHTF_PROMPT = ("Write a Godot canvas item shader that dissolves a sprite. A noise texture decides which pixels go first, "
               "a float uniform called progress from zero to one is the dial, and a ramp texture colors the burning edge. "
               "Mark which texture needs the source color hint, and say why.")
BHTF_CHECKS = ["Check: at progress zero the sprite is untouched, and at one it is gone.",
               "Check: the ramp has the source color hint and the noise does not."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. At progress zero, is the sprite untouched, and at one, is it gone? "
                  "And does the ramp carry the source color hint, while the noise does not?")
BHTF_SEGMENT = "Dissolve a Sprite With Noise"

CUT_LINE = ("Cut, in this order: the tween beat (B26), the brighten beat (B13), the alpha-hole beat (B12), the gray pair (B14, B15), "
            "then the from-code beat (B36): each extends an idea another beat already carries. The dissolve build (B19 to B25), the "
            "two-renderer reveal (B27 to B31) and the hint rules (B33 to B39) stay: they are the film.")

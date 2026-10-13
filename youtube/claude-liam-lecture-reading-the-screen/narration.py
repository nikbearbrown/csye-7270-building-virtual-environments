"""narration.py: every spoken line of "Reading the Screen". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every behaviour claimed below was run in
evidence/planning-checks/), and a third-party video and a long third-party course whose ideas this film follows and nothing of which is copied
(see SOURCES.md). Honesty rules for this film: a measured number says what machine and renderer; scripted input is labelled; behaviour that
differs between the Forward+ and Compatibility renderers is named by renderer, never claimed for both; the editor's own labels are only named where the docs name them.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-reading-the-screen"
TITLE = "Reading the Screen"
TITLE_LINES = ["Reading the Screen"]
OPENING_DESCRIPTION = "How a shader reads what is already drawn"
SUMMARY = ("Learn how a shader can read what the game has already drawn, "
           "so you can filter the whole screen, bend the picture, and build water you can see through.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · READING THE SCREEN"
TAGS = ["Godot", "Shaders", "Screen texture", "hint_screen_texture", "SCREEN_UV", "Post-processing", "CanvasLayer", "BackBufferCopy",
        "Game development", "Nik Bear Brown"]
SOURCE_DOC = ("Godot 4.7 documentation (Screen-reading shaders, CanvasItem shaders, CanvasLayer, BackBufferCopy, Control); "
              "Godot 4.7.2 on Apple M4 Pro (evidence/planning-checks); see SOURCES.md")

ACTS = [
    ("I", "A Copy of the Screen"),
    ("II", "Full-Screen Effects"),
    ("III", "Bend What Is Behind"),
    ("IV", "What It Can See"),
]

BODY = [
    # ── ACT I · a copy of the screen ───────────────────────────────────────────────────────────────
    ("B01", 0, "Give a sprite a shader, and it can color that sprite. But glass, heat haze and water do something different. "
               "They change what is behind them. For that, a shader has to read the picture the game has already drawn."),
    ("B02", 0, "There is a catch. Graphics hardware cannot properly read a picture while it is drawing into it. "
               "So Godot copies the picture drawn so far, and your shader reads the copy. That copy is the screen texture."),
    ("B03", 0, "Here is the smallest use. In the fragment function, each pixel's color becomes whatever the screen holds at that pixel's spot. "
               "Switch it on, and the rectangle vanishes. It is still there. It only shows what is behind it."),
    ("B04", 0, "Now take the uniform line apart. A uniform is a value that comes from outside. "
               "Sampler two D is the type of a texture a shader can read. And the name is yours to choose."),
    ("B05", 0, "Then the hint, after the colon. A hint is a word that tells Godot how to treat a uniform. "
               "This one says: fill it with the screen. Godot refreshes it every frame, so you never set it yourself."),
    ("B06", 0, "Now read it. The function texture takes a texture and an address, and returns the color stored there. "
               "Four numbers come back: red, green, blue, and alpha, which is how visible it is."),
    ("B07", 0, "A pixel has two addresses. U V is its place on its own shape. Screen U V is its place on the whole screen. "
               "Slide the shape, and U V stays the same, while screen U V changes."),
    ("B08", 0, "Read the screen with U V, and the rectangle fills with a tiny copy of the whole screen. "
               "Read it with screen U V, and the rectangle becomes a window onto what is behind it, wherever it slides."),
    ("B09", 0, "Now change the color. Adding r g b after it keeps red, green and blue. One minus each of them flips every color. "
               "Slide the window, and the flipped picture stays pinned to the screen. Only the opening moves."),
    ("B10", 0, "Older tutorials use a shortcut called screen texture, in capital letters. Godot four removed it. "
               "The compiler says so, and points you to the hint instead. If an old line fails, this is why."),

    # ── ACT II · full-screen effects ───────────────────────────────────────────────────────────────
    ("B11", 1, "A full-screen effect, or post-processing, needs a node covering every pixel. A color rect with your shader on it can do that: "
               "set its layout to Full Rect. Its edges follow the screen's corners, even when the game is resized."),
    ("B12", 1, "Put that color rect in a canvas layer. A canvas layer is a group drawn together, with a number. The game is at zero. "
               "A layer numbered one is drawn after it, so it can read everything the game drew."),
    ("B13", 1, "One catch: a color rect catches mouse clicks, so your game never hears them. "
               "Set its mouse filter to Ignore, and the clicks pass through to the game."),
    ("B14", 1, "Start with gray. A gray pixel has equal red, green and blue. The function dot multiplies each by a weight and adds them up. "
               "Green weighs most and blue least, because that is how bright each color looks to us."),
    ("B15", 1, "Then mix. Mix blends two values by an amount: zero gives the first, one gives the second. "
               "Make the amount a uniform with a range hint, and your game can drain the color from the whole picture with one dial."),
    ("B16", 1, "Now a spotlight: color near the player, gray everywhere else. "
               "The shader needs two numbers from your game: where the player is, and how big the circle is. Both are uniforms."),
    ("B17", 1, "Measure each pixel's distance from the player. The function distance gives the gap between two addresses. "
               "If it is more than the radius, make the pixel gray. Otherwise, leave it alone."),
    ("B18", 1, "Look closely: it is an oval. Addresses run zero to one across and zero to one down, but the screen is wider than tall. "
               "So a step across is longer than a step down, and the circle stretches."),
    ("B19", 1, "Screen pixel size is the size of one pixel, as a fraction of the screen. "
               "Its y divided by its x is the aspect ratio: width divided by height. Stretch both addresses across by that, and distances come out equal."),
    ("B20", 1, "The shader cannot see your player. So every frame, your game takes the player's position on screen, divides it by the screen size, "
               "and sends it with set shader parameter. Move the player, and the circle follows."),

    # ── ACT III · bend what is behind ──────────────────────────────────────────────────────────────
    ("B21", 2, "So far, each pixel read the screen exactly where it sits. Read somewhere else, and the picture bends. "
               "Add a small number to the address, and every pixel shows what lies a little further right."),
    ("B22", 2, "Make the number depend on the row. Sine is a smooth wave between minus one and one. "
               "Feed it the vertical address, and each row gets a different push, left, then right. Straight lines now ripple."),
    ("B23", 2, "Add time inside the sine, and the ripples travel. Time is seconds on one clock shared by the whole game, so every pixel ripples in step."),
    ("B24", 2, "Keep the push small. It is a fraction of the screen's width. About one hundredth looks like water. "
               "Much more, and the picture stops rippling and starts to tear."),
    ("B25", 2, "You can also read a blurred copy. Add the hint filter linear mipmap, and Godot builds smaller, blurrier copies of the screen. "
               "Read a higher level with texture lod, and you get frosted glass."),
    ("B26", 2, "Which address drives the waves matters. Use the window's own U V, and the ripples ride along when it moves. "
               "Use screen U V, and they stay put on the screen while the window slides over them."),
    ("B27", 2, "A pool is the same trick with a water color. Mix the bent picture halfway toward blue. "
               "The source color hint gives you a color picker in the Inspector, so an artist can change it."),
    ("B28", 2, "A pool needs a top edge. Compare the pool's own vertical address with a sine of its horizontal address. "
               "Above that wavy line, discard the pixel. Discard throws a pixel away, so the grass shows through."),
    ("B29", 2, "Put it together. The pool bends the grass behind it, tints it, and ripples along its own edge. "
               "Scroll the world, and the pool scrolls with it, because its waves belong to the pool."),

    # ── ACT IV · what it can see ───────────────────────────────────────────────────────────────────
    ("B30", 3, "A shader can only read what exists when the copy is taken. Godot takes it once, right before the first reading node on a layer is drawn. "
               "Everything drawn earlier is in it. Everything drawn later is not."),
    ("B31", 3, "To see what is in the copy, put a tiny copy on screen. It shows the mustard block, drawn before it, and not the violet one, drawn after. "
               "Move the lens later, and the violet block appears too."),
    ("B32", 3, "A second reading node on the same layer reuses that copy. Overlap two windows that each flip the colors. "
               "Flipping twice should restore the original. Instead the overlap stays flipped, because the second window never saw the first."),
    ("B33", 3, "The fix is a node called Back Buffer Copy, placed between them, with its copy mode set to Viewport. "
               "It takes a fresh copy of the whole screen right there. Now the overlap flips back to the original colors."),
    ("B34", 3, "A canvas layer takes its own copy. So the gray filter on its own layer sees everything below it, even the pool, "
               "with no Back Buffer Copy. Pool, player and grass all turn gray together."),
    ("B35", 3, "Anything on a higher layer is untouched. Put the health bar on layer two, above the filter, "
               "and it keeps its color while the game turns gray."),
    ("B36", 3, "The docs' examples add two more hints. Repeat disable means reading past the screen's edge gives the edge pixel, not the far side. "
               "Filter nearest asks for the exact pixel, no blending. The Forward Plus renderer obeys; Compatibility blends anyway."),
    ("B37", 3, "Put them together. Water that bends the grass. A spotlight that follows the player. A health bar the filter never touches. "
               "Two shaders, each reading a copy of what was already drawn."),
    ("B38", 3, "When a screen shader misbehaves, check four things. The old name. The draw order. The copy for each layer. "
               "And which layer your health bar sits on."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people think a shader only knows its own sprite. One line of code breaks that rule. "
         "A shader can read what is already on screen, and build on it.")
BIDEA_TEXT = ("A shader only knows\nits own sprite.", "its own sprite", "what is already on screen")

BDEFS = ("Six terms. A texture is an image a shader can read. U V is a point's address on a shape: zero to one across, zero to one down. "
         "A uniform is a value your game sets from outside. Fragment is the function that runs once for each pixel and sets its color. "
         "Draw order is what gets drawn first; later things cover earlier ones. And post-processing is changing the picture after it is drawn.")
BDEFS_TERMS = [
    ("Texture", "an image a shader can read by address"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
    ("fragment()", "runs once for each pixel the shape covers; sets its color"),
    ("Draw order", "what is drawn first; later things cover earlier ones"),
    ("Post-processing", "changing the picture after it is drawn"),
]

BVDT_HEADING = "Reading the Screen"
BVDT_LINES = [
    "The screen texture is a copy of what was drawn so far, read with screen UV.",
    "A color rect on a canvas layer covers every pixel, so one shader can filter the whole game.",
    "Read the screen at a shifted address, and the picture behind it bends.",
    "One copy is made for each layer, so draw order and layers decide what a shader can see.",
]
BVDT_NARRATION = ("Let's recap with Claude. The screen texture is a copy of what was drawn so far, read with screen U V. "
                  "A color rect on a canvas layer covers every pixel, so one shader can filter the whole game. "
                  "Read the screen at a shifted address, and the picture behind it bends. "
                  "One copy is made for each layer, so draw order and layers decide what a shader can see.")

BHTF_PROMPT = ("Write a Godot four canvas item shader for a full-screen color rect that turns everything behind it gray. One float uniform called amount, "
               "from zero to one: at zero nothing changes, at one it is fully gray. Read the screen with a screen texture hint, never the old built-in. "
               "Then point to the line that reads the screen.")
BHTF_CHECKS = ["Check: the line that reads the screen uses a hint screen texture uniform, not SCREEN_TEXTURE.",
               "Check: at amount zero the game is untouched; at one everything, the player too, is gray."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Now check two things yourself. Does the line that reads the screen use a screen texture hint, and not the old name? "
                  "And at zero is the game untouched, and at one is everything gray, the player too?")
BHTF_SEGMENT = "Gray Out the Screen"

CUT_LINE = ("Cut, in this order: the symptom table (B38), the finale (B37), the mouse-filter beat (B13), the edge-and-filter beat (B36) and the "
            "frosted-glass beat (B25): each repeats an idea another beat already carries, or adds a habit rather than the idea. The window (B03 to B09), "
            "the spotlight with its oval fix (B16 to B20), the pool (B27 to B29) and the overlap with its fix (B32, B33) stay: they carry the idea.")

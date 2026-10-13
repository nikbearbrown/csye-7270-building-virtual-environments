"""narration.py: every spoken line of "Local, World and Screen Space". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/, on Forward+ and re-checked on Compatibility), and a third-party course whose ideas were followed and nothing
copied (see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted motion is labelled; the one place the documentation
and the engine disagree (the range of FRAGCOORD) is said aloud with the measured number.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
Built-ins are spoken as plain words: "model matrix", "canvas matrix", "vertex", "frag coord", "screen U V", "screen pixel size",
"texture pixel size". `vec4` is spoken "vec four".
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-local-world-and-screen-space"
TITLE = "Local, World and Screen Space"
TITLE_LINES = ["Local, World and", "Screen Space"]
OPENING_DESCRIPTION = "One point, three sets of numbers, and how to switch"
SUMMARY = ("Learn why one point has three sets of numbers, and how a shader switches between them "
           "to pin an effect to a sprite, the world or the screen.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · SPACES"
TAGS = ["Godot", "Shaders", "Coordinate spaces", "World space", "Screen space", "Local space", "Model matrix", "Canvas matrix",
        "Varying", "Game development", "Nik Bear Brown"]
SOURCE_DOC = ("Godot 4.7 documentation (canvas item shader reference, shading language, viewport and canvas transforms); "
              "Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md")

ACTS = [
    ("I", "Three Addresses"),
    ("II", "From Local to World"),
    ("III", "Locked to the World"),
    ("IV", "Where Is the Screen?"),
    ("V", "Choosing a Space"),
]

BODY = [
    # ── ACT I · three addresses ─────────────────────────────────────────────────────────────────────
    ("B01", 0, "Two sprites, one starfield. The left sprite carries its stars along as it slides. The right one slides over a sky that stays put. "
               "Same picture, same motion. The only difference is what each position is measured from."),
    ("B02", 0, "A position is two numbers, and they mean nothing until you say where zero is. From this zero, the dot is five across and four down. "
               "Move the zero, and the same dot is one across and three down."),
    ("B03", 0, "Godot gives you three zeros that matter. The sprite's own center: local space. The world's origin: world space. "
               "The window's top-left corner: screen space. One corner of one sprite has an address in each."),
    ("B04", 0, "Start local. A sprite's zero sits at its center, and this one is one hundred twenty-eight pixels wide. "
               "So its top-left corner is minus sixty-four, minus sixty-four. Slide the sprite anywhere, and that answer holds."),
    ("B05", 0, "In world space, zero is the world's origin. Put the sprite at six hundred, four hundred, and the same corner reads "
               "five thirty-six, three thirty-six. Slide the sprite, and these numbers change. The local ones did not."),
    ("B06", 0, "On screen, zero is the window's top-left corner, and the camera decides which part of the world the window shows. "
               "With the camera here, the corner lands at two eighty-six, two thirty-six."),
    ("B07", 0, "Pan the camera right by a hundred. The corner slides left on screen, to one eighty-six. Its world address does not move at all. "
               "The window slid over the world, and the world stayed where it was."),

    # ── ACT II · from local to world ────────────────────────────────────────────────────────────────
    ("B08", 1, "A shader starts out in local space. The vertex function runs once for each corner, and a built-in called vertex holds that corner's "
               "position in pixels. Its zero is the node's own: the center of a sprite, the top-left corner of a color rect."),
    ("B09", 1, "Why a matrix at all? Adding the node's position handles a plain shift. Add a turn and a change of size, and the corner lands "
               "somewhere else entirely. One matrix holds the shift, the turn and the size together."),
    ("B10", 1, "That matrix is called model matrix. It stores the node's whole placement: position, turn and size, parents included. "
               "Multiply a corner by it, and the corner's world numbers come out."),
    ("B11", 1, "One warning. The position shown in the editor is measured from the node's parent, not from the world. A child at fifty, zero, "
               "inside a parent at five hundred, three hundred, sits at five fifty, three hundred in the world."),
    ("B12", 1, "Here is that as code. Wrap the corner in a vec four, multiply by the model matrix, and keep the first two numbers. "
               "The result is a vec two: the corner's world position."),
    ("B13", 1, "Why a zero and a one? The matrix keeps the node's shift in its last column. The final one switches that column on, "
               "so the corner counts as a place. With a zero instead, the shift is skipped: a direction, not a place."),
    ("B14", 1, "Fragment runs once for each pixel, and it cannot read this matrix. Ask, and the compiler stops you: unknown identifier. "
               "Only the vertex function can see model matrix. So how does a pixel learn where it is in the world?"),
    ("B15", 1, "With a varying: a value set at each corner, blended across the shape. Vertex stores the world position at the four corners. "
               "The graphics card blends them, so every pixel gets its own world position for fragment to read."),
    ("B16", 1, "Here it is working. The world position becomes the color: red for across, green for down. Slide the sprite, and its colors change, "
               "because the sprite is a window onto a color field that stays where it is."),

    # ── ACT III · locked to the world ───────────────────────────────────────────────────────────────
    ("B17", 2, "Back to the stars. A texture is normally looked up by U V, which is local space squeezed to run from zero to one. "
               "Local in pixels or local in U V, the picture belongs to the sprite."),
    ("B18", 2, "To pin the picture to the world, look it up by world position instead. In the code, one line changes: the varying is set from "
               "the model matrix, not from vertex. Fragment's line stays the same."),
    ("B19", 2, "World position counts pixels, but a texture wants an address from zero to one. So divide by a tile size you choose. "
               "At five hundred twelve, one copy of the picture covers five hundred twelve world pixels, and then the next copy starts."),
    ("B20", 2, "Past one, the address runs off the picture's edge. Mark the texture repeat enable, and the picture tiles forever. "
               "Leave it off, and the edge pixels smear outward, like this."),
    ("B21", 2, "Now slide the sprite. The stars inside do not move; the sprite uncovers different ones as it passes. "
               "A faint copy of the same sky sits behind it, and the two line up exactly."),
    ("B22", 2, "Turn the sprite, or stretch it, and the sky still holds still. World position already includes the sprite's turn and size, "
               "so the pattern ignores both. Only where a pixel sits in the world matters."),
    ("B23", 2, "A shortcut you will see multiplies by texture pixel size instead of dividing by a tile size. That built-in is one over the "
               "sprite's own art size, so swap in smaller art, and the whole pattern shrinks."),
    ("B24", 2, "A world position can also decide what exists. Discard throws a pixel away. Discard everything within sixty pixels "
               "of a fixed point, and the sprite walks across a hole that stays put."),
    ("B25", 2, "Put it together. A mix amount, from zero to one, blends the sprite's own color with the sky. Animate it up as the sprite walks, "
               "and the character turns into a window onto the stars."),

    # ── ACT IV · where is the screen? ───────────────────────────────────────────────────────────────
    ("B26", 3, "Some effects belong to neither the sprite nor the world. A darkened edge, a damage flash: they stay on the glass "
               "wherever the camera points. They need the pixel's screen address, and there are four ways to read it."),
    ("B27", 3, "The first way you already know: the canvas matrix turns world numbers into screen numbers. The camera lives in it: "
               "pan or zoom, and only this matrix changes. Godot's reference calls the result canvas space."),
    ("B28", 3, "Chain the two: canvas matrix times model matrix times the corner. Read it right to left, so the corner meets the model matrix first. "
               "With the camera zoomed in on the sprite, the corner lands at five twelve, two thirty-two."),
    ("B29", 3, "Swap the order and the answer is wrong, not slightly off. The same corner now lands at minus eighty-eight, minus one sixty-eight, "
               "far outside the window. Order matters."),
    ("B30", 3, "The second way is shorter. Inside fragment, vertex means something new: not the local corner, but the pixel's screen position, "
               "in pixels. Same name, different space, so check which function you are in."),
    ("B31", 3, "The third is frag coord: the pixel's place in the window, counted in pixels. The reference page says its far corner is one, one. "
               "Measured here, in a twelve-eighty by seven-twenty window, the last pixel reads twelve seventy-nine point five."),
    ("B32", 3, "The fourth is screen U V: the same place as a fraction, from zero to one. Screen pixel size is one over the window's size, "
               "so pixels times it give that same fraction."),
    ("B33", 3, "Four tiles, one method each, each painting itself with its own screen address. Watch the gradient grow tile by tile. "
               "If any method disagreed, a seam would show. There is none: all four agree."),
    ("B34", 3, "A pixel here is a real window pixel. In canvas items stretch mode, doubling the window doubles the sprite's width in screen pixels, "
               "while its world numbers stay put. A fraction of the screen, from screen U V, does not care."),

    # ── ACT V · choosing a space ────────────────────────────────────────────────────────────────────
    ("B35", 4, "So which space? Ask what the effect should stay stuck to. The sprite: local. A place in the level: world. The glass: screen. "
               "One experiment tells you which you built: slide the sprite, then pan the camera."),
    ("B36", 4, "Three sprites, the same stripes, three spaces. Slide them right. The local stripes ride along with their sprite. "
               "The world and screen stripes stay put, and each sprite slides over them."),
    ("B37", 4, "Now leave the sprites and pan the camera. The local and world stripes travel with their sprites, because both belong to the world. "
               "Only the screen stripes stay on the glass. Two moves tell all three apart."),
    ("B38", 4, "Here is the map. Local numbers come straight from vertex. World numbers come from the model matrix. Screen numbers come from the "
               "canvas matrix, or ready-made from screen U V. Say which space you mean, and the code follows."),
    ("B39", 4, "The code barely changes. The line that sets the position picks the space: vertex for local, the model matrix for world. "
               "For the screen, read screen U V in fragment instead."),
    ("B40", 4, "This is also how to check a shader an AI wrote for you. It can compile, look right in a still, and be stuck to the wrong thing. "
               "Slide the sprite, pan the camera, and watch where the pattern goes."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. A shader is handed a position, and it is tempting to treat that as a plain fact. It is not. "
         "A position is an address in some space, and the same point has a different address in every space.")
BIDEA_TEXT = ("A position is just a position.", "just a position", "an address in some space")

BDEFS = ("Six terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture on screen. "
         "An origin is where the numbers are zero. A space is a way of measuring positions from one origin. A vertex is a corner point of a shape. "
         "And a texture is an image a shader can read by address.")
BDEFS_TERMS = [      # the card shows the GLOSSARY.md wording word for word (vector is defined in B12, matrix in B09, where each is first spoken)
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Pixel", "one dot of the picture on screen"),
    ("Origin", "where the numbers are zero; the middle of a centered sprite"),
    ("Space", "a way of measuring positions from one origin"),
    ("Vertex", "a corner point of a shape"),
    ("Texture", "an image a shader can read by address"),
]

BVDT_HEADING = "Local, World and Screen Space"
BVDT_LINES = [
    "A position is an address, and each space has its own zero.",
    "The model matrix turns local numbers into world numbers, and a varying carries them to fragment.",
    "Look a texture up by world position and it stays put while the sprite moves.",
    "Four ways read a pixel's screen address, and all four agree.",
    "Slide the sprite, then pan the camera, to see which space a pattern is stuck to.",
    "Pick the space the effect should stay stuck to.",
]
BVDT_NARRATION = "Let's recap with Claude. " + " ".join(BVDT_LINES)

BHTF_PROMPT = ("Write a Godot canvas item shader for a sprite: white vertical stripes, thirty-two pixels wide, over the sprite's own colors. "
               "Fix the stripes to the world, not to the sprite or the screen. Then show me what to change to fix them to the screen instead.")
BHTF_CHECKS = ["Check: slide the sprite, and the stripes hold still.",
               "Check: pan the camera, and the stripes travel with the sprite."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Slide the sprite: do the stripes hold still? "
                  "Pan the camera: do the stripes travel with the sprite?")
BHTF_SEGMENT = "Pin Stripes to the World"

CUT_LINE = ("Cut, in this order: the hole beat (B24), the wrong-order beat (B29), the turn-and-stretch beat (B22) and the parents warning (B11): "
            "each repeats an idea another beat carries, and none leans on its neighbours. Only if that is not enough, drop the frag coord beat (B31) "
            "and its tile in capture C10, and change 'four' to 'three' in B26 and B33 and the counting words in B30 to B32 (re-voice those beats). "
            "The sky window (B21), the world colors (B16), the four-tile agreement (B33) and the two-move test (B36, B37) stay: "
            "they are the proof and the payoff.")

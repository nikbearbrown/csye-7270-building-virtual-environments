"""narration.py: every spoken line of "SubViewports". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13: the Using Viewports tutorial and the SubViewport, ViewportTexture, Viewport, QuadMesh, PlaneMesh,
MeshInstance2D and canvas item shader pages), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in evidence/planning-checks/,
Forward+ and Compatibility), the real editor's Inspector (labels read from the editor itself), and a long third-party course on 2D shaders in Godot
(ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted motion is labelled; a capture is an offline render at a fixed tick rate
and says nothing about real-time frame rate.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
Node and property names are written as separate words ("Sub Viewport", "Viewport Texture", "Mesh Instance two D") for the voice; the screen shows the real names.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-subviewports"
TITLE = "SubViewports"
SPOKEN_TITLE = "Sub Viewports"                  # the voice reads the one-word title unpredictably; the body says "Sub Viewport" as two words, so the title does too (see CHECKS-REPORT.md)
TITLE_LINES = ["SubViewports"]
OPENING_DESCRIPTION = "Draw into a picture, then shade the picture"
SUMMARY = "Learn how a Sub Viewport draws part of your game into a picture, and how to shade that picture with a second shader."
BOPEN = S.bopen(SPOKEN_TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · SUBVIEWPORTS"
TAGS = ["Godot", "Shaders", "SubViewport", "ViewportTexture", "Premultiplied alpha", "HSV", "Vertex shader", "MeshInstance2D", "Render target", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs and editor frames on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "A Picture Off to the Side"),
    ("II", "Two Shaders, One Result"),
    ("III", "Stripes and Hue"),
    ("IV", "Wobble the Result"),
]

BODY = [
    # ── ACT I · a picture off to the side ───────────────────────────────────────────────────────────
    ("B01", 0, "A sprite spins. Rainbow stripes slide across it, and a ripple runs through the whole picture. Two shaders made this, one after the other. The second shades what the first one drew. The trick is drawing into a picture, not onto the screen."),
    ("B02", 0, "That picture comes from a Sub Viewport: a node that draws its children into a picture of its own, not onto the screen. Drawn, but not shown directly: that is what off-screen means. Sprites, text, interface, even a three-D scene can go inside."),
    ("B03", 0, "On its own, a Sub Viewport shows nothing. Its picture is a Viewport Texture: a texture that keeps the latest drawing. Give that texture to a sprite, and the sprite shows the picture."),
    ("B04", 0, "In the editor, add a Sub Viewport node and give it a size. Put a sprite inside it. Add a second sprite outside. In the second sprite's Texture slot, open the menu, and under New choose Viewport Texture. Then pick the Sub Viewport."),
    ("B05", 0, "In code, it is five lines. Make the viewport, give it a size, add it to the scene, put the sprite inside, and hand its texture to the display."),
    ("B06", 0, "The size is the picture's resolution, in pixels. A new Sub Viewport is five hundred twelve pixels square. Shrink it to a hundred twenty-eight, draw it four times bigger, and the pixels show. Set the sprite's Filter to Nearest, and they turn into crisp blocks."),
    ("B07", 0, "Inside the viewport, the top-left corner is the origin, and the picture covers only positive x and y from there. A centered sprite placed at zero, zero has three quarters of itself outside. The eyes are gone."),
    ("B08", 0, "Slide it to the middle, and all of it appears. Slide it off an edge, and it is cut off. The picture is only as big as the viewport, and anything outside is not in it at all."),
    ("B09", 0, "See the box around the sprite? That is the picture's background, filled with the project's clear color. Turn on Transparent B G, and the empty parts become see-through. Now whatever is behind the picture shows through."),
    ("B10", 0, "One catch with see-through pictures, which hard edges hide. A half-transparent pixel is stored already multiplied by its alpha. Draw it the usual way, and soft edges come out too dark. Set the Blend Mode to Premultiplied Alpha, and they come out right."),

    # ── ACT II · two shaders, one result ─────────────────────────────────────────────────────────────
    ("B11", 1, "Now give each side a shader. The inner shader sits on the sprite inside the viewport. The outer shader sits on the sprite that shows the picture. The inner one draws first. The outer one gets the finished picture."),
    ("B12", 1, "In the editor, that is each sprite's Material slot. The inner sprite's Material holds a Shader Material with the inner shader. The display's Material holds one with the outer shader. Each shader sits on its own node."),
    ("B13", 1, "The inner shader is an ordinary one. Its fragment function runs once for each pixel and sets the color. This one blends the sprite from teal at the top to gold at the bottom, using U V, the sprite's own address."),
    ("B14", 1, "The outer shader gets the picture as its texture. It starts with one line that sets Premultiplied Alpha, and one line that copies the picture through unchanged. The result matches the picture exactly. Everything the inner shader made is already in there."),
    ("B15", 1, "Now change something only the outer shader can. Multiply the picture by U V x, and it fades from nothing at the left edge to full at the right. Multiply the whole color, not only the alpha, because the picture's colors already carry their alpha."),
    ("B16", 1, "Here is a question. The sprite now turns inside the viewport. Which effect turns with it: the inner gradient, the outer fade, or both? Decide before you look."),
    ("B17", 1, "The gradient turns with the sprite. The fade stays put. A shader's U V belongs to the thing it draws. The inner shader draws the sprite, and the sprite turns. The outer shader draws the picture, and the picture does not."),
    ("B18", 1, "Add a second sprite, and the same fade runs across both. The outer shader does not know how many things are inside. It sees one picture. Put a fade on each sprite instead, and every sprite starts over at its own edge."),
    ("B19", 1, "That is also the limit. By the time the outer shader runs, the sprites are gone. Only their pixels remain, already flattened together. It cannot ask a sprite where it is, or reach what hides behind another."),
    ("B20", 1, "Resolution splits the same way. The inner shader works in the picture's pixels. The outer shader works in the display's pixels. Here a small picture is drawn big under an outer shader that draws stripes: the picture is coarse, the stripes are sharp."),

    # ── ACT III · stripes and hue ────────────────────────────────────────────────────────────────────
    ("B21", 2, "A fade is one kind of mask. Stripes are another. Start with a diagonal: add the two U V numbers together. The sum climbs from zero at the top left to two at the bottom right, and equal values line up along diagonals."),
    ("B22", 2, "Fract keeps only what comes after the decimal point. Feed it a climbing number and you get a saw: up from zero to one, drop back, climb again. Multiply first, and the saw repeats faster. Times six, six saws."),
    ("B23", 2, "Step makes a hard edge: zero while the saw is below the width, one once it passes. Take that from one, and you get a stripe: on while the saw is under the width. A wider width means thicker stripes."),
    ("B24", 2, "Put it together in the outer shader. Multiply the picture by the stripe, and the sprite shows only inside the stripes. Count and width are uniforms: values your game sets from outside, from the Inspector or from code."),
    ("B25", 2, "To move them, subtract time. Time is the seconds on one clock shared by the whole game. Take speed times time off the diagonal, and every stripe slides along it, while the sprite turns underneath."),
    ("B26", 2, "Now color. Screens mix red, green and blue, but people think in hue, saturation and value. Hue is the angle around a color wheel: which color. Saturation is how far from grey. Value is how bright."),
    ("B27", 2, "Call the hue a number from zero to one, once around the wheel. Zero is red. A sixth is yellow, a third is green, a half is cyan, two thirds is blue, five sixths is magenta. Then it wraps back to red."),
    ("B28", 2, "Red, green and blue each follow the same plateau around the wheel: full for a third, zero for a third, with ramps between. Green is red's plateau pushed a third along. Blue is pushed two thirds."),
    ("B29", 2, "In code, an absolute value and a clamp build the plateau, and fract wraps the hue. Mixing toward white sets the saturation, and the value scales the result. Tested at the six hues, it gives pure red, yellow, green, cyan, blue and magenta."),
    ("B30", 2, "Now give the stripes a hue. Use the diagonal itself as the hue, and each stripe cuts out a band of the rainbow. The diagonal slides with time, so the colors travel with the stripes."),

    # ── ACT IV · wobble the result ───────────────────────────────────────────────────────────────────
    ("B31", 3, "A shader can move corners too. Its vertex function runs once for each vertex, each corner of a shape, and sets where it goes. A sprite has four corners, so it can lean, but it cannot bend."),
    ("B32", 3, "To bend a picture, give it more corners. A Quad Mesh, drawn by a Mesh Instance two D node, is a rectangle you can cut into a grid. Thirty-one cuts each way makes one thousand and eighty-nine corners."),
    ("B33", 3, "Same wobble, two meshes. On a plain quad, only four corners move, so the edge stays straight. On the grid, every corner moves on its own, and the edge becomes a wave."),
    ("B34", 3, "The wobble is one line in the outer shader's vertex function. Move each corner up or down by a sine of its U V x, plus time. Sine swings smoothly between minus one and one, and amplitude sets how far."),
    ("B35", 3, "One catch in two-D. A Quad Mesh is built for three-D, where y points up, but in two-D y points down, so the picture lands upside down. Give the Quad Mesh a negative height, and it lands upright."),
    ("B36", 3, "So the chain is this. Nodes draw into the viewport, and the inner shader colors them. The outer shader paints stripes on the picture and bends it. The sprite inside knows nothing about either."),
    ("B37", 3, "Nothing stops at two. Show a picture inside another Sub Viewport, and that picture can take a third shader. Each stage is a picture, and the next stage shades it."),
    ("B38", 3, "It is not free. A Sub Viewport is a picture the engine draws every frame it is shown. For a picture that never changes, set Update Mode to Once. It draws one time, then keeps that picture, however much the sprite inside moves."),
    ("B39", 3, "One more limit. Mouse and key events do not reach a standalone Sub Viewport. Put it inside a Sub Viewport Container, and the container passes them in. Without that, a button inside the picture will not respond."),
    ("B40", 3, "The picture is only a texture, so it fits wherever a texture does. A sprite, a panel in your interface, a flat plane in a three-D scene, or a sampler in any other shader. One picture, four places."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people think shaders cannot see each other's work: one shader, one node, and no way to build on what another drew. "
         "A Sub Viewport changes that. One shader can shade the picture another shader made.")
BIDEA_TEXT = ("Shaders cannot see\neach other's work.", "cannot see", "can build on")

BDEFS = ("Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A texture is an image a shader can read. "
         "A viewport is a rectangle the engine draws into. U V is a point's address on a shape. And alpha is how visible a pixel is.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Texture", "an image a shader can read by address"),
    ("Viewport", "a rectangle the engine draws into"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Alpha", "how visible a pixel is: 0 invisible, 1 solid"),
]

BVDT_HEADING = "SubViewports"
BVDT_LINES = [
    "A Sub Viewport draws its children into a picture, and a Viewport Texture shows it anywhere.",
    "An inner shader makes the picture, and an outer shader shades it, using the picture's own UV.",
    "Stripes are a saw wave cut by a step, and a hue function colors them.",
    "Cut a mesh into a grid, and the outer vertex function can bend the whole picture.",
]
BVDT_NARRATION = ("Let's recap with Claude. A Sub Viewport draws its children into a picture, and a Viewport Texture shows it anywhere. "
                  "An inner shader makes the picture, and an outer shader shades it, using the picture's own U V. "
                  "Stripes are a saw wave cut by a step, and a hue function colors them. "
                  "Cut a mesh into a grid, and the outer vertex function can bend the whole picture.")

BHTF_PROMPT = ("Write a Godot four scene as a text file. A Sub Viewport, five hundred twelve pixels square with a transparent background, holds the Godot icon, its lower half painted red by its own shader. "
               "A second sprite shows the viewport's texture with Premultiplied Alpha, and its shader keeps only vertical stripes. Also tell me where each shader goes.")
BHTF_CHECKS = ["Check: with the outer shader off, the picture shows the icon with its lower half red, and no box around it.",
               "Check: turn the icon inside the viewport. The red turns with it, and the stripes stay still."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. With the outer shader off, is the icon's lower half red, with no box around it? "
                  "And when you turn the icon, do the stripes stay still?")
BHTF_SEGMENT = "Stripe a Turning Icon"

CUT_LINE = ("Cut, in this order: the input beat (B39), the update-mode beat (B38), the three-in-a-row beat (B37), the per-pixel beat (B20), then the hue beats (B26 to B29), "
            "keeping the stripes at one color. The origin and cut-off pair (B07, B08), the dark-edges beat (B10), the predict-and-reveal pair (B16, B17) and the wobble beats "
            "(B33 to B35) stay: they are the proof and the payoff.")

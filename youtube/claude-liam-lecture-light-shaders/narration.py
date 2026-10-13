"""narration.py: every spoken line of "Light Shaders". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party long course whose ideas this film follows (nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted runs are labelled; screen-space numbers are window pixels.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
Identifiers are written as the words the voice should say (light color, light energy); the screen shows them in capitals.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-light-shaders"
TITLE = "Light Shaders"
TITLE_LINES = ["Light Shaders"]
OPENING_DESCRIPTION = "Take over what a light does to every pixel"
SUMMARY = "Learn what the light function does and what Godot hands it, then use it to build a sweeping lighthouse beam and a ring that spreads from a lamp."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · LIGHT"
TAGS = ["Godot", "Shaders", "2D lights", "Light shader", "PointLight2D", "GDScript", "Game development", "Fragment shader", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Lights in 2D"),
    ("II", "The Light Function"),
    ("III", "Which Way Is the Light?"),
    ("IV", "A Lighthouse"),
    ("V", "Where Is the Light?"),
]

BODY = [
    # ── ACT I · Lights in 2D ───────────────────────────────────────────────────────────────────────
    ("B01", 0, "In a two-D game, a light is a soft glow. Same scene, same light, and one function later, that glow is a beam sweeping the ground. The function is called light, and before this film ends, you will have written it."),
    ("B02", 0, "Godot has two kinds of two-D light. A point light shines out from one spot, like a lamp. A directional light shines the same way everywhere, like the sun. This film works mostly with the lamp."),
    ("B03", 0, "A light needs a dim scene to show against. A two-D scene starts fully lit, so a light can only brighten what is already bright. Add a Canvas Modulate node, which tints everything, and set it dim. That tint is the ambient light."),
    ("B04", 0, "A soft glow is a texture. Godot's docs give the recipe. Give the light a gradient texture, set its fill to radial, and run the gradient from opaque white to transparent white. The transparent part becomes the soft edge."),
    ("B05", 0, "A point light has a few settings. Its texture sets its shape. Its scale sets how far it reaches. Color tints it, and energy is how strong it is. Change each one, and the same lamp lights the same ground differently."),
    ("B06", 0, "Lights add. Two lamps overlapping make the overlap brighter, and three make it brighter still. Underneath, the dim ambient stays put, whether a light reaches a pixel or not."),
    ("B07", 0, "Godot's rule, measured. The pixel is the surface color times the total of the ambient and every light. A grey surface of one half, an ambient of point two, two lamps of point four each: the pixel reads one half."),
    ("B08", 0, "A two-D shader can have three functions. Vertex places corners, and fragment colors each pixel. The third, light, runs for every pixel and every light that reaches it, and asks: how much does this lamp add here?"),

    # ── ACT II · The Light Function ────────────────────────────────────────────────────────────────
    ("B09", 1, "Add a function called light to a shader, and it replaces Godot's default lighting for that sprite. Even an empty one. The lamp still lights the blob, but the ground ignores it. The function belongs to the sprite, not to the lamp."),
    ("B10", 1, "The smallest light function returns one flat answer: point two grey. Add a lamp, and this card brightens by point two. Add another, and it brightens again. Light runs once for each lamp, and Godot adds the answers."),
    ("B11", 1, "Inside light, Godot hands you built-ins, values written in capital letters. Color is this pixel's own color, and U V is its address. Light color and light energy describe the lamp. You hand back one value, also called light: what this lamp adds."),
    ("B12", 1, "Light runs last. Fragment runs first and sets the pixel's color, which arrives in light as the built-in color. Then light runs once for each lamp, and Godot adds all the answers to the dim ambient look. That sum is the pixel."),
    ("B13", 1, "Rebuild Godot's default. The color is the surface, times the lamp's color, times its energy. The fourth number, alpha, passes straight through. Rendered both ways, the same scene differs in no pixel at all."),
    ("B14", 1, "That fourth number is the lamp's soft edge: the texture fades from one to zero. Force it to one, and every pixel the texture covers is lit at full strength. The soft glow becomes a hard square."),
    ("B15", 1, "Now reshape it. Round the fade down to quarters, and the glow becomes bands, like cel shading. Same lamp, same ground. Only the light function changed how the light fades."),
    ("B16", 1, "Or let time shape it. Multiply the light by the absolute value of a sine of time, and the lamp breathes. No animation player and no game code: the shader does it every frame."),
    ("B17", 1, "One more switch. Put render mode unshaded at the top, and the sprite ignores every light, and the ambient tint too. That is right for the lamp's own bulb. Otherwise it goes dim with the room."),
    ("B18", 1, "One caution. This copy matches the default, shadows included. But the default also reads normal maps, images that say which way each pixel faces, and this copy ignores them. The docs show the extra term that fixes it. Change one thing at a time."),

    # ── ACT III · Which Way Is the Light? ──────────────────────────────────────────────────────────
    ("B19", 2, "Now, direction. Light direction is a vector, an arrow from this pixel toward the lamp, always length one. A pixel left of the lamp gets an arrow pointing right. A pixel above it gets an arrow pointing down."),
    ("B20", 2, "To see a number, use it as brightness. Take the arrow's x number, from minus one to one, and squeeze it into zero to one. Multiply the lamp by it. Left of the lamp, full strength. Right of the lamp, nothing."),
    ("B21", 2, "Turn that number into a mask with step. Step gives zero below an edge, and one at or above it. Use an edge of zero, multiply the light by the result, and only the left half of the lamp stays on."),
    ("B22", 2, "Take the absolute value, and both sides count. Raise the edge close to one, and only pixels where the arrow is nearly sideways survive. That leaves a wedge on the left, and a wedge on the right."),
    ("B23", 2, "A directional light is different. Its arrow is the same for every pixel on screen, and its position is always zero. So a direction mask lights everything or nothing. For a beam, use a point light."),

    # ── ACT IV · A Lighthouse ──────────────────────────────────────────────────────────────────────
    ("B24", 3, "To aim a beam, you need an arrow of your own. Cosine and sine of an angle make one, always length one. Turn the angle, and the arrow turns with it."),
    ("B25", 3, "Then compare two arrows with the dot product. It is one when they point the same way, zero at right angles, and minus one when they point opposite ways. Keep the pixels where it is close to one."),
    ("B26", 3, "Let time turn the angle, and the wedge turns with it: a lighthouse. Two details. Our arrow points at the lamp, so flip its sign. And because y points down, a growing angle turns the beam clockwise."),
    ("B27", 3, "Make the cutoff, the number inside step, a uniform: a dial your game sets from outside. Lower it, and the beam widens. Raise it, and the beam narrows."),
    ("B28", 3, "Swap step for smooth step, which ramps between two edges instead of cutting, and the edge of the beam goes soft. Same lamp, same beam, a better look."),
    ("B29", 3, "Add a second lamp, and light runs again for it, with its own arrows. Two beams from one shader, each starting at its own lamp, each in its own color, and no extra code."),
    ("B30", 3, "A beam exists only where a lamp reaches. Outside the lamp's texture, Godot never calls light at all. For a longer beam, scale the lamp, not the shader."),

    # ── ACT V · Where Is the Light? ────────────────────────────────────────────────────────────────
    ("B31", 4, "Two more numbers. Light position is where the lamp is, and light vertex is where this pixel is. Both are in screen space: pixels of the window, counted from the top left, with y growing downward."),
    ("B32", 4, "Subtract the lamp's position from the pixel's, and you get an arrow from the lamp to this pixel. Its length is the distance between them, in pixels. That is what the length function measures."),
    ("B33", 4, "Use that distance as brightness. Nothing at the lamp, a little more with every step away. Now every pixel knows exactly how far it is from the light."),
    ("B34", 4, "Step the distance against a radius, and the ground splits in two: inside and outside. Do it for two radii, subtract one from the other, and what is left is the band between them. A ring."),
    ("B35", 4, "Put it together, and the lamp lights only a band of ground: the distance, two steps, one subtraction, multiplied into the light. The radius and the thickness are uniforms, so the game can change both."),
    ("B36", 4, "Now the game drives it. A tween moves a value smoothly over time. Set the radius to zero from code, then tween it out to the edge of the lamp, and a ring spreads from the light. This run is scripted, not player input."),
    ("B37", 4, "One warning. These are window pixels, so the ring does not follow your world. Zoom the camera in, and the ground doubles in size, but a ring of four hundred fifty pixels stays four hundred fifty pixels."),
    ("B38", 4, "One more tool: mod. It counts up to a number, then starts over. Mod the pixel's x by one hundred twenty-eight, keep the first sixteen, and you get stripes. They belong to the screen, not the sprite: slide the ground, and they stay put."),
    ("B39", 4, "Do the same for y, and join the two with max. You get a grid of light: lines sixteen pixels wide, every one hundred twenty-eight pixels, drawn only where the lamp reaches."),
    ("B40", 4, "So when does a job belong in light? When it depends on a lamp: its direction, its distance, its color. A pattern on the surface alone belongs in fragment, and a wobble in the corners in vertex. Ask where the effect comes from."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Lighting in a two-D game feels built in: you place a light, and Godot does the rest. "
         "Most people think that is where your control ends. It is not. A shader can replace it.")
BIDEA_TEXT = ("Lighting is built in.\nYou can't touch it.", "You can't touch it", "A shader can replace it")

BDEFS = ("Six terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. "
         "A texture is an image a shader can read. The canvas is the surface two-D things are drawn on. A vector is a bundle of two to four numbers. "
         "And a mask is a number from zero to one, for each pixel, saying how much of something to show.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Pixel", "one dot of the picture on screen"),
    ("Texture", "an image a shader can read by address"),
    ("Canvas", "the surface that 2D things are drawn on"),
    ("Vector", "a bundle of two to four numbers"),
    ("Mask", "a number from 0 to 1 per pixel saying how much of something to show"),
]

BVDT_HEADING = "Light Shaders"
BVDT_LINES = [
    "A pixel is its surface times the total of the ambient and every light.",
    "Writing light replaces the default, and you can rebuild it exactly.",
    "Light direction is an arrow from the pixel toward the lamp.",
    "Aim an arrow, compare it with a dot, and a mask becomes a beam.",
    "Light position and light vertex give a distance, and distance makes rings.",
    "Those positions are window pixels, so they ignore your camera zoom.",
]
BVDT_NARRATION = "Let's recap with Claude. " + " ".join(BVDT_LINES)

BHTF_PROMPT = ("Write a Godot canvas item shader with a light function, for a sprite. A narrow beam sweeps clockwise around the lamp, once every two seconds. "
               "Use the built-in light direction and the built-in time, and keep the lamp's soft edge, color and energy. Add a uniform called width. "
               "Then point me to the lines that decide where the beam is.")
BHTF_CHECKS = ["Check: the beam turns clockwise, once every two seconds, by your own stopwatch.",
               "Check: delete the light node, and the beam disappears."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does the beam turn clockwise, once every two seconds, by your own stopwatch? "
                  "And when you delete the light node, does the beam disappear?")
BHTF_SEGMENT = "Build a Lighthouse Beam"

CUT_LINE = ("Cut, in this order: the grid beat (B39), the stripes beat (B38), the pulse beat (B16), then the limits beat (B18). Each repeats an idea "
            "another beat already carries, or sits outside the film's one idea. The rebuild (B13), the lighthouse (B26) and the expanding ring (B36) "
            "stay: they are the proof and the two payoffs.")

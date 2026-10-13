"""narration.py: every spoken line of "Reflections". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), and a third-party video course on 2D shaders whose ideas this film follows (nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input is labelled; nothing about speed is claimed
(the cost of a screen copy was not measured).
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
Node names are spoken as words (Back Buffer Copy, Remote Transform two D); the screen shows them exactly as Godot spells them.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-reflections"
TITLE = "Reflections"
TITLE_LINES = ["Reflections"]
OPENING_DESCRIPTION = "How a hidden map makes a reflection in Godot"
SUMMARY = "Learn how a shader can read a hidden map of the water, and use it to give a character a reflection that shows only over water."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · THE SCREEN TEXTURE"
TAGS = ["Godot", "Shaders", "BackBufferCopy", "Screen texture", "Reflection", "Water", "RemoteTransform2D", "GDScript", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "A Map Nobody Sees"),
    ("II", "When the Screen Is Copied"),
    ("III", "Building the Reflection"),
    ("IV", "Compare With a Range"),
    ("V", "Polish and Limits"),
]

BODY = [
    # ── ACT I · a map nobody sees ───────────────────────────────────────────────────────────────────
    ("B01", 0, "Watch the reflection. The character walks along the shore, and its reflection follows in the water. Over the sandbar, the reflection disappears. No script decides that. A shader looks up a map the player never sees."),
    ("B02", 0, "A shader works one pixel at a time. For each pixel of the reflection, it has to decide: show this pixel, or hide it. To decide, it needs one fact. Is there water under me?"),
    ("B03", 0, "Here is that fact, drawn as a map. Water is red. The coast is green. Everything else is left empty. Each flat color is a label, so this picture is a label map."),
    ("B04", 0, "You could hand this map to the shader as an ordinary texture. Then, for every pixel, you must work out where it sits on the map, whatever the camera is doing. The screen is already lined up with every pixel."),
    ("B05", 0, "There is one problem. Draw the map over the game, and the player sees a red and green sea. The shader should read the map. Nobody else should."),
    ("B06", 0, "The fix is draw order. A game paints in layers, and later layers cover earlier ones. Paint the map first and the art second, and the art covers it. The player sees only the art."),
    ("B07", 0, "A shader reads the screen texture: a copy of the screen made at one moment. Make it after the art, and the map is gone. Make it before the art, and the map is still in it."),
    ("B08", 0, "Godot has a node for choosing that moment: Back Buffer Copy. It makes its copy at its own place in the draw order."),
    ("B09", 0, "And the draw order is the scene tree. The top of the Scene dock is drawn first. So the order is: map, copy node, art, character, reflection."),

    # ── ACT II · when the screen is copied ──────────────────────────────────────────────────────────
    ("B10", 1, "Three flat sprites: A drawn first, then B, then C on top. The window shows what a shader reads when it asks for the screen texture. A hint after the colon tells Godot to fill it with the screen."),
    ("B11", 1, "By default, Godot makes that copy the first time a shader asks for it, right before that shader's node is drawn. So the shader sees everything drawn before it, and nothing after."),
    ("B12", 1, "Now add a Back Buffer Copy. After C, the window shows all three. Move it between B and C, and C vanishes from the window. C is still on the screen. It is only missing from the copy."),
    ("B13", 1, "Between A and B, only A is left. Before A, the window is empty. The node never changes what is drawn. It only changes what the copy contains."),
    ("B14", 1, "Only the first shader that reads the screen triggers a copy. Here it sits before C, so it misses C. The second shader, after C, reuses that copy and misses C too. A new Back Buffer Copy between them refreshes it."),
    ("B15", 1, "Tree order is not the only lever. Z index and canvas layers change the draw order too, and the copy follows them. But a copy only serves shaders on its own canvas layer."),
    ("B16", 1, "Back Buffer Copy has three modes. Viewport copies the whole screen. Rect copies only a box. Disabled copies nothing, so Godot falls back to its automatic copy."),
    ("B17", 1, "A new Back Buffer Copy starts in Rect mode. The box covers only a corner of the screen, wherever the node is. Outside it, the docs call the result undefined. Here the window reads black until the mode becomes Viewport."),
    ("B18", 1, "In the editor, select the node and set Copy Mode to Viewport. If the map spreads over the whole screen, that is the safe choice."),

    # ── ACT III · building the reflection ───────────────────────────────────────────────────────────
    ("B19", 2, "Back to the pond. A reflection is the character again: the same picture, flipped upside down, placed right under its feet. On a Sprite two D, switch on the vertical flip."),
    ("B20", 2, "To keep it in step, give the character a Remote Transform two D. It pushes the character's position to another node whenever the character moves, so the reflection can sit anywhere in the tree."),
    ("B21", 2, "Walk the character along the shore and the reflection follows, but it knows nothing about water. Over the sandbar, it hangs in the sand. Something has to hide it there."),
    ("B22", 2, "So the shader on the reflection looks up the same spot in the screen texture, using screen U V: a pixel's address on the whole screen. That texture holds the map, so the spot holds the label."),
    ("B23", 2, "The color it finds is the label. If it is close to red, this pixel is over water, so keep it. If not, set its alpha, how visible the pixel is, to zero."),
    ("B24", 2, "Here is the proof that the map is hidden. Switch the Label Map node off, and the picture does not change, except the reflection is gone. The map is invisible, and it is doing the work."),
    ("B25", 2, "If the reflection never shows, check the order. Copy after the art: the shader reads the art, finds no red, and hides everything. Map over the art: the reflection works, and so does the red sea."),
    ("B26", 2, "The art must be opaque. At ninety percent, the red and green show through faintly, and the ring around the sandbar gives it away. Cover the map completely, or the player will see it."),

    # ── ACT IV · compare with a range ───────────────────────────────────────────────────────────────
    ("B27", 3, "A moment ago, the shader asked whether the color was close to red, not equal to red. That was on purpose. Godot's documentation warns that comparing decimal numbers with equals may not come out true. Compare against a range."),
    ("B28", 3, "Here is what goes wrong with equals. Same pond, but the water is painted at half strength, and the shader asks for exactly point five. Nothing matches, so the reflection never shows."),
    ("B29", 3, "Ask for a distance instead, and the same map works. How far is this color from half red? Within a tenth counts as water. The reflection is back."),
    ("B30", 3, "Why did equals fail? The screen stores each color channel in eight bits, so two hundred fifty-six steps. Half strength lands on step one hundred twenty-eight, which reads back as point five oh two. Not point five."),
    ("B31", 3, "You can make equals pass by writing one hundred twenty-eight over two hundred fifty-five. It passed in Forward Plus and failed in Compatibility. The distance passed in both."),
    ("B32", 3, "Think of a color as a point. Red is one corner, green another. A radius of a tenth around each is wide enough to catch the painted color, and narrow enough to keep red and green apart."),
    ("B33", 3, "Better still, paint the map in pure values, zero or full. They read back the same in both renderers, and with the H D R two D setting on. Half strength does not: point five oh two normally, point two one six with it on."),

    # ── ACT V · polish and limits ───────────────────────────────────────────────────────────────────
    ("B34", 4, "Now the coast. Paint it green, read it the same way, and give it a lower alpha. The shader adds the two. The reflection is stronger in open water and fainter around the sandbar."),
    ("B35", 4, "Last, a tint. Mix blends two colors by an amount. Here it is halfway toward blue. Now the reflection reads as water, not as a second character."),
    ("B36", 4, "Two limits. This reflects the character only, so the sky and the shore are not in it. Mirroring the whole screen is a different technique."),
    ("B37", 4, "And the reflection moves with the character. When the character jumps, the reflection rises too, where a real one would drop, and the shoreline cuts it off."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people think a reflection means drawing the scene a second time. You do draw the character twice. "
         "But the hard part is knowing where the water is, and a shader can learn that from a map.")
BIDEA_TEXT = ("A reflection needs\na second drawing of the scene.", "a second drawing of the scene", "a map the shader can read")

BDEFS = ("Five terms. A shader is a small program the graphics card runs to decide how something is drawn. "
         "The screen texture is a picture of what has been drawn so far, which a shader can read. Draw order says which things are drawn first. "
         "A label map is a layer of flat colors, each color a label. And a reflection is a flipped, fainter copy, seen in water.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Screen texture", "a copy of the screen made at one moment, which a shader can read"),
    ("Draw order", "what is drawn first; later things cover earlier ones"),
    ("Label map", "a layer of flat colors, each color a label"),
    ("Reflection", "a flipped, fainter copy seen in water"),
]

BVDT_HEADING = "Reflections"
BVDT_LINES = [
    "A label map is a layer of flat colors, drawn first and covered by the art.",
    "A Back Buffer Copy makes the screen texture at its own place in the draw order.",
    "The reflection is a flipped copy that follows the character and shows only where the map says water.",
    "Compare map colors with a distance, never with equals.",
    "Paint the map in pure values: zero or full.",
    "Coast and tint polish the look, and the reflection shows the character only.",
]
BVDT_NARRATION = ("Let's recap with Claude. A label map is a layer of flat colors, drawn first and covered by the art. "
                  "A Back Buffer Copy makes the screen texture at its own place in the draw order. "
                  "The reflection is a flipped copy that follows the character and shows only where the map says water. "
                  "Compare map colors with a distance, never with equals. Paint the map in pure values: zero or full. "
                  "Coast and tint polish the look, and the reflection shows the character only.")

BHTF_PROMPT = ("Give my Godot two D character a reflection that shows only over water, using a hidden label map. Draw the map first, in pure red. "
               "Then a Back Buffer Copy in viewport mode, then my opaque ground. The reflection's shader should keep only pixels within a tenth of red. "
               "Then point me to the three lines I should check.")
BHTF_CHECKS = ["Check: the red map never shows in the running game.",
               "Check: the reflection shows over water and is gone over land."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does the red map ever show in the running game? "
                  "And does the reflection show over water and disappear over land?")
BHTF_SEGMENT = "Give a Character a Reflection"

CUT_LINE = ("Cut, in this order: the renderer-table beat (B31), the color-distance picture (B32), then the polish pair (B34 coast, B35 tint), "
            "then the canvas-layer beat (B15). Each repeats an idea another beat carries or covers a rarer case. The hidden-map idea (B03 to B09), "
            "the copy positions (B12, B13), the rect trap (B17), the lookup and its code (B22, B23), the map toggle (B24) and the equals failure "
            "(B28, B29, B30) stay: they are the proof and the payoff.")

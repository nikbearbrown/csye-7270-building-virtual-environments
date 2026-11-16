"""narration.py: every spoken line of "Making Water in Godot". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-16), the installed Godot 4.7.2 on Bear's Mac (every number below was measured, see
evidence/planning-checks/RESULTS.md), and a third-party Unity Shader Graph water tutorial that Bear named as a model of the PROGRESSION only
(blue, see-through, noise foam, wavy surface); nothing of its wording, sponsor material, jokes or Unity steps is used. See SOURCES.md.
Honesty rules for this film: every picture of water is a real Godot 4.7.2 render of a shader in lab-shaders/ (Forward+ unless a beat says
Compatibility); a measured number says what machine and renderer; scripted events are labelled; drawings are labelled as drawings; the docs
are quoted as quoted. Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the
real figures. Capital-letter built-ins (ALBEDO, TIME, VERTEX) are written as lowercase words in speech; the screen shows the real spelling.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-making-water-in-godot"
TITLE = "Making Water in Godot"
TITLE_LINES = ["Making Water", "in Godot"]
OPENING_DESCRIPTION = "Build a water shader, one layer at a time"
SUMMARY = ("Build a water shader one layer at a time, from flat blue to a see-through, foamy, wavy sea that knows where the shore is. "
           "By the end you can restyle it from the Inspector.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · WATER"
TAGS = ["Godot", "Shaders", "Water shader", "Spatial shader", "Cellular noise", "Normal map", "Vertex shader", "Depth texture", "Game development", "3D", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "Blue and Clear"),
    ("II", "Foam"),
    ("III", "Ripples"),
    ("IV", "Real Waves"),
    ("V", "The Shore"),
]

BODY = [
    # ── ACT I · Blue and Clear ──────────────────────────────────────────────────────────────────────
    ("B01", 0, "This water is one shader on one flat square: blue, see-through, foamy, rippling, with real waves and a white edge at the shore. We will build it in six layers, each only a few lines."),
    ("B02", 0, "A shader draws nothing alone. A mesh gives it a shape, here a flat plane. A material holds the shader, and the mesh node holds the material. Those three links are the whole setup."),
    ("B03", 0, "Here is the first shader, all of it. Shader type spatial means it draws three D surfaces. Fragment runs once for each pixel the plane covers. Albedo is the base color: red, green and blue, each from zero to one."),
    ("B04", 0, "Water color is a uniform: a value the game sets from outside. Source color gives it a color picker. In Forward Plus the numbers you type come out unchanged: point one, point four five, point seven reads twenty-five, one fifteen, one seventy-eight."),
    ("B05", 0, "Roughness runs from zero, a mirror, to one, fully matte. Watch the sun's reflection: it tightens and sharpens as roughness falls, and smears as it rises. Water is smooth, so we keep it low."),
    ("B06", 0, "Right now it is solid plastic: the sea floor, the rocks and the buoy's underside are hidden. Write one line, alpha, and the surface turns see-through. Alpha is how visible a pixel is: zero invisible, one solid."),
    ("B07", 0, "Opacity is another dial. At one, the water hides everything. At zero point three, it barely exists. Zero point seven shows the rocks and the floor and still reads as water, so that is our default."),
    ("B08", 0, "Each pixel is seventy percent water plus thirty percent of what is behind it. We checked one pixel, water over sand. The blend predicts one hundred eight, one twenty-nine, one sixty-one. The screen reads one hundred eight, one twenty-nine, one sixty-two."),
    ("B09", 0, "But not the way you might compute it. Forward Plus blends in linear light, so mixing the typed numbers would predict seventy-three for red, not one hundred eight. Compatibility blends the typed numbers directly, so the same water reads seventy-one."),
    ("B10", 0, "The render mode line is optional. These three are the defaults, written out. Blend mix means alpha is transparency. Depth draw opaque means the water does not write depth. Cull back draws only the top side of the plane."),
    ("B11", 0, "Transparency has a price. Godot draws see-through objects after solid ones, sorted by each node's position, not pixel by pixel. This red plane lies under the water, but its node is nearer, so it draws on top. Let the water write depth, and it vanishes instead."),
    ("B12", 0, "The docs add two more costs. Transparent materials cast no shadows, and they never appear in the depth or screen textures other shaders read. The second one matters soon: the water will read depth to see what lies beneath it."),

    # ── ACT II · Foam ───────────────────────────────────────────────────────────────────────────────
    ("B13", 1, "Foam needs noise, and Godot's shading language has none. No noise function, and no Voronoi node: we counted one hundred ten visual shader nodes in Godot four point seven point two, and none makes noise. So we write one."),
    ("B14", 1, "Here is the plan. Cut the surface into squares and put one point in each, at a random spot. Foam will live along the lines where two points are equally close."),
    ("B15", 1, "A hash picks the spot. It turns a square's address into numbers that look random but never change for that square: a dot product, a sine, then fract, the part after the point."),
    ("B16", 1, "A pixel can be closest to a point in a neighboring square, so check all nine squares around it: its own and the eight beside it. Keep the nearest distance, and the second nearest."),
    ("B17", 1, "Length of the offset is the distance to a point. The nearest distance is zero at a point and grows away from it, like a field of cones. On average a pixel is about forty-three hundredths of a square from its point."),
    ("B18", 1, "The second nearest distance minus the nearest is zero exactly where two points are equally close: along the border between their territories. That thin dark line is where the foam will go."),
    ("B19", 1, "Smooth step turns the thin line into a band of the width you choose, and mix paints foam color where the band is. At width point one, foam covers about thirteen percent of the water."),
    ("B20", 1, "Foam is not see-through, so alpha rises to one where foam is. And foam is matte, so roughness rises too. Without that, the sun's glare streaks along the foam lines like wet paint."),
    ("B21", 1, "Now move it. Each point circles in place: a sine of time plus its own random start. Speed sets how fast they circle, and density sets how many squares fit across the plane."),
    ("B22", 1, "There is another way to sharpen the pattern: one minus the nearest distance, raised to a power. A higher power shrinks the bright blob around each point. It reads as glitter, not foam."),
    ("B23", 1, "It hides a trap. The nearest distance can pass one, so the base goes negative, and a power of a negative number is undefined: black specks. Here, four hundred sixty-two pixels went black. Clamp the base, and they vanish."),
    ("B24", 1, "Godot can bake this net into a texture: a noise texture with Fast Noise Lite set to Cellular. One read instead of nine squares, but its points cannot move, it can only scroll. And Godot smudges a cross where it blends the tile."),

    # ── ACT III · Ripples ───────────────────────────────────────────────────────────────────────────
    ("B25", 2, "Foam on a flat sheet is still lit like a flat sheet. A normal map gives every pixel its own direction to face, so the sun meets a different slope at each point, and one big glare breaks into glints."),
    ("B26", 2, "A normal map is an image where color is direction. Red leans left or right, green leans up or down, and blue is how upright. A flat pixel is half, half, one. The steepest pixel here leans thirteen degrees."),
    ("B27", 2, "You do not paint one. A noise texture wraps a Fast Noise Lite; switch on As Normal Map and Godot makes this image. Also switch on Seamless, or the tile edges show a jump fifty-three times a normal step."),
    ("B28", 2, "In the shader, hint normal says the picture holds directions, not colors. Repeat enable lets the address run past one and wrap around. Without it, Godot stretches the edge pixels into streaks."),
    ("B29", 2, "Add time to the address and the ripples slide. Ripple speed is how far the address moves each second, and scale is how many times the image repeats across the plane."),
    ("B30", 2, "One layer slides in a line, and you can see the repeat. So add a second layer, scaled differently, moving the other way, and average the two. Now the ripples cross and no direction wins."),
    ("B31", 2, "Look from the water's edge. The glints move, but the edge of the plane is ruler straight: the same pixel row in every column. A normal map changes how light hits the water, never its shape."),
    ("B32", 2, "Now bend the foam. The normal map also says which way the surface leans, so shift the foam's address that way before measuring the cells. The net sloshes with the ripples. Warp strength is the dial."),
    ("B33", 2, "Check every renderer you ship. The same water on the same clock reads one hundred thirty-two for red in Forward Plus and one hundred in Compatibility: bluer, more saturated. The shader is identical; the pictures are not."),

    # ── ACT IV · Real Waves ─────────────────────────────────────────────────────────────────────────
    ("B34", 3, "Normal maps fake the light. To move the water itself, move its vertices. A plane has four. Cut it a hundred twenty-seven times each way and it has sixteen thousand six hundred forty-one: two more than the cuts, squared."),
    ("B35", 3, "A wave is a sine of position minus speed times time. Two waves, in different directions and lengths, make the surface lumpy. The function returns the height, and the slope along x and along z."),
    ("B36", 3, "In vertex, add that height to each vertex's y. One line moves sixteen thousand corners, and the graphics card fills in everything between them. Time passes in, and the surface rolls."),
    ("B37", 3, "But the light does not know the surface moved. Leave the normal alone and the glare stays one flat oval. Compute the normal from the slope, and the glare breaks into glints on the crests."),
    ("B38", 3, "From the water's edge again: now the edge bends. The near edge spans up to ninety-five pixel rows, lowest to highest, against none for the flat plane. That is real height, not lighting."),
    ("B39", 3, "The shader moves the drawing, not the nodes. A buoy knows nothing about it. So a script runs the same wave function and sets each floater's height, and the buoy and the crate ride the waves."),
    ("B40", 3, "Give both the same clock. The shader's time and the script's clock start at different moments: on repeated runs here they differed by about three tenths of a second, never quite the same. So the script writes its clock into a uniform, and the shader reads that."),
    ("B41", 3, "Run the same function on the graphics card and in the script and they agree to about three millimeters, on waves nineteen centimeters tall. Wave height, length and speed are three more dials."),

    # ── ACT V · The Shore ───────────────────────────────────────────────────────────────────────────
    ("B42", 4, "Real water foams where it meets things. To know that, the water must know how deep it is. A texture with the hint depth texture holds the depth of everything solid. The water itself is not in it, so it can look beneath."),
    ("B43", 4, "A depth value is not a distance. Turn it into one: rebuild the screen point, multiply by the inverse projection, divide by w, and flip the sign of z. Now you know how far the solid thing is from the camera."),
    ("B44", 4, "The water's own distance is minus its view z. Subtract, and you have the gap: how far the water sits above whatever is beneath it. Over a floor half a meter down, the gap reads zero point five."),
    ("B45", 4, "Hand a built-in to a helper function and Godot answers unknown identifier. Time and the constants are visible everywhere. Built-ins that belong to one function, like U V, vertex and screen U V, are not: pass them in."),
    ("B46", 4, "Foam where the gap is small. The reach is wider where the nearest cell point is far, so the edge scallops instead of drawing a ruler line. Max joins it to the net, and the beach, the rock and the buoy gain a white edge."),
    ("B47", 4, "One more trap. Compatibility counts depth from minus one to one; Forward Plus counts from zero to one. A single preprocessor line picks the right math. Leave it out in Compatibility and the whole surface turns to foam."),
    ("B48", 4, "Every dial is a uniform, and group uniforms turned them into folders. In the Inspector they appear as folders named Color, Clarity, Foam, Ripples, Waves and Shore, with sliders for ranges and pickers for colors."),
    ("B49", 4, "Same shader, three looks. Lagoon: clear, turquoise, fine foam. Pond: dark green, nearly opaque, no foam. Storm: grey, tall fast waves, thick foam. Only the numbers changed."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Water in a game looks like it needs a physics simulation. It does not. "
         "It is one flat plane wearing a few small tricks, stacked one at a time, and each trick is only a few lines.")
BIDEA_TEXT = ("Making water needs\na water simulation.", "a water simulation", "six small tricks")

BDEFS = ("Six terms before we start. A shader is a small program the graphics card runs to decide how something is drawn. A vertex is a corner point of a shape. "
         "A pixel is one dot of the picture. A texture is an image a shader can read by address. U V is a point's address on the shape. "
         "And the renderer is the part of Godot that draws.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Vertex", "a corner point of a shape"),
    ("Pixel", "one dot of the picture on screen"),
    ("Texture", "an image a shader can read by address"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Renderer", "the part of Godot that draws"),
]

BVDT_HEADING = "Making Water in Godot"
BVDT_LINES = [
    "Blue is albedo, and a uniform makes it a dial.",
    "Writing alpha makes water see-through, and the renderer decides how it blends.",
    "Foam is cellular noise: the gap between the nearest and second nearest point.",
    "A normal map lights the ripples, and it can push the foam's address too.",
    "Real waves move vertices, and a script runs the same function for floaters.",
    "The depth texture tells the water where it meets the shore.",
]
BVDT_NARRATION = ("Let's recap with Claude. Blue is albedo, and a uniform makes it a dial. Writing alpha makes water see-through, and the renderer decides how it blends. "
                  "Foam is cellular noise: the gap between the nearest and second nearest point. A normal map lights the ripples, and it can push the foam's address too. "
                  "Real waves move vertices, and a script runs the same function for floaters. The depth texture tells the water where it meets the shore.")

BHTF_PROMPT = ("Write a Godot spatial shader for water on a plane mesh cut sixty-three times each way. Make it blue with an opacity uniform, "
               "foam from cellular noise that moves with time, and waves in vertex that also fix the normal. "
               "Group the uniforms for the Inspector, then tell me how many vertices the plane has.")
BHTF_CHECKS = ["Check: the water is see-through at opacity zero point seven, and the floor shows through.",
               "Check: the vertex count is sixty-five by sixty-five, four thousand two hundred twenty-five."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Is the water see-through at opacity zero point seven, with the floor showing through? "
                  "And does the vertex count match sixty-five by sixty-five?")
BHTF_SEGMENT = "Build Water in Layers"

CUT_LINE = ("Cut, in this order: the renderer-ripples beat (B33: a repeat of the renderer lesson in B09), the power-curve pair (B22 and B23: an alternative to the "
            "edge line, with its trap), the baked-texture beat (B24), the sorting and cost beats (B11 and B12: docs only, nothing is measured), and the "
            "built-ins-in-a-function beat (B45: a compile error, not the main line). The blend arithmetic (B08, B09), the noise net (B14 to B19), the "
            "normal map (B25 to B28), the real waves (B35 to B39) and the shore (B42 to B44, B46) stay: they are the arc.")

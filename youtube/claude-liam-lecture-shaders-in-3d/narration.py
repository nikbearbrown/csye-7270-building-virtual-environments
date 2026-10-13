"""narration.py: every spoken line of "Shaders in 3D". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13, quoted in FACTCHECK.md), the installed Godot 4.7.2 on Bear's Mac (every number below
was measured in evidence/planning-checks/), and one real shader from a small game (lab-shaders/12-signal-pad.gdshader). Neither third-party
source covers three-D; nothing was copied (SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input (the turning lamp, the turning quad, the key-free
sweeps) is labelled; the Inspector and the editor are not shown, so no widget is claimed.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.

TITLE note: TITLE keeps the digit ("3D"), as Bear's plan names the film; the shared lint now accepts "3D" in a title. The narrated opening and
closing use SPOKEN_TITLE ("Shaders in three D") so the voice never has to guess how to read a digit. See CHECKS-REPORT.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-shaders-in-3d"
TITLE = "Shaders in 3D"
TITLE_LINES = ["Shaders in 3D"]
SPOKEN_TITLE = "Shaders in three D"
OPENING_DESCRIPTION = "What changes when a shader goes three-D"
SUMMARY = ("Learn what changes when a shader draws a three-D surface, how lighting and the renderer change the color you get, "
           "and how to read a real one.")
BOPEN = S.bopen(SPOKEN_TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · IN THREE-D"
TAGS = ["Godot", "Shaders", "3D", "Spatial shader", "Albedo", "UV", "Unshaded", "Renderer", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); a shader from a small game; see SOURCES.md"

ACTS = [
    ("I", "Same Shape, New Names"),
    ("II", "Lit or Unlit"),
    ("III", "A Surface That Changes"),
    ("IV", "Read a Real One"),
    ("V", "Which Renderer?"),
]

BODY = [
    # ── ACT I · same shape, new names ────────────────────────────────────────────────────────────────
    ("B01", 0, "This shader comes from a small game. It charges a pad from rust to green, and the whole effect is ten lines. "
               "By the end of this film, you can read every one of them."),
    ("B02", 0, "A shader is a small program the graphics card runs to decide how something is drawn. In two-D or three-D, it has the same "
               "shape: a first line, up to three functions, and dials your game can turn."),
    ("B03", 0, "The first line says what the shader is for. Canvas item means two-D. Spatial means three-D, where the shader draws a mesh: "
               "the points and triangles that make a shape."),
    ("B04", 0, "Both types use the same three functions. Vertex runs once for each vertex, a corner point of the mesh. A flat square has four. "
               "Fragment runs once for each pixel the mesh covers. Light runs once per pixel, for every light."),
    ("B05", 0, "The other change is the output. A two-D shader sets color: four numbers, red, green, blue and alpha. "
               "A three-D shader sets albedo: three numbers. Alpha becomes a separate output."),
    ("B06", 0, "Get either one wrong and Godot says so. Write color in a three-D shader and it answers: constants cannot be modified. "
               "Color exists there, but you can only read it. Give albedo four numbers and it answers: invalid arguments, vec three, vec four."),
    ("B07", 0, "Some mix-ups are silent. Give a three-D mesh a two-D shader, and the running game raises no error. "
               "It draws the mesh as if it had no shader at all. When a shader seems ignored, check the first line."),
    ("B08", 0, "U V is a point's address on the shape: zero to one across, zero to one down. Paint it as a color, red across and green down. "
               "A square, a box and a sphere each show a different map, because the mesh supplies the address."),
    ("B09", 0, "To use a shader, give the mesh instance a shader material. In three-D that slot is called material override. "
               "The node holds the material. The material holds your shader."),
    ("B10", 0, "Now run the one-line albedo shader on a sphere. You wrote one flat teal, so you might expect a flat teal disc. "
               "Instead one side is bright and one is dim. You wrote no lighting rule. Godot lit the sphere with the scene's lamp."),

    # ── ACT II · lit or unlit ────────────────────────────────────────────────────────────────────────
    ("B11", 1, "Back to the lit sphere. A script now moves the lamp. The albedo never changes, but the same surface goes bright, then dim. "
               "The color you write is only a starting point. The lighting does the rest."),
    ("B12", 1, "In three-D, the fragment function describes a surface. Albedo is its base color. Alpha is how visible it is. "
               "Emission is light it gives off. Roughness and metallic describe its finish."),
    ("B13", 1, "Then Godot's own lighting turns that description, and every lamp, into the pixel you see. You describe the surface. "
               "Godot does the lighting. Your color is an input, not the answer."),
    ("B14", 1, "Sometimes you want no lighting. Add a second line: render mode unshaded. Now the result is only albedo, and the lamp is "
               "ignored. Watch the lit sphere beside it."),
    ("B15", 1, "Why choose unshaded? No lamp can change the color, so a flat, graphic look stays flat. Godot's docs add that skipping the "
               "lighting makes the surface faster to render."),
    ("B16", 1, "You can write the light function yourself. Then your function replaces Godot's lighting for that surface. An empty one "
               "is a trap: the lamp stops working. The sphere stays dim, whatever the lamp does."),
    ("B17", 1, "Another trap. A three-D surface has two sides, and by default only the front is drawn. Turn a flat square around and it "
               "vanishes. Add cull disabled to the render mode line, and both sides draw."),
    ("B18", 1, "So when a three-D shader looks wrong, ask two quick questions. Is a lamp changing my color? Add unshaded and see. "
               "Is the back side being skipped? Add cull disabled and see. Godot's docs list many more modes, such as blend add."),

    # ── ACT III · a surface that changes ─────────────────────────────────────────────────────────────
    ("B19", 2, "Now build a surface that changes. Start from a picture you already know: the address as a color. "
               "On a flat square, the corners read dark, red, green and yellow. The top left is zero, zero."),
    ("B20", 2, "Keep only the across part, x. It is a ramp: a smooth run of values from zero up to one. "
               "Everything that follows starts from that ramp."),
    ("B21", 2, "Multiply x by eight and the ramp runs from zero to eight. Fract keeps the part after the decimal point, so it starts over "
               "at zero at every whole number: eight ramps in a row."),
    ("B22", 2, "Step turns a ramp into a switch. Step of point five and x gives zero when x is below one half, and one from one half up. "
               "Feed it the repeating ramp and it switches on and off eight times."),
    ("B23", 2, "Put both in a shader. Stripe is step of point five and fract of eight x: zero or one. "
               "Scale that into two greys and you get eight dark stripes and eight light ones."),
    ("B24", 2, "Mix blends two values. At zero you get the first, at one you get the second, and in between you get a blend. "
               "Mix of a, b and t is a times one minus t, plus b times t."),
    ("B25", 2, "Give mix a dial. A uniform is a value your game sets from outside, the same for every pixel. "
               "Call this one activation, from zero to one. Now one number blends two colors."),
    ("B26", 2, "The word after the colon is a hint. It tells Godot how to treat the uniform. Hint range keeps the dial between "
               "zero and one in the editor. Source color says this is a color."),
    ("B27", 2, "From the game, one line turns the dial. Take the mesh instance's material override, then call set shader parameter "
               "with the dial's name and a value. The name must match exactly, capitals included."),
    ("B28", 2, "Change the value every frame, or tween it, and the surface animates. Set the starting value first. "
               "A tween cannot start from a dial the code has never set."),

    # ── ACT IV · read a real one ─────────────────────────────────────────────────────────────────────
    ("B29", 3, "Here is the whole pad shader again, ten lines. You know every ingredient now. "
               "Read it like a recipe, top to bottom, while the pad charges."),
    ("B30", 3, "Line one: spatial, a three-D surface. Line two: render mode unshaded. "
               "No lamp can change this pad's color, whatever the light does."),
    ("B31", 3, "Lines three to five are three dials. Activation, from zero to one. And two colors, rust and green, "
               "each marked source color, so Godot knows they are colors."),
    ("B32", 3, "Fragment runs once for each pixel the pad covers. Its first line makes the stripe: step of point five and fract of eight x. "
               "Zero, one, zero, one, across the pad."),
    ("B33", 3, "Next, base. It is the rust color, multiplied by a mix: point six five on stripe zero, full strength on stripe one. "
               "Dot r g b keeps red, green and blue, and drops alpha."),
    ("B34", 3, "The last line sets albedo: a mix from base to green, steered by activation. At zero it is the striped rust. "
               "At one it is flat green, and the stripes are gone."),
    ("B35", 3, "Notice what is missing. There is no vertex function and no light function. Godot's default places the corners, "
               "and unshaded skips the lighting. The pad needs only fragment."),
    ("B36", 3, "In the game, this pad is not a flat square but a thin box. A box keeps its map in six pieces, so its top shows only "
               "about a third of the stripes. Same ten lines, different mesh, different picture."),

    # ── ACT V · which renderer? ──────────────────────────────────────────────────────────────────────
    ("B37", 4, "Now run the same pad in two of Godot's three renderers: Forward Plus on the left, Compatibility on the right. "
               "Same file, same activation, no lamp. Watch the greens."),
    ("B38", 4, "They do not match. At half charge, the green channel of a light stripe reads point five four in Forward Plus, "
               "and point four four in Compatibility. Measured on this Mac."),
    ("B39", 4, "Neither is a bug. Take the plainest case: an albedo of one half, unshaded. Forward Plus draws point seven four. "
               "Compatibility draws point five. In two-D, the same number draws point five in both."),
    ("B40", 4, "Forward Plus treats albedo as linear light, then converts it to s R G B for your screen. The curve lifts the dark and "
               "middle values. Compatibility skips that, so a half stays a half."),
    ("B41", 4, "That moves a mix too. The pad's colors are marked source color, so Forward Plus turns them into linear light first, "
               "blends there, then converts back. Compatibility blends the numbers as written. One dial, two midpoints."),
    ("B42", 4, "Godot even lets a shader ask. A three-D shader can read a value called output is s R G B: true in Compatibility, false in "
               "Forward Plus and Mobile. The documentation says so in one line."),
    ("B43", 4, "Which renderer is yours? Open Project Settings, then Rendering, Renderer. Rendering Method shows it, and changing it there needs Save and Restart. "
               "Switching can change how a scene looks, so test again afterwards."),
    ("B44", 4, "So a pixel you read is true for one renderer. When you test a shader, or ask an AI to, name the renderer. "
               "A number from the wrong one is a correct measurement of the wrong picture."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Many people think a three-D shader is a different, harder thing. It is not. "
         "It has the same shape as a two-D shader, with new names and one new idea: light.")
BIDEA_TEXT = ("3D shaders are\na different, harder thing.", "a different, harder thing", "the same shape, new names")

BDEFS = ("Five terms. A mesh is the points and triangles that make a three-D shape. A material tells Godot how to draw a surface. "
         "Albedo is the base color of a surface. Lighting is how lights change that color. A renderer is the part of Godot that draws the picture.")
BDEFS_TERMS = [
    ("Mesh", "the set of vertices and triangles that make a shape"),
    ("Material", "the resource that tells Godot how to draw a surface; it holds the shader"),
    ("Albedo", "the base color of a surface"),
    ("Lighting", "how lights change a surface's color"),
    ("Renderer", "the part of Godot that draws"),
]

BVDT_HEADING = "Shaders in 3D"
BVDT_LINES = [
    "A three-D shader has the same shape as a two-D one, with new names.",
    "Albedo is the base color, and the address comes from the mesh.",
    "Surfaces are lit by default, and unshaded gives you the albedo with no lamp.",
    "Fract, step and mix cut stripes and blend colors, and a uniform lets the game steer.",
    "The pad is ten lines: a type, a mode, three dials, a stripe, a base and a blend.",
    "A pixel is true for one renderer, so name it when you test.",
]
BVDT_NARRATION = ("Let's recap with Claude. A three-D shader has the same shape as a two-D one, with new names. "
                  "Albedo is the base color, and the address comes from the mesh. "
                  "Surfaces are lit by default, and unshaded gives you the albedo with no lamp. "
                  "Fract, step and mix cut stripes and blend colors, and a uniform lets the game steer. "
                  "The pad is ten lines: a type, a mode, three dials, a stripe, a base and a blend. "
                  "A pixel is true for one renderer, so name it when you test.")

BHTF_PROMPT = ("Write a Godot spatial shader for a mesh instance, with render mode unshaded. Give it one float uniform called charge, "
               "from zero to one, and two color uniforms marked source color. Paint eight stripes in the first color using step and fract on the U V address, "
               "and mix toward a plain second color as charge rises. Then tell me which renderer your colors assume.")
BHTF_CHECKS = ["Check: at charge one, the stripes are gone.",
               "Check: switch the renderer. Does the half-charge color change?"]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. At charge one, are the stripes gone? "
                  "And when you switch the renderer, does the half-charge color change?")
BHTF_SEGMENT = "Charge a Striped Surface"

CUT_LINE = ("Cut, in this order: the tween beat (B28), the cull beat (B17), the two-questions beat (B18), the output-is-s R G B beat (B42) "
            "and the missing-functions beat (B35): each repeats an idea another beat carries. The lit sphere (B11), the unshaded pair "
            "(B14), the box reveal (B36) and the two-renderer comparison (B37 to B41) stay: they are the film's proof.")

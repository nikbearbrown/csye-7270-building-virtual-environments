"""narration.py: every spoken line of "Godot Shaders". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured in
evidence/planning-checks/), a third-party introductory video and a long third-party course (ideas followed, nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input is labelled; the graphics card's own time
could not be read on this setup and the film says so.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-godot-shaders"
TITLE = "Godot Shaders"
TITLE_LINES = ["Godot Shaders"]
OPENING_DESCRIPTION = "What a shader is, and how to give one a dial"
SUMMARY = "Learn what a shader is, the words you will meet along the way, and how to write one that your game can control."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · THE BASICS"
TAGS = ["Godot", "Shaders", "GPU", "GDScript", "Game development", "Fragment shader", "Vertex shader", "Uniform", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "One Pixel, All at Once"),
    ("II", "Setting Up a Shader"),
    ("III", "The Three Functions"),
    ("IV", "Dials: Uniforms"),
    ("V", "Where Am I, and When?"),
]

BODY = [
    # ── ACT I · one pixel, all at once ──────────────────────────────────────────────────────────────
    ("B01", 0, "A game can work and still look flat. Same sprite, same background, nothing broken. A shader is the part that decides how it looks: the wobble, the glow, the water, the outline."),
    ("B02", 0, "A shader is a small program that runs on the graphics card, the G P U. It decides how something is drawn. Your game code decides what exists, and where. The shader decides what each part looks like."),
    ("B03", 0, "Why a second chip? The C P U is a few fast workers, doing one job after another. The G P U is a crowd of small workers, all doing the same job at once. A picture is millions of identical little jobs."),
    ("B04", 0, "Here is the slow way. A G D script loop colors every pixel of a full H D picture, one at a time. That is over two million calls, for one picture. Watch what it costs."),
    ("B05", 0, "On this Mac, that loop took about fifty-five milliseconds. A game running at sixty frames per second has sixteen and a half milliseconds for everything. This is one gradient, and it is more than three times the whole budget."),
    ("B06", 0, "The shader way describes one pixel. This line says: the red amount is how far across the shape this pixel sits. Nothing loops. The graphics card runs the line for every pixel, and the gradient appears."),
    ("B07", 0, "Drawing that same gradient this way cost the processor about four hundredths of a millisecond, only to hand over the job. The graphics card did the pixels. Its own time could not be read on this setup, so there is no number for it."),
    ("B08", 0, "So a shader flips the question. Not: for each pixel, do this. Instead: write down what one pixel should do, and let the card do it everywhere. A shader decides the color of one pixel."),
    ("B09", 1, "Where does a shader live? In a file. You attach it to a node through a material. The node holds a Shader Material, and the Shader Material holds your shader."),
    ("B10", 1, "In the editor, that is a few clicks. In the node's Material slot, choose Shader Material under New. Click it, and in its Shader slot choose New Shader. Set the mode to Canvas Item, since it starts on Spatial, and create it. Godot opens the shader editor."),
    ("B11", 1, "What you type there is Godot's own shader language. It is similar to a standard one called G L S L, but simpler. If you can read a few lines of G D script, you can read it. It is strict about types, and statements end in semicolons."),

    # ── ACT II · setting up a shader (B09-B14) / ACT III · the three functions (B15-B24) ────────────────────────────────────────────────────────────────
    ("B12", 1, "The first line of every shader says what it is for. Canvas item is for two-D drawing and interface. Spatial is for three-D. Particles, sky and fog are for those. This film uses canvas item. The ideas carry over to three-D with a few different names."),
    ("B13", 1, "The smallest working shader has one function and one line. In the function called fragment, set color to four numbers: red, green, blue, and how visible it is. One, zero, zero, one: pure red, fully visible."),
    ("B14", 1, "A shader can have up to three special functions, and the engine calls them for you: vertex, fragment and light. You write what each one does. Godot decides when it runs, and how many times."),
    ("B15", 2, "Vertex runs once for each vertex, each corner point of the shape. A plain rectangle has four corners, so vertex runs four times. Its job is to place the corners."),
    ("B16", 2, "A real run. This vertex pushes the bottom two corners fifty pixels to the right and leaves the top two alone. The whole picture leans, because the card fills in everything between the corners."),
    ("B17", 2, "Between the corners, you calculate nothing. The left edge slides evenly from top to bottom: fifty pixels over a hundred and twenty-eight rows. That is why vertex alone cannot ripple a plain rectangle. Four corners can only make straight edges."),
    ("B18", 2, "Fragment runs after the corners are placed. It runs once for each pixel the shape covers, and its job is to set that pixel's color. The shape is already decided. Now the card asks about every pixel inside it."),
    ("B19", 2, "You will hear this called a pixel shader, or a fragment shader. Same job, two names. Microsoft's Direct three D says pixel. OpenGL, Vulkan and Godot say fragment. The careful word is fragment, because a fragment is a pixel-to-be."),
    ("B20", 2, "It is only a pixel-to-be because it can still be thrown away, or blended with others. This shader says discard for the right half. Fragment ran there. No pixel came out, and the background shows through."),
    ("B21", 2, "The third function, light, runs once for each light that touches a pixel. Two lights, two runs, and the results add. If you write light, it replaces Godot's default lighting, even when it is empty. Here we only name it."),
    ("B22", 2, "So the order of work is fixed. First vertex places the corners. Then the card fills in the shape. Then fragment colors each pixel. Information flows one way: forward."),
    ("B23", 2, "Inside these functions the engine hands you values, called built-ins, written in capital letters. Some come in, like a pixel's address and the time. One goes out: the color you set. Which ones exist depends on the function."),
    ("B24", 2, "So far: vertex runs once per corner and places things. Fragment runs once per pixel and colors things. Light runs once per pixel, for each light, and lights things."),

    # ── ACT IV · dials: uniforms ───────────────────────────────────────────────────────────────────
    ("B25", 3, "A shader that always draws the same red is not much use. Your game needs to say: more red now, less red later. But the shader lives on the graphics card, out of reach. How do you talk to it?"),
    ("B26", 3, "With a uniform. A uniform is a value you declare outside the functions, and set from outside the shader. Here is one called red, from zero to one. The shader reads it. The shader can never change it."),
    ("B27", 3, "In the editor, that line becomes a slider. In the Inspector, under Shader Parameters, there is a control labelled Red. Drag it, and the picture changes while you watch."),
    ("B28", 3, "Three uniforms make a color mixer. Red, green, blue, each its own slider. The shader puts the three numbers together into a color."),
    ("B29", 3, "The part after the colon is a hint. It tells the editor how to show the uniform. A range adds a slider bar. Source color gives a color swatch that opens a picker. A hint shapes the editor, not the math."),
    ("B30", 3, "A hint does not clamp. If your game code sets the value to seven, the shader receives seven. The slider only guards the editor. If a range matters, enforce it in your code as well."),
    ("B31", 3, "From the game, you set a uniform with set shader parameter. Get the node's material, then pass the uniform's name and a value. The name is case-sensitive, and it must match the shader exactly."),
    ("B32", 3, "Get the name wrong, and nothing happens. No error. The value is stored as an unused parameter, the real uniform keeps its default, and the effect never appears. When a shader ignores your game, check the spelling first."),
    ("B33", 3, "You can animate a uniform too. Set its starting value from code, then tween it, and the shader follows, every frame. Skip the first step and the tween has nothing to start from. That is how a shader answers to gameplay."),
    ("B34", 4, "A uniform is one value, the same for every pixel in the draw. Some inputs must differ, because each pixel needs to know where it is. The engine hands those in, and they are different for every pixel."),
    ("B35", 4, "Two kinds of input, then. A uniform is set by you. A built-in is set by the engine. Both are names the shader can read, and some built-ins, like the time, are the same for every pixel too."),

    # ── ACT V · where am I, and when? ──────────────────────────────────────────────────────────────
    ("B36", 4, "Now, the pixel's address. U V runs from zero to one across the shape, and zero to one down. The top left is zero, zero. The bottom right is one, one. In two-D, the second number counts downward."),
    ("B37", 4, "Use the address as a color. Red is how far across. Green is how far down. Left to right, red grows. Top to bottom, green grows. The corners give it away: black, red, green, yellow."),
    ("B38", 4, "Use it as a fade instead. Multiply the alpha by the horizontal address. The left edge is invisible, the right edge solid. One line, no loop, no second image."),
    ("B39", 4, "Now time. Time counts up in seconds. Put it inside a sine and you get a smooth back and forth, between minus one and one. Scale that to zero to one, and the color breathes."),
    ("B40", 4, "One catch. Time is not the age of your node. It is one clock for the whole game, started with the engine. Add a node three seconds in, and it already sees three seconds gone."),
    ("B41", 4, "So for a one-time effect, a fade-in, or a reveal that starts when something happens, do not lean on time. Use a uniform, and let your game drive it from zero to one when the moment comes."),
    ("B42", 4, "Put it together: a circle that opens from the middle. For each pixel, measure the distance to the middle of the shape. If it is more than the radius, discard the pixel. The radius is a uniform."),
    ("B43", 4, "Now drive it from the game. When the player presses a key, tween the radius from zero to point eight, and the picture opens like an iris. The shader holds the rule. The game holds the moment."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people meet a shader as a strange file of math. One idea makes it readable. "
         "A shader does not paint the whole screen. It decides the color of one pixel, and the graphics card asks it about every pixel at once.")
BIDEA_TEXT = ("A shader decides the color of\nthe whole screen.", "the whole screen", "one pixel")

BDEFS = ("Five terms. The G P U is the graphics chip: many small workers running at once. A pixel is one dot of the picture. "
         "A vertex is a corner point of a shape. A texture is an image a shader can read. And a material tells Godot how to draw a surface.")
BDEFS_TERMS = [
    ("GPU", "the graphics chip: many small workers running at once"),
    ("Pixel", "one dot of the picture on screen"),
    ("Vertex", "a corner point of a shape"),
    ("Texture", "an image a shader can read by address"),
    ("Material", "the resource that tells Godot how to draw a surface; it holds the shader"),
]

BVDT_HEADING = "Godot Shaders"
BVDT_LINES = [
    "A shader decides the color of one pixel, and the card runs it for every pixel.",
    "A shader lives in a file, on a material, on a node.",
    "Vertex places the corners, fragment colors the pixels, light lights them.",
    "A uniform is a dial your game sets, the same for every pixel.",
    "The address says where a pixel is.",
    "Time is one clock for everyone.",
]
BVDT_NARRATION = ("Let's recap with Claude. A shader decides the color of one pixel, and the card runs it for every pixel. "
                  "A shader lives in a file, on a material, on a node. "
                  "Vertex places the corners, fragment colors the pixels, light lights them. "
                  "A uniform is a dial your game sets, the same for every pixel. "
                  "The address says where a pixel is. Time is one clock for everyone.")

BHTF_PROMPT = ("Write a Godot canvas item shader for a Color Rect. One float uniform called fill, with a hint range from zero to one. "
               "The left part of the rectangle, as wide as fill, is red. The rest is transparent. Then point me to the three lines I should check.")
BHTF_CHECKS = ["Check: the Inspector shows a Fill control with a slider bar.",
               "Check: at fill point five, exactly half the rectangle is red."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Does the Inspector show a Fill control with a slider bar? "
                  "And at point five, is exactly half the rectangle red?")
BHTF_SEGMENT = "Make a Slider Fill the Rectangle"

CUT_LINE = ("Cut, in this order: the budget-bars beat (B05), then the typo beat (B32), the editor-slider beat (B27) and the tween "
            "beat (B33): each repeats an idea another beat already carries. The vertex-lean pair (B16, B17), the discard beat (B20) and "
            "the iris build (B42, B43) stay: they are the proof and the payoff.")

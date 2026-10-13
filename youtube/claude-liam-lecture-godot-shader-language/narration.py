"""narration.py: every spoken line of "Godot Shader Language". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every behavior below was run in
evidence/planning-checks/; the engine's own error messages are quoted exactly), a third-party video course on shaders (ideas followed,
nothing copied; see SOURCES.md).
Honesty rules for this film: engine messages are quoted verbatim from a run; a measured number says what machine and renderer;
the pastel and stripe pictures are real Godot renders of files in lab-shaders/; nothing here is an invented editor screen.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
The correction in each beat is the one the source got loose or wrong (see FACTCHECK.md).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-godot-shader-language"
TITLE = "Godot Shader Language"
TITLE_LINES = ["Godot Shader", "Language"]
OPENING_DESCRIPTION = "How to read any shader, one type at a time"
SUMMARY = ("Learn how a shader file is built, what its types and vectors mean, and how to read any shader line by line, "
           "even one an AI wrote for you.")
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · THE LANGUAGE"
TAGS = ["Godot", "Shaders", "Shader language", "GDScript", "Vectors", "Swizzling", "Functions", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "The Shape of a File"),
    ("II", "Types and Vectors"),
    ("III", "Your Own Functions"),
    ("IV", "Choices and Loops"),
    ("V", "Read One Aloud"),
]

BODY = [
    # ── ACT I · the shape of a file ────────────────────────────────────────────────────────────────
    ("B01", 0, "Here is a real shader, fourteen lines long. It makes a color breathe between pale gray and teal. "
               "Godot refuses a line that breaks the rules. It will not warn you when a legal line does something you did not mean. "
               "So you have to read it."),
    ("B02", 0, "A shader file has three zones, read from the top down. The header says what kind of shader this is. "
               "The globals are values declared outside every function. The functions are where the work happens."),
    ("B03", 0, "The header starts with shader type, and it must be the first line. Canvas item means two-D drawing and interface. "
               "Spatial means three-D. An optional second line, render mode, picks options, such as how a pixel blends with the background."),
    ("B04", 0, "Globals sit outside every function. A uniform is a value your game sets from outside. A const never changes. "
               "A varying hands a value from a shape's corners to its pixels. Declare each one above the code that uses it."),
    ("B05", 0, "Then come the functions. Godot calls three of them for you. Vertex places the corners, fragment sets the color of each pixel, "
               "and light handles each light that touches a pixel. This film uses fragment. Any other function is one you write yourself."),
    ("B06", 0, "Inside a function, every statement ends with a semicolon, and braces group statements into a block. "
               "Forget one semicolon and Godot refuses the whole shader. Here it points at the next line, where it noticed."),
    ("B07", 0, "Spacing and line breaks are for people. Here is one shader that draws a soft gradient, written three ways: neat, "
               "squeezed onto one line, and spread over many. Godot draws the same picture for all three."),
    ("B08", 0, "Comments are notes for people. Two slashes comment out the rest of a line. Slash star starts a block comment, and star slash ends it. "
               "Godot skips both, so a commented-out line does nothing."),
    ("B09", 0, "Godot's language is close to G L S L, the shading language of OpenGL, but not identical. Names must match exactly, "
               "capitals included: a capital L makes level a different name. The other language's G L frag color is unknown here. "
               "Godot calls it color."),

    # ── ACT II · types and vectors ─────────────────────────────────────────────────────────────────
    ("B10", 1, "Every value has a type. A float is a decimal number, an int is a whole number, and a bool is true or false. "
               "A texture has a type too, called sampler two D. You declare a variable with its type first, then its name."),
    ("B11", 1, "Godot is strict about this. A two with no decimal point is an int, and Godot will not quietly turn it into a float. "
               "Put it in a float, or add it to one, and the shader will not compile. Write two point zero."),
    ("B12", 1, "Shaders are full of vectors, bundles of two to four numbers: vec two, vec three, vec four. "
               "A color is a vec four: red, green, blue and alpha, how solid it is. Reading a texture gives back a vec four too."),
    ("B13", 1, "You build a vector by naming its type. Give vec three one number and it fills all three parts. "
               "Give vec four a vec three and a number and it joins them. The pieces must add up to the size, or Godot refuses."),
    ("B14", 1, "Arithmetic works on every part at once. Multiply a vec three by two point zero and all three numbers double. "
               "Multiply two vectors and each part meets its partner. That is why shader code is so short."),
    ("B15", 1, "Here it is in use. U V is the address of each pixel, a vec two. Join it with one half to make a vec three, "
               "scale by zero point six, add zero point four. Red grows to the right, green grows downward."),
    ("B16", 1, "You can reach into a vector by name. Dot R G B takes red, green and blue from a vec four. Dot X Y takes the first two parts. "
               "Picking or reordering parts like this is called swizzling."),
    ("B17", 1, "Order is yours to choose. Dot B G R reverses the order, and the gradient's colors turn over. "
               "R G B A, X Y Z W and S T P Q name the same parts, but never mix sets in one swizzle. Godot refuses."),
    ("B18", 1, "The type on the left must match the type on the right. Color is a vec four. Hand it a vec three and Godot refuses. "
               "Fix it by adding alpha: vec four of c and one point zero."),
    ("B19", 1, "To read any line, say the type of each piece, from the inside out. U V is a vec two. Joined with one half, a vec three. "
               "Times a float, still a vec three. Plus a float, still a vec three."),

    # ── ACT III · your own functions ───────────────────────────────────────────────────────────────
    ("B20", 2, "Now your own functions. The first line of a function is its signature. It has three parts: "
               "the type it hands back, its name, and its arguments, each with a type."),
    ("B21", 2, "Calling the function hands values into the arguments, in order. The body runs. Then return hands one value back, "
               "and it must have the type the signature promised. Break that promise and Godot says so."),
    ("B22", 2, "Godot reads from the top down. A function must be defined above the one that calls it. "
               "Call it first and the message says no matching function found. It does not say the order is wrong."),
    ("B23", 2, "A function you write cannot see most built-ins. A built-in is a value the engine hands to a function. "
               "U V and color are handed to fragment, not to your function. Use U V inside yours and Godot says unknown identifier."),
    ("B24", 2, "The fix is to pass what you need in as an argument. Here U V goes in as address, and the same gradient appears. "
               "A few built-ins are global, such as time and pi, and any function can read those."),
    ("B25", 2, "Arguments come in three modes. In, the default, hands over a copy, so changes stay inside the function. "
               "In out hands over the original, so the caller's variable changes. Out is for writing a result back."),
    ("B26", 2, "The functions Godot gives you follow the same pattern, and the documentation lists each signature. "
               "In it, vec type means a float or a vec two, three or four. Sine takes one of those and hands back the same type."),
    ("B27", 2, "A name can be reused if the argument types differ, and Godot picks by type. This call passes one, an int, and gets teal. "
               "This one passes one point zero, a float, and gets sand. Same name, same digit, different function."),

    # ── ACT IV · choices and loops ─────────────────────────────────────────────────────────────────
    ("B28", 3, "An if needs a bool. A comparison, like U V dot X less than one half, gives true or false. If true, the first block runs, "
               "otherwise the else block. Declare c above: a variable made inside braces ends at the closing brace."),
    ("B29", 3, "The ternary is a one-line if. Write the condition, a question mark, the value if true, a colon, then the value if false. "
               "It gives back a value, so it can sit inside a longer line. Same picture, one line."),
    ("B30", 3, "A for loop repeats a block. This one runs five times, with the counter i going from zero to four, and each pass draws one stripe. "
               "The counter is an int, so convert it with float of i before mixing it with decimals."),
    ("B31", 3, "Use for when you know the count, and while when you do not. Take care: on modern graphics cards an infinite loop can freeze "
               "your application, the editor included, and Godot cannot protect you from it."),
    ("B32", 3, "Compare floats against a range, not with equals. Light U V dot X equal to exactly one half, and nothing draws here: "
               "no pixel center lands on it. A small range draws a thin line. The documentation warns float math varies by hardware."),
    ("B33", 3, "Two performance notes from the documentation. Discard, which throws a pixel away, has a cost. "
               "Modern graphics cards handle an if well when every pixel takes the same path, but too many branches can slow a shader down. "
               "This film did not measure either."),

    # ── ACT V · read one aloud ─────────────────────────────────────────────────────────────────────
    ("B34", 4, "Now read the file from the top. Use the same method: say the type of each piece, inside out, "
               "and check that every line's types fit together."),
    ("B35", 4, "Line three is a uniform, a vec four, so a color. Source color is a hint: the editor treats the value as a color. "
               "With no default, it is black until something sets it. Line four is a float with a default of two."),
    ("B36", 4, "Line six declares breathe. It hands back a vec three. It takes two arguments: a vec three called base, and a float called t. "
               "So the body gets a color and a number, and it must return a color."),
    ("B37", 4, "Line seven. Sine of t is a float that swings between minus one and one. Half of that, plus a half, is still a float, "
               "now swinging between zero and one. It is stored in wave."),
    ("B38", 4, "Line eight. Vec three of zero point nine fills all three parts: a pale gray. Mix blends that gray toward base by the amount wave. "
               "Zero gives the gray, one gives base. The result is a vec three, as promised."),
    ("B39", 4, "In fragment, tint dot R G B is a vec three, and time times speed is a float. Breathe turns them into a vec three. "
               "Vec four adds tint's alpha, and color, a vec four, takes it."),
    ("B40", 4, "Now watch it run. Pale gray blends to teal and back, and speed sets how fast. Every piece has a type, and every type fits. "
               "That is what it means to read a shader."),
    ("B41", 4, "Now change one thing. Make tint a vec three, and keep reading its alpha. A vec three has no alpha, and Godot says invalid member. "
               "Reading by types catches that before you run it."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. When you first read shader code, it is natural to assume each line works on one number at a time. "
         "It does not. Many values in a shader are bundles of numbers, and one operator works on the whole bundle at once.")
BIDEA_TEXT = ("A shader line works on\none number at a time.", "one number", "a bundle of numbers")

BDEFS = ("Five terms. A shader is a small program the graphics card runs to decide how something is drawn. A pixel is one dot of the picture. "
         "A type is the kind of value something holds. A function is a named block of code you can call. "
         "An argument is a value you hand it.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Pixel", "one dot of the picture on screen"),
    ("Type", "the kind of value something holds: whole number, decimal, bundle"),
    ("Function", "a named block of code you can call"),
    ("Argument", "a value you hand to a function when you call it"),
]

BVDT_HEADING = "Godot Shader Language"
BVDT_LINES = [
    "A shader file has a header, globals and functions.",
    "Every value has a type, and Godot will not quietly convert between int and float.",
    "Many values are vectors, and arithmetic works on every part at once.",
    "A function has a signature, and per-pixel built-ins must be passed in.",
    "Choices need a bool, and floats are compared against a range.",
    "To read a line, say the type of each piece.",
]
BVDT_NARRATION = ("Let's recap with Claude. A shader file has a header, globals and functions. "
                  "Every value has a type, and Godot will not quietly convert between int and float. "
                  "Many values are vectors, and arithmetic works on every part at once. "
                  "A function has a signature, and per-pixel built-ins must be passed in. "
                  "Choices need a bool, and floats are compared against a range. "
                  "To read a line, say the type of each piece.")

BHTF_PROMPT = ("Go through the Godot canvas item shader below one line at a time. After each line, add a comment giving the type of each piece. "
               "Flag any line where two types do not match. Then say in one sentence what it draws.")
BHTF_CHECKS = ["Check: pick one line and say the type of each piece yourself before you read Claude's.",
               "Check: run the shader. Does it draw what Claude's one sentence says?"]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Put your own shader under it. Now check two things yourself. Pick one line and say the type of each piece before you read Claude's answer. "
                  "And run the shader: does it draw what Claude's one sentence says?")
BHTF_SEGMENT = "Read a Shader by Its Types"

CUT_LINE = ("Cut, in this order: the overloading beat (B27), the two-performance-notes beat (B33), the global-built-ins half of B24 "
            "(keep the pass-it-in half), and the ternary beat (B29): each repeats an idea another beat already carries or is an extra. "
            "The vectors-and-swizzles beats (B12 to B17), the signature and built-in beats (B20, B23), and the whole reading act (B34 to B41) stay: "
            "they are the film.")

"""narration.py: every spoken line of "Outlines". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13), the installed Godot 4.7.2 on Bear's Mac (every number below was measured or rendered in
evidence/planning-checks/), one GPU programming reference from 2005 (GPU Gems 2, chapter 34) for the branching sentence, and a long third-party
video course whose order of ideas the film follows (nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input is labelled; the graphics card's own timer could not be
read on this setup, so the one timing claim is a labelled wall-clock stress test; the formula taught here assumes hard-edged art and the film says so.
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-outlines"
TITLE = "Outlines"
TITLE_LINES = ["Outlines"]
OPENING_DESCRIPTION = "How a shader draws a line around a sprite"
SUMMARY = "Learn how a shader draws a line around a sprite by asking each pixel about its neighbors, and the traps that make an outline vanish or break."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · OUTLINES"
TAGS = ["Godot", "Shaders", "Outline shader", "Sprite", "2D", "Fragment shader", "Uniform", "TEXTURE_PIXEL_SIZE", "Game development", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 on Apple M4 Pro (evidence/planning-checks); GPU Gems 2 chapter 34; see SOURCES.md"

ACTS = [
    ("I", "Ask the Neighbors"),
    ("II", "Pixel-Sized Steps"),
    ("III", "Say It with a Loop"),
    ("IV", "Room to Draw"),
    ("V", "Where It Breaks"),
]

BODY = [
    # ── ACT I · ask the neighbors ───────────────────────────────────────────────────────────────────
    ("B01", 0, "A sprite can melt into a busy background. Watch what an outline does: one clean line around its shape, in any color you like. The picture file never changes. A shader draws the line."),
    ("B02", 0, "The old trick draws a bigger copy of the sprite behind it. Scale a plus sign up a fifth: the tips get a thick border, the sides a thin one. Each edge moves in proportion to its distance from the middle."),
    ("B03", 0, "The shader asks something else. The graphics card runs one small program for every pixel, and each pixel checks its own alpha and the pixels around it. Am I empty, with an opaque neighbor? Then I am on the outline."),
    ("B04", 0, "To look next door, a pixel reads the sprite's image at another address. The function is texture. U V is the pixel's own address, so U V plus a small step is the spot beside it."),
    ("B05", 0, "What comes back is a color: four numbers, red, green, blue and alpha. Dot a picks the last one. Alpha zero is empty, alpha one is opaque. That one number is all the outline needs to know about a neighbor."),
    ("B06", 0, "Now the color. Mix blends two colors by an amount. Amount zero keeps the sprite's color, amount one gives the line color, and anything between is a blend. Outside zero to one, mix overshoots."),
    ("B07", 0, "First try, one question: is the pixel on my right opaque? If so, mix in the line color. Look what happens. Almost the whole sprite turns blue, because its own pixels have opaque neighbors too, and they all said yes."),
    ("B08", 0, "So ask one more thing: am I empty? Multiply by one minus my own alpha. Opaque pixels have alpha one, so they get zero and keep their color. Only empty pixels, on the left of the sprite, stay blue."),
    ("B09", 0, "Now ask all four sides, and add the answers. Almost right, but the diagonal stretches come out lighter. There, two neighbors are opaque, the sum is two, and mix overshoots past the line color."),
    ("B10", 0, "Cap the sum with min. Min of the sum and one can never be more than one, so mix never overshoots. Now every pixel of the ring is the same blue. Four reads, one cap, one mix: a complete outline."),

    # ── ACT II · pixel-sized steps ──────────────────────────────────────────────────────────────────
    ("B11", 1, "So far the step was point oh two: two percent of the picture. In pixels, that depends on the image: two and a half here, less than one on a thirty-two pixel sprite. Pixel art needs steps of whole pixels."),
    ("B12", 1, "Godot hands your shader a built-in for exactly this: texture pixel size, the size of one image pixel, in address units. For a sixty-four by thirty-two image, one over sixty-four and one over thirty-two."),
    ("B13", 1, "Multiply it by a thickness, a uniform: a value your game sets, the same for every pixel. Thickness one, two, three, four: the line is exactly one, two, three, four pixels wide. I measured it on this render."),
    ("B14", 1, "The line color is a uniform too. The word after the colon, source color, is a hint: it says this vec four is a color. Change the value and the line follows. Nothing else in the shader moves."),
    ("B15", 1, "Another way to see it: each read is the whole picture, slid by the step. Four reads are four slid copies, added together. The outline is wherever the copies stick out past the sprite itself."),
    ("B16", 1, "The step counts pixels of the image, not of the screen. Draw the sprite twice as big, and thickness two becomes four screen pixels. Three times as big, six. The line grows with the sprite, which is what pixel art needs."),
    ("B17", 1, "Four reads have one flaw. On a square sprite they leave the corners empty: at thickness three, a three by three hole in each one. Add the four diagonal neighbors, and the corners fill in."),

    # ── ACT III · say it with a loop ────────────────────────────────────────────────────────────────
    ("B18", 2, "Eight reads, written out: the four sides and the four corners. It works. It is also eight nearly identical reads, which is exactly where typos hide."),
    ("B19", 2, "A loop says it once. For each y from minus one to one, and each x from minus one to one, read the alpha at that offset. Add it all up. Nine offsets, a three by three block."),
    ("B20", 2, "The block's middle is the pixel itself, an extra read that changes nothing on hard-edged art. And those float calls are not decoration: Godot refuses to build a vec two from two whole numbers. Here is its message."),
    ("B21", 2, "Same picture? I rendered both, at thickness one, two, three, four and eight, and compared every pixel. Zero pixels differ. On hard-edged art, the loop does exactly what the eight written-out reads did."),
    ("B22", 2, "Count the work: nine reads in the loop, plus one for the pixel itself, ten per pixel. In a stress test on this Mac, four hundred million pixels a frame, ten reads took about ten milliseconds; a nine by nine block, eighty-two reads, about seventy. Time follows reads."),
    ("B23", 2, "Many outline shaders wrap the loop in an if on the thickness. Thickness zero means off: the loop is skipped, and one read is left. Godot gives you no early exit here: a return inside fragment is a compile error."),
    ("B24", 2, "Is an if slow? Godot's shading language docs warn about discard and endless loops, not about if. A graphics book from two thousand five says a branch costs extra when neighboring pixels disagree. Here every pixel reads the same thickness, so they all agree."),
    ("B25", 2, "The guard does more than save work. Without it, thickness zero still paints line color into the half-transparent rim of a soft-edged sprite: two hundred and twenty-four pixels in my test. With the guard, none."),
    ("B26", 2, "Your game turns the dial. When the unit is selected, set thickness to two. When it is not, set it back to zero. The call is set shader parameter on the material, with the uniform's name and a value."),
    ("B27", 2, "One trap. Set shader parameter changes the material, and units made from one scene share it, so every unit lights up at once. Declare the uniform as instance, and set it on the node instead. That value belongs to this instance only."),

    # ── ACT IV · room to draw ───────────────────────────────────────────────────────────────────────
    ("B28", 3, "Read a step to the right, and each pixel shows what is on its right, so the picture slides left. Slide it far enough, and its left side is cut off flat. A shader paints only inside the sprite's own rectangle."),
    ("B29", 3, "That is the trap for outlines. Here the art was trimmed to its shape, with no empty border. Turn the outline up to four, and nothing appears where the shape touches the edge. The line has nowhere to go."),
    ("B30", 3, "The fix is padding: transparent pixels around the image. In code, make a bigger transparent image, copy the original into the middle with blit rect, and make a texture from it."),
    ("B31", 3, "Same shader, thickness four. No padding: the line is cut off. Two pixels of padding: cut at two. Four: the full ring. Pad by at least your thickest line. A centered sprite stays put; one that is not moves by the padding."),
    ("B32", 3, "A sprite sheet adds a twist: U V covers the whole sheet, not one frame. Godot's docs say so for regions; I measured it for frames. A read past a frame's edge lands in the next frame and draws a stray line. Separate frame images avoid it."),
    ("B33", 3, "Padding is the simple cure. When you cannot pad, Godot gives the shader region rect, the visible frame. Clamp each read into it, and the stray line is gone: zero stray pixels in my test, and the sprite's own ring untouched."),

    # ── ACT V · where it breaks ─────────────────────────────────────────────────────────────────────
    ("B34", 4, "Now push the thickness. At eight, the four-read line pinches in at the diagonals. The eight-read line bulges into a rounded square. A ring of sixteen reads stays round."),
    ("B35", 4, "The reads are the brush. Four make a diamond, eight a square, sixteen a circle. Straight across, each line is eight pixels wide. On the diagonal I measured about five, eleven, and eight."),
    ("B36", 4, "The ring is the loop with a different offset: sixteen angles around a full turn, one distance. Seventeen reads. Sine and cosine at every read cost extra: about thirty-seven milliseconds in the stress test, sixteen with the directions written as constants."),
    ("B37", 4, "Thin parts break it too. This stem is three pixels wide. At thickness eight, eight reads jump clean over it, and the line comes apart into floating copies. The ring of sixteen holds it together."),
    ("B38", 4, "Soft edges are the next trap. Smooth art has half-transparent pixels on its rim. Mix blends alpha too, so the rim stays see-through: a quarter transparent at worst in my test. Compute the alpha yourself, and the seam closes."),
    ("B39", 4, "And the texture filter. Linear filtering blends four pixels on every read, so the alpha you ask about turns blurry. In my test, linear made two thousand half-transparent pixels; nearest made none. Godot's default is linear. For pixel art, set nearest."),
    ("B40", 4, "One more thing a shader can ignore: modulate, the node's own tint and fade. Fade a sprite whose shader assigns color from the texture, and nothing fades. Pass the vertex color on through a varying, and multiply it in."),
    ("B41", 4, "So four checks for any outline shader, yours or an AI's. Is there padding at least as thick as the line? Does the step count image pixels? How many reads per pixel? Is the filter nearest, and does modulate still fade it?"),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Most people picture an outline as a bigger copy of the sprite, hiding behind it. "
         "A shader has no second copy. Each pixel asks a question about its neighbors, and the answers draw the line.")
BIDEA_TEXT = ("An outline is\na bigger copy behind the sprite.", "a bigger copy behind the sprite", "a question about neighbors")

BDEFS = ("Six terms. A shader is a small program the graphics card runs to decide how something is drawn. A texture is an image a shader can read. "
         "Alpha is how visible a pixel is. Opaque means fully visible. A neighbor is the pixel next to this one. And padding is empty space around an image.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("Texture", "an image a shader can read by address"),
    ("Alpha", "how visible a pixel is: 0 invisible, 1 solid"),
    ("Opaque", "fully visible: nothing shows through"),
    ("Neighbor", "the pixel right next to this one"),
    ("Padding", "empty space added around an image"),
]

BVDT_HEADING = "Outlines"
BVDT_LINES = [
    "An outline is a question each pixel asks its neighbors.",
    "Steps count image pixels, from texture pixel size.",
    "A loop reads the neighbors, and the cost follows the reads.",
    "A shader paints only inside its rectangle, so pad the image.",
    "Thick lines bend the brush; thin parts and soft edges break it.",
    "Check padding, step size, reads, filter and modulate, yours or an AI's.",
]
BVDT_NARRATION = ("Let's recap with Claude. An outline is a question each pixel asks its neighbors. Steps count image pixels, from texture pixel size. "
                  "A loop reads the neighbors, and the cost follows the reads. A shader paints only inside its rectangle, so pad the image. "
                  "Thick lines bend the brush; thin parts and soft edges break it. Check padding, step size, reads, filter and modulate, yours or an AI's.")

BHTF_PROMPT = ("Write a Godot canvas item shader that outlines a sprite. Give it a color uniform called line color, and an instance uniform called thickness, "
               "a float in image pixels from zero to four. Read the neighbors in a three by three loop. Thickness zero must change nothing. "
               "Then tell me how much empty border the image needs.")
BHTF_CHECKS = ["Check: at thickness two the line is exactly two image pixels wide on every side.",
               "Check: at thickness zero the sprite looks identical to having no shader."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Now check two things yourself. At thickness two, is the line exactly two image pixels wide on every side? "
                  "And at thickness zero, does the sprite look identical to having no shader?")
BHTF_SEGMENT = "Ask for an Outline, Then Check It"

CUT_LINE = ("Cut, in this order: the line-color beat (B14), the loop-cost beat (B22), the branch beat (B24), the modulate beat (B40), then the thin-part beat (B37) and the "
            "brush-number beat (B35). The corner beat (B17), the padding beats (B29 to B31) and the checks table (B41) stay: they are the proof and the payoff.")

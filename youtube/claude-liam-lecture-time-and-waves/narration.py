"""narration.py: every spoken line of "Time and Waves". Liam, in for Bear (Kokoro am_onyx). Standalone film, not numbered.

Sources: the Godot 4.7 documentation (read 2026-10-13, quoted in evidence/planning-checks/docs-quotes.md), the installed Godot 4.7.2 on Bear's Mac
(every number below was measured in evidence/planning-checks/), and a third-party video course on shader time, sine waves and flags (ideas followed,
nothing copied; see SOURCES.md).
Honesty rules for this film: measured numbers say what machine and renderer; scripted input is labelled; the one-hour roll-over is not waited for
(its mechanism was checked with the limit set to two seconds, and the film does not claim otherwise).
Numbers are written as words and acronyms with spaced letters because the voice reads them better; the screen keeps the real figures.

The model the film teaches: TIME x speed counts cycles; a shape function turns the count into a look. Four numbers describe a sine wave:
amplitude (how far from the middle), frequency (how many cycles across a shape), speed (how quickly the count runs) and offset (where in its cycle it
starts, counted in cycles). "The middle" (the 0.5 in 0.5 + ...) is the lift that fits a sine into zero to one, not a fifth knob.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S  # noqa: E402

SLUG = "claude-liam-lecture-time-and-waves"
TITLE = "Time and Waves"
TITLE_LINES = ["Time and Waves"]
OPENING_DESCRIPTION = "Pulses, loops and ripples from one clock"
SUMMARY = "Learn what a shader's clock really counts, and how one sine wave with four numbers makes a pulse, a loop or a ripple."
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · TIME AND WAVES"
TAGS = ["Godot", "Shaders", "TIME", "Sine wave", "Animation", "Fragment shader", "Uniform", "Tween", "Nik Bear Brown"]
SOURCE_DOC = "Godot 4.7 documentation; Godot 4.7.2 runs on Apple M4 Pro (evidence/planning-checks); see SOURCES.md"

ACTS = [
    ("I", "One Clock"),
    ("II", "The Wave"),
    ("III", "Loops and Curves"),
    ("IV", "Waves on a Shape"),
    ("V", "One Clock, Two Effects"),
]

BODY = [
    # ── ACT I · one clock ───────────────────────────────────────────────────────────────────────────
    ("B01", 0, "Two squares run the same pulse shader. The second one joins late. If time began when a node appears, its pulse would start over from the beginning. Watch. It arrives already in step with the first."),
    ("B02", 0, "A shader cannot count: every frame it starts fresh, remembering nothing from the last. So the engine hands it a clock called time, the seconds since the engine started. One clock, shared by the whole game."),
    ("B03", 0, "Two things you might expect to matter. The game's time scale does: at one half, the clock runs at half speed for every shader. Pausing does not. Scripts freeze, but the shimmer carries on."),
    ("B04", 0, "The clock also has a limit. It wraps back to zero after thirty-six hundred seconds, one hour, by default. A pulse that repeats a whole number of times in that hour will not notice. Any other pulse jumps once."),
    ("B05", 0, "To time a node from its birth, you might reach for the engine's tick counter, and subtract. Do not. It starts earlier than time: about a quarter of a second on this Mac, and a little different every run."),
    ("B06", 0, "It also ignores the time scale. Run one second at half speed, and the tick counter ends up half a second ahead. The two clocks never agree again."),
    ("B07", 0, "To start counting when a node appears, count it yourself. Add delta, the seconds since the last frame, to an age, and pass the age to the shader as a uniform. Now the late square starts its pulse from the beginning."),
    ("B08", 0, "So choose by the job. A loop that never needs to start: use time. An effect that begins with a node: use an age. A one-time effect: use a uniform your game moves when the moment comes."),

    # ── ACT II · the wave ───────────────────────────────────────────────────────────────────────────
    ("B09", 1, "Now the wave. Put the clock inside a sine, and the value swings smoothly between minus one and one. Sine counts in angles, so one full swing takes six point two eight seconds. That number is tau."),
    ("B10", 1, "That is awkward. Multiply time by tau first, so one second becomes one full turn. Now each swing takes exactly one second."),
    ("B11", 1, "A color cannot go below zero, and sine does, half the time. Send a raw sine to a color and every negative value is clamped to zero. The pulse sits at its darkest for half of each swing."),
    ("B12", 1, "So squeeze it into zero to one. Halve the swing, then lift it by a half. Zero point five plus zero point five times sine never leaves the range, and it still swings once per second."),
    ("B13", 1, "Here is that line as a shader. The pulse blends two colors: at zero, all teal; at one, all cream. Mix does the blending. The square swings between them once a second."),
    ("B14", 1, "Four numbers describe a sine wave. The first is amplitude: how far it swings from its middle. Shrink it and the pulse gets shallow; at zero it stops. A half is the most that fits in zero to one."),
    ("B15", 1, "The second is speed: how quickly it repeats. Time times speed counts the cycles, one cycle being one full swing. Speed one half gives a swing every two seconds. Speed two gives two swings every second."),
    ("B16", 1, "The third is offset: where in its cycle the wave starts. Offset a quarter starts it at the top. Offset a half swings exactly opposite to a wave with none: when one is brightest, the other is darkest."),
    ("B17", 1, "Here are all three as uniforms, dials your game can set. Time times speed, plus offset, counts the cycles. Offset is an instance uniform, so each node can keep its own. The fourth number waits for a shape."),
    ("B18", 1, "Five squares, one shader, one clock. Each gets its own offset: zero, a fifth, two fifths, and so on. Their pulses no longer match, and together they roll along the row, like a wave."),

    # ── ACT III · loops and curves ──────────────────────────────────────────────────────────────────
    ("B19", 2, "Sine always swings back. For a loop that starts over, like a loading bar, use fract. It keeps only the part after the decimal point, so the cycle count becomes a ramp from zero to one, restarting every cycle."),
    ("B20", 2, "To go back and forth at a steady pace, fold the ramp: double it, subtract one, take the absolute value, and subtract that from one. You get a triangle, rising and falling at the same rate."),
    ("B21", 2, "Same pace, three personalities. The sine eases into each turn. The triangle turns sharply. The sawtooth never turns back: it climbs, then jumps to the start. Pick the one whose motion you want."),
    ("B22", 2, "Sometimes no formula gives the shape you want: a slow start, a quick snap, a gentle settle. Draw it as a curve. A curve texture bakes the curve into a strip of pixels, brighter where the curve is higher."),
    ("B23", 2, "The lookup is one line. Hand the strip a position from zero to one, and read its red channel. Feed it the restarting ramp, and the curve plays on a loop."),
    ("B24", 2, "Feed the same curve from a sine and it plays forward, then backward, every cycle. Feed it from the ramp and it plays one way, then restarts. Use the ramp when the motion should always go the same way."),
    ("B25", 2, "So one count gives four looks. Sine swings smoothly. Triangle swings at a steady rate. Sawtooth restarts. And a curve is whatever you draw."),

    # ── ACT IV · waves on a shape ───────────────────────────────────────────────────────────────────
    ("B26", 3, "The row of squares gave each one a different offset. A shape has a different position at every pixel. So let the address supply the offset, and every pixel gets its own place in the wave."),
    ("B27", 3, "Use the address across the shape as the count, and the sine becomes stripes. The number of stripes is the fourth number, frequency: how many cycles fit across the shape. Three cycles, three bright stripes."),
    ("B28", 3, "Now subtract time from the address, and the stripes slide right. Speed is how far they travel each second, as a fraction of the shape: one half means half the shape every second. A negative speed slides them left."),
    ("B29", 3, "The count does not have to come from the address across. On a square shape, use the distance from the middle, and the stripes become rings that spread outward, like a drop in water."),
    ("B30", 3, "That is all four. Amplitude is how tall. Frequency is how many cycles across. Speed is how fast they slide. Offset is where they start. Each can change without touching the others."),
    ("B31", 3, "Brightness is only one use. Add the wave to the address you look up, and the picture itself ripples. No new corners are needed: the rectangle stays put, and only the lookup moves."),
    ("B32", 3, "Multiply the wave by the address across, and the left edge cannot move. The right end waves freely, like a flag on a pole."),
    ("B33", 3, "One limit. The rectangle itself does not bend, so a big ripple drags in edge pixels, and the edges smear. Leave empty margin around the art, or move real corners instead."),
    ("B34", 3, "Add two waves with different frequencies and speeds, and the pattern stops repeating so plainly. Each wave has its own amplitude, frequency and speed, and the shader adds the results."),

    # ── ACT V · one clock, two effects ──────────────────────────────────────────────────────────────
    ("B35", 4, "Now use everything at once. A logo breathes, and a banner waves. Two shaders read the same clock, and the game adds one thing: a click."),
    ("B36", 4, "The breath is a curve: a slow rise, a short hold, a long fall. The restarting ramp plays it once per cycle. The logo's size is one plus a quarter of the curve."),
    ("B37", 4, "To make a picture bigger, look it up from closer in. Measure the address from the middle, divide it by the scale, and measure back. A scale of one and a quarter shows the picture a quarter bigger."),
    ("B38", 4, "Here is the logo live. The curve is a texture, the ramp reads it, and the logo swells and settles about its middle. The art keeps empty margin, so nothing smears."),
    ("B39", 4, "The banner is the traveling wave from before, pinned at the left, drawn as stripes so you can see the cloth move. A wind uniform scales the wave: at zero, the banner hangs still."),
    ("B40", 4, "When the player clicks, set wind to one, then tween it back to zero. The banner snaps into motion, then settles. A moment belongs to your game. Time keeps the beat; a uniform picks the moment."),
]

BIDEA = ("Hallo. This is Liam, in for Bear. Every shader can read a clock, called time. Most people expect it to start when their node appears. "
         "It does not. It starts when the game starts, and every shader reads the same one.")
BIDEA_TEXT = ("TIME starts at zero\nwhen my node appears.", "when my node appears", "when the game starts")

BDEFS = ("Six terms. A shader is a small program the graphics card runs to decide how something is drawn. Fragment is the function that runs once for each pixel. "
         "A uniform is a value your game sets from outside. U V is a point's address on the shape. A texture is an image a shader can read. "
         "And sine is a function that swings smoothly between minus one and one.")
BDEFS_TERMS = [
    ("Shader", "a small program the graphics card runs to decide how something is drawn"),
    ("fragment()", "runs once for each pixel the shape covers; sets its color"),
    ("Uniform", "a value your game sets from outside; every pixel sees the same one"),
    ("UV", "a point's address on the shape: 0 to 1 across, 0 to 1 down"),
    ("Texture", "an image a shader can read by address"),
    ("Sine", "a function that swings smoothly between -1 and 1"),
]

BVDT_HEADING = "Time and Waves"
BVDT_LINES = [
    "Time is one clock for the whole game; count your own with an age.",
    "Time times speed counts cycles, and a sine turns the count into a pulse.",
    "Fract, a fold or a curve turns the same count into another loop.",
    "Feed the count from the address, and the wave travels across a shape.",
    "Four numbers set any sine wave: amplitude, frequency, speed and offset.",
    "Time keeps the beat; a uniform picks the moment.",
]
BVDT_NARRATION = "Let's recap with Claude. " + " ".join(BVDT_LINES)

BHTF_PROMPT = ("Write a Godot canvas item shader for a Color Rect that pulses between two colors with a sine of time. "
               "Use three float uniforms: amplitude, speed in cycles per second, and offset in cycles. "
               "Keep the result between zero and one, and show me the line where time becomes a pulse.")
BHTF_CHECKS = ["Check: with amplitude at zero, the color holds still.",
               "Check: a second copy with offset one half pulses exactly opposite the first."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. With amplitude at zero, does the color hold still? "
                  "And does a second copy with offset one half pulse exactly opposite the first?")
BHTF_SEGMENT = "Pulse With Three Dials"

CUT_LINE = ("Cut, in this order: the two-waves beat (B34), the roll-over beat (B04), the edge-smear beat (B33) and the sine-or-ramp beat (B24): "
            "each extends an idea another beat already carries. The late-join demo (B01), the clock-mixing pair (B05, B06), the three knob beats "
            "(B14 to B16), the travel beat (B28) and the wind click (B40) stay: they are the proof and the payoff. The curve-texture pair (B22, B23) "
            "stays because the breathing logo reads one; if both must go, the logo breathes from a sine and B36 to B38 shrink to two beats.")

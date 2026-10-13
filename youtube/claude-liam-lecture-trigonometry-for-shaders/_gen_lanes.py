#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text (and the highlighted line numbers must be the real ones), cue times
must follow the narration, and the shot list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
Cue times are fractions of a beat, computed from where a phrase starts in the narration (words before it / words in the beat), pushed out of
the 45-55 % window that GATE T and Gate V sample. The build session may refine them against the measured audio.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
TEXT = {bid: t for bid, _, t in N.BODY}
E = []          # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def ln(fn, needle, nth=1):
    """1-based line number of the nth line of a shader file containing `needle`."""
    hits = [i + 1 for i, line in enumerate(code_of(fn).split("\n")) if needle in line]
    assert len(hits) >= nth, f"{needle!r} not found in {fn}"
    return hits[nth - 1]


def at(bid, phrase, lead=0.0):
    """Fraction of the beat at which `phrase` starts in the narration, kept out of the 45-55 % window."""
    t = TEXT[bid]
    i = t.lower().index(phrase.lower())
    frac = len(t[:i].split()) / len(t.split())
    v = round(min(0.96, max(0.03, frac + lead)), 2)
    if 0.45 <= v <= 0.55:
        v = 0.44 if v < 0.5 else 0.56
    return v


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (film-local kit objects, see Must exist)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, caption="", lane="capture"):
    props = {"layout": layout, "code": code_of(shader) if shader else "", "codeFile": f"lab-shaders/{shader}" if shader else "", "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption, "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    entry = {"lane": lane, "pattern": "ShaderLab", "props": props, "visual_intent": intent, "motion_claim": motion, "show": show,
             "runner_up": runner, "why": why, "sparse": False}
    if spec:
        entry["capture_spec"] = spec
    add(bid, act, about, entry, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


MOON = "01-moon-fixed.gdshader"
ORBIT = "02-orbit.gdshader"
FAST = "03-orbit-fast.gdshader"
ASPECT = "04-orbit-aspect.gdshader"
MOONS = "05-moons-evenly.gdshader"
METEOR = "06-meteor-orbit.gdshader"
REVERSE = "07-meteor-reverse.gdshader"
COLORS = "08-atan-colors.gdshader"
ONEARG = "09-atan-one-argument.gdshader"
SWEEP = "10-sweep.gdshader"
SWEEPTOP = "11-sweep-top.gdshader"
FLOWER = "12-flower.gdshader"

# ───────────────────────────── ACT I · One Angle, Two Numbers ─────────────────────────────
lab("B01", 0, "the destination: a moon and a meteor on orbits, from one shader", METEOR, "godot-shaders/trig-hook.mp4",
    "Godot 4.7.2 · Forward+ · runs on the game clock", [],
    "Act title 'One Angle, Two Numbers' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a teal planet in the middle, a slate-blue moon circling it clockwise and a small amber meteor circling the moon, all on the warm grey stage color. No code is shown yet.",
    "The moon laps the planet and the meteor laps the moon, continuously, from the first frame.",
    [{"at": 0.0, "event": "window opens with the planet, moon and meteor already moving"}, {"at": 0.6, "event": "still circling: the picture the whole film builds toward"}],
    "manim drawing of a planet, moon and meteor on orbit rings",
    "A real render is the honest preview of the destination; a drawing would only claim it, and later acts rebuild exactly this picture.",
    "C01: Lab rect, lab-shaders/06-meteor-orbit.gdshader, square (480 x 480 logical canvas captured at 1920 x 1920), live TIME, 14 s, 30 fps, Forward+, no input. The moon laps the planet in 6.28 s, so about two laps show.",
    "Lab render C01; shader compiled in the Lab; moon +1.00 rad/s clockwise, meteor +3.00 rad/s around the moon (batch run)", layout="video", title=N.ACTS[0][1])

manim("B02", 0, "the right triangle and the names of its sides", "RightTriangle",
      "A right triangle in grey outline on the cream stage, right angle at the lower right marked with a small square, the other angles at the lower left (30 degrees, marked by a thick terracotta arc and a small terracotta dot) and the top right. As each word is spoken the matching side thickens to ink and takes a 1 to 3 word serif label placed outside the outline: 'hypotenuse' on the long slanted side, 'opposite' on the right-hand vertical (across from the marked angle), 'adjacent' on the bottom (touching the marked angle). The 50 % frame holds the settled picture with the hypotenuse label and the marked angle.",
      "Each side thickens and takes its name exactly when the voice says it.",
      [{"at": 0.05, "event": "triangle draws; right-angle square"}, {"at": at("B02", "Its longest side"), "event": "hypotenuse thickens, label lands"},
       {"at": 0.4, "event": "marked angle (arc and dot) appears at the lower left (done by 0.44)"},
       {"at": at("B02", "The side across from it"), "event": "opposite side thickens, label lands"},
       {"at": at("B02", "The side touching it"), "event": "adjacent side thickens, label lands"}],
      "LectureEvidenceTable (a three-row glossary)",
      "Naming parts of a shape is pointing at them: each side lights up as its name is spoken, which a table cannot do.",
      "Manim only (film-local kit: right_triangle)")

manim("B03", 0, "the ratio belongs to the angle, not to the size", "SameRatio",
      "The same 30-degree triangle anchored at its marked lower-left corner. At the right, a readout in serif: 'opposite ÷ hypotenuse' over a large number. First the triangle scales (about 1.0, then 0.55, then 1.3) while thin grey ghosts of the earlier sizes stay nested at the same corner and the number stays 0.50 the whole time. After a hold (settled still at the 50 % frame: three nested outlines, '30°' and 0.50), the marked angle opens to 50 degrees: the hypotenuse swings up, the triangle reshapes, the angle label reads '50°' and the number settles at 0.77. A terracotta dot rides the top corner.",
      "The triangle grows and shrinks and the number does not move; the angle opens and the number does.",
      [{"at": 0.08, "event": "triangle at 30 degrees, readout 0.50"}, {"at": at("B03", "Fix the angle"), "event": "triangle scales down and up, ghosts nest, readout stays 0.50"},
       {"at": 0.44, "event": "settled: three nested outlines, 30°, 0.50 (hold through the midpoint)"}, {"at": at("B03", "At fifty"), "event": "angle opens to 50°, readout changes to 0.77"}],
      "LectureEvidenceTable (angle against ratio, two rows)",
      "Size changing while the number stays put is the claim, and only moving geometry with a live readout shows it.",
      "evidence/planning-checks/verify-math.gd G (ratio constant to 1e-16 for sizes 1 to 1000; sin 50 degrees = 0.766)")

manim("B04", 0, "sine, cosine and tangent as ratios of sides; the memory trick", "SohCahToa",
      "Left: the 30-degree triangle in grey, smaller. Right: three stacked outlined rows (padding, no fill behind text): 'sine · opposite ÷ hypotenuse', 'cosine · adjacent ÷ hypotenuse', 'tangent · opposite ÷ adjacent'. As each name is spoken its row lands and the two sides it uses thicken to ink on the triangle (sine: opposite and hypotenuse; cosine: adjacent and hypotenuse; tangent: opposite and adjacent) while the others return to grey. At the end 'SOH CAH TOA' sets under the rows with each first letter aligned to its row.",
      "Two sides of the triangle light up for each ratio as the voice names it.",
      [{"at": 0.06, "event": "triangle and the three empty rows"}, {"at": at("B04", "Opposite over hypotenuse"), "event": "sine row lands; opposite and hypotenuse thicken"},
       {"at": at("B04", "Adjacent over hypotenuse"), "event": "cosine row lands; adjacent and hypotenuse thicken"},
       {"at": 0.4, "event": "tangent row lands as text (done by 0.44; hold through the midpoint)"},
       {"at": 0.56, "event": "tangent's two sides thicken: opposite and adjacent"}, {"at": at("B04", "The memory trick"), "event": "SOH CAH TOA sets under the rows"}],
      "LectureEvidenceTable",
      "The table would list the three ratios; lighting the matching sides on the triangle shows which sides each one uses.",
      "Manim only (film-local kit: right_triangle)")

manim("B05", 0, "sine and cosine as lookups: angle in, number out", "Lookup",
      "Two outlined boxes stacked on the cream stage, labelled 'sine' (upper) and 'cosine' (lower). At the left a small wedge token marked '30°' slides along a short drawn arrow into the sine box; a number token '0.50' slides out at the right. The same 30-degree token then enters the cosine box and '0.87' leaves it. One short line under the boxes: 'angle in, number out'. Arrows are drawn shapes, not glyphs; the 50 % frame holds with the sine result '0.50' settled.",
      "A 30-degree token enters each box and a number leaves it.",
      [{"at": 0.08, "event": "two boxes appear"}, {"at": at("B05", "Hand one an angle"), "event": "30° token enters sine; 0.50 leaves"},
       {"at": at("B05", "Cosine of thirty"), "event": "30° token enters cosine; 0.87 leaves"}, {"at": at("B05", "An angle goes in"), "event": "caption 'angle in, number out'"}],
      "DesignPipelineClaim, show-tell isometric",
      "Two tiny functions as boxes with a token passing through is the whole idea; isometric detail would add decoration, not meaning.",
      "evidence/planning-checks/run-1-verify-math.log (sin 30 = 0.5, cos 30 = 0.866) and the Lab 21-trig-values probe (0.502, 0.8667)")

# ───────────────────────────── ACT II · Angle In, Position Out ─────────────────────────────
manim("B06", 1, "the triangle inside a circle: walk out at an angle", "UnitCircle",
      "Act title 'Angle In, Position Out' (serif 40) top-left. On paper orientation (y up, a small grey caption 'on paper'): a circle with a faint cross of axes, 'radius 1' on a radius. A radius line sweeps from the right-hand axis up to 30 degrees and a terracotta dot lands on the circle where it ends. Then the triangle from before draws in: a dashed vertical drop from the dot to the horizontal axis and the horizontal leg along the axis. The marked angle is a thick terracotta arc, never a filled wedge.",
      "The radius turns to the angle, the dot lands on the circle, and the triangle's two short sides drop from it.",
      [{"at": 0.08, "event": "act title; circle, axes, 'on paper' caption"}, {"at": at("B06", "Walk out"), "event": "radius sweeps to 30 degrees; dot lands; 'radius 1'"},
       {"at": 0.44, "event": "settled (hold through the midpoint)"}, {"at": at("B06", "The triangle's two short sides"), "event": "dashed drop and horizontal leg draw in"}],
      "ShaderLab (a shader drawing a circle)",
      "This is paper geometry; Manim draws it exactly, and the same circle and dot are reused unchanged in the next beats (one cast per act).",
      "Manim only (film-local kit: unit_circle, right_triangle)")

manim("B07", 1, "with radius one, the legs are the sine and the cosine", "LegsAreCosSin",
      "The same circle, dot and triangle (paper orientation, y up, as in the previous beat). The tag 'unit circle' lands beside the circle. The horizontal leg takes the label 'cos' and the vertical leg 'sin'; the hypotenuse keeps 'radius 1'. Beside the circle a live readout in serif: 'cos 0.87' over 'sin 0.50'. A faded '÷ 1' on each ratio shrinks away as the voice says dividing by one changes nothing. After a hold (settled at 30 degrees through the midpoint) the angle swings to 60 degrees and back to 30, the legs resizing and both readout numbers following (0.50 and 0.87 at 60 degrees); the point label '(cos, sin)' sits at the dot.",
      "As the angle opens, the two legs and the two readout numbers change together: the point's across and up are exactly the cosine and sine.",
      [{"at": 0.06, "event": "'unit circle' tag; legs labelled cos and sin; readout 0.87 / 0.50"}, {"at": at("B07", "so dividing by one"), "event": "'÷ 1' shrinks away"},
       {"at": 0.44, "event": "settled at 30 degrees (hold through the midpoint)"}, {"at": at("B07", "The point sits at"), "event": "angle swings to 60 and back; legs and readout follow; '(cos, sin)' label"}],
      "LectureEvidenceTable",
      "The claim is that the legs ARE the numbers; watching leg lengths and readouts move together shows it.",
      "evidence/planning-checks/verify-math.gd (cos 30 = 0.8660, sin 30 = 0.5; sin 60 = cos 30 by H)")

rem("B08", 1, "Godot's own manual defines the point at an angle as cosine, sine", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/classes/class_vector2.html#class-vector2-method-from-angle",
     "image": "godot-shaders/docs-vector2-from-angle.png", "caption": "Godot 4.7 documentation · Vector2 · from_angle() · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1},
                                  {"at": 0.2, "x": 0.42, "y": 0.36, "scale": 1.6, "ring": [0.1, 0.34, 0.8, 0.07]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 Vector2 class page scrolled to from_angle(); the camera pushes in on the sentence 'This is equivalent to doing Vector2(cos(angle), sin(angle)) or Vector2.RIGHT.rotated(angle).' and one terracotta ring marks it. The move and ring coordinates are set from the real screenshot at build time.",
    "The camera pushes in on the sentence the voice is describing and a terracotta ring marks it.",
    [{"at": 0, "event": "page"}, {"at": 0.2, "event": "push-in lands on the from_angle entry; the ring draws on the equivalence sentence (all settled before the 45 % mark)"}],
    "manim: GDScript line Vector2.from_angle(a) beside Vector2(cos(a), sin(a))",
    "The claim is that Godot's own manual says it; the manual itself is the evidence (SHOW-THE-THING rung 1).",
    "D1: Playwright capture of the live docs page (1600 x 900 at 2.4x); text read 2026-10-13; anchor id class-vector2-method-from-angle exists; verify-math.gd A: from_angle(a) equals Vector2(cos a, sin a) to 1e-7")

manim("B09", 1, "scale by the radius, shift by the center", "RadiusAndCenter",
      "The circle from before (paper orientation, y up) with its terracotta dot at 30 degrees. A formula builds under it, term by term, in the monospace face (32 or larger): 'c + r * vec2(cos(a), sin(a))'. As 'r *' lands the circle grows from radius 1 to 1.8 with the dot riding on it at the same angle; as 'c +' lands the whole circle slides to a new center (a small terracotta cross marks the center and travels with it). The 50 % frame holds the grown and moved circle with the whole formula landed.",
      "The circle grows when the radius lands and slides when the center lands, with the dot riding along at the same angle.",
      [{"at": 0.06, "event": "circle, dot, empty formula line"}, {"at": at("B09", "Multiply by the radius"), "event": "'r *' lands; circle grows with the dot on it"},
       {"at": at("B09", "Add the center"), "event": "'c +' lands; circle and center cross slide to a new place"}, {"at": at("B09", "So center plus radius"), "event": "whole formula settles"}],
      "LectureCodeTrace (the formula as code)",
      "Scaling and shifting are things the circle does; the formula alone would not show that the same dot stays on the same angle.",
      "Manim only (film-local kit: unit_circle)")

manim("B10", 1, "one worked example by hand", "WorkedExample",
      "A circle drawn as a labelled ring of radius 0.6 (the number 0.6 on its axis) with the terracotta dot at 30 degrees. Two lines of arithmetic build beside it as the voice reads them, serif 32 or larger: '0.6 × cos 30° = 0.52' (the horizontal drop lights up in ink) and '0.6 × sin 30° = 0.30' (the vertical drop lights up). The two results end boxed together as '(0.52, 0.30)' beside the dot with a small grey line 'hold on to these'. Paper orientation (up positive); the dot is not mirrored.",
      "The two drops light up in turn as each product is read, and the two results meet as one point.",
      [{"at": 0.06, "event": "ring r = 0.6 with the dot at 30 degrees"}, {"at": at("B10", "The first number"), "event": "horizontal drop lights; '0.6 × cos 30° = 0.52'"},
       {"at": at("B10", "The second"), "event": "vertical drop lights; '0.6 × sin 30° = 0.30'"}, {"at": at("B10", "Hold on to"), "event": "'(0.52, 0.30)' boxed beside the dot"}],
      "LectureCodeTrace (the two lines of code)",
      "Walking one point through the arithmetic while the circle is on screen is the worked example the idea needs; two beats later the shader must land on these numbers.",
      "verify-math.gd E (0.6 cos 30 = 0.519615, 0.6 sin 30 = 0.3 exactly) and the Lab 01-moon-fixed probe")

manim("B11", 1, "radians: the radius walked around the edge", "Radians",
      "A circle (paper orientation, y up) with its radius drawn as a thick ink bar from the middle. The bar copies itself onto the circle's edge as a bent arc of exactly its own length, starting at the right-hand axis; a thick terracotta arc marks the angle it covers, labelled 'radian' (a thick arc, never a filled wedge). Copies lay end to end around the circle while a counter ticks 1, 2, 3, 4, 5, 6, and a short leftover piece closes the loop; the label ends '6.28 = a full turn'. The 50 % frame holds with about three copies laid and the counter at 3.",
      "The radius is laid end to end around the circle: six whole copies and a short remainder.",
      [{"at": 0.06, "event": "circle and radius bar"}, {"at": at("B11", "Lay one radius"), "event": "first copy lays on the edge; 'radian' arc"},
       {"at": 0.34, "event": "copies 2 and 3 lay (hold through the midpoint)"}, {"at": at("B11", "A full turn takes"), "event": "copies 4 to 6 and the leftover piece; label 6.28"}],
      "plot / ramp strip with a marker",
      "'A radius walked around the edge' is only convincing when you see it walked.",
      "verify-math.gd I (six whole radii and a leftover 0.2832 make a full turn of 6.2832); Godot docs: TAU is 'the number of radians in a full turn'")

manim("B12", 1, "pi and tau name the turns; radians() converts", "PiTau",
      "The same circle after the walk (paper orientation: the sweep goes counterclockwise, y up). A radius sweeps once round from the right-hand axis; tick marks land at the quarter points in turn with code-font labels: 'PI / 2' at the top, 'PI' at the left, '3 * PI / 2' at the bottom and 'TAU' back at the start. Then a wedge outline of 45 degrees draws and a line appears beside the circle: 'radians(45.0)' = 'PI / 4.0'. A small grey credit line under it: 'Godot 4.7 docs · Global built-ins'. The 50 % frame holds with the sweep finished and all four labels landed.",
      "The radius sweeps once round, dropping a label at each quarter, then a 45-degree wedge is named pi over four.",
      [{"at": 0.06, "event": "circle; radius at the start"}, {"at": at("B12", "Pi is half a turn"), "event": "sweep to the left: 'PI / 2' then 'PI' land"},
       {"at": at("B12", "Tau is a full turn"), "event": "sweep finishes: '3 * PI / 2', 'TAU'"},
       {"at": 0.44, "event": "settled with all four labels (hold through the midpoint)"},
       {"at": at("B12", "And the function radians"), "event": "45-degree wedge; 'radians(45.0) = PI / 4.0'"}],
      "BrowserCapture of the docs page",
      "Pi and tau are positions on the turn; a sweep that stops at each shows what they mean, with the docs credited on screen.",
      "Lab 20-constants (PI, TAU, E compile; radians(45) = PI/4; degrees(PI) = 180); Godot 4.7 canvas item reference, Global built-ins")

manim("B13", 1, "the degrees-versus-radians trap", "DegreesTrap",
      "Two small circles side by side on the cream stage (paper orientation, y up). Left, titled 'sin(30.0)': a terracotta dot spins round the circle again and again with a turn counter ticking 1, 2, 3, 4 and stops a little short of the fifth turn near the bottom, with a mid-grey bar beside it (never a dark ink bar) that settles at '-0.99'. Right, titled 'sin(radians(30.0))': the dot moves a short way up to a 30-degree mark and its mid-grey bar shows '0.50'. A small grey credit line: 'math values · checked in a Godot 4.7.2 shader'. The 50 % frame holds with the left dot stopped near the bottom and its counter at 4; the left bar settles just after.",
      "The left dot spins almost five times before it stops near the bottom; the right dot moves a short way.",
      [{"at": 0.06, "event": "two circles with titles"}, {"at": at("B13", "Thirty radians"), "event": "left dot spins, counter ticks to 4, stops near the bottom (done by 0.44)"},
       {"at": 0.44, "event": "left dot stopped (hold through the midpoint)"}, {"at": 0.56, "event": "left bar settles at -0.99 as the voice says 'near minus one'"},
       {"at": at("B13", "Convert first"), "event": "right dot moves to 30 degrees; its bar shows 0.50"}],
      "ShaderLab (two swatches in a real render)",
      "'Thirty radians is almost five turns' is a motion: the dot has to be seen spinning; swatches would show only two colors.",
      "Lab 21-trig-values (right half reads 0.0078, 0.5765, 0.5961: sin(30) about -0.98, turns 4.77); verify-math.gd F (sin(30) = -0.98803, 4.7746 turns)")

manim("B14", 1, "the sine wave is the dot's height", "SineWave",
      "Left: the circle with its terracotta dot (paper orientation, y up). Right: a plot with the angle along the bottom (faint ticks at pi/2, pi, 3pi/2, tau) and 'height' up the side. As the dot goes once round, a thin dashed line runs from the dot across to the plot and a curve draws behind it: up to 1, back through 0, down to -1, home. The finished curve is labelled 'sine'. The 50 % frame holds with the dot at the left of the circle (half turn) and the curve drawn to pi.",
      "A dashed line carries the dot's height across to a curve that grows into the sine wave as the dot goes round.",
      [{"at": 0.06, "event": "circle and empty plot"}, {"at": at("B14", "Plot the point's height"), "event": "dot starts round; the curve starts drawing"},
       {"at": 0.44, "event": "dot paused at the left, curve drawn to pi (hold through the midpoint)"}, {"at": 0.58, "event": "the dot resumes: the second half of the turn, the curve falls to -1 and comes home"},
       {"at": at("B14", "That curve is the sine wave"), "event": "turn complete; curve labelled 'sine'"}],
      "ShaderLab (a shader drawing the wave)",
      "The wave only makes sense as the trace of the dot's height; the drawing connects the two.",
      "verify-math.gd J (sin at 0, pi/2, pi, 3pi/2, tau = 0, 1, 0, -1, 0)")

manim("B15", 1, "cosine is the same wave a quarter turn earlier", "CosineShift",
      "The plot from before with the sine curve in ink. A second curve, cosine, draws in a lighter grey-brown starting at 1 and peaking a quarter turn before sine; a bracket between the two peaks reads 'quarter turn'. A vertical cursor then sweeps along the angle axis; at each position two small dots ride the two curves while, on a small circle at the left, a dot at (cos, sin) is placed by those two values and traces the circle. The 50 % frame holds with both curves drawn and the bracket.",
      "Two curves a quarter turn out of step set a dot's across and up together, and the dot traces the circle.",
      [{"at": 0.0, "event": "plot with the sine curve"}, {"at": 0.06, "event": "cosine curve draws; 'quarter turn' bracket"},
       {"at": 0.44, "event": "both curves and the bracket settled (hold through the midpoint)"}, {"at": at("B15", "Two waves"), "event": "cursor sweeps; the small circle's dot traces the circle"}],
      "LectureEvidenceTable (sine against cosine at four angles)",
      "Two waves a quarter turn out of step is a picture; the cursor shows each pair of values becoming a point on the circle.",
      "verify-math.gd H (cos x = sin(x + pi/2) to 1e-16)")

# ───────────────────────────── ACT III · An Orbit ─────────────────────────────
manim("B16", 2, "the centered pixel address p = UV * 2.0 - 1.0", "CenterAddress",
      "Act title 'An Orbit' (serif 40) top-left. A square drawn the shader way (the second number counts DOWN, small grey 'y' arrow pointing down): corner labels (0, 0) top left and (1, 1) bottom right, a terracotta dot at the middle labelled (0.5, 0.5) and a short tag 'UV'. A small code card lands beside it with 'void fragment() {', the line 'vec2 p = UV * 2.0 - 1.0;' and '}', and a 3-word tag 'once per pixel' on the function line. As the line lands the labels slide to the centered numbers: corners (-1, -1) and (1, 1), middle (0, 0); the dot visits the top-left corner and the middle, showing both numbers. The 50 % frame holds with the line landed and the labels still 0 to 1.",
      "The square's labels slide from 0 to 1 to minus one to one while the dot stays put.",
      [{"at": 0.08, "event": "act title; square with UV labels; dot at the middle"}, {"at": at("B16", "It runs once for each pixel", 0.06), "event": "code card lands with 'void fragment() {' and its 'once per pixel' tag"},
       {"at": 0.36, "event": "the line 'vec2 p = UV * 2.0 - 1.0;' lands in the card (done by 0.44; hold through the midpoint)"},
       {"at": 0.56, "event": "labels slide to -1 to 1; middle becomes (0, 0)"}, {"at": at("B16", "Call that p"), "event": "the dot visits the corner and the middle; 'p' tag"}],
      "ShaderLab (code beside a render that colors p)",
      "The idea is a change of labels on the same square: a relabelling is a motion; a render of p as color would hide the numbers.",
      "Lab 27-pixel-p (UV echoed at the corners and middle; inside the unit circle at the middle only); Godot docs: UV 'Range from 0.0 to 1.0'")

manim("B17", 2, "the planet: a distance test on the pixel grid", "Planet",
      "The centered square (screen orientation, y down) as a 12-by-12 grid of outline-only cells (no fill behind text). A faint teal circle of radius 0.25 (of the half-width) outlines the planet at the middle. A terracotta probe dot starts at the middle and moves outward along a drawn line; a live readout 'length(p) 0.10 ... 0.25 ... 0.40' follows it. When the readout passes 0.25 the probe's own cell changes from teal to the stage grey; at the end every cell whose center is inside the circle is tinted teal. A code line lands under the grid: 'if (length(p) < 0.25)'. The 50 % frame holds with the probe inside the circle and the readout at about 0.20.",
      "The probe moves out from the middle, its length readout grows, and its cell flips from planet to stage at exactly 0.25.",
      [{"at": 0.06, "event": "grid, faint circle, probe at the middle"}, {"at": at("B17", "Length of p"), "event": "probe moves out; readout grows"},
       {"at": 0.44, "event": "probe inside, readout about 0.20 (hold through the midpoint)"}, {"at": at("B17", "Under the radius"), "event": "probe crosses 0.25 and its cell flips; code line lands"},
       {"at": at("B17", "A circle is every point"), "event": "all inside cells tint teal"}],
      "ShaderLab still of the planet",
      "A distance test is something a probe does as it moves; a render of a disc would show the answer without the question.",
      "Lab 22-check-orbit-angle (planet teal at the middle of every probe run); Godot docs: length() 'Returns the length of the vector'")

lab("B18", 2, "the moon: the same test around a different center", MOON, "", "", [
        {"at": at("B18", "The moon is the same test"), "lines": [ln(MOON, "length(p) < 0.25")]},
        {"at": at("B18", "That center is"), "lines": [ln(MOON, "vec2 moon"), ln(MOON, "float a")]},
        {"at": at("B18", "Distance measures"), "lines": [ln(MOON, "distance(p, moon)")], "label": "distance: how far apart two points are"},
        {"at": 0.92, "lines": [ln(MOON, "COLOR =")], "label": "COLOR: the pixel's color"}],
    "The shader file as a code card on the cream stage (the card the next beat shows beside its render). Focus lands on the planet test, then on the moon's center line and its angle line, then on the distance test with the label 'distance: how far apart two points are', and finally on the COLOR line with the label 'COLOR: the pixel's color'. No render yet.",
    "Line focus steps from the planet test to the moon's center to the distance test.",
    [{"at": at("B18", "The moon is the same test"), "event": "planet test line"}, {"at": at("B18", "That center is"), "event": "moon center and angle lines"},
     {"at": at("B18", "Distance measures"), "event": "distance test line, label"}, {"at": 0.92, "event": "COLOR line, label"}],
    "LectureCodeTrace (about ten lines fit; this file has eleven and a different look)",
    "The same code card appears beside the render in the next beat, so the viewer reads the file first and sees its result second.",
    "", "lab-shaders/01-moon-fixed.gdshader compiles in the Lab (01-moon-fixed run)", layout="code", lane="remotion")

lab("B19", 2, "the moon lands exactly where the hand calculation said (right, below)", MOON, "godot-shaders/trig-moon-fixed.png",
    "Godot 4.7.2 · Forward+ · the shader on the left", [
        {"at": at("B19", "Run it"), "lines": [ln(MOON, "float a")]},
        {"at": at("B19", "Across"), "lines": [ln(MOON, "vec2 moon")]},
        {"at": 0.6, "lines": [ln(MOON, "distance(p, moon)")]}],
    "Code card at the left with the focus stepping from the angle line to the moon line; at the right a real Godot window (square) with a teal planet in the middle and the slate-blue moon at the lower right, right of the middle and BELOW the middle line. Readouts land: '0.52 across' above the moon's column, then a terracotta ring on the moon and '0.30 down'.",
    "The moon is already at the predicted spot, and a ring and a '0.30 down' readout show it sits below the middle line.",
    [{"at": at("B19", "Run it"), "event": "angle line focused; render visible"}, {"at": at("B19", "Across"), "event": "moon line focused; '0.52 across' readout"},
     {"at": 0.6, "event": "ring on the moon; '0.30 down' readout"}],
    "manim: the p-square with the predicted dot",
    "A real render landing on the predicted spot is the check; a drawing could only claim it, and the surprise (below, not above) is real.",
    "C02: Lab rect, lab-shaders/01-moon-fixed.gdshader, still PNG (480 x 480 captured at 1920 x 1920), Forward+. Probes: moon (0.502, 0.600, 0.749) at uv (0.7598, 0.65); the y-up mirror spot (0.7598, 0.35) is empty stage (0.851, 0.839, 0.788); planet (0.369, 0.639, 0.569) at the middle.",
    "Lab probes 01-moon-fixed; verify-math.gd E (uv 0.7598, 0.65)",
    readouts=[{"at": at("B19", "Across"), "text": "0.52 across", "x": 0.8, "y": 0.43}, {"at": 0.62, "text": "0.30 down", "x": 0.86, "y": 0.75}],
    rings=[{"at": 0.6, "box": [0.7, 0.59, 0.82, 0.71]}])

manim("B20", 2, "paper has y up; a screen has y down, so the picture flips", "Flip",
      "Two circles side by side, each with the same terracotta dot at a quarter turn. Left, labelled 'on paper': the y axis arrow points UP and the dot sits at the top. Right, labelled 'on a screen': the y axis arrow points DOWN and the dot sits at the bottom. The left circle flips top-to-bottom into the right one (the dot rides the flip); then on the right the dot travels a full turn and a thick terracotta arc arrow shows the direction: clockwise. A small grey credit: 'Godot docs · y is down in 2D'. The 50 % frame holds with both circles and the flipped dot settled.",
      "One circle turns over into the other, and the dot on it then runs clockwise.",
      [{"at": 0.06, "event": "'on paper' circle with the dot at the top"}, {"at": at("B20", "On a screen"), "event": "circle flips; 'on a screen', dot at the bottom"},
       {"at": 0.44, "event": "flipped circle settled (hold through the midpoint)"}, {"at": at("B20", "a growing angle turns clockwise"), "event": "dot travels a full turn; clockwise arc arrow"}],
      "BrowserCapture of the Vector2 docs (DOWN.angle() = PI / 2)",
      "The flip is a mirror; seeing one circle become the other shows that the formulas stay and the picture turns over.",
      "verify-math.gd B (Vector2.DOWN.angle() = 1.5708) and C (RIGHT.rotated(PI/2) = (0, 1)); Lab 22-angle-90 (moon straight down); Godot docs: 'in Godot, the Y axis points down in 2D' and 'rotation is represented clockwise'")

lab("B21", 2, "the angle is TIME: the moon goes round on the game clock", ORBIT, "godot-shaders/trig-orbit.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [
        {"at": 0.04, "lines": [ln(ORBIT, "float a")]},
        {"at": at("B21", "As time counts up"), "lines": [ln(ORBIT, "vec2 moon")]},
        {"at": at("B21", "One line changed"), "lines": [ln(ORBIT, "float a")]}],
    "Code card at the left with the changed line 'float a = TIME;' focused; at the right the real Godot window: the planet in the middle and the moon circling it clockwise on its own, one lap in 6.28 s. A 'clockwise' readout lands under the orbit.",
    "The moon goes round clockwise while the code is on screen, with no animation in the file.",
    [{"at": 0.04, "event": "TIME line focused; moon already moving"}, {"at": at("B21", "As time counts up"), "event": "moon line focused; 'clockwise' readout"},
     {"at": at("B21", "One line changed"), "event": "TIME line focused again"}],
    "manim: a dot going round a circle",
    "The film's first running shader: code and result together is the claim, and the motion is the proof that the file animates itself.",
    "C03: Lab rect, lab-shaders/02-orbit.gdshader, square, live TIME, 14 s, 30 fps, Forward+. Measured: the moon turns clockwise at +0.99 to +1.00 rad/s at a constant 0.600 of the half-width (batch run, 4 intervals).",
    "batch-summary.txt: orbit02 (angle against time); Godot docs: TIME 'Global time since the engine has started, in seconds'",
    readouts=[{"at": 0.62, "text": "clockwise", "x": 0.5, "y": 0.93}], caption="TIME: seconds on one clock shared by the whole game")

lab("B22", 2, "scale the time, scale the speed", FAST, "godot-shaders/trig-orbit-fast.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [{"at": 0.06, "lines": [ln(FAST, "float a")]}],
    "Code card at the left with 'float a = TIME * 2.0;' focused; at the right the same scene with the moon going round visibly faster, a lap every 3.14 s. Caption under the window: 'one lap every 3.14 s · before: 6.28 s'.",
    "The moon laps the planet twice as fast as in the previous clip.",
    [{"at": 0.06, "event": "TIME * 2.0 line focused; moon already racing"}, {"at": 0.6, "event": "caption with the two lap times"}],
    "manim: two moons at different speeds",
    "The change is one multiplication; the same scene faster, with both lap times stated, shows what it does.",
    "C04: Lab rect, lab-shaders/03-orbit-fast.gdshader, square, live TIME, 12 s, 30 fps, Forward+. Measured +2.00 rad/s clockwise (batch run, 3 intervals).",
    "batch-summary.txt: orbit03fast (+2.002, +1.999, +1.999 rad/s)", caption="one lap every 3.14 s · before: 6.28 s")

lab("B23", 2, "add a third of a turn to the angle: three evenly spaced moons", MOONS, "godot-shaders/trig-moons.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [
        {"at": at("B23", "Add a third of a turn"), "lines": [ln(MOONS, "float a =")]},
        {"at": at("B23", "Loop three times"), "lines": [ln(MOONS, "for (int i")]}],
    "Code card at the left (a 'for' loop of three) with the line 'float a = TIME + float(i) * TAU / 3.0;' focused, then the 'for' line; at the right the real window: the planet and three slate-blue moons circling together, always a third of the way round from each other. Readouts land: 'TAU / 3' then '120° apart'.",
    "Three moons circle as a rigid triple, each a third of a turn behind the next.",
    [{"at": at("B23", "Add a third of a turn"), "event": "angle line focused; 'TAU / 3' readout"}, {"at": at("B23", "Loop three times"), "event": "for line focused; '120° apart' readout"}],
    "manim: three dots on a ring",
    "Three real moons holding their spacing while they orbit shows 'add to the angle' better than a static ring.",
    "C05: Lab rect, lab-shaders/05-moons-evenly.gdshader, square, live TIME, 12 s, 30 fps, Forward+. Measured: three moons with gaps of 120.0, 120.0, 120.0 degrees at two times (batch run).",
    "batch-summary.txt: moons05 (gaps 120.0 each)",
    readouts=[{"at": at("B23", "Add a third of a turn"), "text": "TAU / 3", "x": 0.5, "y": 0.06}, {"at": at("B23", "Loop three times"), "text": "120° apart", "x": 0.5, "y": 0.94}])

lab("B24", 2, "the limit: on a wide shape the circle comes out oval; scale p's x by width over height", ASPECT, "godot-shaders/trig-aspect.mp4",
    "Godot 4.7.2 · Forward+ · a wide 16:9 shape · scripted: aspect is raised by the capture", [
        {"at": at("B24", "On a wide one"), "lines": [ln(ASPECT, "vec2 p")]},
        {"at": at("B24", "Scale p's x"), "lines": [ln(ASPECT, "p.x *= aspect")]},
        {"at": at("B24", "passed in as a uniform"), "lines": [ln(ASPECT, "uniform float aspect")]}],
    "Layout stacked: a real wide (16:9) Godot window above the code card. The planet is an oval and the moon's orbit is stretched sideways; as the line 'p.x *= aspect;' is focused the capture raises the aspect uniform from 1.0 to 1.78 and the planet and orbit turn round. Then the uniform line is focused with the caption 'uniform: a value your game sets from outside'. A readout 'aspect 1.78' lands once the circle is round.",
    "The oval planet and orbit turn into true circles as the aspect number rises to width over height.",
    [{"at": at("B24", "On a wide one"), "event": "wide window: oval planet, stretched orbit; p line focused"}, {"at": at("B24", "Scale p's x"), "event": "p.x line focused; the capture raises aspect from 1.0 to 1.78"},
     {"at": at("B24", "passed in as a uniform"), "event": "uniform line focused; caption; 'aspect 1.78' readout"}],
    "manim: an oval and a circle in the same square",
    "A real wide render turning from oval to round as the number rises is the limit and the fix in one clip.",
    "C06: Lab rect, lab-shaders/04-orbit-aspect.gdshader on a 640 x 360 logical canvas captured at 1920 x 1080, live TIME, 16 s, Forward+. aspect holds 1.0 until 0.58 of the beat, rises linearly to 1.7778 by 0.82, holds. Measured: planet 160 x 90 px at aspect 1.0 (ratio 1.778) and 90 x 90 px at aspect 1.7778 (batch run).",
    "batch-summary.txt: wide02, wide04a1.0, wide04a1.7778 (planet 160 x 90, then 90 x 90)", layout="stack",
    readouts=[{"at": 0.84, "text": "aspect 1.78", "x": 0.5, "y": 0.92}], caption="uniform: a value your game sets from outside")

manim("B25", 2, "the recipe: a center, a distance and an angle that grows", "Recipe",
      "At the left the planet and the moon on its ring (screen orientation, y down), drawn flat in the same teal and slate-blue as the renders. Across the top the line 'center + radius * vec2(cos(a), sin(a))' with three parts tinted in turn ('center', 'radius', 'a'). Beside it three small outlined sliders with knobs, labelled 'radius', 'center' and 'speed' (1 to 3 words each). As the voice names each part its slider's knob turns and the orbit responds: the ring grows (0.4 to 0.8), then the whole orbit slides to the right, then the moon speeds up (a pair of small speed marks). The 50 % frame holds with the ring grown.",
      "Each knob turns in turn and the orbit grows, slides, then speeds up.",
      [{"at": 0.06, "event": "orbit and the recipe line"}, {"at": 0.32, "event": "radius slider turns; the ring grows (done by 0.44)"},
       {"at": 0.44, "event": "ring grown (hold through the midpoint)"}, {"at": at("B25", "The center sets the place"), "event": "center slider turns; the orbit slides"},
       {"at": at("B25", "The angle's speed"), "event": "speed slider turns; the moon speeds up"}],
      "ShaderLab (the orbit shader with three uniforms swept)",
      "A drawing can turn each knob alone; the real shader would need three extra uniforms in the code card, and since the angle is TIME times the speed, changing the speed mid-run would make the moon jump.",
      "Lab 22-angle-* probes (position = distance times cos, sin from the center); batch angle0 to angle330 (all 15 angles land)")

# ───────────────────────────── ACT IV · An Orbit Around an Orbit ─────────────────────────────
manim("B26", 3, "the meteor's center is the moon: positions add", "Chain",
      "Act title 'An Orbit Around an Orbit' (serif 40) top-left. Screen orientation (y down), the same teal planet and slate-blue moon as the renders: the planet in the middle, the moon on its ring, and a smaller ring around the moon with the amber meteor on it. A thick ink arrow runs from the planet to the moon and a second, shorter ink arrow from the moon to the meteor, tip to tail, labelled 'moon' and 'meteor' (1 word each). Both angles advance: the second arrow's tail stays on the moon's tip, the small ring rides along, and a dashed line from the planet to the meteor follows. The 50 % frame holds with both arrows and the dashed line settled.",
      "The short arrow stays attached to the moving tip of the long one, so the meteor's small circle rides around the moon's big one.",
      [{"at": 0.06, "event": "act title; planet, moon ring, moon"}, {"at": at("B26", "The moon moves"), "event": "small ring and meteor appear on the moon; arrows tip to tail"},
       {"at": 0.44, "event": "settled: both arrows and the dashed sum (hold through the midpoint)"}, {"at": at("B26", "Positions add"), "event": "both angles advance; the second arrow follows the moon's tip"}],
      "ShaderLab",
      "Vector addition is the idea; arrows laid tip to tail show it, which a render of three dots cannot.",
      "Lab 23-check-meteor-angles (meteor = moon + 0.2 (cos b, sin b), all four probe sets PASS)")

lab("B27", 3, "the meteor line: the moon plus a short circle of its own", METEOR, "", "", [
        {"at": at("B27", "In code"), "lines": [ln(METEOR, "vec2 meteor")]},
        {"at": at("B27", "The meteor is the moon"), "lines": [ln(METEOR, "vec2 meteor"), ln(METEOR, "float b")]},
        {"at": at("B27", "Give that angle"), "lines": [ln(METEOR, "float b")]}],
    "The meteor shader as a code card on the cream stage (fourteen lines). Focus lands on 'vec2 meteor = moon + 0.2 * vec2(cos(b), sin(b));', then on that line together with its angle line, then on 'float b = TIME * 3.0;'. No render.",
    "Line focus lands on the new meteor line and then on its angle.",
    [{"at": at("B27", "In code"), "event": "meteor line"}, {"at": at("B27", "The meteor is the moon"), "event": "meteor line and its angle line"}, {"at": at("B27", "Give that angle"), "event": "'float b = TIME * 3.0;'"}],
    "LectureCodeTrace (about ten lines fit; this file has fourteen)",
    "The same card style as the neighbouring render beats, and the file is longer than the trace card holds.",
    "", "lab-shaders/06-meteor-orbit.gdshader compiles in the Lab (06-meteor-orbit run)", layout="code", lane="remotion")

lab("B28", 3, "the meteor laps the moon three times for every lap of the moon", METEOR, "godot-shaders/trig-meteor.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [],
    "A real Godot render filling the framed window: the teal planet, the slate-blue moon on its orbit and the amber meteor circling the moon, clearly faster. Caption under the window: 'meteor angle TIME * 3.0 · moon angle TIME'. Readout 'three to one' lands near the bottom.",
    "The meteor circles the moon three times for every lap the moon makes around the planet.",
    [{"at": 0.04, "event": "scene running"}, {"at": at("B28", "The meteor laps the moon"), "event": "'three to one' readout"}],
    "manim: orbit with a path trail",
    "The ratio three to one is the claim; a real run lets the viewer count the meteor's laps against the moon's.",
    "C07: Lab rect, lab-shaders/06-meteor-orbit.gdshader, square, live TIME, 14 s, 30 fps, Forward+ (same file as C01). Measured: moon +1.00 rad/s around the planet; meteor +3.00 rad/s around the MOON (batch run).",
    "batch-summary.txt: meteor06 (moon +1.00, meteor around moon +3.00 rad/s)", layout="video",
    readouts=[{"at": at("B28", "The meteor laps the moon"), "text": "three to one", "x": 0.22, "y": 0.06}], caption="meteor angle: TIME * 3.0 · moon angle: TIME")

lab("B29", 3, "negate the meteor's angle: it circles the other way, the moon does not", REVERSE, "godot-shaders/trig-meteor-reverse.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [
        {"at": 0.05, "lines": [ln(REVERSE, "float b")]},
        {"at": at("B29", "The minus sign"), "lines": [ln(REVERSE, "vec2 meteor")]}],
    "Code card at the left with 'float b = -TIME * 3.0;' focused; at the right the real window: the moon still going clockwise around the planet while the meteor circles the moon the other way (counterclockwise on screen). Readout 'meteor reversed' lands.",
    "The meteor turns counterclockwise around the moon while the moon keeps turning clockwise.",
    [{"at": 0.05, "event": "negated angle line focused; meteor already reversed"}, {"at": at("B29", "The minus sign"), "event": "meteor line focused; readout"}],
    "ShaderLab stills of both directions",
    "Two directions in one picture, with the moon unchanged, is the claim: only a running render shows the moon keeping its direction.",
    "C08: Lab rect, lab-shaders/07-meteor-reverse.gdshader, square, live TIME, 14 s, 30 fps, Forward+. Measured: moon +1.00 rad/s, meteor around the moon -3.00 rad/s (batch run).",
    "batch-summary.txt: meteor07reverse (meteor around moon -3.00 rad/s); Lab 23-meteor-a0.8-bm2.0",
    readouts=[{"at": at("B29", "Same circle"), "text": "meteor reversed", "x": 0.24, "y": 0.06}])

manim("B30", 3, "the pattern chains: an arm with an elbow, a tentacle", "Arm",
      "A two-segment arm in ink: a fixed shoulder (terracotta dot), a first segment to an elbow, a second segment to a hand. The two segment angles drift in turn so the arm waves. Beside it the pattern line 'center + radius * vec2(cos(a), sin(a))' appears once per segment; for the second segment the word 'center' is replaced by 'elbow'. Then a third segment grows from the hand (a tentacle) and the whole chain waves. Labelled 'elbow' and 'hand' (1 word each). The 50 % frame holds with the two-segment arm and both pattern lines.",
      "Each segment starts where the last one ended, so adding a segment adds one more circle's worth of motion.",
      [{"at": 0.06, "event": "shoulder, first segment, elbow; first pattern line"}, {"at": 0.26, "event": "second segment to the hand; second pattern line ('elbow' replaces 'center')"},
       {"at": 0.44, "event": "two-segment arm settled with both lines (hold through the midpoint)"}, {"at": 0.56, "event": "labels 'elbow' and 'hand' land as the voice says 'Chain two'"},
       {"at": at("B30", "Chain three"), "event": "third segment grows; the chain waves"}],
      "ShaderLab (a three-segment chain in a shader)",
      "A shader would need a loop and arrays; the drawing makes the same point (each joint is the previous joint plus a circle) with no new code.",
      "Manim only; the nesting itself is verified by Lab 23-check-meteor-angles")

# ───────────────────────────── ACT V · Angle from a Position ─────────────────────────────
manim("B31", 4, "run it backwards: from a position to an angle", "TwoWays",
      "Act title 'Angle from a Position' (serif 40) top-left. A circle drawn the screen way (small grey axes, the y arrow pointing DOWN) with a terracotta dot at a fixed place at the lower right. Along the top a drawn arrow shape (not a glyph) runs left to right labelled 'angle in, position out' while a thick arc grows from the right-hand axis to the dot; then a second arrow shape runs back along the bottom labelled 'position in, angle out', and a question mark sits on the arc and turns into the word 'angle'. The 50 % frame holds with the forward arrow done and the arc drawn.",
      "A forward arrow runs once, then a backward arrow runs and the angle becomes the unknown.",
      [{"at": 0.0, "event": "act title; circle, axes, dot at the lower right"}, {"at": 0.03, "event": "forward arrow; the arc grows to the dot (done by 0.3)"},
       {"at": 0.44, "event": "forward arrow done and the arc drawn (hold through the midpoint, over 'Now run it backwards')"}, {"at": 0.56, "event": "backward arrow runs; question mark on the arc"},
       {"at": at("B31", "What angle"), "event": "the question mark becomes 'angle'"}],
      "FormACard",
      "A card of words would be a punt; two arrows between a position and an angle on the same circle is the structure of the act.",
      "Manim only (film-local kit: unit_circle in screen orientation)")

manim("B32", 4, "arc tangent: two sides in, the angle out", "AtanIdea",
      "Screen orientation (y down). A pixel dot at the lower right of the middle (p = (0.5, 0.35)); a right triangle from the middle whose legs are first labelled 'opposite' and 'adjacent' (the first act's words), and a thick terracotta arc at the middle for the angle labelled 'angle?'. A function box 'arc tangent' lands at the right; the two leg numbers travel into it and an arrow carries 'angle' out, the arc's label changing from 'angle?' to '0.61 rad'. After a hold, the leg labels change to 'down' and 'across' for a pixel. The 50 % frame holds with the box settled and the old labels.",
      "The two legs travel into a box and the angle comes out the other side.",
      [{"at": 0.06, "event": "pixel dot, triangle with legs labelled 'opposite' and 'adjacent', 'angle?' on the arc"}, {"at": at("B32", "Arc tangent undoes it"), "event": "'arc tangent' box lands; the two leg numbers travel in; the angle comes out as '0.61 rad' (done by 0.44)"},
       {"at": 0.44, "event": "legs and box settled (hold through the midpoint)"}, {"at": 0.56, "event": "the leg labels change to 'down' and 'across' as the voice says 'For a pixel'"}],
      "LectureCodeTrace (atan(p.y, p.x))",
      "The idea is 'two sides in, angle out' on the triangle from the first act; the code comes in the next beat.",
      "verify-math.gd L (atan2 landmarks); atan2(0.35, 0.5) = 0.6107 rad, computed")

rem("B33", 4, "Godot's reference: arc tangent takes y first, then x, over the whole turn", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_functions.html#shader-func-atan2",
     "image": "godot-shaders/docs-shader-functions-atan.png", "caption": "Godot 4.7 documentation · Built-in shader functions · atan(y, x) · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1},
                                  {"at": 0.26, "x": 0.45, "y": 0.4, "scale": 1.6, "ring": [0.08, 0.36, 0.84, 0.16]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 built-in functions page scrolled to the two-argument atan(y, x) entry; the camera pushes in on its description ('Calculates the arc tangent given a numerator and denominator. The signs of y and x are used to determine the quadrant that the angle lies in.') and the return line ('in the range [-PI, PI]'), and one terracotta ring marks them. Coordinates are set from the real screenshot at build time.",
    "The camera pushes in on the entry's description and range while the voice reads them.",
    [{"at": 0, "event": "page at the atan entry"}, {"at": 0.26, "event": "push-in lands on the entry; the ring draws on the description and the range (all settled before the 45 % mark)"}],
    "LectureCodeTrace: atan(p.y, p.x)",
    "'y first' and the range are documentation claims: the page itself is the evidence.",
    "D2: Playwright capture of the live docs page (1600 x 900 at 2.4x); text read 2026-10-13; anchor id shader-func-atan2 (the two-argument entry) exists. Khronos agrees: range [-pi, pi].")

manim("B34", 4, "the numbers around the circle and the seam at the left", "Compass",
      "Screen orientation circle (y down) with a terracotta dot at the right-hand axis and a readout box at the side titled 'arc tangent' with the live number. The dot walks clockwise a full turn in the order the voice says it, pausing at each compass point while the readout lands: right '0', down '1.57', then on to just below the left axis where the readout has climbed to 3.14; once the dot passes the left axis the readout JUMPS to -3.14 (a brief flash on the jump); then up '-1.57', and back to '0' at the right. A short thick mark on the left axis is labelled 'seam'. The 50 % frame holds with the dot paused just below the left axis and the readout at 3.14.",
      "The readout climbs to 3.14 as the dot nears the left, jumps to -3.14 as it passes, and climbs back to zero.",
      [{"at": 0.06, "event": "circle, dot at the right, readout 0"}, {"at": at("B34", "Straight down is half pi"), "event": "dot walks to the bottom: 1.57"},
       {"at": at("B34", "Straight left is where it wraps"), "event": "dot walks on to just below the left axis; readout climbs to 3.14; 'seam' mark (done by 0.44)"},
       {"at": 0.44, "event": "dot paused just below the left axis, readout 3.14 (hold through the midpoint)"}, {"at": 0.58, "event": "dot passes the left axis; readout jumps to -3.14 (a brief flash)"},
       {"at": at("B34", "Past the wrap"), "event": "dot goes up: -1.57"}, {"at": 0.93, "event": "dot home at the right: 0"}],
      "ShaderLab (the angular color picture)",
      "The jump is a property of the walk: seeing the number change as the dot passes the left shows where it wraps; the picture comes next beat.",
      "Lab 24-atan ring probes (just above the left axis 0.000, just below 1.000 in the t scale; right 0.498, down 0.749, up 0.251); verify-math.gd L (+3.14059 and -3.14059 either side of the left)")

lab("B35", 4, "the pixel's angle shown as color: teal to amber, with a seam", COLORS, "godot-shaders/trig-atan-colors.png",
    "Godot 4.7.2 · Forward+ · the shader on the left", [
        {"at": at("B35", "Divide by tau"), "lines": [ln(COLORS, "float t")]},
        {"at": 0.58, "lines": [ln(COLORS, "COLOR =")]}],
    "Code card at the left with the line 'float t = atan(p.y, p.x) / TAU + 0.5;' focused, then the COLOR line; at the right a real Godot window with a conic color picture: teal at the start, amber at the end, a hard edge along the left half of the horizontal axis (the seam). A thin 0 to 1 ramp under the render with a marker that sweeps from teal to amber, and a terracotta ring on the seam at the end. Caption: 'mix: blend two colors by a number from 0 to 1'.",
    "The ramp marker sweeps from zero to one under the picture, then a ring settles on the hard edge at the left.",
    [{"at": at("B35", "Divide by tau"), "event": "t line focused; render visible"}, {"at": 0.58, "event": "COLOR line focused; ramp marker sweeps 0 to 1"},
     {"at": at("B35", "The hard edge"), "event": "ring on the seam"}],
    "manim: a color wheel",
    "The real render shows the seam as a hard edge exactly where the numbers wrap.",
    "C09: Lab rect, lab-shaders/08-atan-colors.gdshader, still PNG (480 x 480 captured at 1920 x 1920), Forward+. Probes: right (0.635, 0.643, 0.412), down (0.769, 0.647, 0.329), up (0.502, 0.643, 0.490); just above the left axis teal (0.373, 0.639, 0.569), just below amber (0.898, 0.651, 0.251).",
    "Lab probes 08-atan-colors; batch atan-ring-480 (24 directions all PASS)",
    ramp={"at": 0.58, "from": 0, "to": 1}, rings=[{"at": at("B35", "The hard edge"), "box": [0.0, 0.46, 0.5, 0.54]}],
    caption="mix: blend two colors by a number from 0 to 1")

lab("B36", 4, "the one-argument slip: opposite directions get the same answer", ONEARG, "godot-shaders/trig-atan-one-argument.png",
    "Godot 4.7.2 · Forward+ · the shader on the left", [
        {"at": at("B36", "A common slip"), "lines": [ln(ONEARG, "float t")]},
        {"at": at("B36", "Dividing throws away"), "lines": [ln(ONEARG, "float t")]}],
    "Code card at the left with the changed line 'float t = atan(p.y / p.x) / PI + 0.5;' focused; at the right a real Godot window with a butterfly-like color picture: the upper-left and lower-right quadrants are identical, and so are the upper-right and lower-left. Two terracotta rings land in turn on opposite quadrants with the readout 'same' in each.",
    "Rings land on opposite quadrants in turn and both read 'same'.",
    [{"at": at("B36", "A common slip"), "event": "changed line focused; butterfly picture visible"}, {"at": 0.62, "event": "ring on the lower-right quadrant; 'same'"},
     {"at": at("B36", "the left half repeats"), "event": "ring on the upper-left quadrant; 'same'"}],
    "manim: two opposite arrows with equal arcs",
    "The bug is visible in the render as a butterfly; a diagram would only assert it.",
    "C10: Lab rect, lab-shaders/09-atan-one-argument.gdshader, still PNG (480 x 480 captured at 1920 x 1920), Forward+. Probes: lower right and upper left both (0.769, 0.647, 0.329); upper right and lower left both (0.502, 0.643, 0.490). The docs say it too: 'cannot determine with certainty in which quadrant the angle falls'.",
    "Lab probes 09-atan-one-argument and 25-atan-one-argument; batch atan-one-arg-pairs (16 opposite pairs agree)",
    rings=[{"at": 0.62, "box": [0.5, 0.5, 1.0, 1.0]}, {"at": at("B36", "the left half repeats"), "box": [0.0, 0.0, 0.5, 0.5]}],
    readouts=[{"at": 0.62, "text": "same", "x": 0.75, "y": 0.75}, {"at": at("B36", "the left half repeats"), "text": "same", "x": 0.25, "y": 0.25}])

manim("B37", 4, "one pixel by hand: p = (-0.3, -0.3) has the number one eighth", "WorkedPixel",
      "The centered square (screen orientation) with one terracotta dot at p = (-0.3, -0.3), up and to the left, labelled 'p'. Three lines of arithmetic build beneath it as the voice reads them, in the monospace face (32 or larger): 'atan(-0.3, -0.3) = -3 * PI / 4', then '÷ TAU = -0.375', then '+ 0.5 = 0.125'. The last result lands on a thin 0-to-1 ramp strip drawn under the square as a terracotta marker at 0.125 labelled '1/8'. The 50 % frame holds with the first line done.",
      "The three lines of arithmetic build in turn and the result lands as a marker on the ramp.",
      [{"at": 0.06, "event": "square, dot at (-0.3, -0.3), empty lines"}, {"at": at("B37", "Arc tangent says"), "event": "'atan(-0.3, -0.3) = -3 * PI / 4' lands (done by 0.44)"},
       {"at": 0.44, "event": "first line settled (hold through the midpoint)"}, {"at": 0.56, "event": "'÷ TAU = -0.375' lands as the voice says 'Divide by tau'"},
       {"at": at("B37", "Add one half"), "event": "'+ 0.5 = 0.125' lands"}, {"at": at("B37", "One eighth"), "event": "marker at 0.125 on the ramp, labelled '1/8'"}],
      "LectureCodeTrace",
      "One concrete pixel carried through the three operations is the worked example; the ramp marker shows where the answer lands.",
      "verify-math.gd L and run_batch sweep10-worked-pixel (hidden at sweep 0.12, shown at 0.13 for this pixel); atan2(-0.3, -0.3)/TAU + 0.5 = 0.125")

lab("B38", 4, "compare the pixel's number with a sweep uniform: a clock hand reveals the picture", SWEEP, "godot-shaders/trig-sweep.mp4",
    "Godot 4.7.2 · Forward+ · scripted: the capture raises sweep from 0 to 1", [
        {"at": at("B38", "A uniform is a number"), "lines": [ln(SWEEP, "uniform float sweep")]},
        {"at": at("B38", "If a pixel's number"), "lines": [ln(SWEEP, "if (t < sweep)"), ln(SWEEP, "COLOR = texture")], "label": "texture: the picture at this address"},
        {"at": at("B38", "Raise sweep"), "lines": [ln(SWEEP, "if (t < sweep)")]}],
    "Code card at the left (the sweep uniform, the comparison, the texture line) with focus stepping uniform line, comparison and texture lines, then the comparison again; at the right a real Godot window: the teal test sprite is revealed by a growing wedge from the left, over the top and round, like a clock hand. A thin 0 to 1 ramp under the render whose marker rides the sweep value. Caption: 'uniform: a value your game sets from outside'.",
    "The wedge grows clockwise from the left as the ramp marker rises from 0 to 1.",
    [{"at": at("B38", "A uniform is a number"), "event": "uniform line focused; caption"}, {"at": at("B38", "If a pixel's number"), "event": "comparison and texture lines focused; label"},
     {"at": at("B38", "Raise sweep"), "event": "the capture raises sweep 0 to 1; ramp marker rides it; the wedge grows"}],
    "manim: a wedge growing on a circle",
    "A running reveal with the value on a ramp shows both the effect and the number behind it.",
    "C11: Lab sprite (test sprite scaled to fit, square 480 x 480 captured at 1920 x 1920), lab-shaders/10-sweep.gdshader, Forward+, 16 s, scripted sweep: 0.30 until 0.68 of the beat (a partial reveal, so the window is never empty while the uniform and the test are explained), then 0.0 and a linear rise to 1.0 by 0.97 (the beat's cue 'Raise sweep'). Verified: at sweep 0.5 the upper half of the blob is shown (UL, UR) and the lower half hidden (LR, LL); the worked pixel appears between sweep 0.12 and 0.13.",
    "Lab probes 10-sweep-0.5; batch sweep10-0 to 1.0 and the worked-pixel threshold (all PASS)",
    ramp={"at": at("B38", "Raise sweep"), "from": 0, "to": 1}, caption="uniform: a value your game sets from outside")

lab("B39", 4, "start at twelve: add a quarter turn and keep the fraction", SWEEPTOP, "godot-shaders/trig-sweep-top.mp4",
    "Godot 4.7.2 · Forward+ · scripted: the capture raises sweep from 0 to 1", [
        {"at": 0.05, "lines": [ln(SWEEPTOP, "float t")]},
        {"at": at("B39", "To start at twelve"), "lines": [ln(SWEEPTOP, "float t")], "label": "fract: keeps the part after the decimal point"}],
    "Code card at the left with the changed line 'float t = fract(atan(p.y, p.x) / TAU + 0.25);' focused; at the right the same reveal, now starting at the top (twelve o'clock) and going clockwise. A terracotta ring marks the start line at the top and a readout '12 o'clock' lands.",
    "The wedge now grows clockwise from the top instead of from the left.",
    [{"at": 0.05, "event": "changed line focused; a partial reveal that starts at the top is already showing"}, {"at": at("B39", "To start at twelve"), "event": "line focused with the fract label"}, {"at": 0.62, "event": "the capture resets sweep to 0 and raises it: ring at the start line, '12 o'clock' readout"}],
    "ShaderLab still of both starts side by side",
    "Moving the start is visible only as the wedge starting somewhere else; a still of two wedges would not show which way it grows.",
    "C12: Lab sprite, lab-shaders/11-sweep-top.gdshader, square, Forward+, 16 s, scripted sweep: 0.30 until 0.60 of the beat (a partial reveal from twelve o'clock), then 0.0 and a linear rise to 1.0 by 0.97. Verified at sweep 0.5: the right half is shown (UR, LR) and the left half hidden (UL, LL).",
    "Lab probes 11-sweep-top-0.5; batch sweep11top-0 to 1.0 (all PASS)",
    rings=[{"at": 0.62, "box": [0.44, 0.05, 0.56, 0.5]}], readouts=[{"at": 0.62, "text": "12 o'clock", "x": 0.5, "y": 0.04}],
    caption="fract: keeps the part after the decimal point")

lab("B40", 4, "feed the pixel's angle to cosine again: a flower with eight petals that turns", FLOWER, "godot-shaders/trig-flower.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [
        {"at": 0.05, "lines": [ln(FLOWER, "float a")]},
        {"at": at("B40", "Multiply it by eight"), "lines": [ln(FLOWER, "float edge")]},
        {"at": at("B40", "Subtract time"), "lines": [ln(FLOWER, "float edge")]}],
    "Code card at the left with the angle line, then 'float edge = 0.55 + 0.15 * cos(8.0 * (a - TIME));' focused; at the right a real Godot window: a teal flower with eight rounded petals on the stage, turning clockwise at one radian per second. Readout '8 petals' lands.",
    "A teal eight-petal flower turns steadily, its edge swelling and shrinking eight times round.",
    [{"at": 0.05, "event": "angle line focused; flower already turning"}, {"at": at("B40", "Multiply it by eight"), "event": "edge line focused; '8 petals' readout"},
     {"at": at("B40", "Subtract time"), "event": "edge line focused again"}],
    "manim: a polar plot of the radius against the angle",
    "The finished shape moving is the payoff; it uses the pixel's angle, cosine, a multiplier and time in one picture.",
    "C13: Lab rect, lab-shaders/12-flower.gdshader, square, live TIME, 14 s, 30 fps, Forward+. Measured: edge radius between 0.398 and 0.700 (expected 0.40 to 0.70); the pattern turns +1.00 rad/s clockwise; 32 edge probes for a 8-petal static twin all PASS.",
    "Lab 12-flower and 26-flower-static-8; batch flower12 (turn +1.00 rad/s) and flower-static-8 (64 probes PASS)",
    readouts=[{"at": at("B40", "Multiply it by eight"), "text": "8 petals", "x": 0.5, "y": 0.93}])

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(len(N.ACTS)):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Trigonometry for Shaders\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot picture is a Shader Lab render of a tested file in `lab-shaders/` (13 captures, no editor frames needed), plus two Godot-docs screenshots. Four things must exist before the build (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; layouts used here: `side`, `stack`, `video`, `code`; props used: `cues` with labels, `readouts`, `rings`, `ramp`, `caption`, `title`). Check `./brutalist.art/art scenes --check ShaderLab`; if it is not renderable the build starts there.\n"
      "2. **`shader_kit.py`** Manim helpers (same spec file: `ramp_strip`, `pixel_grid`, `plot`, `uv_square`, `code_card`) **plus these film-local objects**, written into this film's scenes file, not the shared kit: `right_triangle(angle, hyp)` with side highlight and a thick terracotta angle arc; `unit_circle(radius, orientation)` with a terracotta dot, axes and a screen/paper flag (paper = y up, screen = y down); `wave_plot` (the shared `plot` with a travelling dashed link from a circle's dot); `radius_tape` (a bar copied end to end round a circle's edge); `vector_chain` (arrows tip to tail with a riding small ring); `compass_readout` (a live number box beside a walking dot); `knob_slider` (an outlined slider with a turning knob).\n"
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same spec file): options `--animate name:from:to` (a piecewise schedule is needed for C06, C11 and C12), `--size` for a square 480 x 480 and a wide 640 x 360 logical canvas, live `TIME`, PNG sequence then ffmpeg to MP4, still PNG.\n"
      "4. **Two docs screenshots** (B08, B33) with Playwright at 1600 x 900, device scale 2.4: see `CAPTURE-PLAN.md`.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)

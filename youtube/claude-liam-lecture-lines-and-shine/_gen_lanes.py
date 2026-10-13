#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md (the pilot's way).

Why a generator: the code shown on screen must be the tested file text (line numbers for the cues are looked up in the files, not typed),
and the shot list must say exactly what the lanes say. Re-run after any edit:
    python3 _gen_lanes.py && python3 make_sheet.py
(never re-run make_sheet.py after `art final`).

Timing note for every ShaderLab cue, readout and ring: `at` is a fraction of the BEAT's measured audio length. A capture clip is cut to the
beat's length and its sweeps are given as fractions too (CAPTURE-PLAN.md); no overlay starts inside 45 to 55 percent.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
E = []          # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def ln(fn, needle, nth=1):
    """1-based line number of the nth line of the shader file that contains `needle`."""
    hits = [i + 1 for i, line in enumerate(code_of(fn).split("\n")) if needle in line]
    if len(hits) < nth:
        raise SystemExit(f"{fn}: no line {nth} containing {needle!r}")
    return hits[nth - 1]


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects and plain Manim shapes)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, code=None, code_file=None, caption=""):
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    add(bid, act, about, {"lane": "capture", "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


# Frame fractions of the single test card in the 640 x 360 capture frame: x = 0.275 + 0.45 u, y = 0.10 + 0.80 v.
def card_xy(u, v):
    return round(0.275 + 0.45 * u, 3), round(0.10 + 0.80 * v, 3)


FRAME = "Godot 4.7.2 · Forward+ · "
S1, S2 = "01-signed-test.gdshader", "02-angle-line.gdshader"
S4, S5, S6, S7 = "04-band-raw.gdshader", "05-band-true.gdshader", "06-wide-fix.gdshader", "07-slide.gdshader"
S9L, S10, S11, S12 = "09-shine-leak.gdshader", "10-shine.gdshader", "11-shine-clock.gdshader", "12-direction.gdshader"
S8, S13 = "08-center-shift.gdshader", "13-direction-signed.gdshader"

# ───────────────────────────── ACT I · A Line as a Test ─────────────────────────────
lab("B01", 0, "the goal: a glint sliding across a sprite", S11, "lines-and-shine/c01-hook.mp4", FRAME + "the finished shine · scripted clock",
    [], "Act title 'A Line as a Test' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite with a white diagonal glint that slides across it from upper left to lower right, rests for a moment off the sprite, and repeats. Label: 'the finished shine'.",
    "The white band sweeps across the sprite and stays inside its outline.",
    [{"at": 0.0, "event": "sprite, window labelled, title on the card"}, {"at": 0.2, "event": "first glint crosses the sprite"}, {"at": 0.6, "event": "next glint crosses"}],
    "manim drawing of a stripe crossing a blob", "A real render is the honest picture of the goal; a drawing would only claim it.",
    "C01: Lab blob sprite (teal test sprite, scale to fit), lab-shaders/11-shine-clock.gdshader (TIME-driven, angle 35, thickness 0.1 as in the file); 12 s at 30 fps, Forward+, offline fixed tick; the sweep period is 2 s so the 12 s clip loops seamlessly; no input.",
    "Lab: the clock version moves with TIME (measurements F); band off the sprite at offset -1.5 and +1.5", layout="video", title="A Line as a Test")
manim("B02", 0, "a line from school: slope and starting height", "SchoolLine",
      "Axes on the cream stage with a warm-grey line y = m x + b crossing the vertical axis above the origin, a terracotta dot marking b. A right triangle (one step across, m up) rides along the line under the label 'slope m: up per step across'. Then the line slides down until it passes through the origin: the b dot lands on 0 and the label becomes 'y = m x'.",
      "The slope triangle rides along the line, then b shrinks to zero as the line settles through the middle.",
      [{"at": 0.1, "event": "axes, line, b dot"}, {"at": 0.3, "event": "triangle rides along the line (slope)"}, {"at": 0.58, "event": "b dot ringed: its starting height"}, {"at": 0.72, "event": "line slides to the middle; b = 0"}],
      "LectureEvidenceTable listing m and b", "A rise-over-run triangle that moves along the line is the meaning of slope; a table of two terms would only name them.")
manim("B03", 0, "centering the address: zero moves to the middle", "CenterTheAddress",
      "A square with corner labels (0, 0) at the top left and (1, 1) at the bottom right and its second axis pointing down (shader_kit uv_square). A terracotta dot sits at the top-left corner. The labels morph to -1, 0 and 1 and the dot glides to the middle; the formula 'p = UV × 2 − 1' appears under the square.",
      "The zero moves from the corner to the middle of the square.",
      [{"at": 0.1, "event": "UV square, dot at the corner"}, {"at": 0.38, "event": "labels morph, dot glides to the middle (settled by 50 %)"}, {"at": 0.68, "event": "formula appears"}],
      "ShaderLab with the line `vec2 p = UV * 2.0 - 1.0;` over a gradient", "Moving the zero is a change of coordinate system; Manim shows the labels and the dot move, a gradient would not.")
manim("B04", 0, "flipping the second number so up is up", "FlipUp",
      "The centered square with its vertical axis pointing down (+1 at the bottom). A terracotta dot sits in the upper right labelled (0.5, -0.5). The vertical axis flips to point up and the dot's label becomes (0.5, 0.5) while the dot stays where it is on screen; a short warm-grey line y = 0.5 x then draws, climbing to the right, under the label 'p.y = -p.y'.",
      "The vertical axis flips and the dot's second number changes sign while the dot does not move.",
      [{"at": 0.1, "event": "square, y pointing down, dot labelled (0.5, -0.5)"}, {"at": 0.3, "event": "axis flips; label becomes (0.5, 0.5) (settled by 50 %)"}, {"at": 0.6, "event": "line climbs to the right"}],
      "ShaderLab showing the signed map upside down then upright", "A relabelling of the same dot on the same screen is the claim; only a drawing can hold the dot still while the numbers change.")
manim("B05", 0, "rewriting the line as a test", "TheTest",
      "Left: the equation 'y = m x'. The 'm x' term travels across the equals sign and the equation becomes 'y − m x = 0', captioned 'the test'. Right: the square with the line m = 0.5 and a terracotta dot riding along it, labelled '0'; then a second dot off the line reads +0.6.",
      "A term crosses the equals sign while a dot rides the line with the value 0 on it.",
      [{"at": 0.1, "event": "y = m x, line and dot"}, {"at": 0.25, "event": "m x crosses to the left side"}, {"at": 0.4, "event": "'y − m x = 0' captioned 'the test' (settled by 50 %)"}, {"at": 0.57, "event": "the dot on the line reads 0"}, {"at": 0.75, "event": "a second dot off the line reads +0.6"}],
      "LectureCodeTrace of the single line y - m * x", "An equation that rearranges itself is a Transform; the term visibly changing sides is the step the voice names.")
manim("B06", 0, "three points: on, above and below the line", "ThreeDots",
      "The test square with the line m = 0.5. Three terracotta dots land at across = 0.4: on the line (label 0), above it (label +0.6) and below it (label -0.6). Warm-grey dashed vertical connectors then run from the two outer dots to the line, labelled 'straight up' and 'straight down', each 0.6 long.",
      "Dots land one at a time with their numbers; dashed verticals then measure the gap straight up and down.",
      [{"at": 0.15, "event": "line, dot on the line: 0"}, {"at": 0.33, "event": "dot above: +0.6"}, {"at": 0.43, "event": "dot below: −0.6 (all three settled by 50 %)"}, {"at": 0.78, "event": "dashed vertical gaps, 0.6 each"}],
      "ShaderLab with three probe readouts", "Exact arithmetic with vertical gaps drawn is the claim, and the gaps set up the distance argument later.",
      "arithmetic: 0.2 - 0.5 x 0.4 = 0, 0.8 - 0.2 = 0.6, -0.4 - 0.2 = -0.6; Lab A1 reads +0.593, +0.005, -0.603")
manim("B07", 0, "one number for a whole parallel line", "Parallel",
      "The same square: the line m = 0.5 and a warm-grey dashed parallel line through the 'above' dot. A terracotta dot slides along the parallel line while its label stays '+0.6'. Then three parallel warm-grey lines appear labelled -0.6, 0 and +0.6.",
      "The dot moves along the parallel line and its number does not change.",
      [{"at": 0.12, "event": "line, parallel line, dot labelled +0.6"}, {"at": 0.35, "event": "dot slides, label stays +0.6 (settled by 50 %)"}, {"at": 0.62, "event": "three parallel lines with −0.6, 0, +0.6"}],
      "ShaderLab signed map with a moving probe", "A number that stays put while a dot moves is only visible in a drawing; the shader picture comes next.",
      "arithmetic: along y = 0.5 x + 0.6 the test is 0.6 everywhere")
px_a, py_a = card_xy(0.7, 0.1)
px_b, py_b = card_xy(0.7, 0.4)
px_c, py_c = card_xy(0.7, 0.7)
lab("B08", 0, "the test as a shader: warm, cool, grey", S1, "lines-and-shine/c02-signed.png", FRAME + "slope 0.5 · the card is a square sprite",
    [{"at": 0.02, "lines": [1], "label": "shader_type canvas_item: the first line says this shader is for 2D drawing"}, {"at": 0.1, "lines": [ln(S1, "void fragment")], "label": "fragment(): runs once for each pixel the shape covers; sets its color"},
     {"at": 0.28, "lines": [ln(S1, "vec2 p"), ln(S1, "p.y = -p.y"), ln(S1, "float v")]}, {"at": 0.36, "lines": [ln(S1, "COLOR")]}],
    "Code card at left (the ten-line shader) whose first two lines carry one-line labels ('shader_type canvas_item: the first line says this shader is for 2D drawing', 'fragment(): runs once for each pixel the shape covers; sets its color'); at right a real Godot window with a square card showing the signed test: warm at the upper left, cool at the lower right, a grey strip between. Three readouts land on the card at the three points from the drawing: +0.6, 0 and −0.6.",
    "Readouts land on the warm, cool and grey regions in the order the voice names them.",
    [{"at": 0.02, "event": "shader_type line labelled"}, {"at": 0.1, "event": "fragment() line labelled"}, {"at": 0.28, "event": "address and test lines highlighted"}, {"at": 0.36, "event": "COLOR line highlighted"}, {"at": 0.42, "event": "+0.6 on the warm side"}, {"at": 0.66, "event": "−0.6 on the cool side"}, {"at": 0.88, "event": "0 on the grey strip"}],
    "LectureCodeTrace alone", "The same three numbers from the drawing, now computed by every pixel, side by side with the code that does it.",
    "C02: Lab card, lab-shaders/01-signed-test.gdshader, slope 0.5, still PNG (640 x 360 frame, card 288 px centred). Probes: p = (0.40, 0.80) reads +0.593, (0.40, 0.20) reads +0.005, (0.40, -0.40) reads -0.603.",
    "Lab A1 (probes) and A0 (UV.y counts downward)",
    readouts=[{"at": 0.42, "text": "+0.6", "x": px_a, "y": py_a}, {"at": 0.88, "text": "0", "x": px_b, "y": py_b}, {"at": 0.66, "text": "−0.6", "x": px_c, "y": py_c}],
    caption="vector: a bundle of two to four numbers (vec2, vec4) · COLOR: the color of the pixel being drawn")
lab("B09", 0, "changing the slope pivots the line", S1, "lines-and-shine/c03-slope-sweep.mp4", FRAME + "slope swept by script",
    [{"at": 0.1, "lines": [ln(S1, "uniform float slope")]}],
    "Code card at left with the uniform line highlighted; at right a real Godot card whose warm and cool halves pivot around the middle as slope sweeps from 0 to 1.5: flat at 0, a diagonal at 1.",
    "The grey strip rotates about the centre as the slope grows.",
    [{"at": 0.06, "event": "slope 0: flat"}, {"at": 0.67, "event": "slope 1: a diagonal"}],
    "manim line pivoting about the origin", "The real picture pivoting is stronger than a drawing of it, and it is the same shader the viewer just read.",
    "C03: Lab card, 01-signed-test, slope 0 to 1.5 linearly over the clip (6 s), Forward+; slope is 1 at 67 percent of the clip.",
    "Lab A2 (stills at slope 0 and 1)", readouts=[{"at": 0.06, "text": "slope 0", "x": 0.5, "y": 0.95}, {"at": 0.67, "text": "slope 1", "x": 0.5, "y": 0.95}])

# ───────────────────────────── ACT II · Slope from an Angle ─────────────────────────────
manim("B10", 1, "the tangent is the slope", "TangentIsSlope",
      "Act title 'Slope from an Angle' (serif 40) top-left. Axes, a warm-grey line through the origin and a pale grey filled wedge for its angle. At across = 1 a warm-grey dashed vertical runs from the axis up to the line, ending in a terracotta dot; its height is a live number. The angle grows from 0 to 60 degrees and the height reads 0, 0.58, 1.0 and 1.73. Labels: 'angle', 'one step across', 'tangent of the angle = the slope'.",
      "The line turns and the height at one step across grows with live numbers.",
      [{"at": 0.1, "event": "title, axes, line at 0"}, {"at": 0.32, "event": "angle grows; height 0.58 at 30, 1.0 at 45 (settled by 50 %)"}, {"at": 0.65, "event": "label 'tangent = slope' settles at 60 degrees: 1.73"}],
      "ShaderLab with tangent readouts", "A height that grows as the angle turns is a mechanism; Manim can show the two numbers move together.",
      "arithmetic (tan 30 = 0.577, tan 45 = 1, tan 60 = 1.732); Lab B (GPU values 0.57735, 1.0, 1.73205)")
lab("B11", 1, "slope = tan(radians(angle)) in the shader", S2, "lines-and-shine/c04-angle-sweep.mp4", FRAME + "angle swept by script",
    [{"at": 0.1, "lines": [ln(S2, "float m")]}],
    "Code card at left with the slope line highlighted; at right a real Godot card whose grey strip turns, climbing to the right, as the angle sweeps from 0 to 60 degrees. Readouts: '0°: m = 0' at the start and '45°: m = 1' as it passes 45.",
    "The strip turns and the readouts give the slope at 0 and 45 degrees.",
    [{"at": 0.1, "event": "slope line highlighted"}, {"at": 0.75, "event": "45°: m = 1"}],
    "LectureCodeTrace alone", "The line turning with the angle uniform is the claim the code makes; the readouts tie the picture to the number.",
    "C04: Lab card, 02-angle-line, angle 0 to 60 linearly over the clip (6 s); angle is 45 at 75 percent. GPU slopes: 0.57735 (30), 1.0 (45), 1.73205 (60).",
    "Lab B (tan values read from the GPU) and C (line climbs to the right)",
    readouts=[{"at": 0.04, "text": "0°: m = 0", "x": 0.5, "y": 0.95}, {"at": 0.75, "text": "45°: m = 1", "x": 0.5, "y": 0.95}], caption="radians: a full turn is about 6.28")
lab("B12", 1, "forgetting radians: thirty degrees read as thirty radians", None, "lines-and-shine/c05-radians-compare.mp4", FRAME + "two cards, same angle, one missing radians()",
    [{"at": 0.08, "lines": [2]}],
    "Two real Godot cards side by side on the stage, the same angle sweeping to 30 degrees. Left: the grey strip climbs gently to the right (m = 0.58). Right: the strip is steep and leans the other way (m = -6.4). Below, the two code lines that differ; a terracotta ring settles on the right card.",
    "Both lines start together; the right one jumps steep and backwards while the left turns smoothly.",
    [{"at": 0.1, "event": "m = 0.58 under the left card"}, {"at": 0.34, "event": "m = -6.4 under the right card"}, {"at": 0.6, "event": "ring on the right card"}],
    "LectureCodeTrace of the two lines", "The wrong picture next to the right one is the whole lesson; the code differs by one word, the picture by everything.",
    "C05: custom scene two_panels.gd (cards 256 px at (170, 190) and (470, 190)): left 02-angle-line, right 03-no-radians; angle 0 to 30 over the first 4 s, then hold 2 s (6 s). GPU slope at 30 without radians(): -6.40533.",
    "Lab B (tan(30.0) = -6.405), two-panel scene I-radians-30", layout="stack",
    code="float m = tan(radians(angle));\nfloat m = tan(angle);", code_file="lab-shaders/02-angle-line.gdshader and 03-no-radians.gdshader (line 8 of each)",
    readouts=[{"at": 0.1, "text": "m = 0.58", "x": 0.266, "y": 0.94}, {"at": 0.34, "text": "m = −6.4", "x": 0.734, "y": 0.94}], rings=[{"at": 0.6, "box": [0.534, 0.17, 0.934, 0.89]}])
manim("B13", 1, "the slope grows without limit toward ninety degrees", "TanExplodes",
      "A plot (shader_kit plot) of tan(angle) against the angle from 0 to 90 degrees, y axis clipped at 10. A terracotta dot rides the curve from 0 degrees; numbers land at 45 (1), 75 (3.7) and 89 (57); the dot leaves the top of the plot as the curve shoots up and a label reads 'no limit'. A small grey line at the left turns with the angle.",
      "The dot rides the curve and then shoots off the top of the plot as the angle nears ninety.",
      [{"at": 0.1, "event": "axes and the start of the curve"}, {"at": 0.22, "event": "45 → 1"}, {"at": 0.38, "event": "75 → 3.7"}, {"at": 0.43, "event": "89 → 57 (all three settled by 50 %)"}, {"at": 0.65, "event": "the dot leaves the top of the plot: 'no limit'"}],
      "LectureEvidenceTable of angle and slope", "A curve that leaves the frame is the claim; a table lists the numbers but cannot run off its own edge.",
      "Lab B: GPU tan 1.0 (45), 3.73205 (75), 57.29004 (89)")
lab("B14", 1, "at ninety the slope jumps sign and the picture swaps sides", S2, "lines-and-shine/c06-seam.mp4", FRAME + "Apple M4 Pro · angle held at three values",
    [{"at": 0.1, "lines": [ln(S2, "float m")]}],
    "Code card at left; at right a real Godot card held at 89.9, then 90, then 91 degrees. The warm and cool halves meet at a vertical edge each time (the grey strip has shrunk to nothing), but at 90 they trade sides and stay traded at 91. Readouts: '89.9°: +573', '90°: −23 million', '91°: −57'.",
    "Warm and cool swap sides between 89.9 and 90 degrees.",
    [{"at": 0.05, "event": "89.9°: +573, warm on the left"}, {"at": 0.38, "event": "90°: −23 million, the halves have swapped"}, {"at": 0.72, "event": "91°: −57, still swapped"}],
    "manim two-line diagram of tan jumping from plus to minus", "The swap is a real event on the real shader; held values make it undeniable and the readouts carry the numbers.",
    "C06: Lab card, 02-angle-line, angle held at 89.9 (0 to 33 percent of the clip), 90.0 (33 to 67), 91.0 (67 to 100); 6 s. GPU tan: +572.967, -22877334, -57.2901.",
    "Lab B and G (sides swap between 89.9 and 90 in both renderers)",
    readouts=[{"at": 0.05, "text": "89.9°: +573", "x": 0.5, "y": 0.95}, {"at": 0.38, "text": "90°: −23 million", "x": 0.5, "y": 0.95}, {"at": 0.72, "text": "91°: −57", "x": 0.5, "y": 0.95}])

# ───────────────────────────── ACT III · Distance to the Line ─────────────────────────────
manim("B15", 2, "two small tools: absolute value and step", "AbsAndStep",
      "Act title 'Distance to the Line' (serif 40) top-left. Left: the test square with the warm-grey line m = 0.5; a pale grey band grows out around the line (the pixels whose answer is near zero), labelled 'a band'. Right, arriving after the band: two small plots. abs(x) as a V with a terracotta dot sliding along x and its height mirrored, labelled 'abs: drop the sign'; step(a, b) as a flat zero that jumps to one where b reaches a, a dot sliding along b, labelled 'step(a, b): 0 until b reaches a, then 1' and the docs rule 'b < a ? 0.0 : 1.0'.",
      "The band grows out of the line, then dots slide along the two plots: the V folds the negative side up, the step jumps from 0 to 1.",
      [{"at": 0.08, "event": "title, the square and its line"}, {"at": 0.25, "event": "a band grows out around the line (settled by 50 %)"}, {"at": 0.66, "event": "the two plots arrive"}, {"at": 0.76, "event": "left dot slides through zero: the V folds the sign away"}, {"at": 0.9, "event": "right dot crosses the jump: 0 then 1"}],
      "LectureEvidenceTable of the two functions", "Each function is a curve with a moving dot; a table of definitions would not show the fold or the jump.",
      "Godot 4.7 docs, built-in functions: abs, step ('b < a ? 0.0 : 1.0')")
cl, cr = card_xy(0.8, 0.2), card_xy(0.75, 0.75)
lab("B16", 2, "step(d, thickness) makes a band", S4, "lines-and-shine/c07-band-raw-45.png", FRAME + "angle 45 · thickness 0.1",
    [{"at": 0.1, "lines": [ln(S4, "float d")]}, {"at": 0.36, "lines": [ln(S4, "COLOR")]}],
    "Code card at left; at right a real Godot card with a white diagonal band across a grey card, climbing to the right. Two readouts on the card: '1' on the band and '0' beside it.",
    "The distance line then the step line are highlighted; '1' lands on the band and '0' off it.",
    [{"at": 0.1, "event": "d line highlighted"}, {"at": 0.36, "event": "step line highlighted"}, {"at": 0.6, "event": "1 on the band"}, {"at": 0.9, "event": "0 off the band"}],
    "LectureCodeTrace alone", "The band and the two lines that make it, with the two values the step returns, is the claim.",
    "C07: Lab card, 04-band-raw, angle 45, thickness 0.1, still PNG. Probes: on the line reads white (1.0), off it grey (0.502).",
    "Lab D-step-order (1 on the line, 0 away; band climbs to the right)",
    readouts=[{"at": 0.6, "text": "1", "x": cl[0], "y": cl[1]}, {"at": 0.9, "text": "0", "x": cr[0], "y": cr[1]}], caption="step(a, b): 0 while b < a, otherwise 1 · vec3(x): the grey x")
lab("B17", 2, "the raw band thins out as the line steepens", S4, "lines-and-shine/c08-band-raw-sweep.mp4", FRAME + "angle swept by script · widths measured",
    [{"at": 0.08, "lines": [ln(S4, "float d")]}],
    "Code card at left; at right the same card with the white band while the angle sweeps: the band is a clear stripe at 0 degrees, visibly thinner at 45, a thin line at 75. Three readouts on the right of the card: '10%', '7%', 'under 3%'.",
    "The band thins to a hairline as the angle grows.",
    [{"at": 0.3, "event": "0°: 10%"}, {"at": 0.64, "event": "45°: 7%"}, {"at": 0.78, "event": "75°: under 3%"}],
    "manim plot of width against angle", "A real band getting thinner is the surprise the voice asks the viewer to predict; the readouts are measured.",
    "C08: Lab card, 04-band-raw, thickness 0.1; angle keyframes as fractions of the clip: 0 until 28 percent, 45 at 62, 75 at 78, 85 at 95. Measured widths (percent of card): 9.7 (0), 6.9 (45), 2.7 (75), 0.7 (85), 0.0 (89, 90).",
    "Lab D (raw band widths)",
    readouts=[{"at": 0.3, "text": "10%", "x": 0.8, "y": 0.25}, {"at": 0.64, "text": "7%", "x": 0.8, "y": 0.45}, {"at": 0.78, "text": "under 3%", "x": 0.8, "y": 0.65}])
manim("B18", 2, "straight up is longer than the shortest way", "TwoGaps",
      "A warm-grey line through the origin and a terracotta dot above it. A light-grey dashed vertical from the dot to the line (label 'straight up 0.6') and a darker solid grey segment at a right angle (label 'shortest way'). The line tilts from 0 to 60 degrees while the point rides with it so the vertical gap stays 0.6; the right-angle segment shrinks and its label reads 0.60, 0.42, 0.30.",
      "The vertical gap stays at 0.6 while the shortest-way segment shrinks as the line tilts.",
      [{"at": 0.05, "event": "line, point, the vertical gap 'straight up 0.6'"}, {"at": 0.25, "event": "the right-angle segment 'shortest way' (0.60 at 0 degrees; settled by 50 %)"}, {"at": 0.6, "event": "tilt to 45 degrees: 0.42"}, {"at": 0.78, "event": "tilt to 60 degrees: 0.30; labels settled"}],
      "ShaderLab with a drawn overlay on the raw band", "Two segments, one fixed and one shrinking, is the argument; a capture cannot draw the right-angle gap.",
      "geometry: shortest = straight-up x cos(angle) = 0.6 x 0.707 = 0.42 (45), 0.6 x 0.5 = 0.30 (60)")
manim("B19", 2, "one right triangle gives the divide", "RightTriangle",
      "A right triangle with legs 1 (across) and 0.5 (up) along a warm-grey line, the long side labelled 'sqrt(1 + 0.5²) = 1.118' (sqrt: the square root). Beside it a second, same-shaped triangle at the point: the straight-up gap 0.6 as its long side. An arrow labelled '÷ 1.118' turns 0.6 into 0.54, 'the shortest distance'.",
      "The small triangle's long side scales the big one; the arrow turns 0.6 into 0.54.",
      [{"at": 0.1, "event": "slope triangle: legs 1 and 0.5"}, {"at": 0.3, "event": "long side 'sqrt(1 + 0.5²) = 1.118'"}, {"at": 0.42, "event": "second triangle at the point, same shape (settled by 50 %)"}, {"at": 0.75, "event": "÷ 1.118 turns 0.6 into 0.54"}],
      "LectureCodeTrace of the formula", "The divide is a similar-triangles fact; two triangles of one shape make it visible, a formula alone would not.",
      "geometry; Lab A3: GPU distance at p = (0.40, 0.80), slope 0.5 reads 0.5373 (expected 0.5388); raw test reads 0.6039 (expected 0.6024)")
lab("B20", 2, "the distance in code, and what thickness means", S5, "lines-and-shine/c09-band-true-45.png", FRAME + "angle 45 · thickness 0.1",
    [{"at": 0.08, "lines": [ln(S5, "float d")]}],
    "Code card at left with the distance line highlighted; at right the white band across the grey card, with a readout '10% wide' on the band.",
    "The distance line is highlighted, then '10% wide' lands on the band.",
    [{"at": 0.08, "event": "d line highlighted"}, {"at": 0.72, "event": "10% wide"}],
    "LectureCodeTrace alone", "The one line that changed, next to the band it makes, with the width the number means.",
    "C09: Lab card, 05-band-true, angle 45, thickness 0.1, still PNG. Measured width 9.8 percent of the card (theory 10).",
    "Lab D (true band widths, 10 percent at every angle)", readouts=[{"at": 0.72, "text": "10% wide", "x": 0.62, "y": 0.3}],
    caption="sqrt(x): the square root of x · thickness is in address units")
lab("B21", 2, "the new band keeps its width while the old one fades away", None, "lines-and-shine/c10-bands-compare.mp4", FRAME + "old and new side by side · angle swept by script",
    [],
    "Two real Godot cards side by side: left the old band, right the new one. The angle sweeps through 15, 45, 75 and 85 degrees: the left band thins to a hairline while the right keeps its width. Readouts: the angle at the centre, 'new: 10%' under the right card and 'old: under 1%' under the left.",
    "The left band fades to a hairline while the right band never changes.",
    [{"at": 0.29, "event": "15°"}, {"at": 0.34, "event": "45°"}, {"at": 0.39, "event": "75°"}, {"at": 0.43, "event": "85°"}, {"at": 0.62, "event": "new: 10%"}, {"at": 0.86, "event": "old: under 1%"}],
    "manim plot of both widths against angle", "Side by side, the same angle, two widths: the comparison is the claim and a real render is its evidence.",
    "C10: custom scene two_panels.gd, cards 256 px at (170, 190) and (470, 190): left 04-band-raw, right 05-band-true, thickness 0.1; angle keyframes (fractions of the clip): 0 until 20 percent, 15 at 30, 45 at 35, 75 at 40, 85 at 44, hold. Measured widths: raw 9.7, 6.6, 2.4, 0.8 percent; true 9.7, 10.0, 9.7, 10.2 percent.",
    "Lab D and two-panel scenes I-bands-15 to 85", layout="video",
    readouts=[{"at": 0.29, "text": "15°", "x": 0.5, "y": 0.95}, {"at": 0.34, "text": "45°", "x": 0.5, "y": 0.95}, {"at": 0.39, "text": "75°", "x": 0.5, "y": 0.95}, {"at": 0.43, "text": "85°", "x": 0.5, "y": 0.95},
              {"at": 0.62, "text": "new: 10%", "x": 0.734, "y": 0.94}, {"at": 0.86, "text": "old: under 1%", "x": 0.266, "y": 0.94}])

# ───────────────────────────── ACT IV · Shine ─────────────────────────────
lab("B22", 3, "an offset slides the line straight across at any angle", S7, "lines-and-shine/c11-slide.mp4", FRAME + "angle and offset set by script",
    [{"at": 0.08, "lines": [ln(S7, "float d")]}],
    "Act title 'Shine' (serif 40) top-left. Code card at left with the distance line highlighted; at right the white band on the grey card sliding from the upper left to the lower right at 35 degrees, then again at 70 degrees at the same speed. Final hold: readouts 'offset 0.5' and '¼ of card'.",
    "The band slides straight across the card, at the same speed at both angles.",
    [{"at": 0.08, "event": "d line (with + offset) highlighted"}, {"at": 0.2, "event": "slides at 35 degrees"}, {"at": 0.66, "event": "slides at 70 degrees"}, {"at": 0.82, "event": "offset 0.5: ¼ of card"}],
    "manim line sliding with distance labels", "The real band sliding at two angles, equally far for equal offsets, is the claim, and the readout is measured.",
    "C11: Lab card, 07-slide, thickness 0.1: angle 35 with offset -0.8 to 0.8 over 5 to 40 percent of the clip; angle 70 with offset -0.8 to 0.5 over 55 to 80 percent, then hold at 0.5; 8 s. Measured: offset 0.5 moves the band 0.250 of the card width at 0, 35 and 70 degrees.",
    "Lab E (offset slide at 0, 35, 70 degrees)", title="Shine",
    readouts=[{"at": 0.82, "text": "offset 0.5", "x": 0.5, "y": 0.05}, {"at": 0.9, "text": "¼ of card", "x": 0.5, "y": 0.95}], caption="offset: how far the line has been slid")
lab("B23", 3, "shifting the center moves the line by an angle-dependent amount", None, "lines-and-shine/c12-center-vs-offset.mp4", FRAME + "flat line, both sweeps scripted",
    [{"at": 0.1, "lines": [1]}],
    "Two real Godot cards side by side, a flat white band across each. Left: the center shifted across from -0.6 to 0.6; the band does not move. Right: the offset swept the same way; the band slides up and down. Readouts under the cards: 'center: no move' and 'offset: slides'.",
    "The flat band on the left never moves while the one on the right slides.",
    [{"at": 0.3, "event": "both sweeps start"}, {"at": 0.62, "event": "center: no move"}, {"at": 0.86, "event": "offset: slides"}],
    "manim arrows showing how far each shift moves a tilted line", "A flat line that ignores a sideways shift is the surprise; a real pair of cards shows it without a word of algebra.",
    "C12: custom scene two_panels.gd, cards 256 px at (170, 190) and (470, 190), angle 0 on both: left 08-center-shift with center.x -0.6 to 0.6, right 07-slide with offset -0.6 to 0.6, over 30 to 78 percent of the clip. Measured: the left band stays at 0.0 px, the right moves 77 px at 0.6.",
    "Lab E and two-panel scenes I-center (centre shift moves the band by shift x sin(angle) or x cos(angle))", layout="stack",
    code="vec2 q = p - center;", code_file="lab-shaders/08-center-shift.gdshader (line 10)",
    readouts=[{"at": 0.62, "text": "center: no move", "x": 0.266, "y": 0.94}, {"at": 0.86, "text": "offset: slides", "x": 0.734, "y": 0.94}])
lab("B24", 3, "mix white into the sprite where the band is", S9L, "lines-and-shine/c13-leak.mp4", FRAME + "first attempt · offset swept by script",
    [{"at": 0.1, "lines": [ln(S9L, "float band")]}, {"at": 0.36, "lines": [ln(S9L, "COLOR =")]}],
    "Code card at left (first attempt, mix on the whole color); at right a real Godot window with the teal test sprite and a white band sweeping across it. The mix line is highlighted.",
    "The white band sweeps across the sprite as the band and mix lines light up.",
    [{"at": 0.1, "event": "band line highlighted"}, {"at": 0.36, "event": "mix line highlighted"}],
    "LectureCodeTrace alone", "Code and its moving result together; the leak is visible here and named in the next beat.",
    "C13: Lab blob sprite, 09-shine-leak, angle 35, thickness 0.1; offset -1.5 to 1.5 linearly over the whole clip (6 s). The white stripe also crosses the empty parts of the sprite's square.",
    "Lab F (leak: the empty pixel on the band line reads white)", caption="mix(a, b, t): t = 0 gives a, t = 1 gives b · vec4(1.0) is white")
lab("B25", 3, "the highlight leaks onto the empty pixels", S9L, "lines-and-shine/c13-leak.mp4", FRAME + "first attempt · offset swept by script",
    [{"at": 0.3, "lines": [ln(S9L, "COLOR =")]}],
    "The same capture and code as before. A readout 'leaks' lands at the upper left where the white stripe crosses the empty part of the sprite's square; the mix line stays highlighted.",
    "The stripe is visible on the empty corners of the sprite's square while the voice names the leak.",
    [{"at": 0.18, "event": "leaks"}, {"at": 0.3, "event": "mix line highlighted"}],
    "ShaderLab with a ring on the stripe", "Pointing at the stripe on the empty corner is the claim; the capture already contains the evidence.",
    "C13 again (same file, no new recording). Measured: the empty pixel on the band line reads white (1.0, 1.0, 1.0) instead of the stage color (0.851, 0.835, 0.792), in both renderers.",
    "Lab F and J", readouts=[{"at": 0.18, "text": "leaks", "x": 0.31, "y": 0.2}])
lab("B26", 3, "multiply the band by alpha", S10, "lines-and-shine/c14-leak-vs-fixed.mp4", FRAME + "old left, fixed right · offset swept by script",
    [{"at": 0.1, "lines": [ln(S10, "float band")]}, {"at": 0.62, "lines": [ln(S10, "float band"), ln(S10, "COLOR.rgb")]}],
    "Two real Godot windows side by side with the teal sprite and a sweeping band: left the first attempt (the stripe spills onto the empty parts), right the fixed shader (the band stays on the sprite). Code card shows the fixed shader with the band line highlighted. Readouts: 'leaks' under the left and 'stays inside' under the right.",
    "The left stripe spills off the sprite; the right band stops at the sprite's edge.",
    [{"at": 0.1, "event": "band line highlighted: * COLOR.a"}, {"at": 0.3, "event": "leaks under the left"}, {"at": 0.7, "event": "stays inside under the right"}],
    "ShaderLab single capture of the fixed shader", "Before and after on the same sweep is the clearest proof the multiplication does the job.",
    "C14: custom scene two_panels.gd, blob sprites 256 px at (170, 190) and (470, 190): left 09-shine-leak, right 10-shine, angle 35, thickness 0.1; offset -1.5 to 1.5 over 5 to 95 percent of the clip (6 s). Measured: the right panel's empty pixel on the band line equals the stage color.",
    "Lab F and two-panel scenes I-leak", readouts=[{"at": 0.3, "text": "leaks", "x": 0.266, "y": 0.94}, {"at": 0.7, "text": "stays inside", "x": 0.734, "y": 0.94}])
lab("B27", 3, "a clock drives the offset: a ramp that repeats", S11, "lines-and-shine/c01-hook.mp4", FRAME + "TIME-driven · scripted clock",
    [{"at": 0.08, "lines": [ln(S11, "float offset")]}],
    "Code card at left with the offset line highlighted; at right the sprite with the glint looping every two seconds (the same capture as the opening) and a thin 0 to 1 ramp strip beneath it whose marker runs from 0 to 1 and restarts every two seconds. A readout 'fract: 0–1' lands at the ramp.",
    "The marker runs along the ramp and restarts as the glint crosses the sprite each cycle.",
    [{"at": 0.08, "event": "offset line highlighted"}, {"at": 0.4, "event": "ramp marker running"}, {"at": 0.64, "event": "fract: 0–1"}],
    "manim sawtooth plot of fract(TIME * 0.5)", "The marker restarting each cycle beside the glint it drives is the claim; the real sprite is the evidence.",
    "C01 reused (11-shine-clock, 12 s loop). The ramp marker repeats with the clip's 2 s period (ShaderLab ramp needs a period; see BUILD-PROMPT).",
    "Lab F (the clock version moves with TIME); docs: fract, TIME", ramp={"at": 0.4, "from": 0, "to": 1, "period": 2.0},
    readouts=[{"at": 0.64, "text": "fract: 0–1", "x": 0.5, "y": 0.95}], caption="TIME: seconds on one clock shared by the whole game")
TWEEN = ('func shine():\n\tvar mat: ShaderMaterial = $Sprite.material\n\tmat.set_shader_parameter("offset", -1.5)\n'
         '\tcreate_tween().tween_property(mat, "shader_parameter/offset", 1.5, 0.8)')
lab("B28", 3, "the game drives the offset with a tween (start value set first)", None, "lines-and-shine/c16-tween.mp4", FRAME + "scripted call at 1 s · no real input",
    [{"at": 0.05, "lines": [1]}, {"at": 0.34, "lines": [3]}, {"at": 0.43, "lines": [4]}, {"at": 0.72, "lines": [3]}],
    "A four-line GDScript card at left (the function that sets the start and tweens the offset); at right the sprite at rest, then one glint crossing it each time the scripted call fires. A label 'scripted call' stays on screen.",
    "The sprite rests, the call fires, one glint crosses, and it rests again.",
    [{"at": 0.05, "event": "func shine() highlighted"}, {"at": 0.34, "event": "set start highlighted"}, {"at": 0.43, "event": "tween line highlighted"}, {"at": 0.72, "event": "start line highlighted again"}],
    "LectureCodeTrace of the GDScript alone", "Cause (one function) and effect (one glint) together; the capture is a real scripted run.",
    "C16: custom scene (verify1.gd T1): Sprite2D 'Sprite' with 10-shine, scene script exactly the four lines shown; the harness calls shine() at 1.0 s and again every 3 s; 12 s loop, Forward+. Verified: the band covers the blob centre 0.388 to 0.429 s after the call (expected 0.373 to 0.427); offset ends at 1.5; resting offset is the default -2.0.",
    "verify1.gd T1 (sweep) and T2 (a tween on a never-set uniform fails: run-1-verify1.log)",
    code=TWEEN, code_file="scene script (GDScript)", readouts=[{"at": 0.1, "text": "scripted call", "x": 0.5, "y": 0.05}],
    caption="tween: glides a value from one number to another over time")
lab("B29", 3, "the whole shine, line by line", S10, "lines-and-shine/c17-shine-sweep.mp4", FRAME + "offset swept by script",
    [{"at": 0.15, "lines": [ln(S10, "vec2 p"), ln(S10, "p.y = -p.y")]}, {"at": 0.24, "lines": [ln(S10, "float m")]}, {"at": 0.41, "lines": [ln(S10, "float d")]},
     {"at": 0.71, "lines": [ln(S10, "float band")]}, {"at": 0.91, "lines": [ln(S10, "COLOR.rgb")]}],
    "The finished fourteen-line shader at left with focus stepping down it as each step is named; at right the sprite with the glint sweeping across once.",
    "Focus steps down the lines in the order the voice names the steps while the glint crosses.",
    [{"at": 0.15, "event": "address lines"}, {"at": 0.24, "event": "slope line"}, {"at": 0.41, "event": "distance line (with the offset)"}, {"at": 0.71, "event": "band line (times alpha)"}, {"at": 0.91, "event": "mix line"}],
    "LectureCodeTrace alone", "The recap needs the code and the result together; paced focus is exactly 'each line earns its place'.",
    "C17: Lab blob sprite, 10-shine, angle 35, thickness 0.1; offset -1.5 to 1.5 over 10 to 90 percent of the clip (8 s). Measured: band on the blob at offset 0, off the sprite at +-1.5.",
    "Lab F")
lab("B30", 3, "a wide shape stretches the address: scale the across part", None, "lines-and-shine/c18-wide-compare.mp4", FRAME + "two 16:9 panels · angle swept by script",
    [{"at": 0.77, "lines": [3]}],
    "Two real 16:9 Godot panels side by side. Left: the band at 45 degrees runs shallow, near 29 degrees on screen. Right, with the across part scaled: 45 degrees really is 45. Readouts: '45° shows 29°' under the left, '45° shows 45°' under the right. Three code lines below.",
    "The left band stays shallow as the angle reaches 45 while the right band reaches a true diagonal.",
    [{"at": 0.58, "event": "45° shows 29°"}, {"at": 0.77, "event": "p.x *= aspect highlighted"}, {"at": 0.8, "event": "45° shows 45°"}],
    "manim rectangle with the address square stretched over it", "The bent angle is visible on real wide panels; a drawing of a stretched square would only describe it.",
    "C18: custom scene two_panels.gd, wide panels 304 x 171 at (160, 180) and (480, 180): left 05-band-true, right 06-wide-fix (aspect 1.7778), thickness 0.1; angle 0 to 45 over 5 to 38 percent of the clip, then hold. Measured: 29.2 degrees on screen without the fix, 44.7 with it; thickness drifts 17.8, 20.8, 27.1 px at 20, 45, 70 degrees without it, constant 17.1 with it.",
    "Lab H and two-panel scenes I-wide", layout="stack",
    code="vec2 p = UV * 2.0 - 1.0;\np.y = -p.y;\np.x *= aspect;", code_file="lab-shaders/06-wide-fix.gdshader (lines 8 to 10)",
    readouts=[{"at": 0.58, "text": "45° shows 29°", "x": 0.266, "y": 0.94}, {"at": 0.8, "text": "45° shows 45°", "x": 0.734, "y": 0.94}])

# ───────────────────────────── ACT V · The Angle-Safe Way ─────────────────────────────
manim("B31", 4, "describe the line by a direction: cosine across, sine up", "UnitStep",
      "Act title 'The Angle-Safe Way' (serif 40) top-left. A grey arrow of length one from the origin at 35 degrees; its across part is drawn along the horizontal axis labelled 'cosine: across' and its up part labelled 'sine: up' (for a step of length one). The arrow turns from 0 to 60 degrees and the two legs grow and shrink.",
      "The arrow turns and its two legs trade length.",
      [{"at": 0.08, "event": "title, axes, the unit arrow at 35 degrees"}, {"at": 0.25, "event": "arrow turns from 0 to 60: the step of length one"}, {"at": 0.44, "event": "settled at 35 degrees (the 50 % frame)"}, {"at": 0.68, "event": "'cosine: across' on the horizontal leg"}, {"at": 0.88, "event": "'sine: up' on the vertical leg"}],
      "ShaderLab with sine and cosine readouts", "Two legs that trade length as the arrow turns is the meaning of cosine and sine; Manim shows it.",
      "geometry (unit circle); Lab G: the direction form equals the slope form pixel for pixel")
manim("B32", 4, "the normal and the dot give the signed distance", "NormalAndDot",
      "The warm-grey line at 35 degrees with its unit arrow along it; a second arrow turned a quarter turn, labelled 'the normal'. A terracotta dot P drops a warm-grey dashed line onto the normal's axis, labelled 'dot(p, n)' with a signed number; P then moves to the other side of the line and the number turns negative. Under it: 'dot: across × across + up × up'.",
      "The point crosses the line and its dot value changes sign while its distance changes smoothly.",
      [{"at": 0.08, "event": "line and its unit arrow"}, {"at": 0.2, "event": "the arrow turns a quarter turn: 'the normal'"}, {"at": 0.42, "event": "label 'dot: across × across + up × up' (settled by 50 %)"}, {"at": 0.7, "event": "P drops onto the normal's axis: dot(p, n)"}, {"at": 0.88, "event": "P crosses the line; the number turns negative"}],
      "LectureCodeTrace of the dot line", "A point projecting onto the normal is the meaning of dot here; a line of code would not show the projection.",
      "Godot 4.7 docs: dot ('a.x * b.x + a.y * b.y + ...'), normalize; geometry")
manim("B33", 4, "the divide was a disguised cosine", "SameThing",
      "An equation chain, one line at a time, each line rewriting the one above: '(y − m x) ÷ sqrt(1 + m²)' → '(y − m x) × cosine' → 'y × cosine − x × sine' → 'p · n'. Beside it the earlier triangle (1, m, sqrt(1 + m²)) with cosine = 1 ÷ sqrt(1 + m²) marked on it.",
      "Each line of the chain rewrites itself into the next, ending on p dot n.",
      [{"at": 0.1, "event": "first line and the triangle"}, {"at": 0.3, "event": "divide becomes × cosine"}, {"at": 0.42, "event": "second line settled (the 50 % frame)"}, {"at": 0.65, "event": "y × cosine − x × sine"}, {"at": 0.8, "event": "ends on p · n"}],
      "LectureEvidenceTable of the two forms", "An equation that transforms into the other form is the claim; a table of two formulas would not show why they match.",
      "algebra: sqrt(1 + m²) = 1 / cos(angle) for angles under 90; Lab G: 0 of 230,400 pixels differ at 30, 60, 89 degrees")
lab("B34", 4, "the direction form in code, matching the slope form", S12, "lines-and-shine/c19-direction-compare.mp4", FRAME + "slope form left, direction form right · angle swept by script",
    [{"at": 0.08, "lines": [ln(S12, "float a ="), ln(S12, "vec2 n")]}, {"at": 0.38, "lines": [ln(S12, "float d")]}],
    "Code card at left (the thirteen-line direction shader); at right two real Godot cards side by side with the slope version on the left and the direction version on the right, the same angle sweeping through 30, 60 and 89 degrees: the two white bands are identical. Labels 'slope form' and 'direction form' under them and 'identical' at the end.",
    "Both bands turn together and stay identical.",
    [{"at": 0.08, "event": "angle and normal lines highlighted"}, {"at": 0.38, "event": "distance line highlighted"}, {"at": 0.8, "event": "identical"}],
    "LectureCodeTrace alone", "Two bands that never differ are the proof of 'pixel for pixel'; a single picture could not show it.",
    "C19: custom scene two_panels.gd, cards 256 px at (170, 190) and (470, 190): left 05-band-true, right 12-direction, thickness 0.1; angle 0 to 89 linearly over 5 to 95 percent of the clip (6 s). Measured: 0 of 230,400 pixels differ at 30, 60 and 89 degrees.",
    "Lab G (pixel differences) and two-panel scene I-bands",
    readouts=[{"at": 0.1, "text": "slope form", "x": 0.266, "y": 0.94}, {"at": 0.1, "text": "direction form", "x": 0.734, "y": 0.94}, {"at": 0.8, "text": "identical", "x": 0.5, "y": 0.05}])
lab("B35", 4, "through ninety the direction form never swaps sides", S13, "lines-and-shine/c20-seam-compare.mp4", FRAME + "slope form left, direction form right · angle held at three values",
    [{"at": 0.08, "lines": [ln(S13, "float v")]}],
    "Two real Godot cards side by side on the stage, held at 89.9, 90 and 91 degrees. Left (slope form): the warm and cool halves trade sides at 90. Right (direction form): they never move. Angle labels at the centre.",
    "The left halves swap at ninety while the right halves stay put.",
    [{"at": 0.06, "event": "89.9°"}, {"at": 0.36, "event": "90°: left swaps"}, {"at": 0.42, "event": "right steady"}, {"at": 0.7, "event": "91°"}],
    "ShaderLab single capture of the direction form", "Side by side, the same angles: the swap on one side and its absence on the other is the claim.",
    "C20: custom scene two_panels.gd, cards 256 px: left 02-angle-line, right 13-direction-signed; angle held at 89.9 (0 to 33 percent of the clip), 90.0 (33 to 67), 91.0 (67 to 100); 6 s. Measured: left swaps between 89.9 and 90 in both renderers; right never swaps from 80 to 100 degrees.",
    "Lab G and J, two-panel scene I-seam",
    readouts=[{"at": 0.06, "text": "89.9°", "x": 0.5, "y": 0.95}, {"at": 0.36, "text": "90°", "x": 0.5, "y": 0.95}, {"at": 0.7, "text": "91°", "x": 0.5, "y": 0.95},
              {"at": 0.36, "text": "swaps", "x": 0.266, "y": 0.06}, {"at": 0.42, "text": "steady", "x": 0.734, "y": 0.06}])

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(5):
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
sl = ["# Shot list: Lines and Shine\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab or scene capture of a tested file in `lab-shaders/`; no editor frames and no docs screenshots are needed. Four things must exist before the build (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`; this film also uses its `caption` prop for one-line definitions and a `ramp.period`). 2. **`shader_kit.py`** Manim helpers (same file; this film uses `uv_square`, `plot` and plain Manim lines, arcs, dots and MathTex). "
      "3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file), plus the two-panel scene `evidence/planning-checks/two_panels.gd` (provided, verified as stills) for the seven compare captures. 4. **Fourteen Manim scenes** named in the rows below.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)

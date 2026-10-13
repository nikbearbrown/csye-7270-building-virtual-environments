#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text; every cue time must follow the spoken words (a cue is placed where its phrase
starts in the beat's narration, as a fraction of the beat's words); and the shot list must say exactly what the lanes say.
Re-run after any edit:  python3 _gen_lanes.py && python3 make_sheet.py
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
spec = importlib.util.spec_from_file_location("narration", HERE / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
NARR = {bid: text for bid, _, text in N.BODY}
E = []      # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def A(bid, phrase, lead=0.02):
    """Fraction of the beat at which `phrase` starts in its narration (a little early, so the picture lands as the words do)."""
    t = NARR[bid]
    i = t.lower().find(phrase.lower())
    assert i >= 0, (bid, phrase)
    f = len(t[:i].split()) / len(t.split())
    return round(min(0.92, max(0.03, f - lead)), 2)


def AW(bid, phrase, lead=0.02):
    """Window-safe A(): a Remotion cue never starts inside the 45 to 55 % window (the midpoint frame is sampled by the gates)."""
    f = A(bid, phrase, lead)
    if 0.45 <= f <= 0.55:
        f = 0.44 if f < 0.50 else 0.56
    return f


def LN(code, sub):
    """1-based line number of the first line of `code` containing `sub`."""
    for i, line in enumerate(code.split("\n"), 1):
        if sub in line:
            return i
    raise AssertionError(sub)


def sq(u, v):
    """Position on the result frame of a SQUARE render centred on the 16:9 capture (the square spans x 0.219 to 0.781, full height)."""
    return round(0.21875 + 0.5625 * u, 3), round(v, 3)


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence):
    """show = [(phrase | float, event)]; a phrase is turned into a fraction of the beat, a float is used as is."""
    cues = [{"at": (A(bid, p) if isinstance(p, str) else p), "event": ev} for p, ev in show]
    cues.sort(key=lambda c: c["at"])
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": cues, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, caption=""):
    props = {"layout": layout, "code": code_of(shader), "codeFile": f"lab-shaders/{shader}", "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    shows = [{"at": (A(bid, p) if isinstance(p, str) else p), "event": ev} for p, ev in show]
    shows.sort(key=lambda c: c["at"])
    add(bid, act, about, {"lane": "capture", "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": shows, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    shows = [{"at": (AW(bid, p) if isinstance(p, str) else p), "event": ev} for p, ev in show]
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": shows, "runner_up": runner, "why": why, "sparse": False}, evidence)


def cue(bid, phrase, code, sub, label=None):
    subs = sub if isinstance(sub, list) else [sub]
    c = {"at": AW(bid, phrase), "lines": [LN(code, s) for s in subs]}
    if label:
        c["label"] = label
    return c


RENDERER = "Forward+"
LAB_NOTE = "Godot 4.7.2 · Forward+ · the shader on the left"
OUT = "godot-shaders/math-toolkit"

# ═══════════════════════════ ACT I · Ramps and Plots ═══════════════════════════
c = code_of("15-ring-final.gdshader")
lab("B01", 0, "the finished ring, drawn by three functions", "15-ring-final.gdshader", f"{OUT}/ring-grow.mp4",
    "Godot 4.7.2 · Forward+ · radius swept by script", [],
    "Act title 'Ramps and Plots' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a soft teal ring on cream, centred, that "
    "grows smoothly from small to large. No code yet.",
    "The ring grows outward the whole time the voice names the three functions that draw it.",
    [(0.0, "small ring, window labelled"), ("one measures distance", "ring growing"), ("By the end, you will be able", "ring near full size")],
    "manim: a ring outline with three function names around it",
    "A real render is the honest 'what you will build'; a drawing would only claim it, and the same file is read line by line in the last act.",
    "C01: Lab render of lab-shaders/15-ring-final.gdshader on a 720x720 square centred in the 1280x720 logical canvas (stage #D9D5CA either side). radius swept "
    "0.12 to 0.38 linearly from 0.5 s to 11.0 s, then held; 13 s, 30 fps, Forward+, no input. Verified: radius 0.12 -> teal at d = 0.16; 0.38 -> teal at d = 0.42.",
    "Lab C01 (15-ring-final; lab-summary.txt rows 15-ring-final-radius*)", layout="video", title="Ramps and Plots")

manim("B02", 0, "a ramp: a smooth run of values from 0 up to 1", "RampStrip",
      "A wide horizontal RAMP STRIP on the cream stage (a row of 64 narrow tiles with thin cream gaps, true grays: value v drawn as gray v, 0 black and 1 white), end labels '0' and '1', and a terracotta "
      "dot riding it with a live value label. Under the strip, in mono: 'UV.x · across the shape'. Caption in serif, the GLOSSARY wording: 'ramp · a smooth run of "
      "values from 0 up to 1'.",
      "The dot slides along the strip from 0 to 1 and its value label climbs; the strip is the ramp.",
      [(0.0, "ramp strip with the end labels 0 and 1; dot not yet shown"), ("Start with a ramp", "caption 'ramp' lands with its definition (landed by 0.30)"),
       ("The simplest ramp", "'pixel' dot appears at the left end with the live value 0.0"), (0.5, "midpoint hold: dot rests at the left end (value 0.0), caption and strip settled"),
       ("zero at the left edge", "dot rides to the right end, the value label climbing to 1.0 (done by 0.76)"), ("In code, that is", "'UV.x · across the shape' tag lands")],
      "ShaderLab: the real gradient with a marker",
      "The ramp is the film's one idea; a strip with a travelling value is the cleanest picture of 'a smooth run of values', and the real render follows in B03.",
      "Manim only (shader_kit ramp_strip; values from plot_data.py 'identity'); Lab 01-ramp probes 0.0196 / 0.498 / 0.9804")

c = code_of("01-ramp.gdshader")
lab("B03", 0, "a number shown as gray: fragment sets COLOR", "01-ramp.gdshader", f"{OUT}/ramp.png", LAB_NOTE,
    [cue("B03", "Fragment runs once", c, "void fragment", "runs once for each pixel the shape covers; sets its color"),
     cue("B03", "Here the color is three copies", c, "COLOR =", "the color of the pixel being drawn; fragment() sets it"),
     cue("B03", "one is white", c, "COLOR =", "alpha · how visible a pixel is: 0 invisible, 1 solid")],
    "Code card at left (the five-line shader), at right a real Godot window showing the black-to-white gradient with a thin 0 to 1 ramp strip under it. "
    "Labels on the highlighted lines carry the GLOSSARY definitions of fragment() and COLOR word for word (60 characters at most each, so they fit on one line or wrap to two); a last label on the COLOR line "
    "gives the GLOSSARY wording of alpha for the final number, 1.0 (the word alpha is on screen only, not spoken).",
    "The fragment line is highlighted, then the COLOR line; the ramp marker sweeps the gradient from 0 to 1 as the voice says 'zero is black, one is white'.",
    [("Fragment runs once", "fragment line highlighted with its label"), ("Here the color is three copies", "COLOR line highlighted with its label"),
     ("zero is black", "ramp marker sweeps left to right under the render"), ("one is white", "marker rests at 1; label 'alpha · how visible a pixel is: 0 invisible, 1 solid' on the COLOR line")],
    "LectureCodeTrace alone",
    "The sentence is about code and its result together: one line, the whole gradient; a code card alone would hide the result.",
    "C02: Lab rect, lab-shaders/01-ramp.gdshader, still PNG 1920x1080 (probes 0.0196 / 0.498 / 0.9804 at x = 0.02 / 0.5 / 0.98; red = green = blue).",
    "Lab C02 (01-ramp)", ramp={"at": AW("B03", "zero is black"), "from": 0, "to": 1}, caption="")

manim("B04", 0, "how to read the series' standard plot", "ReadThePlot",
      "The STANDARD PLOT (defined once in SHOTLIST.md) on the cream stage: square axes, 'input' along the bottom with 0 and 1, 'output' up the side with 0 and 1, "
      "the straight diagonal of f(x) = x, a terracotta dot riding it, a thin dashed drop line from the dot to the ramp strip placed under the axes at the same x "
      "scale, and the ramp strip filling with its tiles up to the drop line. Mono formula tag 'f(x) = x'. A small gray credit under the plot: 'curves drawn from the formulas · checked against Godot 4.7.2 renders'.",
      "The dot travels the diagonal; the drop line keeps its x on the strip and the strip fills up to there.",
      [(0.0, "axes and ticks"), ("The input runs", "'input' label lands along the bottom"), ("the output up the side", "'output' label lands up the side"),
       (0.38, "diagonal draws, dot appears at 0, the empty strip appears below"), (0.4, "dot hops to x = 0.5 (done by 0.45); drop line and strip filled to the middle"),
       (0.5, "midpoint hold: dot rests at x = 0.5, drop line and strip settled, labels visible"), (0.58, "dot rides on to 1; the strip fills fully (done by 0.76)"),
       ("A function that changes nothing", "diagonal highlighted; tag 'f(x) = x' and the small credit line land")],
      "ShaderLab: the real gradient with a marker",
      "The plot grammar is what is being taught and it is reused for every function below, so it is drawn once, slowly, with the dot and the strip locked together.",
      "Manim only (standard plot; plot_data.py 'identity')")

manim("B05", 0, "bending the line bends the strip: 1 - x", "BendTheLine",
      "The standard plot as in B04, now with f(x) = 1 - x: the line starts as the diagonal and swings to run downhill from (0, 1) to (1, 0); the strip beneath "
      "flips from dark-to-light to light-to-dark with it. Mono tag 'f(x) = 1 - x'. A small caption 'predict the strip'.",
      "The diagonal pivots to run downhill and the strip under it flips; the dot then rides the new line.",
      [(0.0, "diagonal plot as in B04, tag f(x) = x"), ("Here the function is one minus x", "tag changes to 1 - x; the line pivots to run downhill (done by 0.34)"),
       (0.36, "dot appears on the downhill line and hops to x = 0.5 (done by 0.44)"), (0.5, "midpoint hold: pivot complete, the strip still shows the old ramp (a beat to predict)"),
       (0.58, "the strip flips to light-to-dark (done by 0.66)"), ("Read the line", "dot rides the downhill line to 1; caption 'predict the strip' lands")],
      "ShaderLab: the real flipped gradient",
      "The point is predicting the strip from the line; the line must visibly bend and the strip must follow, which only a drawn plot can do.",
      "plot_data.py 'one_minus'; dense-compare: one_minus (max difference 0 levels)")

manim("B06", 0, "the toolkit in three families, and where it is going", "ToolkitMap",
      "Three columns of small mono function chips on the cream stage, each under a serif family title: 'Cut and blend' (step, smoothstep, mix, clamp), 'Repeat and fold' "
      "(abs, fract, floor, mod), 'Distance and curves' (length, normalize, distance, pow, sin). At the right a ring outline; thin lines run from the chips distance, "
      "smoothstep and mix to it.",
      "Each family's chips pop in as the voice names it; then three lines draw from distance, smoothstep and mix to the ring and it fills.",
      [(0.03, "three family titles land (by 0.18)"), ("Cut and blend", "first column's chips pop in one by one as named (done by 0.38)"),
       (0.39, "second column's title and chips pop in together (done by 0.45)"), (0.5, "midpoint hold: two columns settled; the third column's title is visible, its chips are not"),
       (0.56, "third column's chips pop in together (done by 0.62)"), ("Then we use three of them", "lines from distance, smoothstep, mix draw to the ring; the ring fills teal")],
      "LibraryIconRow of the function names",
      "A taxonomy with a destination (the ring) is a diagram drawn on the spoken cue; icons would carry no meaning for function names.",
      "Manim only (shader_kit chips; the ring from the last act's capture C16 may be reused as a still)")

# ═══════════════════════════ ACT II · Cut and Blend ═══════════════════════════
manim("B07", 1, "step: 0 below the edge, 1 at or above", "StepSwitch",
      "Act title 'Cut and Blend' (serif 40) top-left. The standard plot with a dashed vertical line at x = 0.5 labelled 'edge'. The curve is 0 until the edge, then 1; at the "
      "edge an open dot at (0.5, 0) and a closed dot at (0.5, 1) mark that the value AT the edge is 1. Mono tag 'step(edge, x) · 0 below the edge, 1 from the edge up' (the GLOSSARY wording). "
      "Strip beneath: left half black tiles, right half white tiles.",
      "The dot rides the 0 level up to the edge, jumps to 1 at the edge and rides on at 1; the strip's hard split lands with it.",
      [(0.0, "axes, edge line labelled 'edge', tag 'step(edge, x)'"), ("Give it an edge", "edge line highlighted"),
       ("Where the ramp is below the edge", "dot appears at x = 0 on the 0 level and rides toward the edge (arrives just left of it by 0.44)"),
       (0.5, "midpoint hold: dot rests just left of the edge on the 0 level, everything settled"),
       ("At the edge or above", "dot jumps to 1 at the edge; closed dot"), ("The plot is a single jump", "dot rides on at 1; the strip's hard split lit")],
      "ShaderLab step render",
      "The jump at the edge is the claim; a plot shows it, shows what happens exactly at the edge, and the real render follows in B08.",
      "function-tables: step_edge_half (x = 0.5 gives 1); dense-compare: step_half (max difference 0 levels)")

c = code_of("02-step.gdshader")
UNIFORM_DEF = "a value your game sets from outside"
UNIFORM_CAPTION = "uniform: a value your game sets from outside; every pixel sees the same one"
lab("B08", 1, "step in a shader; the edge is a uniform dial", "02-step.gdshader", f"{OUT}/step-sweep.mp4", "Godot 4.7.2 · Forward+ · edge swept by script",
    [cue("B08", "In a shader, the edge goes first", c, "step(edge"), cue("B08", "Here the edge is a uniform", c, "uniform float edge", UNIFORM_DEF),
     cue("B08", "Slide it", c, "step(edge")],
    "Code card at left (the eight-line shader); at right a real Godot window split into a black half and a white half by a hard vertical line. A label on the uniform line gives the "
    "first half of the GLOSSARY definition ('a value your game sets from outside') and the caption under the result gives all of it ('uniform: a value your game sets from outside; every pixel sees the same one'). The split slides left and right as the edge dial is swept.",
    "The hard split slides along the window as the edge value is swept.",
    [("In a shader, the edge goes first", "step line highlighted"), ("Here the edge is a uniform", "uniform line highlighted with its label; the caption with the whole definition is on screen"),
     ("Slide it", "the split starts to slide (the capture holds 0.5 until about 4 s)")],
    "manim: the edge marker sliding on the plot",
    "The real hard split sliding is the proof that the edge is the only choice; the code and the dial definition sit beside it.",
    "C03: Lab rect, lab-shaders/02-step.gdshader; edge held at 0.5 until 4.0 s, then 0.5 -> 0.2 over 4.0-6.5 s, then 0.2 -> 0.8 over 6.5-10.5 s, held to 12.5 s; 30 fps, Forward+. "
    "Verified: edge 0.5 -> 0 at x = 0.45 and 1 at x = 0.55; edge 0.2 -> 0 at 0.15, 1 at 0.25; edge 0.8 -> 0 at 0.75, 1 at 0.85.",
    "Lab C03 (02-step; lab-summary.txt rows 02-step-edge*)", caption=UNIFORM_CAPTION)

manim("B09", 1, "clamp pins a number inside a range", "ClampPins",
      "The standard plot with two horizontal guide lines at y = 0 and y = 1 labelled 'low end' and 'high end'. A dashed overshooting ramp y = 2x - 0.5 runs from "
      "(0, -0.5) to (1, 1.5) beyond the guides; the solid curve is clamp(2x - 0.5, 0, 1): flat at 0 until x = 0.25, a ramp to 1 at x = 0.75, flat at 1 after. Short "
      "labels 'max · the higher of two' and 'min · the lower of two' on the two ends, mono tag 'clamp(x, low, high) = min(max(x, low), high)'. Strip beneath: black tiles, a ramp of tiles, white tiles.",
      "The dashed ramp overshoots; the solid curve cuts it flat at the low end, then at the high end; the dot rides the pinned curve.",
      [(0.0, "axes, guides 'low end' and 'high end', tag 'clamp(x, low, high)'"), ("Below the low end", "the dashed overshooting ramp draws; dot on the flat low part, label 'pinned' (done by 0.38)"),
       (0.5, "midpoint hold: dot rests on the flat low part, label 'pinned', settled"), (0.56, "dot rides to the flat high part, label 'pinned' (done by 0.66)"),
       ("In between, nothing changes", "dot rides back along the middle ramp"), ("It is max first, then min", "labels max and min land on the two corners")],
      "ShaderLab clamp render",
      "Pinning is easiest to see as a dashed overshoot cut flat at both ends; a render of a trapezoid gradient would show less.",
      "function-tables: clamp_range, clamp_is_min_max (docs: clamp = min(max(x, minVal), maxVal)); dense-compare: clamp_overshoot (max difference 0 levels)")

manim("B10", 1, "smoothstep: a smooth S between two edges", "SoftSwitch",
      "The standard plot with two dashed vertical edges at x = 0.3 and 0.7 labelled 'first edge' and 'second edge'. The curve is flat at 0, a smooth S rising to 1 between "
      "the edges, flat at 1 after. Mono tag 'smoothstep(a, b, x) · a smooth S between two edges'. Strip beneath: black tiles, a soft ramp of tiles, white tiles.",
      "The curve flattens at 0, swells through a smooth S and lands flat at 1; the dot rides it and the strip's edge is soft.",
      [(0.0, "axes, tag smoothstep(a, b, x); the full S curve draws (done by 0.2)"), ("Give it two edges", "two edge lines labelled 'first edge' and 'second edge' land (done by 0.36)"),
       (0.4, "dot appears on the flat left part"), (0.5, "midpoint hold: dot rests on the flat left part, label '0', settled"),
       (0.56, "dot rides the flat 0 part to the first edge (done by 0.62)"), ("Above the second", "dot jumps ahead to the flat 1 beyond the second edge, label '1' (done by 0.72)"),
       ("Between them", "dot rides the S from the first edge to the second; the strip's soft edge lit (done by 0.95)")],
      "ShaderLab smoothstep render",
      "The S between two edges is the claim; the plot shows that the corners are gone and the strip shows the soft edge.",
      "function-tables: smoothstep_25_75 (0.5 at the middle); dense-compare: smoothstep_3_7 (max difference 0 levels)")

manim("B11", 1, "smoothstep is not a straight line: 0.028, not 0.1", "NotALine",
      "A plot with the input from 0 to 10 and the output from 0 to 1. A dashed straight line from (0, 0) to (10, 1) labelled 'a straight line' and the solid S curve of "
      "smoothstep(0, 10, x) labelled 'the S'. A vertical guide at x = 1 drops; two dots land on the two curves; read-outs '0.1' on the line and '0.028' on the S. A "
      "terracotta ring (grey-backed) rings the slow start of the S near x = 0 to 2. Small grey credit: 'checked in Godot 4.7.2 · Forward+'.",
      "The guide at x = 1 lands two dots on the two curves; the line's reads 0.1, the S's reads 0.028, and the S visibly lies below the line near the start.",
      [(0.0, "plot with both curves and their labels"), ("Say the edges are zero and ten", "guide drops at x = 1; two dots land on the curves (done by 0.40)"),
       (0.5, "midpoint hold: guide and both dots settled, no read-outs yet"), (0.57, "read-out '0.1' on the straight line (done by 0.62)"),
       ("The S gives point zero two eight", "read-out '0.028' on the S; ring on the slow start (done by 0.78)"), ("because it starts out slowly", "credit line lands")],
      "LectureEvidenceTable (0.1 against 0.028)",
      "Two curves and two dots at the same input make the difference visible; a table would only list the numbers.",
      "function-tables: smoothstep_0_10_at_1 (0.02797 measured; linear 0.1004); docs formula t*t*(3.0 - 2.0*t); dense-compare: smoothstep_0_10_over_0_10")

SMOOTH_URL = "https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shader_functions.html#shader-func-smoothstep"
rem("B12", 1, "the docs: smoothstep's formula and its warning", "BrowserCapture",
    {"url": SMOOTH_URL, "image": f"{OUT}/docs-smoothstep.png", "caption": "Godot 4.7 documentation · Built-in shader functions · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1},
                                   {"at": AW("B12", "Squeeze the input"), "x": 0.4, "y": 0.4, "scale": 1.6, "ring": [0.18, 0.36, 0.5, 0.1]},
                                   {"at": AW("B12", "They also warn"), "x": 0.4, "y": 0.5, "scale": 1.6, "ring": [0.18, 0.47, 0.5, 0.05]}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Built-in shader functions' page (the /en/4.7/ address) at the smoothstep entry in a browser window; the camera pushes in on the formula (clamp, then t * t * (3.0 - 2.0 * t)) and a "
    "terracotta ring marks it; later it pushes to the sentence 'Results are undefined if a >= b' and the ring moves there. Ring and camera numbers are fitted to the real capture.",
    "The camera pushes in on the formula the voice describes, then on the warning sentence.",
    [(0.0, "page at the smoothstep entry"), ("Squeeze the input", "push-in + ring on the formula"), ("They also warn", "push to the warning sentence + ring")],
    "manim: the formula typed out",
    "The formula and the warning are documentation claims; the documentation itself is the evidence (SHOW-THE-THING).",
    "Playwright capture D1 of the live 4.7 docs page (1600x900 at 2.4x) at build time; docs read 2026-10-13 (both /en/stable/ and /en/4.7/): 't = clamp((c - a) / (b - a), 0.0, 1.0); return t * t * (3.0 - 2.0 * t);' and 'Results are undefined if a >= b.'")

c = code_of("03-smoothstep.gdshader")
lab("B13", 1, "smoothstep in a shader; narrowing the edges", "03-smoothstep.gdshader", f"{OUT}/smoothstep-sweep.mp4", "Godot 4.7.2 · Forward+ · width swept by script",
    [cue("B13", "In code, the edges", c, "smoothstep("), cue("B13", "Here they sit", c, ["uniform float width", "smoothstep("]),
     cue("B13", "Pull them together", c, "uniform float width")],
    "Code card at left (the eight-line shader with the width dial); at right a real Godot window with a soft black-to-white transition across the middle that sharpens into a "
    "near-hard split as the width is swept down.",
    "The soft edge tightens into a hard split while the voice says 'pull them together'.",
    [("In code, the edges", "smoothstep line highlighted"), ("Here they sit", "uniform and smoothstep lines highlighted"),
     ("Pull them together", "the transition starts to narrow (the capture holds width 0.4 until about 3.5 s)")],
    "manim: the S tightening on the plot",
    "A real render of the edges closing in shows smoothstep turning into a step; the dial and the code are beside it.",
    "C04: Lab rect, lab-shaders/03-smoothstep.gdshader; width held at 0.4 until 3.5 s, then 0.4 -> 0.03 over 3.5-10.0 s, held to 13 s; 30 fps, Forward+. Verified: width 0.45 -> 0.1255 / 0.498 / 0.8745 "
    "at x = 0.25 / 0.5 / 0.75; width 0.3 -> 0.0196 / 0.498 / 0.9804; width 0.03 -> 0 / 0.4824 / 1.",
    "Lab C04 (03-smoothstep; lab-summary.txt rows 03-smoothstep-width*)")

manim("B14", 1, "mix slides from a start to an end by a weight; it does not pin the weight", "MixSlides",
      "The standard plot with the weight (the ramp, axis label 't · weight') as input from 0 to 2 and the output going from a start value to an end value: a straight line from (0, 0.2) "
      "through (1, 0.9), continuing dashed to (2, 1.6); tick labels 'a · start' and 'b · end' on the y axis at 0.2 and 0.9. Read-outs on the line at weights 0, 1 and one half: 'start', 'end', "
      "'halfway'; then at weight 2 the read-out 'overshoots: 1.6'. Mono tag 'mix(a, b, t) · blends from a to b: t of 0 gives a, 1 gives b' (the GLOSSARY wording) and a smaller 'a x (1 - t) + b x t'. A small bracket 'clamp(t, 0, 1)' lands "
      "on the weight axis between 0 and 1. Strip beneath, for weights 0 to 1 only, from the gray of 0.2 up to the gray of 0.9.",
      "The dot rides the line from the start value to the end value, stops at three read-outs, then runs on past the end to 1.6 where the clamp bracket marks the safe range.",
      [(0.0, "axes, tag"), ("Give it a start", "'start' and 'end' ticks land on the y axis (done by 0.25)"), (0.3, "dot at weight 0, read-out 'start'"),
       (0.38, "dot at weight 1, read-out 'end' (done by 0.44)"), (0.5, "midpoint hold: dot rests at weight 1 with 'end', everything settled"),
       (0.57, "dot at one half, read-out 'halfway' (done by 0.62)"), (0.62, "dashed continuation appears"),
       ("a weight of two overshoots the end", "dot runs to weight 2, read-out 'overshoots: 1.6'"), ("so clamp it first", "bracket 'clamp(t, 0, 1)' lands on the weight axis")],
      "ShaderLab mix render",
      "mix is a slide between two values; a line from the start to the end value, with read-outs and a visible overshoot past weight one, is the plot grammar applied.",
      "function-tables: mix_scalar, mix_extrapolates; extra-checks: mix_overshoot (mix(0.2, 0.9, 2.0) = 1.6); dense-compare: mix_a_b (max difference 0 levels); docs formula a * (1 - c) + b * c; "
      "docs (GDScript lerp): 'values outside this range are allowed and can be used to perform extrapolation'")

c = code_of("04-mix-colors.gdshader")
lab("B15", 1, "mix on colours: teal into gold", "04-mix-colors.gdshader", f"{OUT}/mix-colors.png", LAB_NOTE,
    [cue("B15", "A color is a vector", c, "mix(teal"), cue("B15", "Here it blends teal into gold", c, ["vec3 teal", "vec3 gold"]),
     cue("B15", "The function that slid", c, "mix(teal")],
    "Code card at left (the seven-line shader), at right a real Godot window showing a smooth teal-to-gold gradient with the thin 0 to 1 ramp under it.",
    "The mix line is highlighted, then the two colour lines; the ramp marker sweeps the gradient as the voice says 'with the ramp as the weight'.",
    [("A color is a vector", "mix line highlighted"), ("Here it blends teal into gold", "teal and gold lines highlighted"),
     ("with the ramp as the weight", "ramp marker sweeps left to right"), ("The function that slid", "mix line highlighted again")],
    "manim: two colour dots mixing",
    "A real teal-to-gold blend beside the line that makes it shows 'the same function, now on a whole colour'; there is no dark field, so the type gate stays calm.",
    "C05: Lab rect, lab-shaders/04-mix-colors.gdshader, still PNG 1920x1080. Verified: x = 0.02 -> (0.3804, 0.6431, 0.5686); 0.5 -> (0.6627, 0.7216, 0.5098); 0.98 -> (0.949, 0.7961, 0.451).",
    "Lab C05 (04-mix-colors); dense-compare: blend_plain_ramp (max difference 0 levels)",
    ramp={"at": AW("B15", "with the ramp as the weight"), "from": 0, "to": 1})

manim("B16", 1, "any reshaped ramp can be the weight; the word 'mask'", "AnyWeight",
      "Three stacked rows. Each row: a small plot of a weight curve (the plain ramp; step at 0.5; smoothstep 0.4 to 0.6), an arrow drawn as a shape, then a teal-to-gold "
      "strip blended with that weight (hard cut for step, soft edge for smoothstep). Row captions 'plain ramp', 'step', 'smoothstep'. At the end a grey-backed bracket round the "
      "three weight plots and the GLOSSARY wording in serif: 'mask · a number from 0 to 1 per pixel saying how much of something to show'.",
      "Each row builds left to right on its spoken word; the bracket and the word 'mask' land last.",
      [(0.0, "three row captions"), ("The plain ramp gives", "row 1: ramp plot, arrow, smooth blend (done by 0.28)"), ("Step gives a hard cut", "row 2: step plot, arrow, hard-cut blend (done by 0.40)"),
       (0.36, "row 3 (smoothstep): plot, arrow, soft blend (done by 0.44)"), (0.5, "midpoint hold: all three rows settled"), (0.58, "grey-backed bracket round the three weight plots (done by 0.66)"),
       (0.72, "the 'mask' definition types in"), ("is called a mask", "the word 'mask' highlighted")],
      "ShaderLab: three real renders",
      "Three weights in a column, each with its curve and its blend, is the comparison itself; the blends are checked against real renders (dense-compare).",
      "dense-compare: blend_plain_ramp, blend_step, blend_smoothstep (each max difference 0 levels); GLOSSARY: mask")

# ═══════════════════════════ ACT III · Repeat and Fold ═══════════════════════════
manim("B17", 2, "re-centering a ramp: x * 2 - 1 runs from -1 to 1", "Recenter",
      "Act title 'Repeat and Fold' (serif 40) top-left. The ramp strip with tick labels 0 and 1 and a terracotta dot at its middle. Mono formula tag 'x × 2 − 1' appears; the "
      "tick labels first stretch to 0 and 2 (the '× 2' step), then slide to −1 and 1 (the '− 1' step), with a zero marker landing at the centre under the dot. "
      "A small caption 'zero here'.",
      "The strip's tick labels stretch to 0..2 and then shift to −1..1 while the strip itself stays put; zero lands under the dot.",
      [(0.0, "strip with 0 and 1, dot at the middle"), ("Multiply by two", "tag '× 2'; ticks stretch to 0 and 2 (done by 0.30)"),
       (0.32, "tag '− 1'; ticks slide to −1 and 1 (done by 0.42)"), (0.5, "midpoint hold: ticks −1 and 1 settled, both tags visible"),
       (0.58, "a zero marker lands at the centre under the dot"), ("Now negative numbers", "caption 'zero here' and a highlight on the left half")],
      "LectureEvidenceTable of before and after ranges",
      "Moving the ticks of the strip from 0..1 to −1..1 is the whole idea, and a table would not move.",
      "function-tables: abs_centered (x * 2 - 1 gives -1 at x = 0, 0 at 0.5, 1 at 1 via abs); plain arithmetic")

manim("B18", 2, "abs folds a −1..1 ramp at zero: a V", "FoldAtZero",
      "The ramp strip with ticks −1, 0, 1 (from B17), a terracotta dot at 0. The strip's left half folds over onto the right half like a page about the zero line (a half-turn "
      "Transform, finished by 0.44). Below it the standard plot of abs(x) over −1..1: a V with the dot riding down the left arm and up the right arm. Mono tag 'abs(x) · drops "
      "the minus sign'. Strip beneath the plot: white, black, white tiles.",
      "The left half of the strip folds onto the right half; then the dot rides the V and the strip beneath reads white, black, white.",
      [(0.0, "strip with −1, 0, 1; tag abs(x)"), ("Fold the ramp at zero", "the left half folds over the right half (done by 0.40)"),
       (0.5, "midpoint hold: folded strip settled, dot at 0"), (0.58, "the V plot draws under the strip"), ("The plot is a V", "dot rides down the left arm and up the right arm (done by 0.85)"),
       ("bright, dark, bright", "mirror strip lit")],
      "ShaderLab abs render",
      "The fold is a motion: the left half of the strip lands on the right half; a render would show only the result.",
      "function-tables: abs_centered (1, 0.5, 0, 0.5, 1); dense-compare: abs_centered (max difference 0 levels)")

manim("B19", 2, "fract: the part after the decimal point; four ramps in a row", "RampRestarts",
      "A small inset number line with a dot at 2.75 splitting into '2' and '.75' and the arrow '2.75 → 0.75'; mono tag 'fract(x) · the part after the point: x minus floor(x)'. Then the standard plot: a steep dashed "
      "ramp 4x leaves the top of the plot, and the solid curve is fract(4x): four saw teeth (each climbing 0 to 1, falling back to 0 at x = 0.25, 0.5, 0.75) with open and "
      "closed dots at the jumps. The dot rides the teeth; the strip beneath shows four ramps in a row.",
      "The dot climbs a tooth, drops back to zero at each whole number and climbs again; the strip repeats four times.",
      [(0.0, "the fract tag lands"), ("Two point seven five becomes", "inset: 2.75 splits into 2 and 0.75; arrow to 0.75 (done by 0.42)"),
       (0.5, "midpoint hold: inset and tag settled, the plot not yet drawn"), (0.57, "the dashed 4x line and the four teeth draw (done by 0.70)"),
       (0.72, "dot rides the teeth; the strip shows four ramps (done by 0.95)")],
      "ShaderLab fract render",
      "A dot falling back to zero at each whole number is the sawtooth's meaning; the real render follows in B20.",
      "function-tables: fract_x4, fract_negative (docs: x - floor(x)); dense-compare: fract_4 (max difference 0 levels)")

c = code_of("05-fract.gdshader")
lab("B20", 2, "fract in a shader; the count dial", "05-fract.gdshader", f"{OUT}/fract-sweep.mp4", "Godot 4.7.2 · Forward+ · count swept by script",
    [cue("B20", "Fract is one line", c, "fract("), cue("B20", "The number you multiply by", c, ["uniform float count", "fract("]),
     cue("B20", "Turn that dial", c, "uniform float count")],
    "Code card at left (the eight-line shader with the count dial); at right a real Godot window showing one black-to-white ramp that splits into 2, 3, 4 ... 6 repeating ramps as "
    "the count is swept up.",
    "The picture fills with more and more repeating ramps while the voice says 'from one up to six'.",
    [("Fract is one line", "fract line highlighted"), ("The number you multiply by", "uniform and fract lines highlighted"),
     ("Turn that dial", "the count starts to climb (the capture holds 1 until about 4.5 s)")],
    "manim: the count changing on the plot",
    "Turning the dial and seeing ramps multiply is the effect; the real render beside one line of code is the proof.",
    "C06: Lab rect, lab-shaders/05-fract.gdshader; count held at 1 until 4.5 s, then 1 -> 6 over 4.5-10.5 s, held to 12.5 s; 30 fps, Forward+. Verified: count 1 -> 0.098 / 0.298 / 0.6 / 0.898 at x = 0.1 / 0.3 / 0.6 / 0.9; "
    "count 4 -> 0.3961 / 0.1961 / 0.3961 / 0.5961; count 6 -> 0.5961 / 0.7961 / 0.5961 / 0.3961.",
    "Lab C06 (05-fract; lab-summary.txt rows 05-fract-count*)")

manim("B21", 2, "floor: rounds down; floor(4x) is four flat steps", "RoundDown",
      "Mono tag 'floor(x) · rounds down to the whole number below' with a tiny inset '2.75 → 2'. The standard plot with output 0 to 4: a dashed diagonal 4x and the solid "
      "staircase floor(4x) with values 0, 1, 2, 3 (closed dot at the left end of each step, open dot at the right end). Strip beneath: four flat bands (shown divided by 3, "
      "note '÷ 3 to fit') labelled 0 1 2 3.",
      "The staircase builds one step at a time as the voice counts zero, one, two, three; the strip gets four flat bands.",
      [(0.0, "tag 'floor(x)'"), ("It rounds down", "inset '2.75 → 2' lands (done by 0.30)"), (0.38, "plot appears: the dashed 4x diagonal and the first step (done by 0.45)"),
       (0.5, "midpoint hold: dashed diagonal and the first step settled"), ("zero, one, two, three", "steps 1, 2, 3 land one by one (done by 0.82)"),
       ("with a jump between each", "the strip's four bands lit; open and closed dots visible")],
      "ShaderLab floor render",
      "A staircase with open and closed dots shows exactly where each step starts; the strip's four flat bands carry the idea.",
      "function-tables: floor_x4, floor_negative; dense-compare: floor_4_over_3 (max difference 0 levels)")

manim("B22", 2, "x splits into floor and fract", "WholeAndLeftover",
      "A number line from 0 to 4 with a dot at 2.75. Two brackets under it: from 0 to 2 labelled 'floor = 2' and from 2 to 2.75 labelled 'fract = 0.75'; equation in serif "
      "'2.75 = 2 + 0.75'. Then the dot slides from 0 to 4 with two live read-outs: 'floor' stepping 0, 1, 2, 3 and 'fract' climbing and resetting.",
      "The dot splits into a whole part and a leftover; then it slides along the line while 'floor' steps and 'fract' resets at each whole number.",
      [(0.0, "number line 0 to 4 with the dot at 2.75"), ("Floor is the whole part", "bracket 'floor = 2' (done by 0.2)"), ("fract is the leftover", "bracket 'fract = 0.75' (done by 0.33)"),
       (0.37, "equation '2.75 = 2 + 0.75' lands (done by 0.44)"), (0.5, "midpoint hold: equation settled"), ("So floor says which section", "dot slides 0 to 4; floor steps, fract resets (done by 0.9)"),
       ("where inside it", "dot ends at 4")],
      "LectureEvidenceTable (x, floor, fract)",
      "A number line with a dot that splits into two read-outs is the whole-and-leftover idea in motion.",
      "function-tables: floor_plus_fract (floor(x) + fract(x) = x, negatives included)")

c = code_of("06-stripes.gdshader")
lab("B23", 2, "fract then step: stripes", "06-stripes.gdshader", f"{OUT}/stripes.png", LAB_NOTE,
    [cue("B23", "Fract makes the ramp restart", c, "step(0.5", "fract · restarts"),
     cue("B23", "and step cuts each copy", c, "step(0.5", "step · cuts"),
     cue("B23", "Change the multiplier", c, "step(0.5", "× 8 · the count")],
    "Code card at left (the six-line shader), at right a real Godot window of black and white vertical stripes (sixteen bands: eight ramps, each cut in half). The step(...fract(...)) line is highlighted with a short "
    "label (one or two words) that changes to name each function's job.",
    "The same line is highlighted while three labels name what fract does, what step does, and what the multiplier sets.",
    [("Combine fract with step", "stripes visible, line highlighted"), ("Fract makes the ramp restart", "label: fract · restarts"), ("and step cuts each copy", "label: step · cuts"),
     ("Change the multiplier", "label: × 8 · the count")],
    "manim: stripes built from two plots",
    "Stripes from two functions are best shown as real stripes; labels on the code line name each function's job.",
    "C07: Lab rect, lab-shaders/06-stripes.gdshader, still PNG 1920x1080. Verified: x = 0.05 -> 0; 0.1 -> 1; 0.15 -> 0; 0.2 -> 1.",
    "Lab C07 (06-stripes); dense-compare: stripes (max difference 0 levels)")

manim("B24", 2, "mod: the remainder; mod(x, 1) is fract", "Remainder",
      "A mono tag 'mod(x, y) · the remainder after dividing x by y' (the GLOSSARY wording) and the formula 'mod(x, y) = x − y · floor(x / y)' assembling term by term. Then a small card 'y = 1: same as fract(x)' and the standard plot of mod(x, 0.25): four "
      "teeth of height 0.25 (plot output 0 to 0.25) with the dot riding them; caption 'y = 0.25: repeats every 0.25'. Strip beneath: four ramps.",
      "The formula assembles; then the dot rides four teeth that each repeat every quarter.",
      [(0.0, "'mod(x, y) =' lands"), ("x minus y times floor", "the right-hand side assembles term by term (done by 0.40)"),
       (0.4, "card 'y = 1: same as fract(x)' lands (done by 0.45)"), (0.5, "midpoint hold: formula and card settled, nothing moving"),
       ("With y of point two five", "teeth plot draws; dot rides four teeth; the strip shows four ramps (done by 0.95)")],
      "LectureCodeTrace of the formula",
      "The formula assembling term by term, then repeating as teeth on the plot, shows both the rule and what it does.",
      "function-tables: mod_quarter, mod_one_minus_fract, mod_formula, mod_is_y_times_fract (docs: x - y * floor(x/y)); dense-compare: mod_quarter_x4")

MOD_ROWS = [["shader", "mod(-0.25, 1.0)", "0.75"], ["GDScript", "fmod(-0.25, 1.0)", "-0.25"], ["GDScript", "fposmod(-0.25, 1.0)", "0.75"]]
rem("B25", 2, "the mod trap: a shader and GDScript disagree on negatives", "LectureEvidenceTable",
    {"title": "mod of a negative number", "headers": ["Where", "Call", "Result"], "rows": MOD_ROWS,
     "note": "Godot 4.7.2 · Forward+ · shader value read from a render · GDScript values from a script run",
     "cues": [0.06, 0.38, 0.60], "durationSeconds": "__AUDIO__"},
    "A three-row table: the shader row, then GDScript's fmod row (keeps the sign), then fposmod (matches the shader); the active row is ringed as the voice names it.",
    "The ring moves down the rows with the voice; the minus sign on the fmod result is the surprise.",
    [(0.06, "shader row"), (0.38, "fmod row (landed by 0.44)"), (0.60, "fposmod row")],
    "manim: number line with a floor arrow",
    "A three-row table of measured values from two environments is exactly a comparison of where, call and result.",
    "function-tables: mod_one_negative (0.749 at -0.25 and -1.25); run-1-verify-mod.log: fmod(-0.25, 1.0) = -0.25, fposmod = 0.75; docs: fmod keeps the sign of x, fposmod wraps equally in positive and negative")

# ═══════════════════════════ ACT IV · Distance and Curves ═══════════════════════════
manim("B26", 3, "length of a vector: (3, 4) has length 5", "HowLong",
      "Act title 'Distance and Curves' (serif 40) top-left. A pair of axes with the origin at the top left, x to the right and y counting DOWN (a small label 'y counts down', as the address does), and a vector arrow from the origin to (3, 4): "
      "dashed legs 3 across and 4 down, hypotenuse labelled 5; mono tag 'length(v) · the length of a vector' (the GLOSSARY wording, cut before its 'of an offset' clause because the film never says offset) and the formula '√(x² + y²)', plus 'v = (3, 4)'.",
      "The legs draw (three across, then four down), the arrow follows, and the length 5 lands last.",
      [(0.0, "axes, tag length(v)"), ("A vector bundles them", "vector (3, 4) arrow drawn from the origin; label 'v = (3, 4)' (done by 0.30)"),
       (0.5, "midpoint hold: arrow and label settled"), (0.58, "legs draw: 3 across, then 4 down (done by 0.72)"),
       ("the square root of nine", "label '5' lands on the arrow; formula '3² + 4² = 25' (done by 0.9)")],
      "LectureEvidenceTable",
      "A right triangle drawn leg by leg is what 'length' means; the number five lands last.",
      "function-tables: length_3_4 (5.0 within 0.00002); docs: length = sqrt(x[0] * x[0] + x[1] * x[1] + ...)")

manim("B27", 3, "normalize: same direction, length 1", "UnitArrow",
      "The axes of B26 (origin top left, y counting down) with the vector (3, 4) in grey and a unit circle (radius 1, the quarter that lies in the picture) drawn at the origin. The arrow shrinks along its own line until its tip rests on the "
      "circle at (0.6, 0.8). Labels change from 'length 5' to 'length 1'; mono tag 'normalize(v) · same direction, length 1'.",
      "The arrow slides back along its own line onto the unit circle: the direction stays, the length becomes one.",
      [(0.0, "axes, unit circle, tag normalize(v)"), ("Take the arrow", "grey arrow (3, 4) drawn; label 'length 5' (done by 0.42)"),
       (0.5, "midpoint hold: arrow and circle settled, nothing moving"), (0.58, "the arrow shrinks along its own line onto the circle; label '(0.6, 0.8)' (done by 0.72)"),
       ("same direction, length one", "label 'length 1' lands")],
      "ShaderLab normalize render",
      "The arrow shrinking along its own line onto the unit circle is the idea; a render would hide it.",
      "function-tables: normalize_length (1.0 within 0.00002); Lab: normalize(vec2(3, 4)) = (0.6, 0.8); docs: same direction as x, length 1.0")

manim("B28", 3, "distance: ask every pixel how far it is from the middle", "AskEveryPixel",
      "The UV square (0 to 1 across, 0 to 1 down, y pointing down) with a terracotta dot at the middle labelled 'middle'. Mono tag 'distance(a, b) = length(a − b)'. Five pixel dots "
      "appear one at a time, each joined to the middle by a dashed line and carrying its real distance: (0.9, 0.5) 0.40, (0.5, 0.2) 0.30, (0.15, 0.85) 0.49, (0.95, 0.95) 0.64, "
      "(0.55, 0.55) 0.07.",
      "Pixel dots land one by one with dashed lines to the middle and their distances; near dots read small, far dots read big.",
      [(0.0, "UV square, tag distance(a, b) = length(a − b)"), ("Pick the middle", "'middle' dot lands (done by 0.32)"),
       (0.34, "pixel dots land one by one with dashed lines and numbers: 0.40, 0.30, 0.49 (done by 0.45)"), (0.5, "midpoint hold: three pixel dots settled with their distances"),
       ("Pixels near the middle", "a near dot (0.07) lands"), ("pixels far away", "a far dot (0.64) lands")],
      "ShaderLab distance render",
      "A middle dot and several pixels with dashed lines and numbers is 'ask every pixel how far'; the real render is next.",
      "function-tables: distance_to_middle (0.7071 at the corners, 0.5 straight below the middle); docs: distance = length(a - b)")

c = code_of("08-distance.gdshader")
lab("B29", 3, "distance in a shader: a ramp growing outward", "08-distance.gdshader", f"{OUT}/distance.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B29", "That is one line of shader", c, "float d"), cue("B29", "The result is a ramp", c, "COLOR =")],
    "Code card at left (the six-line shader); at right a real Godot window with a square picture: black in the middle growing to light grey at the edges and corners, like a cone seen "
    "from above. Two read-outs: '0.5' at the middle of the right edge and '0.71' near a corner.",
    "The distance line is highlighted, then the COLOR line; read-outs land on the edge middle and on a corner.",
    [("That is one line of shader", "distance line highlighted"), ("The result is a ramp", "COLOR line highlighted"),
     ("The middle of each edge", "read-out 0.5 at the edge middle"), ("the corners are about", "read-out 0.71 at a corner")],
    "manim: the UV square shaded",
    "The real distance picture beside its one line shows the ramp that grows outward and carries the two key numbers, 0.5 and 0.71.",
    "C08: Lab square render of lab-shaders/08-distance.gdshader (720x720 centred in the 1280x720 canvas), still. Verified (360x360 Lab): middle 0.0039; (0.75, 0.5) 0.2471; "
    "edge middle 0.4941; corner 0.7059 (the exact corner value is 0.7071).",
    "Lab C08 (08-distance); function-tables: distance_corner_exact",
    readouts=[{"at": AW("B29", "The middle of each edge"), "text": "0.5", "x": sq(0.9, 0.5)[0], "y": sq(0.9, 0.5)[1]},
              {"at": AW("B29", "the corners are about"), "text": "0.71", "x": sq(0.1, 0.1)[0], "y": sq(0.1, 0.1)[1]}])

manim("B30", 3, "a circle on a wide shape becomes an oval: UV runs 0 to 1 on both sides", "RoundOnSquare",
      "A square UV picture with the ticks '0 → 1' across the top and '0 → 1' down the left side (y counts down, as everywhere in the film) and an outlined circle of radius 0.3 drawn in it, label 'square: round'. The square then stretches horizontally into a 2:1 "
      "rectangle and the circle stretches with it into an oval; the ticks across and down still read '0 → 1'. Labels 'wide: oval' and a small grey credit 'measured: 384 × 192 px · "
      "Godot 4.7.2 · Forward+'.",
      "The square stretches into a wide rectangle and carries the circle with it into an oval while the tick labels stay 0 to 1.",
      [(0.0, "square with the circle; label 'square: round'"), ("On a wide one", "the square stretches to 2:1, the circle becomes an oval (done by 0.40)"),
       (0.44, "label 'wide: oval' lands"), (0.5, "midpoint hold: wide rectangle and oval settled"), (0.58, "tick labels on both sides highlighted: 0 → 1 (done by 0.64)"),
       ("so the circle stretches", "credit line lands")],
      "ShaderLab: a real wide render",
      "A square stretching into a rectangle and carrying the circle with it is the cause (the address runs 0 to 1 on both sides); the measured proof sits in the evidence.",
      "evidence/planning-checks/ellipse-measure.md: 640x320 shape, disk 384 x 192 px (width/height 2.0); square 216 x 216")

c = code_of("09-glow.gdshader")
lab("B31", 3, "distance as a weight: a soft spot of light", "09-glow.gdshader", f"{OUT}/glow.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B31", "Distance is another ramp", c, "float d"), cue("B31", "One minus a smooth step", c, "float glow")],
    "Code card at left (the seven-line shader); at right a real Godot window with a square picture: a soft white spot in the middle fading to black at the edges. Read-outs '1' in the "
    "middle and '0' near the edge.",
    "The distance line is highlighted, then the glow line; read-outs land on the middle and the edge.",
    [("Distance is another ramp", "distance line highlighted"), ("One minus a smooth step", "glow line highlighted"),
     ("It is brightest in the middle", "read-out 1 in the middle"), ("fades to nothing at the edge", "read-out 0 near the edge")],
    "manim: the three curves multiplied",
    "A real soft spot beside the line '1 - smoothstep' shows the composition of the two functions.",
    "C09: Lab square render of lab-shaders/09-glow.gdshader, still. Verified (360x360 Lab): middle 1.0; (0.75, 0.5) 0.5059; edge middle 0.0; corner 0.0.",
    "Lab C09 (09-glow); dense-compare: sq_09_glow (max difference 0 levels)",
    readouts=[{"at": AW("B31", "It is brightest in the middle"), "text": "1", "x": sq(0.5, 0.5)[0], "y": sq(0.5, 0.5)[1]},
              {"at": AW("B31", "fades to nothing at the edge"), "text": "0", "x": sq(0.9, 0.5)[0], "y": sq(0.9, 0.5)[1]}])

manim("B32", 3, "pow bends the curve: above 1 pulls down, below 1 pushes up", "BendTheCurve",
      "The standard plot with three curves: the diagonal (power 1), a sagging curve (power 3) and a bowing curve (power 1/2), each labelled in mono ('x^3', 'x', 'x^0.5') and "
      "mono tag 'pow(x, y) · x to the power y'. The dot rides power 3 with a strip that is bright only near the right end; then power 1/2 with a brighter strip; then power 1 (the diagonal).",
      "The dot rides the sagging curve and the strip stays dark until the far end; on the bowing curve the strip is bright early; on power 1 nothing changes.",
      [(0.0, "axes, tag pow(x, y)"), ("On a ramp from zero to one", "power-3 curve draws; dot appears at x = 0 (done by 0.34)"),
       (0.36, "dot rides the power-3 curve to x = 0.5; the strip fills dark so far (done by 0.44)"), (0.5, "midpoint hold: dot at x = 0.5 on the power-3 curve, strip dark so far, settled"),
       (0.58, "dot rides on to 1; the strip is bright only near the right end (done by 0.72)"), ("Below one", "power-1/2 curve draws; dot rides it; the strip is bright early (done by 0.88)"),
       ("Exactly one changes nothing", "diagonal highlighted; dot rides it")],
      "ShaderLab pow render",
      "Three curves of different powers with the strip changing under the travelling dot show 'pulls down, pushes up' better than any one render.",
      "function-tables: pow_3, pow_2, pow_half, pow_one; dense-compare: pow_3, pow_half (max difference 0 levels)")

c = code_of("07-pow.gdshader")
lab("B33", 3, "pow in a shader; the power dial; the negative-base warning", "07-pow.gdshader", f"{OUT}/pow-sweep.mp4", "Godot 4.7.2 · Forward+ · power swept by script",
    [cue("B33", "In code, pow takes", c, "pow("), cue("B33", "Turn the power up", c, ["uniform float power", "pow("]),
     cue("B33", "Keep the first number", c, "pow(", "first number ≥ 0")],
    "Code card at left (the eight-line shader with the power dial); at right a real Godot window with a black-to-white gradient whose bright part squeezes toward the right edge as the "
    "power is swept from 1 up to 6. The pow line carries the short label 'first number ≥ 0' (the docs' warning is in the voice).",
    "The bright region shrinks toward the right edge while the voice says 'squeezes toward the right edge'.",
    [("In code, pow takes", "pow line highlighted"), ("Turn the power up", "uniform and pow lines highlighted; the sweep begins (the capture holds 1 until about 3 s)"),
     ("Keep the first number", "pow line highlighted with the warning label")],
    "manim: the bright region shrinking",
    "Turning the power dial on a real render is the effect; the caution about a negative base sits on the code line.",
    "C10: Lab rect, lab-shaders/07-pow.gdshader; power held at 1 until 3.0 s, then 1 -> 6 over 3.0-11.0 s, held to 15.5 s; 30 fps, Forward+. Verified: power 1 -> 0.498 / 0.898 at x = 0.5 / 0.9; "
    "power 3 -> 0.1255 / 0.7255; power 6 -> 0.0157 / 0.5294.",
    "Lab C10 (07-pow; lab-summary.txt rows 07-pow-power*); docs: pow undefined if x < 0 (observation row OBS-pow_negative_base, not relied on)")

manim("B34", 3, "sine: the smooth repeat, squeezed into 0..1", "SmoothRepeat",
      "A plot of sin over two cycles with the output from −1 to 1 and a dot riding it; range ticks −1 and 1. Mono tag 'sin(x) · a smooth wave between −1 and 1'. The curve is then squeezed and lifted into 0..1 "
      "('0.5 + 0.5 · sin(x)') and the strip beneath shows two soft bands. A faint grey ghost of the fract saw teeth appears behind it with the caption 'smooth cousin'.",
      "The wave rolls between −1 and 1, is squeezed into 0 to 1, and a ghost of fract's sharp teeth shows the smooth version beside it.",
      [(0.0, "axes, tag sin(x)"), ("Sine repeats smoothly", "the wave draws; dot rides it; ticks −1 and 1 land (done by 0.40)"),
       (0.5, "midpoint hold: wave and ticks settled, nothing moving"), (0.56, "the wave squeezes and lifts into 0 to 1; the strip shows two soft bands (done by 0.68)"),
       ("Think of it as", "fract ghost and caption 'smooth cousin'")],
      "ShaderLab sine render",
      "A wave squeezed from −1..1 into 0..1 is a change of axes, and a ghost of fract's teeth beside it makes 'smooth cousin' literal.",
      "function-tables: sine_squeezed, sine_range_min; dense-compare: sine_two_cycles (max difference 0 levels)")

# ═══════════════════════════ ACT V · Build a Ring ═══════════════════════════
c = code_of("10-disk.gdshader")
lab("B35", 4, "step on the distance: a disk", "10-disk.gdshader", f"{OUT}/disk.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B35", "Take the distance to the middle", c, "float d"), cue("B35", "cut it with step at point three", c, "step(0.3")],
    "Act title 'Build a Ring' (serif 40) top-left. Code card at left (the six-line shader); at right a real Godot window with a square picture: a black disk on white. Read-outs '0' "
    "in the disk and '1' outside; a terracotta ring (grey-backed) round the disk's edge at the end.",
    "The distance line, then the step line, are highlighted; the read-outs name the two sides and the ring marks the edge.",
    [("Time to build", "title; picture visible"), ("Take the distance to the middle", "distance line highlighted"), ("cut it with step at point three", "step line highlighted"),
     ("Closer than that is zero", "read-out 0 inside"), ("farther is one", "read-out 1 outside"), ("The result is a circle", "ring round the disk's edge")],
    "manim: the cone cut at 0.3",
    "Predict-then-reveal on the real disk beside two lines of code; the 0 and 1 read-outs name each side.",
    "C11: Lab square render of lab-shaders/10-disk.gdshader, still. Verified (360x360 Lab): middle 0; d = 0.2 -> 0; d = 0.4 -> 1; corner 1; the disk spans 0.6 of the width (216 of 360 px).",
    "Lab C11 (10-disk); dense-compare: sq_10_disk (max difference 0 levels)", title="Build a Ring",
    readouts=[{"at": AW("B35", "Closer than that is zero"), "text": "0", "x": sq(0.5, 0.5)[0], "y": sq(0.5, 0.5)[1]},
              {"at": AW("B35", "farther is one"), "text": "1", "x": sq(0.9, 0.12)[0], "y": sq(0.9, 0.12)[1]}],
    rings=[{"at": AW("B35", "The result is a circle"), "box": [sq(0.2, 0.2)[0], 0.2, sq(0.8, 0.8)[0], 0.8]}])

c = code_of("11-disk-flip.gdshader")
lab("B36", 4, "swap the arguments: the disk flips", "11-disk-flip.gdshader", f"{OUT}/disk-flip.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B36", "Swap the two inputs", c, "step(d"), cue("B36", "The edge always comes first", c, "step(d", "edge first")],
    "Code card at left (the six-line shader with the arguments swapped); at right a real Godot window with a square picture: a white disk on black. Read-outs '1' inside and '0' outside.",
    "The swapped step line is highlighted; the disk is now white inside; read-outs name the two sides.",
    [("Swap the two inputs", "step line highlighted"), ("one inside", "read-out 1 inside"), ("zero outside", "read-out 0 outside"),
     ("The edge always comes first", "label 'edge first' on the step line")],
    "manim: the two argument orders side by side",
    "The flip is visible in the real render; the code line with the swapped arguments is highlighted.",
    "C12: Lab square render of lab-shaders/11-disk-flip.gdshader, still. Verified (360x360 Lab): middle 1; d = 0.2 -> 1; d = 0.4 -> 0; corner 0. Edge case: step(0.3, 0.3) and step(0.3, 0.3) swapped are both 1 "
    "(function-tables: step_args_swapped).",
    "Lab C12 (11-disk-flip); function-tables: disk_step_flipped",
    readouts=[{"at": AW("B36", "one inside"), "text": "1", "x": sq(0.5, 0.5)[0], "y": sq(0.5, 0.5)[1]},
              {"at": AW("B36", "zero outside"), "text": "0", "x": sq(0.9, 0.12)[0], "y": sq(0.9, 0.12)[1]}])

manim("B37", 4, "two steps, subtracted: a pulse", "TwoCuts",
      "The standard plot with the input as the distance d from 0 to 0.7 (axis label 'distance'). Curve A: step(0.3, d) in light grey; curve B: step(0.38, d) in mid grey; then the "
      "bold curve A − B: a pulse of height 1 between d = 0.3 and 0.38. Mono tag 'ring = step(0.3, d) − step(0.38, d)'. Strip beneath: a bright band in the middle.",
      "Curve A rises at 0.3, curve B rises at 0.38, and their difference is a one-wide pulse that lights a band on the strip.",
      [(0.0, "axes with 'distance', tag"), ("Step at point three is one", "curve A draws (done by 0.26)"), (0.38, "curve B draws (done by 0.45)"),
       (0.5, "midpoint hold: curves A and B settled, the difference not yet drawn"), (0.66, "the bold pulse A − B draws; the strip band lit (done by 0.80)"),
       ("a pulse", "dot rides the pulse")],
      "ShaderLab ring render",
      "A one-dimensional cut through the ring (two steps and their difference) is the cleanest picture of 'cut twice and subtract'.",
      "function-tables: ring_profile (0, 1, 1, 0, 0 at d = 0.2, 0.3, 0.34, 0.38, 0.45); dense-compare: ring_profile_hard (max difference 0 levels)")

c = code_of("12-ring-hard.gdshader")
lab("B38", 4, "step minus step: the hard ring, a mask", "12-ring-hard.gdshader", f"{OUT}/ring-hard.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B38", "In code, that is step minus step", c, "float ring"), cue("B38", "Here is the ring", c, "COLOR =")],
    "Code card at left (the seven-line shader); at right a real Godot window with a square picture: a white ring on black with hard edges. Read-outs '1' on the ring and '0' in the middle; a "
    "terracotta ring (grey-backed) round a piece of the hard outer edge at the end.",
    "The ring line is highlighted; read-outs name the mask's one and zero; the ring marks a hard edge.",
    [("In code, that is step minus step", "ring line highlighted"), ("one on the ring", "read-out 1 on the ring"), ("zero everywhere else", "read-out 0 in the middle"),
     ("The edges are hard", "ring round a piece of the edge")],
    "manim: the pulse spun around the middle",
    "The real hard ring beside 'step minus step'; the mask is named right where it is visible.",
    "C13: Lab square render of lab-shaders/12-ring-hard.gdshader, still. Verified (360x360 Lab): d = 0.2 -> 0; 0.34 -> 1; 0.45 -> 0.",
    "Lab C13 (12-ring-hard); function-tables: ring_profile; dense-compare: sq_12_ring_hard (max difference 0 levels)",
    readouts=[{"at": AW("B38", "one on the ring"), "text": "1", "x": sq(0.84, 0.5)[0], "y": sq(0.84, 0.5)[1]},
              {"at": AW("B38", "zero everywhere else"), "text": "0", "x": sq(0.5, 0.5)[0], "y": sq(0.5, 0.5)[1]}],
    rings=[{"at": AW("B38", "The edges are hard"), "box": [sq(0.8, 0.45)[0], 0.4, sq(0.92, 0.55)[0], 0.6]}])

c = code_of("13-ring-color.gdshader")
lab("B39", 4, "mix colours with the ring as the weight", "13-ring-color.gdshader", f"{OUT}/ring-color.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B39", "Now color it with mix", c, "mix(cream"), cue("B39", "you get cream", c, "vec3 cream"), cue("B39", "you get teal", c, "vec3 teal")],
    "Code card at left (the nine-line shader); at right a real Godot window with a square picture: a teal ring on a cream background. Labels 'cream' on the background and 'teal' on the ring.",
    "The mix line, then the cream line, then the teal line are highlighted as the voice names them; the two labels land on the picture.",
    [("Now color it with mix", "mix line highlighted"), ("you get cream", "cream line highlighted; label 'cream' on the background"),
     ("you get teal", "teal line highlighted; label 'teal' on the ring"), ("The mask decides", "both labels visible")],
    "manim: a mix dial",
    "Real colours at last: the mask decides cream or teal; the picture is the evidence.",
    "C14: Lab square render of lab-shaders/13-ring-color.gdshader, still. Verified (360x360 Lab): d = 0.2 -> cream (0.9804, 0.9608, 0.9216); 0.34 -> teal (0.3686, 0.6392, 0.5686); 0.45 -> cream.",
    "Lab C14 (13-ring-color); dense-compare: sq_13_ring_color (max difference 0 levels)",
    readouts=[{"at": AW("B39", "you get cream"), "text": "cream", "x": sq(0.1, 0.12)[0], "y": sq(0.1, 0.12)[1]},
              {"at": AW("B39", "you get teal"), "text": "teal", "x": sq(0.5, 0.06)[0], "y": sq(0.5, 0.06)[1]}])

c = code_of("14-ring-soft.gdshader")
lab("B40", 4, "smoothstep for both edges: the soft ring", "14-ring-soft.gdshader", f"{OUT}/ring-soft.png", "Godot 4.7.2 · Forward+ · a square shape",
    [cue("B40", "Swap each step for a smooth step", c, ["float inner", "float outer"]), cue("B40", "The same ring", c, "mix(cream")],
    "Code card at left (the ten-line shader); at right a real Godot window with a square picture: the same teal ring on cream, now with soft edges. A read-out 'soft' beside the outer edge; a "
    "terracotta ring (grey-backed) round the fading inner edge at the end.",
    "The two smoothstep lines are highlighted, then the mix line; the read-out and ring mark the soft edge.",
    [("Swap each step for a smooth step", "inner and outer lines highlighted"), ("Each edge now has a width", "read-out 'soft' at the outer edge"),
     ("fades in and fades out", "ring round the fading inner edge"), ("The same ring", "mix line highlighted")],
    "ShaderLab hard and soft ring side by side",
    "Replacing the two steps by smoothsteps and seeing the soft edge on the real render shows what each function adds.",
    "C15: Lab square render of lab-shaders/14-ring-soft.gdshader, still. Verified (360x360 Lab): d = 0.2 -> cream; 0.28 -> (0.6941, 0.8118, 0.7569) (half way); 0.34 -> teal; 0.40 -> (0.6431, 0.7843, 0.7255); 0.45 -> cream.",
    "Lab C15 (14-ring-soft); dense-compare: sq_14_ring_soft (max difference 1 level)",
    readouts=[{"at": AW("B40", "Each edge now has a width"), "text": "soft", "x": sq(0.95, 0.5)[0], "y": sq(0.95, 0.5)[1]}],
    rings=[{"at": AW("B40", "fades in and fades out"), "box": [sq(0.72, 0.42)[0], 0.38, sq(0.8, 0.58)[0], 0.62]}])

c = code_of("15-ring-final.gdshader")
lab("B41", 4, "the finished shader; the radius is a uniform dial", "15-ring-final.gdshader", f"{OUT}/ring-dial.mp4", "Godot 4.7.2 · Forward+ · radius swept by script",
    [cue("B41", "Distance makes the ramp", c, "float d"), cue("B41", "smooth step shapes it twice", c, ["float inner", "float outer"]),
     cue("B41", "mix paints it", c, "mix(cream"), cue("B41", "The radius is a uniform", c, "uniform float radius")],
    "Code card at left (the twelve-line finished shader); at right a real Godot window with the soft teal ring from B40 that first holds still, then shrinks and grows as the radius dial is swept. "
    "Each highlighted line is named by the voice.",
    "Each function's line lights up as it is named; then the ring grows as the radius is turned.",
    [("Here is the finished shader", "full shader visible, ring at rest"), ("Distance makes the ramp", "distance line highlighted"), ("smooth step shapes it twice", "the two smoothstep lines highlighted"),
     ("mix paints it", "mix line highlighted"), ("The radius is a uniform", "uniform line highlighted"), ("and the ring grows", "the ring grows (the capture holds 0.3 until 6 s)")],
    "LectureCodeTrace alone",
    "The finished shader, each function highlighted as it is named, beside the ring growing as the radius dial turns, closes the loop with the film's first image.",
    "C16: Lab square render of lab-shaders/15-ring-final.gdshader; radius held at 0.30 until 6.0 s, then 0.30 -> 0.12 over 6.0-8.5 s, then 0.12 -> 0.38 over 8.5-11.5 s, held to 12.5 s; 30 fps, Forward+. "
    "Verified (360x360 Lab): radius 0.12 -> cream / teal / cream at d = 0.06 / 0.16 / 0.32 ... see lab-summary.txt; radius 0.3 -> teal at d = 0.34; radius 0.38 -> teal at d = 0.42.",
    "Lab C16 (15-ring-final); dense-compare: sq_15_ring_final_r0.1 / r0.3 / r0.38 (max difference 0 to 1 level)")

# ───────────────────────────── self-check: the midpoint rule (the 45 to 55 % frame is a settled still) ─────────────────────────────
def check_windows():
    problems = []
    for e in E:
        bid, L = e["bid"], e["entry"]
        if L["lane"] == "manim":
            holds = [c for c in L["show"] if "midpoint hold" in c["event"]]
            if len(holds) != 1:
                problems.append(f"{bid}: a Manim beat needs exactly one 'midpoint hold' event, has {len(holds)}")
            for c in L["show"]:
                if "midpoint hold" not in c["event"] and 0.45 <= c["at"] <= 0.55:
                    problems.append(f"{bid}: motion event at {c['at']} starts inside 45 to 55 %: {c['event'][:50]}")
        else:
            p = L.get("props", {})
            times = [("cue", c["at"] if isinstance(c, dict) else c) for c in (p.get("cues") or [])]
            times += [("readout", r["at"]) for r in p.get("readouts", [])] + [("ring", r["at"]) for r in p.get("rings", [])]
            times += [("move", m["at"]) for m in p.get("moves", [])]
            if p.get("ramp"):
                times.append(("ramp", p["ramp"]["at"]))
            for kind, t in times:
                if 0.45 <= t <= 0.55:
                    problems.append(f"{bid}: {kind} at {t} starts inside 45 to 55 %")
            for c in (p.get("cues") or []):
                if isinstance(c, dict) and len(c.get("label", "")) > 60:
                    problems.append(f"{bid}: a cue label is {len(c['label'])} characters (COMPONENT-SPECS allows 60): {c['label']}")
            if len(p.get("caption", "")) > 80:
                problems.append(f"{bid}: the caption is {len(p['caption'])} characters (COMPONENT-SPECS allows 80)")
            for r in p.get("readouts", []):
                if len(r["text"].split()) > 3:
                    problems.append(f"{bid}: a read-out has more than three words: {r['text']}")
    assert not problems, "\n".join(problems)


check_windows()

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for old in (HERE / "lanes").glob("act*.json"):
    old.unlink()
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
sl = ["# Shot list: The Shader Math Toolkit\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab capture of a tested file in `lab-shaders/`; every curve drawn in Manim is the same formula the shader computes "
      "(`evidence/planning-checks/plot_data.py`, compared pixel for pixel with Godot's renders in `dense-compare.md`).\n",
      "## The standard plot (defined once; B04 teaches it, every later plot reuses it)\n",
      "Square axes about 4.4 Manim units wide on the cream stage; `input` along the bottom with the ticks 0 and 1, `output` up the side with 0 and 1 (or the range the beat needs); the curve in "
      "ink-grey stroke; a terracotta dot travelling the curve; a thin dashed drop line from the dot to the **ramp strip** under the axes, at the same x scale; the strip drawn "
      "as a row of 64 narrow tiles with thin cream gaps in true grays (value v drawn as gray v: 0 black, 1 white; each tile is taller than wide, so GATE T cannot read a run of mid-dark tiles as one text blob; if it still does, fall back to a lifted scale, gray 0.50 + 0.50 v, and say so in BUILD-LOG), end labels 0 and 1; the formula in mono at least 32 on "
      "the top right. Terracotta only as the dot and as grey-backed rings; never as text. Midpoint rule: the 45 to 55 % frame is a settled still with its labels.\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (shared; spec `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file): `plot`, `ramp_strip`, `ramp_marker`, `uv_square`. "
      "This film also needs, if the shared kit does not have them, a `plot_with_strip` (the standard plot above), a `number_line`, a `vec_arrow` and a `chip` (function-name chip); write them in `_kit_extra.py` "
      "beside the film and say so in `BUILD-LOG.md`. 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file): this film uses only `--animate` sequences on one uniform and still PNGs "
      "(no scene scripts, no key events). 4. **Docs screenshot D1** for B12 via Playwright (`CAPTURE-PLAN.md`). 5. **No editor frames** are needed. The curves' numpy formulas are in "
      "`evidence/planning-checks/plot_data.py`.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)

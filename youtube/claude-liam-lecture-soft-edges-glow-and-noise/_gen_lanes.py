#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md.

Why a generator: the code shown on screen must be the tested file text (never retyped), and the shot list must say exactly what the lanes say.
Re-run after any edit:   python3 _gen_lanes.py && python3 make_sheet.py
Geometry used for readouts and rings (fractions of the capture frame): the square target is 0.8 of the frame height, centred, so
a point (u, v) of the shader's UV square sits at frame x = 0.275 + 0.45 u, y = 0.1 + 0.8 v.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
PUB = "soft-edges-glow-and-noise"          # folder under TK/runtime/remotion/public/ for this film's captures
E = []


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def ln(fn, *snips):
    """1-based line numbers of the first line that contains each snippet (so cues follow the real file)."""
    lines = code_of(fn).split("\n")
    out = []
    for s in snips:
        hit = [i + 1 for i, l in enumerate(lines) if s in l]
        assert hit, f"{fn}: no line contains {s!r}"
        out.append(hit[0])
    return out


def fx(u):
    return round(0.275 + 0.45 * u, 3)


def fy(v):
    return round(0.1 + 0.8 * v, 3)


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, lane="capture", caption="", nocode=False):
    props = {"layout": layout, "code": code_of(shader) if (shader and not nocode) else "", "codeFile": f"lab-shaders/{shader}" if shader else "",
             "cues": cues, "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    add(bid, act, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": "remotion", "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def V(name):
    return f"{PUB}/{name}"


# ═════════════════════════ ACT I · From Cut to Ramp ═════════════════════════
lab("B01", 0, "one circle, hard edge then soft edge: one function changed", "02-soft-disc.gdshader", V("c01-hook.mp4"),
    "Godot 4.7.2 · same circle, shader swapped at 6 s · scripted", [],
    "Act title 'From Cut to Ramp' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a teal disc with a razor-sharp edge sits still, then at the swap the same disc keeps its size and colour but its edge fades softly into the grey stage. Labels 'hard edge' then 'soft edge'.",
    "The sharp rim melts into a fade the moment the shader is swapped, with nothing else changing.",
    [{"at": 0.05, "event": "hard disc, label 'hard edge'"}, {"at": 0.6, "event": "shader swapped: the rim fades, label 'soft edge'"}],
    "manim drawing of a sharp and a soft circle", "A real render is the honest picture of 'nothing was blurred, one function changed'; a drawing would only claim it.",
    "C01: square target (ColorRect 576 x 576 logical px centred on the 1280 x 720 canvas), lab-shaders/01-hard-disc.gdshader from 0 s, material swapped to lab-shaders/02-soft-disc.gdshader at 6.0 s (`--material-at 6.0`), 10 s, 30 fps, Forward+, stage #D9D5CA, no input. Verified: 01 draws exactly two colors in a 256 px render; 02 has 16,780 in-between pixels of 65,536.",
    "C01 · Lab 01-hard-disc and 02-soft-disc (lab-analysis.txt)", layout="video", title="From Cut to Ramp",
    readouts=[{"at": 0.1, "text": "hard edge", "x": 0.5, "y": 0.95}, {"at": 0.7, "text": "soft edge", "x": 0.5, "y": 0.95}])

manim("B02", 0, "step: zero below the line, one from the line up", "StepPlot",
      "Axes on the cream stage: horizontal x from 0 to 1, vertical result 0 to 1. A grey dashed vertical line at the edge 0.4, labelled 'edge'. A terracotta dot slides along the bottom at height 0 from the left; when it crosses the line it jumps up to height 1 and runs on along the top, leaving a cliff-shaped curve behind it. Beneath the axes the GLOSSARY wording: 'step(edge, x): 0 below the edge, 1 from the edge up'.",
      "The dot slides along zero, jumps to one at the line, and the curve behind it is a cliff.",
      [{"at": 0.1, "event": "axes and the line a"}, {"at": 0.3, "event": "dot slides along zero"}, {"at": 0.62, "event": "dot jumps to one; cliff curve drawn"}, {"at": 0.8, "event": "rule label"}],
      "LectureCodeTrace on the docs line 'b < a ? 0.0 : 1.0'", "A jump from zero to one is a motion; the code line would only state it.",
      "Godot 4.7 docs, built-in functions: step = 'b < a ? 0.0 : 1.0' (FACTCHECK 3, 4)")

lab("B03", 0, "a circle is a distance test; one minus a step on the distance", "01-hard-disc.gdshader", V("c02-hard-disc.png"),
    "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.12, "lines": ln("01-hard-disc.gdshader", "distance(UV"), "label": "distance(a, b): how far apart two points are"},
     {"at": 0.62, "lines": ln("01-hard-disc.gdshader", "step(0.4"), "label": "step(edge, x): 0 below the edge, 1 from the edge up"}],
    "Code card at left (the hard-disc shader); at right a real Godot window with the teal disc and its razor-sharp edge. A terracotta ring settles on the right-hand part of the rim. A label on each highlighted line defines distance and step (GLOSSARY wording).",
    "The distance line is highlighted, then the step line; the ring lands on the rim as 'inside / outside' is said.",
    [{"at": 0.12, "event": "distance line + definition label"}, {"at": 0.62, "event": "step line + definition label; ring on the rim"}],
    "manim rings of equal distance around the middle", "The code and its exact result side by side is the claim; the rings picture would not show the real edge.",
    "C02: the same square target, lab-shaders/01-hard-disc.gdshader, still PNG at 3840 x 2160, Forward+. Verified in the 256 px Lab render: the pixel at UV x 0.8965 is body (alpha 1.0), the pixel at 0.9043 is stage (alpha 0.0).",
    "Lab 01-hard-disc (alpha 1.0 / 0.0 across the cliff)",
    rings=[{"at": 0.7, "box": [fx(0.88), fy(0.38), fx(0.97), fy(0.62)]}])

manim("B04", 0, "a hard edge is a staircase: every pixel is all color or none", "Staircase",
      "A 10-by-7 block of big outline cells cut from the REAL hard-disc render (data in evidence/planning-checks/staircase-cells.txt: columns 196 to 205, rows 51 to 57): cells that are teal in the render are filled teal and labelled 1, empty ones are stage grey and labelled 0. A terracotta outline walks along the boundary one step at a time. Caption: 'no in-between values'.",
      "The outline climbs the staircase one square step at a time along the real boundary.",
      [{"at": 0.1, "event": "the block of cells from the real render"}, {"at": 0.35, "event": "outline starts walking the boundary"}, {"at": 0.7, "event": "caption 'no in-between values'"}],
      "ShaderLab zoom of the hard-disc capture", "Cells with real 1 and 0 values show 'each pixel is all or none' better than a blurry magnified crop.",
      "evidence/planning-checks/staircase-cells.txt (from png/01-hard-disc.png; 2 distinct colors in the whole picture)")

manim("B05", 0, "smoothstep: two lines and a smooth climb between them", "TwoLines",
      "Axes: horizontal x from 0 to 0.5, vertical result 0 to 1. Two grey dashed vertical lines at a = 0.25 and b = 0.4, labelled 'a' and 'b'. A terracotta dot rides along the x axis; the curve behind it is flat at 0, S-shaped between the two lines, then flat at 1. Rule label under the plot in two lines, in the GLOSSARY wording (the two edges are the dashed lines a and b): 'smoothstep(a, b, x): a switch that eases in and out between two edges:' then '0 below a, 1 above b, a smooth S between'.",
      "The dot rides along and the curve it leaves is flat, then an S, then flat again.",
      [{"at": 0.1, "event": "axes with lines a and b"}, {"at": 0.3, "event": "dot rides; flat part drawn"}, {"at": 0.6, "event": "S-shaped climb between a and b"}, {"at": 0.82, "event": "rule label"}],
      "ShaderLab ramp strip", "A curve that bends between two lines is a plot; the dot makes 'slow, fast, slow' visible as speed.",
      "Godot 4.7 docs, smoothstep (FACTCHECK 9, 10, 11)")

manim("B06", 0, "the S-curve is not a line: 0.1 along reads 0.028", "SCurveNumber",
      "The same plot in unit form: t (labelled 'how far along the band, 0 to 1') from 0 to 1, a grey dashed diagonal (the straight ramp) and the terracotta S-curve. At t = 0.1 a vertical marker with two dots: the straight ramp at 0.1 and the curve at 0.028, a bracket between them. At t = 0.5 the dots coincide at 0.5. Typeset at top right: 3t^2 - 2t^3 (real MathTex, per docs/MATH-TYPESETTING.md) and under it, in monospace and labelled as code, t * t * (3.0 - 2.0 * t).",
      "The marker lands at ten percent and the two dots split: 0.1 on the line, 0.028 on the curve.",
      [{"at": 0.1, "event": "diagonal and S-curve"}, {"at": 0.3, "event": "marker at t = 0.1, dots 0.1 and 0.028, bracket"}, {"at": 0.62, "event": "marker moves to t = 0.5: dots coincide"}, {"at": 0.8, "event": "typeset formula and code form"}],
      "LectureEvidenceTable of t, line, curve", "The gap between a line and a curve at one marked spot is a picture; a table lists numbers without showing the gap.",
      "Computed t*t*(3-2t) at 0.1, 0.5 and the Lab render at t = 0.1004: body 0.966 against the formula 0.972 (lab-analysis.txt)")

lab("B07", 0, "smoothstep on the distance: a soft edge with a band", "02-soft-disc.gdshader", V("c03-soft-disc.png"),
    "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.12, "lines": ln("02-soft-disc.gdshader", "smoothstep(0.25")}, {"at": 0.62, "lines": ln("02-soft-disc.gdshader", "COLOR")}],
    "Code card at left (the soft-disc shader, one line changed from the hard disc); at right the real render: the teal disc whose edge fades over a band. A terracotta ring on the band at the right side, small labels '0.25' and '0.4' at the band's two ends.",
    "The smoothstep line is highlighted and the ring settles on the fading band.",
    [{"at": 0.12, "event": "smoothstep line highlighted"}, {"at": 0.62, "event": "ring on the band; '0.25' and '0.4' labels"}],
    "manim", "The real picture of the band, next to the one line that makes it, is the claim.",
    "C03: the square target, lab-shaders/02-soft-disc.gdshader, still PNG 3840 x 2160. Verified in the 256 px render: body alpha 0.966 / 0.496 / 0.026 at t = 0.100 / 0.500 / 0.900 (formula 0.972 / 0.500 / 0.028); every pixel within 0.008 of the formula.",
    "Lab 02-soft-disc and 02-soft-disc-t (lab-analysis.txt)",
    readouts=[{"at": 0.62, "text": "0.25", "x": fx(0.75), "y": fy(0.62)}, {"at": 0.62, "text": "0.4", "x": fx(0.9), "y": fy(0.62)}],
    rings=[{"at": 0.62, "box": [fx(0.74), fy(0.4), fx(0.92), fy(0.6)]}],
    caption="band: the strip of pixels near the edge, between the two radii")

lab("B08", 0, "the softness dial: crisp to cloud", "03-soft-width.gdshader", V("c04-softness-sweep.mp4"),
    "Godot 4.7.2 · Forward+ · softness swept by script",
    [{"at": 0.1, "lines": ln("03-soft-width.gdshader", "uniform float softness")}, {"at": 0.34, "lines": ln("03-soft-width.gdshader", "smoothstep(0.4 - width")}],
    "Code card at left (the soft-width shader); at right a real Godot window whose disc starts with a crisp rim and, as softness is swept up, spreads into a cloud while the outer edge stays put. Labels 'crisp' then 'cloud'.",
    "The fade widens inward from the same outer edge as the dial climbs.",
    [{"at": 0.1, "event": "uniform line highlighted"}, {"at": 0.34, "event": "smoothstep line; sweep under way"}, {"at": 0.7, "event": "label 'cloud'"}],
    "manim", "A dial moving a real picture is the claim: the inner edge travels, the outer one does not.",
    "C04: the square target, lab-shaders/03-soft-width.gdshader, softness 0.02 held 1 s, swept to 0.4 by 7 s, held (`--animate softness:0:0.02,1:0.02,7:0.4`); 12 s, 30 fps, Forward+. Verified stills: softness 0.05 gives 6,448 in-between pixels, 0.15 gives 16,780, 0.4 gives 27,400; outer edge unchanged.",
    "Lab 03-soft-width-0.05 / 0.15 / 0.4",
    readouts=[{"at": 0.12, "text": "crisp", "x": 0.5, "y": 0.95}, {"at": 0.7, "text": "cloud", "x": 0.5, "y": 0.95}])

manim("B09", 0, "squeeze the band: smoothstep becomes step; equal lines are undefined", "BandsMeet",
      "The S-curve plot with its two lines a and b. The lines slide together; the S-curve steepens into a vertical cliff, a step, at the moment they touch. At the touch a label 'a = b: undefined (docs)' and, in grey, 'this Mac: a hard cut' with the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ and Compatibility'. Then a code chip slides in beside it: max(softness, 0.01), with the label 'max(a, b): the larger of two values'.",
      "The two dashed lines slide together and the smooth curve collapses into a cliff.",
      [{"at": 0.1, "event": "S-curve with lines a and b"}, {"at": 0.35, "event": "lines slide together; curve steepens"}, {"at": 0.68, "event": "cliff; label 'a = b: undefined (docs)'"}, {"at": 0.85, "event": "chip: max(softness, 0.01)"}],
      "BrowserCapture of the docs sentence 'Results are undefined if a >= b.'", "The collapse of the S into a cliff is the picture of 'step is smoothstep with no band'; the docs sentence goes on the screen as the label.",
      "Docs: 'Results are undefined if a >= b.'; Lab ev-equal-edges: a hard cut in both renderers; extra_checks H: a hint range does not clamp (FACTCHECK 17, 18, 19, 20)")

manim("B10", 0, "swapped lines flip the ramp; undefined in the docs; write one minus smoothstep", "SwappedLines",
      "The smooth-curve plot with lines a = 0.25 and b = 0.4. The two lines swap places (b now left of a) and the S-curve flips to fall from one to zero. Label 'smoothstep(0.4, 0.25, x): flipped on this Mac, undefined in the docs' with the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ and Compatibility'. Then, beneath the same flipped curve, the safe form slides in: '1.0 - smoothstep(0.25, 0.4, x)'.",
      "The curve flips when the lines swap, then the safe one-minus form draws the very same curve.",
      [{"at": 0.1, "event": "S-curve and lines"}, {"at": 0.36, "event": "lines swap; curve flips"}, {"at": 0.7, "event": "safe form slides in under the flipped curve"}],
      "ShaderLab render of the swapped shader", "Two curves that overlap exactly show that the safe form is the same picture; a render would hide the argument order.",
      "Lab ev-reversed-edges: a flipped S in both renderers, alpha 0.958 / 0.487 / 0.017 at the same pixels as 1 - smoothstep (FACTCHECK 21)")

# ═════════════════════════ ACT II · Falloff and Highlight ═════════════════════════
manim("B11", 1, "falloff: one minus the distance", "Falloff",
      "Act title 'Falloff and Highlight' (serif 40) top-left. An 11-by-11 pixel grid of outline cells with a terracotta spot on the cell left of centre. Concentric distance rings expand from the spot; each cell fills teal in proportion to 1 minus its distance, with its number written on one row: 1.0, 0.8, 0.6, 0.4, 0.2, 0.0. At right a profile: value against distance, a straight line falling from 1 to 0 at distance 1. Label 'falloff: how quickly a value fades with distance'.",
      "The rings spread from the spot and the cells behind them fill less and less, down to zero at distance one.",
      [{"at": 0.1, "event": "grid and spot, act title"}, {"at": 0.35, "event": "rings expand; cells fill with their numbers"}, {"at": 0.7, "event": "profile line and the falloff label"}],
      "ShaderLab render of the spot", "Numbers falling cell by cell as the rings spread is the definition of a falloff; the render comes next as proof.",
      "Arithmetic 1 - d; Lab 04-spot: alpha 1.000 / 0.895 / 0.796 / 0.700 at d = 0 / 0.1 / 0.2 / 0.3 (FACTCHECK 24)")

lab("B12", 1, "the spot as paint: it does not stop at the picture's edge", "04-spot.gdshader", V("c05-spot.png"),
    "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.12, "lines": ln("04-spot.gdshader", "float spot")}, {"at": 0.62, "lines": ln("04-spot.gdshader", "COLOR")}],
    "Code card at left (four lines); at right the real render: a teal haze thickest at the spot near the upper left and still clearly teal at the right edge and the bottom of the picture, where it ends in a hard straight cut. A terracotta ring on the right edge with the label 'still 0.35'.",
    "The haze spreads from the spot to the picture's edge, and the ring marks the cut.",
    [{"at": 0.12, "event": "spot line highlighted"}, {"at": 0.62, "event": "ring on the right edge: 'still 0.35'"}],
    "LectureCodeTrace alone", "The cut at the picture's edge is only visible in the real render, and it is the whole point of the beat.",
    "C05: the square target, lab-shaders/04-spot.gdshader, still PNG 3840 x 2160. Verified in the 256 px render: alpha 0.351 at the right edge on the spot's row (formula 0.352), 0.082 at the far corner (0.084).",
    "Lab 04-spot (lab-analysis.txt)",
    readouts=[{"at": 0.62, "text": "still 0.35", "x": fx(0.9), "y": fy(0.2)}], rings=[{"at": 0.62, "box": [fx(0.9), fy(0.22), fx(1.0), fy(0.5)]}])

manim("B13", 1, "pow: numbers between zero and one shrink", "PowerCurves",
      "Axes 0 to 1. Three curves drawn in turn: the straight line x^1, then x^3, then x^6, each labelled at its end. A vertical guide at x = 0.7 with a dot landing on each curve: 0.7, 0.343, 0.118. Label 'pow(x, p): x raised to the power p'.",
      "Each curve sags further below the straight line, and the dots on the guide drop: 0.7, 0.343, 0.118.",
      [{"at": 0.1, "event": "axes and the straight line"}, {"at": 0.3, "event": "x^3 curve; dot 0.343"}, {"at": 0.58, "event": "x^6 curve; dot 0.118"}, {"at": 0.82, "event": "pow label"}],
      "ShaderLab power sweep", "Curves that sag further as the power climbs, with one input landing at three outputs, show 'raise to a power' as a function.",
      "0.7^3 = 0.343 and 0.7^6 = 0.1176; Lab 05-spot-power (FACTCHECK 26)")

lab("B14", 1, "the power dial shrinks the spot; the clamp keeps the base non-negative", "05-spot-power.gdshader", V("c06-power-sweep.mp4"),
    "Godot 4.7.2 · Forward+ · power swept by script",
    [{"at": 0.1, "lines": ln("05-spot-power.gdshader", "uniform float power")}, {"at": 0.3, "lines": ln("05-spot-power.gdshader", "pow(spot, power)")},
     {"at": 0.62, "lines": ln("05-spot-power.gdshader", "clamp(1.0"), "label": "clamp(x, lo, hi): keep x between lo and hi"}],
    "Code card at left (the power shader); at right a real Godot window whose teal spot shrinks from a broad haze to a pinpoint as power sweeps from 1 to 8. Labels 'power 1', 'power 3', 'power 8' as the values pass; the clamp line is highlighted with its one-line definition at the end.",
    "The spot contracts as the power climbs; the clamp line lights up last.",
    [{"at": 0.1, "event": "power 1: haze"}, {"at": 0.3, "event": "power 3: soft highlight"}, {"at": 0.62, "event": "power 8: pinpoint; clamp line + definition"}],
    "manim", "A dial moving a real picture is the claim, with the numbers named as they pass.",
    "C06: the square target, lab-shaders/05-spot-power.gdshader, power 1 held 1.5 s, swept to 8 by 8.5 s, held (`--animate power:0:1,1.5:1,8.5:8`); 14 s, 30 fps, Forward+. Verified stills: alpha 0.895 / 0.722 / 0.422 at 0.1 from the spot for power 1 / 3 / 8.",
    "Lab 05-spot-power-1 / 3 / 8; ev-pow-negative (NaN for a fractional power)",
    readouts=[{"at": 0.1, "text": "power 1", "x": 0.5, "y": 0.95}, {"at": 0.3, "text": "power 3", "x": 0.5, "y": 0.95}, {"at": 0.62, "text": "power 8", "x": 0.5, "y": 0.95}])

lab("B15", 1, "multiply the falloff by the disc so it stays on the bubble", "06-spot-in-disc.gdshader", V("c07-spot-in-disc.mp4"),
    "Godot 4.7.2 · Forward+ · shader swapped at 3 s · scripted",
    [{"at": 0.12, "lines": ln("06-spot-in-disc.gdshader", "float disc")}, {"at": 0.62, "lines": ln("06-spot-in-disc.gdshader", "COLOR")}],
    "Code card at left (the spot-in-disc shader); at right a real Godot window: first the teal spot with its faint tail running past where the bubble will be, then at the swap the tail beyond the disc vanishes and the highlight is confined to the disc. A terracotta ring on the tail beyond the disc with readouts '0.09' then '0'.",
    "The tail outside the disc disappears the moment the shader is swapped.",
    [{"at": 0.1, "event": "unmasked spot with its tail"}, {"at": 0.62, "event": "swap: tail gone; ring reads 0.09 then 0"}],
    "manim mask product", "The real before and after, with the same pixel reading 0.09 then 0, is the proof that multiplying cuts.",
    "C07: the square target, lab-shaders/05-spot-power.gdshader (power 3) from 0 s, swapped to lab-shaders/06-spot-in-disc.gdshader at 3.0 s (`--material-at 3.0`), 8 s, 30 fps, Forward+. Verified: at the pixel (230, 89) the alpha is 0.090 before and 0.000 after (formulas 0.091 and 0).",
    "Lab 05-spot-power-3 and 06-spot-in-disc (lab-analysis.txt)",
    readouts=[{"at": 0.3, "text": "0.09", "x": fx(0.9), "y": fy(0.2)}, {"at": 0.7, "text": "0", "x": fx(0.9), "y": fy(0.2)}],
    rings=[{"at": 0.3, "box": [fx(0.82), fy(0.25), fx(0.97), fy(0.45)]}])

lab("B16", 1, "the spot's centre is a vec2 uniform: slide it", "07-spot-moves.gdshader", V("c08-spot-orbit.mp4"),
    "Godot 4.7.2 · Forward+ · spot_center moved by script",
    [{"at": 0.1, "lines": ln("07-spot-moves.gdshader", "uniform vec2")}, {"at": 0.34, "lines": ln("07-spot-moves.gdshader", "spot_center)")}],
    "Code card at left (the spot-moves shader); at right a real Godot window where the highlight travels once around inside the disc. A small terracotta dot marks spot_center's position on the render.",
    "The highlight circles inside the disc while the highlighted line says where it comes from.",
    [{"at": 0.1, "event": "vec2 uniform line highlighted"}, {"at": 0.34, "event": "spot line highlighted; highlight starts to travel"}, {"at": 0.7, "event": "highlight on its way round"}],
    "manim", "A real highlight following a dial is the claim: 'you decide where the light comes from'.",
    "C08: the square target, lab-shaders/07-spot-moves.gdshader, spot_center driven by a scene script (`--scene`) along a circle of radius 0.18 around (0.5, 0.5), one turn in 6 s starting at the upper left, 9 s, 30 fps, Forward+. Verified stills: spot_center (0.35, 0.35) and (0.65, 0.4) match the formula within 0.008 on all pixels.",
    "Lab 07-spot-moves-a / b (lab-analysis.txt)")

# ═════════════════════════ ACT III · Layering ═════════════════════════
manim("B17", 2, "a layer is a color plus a mask; two layers make a bubble", "Layers",
      "Act title 'Layering' (serif 40) top-left. Two sheets slide in over the stage: a teal disc sheet labelled 'body · mask: the disc' and a pale highlight sheet labelled 'highlight · mask: the spot'. They slide together into one bubble (a teal disc with a pale highlight) that settles where they met.",
      "The two sheets slide together and settle into one bubble.",
      [{"at": 0.1, "event": "teal sheet, act title"}, {"at": 0.35, "event": "pale highlight sheet slides in"}, {"at": 0.65, "event": "the sheets merge into a bubble"}],
      "isometric stack of two sheets (show-tell)", "Two things becoming one is the idea of layering; a flat slide-together keeps the cast (disc, spot) the viewer already knows.",
      "Construction of lab-shaders/08-bubble.gdshader (FACTCHECK 31, 36)")

manim("B18", 2, "multiply keeps both, add shows either", "MultiplyAdd",
      "Two overlapping discs A (teal outline) and B (pale outline) with four sample points: in both, only A, only B, in neither. A left column 'multiply' lights the lens where both are one and writes each point's product: 1, 0, 0, 0. A right column 'add' lights the union and writes the sums: 2 (capped to 1), 1, 1, 0.",
      "The lens lights up under 'multiply', the whole union under 'add', and each point shows its number.",
      [{"at": 0.1, "event": "two discs and four points"}, {"at": 0.35, "event": "multiply: the lens lights; products"}, {"at": 0.68, "event": "add: the union lights; sums, 2 capped to 1"}],
      "LectureEvidenceTable of products and sums", "Overlapping regions with a number at each point make 'both' and 'either' visible; a table would list them.",
      "Arithmetic; the cap is the 8-bit output clamp (FACTCHECK 32)")

lab("B19", 2, "color uniforms with the hint source color: a color picker", "08-bubble.gdshader", V("e3-color-pickers.mp4"),
    "Godot 4.7.2 editor · scripted editor session",
    [{"at": 0.12, "lines": ln("08-bubble.gdshader", "uniform vec3 body_color", "uniform vec3 highlight_color"), "label": "hint: how Godot treats this uniform"},
     {"at": 0.62, "lines": ln("08-bubble.gdshader", "uniform vec3 body_color", "uniform vec3 highlight_color"), "label": "source_color: a color picker"}],
    "Code card at left with the two color-uniform lines highlighted; at right a real still of Godot's Inspector from a scripted editor session, the material's Shader Parameters group showing two color swatches (Body Color and Highlight Color) and a Brightness number box with a slider bar, with a terracotta ring on the first swatch; then the same swatch clicked, its picker open (color wheel, brightness bar, RGB, HSV, Linear, Hex). The one-line definition of a hint (GLOSSARY wording) sits under the result.",
    "The uniform lines light up, the ring lands on the color swatch they produce, and the swatch opens its picker.",
    [{"at": 0.12, "event": "uniform lines highlighted; hint label and the definition caption"}, {"at": 0.62, "event": "'source_color' label on the code lines"}, {"at": 0.72, "event": "ring on the Body Color swatch (E3-1)"}, {"at": 0.86, "event": "dissolve to E3-2: the swatch's picker open"}],
    "ShaderLab render of the bubble (labelled)", "Real editor frames, recorded by script, are the rung-1 SHOW-THE-THING answer for 'the editor shows a color picker': a swatch, and the picker it opens; the Lab render of the bubble does not show an editor widget.",
    "E3 (DONE by script, 2026-10-13: the one film-specific editor run; state script, scene and log in evidence/planning-checks/editor-capture/): the bubble material (lab-shaders/08-bubble.gdshader, byte-identical in the scratch project) on a 480 x 480 ColorRect. Frames in `_godot-shaders-series/editor-capture/png/1920x1080/soft-edges-glow-and-noise/`: soft-edges_E3-1_bubble-shader-parameters-two-color-swatches-and-slider (group Shader Parameters: rows Body Color and Highlight Color, both color swatches, and Brightness, a number box with a slider bar) and soft-edges_E3-2_body-color-picker-popup-open (the picker after a scripted click on the Body Color swatch: R 94, G 163, B 145, Hex 5ea391, Swatches, Recent Colors). Only 1920x1080 was recorded (one run); a 640 x 360 crop of it would blur in the 4K window, so re-record at native size (recipe in CAPTURE-PLAN.md section E, about 30 s) and crop the native frames: E3-1 x 1275 to 1915, y 195 to 555 (1920 coordinates, times 1.8 for native), E3-2 x 1275 to 1915, y 410 to 770, which ends above the line 'Screen Recording permission missing!' (the eyedropper needs a macOS permission). The ring box is a fraction of the E3-1 crop. Cross-dissolve at 0.86. No pointer is visible (the picker was opened by a scripted click): label 'scripted editor session'.",
    "Editor frames E3-1 and E3-2, DONE by script (_godot-shaders-series/editor-capture/png/1920x1080/soft-edges-glow-and-noise/); FACTCHECK rows 33, 35 (PASS); extra_checks U: source_color vec3 is type Color (20), a plain vec4 is Vector4 (12)",
    lane="editor", caption="hint: the word after a colon that tells Godot how to treat a uniform",
    rings=[{"at": 0.72, "box": [0.777, 0.625, 0.983, 0.7]}])

lab("B20", 2, "the sum: body color plus highlight color times the highlight mask", "08-bubble.gdshader", V("c09-bubble.png"),
    "Godot 4.7.2 · Forward+ · the shader on the left",
    [{"at": 0.1, "lines": ln("08-bubble.gdshader", "vec3 rgb")}, {"at": 0.62, "lines": ln("08-bubble.gdshader", "float highlight"), "label": "highlight: the mask"}],
    "Code card at left (the 14-line bubble shader); at right the real render: the teal bubble with its pale highlight at the upper left. The rgb line is highlighted first, then the highlight line.",
    "The sum line lights up, then the highlight mask line.",
    [{"at": 0.1, "event": "rgb line highlighted"}, {"at": 0.62, "event": "highlight line highlighted; 'highlight: the mask'"}],
    "manim", "The complete bubble next to its one summing line is the claim of the beat.",
    "C09: the square target, lab-shaders/08-bubble.gdshader at its defaults (brightness 1.0), still PNG 3840 x 2160, Forward+. Verified: the highlight's centre reads (0.918, 1.000, 1.000) on screen (the shader's rgb is 0.919, 1.159, 1.019 before the screen clips it); the body away from the highlight reads (0.514, 0.776, 0.690).",
    "Lab 08-bubble-1.0 (lab-analysis.txt)")

manim("B21", 2, "multiplication before addition: a + b * c against (a + b) * c", "EvaluationOrder",
      "The expression a + b * c as a small tree: b * c is ringed first (terracotta), then the plus. Beneath it the parenthesised (a + b) * c with the plus ringed first. Numbers on the leaves: a = 0.64 (the body, green channel), b = 0.52 (the highlight, green channel), c = 0.6 (brightness); results written under each: 0.95 and 0.70. Label 'multiply binds first'.",
      "The ring lands on b * c first in the left tree and on a + b first in the right one, and the two results differ.",
      [{"at": 0.1, "event": "left tree a + b * c"}, {"at": 0.34, "event": "ring on b * c; result 0.95"}, {"at": 0.66, "event": "right tree (a + b) * c; ring on a + b; result 0.70"}],
      "BrowserCapture of the docs operator table", "A tree with the order of work ringed step by step shows what the rule does to real numbers; the table is the next beat.",
      "Arithmetic 0.64 + 0.52 * 0.6 = 0.952 and (0.64 + 0.52) * 0.6 = 0.696; Lab 08/09-bubble at brightness 0.6 (FACTCHECK 37, 38, 39)")

lab("B22", 2, "the parentheses bug with real numbers: 0.70 against 0.95", "08-bubble.gdshader", V("c10-bubble-two-up.mp4"),
    "Godot 4.7.2 · Forward+ · brightness swept by script on both",
    [], "Two real Godot panels side by side on the cream stage: the left bubble uses the shader with the parentheses, the right one the shader without. Brightness is swept from 1.0 to 0.6 on both; the left bubble dims all over, the right one keeps its teal body and only its highlight dims. Readouts under each: 'with: green 0.70' and 'without: green 0.95'.",
    "Both bubbles are dialled down together: one dims all over, the other barely changes.",
    [{"at": 0.1, "event": "two bubbles at brightness 1.0"}, {"at": 0.3, "event": "the sweep to 0.6 starts"}, {"at": 0.65, "event": "left dimmed, right nearly unchanged; readouts"}],
    "ShaderLab stills", "The two results side by side under the same sweep are the proof; a still pair would hide the dial moving.",
    "C10: two-panel scene script (`--scene`, as the Lines film's two_panels.gd): two square targets side by side (left lab-shaders/08-bubble.gdshader, right lab-shaders/09-bubble-bug.gdshader), brightness 1.0 held 1.5 s then swept to 0.6 by 4.5 s on both (`--animate left.brightness:0:1,1.5:1,4.5:0.6` and the same for right), held; 12 s, 30 fps, Forward+, stage #D9D5CA. Verified: at brightness 0.6 the highlight centre reads green 0.694 (with parentheses) and 0.953 (without); the body away from the highlight reads green 0.467 and 0.722; at 1.0 both read 0.776.",
    "Lab 08-bubble-0.6 and 09-bubble-bug-0.6 (lab-analysis.txt)", layout="video",
    readouts=[{"at": 0.65, "text": "with: green 0.70", "x": 0.27, "y": 0.95}, {"at": 0.65, "text": "without: green 0.95", "x": 0.73, "y": 0.95}])

rem("B23", 2, "Godot's own operator table", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#operators",
     "image": V("d2-operators.png"), "caption": "Godot 4.7 documentation · Shading language · Operators · captured at build time",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1}, {"at": 0.25, "x": 0.5, "y": 0.45, "scale": 1.5}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real Godot 4.7 'Operators' table in a browser window; the camera pushes in on the first four rows (parenthetical grouping, unary, multiplicative, additive) and a terracotta ring marks the multiplicative and additive rows.",
    "The camera pushes in on the table and the ring lands on 'multiplicative' above 'additive'.",
    [{"at": 0, "event": "page"}, {"at": 0.25, "event": "push-in; ring on the multiplicative and additive rows"}],
    "manim table redrawn", "The rule is a documentation fact; the documentation itself is the evidence (SHOW-THE-THING).",
    "Playwright capture of the live docs page (1600 x 900 at 2.4x) at build time; read 2026-10-13: precedence 1 parenthetical grouping, 3 multiplicative, 4 additive")

# ═════════════════════════ ACT IV · Noise That Moves ═════════════════════════
lab("B24", 3, "noise: a texture of smooth random values, made by a NoiseTexture2D", "10-noise-cloud.gdshader", V("e1-noise-inspector.mp4"),
    "Godot 4.7.2 editor · scripted editor session",
    [{"at": 0.1, "lines": ln("10-noise-cloud.gdshader", "uniform sampler2D"), "label": "noise: a texture of smooth random values"},
     {"at": 0.62, "lines": ln("10-noise-cloud.gdshader", "uniform sampler2D"), "label": "texture: an image a shader can read by address"}],
    "Act title 'Noise That Moves' (serif 40) top-left. Code card at left with the sampler line highlighted twice, each time with its definition label (noise, then texture). At right two real stills of Godot's Inspector from a scripted editor session, one after the other: first the NoiseTexture2D itself (Width 512 px, Height 512 px, its Noise slot holding a FastNoiseLite, a Seamless row; this view has no preview), with a terracotta ring on the NoiseTexture2D header and then on the Noise slot; then the FastNoiseLite itself, where the grey clouds preview appears, with the ring on the preview.",
    "The ring lands on the NoiseTexture2D, then on its Noise slot, then on the cloud preview of the generator, as the voice names them.",
    [{"at": 0.1, "event": "sampler line + 'noise' definition; the NoiseTexture2D view"}, {"at": 0.62, "event": "'texture' definition"}, {"at": 0.66, "event": "ring on the NoiseTexture2D header"}, {"at": 0.78, "event": "ring on the Noise slot (FastNoiseLite)"},
     {"at": 0.84, "event": "dissolve to the FastNoiseLite view"}, {"at": 0.9, "event": "ring on the clouds preview"}],
    "ShaderLab render of the noise texture as teal alpha (labelled)", "The real Inspector is the thing the sentence names (SHOW-THE-THING), and the two views are the honest order: the texture holds a generator, the generator shows the clouds; the Lab render of the same texture does not show an editor.",
    "E1 (reused; DONE by script, 2026-10-13): two frames recorded in the same scratch project for the Textures and Color film and shown here because they show the same thing (the resource itself, not the slot's label, so the other film's shader does not show): `_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/textures-and-color_E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite.png` (the NoiseTexture2D view: Width, Height, Generate Mipmaps, Noise = FastNoiseLite, Color Ramp, Seamless, Invert, In 3D Space, As Normal Map, Normalize; NO preview) and `textures-and-color_E1-3b_inside-FastNoiseLite-preview-clouds.png` (the FastNoiseLite view: the grey clouds preview with a 3D button, Noise Type Simplex Smooth, Seed 0, Frequency 0.01, Offset, Fractal, Domain Warp). Both also exist as native 3456x1944 twins in png/3456x1944/textures-and-color/: crop those, x 1275 to 1915, y 195 to 555 in 1920 coordinates (times 1.8 for native). Cross-dissolve at 0.84; the ring boxes are fractions of that crop. (This film's own scene with a `noise` slot was never recorded: the frames above show the same two views.) No pointer: label 'scripted editor session'.",
    "Editor frames E1-3a and E1-3b, DONE by script (_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/); FACTCHECK row 57; noise_check T: neighbouring pixels differ by 0.011, pairs over 200 px apart by 0.19",
    layout="side", lane="editor", title="Noise That Moves",
    rings=[{"at": 0.66, "box": [0.352, 0.028, 0.992, 0.125]}, {"at": 0.78, "box": [0.356, 0.417, 0.995, 0.5]}, {"at": 0.9, "box": [0.352, 0.025, 0.992, 0.497]}])

lab("B25", 3, "a sampler2D uniform, texture() as a lookup, noise into the alpha", "10-noise-cloud.gdshader", V("c11-noise-cloud.png"),
    "Godot 4.7.2 · Forward+ · NoiseTexture2D, seamless on",
    [{"at": 0.1, "lines": ln("10-noise-cloud.gdshader", "uniform sampler2D"), "label": "sampler2D: the type of a texture a shader reads"},
     {"at": 0.38, "lines": ln("10-noise-cloud.gdshader", "float n"), "label": "texture(noise, UV): a texture read at this address"},
     {"at": 0.65, "lines": ln("10-noise-cloud.gdshader", "COLOR")}],
    "Code card at left (the noise-cloud shader); at right the real render: the teal disc turned to cloud, bright patches where the noise is high and see-through patches where it is low.",
    "The three lines light up in turn while the clouds sit in the disc.",
    [{"at": 0.1, "event": "sampler2D line + definition"}, {"at": 0.38, "event": "texture line + 'lookup'"}, {"at": 0.65, "event": "COLOR line: noise into the alpha"}],
    "manim", "The cloud is the real result of the lookup, next to the line that does it.",
    "C11: scene script (`--scene`; the Lab only binds a plain image): NoiseTexture2D with FastNoiseLite defaults, 512 x 512, seamless on, bound to the 'noise' uniform of lab-shaders/10-noise-cloud.gdshader on the square target; still PNG 3840 x 2160, Forward+. Node setup as in evidence/planning-checks/noise_check.gd (make_noise, make_rect).",
    "Lab 10-noise-cloud (plain image, same look); noise_check T, F")

lab("B26", 3, "add TIME to the address: the clouds drift", "11-noise-scroll.gdshader", V("c12-noise-scroll.mp4"),
    "Godot 4.7.2 · Forward+ · a live clock",
    [{"at": 0.12, "lines": ln("11-noise-scroll.gdshader", "float n"), "label": "TIME: seconds on one clock shared by the whole game"}, {"at": 0.62, "lines": ln("11-noise-scroll.gdshader", "COLOR")}],
    "Code card at left (the scroll shader: the lookup now adds TIME times a tenth to the address); at right the real render: the clouds drift steadily sideways inside the disc. The TIME definition is on screen.",
    "The clouds drift while the lookup line is highlighted.",
    [{"at": 0.12, "event": "lookup line + TIME definition"}, {"at": 0.45, "event": "clouds drifting"}, {"at": 0.8, "event": "still drifting"}],
    "manim sliding lookup", "A live render of the drift is the claim; the direction detail comes next.",
    "C12: scene script as C11 (NoiseTexture2D seamless on) with lab-shaders/11-noise-scroll.gdshader; 12 s, 30 fps, Forward+, `--time-origin 0` so TIME is 0 at the first frame (no scripted input). Verified: a 3.0 s clock step moves the shader's TIME by 3.01 s and the pattern by 0.3 of the width, i.e. 0.1 per second (noise_check Z); the natural clock matched the engine's ticks in an earlier run (run-0 transcription, item 7).",
    "noise_check Z (TIME decoded from the same frame)")

manim("B27", 3, "adding to the address moves the picture the other way: left", "WindowSlides",
      "A long strip of noise bars (grey tones) with a terracotta window frame laid over it, the picture seen through the frame shown above. The frame slides right along the strip while the pattern seen through it shifts left. Labels 'lookup moves right' and 'picture moves left'; a readout '+0.125 → 32 px left' with the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+'.",
      "The frame slides right and the pattern inside it slides left.",
      [{"at": 0.1, "event": "strip, frame and the view through it"}, {"at": 0.4, "event": "frame slides right; view shifts left"}, {"at": 0.75, "event": "readout '+0.125 → 32 px left'"}],
      "ShaderLab with a direction arrow", "A window sliding over a fixed strip is the exact reason the picture appears to move the other way.",
      "noise_check D: offset 0.125 gave a best shift of -32 px (exactly 0.125 of 256), err 0.0 (FACTCHECK 50, 51)")

lab("B28", 3, "without the hint the lookup past the edge returns the edge pixel: streaks", "12-noise-no-repeat.gdshader", V("c13-noise-no-repeat.mp4"),
    "Godot 4.7.2 · Forward+ · the hint deleted",
    [{"at": 0.1, "lines": ln("12-noise-no-repeat.gdshader", "uniform sampler2D")}, {"at": 0.7, "lines": ln("12-noise-no-repeat.gdshader", "float n")}],
    "Code card at left: the same scroll shader with the hint removed from the uniform line; at right the real render: the clouds drift for a moment, then the right side of the disc smears into horizontal streaks that grow leftward as time passes. A terracotta ring on the streaks.",
    "Streaks grow from the right edge and take over the picture while the clouds stop moving there.",
    [{"at": 0.1, "event": "the uniform line without its hint"}, {"at": 0.4, "event": "streaks begin at the right"}, {"at": 0.7, "event": "ring on the streaks; they have spread"}],
    "manim", "A real streak growing across the picture is the failure the hint prevents; a drawing would not show how it spreads.",
    "C13: scene script as C11 with lab-shaders/12-noise-no-repeat.gdshader; 12 s, 30 fps, Forward+, `--time-origin 0`. Verified: a raw greyscale check with lookups past 1.0 has row standard deviation 0.0 in the clamped half (identical along every row) and 0.1485 with repeat_enable (noise_check C).",
    "noise_check C-default-no-hint (row std 0.0) and F-norepeat-seamless (TIME 4.5 s and 9.5 s pictures)",
    rings=[{"at": 0.7, "box": [fx(0.6), fy(0.3), fx(0.95), fy(0.7)]}])

lab("B29", 3, "repeat_enable wraps the lookup; a seam shows where the edges do not match", "11-noise-scroll.gdshader", V("c14-noise-seam.mp4"),
    "Godot 4.7.2 · Forward+ · NoiseTexture2D, seamless off",
    [{"at": 0.1, "lines": ln("11-noise-scroll.gdshader", "uniform sampler2D"), "label": "repeat_enable: past one, wrap to the start"}],
    "Code card at left (the hint is back on the uniform line); at right the real render with a plain, non-seamless noise texture: the clouds scroll forever, and a straight vertical line, a seam, crosses the disc and travels left. A terracotta ring on the seam.",
    "The seam travels left across the disc as the clouds scroll.",
    [{"at": 0.1, "event": "the hint highlighted"}, {"at": 0.38, "event": "clouds wrap; the seam enters the disc"}, {"at": 0.68, "event": "ring on the seam"}],
    "manim", "A straight line cutting through the clouds is the defect; only a real render shows how visible it is.",
    "C14: scene script: NoiseTexture2D with FastNoiseLite defaults, 512 x 512, seamless OFF, bound to lab-shaders/11-noise-scroll.gdshader on the square target; 12 s, 30 fps, Forward+, `--time-origin 0` (the seam then sits at UV x 0.9 at 1 s and 0.2 at 8 s). Verified: the plain texture's wrap difference is 14.25x the normal neighbour difference; the render's biggest column jump sits at the wrap position (ratio 7.4 to 7.7) and moves as 1 - 0.1 * TIME (77 px per 3 s step).",
    "noise_check T-plain, S-plain, Z-scroll-plain, F-scroll-plain (TIME 14.5 s picture)",
    rings=[{"at": 0.68, "box": [fx(0.4), fy(0.2), fx(0.6), fy(0.8)]}])

lab("B30", 3, "Seamless on: the edges are blended so they meet", None, V("c15-noise-two-up.mp4"),
    "Godot 4.7.2 · Forward+ · two NoiseTexture2D, seamless off and on",
    [], "Two real Godot panels side by side showing the scrolling disc: the left uses a plain noise texture and a seam crosses it; the right uses the same settings with Seamless switched on and no seam appears. Labels 'seamless off' and 'seamless on'.",
    "The seam crosses the left disc while the right disc scrolls cleanly.",
    [{"at": 0.1, "event": "both discs scrolling; labels"}, {"at": 0.4, "event": "seam crosses the left disc"}, {"at": 0.7, "event": "right disc still clean"}],
    "ShaderLab stills", "The two results under the same scroll are the proof; the seam is a motion across the picture.",
    "C15: two-panel scene script (`--scene`): two square targets side by side with lab-shaders/11-noise-scroll.gdshader, left NoiseTexture2D seamless off, right seamless on (same FastNoiseLite defaults, 512 x 512); 12 s, 30 fps, Forward+, `--time-origin 0`. Verified: wrap difference 14.25x the neighbour difference (off) against 1.07x (on); contrast (standard deviation) 0.168 against 0.158; the render has no outlier column with seamless on (ratio 1.3 to 1.6).",
    "noise_check T-plain / T-seamless, S-seamless, Z-scroll-seamless, F-scroll-seamless", layout="video",
    readouts=[{"at": 0.1, "text": "seamless off", "x": 0.27, "y": 0.95}, {"at": 0.1, "text": "seamless on", "x": 0.73, "y": 0.95}],
    caption="seamless: the edges match, so repeats show no seam")

lab("B31", 3, "noise as a threshold: a reveal driven by a uniform", "13-noise-reveal.gdshader", V("c16-noise-reveal.mp4"),
    "Godot 4.7.2 · Forward+ · progress swept by script",
    [{"at": 0.1, "lines": ln("13-noise-reveal.gdshader", "uniform float progress")}, {"at": 0.4, "lines": ln("13-noise-reveal.gdshader", "step(n, progress)")}],
    "Code card at left (the reveal shader); at right the real render: as progress climbs from 0 to 1 the disc blooms in blotches, small islands first, then merging until the whole disc is on. A label with the progress value.",
    "Islands of teal appear, grow and merge as the number climbs.",
    [{"at": 0.1, "event": "progress line highlighted"}, {"at": 0.4, "event": "step line; first islands"}, {"at": 0.7, "event": "islands merging"}],
    "manim", "The reveal is a motion by nature; the real render shows the noise's own blotch pattern.",
    "C16: custom scene as C11 (seamless on) with lab-shaders/13-noise-reveal.gdshader, progress held 0 for 1 s, swept to 1 by 9 s, held (`--animate progress:0:0,1:0,9:1`); 12 s, 30 fps, Forward+. Verified: coverage of the disc interior 1.3 % / 43.7 % / 93.1 % at progress 0.25 / 0.5 / 0.75 (noise_check R).",
    "noise_check R-reveal-0.25 / 0.5 / 0.75 and R-curve")

manim("B32", 3, "progress is not percent shown: the reveal's pace follows the noise histogram", "RevealPace",
      "Top: a bell-shaped histogram of the noise values from 0 to 1 (20 bars, real data from noise_check T-seamless), centred near 0.5. Below it the cumulative curve from the same noise (real data, noise_check R-curve): an S rising slowly, then fast, then slowly. Three terracotta dots on the curve at progress 0.25, 0.5 and 0.75, labelled '1 %', '44 %' and '93 %'. Label 'progress is not percent shown' and the small grey credit 'Apple M4 Pro · Godot 4.7.2 · Forward+ · NoiseTexture2D defaults'.",
      "The bars rise into a bell, the curve draws as their running total, and the three dots land at 1, 44 and 93 percent.",
      [{"at": 0.1, "event": "histogram bars"}, {"at": 0.4, "event": "cumulative curve draws"}, {"at": 0.7, "event": "three dots with their percentages"}],
      "ShaderLab with a percent readout", "A running total of a bell is an S-curve: the same shape as smoothstep, and the picture shows why the pace is uneven.",
      "noise_check T-seamless histogram_20_bins_of_0.05 and R-curve; evidence/planning-checks/RESULTS.md (FACTCHECK 59, 60)")

# ═════════════════════════ ACT V · Glow, Honestly ═════════════════════════
manim("B33", 4, "a number above one is cut off at one: teal times six turns white", "ClipAtOne",
      "Act title 'Glow, Honestly' (serif 40) top-left. Three vertical bars (red, green, blue channels of teal times six: heights 2.2, 3.8 and 3.4) grow past a horizontal line at 1.0 labelled 'the screen stops here'. The parts above the line are cut away in hatched grey and all three bars end at 1. A swatch at right turns from teal to white. Label 'teal × 6'.",
      "The bars grow past the line, the tops are cut off, and the swatch turns white.",
      [{"at": 0.1, "event": "bars and the line at 1.0, act title"}, {"at": 0.38, "event": "bars grow past the line"}, {"at": 0.68, "event": "tops cut away; swatch turns white"}],
      "ShaderLab render of the flat white bubble", "Bars crossing a line and being cut off is the clipping, and it comes before the render that proves it.",
      "Arithmetic 0.37, 0.64, 0.57 times 6 = 2.2, 3.8, 3.4 (the numbers the default 2D pipeline multiplies); Lab 14-glow-bubble-1: body reads (1, 1, 1) (FACTCHECK 61, 62)")

lab("B34", 4, "the glow dial in the shader; in the default pipeline the bubble just goes white", "14-glow-bubble.gdshader", V("c17-glow-dial-sdr.mp4"),
    "Godot 4.7.2 · Forward+ · default 2D rendering · glow swept by script",
    [{"at": 0.1, "lines": ln("14-glow-bubble.gdshader", "COLOR"), "label": "multiply binds first: the sum needs parentheses"},
     {"at": 0.4, "lines": ln("14-glow-bubble.gdshader", "uniform float glow")}],
    "Code card at left (the 14-line glow shader); at right a real Godot window on a slate-blue stage: the teal bubble with its highlight turns paler and then flat white as glow is swept from 0 to 1. Readouts 'glow 0' and 'glow 1'.",
    "The bubble loses its teal and its highlight and ends as a flat white disc.",
    [{"at": 0.1, "event": "COLOR line with the parentheses"}, {"at": 0.4, "event": "glow uniform; sweep under way"}, {"at": 0.7, "event": "flat white, readout 'glow 1'"}],
    "manim", "The flat white disc is the real result of the multiplier in the default pipeline.",
    "C17: the square target, lab-shaders/14-glow-bubble.gdshader, default 2D rendering (no HDR 2D, no environment), stage #5F7A96, glow 0 held 1 s, swept to 1 by 7 s, held (`--animate glow:0:0,1:0,7:1`; stage via `--clear`/the scene script); 12 s, 30 fps, Forward+. Verified: glow 0 body (0.514, 0.776, 0.690); glow 1 body (1, 1, 1), spot (1, 1, 1) (glow-results G0, G1).",
    "glow-results G0, G1; Lab 14-glow-bubble-0 / 0.1 / 1",
    readouts=[{"at": 0.1, "text": "glow 0", "x": 0.5, "y": 0.95}, {"at": 0.7, "text": "glow 1", "x": 0.5, "y": 0.95}],
    caption="glow: bright pixels bleeding light onto the pixels around them")

rem("B35", 4, "H D R and the project setting, in Godot's own words", "BrowserCapture",
    {"url": "https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html#using-glow-in-2d",
     "image": V("d1-using-glow-in-2d.png"), "caption": "HDR 2D: a project setting: 2D is drawn in light and numbers past one are kept",
     "frame": "browser", "moves": [{"at": 0, "x": 0.5, "y": 0.3, "scale": 1}, {"at": 0.25, "x": 0.5, "y": 0.5, "scale": 1.5}],
     "ringColor": "#A64A24", "durationSeconds": "__AUDIO__"},
    "The real 'Using glow in 2D' section of the Godot 4.7 documentation in a browser window; the camera pushes in on 'To enable HDR in 2D, open the Project Settings, enable Rendering > Viewport > HDR 2D then restart the editor.' and a terracotta ring marks it. The caption under the browser window is the GLOSSARY definition of HDR 2D, one line; the real address in the window's bar and SOURCES.md carry the provenance.",
    "The camera pushes in on the sentence the voice is describing.",
    [{"at": 0, "event": "page"}, {"at": 0.28, "event": "push-in; ring on the HDR 2D sentence; HDR 2D definition"}],
    "GodotDevWorkbench reconstruction of Project Settings (labelled)", "The setting's name and the restart note are documentation facts; the documentation itself is the evidence (SHOW-THE-THING).",
    "Playwright capture of the live docs page (1600 x 900 at 2.4x) at build time; read 2026-10-13: 'To enable HDR in 2D, open the Project Settings, enable Rendering > Viewport > HDR 2D then restart the editor.'")

lab("B36", 4, "run one: H D R 2D on, glow off: still white, a tinted rim, the frame holds numbers above one", "14-glow-bubble.gdshader", V("c18-hdr-on.mp4"),
    "Godot 4.7.2 · Forward+ · H D R 2D switched on at 2 s · scripted", [],
    "A real Godot window on the slate-blue stage showing the flat white bubble (glow 1), then at 2 s H D R 2D is switched on: the disc stays white but its rim picks up a teal-cyan tint. Readouts 'HDR 2D on', 'frame: green 2.57' and 'screen: 1.0'.",
    "The rim turns cyan the moment the setting is switched on, and the two readouts show what the frame holds and what the screen shows.",
    [{"at": 0.1, "event": "flat white bubble"}, {"at": 0.4, "event": "H D R 2D switched on; the rim picks up a tint"}, {"at": 0.7, "event": "readouts 'frame: green 2.57' and 'screen: 1.0'"}],
    "manim", "A real switch with a real before and after is the claim; the two readouts are measured values.",
    "C18: custom scene: the square target with lab-shaders/14-glow-bubble.gdshader (glow 1.0), stage #5F7A96, root Viewport.use_hdr_2d set to true at 2.0 s (`--call-at 2.0:enable_hdr_2d`, scripted), no environment; 8 s, 30 fps, Forward+. Verified (toggle_check, glow-results G1 and G3): the soft band reads (0.678, 0.733, 0.788) before and (0.726, 1.000, 1.000) after; a 256 px SubViewport with use_hdr_2d holds green 2.572 at the sample pixel (format RGBAH) while the screen shows 1.0; with it off the frame holds 1.0.",
    "glow-results G1, G3; run-toggle.log step 1", layout="video",
    readouts=[{"at": 0.4, "text": "HDR 2D on", "x": 0.5, "y": 0.05}, {"at": 0.7, "text": "frame: green 2.57", "x": 0.27, "y": 0.95}, {"at": 0.7, "text": "screen: 1.0", "x": 0.73, "y": 0.95}])

lab("B37", 4, "run two: world environment, glow on, background canvas: a teal halo", "14-glow-bubble.gdshader", V("c19-env-glow-on.mp4"),
    "Godot 4.7.2 · Forward+ · H D R 2D on · glow switched on at 2 s · scripted", [],
    "The same window, H D R 2D already on, flat white bubble on the slate-blue stage. At 2 s a world environment with glow on, background Canvas and intensity 2 comes into effect: a soft teal halo blooms around the disc. Readouts 'glow on', 'background: Canvas' and 'intensity 2'.",
    "A teal halo blooms around the white disc the moment the environment's glow is switched on.",
    [{"at": 0.1, "event": "white bubble, H D R 2D on"}, {"at": 0.4, "event": "environment glow on: the halo blooms"}, {"at": 0.7, "event": "readouts: glow on, background Canvas, intensity 2"}],
    "manim", "A real halo appearing at a real switch is the claim; the readouts name the three settings used.",
    "C19: custom scene: as C18 with use_hdr_2d already true; at 2.0 s a WorldEnvironment with an Environment (glow_enabled true, background_mode Canvas, glow_intensity 2.0, everything else default) is added (`--call-at 2.0:add_environment`, scripted); 8 s, 30 fps, Forward+. Verified (toggle_check step 2, glow-results G6): the stage next to the disc reads (0.373, 0.478, 0.588); 6 px beyond the band the halo reads (0.419, 0.553, 0.629), 16 px beyond (0.394, 0.513, 0.607), 28 px beyond (0.382, 0.494, 0.596). Without the Canvas background the same environment changes nothing (G4).",
    "glow-results G4, G5, G6; run-toggle.log step 2", layout="video",
    readouts=[{"at": 0.7, "text": "glow on", "x": 0.2, "y": 0.95}, {"at": 0.7, "text": "background: Canvas", "x": 0.5, "y": 0.95}, {"at": 0.7, "text": "intensity 2", "x": 0.8, "y": 0.95}])

manim("B38", 4, "glow is three agreements: shader, viewport, environment", "ThreeAgreements",
      "A flow of three stages left to right with a tall bar (the number above one) travelling through them: 'shader · makes a number above one', 'viewport · keeps it (H D R 2D)', 'environment · turns it into light (glow, Canvas)'. Run A: the bar passes all three and a halo blooms at the end. Run B: the viewport stage is off, a gate at height 1 cuts the bar to a stub and the picture ends flat white. Run C: the environment stage is missing, the tall bar arrives intact and nothing blooms.",
      "A tall bar travels the chain: it blooms at the end when every stage is on, and is cut or ignored when one is off.",
      [{"at": 0.1, "event": "three stages"}, {"at": 0.3, "event": "run A: bar passes; halo"}, {"at": 0.55, "event": "run B: the gate at one cuts the bar"}, {"at": 0.8, "event": "run C: no environment, no bloom"}],
      "DesignPipelineClaim, show-tell isometric", "A bar that is cut at a gate shows exactly where each missing agreement stops the effect; an isometric chain would draw the stages but not the height that matters.",
      "glow-results G1, G3, G4, G6 (FACTCHECK 70, 71, 72, 73)")

lab("B39", 4, "the halo grows with how far above one; a light stage leaves it nowhere to go", "14-glow-bubble.gdshader", V("c20-glow-dial-full.mp4"),
    "Godot 4.7.2 · Forward+ · H D R 2D on, glow on, Canvas, intensity 2 · glow swept and the stage switched by script", [],
    "The slate-blue stage with the white-hot bubble: as glow is swept from 0 to 1 the teal halo is absent, then faint around 0.5, then clear at 1. Near the end the stage colour is switched to the pale warm grey and the halo almost vanishes. Readouts 'glow 0.5', 'glow 1', 'light stage'.",
    "The halo swells as the dial climbs, then fades into a pale stage when the stage colour is switched.",
    [{"at": 0.1, "event": "glow 0, no halo"}, {"at": 0.35, "event": "glow 0.5: faint; glow 1: clear"}, {"at": 0.78, "event": "stage switched to light grey: the halo all but vanishes"}],
    "manim", "A halo that grows with the dial and disappears on a light stage is the claim; it needs the real render.",
    "C20: custom scene: as C19 (H D R 2D on, environment from the start), glow held 0 for 1 s, swept to 1 by 7 s, held (`--animate glow:0:0,1:0,7:1`), then at 9.0 s the clear colour switched from #5F7A96 to #D9D5CA (`--call-at 9.0:use_light_stage`, scripted); 12 s, 30 fps, Forward+. Verified (glow-results G11 to G15): halo at 6 px beyond the band: glow 0.1 and 0.3 none, 0.5 +0.003/+0.006/+0.003, 1.0 +0.046/+0.075/+0.041; on the light stage +0.008/+0.020/+0.020.",
    "glow-results G11, G12, G13, G14, G6, G15", layout="video",
    readouts=[{"at": 0.35, "text": "glow 0.5", "x": 0.2, "y": 0.95}, {"at": 0.45, "text": "glow 1", "x": 0.5, "y": 0.95}, {"at": 0.85, "text": "light stage", "x": 0.8, "y": 0.95}])

lab("B40", 4, "H D R 2D renders in linear light: a color without the hint comes out washed out", None, V("c21-hint-swatches.mp4"),
    "Godot 4.7.2 · Forward+ · H D R 2D switched on at 2 s · scripted", [],
    "Two flat teal squares side by side on the stage, one whose color uniform has the source color hint and one without, identical at first. At 2 s H D R 2D is switched on: the left one stays teal, the right one turns pale. Readouts 'hinted: red 0.37' and 'unhinted: red 0.64'.",
    "The right square washes out at the switch while the left one stays the same.",
    [{"at": 0.1, "event": "two identical teal squares"}, {"at": 0.4, "event": "H D R 2D on: the right square washes out"}, {"at": 0.7, "event": "readouts"}],
    "manim", "Two squares that start identical and part ways at one switch are the proof.",
    "C21: custom scene: two 60 x 60 flat-color squares (uniform vec4 flat_color = vec4(0.37, 0.64, 0.57, 1.0), left with source_color, right without; evidence/planning-checks/shaders/ev-flat-hint.gdshader and ev-flat-nohint.gdshader), root use_hdr_2d set to true at 2.0 s (`--call-at 2.0:enable_hdr_2d`, scripted); 6 s, 30 fps, Forward+. Verified: SDR both read (0.369, 0.639, 0.569); H D R 2D with the hint (0.370, 0.640, 0.570), without (0.642, 0.821, 0.780). The Compatibility renderer shows no difference (not shown).",
    "glow-results H0 to H3; run-toggle.log steps 0 and 1", layout="video",
    readouts=[{"at": 0.7, "text": "hinted: red 0.37", "x": 0.27, "y": 0.95}, {"at": 0.7, "text": "unhinted: red 0.64", "x": 0.73, "y": 0.95}],
    caption="linear light: the scale light adds up on, in a straight line")

lab("B41", 4, "glow without H D R 2D: lower the threshold; faint and colourless", "14-glow-bubble.gdshader", V("c22-sdr-threshold.mp4"),
    "Godot 4.7.2 · Forward+ · threshold 0.5 without H D R 2D, then H D R 2D at 3 s · scripted", [],
    "The slate-blue stage with the white bubble in the default pipeline and a world environment with glow on, background Canvas, threshold 0.5, intensity 2: only a faint, colourless halo. At 3 s H D R 2D is switched on and the threshold returns to 1: the halo grows and turns teal. Readouts 'threshold 0.5' then 'HDR 2D'.",
    "A faint grey halo becomes a clear teal one at the switch.",
    [{"at": 0.1, "event": "faint halo, threshold 0.5"}, {"at": 0.45, "event": "H D R 2D on, threshold 1: the halo grows and tints"}, {"at": 0.75, "event": "readout 'HDR 2D'"}],
    "manim", "A real faint halo turning into a clear one at one switch is the comparison.",
    "C22: custom scene: the square target with lab-shaders/14-glow-bubble.gdshader (glow 1.0), stage #5F7A96, WorldEnvironment (glow on, Canvas background, intensity 2) with glow_hdr_threshold 0.5 and no HDR 2D; at 3.0 s use_hdr_2d true and the threshold back to 1.0 (`--call-at 3.0:enable_hdr_2d_and_reset_threshold`, scripted); 8 s, 30 fps, Forward+. Verified (glow-results G8 against G6): 6 px beyond the band the halo is +0.008/+0.004/+0.004 (no tint) against +0.046/+0.075/+0.041.",
    "glow-results G8, G9, G6", layout="video",
    readouts=[{"at": 0.15, "text": "threshold 0.5", "x": 0.5, "y": 0.95}, {"at": 0.7, "text": "HDR 2D", "x": 0.5, "y": 0.95}],
    caption="threshold: the brightness above which light starts to bleed")


lab("B42", 4, "all the layers together: soft edge, highlight, drifting noise, the glow dial", "15-bubble-complete.gdshader", V("c23-bubble-complete.mp4"),
    "Godot 4.7.2 · Forward+ · H D R 2D on, glow on, Canvas, intensity 2 · glow swept by script", [],
    "The slate-blue stage with the finished bubble: a teal disc with a soft edge, a pale highlight at the upper left, clouds of noise drifting through it, and the glow dial sweeping from 0 to 1 so the bubble brightens toward white with a soft halo. Readouts 'glow 0' and 'glow 1'. No code panel: the shader is 16 lines (lab-shaders/15-bubble-complete.gdshader) and every line has been on screen already.",
    "The finished bubble drifts and brightens as the dial climbs, all five layers at once.",
    [{"at": 0.1, "event": "the bubble at glow 0: soft edge, highlight, drifting clouds"}, {"at": 0.45, "event": "glow rising: brighter, halo starting"}, {"at": 0.8, "event": "glow 1: near white with the halo; readout"}],
    "manim exploded view of the five layers", "The payoff of the film is the real, finished effect with every layer running at once; an exploded drawing would show the parts but not the whole alive.",
    "C23: scene script (`--scene`): the square target with lab-shaders/15-bubble-complete.gdshader and a seamless NoiseTexture2D (FastNoiseLite defaults, 512 x 512) bound to `noise`, H D R 2D on and a WorldEnvironment (glow on, Canvas background, intensity 2) from the first frame, stage #5F7A96, glow held 0 for 2 s, swept to 1 by 9 s, held (`--animate glow:0:0,2:0,9:1`), `--time-origin 0`; 12 s, 30 fps, Forward+. Verified (finale_check.gd, run-finale.log): the body at the sample pixel shows about (0.45, 0.66, 0.61) at glow 0, (0.66, 0.96, 0.87) at 0.3, (0.80, 1, 1) at 0.6, (0.98, 1, 1) at 1 (the scrolling noise moves each value by about 0.02 from run to run); the highlight centre reaches (1, 1, 1) by glow 0.6; 6 px beyond the band the stage (0.373, 0.478, 0.588) reads (0.383, 0.494, 0.597) at glow 1 (a faint halo: the noise thins the alpha).",
    "finale_check (run-finale.log); Lab 15-bubble-complete compiles", layout="video", nocode=True,
    readouts=[{"at": 0.1, "text": "glow 0", "x": 0.5, "y": 0.95}, {"at": 0.8, "text": "glow 1", "x": 0.5, "y": 0.95}],
    caption="lab-shaders/15-bubble-complete.gdshader · Forward+ · scripted glow sweep")

# ───────────────────── write lanes + SHOTLIST ─────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
for ai in range(5):
    chunk = {e["bid"]: e["entry"] for e in E if e["act"] == ai}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

hist = {}
for e in E:
    hist[e["entry"]["lane"]] = hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Soft Edges, Glow and Noise\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot render shown is a Shader Lab, custom-scene or editor capture of a tested file in `lab-shaders/`. The build must first create the shared pieces below (they are specified, not yet built), then record the 23 captures and the two documentation screenshots listed in `CAPTURE-PLAN.md` and copy the editor frames, which are already recorded by script.\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file): `ramp_strip`, `pixel_grid`, `plot` are used here; this film also needs a **plot with a travelling dot and dashed guides**, a **distance-ring spot on a pixel grid** and a **bar-through-gate** drawing, all built on the same kit. 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file) with `--material-at`, `--animate` (piecewise), `--scene`, `--call-at`, `--time-origin`; the scene scripts do the scripted switches (root `use_hdr_2d`, a WorldEnvironment appearing, a clear-colour change, the vec2 orbit) and set the stage colour. 4. **Editor frames E1, E3**: already recorded by script (B19: this film's own frames; B24: two frames reused from the Textures and Color recording), copy them (`CAPTURE-PLAN.md`). 5. **Documentation screenshots D1, D2** via Playwright (`BrowserCapture` convention).\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", hist)

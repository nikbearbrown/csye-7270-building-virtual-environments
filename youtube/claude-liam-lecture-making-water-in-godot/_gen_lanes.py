#!/usr/bin/env python3
"""_gen_lanes.py: writes lanes/act1..act5.json and SHOTLIST.md from the tested shader files (code excerpts are cut from the real files, so the code on
screen is always what was run). Re-run after editing a shader or a capture; never hand-edit lanes/ or SHOTLIST.md.
Cue lines are given as ABSOLUTE line numbers of the file and converted to the excerpt's own numbering."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
LS = "lab-shaders/"
V = "making-water/"          # public folder of the film's captures at build time (BUILD-PROMPT.md)
LAB = "Godot 4.7.2 · Forward+ · "



import math, re


def _rows(line, layout):
    """ShaderLab.tsx buildRows for ONE line (32 px code, card width by layout): the rows the card would draw, as (text, start index in the line)."""
    per = max(20, math.floor(((1100 if layout == "stack" else 736) - 68 - 22 - 24) / (0.602 * 32)))
    t = line.replace("\t", "    ")
    if len(t) <= per:
        return [(t, 0)]
    out, pos, first = [], 0, True
    while pos < len(t):
        room = per if first else per - 6
        cut = len(t) - pos
        if len(t) - pos > room:
            cut = room
            for k in range(room, int(room * 0.5), -1):
                if t[pos + k - 1] in " ,.(/":
                    cut = k
                    break
        out.append((t[pos:pos + cut], pos))
        pos += cut
        while pos < len(t) and t[pos] == " ":
            pos += 1
        first = False
    return out


def reflow(lines, layout):
    """Whitespace-only re-break of lines where the card's own wrap would cut a number in two (0. / 15): the line is split before that number.
    Returns (new_lines, map old index -> first new index). Tabs count as four spaces in the card, so the split works on the tab-expanded text."""
    new, mp = [], []
    for ln in lines:
        mp.append(len(new))
        cur = ln.replace("\t", "    ")
        lead = len(cur) - len(cur.lstrip(" "))
        for _ in range(5):
            rs = _rows(cur, layout)
            bad = next((k for k in range(len(rs) - 1) if re.search(r"\d\.$", rs[k][0]) and re.match(r"^\d", rs[k + 1][0])), None)
            if bad is None:
                break
            cutpos = rs[bad + 1][1]
            m = list(re.finditer(r"\d+\.$", cur[:cutpos]))[-1]
            k = cur.rfind(" ", 0, m.start())
            assert k > lead, ("no space to break at", ln)
            new.append(cur[:k].replace("    ", "\t", 1) if cur.startswith("    ") else cur[:k])
            cur = " " * (lead + 4) + cur[k + 1:]
        new.append(cur.replace("    ", "\t", 1) if cur.startswith("    ") else cur)
    return new, mp


def lines_of(path):
    return (R / path).read_text().splitlines()


def excerpt(path, a, b):
    return "\n".join(lines_of(path)[a - 1:b])


def cue(at, line, a, label=None):
    c = {"at": at, "lines": [line - a + 1]}
    if label:
        assert len(label) <= 60, (label, len(label))
        c["label"] = label
    return c


def SL(layout, file, a=None, b=None, cues=(), video="", vlabel="", aspect=None, readouts=(), rings=(), ramp=None, caption="", title="", full=False):
    """ShaderLab props. file: path relative to the film folder (lab-shaders/... or water-project/scripts/...)."""
    p = {"layout": layout, "durationSeconds": "__AUDIO__"}
    if title:
        p["title"] = title
    if file:
        n = len(lines_of(file))
        a = a or 1
        b = b or n
        raw = excerpt(file, a, b).split("\n")
        newl, mp = reflow(raw, layout)
        p["code"] = "\n".join(newl)
        assert len(newl) <= 14, (file, a, b, len(newl))
        p["codeFile"] = file if (a == 1 and b == n) else f"{file} · lines {a} to {b}"
        if len(newl) != len(raw):
            p["codeFile"] += " (long lines re-broken)"
        p["cues"] = []
        for at, ln, lab in cues:
            c = cue(at, ln, a, lab)
            rel = c["lines"][0]
            assert 1 <= rel <= len(raw) and raw[rel - 1].strip(), ("cue on a missing or blank line", file, ln, a, b)
            c["lines"] = [mp[rel - 1] + 1]
            p["cues"].append(c)
        for c in p["cues"]:
            assert not (0.45 <= c["at"] <= 0.55), ("cue in the midpoint window", file, c)
    if video:
        p["video"] = V + video
        p["videoLabel"] = vlabel
        assert len(vlabel) <= 60, (vlabel, len(vlabel))
    if aspect:
        p["videoAspect"] = aspect
    p["readouts"] = [{"at": at, "text": t, "x": x, "y": y} for at, t, x, y in readouts]
    for r in p["readouts"]:
        assert len(r["text"].split()) <= 3 and not (0.45 <= r["at"] <= 0.55), r
    p["rings"] = [{"at": at, "box": box} for at, box in rings]
    if ramp:
        p["ramp"] = ramp
    if caption:
        assert len(caption) <= 80, (caption, len(caption))
        p["caption"] = caption
    return p


def capture(props, spec, vi, mc, show, ru, why, sparse=False):
    return {"lane": "capture", "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": vi, "motion_claim": mc, "show": show, "runner_up": ru, "why": why, "sparse": sparse}


def manim(cls, vi, mc, show, ru, why, sparse=True):
    return {"lane": "manim", "class": cls, "visual_intent": vi, "motion_claim": mc, "show": show, "runner_up": ru, "why": why, "sparse": sparse}


def table(title, headers, rows, note, cues, vi, mc, show, ru, why):
    return {"lane": "remotion", "pattern": "LectureEvidenceTable", "props": {"title": title, "headers": headers, "rows": rows, "note": note, "cues": cues, "durationSeconds": "__AUDIO__"},
            "visual_intent": vi, "motion_claim": mc, "show": show, "runner_up": ru, "why": why, "sparse": False}


S3 = LS + "03-noise-foam.gdshader"
S3A = LS + "03a-cells-debug.gdshader"
S3B = LS + "03b-power-curve.gdshader"
S3D = LS + "03d-foam-from-texture.gdshader"
S4A = LS + "04a-normal-map.gdshader"
S4B = LS + "04b-scrolling-normals.gdshader"
S4C = LS + "04c-two-layers.gdshader"
S4D = LS + "04d-warped-foam.gdshader"
S5 = LS + "05-vertex-waves.gdshader"
S5B = LS + "05b-synced-clock.gdshader"
S6 = LS + "06-shore-foam.gdshader"
WM = "water-project/scripts/wave_math.gd"
WD = "water-project/scripts/water_driver.gd"

L = {}
ABOUT = {}
EVID = {}

# ═══════════════════════════════ ACT I · Blue and Clear ═══════════════════════════════
L["B01"] = capture(SL("video", None, video="hook.mp4", vlabel=LAB + "scripted run", caption="one shader on one plane mesh: the finished water, built in this film", title="Blue and Clear"),
    "C01: scene water_scene.gd, shader 06-shore-foam, plane cut 127 x 127, iso camera, wave clock driven by the capture clock (W_FOLLOW), Forward+, the whole beat plus 1.0 s tail.",
    "Act title 'Blue and Clear' (serif 40) top-left; the finished water fills the framed window: blue and see-through over sand, a foam net, glints, rolling waves, a white shore line on the beach, the teal buoy and the cream crate riding the waves.",
    "The waves roll and the buoy and crate rise and fall with them while the foam net drifts: the whole film's result before any code.",
    [{"at": 0.0, "event": "the finished water already moving"}, {"at": 0.6, "event": "buoy and crate ride a crest"}],
    "manim drawing of a wave", "A real render is the honest first picture of what a shader can make; a drawing would only claim it.")
ABOUT["B01"] = "the finished water, before any code"; EVID["B01"] = "C01 hook (real render, stage 06)"

L["B02"] = manim("B02_ThreeLinks",
    "Left to right on the cream stage: a flat isometric plane tile labelled 'PlaneMesh'; an outlined slot labelled 'Material Override' holding a round preview tile labelled 'ShaderMaterial'; a small code-card icon labelled 'shader'. An outline box labelled 'MeshInstance3D' encloses the plane and the slot. Arrow shapes link them in turn: mesh to node, material into the slot, shader into the material.",
    "Three links draw in the order the voice names them, ending with the node holding the material.",
    [{"at": 0.2, "event": "PlaneMesh and node box"}, {"at": 0.5, "event": "ShaderMaterial into the slot"}, {"at": 0.8, "event": "shader into the material"}],
    "ShaderLab: a real Inspector frame from the editor driver", "The three-link chain is a structure with a direction; a drawing shows which holds which. A real Inspector frame comes in the last act.")
ABOUT["B02"] = "mesh, material and shader: the whole setup"; EVID["B02"] = "Manim only (labels from the real Inspector: Mesh, Material Override)"

L["B03"] = capture(SL("side", LS + "01-blue.gdshader", cues=[(0.08, 1, "spatial: a shader for 3D surfaces"), (0.30, 8, "fragment: runs once for each pixel the shape covers"), (0.60, 9, "albedo: the base color of a 3D surface")],
        video="blue-applied.mp4", vlabel=LAB + "shader assigned at 55 %", caption="built-in: a value the engine hands to a function"),
    "C02: scene water_scene.gd, W_LATE: the water plane has no material until 55 % of the beat, then 01-blue.gdshader is assigned; iso camera, Forward+.",
    "Code card with all eleven lines of 01-blue.gdshader at left (three cue labels land on lines 1, 8 and 9); at right the real render: a pale unshaded-looking grey plane over the sand until 55 % of the beat, then the plane turns solid blue with the sun's glare.",
    "A plain grey plane turns blue the moment the shader is assigned, while the three code lines light up.",
    [{"at": 0.08, "event": "shader_type line"}, {"at": 0.3, "event": "fragment line"}, {"at": 0.55, "event": "the plane turns blue"}, {"at": 0.6, "event": "ALBEDO line"}],
    "LectureCodeTrace alone", "The first shader is eleven lines: code and its real result side by side show that those lines are the blue.")
ABOUT["B03"] = "the first shader: spatial, fragment, albedo"; EVID["B03"] = "C02 blue-applied; lab-shaders/01-blue.gdshader (compiled in both renderers)"

L["B04"] = capture(SL("side", LS + "01-blue.gdshader", 3, 6, cues=[(0.18, 4, "uniform: set from outside; every pixel sees the same one"), (0.34, 4, "source_color: the numbers are sRGB; convert to light first")],
        video="blue-dial.mp4", vlabel=LAB + "scripted: color changed", readouts=[(0.88, "25 115 178", 0.5, 0.1)], caption="typed 0.10, 0.45, 0.70 reads 25, 115, 178 in an unshaded test, Forward+"),
    "C03: scene water_scene.gd, shader 01-blue, water_color set to green-teal at 35 %, violet at 62 %, back to the default 0.10, 0.45, 0.70 at 82 %. The 25, 115, 178 reading is the unshaded test E1 (evidence/planning-checks/RESULTS.md).",
    "Code card with the uniform lines; the real cove whose water turns green-teal, then violet, then back to blue; the pill '25 115 178' lands when the default colour returns, with the caption naming the unshaded test.",
    "The uniform is a dial: the colour changes three times without touching the code.",
    [{"at": 0.18, "event": "uniform line lit"}, {"at": 0.35, "event": "colour goes green-teal"}, {"at": 0.62, "event": "colour goes violet"}, {"at": 0.88, "event": "pill: 25 115 178"}],
    "manim: a typed colour and a pixel byte triple", "The dial is something to watch turn; the measured bytes arrive as one caption-backed pill, on the real shader.")
ABOUT["B04"] = "a uniform, source_color and the typed numbers"; EVID["B04"] = "C03; E1: typed 0.10, 0.45, 0.70 reads 25, 115, 178 (Forward+), 22, 115, 179 (Compatibility), plain uniform 89, 179, 218"

L["B05"] = capture(SL("side", LS + "01-blue.gdshader", 8, 11, cues=[(0.30, 10, "roughness: 0 is a mirror, 1 is fully matte")],
        video="roughness.mp4", vlabel=LAB + "scripted sweep", ramp={"at": 0.0, "from": 0.9, "to": 0.03}, caption="roughness 0.9 down to 0.03"),
    "C04: scene water_scene.gd, shader 01-blue, roughness swept linearly from 0.9 to 0.03 across the beat.",
    "Code card (the four fragment lines, ROUGHNESS lit); the real cove with the sun's reflection: a wide soft smear at the start that shrinks to a tight bright oval as the ramp marker runs from 0.9 to 0.03.",
    "The reflection tightens and sharpens as roughness falls.",
    [{"at": 0.3, "event": "ROUGHNESS line"}, {"at": 0.5, "event": "glare half as wide"}, {"at": 0.95, "event": "tight bright oval"}],
    "manim: a lobe shrinking", "The sun's reflection on the real plane is the evidence; a lobe drawing would be a model of it.")
ABOUT["B05"] = "roughness, mirror to matte"; EVID["B05"] = "C04 roughness (real render, ramp 0.9 to 0.03)"

L["B06"] = capture(SL("side", LS + "02-transparent.gdshader", 7, 15, cues=[(0.36, 14, None), (0.62, 14, "alpha: 0 is invisible, 1 is solid")],
        video="alpha-switch.mp4", vlabel=LAB + "shader swapped at 40 %", caption="stage 01, solid, swapped for stage 02: one more line"),
    "C05: scene water_scene.gd, solid 01-blue on the water, swapped (swap_shader) at 40 % of the beat for 02-transparent on the same material, opacity set to 1.0 then easing to 0.7.",
    "Code card with the stage-two fragment (ALPHA line lit); the real cove: a solid blue plane hiding the floor, then at 40 % the surface turns see-through and the sand, the rock and the buoy's underside appear under it.",
    "One line is added and the sand and the rocks appear through the water.",
    [{"at": 0.0, "event": "solid blue plane"}, {"at": 0.4, "event": "swap: ALPHA enters"}, {"at": 0.7, "event": "sand and rocks visible"}],
    "manim: a stack of layers", "The floor appearing under the real water is the proof that one line did it.")
ABOUT["B06"] = "writing alpha makes the surface see-through"; EVID["B06"] = "C05 alpha-switch; docs: ALPHA written -> transparent pipeline"

L["B07"] = capture(SL("side", LS + "02-transparent.gdshader", 11, 15, cues=[(0.20, 14, None)],
        video="opacity.mp4", vlabel=LAB + "scripted sweep", readouts=[(0.08, "1.0", 0.5, 0.1), (0.43, "0.3", 0.5, 0.1), (0.72, "0.7", 0.5, 0.1)], caption="opacity: how much of the surface shows"),
    "C06: scene water_scene.gd, shader 02-transparent, opacity 1.0 held to 20 %, down to 0.3 by 42 % (held to 56 %), up to 0.7 by 72 %.",
    "Code card (fragment, ALPHA lit); the real cove going from hiding everything (1.0) through almost invisible (0.3) to the readable default (0.7); the pill shows the opacity at each hold.",
    "The water fades from solid to almost gone and settles at point seven.",
    [{"at": 0.08, "event": "pill 1.0, floor hidden"}, {"at": 0.43, "event": "pill 0.3, water barely there"}, {"at": 0.72, "event": "pill 0.7, the default"}],
    "ShaderLab ramp only", "Three holds on the real water let the viewer pick the value by eye, which is how the default was chosen.")
ABOUT["B07"] = "opacity as a dial, and the default"; EVID["B07"] = "C06 opacity"

L["B08"] = manim("B08_BlendArithmetic",
    "Left: three flat swatches in the measured colours: water (25, 115, 178), sand (184, 157, 110) and a result swatch (108, 129, 162), joined by the sum '70 percent water plus 30 percent sand' drawn as two proportion bars. Under them two number rows: 'predicted 108, 129, 161' and 'screen 108, 129, 162'. Right: the real Forward+ test render (captures/blend-fp.png through lab_window) with one grey-backed terracotta ring on the probe point (plate over sand). Every number is a measured or computed figure from FACTCHECK.",
    "The bars slide together into the result swatch and the two number rows land one under the other, differing by one in the last place.",
    [{"at": 0.15, "event": "water and sand swatches"}, {"at": 0.45, "event": "result swatch and predicted row"}, {"at": 0.8, "event": "screen row and ring on the render"}],
    "ShaderLab with the test render and readouts", "A sum with real numbers is a Manim kind of picture; the real render is inset so the figures are never free-floating.")
ABOUT["B08"] = "the blend: seventy percent water plus thirty percent behind"; EVID["B08"] = "E3 (evidence/planning-checks): plate over sand, alpha 0.7: measured 108, 129, 162; linear-light prediction 108, 129, 161"

L["B09"] = manim("B09_TwoRenderers",
    "Two real test renders side by side (captures/blend-fp.png labelled 'Forward+', captures/blend-compat.png labelled 'Compatibility'), the probe point ringed in each; under them the red channel read: 108 and 71. A number line 0 to 255 under both shows two ticks, 'typed-number mix' at 73 and 'linear-light blend' at 108: the Compatibility reading sits on 73 and the Forward+ reading on 108.",
    "The two readings drop onto the number line one after the other and snap to the tick they match.",
    [{"at": 0.2, "event": "both renders"}, {"at": 0.5, "event": "Forward+ reading 108 lands on the linear tick"}, {"at": 0.78, "event": "Compatibility reading 71 lands on the typed tick"}],
    "ShaderLab video of both renderers", "Two renderers, one pixel, one number line: the choice of arithmetic is the claim, and a number line shows which arithmetic each renderer used.")
ABOUT["B09"] = "Forward+ blends in linear light, Compatibility on the typed numbers"; EVID["B09"] = "E3: red 108 (Forward+) vs 71 (Compatibility); naive mix of the typed numbers 73; blend-fp.png, blend-compat.png"

L["B10"] = table("render_mode: the three defaults", ["render mode", "Godot 4.7 docs, quoted"],
    [["blend_mix", "Mix blend mode (alpha is transparency), default."], ["depth_draw_opaque", "Only draw depth for opaque geometry (not transparent)."], ["cull_back", "Cull back-faces (default)."]],
    "Godot 4.7 docs · spatial shaders · render modes · read 2026-10-16", [0.22, 0.46 - 0.06, 0.66],
    "Three rows, one per render mode in the shader's second line, each with the docs' own words in a second column; the row for the mode being spoken is highlighted.",
    "The highlight steps down the table as the voice names each mode.",
    [{"at": 0.2, "event": "blend_mix row"}, {"at": 0.4, "event": "depth_draw_opaque row"}, {"at": 0.66, "event": "cull_back row"}],
    "BrowserCapture of the docs page", "The docs' exact words belong in a table the viewer can read; a page screenshot would be too small to read at four K.")
ABOUT["B10"] = "the render mode line and its three defaults"; EVID["B10"] = "docs spatial_shader (render modes table); lab-shaders/02-transparent.gdshader line 2 compiled"

_b11 = SL("side", None, video="sorting.mp4", vlabel=LAB + "water made to write depth at 78 %", caption="a red plane under the water: drawn on top, then hidden")
_b11["code"] = excerpt(LS + "02-transparent.gdshader", 2, 2) + "\n" + excerpt(LS + "02a-depth-draw-always.gdshader", 2, 2)
_b11["codeFile"] = "02-transparent line 2, then 02a-depth-draw-always line 2"
_b11["cues"] = [{"at": 0.30, "lines": [1], "label": "depth_draw_opaque: the water writes no depth"}, {"at": 0.80, "lines": [2], "label": "depth_draw_always: the water writes depth"}]
L["B11"] = capture(_b11,
    "C37: scene water_scene.gd, W_EXTRA=sort adds a red see-through plane (alpha 0.6) at y = -0.4 UNDER the water with its node origin nearer the camera; shader 02-transparent swapped at 78 % of the beat for 02a-depth-draw-always on the same material; iso camera, Forward+. Measured in evidence/planning-checks (E16): no render_mode line and the written defaults render pixel-identical; depth_draw_always hides the plane (56,099 pixels differ by more than 8 levels).",
    "Code card with the two render_mode lines (the default first, depth_draw_always second); the real cove with a red see-through plane lying under the water yet painted over it at the bottom of the frame; at 78 % of the beat the plane vanishes and the water shows blue and clean there.",
    "A red plane that should be under the water is painted on top of it, then disappears when the water is made to write depth.",
    [{"at": 0.3, "event": "depth_draw_opaque line, red plane over the water"}, {"at": 0.78, "event": "swap: the red plane vanishes"}, {"at": 0.8, "event": "depth_draw_always line"}],
    "manim: the draw order drawn (kept in _superseded/)", "A real plane drawn in the wrong order is the claim itself; the drawing could only say it.")
ABOUT["B11"] = "transparent objects draw after solid ones, sorted by node position, not by pixel"; EVID["B11"] = "C37 sorting; E16: the written render_mode defaults and no render_mode line render pixel-identical; docs 3d_rendering_limitations, Transparency sorting"

L["B12"] = table("What transparent materials cannot do", ["a transparent material", "Godot 4.7 docs"],
    [["casts shadows", "cannot"], ["appears in the depth texture", "cannot · gap read 0.500 m, not 0"], ["appears in the screen texture", "cannot"]],
    "Godot 4.7 docs · spatial shaders · E8: 0.500 m.", [0.2, 0.5 - 0.1, 0.66],
    "Three rows: casts shadows, appears in the depth texture, appears in the screen texture; each answered 'cannot' by the docs; the depth row also carries the measured gap of 0.500 m.",
    "The rows light in the order the voice lists them, the depth row last and longest.",
    [{"at": 0.2, "event": "shadows row"}, {"at": 0.4, "event": "depth row with the measured gap"}, {"at": 0.66, "event": "screen row"}],
    "Manim: a shadow and a depth strip", "Three yes-or-no facts with one measured number are a table's job; a drawing would add nothing the words do not carry.")
ABOUT["B12"] = "two more costs: no shadows, not in the depth or screen textures"; EVID["B12"] = "docs spatial_shader; E8 gap read 0.500 m"

# ═══════════════════════════════ ACT II · Foam ═══════════════════════════════
L["B13"] = table("Foam: noise in Godot 4.7.2", ["look in", "a noise or Voronoi maker?"],
    [["shading language functions", "none"], ["visual shader nodes: 110", "none (only random range)"], ["FastNoiseLite resource", "yes: a Cellular type"]],
    "ClassDB on Godot 4.7.2 · docs function list · 2026-10-16", [0.2, 0.42, 0.68],
    "Act title 'Foam' in the table heading; three rows: the shading language's function list (no noise function), the visual shader's 110 nodes (no Voronoi or noise node, only random range), and the FastNoiseLite resource (yes, a Cellular type).",
    "Rows light one at a time; the first two answer 'none', the third 'yes'.",
    [{"at": 0.2, "event": "functions: none"}, {"at": 0.42, "event": "visual nodes: none"}, {"at": 0.68, "event": "FastNoiseLite: Cellular"}],
    "LibraryIconRow of Godot nodes", "The claim is a count and a lookup in the engine itself; a table with the counted number is the evidence.")
ABOUT["B13"] = "Godot has no noise function and no Voronoi node"; EVID["B13"] = "facts1_classdb.gd: 110 visual shader nodes, none noise or Voronoi; docs function list; FastNoiseLite.TYPE_CELLULAR = 2"

L["B14"] = manim("B14_OnePointEach",
    "A grid of six by four outline squares (the series pixel-grid cast) on the cream stage; one terracotta dot (grey-ringed) drops into each of the 24 squares at a different spot; then two neighbouring dots are joined by a thin line and a dashed grey line (the perpendicular bisector between them) is drawn with the label 'equally close'. Labels: 'one point each'. Drawn, not rendered: labelled 'drawing'.",
    "Dots land one per square; then the line of equal distance grows between two neighbours.",
    [{"at": 0.2, "event": "dots drop into the squares"}, {"at": 0.65, "event": "two neighbours and the bisector"}],
    "ShaderLab: the real points render first", "The plan is a picture of squares and points; the real render of the same idea follows in the next beat.")
ABOUT["B14"] = "one random point per square; foam where two are equally close"; EVID["B14"] = "Manim only (drawing)"

L["B15"] = capture(SL("side", S3, 17, 20, cues=[(0.58, 18, "dot: multiply matching parts, add them up"), (0.68, 19, "sine: a smooth wave between -1 and 1"), (0.80, 19, "fract: the part after the point: x minus floor(x)")],
        video="foam-points.mp4", vlabel=LAB + "top view · points circle", aspect=1.0, caption="hash: an address in, random-looking numbers out; same address, same numbers"),
    "C08: scene water_scene.gd, W_BARE top view of the plane, shader 03a-cells-debug show=0 (points and grid), cell_density 8, 1080 x 1080.",
    "Code card with the four hash lines (cues on dot, sine, fract); at right a real top view: pale squares with a grey grid and a small deep-blue dot in every square, the dots slowly circling.",
    "A dot sits in every square and slowly circles; the same square always has its dot in the same place.",
    [{"at": 0.58, "event": "dot cue"}, {"at": 0.68, "event": "sine cue"}, {"at": 0.8, "event": "fract cue"}],
    "manim: a hash drawn as a function box", "The real points are the hash's output; the code beside them shows what made them.")
ABOUT["B15"] = "a hash picks each square's point"; EVID["B15"] = "C08 foam-points; lab-shaders/03a-cells-debug.gdshader show=0"

L["B16"] = manim("B16_NineSquares",
    "The grid from the last act's cast. One pixel (a small cream dot with a dark ring) sits near the border of a square. The 3 by 3 block of squares around it is outlined; the nine points inside are marked and nine thin lines run from the pixel to them; the nearest line is drawn thick, the second nearest medium; labels 'nearest' and 'second'.",
    "The nine lines draw in, then all but two fade, leaving the nearest thick and the second nearest medium.",
    [{"at": 0.2, "event": "3 by 3 block outlined"}, {"at": 0.5, "event": "nine lines"}, {"at": 0.8, "event": "nearest and second nearest kept"}],
    "ShaderLab with the loop highlighted", "Choosing a minimum among nine candidates is a picture of lines of different lengths; a drawing shows the competition.")
ABOUT["B16"] = "check the nine squares; keep the nearest and the second nearest"; EVID["B16"] = "Manim only; E7: 3 by 3 and 5 by 5 searches agree on the nearest distance at every pixel and on the edge at 99.86 % of pixels"

L["B17"] = capture(SL("side", S3, 27, 34, cues=[(0.20, 31, "length: of an offset, the distance"), (0.38, 32, None)],
        video="foam-nearest.mp4", vlabel=LAB + "top view · nearest distance", aspect=1.0, readouts=[(0.72, "mean 0.43", 0.5, 0.08)], caption="nearest distance, pale 0 to deep 1 of a square: a field of cones"),
    "C09: scene water_scene.gd, W_BARE top view, shader 03a-cells-debug show=1 (the nearest distance as a grey ramp), 1080 x 1080. mean 0.43 is E7 (evidence/planning-checks).",
    "Code card with the eight loop lines (length line then the keep-two line lit); at right a real top view: a field of soft cones, pale at every point and deepening away from it, slowly moving; the pill 'mean 0.43' lands near the end.",
    "A field of cones: pale at each point, deepening away from it, while the points circle.",
    [{"at": 0.2, "event": "length line"}, {"at": 0.38, "event": "keep-two line"}, {"at": 0.72, "event": "pill mean 0.43"}],
    "manim: cone cross-section plot", "The real nearest-distance field is the picture itself; a plot would describe one slice of it.")
ABOUT["B17"] = "the nearest distance as a field of cones; average 0.43"; EVID["B17"] = "C09; E7: mean nearest distance 0.429 of a square, max 1.042"

L["B18"] = capture(SL("side", S3, 35, 40, cues=[(0.30, 40, "c.y - c.x: second nearest minus nearest")],
        video="foam-edge.mp4", vlabel=LAB + "top view · edge distance", aspect=1.0, caption="second nearest minus nearest: zero on the border between two points"),
    "C10: scene water_scene.gd, W_BARE top view, shader 03a-cells-debug show=2 (second minus nearest as a ramp), 1080 x 1080.",
    "Code card (the cells return and the fragment's first lines, the foam line lit); at right a real top view: deep-blue cells whose borders are a thin pale net, moving as the points circle.",
    "Thin pale lines trace the borders between the cells and wobble as the points move.",
    [{"at": 0.3, "event": "c.y - c.x line"}, {"at": 0.6, "event": "net visible"}],
    "manim: two circles and their equal-distance line", "The real edge map is the shape foam will take; a drawing of two circles would show the idea but not the net.")
ABOUT["B18"] = "second nearest minus nearest is zero on the cell borders"; EVID["B18"] = "C10; lab-shaders/03a-cells-debug.gdshader show=2"

L["B19"] = capture(SL("side", S3, 38, 44, cues=[(0.20, 40, "smoothstep: eases from 0 to 1 between two edges"), (0.62, 41, "mix: blends from a to b; t of 0 gives a, 1 gives b")],
        video="foam-width.mp4", vlabel=LAB + "top view · width widens", aspect=1.0, readouts=[(0.86, "13 % foam", 0.5, 0.08)], caption="edge_width 0.02 widening to 0.1: foam covers about 13 % of the water"),
    "C11: scene water_scene.gd, W_BARE top view, shader 03-noise-foam, edge_width 0.02 widening to 0.1 by 75 % of the beat; the 13 % figure is E7.",
    "Code card (the fragment: foam line then ALBEDO line lit); at right the real top view of blue water whose thin pale lines swell into white foam bands as edge_width grows; the pill '13 % foam' lands at the end.",
    "Thin lines swell into white bands as the width grows, and settle at thirteen percent of the surface.",
    [{"at": 0.2, "event": "smoothstep line"}, {"at": 0.62, "event": "mix line"}, {"at": 0.86, "event": "pill 13 % foam"}],
    "ShaderLab ramp of edge_width", "The band widening on the real water is the claim, and the coverage number is measured from that same render.")
ABOUT["B19"] = "smoothstep widens the line to a band; mix paints foam; 13 percent coverage"; EVID["B19"] = "C11; E7: foam coverage 6.6 / 12.8 / 24.4 / 34.9 % at edge_width 0.05 / 0.1 / 0.2 / 0.3"

L["B20"] = capture(SL("side", S3, 41, 44, cues=[(0.25, 42, "alpha: 0 is invisible, 1 is solid"), (0.62, 43, "roughness: 0 is a mirror, 1 is fully matte")],
        video="foam-matte.mp4", vlabel=LAB + "scripted sweep", caption="foam_roughness 0.15 up to 0.9: the glare on the foam lines fades"),
    "C12: scene water_scene.gd, shader 03-noise-foam, foam_roughness swept 0.15 to 0.9 between 15 % and 85 % of the beat.",
    "Code card (ALBEDO, ALPHA, ROUGHNESS lines); the real cove: at first the foam lines streak with the sun's glare like wet paint, then as foam_roughness rises the streaks fade to flat white.",
    "The glare streaks along the foam lines die away as the foam turns matte.",
    [{"at": 0.25, "event": "ALPHA line"}, {"at": 0.62, "event": "ROUGHNESS line, streaks fading"}],
    "manim: a lobe on foam vs water", "The streaks fading on the real foam is the evidence; the sentence is about a visible artifact.")
ABOUT["B20"] = "foam is opaque and matte"; EVID["B20"] = "C12 foam-matte"

L["B21"] = capture(SL("side", S3, 28, 39, cues=[(0.18, 30, "o: where this square's point sits, circling"), (0.58, 39, "TIME: seconds on one clock shared by the whole game"), (0.80, 39, "density: how many squares fit across the plane")],
        video="foam-move.mp4", vlabel=LAB + "scripted sweep", caption="cell_speed 0 to 2, then cell_density 10 to 18"),
    "C13: scene water_scene.gd, shader 03-noise-foam, cell_speed swept 0 to 2 between 30 % and 60 %, then cell_density 10 to 18 from 62 % to the end.",
    "Code card (the point's offset line and the call line lit in turn); the real cove: the foam net frozen, then breathing faster, then the cells shrinking as the density rises.",
    "The net starts to breathe, speeds up, then the squares shrink.",
    [{"at": 0.18, "event": "the sine line"}, {"at": 0.35, "event": "speed rising"}, {"at": 0.8, "event": "density rising"}],
    "manim: a point circling in its square", "The real net breathing and tightening is the sentence's motion.")
ABOUT["B21"] = "the points circle with time; speed and density dials"; EVID["B21"] = "C13 foam-move"

L["B22"] = capture(SL("side", S3B, 33, 40, cues=[(0.30, 35, "pow: x raised to the power y")],
        video="power-curve.mp4", vlabel=LAB + "top view · power rises", aspect=1.0, readouts=[(0.10, "power 2", 0.5, 0.08), (0.90, "power 10", 0.5, 0.08)], caption="one minus the nearest distance, to a power: a soft dot per point"),
    "C14: scene water_scene.gd, W_BARE top view, shader 03b-power-curve (clamped), sharpness swept 2 to 10 across the beat, 1080 x 1080.",
    "Code card (the power-curve fragment, the pow line lit); the real top view of blue water with a soft white blob around every point that shrinks to a glitter dot as the power rises; pills 'power 2' then 'power 10'.",
    "Soft white blobs shrink into glitter as the power rises.",
    [{"at": 0.1, "event": "power 2"}, {"at": 0.3, "event": "pow line"}, {"at": 0.9, "event": "power 10"}],
    "manim: the curve of one minus d to the power p", "Two real hold frames of the render, linked by the sweep, show how the power sharpens; a plot would show the function only.")
ABOUT["B22"] = "a power curve sharpens the nearest distance into glitter"; EVID["B22"] = "C14 power-curve; lab-shaders/03b-power-curve.gdshader (clamped)"

L["B23"] = capture(SL("side", S3B, 35, 36, cues=[(0.20, 35, "pow of a negative base is undefined"), (0.62, 36, "clamp: pins x inside a range")],
        video="power-specks.mp4", vlabel=LAB + "top view · clamp at 55 %", aspect=1.0, readouts=[(0.30, "462 px", 0.5, 0.08)], rings=[(0.30, [0.165, 0.465, 0.245, 0.545])], caption="462 of 1,166,400 pixels read exactly black; with the clamp, none"),
    "C15: scene water_scene.gd, W_BARE top view, shader 03b-power-curve unclamped (sharpness 5, cell_speed 0 so the pattern is frozen and the specks stay put), clamped by --set-at at 55 % of the beat; 1080 x 1080. Ring box = the 258-pixel speck at (221, 545) of the 1080 x 1080 frame (evidence/planning-checks/png/pow-static-broken.png).",
    "Code card (the two glow lines; the unclamped line lit then the clamp line); the real top view with tiny black specks that blink in the first half and are gone after the clamp at 55 %; a terracotta ring around one speck at 30 % and the pill '88 px'.",
    "Black specks blink on the foam, then vanish when the clamp is applied.",
    [{"at": 0.2, "event": "unclamped line"}, {"at": 0.3, "event": "ring on a speck, pill 88 px"}, {"at": 0.55, "event": "clamp applied"}, {"at": 0.62, "event": "clamp line"}],
    "manim: a negative base on a number line", "A real speck on the real frame, ringed, with the real pixel count, is stronger than a diagram of why it happens.")
ABOUT["B23"] = "pow of a negative base is undefined: black specks; clamp"; EVID["B23"] = "C15; pow-static-broken vs pow-static-clamped stills (evidence/planning-checks/png): 462 black pixels (4 specks: 258, 167, 22, 15) vs 0; with moving points 88 black pixels in one frame; E7: nearest distance exceeds 1 at 0.035 % of pixels"

L["B24"] = capture(SL("stack", S3D, 15, 16, cues=[(0.25, 15, "texture: an image a shader can read by address")],
        video="foam-vs-texture.mp4", vlabel=LAB + "left: function · right: texture", aspect=2.0, readouts=[(0.35, "9 hashes", 0.25, 0.08), (0.35, "1 read", 0.75, 0.08)],
        rings=[(0.72, [0.595, 0.37, 0.735, 0.57])], caption="Cellular · fractal off · Seamless"),
    "C16: scene water_scene.gd, W_BARE top view, left: 03-noise-foam (function), right: 03d-foam-from-texture (a baked cellular NoiseTexture2D: Cellular, return Distance2 Sub, fractal type None, Seamless), both 1080 x 1080 joined side by side. The ring box [0.595, 0.37, 0.735, 0.57] is the smudged cross where the seamless blend shows, read off the recorded frame at 10.5 s (72 % of the estimated beat); the cross scrolls with the texture, so re-read it if the beat length changes by more than a second.",
    "Wide window with the two top views side by side: the function's crisp net (left) and the baked texture's net (right) with a visible smudge in the middle; code excerpt below (the two texture lines); pills '9 hashes' and '1 read'; a ring on the smudge.",
    "The two nets drift side by side; the right one scrolls rigidly and the cells never change shape.",
    [{"at": 0.25, "event": "texture cue"}, {"at": 0.35, "event": "pills 9 hashes, 1 read"}, {"at": 0.72, "event": "ring on the smudge"}],
    "manim: a texture tile and a function box", "Two real nets side by side are the comparison; the smudge is a real artifact the viewer can see.")
ABOUT["B24"] = "baked cellular texture: one read, cannot move its points, smudge at the blend"; EVID["B24"] = "C16 foam-vs-texture; facts3_cell_texture.gd (fractal None gives min 0.000, FBM default 0.004 and mush)"

# ═══════════════════════════════ ACT III · Ripples ═══════════════════════════════
L["B25"] = capture(SL("side", S4A, 15, 21, cues=[(0.40, 19, "normal map: an image of which way each pixel faces")],
        video="normal-strength.mp4", vlabel=LAB + "scripted sweep", title="Ripples", readouts=[(0.10, "strength 0", 0.5, 0.1), (0.90, "strength 1.5", 0.5, 0.1)], caption="ripple_strength 0 to 1.5 on one still normal map"),
    "C17: scene water_scene.gd, shader 04a-normal-map, ripple_strength swept 0 to 1.5 across the beat (one static normal map: a NoiseTexture2D, As Normal Map, Seamless).",
    "Act title 'Ripples'; code card (the 04a fragment, NORMAL_MAP lit); the real cove: first one big flat sun glare, then as the strength rises the glare breaks into thousands of small glints.",
    "One big glare breaks into glints as the strength rises.",
    [{"at": 0.1, "event": "strength 0, one glare"}, {"at": 0.4, "event": "NORMAL_MAP line"}, {"at": 0.9, "event": "strength 1.5, glints"}],
    "manim: light on a flat and a bumpy line", "The real glare breaking up is the claim; the drawing would only model it.")
ABOUT["B25"] = "a normal map gives each pixel its own direction; the glare breaks into glints"; EVID["B25"] = "C17 normal-strength; docs NORMAL_MAP rows"

L["B26"] = manim("B26_ColorIsDirection",
    "Left: the real normal map (captures/normal_a.png, 512 by 512, through lab_window) with two grey-backed rings on two pixels. Right: two swatches in the pixels' real colours: 'flat' (127, 127, 254) with an arrow pointing straight up, and 'leans' (124, 133, 254) with a slightly tilted arrow; a legend with three arrow shapes in the channel colours: 'left or right' (red), 'up or down' (green), 'upright' (blue); a number '13°' for the steepest pixel.",
    "The two arrows draw from the swatches (one upright, one tilted) as the voice says flat and leans; the legend arrows draw with red, green, blue.",
    [{"at": 0.2, "event": "the real image"}, {"at": 0.5, "event": "flat swatch and arrow"}, {"at": 0.7, "event": "leaning swatch and arrow, legend"}, {"at": 0.9, "event": "13 degrees"}],
    "ShaderLab still of the texture", "Colour-to-direction is a coding scheme; swatches next to arrows decode it, and the real texture proves the numbers.")
ABOUT["B26"] = "color is direction: flat is half, half, one; steepest lean 13 degrees"; EVID["B26"] = "facts2: flat mean (0.498, 0.498, 0.996); mean lean 3.4 deg, max 12.8 deg at bump 6; normal_a.png pixel (100,100) = (124, 133, 254)"

L["B27"] = manim("B27_Seamless",
    "Two real 2 by 2 tilings of the normal map side by side (captures/tiles-not-seamless.png labelled 'Seamless off', captures/tiles-seamless.png labelled 'Seamless on'), each with the tile-crossing lines marked by two thin grey lines; a ring on the visible jump in the left one. Under them the measured edge jump: '53 times a normal step' for off and 'about 1 time' for on; at the top the two switch names 'As Normal Map' and 'Seamless' as outlined chips.",
    "The two chips light; the ring appears on the left tiling's seam; the numbers land under each picture.",
    [{"at": 0.2, "event": "chips As Normal Map and Seamless"}, {"at": 0.55, "event": "ring on the seam"}, {"at": 0.8, "event": "numbers under each tiling"}],
    "ShaderLab with a tiling video", "The seam is a picture of an edge mismatch; two real tilings next to each other show it without a word of explanation.")
ABOUT["B27"] = "NoiseTexture2D makes the image; Seamless hides the tile edge"; EVID["B27"] = "facts2: normal map edge jump 0.353 vs 0.0067 neighbour step (53 times) not seamless; 0.0063 seamless; tiles-*.png"

L["B28"] = capture(SL("side", S4B, 9, 10, cues=[(0.30, 10, "hint_normal: the image holds directions, not colors"), (0.62, 10, "repeat_enable: the address may wrap past 1")],
        video="repeat-switch.mp4", vlabel=LAB + "repeat enabled at 55 %", caption="repeat_disable smears the edge pixels; repeat_enable wraps the picture"),
    "C19: scene water_scene.gd, shader 04e-no-repeat (repeat_disable) swapped at 55 % of the beat for 04b-scrolling-normals (repeat_enable), iso camera.",
    "Code card (the group and the sampler line lit twice); the real cove: first long smeared streaks of glare across most of the water, then at 55 % the streaks resolve into fine ripples.",
    "Long smeared streaks turn into fine ripples the instant repeat is enabled.",
    [{"at": 0.3, "event": "hint_normal label"}, {"at": 0.55, "event": "swap: streaks resolve"}, {"at": 0.62, "event": "repeat_enable label"}],
    "manim: a tile with clamped edges", "The smear is a visible bug; the real before and after proves what the hint does.")
ABOUT["B28"] = "hint_normal and repeat_enable; without repeat, edge pixels smear"; EVID["B28"] = "C19 repeat-switch; evidence stills repeat-disable/repeat-enable: 10.1 % of pixels differ by more than 10 of 255"

L["B29"] = capture(SL("side", S4B, 16, 23, cues=[(0.30, 20, "TIME: seconds on one clock shared by the whole game"), (0.75, 20, None)],
        video="scroll.mp4", vlabel=LAB + "live clock", caption="ripple_speed: how far the address moves each second"),
    "C20: scene water_scene.gd, shader 04b-scrolling-normals, iso camera, TIME runs from the capture start.",
    "Code card (the 04b fragment, the scrolled address line lit); the real cove: the glints drift steadily across the water in one direction.",
    "The whole glitter pattern drifts one way across the water.",
    [{"at": 0.3, "event": "the address line with TIME"}, {"at": 0.75, "event": "scale and speed"}],
    "manim: a window sliding over a tile", "The drifting glints are the result; a sliding window drawing would show the mechanism.")
ABOUT["B29"] = "add time to the address: the ripples slide"; EVID["B29"] = "C20 scroll"

L["B30"] = capture(SL("side", S4C, 17, 25, cues=[(0.25, 21, None), (0.40, 22, "the second layer: scaled 0.7, moving the other way"), (0.62, 23, "mix: blends from a to b; t of 0 gives a, 1 gives b")],
        video="two-layers.mp4", vlabel=LAB + "second layer at 50 %", caption="two normal maps, averaged: the repeat disappears"),
    "C21: scene water_scene.gd, shader 04b-scrolling-normals swapped at 50 % of the beat for 04c-two-layers, iso camera.",
    "Code card (the 04c fragment; the two address lines then the mix line lit); the real cove: one steadily drifting glint pattern, then after the swap the glints cross and shimmer with no single direction.",
    "A steady drift turns into crossing shimmer when the second layer arrives.",
    [{"at": 0.25, "event": "layer one address"}, {"at": 0.4, "event": "layer two address"}, {"at": 0.5, "event": "swap: crossing ripples"}, {"at": 0.62, "event": "mix line"}],
    "manim: two sliding windows", "The change from drift to shimmer is the claim and a real swap shows it; the drawing of two windows cannot.")
ABOUT["B30"] = "a second layer, scaled differently and moving the other way, averaged"; EVID["B30"] = "C21 two-layers"

L["B31"] = capture(SL("video", None, video="low-flat.mp4", vlabel=LAB + "low camera", readouts=[(0.62, "same row", 0.5, 0.676)], caption="the near edge is the same pixel row in every column (row 487 of 720)"),
    "C22: scene water_scene.gd, W_BARE low camera (1.1 m above the water, fov 30), shader 04d-warped-foam, plane NOT cut; the near edge was measured at row 487 of a 1280 x 720 frame in every column (evidence/planning-checks).",
    "The framed window shows a flat plane seen from just above the waterline: the glints and the foam net move across it, and the near and far edges stay ruler straight; a pill 'same row' sits on the near edge.",
    "Everything on the plane moves; its edge never does.",
    [{"at": 0.1, "event": "glints moving on a flat plane"}, {"at": 0.62, "event": "pill same row on the near edge"}],
    "manim: a straight line over a bumpy normal", "A real photograph-like render with a straight edge, measured to the pixel row, is the claim itself.")
ABOUT["B31"] = "a normal map changes the light, not the shape"; EVID["B31"] = "C22; evidence/planning-checks: near edge row 487 in every column (spread 0 px)"

L["B32"] = capture(SL("side", S4D, 48, 51, cues=[(0.30, 49, "warp: the foam's address, pushed along the lean"), (0.62, 50, None)],
        video="warp.mp4", vlabel=LAB + "scripted sweep", readouts=[(0.10, "warp 0", 0.5, 0.1), (0.90, "warp 0.4", 0.5, 0.1)], caption="warp_strength 0 to 0.4: the foam net bends with the ripples"),
    "C23: scene water_scene.gd, shader 04d-warped-foam, warp_strength swept 0 to 0.4 across the beat, iso camera.",
    "Code card (the warp lines lit); the real cove: a straight-edged foam net that bends and sloshes with the ripples as the warp rises.",
    "The foam lines bend and slosh as the warp rises.",
    [{"at": 0.1, "event": "warp 0: straight lines"}, {"at": 0.3, "event": "warp line"}, {"at": 0.9, "event": "warp 0.4: bent net"}],
    "manim: a grid bent by arrows", "The foam net bending on the real water is the result.")
ABOUT["B32"] = "shift the foam's address along the lean"; EVID["B32"] = "C23 warp"

L["B33"] = capture(SL("video", None, video="renderers-ripples.mp4", vlabel="left Forward+ · right Compatibility", aspect=2.0, readouts=[(0.30, "red 132", 0.25, 0.08), (0.30, "red 100", 0.75, 0.08)], caption="median red of the water, same shader, same clock: 132 against 100"),
    "C24: scene water_scene.gd, shader 04d-warped-foam, iso camera, recorded twice (Forward+ and Compatibility) at 1080 x 1080 and joined side by side. The medians (132, 163, 204 against 100, 158, 205) are E15, measured on a top view of the bare plane at the same clock (evidence/planning-checks/logs/e15-renderers-ripples.txt).",
    "Wide window: two identical scenes side by side, both moving on the same clock: left Forward+ (a lighter, greyer blue), right Compatibility (a deeper, more saturated blue); pills 'red 132' and 'red 100'.",
    "Both scenes ripple in step; the right one is a deeper blue.",
    [{"at": 0.1, "event": "both renders"}, {"at": 0.7, "event": "the warmer glints on the right"}],
    "manim: two swatches", "The side by side is the claim; no drawing is as convincing as the two real renders.")
ABOUT["B33"] = "the same shader in two renderers looks different"; EVID["B33"] = "C24 renderers-ripples (Forward+ left, Compatibility right); E15: median red 132 vs 100 on the same shader and clock"

# ═══════════════════════════════ ACT IV · Real Waves ═══════════════════════════════
L["B34"] = capture(SL("video", None, video="cuts-compare.mp4", vlabel=LAB + "low camera · same shader", aspect=2.0, title="Real Waves",
        readouts=[(0.35, "4 vertices", 0.25, 0.08), (0.60, "16,641 vertices", 0.75, 0.08)], caption="PlaneMesh: vertices = (cuts + 2) × (cuts + 2)"),
    "C25: scene water_scene.gd, W_BARE low camera, shader 05-vertex-waves (TIME): left an UNCUT plane, right cut 127 x 127; both 1080 x 1080 joined. Vertex counts are read from the mesh (facts1_classdb.gd: 4, 25, 4225, 16,641).",
    "Act title 'Real Waves'; two framed views of the same wave shader from just above the waterline: the uncut plane only tilts (straight edges), the cut plane rolls with real waves; pills '4 vertices' and '16,641 vertices'.",
    "The left plane tilts like a board; the right plane rolls like water.",
    [{"at": 0.35, "event": "pill 4 vertices"}, {"at": 0.6, "event": "pill 16,641 vertices"}],
    "manim: a dot grid counting up", "Two real planes with the same shader are the lesson; the count pills carry the numbers.")
ABOUT["B34"] = "cut the plane so it has vertices to move"; EVID["B34"] = "C25; facts1: PlaneMesh cuts 0 -> 4, 3 -> 25, 63 -> 4225, 127 -> 16,641 vertices"

L["B35"] = capture(SL("side", S5, 55, 60, cues=[(0.20, 55, "phase: position minus speed times time"), (0.65, 57, "sine: a smooth wave between -1 and 1"), (0.85, 59, "x: height · y, z: slope along x and z")],
        video="waves-low.mp4", vlabel=LAB + "low camera · live clock", caption="two waves, two directions, two lengths, added"),
    "C26: scene water_scene.gd, W_BARE low camera, shader 05-vertex-waves cut 127, TIME from the capture start.",
    "Code card with the last six lines of wave() (the phase line, the sine line and the return line lit in turn); the real low view of the plane with a lumpy rolling surface.",
    "Two waves of different lengths roll through each other.",
    [{"at": 0.2, "event": "phase line"}, {"at": 0.65, "event": "sine line"}, {"at": 0.85, "event": "return line"}],
    "manim: two sines adding", "The real rolling surface is the sum; the code beside it is the recipe.")
ABOUT["B35"] = "a wave is a sine of position minus speed times time; two of them"; EVID["B35"] = "C26 waves-low; lab-shaders/05-vertex-waves.gdshader wave()"

L["B36"] = capture(SL("side", S5, 62, 66, cues=[(0.30, 63, "TIME: seconds on one clock shared by the whole game"), (0.62, 64, "vertex(): runs once for each vertex; places the corners")],
        video="waves-iso.mp4", vlabel=LAB + "live clock", caption="one line moves 16,641 vertices; the card fills in between"),
    "C27: scene water_scene.gd, shader 05-vertex-waves cut 127, iso camera, TIME from the capture start; floaters not following (still).",
    "Code card (the vertex function; the wave call then the add-to-y line lit); the real cove with rolling waves: the shoreline against the beach wobbles, the floaters stay at y 0.",
    "The water surface rolls and the shoreline wobbles.",
    [{"at": 0.3, "event": "wave call line"}, {"at": 0.62, "event": "VERTEX.y line"}],
    "manim: vertices rising and falling", "The real rolling shoreline is the effect of the one line.")
ABOUT["B36"] = "vertex adds the height to y"; EVID["B36"] = "C27 waves-iso"

L["B37"] = capture(SL("side", S5B, 63, 67, cues=[(0.30, 66, "normal: a direction at right angles to a surface")],
        video="normal-swap.mp4", vlabel=LAB + "normal line added at 55 %", readouts=[(0.20, "old normal", 0.5, 0.1), (0.72, "new normal", 0.5, 0.1)], caption="the glare: one flat oval, then glints on the crests"),
    "C28: scene water_scene.gd, W_FOLLOW, shader 05c-no-normal-update (NORMAL line removed) swapped at 55 % for 05b-synced-clock; ripples and foam turned down (ripple_strength 0, edge_width 0.01) so the glare is the only light effect.",
    "Code card (the vertex function, NORMAL line lit); the real cove with rolling waves: first the sun's glare is one flat oval whatever the waves do, then after 55 % it breaks into glints along the crests; pills 'old normal' and 'new normal'.",
    "The one flat glare shatters into crest glints when the normal line arrives.",
    [{"at": 0.2, "event": "pill old normal, one oval"}, {"at": 0.3, "event": "NORMAL line"}, {"at": 0.55, "event": "swap: glints on crests"}, {"at": 0.72, "event": "pill new normal"}],
    "manim: normals drawn on a wave", "A real before and after of the same waves shows the light not knowing; a drawing of normals would explain the maths only.")
ABOUT["B37"] = "recompute the normal from the slope or the light stays flat"; EVID["B37"] = "C28; evidence/planning-checks/png/normal-missing2 vs normal-updated2"

L["B38"] = capture(SL("video", None, video="low-waves.mp4", vlabel=LAB + "low camera · script clock", readouts=[(0.62, "up to 95", 0.5, 0.74)], caption="near edge, lowest to highest row: up to 95 rows (flat plane: 0)"),
    "C29: scene water_scene.gd, W_BARE low camera, shader 05b-synced-clock cut 127, wave_clock from the script (W_FOLLOW); the 95-row figure is the maximum over the recorded clip (40 to 96 rows, mean 78, logs/edge-spread.txt) and the still (95).",
    "The framed window shows the plane from just above the waterline: the near edge is a rolling line; the pill 'up to 95' sits below it.",
    "The near edge of the water rolls up and down.",
    [{"at": 0.1, "event": "rolling near edge"}, {"at": 0.62, "event": "pill up to 95"}],
    "manim: a straight line and a wavy line", "The same camera as the flat plane two beats ago, now with an edge that bends: the contrast is real and measured.")
ABOUT["B38"] = "now the edge bends: real height, not lighting"; EVID["B38"] = "C29; the still: near edge rows 440 to 535 = 95 rows; the clip: spread 40 to 96 rows, mean 78 (logs/edge-spread.txt); flat: 0"

L["B39"] = capture(SL("side", WM, 4, 11, cues=[(0.30, 4, "the same two waves as the shader, in GDScript")],
        video="floaters.mp4", vlabel=LAB + "script clock", caption="a script sets each floater's height from the same function"),
    "C30: scene water_scene.gd, W_FOLLOW: water_driver.gd drives wave_clock and sets the buoy and the crate to WaveMath.height each frame; shader 05b, iso camera.",
    "Code card with the eight GDScript lines of the height function (first line lit); the real cove: the teal buoy and the cream crate rise and fall exactly with the waves.",
    "The buoy and the crate ride the crests and troughs.",
    [{"at": 0.3, "event": "height function lit"}, {"at": 0.6, "event": "buoy on a crest"}],
    "manim: a node and the invisible surface", "Floaters riding the real waves are the point; the code is the other half.")
ABOUT["B39"] = "the script runs the same function and places the floaters"; EVID["B39"] = "C30; water-project/scripts/wave_math.gd; E9: GPU and CPU heights agree to 3 mm"

L["B40"] = manim("B40_OneClock",
    "Two horizontal time lines labelled 'shader time' and 'script clock' with tick marks; the script's line starts later: a bracket between the two starts is labelled with the three measured gaps '0.32 s', '0.28 s', '0.31 s' (three of the six logged real-time runs, which ranged 0.28 to 0.32 s); then a box labelled 'wave_clock' (a uniform) receives an arrow from the script line, and the shader line is redrawn lined up with it; the final state shows both lines aligned with 'one number' between them.",
    "The script line slides to the right to show the gap, three gap labels appear one per run, then an arrow into the uniform box pulls the two lines into alignment.",
    [{"at": 0.2, "event": "two time lines"}, {"at": 0.5, "event": "gap bracket and three values"}, {"at": 0.8, "event": "uniform box and alignment"}],
    "ShaderLab with GDScript code", "Two clocks and a gap between them is a timeline diagram; the three measured offsets make it real.")
ABOUT["B40"] = "give the shader and the script one clock"; EVID["B40"] = "E10 (real-time runs): script clock minus shader TIME = 0.316, 0.281, 0.283 s (logs/e10-clock.txt) and 0.321, 0.308, 0.286 s (logs/e10-clock-rerun.txt)"

L["B41"] = capture(SL("side", WD, 16, 25, cues=[(0.30, 16, None), (0.56, 20, "wave_height: how tall"), (0.70, 21, "wave_length: how long"), (0.86, 22, "wave_speed: how fast")],
        video="wave-dials.mp4", vlabel=LAB + "script clock · scripted sweeps", readouts=[(0.25, "within 3 mm", 0.5, 0.1), (0.58, "height", 0.5, 0.1), (0.72, "length", 0.5, 0.1), (0.88, "speed", 0.5, 0.1)],
        caption="GPU and script heights agree to 3 mm on waves 192 mm tall"),
    "C31: scene water_scene.gd, W_FOLLOW, shader 05b: the driver's wave_height, wave_length and wave_speed are swept one after another between 56 % and 95 % of the beat; the 3 mm agreement is E9 (evidence/planning-checks).",
    "Code card (the driver's set_clock lines; the three uniform writes lit one by one); the real cove: the waves grow taller, then longer, then faster, with the floaters still riding them; pills 'within 3 mm', 'height', 'length', 'speed'.",
    "Height, length and speed are swept in turn and the buoy keeps riding.",
    [{"at": 0.25, "event": "pill within 3 mm"}, {"at": 0.56, "event": "height sweep"}, {"at": 0.7, "event": "length sweep"}, {"at": 0.86, "event": "speed sweep"}],
    "ShaderLab ramp per dial", "Three sweeps on the real water show what each dial changes.")
ABOUT["B41"] = "GPU and CPU agree to 3 mm; three wave dials"; EVID["B41"] = "C31; E9: rms 0.95 mm, max 3.1 mm on a 192 mm peak"

# ═══════════════════════════════ ACT V · The Shore ═══════════════════════════════
L["B42"] = manim("B42_DepthTexture",
    "Act title 'The Shore' (serif 40) top-left. A side-on diagram on the cream stage: a small camera icon at the left, a horizontal blue line for the water surface, a sand line below it; one view ray runs from the camera through the surface to the sand. Two labelled distances along the ray: 'water 6.0 m' and 'floor 6.5 m'. A box labelled 'depth texture' sits above and holds a single value '6.5 m' fed from the floor point; a crossed-out grey arrow from the surface point to the box is labelled 'not in it'. The numbers are the measured test geometry (FACTCHECK).",
    "The ray draws from the camera, a dot marks each hit, only the floor value flows into the box, and the water's arrow is struck out.",
    [{"at": 0.2, "event": "camera and ray"}, {"at": 0.5, "event": "floor value into the box"}, {"at": 0.78, "event": "water arrow struck out"}],
    "ShaderLab: a depth image render", "Which surfaces are in the buffer is a diagram of a ray; the measured 6.0 and 6.5 metre numbers make it exact.")
ABOUT["B42"] = "the depth texture holds the solid scene; the water is not in it"; EVID["B42"] = "E8: camera 6 m above the water, floor 0.5 m below: gap read 0.500 m, so the depth texture held the floor (6.5 m) and not the water (6.0 m); docs advanced post-processing, depth texture"

L["B43"] = capture(SL("side", S6, 73, 82, cues=[(0.22, 74, "depth: near is 1, far is 0, and not a distance"), (0.62, 80, "inverse projection: the screen point back to view space"), (0.80, 81, "flip z: the camera looks down minus z")],
        video="gap-view.mp4", vlabel=LAB + "gap view", caption="white where the solid scene is close under the water"),
    "C32: scene water_scene.gd, shader 06a-gap-view (unshaded gap map: white = close under the water), uncut plane, iso camera.",
    "Code card with the ten lines of scene_depth (depth, inverse projection and the sign flip lit in turn); the real cove drawn as a map: blue water with white along the beach's edge, around the rocks and under the floaters.",
    "White glows along every place where the solid scene is close under the water.",
    [{"at": 0.22, "event": "depth line"}, {"at": 0.62, "event": "inverse projection line"}, {"at": 0.8, "event": "z flip line"}],
    "manim: the matrix multiply as boxes", "The real gap map shows the result of the recipe; the code beside it is the recipe.")
ABOUT["B43"] = "turn the depth value into a distance"; EVID["B43"] = "C32; docs advanced post-processing (depth texture recipe); lab-shaders/06a-gap-view.gdshader"

L["B44"] = capture(SL("stack", S6, 92, 92, cues=[(0.30, 92, "gap: how far the water is above what lies under it")],
        video="gap-test.mp4", vlabel=LAB + "top-down test", aspect=16 / 9, readouts=[(0.10, "0.2 m", 0.25, 0.1), (0.58, "0.9 m", 0.25, 0.1), (0.76, "0.5 m", 0.25, 0.1)], caption="measured gap equals the floor's depth: 0.200, 0.902, 0.500 m (Forward+)"),
    "C33: scene gap_scene.gd, a plate wearing 06a-gap-view over a floor under its left half; the floor height steps 0.2 m, then 0.9 m, then 0.5 m (G_STEPS); measured gap (e8-depth-gap): 0.200, 0.500, 0.902 m on Forward+ (evidence/planning-checks/logs/e8b-gap-three-heights.txt).",
    "Wide window, a camera straight down on a plate: the left half over a floor goes from bright (floor close) to dark (floor deep) to mid as the floor moves; the right half over nothing stays dark; pills '0.2 m', '0.9 m', '0.5 m'; one code line below.",
    "The left half brightens and darkens as the floor rises and sinks, and the number follows.",
    [{"at": 0.1, "event": "pill 0.2 m"}, {"at": 0.58, "event": "pill 0.9 m"}, {"at": 0.76, "event": "pill 0.5 m"}],
    "manim: a number line with the gap", "A real test with three exact heights and the measured gap equal to each is the proof of the formula.")
ABOUT["B44"] = "subtract the water's own distance: the gap"; EVID["B44"] = "C33; E8b: gap 0.200 / 0.500 / 0.902 m (Forward+), 0.18 / 0.494 / 0.902 m (Compatibility, with the branch)"

L["B45"] = {"lane": "terminal", "pattern": "CCPlainShell", "props": {"title": "Godot 4.7.2 · six one-line helper shaders · same compiler", "lines": ["TRANSCRIPT"], "startCue": 10, "lineGap": 12, "fontSize": 36, "windowMargin": 90,
    "durationSeconds": "__AUDIO__"},
    "visual_intent": "A plain terminal card whose lines are the verbatim output of a script that compiled six one-line helper shaders on Godot 4.7.2: TIME and TAU compile, UV, VERTEX, SCREEN_UV and INV_PROJECTION_MATRIX each give 'Unknown identifier in expression'; a ring on the first failing line.",
    "motion_claim": "The six result lines print one after another; the first failure line is ringed.", "show": [{"at": 0.15, "event": "TIME and TAU compile"}, {"at": 0.6, "event": "the identifiers that fail"}],
    "runner_up": "ShaderLab with the real engine error block", "why": "A terminal's printed lines are the honest place for a compile result; six lines show the rule better than one error.", "sparse": False}
ABOUT["B45"] = "built-ins live in their own function: pass them in"; EVID["B45"] = "e12_builtins.sh transcript (evidence/planning-checks/logs/e12-transcript.txt); engine block e12-builtin-in-helper-engine-log.txt"

L["B46"] = capture(SL("side", S6, 89, 94, cues=[(0.25, 91, "reach: wider where the nearest point is far"), (0.60, 93, "shore: 1 right at the contact, fading to 0"), (0.80, 94, "max: the larger of two values")],
        video="shore-width.mp4", vlabel=LAB + "scripted sweep", ramp={"at": 0.0, "from": 0.05, "to": 1.0}, caption="shore_width 0.05 to 1.0: the white edge widens along the shore"),
    "C34: scene water_scene.gd, W_FOLLOW, shader 06-shore-foam cut 127, shore_width swept 0.05 to 1.0 across the beat, iso camera.",
    "Code card (the six lines that make the shore band; reach, shore and max lit in turn); the real finished cove: a thin white edge along the beach and around the rock and the floaters that widens into a ragged band as shore_width grows.",
    "The white edge along the shore widens into a ragged band.",
    [{"at": 0.25, "event": "reach line"}, {"at": 0.6, "event": "shore line"}, {"at": 0.8, "event": "max line, band widest"}],
    "manim: gap thresholds on a profile", "The ragged band on the real shore is the result; the drawing would hide the scalloping.")
ABOUT["B46"] = "foam where the gap is small; reach wider where the nearest cell point is far"; EVID["B46"] = "C34 shore-width"

L["B47"] = capture(SL("side", S6, 74, 79, cues=[(0.25, 75, "CURRENT_RENDERER: which renderer is running")],
        video="compat-branch.mp4", vlabel="Godot 4.7.2 · Compatibility · branch removed at 66 %", caption="without the branch the gap reads 0.000 everywhere: all foam (measured)"),
    "C35: scene water_scene.gd, renderer gl_compatibility, shader 06-shore-foam swapped at 66 % of the beat for 06b-no-renderer-branch; the 0.000 reading is E8 (evidence/planning-checks/logs/e8-compat-direct-decode.txt).",
    "Code card (the six depth lines; the preprocessor line lit); the real cove in Compatibility: foam only along the shore, then after 66 % the whole surface washes to white foam.",
    "The whole surface washes to white foam when the renderer branch goes.",
    [{"at": 0.25, "event": "CURRENT_RENDERER line"}, {"at": 0.66, "event": "swap: all foam"}],
    "manim: two NDC ranges as bars", "The washed-out cove is the failure in the real renderer it fails in.")
ABOUT["B47"] = "Compatibility counts depth from minus one to one: one preprocessor line"; EVID["B47"] = "C35; E8: Compatibility gap 0.494 m with the branch, 0.000 m without; docs advanced post-processing"

L["B48"] = capture(SL("video", None, video="editor-inspector.png", vlabel="Godot 4.7.2 · scripted editor session", aspect=1920 / 1080, caption="the six group_uniforms folders; they replace the Shader Parameters header"),
    "C38: the series editor driver (editor-capture/) in a scratch copy of water-project/: scenes/water.tscn open in the real Godot 4.7.2 editor, Water selected, its Material Override's ShaderMaterial opened, all six folders unfolded (state script capture-scenes/editor-states/water-W.json, mark W2-all); the Inspector dock cut from the NATIVE 3456 x 1944 frame (1300 x 1849) so the scratch FileSystem dock is not shown; labelled 'scripted editor session'. The uncropped frame is captures/editor-inspector.png.",
    "The real Godot editor's Inspector (a tall portrait crop) showing the water's ShaderMaterial: folders Color, Clarity, Foam, Ripples, Waves, Shore; colour swatches for Water Color and Foam Color; number boxes with a thin slider bar for the ranged floats; two texture slots for Normal A and Normal B.",
    "The real Inspector holds still while the voice names the folders and the widget types.",
    [{"at": 0.2, "event": "the folder names"}, {"at": 0.65, "event": "sliders and pickers"}],
    "GodotDevWorkbench reconstruction (labelled)", "The viewer will recreate this panel in their own editor, so it must be the real one; the reconstruction would have been the labelled fallback.")
ABOUT["B48"] = "group uniforms make Inspector folders; sliders and pickers"; EVID["B48"] = "C38 editor frames (captures/editor/, EDITOR-LABELS.md): W2-all; water-project/scenes/water.tscn"

L["B49"] = capture(SL("video", None, video="restyle.mp4", vlabel=LAB + "same shader, three sets of numbers", aspect=3.0,
        readouts=[(0.15, "Lagoon", 0.17, 0.08), (0.32, "Pond", 0.5, 0.08), (0.58, "Storm", 0.83, 0.08)], caption="one shader · only the numbers differ"),
    "C36: scene water_scene.gd, shader 06-shore-foam, W_FOLLOW, three recordings (Lagoon, Pond, Storm) at 1080 x 1080 joined side by side; the parameter sets are in captures.py.",
    "Three framed views side by side of the same finished cove: Lagoon (clear turquoise, fine foam, small waves), Pond (dark green, nearly opaque, no foam), Storm (grey, tall fast waves, thick foam); labels land under each name as the voice says it.",
    "Three different waters move side by side from one shader.",
    [{"at": 0.15, "event": "Lagoon"}, {"at": 0.32, "event": "Pond"}, {"at": 0.58, "event": "Storm"}],
    "manim: a table of three parameter sets", "Three real renders are the payoff; the numbers behind them are in CAPTURE-PLAN.md.")
ABOUT["B49"] = "three looks from one shader"; EVID["B49"] = "C36 restyle"

# ═══════════════════════════════ write ═══════════════════════════════
ACT_OF = {}
for i, rng in enumerate([(1, 12), (13, 24), (25, 33), (34, 41), (42, 49)]):
    for n in range(rng[0], rng[1] + 1):
        ACT_OF[f"B{n:02d}"] = i + 1

# the B45 terminal lines come from the real transcript if it exists
tr = R / "evidence/planning-checks/logs/e12-transcript.txt"
if tr.exists():
    L["B45"]["props"]["lines"] = tr.read_text().rstrip("\n").split("\n")
    # scaled from 14s design to measured 12.78s: keep all 7 lines before 45% (frame 130/306) and ring after 55%
    L["B45"]["props"]["lineCues"] = [10, 57, 73, 90, 103, 117, 130][:len(L["B45"]["props"]["lines"])]
    L["B45"]["props"]["rings"] = [{"line": 3, "cue": 265}]

(R / "lanes").mkdir(exist_ok=True)
for act in range(1, 6):
    d = {k: v for k, v in L.items() if ACT_OF[k] == act}
    (R / "lanes" / f"act{act}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")

spec_n = importlib = None
import importlib.util
spec = importlib.util.spec_from_file_location("narration", R / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
hist = {}
for k, v in L.items():
    hist[v["lane"]] = hist.get(v["lane"], 0) + 1
rows = []
for bid, ai, text in N.BODY:
    v = L[bid]
    if v["lane"] == "manim":
        lane = f"manim · {v['class']}"
    elif v["lane"] == "capture":
        lane = "capture · ShaderLab"
    elif v["lane"] == "terminal":
        lane = "terminal · CCPlainShell"
    else:
        lane = f"remotion · {v['pattern']}"
    rows.append(f"| {bid} | {ABOUT[bid]} | {lane} | {v['runner_up']} | {v['why']} | {EVID[bid]} |")
head = f"""# Shot list: {N.TITLE}

**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.

**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code. Every picture of water is a real Godot 4.7.2 render of a shader in `lab-shaders/` (or a scene built by `capture-scenes/` and `water-project/scripts/`); the drawings are labelled as drawings.

**Found.** {len(N.BODY)} body beats. Lane histogram: {', '.join(f'{k} {v}' for k, v in sorted(hist.items(), key=lambda kv: -kv[1]))}. The capture share is high because most claims are about what Godot draws, and the router sends a real shader's result to `ShaderLab`. Nothing in the film is a mock of Godot's output: the only reconstruction, if the editor frame fails, is a labelled `GodotDevWorkbench` card for B48.

## Must exist before the build

1. **`ShaderLab`** (Remotion, exists: `brutalist.art/runtime/remotion/src/scenes/ShaderLab.tsx`), **`shader_kit.py`** (Manim kit, exists: `_godot-shaders-series/shader_kit.py`), the capture harness (exists: `_godot-shaders-series/lab/`). This film adds nothing to them.
2. The captures in `captures/` (this folder; recorded in the Cowork stage at 1080p at ESTIMATED durations): the build re-records any capture whose measured beat differs by more than half a second (`python3 captures.py --only C..`; see `CAPTURE-PLAN.md`).
3. The Manim scenes (`scenes_act1.py` to `scenes_act5.py`, ten classes, written in the layout stage and checked with `preflight.sh`).

## Rows

| beat | about | lane picked | runner-up | why this one wins | evidence / capture |
|---|---|---|---|---|---|
"""
(R / "SHOTLIST.md").write_text(head + "\n".join(rows) + "\n")
print("lanes written; histogram", hist)

#!/usr/bin/env python3
"""_gen_lanes.py: the single source for this film's lanes/*.json AND SHOTLIST.md (the pilot's way).

Why a generator: the code shown on screen must be the tested file text, and the shot list must say exactly what the lanes say.
Re-run after any edit:   python3 _gen_lanes.py && python3 make_sheet.py
Every capture named below is recorded from evidence/planning-checks/scratch-project/capture_scenes.gd (custom scenes) or from the Shader Lab (single sprite);
see CAPTURE-PLAN.md. Code cards show the real shader text (or, for GDScript, the exact lines run in the planning checks).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SH = HERE / "lab-shaders"
E = []          # entries in beat order


def code_of(fn):
    return (SH / fn).read_text().rstrip("\n")


def add(bid, act, about, entry, evidence=""):
    E.append({"bid": bid, "act": act, "about": about, "evidence": evidence, "entry": entry})


def manim(bid, act, about, cls, intent, motion, show, runner, why, evidence="Manim only (shader_kit objects)"):
    add(bid, act, about, {"lane": "manim", "class": f"{bid}_{cls}", "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": True}, evidence)


def lab(bid, act, about, shader, video, label, cues, intent, motion, show, runner, why, spec, evidence, layout="side",
        readouts=None, rings=None, ramp=None, title=None, code=None, code_file=None, lane="capture", caption=""):
    props = {"layout": layout, "code": code if code is not None else (code_of(shader) if shader else ""),
             "codeFile": code_file or (f"lab-shaders/{shader}" if shader else ""), "cues": cues,
             "video": video, "videoLabel": label, "readouts": readouts or [], "rings": rings or [], "caption": caption,
             "durationSeconds": "__AUDIO__"}
    if title:
        props["title"] = title
    if ramp:
        props["ramp"] = ramp
    add(bid, act, about, {"lane": lane, "pattern": "ShaderLab", "props": props, "capture_spec": spec, "visual_intent": intent,
                          "motion_claim": motion, "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


def rem(bid, act, about, lane, pattern, props, intent, motion, show, runner, why, evidence):
    add(bid, act, about, {"lane": lane, "pattern": pattern, "props": props, "visual_intent": intent, "motion_claim": motion,
                          "show": show, "runner_up": runner, "why": why, "sparse": False}, evidence)


SCENES = "evidence/planning-checks/scratch-project/capture_scenes.gd"
SCRIPTED = "Godot 4.7.2 · Apple M4 Pro · Forward+ · scripted: shader switched on mid-beat"

# ───────────────────────────── ACT I · Corners ─────────────────────────────
lab("B01", 0, "a waving flag, before any code", "11-flag-final.gdshader", "vertex-shaders/flag-final.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [],
    "Act title 'Corners' (serif 40) top-left. A real Godot render in a framed window on the cream stage: a cream and teal checker flag pinned to a grey pole waves smoothly with its folds lit, in a seamless loop. Label: 'live clock'.",
    "The flag is already waving on the first frame: the ripple travels along it while the pole end stays still.",
    [{"at": 0.0, "event": "flag waving, window labelled"}, {"at": 0.6, "event": "the same loop keeps running"}],
    "manim drawing of a waving flag", "A real render is the honest picture of what a vertex shader does; a drawing would only claim it.",
    f"C01: scene `final` of {SCENES}: a MeshInstance2D with a QuadMesh 384 x 168 cut 31 x 7 (297 vertices), cream and teal checker texture of 16 x 7 cells, a grey pole beside the left edge, shader lab-shaders/11-flag-final.gdshader from the first frame; canvas 1280 x 720; record 252 frames (8.4 s: four wave periods at speed 3, so the loop seam is under 1 % of a period out), 30 fps, Forward+, no input.",
    "Lab compile of 11-flag-final; planning frames png/scene-final-t3.00.png", layout="video", title="Corners")
manim("B02", 0, "vertex() runs once for each corner", "FourCorners",
      "A rectangle on the cream stage with a terracotta dot on each corner. The dots flash one after another, each with a counter 1, 2, 3, 4 and a small 'where?' tag; then the four dots slide to new places and the rectangle follows as a leaning parallelogram. Caption in the GLOSSARY wording: 'vertex(): runs once for each vertex; places the corners'.",
      "Each corner flashes in turn with its count, then the shape follows the four moved corners.",
      [{"at": 0.1, "event": "rectangle with four terracotta dots"}, {"at": 0.3, "event": "dots flash in order, counter 1 to 4"}, {"at": 0.65, "event": "dots slide; shape follows; caption"}],
      "ShaderLab with a Lab render", "The count of four is the claim; four flashes in turn is the count, and the drag shows what the answer does.")
manim("B03", 0, "VERTEX: a built-in that goes in and comes out", "InAndOut",
      "A box labelled vertex(). A terracotta dot labelled VERTEX (monospace) arrives from the left at the corner (-64, -64), passes through the box where the line `VERTEX.x += 40.0;` is shown, and leaves on the right at (-24, -64). Caption in the GLOSSARY wording: 'built-in: a value the engine hands to a function'.",
      "The dot goes in, the line acts on it, and a moved dot comes out the other side.",
      [{"at": 0.12, "event": "box and the line of code"}, {"at": 0.3, "event": "dot arrives at (-64, -64)"}, {"at": 0.65, "event": "dot leaves at (-24, -64); caption"}],
      "LectureCodeTrace with the line highlighted", "In and out is a flow; a dot that visibly changes on its way through says it with motion.")
manim("B04", 0, "VERTEX counts pixels from the middle; y points down", "PixelsFromTheMiddle",
      "A 128 by 128 square with a small cross at its middle and two axis arrows drawn as shapes: x to the right, y pointing DOWN. The four corners get labels in turn: (-64, -64) top left, (64, -64) top right, (-64, 64) bottom left, (64, 64) bottom right; a scale bar '128 px'. Small grey credit: 'measured in Godot 4.7.2 · Forward+'.",
      "Corner labels land one by one; the y arrow points down and the top corners carry the minus sign.",
      [{"at": 0.1, "event": "square, cross, axes"}, {"at": 0.3, "event": "corner labels land in order"}, {"at": 0.7, "event": "y arrow pointing down is ringed"}],
      "ShaderLab: Lab render coloured by VERTEX", "That render needs a varying the film has not taught yet; the drawing, with numbers confirmed by the Lab probes, says it plainly.",
      "Lab probes c1-vertex-local: corners read as -64 and +64 at scale 1.0 and at the Lab's 2.25 scale")
lab("B05", 0, "add forty to x: every corner moves, the square slides", "01-slide.gdshader", "vertex-shaders/slide.mp4", SCRIPTED,
    [{"at": 0.2, "lines": [4]}],
    "Code card at left with the one line `VERTEX.x += 40.0;` highlighted; at right a real Godot window (640 by 360): the 128 px checker square sits still, then jumps 40 px to the right as the voice says 'add forty to x' (the shader switches on at 22 % of the beat). A terracotta ring on its new left edge, readout '+40 px'.",
    "The square sits still, then slides forty pixels the moment the shader switches on.",
    [{"at": 0.2, "event": "the VERTEX line highlighted"}, {"at": 0.24, "event": "square slides 40 px"}, {"at": 0.4, "event": "ring on the new left edge; +40 px"}],
    "manim", "A real slide measured to the pixel; a drawing could only illustrate it.",
    f"C02: scene `slide` of {SCENES} (canvas 640 x 360): Sprite2D, checker 128 px at scale 1.0, centred; lab-shaders/01-slide.gdshader assigned at 0.22 of the beat; record from 0 to the event plus 1.5 s and hold the last frame; 30 fps; Forward+. Measured: left edge 256 -> 296.",
    "Lab 01-slide-white (box 256..383 -> 296..423)", readouts=[{"at": 0.4, "text": "+40 px", "x": 0.72, "y": 0.8}], rings=[{"at": 0.4, "box": [0.43, 0.3, 0.5, 0.7]}])
lab("B06", 0, "the forty is local: a scaled node moves farther on screen", "01-slide.gdshader", "vertex-shaders/local.mp4", SCRIPTED,
    [{"at": 0.15, "lines": [4]}],
    "Same code card. At right, two real Godot squares side by side: one at its own size, one scaled to twice its size, both given the same `VERTEX.x += 40.0` at 52 % of the beat. The small one jumps 40 px, the large one 80 px. Readouts '40 px' and '80 px' under them; label 'same shader'.",
    "Both squares jump at the same instant; the large one travels twice as far.",
    [{"at": 0.15, "event": "same line highlighted"}, {"at": 0.62, "event": "both jump; readouts: 40 px, 80 px"}],
    "manim", "Two real nodes, one shader, two distances: the proof that VERTEX is counted before the node's scale.",
    f"C03: scene `local` of {SCENES} (canvas 640 x 360): two Sprite2D checker squares, scale 1.0 at x 130 and scale 2.0 at x 380; 01-slide on both at 0.52 of the beat; record to the event plus 1.5 s, then hold. Measured: left edge moved 40 px (scale 1.0), 80 px (scale 2.0), 90 px (Lab default scale 2.25).",
    "Lab 01-slide-white-scale2 (+80) and -scale2.25 (+90)", readouts=[{"at": 0.62, "text": "40 px", "x": 0.2, "y": 0.9}, {"at": 0.62, "text": "80 px", "x": 0.6, "y": 0.9}])
lab("B07", 0, "multiply: corners move away from the middle", "02-squash.gdshader", "vertex-shaders/squash.mp4", SCRIPTED,
    [{"at": 0.2, "lines": [4]}],
    "Code card at left with `VERTEX *= vec2(1.5, 0.5);` highlighted; at right a real Godot window: the 128 px square, still, then at 35 % of the beat stretches to 192 px wide and flattens to 64 px tall about its middle. Readout '192×64 px'.",
    "The square stretches wide and flattens about its own middle when the shader switches on.",
    [{"at": 0.2, "event": "VERTEX line highlighted"}, {"at": 0.42, "event": "square squashes; readout 192×64 px"}],
    "manim", "A real squash measured to the pixel (width 192, height 64, centred); a drawing could only illustrate it.",
    f"C04: scene `squash` of {SCENES} (canvas 640 x 360): Sprite2D checker 128 px at scale 1.0; 02-squash at 0.35 of the beat; record to the event plus 1.5 s, then hold. Measured box 192 x 64, centre unchanged.",
    "Lab 02-squash-white (box 224..415 x 148..211)", readouts=[{"at": 0.42, "text": "192×64 px", "x": 0.5, "y": 0.8}])
manim("B08", 0, "UV: each corner's address, 0 to 1", "Address",
      "The same square, now with BOTH numberings at each corner in two rows: pixels from the middle (-64, -64) and address (0, 0), then (64, -64)/(1, 0), (-64, 64)/(0, 1), (64, 64)/(1, 1). A terracotta dot visits the corners. Caption in the GLOSSARY wording: 'UV: a point's address on the shape: 0 to 1 across, 0 to 1 down'.",
      "A dot visits the four corners and the address row of numbers lands beside each pixel row.",
      [{"at": 0.1, "event": "square with pixel labels"}, {"at": 0.3, "event": "address labels land in turn"}, {"at": 0.7, "event": "top left (0, 0) and bottom right (1, 1) ringed; caption"}],
      "ShaderLab: Lab render coloured by UV", "Two ways to say where one corner is is a naming claim; both labels on one square show it at a glance.",
      "Lab probes c1-vertex-local: blue (UV.x) reads 0.02 at the left edge, 0.98 at the right")
lab("B09", 0, "scale a move by the address: the square leans", "03-lean.gdshader", "vertex-shaders/lean.mp4", SCRIPTED,
    [{"at": 0.2, "lines": [4]}],
    "Code card at left with `VERTEX.x += 50.0 * UV.y;` highlighted; at right a real Godot window: the 128 px checker square, still, then at 72 % of the beat it leans: the bottom edge slides 50 px right while the top stays. A terracotta ring on the bottom edge, readout '+50 px'.",
    "The square shears sideways when the shader switches on: top corners stay, bottom corners go fifty pixels.",
    [{"at": 0.2, "event": "VERTEX line highlighted"}, {"at": 0.74, "event": "square leans"}, {"at": 0.8, "event": "ring on the bottom edge; +50 px"}],
    "manim", "A real shear measured to the pixel; the line and its result together are the whole lesson.",
    f"C05: scene `lean` of {SCENES} (canvas 640 x 360): Sprite2D checker 128 px at scale 1.0; 03-lean at 0.72 of the beat; record to the event plus 1.5 s, then hold. Measured left edge 256 -> 306 (+50 px over 128 rows).",
    "Lab 03-lean-white (left edge 256 -> 306)", readouts=[{"at": 0.8, "text": "+50 px", "x": 0.72, "y": 0.8}], rings=[{"at": 0.8, "box": [0.4, 0.62, 0.72, 0.7]}])
manim("B10", 0, "four corners give straight edges, in even steps", "EvenSteps",
      "The leaning square's left edge drawn as a slanted line with five sample dots along it, labelled with the measured shifts +1, +12, +25, +37 and +49 px (rows 2, 31, 63, 95 and 124 of 128). A caption: 'four corners: straight edges'. Small grey credit: 'Apple M4 Pro · Godot 4.7.2 · Forward+ · straight to within half a pixel'.",
      "The five dots land one after another down the edge, each with its measured number, evenly spaced.",
      [{"at": 0.14, "event": "slanted edge"}, {"at": 0.35, "event": "five dots with numbers, in order"}, {"at": 0.72, "event": "caption and credit"}],
      "ShaderLab with readouts", "The even spacing of five real measurements is the proof that nothing was calculated between the corners.",
      "evidence/planning-checks/measurements.txt: lean edge x = 257, 268, 281, 293, 305 from 256; straight within 0.49 px")

# ───────────────────────────── ACT II · More Corners ─────────────────────────────
lab("B11", 1, "four corners are enough when the whole shape moves as one", None, "vertex-shaders/triptych.mp4", SCRIPTED, [],
    "Act title 'More Corners' (serif 40) top-left. Three real Godot squares in a row: the left slides, the middle squashes, the right leans, all switched on together at 12 % of the beat, as the three words are said. One word under each: slide, squash, lean.",
    "Three squares change at once, each by its own one-line shader.",
    [{"at": 0.1, "event": "three plain squares, window labelled"}, {"at": 0.3, "event": "slide, squash and lean at once; one-word labels"}],
    "manim: three drawn squares", "Three real results at once is the claim: whole-shape moves need nothing but the four corners.",
    f"C06: scene `triptych` of {SCENES} (canvas 640 x 360): three Sprite2D checker squares at x 130, 320, 510; shaders 01-slide, 02-squash, 03-lean at 0.12 of the beat; record to the event plus 1.5 s, then hold.",
    "Lab 01, 02, 03 renders (same values)", layout="video", title="More Corners",
    readouts=[{"at": 0.3, "text": "slide", "x": 0.2, "y": 0.85}, {"at": 0.3, "text": "squash", "x": 0.5, "y": 0.85}, {"at": 0.3, "text": "lean", "x": 0.8, "y": 0.85}])
lab("B12", 1, "a ripple on four corners: it only tilts", "04-ripple.gdshader", "vertex-shaders/tilt.mp4", SCRIPTED,
    [{"at": 0.2, "lines": [4]}],
    "Code card at left with `VERTEX.y += sin(UV.x * 8.0) * 24.0;` highlighted; at right a real Godot window: a cream and teal checker flag (four corners), flat for a moment, then at 58 % of the beat its right end drops 24 px and every edge stays straight: a tilt, not a ripple. Terracotta ring on the right end, readout '+24 px'. Caption: 'sine: a smooth wave between -1 and 1'.",
    "The flag does not ripple: its right end drops and the whole shape tilts, edges straight.",
    [{"at": 0.2, "event": "the ripple line highlighted"}, {"at": 0.6, "event": "right end drops"}, {"at": 0.66, "event": "ring and +24 px"}],
    "manim", "The failure is the lesson and a real render shows it honestly; a drawing could be accused of rigging it.",
    f"C07: scene `tilt` of {SCENES}: Sprite2D flag 384 x 168 (four vertices), canvas 1280 x 720; 04-ripple assigned at 0.58 of the beat; record to the event plus 1.5 s, then hold. Measured on the Lab's 128 px sprite: right end +24 px (sin 8 x 24 = 23.7), top and bottom edges straight to within 0.49 px.",
    "Lab 04-ripple-white (top edge 116 -> 140, straight within 0.49 px)", caption="sine: a smooth wave between -1 and 1",
    readouts=[{"at": 0.66, "text": "+24 px", "x": 0.8, "y": 0.78}], rings=[{"at": 0.66, "box": [0.7, 0.35, 0.86, 0.7]}])
manim("B13", 1, "vertex can only move the vertices that exist", "OnlyWhatExists",
      "A sine curve on a grid. Two terracotta vertex dots at its ends joined by a straight chord (label '2 vertices'); then dots are added at 3, 5 and 9 positions and the chord becomes a polyline hugging the curve (labels '3', '5', '9 vertices'). A caption: 'vertex moves only the vertices that exist'.",
      "More dots appear along the curve and the straight chord bends into a polyline that follows it.",
      [{"at": 0.12, "event": "curve and a two-dot chord"}, {"at": 0.32, "event": "dots added; polyline follows the curve"}, {"at": 0.7, "event": "caption"}],
      "ShaderLab with the tilted flag", "The relation between the number of vertices and the shape they can draw is a plot, and a plot shows the chord turning into a curve.")
manim("B14", 1, "two ways to get more vertices", "TwoWays",
      "Two panels on the cream stage. Left: a polygon outline whose points appear one at a time as if placed by hand, label 'Polygon2D: you place the points'. Right: a rectangle cut by grid lines into small cells with a dot at every crossing, label 'MeshInstance2D: a mesh cut into a grid'. Caption in the GLOSSARY wording: 'mesh: the vertices and triangles that make a shape'.",
      "Points appear one by one on the left while the right-hand rectangle is cut into a grid.",
      [{"at": 0.1, "event": "two empty panels with labels"}, {"at": 0.3, "event": "points placed; grid lines cut"}, {"at": 0.7, "event": "mesh caption"}],
      "GodotDevWorkbench scene tree (labelled reconstruction)", "A structure with two branches is a diagram; the reconstruction would show node names but not the vertices, which are the point.")
lab("B15", 1, "the recipe: a quad mesh cut into a grid", None, "vertex-shaders/mesh-recipe.mp4", "Godot 4.7.2 · Forward+ · cuts raised by script · dots = the mesh's vertices",
    [{"at": 0.1, "lines": [2]}, {"at": 0.62, "lines": [3, 4]}],
    "Code card at left with five GDScript lines (quad mesh, size, subdivide width, subdivide depth, assign to the node); at right a real Godot window: a 320 px checker square drawn by a MeshInstance2D with terracotta dots on the mesh's vertices: four dots, then nine as the cuts go to one, then twenty-five as they go to three. Readouts '4 vertices', '9 vertices', '25 vertices'.",
    "Dots multiply on the square as the cuts are raised: four, nine, twenty-five.",
    [{"at": 0.1, "event": "size line highlighted; four dots"}, {"at": 0.62, "event": "cuts to 1: nine dots"}, {"at": 0.82, "event": "cuts to 3: twenty-five dots"}],
    "LectureCodeTrace alone", "The code and the vertices it creates side by side: the dots are the vertices, so the idea becomes countable.",
    f"C08: scene `mesh-recipe` of {SCENES} (canvas 1280 x 720): MeshInstance2D with a QuadMesh 320 x 320, checker texture, subdivide width and depth 0 -> 1 at 0.6 of the beat -> 3 at 0.8 of the beat; a child Node2D draws a terracotta dot at every vertex of the mesh (read from surface_get_arrays); 12 s.",
    "verify1.gd 1a: 0x0 -> 4, 1x1 -> 9, 3x3 -> 25 vertices; verify12.gd: the five lines as shown give 25 vertices, 32 triangles",
    code='var mesh := QuadMesh.new()\nmesh.size = Vector2(320, 320)\nmesh.subdivide_width = 3\nmesh.subdivide_depth = 3\n$Quad.mesh = mesh',
    code_file="scene script (GDScript)", caption="MeshInstance2D: the node that draws a mesh in 2D",
    readouts=[{"at": 0.12, "text": "4 vertices", "x": 0.5, "y": 0.92}, {"at": 0.62, "text": "9 vertices", "x": 0.5, "y": 0.92}, {"at": 0.82, "text": "25 vertices", "x": 0.5, "y": 0.92}])
manim("B16", 1, "counting vertices: always two more than the cuts", "CountThem",
      "A 5 by 5 grid of terracotta dots appears row by row with a running counter up to 25, labelled 'cut 3 by 3'. Beside it the formula '(cuts + 2) x (cuts + 2)'. Then the flag's 33 by 9 grid, drawn small, with its counter ending at 297, labelled 'cut 31 by 7'. Small grey credit: 'counted from the mesh in Godot 4.7.2'.",
      "Dots appear row by row while the counter climbs to twenty-five, then the larger grid counts to two hundred ninety-seven.",
      [{"at": 0.1, "event": "5 by 5 grid counts to 25"}, {"at": 0.35, "event": "formula lands"}, {"at": 0.7, "event": "33 by 9 grid counts to 297"}],
      "LectureEvidenceTable", "A count is a motion: dots appearing while a number climbs; a table would only list the results.",
      "verify1.gd 1a: (w+2) x (d+2) = 4, 9, 25, 18, 18, 441, 297 vertices read from the mesh arrays")
lab("B17", 1, "same ripple on four vertices and on 297", None, "vertex-shaders/pair.mp4", SCRIPTED, [],
    "Two real Godot flags side by side on the stage, the same cream and teal checker texture and the same `VERTEX.y += sin(UV.x * 8.0) * 24.0;` switched on at 10 % of the beat. Left: four vertices, the flag tilts. Right: 297 vertices, the flag ripples. Readouts '4 vertices' and '297 vertices'; label 'same shader on both'.",
    "Both flags get the same one line at the same instant; the left one tilts, the right one ripples.",
    [{"at": 0.1, "event": "two plain flags, readouts"}, {"at": 0.3, "event": "shader on: left tilts, right ripples"}],
    "manim: two drawn flags", "The single most convincing frame of the film: one shader, two shapes, two results, both real.",
    f"C09: scene `pair` of {SCENES}: left Sprite2D flag 384 x 168 at x 340, right MeshInstance2D QuadMesh 384 x 168 cut 31 x 7 at x 940; 04-ripple on both at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold.",
    "Lab 04-ripple-white (left) and the mesh frame png/scene-pair-t3.00.png", layout="video",
    readouts=[{"at": 0.3, "text": "4 vertices", "x": 0.27, "y": 0.9}, {"at": 0.3, "text": "297 vertices", "x": 0.73, "y": 0.9}])
lab("B18", 1, "the smoothness depends on the pieces; a rule of thumb", None, "vertex-shaders/densities.mp4", "Godot 4.7.2 · Apple M4 Pro · Forward+ · scripted: ripple switched on mid-beat · gaps measured at 3x zoom", [],
    "Three real Godot flags in a row, the same ripple switched on at 10 % of the beat, cut into 4, 10 and 32 straight pieces (subdivide width 3, 9 and 31, depth 0). The first shows every joint, the second softens them, the third has none. Readouts under them: '11 px gap', '2 px gap', 'under 1 px'. Caption: 'measured worst gap · 8 pieces per wave: about 8 % of the wave's height'.",
    "Three flags ripple at once; the joints are plain to see on the left and gone on the right.",
    [{"at": 0.1, "event": "three plain flags"}, {"at": 0.3, "event": "ripple on: joints visible on the left only"}, {"at": 0.75, "event": "readouts and caption"}],
    "manim sine with polylines", "Real flags with measured gaps are the evidence; the formula 1 - cos(pi / pieces per wave) is checked against them.",
    f"C10: scene `densities` of {SCENES}: three MeshInstance2D QuadMesh 288 x 126 at x 215, 640, 1065 with subdivide width 3, 9, 31 and depth 0; 04-ripple on all at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold. Measured at 3x zoom: worst gap 10.8, 2.0 and 0.35 px (formula 11.0, 1.9, 0.2).",
    "verify11.gd + analyze_densities.py: 10.76, 1.99, 0.35 px", layout="video", caption="measured worst gap · 8 pieces per wave: about 8 % of the wave's height",
    readouts=[{"at": 0.75, "text": "11 px gap", "x": 0.17, "y": 0.92}, {"at": 0.75, "text": "2 px gap", "x": 0.5, "y": 0.92}, {"at": 0.75, "text": "under 1 px", "x": 0.83, "y": 0.92}])
lab("B19", 1, "cut only where it bends: 297 vertices and 66 draw the same picture", None, "vertex-shaders/cut-along.mp4", SCRIPTED, [],
    "Two real Godot flags side by side, the same ripple on at 10 % of the beat: left cut 31 by 7 (297 vertices), right cut 31 by 0 (66 vertices). They look identical. Readouts '297 vertices' and '66 vertices'; a caption 'identical, pixel for pixel'.",
    "The two flags ripple in the same way and cannot be told apart.",
    [{"at": 0.1, "event": "two plain flags with vertex counts"}, {"at": 0.3, "event": "ripple on; they match"}, {"at": 0.75, "event": "caption: identical"}],
    "manim: a grid with the unused rows greyed", "Real renders that match pixel for pixel are a stronger statement than a diagram of why they should.",
    f"C11: scene `cut-along` of {SCENES}: left QuadMesh 384 x 168 cut 31 x 7 at x 340, right the same cut 31 x 0 at x 940; 04-ripple on both at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold. Measured: 0 differing pixels of 288,000.",
    "pixel diff of the two flags: 0 differing pixels", layout="video", caption="identical, pixel for pixel",
    readouts=[{"at": 0.3, "text": "297 vertices", "x": 0.27, "y": 0.9}, {"at": 0.3, "text": "66 vertices", "x": 0.73, "y": 0.9}])
lab("B20", 1, "a Polygon2D with outline points only twists the picture", None, "vertex-shaders/polygon.mp4", SCRIPTED, [],
    "Two real Godot flags side by side, the same ripple on at 10 % of the beat. Left: a Polygon2D with 66 points around its outline; the outline ripples but the checker inside twists along crossing lines. Right: the 297-vertex mesh, clean. A terracotta ring on the twisted crossing lines; readouts 'Polygon2D · 66 points' and 'mesh · 297 vertices'.",
    "Both outlines ripple, but the left flag's inside twists along long diagonal lines.",
    [{"at": 0.1, "event": "two plain flags with labels"}, {"at": 0.3, "event": "ripple on: left twists"}, {"at": 0.7, "event": "ring on the twisted lines"}],
    "manim: triangles drawn over the polygon", "The twist is something you see; a drawn fan of triangles would explain it but not prove Godot does it.",
    f"C12: scene `polygon` of {SCENES}: left Polygon2D with 66 outline points (33 on top, 33 on the bottom) and uv in texture pixels, right QuadMesh 31 x 7; 04-ripple on both at 0.1 of the beat; canvas 1280 x 720; record to the event plus 1.5 s, then hold. Verified: 64 triangles from Geometry2D.triangulate_polygon, one point in 34 of them, longest edge 419 px; the default render equals those triangles pixel for pixel; a grid of points with a cell list (polygons) equals the mesh pixel for pixel.",
    "verify5.gd 5c, verify8.gd (0 differing pixels), scene polygon-grid (0 differing pixels)", layout="video",
    readouts=[{"at": 0.3, "text": "66 points", "x": 0.27, "y": 0.9}, {"at": 0.3, "text": "297 vertices", "x": 0.73, "y": 0.9}], rings=[{"at": 0.7, "box": [0.12, 0.3, 0.42, 0.72]}])

# ───────────────────────────── ACT III · A Waving Flag ─────────────────────────────
lab("B21", 2, "let the ripple travel with time", "05-flag-travelling.gdshader", "vertex-shaders/travel.mp4",
    "Godot 4.7.2 · Forward+ · live clock · scripted: shader switched on at 58 % of the beat",
    [{"at": 0.56, "lines": [4]}],
    "Act title 'A Waving Flag' (serif 40) top-left. Code card at left with `VERTEX.y += sin(UV.x * 8.0 - TIME * 3.0) * 24.0;` highlighted; at right a real Godot window: the mesh flag on a grey pole shows the static ripple, then at the 58 % mark the ripple starts to slide to the right. Caption in the GLOSSARY wording: 'TIME: seconds on one clock shared by the whole game'.",
    "A frozen ripple starts to travel to the right along the flag, the left end bobbing with it.",
    [{"at": 0.1, "event": "static ripple, pole; caption TIME"}, {"at": 0.56, "event": "TIME line highlighted"}, {"at": 0.7, "event": "the ripple travelling right"}],
    "manim sine plot with a phase marker", "A ripple that starts to move on the real flag is the claim; the plot would only describe the phase.",
    f"C13: scene `travel` of {SCENES}: MeshInstance2D flag (QuadMesh 384 x 168 cut 31 x 7) with a grey pole at the left edge; 04-ripple from the start, 05-flag-travelling assigned at 0.58 of the beat; canvas 1280 x 720; record the whole beat (D) and hold. Verified: the wave moves right as TIME grows (fitted phase advanced with the clock; mean error 0.25 px).",
    "flag_motion.py: fitted TIME advances +0.2 s per 0.2 s; wave fits sin(8u - 3T) to 0.25 px", caption="TIME: seconds on one clock shared by the whole game", title="A Waving Flag")
lab("B22", 2, "pin one end: multiply by the address across", "06-flag-pinned.gdshader", "vertex-shaders/pinned.mp4",
    "Godot 4.7.2 · Forward+ · live clock · scripted: shader switched at 30 % of the beat",
    [{"at": 0.28, "lines": [4]}],
    "Code card at left with `VERTEX.y += sin(UV.x * 8.0 - TIME * 3.0) * 24.0 * UV.x;` and the final `* UV.x` highlighted; at right a real Godot window: the travelling flag bobs at its left end as well; at the 30 % mark the new line goes on and the left end, beside the grey pole, stops moving while the rest keeps rippling. A terracotta ring on the left edge, readout 'pinned'.",
    "The left edge stops moving the moment the multiplication goes on; the rest of the flag keeps waving.",
    [{"at": 0.15, "event": "unpinned flag bobbing"}, {"at": 0.4, "event": "UV.x factor highlighted"}, {"at": 0.7, "event": "left edge still, ring and pinned"}],
    "manim", "A real flag losing its flapping at the pole end is the picture of 'held at one end'.",
    f"C14: scene `pinned` of {SCENES}: the mesh flag with pole; 05-flag-travelling from the start, 06-flag-pinned assigned at 0.3 of the beat; canvas 1280 x 720; record the whole beat (D) and hold. Verified: the left edge's top row stays at y = 276 in every frame.",
    "flag_motion.py: left-edge top y = 276 in all pinned frames; the unpinned left end bobs between 256 and 300", readouts=[{"at": 0.7, "text": "pinned", "x": 0.16, "y": 0.8}], rings=[{"at": 0.7, "box": [0.15, 0.3, 0.25, 0.65]}])
lab("B23", 2, "three dials: amplitude, frequency, speed (uniforms)", "07-flag-dials.gdshader", "vertex-shaders/dials-rest.mp4",
    "Godot 4.7.2 · Forward+ · live clock · the three values at their defaults",
    [{"at": 0.2, "lines": [3]}, {"at": 0.3, "lines": [4]}, {"at": 0.4, "lines": [5]}, {"at": 0.62, "lines": [3, 4, 5]}],
    "Code card at left with the three uniform lines highlighted in turn (amplitude, frequency, speed); at right the real waving flag on its pole, at the defaults. Caption in the GLOSSARY wording: 'uniform: a value your game sets from outside; every pixel sees the same one'. Three small labels as each line lands: how tall, how many waves fit, how fast.",
    "The three uniform lines light up in turn while the flag keeps waving.",
    [{"at": 0.2, "event": "amplitude line"}, {"at": 0.3, "event": "frequency line"}, {"at": 0.4, "event": "speed line"}, {"at": 0.62, "event": "caption: uniform"}],
    "LectureCodeTrace alone", "The dial is a line of code and a real result: the flag beside the line that gives it a dial.",
    f"C15: scene `dials-rest` of {SCENES}: the mesh flag with pole; 07-flag-dials from the first frame, uniforms at their defaults (24, 8, 3); canvas 1280 x 720; record 252 frames (8.4 s, four wave periods) and loop them.",
    "Lab 07-flag-dials-white (compile); uniforms read amplitude, frequency, speed", caption="uniform: a value your game sets from outside; every pixel sees the same one",
    readouts=[{"at": 0.2, "text": "how tall", "x": 0.3, "y": 0.88}, {"at": 0.3, "text": "how many waves", "x": 0.5, "y": 0.88}, {"at": 0.4, "text": "how fast", "x": 0.7, "y": 0.88}])
lab("B24", 2, "turn each dial and watch what changes", "07-flag-dials.gdshader", "vertex-shaders/sweeps.mp4",
    "Godot 4.7.2 · Forward+ · values swept by script, one dial at a time",
    [{"at": 0.04, "lines": [3]}, {"at": 0.36, "lines": [4]}, {"at": 0.68, "lines": [5]}],
    "Code card at left (the same nine lines); at right the real flag as amplitude is swept up and back, then frequency, then speed, each with a label naming the dial: 'amplitude', 'frequency', 'speed'. Captions in plain words: 'how tall', 'how many waves fit', 'how fast'.",
    "Each dial moves in turn and only the property its name says changes.",
    [{"at": 0.04, "event": "amplitude swept: taller, flat, back"}, {"at": 0.36, "event": "frequency swept: more waves, fewer, back"}, {"at": 0.68, "event": "speed swept: faster, stopped, back"}],
    "ShaderLab stills", "Motion of the flag under three sweeps is the point; stills could not show 'faster'.",
    f"C16: scene `sweeps` of {SCENES}: the mesh flag with pole and 07-flag-dials; amplitude 24 -> 40 -> 0 -> 24 over 0.03 to 0.28 of the beat, frequency 8 -> 16 -> 2 -> 8 over 0.34 to 0.60, speed 3 -> 8 -> 0 -> 3 over 0.66 to 0.92 (all smoothstep, scripted via set_shader_parameter); canvas 1280 x 720; 12 s.",
    "Lab 07-flag-dials-amplitude0: amplitude 0 gives a flat top edge", readouts=[{"at": 0.04, "text": "amplitude", "x": 0.5, "y": 0.9}, {"at": 0.36, "text": "frequency", "x": 0.5, "y": 0.9}, {"at": 0.68, "text": "speed", "x": 0.5, "y": 0.9}])
lab("B25", 2, "the game turns a dial while it runs", None, "vertex-shaders/wind.mp4", "Godot 4.7.2 · Forward+ · scripted: the call fires at 75 % of the beat",
    [{"at": 0.3, "lines": [1]}],
    "One-line GDScript card at left, `$Flag.material.set_shader_parameter(\"amplitude\", 40.0)`, highlighted when the call fires; at right the real flag at its defaults, then waves taller from the moment of the call. Readout 'amplitude 40'.",
    "The flag's waves grow taller in the frame after the highlighted call fires.",
    [{"at": 0.3, "event": "the call highlighted"}, {"at": 0.76, "event": "waves grow"}, {"at": 0.8, "event": "readout"}],
    "LectureCodeTrace", "The cause (one line of game code) and the effect (a taller flag) together.",
    f"C17: scene `wind` of {SCENES}: the mesh flag with pole and 07-flag-dials; material.set_shader_parameter(\"amplitude\", 40.0) at 0.75 of the beat; canvas 1280 x 720; record the whole beat (D).",
    "ShaderMaterial docs 4.7 (set_shader_parameter); verify13.gd: the call as shown moves the top edge from the amplitude-24 formula to the amplitude-40 formula within 1 px",
    code='$Flag.material.set_shader_parameter("amplitude", 40.0)', code_file="scene script (GDScript)",
    readouts=[{"at": 0.8, "text": "amplitude 40", "x": 0.5, "y": 0.9}])
lab("B26", 2, "read the whole shader as one", "07-flag-dials.gdshader", "vertex-shaders/dials-rest.mp4", "Godot 4.7.2 · Forward+ · live clock",
    [{"at": 0.08, "lines": [3, 4, 5]}, {"at": 0.3, "lines": [8]}, {"at": 0.72, "lines": [8]}],
    "The nine-line shader on a code card at left; the three uniform lines highlighted as 'three dials' is said, then the single `VERTEX.y += ...` line held while the voice walks through its parts; at right the real flag waves on its pole.",
    "Focus lands on the three dials, then on the one line that moves the flag, while the flag waves.",
    [{"at": 0.08, "event": "uniform lines"}, {"at": 0.3, "event": "the one wave line"}, {"at": 0.72, "event": "the same line: one of nine"}],
    "manim: the line split into labelled parts", "The whole shader is nine lines and fits on screen with its result; nothing teaches the finish faster.",
    f"C15 again (the same recording as B23): scene `dials-rest` of {SCENES}, 07-flag-dials at its defaults.",
    "Lab 07-flag-dials-white: nine lines, three uniforms")

# ───────────────────────────── ACT IV · Passing Data Forward ─────────────────────────────
manim("B27", 3, "fragment runs later and never sees the corners", "FragmentCannotSee",
      "Act title 'Passing Data Forward' (serif 40) top-left. A three-stage strip left to right: 'vertex()' with four terracotta corner dots, 'the card fills the shape', 'fragment()' drawn as a pixel grid. A small question mark leaves fragment() looking back for the corners and stops at a pane of glass. Caption in the GLOSSARY wording: 'fragment(): runs once for each pixel the shape covers; sets its color'.",
      "A question mark travels back from fragment toward the corners and stops at the glass.",
      [{"at": 0.1, "event": "three stages with the act title"}, {"at": 0.35, "event": "question travels back and stops at the glass"}, {"at": 0.7, "event": "caption: fragment()"}],
      "DesignPipelineClaim, show-tell isometric", "A strip with a barrier is the claim 'it never sees the corners'; the motion is the question stopping at the glass.")
manim("B28", 3, "a varying: set at the corners, blended, read in fragment", "Varying",
      "A quad with a number on each corner dot (0 at the left corners, 1 at the right ones). The numbers flow right into the filled quad and blend into a smooth ramp as an arrow labelled 'forward' passes from 'set in vertex()' to 'read in fragment()'. Caption in the GLOSSARY wording: 'varying: a value set at each corner, blended across the shape for fragment() to read'.",
      "The corner numbers flow into the quad and spread into a smooth ramp, in the forward direction only.",
      [{"at": 0.1, "event": "quad with corner numbers"}, {"at": 0.32, "event": "values blend across the quad; forward arrow"}, {"at": 0.7, "event": "caption: varying"}],
      "LectureCodeTrace with the three lines", "A value that is set at points and spreads across a surface is a picture of blending; code alone would hide the spreading.")
lab("B29", 3, "four corner colours, one smooth blend (exact at the middle of an edge)", "08-corner-colors.gdshader", "vertex-shaders/corner-colors.png",
    "Godot 4.7.2 · Apple M4 Pro · Forward+ (Compatibility reads the same) · the shader on the left", [{"at": 0.08, "lines": [6]}, {"at": 0.3, "lines": [10]}],
    "Code card at left (varying tint, set in vertex, read in fragment); at right a real Godot window showing a square blended from blue (top left), red (top right), cyan (bottom left) and yellow (bottom right). Readouts above its top edge: 'red 0', 'red 0.5', 'red 1'.",
    "The corner colours blend; the readouts land along the top edge as the voice says one half.",
    [{"at": 0.08, "event": "tint set in vertex"}, {"at": 0.3, "event": "fragment reads it"}, {"at": 0.75, "event": "readouts along the top edge"}],
    "manim", "The picture itself is the evidence of the blend; the probe values (0, 0.5, 1) make 'exact' checkable.",
    "C18: Lab rect/sprite still: `check_shader.sh lab-shaders/08-corner-colors.gdshader --kind sprite --sprite-tex white` (default fit scale), PNG 1920 x 1080 by the harness. Probes (Forward+ and Compatibility agree): top left (0.02, 0.02, 0.98), top right (0.98, 0.02, 0.02), middle of the top edge (0.50, 0.02, 0.50), centre (0.50, 0.50, 0.50).",
    "Lab 08-corner-colors (+ gl_compatibility): middle of the top edge red 0.502",
    readouts=[{"at": 0.75, "text": "red 0", "x": 0.28, "y": 0.05}, {"at": 0.75, "text": "red 0.5", "x": 0.5, "y": 0.05}, {"at": 0.75, "text": "red 1", "x": 0.72, "y": 0.05}])
lab("B30", 3, "flat: no blending, each triangle keeps one corner's value", "09-corner-colors-flat.gdshader", "vertex-shaders/flat-mesh.png",
    "Godot 4.7.2 · Forward+ · the same colours on a mesh cut 7 by 7, smooth on the left, flat on the right", [{"at": 0.15, "lines": [3]}],
    "Code card at left with the one changed line `varying flat vec3 tint;` highlighted; at right two real Godot meshes cut 7 by 7: on the left the smooth four-colour blend, on the right the same colours with flat, broken into diagonal tiles, one per triangle. Labels 'smooth' and 'flat'. Caption: 'flat: the value is not blended'.",
    "The smooth blend on the left breaks into tiles on the right as the flat line is highlighted.",
    [{"at": 0.15, "event": "the flat line highlighted"}, {"at": 0.6, "event": "labels smooth and flat"}],
    "manim: two triangles with flat colours", "The tiles are the triangles: a real mesh shows them, and a drawing of two triangles could not show 'one per triangle'.",
    f"C19: scene `flat-mesh` of {SCENES}: two MeshInstance2D QuadMesh 300 x -300 (size.y negative, so UV.y runs down the screen and the colours sit as on the Lab sprite) cut 7 x 7 with a white texture; 08-corner-colors on the left, 09-corner-colors-flat on the right; still PNG; canvas 1280 x 720. Verified: a four-vertex sprite with flat shows ONE colour (the first vertex's) on both triangles; a QuadMesh 0 x 0 has 6 indices, i.e. two triangles.",
    "Lab 09-corner-colors-flat (sprite: one colour); verify1.gd 1a (0x0: 6 indices = 2 triangles)", caption="flat: the value is not blended",
    readouts=[{"at": 0.6, "text": "smooth", "x": 0.27, "y": 0.92}, {"at": 0.6, "text": "flat", "x": 0.73, "y": 0.92}])
manim("B31", 3, "UV and the color are varyings the engine passes for you", "BuiltInVaryings",
      "Top: a 0 to 1 ramp strip with two terracotta corner dots (0 and 1), the values between them filling in, labelled 'U V: set at the corners, blended'. Below: a small tinted block times a checker picture equals a tinted checker, labelled 'color from vertex x the picture = color in fragment'. Caption: 'COLOR: the color being drawn'.",
      "The ramp fills in between its two corner values, then the tint multiplies the picture.",
      [{"at": 0.1, "event": "ramp with two corner dots"}, {"at": 0.32, "event": "values fill in between"}, {"at": 0.7, "event": "tint times picture equals tinted picture"}],
      "LectureEvidenceTable", "Two parallel facts as motion: a ramp filling in and a multiplication landing, each a still-frame failure if shown as text.",
      "c4-uv-passes-through (Lab: a UV changed in vertex() reaches fragment(), blended: 0.008 left, 0.490 right, 0.251 middle); verify6.gd 6 (color in vertex x modulate)")
lab("B32", 3, "light the folds with a varying", "10-flag-lit.gdshader", "vertex-shaders/lit.mp4",
    "Godot 4.7.2 · Forward+ · live clock · scripted: lit version switched on at 62 % of the beat",
    [{"at": 0.12, "lines": [3, 6, 8], "label": "phase: where the wave is · fold: how the cloth slopes"}, {"at": 0.56, "lines": [12]}],
    "Code card at left (thirteen lines: varying fold, set in vertex, used in fragment); at right the real flag on its pole: first flat-looking, then at the 62 % mark the folds darken where the cloth slopes away. Highlight on the `phase` and `fold` lines as 'pass it as a varying' is said, with a rendered tag 'phase: where the wave is · fold: how the cloth slopes', then on the fragment line. Caption in the GLOSSARY wording: 'slope: how steeply a line rises: up divided by across'.",
    "The flag looks flat, then its folds read as folds when the lit shader goes on.",
    [{"at": 0.12, "event": "varying and the line that sets it"}, {"at": 0.56, "event": "the fragment line that uses it"}, {"at": 0.7, "event": "lit flag"}],
    "manim", "The lit flag against the flat one is the payoff of passing data forward, and only a real render shows cloth.",
    f"C20: scene `lit` of {SCENES}: the mesh flag with pole; 06-flag-pinned from the start, 10-flag-lit assigned at 0.62 of the beat; canvas 1280 x 720; record the whole beat (D).",
    "Lab 10-flag-lit-checker (compile); planning frames png/scene-lit-*.png",
    layout="side", caption="slope: how steeply a line rises: up divided by across")
lab("B33", 3, "the shorter way: the color already travels forward", "11-flag-final.gdshader", "vertex-shaders/flag-final.mp4",
    "Godot 4.7.2 · Forward+ · live clock", [{"at": 0.3, "lines": [10]}],
    "Code card at left (eleven lines: the three dials, the phase, the wave line and one `COLOR.rgb *= ...` line, no varying and no fragment function) with the COLOR line highlighted; at right the same real lit flag as the opening, waving. Readout 'same picture'.",
    "The COLOR line is highlighted while the flag waves, lit exactly as before.",
    [{"at": 0.3, "event": "COLOR line highlighted"}, {"at": 0.7, "event": "readout: same picture"}],
    "manim: the two shaders side by side with a diff", "The proof is the finished flag next to eleven lines; the pixel diff (zero) is in the fact-check.",
    f"C01 again (the same recording as the opening): scene `final` of {SCENES}, 11-flag-final from the first frame. Verified: the explicit-varying version (10) and this one draw the same picture, 0 differing pixels (scene equiv-lit-color).",
    "scene equiv-lit-color: 0 differing pixels; verify6.gd 6 (color in vertex)", readouts=[{"at": 0.7, "text": "same picture", "x": 0.5, "y": 0.92}])
lab("B34", 3, "a varying is only as detailed as the corners", "12-stripes-from-vertex.gdshader", "vertex-shaders/stripes.png",
    "Godot 4.7.2 · Forward+ · two four-corner squares, same stripes, computed in two places", [{"at": 0.2, "lines": [6]}, {"at": 0.62, "lines": [6]}],
    "Code card at left (the stripes computed in vertex and passed as a varying) with the sine line highlighted; at right two real Godot squares on four corners: the left shows plain flat grey, the right shows six clear stripes. Labels 'in vertex()' and 'in fragment()'.",
    "The left square stays plain grey while the right one shows six stripes.",
    [{"at": 0.2, "event": "sine line highlighted"}, {"at": 0.62, "event": "labels: in vertex(), in fragment()"}],
    "manim: sampled sine with two end values", "Two real squares, one plain and one striped, are the claim; the numbers (both corners compute zero) are in the fact-check.",
    f"C21: scene `stripes` of {SCENES}: two Sprite2D white squares at scale 3.0 (12-stripes-from-vertex on the left, 13-stripes-from-fragment on the right); still PNG; canvas 1280 x 720. Measured (Lab): the vertex version reads 0.749 at every probe; the fragment version reads 0.58 to 0.92.",
    "Lab 12-stripes-from-vertex (0.749 everywhere) and 13-stripes-from-fragment (0.58 to 0.92)",
    readouts=[{"at": 0.62, "text": "in vertex()", "x": 0.27, "y": 0.92}, {"at": 0.62, "text": "in fragment()", "x": 0.73, "y": 0.92}])

# ───────────────────────────── ACT V · When It Looks Wrong ─────────────────────────────
lab("B35", 4, "a QuadMesh draws upside down in 2D until its size.y is negative", None, "vertex-shaders/flip.mp4",
    "Godot 4.7.2 · Forward+ · scripted: size.y made negative at 60 % of the beat", [{"at": 0.62, "lines": [1]}],
    "Act title 'When It Looks Wrong' (serif 40) top-left. One-line GDScript card at left, `mesh.size = Vector2(256, -256)`, highlighted when it runs; at right two real Godot pictures of the same blob with two eyes: a sprite on the left (eyes up) and a quad mesh on the right drawn upside down (eyes down) that flips upright at the moment the size goes negative. Labels 'sprite' and 'quad mesh'.",
    "The mesh picture flips to stand upright the moment its size.y goes negative, matching the sprite.",
    [{"at": 0.1, "event": "sprite upright, mesh upside down"}, {"at": 0.62, "event": "size line highlighted; mesh flips"}],
    "manim: a flipped icon", "A real upside-down mesh turning upright beside a sprite is the evidence the fix works.",
    f"C22: scene `flip` of {SCENES}: left Sprite2D of the blob at scale 2.0, right MeshInstance2D QuadMesh 256 x 256 with the same texture; at 0.6 of the beat mesh.size = Vector2(256, -256); canvas 1280 x 720; record the whole beat (D). Verified: eyes below the middle with +size.y, above it with -size.y, same as the sprite.",
    "verify1.gd 1b (mean eye row +6.8 with +y, -7.8 with -y, sprite -7.8)", title="When It Looks Wrong", code="mesh.size = Vector2(256, -256)", code_file="scene script (GDScript)",
    readouts=[{"at": 0.1, "text": "sprite", "x": 0.23, "y": 0.9}, {"at": 0.1, "text": "quad mesh", "x": 0.73, "y": 0.9}])
manim("B36", 4, "VERTEX means two things: corner in vertex, pixel on screen in fragment", "TwoMeanings",
      "A 1280 by 720 screen frame (outline) with a 128 px sprite square in its middle. The square's top left is ringed. Two labels on it in turn: 'in vertex(): (-64, -64), from the node's middle' and 'in fragment(): (576, 296), from the screen's top left'. Both name VERTEX in a monospace face. Small grey credit: 'measured in Godot 4.7.2 · Forward+'.",
      "The same corner gets two labels with two different pairs of numbers.",
      [{"at": 0.1, "event": "screen frame and sprite; corner ringed"}, {"at": 0.3, "event": "vertex() label and numbers"}, {"at": 0.7, "event": "fragment() label and numbers"}],
      "LectureEvidenceTable", "Two numberings of one spot are a picture of 'same word, different numbers'; a table would list them without showing where they are measured from.",
      "Lab 11/15 and 10/14 probes: vertex-stage corner = (-64, -64); fragment-stage first pixel of the sprite = about (576, 296) in a 1280 x 720 window")
lab("B37", 4, "move the node: one gradient travels, one stays on the screen", None, "vertex-shaders/vertex-two.mp4",
    "Godot 4.7.2 · Forward+ · both squares slide right by script", [],
    "Two real Godot squares stacked, each 256 px, both coloured blue to orange by the same last line. Top: colour from the corner position through a varying. Bottom: colour from VERTEX in fragment. Both slide to the right together: the top gradient moves with its square, the bottom square changes colour as it crosses a gradient that stays on the screen. Labels 'from vertex()' and 'from fragment()'.",
    "Both squares slide right; the top one keeps its colours, the bottom one's colours change.",
    [{"at": 0.1, "event": "two squares with labels"}, {"at": 0.35, "event": "slide starts"}, {"at": 0.75, "event": "top unchanged, bottom has changed colour"}],
    "manim: two squares and a ruler", "A move is the only way to show the difference between 'attached to the shape' and 'fixed to the screen'.",
    f"C23: scene `vertex-two` of {SCENES}: two Sprite2D white squares at scale 2.0 (top 15-position-from-vertex, bottom 14-position-from-fragment), canvas 1280 x 720; both slide from x 300 to x 1000 over 0.3 to 0.7 of the beat; 12 s. Verified: corner pixel red = 0.02 (top) against 0.45 (bottom) in both renderers.",
    "Lab 14/15-position-* (Forward+ and Compatibility agree)", layout="video",
    readouts=[{"at": 0.1, "text": "from vertex()", "x": 0.1, "y": 0.2}, {"at": 0.1, "text": "from fragment()", "x": 0.1, "y": 0.8}])
lab("B38", 4, "a Polygon2D has no UV without a texture", "06-flag-pinned.gdshader", "vertex-shaders/polygon-uv.mp4",
    "Godot 4.7.2 · Forward+ · live clock · the same shader on both, switched on at 10 % of the beat", [{"at": 0.1, "lines": [4]}],
    "Code card at left with the pinned flag line (it multiplies by `UV.x`) highlighted; at right two real Godot polygons with the same grid of points: on the left, no texture, a flat teal rectangle that does not wave at all; on the right, with a texture, a waving flag. Labels 'no texture' and 'with texture'. Caption in the GLOSSARY wording: 'texture: an image a shader can read'.",
    "The left polygon stays a still rectangle while the right one waves, under the same shader.",
    [{"at": 0.1, "event": "the UV.x factor highlighted"}, {"at": 0.4, "event": "left stays flat, right waves"}, {"at": 0.75, "event": "labels and caption"}],
    "manim: UV values on a polygon", "The same shader doing nothing on one polygon and waving on the other is the trap in one picture.",
    f"C24: scene `polygon-uv` of {SCENES}: two Polygon2D with a 33 x 9 grid of points and a cell list (polygons); left without a texture (colour teal), right with the checker texture and uv in texture pixels; 06-flag-pinned on both at 0.1 of the beat; canvas 1280 x 720; record the whole beat (D). Verified: UV reads 0 everywhere without a texture, even with uv set.",
    "verify7.gd 7 (UV (0, 0) everywhere without a texture)", caption="texture: an image a shader can read",
    readouts=[{"at": 0.4, "text": "no texture", "x": 0.27, "y": 0.9}, {"at": 0.4, "text": "with texture", "x": 0.73, "y": 0.9}])
lab("B39", 4, "a vertex shader changes the drawing, not the node", "16-slide-far.gdshader", "vertex-shaders/drawing-only.mp4",
    "Godot 4.7.2 · Apple M4 Pro · Forward+ · scripted: shader switched on at 30 % of the beat", [{"at": 0.3, "lines": [4]}],
    "Code card at left with `VERTEX.x += 200.0;` highlighted; at right a real Godot window with a thin grey outline marking the node's own rectangle (from get_rect()). The checker square starts inside it, then the picture slides 200 px to the right while the outline stays. Readouts 'rect unchanged' and 'collision unchanged'. Caption: 'collision shape: what physics collides with'.",
    "The picture slides away from its outline, which does not move.",
    [{"at": 0.3, "event": "slide line highlighted; picture slides away from the outline"}, {"at": 0.75, "event": "readouts: rect and collision unchanged"}],
    "manim: a node and a ghost picture", "The outline staying put while the picture leaves is the claim, and the numbers come from get_rect and an Area2D overlap test.",
    f"C25: scene `drawing-only` of {SCENES} (canvas 640 x 360): Sprite2D checker 128 px at scale 1.0 with a grey outline drawn from get_rect(); 16-slide-far assigned at 0.3 of the beat; record to the event plus 1.5 s, then hold. Verified: get_rect() = (-64, -64, 128, 128) before and after; an Area2D collision shape on the node overlaps the probe at the node's position and not the probe where the picture is drawn; the picture's left edge moves from x 156 to 356.",
    "verify9.gd 9a, 9b, 9c", caption="collision shape: what physics collides with",
    readouts=[{"at": 0.75, "text": "rect unchanged", "x": 0.3, "y": 0.9}, {"at": 0.75, "text": "collision unchanged", "x": 0.7, "y": 0.9}])
rem("B40", 4, "count the vertices: print the mesh's vertex array", "terminal", "CCPlainShell",
    {"title": "Godot output", "lines": ["print($Flag.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size())",
                                        "", "Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org",
                                        "Metal 4.0 - Forward+ - Using Device #0: Apple - Apple M4 Pro (Apple9)", "", "297"],
     "startCue": 0.1, "lineGap": 0.12, "durationSeconds": "__AUDIO__"},
    "A plain terminal on the cream stage: the one-line print statement, then the real output of running it in a node's _ready(): the engine banner and the number 297. Caption: 'Mesh.ARRAY_VERTEX: the list of vertex positions'.",
    "The line is typed and the number 297 lands last.",
    [{"at": 0.1, "event": "the print line"}, {"at": 0.4, "event": "banner lines"}, {"at": 0.72, "event": "297 lands"}],
    "ShaderLab", "The answer to 'how many vertices' is a number a real run printed; a terminal is the honest place for a printed number.",
    "verify10.gd (the line run in _ready() of a node with a MeshInstance2D named Flag: prints 297); logs/verify10.log")

# ───────────────────────────── write lanes + SHOTLIST ─────────────────────────────
(HERE / "lanes").mkdir(exist_ok=True)
acts = [(0, 10), (10, 20), (20, 26), (26, 34), (34, 40)]
for ai, (a, b) in enumerate(acts):
    chunk = {e["bid"]: e["entry"] for e in E[a:b]}
    (HERE / "lanes" / f"act{ai + 1}.json").write_text(json.dumps(chunk, indent=1, ensure_ascii=False) + "\n")

lanes_hist = {}
for e in E:
    lanes_hist[e["entry"]["lane"]] = lanes_hist.get(e["entry"]["lane"], 0) + 1
rows = []
for e in E:
    en = e["entry"]
    pick = f"{en['lane']} · {en.get('class') or en.get('pattern')}"
    rows.append(f"| {e['bid']} | {e['about']} | {pick} | {en['runner_up']} | {en['why']} | {e['evidence']} |")
sl = ["# Shot list: Vertex Shaders\n",
      "**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.\n",
      "**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.\n",
      f"**Found.** {len(E)} body beats. Lane histogram: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes_hist.items(), key=lambda kv: -kv[1])) +
      ". Every Godot picture shown is a Shader Lab render or a capture of a custom scene built in `evidence/planning-checks/scratch-project/capture_scenes.gd`, using a tested file in `lab-shaders/`. Nothing needs the Godot editor. Three things must be built or recorded first (below).\n",
      "## Must exist before the build\n",
      "1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file; this film also needs a vertex dot, a polyline through dots, a dot grid with a counter and a screen frame: see below). 3. **Capture harness** (`lab/capture.gd` + `capture_shader.sh`, same file) with a scene-script option that can load `evidence/planning-checks/scratch-project/capture_scenes.gd` (`build(id, parent, shader_dir, duration)` and `tick(ctx, t)`).\n",
      "**This film's `shader_kit` additions:** `vertex_dot(label)` (terracotta dot with a monospace label), `polyline_through(points)`, `dot_grid(cols, rows)` with `count_up(grid)`, `screen_frame(w, h)` (an outlined 16:9 frame with a node square inside), `sine_curve(samples)`. All in the Claude palette; terracotta only as dots and rings.\n",
      "## Rows\n",
      "| beat | about | lane picked | runner-up | why this one wins | evidence / capture |",
      "|---|---|---|---|---|---|"] + rows
(HERE / "SHOTLIST.md").write_text("\n".join(sl) + "\n")
print(len(E), "beats;", lanes_hist)
